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
  /* Academy: structured courses                                         */
  /* ------------------------------------------------------------------ */
  categories: [
    { id: "all", name: "All" },
    { id: "philosophy", name: "Philosophy" },
    { id: "deities", name: "Deities" },
    { id: "scripture", name: "Scripture" },
    { id: "practice", name: "Practice" },
    { id: "temples", name: "Temples" }
  ],

  courses: [
    {
      id: "foundations",
      category: "philosophy",
      title: "Foundations of Hinduism",
      subtitle: "Key ideas in five short lessons",
      glyph: "🕉️",
      gradient: "g1",
      lessons: [
        {
          title: "Sanatana Dharma: the eternal way",
          body: "<p>Many Hindus call their tradition <strong>Sanatana Dharma</strong>, the “eternal way” or “timeless order.” It has no single founder, no single book and no central authority. It is a family of traditions, philosophies and practices that grew over thousands of years across South Asia.</p><p>This variety is a feature, not a flaw. Hindus are encouraged to approach truth in the way that best suits their nature, whether through devotion, knowledge, selfless action or meditation.</p>"
        },
        {
          title: "Brahman and Atman",
          body: "<p><strong>Brahman</strong> is the ultimate reality: infinite, unchanging and the ground of everything that exists. <strong>Atman</strong> is the true Self within each being.</p><p>The Upanishads teach that Atman and Brahman are deeply connected. Some schools (Advaita) say they are identical, while others (Dvaita, Vishishtadvaita) describe a loving relationship between the soul and God.</p>"
        },
        {
          title: "Karma and rebirth",
          body: "<p><strong>Karma</strong> means “action” and the results that follow from it. Every intentional thought, word and deed leaves an impression that shapes future experience.</p><p>Through <strong>samsara</strong>, the cycle of birth, death and rebirth, the soul carries these impressions forward. Karma is not fate or punishment. It is a moral law of cause and effect, and our present choices can always change our direction.</p>"
        },
        {
          title: "The four goals of life",
          body: "<p>Hindu thought describes four <strong>purusharthas</strong>, or legitimate aims of human life:</p><ul><li><strong>Dharma</strong>: righteousness, duty and ethical living</li><li><strong>Artha</strong>: prosperity and meaningful work</li><li><strong>Kama</strong>: love, pleasure and beauty</li><li><strong>Moksha</strong>: liberation from the cycle of rebirth</li></ul><p>A balanced life pursues wealth and pleasure guided by dharma, always oriented toward moksha.</p>"
        },
        {
          title: "Four paths of yoga",
          body: "<p>The Bhagavad Gita describes several paths to the divine:</p><ul><li><strong>Bhakti yoga</strong>: loving devotion</li><li><strong>Jnana yoga</strong>: knowledge and self-inquiry</li><li><strong>Karma yoga</strong>: selfless action</li><li><strong>Raja yoga</strong>: meditation and mental discipline</li></ul><p>Most people blend these paths. Choose the one that feels most natural to you and let the others support it.</p>"
        }
      ]
    },
    {
      id: "trimurti",
      category: "deities",
      title: "The Trimurti",
      subtitle: "Brahma, Vishnu and Shiva",
      glyph: "🔱",
      gradient: "g2",
      lessons: [
        {
          title: "One reality, many forms",
          body: "<p>Hindus often describe one divine reality expressed through many forms. The <strong>Trimurti</strong> shows three cosmic functions: creation (Brahma), preservation (Vishnu) and dissolution or transformation (Shiva).</p><p>Different traditions place a different deity at the centre. Vaishnavas focus on Vishnu, Shaivas on Shiva and Shaktas on the Goddess.</p>"
        },
        {
          title: "Brahma, the creator",
          body: "<p>Brahma is shown with four faces looking in the four directions, symbolising the four Vedas. He sits on a lotus and is accompanied by a swan. His consort is <strong>Saraswati</strong>, goddess of knowledge.</p><p>Brahma has few temples. The best known is at Pushkar in Rajasthan.</p>"
        },
        {
          title: "Vishnu, the preserver",
          body: "<p>Vishnu maintains cosmic order. When dharma declines, he descends as an <strong>avatar</strong>. The ten best-known avatars, the Dashavatara, include Rama and Krishna.</p><p>He holds a conch (sound of creation), a discus (the mind), a mace (strength) and a lotus (purity). His consort is <strong>Lakshmi</strong>, goddess of prosperity.</p>"
        },
        {
          title: "Shiva, the transformer",
          body: "<p>Shiva is the great yogi who destroys ignorance so that renewal can follow. As <strong>Nataraja</strong> he dances the cosmic dance of creation and dissolution.</p><p>He is often worshipped as the <strong>lingam</strong>, a formless symbol of the infinite. His consort is <strong>Parvati</strong>, and their sons are Ganesha and Kartikeya.</p>"
        }
      ]
    },
    {
      id: "devi",
      category: "deities",
      title: "The Divine Mother",
      subtitle: "Shakti, Durga, Lakshmi and Saraswati",
      glyph: "🌺",
      gradient: "g4",
      lessons: [
        {
          title: "Shakti: divine energy",
          body: "<p><strong>Shakti</strong> is the dynamic power of the divine. In Shakta traditions the Goddess, <strong>Devi</strong>, is the supreme reality, and all gods draw their power from her.</p>"
        },
        {
          title: "Durga and Kali",
          body: "<p><strong>Durga</strong> rides a lion and carries weapons given by the gods to defeat the buffalo demon Mahishasura, a symbol of ego and ignorance. Her victory is celebrated at Navaratri.</p><p><strong>Kali</strong> is her fierce form. She cuts through illusion and fear, and devotees approach her as a loving mother.</p>"
        },
        {
          title: "Lakshmi and Saraswati",
          body: "<p><strong>Lakshmi</strong> brings prosperity, beauty and good fortune, both material and spiritual. She is honoured especially at Diwali.</p><p><strong>Saraswati</strong> is the goddess of learning, music and the arts. Students worship her at Vasant Panchami and before exams.</p>"
        }
      ]
    },
    {
      id: "ganesha",
      category: "deities",
      title: "Ganesha",
      subtitle: "Remover of obstacles",
      glyph: "🐘",
      gradient: "g5",
      lessons: [
        {
          title: "Why Ganesha comes first",
          body: "<p>Ganesha is honoured at the start of every new venture, ceremony and journey. As <strong>Vighneshvara</strong>, lord of obstacles, he both removes obstacles and places them when we need to slow down and learn.</p>"
        },
        {
          title: "The story of the elephant head",
          body: "<p>Parvati created a boy from clay and asked him to guard her door. Shiva, not knowing the child, was refused entry and struck off his head in anger. To console Parvati, Shiva restored the boy with the head of the first creature found, an elephant, and made him leader of his attendants, the ganas.</p>"
        },
        {
          title: "Reading the symbolism",
          body: "<ul><li><strong>Large head</strong>: think big</li><li><strong>Large ears</strong>: listen more</li><li><strong>Small eyes</strong>: concentrate</li><li><strong>Broken tusk</strong>: sacrifice for knowledge (he used it to write the Mahabharata)</li><li><strong>Mouse vehicle</strong>: mastery over restless desire</li><li><strong>Modak sweet</strong>: the reward of spiritual practice</li></ul>"
        }
      ]
    },
    {
      id: "gita",
      category: "scripture",
      title: "Bhagavad Gita Essentials",
      subtitle: "The Song of God in six lessons",
      glyph: "📜",
      gradient: "g6",
      lessons: [
        {
          title: "The setting",
          body: "<p>The Gita is a 700-verse dialogue within the Mahabharata. On the battlefield of Kurukshetra, the warrior <strong>Arjuna</strong> loses heart at the thought of fighting his own relatives. His charioteer, <strong>Krishna</strong>, responds with teachings on duty, the Self and the paths to liberation.</p>"
        },
        {
          title: "The eternal Self (Chapter 2)",
          body: "<p>Krishna begins by teaching that the true Self cannot be killed. The body perishes, but the Atman is eternal. Grief comes from mistaking ourselves for the body alone.</p>"
        },
        {
          title: "Action without attachment (Chapters 3–5)",
          body: "<p>Withdrawing from the world is not the answer. Act according to your duty, offer the results to the divine, and stay calm in success and failure. This is <strong>karma yoga</strong>.</p>"
        },
        {
          title: "Meditation (Chapter 6)",
          body: "<p>Sit in a clean, quiet place with a steady posture. Bring the restless mind back again and again. With practice and detachment, the mind becomes as steady as a flame in a windless place.</p>"
        },
        {
          title: "The cosmic form (Chapter 11)",
          body: "<p>Arjuna asks to see Krishna's universal form and is shown the whole cosmos within him: every being, every era, creation and destruction. Overwhelmed, he asks Krishna to return to his gentle human form.</p>"
        },
        {
          title: "Surrender (Chapter 18)",
          body: "<p>The Gita ends with Krishna's most intimate teaching: set aside every other concern and take refuge in the divine. Arjuna's doubts are dispelled and he resolves to act.</p>"
        }
      ]
    },
    {
      id: "epics",
      category: "scripture",
      title: "The Great Epics",
      subtitle: "Ramayana and Mahabharata",
      glyph: "🏹",
      gradient: "g3",
      lessons: [
        {
          title: "The Ramayana",
          body: "<p>Attributed to the sage <strong>Valmiki</strong>, the Ramayana tells of Prince <strong>Rama</strong>, exiled to the forest for fourteen years with his wife <strong>Sita</strong> and brother <strong>Lakshmana</strong>. Sita is abducted by Ravana, king of Lanka. With the help of <strong>Hanuman</strong> and an army of vanaras, Rama rescues her and returns to rule Ayodhya.</p><p>Rama is the model of dharma in every role: son, husband, brother and king.</p>"
        },
        {
          title: "The Mahabharata",
          body: "<p>Attributed to <strong>Vyasa</strong>, the Mahabharata is one of the longest poems in the world. It follows the rivalry between the <strong>Pandava</strong> and <strong>Kaurava</strong> cousins, which ends in the great war at Kurukshetra.</p><p>Its characters are deeply human and morally complex. It asks how to live rightly when dharma itself is subtle and hard to see.</p>"
        },
        {
          title: "Lessons for today",
          body: "<ul><li>Integrity matters even when it costs you (Rama keeps his father's word).</li><li>Devotion gives strength beyond your limits (Hanuman's leap to Lanka).</li><li>Greed and envy destroy families (Duryodhana).</li><li>Seek wise counsel in a crisis (Arjuna turns to Krishna).</li></ul>"
        }
      ]
    },
    {
      id: "meditation",
      category: "practice",
      title: "Meditation & Mantra",
      subtitle: "A beginner's daily practice",
      glyph: "🧘",
      gradient: "g7",
      lessons: [
        {
          title: "Preparing your space",
          body: "<p>Choose a quiet corner and keep it clean. A small lamp, a picture of your chosen deity, or simply a flower is enough. Sit at the same time each day, ideally at dawn or dusk.</p>"
        },
        {
          title: "Breath (pranayama)",
          body: "<p>Sit tall and relax your shoulders. Try <strong>alternate-nostril breathing</strong>: close the right nostril and inhale through the left, close the left and exhale through the right, inhale right, then exhale left. That is one round. Do five to ten rounds slowly.</p>"
        },
        {
          title: "Japa: repeating a mantra",
          body: "<p><strong>Japa</strong> is the repetition of a sacred sound. A traditional mala has 108 beads. Choose a mantra such as <em>Om Namah Shivaya</em> or <em>Om Namo Narayanaya</em> and repeat it once per bead, softly or silently.</p><p>Use the japa counter on the Puja tab to keep count.</p>"
        },
        {
          title: "Building a habit",
          body: "<p>Start with five minutes. Consistency matters more than length. When the mind wanders, return to the mantra without judging yourself. Each return is the practice.</p>"
        }
      ]
    },
    {
      id: "temples",
      category: "temples",
      title: "Understanding the Temple",
      subtitle: "Architecture, etiquette and pilgrimage",
      glyph: "🛕",
      gradient: "g8",
      lessons: [
        {
          title: "The temple as cosmos",
          body: "<p>A Hindu temple, or <strong>mandir</strong>, is designed as a model of the universe and a home for the deity. The innermost sanctum, the <strong>garbhagriha</strong> (“womb chamber”), holds the main image. Above it rises the tower: the <strong>shikhara</strong> in northern styles and the <strong>vimana</strong> in southern styles. Southern temples also have tall gateway towers called <strong>gopurams</strong>.</p>"
        },
        {
          title: "Visiting a temple",
          body: "<ul><li>Remove your shoes before entering.</li><li>Dress modestly and wash your hands and feet.</li><li>Walk clockwise around the shrine (<strong>pradakshina</strong>).</li><li>Accept <strong>prasad</strong> (blessed food) with your right hand.</li><li>Ask before taking photos; many sanctums forbid them.</li></ul>"
        },
        {
          title: "Great pilgrimage sites",
          body: "<ul><li><strong>Varanasi</strong>: Shiva's city on the Ganga</li><li><strong>Tirupati</strong>: hilltop shrine of Lord Venkateswara</li><li><strong>The Char Dham</strong>: Badrinath, Dwarka, Puri and Rameswaram</li><li><strong>The 12 Jyotirlingas</strong>: Shiva's shrines of light</li><li><strong>Meenakshi Temple, Madurai</strong>: famed for its colourful gopurams</li></ul>"
        }
      ]
    }
  ],

  /* ------------------------------------------------------------------ */
  /* Festivals. month = typical Gregorian month (1-12); lunar dates vary */
  /* ------------------------------------------------------------------ */
  festivals: [
    {
      id: "makar-sankranti",
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
      name: "Kartik Purnima / Dev Deepavali",
      month: 11,
      when: "Full moon of Kartika (Nov)",
      glyph: "✨",
      gradient: "g6",
      summary: "The Diwali of the gods.",
      meaning: "In Varanasi, the ghats are lit with countless lamps to honour Shiva's victory over the demon Tripurasura. It is also an auspicious day for holy bathing and charity.",
      traditions: ["Floating lamps on rivers", "Holy bathing", "Charity"],
      atHome: ["Float a small lamp in a bowl of water.", "Give to a cause close to your heart."]
    }
  ],

  /* ------------------------------------------------------------------ */
  /* Life events (samskaras)                                             */
  /* ------------------------------------------------------------------ */
  lifeEvents: [
    {
      id: "birth",
      name: "Birth & Naming",
      sanskrit: "Jatakarma & Namakarana",
      glyph: "👶",
      gradient: "g5",
      summary: "Welcoming a new soul into the family.",
      meaning: "Jatakarma welcomes the newborn. Traditionally the father touches honey and ghee to the baby's lips and whispers a blessing. Namakarana, the naming ceremony, is usually held on the 11th or 12th day, or any auspicious day soon after.",
      steps: [
        "Choose a date with your family or a priest, often the 11th or 12th day after birth.",
        "Begin with a Ganesha prayer to remove obstacles.",
        "Light a lamp and offer flowers and rice to the family deity.",
        "Whisper the chosen name into the baby's right ear, then announce it to the family.",
        "Elders bless the baby by placing a little rice on the head.",
        "Share sweets with guests."
      ],
      withPriest: "A priest may perform a havan (fire offering) and calculate the first letter of the name from the baby's birth star (nakshatra)."
    },
    {
      id: "annaprashan",
      name: "First Solid Food",
      sanskrit: "Annaprashana",
      glyph: "🍚",
      gradient: "g3",
      summary: "The baby's first taste of grain.",
      meaning: "Usually performed around six months, this ceremony gives the baby their first solid food, often sweet rice pudding (kheer), as a blessing for health and nourishment.",
      steps: [
        "Prepare a small amount of kheer or mashed rice.",
        "Offer it first to the deity with a short prayer.",
        "A parent or grandparent feeds the baby the first spoonful.",
        "Some families place objects such as a book, coin and pen before the child and see which they reach for."
      ],
      withPriest: "A priest can chant Vedic verses for health and add a short havan."
    },
    {
      id: "mundan",
      name: "First Haircut",
      sanskrit: "Chudakarana (Mundan)",
      glyph: "✂️",
      gradient: "g6",
      summary: "Shaving the first hair for a fresh start.",
      meaning: "Performed between ages one and three, the first haircut symbolises letting go of past impressions. Some families perform it at a temple or holy river.",
      steps: [
        "Choose an auspicious date and location.",
        "Offer prayers to Ganesha and the family deity.",
        "A barber or family member shaves the child's head, sometimes leaving a small tuft (shikha).",
        "Apply sandalwood paste or turmeric to soothe the scalp.",
        "Offer the hair to a river or temple."
      ],
      withPriest: "Many families travel to temples such as Tirupati for this rite."
    },
    {
      id: "upanayana",
      name: "Sacred Thread",
      sanskrit: "Upanayana",
      glyph: "🧶",
      gradient: "g1",
      summary: "Beginning formal spiritual study.",
      meaning: "Traditionally, the child receives the sacred thread and is taught the Gayatri Mantra by a guru or parent, marking the start of study. Many modern families offer a similar initiation to children of any gender.",
      steps: [
        "The child bathes and wears new clothes.",
        "A havan is lit and prayers are offered.",
        "The sacred thread is placed over the left shoulder.",
        "The guru or parent teaches the Gayatri Mantra.",
        "The child symbolically asks elders for alms (bhiksha), learning humility."
      ],
      withPriest: "This rite is usually guided by a priest because of the detailed Vedic recitations."
    },
    {
      id: "vivaha",
      name: "Wedding",
      sanskrit: "Vivaha",
      glyph: "💍",
      gradient: "g4",
      summary: "Two families, two souls, seven steps.",
      meaning: "The Hindu wedding unites two people as partners in dharma. Customs vary widely by region, but the sacred fire (Agni) as witness and the seven steps (saptapadi) are central to most.",
      steps: [
        "Ganesha puja to bless the proceedings.",
        "Kanyadaan: the bride's parents give her hand to the groom.",
        "Hasta milap: the couple's hands are joined.",
        "Mangal pheras: the couple walk around the sacred fire.",
        "Saptapadi: seven steps together, each a vow for food, strength, prosperity, happiness, children, harmony and lifelong friendship.",
        "Sindoor and mangalsutra are given as signs of marriage.",
        "The couple receive blessings from elders."
      ],
      withPriest: "A priest leads the Vedic recitations. Many offer short ceremonies with English explanations for interfaith or overseas weddings."
    },
    {
      id: "griha-pravesh",
      name: "Housewarming",
      sanskrit: "Griha Pravesha",
      glyph: "🏡",
      gradient: "g3",
      summary: "Blessing a new home.",
      meaning: "Before living in a new home, families perform this ceremony to purify the space and invite peace and prosperity.",
      steps: [
        "Enter with your right foot first, carrying a kalash (pot) of water topped with mango leaves and a coconut.",
        "Boil milk in the new kitchen until it overflows, a sign of abundance.",
        "Light a lamp and offer prayers to Ganesha and Lakshmi.",
        "Sprinkle water in each room.",
        "Share a meal with family and friends."
      ],
      withPriest: "A priest may perform a Vastu shanti puja and a havan."
    },
    {
      id: "antyeshti",
      name: "Last Rites",
      sanskrit: "Antyeshti",
      glyph: "🕯️",
      gradient: "g8",
      summary: "Honouring the departed and supporting the soul's journey.",
      meaning: "Antyeshti, the “final sacrifice,” returns the body to the elements and helps the soul move on. A period of mourning follows, and ancestors are remembered each year during Pitru Paksha.",
      steps: [
        "The body is bathed, dressed in clean clothes and placed with the head facing south.",
        "Family members chant prayers and the name of God.",
        "Cremation is performed, usually lit by a close family member.",
        "Ashes are later immersed in a holy river or flowing water.",
        "A mourning period of 10 to 13 days ends with the shraddha ceremony and a meal for family and the community."
      ],
      withPriest: "Funeral homes in many countries can arrange a Hindu priest and cremation that follows these customs."
    }
  ],

  /* ------------------------------------------------------------------ */
  /* Prayers & mantras                                                   */
  /* ------------------------------------------------------------------ */
  prayers: [
    {
      id: "gayatri",
      name: "Gayatri Mantra",
      deity: "Savitr (the Sun)",
      time: "Dawn, noon and dusk",
      glyph: "☀️",
      gradient: "g5",
      source: "Rig Veda 3.62.10",
      sanskrit: "ॐ भूर्भुवः स्वः\nतत्सवितुर्वरेण्यं\nभर्गो देवस्य धीमहि\nधियो यो नः प्रचोदयात्",
      transliteration: "Om bhūr bhuvaḥ svaḥ\ntat savitur vareṇyaṃ\nbhargo devasya dhīmahi\ndhiyo yo naḥ pracodayāt",
      meaning: "We meditate on the radiant light of the divine Sun, which fills the earth, the sky and the heavens. May it awaken and guide our minds."
    },
    {
      id: "morning",
      name: "Morning Prayer",
      deity: "Lakshmi, Saraswati, Govinda",
      time: "On waking",
      glyph: "🌅",
      gradient: "g1",
      source: "Traditional",
      sanskrit: "कराग्रे वसते लक्ष्मीः\nकरमध्ये सरस्वती\nकरमूले तु गोविन्दः\nप्रभाते करदर्शनम्",
      transliteration: "Karāgre vasate lakṣmīḥ\nkaramadhye sarasvatī\nkaramūle tu govindaḥ\nprabhāte karadarśanam",
      meaning: "Lakshmi dwells at the fingertips, Saraswati in the palm and Govinda at the base of the hand. So look at your hands on waking.\n\nA reminder that prosperity, knowledge and the divine are present in the work of our own hands."
    },
    {
      id: "ganesha",
      name: "Vakratunda Mahakaya",
      deity: "Ganesha",
      time: "Before any new task",
      glyph: "🐘",
      gradient: "g5",
      source: "Traditional",
      sanskrit: "वक्रतुण्ड महाकाय\nसूर्यकोटि समप्रभ\nनिर्विघ्नं कुरु मे देव\nसर्वकार्येषु सर्वदा",
      transliteration: "Vakratuṇḍa mahākāya\nsūryakoṭi samaprabha\nnirvighnaṃ kuru me deva\nsarvakāryeṣu sarvadā",
      meaning: "O Lord with the curved trunk and mighty body, radiant as a million suns: please remove the obstacles from all my work, always."
    },
    {
      id: "shiva",
      name: "Om Namah Shivaya",
      deity: "Shiva",
      time: "Any time; ideal for japa",
      glyph: "🔱",
      gradient: "g2",
      source: "Krishna Yajurveda (Sri Rudram)",
      sanskrit: "ॐ नमः शिवाय",
      transliteration: "Om namaḥ śivāya",
      meaning: "I bow to Shiva, the auspicious one and the inner Self.\n\nThe five syllables (na-maḥ-śi-vā-ya) are also linked to the five elements."
    },
    {
      id: "mahamrityunjaya",
      name: "Mahamrityunjaya Mantra",
      deity: "Shiva",
      time: "For healing and protection",
      glyph: "🌿",
      gradient: "g3",
      source: "Rig Veda 7.59.12",
      sanskrit: "ॐ त्र्यम्बकं यजामहे\nसुगन्धिं पुष्टिवर्धनम्\nउर्वारुकमिव बन्धनान्\nमृत्योर्मुक्षीय मामृतात्",
      transliteration: "Om tryambakaṃ yajāmahe\nsugandhiṃ puṣṭivardhanam\nurvārukam iva bandhanān\nmṛtyor mukṣīya māmṛtāt",
      meaning: "We worship the three-eyed one, who is fragrant and nourishes all beings. As a ripe cucumber falls easily from its vine, may we be freed from death, but not from immortality."
    },
    {
      id: "saraswati",
      name: "Saraswati Vandana",
      deity: "Saraswati",
      time: "Before study",
      glyph: "🪷",
      gradient: "g6",
      source: "Traditional",
      sanskrit: "सरस्वति नमस्तुभ्यं\nवरदे कामरूपिणि\nविद्यारम्भं करिष्यामि\nसिद्धिर्भवतु मे सदा",
      transliteration: "Sarasvati namastubhyaṃ\nvarade kāmarūpiṇi\nvidyārambhaṃ kariṣyāmi\nsiddhir bhavatu me sadā",
      meaning: "Salutations to you, Saraswati, giver of blessings who takes any form. I am beginning my studies; may I always succeed."
    },
    {
      id: "asato-ma",
      name: "Asato Ma",
      deity: "Brahman",
      time: "Any time",
      glyph: "🪔",
      gradient: "g7",
      source: "Brihadaranyaka Upanishad 1.3.28",
      sanskrit: "असतो मा सद्गमय\nतमसो मा ज्योतिर्गमय\nमृत्योर्मा अमृतं गमय\nॐ शान्तिः शान्तिः शान्तिः",
      transliteration: "Asato mā sad gamaya\ntamaso mā jyotir gamaya\nmṛtyor mā amṛtaṃ gamaya\nOm śāntiḥ śāntiḥ śāntiḥ",
      meaning: "Lead me from the unreal to the real.\nLead me from darkness to light.\nLead me from death to immortality.\nOm, peace, peace, peace."
    },
    {
      id: "sahana",
      name: "Om Saha Navavatu",
      deity: "Brahman",
      time: "Before learning together",
      glyph: "🤝",
      gradient: "g4",
      source: "Taittiriya Upanishad 2.2.2",
      sanskrit: "ॐ सह नाववतु\nसह नौ भुनक्तु\nसह वीर्यं करवावहै\nतेजस्वि नावधीतमस्तु\nमा विद्विषावहै\nॐ शान्तिः शान्तिः शान्तिः",
      transliteration: "Om saha nāv avatu\nsaha nau bhunaktu\nsaha vīryaṃ karavāvahai\ntejasvi nāv adhītam astu\nmā vidviṣāvahai\nOm śāntiḥ śāntiḥ śāntiḥ",
      meaning: "May we be protected together. May we be nourished together. May we work together with energy. May our study be enlightening. May there be no ill will between us. Om, peace, peace, peace."
    },
    {
      id: "purnamadah",
      name: "Purnamadah",
      deity: "Brahman",
      time: "Opening or closing prayer",
      glyph: "⭕",
      gradient: "g8",
      source: "Isha Upanishad, invocation",
      sanskrit: "ॐ पूर्णमदः पूर्णमिदं\nपूर्णात्पूर्णमुदच्यते\nपूर्णस्य पूर्णमादाय\nपूर्णमेवावशिष्यते\nॐ शान्तिः शान्तिः शान्तिः",
      transliteration: "Om pūrṇam adaḥ pūrṇam idaṃ\npūrṇāt pūrṇam udacyate\npūrṇasya pūrṇam ādāya\npūrṇam evāvaśiṣyate\nOm śāntiḥ śāntiḥ śāntiḥ",
      meaning: "That is whole; this is whole. From wholeness, wholeness arises. When wholeness is taken from wholeness, wholeness remains. Om, peace, peace, peace."
    },
    {
      id: "hare-krishna",
      name: "Maha Mantra",
      deity: "Krishna & Rama",
      time: "Any time; ideal for japa",
      glyph: "🦚",
      gradient: "g2",
      source: "Kali-Santarana Upanishad",
      sanskrit: "हरे राम हरे राम\nराम राम हरे हरे\nहरे कृष्ण हरे कृष्ण\nकृष्ण कृष्ण हरे हरे",
      transliteration: "Hare Rāma Hare Rāma\nRāma Rāma Hare Hare\nHare Kṛṣṇa Hare Kṛṣṇa\nKṛṣṇa Kṛṣṇa Hare Hare",
      meaning: "A call to the divine using the names Hari, Rama and Krishna, asking to be drawn into loving service."
    }
  ]
};
