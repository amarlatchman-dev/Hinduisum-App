/*
 * Dharma Path content.
 * All text here is original writing for this app. Sanskrit verses are public-domain
 * scripture; transliterations and translations are our own.
 * To add content, append objects to the arrays below. No build step is needed.
 */
window.CONTENT = {
  /* ------------------------------------------------------------------ */
  /* Daily wisdom: one per day, rotates by day of year                   */
  /* ------------------------------------------------------------------ */
  wisdom: [
    {
      text: "You have a right to your actions, but never to their fruits. Act without craving results, and without clinging to inaction.",
      source: "Bhagavad Gita 2.47",
      reflection: "Do today's work well for its own sake. Let go of anxiety about outcomes you cannot control."
    },
    {
      text: "Lead me from the unreal to the real, from darkness to light, from death to immortality.",
      source: "Brihadaranyaka Upanishad 1.3.28",
      reflection: "Notice one place where you are living by habit rather than truth, and bring a little light to it."
    },
    {
      text: "Truth is one; the wise call it by many names.",
      source: "Rig Veda 1.164.46",
      reflection: "Look for the common ground in a view that differs from your own."
    },
    {
      text: "The Self is never born, nor does it ever die. Unborn, eternal and ancient, it is not slain when the body is slain.",
      source: "Bhagavad Gita 2.20",
      reflection: "Behind every changing mood is an unchanging witness. Rest as that witness for a few breaths."
    },
    {
      text: "Whatever you do, whatever you eat, whatever you offer or give away, whatever discipline you keep — do it as an offering to Me.",
      source: "Bhagavad Gita 9.27",
      reflection: "Turn one ordinary task today, such as cooking or commuting, into a quiet offering."
    },
    {
      text: "As a person puts on new clothes and discards the old, the embodied Self takes on new bodies and leaves the worn-out ones.",
      source: "Bhagavad Gita 2.22",
      reflection: "Change is natural. What in your life is ready to be released?"
    },
    {
      text: "Arise, awake, and learn by approaching the wise. The path is as sharp as a razor's edge, hard to cross.",
      source: "Katha Upanishad 1.3.14",
      reflection: "Seek out one teacher, book or conversation that stretches your understanding."
    },
    {
      text: "One who sees Me in everything, and everything in Me, is never lost to Me, nor am I ever lost to them.",
      source: "Bhagavad Gita 6.30",
      reflection: "Practise seeing the sacred in the next person you meet."
    },
    {
      text: "That is whole, this is whole. From wholeness comes wholeness. Take wholeness from wholeness, and wholeness remains.",
      source: "Isha Upanishad, invocation",
      reflection: "You are already complete. Act today from fullness rather than lack."
    },
    {
      text: "The mind alone is the cause of bondage and liberation.",
      source: "Amritabindu Upanishad 2",
      reflection: "Watch where your attention goes. Guide it gently, like a calf to its mother."
    },
    {
      text: "Better is one's own dharma, though imperfectly done, than the dharma of another well performed.",
      source: "Bhagavad Gita 3.35",
      reflection: "Stop comparing your path to someone else's. What is yours to do?"
    },
    {
      text: "Non-violence is the highest dharma.",
      source: "Mahabharata, Anushasana Parva",
      reflection: "Choose gentleness in speech today, especially when you feel provoked."
    },
    {
      text: "When meditation is mastered, the mind is unwavering like the flame of a lamp in a windless place.",
      source: "Bhagavad Gita 6.19",
      reflection: "Sit for five minutes and simply watch the breath."
    },
    {
      text: "You are That.",
      source: "Chandogya Upanishad 6.8.7",
      reflection: "The reality you seek outside is the reality you are."
    }
  ],

  /* ------------------------------------------------------------------ */
  /* Gita verse of the day: [chapter, verse] refs, rotated by day        */
  /* ------------------------------------------------------------------ */
  gitaDaily: [
    [2, 13], [2, 14], [2, 20], [2, 22], [2, 23], [2, 47], [2, 48], [2, 50], [2, 56], [2, 62],
    [2, 63], [2, 70], [3, 8], [3, 19], [3, 21], [3, 27], [3, 35], [4, 7], [4, 8], [4, 18],
    [4, 38], [4, 39], [5, 10], [5, 18], [6, 5], [6, 6], [6, 17], [6, 19], [6, 26], [6, 30],
    [6, 35], [7, 7], [7, 19], [8, 5], [9, 22], [9, 26], [9, 27], [9, 29], [10, 8], [10, 20],
    [12, 13], [12, 14], [12, 15], [13, 27], [15, 7], [15, 15], [16, 1], [16, 21], [17, 15], [17, 20],
    [18, 46], [18, 47], [18, 63], [18, 65], [18, 66], [18, 78]
  ],

  /* ------------------------------------------------------------------ */
  /* Scripture library (texts are in /texts, built by scripts/build_texts.py) */
  /* ------------------------------------------------------------------ */
  bookCategories: [
    { id: "gita", name: "Bhagavad Gita" },
    { id: "veda", name: "The Vedas" },
    { id: "upanishad", name: "Upanishads" },
    { id: "itihasa", name: "The epics" },
    { id: "purana", name: "Puranas" },
    { id: "darshana", name: "Yoga and philosophy" }
  ],

  books: [
    {
      id: "gita",
      title: "Bhagavad Gita",
      sanskritTitle: "भगवद्गीता",
      tagline: "Krishna's teaching to Arjuna · 18 chapters, 701 verses",
      partLabel: "Chapter",
      sectionLabel: null,
      verses: true,
      sanskrit: true,
      category: "gita",
      glyph: "🪷",
      gradient: "g1",
      translation: "English by Annie Besant (1922). Sanskrit with transliteration.",
      about: "The Bhagavad Gita is a 700-verse dialogue set on the battlefield of Kurukshetra, part of the Mahabharata's Bhishma Parva. Krishna counsels the warrior Arjuna on duty, the Self and the paths of action, knowledge and devotion."
    },
    {
      id: "ramayana",
      title: "Ramayana",
      sanskritTitle: "रामायण",
      tagline: "Valmiki's epic of Rama · 7 kandas",
      partLabel: "Kanda",
      sectionLabel: "Sarga",
      verses: true,
      sanskrit: true,
      category: "itihasa",
      glyph: "🏹",
      gradient: "g3",
      translation: "English by Manmatha Nath Dutt (1891–94), verse by verse with the Sanskrit critical edition. Verses that could not be matched reliably are omitted.",
      about: "Attributed to the sage Valmiki, the Ramayana tells of Prince Rama's exile, the abduction of Sita by Ravana, her rescue with the help of Hanuman, and Rama's return to Ayodhya."
    },
    {
      id: "ramcharitmanas",
      title: "Ramcharitmanas",
      sanskritTitle: "रामचरितमानस",
      tagline: "Tulsidas's Ramayan · 7 kands · Awadhi",
      partLabel: "Kand",
      sectionLabel: "Doha",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "itihasa",
      translation: "Tulsidas's Awadhi, from the IIT Kanpur Ramcharitmanas project via DharmicData, with a transliteration that drops the silent final a, as the Manas is sung. The closing passage of each kand from the Ayodhya Kand on is missing from the source and will be added; F. S. Growse's English translation (1883) is being prepared.",
      about: "The Ramayan of the poet-saint Tulsidas (1574), retold in Awadhi for everyone, and the scripture most sung in Hindu homes and mandirs across North India and the diaspora. Its chaupais and dohas tell the whole story of Rama, from his birth to his reign, as an outpouring of devotion: Shiva tells it to Parvati, Kakabhushundi to Garuda, and Tulsidas to us."
    },
    {
      id: "sundarkand",
      title: "Sundar Kand",
      sanskritTitle: "सुन्दरकाण्ड",
      tagline: "Hanuman's journey to Lanka · from the Ramcharitmanas",
      partLabel: "Kand",
      sectionLabel: "Doha",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      singlePart: true,
      category: "itihasa",
      translation: "Tulsidas's Awadhi, from the IIT Kanpur Ramcharitmanas project via DharmicData, with a transliteration that drops the silent final a, as the Manas is sung. The closing passage of the kand (doha 60) is missing from the source and will be added; F. S. Growse's English translation (1883) is being prepared.",
      about: "The fifth book of the Ramcharitmanas, read on its own in countless homes, often on Tuesdays and Saturdays or in times of trouble: Hanuman leaps the ocean, finds Sita in Lanka, gives her Rama's ring, sets Lanka ablaze and returns with her token, and Rama's army reaches the shore."
    },
    {
      id: "mahabharata",
      title: "Mahabharata",
      sanskritTitle: "महाभारत",
      tagline: "Vyasa's great epic · all 18 parvas",
      partLabel: "Parva",
      sectionLabel: "Section",
      verses: false,
      category: "itihasa",
      glyph: "🐚",
      gradient: "g2",
      translation: "Complete English prose translation by Kisari Mohan Ganguli (1883–96), as scanned and proofed by sacred-texts.com.",
      about: "Attributed to Vyasa, the Mahabharata follows the rivalry of the Pandavas and Kauravas, culminating in the war at Kurukshetra. It is among the longest poems ever composed and contains the Bhagavad Gita."
    },
    {
      id: "rigveda",
      title: "Rig Veda",
      sanskritTitle: "ऋग्वेद",
      tagline: "All 1,028 hymns · Sanskrit with English",
      partLabel: "Mandala",
      sectionLabel: "Hymn",
      verses: true,
      sanskrit: true,
      category: "veda",
      translation: "Sanskrit from the Vedic Heritage Portal, via the open DharmicData project. The ten mandalas in the English verse translation of Ralph T. H. Griffith (1896), public domain, from Wikisource; the opening selection translated by Dharma Path.",
      about: "The oldest scripture of Hinduism, composed more than 3,000 years ago: 1,028 hymns in ten books (mandalas) to the divine powers of fire, dawn, sky and the cosmos. It opens here with ten of its most beloved hymns, including the Gayatri, the Purusha Sukta and the Hymn of Creation, followed by the complete text, hymn by hymn."
    },
    {
      id: "samaveda",
      title: "Sama Veda",
      sanskritTitle: "सामवेद",
      tagline: "The Veda of chant · 1,794 verses",
      partLabel: "Book",
      sectionLabel: "Chapter",
      verses: true,
      category: "veda",
      translation: "English verse translation by Ralph T. H. Griffith (1895), public domain.",
      about: "The Veda of melody. Most of its verses come from the Rig Veda, arranged to be sung by the priests during the Soma sacrifice; Indian classical music traces its roots to these chants. Krishna says in the Gita: “Among the Vedas, I am the Sama Veda.”"
    },
    {
      id: "yajurveda",
      title: "Yajur Veda",
      sanskritTitle: "यजुर्वेद",
      tagline: "The White Yajur Veda · 40 books of sacred formulas",
      partLabel: "Book",
      sectionLabel: "Book",
      verses: true,
      sanskrit: true,
      category: "veda",
      translation: "Sanskrit of the Madhyandina Vajasaneyi Samhita via the open DharmicData project. English translation by Ralph T. H. Griffith, The Texts of the White Yajurveda (1899), public domain, cleaned from two scans of the printed book.",
      about: "The Veda of ritual. Its prose formulas and verses were spoken by the Adhvaryu priest as he built the altar, kindled the fires and made the offerings. Among its forty books are the Shatarudriya, the great litany to Rudra still chanted in Shiva temples (Book 16); the Purusha hymn (Book 31); the Shiva Sankalpa, 'may my mind be of auspicious resolve' (Book 34); and, as its last book, the Isha Upanishad."
    },
    {
      id: "atharvaveda",
      title: "Atharva Veda",
      sanskritTitle: "अथर्ववेद",
      tagline: "Hymns, prayers and charms · 20 books",
      partLabel: "Book",
      sectionLabel: "Hymn",
      verses: true,
      sanskrit: true,
      category: "veda",
      translation: "Sanskrit of the Shaunaka recension via the open DharmicData project. English verse translation by Ralph T. H. Griffith, The Hymns of the Atharva-Veda (1895–96), public domain, cleaned from two scans of the printed book.",
      about: "The Veda of everyday life. Beside hymns to the gods it holds prayers for healing, long life, harmony in the family, a good harvest and protection from harm, and some of the most profound hymns of the Vedas: the Hymn to the Earth (12.1), Skambha, the pillar of the universe (10.7), and the hymns to Time (19.53–54). Ayurveda traces its roots to it."
    },
    {
      id: "upanishads",
      title: "Upanishads",
      sanskritTitle: "उपनिषद्",
      tagline: "The eleven principal Upanishads",
      partLabel: "Upanishad",
      sectionLabel: "Part",
      verses: true,
      sanskrit: true,
      category: "upanishad",
      translation: "Isha, Katha and Kena: translation with commentary by Swami Paramananda (1919). Prasna, Mundaka, Taittiriya, Aitareya, Chandogya, Brihadaranyaka and Svetasvatara: F. Max Müller, Sacred Books of the East (1879 and 1884), with Sanskrit names in modern spelling. Mandukya: Robert Ernest Hume (1921). All public domain. The Sanskrit, with a transliteration, is from Sanskrit Wikisource (CC BY-SA), checked against the translations verse by verse.",
      about: "The philosophical heart of the Vedas, teaching the oneness of the Self (Atman) and the Absolute (Brahman). Here are the principal Upanishads: the Isha; the Katha, with the young Nachiketas questioning Death himself; the Kena; the Prasna's six questions; the Mundaka's higher knowledge; the Mandukya on Om and the four states of the Self; the Taittiriya's five sheaths; the Aitareya; the Chandogya, with its 'That thou art'; the vast Brihadaranyaka; and the devotional Svetasvatara."
    },
    {
      id: "bhagavata",
      title: "Bhagavata Purana",
      sanskritTitle: "भागवतपुराणम्",
      tagline: "Devotion to Vishnu and Krishna · 12 skandhas · Sanskrit",
      partLabel: "Skandha",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "The most beloved of the Puranas. The sage Shuka tells the dying King Parikshit the stories of Vishnu's avatars and of his devotees, Dhruva, Prahlada and Gajendra among them, and, in the tenth skandha, the life of Krishna, from his childhood in Vrindavan to the rasa dance with the gopis. Its theme throughout is bhakti, loving devotion."
    },
    {
      id: "vishnu",
      title: "Vishnu Purana",
      sanskritTitle: "विष्णुपुराण",
      tagline: "Creation, the ages and the life of Krishna · 6 books",
      partLabel: "Book",
      sectionLabel: "Chapter",
      verses: false,
      category: "purana",
      translation: "English prose translation by Manmatha Nath Dutt, based on H. H. Wilson's translation, public domain. Footnote markers have been removed.",
      about: "One of the eighteen great Puranas, told by the sage Parashara to his disciple Maitreya: the creation of the world, the cycles of time, the stories of Dhruva and Prahlada, the great royal dynasties and the life of Krishna."
    },
    {
      id: "garuda",
      title: "Garuda Purana",
      sanskritTitle: "गरुडपुराण",
      tagline: "The Saroddhara · death, the afterlife and liberation",
      partLabel: "Part",
      sectionLabel: "Chapter",
      verses: true,
      singlePart: true,
      category: "purana",
      translation: "English translation by Ernest Wood and S. V. Subrahmanyam, The Garuda Purana (Saroddhara), 1911, public domain. A few mantras that the translators gave only in Sanskrit are left out.",
      about: "Vishnu's teaching to Garuda, king of birds, on what happens at death and after: the soul's journey to the city of Yama, the fruits of good and evil deeds, the rites by which a family helps its departed through the first year, and, at the last, the way to liberation. Many Hindu families read it during the days of mourning after a death."
    },
    {
      id: "devibhagavatam",
      title: "Devi Bhagavatam",
      sanskritTitle: "देवीभागवतम्",
      tagline: "The Purana of the Goddess · 12 books",
      partLabel: "Book",
      sectionLabel: "Chapter",
      verses: true,
      category: "purana",
      translation: "English translation by Swami Vijnanananda (Hari Prasanna Chatterji), The Srimad Devi Bhagawatam, 1921–23, public domain. The translator's notes appear beneath their verses.",
      about: "The great Purana of the Divine Mother, counted by her devotees among the eighteen Mahapuranas. It tells how the Goddess, the Supreme Shakti, creates, sustains and dissolves the worlds; of her battles with Mahishasura, Shumbha and Nishumbha; of Navaratri, first kept by Rama; and, in the Devi Gita, her own teaching on the Self, Yoga and devotion."
    },
    {
      id: "shiva",
      title: "Shiva Purana",
      sanskritTitle: "शिवपुराणम्",
      tagline: "Two of its seven samhitas · Sanskrit",
      partLabel: "Samhita",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "The great Purana of Shiva. Here are its first book, the Vidyeshvara Samhita, on the power of Shiva's name, the linga, the sacred ash and the rudraksha, and its last, the Vayaviya Samhita, in which the wind god Vayu teaches the sages the knowledge of Shiva. The other five samhitas, with the stories of Sati, Parvati and Shiva's sons, are not yet available here."
    },
    {
      id: "linga",
      title: "Linga Purana",
      sanskritTitle: "लिङ्गपुराणम्",
      tagline: "Shiva and the pillar of light · Sanskrit",
      partLabel: "Bhaga",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "A Purana of Shiva and of his worship in the linga, the sign of the formless. It tells how Brahma and Vishnu, quarrelling over which of them was greater, saw an endless pillar of fire from which Shiva appeared, and it teaches the ways of worshipping him."
    },
    {
      id: "skanda",
      title: "Skanda Purana",
      sanskritTitle: "स्कन्दपुराणम्",
      tagline: "The Reva Khanda, on the holy Narmada · Sanskrit",
      partLabel: "Part",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      singlePart: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "The largest of the Puranas, named after Shiva's son Skanda. This is its Reva Khanda, in praise of the sacred river Narmada, also called Reva, and of the places of pilgrimage along her banks."
    },
    {
      id: "narada",
      title: "Narada Purana",
      sanskritTitle: "नारदपुराणम्",
      tagline: "Dharma, devotion and the Ekadashi fast · Sanskrit",
      partLabel: "Bhaga",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "A Purana of Vishnu in which the sage Narada learns from the four Kumaras about dharma, devotion and the vows of the year; its first part also summarises all eighteen Puranas. Its second part, given here in part, tells the story of King Rukmangada and his devotion to the Ekadashi fast, and the glory of the Ganga."
    },
    {
      id: "padma",
      title: "Padma Purana",
      sanskritTitle: "पद्मपुराणम्",
      tagline: "The lotus of creation, holy places and devotion to Vishnu · Sanskrit",
      partLabel: "Khanda",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from Sanskrit Wikisource (CC BY-SA), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "One of the longest Puranas, named for the lotus from which Brahma rose at the start of creation. Its seven khandas tell of creation and the lines of kings, the holy lake of Pushkara, the sacred rivers and places of pilgrimage, the story of Rama's horse sacrifice, and the vows and festivals dear to Vishnu, among them the glories of Ekadashi and of the Bhagavad Gita."
    },
    {
      id: "brahma",
      title: "Brahma Purana",
      sanskritTitle: "ब्रह्मपुराणम्",
      tagline: "Creation, holy places and Krishna · Sanskrit",
      partLabel: "Part",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      singlePart: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "Counted first among the eighteen Puranas. Besides creation and the royal lines, it praises the holy places of India, above all Puri and the Godavari, and tells of the life of Krishna."
    },
    {
      id: "brahmanda",
      title: "Brahmanda Purana",
      sanskritTitle: "ब्रह्माण्डपुराणम्",
      tagline: "The cosmic egg · with the story of Lalita · Sanskrit",
      partLabel: "Bhaga",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "The Purana of the cosmic egg, brahmanda, from which the universe unfolds: creation, the ages of the world, the lines of gods, sages and kings, and the shape of the worlds. Its last part holds the Lalitopakhyana, the story of the Goddess Lalita Tripurasundari."
    },
    {
      id: "bhavishya",
      title: "Bhavishya Purana",
      sanskritTitle: "भविष्यपुराणम्",
      tagline: "Sun worship, rites and the ages to come · Sanskrit",
      partLabel: "Part",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from Sanskrit Wikisource (CC BY-SA), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "The Purana of things to come, bhavishya, told by the sage Sumantu to King Shatanika and by Krishna to Yudhishthira. Its Brahma Parva teaches the rites of life and the worship of the Sun; the Madhyama Parva the building and consecration of temples; the Pratisarga Parva tells of the kings and saints of the ages to come; and the Uttara Parva of the vows and gifts of the whole year."
    },
    {
      id: "kurma",
      title: "Kurma Purana",
      sanskritTitle: "कूर्मपुराणम्",
      tagline: "Vishnu as the tortoise · with the Ishvara Gita · Sanskrit",
      partLabel: "Bhaga",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "Told by Vishnu in his tortoise avatar, Kurma, it honours Vishnu and Shiva as one. Its second part opens with the Ishvara Gita, Shiva's teaching on the Self and on Yoga, followed by the Vyasa Gita on right conduct."
    },
    {
      id: "vamana",
      title: "Vamana Purana",
      sanskritTitle: "वामनपुराणम्",
      tagline: "The dwarf who measured the worlds · Sanskrit",
      partLabel: "Part",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      singlePart: true,
      category: "purana",
      translation: "Sanskrit text from GRETIL, the Göttingen Register of Electronic Texts in Indian Languages (CC BY-NC-SA 4.0), in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "Named after Vishnu's dwarf avatar, who asked the demon king Bali for three steps of land and with them crossed the universe. It also tells of Shiva and Parvati and praises the holy land of Kurukshetra."
    },
    {
      id: "varaha",
      title: "Varaha Purana",
      sanskritTitle: "वराहपुराणम्",
      tagline: "Vishnu as the boar, in dialogue with the Earth · Sanskrit",
      partLabel: "Part",
      sectionLabel: "Adhyaya",
      verses: true,
      sanskrit: true,
      sanskritOnly: true,
      singlePart: true,
      category: "purana",
      translation: "Sanskrit text from Sanskrit Wikisource (CC BY-SA), converted by an archive.org contributor, in Devanagari with a transliteration. A free English translation is still being looked for.",
      about: "Vishnu, as the boar who lifted the Earth out of the cosmic ocean, answers the questions of the Earth goddess herself: on worship, vows, holy places such as Mathura, and the life of his devotees."
    },
    {
      id: "yoga",
      title: "Yoga Sutras of Patanjali",
      sanskritTitle: "योगसूत्र",
      tagline: "The classic guide to meditation · 4 books",
      partLabel: "Book",
      sectionLabel: "Book",
      verses: true,
      category: "darshana",
      translation: "English translation with commentary by Charles Johnston (1912), public domain.",
      about: "Patanjali's concise aphorisms (sutras) on stilling the mind, the eight limbs of yoga and the path to freedom. Johnston adds a short commentary after each sutra."
    }
  ],

  /* ------------------------------------------------------------------ */
  /* Recurring observances shown on the calendar                         */
  /* ------------------------------------------------------------------ */
  vrats: {
    ekadashi: {
      name: "Ekadashi", deva: "एकादशी", deity: "vishnu",
      summary: "The eleventh lunar day, sacred to Vishnu.",
      meaning: "Ekadashi falls twice a month, on the eleventh day of each lunar fortnight. Devotees of Vishnu fast from grains and beans, or eat simply, and spend the day in prayer. The fast is broken the next morning after sunrise. Each of the 24 Ekadashis of the year has its own name and story.",
      prayers: ["vasudeva", "shantakaram", "jagdish", "narayana"]
    },
    purnima: {
      name: "Purnima", deva: "पूर्णिमा", deity: "vishnu",
      summary: "Full moon.",
      meaning: "The full moon is an auspicious day for worship, charity and fasting. Many families perform the Satyanarayan Katha, a puja to Vishnu, on Purnima.",
      prayers: ["jagdish", "gayatri", "purnamadah"]
    },
    amavasya: {
      name: "Amavasya", deva: "अमावस्या", deity: "universal",
      summary: "New moon, a day to remember the ancestors.",
      meaning: "On the new moon, offerings of water and sesame (tarpan) are made to the ancestors, and many people keep a quiet, reflective day. New ventures are usually not begun.",
      prayers: ["mahamrityunjaya", "tvameva", "sarve-bhavantu"]
    },
    sankashti: {
      name: "Sankashti Chaturthi", deva: "संकष्टी", deity: "ganesha",
      summary: "Ganesha's monthly fast, broken at moonrise.",
      meaning: "On the fourth day after each full moon, devotees fast for Ganesha, the remover of difficulties (sankat), and break the fast after sighting the moon. When it falls on a Tuesday it is Angaraki Chaturthi, especially auspicious.",
      prayers: ["ganesh-mantra", "ganesha", "ganesh-aarti", "sukhkarta"]
    },
    pradosh: {
      name: "Pradosh Vrat", deva: "प्रदोष", deity: "shiva",
      summary: "Shiva's twilight worship on the thirteenth lunar day.",
      meaning: "Twice a month, on the thirteenth lunar day, Shiva is worshipped in the hour and a half after sunset, when he is said to dance in joy on Mount Kailash. Pradosh on a Monday (Soma Pradosh) or Saturday (Shani Pradosh) is especially valued.",
      prayers: ["shiva", "shiv-aarti", "rudrashtakam", "karpura-gauram"]
    },
    shivaratri: {
      name: "Masik Shivaratri", deva: "शिवरात्रि", deity: "shiva",
      summary: "Shiva's monthly night of worship.",
      meaning: "Every month, the fourteenth night of the waning moon is Shivaratri. Devotees fast and worship Shiva at night. The greatest of these is Maha Shivaratri in Phalguna.",
      prayers: ["shiva", "mahamrityunjaya", "shiv-chalisa", "shiva-panchakshara"]
    }
  },

  /* Deity traditionally worshipped on each weekday, Sunday first */
  weekdays: [
    { deity: "surya", name: "Ravivar", note: "Sunday is the Sun's day.", prayers: ["japa-kusuma", "surya-mantra", "gayatri"] },
    { deity: "shiva", name: "Somvar", note: "Monday is sacred to Shiva.", prayers: ["shiva", "rudrashtakam", "shiv-aarti"] },
    { deity: "hanuman", name: "Mangalvar", note: "Tuesday is for Hanuman and Ganesha.", prayers: ["hanuman-chalisa", "manojavam", "hanuman-aarti"] },
    { deity: "ganesha", name: "Budhvar", note: "Wednesday is Ganesha's day.", prayers: ["ganesha", "ganesh-mantra", "ganesh-aarti"] },
    { deity: "vishnu", name: "Guruvar", note: "Thursday is for Vishnu and the guru.", prayers: ["jagdish", "vasudeva", "guru"] },
    { deity: "devi", name: "Shukravar", note: "Friday is for the Goddess: Durga, Lakshmi and Santoshi Ma.", prayers: ["lakshmi-aarti", "mahalakshmi", "ambe-aarti"] },
    { deity: "hanuman", name: "Shanivar", note: "Saturday is for Shani and Hanuman.", prayers: ["hanuman-chalisa", "ramaskandam", "navagraha"] }
  ],

  /* ------------------------------------------------------------------ */
  /* Festivals. month = typical Gregorian month (1-12); lunar dates vary */
  /* ------------------------------------------------------------------ */
  festivals: [
    {
      id: "makar-sankranti",
      deva: "संक्रान्ति",
      prayers: ["surya-mantra", "japa-kusuma", "gayatri"],
      name: "Makar Sankranti",
      month: 1,
      when: "Around 14 January, when the sun enters Capricorn",
      glyph: "🪁",
      gradient: "g5",
      summary: "A harvest festival marking the sun's northward journey.",
      meaning: "One of the few festivals set by the solar calendar, Sankranti marks the start of longer days. It is a time of thanks for the harvest and is celebrated as Pongal in Tamil Nadu and Lohri in Punjab.",
      traditions: ["Flying kites", "Sweets made from sesame and jaggery", "Holy dips in rivers", "Giving to those in need"],
      atHome: ["Prepare til-gud (sesame-jaggery sweets) and share them, saying “eat sweet, speak sweet.”", "Offer water to the rising sun.", "Donate food or warm clothing."]
    },
    {
      id: "vasant-panchami",
      deva: "वसन्त",
      prayers: ["ya-kundendu", "saraswati", "saraswati-aarti"],
      name: "Vasant Panchami",
      month: 2,
      when: "Fifth day of the bright half of Magha (Jan–Feb)",
      glyph: "📚",
      gradient: "g5",
      summary: "Welcoming spring and honouring Saraswati.",
      meaning: "Devotees worship Saraswati, goddess of knowledge and the arts. Yellow, the colour of mustard flowers, is worn everywhere. Many children write their first letters on this day.",
      traditions: ["Wearing yellow", "Saraswati puja", "Blessing books and instruments"],
      atHome: ["Place books, pens or instruments before an image of Saraswati.", "Offer yellow flowers and sweets.", "Chant the Saraswati prayer from the Puja tab."]
    },
    {
      id: "maha-shivaratri",
      deva: "शिवरात्रि",
      prayers: ["shiva", "mahamrityunjaya", "rudrashtakam", "shiv-chalisa"],
      name: "Maha Shivaratri",
      month: 2,
      when: "Night before the new moon in Phalguna (Feb–Mar)",
      glyph: "🔱",
      gradient: "g2",
      summary: "The great night of Shiva.",
      meaning: "Devotees stay awake through the night in prayer and meditation, honouring Shiva and the triumph of awareness over darkness. Many traditions say it marks Shiva's marriage to Parvati.",
      traditions: ["Fasting", "All-night vigil", "Bathing the lingam with milk, water and honey", "Chanting Om Namah Shivaya"],
      atHome: ["Fast or eat simply.", "Offer water, milk and bilva leaves to a Shiva image or lingam.", "Chant Om Namah Shivaya 108 times with the japa counter."]
    },
    {
      id: "holi",
      deva: "होली",
      prayers: ["madhurashtakam", "kunj-bihari", "hare-krishna"],
      name: "Holi",
      month: 3,
      when: "Full moon of Phalguna (Feb–Mar)",
      glyph: "🎨",
      gradient: "g4",
      summary: "The festival of colours and the arrival of spring.",
      meaning: "Holi celebrates good over evil through the story of Prahlada, the young devotee of Vishnu who survived the fire of the demoness Holika. It also recalls Krishna's playful love for Radha. On the eve, bonfires (Holika Dahan) are lit.",
      traditions: ["Holika Dahan bonfire", "Throwing coloured powder and water", "Forgiving old quarrels", "Sweets such as gujiya"],
      atHome: ["Light a small lamp in place of a bonfire and reflect on what to let go of.", "Use natural colours made from turmeric, beetroot or flowers.", "Reach out to someone you have drifted apart from."]
    },
    {
      id: "ram-navami",
      deva: "राम",
      prayers: ["ramchandra-kripalu", "rama-mantra", "ramaya"],
      name: "Rama Navami",
      month: 4,
      when: "Ninth day of the bright half of Chaitra (Mar–Apr)",
      glyph: "🏹",
      gradient: "g1",
      summary: "The birth of Lord Rama.",
      meaning: "Celebrates the birth of Rama, the seventh avatar of Vishnu and the ideal of righteous living. It concludes the nine-day spring Navaratri.",
      traditions: ["Reading the Ramayana", "Bhajans and processions", "Fasting until midday"],
      atHome: ["Read a chapter of the Ramayana as a family.", "Chant “Sri Rama Jaya Rama Jaya Jaya Rama.”", "Offer panakam (jaggery drink) and fruit."]
    },
    {
      id: "raksha-bandhan",
      deva: "रक्षा",
      prayers: ["sarve-bhavantu", "vanamali"],
      name: "Raksha Bandhan",
      month: 8,
      when: "Full moon of Shravana (Jul–Aug)",
      glyph: "🧵",
      gradient: "g4",
      summary: "Celebrating the bond between siblings.",
      meaning: "A sister ties a sacred thread, the rakhi, on her brother's wrist and prays for his wellbeing. He promises to protect her. Today it honours all protective relationships.",
      traditions: ["Tying the rakhi", "Aarti and exchanging sweets", "Gifts"],
      atHome: ["Tie a rakhi on a sibling or cousin, even over video call.", "Perform a simple aarti with a lamp.", "Share a meal together."]
    },
    {
      id: "janmashtami",
      deva: "कृष्ण",
      prayers: ["madhurashtakam", "kunj-bihari", "krishna-vande", "hare-krishna"],
      name: "Krishna Janmashtami",
      month: 8,
      when: "Eighth day of the dark half of Bhadrapada (Aug–Sep)",
      glyph: "🦚",
      gradient: "g2",
      summary: "The midnight birth of Lord Krishna.",
      meaning: "Krishna was born at midnight in a prison cell in Mathura and carried across the Yamuna to safety in Gokul. Devotees celebrate his life, love and teachings.",
      traditions: ["Fasting until midnight", "Decorating a cradle for baby Krishna", "Dahi handi (forming human pyramids)", "Singing bhajans"],
      atHome: ["Decorate a small cradle with flowers.", "Offer butter, milk sweets and tulsi leaves at midnight.", "Read a story from Krishna's childhood."]
    },
    {
      id: "ganesh-chaturthi",
      deva: "गणेश",
      prayers: ["ganesh-aarti", "sukhkarta", "ganesh-mantra", "ganesha"],
      name: "Ganesh Chaturthi",
      month: 9,
      when: "Fourth day of the bright half of Bhadrapada (Aug–Sep)",
      glyph: "🐘",
      gradient: "g5",
      summary: "Welcoming Ganesha into the home.",
      meaning: "Families install a clay image of Ganesha and worship him for 1 to 11 days before immersing it in water, a reminder that all forms return to the formless.",
      traditions: ["Installing a clay murti", "Offering modaks", "Daily aarti", "Visarjan (immersion)"],
      atHome: ["Choose an eco-friendly clay image.", "Offer 21 modaks or durva grass.", "Immerse the image in a bucket at home and pour the water onto plants."]
    },
    {
      id: "navaratri",
      dayName: "Sharad Navaratri begins",
      deva: "नवरात्रि",
      prayers: ["ya-devi", "ambe-aarti", "durga-chalisa", "durga-mantra"],
      name: "Navaratri & Dussehra",
      month: 10,
      when: "First ten days of the bright half of Ashvin (Sep–Oct)",
      glyph: "🌺",
      gradient: "g4",
      summary: "Nine nights of the Goddess and a day of victory.",
      meaning: "Nine nights honour the forms of the Goddess: three each for Durga, Lakshmi and Saraswati. The tenth day, Vijayadashami or Dussehra, celebrates Durga's victory over Mahishasura and Rama's victory over Ravana.",
      traditions: ["Garba and dandiya dances", "Durga Puja in Bengal", "Golu doll displays in the South", "Burning effigies of Ravana"],
      atHome: ["Light a lamp each night and offer a flower to the Goddess.", "Honour young girls as forms of Devi (kanya puja).", "On Dussehra, name one inner obstacle you will conquer."]
    },
    {
      id: "karva-chauth",
      deva: "करवा",
      prayers: ["sarva-mangala", "shiva"],
      name: "Karva Chauth",
      month: 10,
      when: "Fourth day after the Ashvin full moon (Oct–Nov)",
      glyph: "🌙",
      gradient: "g7",
      summary: "A fast for the wellbeing of a spouse.",
      meaning: "Mainly observed in North India, married women fast from sunrise until they see the moon, praying for their husband's long life. Many couples now fast together.",
      traditions: ["Sunrise meal (sargi)", "Day-long fast", "Viewing the moon through a sieve"],
      atHome: ["Fast together as a couple if you wish.", "Gather with friends to hear the Karva Chauth story.", "Break the fast after offering water to the moon."]
    },
    {
      id: "diwali",
      dayName: "Diwali · Lakshmi Puja",
      deva: "दीपावली",
      prayers: ["lakshmi-aarti", "mahalakshmi", "deepa-jyoti", "ganesh-aarti"],
      name: "Diwali",
      month: 11,
      when: "New moon of Kartika (Oct–Nov)",
      glyph: "🪔",
      gradient: "g1",
      summary: "The festival of lights.",
      meaning: "Diwali celebrates the victory of light over darkness. It marks Rama's return to Ayodhya, Krishna's victory over Narakasura, and the worship of Lakshmi. It spans five days, from Dhanteras to Bhai Dooj.",
      traditions: ["Lighting diyas", "Rangoli designs", "Lakshmi puja", "Sharing sweets and gifts", "New clothes and cleaning the home"],
      atHome: ["Clean and declutter your home before the day.", "Draw a rangoli at the entrance.", "Light diyas at dusk and perform Lakshmi puja.", "Share sweets with neighbours."]
    },
    {
      id: "kartik-purnima",
      deva: "कार्तिक",
      prayers: ["deepa-jyoti", "shiva", "jagdish"],
      name: "Kartik Purnima / Dev Deepavali",
      month: 11,
      when: "Full moon of Kartika (Nov)",
      glyph: "✨",
      gradient: "g6",
      summary: "The Diwali of the gods.",
      meaning: "In Varanasi, the ghats are lit with countless lamps to honour Shiva's victory over the demon Tripurasura. It is also an auspicious day for holy bathing and charity.",
      traditions: ["Floating lamps on rivers", "Holy bathing", "Charity"],
      atHome: ["Float a small lamp in a bowl of water.", "Give to a cause close to your heart."]
    },
    {
      id: "ugadi", name: "Ugadi · Gudi Padwa", deva: "नववर्ष", month: 3,
      when: "First day of the bright half of Chaitra (Mar–Apr)",
      summary: "The Hindu New Year, and the start of the spring Navaratri.",
      meaning: "Chaitra Shukla Pratipada begins the new lunar year in much of India. It is Ugadi in Karnataka, Andhra Pradesh and Telangana, Gudi Padwa in Maharashtra and Cheti Chand for Sindhis. Tradition holds that Brahma began creation on this day. Chaitra Navaratri, nine nights of the Goddess, begins now and ends on Rama Navami.",
      traditions: ["Raising a gudi (a decorated pole with an inverted pot) in Maharashtra", "Ugadi pachadi: a dish of six tastes, for life's mix of experiences", "Hearing the year's panchanga read aloud", "Oil bath, new clothes and mango-leaf garlands on doorways"],
      atHome: ["Clean the home and hang a string of mango leaves at the door.", "Make a simple dish mixing sweet, sour, bitter, salty, spicy and astringent tastes, and share it.", "Begin the spring Navaratri by lighting a lamp each evening."],
      prayers: ["ganesha", "durga-mantra", "ya-devi"]
    },
    {
      id: "hanuman-jayanti", name: "Hanuman Jayanti", deva: "हनुमान", month: 4,
      when: "Full moon of Chaitra (Mar–Apr)",
      summary: "The birth of Hanuman, the devoted servant of Rama.",
      meaning: "Hanuman embodies strength placed wholly in the service of love. In North India his birth is celebrated on the full moon of Chaitra; some regions celebrate it at other times of year.",
      traditions: ["Reciting the Hanuman Chalisa, often 7 or 108 times", "Offering sindoor and jasmine oil at Hanuman temples", "Reading the Sundara Kanda of the Ramayana"],
      atHome: ["Recite the Hanuman Chalisa at sunrise.", "Offer red flowers and a sweet such as boondi.", "Read the story of Hanuman's leap to Lanka in the Ramayana."],
      prayers: ["hanuman-chalisa", "manojavam", "hanuman-aarti"]
    },
    {
      id: "akshaya-tritiya", name: "Akshaya Tritiya", deva: "अक्षय", month: 4,
      when: "Third day of the bright half of Vaishakha (Apr–May)",
      summary: "A day of imperishable blessings for new beginnings and generosity.",
      meaning: "“Akshaya” means never diminishing. Good deeds, charity and new ventures begun today are believed to bear lasting fruit. It is also remembered as the birthday of Parashurama and the day the Treta Yuga began.",
      traditions: ["Charity, especially of food, water and grain", "Beginning new ventures or buying gold", "Worship of Vishnu and Lakshmi"],
      atHome: ["Give food or water to someone in need.", "Begin something you have been putting off.", "Offer a lamp to Lakshmi and Vishnu in the evening."],
      prayers: ["lakshmi-mantra", "mahalakshmi", "vasudeva"]
    },
    {
      id: "ganga-dussehra", name: "Ganga Dussehra", deva: "गङ्गा", month: 6,
      when: "Tenth day of the bright half of Jyeshtha (May–Jun)",
      summary: "The descent of the holy Ganga from heaven to earth.",
      meaning: "Celebrates the day the Ganga descended to earth through Shiva's matted locks, brought down by the austerities of King Bhagiratha to free his ancestors.",
      traditions: ["Bathing in the Ganga or another river", "Evening Ganga aarti at Haridwar and Varanasi", "Floating lamps on the water"],
      atHome: ["Recite Gange Cha Yamune while bathing.", "Float a small lamp in a bowl of water at dusk."],
      prayers: ["ganga-snana", "shiva", "deepa-jyoti"]
    },
    {
      id: "rath-yatra", name: "Jagannath Rath Yatra", deva: "रथयात्रा", month: 7,
      when: "Second day of the bright half of Ashadha (Jun–Jul)",
      summary: "The great chariot procession of Lord Jagannath at Puri.",
      meaning: "Jagannath, a form of Krishna, rides out of his temple at Puri with his brother Balabhadra and sister Subhadra on three towering wooden chariots, pulled by hundreds of thousands of devotees. Rath Yatras are now held in cities around the world.",
      traditions: ["Pulling the chariots with ropes", "Kirtan and dancing in the streets", "Sharing mahaprasad"],
      atHome: ["Join a local Rath Yatra if one is held nearby.", "Sing the Hare Krishna mantra or Jaya Radha Madhava."],
      prayers: ["hare-krishna", "radha-madhav", "achyutam"]
    },
    {
      id: "guru-purnima", name: "Guru Purnima", deva: "गुरु", month: 7,
      when: "Full moon of Ashadha (Jun–Jul)",
      summary: "A day to honour your teachers.",
      meaning: "Also called Vyasa Purnima, it honours the sage Vyasa, who compiled the Vedas and composed the Mahabharata, and through him every teacher who has guided us.",
      traditions: ["Honouring one's guru with flowers and gifts", "Reading scripture", "Thanking teachers and mentors"],
      atHome: ["Thank a teacher who shaped you, with a call, a message or a visit.", "Recite Gurur Brahma.", "Read a passage of the Bhagavad Gita."],
      prayers: ["guru", "krishna-vande", "asato-ma"]
    },
    {
      id: "nag-panchami", name: "Nag Panchami", deva: "नाग", month: 8,
      when: "Fifth day of the bright half of Shravana (Jul–Aug)",
      summary: "Honouring the serpent deities.",
      meaning: "Serpents are revered as guardians of the earth's waters and treasures, and are closely linked with Shiva and Vishnu. On this day they are offered milk and prayers for the family's protection.",
      traditions: ["Worship of serpent images in clay or silver", "Offering milk at anthills or temples", "Not digging the earth"],
      atHome: ["Offer prayers to Shiva, who wears the serpent Vasuki.", "Avoid harming any living creature today."],
      prayers: ["shiva", "karpura-gauram"]
    },
    {
      id: "hartalika-teej", name: "Hartalika Teej", deva: "तीज", month: 9,
      when: "Third day of the bright half of Bhadrapada (Aug–Sep)",
      summary: "Women honour Parvati's devotion to Shiva.",
      meaning: "Parvati performed long austerities to win Shiva as her husband. On Hartalika Teej women fast, often without water, and worship Shiva and Parvati for marital happiness, or for a good husband.",
      traditions: ["A strict fast", "Clay images of Shiva and Parvati", "Night-long singing"],
      atHome: ["Make simple clay images of Shiva and Parvati and offer flowers.", "Hear the story of Parvati's penance."],
      prayers: ["shiva", "sarva-mangala", "shiv-aarti"]
    },
    {
      id: "anant-chaturdashi", name: "Anant Chaturdashi", deva: "अनन्त", month: 9,
      when: "Fourteenth day of the bright half of Bhadrapada (Sep)",
      summary: "Farewell to Ganesha, and worship of the infinite Vishnu.",
      meaning: "The final day of Ganeshotsav, when clay images of Ganesha are immersed in water. It is also the day of Anant, the infinite Vishnu, whose protective thread with fourteen knots is tied on the arm.",
      traditions: ["Ganesh visarjan processions", "Tying the anant sutra", "Vishnu puja"],
      atHome: ["Immerse a clay Ganesha in a bucket of water and pour it onto plants.", "Tie a thread on your wrist as a prayer for protection."],
      prayers: ["ganesh-aarti", "sukhkarta", "vasudeva"]
    },
    {
      id: "pitru-paksha", name: "Pitru Paksha begins", deva: "पितृ", month: 9,
      when: "Dark half of Bhadrapada (Sep–Oct)",
      summary: "Sixteen days for remembering the ancestors.",
      meaning: "During Pitru Paksha families offer shraddha and tarpan (water, sesame and food) to their ancestors on the lunar day of each one's passing. New ventures and celebrations are traditionally postponed. It ends on Mahalaya Amavasya.",
      traditions: ["Tarpan: offering water mixed with sesame", "Feeding brahmins, the poor, crows and cows", "Remembering the names of departed family"],
      atHome: ["Light a lamp before photos of departed family members.", "Cook a dish they loved and give food to someone in need.", "Share family stories with younger relatives."],
      prayers: ["mahamrityunjaya", "sarve-bhavantu", "tvameva"]
    },
    {
      id: "sharad-purnima", name: "Sharad Purnima", deva: "शरद", month: 10,
      when: "Full moon of Ashvin (Oct)",
      summary: "The brightest full moon of the year.",
      meaning: "On this autumn night the moon is said to shine with all sixteen kalas and to pour amrit into its rays. It recalls Krishna's Raas Leela with the gopis, and in Bengal and Odisha it is Kojagari Lakshmi Puja.",
      traditions: ["Leaving kheer out in the moonlight overnight", "Staying awake to worship Lakshmi", "Raas and garba under the moon"],
      atHome: ["Make kheer and leave it in the moonlight, then share it in the morning.", "Sit outside for a few minutes under the full moon in quiet reflection."],
      prayers: ["lakshmi-aarti", "madhurashtakam", "lakshmi-mantra"]
    },
    {
      id: "chhath", name: "Chhath Puja", deva: "छठ", month: 11,
      when: "Sixth day of the bright half of Kartika (Oct–Nov)",
      summary: "Offerings to the setting and rising sun.",
      meaning: "A festival of Bihar, Jharkhand and eastern Uttar Pradesh, now celebrated worldwide. Over four days, devotees fast and stand in rivers to offer arghya to the setting sun and, at dawn, the rising sun, giving thanks to Surya and Chhathi Maiya.",
      traditions: ["A 36-hour waterless fast", "Evening and dawn arghya in a river or pond", "Thekua and fruit offered in bamboo baskets"],
      atHome: ["Offer water to the sun at sunset and again at sunrise.", "Make thekua and share it."],
      prayers: ["japa-kusuma", "surya-mantra", "gayatri"]
    },
    {
      id: "tulsi-vivah", name: "Tulsi Vivah", deva: "तुलसी", month: 11,
      when: "Twelfth day of the bright half of Kartika (Nov)",
      summary: "The ceremonial wedding of the tulsi plant to Vishnu.",
      meaning: "The holy basil, Tulsi, is honoured as a goddess and married to Vishnu in the form of Shaligram or Krishna. It marks the start of the wedding season after the four months of Chaturmas.",
      traditions: ["Decorating the tulsi plant as a bride", "A wedding ceremony with a Shaligram stone", "Sharing sweets"],
      atHome: ["Water your tulsi plant, decorate it with a red cloth and light a lamp beside it.", "Sing Om Jai Jagdish Hare."],
      prayers: ["jagdish", "vasudeva", "shantakaram"]
    },
    {
      id: "holika-dahan", name: "Holika Dahan", deva: "होलिका", parent: "holi",
      summary: "The bonfire on the eve of Holi.",
      meaning: "A bonfire is lit after sunset to recall how the demoness Holika burned while the devoted child Prahlada was protected by Vishnu."
    },
    {
      id: "janmashtami-vaishnava", name: "Janmashtami (ISKCON / Vaishnava)", deva: "कृष्ण", parent: "janmashtami",
      summary: "Krishna's birthday as observed by ISKCON and Vaishnava communities.",
      meaning: "Vaishnava communities, including ISKCON, follow a different rule from Smarta households and this year celebrate Janmashtami a day later."
    },
    {
      id: "mahalaya", name: "Mahalaya Amavasya", deva: "महालय", parent: "pitru-paksha",
      summary: "The final day of Pitru Paksha and the eve of Navaratri.",
      meaning: "The most important day for remembering all ancestors, including those whose date of passing is unknown. In Bengal it marks the invocation of Durga before Durga Puja."
    },
    {
      id: "durga-ashtami", name: "Durga Ashtami", deva: "अष्टमी", parent: "navaratri",
      summary: "The eighth day of Navaratri, honouring Mahagauri.",
      meaning: "One of the most sacred days of Navaratri. Many families perform kanya puja, honouring young girls as forms of the Goddess, and in Bengal it is the height of Durga Puja."
    },
    {
      id: "maha-navami", name: "Maha Navami", deva: "नवमी", parent: "navaratri",
      summary: "The ninth night of Navaratri, honouring Siddhidatri.",
      meaning: "The final day of Navaratri worship. In the South, books, tools and instruments are worshipped as Ayudha Puja."
    },
    {
      id: "dussehra", name: "Dussehra · Vijayadashami", deva: "विजय", parent: "navaratri",
      summary: "The victory of good over evil.",
      meaning: "Celebrates Rama's victory over Ravana and Durga's victory over Mahishasura. Effigies of Ravana are burned, and it is an auspicious day to begin learning."
    },
    {
      id: "dhanteras", name: "Dhanteras", deva: "धनतेरस", parent: "diwali",
      summary: "The first day of Diwali.",
      meaning: "Honours Dhanvantari, the physician of the gods, who rose from the churning ocean with the nectar of immortality. Families buy a new vessel or metal and light the first lamps of Diwali."
    },
    {
      id: "naraka-chaturdashi", name: "Naraka Chaturdashi", deva: "नरक", parent: "diwali",
      summary: "Choti Diwali: Krishna's victory over Narakasura.",
      meaning: "Celebrates Krishna and Satyabhama's defeat of the demon Narakasura. An oil bath before sunrise and lamps at dusk mark the day."
    },
    {
      id: "govardhan-puja", name: "Govardhan Puja · Annakut", deva: "गोवर्धन", parent: "diwali",
      summary: "Krishna lifts Govardhan hill.",
      meaning: "Remembers how Krishna lifted Govardhan hill to shelter the people of Vraja from Indra's storms. A “mountain of food” (annakut) is offered and shared."
    },
    {
      id: "bhai-dooj", name: "Bhai Dooj", deva: "भाई दूज", parent: "diwali",
      summary: "Celebrating brothers and sisters.",
      meaning: "Sisters apply tilaka to their brothers' foreheads and pray for their long life, recalling the god of death Yama's visit to his sister Yamuna. It closes the five days of Diwali."
    }
  ]
};
