"""Checks for specs/page.md. Run from the repo root: python3 -I tests/test_page.py"""
import json
import os
import re
import subprocess
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/"


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        return f.read()


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.metas = []
        self.links = []
        self.anchors = []
        self.ids = set()
        self.jsonld = []
        self.h1 = ""
        self.h2 = []
        self.body_text = ""
        self._stack = []
        self._cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self._stack.append(tag)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag == "a":
            self.anchors.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._cur = "jsonld"
            self.jsonld.append("")
        elif tag == "h2":
            self.h2.append("")

    def handle_endtag(self, tag):
        if tag in self._stack:
            while self._stack and self._stack.pop() != tag:
                pass
        if tag == "script":
            self._cur = None

    def handle_data(self, data):
        top = self._stack[-1] if self._stack else ""
        if top == "title":
            self.title += data
        elif top == "h1":
            self.h1 += data
        elif top == "h2":
            self.h2[-1] += data
        elif self._cur == "jsonld":
            self.jsonld[-1] += data
        if "body" in self._stack and top not in ("script", "style"):
            self.body_text += data

    def meta(self, key, value):
        for m in self.metas:
            if m.get(key) == value:
                return m.get("content", "")
        return None


def page():
    p = Page()
    p.feed(read("index.html"))
    return p


def persian(s):
    return bool(re.search(r"[؀-ۿ]", s))


