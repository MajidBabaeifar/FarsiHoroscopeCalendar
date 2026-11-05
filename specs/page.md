# Page: findable in Persian search

Status: Live: PAGE-1..12

The calendar page at `https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/` (`index.html`, called "the page" below) is a single static page on GitHub Pages with no build step. These requirements make it findable by people searching in Persian and link it with the two Telegram channels. All are Draft until the code PR builds them.

Site address used below: `https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/` ("the site URL").

### PAGE-1 · Descriptive title

The page's title says in Persian that this is an astrology (horoscope) calendar you can subscribe to.

- `<title>` contains «تقویم آسترولوژی» and «تقویم طالع‌بینی», is at most 70 characters, and differs from the `<h1>`.
- The `<h1>` stays «تقویم آسترولوژی».
- Verified by: `page: title is descriptive Persian`

### PAGE-2 · Search description

The page has a short Persian description that search engines can show under the title.

- `<meta name="description">` in Persian, 70–160 characters, mentions good and challenging astrological days («روزهای خوب و بد نجومی»), phone calendar subscription, and the Telegram source.
- Verified by: `page: meta description is Persian and 70-160 chars`

### PAGE-3 · Canonical address

The page tells search engines its one official address.

- `<link rel="canonical" href="https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/">`, with the trailing slash; it is the only canonical link.
- Verified by: `page: canonical link is the site URL`

### PAGE-4 · Link-preview tags

A shared link to the page shows a title, text and image in Telegram and other apps.

- Open Graph: `og:type` = `website`, `og:url` = site URL, `og:title`, `og:description`, `og:image` (absolute URL of the PAGE-5 image), `og:image:alt`, `og:locale` = `fa_IR`, `og:site_name`.
- `twitter:card` = `summary_large_image`, plus `twitter:title`, `twitter:description`, `twitter:image`.
- Title and description repeat PAGE-1 and PAGE-2 text.
- Verified by: `page: open graph tags complete`, `page: twitter card tags complete`

### PAGE-5 · Preview image

A preview image file ships in the repo next to the page, so the link preview has a picture.

- `og-image.png`, 1200×630, under 300 KB, served at the site URL plus `og-image.png`; contains the Persian page name.
- Verified by: `page: og image file exists and is referenced`

### PAGE-6 · Structured data

Search engines get a machine-readable description of the page and the calendar.

- One `<script type="application/ld+json">` that parses as JSON, with `@context` = `https://schema.org`, a `WebSite` (name, url, `inLanguage` = `fa`) and a `WebPage` describing the calendar, with `sameAs` listing `https://t.me/FarsiHoroscopeCalendar` and `https://t.me/FarsiHoroscope`.
- Contains no claims that are not visible on the page (no ratings, no reviews).
- Verified by: `page: json-ld parses and has required fields`

### PAGE-7 · Sitemap and robots

Search engines can find a sitemap, and nothing blocks them.

- `sitemap.xml` is a valid sitemap listing only the site URL, with `lastmod` set to the build date of the page.
- `robots.txt` allows all crawling and has `Sitemap: https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/sitemap.xml`.
- The page has no `noindex` robots meta tag.
- `calendar.ics` is not listed in the sitemap.
- Verified by: `sitemap: valid and lists site URL`, `robots: allows crawling and names sitemap`, `page: not noindex`

### PAGE-8 · Visible explanation

A short visible text on the page says what the calendar is, where its dates come from and how often it updates.

- A section with an `<h2>` in Persian, in the page body (not hidden or collapsed), of 2–4 sentences.
- States: the calendar shows astrologically good, challenging and neutral days; dates come from the Telegram channel @FarsiHoroscope; subscribed calendars refresh on their own, and the feed asks apps to check every 6 hours (matches `REFRESH-INTERVAL` in `calendar.ics`).
- The existing legend and subscribe cards stay.
- Verified by: `page: about section visible with source and update frequency`

### PAGE-9 · Channel links

The page links to both Telegram channels and says how they relate.

- A visible link to `https://t.me/FarsiHoroscopeCalendar` (the calendar's own channel) and a visible link to `https://t.me/FarsiHoroscope` (the original channel the dates come from), each with Persian text saying which is which; both `rel="noopener"`.
- The plain-text mention of @FarsiHoroscope in the intro becomes a link.
- The page does not claim endorsement by the original channel's owner.
- Verified by: `page: links to both telegram channels with relation text`

### PAGE-10 · Search-engine verification files

Google Search Console and Bing Webmaster Tools can verify ownership from files or tags in the repo.

- Verification is by static file or `<meta>` tag only, committed at the site root; the exact token values come from the owner (PAGE-11) and are not invented. Until provided, none is added.
- Verification files are not listed in the sitemap.
- Verified by: `page: verification artifacts match owner-provided tokens` (passes with none present)

### PAGE-11 · Owner setup steps

The steps only the owner can do are written down.

- `docs/search-setup.md` lists, in order: sign in to Google Search Console and add the site URL as a URL-prefix property; copy the HTML tag or file it gives; commit it (or give it to the agent); press Verify; submit `sitemap.xml`; repeat for Bing Webmaster Tools (importing from Search Console is acceptable); optionally ask the owner of @FarsiHoroscope to link to the page.
- Written in English, short numbered steps, with the exact URLs to use.
- Verified by: `docs: search setup steps cover google, bing and sitemap`

### PAGE-12 · Stays static and bot-safe

The page stays one static file on GitHub Pages, and the calendar bot is not disturbed.

- No build step, package manager, or script dependency is added; new files are static assets next to `index.html`.
- Nothing in the change edits `calendar.ics`, and no workflow is added that writes to `main`.
- The page's subscribe behaviour (Apple, Google, copy URL) is unchanged.
- No subdomain or custom domain is introduced (no `CNAME` file).
- Verified by: `repo: no build files and calendar.ics untouched`, `page: subscribe links still work`
