# Dharma Path

A free, open guide to Hinduism for modern life: a Hindu calendar with real dates, prayers for every moment of the day, the great scriptures and short courses. It works offline on any phone or computer.

## Features

| Tab | What it offers |
| --- | --- |
| **Today** | The Hindu date (tithi, month, Vikram Samvat), what is observed today and tomorrow, a Bhagavad Gita verse of the day (shareable as an image), a month calendar with upcoming festivals, a prayer suggested for the time of day, your practice streak, books in progress and a daily reflection |
| **Calendar** | Month view of festivals and vrats (Ekadashi, Purnima, Amavasya, Sankashti, Pradosh, Shivaratri) for 2026–2028, a page for every day with its meaning and prayers, festival guides, and a choice of 18 cities |
| **Puja** | 70 prayers grouped as mantras, shlokas, stotras, aartis, chalisas and bhajans, filterable by deity and by moment (waking, meals, study, travel, sleep…). Suggestions change with the time of day, weekday and today's festival. Every prayer can be heard chanted, verse by verse, and the 108-bead japa counter has a "chant along" mode that chants the mantra and counts each repetition, with an optional tanpura drone. **Aarti mode** shows one verse at a time in large type on a dark screen for the whole family, repeats the refrain after each verse and can turn the pages itself while it chants. Any prayer can be **recorded in your own voice**, and that recording then plays instead of the device voice |
| **Read** | The Bhagavad Gita, Rig Veda (selected hymns), Sama Veda, Upanishads, Ramayana, Mahabharata, Vishnu Purana and Yoga Sutras, with Sanskrit where available. Your place in each book is saved automatically. Tap any verse to bookmark it, highlight it, write a note, copy it or share it as an image |
| **Learn** | 18 illustrated courses with 96 lessons on philosophy, deities, scripture, practice, temples and pilgrimage. Each lesson has its own page with an original illustration, key terms, a short practice and links to the prayers and scriptures it mentions, and completed lessons count toward your practice. **Rites of passage**: 14 illustrated guides to the samskaras, set out as a journey of life from the blessing of the mother-to-be to remembering the ancestors. Each guide has when, where and who at a glance, the meaning, a checklist of what you'll need, every step (the wedding in three phases), customs across regions including the Caribbean, notes for working with a priest and for families abroad, and the prayers to use |

Across the app:

- **Search** (top bar) finds prayers, festivals, lessons and words in every scripture. Spellings with or without diacritics both match, so "Krishna" finds "Kṛṣṇa". The Ramayana and Mahabharata are searched on request because of their size.
- **Your practice** keeps a private record of mantras and malas chanted, chapters read, aartis sung and lessons finished, with a daily streak, a 12-week view and simple check-ins (prayed, meditated, fasted…).
- **Backup and restore** saves everything the app keeps on the device (bookmarks, highlights and notes, practice history, japa counts, favourites, finished lessons, reading places, rite checklists, reminder choices, settings and, if chosen, your recordings) to one file, and restores it on any device, either added to what is there or replacing it.
- **Reminders** cover festivals, Ekadashi, moon days and vrats, the evening before or the same morning, plus an optional daily prayer reminder. They can be added to the phone's own calendar as an `.ics` file for exact alerts, and on browsers that allow it the app can show its own notices.

It also has dark mode and works offline as an installable PWA. It needs no account, sends no tracking, and saves progress only on the user's own device, which can be backed up to a file. Planned work is listed in [ROADMAP.md](ROADMAP.md).

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

Content lives in two files. To add more, append an object to the relevant array:

- [`js/content.js`](js/content.js)
  - `wisdom`: daily verses (one is chosen per day of the year)
  - `gitaDaily`: Bhagavad Gita verses for the verse of the day
  - `festivals`: festival guides; the `id` must match the calendar's festival ids
  - `vrats`, `weekdays`: text for recurring observances and each weekday's deity
  - `courses`, `lifeEvents`: Academy courses and rites of passage
- [`js/prayers.js`](js/prayers.js): prayers, each with a type, deity, moments and verses (`[devanagari, romanisation, english, label?]`)
- [`js/rites.js`](js/rites.js): the rites of passage, grouped into stages of life. Each rite has `when`, `where`, `who`, `length`, `summary`, an HTML `intro`, a `need` checklist, `steps` (or `phases` of steps), `customs`, `withPriest`, `abroad`, an optional `verse` and `prayers`.
- [`js/academy.js`](js/academy.js): the Academy courses. Each lesson has a `title`, an `art` illustration, an optional `caption`, an HTML `body`, and optional `terms`, `practice` and `links`. Reading time is worked out from the text.
- [`img/learn/`](img/learn/): the lesson paintings as WebP. A lesson's `art` is the file name without its extension; it can also be a full path to another image (for example `img/learn/varanasi.jpg`).
- [`scripts/art/`](scripts/art/): the code that paints them. Every painting is generated procedurally, with no traced or downloaded imagery; see [its README](scripts/art/README.md).

