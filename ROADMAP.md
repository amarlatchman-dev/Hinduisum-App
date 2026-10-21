# Dharma Path roadmap

Ideas agreed for the app, roughly in the order we plan to do them. Tick them off as they ship.

## Next up

- [x] **Backup and restore**: save everything kept on the device (bookmarks, notes, highlights, practice
      history, japa counts, favourites, reading places, reminders, settings and your own recordings) to one
      file, and restore it on any device.
- [x] **Plain transliteration**: a switch to show "Om Namah Shivaya" instead of "oṃ namaḥ śivāya", for
      readers who find diacritics hard.
- [x] **Sanskrit for the Upanishads**: the Upanishads are in English only; add the Devanagari and IAST
      (GRETIL has the texts).
- [ ] **The Ramcharitmanas**, and the Sundar Kand on its own: Tulsidas's Awadhi with F. S. Growse's
      public-domain English (1883). For many diaspora families this is the scripture they sing. The
      DharmicData set already used for the Vedas has the Ramcharitmanas text.
      **Done:** the Awadhi text with transliteration, all seven kands and the Sundar Kand on its own.
      **Still to do:** Growse's English, matched doha by doha (his scan marks each doha); the closing
      passage of six kands, missing from DharmicData (Hindi Wikisource has it, once hi.wikisource.org is allowed).
- [x] **Dates by tithi for loved ones**: enter the date someone passed away and get their yearly
      shraddha tithi and their day in Pitru Paksha; birthdays by Hindu tithi too. The city calendars
      already hold the tithis.

## Daily practice

- [x] **Daily timings**: Rahu Kalam, Yamaganda, Gulika, Abhijit and Brahma muhurta, the time each tithi
      ends, and the Ekadashi parana (fast-breaking) window, on each day page and the Today page.
- [x] **Rite booklets and follow-along mode**: print or save a rite (above all the wedding) as a programme
      with each step and mantra for guests, and a big-text mode that shows one mantra at a time during the
      ceremony, like Aarti mode.
- [ ] **Recorded audio**: finish the ElevenLabs prayer recordings (16 prayers left), then the 141 rite
      mantras (about 13,000 characters, more than one month's free quota).
- [x] **Listen to any book with the device voice**: a Listen button in the reader that reads verse by
      verse, highlights each one and carries on into the next chapter, in English and (where the phone
      has a Hindi voice) Sanskrit. Free, works offline, about a day's work.
- [ ] **Recorded readings of the most-read texts** with ElevenLabs: the Bhagavad Gita (about 160,000
      characters, Sanskrit and English), then the Sundar Kand and the key Upanishads. One or two months of a
      paid plan rather than years of the free quota. Recording every book (about 43 million characters,
      roughly 800 hours and 20–25 GB of audio) would need paid hosting and is not planned.
- [ ] Link public-domain human readings where they exist (e.g. LibriVox English readings of the Gita and
      Upanishads; Sanskrit chanting on archive.org once each licence is checked).
- [ ] Notes on each rite page where the old manuals differ from today's custom (e.g. three rounds of the
      fire in Paraskara; the meaning of the seven steps).

## Texts

- [ ] **English Puranas**: Markandeya (with the Devi Mahatmya), Brahma Vaivarta, Matsya and Agni, cleaned
      from archive.org scans.
- [ ] Partial English for the Bhagavata Purana (M. N. Dutt).
- [ ] **Tamil texts** for South Indian diaspora families: the Tirukkural and the Thiruvasagam in
      G. U. Pope's public-domain translations.
- [ ] Popular verses not yet confirmed from a source (the mangalsutra verse, the modern kanyadan formula,
      "kṛtvā tu duṣkaraṃ karma", "Om namah siddham"): add them once checked against a printed paddhati.

## Caribbean and community

- [ ] Guides for **Jhandi puja**, **Phagwah chowtal**, **Ramleela**, **Kartik snan** and the matikor songs.
- [ ] A **Dutch or Sarnami** interface for Suriname.
- [ ] A **mandir finder** for each city (needs a list someone keeps up to date).

## Learning

- [ ] **Quizzes** at the end of each course.
- [ ] **Gita memorisation** with spaced repetition.
- [ ] **Reading plans**, such as "the Gita in 18 days" or "the Sundar Kand on Tuesdays".
- [ ] **Children's stories** from the Panchatantra and Hitopadesha, illustrated in the app's painting style.

## Quality and reach

- [ ] A **"report a mistake"** button on every verse and mantra.
- [ ] Review of the rite mantras by a pandit.
- [ ] **Automated tests and CI** on GitHub (the browser checks now run only in development sessions).
- [ ] A **Google Play** listing, by wrapping the web app (the App Store is possible but harder).
- [ ] Simple, **privacy-friendly usage counts**.
- [ ] **Sync between devices** (needs a server; backup and restore covers moving phones until then).
- [ ] Optional **"ask about this verse"**, answered only from the app's own texts with their sources
      (needs a small server and has running costs).