class TestPage(unittest.TestCase):
    def test_title_is_descriptive_persian(self):
        p = page()
        t = p.title.strip()
        self.assertLessEqual(len(t), 70)
        self.assertIn("تقویم آسترولوژی", t)
        self.assertIn("طالع‌بینی", t)
        self.assertNotEqual(t, p.h1.strip())
        self.assertEqual(p.h1.strip(), "تقویم آسترولوژی")

    def test_meta_description_is_persian_and_70_160_chars(self):
        d = page().meta("name", "description")
        self.assertIsNotNone(d)
        self.assertTrue(persian(d))
        self.assertTrue(70 <= len(d) <= 160, len(d))
        self.assertIn("روزهای خوب و بد نجومی", d)

    def test_canonical_link_is_the_site_url(self):
        c = [l for l in page().links if l.get("rel") == "canonical"]
        self.assertEqual([l["href"] for l in c], [SITE])

    def test_open_graph_tags_complete(self):
        p = page()
        exp = {"og:type": "website", "og:url": SITE, "og:locale": "fa_IR"}
        for k, v in exp.items():
            self.assertEqual(p.meta("property", k), v, k)
        for k in ("og:title", "og:description", "og:image:alt", "og:site_name"):
            self.assertTrue(p.meta("property", k), k)
        self.assertEqual(p.meta("property", "og:image"), SITE + "og-image.png")
        self.assertEqual(p.meta("property", "og:title"), p.title.strip())
        self.assertEqual(p.meta("property", "og:description"), p.meta("name", "description"))

    def test_twitter_card_tags_complete(self):
        p = page()
        self.assertEqual(p.meta("name", "twitter:card"), "summary_large_image")
        for k in ("twitter:title", "twitter:description", "twitter:image"):
            self.assertTrue(p.meta("name", k), k)

    def test_og_image_file_exists_and_is_referenced(self):
        path = os.path.join(ROOT, "og-image.png")
        self.assertTrue(os.path.exists(path))
        self.assertLess(os.path.getsize(path), 300 * 1024)
        with open(path, "rb") as f:
            head = f.read(24)
        self.assertEqual(head[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(int.from_bytes(head[16:20], "big"), 1200)
        self.assertEqual(int.from_bytes(head[20:24], "big"), 630)
        self.assertIn(SITE + "og-image.png", read("index.html"))

    def test_json_ld_parses_and_has_required_fields(self):
        p = page()
        self.assertEqual(len(p.jsonld), 1)
        data = json.loads(p.jsonld[0])
        self.assertEqual(data["@context"], "https://schema.org")
        nodes = data["@graph"]
        types = {n["@type"]: n for n in nodes}
        site = types["WebSite"]
        self.assertTrue(site["name"])
        self.assertEqual(site["url"], SITE)
        self.assertEqual(site["inLanguage"], "fa")
        wp = types["WebPage"]
        self.assertEqual(
            set(wp["sameAs"]),
            {"https://t.me/FarsiHoroscopeCalendar", "https://t.me/FarsiHoroscope"},
        )
        self.assertNotIn("aggregateRating", json.dumps(data))
        self.assertNotIn("review", json.dumps(data).lower())

    def test_not_noindex(self):
        robots = page().meta("name", "robots")
        self.assertTrue(robots is None or "noindex" not in robots.lower())

    def test_about_section_visible_with_source_and_update_frequency(self):
        p = page()
        self.assertIn("درباره این تقویم", [h.strip() for h in p.h2])
        text = re.sub(r"\s+", " ", p.body_text)
        self.assertIn("@FarsiHoroscope", text)
        self.assertIn("۶ ساعت", text)
        self.assertIn("REFRESH-INTERVAL;VALUE=DURATION:PT6H", read("calendar.ics"))

    def test_links_to_both_telegram_channels_with_relation_text(self):
        p = page()
        for url in ("https://t.me/FarsiHoroscopeCalendar", "https://t.me/FarsiHoroscope"):
            links = [a for a in p.anchors if a.get("href") == url]
            self.assertTrue(links, url)
            self.assertTrue(all("noopener" in a.get("rel", "") for a in links), url)
        text = re.sub(r"\s+", " ", p.body_text)
        self.assertIn("کانال اصلی", text)
        self.assertIn("کانال تقویم", text)

    def test_verification_artifacts_match_owner_provided_tokens(self):
        # No tokens are provided yet, so none may be invented.
        names = os.listdir(ROOT)
        self.assertFalse([n for n in names if re.match(r"google[0-9a-f]+\.html$", n)])
        self.assertFalse([n for n in names if n == "BingSiteAuth.xml"])
        p = page()
        for k in ("google-site-verification", "msvalidate.01"):
            self.assertIsNone(p.meta("name", k))

    def test_subscribe_links_still_work(self):
        p = page()
        self.assertLessEqual({"apple", "google", "ics", "copy"}, p.ids)
        src = read("index.html")
        self.assertIn('new URL("calendar.ics", location.href)', src)
        self.assertIn("calendar.google.com/calendar/render?cid=", src)


class TestSitemap(unittest.TestCase):
    def test_valid_and_lists_site_url(self):
        root = ET.fromstring(read("sitemap.xml").encode("utf-8"))
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = [e.text.strip() for e in root.findall("s:url/s:loc", ns)]
        self.assertEqual(locs, [SITE])
        lastmod = root.find("s:url/s:lastmod", ns).text
        self.assertRegex(lastmod, r"^\d{4}-\d{2}-\d{2}$")
        self.assertNotIn("calendar.ics", read("sitemap.xml"))


class TestRobots(unittest.TestCase):
    def test_allows_crawling_and_names_sitemap(self):
        txt = read("robots.txt")
        self.assertRegex(txt, r"(?m)^User-agent: \*$")
        self.assertNotRegex(txt, r"(?m)^Disallow:\s*/\s*$")
        self.assertIn("Sitemap: " + SITE + "sitemap.xml", txt)


class TestDocs(unittest.TestCase):
    def test_search_setup_steps_cover_google_bing_and_sitemap(self):
        d = read("docs/search-setup.md")
        for s in ("Google Search Console", "Bing Webmaster Tools", "sitemap.xml", SITE, "@FarsiHoroscope"):
            self.assertIn(s, d)
        self.assertRegex(d, r"(?m)^1\. ")


class TestRepo(unittest.TestCase):
    def test_no_build_files_and_calendar_ics_untouched(self):
        for n in ("package.json", "CNAME", "Makefile", "requirements.txt"):
            self.assertFalse(os.path.exists(os.path.join(ROOT, n)), n)
        self.assertFalse(os.path.exists(os.path.join(ROOT, ".github", "workflows")))
        r = subprocess.run(
            ["git", "diff", "--quiet", "HEAD", "--", "calendar.ics"], cwd=ROOT
        )
        self.assertEqual(r.returncode, 0, "calendar.ics has local changes")


if __name__ == "__main__":
    unittest.main()
