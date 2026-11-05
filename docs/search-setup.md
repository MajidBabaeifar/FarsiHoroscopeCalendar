# Search setup (owner steps)

These steps need your Google and Microsoft accounts, so they can't be done from the repo. The site URL is `https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/`. No verification token is committed yet; the repo only gets one after you send it.

## Google Search Console

1. Go to https://search.google.com/search-console and sign in.
2. Add a property of type "URL prefix" with `https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/`.
3. Choose the "HTML tag" method (or "HTML file") and copy what Google shows.
4. Send it to the agent or commit it yourself: the `<meta name="google-site-verification" ...>` tag goes in the `<head>` of `index.html`; a file goes next to `index.html` at the repo root.
5. After it is live on GitHub Pages, press Verify.
6. Open Sitemaps, enter `sitemap.xml` and press Submit.

## Bing Webmaster Tools

1. Go to https://www.bing.com/webmasters and sign in.
2. Either import the site from Google Search Console (easiest), or add the site URL and choose the HTML meta tag or `BingSiteAuth.xml` file method, commit it as in step 4 above, and press Verify.
3. Open Sitemaps and submit `https://majidbabaeifar.github.io/FarsiHoroscopeCalendar/sitemap.xml`.

## Optional: a link from the original channel

1. Ask the owner of @FarsiHoroscope (https://t.me/FarsiHoroscope) to link to the page. Only they can decide that.