When you change files, increase `CACHE` in `sw.js` (for example `dharma-path-v9`) so installed apps pick up the update.

## Audio

Prayers are chanted by the phone's built-in Hindi voice (Web Speech API), reading the Devanagari. Phones without a Hindi voice hear the romanised words read in English. The tanpura drone is synthesised in the browser with the Web Audio API, so it needs no audio files.

Recordings take priority. The prayers are chanted verse by verse from clips made with ElevenLabs text to speech by `scripts/build_audio.py`, so the verse being chanted is highlighted as it plays. Anyone can also record a prayer in the app (stored on their device in IndexedDB) and share the file, and a recording can be published for everyone by adding it to `audio/` and listing it in `audio/index.json`. See [`audio/README.md`](audio/README.md). The order is: the person's own recording, then a published one, then the device voice.

## Calendar

`calendar/` is generated by `scripts/build_calendar.py`, which computes the panchang with the Swiss Ephemeris:

```sh
pip install pyswisseph
python3 scripts/build_calendar.py 2026 2028
```

Each tithi is reckoned from local sunrise, so dates are calculated separately for each city. Months are amanta and named by the sidereal (Lahiri) sign of the sun at the new moon, with adhika (leap) months detected automatically. Each festival is placed on the day its tithi covers the traditional time of worship: sunrise, forenoon, midday, afternoon, evening (pradosh), midnight (nishita) or moonrise. Raksha Bandhan avoids Bhadra, and Janmashtami lists the ISKCON/Vaishnava date when it differs. The results were checked against published panchang dates for 2026 and 2027. Some communities and temples follow regional rules and may observe a day earlier or later.

To add a city, add it to `CITIES` in the script and run it again.

## Scriptures

The texts in `texts/` are generated from public-domain and openly licensed sources by the scripts in `scripts/`:

| Book | English translation | Sanskrit |
| --- | --- | --- |
| Bhagavad Gita | Annie Besant, 4th ed. (1922), all 701 verses | gita/gita open dataset |
| Rig Veda | Ralph T. H. Griffith (1896), all 1,028 hymns, from Wikisource; ten selected hymns translated for Dharma Path | Vedic Heritage Portal, via DharmicData (ODbL) |
| Sama Veda | Ralph T. H. Griffith (1895), all 1,794 verses, via DharmicData | — |
| Yajur Veda | Ralph T. H. Griffith, *The Texts of the White Yajurveda* (1899), all 40 books, cleaned from two archive.org scans | DharmicData |
| Atharva Veda | Ralph T. H. Griffith (1895–96), all 20 books, cleaned from two archive.org scans | DharmicData |
| Upanishads | Swami Paramananda (1919): Isha, Katha, Kena; F. Max Müller (1879, 1884): Prasna, Mundaka, Taittiriya, Aitareya, Chandogya, Brihadaranyaka, Svetasvatara; R. E. Hume (1921): Mandukya | — |
| Ramayana | Manmatha Nath Dutt (1891–94), about 15,000 verses across all 7 kandas | Critical edition e-text |
| Mahabharata | Kisari Mohan Ganguli (1883–96), complete, all 18 parvas | — |
| Vishnu Purana | Manmatha Nath Dutt after H. H. Wilson, all 6 books | — |
| Garuda Purana | Ernest Wood and S. V. Subrahmanyam (1911), the Saroddhara | — |
| Devi Bhagavatam | Swami Vijnanananda (1921–23), complete, with his notes | — |
| Bhagavata, Shiva, Linga, Skanda, Narada, Padma, Brahma, Brahmanda, Bhavishya, Kurma, Vamana and Varaha Puranas | none yet | GRETIL (CC BY-NC-SA 4.0); the Padma, Bhavishya and Varaha from Sanskrit Wikisource (CC BY-SA) |
| Yoga Sutras | Charles Johnston (1912), all 4 books, with his commentary | — |

