/* Dharma Path: reading plans. Each plan reads a book in daily portions.
   days: a list of [part, fromSection, toSection] (sections numbered from 1, as in the reader), or
   breaks: [[part, doha], ...] for the Ramcharitmanas, where a day ends after that doha
   ("end" for the last section of the part). A weekly plan reads the whole book on one weekday. */
window.CONTENT.plans = [
  {
    id: "gita-18", book: "gita", deva: "गीता", title: "The Bhagavad Gita in 18 days",
    summary: "One chapter a day.",
    about: "The eighteen chapters of the Gita, one a day. Many read the whole Gita this way before Gita Jayanti, in the month of Margashirsha, or begin on any day they choose. The chapters are short, from 20 verses to 78, so a day's reading takes ten to thirty minutes.",
    days: Array.from({ length: 18 }, (_, i) => [i + 1, 1, 1])
  },
  {
    id: "manas-30", book: "ramcharitmanas", deva: "मास", title: "The Ramcharitmanas in 30 days",
    summary: "Masparayan: the traditional month-long reading.",
    about: "The masparayan, the reading of the whole Manas in a month, with the thirty resting places (vishram) marked in the Gita Press edition. Many keep it through a sacred month such as Shravan or Kartik, but it can be begun on any day. About 35 dohas a day.",
    breaks: [[1, 25], [1, 55], [1, 89], [1, 120], [1, 152], [1, 183], [1, 211], [1, 239], [1, 270], [1, 304], [1, 326], [1, "end"],
      [2, 28], [2, 60], [2, 93], [2, 116], [2, 133], [2, 176], [2, 215], [2, 236], [2, "end"],
      [3, "end"], [4, "end"], [5, "end"], [6, 48], [6, 98], [6, "end"], [7, 62], [7, 114], [7, "end"]]
  },
  {
    id: "manas-9", book: "ramcharitmanas", deva: "नवाह", title: "The Ramcharitmanas in 9 days",
    summary: "Navahparayan: the nine-day reading, often kept in Navaratri.",
    about: "The navahparayan, the reading of the whole Manas in nine days, with the nine resting places of the Gita Press edition. Many families keep it during Chaitra Navaratri, finishing on Rama Navami, or in Sharad Navaratri before Dussehra. It is a long reading, about two hours a day.",
    breaks: [[1, 120], [1, 239], [1, 358], [2, 116], [2, 236], [3, 29], [6, 12], [7, 10], [7, "end"]]
  },
  {
    id: "sundar-7", book: "sundarkand", deva: "सुन्दर", title: "The Sundar Kand in 7 days",
    summary: "Hanuman's journey to Lanka, a little each day.",
    about: "The Sundar Kand in seven daily readings of eight or nine dohas, from Hanuman's leap across the ocean to the army reaching the shore.",
    days: [[1, 1, 9], [1, 10, 18], [1, 19, 27], [1, 28, 36], [1, 37, 44], [1, 45, 52], [1, 53, 61]]
  },
  {
    id: "sundar-weekly", book: "sundarkand", deva: "हनुमान", title: "The Sundar Kand every week",
    summary: "The whole Sundar Kand on Tuesday or Saturday.",
    about: "Many families read the whole Sundar Kand every Tuesday or Saturday, the days of Hanuman, or in times of trouble, often ending with the Hanuman Chalisa and aarti. It takes about an hour and a half. Choose your day.",
    weekly: true
  },
  {
    id: "upanishads-13", book: "upanishads", deva: "उपनिषद्", title: "The principal Upanishads in 13 days",
    summary: "One Upanishad a day; the two longest over two days each.",
    about: "The eleven principal Upanishads, from the eighteen verses of the Isha to the great Brihadaranyaka, in Max Müller's translation. The short ones take a few minutes; the Chandogya and Brihadaranyaka are given two days each.",
    days: [[1, 1, 1], [3, 1, 4], [2, 1, 6], [4, 1, 6], [5, 1, 3], [6, 1, 1], [7, 1, 3], [8, 1, 3], [11, 1, 6],
      [9, 1, 4], [9, 5, 8], [10, 1, 3], [10, 4, 6]]
  }
];
