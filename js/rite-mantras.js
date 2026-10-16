/* Dharma Path: the mantras said during each rite of passage, in order, keyed by rite id.
   use: "core" marks a mantra central to the rite, "some" one said only in some traditions.
   Each: { basis, groups: [{ title, mantras: [{ at, do, sa, tr, en, src, use?, read? }] }] }.
   The Sanskrit is taken from the Grihya Sutras (chiefly Paraskara, from Sanskrit Wikisource, and
   Ashvalayana, from GRETIL) and from the Vedic samhitas in texts/; the English is our own. */
window.CONTENT.riteMantras = {
 "simanta": {
  "basis": "This sequence follows the Paraskara Grihya Sutra (1.11, 1.14 and 1.15), the White Yajurveda manual that most North Indian and Caribbean pandits follow, with the Rig Veda blessing for conception that the Brihadaranyaka Upanishad and the other Grihya Sutras prescribe, and a few verses from other traditions marked as optional. Today the three rites before birth are rarely done separately: a family priest usually performs a short Simantonnayana with a havan, often folding in Pumsavana verses, before the women's celebration.",
  "groups": [
   {
    "title": "Garbhadhana: praying for a child",
    "mantras": [
     {
      "at": "Touching her heart",
      "do": "In Paraskara's rite for the couple's first nights together, repeated in the months after, the husband reaches over his wife's right shoulder, touches her heart and says:",
      "sa": "यत्ते सुसीमे हृदयं दिवि चन्द्रमसि श्रितम् ।\nवेदाहं तन्मां तद्विद्यात्\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतम् ॥",
      "tr": "yatte susīme hṛdayaṃ divi candramasi śritam\nvedāhaṃ tanmāṃ tadvidyāt\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śatam",
      "en": "Lovely one, your heart that dwells in heaven, in the moon: I know it, and may it know me. May we see a hundred autumns, live a hundred autumns, hear a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.11.9–10"
     },
     {
      "at": "Blessing for conception",
      "do": "The husband blesses his wife with the first of three Rig Veda verses that the Brihadaranyaka Upanishad and several Grihya Sutras give for this moment:",
      "sa": "विष्णुर्योनिं कल्पयतु त्वष्टा रूपाणि पिंशतु ।\nआ सिञ्चतु प्रजापतिर्धाता गर्भं दधातु ते ॥",
      "tr": "viṣṇuryoniṃ kalpayatu tvaṣṭā rūpāṇi piṃśatu\nā siñcatu prajāpatirdhātā garbhaṃ dadhātu te",
      "en": "May Vishnu make the womb ready, may Tvashtr shape the forms; may Prajapati pour in the seed, and may Dhatr set the child within you.",
      "src": "Rig Veda 10.184.1; Brihadaranyaka Upanishad 6.4.21; Apastamba Grihya Sutra 8.13; Jaiminiya Grihya Sutra 1.22; Manava Grihya Sutra 2.18.2",
      "use": "core",
      "read": "#/read/rigveda/11/184?v=1"
     }
    ]
   },
   {
    "title": "Pumsavana: blessing the life within",
    "mantras": [
     {
      "at": "Drops of banyan",
      "do": "In the second or third month, before the baby moves, the husband crushes fresh banyan shoots in water at night and puts a few drops into his wife's right nostril with two verses. The first:",
      "sa": "हिरण्यगर्भः समवर्तताग्रे भूतस्य जातः पतिरेक आसीत् ।\nस दाधार पृथिवीं द्यामुतेमां कस्मै देवाय हविषा विधेम ॥",
      "tr": "hiraṇyagarbhaḥ samavartatāgre bhūtasya jātaḥ patireka āsīt\nsa dādhāra pṛthivīṃ dyāmutemāṃ kasmai devāya haviṣā vidhema",
      "en": "In the beginning the Golden Womb arose; as soon as he was born he was the one lord of all that is. He holds up the earth and this sky. Which god shall we worship with our offering?",
      "src": "Paraskara Grihya Sutra 1.14.3; Vajasaneyi Samhita 13.4 (also Rig Veda 10.121.1)",
      "use": "core",
      "read": "#/read/yajurveda/13/1?v=4"
     },
     {
      "at": "Shaped from water and earth",
      "do": "He continues with the second verse:",
      "sa": "अद्भ्यः सम्भृतः पृथिव्यै रसाच्च विश्वकर्मणः समवर्तताग्रे ।\nतस्य त्वष्टा विदधद्रूपमेति तन्मर्त्यस्य देवत्वमाजानमग्रे ॥",
      "tr": "adbhyaḥ sambhṛtaḥ pṛthivyai rasācca viśvakarmaṇaḥ samavartatāgre\ntasya tvaṣṭā vidadhadrūpameti tanmartyasya devatvamājānamagre",
      "en": "Gathered from the waters and from the sap of the earth, he came forth in the beginning from Vishvakarman, maker of all. Tvashtr goes on, shaping his form: this is a mortal's divinity, his birth from the very first.",
      "src": "Paraskara Grihya Sutra 1.14.3; Vajasaneyi Samhita 31.17",
      "read": "#/read/yajurveda/31/1?v=17"
     }
    ]
   },
   {
    "title": "Simantonnayana: parting the hair",
    "mantras": [
     {
      "at": "Parting her hair",
      "do": "With his wife seated on a soft seat west of the fire, the husband gently parts her hair upwards from the front with darbha grass, a porcupine quill and a sprig of unripe udumbara figs, saying (once, or once with each word):",
      "sa": "भूर्भुवः स्वः",
      "tr": "bhūrbhuvaḥ svaḥ",
      "en": "Earth, sky, heaven!",
      "src": "Paraskara Grihya Sutra 1.15.4–5",
      "use": "core"
     },
     {
      "at": "Calling on the full-moon goddess",
      "do": "Rig Veda priests also invoke Raka, goddess of the full moon, with this verse; Gobhila has it said as the hair is parted with a spindle full of thread:",
      "sa": "राकामहं सुहवां सुष्टुती हुवे शृणोतु नः सुभगा बोधतु त्मना ।\nसीव्यत्वपः सूच्याच्छिद्यमानया ददातु वीरं शतदायमुक्थ्यम् ॥",
      "tr": "rākāmahaṃ suhavāṃ suṣṭutī huve śṛṇotu naḥ subhagā bodhatu tmanā\nsīvyatvapaḥ sūcyācchidyamānayā dadātu vīraṃ śatadāyamukthyam",
      "en": "With sweet praise I call on Raka, who comes when she is called. May the gracious one hear us and take notice. May she sew her work with a needle that never breaks, and give us a brave child, worthy of praise and rich in blessings.",
      "src": "Rig Veda 2.32.4; Ashvalayana Grihya Sutra 1.14.3; Sankhayana Grihya Sutra 1.22.12; Gobhila Grihya Sutra 2.7.7",
      "use": "some",
      "read": "#/read/rigveda/3/32?v=4"
     },
     {
      "at": "Tying the figs",
      "do": "He ties the udumbara figs on a thread of three strands and puts it on her, saying:",
      "sa": "अयमूर्जावतो वृक्ष उर्जीव फलिनी भव",
      "tr": "ayamūrjāvato vṛkṣa urjīva phalinī bhava",
      "en": "This tree is full of sap. Full of life like it, may you bear fruit.",
      "src": "Paraskara Grihya Sutra 1.15.6"
     },
     {
      "at": "What do you see?",
      "do": "In some traditions he has her look into a bronze bowl of water with gold in it and asks her the question; she answers:",
      "sa": "भूर्भुवः स्वः किं पश्यसि ।\nप्रजां पशून्सौभाग्यं मह्यं दीर्घमायुः पत्युः ॥",
      "tr": "bhūrbhuvaḥ svaḥ kiṃ paśyasi\nprajāṃ paśūnsaubhāgyaṃ mahyaṃ dīrghamāyuḥ patyuḥ",
      "en": "Earth, sky, heaven: what do you see? (She answers:) Children, plenty, good fortune for me, and a long life for my husband.",
      "src": "Jaiminiya Grihya Sutra 1.7 (compare Gobhila Grihya Sutra 2.7.9–10)",
      "use": "some"
     },
     {
      "at": "Music for mother and child",
      "do": "The husband asks two lute players to sing of the king, or of someone braver still; some have them sing this verse, naming the river near the family home:",
      "sa": "सोम एव नो राजेमा मानुषीः प्रजाः ।\nअविमुक्तचक्र आसीरंस्तीरे तुभ्यमसौ ॥",
      "tr": "soma eva no rājemā mānuṣīḥ prajāḥ\navimuktacakra āsīraṃstīre tubhyamasau",
      "en": "Soma alone is our king, king of all these people. With their wheels at rest, may they live in peace on your banks, O (name of the river).",
      "src": "Paraskara Grihya Sutra 1.15.7–8"
     }
    ]
   }
  ]
 },
 "birth": {
  "basis": "The birth blessings follow the Paraskara Grihya Sutra 1.16, with two verses that Paraskara gives for a father greeting his son (1.18) and that other manuals place at the birth itself. Paraskara gives only rules for the name (1.17), no naming mantra, so the naming verses here come from other traditions and are optional. Today the birth blessings are usually performed together with the naming on the naming day, and a family priest chooses verses from his own manual.",
  "groups": [
   {
    "title": "Jatakarma: welcoming the newborn",
    "mantras": [
     {
      "at": "Honey and ghee",
      "do": "Before the cord is cut, the father touches honey and ghee to the baby's lips with his ring finger, a gold ring between, and says:",
      "sa": "भूस्त्वयि दधामि भुवस्त्वयि दधामि स्वस्त्वयि दधामि ।\nभूर्भुवः स्वः सर्वं त्वयि दधामि ॥",
      "tr": "bhūstvayi dadhāmi bhuvastvayi dadhāmi svastvayi dadhāmi\nbhūrbhuvaḥ svaḥ sarvaṃ tvayi dadhāmi",
      "en": "I place the earth in you. I place the sky in you. I place heaven in you. Earth, sky and heaven: I place everything in you.",
      "src": "Paraskara Grihya Sutra 1.16.3–4",
      "use": "core"
     },
     {
      "at": "Blessing for long life",
      "do": "Close to the baby's navel or right ear, the father murmurs eight such blessings, naming in turn Agni, Soma, Brahman, the gods, the rishis, the ancestors, sacrifice and the ocean. The first:",
      "sa": "अग्निरायुष्मान्त्स वनस्पतिभिरायुष्मांस्तेन त्वाऽऽयुषाऽऽयुष्मन्तं करोमि ।",
      "tr": "agnirāyuṣmāntsa vanaspatibhirāyuṣmāṃstena tvā''yuṣā''yuṣmantaṃ karomi",
      "en": "Agni is long-lived; through the trees he lives long. By that long life I make you long-lived.",
      "src": "Paraskara Grihya Sutra 1.16.5–6",
      "use": "core"
     },
     {
      "at": "Three lifetimes",
      "do": "Three times the father says:",
      "sa": "त्र्यायुषं जमदग्नेः कश्यपस्य त्र्यायुषम् ।\nयद्देवेषु त्र्यायुषं तन्नो अस्तु त्र्यायुषम् ॥",
      "tr": "tryāyuṣaṃ jamadagneḥ kaśyapasya tryāyuṣam\nyaddeveṣu tryāyuṣaṃ tanno astu tryāyuṣam",
      "en": "The threefold life of Jamadagni, the threefold life of Kashyapa, the threefold life the gods enjoy: may that threefold life be ours.",
      "src": "Paraskara Grihya Sutra 1.16.7; Vajasaneyi Samhita 3.62",
      "read": "#/read/yajurveda/3/1?v=62"
     },
     {
      "at": "Blessing the birthplace",
      "do": "He speaks to the place where the baby was born:",
      "sa": "वेद ते भूमि हृदयं दिवि चन्द्रमसि श्रितम् ।\nवेदाहं तन्मां तद्विद्यात्\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतम् ॥",
      "tr": "veda te bhūmi hṛdayaṃ divi candramasi śritam\nvedāhaṃ tanmāṃ tadvidyāt\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śatam",
      "en": "Earth, I know your heart that dwells in heaven, in the moon. I know it; may it know me. May we see a hundred autumns, live a hundred autumns, hear a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.16.17",
      "use": "some"
     },
     {
      "at": "Be strong as a stone",
      "do": "Touching the baby, the father says:",
      "sa": "अश्मा भव परशुर्भव हिरण्यमस्रुतं भव ।\nआत्मा वै पुत्रनामाऽसि स जीव शरदः शतम् ॥",
      "tr": "aśmā bhava paraśurbhava hiraṇyamasrutaṃ bhava\nātmā vai putranāmā'si sa jīva śaradaḥ śatam",
      "en": "Be firm as a stone, keen as an axe, pure as gold that never fades. You are my own self, now called my child: live a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.16.18",
      "use": "core"
     },
     {
      "at": "Born of my heart",
      "do": "Holding the baby's head, he says this verse, which Paraskara gives for a father coming home to his son and the Varaha and Jaiminiya Grihya Sutras say at the birth:",
      "sa": "अङ्गादङ्गात्संभवसि हृदयादधिजायसे ।\nआत्मा वै पुत्रनामाऽसि स जीव शरदः शतम् ॥",
      "tr": "aṅgādaṅgātsaṃbhavasi hṛdayādadhijāyase\nātmā vai putranāmā'si sa jīva śaradaḥ śatam",
      "en": "From every limb of mine you have come into being; you are born from my heart. You are my own self, now called my child: live a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.18.2; Varaha Grihya Sutra 2.5; Jaiminiya Grihya Sutra 1.8"
     },
     {
      "at": "The secret name",
      "do": "In some traditions the father asks the baby who it is and gives it a secret name, here 'Veda', known only to the parents; the everyday name is given on the naming day:",
      "sa": "को ऽसि कतमो ऽसि । सं मासं प्रविशासौ ।\nवेदो ऽसि ॥",
      "tr": "ko 'si katamo 'si saṃ māsaṃ praviśāsau\nvedo 'si",
      "en": "Who are you? Which one are you? Enter into the month, (name)! You are Veda, sacred knowledge.",
      "src": "Jaiminiya Grihya Sutra 1.8; compare Brihadaranyaka Upanishad 6.4.26, Sankhayana Grihya Sutra 1.24.4–5 and Apastamba Grihya Sutra 15.2–3",
      "use": "some"
     },
     {
      "at": "Honouring the mother",
      "do": "The father then speaks these words of praise to the mother:",
      "sa": "इडासि मैत्रावरुणी वीरे वीरमजीजनथाः ।\nसा त्वं वीरवती भव याऽस्मान्वीरवतोऽकरत् ॥",
      "tr": "iḍāsi maitrāvaruṇī vīre vīramajījanathāḥ\nsā tvaṃ vīravatī bhava yā'smānvīravato'karat",
      "en": "You are Ida, daughter of Mitra and Varuna. Strong woman, you have borne a strong child. Be blessed with strong children, you who have blessed us with a strong child.",
      "src": "Paraskara Grihya Sutra 1.16.19 (also Brihadaranyaka Upanishad 6.4.28)",
      "read": "#/read/upanishads/10/6?v=71"
     },
     {
      "at": "The first feed",
      "do": "The father washes the mother's right breast and gives it to the baby with this verse; the left breast follows with a verse to Sarasvati (Vajasaneyi Samhita 38.5):",
      "sa": "इमं स्तनमूर्जस्वन्तं धयापां प्रपीनमग्ने सरिरस्य मध्ये ।\nउत्सं जुषस्व मधुमन्तमर्वन्त्समुद्रियं सदनमा विशस्व ॥",
      "tr": "imaṃ stanamūrjasvantaṃ dhayāpāṃ prapīnamagne sarirasya madhye\nutsaṃ juṣasva madhumantamarvantsamudriyaṃ sadanamā viśasva",
      "en": "Drink this breast, rich in strength and swelling with the waters, young Agni, here in the midst of the flood. Enjoy this honey-sweet spring, swift one, and come into your home.",
      "src": "Paraskara Grihya Sutra 1.16.20–21; Vajasaneyi Samhita 17.87",
      "use": "some",
      "read": "#/read/yajurveda/17/1?v=87"
     },
     {
      "at": "Waters, keep watch",
      "do": "He sets a pot of water near the mother's head, saying:",
      "sa": "आपो देवेषु जाग्रथ यथा देवेषु जाग्रथ ।\nएवमस्यां सूतिकायांसपुत्रिकायां जाग्रथ ॥",
      "tr": "āpo deveṣu jāgratha yathā deveṣu jāgratha\nevamasyāṃ sūtikāyāṃsaputrikāyāṃ jāgratha",
      "en": "Waters, you keep watch among the gods. As you keep watch among the gods, so keep watch over this new mother and her child.",
      "src": "Paraskara Grihya Sutra 1.16.22",
      "use": "some"
     }
    ]
   },
   {
    "title": "Namakarana: giving the name",
    "mantras": [
     {
      "at": "A stream of life",
      "do": "In the Atharva Veda tradition, after the opening offerings, an unbroken stream of water is poured into the baby's right hand with the long-life hymn that begins:",
      "sa": "आ रभस्वेमाममृतस्य श्नुष्टिमच्छिद्यमाना जरदष्टिरस्तु ते ।\nअसुं त आयुः पुनरा भरामि रजस्तमो मोप गा मा प्र मेष्ठाः ॥",
      "tr": "ā rabhasvemāmamṛtasya śnuṣṭimacchidyamānā jaradaṣṭirastu te\nasuṃ ta āyuḥ punarā bharāmi rajastamo mopa gā mā pra meṣṭhāḥ",
      "en": "Hold on to this, a gift of the deathless; may your life run on unbroken to old age. I bring you breath and life: do not go into mist and darkness, do not fade away.",
      "src": "Kaushika Sutra 58.14; Atharva Veda 8.2.1",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=1"
     },
     {
      "at": "Calling the child by name",
      "do": "The father gives the name, chosen by the rules of Paraskara 1.17, then kisses the baby's head and blesses the child, saying the new name where the verse says 'asau':",
      "sa": "प्रजापतेष्ट्वा हिंकारेणावजिघ्रामि सहस्रायुषाऽसौ जीव शरदः शतम्",
      "tr": "prajāpateṣṭvā hiṃkāreṇāvajighrāmi sahasrāyuṣā'sau jīva śaradaḥ śatam",
      "en": "With Prajapati's tender call, like a cow's to her calf, I kiss you. With a life a thousand strong, (name), live a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.17.1–4 and 1.18.3",
      "use": "some"
     },
     {
      "at": "Whispering in the right ear",
      "do": "Three times the father whispers this verse into the baby's right ear, and another (Rig Veda 2.21.6) into the left. Paraskara gives these for a father greeting his son, Ashvalayana for the birth:",
      "sa": "अस्मे प्र यन्धि मघवन्नृजीषिन्निन्द्र रायो विश्ववारस्य भूरेः ।\nअस्मे शतं शरदो जीवसे धा अस्मे वीराञ्छश्वत इन्द्र शिप्रिन् ॥",
      "tr": "asme pra yandhi maghavannṛjīṣinnindra rāyo viśvavārasya bhūreḥ\nasme śataṃ śarado jīvase dhā asme vīrāñchaśvata indra śiprin",
      "en": "Generous Indra, eager and strong, give us riches in plenty that all desire. Give us a hundred autumns to live, and brave children, Indra, mighty one.",
      "src": "Paraskara Grihya Sutra 1.18.4–5; Rig Veda 3.36.10; Ashvalayana Grihya Sutra 1.15.3",
      "use": "some",
      "read": "#/read/rigveda/4/36?v=10"
     },
     {
      "at": "New clothes",
      "do": "In the Atharva Veda tradition the baby is then wrapped in a new cloth with this verse:",
      "sa": "यत् ते वासः परिधानं यां नीविं कृणुषे त्वम् ।\nशिवं ते तन्वे३तत् कृण्मः संस्पर्शेऽद्रूक्ष्णमस्तु ते ॥",
      "tr": "yat te vāsaḥ paridhānaṃ yāṃ nīviṃ kṛṇuṣe tvam\nśivaṃ te tanvetat kṛṇmaḥ saṃsparśe'drūkṣṇamastu te",
      "en": "The clothes you wear, the cloth you tie around you: we make them kind to your body. May they be soft to your touch.",
      "src": "Kaushika Sutra 58.17; Atharva Veda 8.2.16",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=16"
     }
    ]
   }
  ]
 },
 "nishkramana": {
  "basis": "Paraskara Grihya Sutra 1.17.5–6 gives the whole rite in one line: in the fourth month the child is taken out and shown the sun with the verse 'That eye'. Showing the moon comes from other traditions: the Atharva Veda manual (Kaushika Sutra) carries the child out with verses asking the sun and moon to guard it, and Gobhila has the father worship the moon with the baby. A family priest often adds the Gayatri, as in the daily worship of the sun.",
  "groups": [
   {
    "title": null,
    "mantras": [
     {
      "at": "Greeting the sun",
      "do": "In the fourth month the father carries the baby outside and turns the child toward the sun, saying:",
      "sa": "तच्चक्षुर्देवहितं पुरस्ताच्छुक्रमुच्चरत् ।\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतं\nप्र ब्रवाम शरदः शतमदीनाः स्याम शरदः शतं भूयश्च शरदः शतात् ॥",
      "tr": "taccakṣurdevahitaṃ purastācchukramuccarat\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śataṃ\npra bravāma śaradaḥ śatamadīnāḥ syāma śaradaḥ śataṃ bhūyaśca śaradaḥ śatāt",
      "en": "That eye, set in place by the gods, rises shining in the east. May we see a hundred autumns, live a hundred autumns, hear a hundred autumns, speak for a hundred autumns, live free from want for a hundred autumns, and for more than a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.17.5–6; Vajasaneyi Samhita 36.24",
      "use": "core",
      "read": "#/read/yajurveda/36/1?v=24"
     },
     {
      "at": "The Gayatri",
      "do": "Many priests add the Gayatri, the prayer to the sun as Savitr, which Katyayana's bathing rules join with 'That eye' in the daily worship of the sun:",
      "sa": "भूर्भुवः स्वः ।\nतत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि ।\nधियो यो नः प्रचोदयात् ॥",
      "tr": "bhūrbhuvaḥ svaḥ\ntatsaviturvareṇyaṃ bhargo devasya dhīmahi\ndhiyo yo naḥ pracodayāt",
      "en": "Earth, sky, heaven. We meditate on the glorious light of the divine Savitr: may it inspire our minds.",
      "src": "Vajasaneyi Samhita 36.3; Katyayana's Snana Sutra (a supplement to Paraskara)",
      "read": "#/read/yajurveda/36/1?v=3"
     },
     {
      "at": "The first step outside",
      "do": "In the Atharva Veda tradition the baby is carried out of the house for the first time with two verses. The first:",
      "sa": "शिवे ते स्तां द्यावापृथिवी असंतापे अभिश्रियौ ।\nशं ते सूर्य आ तपतु शं वातो वातु ते हृदे ।\nशिवा अभि क्षरन्तु त्वापो दिव्याः पयस्वतीः ॥",
      "tr": "śive te stāṃ dyāvāpṛthivī asaṃtāpe abhiśriyau\nśaṃ te sūrya ā tapatu śaṃ vāto vātu te hṛde\nśivā abhi kṣarantu tvāpo divyāḥ payasvatīḥ",
      "en": "May heaven and earth be kind to you, gentle and full of blessings. May the sun shine kindly on you, may the wind blow softly to your heart, and may the heavenly waters, rich as milk, flow kindly over you.",
      "src": "Kaushika Sutra 58.18; Atharva Veda 8.2.14",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=14"
     },
     {
      "at": "Sun and moon, guard this child",
      "do": "The second verse asks the sun and the moon together to protect the child; it suits the evening, when the baby is shown the moon:",
      "sa": "शिवास्ते सन्त्वोषधय उत् त्वाहार्षमधरस्या उत्तरां पृथिवीमभि ।\nतत्र त्वादित्यौ रक्षतां सूर्याचन्द्रमसावुभा ॥",
      "tr": "śivāste santvoṣadhaya ut tvāhārṣamadharasyā uttarāṃ pṛthivīmabhi\ntatra tvādityau rakṣatāṃ sūryācandramasāvubhā",
      "en": "May the plants be kind to you. I have lifted you up from the lower earth to the higher; there may the two lights of heaven, the sun and the moon, both guard you.",
      "src": "Kaushika Sutra 58.18; Atharva Veda 8.2.15",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=15"
     },
     {
      "at": "Entrusting to day and night",
      "do": "The child is then given into the care of day and night:",
      "sa": "अह्ने च त्वा रात्रये चोभाभ्यां परि दद्मसि ।\nअरायेभ्यो जिघत्सुभ्य इमं मे परि रक्षत ॥",
      "tr": "ahne ca tvā rātraye cobhābhyāṃ pari dadmasi\narāyebhyo jighatsubhya imaṃ me pari rakṣata",
      "en": "We give you into the care of Day and of Night, of both together. Guard this child of mine from every hungry, harmful spirit.",
      "src": "Kaushika Sutra 58.18, 58.20; Atharva Veda 8.2.20",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=20"
     }
    ]
   }
  ]
 },
 "annaprashan": {
  "basis": "This follows Paraskara Grihya Sutra 1.19: two offerings of ghee with verses on speech and strength, four offerings of the cooked food, and then the first feeding. The verse 'Lord of food' comes from the Rig Veda and Sama Veda manuals and is widely used, and the last two verses are from the Atharva Veda tradition. A family priest may use only some of these, and the first food today is usually kheer or rice with ghee rather than the meats and fish Paraskara lists.",
  "groups": [
   {
    "title": null,
    "mantras": [
     {
      "at": "Offering for the gift of speech",
      "do": "After cooking the rice, the father or priest offers ghee into the fire with a verse to the goddess Speech:",
      "sa": "देवीं वाचमजनयन्त देवास्तां विश्वरूपाः पशवो वदन्ति ।\nसा नो मन्द्रेषमूर्जं दुहाना धेनुर्वागस्मानुपसुष्टुतैतु स्वाहा ॥",
      "tr": "devīṃ vācamajanayanta devāstāṃ viśvarūpāḥ paśavo vadanti\nsā no mandreṣamūrjaṃ duhānā dhenurvāgasmānupasuṣṭutaitu svāhā",
      "en": "The gods brought forth the goddess Speech, and creatures of every kind speak her. May she, the joyful one, like a cow giving food and strength, come to us, Speech, well praised. Svaha!",
      "src": "Paraskara Grihya Sutra 1.19.2; Rig Veda 8.100.11",
      "read": "#/read/rigveda/9/100?v=11"
     },
     {
      "at": "Offering for strength",
      "do": "A second offering of ghee follows with this verse:",
      "sa": "वाजो नो अद्य प्र सुवाति दानं वाजो देवाँ२ ऋतुभिः कल्पयाति ।\nवाजो हि मा सर्ववीरं जजान विश्वा आशा वाजपतिर्जयेयम् ॥",
      "tr": "vājo no adya pra suvāti dānaṃ vājo devā~ ṛtubhiḥ kalpayāti\nvājo hi mā sarvavīraṃ jajāna viśvā āśā vājapatirjayeyam",
      "en": "May nourishment bring us its gifts today; nourishment keeps the gods in step with the seasons. Nourishment has made me strong in all my family: as master of nourishment, may I win every direction.",
      "src": "Paraskara Grihya Sutra 1.19.3; Vajasaneyi Samhita 18.33",
      "read": "#/read/yajurveda/18/1?v=33"
     },
     {
      "at": "Offerings of the food",
      "do": "Four offerings of the cooked rice are made into the fire, one with each phrase:",
      "sa": "प्राणेनान्नमशीय स्वाहाऽपानेन गन्धानशीय स्वाहा ।\nचक्षुषा रूपाण्यशीय स्वाहा श्रोत्रेण यशोऽशीय स्वाहा ॥",
      "tr": "prāṇenānnamaśīya svāhā'pānena gandhānaśīya svāhā\ncakṣuṣā rūpāṇyaśīya svāhā śrotreṇa yaśo'śīya svāhā",
      "en": "Through my breath may I enjoy food. Svaha! Through my breathing out may I enjoy fragrance. Svaha! Through my eyes may I enjoy all that is beautiful. Svaha! Through my ears may I enjoy good fame. Svaha!",
      "src": "Paraskara Grihya Sutra 1.19.4",
      "use": "core"
     },
     {
      "at": "Blessing the food",
      "do": "Before the feeding, many priests bless the food with this verse, which the Rig Veda and Sama Veda manuals give for the child's first meal:",
      "sa": "अन्नपतेऽन्नस्य नो देह्यनमीवस्य शुष्मिणः ।\nप्र-प्र दातारं तारिष ऊर्जं नो धेहि द्विपदे चतुष्पदे ॥",
      "tr": "annapate'nnasya no dehyanamīvasya śuṣmiṇaḥ\npra-pra dātāraṃ tāriṣa ūrjaṃ no dhehi dvipade catuṣpade",
      "en": "Lord of food, give us food that is wholesome and strengthening. Carry the giver safely forward, and give strength to us, to people and to animals alike.",
      "src": "Vajasaneyi Samhita 11.83; Ashvalayana Grihya Sutra 1.16.5; Sankhayana Grihya Sutra 1.27.7; Jaiminiya Grihya Sutra 1.10",
      "read": "#/read/yajurveda/11/1?v=83"
     },
     {
      "at": "The first bite",
      "do": "Having set aside a little of every food and every flavour, the father feeds the baby, in silence or with the happy word 'hanta', for the Veda says that people live by that word:",
      "sa": "हन्त",
      "tr": "hanta",
      "en": "Here, take it!",
      "src": "Paraskara Grihya Sutra 1.19.5–6",
      "use": "core"
     },
     {
      "at": "Rice and barley",
      "do": "In the Atharva Veda tradition the baby is fed a little rice and barley with two verses. The first:",
      "sa": "शिवौ ते स्तां व्रीहियवावबलासावदोमधौ ।\nएतौ यक्ष्मं वि बाधेते एतौ मुञ्चतो अंहसः ॥",
      "tr": "śivau te stāṃ vrīhiyavāvabalāsāvadomadhau\netau yakṣmaṃ vi bādhete etau muñcato aṃhasaḥ",
      "en": "May rice and barley be kind to you, bringing no sickness, sweet to eat. They drive away illness; they set you free from harm.",
      "src": "Kaushika Sutra 58.19; Atharva Veda 8.2.18",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=18"
     },
     {
      "at": "All your food made wholesome",
      "do": "And the second:",
      "sa": "यदश्नासि यत् पिबसि धान्यं कृष्याः पयः ।\nयदाद्यं यदनाद्यं सर्वं ते अन्नमविषं कृणोमि ॥",
      "tr": "yadaśnāsi yat pibasi dhānyaṃ kṛṣyāḥ payaḥ\nyadādyaṃ yadanādyaṃ sarvaṃ te annamaviṣaṃ kṛṇomi",
      "en": "Whatever you eat, whatever you drink, grain from the fields or milk, food fit to eat or not, I make all your food free from harm.",
      "src": "Kaushika Sutra 58.19; Atharva Veda 8.2.19",
      "use": "some",
      "read": "#/read/atharvaveda/8/2?v=19"
     }
    ]
   }
  ]
 },
 "karnavedha": {
  "basis": "The ear-piercing rite is not described in the Paraskara Grihya Sutra or in the other Grihya Sutras in these sources; it comes from later supplements and manuals. 'May we hear what is good with our ears' is the verse most priests use, and the Sankhayana Grihya Sutra already uses it when touching the ears in other rites. A family priest usually adds a Ganesha puja and a short havan, and the piercing itself is done by a trained piercer.",
  "groups": [
   {
    "title": null,
    "mantras": [
     {
      "at": "Before the first ear",
      "do": "With the child in a parent's lap, the father or priest touches the ear to be pierced first (traditionally the right for a boy, the left for a girl) and recites:",
      "sa": "भद्रं कर्णेभिः शृणुयाम देवा भद्रं पश्येमाक्षभिर्यजत्राः ।\nस्थिरैरङ्गैस्तुष्टुवांसस्तनूभिर्व्यशेमहि देवहितं यदायुः ॥",
      "tr": "bhadraṃ karṇebhiḥ śṛṇuyāma devā bhadraṃ paśyemākṣabhiryajatrāḥ\nsthirairaṅgaistuṣṭuvāṃsastanūbhirvyaśemahi devahitaṃ yadāyuḥ",
      "en": "Gods, may we hear with our ears what is good. Holy ones, may we see with our eyes what is good. With strong limbs and bodies, singing your praise, may we live out the full life the gods have given.",
      "src": "Vajasaneyi Samhita 25.21 (Rig Veda 1.89.8); used for touching the ears in Sankhayana Grihya Sutra 3.8.6 and 5.5.11",
      "read": "#/read/yajurveda/25/1?v=21"
     },
     {
      "at": "Before the second ear",
      "do": "Some manuals, such as the Arya Samaj Sanskar Vidhi, use this verse for the other ear; it pictures something drawing close to the ear like a dear friend:",
      "sa": "वक्ष्यन्तीवेदा गनीगन्ति कर्णं प्रियं सखायं परिषस्वजाना ।\nयोषेव शिङ्क्ते वितताधि धन्वञ्ज्या इयं समने पारयन्ती ॥",
      "tr": "vakṣyantīvedā ganīganti karṇaṃ priyaṃ sakhāyaṃ pariṣasvajānā\nyoṣeva śiṅkte vitatādhi dhanvañjyā iyaṃ samane pārayantī",
      "en": "As if about to whisper, she comes close to the ear again and again, embracing it like a dear friend. Stretched on the bow, this bowstring hums like a young woman and carries us safely through the struggle.",
      "src": "Vajasaneyi Samhita 29.40 (Rig Veda 6.75.3)",
      "use": "some",
      "read": "#/read/yajurveda/29/1?v=40"
     },
     {
      "at": "A hundred autumns",
      "do": "Once the earrings are in, the next verse of the same hymn makes a fitting blessing; Sankhayana pairs the two:",
      "sa": "शतमिन्नु शरदो अन्ति देवा यत्रा नश्चक्रा जरसं तनूनाम् ।\nपुत्रासो यत्र पितरो भवन्ति मा नो मध्या रीरिषतायुर्गन्तोः ॥",
      "tr": "śataminnu śarado anti devā yatrā naścakrā jarasaṃ tanūnām\nputrāso yatra pitaro bhavanti mā no madhyā rīriṣatāyurgantoḥ",
      "en": "A hundred autumns lie before us, gods, within which you have set old age for our bodies, within which sons become fathers in their turn. Do not cut our life short on its way.",
      "src": "Vajasaneyi Samhita 25.22 (Rig Veda 1.89.9); Sankhayana Grihya Sutra 5.5.12",
      "use": "some",
      "read": "#/read/yajurveda/25/1?v=22"
     }
    ]
   }
  ]
 },
 "mundan": {
  "basis": "These are the mantras of the Chudakarana in the Paraskara Grihya Sutra (2.1), the manual of the White Yajurveda that most North Indian and Caribbean pandits follow, with the Vedic verses it quotes. A family priest usually adds a Ganesha puja and a short havan first, may say only some of these verses, and often lets the barber do most of the shaving after the father's first few symbolic cuts.",
  "groups": [
   {
    "title": null,
    "mantras": [
     {
      "at": "Warm water for the shave",
      "do": "The father pours warm water into a pot of cold water for the shaving, saying:",
      "sa": "उष्णेन वाय उदकेनेह्यदिते केशान्वप ॥",
      "tr": "uṣṇena vāya udakenehyadite keśānvapa",
      "en": "Come, Vayu, with warm water. Aditi, shave the hair.",
      "src": "Paraskara Grihya Sutra 2.1.6 (compare Atharva Veda 6.68.1–2)"
     },
     {
      "at": "Wetting the hair",
      "do": "After stirring in a little butter or curd, he takes some of the water and wets the hair above the child's right ear, saying:",
      "sa": "सवित्रा प्रसूता दैव्या आप उन्दन्तु ते तनूं ।\nदीर्घायुत्वाय वर्चसे ॥",
      "tr": "savitrā prasūtā daivyā āpa undantu te tanūṃ\ndīrghāyutvāya varcase",
      "en": "Sent by Savitr, may the divine waters soften your hair and bathe your body, for a long life and a bright one.",
      "src": "Paraskara Grihya Sutra 2.1.9"
     },
     {
      "at": "Taking up the razor",
      "do": "He sets three young kusha shoots in the wet hair, takes up the razor with the first line and begins to cut with the second:",
      "sa": "शिवो नामासि स्वधितिस्ते पिता नमस्ते अस्तु मा मा हिंसीः ।\nनि वर्तयाम्यायुषेऽन्नाद्याय प्रजननाय रायस्पोषाय सुप्रजास्त्वाय सुवीर्याय ॥",
      "tr": "śivo nāmāsi svadhitiste pitā namaste astu mā mā hiṃsīḥ\nni vartayāmyāyuṣe'nnādyāya prajananāya rāyaspoṣāya suprajāstvāya suvīryāya",
      "en": "Your name is Kindly, and the steel is your father. Honour to you: do me no harm. I cut this hair for long life and good food, for children to come, for growing wealth, for fine offspring and strength.",
      "src": "Paraskara Grihya Sutra 2.1.11; Vajasaneyi Samhita 3.63",
      "read": "#/read/yajurveda/3/1?v=63"
     },
     {
      "at": "The first lock",
      "do": "Cutting the first lock together with the kusha shoots, he says this verse, and the hair is laid on a lump of cow dung kept north of the fire:",
      "sa": "येनावपत्सविता क्षुरेण सोमस्य राज्ञो वरुणस्य विद्वान् ।\nतेन ब्रह्माणो वपतेदमस्यायुष्यञ्जरदष्टिर्यथासत् ॥",
      "tr": "yenāvapatsavitā kṣureṇa somasya rājño varuṇasya vidvān\ntena brahmāṇo vapatedamasyāyuṣyañjaradaṣṭiryathāsat",
      "en": "With the razor that wise Savitr used to shave King Soma and Varuna, shave this child, you priests, so that he may live long and reach a ripe old age.",
      "src": "Paraskara Grihya Sutra 2.1.11 (a variant of Atharva Veda 6.68.3)",
      "use": "core"
     },
     {
      "at": "The back of the head",
      "do": "The wetting and cutting are repeated for a lock at the back of the head, with this verse:",
      "sa": "त्र्यायुषं जमदग्नेः कश्यपस्य त्र्यायुषम् ।\nयद्देवेषु त्र्यायुषं तन्नो अस्तु त्र्यायुषम् ॥",
      "tr": "tryāyuṣaṃ jamadagneḥ kaśyapasya tryāyuṣam\nyaddeveṣu tryāyuṣaṃ tanno astu tryāyuṣam",
      "en": "The threefold life of Jamadagni, the threefold life of Kashyapa, the threefold life the gods enjoy: may that threefold life be ours.",
      "src": "Paraskara Grihya Sutra 2.1.15; Vajasaneyi Samhita 3.62",
      "use": "core",
      "read": "#/read/yajurveda/3/1?v=62"
     },
     {
      "at": "The left side",
      "do": "Then a lock on the left (northern) side is cut, with this verse:",
      "sa": "येन भूरिश्चरा दिवं ज्योक्च पश्चाद्धि सूर्यम् ।\nतेन ते वपामि ब्रह्मणा जीवातवे जीवनाय सुश्लोक्याय स्वस्तये ॥",
      "tr": "yena bhūriścarā divaṃ jyokca paścāddhi sūryam\ntena te vapāmi brahmaṇā jīvātave jīvanāya suślokyāya svastaye",
      "en": "By the prayer through which the mighty one rises to heaven and long sees the sun, by that prayer I shave you, for life and living, for a good name and for well-being.",
      "src": "Paraskara Grihya Sutra 2.1.16"
     },
     {
      "at": "Handing the razor to the barber",
      "do": "He wets the head with the rest of the water and hands the razor to the barber, saying:",
      "sa": "अक्षुण्वन्परिवप ॥",
      "tr": "akṣuṇvanparivapa",
      "en": "Shave him all round, without a single cut.",
      "src": "Paraskara Grihya Sutra 2.1.20"
     }
    ]
   }
  ]
 },
 "vidyarambha": {
  "basis": "No Grihya Sutra has a chapter for Vidyarambha: it is a later rite, shaped by regional custom, so there is no fixed sequence of mantras. The verses here are Vedic prayers to Ganesha and Saraswati and for wisdom, from the Rig Veda, the White Yajurveda and the Paraskara Grihya Sutra, which priests often draw on. The short prayers most families know, such as 'Saraswati namastubhyam' and the words written in the rice, come from later tradition (see notes).",
  "groups": [
   {
    "title": null,
    "mantras": [
     {
      "at": "Calling on Ganesha",
      "do": "To begin, the priest or an elder calls on Ganesha, Lord of the hosts, with this Rig Veda verse (originally addressed to Brahmanaspati, lord of sacred speech):",
      "sa": "गणानां त्वा गणपतिं हवामहे कविं कवीनामुपमश्रवस्तमम् ।\nज्येष्ठराजं ब्रह्मणां ब्रह्मणस्पत आ नः शृण्वन्नूतिभिः सीद सादनम् ॥",
      "tr": "gaṇānāṃ tvā gaṇapatiṃ havāmahe kaviṃ kavīnāmupamaśravastamam\njyeṣṭharājaṃ brahmaṇāṃ brahmaṇaspata ā naḥ śṛṇvannūtibhiḥ sīda sādanam",
      "en": "We call on you, Lord of the hosts, poet of poets, most famous of all, eldest king of sacred words, Brahmanaspati: hear us, and come with your help to sit in your place.",
      "src": "Rig Veda 2.23.1",
      "read": "#/read/rigveda/3/23?v=1"
     },
     {
      "at": "Invoking Saraswati",
      "do": "Before the books, pens and image of Saraswati, the family invokes her with three verses beginning:",
      "sa": "पावका नः सरस्वती वाजेभिर्वाजिनीवती ।\nयज्ञं वष्टु धियावसुः ॥",
      "tr": "pāvakā naḥ sarasvatī vājebhirvājinīvatī\nyajñaṃ vaṣṭu dhiyāvasuḥ",
      "en": "May Saraswati, the purifier, rich in gifts and strength, whose wealth is wisdom, gladly accept our worship.",
      "src": "Vajasaneyi Samhita 20.84–86 (also Rig Veda 1.3.10–12)",
      "use": "some",
      "read": "#/read/yajurveda/20/1?v=84"
     },
     {
      "at": "Guardian of our thoughts",
      "do": "Another short Vedic prayer to Saraswati that many priests use:",
      "sa": "प्र णो देवी सरस्वती वाजेभिर्वाजिनीवती ।\nधीनामवित्र्यवतु ॥",
      "tr": "pra ṇo devī sarasvatī vājebhirvājinīvatī\ndhīnāmavitryavatu",
      "en": "May the goddess Saraswati, rich in gifts and strength, help us on our way; may she who guards our thoughts protect us.",
      "src": "Rig Veda 6.61.4",
      "use": "some",
      "read": "#/read/rigveda/7/61?v=4"
     },
     {
      "at": "A prayer for insight",
      "do": "As the child writes the first letters, or tastes the honey, an elder can say this prayer for insight, which the Paraskara Grihya Sutra gives to a new student:",
      "sa": "मेधां मे देवः सविता आदधातु मेधां मे देवी सरस्वती आदधातु ।\nमेधामश्विनौ देवावाधत्तां पुष्करस्रजौ ॥",
      "tr": "medhāṃ me devaḥ savitā ādadhātu medhāṃ me devī sarasvatī ādadhātu\nmedhāmaśvinau devāvādhattāṃ puṣkarasrajau",
      "en": "May the god Savitr give me insight; may the goddess Saraswati give me insight; may the two divine Ashvins, garlanded with lotuses, give me insight.",
      "src": "Paraskara Grihya Sutra 2.4.8",
      "use": "some"
     },
     {
      "at": "Blessing for wisdom",
      "do": "As the child bows to the teacher, the elders ask that the child be given wisdom:",
      "sa": "यां मेधां देवगणाः पितरश्चोपासते ।\nतया मामद्य मेधयाऽग्ने मेधाविनं कुरु स्वाहा ॥",
      "tr": "yāṃ medhāṃ devagaṇāḥ pitaraścopāsate\ntayā māmadya medhayā'gne medhāvinaṃ kuru svāhā",
      "en": "Agni, the wisdom that the hosts of gods and the ancestors cherish: with that wisdom make me wise today. Svaha!",
      "src": "Vajasaneyi Samhita 32.14",
      "use": "some",
      "read": "#/read/yajurveda/32/1?v=14"
     }
    ]
   }
  ]
 },
 "upanayana": {
  "basis": "This follows the Upanayana in the Paraskara Grihya Sutra (2.2 to 2.5), the White Yajurveda manual that most North Indian and Caribbean pandits follow, with the Vedic verses it quotes. Family priests often shorten it and change the order (many give the thread and the Gayatri first and the staff afterwards), and nearly all add the sacred-thread verse, which is found in some texts of Paraskara but not in the critical edition.",
  "groups": [
   {
    "title": "Dressing the new student",
    "mantras": [
     {
      "at": "I have come to be a student",
      "do": "Standing west of the fire, the child says these words after the teacher:",
      "sa": "ब्रह्मचर्यमागाम् ।\nब्रह्मचार्यसानि ॥",
      "tr": "brahmacaryamāgām\nbrahmacāryasāni",
      "en": "I have come to the life of a student. Let me be a student.",
      "src": "Paraskara Grihya Sutra 2.2.6"
     },
     {
      "at": "The new garment",
      "do": "The teacher dresses the child in the new garment, saying:",
      "sa": "येनेन्द्राय बृहस्पतिर्वासः पर्यदधादमृतं ।\nतेन त्वा परिदधाम्यायुषे दीर्घायुत्वाय बलाय वर्चसे ॥",
      "tr": "yenendrāya bṛhaspatirvāsaḥ paryadadhādamṛtaṃ\ntena tvā paridadhāmyāyuṣe dīrghāyutvāya balāya varcase",
      "en": "As Brihaspati wrapped Indra in the garment of immortality, so I wrap this around you, for life and a long life, for strength and for radiance.",
      "src": "Paraskara Grihya Sutra 2.2.7"
     },
     {
      "at": "The girdle",
      "do": "The girdle of munja grass is tied around the child's waist with this verse, which some say the teacher recites and others the child:",
      "sa": "इयं दुरुक्तम् परिबाधमाना वर्णं पवित्रं पुनती म आगात् ।\nप्राणापानाभ्यां बलमादधाना स्वसा देवी सुभगा मेखलेयम् ॥",
      "tr": "iyaṃ duruktam paribādhamānā varṇaṃ pavitraṃ punatī ma āgāt\nprāṇāpānābhyāṃ balamādadhānā svasā devī subhagā mekhaleyam",
      "en": "Here she has come to me, keeping harsh words away, purifying my nature as a cleansing stream does, bringing me strength through the breath going in and out: this girdle, a sister, a goddess, full of blessing.",
      "src": "Paraskara Grihya Sutra 2.2.8"
     },
     {
      "at": "Or: the well-dressed youth",
      "do": "Paraskara allows this Rig Veda verse instead, and many priests say it as the child is dressed or given the thread:",
      "sa": "युवा सुवासाः परिवीत आगात् स उ श्रेयान् भवति जायमानः ।\nतं धीरासः कवय उन्नयन्ति स्वाध्यो३ मनसा देवयन्तः ॥",
      "tr": "yuvā suvāsāḥ parivīta āgāt sa u śreyān bhavati jāyamānaḥ\ntaṃ dhīrāsaḥ kavaya unnayanti svādhyo manasā devayantaḥ",
      "en": "Well dressed and well clothed, the young one has come; as he is born, he grows in glory. Wise and thoughtful seers, their hearts turned to the gods, raise him up.",
      "src": "Paraskara Grihya Sutra 2.2.9; Rig Veda 3.8.4",
      "read": "#/read/rigveda/4/8?v=4"
     },
     {
      "at": "The sacred thread",
      "do": "The yajnopavita is placed over the child's left shoulder and across the body while this is said:",
      "sa": "यज्ञोपवीतं परमं पवित्रं प्रजापतेर्यत्सहजं पुरस्तात् ।\nआयुष्यमग्र्यं प्रतिमुञ्च शुभ्रं यज्ञोपवीतं बलमस्तु तेजः ।\nयज्ञोपवीतमसि यज्ञस्य त्वा यज्ञोपवीतेनोपनह्यामि ॥",
      "tr": "yajñopavītaṃ paramaṃ pavitraṃ prajāpateryatsahajaṃ purastāt\nāyuṣyamagryaṃ pratimuñca śubhraṃ yajñopavītaṃ balamastu tejaḥ\nyajñopavītamasi yajñasya tvā yajñopavītenopanahyāmi",
      "en": "The sacred thread is supremely pure, born together with Prajapati in the beginning. Put on this bright thread, the foremost, which gives long life: may it be your strength and your light. You are the sacred thread: I clothe you with the sacred thread of worship.",
      "src": "Paraskara Grihya Sutra 2.2.11, in the text as printed in India",
      "use": "core"
     },
     {
      "at": "The staff",
      "do": "Receiving the staff from the teacher, the child says:",
      "sa": "यो मे दण्डः परापतद्वैहायसोऽधिभूम्यां ।\nतमहं पुनरादद आयुषे ब्रह्मणे ब्रह्मवर्चसाय ॥",
      "tr": "yo me daṇḍaḥ parāpatadvaihāyaso'dhibhūmyāṃ\ntamahaṃ punarādada āyuṣe brahmaṇe brahmavarcasāya",
      "en": "My staff, which fell from the open sky to the ground, I take up again, for long life, for sacred knowledge and its radiance.",
      "src": "Paraskara Grihya Sutra 2.2.12"
     }
    ]
   },
   {
    "title": "Teacher and student",
    "mantras": [
     {
      "at": "Looking at the sun",
      "do": "After filling the child's cupped hands with water, the teacher has the child look up at the sun, saying:",
      "sa": "तच्चक्षुर्देवहितं पुरस्ताच्छुक्रमुच्चरत् ।\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतं प्र ब्रवाम शरदः शतमदीनाः स्याम शरदः शतं भूयश्च शरदः शतात् ॥",
      "tr": "taccakṣurdevahitaṃ purastācchukramuccarat\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śataṃ pra bravāma śaradaḥ śatamadīnāḥ syāma śaradaḥ śataṃ bhūyaśca śaradaḥ śatāt",
      "en": "That bright eye, set in place by the gods, rises in the east. May we see a hundred autumns and live a hundred autumns; may we hear a hundred autumns and speak a hundred autumns; may we live free from want for a hundred autumns, and longer still.",
      "src": "Paraskara Grihya Sutra 2.2.15; Vajasaneyi Samhita 36.24",
      "read": "#/read/yajurveda/36/1?v=24"
     },
     {
      "at": "Touching the heart",
      "do": "Reaching over the child's right shoulder, the teacher lays a hand on the child's heart and says:",
      "sa": "मम व्रते ते हृदयं दधामि । मम चित्तमनुचित्तं ते अस्तु ।\nमम वाचमेकमना जुषस्व बृहस्पतिष्ट्वा नियुनक्तु मह्यम् ॥",
      "tr": "mama vrate te hṛdayaṃ dadhāmi mama cittamanucittaṃ te astu\nmama vācamekamanā juṣasva bṛhaspatiṣṭvā niyunaktu mahyam",
      "en": "I place your heart within my vow; may your mind follow my mind. Listen to my words with all your heart. May Brihaspati join you to me.",
      "src": "Paraskara Grihya Sutra 2.2.16"
     },
     {
      "at": "Whose student are you?",
      "do": "Holding the child's right hand, the teacher asks the child's name and whose student the child is, and when the child answers “Yours,” declares:",
      "sa": "इन्द्रस्य ब्रह्मचार्यस्यग्निराचार्यस्तवाहमाचार्यस्तवासौ ॥",
      "tr": "indrasya brahmacāryasyagnirācāryastavāhamācāryastavāsau",
      "en": "You are Indra's student. Agni is your teacher, and I am your teacher, [child's name].",
      "src": "Paraskara Grihya Sutra 2.2.17–20"
     },
     {
      "at": "Into the care of all beings",
      "do": "The teacher entrusts the child to the gods and to every living thing, saying:",
      "sa": "प्रजापतये त्वा परिददामि देवाय त्वा सवित्रे परिददाम्यद्भ्यस्त्वौषधीभ्यः परिददामि ।\nद्यावापृथिवीभ्यां त्वा परिददामि विश्वेभ्यस्त्वा देवेभ्यः परिददामि ।\nसर्वेभ्यस्त्वा भूतेभ्यः परिददाम्यरिष्ट्यै ॥",
      "tr": "prajāpataye tvā paridadāmi devāya tvā savitre paridadāmyadbhyastvauṣadhībhyaḥ paridadāmi\ndyāvāpṛthivībhyāṃ tvā paridadāmi viśvebhyastvā devebhyaḥ paridadāmi\nsarvebhyastvā bhūtebhyaḥ paridadāmyariṣṭyai",
      "en": "I give you into the care of Prajapati and of the god Savitr, of the waters and the plants, of Heaven and Earth, of all the gods and of all beings, so that no harm may come to you.",
      "src": "Paraskara Grihya Sutra 2.2.21",
      "use": "some"
     }
    ]
   },
   {
    "title": "The Gayatri",
    "mantras": [
     {
      "at": "The student's vows",
      "do": "After walking around the fire and making the ghee offerings, the teacher instructs the new student:",
      "sa": "ब्रह्मचार्यस्यपोशान कर्म कुरु मा दिवा सुषुप्था ।\nवाचं यच्छ समिधमाधेह्यपोशान ॥",
      "tr": "brahmacāryasyapośāna karma kuru mā divā suṣupthā\nvācaṃ yaccha samidhamādhehyapośāna",
      "en": "You are a student now. Sip water. Do your work. Do not sleep in the daytime. Guard your speech. Feed the sacred fire. Sip water.",
      "src": "Paraskara Grihya Sutra 2.3.2",
      "use": "core"
     },
     {
      "at": "The Gayatri Mantra",
      "do": "Seated north of the fire and facing the teacher, the child learns the Savitri, first phrase by phrase, then half by half, then whole, reciting it together with the teacher. Priests begin it with Om:",
      "sa": "भूर्भुवः स्वः\nतत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि ।\nधियो यो नः प्रचोदयात् ॥",
      "tr": "bhūrbhuvaḥ svaḥ\ntatsaviturvareṇyaṃ bhargo devasya dhīmahi\ndhiyo yo naḥ pracodayāt",
      "en": "Earth, sky, heaven. We meditate on the glorious light of the divine Savitr: may it inspire our minds.",
      "src": "Paraskara Grihya Sutra 2.3.3–10; Vajasaneyi Samhita 36.3 (also Rig Veda 3.62.10)",
      "use": "core",
      "read": "#/read/yajurveda/36/1?v=3"
     }
    ]
   },
   {
    "title": "The sacred fire",
    "mantras": [
     {
      "at": "Feeding the fire",
      "do": "The new student stands and lays a stick of wood on the fire, and does so three times, saying each time:",
      "sa": "अग्नये समिधमहार्ष बृहते जातवेदसे ।\nयथा त्वमग्ने समिधा समिध्यस एवमहमायुषा मेधया वर्च्चसा प्रजया पशुभिर्ब्रह्मवर्चसेन समिन्धे ।\nजीवपुत्रो ममाचार्यो मेधाव्यहमसान्यनिराकारिष्णुर्यशस्वी तेजस्वी ब्रह्मवर्चस्यन्नादो भूयासं स्वाहा ॥",
      "tr": "agnaye samidhamahārṣa bṛhate jātavedase\nyathā tvamagne samidhā samidhyasa evamahamāyuṣā medhayā varccasā prajayā paśubhirbrahmavarcasena samindhe\njīvaputro mamācāryo medhāvyahamasānyanirākāriṣṇuryaśasvī tejasvī brahmavarcasyannādo bhūyāsaṃ svāhā",
      "en": "I have brought fuel for Agni, the great knower of all. As you, Agni, are kindled by the fuel, so may I be kindled with life and insight, with vigour, children and cattle, and the radiance of sacred knowledge. May my teacher's children live long; may I be wise and never lose what I learn; may I be honoured, bright and radiant, and never lack for food. Svaha!",
      "src": "Paraskara Grihya Sutra 2.4.3"
     },
     {
      "at": "A prayer for insight",
      "do": "Warming their hands at the fire and touching them to the face, the student prays:",
      "sa": "मेधां मे देवः सविता आदधातु मेधां मे देवी सरस्वती आदधातु ।\nमेधामश्विनौ देवावाधत्तां पुष्करस्रजौ ॥",
      "tr": "medhāṃ me devaḥ savitā ādadhātu medhāṃ me devī sarasvatī ādadhātu\nmedhāmaśvinau devāvādhattāṃ puṣkarasrajau",
      "en": "May the god Savitr give me insight; may the goddess Saraswati give me insight; may the two divine Ashvins, garlanded with lotuses, give me insight.",
      "src": "Paraskara Grihya Sutra 2.4.8"
     }
    ]
   }
  ]
 },
 "coming-of-age": {
  "basis": "The first shave (Keshanta) and the graduation bath (Samavartana) follow the Paraskara Grihya Sutra (2.1 and 2.6), the White Yajurveda manual that most North Indian and Caribbean pandits follow. Both are rarely performed in full today, so a priest may use only a few of these verses in a simple puja for a birthday or a graduation. The Grihya Sutras have no rite for a girl's coming of age, so Ritu Shuddhi and its regional forms rest on family custom (see notes).",
  "groups": [
   {
    "title": "Keshanta: the first shave",
    "mantras": [
     {
      "at": "Warm water for the first shave",
      "do": "As at the first haircut, the father mixes warm water into cold, but says “hair and beard” (keshashmashru) where the child's rite says “hair” (keshan):",
      "sa": "उष्णेन वाय उदकेनेह्यदिते केशान्वप ॥",
      "tr": "uṣṇena vāya udakenehyadite keśānvapa",
      "en": "Come, Vayu, with warm water. Aditi, shave the hair [and beard].",
      "src": "Paraskara Grihya Sutra 2.1.6–7"
     },
     {
      "at": "Shaving the face",
      "do": "The young man's hair and face are shaved, the razor going round three times, with the razor verse in its “hair and beard” form, as the Atharva Veda gives it:",
      "sa": "यत् क्षुरेण मर्चयता सुतेजसा वप्ता वपसि केशश्मश्रु ।\nशुभं मुखं मा न आयुः प्र मोषीः ॥",
      "tr": "yat kṣureṇa marcayatā sutejasā vaptā vapasi keśaśmaśru\nśubhaṃ mukhaṃ mā na āyuḥ pra moṣīḥ",
      "en": "Barber, as you shave the hair and beard with your keen and cleansing razor, leave the face fair, but do not take away our life.",
      "src": "Paraskara Grihya Sutra 2.1.17–20; Atharva Veda 8.2.17",
      "read": "#/read/atharvaveda/8/2?v=17"
     }
    ]
   },
   {
    "title": "Samavartana: the graduation bath",
    "mantras": [
     {
      "at": "Drawing water for the bath",
      "do": "Standing on kusha grass east of eight pots of water, the student draws water from the first pot, saying:",
      "sa": "ये अप्स्वन्तरग्नयः प्रविष्टा ।\nगोह्य उपगोह्यो मयूषो मनोहास्खलो विरुजस्तनूदूषुरिन्द्रियहातान्विजहामि ।\nयो रोचनस्तमिह गृह्णामि ॥",
      "tr": "ye apsvantaragnayaḥ praviṣṭā\ngohya upagohyo mayūṣo manohāskhalo virujastanūdūṣurindriyahātānvijahāmi\nyo rocanastamiha gṛhṇāmi",
      "en": "Of the fires that dwell within the waters, I leave behind the hidden and the covered, the searing ray, the one that harms the mind, the one that brings pain, the one that spoils the body and the one that dulls the senses. The bright one, that one I take up here.",
      "src": "Paraskara Grihya Sutra 2.6.10",
      "use": "core"
     },
     {
      "at": "The graduation bath",
      "do": "The student pours the water over their head, saying this, and then bathes from the other pots, with the “apo hi shtha” verses and in silence:",
      "sa": "तेन मामभिषिञ्चामि श्रियै यशसे ब्रह्मणे ब्रह्मवर्चसाय ॥",
      "tr": "tena māmabhiṣiñcāmi śriyai yaśase brahmaṇe brahmavarcasāya",
      "en": "With this I bathe myself, for prosperity and good name, for sacred knowledge and its radiance.",
      "src": "Paraskara Grihya Sutra 2.6.11",
      "use": "core"
     },
     {
      "at": "Taking off the girdle",
      "do": "The student unties the student's girdle and lays down the staff, saying:",
      "sa": "उदुत्तमं वरुण पाशमस्मदवाधमं वि मध्यमं श्रथाय ।\nअथा वयमादित्य व्रते तवानागसो अदितये स्याम ॥",
      "tr": "uduttamaṃ varuṇa pāśamasmadavādhamaṃ vi madhyamaṃ śrathāya\nathā vayamāditya vrate tavānāgaso aditaye syāma",
      "en": "Varuna, loosen the highest bond from us, and untie the lowest and the middle. Then, Aditya, keeping your law, may we stand blameless before Aditi.",
      "src": "Paraskara Grihya Sutra 2.6.15; Vajasaneyi Samhita 12.12",
      "read": "#/read/yajurveda/12/1?v=12"
     },
     {
      "at": "Greeting the sun",
      "do": "Dressed in a fresh garment, the student stands before the sun with three formulas for morning, midday and evening, the first of which is:",
      "sa": "उद्यन्भ्राजभृष्णुरिन्द्रो मरुद्भिरस्थात् ।\nप्रातर्यावभिरस्थाद्दशसनिरसि दशसनिं मा कुर्वाविदन्मागमय ॥",
      "tr": "udyanbhrājabhṛṣṇurindro marudbhirasthāt\nprātaryāvabhirasthāddaśasanirasi daśasaniṃ mā kurvāvidanmāgamaya",
      "en": "Rising with his blazing spear, Indra has taken his stand with the Maruts, with those who travel at dawn. You win tenfold: make me win tenfold. Bring me to renown.",
      "src": "Paraskara Grihya Sutra 2.6.16"
     },
     {
      "at": "Anointing",
      "do": "After a shave, a fresh bath and anointing, the student touches fragrant paste to the eyes, face and ears, saying:",
      "sa": "सुचक्षा अहमक्षीभ्यां भूयासं सुवर्चा मुखेन ।\nसुश्रुत्कर्णाभ्यां भूयासम् ॥",
      "tr": "sucakṣā ahamakṣībhyāṃ bhūyāsaṃ suvarcā mukhena\nsuśrutkarṇābhyāṃ bhūyāsam",
      "en": "May I see clearly with my eyes, shine with my face, and hear well with my ears.",
      "src": "Paraskara Grihya Sutra 2.6.19"
     },
     {
      "at": "New clothes",
      "do": "The student puts on a new, unwashed garment, saying:",
      "sa": "परिधास्यै यशोधास्यै दीर्घायुत्वाय जरदष्टिरस्मि ।\nशतं च जीवामि शरदः पुरूचीरायस्पोषमभिसंव्ययिष्ये ॥",
      "tr": "paridhāsyai yaśodhāsyai dīrghāyutvāya jaradaṣṭirasmi\nśataṃ ca jīvāmi śaradaḥ purūcīrāyaspoṣamabhisaṃvyayiṣye",
      "en": "I put this on to clothe myself in honour and long life: I will live to a ripe old age. I will live a hundred full autumns, and wrap myself in growing wealth.",
      "src": "Paraskara Grihya Sutra 2.6.20"
     },
     {
      "at": "The upper cloth",
      "do": "Then comes the upper cloth with this verse:",
      "sa": "यशसा मा द्यावापृथिवी यशसेन्द्राबृहस्पती ।\nयशो भगश्च माविन्दद्यशो मा प्रतिपद्यताम् ॥",
      "tr": "yaśasā mā dyāvāpṛthivī yaśasendrābṛhaspatī\nyaśo bhagaśca māvindadyaśo mā pratipadyatām",
      "en": "May Heaven and Earth fill me with honour, and Indra and Brihaspati too. May honour and good fortune find me; may honour be mine.",
      "src": "Paraskara Grihya Sutra 2.6.21",
      "use": "some"
     },
     {
      "at": "Flowers",
      "do": "The student accepts a garland of flowers, saying:",
      "sa": "या आहरज्जमदग्निः श्रद्धायै मेधायै कामायेन्द्रियाय ।\nता अहं प्रतिगृह्णामि यशसा च भगेन च ॥",
      "tr": "yā āharajjamadagniḥ śraddhāyai medhāyai kāmāyendriyāya\ntā ahaṃ pratigṛhṇāmi yaśasā ca bhagena ca",
      "en": "The flowers that Jamadagni brought for faith, for wisdom, for love and for strength, I accept them, with honour and good fortune.",
      "src": "Paraskara Grihya Sutra 2.6.23",
      "use": "some"
     }
    ]
   }
  ]
 },
 "vivaha": {
  "basis": "This sequence follows the wedding rite of the Paraskara Grihya Sutra (1.3 to 1.8), the manual of the White Yajurveda that most North Indian and Caribbean pandits follow, with the Vedic verses it quotes, most of them from the great wedding hymn of the Rig Veda (10.85). Family priests often change the order (many do the kanyadan and the joining of hands before the fire offerings), shorten or skip some moments, and add later verses such as the mangalashtak or a verse for the mangalsutra; priests of other Vedic schools use different but closely related mantras.",
  "groups": [
   {
    "title": "Welcoming the groom",
    "mantras": [
     {
      "at": "Welcoming the groom with honey",
      "do": "The bride's family receives the groom as an honoured guest and offers him madhuparka, a mix of curd, honey and ghee, which he tastes three times, saying:",
      "sa": "यन्मधुनो मधव्यं परमं रूपमन्नाद्यम् ।\nतेनाहं मधुनो मधव्येन परमेण रूपेणान्नाद्येन परमो मधव्योऽन्नादोऽसानि ॥",
      "tr": "yanmadhuno madhavyaṃ paramaṃ rūpamannādyam\ntenāhaṃ madhuno madhavyena parameṇa rūpeṇānnādyena paramo madhavyo'nnādo'sāni",
      "en": "Whatever is the sweetest, finest form of honey, the best of all food: through that sweetness, that finest form and that food, may I become the finest too, full of sweetness, and blessed with plenty to eat.",
      "src": "Paraskara Grihya Sutra 1.3.20"
     }
    ]
   },
   {
    "title": "Giving and receiving the bride",
    "mantras": [
     {
      "at": "Dressing the bride",
      "do": "The groom gives the bride a new garment to put on, saying:",
      "sa": "जरां गच्छ परिधत्स्व वासो भवाकृष्टीनामभिशस्तिपावा ।\nशतं च जीव शरदः सुवर्च्चा रयिं च पुत्राननुसंव्ययस्वायुष्मतीदं परिधत्स्व वासः ॥",
      "tr": "jarāṃ gaccha paridhatsva vāso bhavākṛṣṭīnāmabhiśastipāvā\nśataṃ ca jīva śaradaḥ suvarccā rayiṃ ca putrānanusaṃvyayasvāyuṣmatīdaṃ paridhatsva vāsaḥ",
      "en": "Grow old in happiness: put on this garment, and be a shield for your people against every harm. Live a hundred autumns, full of radiance, and wrap yourself in wealth and children. Blessed with long life, put on this garment.",
      "src": "Paraskara Grihya Sutra 1.4.12"
     },
     {
      "at": "Anointing the couple",
      "do": "The bride and groom are anointed together, traditionally by the bride's father, while the groom says:",
      "sa": "समञ्जन्तु विश्वे देवाः समापो हृदयानि नौ ।\nसं मातरिश्वा सं धाता समु देष्ट्री दधातु नौ ॥",
      "tr": "samañjantu viśve devāḥ samāpo hṛdayāni nau\nsaṃ mātariśvā saṃ dhātā samu deṣṭrī dadhātu nau",
      "en": "May all the gods and the waters join our two hearts as one. May Matarishvan the wind, Dhatr the creator and Deshtri the guiding goddess bind us close together.",
      "src": "Paraskara Grihya Sutra 1.4.14; Rig Veda 10.85.47",
      "read": "#/read/rigveda/11/85?v=47"
     },
     {
      "at": "Giving the bride (kanyadan)",
      "do": "When the father places his daughter's hand in the groom's, Manu says he should honour the couple and tell them:",
      "sa": "सहोभौ चरतां धर्मम्",
      "tr": "sahobhau caratāṃ dharmam",
      "en": "May you both walk the path of dharma together.",
      "src": "Manusmriti 3.30",
      "use": "some"
     },
     {
      "at": "The groom receives the bride",
      "do": "The groom accepts the bride from her father and leads her from his side, saying this verse and then her name:",
      "sa": "यदैषि मनसा दूरं दिशोऽनु पवमानो वा ।\nहिरण्यपर्णो वैकर्णः स त्वा मन्मनसां करोतु ॥",
      "tr": "yadaiṣi manasā dūraṃ diśo'nu pavamāno vā\nhiraṇyaparṇo vaikarṇaḥ sa tvā manmanasāṃ karotu",
      "en": "When your heart wanders far away, to the ends of the earth like the wind, may the golden-winged Vaikarna turn your heart toward mine.",
      "src": "Paraskara Grihya Sutra 1.4.15"
     },
     {
      "at": "Looking at each other",
      "do": "The groom has the couple look at each other, the moment many families mark with the jaimala or shubho drishti, saying this and three more verses:",
      "sa": "अघोरचक्षुरपतिघ्न्येधि शिवा पशुभ्यः सुमनाः सुवर्चाः ।\nवीरसूर्देवकामा स्योना शं नो भव द्विपदे शं चतुष्पदे ॥",
      "tr": "aghoracakṣurapatighnyedhi śivā paśubhyaḥ sumanāḥ suvarcāḥ\nvīrasūrdevakāmā syonā śaṃ no bhava dvipade śaṃ catuṣpade",
      "en": "Look with kind eyes, and bring no harm to your husband. Be gentle to all living things, warm-hearted and radiant. Mother of brave children, loving the gods, full of joy: bring blessings to us all, to people and to animals alike.",
      "src": "Paraskara Grihya Sutra 1.4.16; Rig Veda 10.85.44",
      "read": "#/read/rigveda/11/85?v=44"
     }
    ]
   },
   {
    "title": "Offerings and taking her hand",
    "mantras": [
     {
      "at": "The puffed rice offering (laja homa)",
      "do": "The bride's brother pours puffed rice mixed with shami leaves into her cupped hands, and standing, she offers it into the fire as the groom recites three verses, beginning:",
      "sa": "अर्यमणं देवं कन्याऽऽग्निमयक्षत ।\nसनो अर्यमा देवः प्रेतो मुञ्चतु मा पतेः स्वाहा ।",
      "tr": "aryamaṇaṃ devaṃ kanyā''gnimayakṣata\nsano aryamā devaḥ preto muñcatu mā pateḥ svāhā",
      "en": "Brides have always worshipped the god Aryaman in the fire. May Aryaman release her from her father's home, but never from her husband. Svaha!",
      "src": "Paraskara Grihya Sutra 1.6.1–2",
      "use": "core"
     },
     {
      "at": "The bride's prayer",
      "do": "The second verse puts the bride's own prayer into words as she pours the grain:",
      "sa": "इयं नार्युपब्रूते लाजानावपन्तिका ।\nआयुष्मानस्तु मे पतिरेधन्तां ज्ञातयो मम स्वाहा ।",
      "tr": "iyaṃ nāryupabrūte lājānāvapantikā\nāyuṣmānastu me patiredhantāṃ jñātayo mama svāhā",
      "en": "Pouring the grain into the fire, this woman prays: \"May my husband live long, and may my family flourish.\" Svaha!",
      "src": "Paraskara Grihya Sutra 1.6.2; compare Atharva Veda 14.2.63"
     },
     {
      "at": "Taking her hand (panigrahana)",
      "do": "The groom takes the bride's right hand, thumb and all, saying:",
      "sa": "गृभ्णामि ते सौभगत्वाय हस्तं मया पत्या जरदष्टिर्यथासः ।\nभगो अर्यमा सविता पुरंधिर्मह्यं त्वादुर्गार्हपत्याय देवाः ॥",
      "tr": "gṛbhṇāmi te saubhagatvāya hastaṃ mayā patyā jaradaṣṭiryathāsaḥ\nbhago aryamā savitā puraṃdhirmahyaṃ tvādurgārhapatyāya devāḥ",
      "en": "I take your hand for our happiness, so that you may grow old with me, your husband. Bhaga, Aryaman, Savitr and Purandhi, the gods, have given you to me, to keep a home together.",
      "src": "Paraskara Grihya Sutra 1.6.3; Rig Veda 10.85.36",
      "use": "core",
      "read": "#/read/rigveda/11/85?v=36"
     },
     {
      "at": "I am he, you are she",
      "do": "Still holding her hand, the groom goes on:",
      "sa": "अमोऽहमस्मि सा त्वं सा त्वमस्यमोऽहम् ।\nसामाहमस्मि ऋक्त्वं द्यौरहं पृथिवी त्वं ॥",
      "tr": "amo'hamasmi sā tvaṃ sā tvamasyamo'ham\nsāmāhamasmi ṛktvaṃ dyaurahaṃ pṛthivī tvaṃ",
      "en": "I am he, you are she; you are she, I am he. I am the melody, you are the verse. I am the sky, you are the earth.",
      "src": "Paraskara Grihya Sutra 1.6.3; compare Atharva Veda 14.2.71",
      "read": "#/read/atharvaveda/14/2?v=71"
     },
     {
      "at": "Come, let us marry",
      "do": "And he ends the taking of her hand with:",
      "sa": "तावेहि विवहावहै सहरेतो दधावहै प्रजां प्रजनयावहै पुत्रान्विन्द्यावहै बहून् ।\nते सन्तु जरदष्टयः संप्रियौ रोचिष्णू सुमनस्यमानौ ।\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतम् ॥",
      "tr": "tāvehi vivahāvahai sahareto dadhāvahai prajāṃ prajanayāvahai putrānvindyāvahai bahūn\nte santu jaradaṣṭayaḥ saṃpriyau rociṣṇū sumanasyamānau\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śatam",
      "en": "Come, let us marry. Let us join our lives and bring children into the world, many children, and may they live to a good old age. Loving each other, bright and glad of heart, may we see a hundred autumns, live a hundred autumns, hear a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.6.3"
     }
    ]
   },
   {
    "title": "Around the fire",
    "mantras": [
     {
      "at": "Stepping on the stone",
      "do": "The groom has the bride step with her right foot onto a stone north of the fire, saying:",
      "sa": "आरोहेममश्मानमश्मेव त्वं स्थिरा भव ।\nअभितिष्ठ पृतन्यतोऽवबाधस्व पृतनायतः ॥",
      "tr": "ārohemamaśmānamaśmeva tvaṃ sthirā bhava\nabhitiṣṭha pṛtanyato'vabādhasva pṛtanāyataḥ",
      "en": "Step onto this stone, and be as steady as a stone. Stand firm against anyone who would harm you, and push back all who oppose you.",
      "src": "Paraskara Grihya Sutra 1.7.1"
     },
     {
      "at": "The song to Sarasvati",
      "do": "The groom then sings this song (gatha):",
      "sa": "सरस्वति प्रेदमव सुभगे वाजिनीवती ।\nयां त्वा विश्वस्य भूतस्य प्रजायामस्याग्रतः ।\nयस्यां भूतं समभवद्यस्यां विश्वमिदं जगत् ।\nतामद्य गाथां गास्यामि या स्त्रीणामुत्तमं यशः ॥",
      "tr": "sarasvati predamava subhage vājinīvatī\nyāṃ tvā viśvasya bhūtasya prajāyāmasyāgrataḥ\nyasyāṃ bhūtaṃ samabhavadyasyāṃ viśvamidaṃ jagat\ntāmadya gāthāṃ gāsyāmi yā strīṇāmuttamaṃ yaśaḥ",
      "en": "Sarasvati, gracious and generous goddess, bless what we do here. You whom we praise first of all beings, in whom all that is came to be, in whom this whole world lives: today I will sing the song that is the highest glory of women.",
      "src": "Paraskara Grihya Sutra 1.7.2",
      "use": "some"
     },
     {
      "at": "Circling the fire (pheras)",
      "do": "The couple walk around the fire as the groom recites this verse, and the grain offering, the stone and the song are repeated for each round, three in all:",
      "sa": "तुभ्यमग्रे पर्यवहन्त्सूर्यां वहतुना सह ।\nपुनः पतिभ्यो जायां दा अग्ने प्रजया सह ॥",
      "tr": "tubhyamagre paryavahantsūryāṃ vahatunā saha\npunaḥ patibhyo jāyāṃ dā agne prajayā saha",
      "en": "To you, Agni, they first brought Surya, the bride of the sun, with her wedding procession. Now, Agni, give the wife back to her husband, blessed with children.",
      "src": "Paraskara Grihya Sutra 1.7.3–4; Rig Veda 10.85.38",
      "use": "core",
      "read": "#/read/rigveda/11/85?v=38"
     }
    ]
   },
   {
    "title": "Seven steps and blessings",
    "mantras": [
     {
      "at": "The seven steps (saptapadi)",
      "do": "The groom leads the bride seven steps toward the north, adding \"May Vishnu lead you\" to each step:",
      "sa": "एकमिषे द्वे ऊर्जे त्रीणि रायस्पोषाय चत्वारि मायोभवाय ।\nपञ्च पशुभ्यः षड् ऋतुभ्यः सखे सप्तपदा भव सा मामनुव्रता भव ॥",
      "tr": "ekamiṣe dve ūrje trīṇi rāyaspoṣāya catvāri māyobhavāya\npañca paśubhyaḥ ṣaḍ ṛtubhyaḥ sakhe saptapadā bhava sā māmanuvratā bhava",
      "en": "One step for food, two for strength, three for growing wealth, four for happiness, five for our animals, six for the seasons. Friend, with seven steps be mine: share my vows and walk with me.",
      "src": "Paraskara Grihya Sutra 1.8.1–2",
      "use": "core"
     },
     {
      "at": "Sprinkling with water",
      "do": "A helper who has stood in silence by the fire with a pot of water comes forward, and the bride's head is sprinkled from it with this blessing and the three verses beginning \"apo hi shtha\":",
      "sa": "आपः शिवाः शिवतमाः शान्ताः शान्ततमास्तास्ते कृण्वन्तु भेषजम् ॥",
      "tr": "āpaḥ śivāḥ śivatamāḥ śāntāḥ śāntatamāstāste kṛṇvantu bheṣajam",
      "en": "May the blessed waters, most blessed, peaceful, most peaceful, bring you healing.",
      "src": "Paraskara Grihya Sutra 1.8.3–6"
     },
     {
      "at": "Looking at the sun",
      "do": "The groom has the bride look at the sun, saying:",
      "sa": "तच्चक्षुर्देवहितं पुरस्ताच्छुक्रमुच्चरत् ।\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतं\nप्र ब्रवाम शरदः शतमदीनाः स्याम शरदः शतं भूयश्च शरदः शतात् ॥",
      "tr": "taccakṣurdevahitaṃ purastācchukramuccarat\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śataṃ\npra bravāma śaradaḥ śatamadīnāḥ syāma śaradaḥ śataṃ bhūyaśca śaradaḥ śatāt",
      "en": "That bright eye set in place by the gods, the sun, is rising in the east. May we see a hundred autumns, live a hundred autumns, hear a hundred autumns, speak for a hundred autumns, live free from want for a hundred autumns, and more than a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.8.7; Vajasaneyi Samhita 36.24",
      "read": "#/read/yajurveda/36/1?v=24"
     },
     {
      "at": "Touching the heart",
      "do": "Reaching over her right shoulder, the groom touches the bride's heart, saying:",
      "sa": "मम व्रते ते हृदयं दधामि मम चित्तमनुचित्तं ते अस्तु ।\nमम वाचमेकमना जुषस्व प्रजापतिष्ट्वा नियुनक्तु मह्यम् ॥",
      "tr": "mama vrate te hṛdayaṃ dadhāmi mama cittamanucittaṃ te astu\nmama vācamekamanā juṣasva prajāpatiṣṭvā niyunaktu mahyam",
      "en": "I hold your heart within my vows; may your mind follow my mind. Delight in my words with all your heart; may Prajapati join you to me.",
      "src": "Paraskara Grihya Sutra 1.8.8"
     },
     {
      "at": "Blessing the bride",
      "do": "The groom presents the bride to everyone gathered, and in many weddings this is when he places sindoor in the parting of her hair:",
      "sa": "सुमङ्गलीरियं वधूरिमां समेत पश्यत ।\nसौभाग्यमस्यै दत्त्वायाऽथास्तं वि परेतन ॥",
      "tr": "sumaṅgalīriyaṃ vadhūrimāṃ sameta paśyata\nsaubhāgyamasyai dattvāyā'thāstaṃ vi paretana",
      "en": "This bride is the picture of blessing. Come, all of you, and look at her. Wish her every good fortune, then go back to your homes.",
      "src": "Paraskara Grihya Sutra 1.8.9; Rig Veda 10.85.33",
      "read": "#/read/rigveda/11/85?v=33"
     }
    ]
   },
   {
    "title": "After sunset",
    "mantras": [
     {
      "at": "Seeing the pole star",
      "do": "After sunset the groom shows the bride the pole star, the sign of constancy, and even if she cannot see it she answers \"I see it\":",
      "sa": "ध्रुवमसि ध्रुवं त्वा पश्यामि ध्रुवैधिपोष्ये मयि ।\nमह्यं त्वादादबृहस्पतिर्मया पत्या प्रजावती संजीव शरदः शतम् ॥",
      "tr": "dhruvamasi dhruvaṃ tvā paśyāmi dhruvaidhipoṣye mayi\nmahyaṃ tvādādabṛhaspatirmayā patyā prajāvatī saṃjīva śaradaḥ śatam",
      "en": "You are steady; I see you, the steady one. Be steady with me, you who will flourish. Brihaspati has given you to me: blessed with children through me, your husband, live with me a hundred autumns.",
      "src": "Paraskara Grihya Sutra 1.8.19–20"
     }
    ]
   }
  ]
 },
 "griha-pravesh": {
  "basis": "This sequence follows the rite for building and entering a house (shala-karma) in the Paraskara Grihya Sutra 3.4. It uses the four verses to Vastoshpati, the guardian spirit of the home, from the Rig Veda (7.54–55), which the Ashvalayana Grihya Sutra (2.9) also uses, and one verse from the Atharva Veda's house hymn, said as the family carries the water-pot inside. A modern Griha Pravesha usually adds a Ganesha puja, a Navagraha puja and a Vastu Shanti from later manuals, so a family priest may use only some of these mantras, or many more.",
  "groups": [
   {
    "title": "Raising the house",
    "mantras": [
     {
      "at": "Raising the main post",
      "do": "For a newly built house, an offering is poured into the pit for the main post (\"to the steady one, to the earth, svaha\"), and the householder raises the posts, going to each of the four with a verse; the first is:",
      "sa": "इमामुच्छ्रयामि भुवनस्य नाभिं वसोर्धारां प्रतरणीं वसूनाम् ।\nइहैव ध्रुवां निमिनोमि शालां क्षेमे तिष्ठतु घृतमुक्षमाणा ।",
      "tr": "imāmucchrayāmi bhuvanasya nābhiṃ vasordhārāṃ prataraṇīṃ vasūnām\nihaiva dhruvāṃ niminomi śālāṃ kṣeme tiṣṭhatu ghṛtamukṣamāṇā",
      "en": "I raise this navel of the world, a stream of riches that makes wealth grow. Here I set up a steady home: may it stand in peace, overflowing with ghee.",
      "src": "Paraskara Grihya Sutra 3.4.3–4; compare Atharva Veda 3.12.1",
      "use": "some"
     }
    ]
   },
   {
    "title": "Entering the home",
    "mantras": [
     {
      "at": "Carrying in the full pot",
      "do": "In the Atharva Veda tradition, the wife carries a full pot of water across the threshold, the householder carries the fire and the family follows, as the priest says:",
      "sa": "पूर्णं नारि प्र भर कुम्भमेतं घृतस्य धाराममृतेन संभृताम् ।\nइमां पातॄनमृतेना समङ्ग्धीष्टापूर्तमभि रक्षात्येनाम् ॥",
      "tr": "pūrṇaṃ nāri pra bhara kumbhametaṃ ghṛtasya dhārāmamṛtena saṃbhṛtām\nimāṃ pātṝnamṛtenā samaṅgdhīṣṭāpūrtamabhi rakṣātyenām",
      "en": "Bring it in, woman, this full pot, a stream of ghee mixed with the nectar of life. Bless all who drink here with that nectar, and may the good we do and the good we give protect this home.",
      "src": "Kaushika Sutra 43.10 (with Keshava's paddhati); Atharva Veda 3.12.8",
      "use": "some",
      "read": "#/read/atharvaveda/3/12?v=8"
     },
     {
      "at": "Stepping inside",
      "do": "Standing at the door, the householder asks the priest \"Brahman, may I enter?\" and, given leave, steps inside, saying:",
      "sa": "ऋतं प्रपद्ये शिवं प्रपद्ये",
      "tr": "ṛtaṃ prapadye śivaṃ prapadye",
      "en": "I step into truth; I step into blessing.",
      "src": "Paraskara Grihya Sutra 3.4.5–6",
      "use": "core"
     }
    ]
   },
   {
    "title": "The fire offering for the house",
    "mantras": [
     {
      "at": "Here is joy",
      "do": "Once the sacred fire is lit inside the house, the first two offerings of ghee are made with:",
      "sa": "इह रतिरिह रमध्वमिह धृतिरिह स्वधृतिः स्वाहा ।",
      "tr": "iha ratiriha ramadhvamiha dhṛtiriha svadhṛtiḥ svāhā",
      "en": "Here is joy: be happy here. Here is steadiness, here a firm footing of your own. Svaha!",
      "src": "Paraskara Grihya Sutra 3.4.7; Vajasaneyi Samhita 8.51",
      "read": "#/read/yajurveda/8/1?v=51"
     },
     {
      "at": "To the guardian of the home",
      "do": "Four offerings of ghee are then made to Vastoshpati, the guardian spirit of the home, each verse ending with svaha; the first is:",
      "sa": "वास्तोष्पते प्रति जानीह्यस्मान्त्स्वावेशो अनमीवो भवा नः ।\nयत्त्वेमहे प्रति तन्नो जुषस्व शं नो भव द्विपदे शं चतुष्पदे ॥",
      "tr": "vāstoṣpate prati jānīhyasmāntsvāveśo anamīvo bhavā naḥ\nyattvemahe prati tanno juṣasva śaṃ no bhava dvipade śaṃ catuṣpade",
      "en": "Vastoshpati, guardian of the home, welcome us as your own. Give us a happy entry and keep all sickness away. Grant us what we ask of you, and bless our people and our animals.",
      "src": "Paraskara Grihya Sutra 3.4.7; Ashvalayana Grihya Sutra 2.9.9; Rig Veda 7.54.1",
      "use": "core",
      "read": "#/read/rigveda/8/54?v=1"
     },
     {
      "at": "A friend to the family",
      "do": "The fourth and last offering to Vastoshpati is made with:",
      "sa": "अमीवहा वास्तोष्पते विश्वा रूपाण्याविशन् । सखा सुशेव एधि नः ॥",
      "tr": "amīvahā vāstoṣpate viśvā rūpāṇyāviśan sakhā suśeva edhi naḥ",
      "en": "Vastoshpati, you who drive away sickness and take every form: be a kind and loving friend to us.",
      "src": "Paraskara Grihya Sutra 3.4.7; Rig Veda 7.55.1",
      "read": "#/read/rigveda/8/55?v=1"
     },
     {
      "at": "Asking for a happy home",
      "do": "Offerings of cooked rice follow, calling on the gods, the mountains, the times of day and the makers of all things to grant a home, and ending with:",
      "sa": "स्योनं शिवमिदं वास्तु दत्तं ब्रह्मप्रजापती ।\nसर्वाश्च देवताः स्वाहा ॥",
      "tr": "syonaṃ śivamidaṃ vāstu dattaṃ brahmaprajāpatī\nsarvāśca devatāḥ svāhā",
      "en": "Brahma and Prajapati, and all you gods: give us this home as a happy and blessed place. Svaha!",
      "src": "Paraskara Grihya Sutra 3.4.8",
      "use": "some"
     }
    ]
   },
   {
    "title": "Blessing the house",
    "mantras": [
     {
      "at": "Sprinkling the house",
      "do": "Water is sprinkled through the house in an unbroken stream with the three verses beginning:",
      "sa": "आपो हि ष्ठा मयोभुवस्ता न ऊर्जे दधातन । महे रणाय चक्षसे ॥",
      "tr": "āpo hi ṣṭhā mayobhuvastā na ūrje dadhātana mahe raṇāya cakṣase",
      "en": "Waters, you are the source of joy. Give us strength, so that we may see great happiness.",
      "src": "Ashvalayana Grihya Sutra 2.9.8; Paraskara Grihya Sutra 3.5.4; Vajasaneyi Samhita 11.50 (Rig Veda 10.9.1)",
      "read": "#/read/yajurveda/11/1?v=50"
     },
     {
      "at": "Touching the four sides",
      "do": "The householder touches the walls where they meet the posts on each side of the house, east, south, west and north, saying in turn:",
      "sa": "श्रीश्च त्वा यशश्च पूर्वे सन्धौ गोपायेताम् ।\nयज्ञश्च त्वा दक्षिणा च दक्षिणे सन्धौ गोपायेताम् ।\nअन्नं च त्वा ब्राह्मणाश्च पश्चिमे सन्धौ गोपायेताम् ।\nऊर्क्च त्वा सूनृता चोत्तरे सन्धौ गोपायेताम् ॥",
      "tr": "śrīśca tvā yaśaśca pūrve sandhau gopāyetām\nyajñaśca tvā dakṣiṇā ca dakṣiṇe sandhau gopāyetām\nannaṃ ca tvā brāhmaṇāśca paścime sandhau gopāyetām\nūrkca tvā sūnṛtā cottare sandhau gopāyetām",
      "en": "May good fortune and good name protect you on the east. May worship and generous giving protect you on the south. May food and the learned protect you on the west. May strength and kind words protect you on the north.",
      "src": "Paraskara Grihya Sutra 3.4.10–13"
     },
     {
      "at": "Honouring the directions",
      "do": "Stepping outside, the householder honours each direction in turn, beginning with the east (day and night then guard the south, food and breath the west, and the moon and the wind the north):",
      "sa": "केता च मा सुकेता च पुरस्ताद्गोपायेतामित्यग्निर्वै केतादित्यः सुकेता ।\nतौ प्रपद्ये ताभ्यां नमोऽस्तु तौ मा पुरस्ताद्गोपायेताम् ॥",
      "tr": "ketā ca mā suketā ca purastādgopāyetāmityagnirvai ketādityaḥ suketā\ntau prapadye tābhyāṃ namo'stu tau mā purastādgopāyetām",
      "en": "May Keta and Suketa protect me from the east. Agni is Keta and the sun is Suketa: I turn to them and bow to them; may they protect me from the east.",
      "src": "Paraskara Grihya Sutra 3.4.14–17",
      "use": "some"
     }
    ]
   },
   {
    "title": "Moving in",
    "mantras": [
     {
      "at": "Entering the finished home",
      "do": "When the house is ready to live in, the family enters it, naming dharma as its main pillar, prosperity as its roof and day and night as its two doors, and saying:",
      "sa": "इन्द्रस्य गृहा वसुमन्तो वरूथिनस्तानहं प्रपद्ये सह प्रजया पशुभिः सह ।",
      "tr": "indrasya gṛhā vasumanto varūthinastānahaṃ prapadye saha prajayā paśubhiḥ saha",
      "en": "This is Indra's house, rich and sheltering. I enter it with my children and with my animals.",
      "src": "Paraskara Grihya Sutra 3.4.18"
     },
     {
      "at": "Blessed is this home",
      "do": "After the priests and guests have shared a meal, the householder asks them to bless the house, and they say:",
      "sa": "शिवम् वास्तु शिवम् वास्तु",
      "tr": "śivam vāstu śivam vāstu",
      "en": "Blessed is this home! Blessed is this home!",
      "src": "Ashvalayana Grihya Sutra 2.9.9",
      "use": "some"
     }
    ]
   }
  ]
 },
 "shashtipurti": {
  "basis": "No Grihya Sutra has a chapter on the Shashtipurti. The rite appears only in later manuals, and its mantras are prayers for long life that the priest chooses from the Vedas. The verses here are verified Vedic prayers widely used for this purpose, including the Mahamrityunjaya mantra and the long-life formulas the Grihya Sutras give for a newborn child. Priests following South Indian manuals often add the Ayushya Sukta, Navagraha mantras and a full repetition of the wedding rites, so your family's ceremony may differ.",
  "groups": [
   {
    "title": "Prayers for long life",
    "mantras": [
     {
      "at": "A hundred autumns",
      "do": "The ceremony opens with the svasti-vachana, the verses of blessing, which include this prayer for a full life:",
      "sa": "शतमिन्नु शरदो अन्ति देवा यत्रा नश्चक्रा जरसं तनूनाम् ।\nपुत्रासो यत्र पितरो भवन्ति मा नो मध्या रीरिषतायुर्गन्तोः ॥",
      "tr": "śataminnu śarado anti devā yatrā naścakrā jarasaṃ tanūnām\nputrāso yatra pitaro bhavanti mā no madhyā rīriṣatāyurgantoḥ",
      "en": "A hundred autumns lie before us, O gods, in which you bring our bodies to old age, in which our sons become fathers in turn. Do not cut our life short before it has run its course.",
      "src": "Vajasaneyi Samhita 25.22 (Rig Veda 1.89.9)",
      "read": "#/read/yajurveda/25/1?v=22"
     },
     {
      "at": "The Mahamrityunjaya mantra",
      "do": "At the heart of the havan, the priest and family chant this mantra to Shiva, often 108 times, offering ghee into the fire:",
      "sa": "त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम् ।\nउर्वारुकमिव बन्धनान्मृत्योर्मुक्षीय मामृतात् ॥",
      "tr": "tryambakaṃ yajāmahe sugandhiṃ puṣṭivardhanam\nurvārukamiva bandhanānmṛtyormukṣīya māmṛtāt",
      "en": "We worship the three-eyed Lord, fragrant, who makes all life grow strong. As a ripe cucumber is freed from its vine, may I be freed from death, but not from immortality.",
      "src": "Rig Veda 7.59.12 (also Vajasaneyi Samhita 3.60)",
      "use": "core",
      "read": "#/read/rigveda/8/59?v=12"
     },
     {
      "at": "Freed to live",
      "do": "Offerings for health are made with the five verses of the Rig Veda's hymn for recovery and long life, beginning:",
      "sa": "मुञ्चामि त्वा हविषा जीवनाय कमज्ञातयक्ष्मादुत राजयक्ष्मात् ।\nग्राहिर्जग्राह यदि वैतदेनं तस्या इन्द्राग्नी प्र मुमुक्तमेनम् ॥",
      "tr": "muñcāmi tvā haviṣā jīvanāya kamajñātayakṣmāduta rājayakṣmāt\ngrāhirjagrāha yadi vaitadenaṃ tasyā indrāgnī pra mumuktamenam",
      "en": "With this offering I set you free to live, free from hidden illness and from wasting disease. If any grasping ill has taken hold of this dear one, Indra and Agni, set them free.",
      "src": "Rig Veda 10.161.1",
      "read": "#/read/rigveda/11/161?v=1"
     },
     {
      "at": "Live a hundred autumns",
      "do": "The fourth verse of the same hymn is the classic blessing for a long life:",
      "sa": "शतं जीव शरदो वर्धमानः शतं हेमन्ताञ्छतमु वसन्तान् ।\nशतमिन्द्राग्नी सविता बृहस्पतिः शतायुषा हविषेमं पुनर्दुः ॥",
      "tr": "śataṃ jīva śarado vardhamānaḥ śataṃ hemantāñchatamu vasantān\nśatamindrāgnī savitā bṛhaspatiḥ śatāyuṣā haviṣemaṃ punarduḥ",
      "en": "Live a hundred autumns, growing in strength, a hundred winters and a hundred springs. With this offering for a long life, may Indra and Agni, Savitr and Brihaspati give this dear one back to us for a hundred years.",
      "src": "Rig Veda 10.161.4",
      "read": "#/read/rigveda/11/161?v=4"
     },
     {
      "at": "Blessed with long life",
      "do": "Some priests bless the one turning sixty with the long-life formula a father says over his newborn child, which goes on to name the gods, the sages, the ancestors, sacrifice and the ocean:",
      "sa": "अग्निरायुष्मान्त्स वनस्पतिभिरायुष्मांस्तेन त्वाऽऽयुषाऽऽयुष्मन्तं करोमि ।\nसोम आयुष्मान्त्स ओषधीभिरायुष्मांस्तेनत्वाऽऽयुषाऽऽयुष्मन्तं करोमि ।",
      "tr": "agnirāyuṣmāntsa vanaspatibhirāyuṣmāṃstena tvā''yuṣā''yuṣmantaṃ karomi\nsoma āyuṣmāntsa oṣadhībhirāyuṣmāṃstenatvā''yuṣā''yuṣmantaṃ karomi",
      "en": "Agni is long-lived; through the trees he is long-lived: with that long life I make you long-lived. Soma is long-lived; through the healing plants he is long-lived: with that long life I make you long-lived.",
      "src": "Paraskara Grihya Sutra 1.16.6",
      "use": "some"
     },
     {
      "at": "The threefold life",
      "do": "Sacred ash from the fire is touched to the forehead, throat, right shoulder and heart, with one part of this verse for each:",
      "sa": "त्र्यायुषं जमदग्नेः कश्यपस्य त्र्यायुषम् ।\nयद्देवेषु त्र्यायुषं तन्नो अस्तु त्र्यायुषम् ॥",
      "tr": "tryāyuṣaṃ jamadagneḥ kaśyapasya tryāyuṣam\nyaddeveṣu tryāyuṣaṃ tanno astu tryāyuṣam",
      "en": "The threefold life of Jamadagni, the threefold life of Kashyapa, the threefold life the gods enjoy: may that threefold life be ours.",
      "src": "Vajasaneyi Samhita 3.62; Paraskara Grihya Sutra 1.16.7",
      "read": "#/read/yajurveda/3/1?v=62"
     }
    ]
   },
   {
    "title": "Blessing the couple",
    "mantras": [
     {
      "at": "The sacred bath",
      "do": "Water from the kalash, blessed during the puja, is poured over the couple with the three verses beginning:",
      "sa": "आपो हि ष्ठा मयोभुवस्ता न ऊर्जे दधातन । महे रणाय चक्षसे ॥",
      "tr": "āpo hi ṣṭhā mayobhuvastā na ūrje dadhātana mahe raṇāya cakṣase",
      "en": "Waters, you are the source of joy. Give us strength, so that we may see great happiness.",
      "src": "Vajasaneyi Samhita 36.14 (= 11.50; Rig Veda 10.9.1)",
      "read": "#/read/yajurveda/36/1?v=14"
     },
     {
      "at": "Renewing the vows",
      "do": "Renewing their wedding, the husband takes his wife's hand once more with the verse first said at their wedding, a prayer to grow old together:",
      "sa": "गृभ्णामि ते सौभगत्वाय हस्तं मया पत्या जरदष्टिर्यथासः ।\nभगो अर्यमा सविता पुरंधिर्मह्यं त्वादुर्गार्हपत्याय देवाः ॥",
      "tr": "gṛbhṇāmi te saubhagatvāya hastaṃ mayā patyā jaradaṣṭiryathāsaḥ\nbhago aryamā savitā puraṃdhirmahyaṃ tvādurgārhapatyāya devāḥ",
      "en": "I take your hand for our happiness, so that you may grow old with me, your husband. Bhaga, Aryaman, Savitr and Purandhi, the gods, have given you to me, to keep a home together.",
      "src": "Rig Veda 10.85.36 (Paraskara Grihya Sutra 1.6.3)",
      "use": "some",
      "read": "#/read/rigveda/11/85?v=36"
     },
     {
      "at": "Many more years",
      "do": "As the children and grandchildren honour the couple, everyone joins in this prayer for many more years of seeing, hearing and living:",
      "sa": "तच्चक्षुर्देवहितं पुरस्ताच्छुक्रमुच्चरत् ।\nपश्येम शरदः शतं जीवेम शरदः शतं शृणुयाम शरदः शतं\nप्र ब्रवाम शरदः शतमदीनाः स्याम शरदः शतं भूयश्च शरदः शतात् ॥",
      "tr": "taccakṣurdevahitaṃ purastācchukramuccarat\npaśyema śaradaḥ śataṃ jīvema śaradaḥ śataṃ śṛṇuyāma śaradaḥ śataṃ\npra bravāma śaradaḥ śatamadīnāḥ syāma śaradaḥ śataṃ bhūyaśca śaradaḥ śatāt",
      "en": "That bright eye set in place by the gods, the sun, is rising in the east. May we see a hundred autumns, live a hundred autumns, hear a hundred autumns, speak for a hundred autumns, live free from want for a hundred autumns, and more than a hundred autumns.",
      "src": "Vajasaneyi Samhita 36.24",
      "read": "#/read/yajurveda/36/1?v=24"
     }
    ]
   }
  ]
 },
 "antyeshti": {
  "basis": "This order follows the Ashvalayana Grihya Sutra (4.1–4.6), the fullest Grihya Sutra account of the funeral, with the Rig Veda funeral verses it quotes, together with the Paraskara Grihya Sutra (3.10) for the water offering and Katyayana's Shraddha Sutra for joining the ancestors; where a verse is also in the White Yajurveda (Vajasaneyi Samhita 35 and 40), that form is given. Family priests today usually work from a later handbook (paddhati) and add Puranic verses, so the choice and order of mantras, and the days on which the later rites fall, often differ.",
  "groups": [
   {
    "title": "Preparing the body",
    "mantras": [
     {
      "at": "Dressing the body",
      "do": "When the body has been washed, anointed with sandalwood and garlanded, the family wraps it in a new, unwashed cloth as the priest says:",
      "sa": "एतत् त्वा वासः प्रथमं न्वागन्नपैतदूह यदिहाबिभः पुरा ।\nइष्टापूर्तमनुसंक्राम विद्वान् यत्र ते दत्तं बहुधा विबन्धुषु ॥",
      "tr": "etat tvā vāsaḥ prathamaṃ nvāgannapaitadūha yadihābibhaḥ purā\niṣṭāpūrtamanusaṃkrāma vidvān yatra te dattaṃ bahudhā vibandhuṣu",
      "en": "This garment has now come to you first; lay aside what you wore here before. Knowing the way, go on to the good you have done in worship and in charity, wherever you gave your many gifts to those who had no one.",
      "src": "Kaushika Sutra 80.17; Atharva Veda 18.2.57",
      "use": "some",
      "read": "#/read/atharvaveda/18/2?v=57"
     }
    ]
   },
   {
    "title": "The procession and the pyre",
    "mantras": [
     {
      "at": "Clearing the cremation ground",
      "do": "On reaching the cremation ground, the chief mourner walks three times around the place with the left side towards it, sprinkling water from a shami branch and saying:",
      "sa": "अपेत वीत वि च सर्पतातोऽस्मा एतं पितरो लोकमक्रन् ।\nअहोभिरद्भिरक्तुभिर्व्यक्तं यमो ददात्यवसानमस्मै ॥",
      "tr": "apeta vīta vi ca sarpatāto'smā etaṃ pitaro lokamakran\nahobhiradbhiraktubhirvyaktaṃ yamo dadātyavasānamasmai",
      "en": "Go away, move off, slip away from here: the Fathers have made this place for him. Yama gives him a resting place, marked out by days, by waters and by nights.",
      "src": "Ashvalayana Grihya Sutra 4.2.10; Rig Veda 10.14.9",
      "read": "#/read/rigveda/11/14?v=9"
     }
    ]
   },
   {
    "title": "The fire",
    "mantras": [
     {
      "at": "Lighting the pyre",
      "do": "The chief mourner makes the last offering of ghee on the chest of the departed and sets the pyre alight, saying the person's name in place of \"asau\":",
      "sa": "अस्मात्त्वमधि जातोऽसि त्वदयं जायतां पुनः ।\nअसौ स्वर्गाय लोकाय स्वाहा ॥",
      "tr": "asmāttvamadhi jāto'si tvadayaṃ jāyatāṃ punaḥ\nasau svargāya lokāya svāhā",
      "en": "Agni, you were born from this one; now let him be born again from you. For [name], to the world of heaven: svaha!",
      "src": "Ashvalayana Grihya Sutra 4.3.27; Vajasaneyi Samhita 35.22",
      "use": "core",
      "read": "#/read/yajurveda/35/1?v=22"
     },
     {
      "at": "As the fire takes hold",
      "do": "While the body burns, the priest and the chief mourner recite the Rig Veda funeral verses over it, beginning with this one:",
      "sa": "प्रेहि प्रेहि पथिभिः पूर्व्येभिर्यत्रा नः पूर्वे पितरः परेयुः ।\nउभा राजाना स्वधया मदन्ता यमं पश्यासि वरुणं च देवम् ॥",
      "tr": "prehi prehi pathibhiḥ pūrvyebhiryatrā naḥ pūrve pitaraḥ pareyuḥ\nubhā rājānā svadhayā madantā yamaṃ paśyāsi varuṇaṃ ca devam",
      "en": "Go forth, go forth, on the ancient paths by which our forefathers went before us. There you will see the two kings rejoicing in the offerings, Yama and the god Varuna.",
      "src": "Ashvalayana Grihya Sutra 4.4.6; Rig Veda 10.14.7",
      "use": "core",
      "read": "#/read/rigveda/11/14?v=7"
     },
     {
      "at": "Back to the elements",
      "do": "Among the verses recited over the burning pyre is this one, which gives each part of the person back to the world:",
      "sa": "सूर्यं चक्षुर्गच्छतु वातमात्मा द्यां च गच्छ पृथिवीं च धर्मणा ।\nअपो वा गच्छ यदि तत्र ते हितमोषधीषु प्रति तिष्ठा शरीरैः ॥",
      "tr": "sūryaṃ cakṣurgacchatu vātamātmā dyāṃ ca gaccha pṛthivīṃ ca dharmaṇā\napo vā gaccha yadi tatra te hitamoṣadhīṣu prati tiṣṭhā śarīraiḥ",
      "en": "May your eye go to the sun and your breath to the wind. Go to the sky and to the earth, as is right; or go to the waters, if your place is there, and take root in the plants with all your limbs.",
      "src": "Ashvalayana Grihya Sutra 4.4.6 (the funeral verses); Rig Veda 10.16.3",
      "read": "#/read/rigveda/11/16?v=3"
     },
     {
      "at": "Breath to the wind",
      "do": "Many priests also recite this verse from the Isha Upanishad, the last chapter of the White Yajurveda, as the body burns:",
      "sa": "वायुरनिलममृतमथेदं भस्मान्तं शरीरम् ।\nओ३म् क्रतो स्मर । क्लिबे स्मर । कृतं स्मर ॥",
      "tr": "vāyuranilamamṛtamathedaṃ bhasmāntaṃ śarīram\nom krato smara klibe smara kṛtaṃ smara",
      "en": "Let the breath go to the wind, the deathless; this body ends in ashes. Om. Mind, remember. Remember, for the world to come. Remember all you have done.",
      "src": "Vajasaneyi Samhita 40.15 (Isha Upanishad 17)",
      "read": "#/read/yajurveda/40/1?v=15"
     },
     {
      "at": "Turning back to life",
      "do": "When the rites at the pyre are complete, this verse is said, and the mourners turn round and walk away without looking back:",
      "sa": "इमे जीवा वि मृतैराववृत्रन्नभूद्भद्रा देवहूतिर्नो अद्य ।\nप्राञ्चो अगाम नृतये हसाय द्राघीय आयुः प्रतरं दधानाः ॥",
      "tr": "ime jīvā vi mṛtairāvavṛtrannabhūdbhadrā devahūtirno adya\nprāñco agāma nṛtaye hasāya drāghīya āyuḥ prataraṃ dadhānāḥ",
      "en": "These living ones have turned away from the dead; our call to the gods today has been blessed. We go forward to dancing and laughter, holding on to a longer life.",
      "src": "Ashvalayana Grihya Sutra 4.4.9; Rig Veda 10.18.3",
      "read": "#/read/rigveda/11/18?v=3"
     }
    ]
   },
   {
    "title": "The water offering and the bones",
    "mantras": [
     {
      "at": "Water for the departed",
      "do": "The relatives bathe facing south, and each pours out one handful of water for the departed, saying their name (and gotra) in place of \"asau\":",
      "sa": "असावेतत्त उदकम्",
      "tr": "asāvetatta udakam",
      "en": "[Name], this water is for you.",
      "src": "Paraskara Grihya Sutra 3.10.21 (also Ashvalayana Grihya Sutra 4.4.10)",
      "use": "core"
     },
     {
      "at": "Water and milk for the night",
      "do": "That night, after the first pinda has been given in the departed's name, water and milk are set out in a clay pot hung in the open air with the words:",
      "sa": "प्रेतात्रस्नाहि",
      "tr": "pretātrasnāhi",
      "en": "Departed one, bathe here.",
      "src": "Paraskara Grihya Sutra 3.10.28",
      "use": "some"
     },
     {
      "at": "Laying the bones to rest",
      "do": "Some days later the bones are gathered into an urn, feet first and head last, and as the urn is laid in the earth the chief mourner says:",
      "sa": "उप सर्प मातरं भूमिमेतामुरुव्यचसं पृथिवीं सुशेवाम् ।\nऊर्णम्रदा युवतिर्दक्षिणावत एषा त्वा पातु निॠतेरुपस्थात् ॥",
      "tr": "upa sarpa mātaraṃ bhūmimetāmuruvyacasaṃ pṛthivīṃ suśevām\nūrṇamradā yuvatirdakṣiṇāvata eṣā tvā pātu niṝterupasthāt",
      "en": "Go now to the earth, your mother, this wide, open and kindly earth. Soft as wool to one who has been generous, may she, ever young, keep you from the lap of decay.",
      "src": "Ashvalayana Grihya Sutra 4.5.7; Rig Veda 10.18.10",
      "use": "some",
      "read": "#/read/rigveda/11/18?v=10"
     }
    ]
   },
   {
    "title": "The days after",
    "mantras": [
     {
      "at": "A new fire for the home",
      "do": "To end the time of mourning, the old fire is carried out of the house to the south with the first half of this verse, and a new household fire is kindled with the second half:",
      "sa": "क्रव्यादमग्निं प्र हिणोमि दूरं यमराज्यं गच्छतु रिप्रवाहः ।\nइहैवायमितरो जातवेदा देवेभ्यो हव्यं वहतु प्रजानन् ॥",
      "tr": "kravyādamagniṃ pra hiṇomi dūraṃ yamarājyaṃ gacchatu ripravāhaḥ\nihaivāyamitaro jātavedā devebhyo havyaṃ vahatu prajānan",
      "en": "I send the flesh-eating fire far away; let it go to Yama's kingdom and take all impurity with it. But let this other fire, which knows all beings, stay here and carry our offerings to the gods, for it knows the way.",
      "src": "Ashvalayana Grihya Sutra 4.6.2 and 4.6.5; Vajasaneyi Samhita 35.19 (Rig Veda 10.16.9)",
      "use": "some",
      "read": "#/read/yajurveda/35/1?v=19"
     },
     {
      "at": "Joining the ancestors",
      "do": "At the sapindikarana, on the twelfth day or at the end of the year, water from the departed's vessel is poured into the vessels of the three ancestors with this verse and the next, and the pindas are joined in the same way:",
      "sa": "ये समानाः समनसः पितरो यमराज्ये ।\nतेषाँल्लोकः स्वधा नमो यज्ञो देवेषु कल्पताम् ॥",
      "tr": "ye samānāḥ samanasaḥ pitaro yamarājye\nteṣā~llokaḥ svadhā namo yajño deveṣu kalpatām",
      "en": "The Fathers in Yama's kingdom, one with each other and one in mind: theirs is that world, with svadha and homage. May our offering be made complete among the gods.",
      "src": "Katyayana's Shraddha Sutra 5 (Paraskara parishishta); Vajasaneyi Samhita 19.45",
      "read": "#/read/yajurveda/19/1?v=45"
     }
    ]
   }
  ]
 },
 "shraddha": {
  "basis": "This follows Katyayana's Shraddha Sutra and his rule for the daily bath and tarpana (both printed with the Paraskara Grihya Sutra, the White Yajurveda manual), with the Vajasaneyi Samhita verses they name; the Ashvalayana Grihya Sutra (4.7) gives a close Rig Veda parallel. A family priest will usually add a sankalpa and Puranic formulas that name each ancestor with their gotra, and many families do tarpana and pinda daan without the full meal for brahmins.",
  "groups": [
   {
    "title": "Tarpana: water for the ancestors",
    "mantras": [
     {
      "at": "Water for Yama",
      "do": "After bathing, with the sacred thread over the right shoulder and facing south, the performer first offers three handfuls of water with black sesame to Yama, lord of the departed, under each of his fourteen names:",
      "sa": "यमाय धर्मराजाय मृत्यवे चान्तकाय च ।\nवैवस्वताय कालाय सर्वभूतक्षयाय च ।\nऔदुम्बराय दध्नाय नीलाय परमेष्ठिने ।\nवृकोदराय चित्राय चित्रगुप्ताय वै नमः ॥",
      "tr": "yamāya dharmarājāya mṛtyave cāntakāya ca\nvaivasvatāya kālāya sarvabhūtakṣayāya ca\naudumbarāya dadhnāya nīlāya parameṣṭhine\nvṛkodarāya citrāya citraguptāya vai namaḥ",
      "en": "Homage to Yama, the king of dharma; to Death and to the Ender; to the son of Vivasvan; to Time, which ends all beings; to Audumbara, Dadhna, Nila and Parameshthin; to Vrikodara, Chitra and Chitragupta.",
      "src": "Katyayana's Snana Sutra 3 (Paraskara parishishta)"
     },
     {
      "at": "Calling the Fathers",
      "do": "Then three handfuls of sesame water are poured for each ancestor, naming father, grandfather and great-grandfather (and the mother's side in the same way), while a series of Pitri verses is recited, beginning:",
      "sa": "उदीरतामवर उत्परास उन्मध्यमाः पितरः सोम्यासः ।\nअसुं य ईयुरवृका ऋतज्ञास्ते नोऽवन्तु पितरो हवेषु ॥",
      "tr": "udīratāmavara utparāsa unmadhyamāḥ pitaraḥ somyāsaḥ\nasuṃ ya īyuravṛkā ṛtajñāste no'vantu pitaro haveṣu",
      "en": "May the Fathers rise up, the lower, the higher and those in between, the gentle ones worthy of Soma. May those Fathers who have reached the life beyond, kindly and true, help us when we call to them.",
      "src": "Katyayana's Snana Sutra 3; Vajasaneyi Samhita 19.49 (Rig Veda 10.15.1)",
      "read": "#/read/yajurveda/19/1?v=49"
     },
     {
      "at": "Water that satisfies",
      "do": "Among these verses is this one, the heart of every tarpana:",
      "sa": "ऊर्जं वहन्तीरमृतं घृतं पयः कीलालं परिस्रुतम् ।\nस्वधा स्थ तर्पयत मे पितॄन् ॥",
      "tr": "ūrjaṃ vahantīramṛtaṃ ghṛtaṃ payaḥ kīlālaṃ parisrutam\nsvadhā stha tarpayata me pitṝn",
      "en": "You waters carry strength: nectar, ghee and milk, and sweet, flowing drink. You are svadha, the Fathers' food: satisfy my ancestors.",
      "src": "Katyayana's Snana Sutra 3; Vajasaneyi Samhita 2.34",
      "use": "core",
      "read": "#/read/yajurveda/2/1?v=34"
     },
     {
      "at": "Svadha to three generations",
      "do": "The verses go on with this one, and the tarpana closes with \"tripyadhvam\" (\"be satisfied\"), said three times, and the homage \"namo vah pitarah\":",
      "sa": "पितृभ्यः स्वधायिभ्यः स्वधा नमः\nपितामहेभ्यः स्वधायिभ्यः स्वधा नमः\nप्रपितामहेभ्यः स्वधायिभ्यः स्वधा नमः ।\nअक्षन् पितरो ऽमीमदन्त पितरो ऽतीतृपन्त पितरः पितरः शुन्धध्वम् ॥",
      "tr": "pitṛbhyaḥ svadhāyibhyaḥ svadhā namaḥ\npitāmahebhyaḥ svadhāyibhyaḥ svadhā namaḥ\nprapitāmahebhyaḥ svadhāyibhyaḥ svadhā namaḥ\nakṣan pitaro 'mīmadanta pitaro 'tītṛpanta pitaraḥ pitaraḥ śundhadhvam",
      "en": "To the Fathers who receive svadha: svadha and homage. To the grandfathers who receive svadha: svadha and homage. To the great-grandfathers who receive svadha: svadha and homage. The Fathers have eaten; the Fathers have rejoiced; the Fathers are satisfied. Fathers, be pure.",
      "src": "Katyayana's Snana Sutra 3; Vajasaneyi Samhita 19.36",
      "read": "#/read/yajurveda/19/1?v=36"
     },
     {
      "at": "For all who are owed water",
      "do": "Many families end the tarpana with one more handful of water, for every soul, kin or not, who has no one else to offer it:",
      "sa": "ये बान्धवाबान्धवा ये येऽन्यजन्मनि बान्धवाः ।\nते तृप्तिमखिला यान्तु ये चास्मत्तोऽभिवाञ्छति ॥",
      "tr": "ye bāndhavābāndhavā ye ye'nyajanmani bāndhavāḥ\nte tṛptimakhilā yāntu ye cāsmatto'bhivāñchati",
      "en": "Those who were our family and those who were not, and those who were our family in other lives: may they all be satisfied, and all who look to us for water.",
      "src": "Vishnu Purana 3.11.36"
     }
    ]
   },
   {
    "title": "Inviting the ancestors",
    "mantras": [
     {
      "at": "Inviting the Fathers",
      "do": "At the shraddha itself, after the All-Gods have been invited, the performer asks the guests who stand for the ancestors, \"Shall I invite the Fathers?\", and when they answer \"Invite them\", calls the ancestors to their seats, scattering sesame, with:",
      "sa": "उशन्तस्त्वा नि धीमह्युशन्तः समिधीमहि ।\nउशन्नुशत आ वह पितॄन् हविषे अत्तवे ॥",
      "tr": "uśantastvā ni dhīmahyuśantaḥ samidhīmahi\nuśannuśata ā vaha pitṝn haviṣe attave",
      "en": "Gladly we set you in place, Agni; gladly we kindle you. Gladly bring the Fathers, who long for it, to eat this offering.",
      "src": "Katyayana's Shraddha Sutra 2; Vajasaneyi Samhita 19.70",
      "use": "core",
      "read": "#/read/yajurveda/19/1?v=70"
     },
     {
      "at": "Welcoming them",
      "do": "Then the performer softly recites:",
      "sa": "आ यन्तु नः पितरः सोम्यासोऽग्निष्वात्ताः पथिभिर्देवयानैः ।\nअस्मिन् यज्ञे स्वधया मदन्तोऽधि ब्रुवन्तु तेऽवन्त्वस्मान् ॥",
      "tr": "ā yantu naḥ pitaraḥ somyāso'gniṣvāttāḥ pathibhirdevayānaiḥ\nasmin yajñe svadhayā madanto'dhi bruvantu te'vantvasmān",
      "en": "May our Fathers come, the gentle ones whom the fire has received, along the paths the gods travel. Rejoicing in the svadha at this offering, may they speak for us and protect us.",
      "src": "Katyayana's Shraddha Sutra 2; Vajasaneyi Samhita 19.58",
      "read": "#/read/yajurveda/19/1?v=58"
     }
    ]
   },
   {
    "title": "Water, sesame and the meal",
    "mantras": [
     {
      "at": "Sesame in the water",
      "do": "Water is poured over a kusha blade into a vessel for each ancestor with \"sham no devih\", and black sesame is dropped into each with:",
      "sa": "तिलोऽसि सोमदैवत्यो गोसवो देवनिर्मितः ।\nप्रत्नमद्भिः पृक्तः स्वधया पितॄँल्लोकान् प्रीणाहि नः स्वाहा ॥",
      "tr": "tilo'si somadaivatyo gosavo devanirmitaḥ\npratnamadbhiḥ pṛktaḥ svadhayā pitṝ~llokān prīṇāhi naḥ svāhā",
      "en": "You are sesame, sacred to Soma, made by the gods at the Gosava rite. Long ago you were mixed with water: with svadha, delight the Fathers and these worlds for us. Svaha!",
      "src": "Katyayana's Shraddha Sutra 2 (cf. Ashvalayana Grihya Sutra 4.7.11)"
     },
     {
      "at": "Serving the meal",
      "do": "After a portion of food has been offered in the fire, the meal is served to the guests who stand for the ancestors, and the performer touches each plate and says:",
      "sa": "पृथिवी ते पात्रं द्यौरपिधानं ब्राह्मणस्य मुखे अमृते अमृतं जुहोमि स्वाहा",
      "tr": "pṛthivī te pātraṃ dyaurapidhānaṃ brāhmaṇasya mukhe amṛte amṛtaṃ juhomi svāhā",
      "en": "The earth is your plate and the sky its cover. Into the deathless mouth of the brahmin I offer this deathless food. Svaha!",
      "src": "Katyayana's Shraddha Sutra 3"
     },
     {
      "at": "Sweetness for the satisfied",
      "do": "When the guests have eaten their fill, the performer recites the three \"honey\" verses, beginning:",
      "sa": "मधु वाता ऋतायते मधु क्षरन्ति सिन्धवः ।\nमाध्वीर्नः सन्त्वोषधीः ॥",
      "tr": "madhu vātā ṛtāyate madhu kṣaranti sindhavaḥ\nmādhvīrnaḥ santvoṣadhīḥ",
      "en": "For the one who keeps the sacred order, the winds blow sweetness and the rivers flow with sweetness. May the plants be sweet for us.",
      "src": "Katyayana's Shraddha Sutra 3; Ashvalayana Grihya Sutra 4.7.26; Vajasaneyi Samhita 13.27 (Rig Veda 1.90.6)",
      "read": "#/read/yajurveda/13/1?v=27"
     }
    ]
   },
   {
    "title": "The pinda offering",
    "mantras": [
     {
      "at": "Setting down the pindas",
      "do": "Three balls of rice (pindas) are laid on kusha grass, one each for father, grandfather and great-grandfather, naming each; the performer says the first line, turns away holding the breath, and turning back says the second:",
      "sa": "अत्र पितरो मादयध्वं यथाभागमावृषायध्वम् ।\nअमीमदन्त पितरो यथाभागमावृषायिषत ॥",
      "tr": "atra pitaro mādayadhvaṃ yathābhāgamāvṛṣāyadhvam\namīmadanta pitaro yathābhāgamāvṛṣāyiṣata",
      "en": "Fathers, rejoice here; come, each of you, eagerly to your own share. The Fathers have rejoiced; each has come eagerly to his share.",
      "src": "Katyayana's Shraddha Sutra 3 (\"as in the pinda-pitri-yajna\"); Vajasaneyi Samhita 2.31 (cf. Gobhila Grihya Sutra 4.3.11–12)",
      "read": "#/read/yajurveda/2/1?v=31"
     },
     {
      "at": "Homage over the pindas",
      "do": "With joined hands over the pindas, the performer pays homage to the ancestors in these words, which go on to ask the Fathers for a home and to offer them a garment (a thread laid on each pinda):",
      "sa": "नमो वः पितरो रसाय नमो वः पितरः शोषाय\nनमो वः पितरो जीवाय नमो वः पितरः स्वधायै\nनमो वः पितरो घोराय नमो वः पितरो मन्यवे",
      "tr": "namo vaḥ pitaro rasāya namo vaḥ pitaraḥ śoṣāya\nnamo vaḥ pitaro jīvāya namo vaḥ pitaraḥ svadhāyai\nnamo vaḥ pitaro ghorāya namo vaḥ pitaro manyave",
      "en": "Homage to you, Fathers, for the sap of life; homage to you, Fathers, for its fire. Homage to you, Fathers, for life itself; homage to you, Fathers, for svadha. Homage to you, Fathers, for your awesome power; homage to you, Fathers, for your fervour.",
      "src": "Katyayana's Shraddha Sutra 3 and Snana Sutra 3; Vajasaneyi Samhita 2.32 (cf. Gobhila Grihya Sutra 4.3.18–21)",
      "read": "#/read/yajurveda/2/1?v=32"
     }
    ]
   },
   {
    "title": "The close",
    "mantras": [
     {
      "at": "Asking for blessings",
      "do": "After water, flowers and rice are given for the ancestors' lasting satisfaction, the performer says \"May the Fathers be gentle\" and \"May our family grow\", the guests answer \"So be it\" each time, and the performer asks for their blessing with:",
      "sa": "दातारो नोऽभिवर्धन्तां वेदाः सन्ततिरेव च ।\nश्रद्धा च नो माव्यगमद्बहुधेयं च नोऽस्तु ॥",
      "tr": "dātāro no'bhivardhantāṃ vedāḥ santatireva ca\nśraddhā ca no māvyagamadbahudheyaṃ ca no'stu",
      "en": "May the givers in our family flourish, and our learning, and our children after us. May faith never leave us, and may we always have much to give.",
      "src": "Katyayana's Shraddha Sutra 3 (the same verse is in Manusmriti and the Yajnavalkya Smriti)"
     },
     {
      "at": "Bidding them farewell",
      "do": "After the guests have been asked to say \"svadha\" and have been given gifts, the ancestors are sent on their way with this verse, and the performer walks the guests out with the next (VS 9.19):",
      "sa": "वाजे-वाजेऽवत वाजिनो नो धनेषु विप्रा अमृता ऋतज्ञाः ।\nअस्य मध्वः पिबत मादयध्वं तृप्ता यात पथिभिर्देवयानैः ॥",
      "tr": "vāje-vāje'vata vājino no dhaneṣu viprā amṛtā ṛtajñāḥ\nasya madhvaḥ pibata mādayadhvaṃ tṛptā yāta pathibhirdevayānaiḥ",
      "en": "In every struggle help us, strong ones, wise and deathless, knowing the truth, in every gain. Drink this sweetness and rejoice; then, satisfied, go by the paths the gods travel.",
      "src": "Katyayana's Shraddha Sutra 3; Vajasaneyi Samhita 9.18",
      "use": "some",
      "read": "#/read/yajurveda/9/1?v=18"
     }
    ]
   }
  ]
 }
};
