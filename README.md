# Dharma Path

A free, open guide to Hinduism for modern life. It offers daily wisdom, structured courses, festivals, life rituals and prayers, and it works offline on any phone or computer.

## Features

| Tab | What it offers |
| --- | --- |
| **Today** | A daily verse with a reflection, the prayer of the day, upcoming festivals and courses in progress |
| **Academy** | Short courses on philosophy, deities, scripture, practice and temples, with progress tracking |
| **Festivals** | Major festivals by month, with their meaning, traditions and how to celebrate at home |
| **Life Events** | The samskaras (birth, naming, wedding, housewarming, last rites and more) with step-by-step guidance |
| **Puja** | Prayers and mantras in Devanagari with transliteration and meaning, favourites, read-aloud and a 108-bead japa counter |

It also has dark mode and works offline as an installable PWA. It needs no account, sends no tracking, and saves progress only on the user's own device.

## Run it

It is plain HTML, CSS and JavaScript with no build step.

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

Opening `index.html` directly also works, but offline caching needs a server.

## Deploy for free

The app is fully static, so you can host it on GitHub Pages (Settings → Pages → deploy from branch), Netlify or Cloudflare Pages. On a phone, open the site and choose **Add to Home Screen** to install it like an app.

## Adding content

All content is in [`js/content.js`](js/content.js). To add more, append an object to the relevant array:

- `wisdom`: daily verses (one is chosen per day of the year)
- `courses`: Academy courses, each with `lessons` (lesson bodies may contain simple HTML)
- `festivals`: `month` is the typical Gregorian month, used for sorting
- `lifeEvents`: rites with `steps`
- `prayers`: Sanskrit, transliteration and meaning

When you change files, increase `CACHE` in `sw.js` (for example `dharma-path-v2`) so installed apps pick up the update.

## Content notes

All explanations are original writing for this project. Sanskrit verses come from public-domain scripture, and the translations are our own. Festival dates follow the lunar calendar and vary by year and region, so the app shows the traditional timing rather than fixed dates.