The Gita and Ramayana verse pairings come from the open-source [Katha](https://github.com/radhepa/Katha) project. Ganguli's text comes from [sacred-texts.com](https://sacred-texts.com/hin/maha/) via [rahulnyk/mahabharata](https://github.com/rahulnyk/mahabharata). The Vishnu Purana is Project Gutenberg #66208 as prepared by [Tattvika (Kathaveda)](https://github.com/jagdishak-hub/Kathaveda); the Vedic Sanskrit and the Sama Veda come from [DharmicData](https://github.com/bhavykhatri/DharmicData); the Paramananda Upanishads and the Yoga Sutras are Project Gutenberg #3283 and #2526 via [GITenberg](https://github.com/GITenberg). Ramayana verses that could not be matched reliably to the Sanskrit are left out, so its verse numbers sometimes skip.

The Sanskrit-only Puranas come from [GRETIL](https://gretil.sub.uni-goettingen.de/), the Göttingen Register of Electronic Texts in Indian Languages, under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 licence, and the Padma, Bhavishya and Varaha Puranas from [Sanskrit Wikisource](https://sa.wikisource.org/) under CC BY-SA; the files made from them in `texts/` are shared under the same terms. The Puranas with free English translations (Markandeya, Brahma Vaivarta, Matsya, Agni) are being prepared from scans.

The mantras of the rites of passage (`js/rite-mantras.js`) follow the ritual manuals, the Grihya Sutras, in the order each rite is performed: chiefly the Paraskara Grihya Sutra of the White Yajurveda, with Katyayana's supplements on shraddha and tarpana, from [Sanskrit Wikisource](https://sa.wikisource.org/) (CC BY-SA), and the Ashvalayana Grihya Sutra for the funeral, from GRETIL (CC BY-NC-SA 4.0), with the Vedic verses they quote taken from the samhitas in `texts/`. Each mantra's Sanskrit was checked against its source; Hermann Oldenberg's translation of the Grihya Sutras (*Sacred Books of the East* 29–30, 1886–92) was used to place the verses, and the English is our own. Rites with no chapter in the Grihya Sutras, such as Vidyarambha and Shashtipurti, use Vedic prayers that priests commonly choose for them.

To rebuild:

```sh
pip install indic-transliteration wordfreq
git clone --depth 1 https://github.com/radhepa/Katha /tmp/katha
git clone --depth 1 https://github.com/rahulnyk/mahabharata /tmp/mbh
git clone --depth 1 https://github.com/jagdishak-hub/Kathaveda /tmp/kathaveda
git clone --depth 1 https://github.com/bhavykhatri/DharmicData /tmp/dharmic
git clone --depth 1 https://github.com/GITenberg/The-Upanishads_3283 /tmp/upanishads
git clone --depth 1 https://github.com/GITenberg/The-Yoga-Sutras-of-Patanjali--The-Book-of-the-Spiritual-Man_2526 /tmp/yoga
cat /tmp/kathaveda/data/extra-parts/gutenberg-sources/part-* > /tmp/gutenberg-sources.json.gz

python3 scripts/build_texts.py /tmp/katha/assets/data /tmp/mbh/text/KMGanguli
python3 scripts/build_more_texts.py /tmp/gutenberg-sources.json.gz /tmp/dharmic /tmp/upanishads/3283.txt /tmp/yoga/2526.txt
```

The later books are built by their own scripts, each of which explains in its header where its sources come from and how to fetch them:

- `scripts/build_vedas.py`: the complete Rig Veda, from Griffith's hymns on Wikisource and DharmicData.
- `scripts/build_yajurveda.py` and `scripts/build_atharvaveda.py`: Griffith's Yajur and Atharva Vedas, from two archive.org scans of each book, corrected against each other and paired with DharmicData.
- `scripts/build_upanishads.py` (with `scripts/upanishads_sbe15.py`): the Upanishads from Müller's and Hume's translations.
- `scripts/build_puranas.py`: the Garuda Purana and the Devi Bhagavatam, from archive.org.
- `scripts/build_sanskrit_puranas.py`: the Sanskrit-only Puranas, from GRETIL and Sanskrit Wikisource.
- `scripts/build_wikisource_puranas.py`: the Padma and Bhavishya Puranas, from Sanskrit Wikisource.

The Rig Veda hymn selection and its English translations live in `scripts/rigveda_hymns.py`.

## Content notes

All explanations and lessons, and the translations of the prayers and daily wisdom, are original writing for this project, and the lesson paintings are original works generated by the code in `scripts/art`. The prayers themselves are traditional texts in the public domain; their Devanagari was checked against an independent transcription where one was available. The scripture translations are the public-domain editions listed above, except the Rig Veda selection, which was translated for this project. Texts cleaned from scans were checked by reading, but a scanning error can remain here and there.
