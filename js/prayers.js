/*
 * Dharma Path prayer library.
 * Texts are traditional and in the public domain. Romanisations, introductions
 * and English translations are original to this app.
 *
 * Each prayer: { id, name, type, deity, moments, lang, author, about, japa?, verses }
 * verses: [devanagari, romanisation, english, label?]
 */
window.PRAYER_META = {
  types: [
    { id: "mantra", deva: "मन्त्र", name: "Mantras", one: "Mantra", about: "Short sacred formulas for chanting and japa" },
    { id: "shloka", deva: "श्लोक", name: "Shlokas", one: "Shloka", about: "Single verses for moments through the day" },
    { id: "stotra", deva: "स्तोत्र", name: "Stotras", one: "Stotra", about: "Sanskrit hymns of praise" },
    { id: "aarti", deva: "आरती", name: "Aartis", one: "Aarti", about: "Sung while waving the lamp" },
    { id: "chalisa", deva: "चालीसा", name: "Chalisas", one: "Chalisa", about: "Forty-verse devotional hymns" },
    { id: "bhajan", deva: "भजन", name: "Bhajans", one: "Bhajan", about: "Devotional songs of the saints" }
  ],
  deities: [
    { id: "ganesha", name: "Ganesha", deva: "गणेश" },
    { id: "shiva", name: "Shiva", deva: "शिव" },
    { id: "vishnu", name: "Vishnu", deva: "विष्णु" },
    { id: "krishna", name: "Krishna", deva: "कृष्ण" },
    { id: "rama", name: "Rama", deva: "राम" },
    { id: "hanuman", name: "Hanuman", deva: "हनुमान" },
    { id: "devi", name: "Durga & Devi", deva: "देवी" },
    { id: "lakshmi", name: "Lakshmi", deva: "लक्ष्मी" },
    { id: "saraswati", name: "Saraswati", deva: "सरस्वती" },
    { id: "surya", name: "Surya", deva: "सूर्य" },
    { id: "guru", name: "Guru", deva: "गुरु" },
    { id: "universal", name: "Universal", deva: "ॐ" }
  ],
  moments: [
    { id: "waking", name: "On waking" },
    { id: "bath", name: "While bathing" },
    { id: "morning", name: "Morning worship" },
    { id: "study", name: "Before study" },
    { id: "work", name: "Starting something new" },
    { id: "meal", name: "Before meals" },
    { id: "travel", name: "Before travel" },
    { id: "lamp", name: "Lighting the lamp" },
    { id: "evening", name: "Evening aarti" },
    { id: "sleep", name: "Before sleep" },
    { id: "peace", name: "For peace" },
    { id: "health", name: "For health and healing" },
    { id: "protection", name: "For courage and protection" }
  ]
};

window.PRAYERS = [
  /* ================================================================== */
  /* MANTRAS                                                             */
  /* ================================================================== */
  {
    id: "shiva", name: "Om Namah Shivaya", type: "mantra", deity: "shiva", japa: true,
    moments: ["morning", "peace", "evening"], lang: "Sanskrit", author: "Krishna Yajurveda, Shri Rudram",
    about: "The panchakshara, Shiva's five-syllable mantra, is the heart of the Shri Rudram in the Yajurveda. It can be repeated at any time, by anyone.",
    verses: [["ॐ नमः शिवाय", "oṃ namaḥ śivāya", "Om. I bow to Shiva, the auspicious one, the Self within all."]]
  },
  {
    id: "gayatri", name: "Gayatri Mantra", type: "mantra", deity: "surya", japa: true,
    moments: ["morning", "study", "waking"], lang: "Sanskrit", author: "Rig Veda 3.62.10, seer Vishvamitra",
    about: "The most revered verse of the Vedas, addressed to Savitr, the divine light of the sun. It is traditionally chanted at dawn, noon and dusk.",
    verses: [["ॐ भूर्भुवः स्वः\nतत्सवितुर्वरेण्यं\nभर्गो देवस्य धीमहि\nधियो यो नः प्रचोदयात्", "oṃ bhūr bhuvaḥ svaḥ\ntat savitur vareṇyaṃ\nbhargo devasya dhīmahi\ndhiyo yo naḥ pracodayāt", "Om. Earth, sky and heaven. We meditate on the glorious light of the divine Savitr. May that light inspire and guide our minds."]]
  },
  {
    id: "mahamrityunjaya", name: "Mahamrityunjaya Mantra", type: "mantra", deity: "shiva", japa: true,
    moments: ["health", "protection", "peace"], lang: "Sanskrit", author: "Rig Veda 7.59.12",
    about: "The “great death-conquering” mantra to Shiva as Tryambaka, the three-eyed one. It is chanted for healing, protection and release from fear.",
    verses: [["ॐ त्र्यम्बकं यजामहे\nसुगन्धिं पुष्टिवर्धनम्।\nउर्वारुकमिव बन्धनान्\nमृत्योर्मुक्षीय माऽमृतात्॥", "oṃ tryambakaṃ yajāmahe\nsugandhiṃ puṣṭivardhanam\nurvārukam iva bandhanān\nmṛtyor mukṣīya mā'mṛtāt", "We worship the three-eyed Lord, fragrant, who nourishes all life. As the ripe cucumber is freed from its vine, may we be freed from death, and never from immortality."]]
  },
  {
    id: "ganesh-mantra", name: "Om Gam Ganapataye Namah", type: "mantra", deity: "ganesha", japa: true,
    moments: ["work", "morning", "study"], lang: "Sanskrit", author: "Ganapati Atharvashirsha tradition",
    about: "Ganesha's seed-syllable mantra. “Gam” is his bija sound. Chant it before any beginning to clear the way.",
    verses: [["ॐ गं गणपतये नमः", "oṃ gaṃ gaṇapataye namaḥ", "Om. Salutations to Ganapati, lord of all beings, remover of obstacles."]]
  },
  {
    id: "vasudeva", name: "Om Namo Bhagavate Vasudevaya", type: "mantra", deity: "vishnu", japa: true,
    moments: ["morning", "peace", "evening"], lang: "Sanskrit", author: "Bhagavata Purana",
    about: "The twelve-syllable mantra (dvadashakshari) to Vishnu and Krishna, beloved of devotees since the Bhagavata Purana.",
    verses: [["ॐ नमो भगवते वासुदेवाय", "oṃ namo bhagavate vāsudevāya", "Om. I bow to the Blessed Lord Vasudeva, who dwells in all beings."]]
  },
  {
    id: "narayana", name: "Om Namo Narayanaya", type: "mantra", deity: "vishnu", japa: true,
    moments: ["morning", "peace", "sleep"], lang: "Sanskrit", author: "Narayana Upanishad",
    about: "The eight-syllable mantra (ashtakshari) of Narayana, the refuge of all beings, central to Sri Vaishnava worship.",
    verses: [["ॐ नमो नारायणाय", "oṃ namo nārāyaṇāya", "Om. Salutations to Narayana, the resting place of all beings."]]
  },
  {
    id: "hare-krishna", name: "Hare Krishna Maha Mantra", type: "mantra", deity: "krishna", japa: true,
    moments: ["morning", "evening", "peace"], lang: "Sanskrit", author: "Kali-Santarana Upanishad",
    about: "The “great mantra” of sixteen names, popularised by Chaitanya Mahaprabhu as the simplest path of devotion for this age.",
    verses: [["हरे राम हरे राम राम राम हरे हरे।\nहरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे॥", "hare rāma hare rāma rāma rāma hare hare\nhare kṛṣṇa hare kṛṣṇa kṛṣṇa kṛṣṇa hare hare", "A call to the Divine through the names Hari, Rama and Krishna, asking to be drawn into loving service."]]
  },
  {
    id: "rama-mantra", name: "Shri Ram Jai Ram", type: "mantra", deity: "rama", japa: true,
    moments: ["morning", "peace", "protection"], lang: "Sanskrit", author: "Traditional; made famous by Samarth Ramdas",
    about: "The thirteen-syllable Rama mantra, chanted by saints such as Samarth Ramdas and still sung in homes and temples across India.",
    verses: [["श्री राम जय राम जय जय राम", "śrī rāma jaya rāma jaya jaya rāma", "Glory to Shri Rama. Victory to Rama, victory, victory to Rama."]]
  },
  {
    id: "hanuman-mantra", name: "Om Shri Hanumate Namah", type: "mantra", deity: "hanuman", japa: true,
    moments: ["protection", "morning", "health"], lang: "Sanskrit", author: "Traditional",
    about: "A simple salutation to Hanuman, traditionally chanted on Tuesdays and Saturdays for strength, courage and protection.",
    verses: [["ॐ श्री हनुमते नमः", "oṃ śrī hanumate namaḥ", "Om. Salutations to the glorious Hanuman."]]
  },
  {
    id: "durga-mantra", name: "Om Dum Durgayai Namah", type: "mantra", deity: "devi", japa: true,
    moments: ["protection", "morning"], lang: "Sanskrit", author: "Traditional",
    about: "Durga's mantra with her bija syllable “dum”. It is especially chanted during Navaratri.",
    verses: [["ॐ दुं दुर्गायै नमः", "oṃ duṃ durgāyai namaḥ", "Om. Salutations to Durga, the invincible Mother who protects her children."]]
  },
  {
    id: "lakshmi-mantra", name: "Om Shreem Mahalakshmyai Namah", type: "mantra", deity: "lakshmi", japa: true,
    moments: ["morning", "work", "lamp"], lang: "Sanskrit", author: "Traditional",
    about: "Lakshmi's mantra with her bija syllable “shreem”, chanted for abundance in every sense: wealth, harmony and grace. Fridays and Diwali are her special days.",
    verses: [["ॐ श्रीं महालक्ष्म्यै नमः", "oṃ śrīṃ mahālakṣmyai namaḥ", "Om. Salutations to the great Lakshmi, source of all good fortune."]]
  },
  {
    id: "saraswati-mantra", name: "Om Aim Saraswatyai Namah", type: "mantra", deity: "saraswati", japa: true,
    moments: ["study", "morning"], lang: "Sanskrit", author: "Traditional",
    about: "Saraswati's mantra with her bija syllable “aim”. Students chant it before study and examinations.",
    verses: [["ॐ ऐं सरस्वत्यै नमः", "oṃ aiṃ sarasvatyai namaḥ", "Om. Salutations to Saraswati, goddess of wisdom, speech and the arts."]]
  },
  {
    id: "surya-mantra", name: "Om Suryaya Namah", type: "mantra", deity: "surya", japa: true,
    moments: ["waking", "morning", "health"], lang: "Sanskrit", author: "Traditional",
    about: "A greeting to the Sun, often repeated while offering water at sunrise or with each round of Surya Namaskar.",
    verses: [["ॐ सूर्याय नमः", "oṃ sūryāya namaḥ", "Om. Salutations to Surya, the Sun, giver of light and life."]]
  },
  {
    id: "lokah", name: "Lokah Samastah", type: "mantra", deity: "universal", japa: true,
    moments: ["peace", "evening", "sleep"], lang: "Sanskrit", author: "Traditional closing prayer",
    about: "A short universal blessing often used to close prayer, yoga or meditation.",
    verses: [["लोकाः समस्ताः सुखिनो भवन्तु", "lokāḥ samastāḥ sukhino bhavantu", "May all beings in all the worlds be happy."]]
  },

  /* ================================================================== */
  /* SHLOKAS                                                             */
  /* ================================================================== */
  {
    id: "morning", name: "Karagre Vasate", type: "shloka", deity: "universal",
    moments: ["waking"], lang: "Sanskrit", author: "Traditional",
    about: "Said on waking while looking at your open palms, before anything else. It reminds us that wealth, wisdom and the Divine are present in the work of our own hands.",
    verses: [["कराग्रे वसते लक्ष्मीः करमध्ये सरस्वती।\nकरमूले तु गोविन्दः प्रभाते करदर्शनम्॥", "karāgre vasate lakṣmīḥ karamadhye sarasvatī\nkaramūle tu govindaḥ prabhāte karadarśanam", "Lakshmi dwells at the fingertips, Saraswati in the palm, and Govinda at the base of the hand. So look at your hands at dawn."]]
  },
  {
    id: "bhumi", name: "Samudra Vasane Devi", type: "shloka", deity: "universal",
    moments: ["waking"], lang: "Sanskrit", author: "Traditional",
    about: "Said as your feet first touch the floor in the morning, asking Mother Earth's pardon for stepping on her.",
    verses: [["समुद्रवसने देवि पर्वतस्तनमण्डले।\nविष्णुपत्नि नमस्तुभ्यं पादस्पर्शं क्षमस्व मे॥", "samudravasane devi parvatastanamaṇḍale\nviṣṇupatni namas tubhyaṃ pādasparśaṃ kṣamasva me", "O Goddess Earth, robed in the oceans and adorned with mountains, consort of Vishnu, I bow to you. Forgive me for touching you with my feet."]]
  },
  {
    id: "ganga-snana", name: "Gange Cha Yamune", type: "shloka", deity: "universal",
    moments: ["bath"], lang: "Sanskrit", author: "Traditional",
    about: "Said while bathing, inviting the seven sacred rivers of India into the water so that every bath becomes a holy dip.",
    verses: [["गङ्गे च यमुने चैव गोदावरि सरस्वति।\nनर्मदे सिन्धु कावेरि जलेऽस्मिन् सन्निधिं कुरु॥", "gaṅge ca yamune caiva godāvari sarasvati\nnarmade sindhu kāveri jale'smin sannidhiṃ kuru", "O Ganga and Yamuna, Godavari and Saraswati, Narmada, Sindhu and Kaveri: be present in this water."]]
  },
  {
    id: "ganesha", name: "Vakratunda Mahakaya", type: "shloka", deity: "ganesha",
    moments: ["work", "morning", "study", "travel"], lang: "Sanskrit", author: "Traditional",
    about: "The best-known prayer to Ganesha, said before beginning any task, journey, ceremony or study.",
    verses: [["वक्रतुण्ड महाकाय सूर्यकोटि समप्रभ।\nनिर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥", "vakratuṇḍa mahākāya sūryakoṭi samaprabha\nnirvighnaṃ kuru me deva sarvakāryeṣu sarvadā", "O Lord with the curved trunk and mighty form, radiant as ten million suns: remove every obstacle from all my undertakings, always."]]
  },
  {
    id: "shuklambaradharam", name: "Shuklambaradharam", type: "shloka", deity: "ganesha",
    moments: ["work", "morning"], lang: "Sanskrit", author: "Traditional",
    about: "Recited at the start of pujas and recitations, especially in South India, to invoke Ganesha's blessing.",
    verses: [["शुक्लाम्बरधरं विष्णुं शशिवर्णं चतुर्भुजम्।\nप्रसन्नवदनं ध्यायेत् सर्वविघ्नोपशान्तये॥", "śuklāmbaradharaṃ viṣṇuṃ śaśivarṇaṃ caturbhujam\nprasannavadanaṃ dhyāyet sarvavighnopaśāntaye", "Meditate on the all-pervading one, dressed in white, bright as the moon, four-armed and smiling, so that every obstacle may be calmed."]]
  },
  {
    id: "saraswati", name: "Saraswati Namastubhyam", type: "shloka", deity: "saraswati",
    moments: ["study"], lang: "Sanskrit", author: "Traditional",
    about: "Said by students before opening their books, and by anyone beginning to learn something new.",
    verses: [["सरस्वति नमस्तुभ्यं वरदे कामरूपिणि।\nविद्यारम्भं करिष्यामि सिद्धिर्भवतु मे सदा॥", "sarasvati namas tubhyaṃ varade kāmarūpiṇi\nvidyārambhaṃ kariṣyāmi siddhir bhavatu me sadā", "Salutations to you, Saraswati, giver of blessings, who takes any form you wish. I am beginning my studies: may I always succeed."]]
  },
  {
    id: "ya-kundendu", name: "Ya Kundendu", type: "shloka", deity: "saraswati",
    moments: ["study", "morning"], lang: "Sanskrit", author: "Traditional dhyana verse",
    about: "A meditation verse describing Saraswati in white, seated on a white lotus with her veena. It is sung at Vasant Panchami and in schools across India.",
    verses: [["या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता\nया वीणावरदण्डमण्डितकरा या श्वेतपद्मासना।\nया ब्रह्माच्युतशङ्करप्रभृतिभिर्देवैः सदा वन्दिता\nसा मां पातु सरस्वती भगवती निःशेषजाड्यापहा॥", "yā kundendutuṣārahāradhavalā yā śubhravastrāvṛtā\nyā vīṇāvaradaṇḍamaṇḍitakarā yā śvetapadmāsanā\nyā brahmācyutaśaṅkaraprabhṛtibhir devaiḥ sadā vanditā\nsā māṃ pātu sarasvatī bhagavatī niḥśeṣajāḍyāpahā", "She who is white as jasmine, the moon, snow and a string of pearls, who is dressed in white, whose hands hold the beautiful veena, who sits on a white lotus, and whom Brahma, Vishnu, Shiva and all the gods ever praise: may that blessed Saraswati, who removes all dullness of mind, protect me."]]
  },
  {
    id: "guru", name: "Gurur Brahma", type: "shloka", deity: "guru",
    moments: ["study", "morning"], lang: "Sanskrit", author: "Guru Gita",
    about: "The classic salutation to the teacher, who is seen as the Divine itself. It is said before lessons and on Guru Purnima.",
    verses: [["गुरुर्ब्रह्मा गुरुर्विष्णुः गुरुर्देवो महेश्वरः।\nगुरुः साक्षात् परब्रह्म तस्मै श्रीगुरवे नमः॥", "gurur brahmā gurur viṣṇuḥ gurur devo maheśvaraḥ\nguruḥ sākṣāt parabrahma tasmai śrīgurave namaḥ", "The guru is Brahma, the guru is Vishnu, the guru is the god Maheshvara. The guru is the Supreme Reality itself. To that revered guru I bow."]]
  },
  {
    id: "shantakaram", name: "Shantakaram Bhujagashayanam", type: "shloka", deity: "vishnu",
    moments: ["morning", "peace", "sleep"], lang: "Sanskrit", author: "Traditional dhyana verse",
    about: "A meditation on Vishnu resting on the serpent Shesha, at peace beyond the storms of the world.",
    verses: [["शान्ताकारं भुजगशयनं पद्मनाभं सुरेशं\nविश्वाधारं गगनसदृशं मेघवर्णं शुभाङ्गम्।\nलक्ष्मीकान्तं कमलनयनं योगिभिर्ध्यानगम्यं\nवन्दे विष्णुं भवभयहरं सर्वलोकैकनाथम्॥", "śāntākāraṃ bhujagaśayanaṃ padmanābhaṃ sureśaṃ\nviśvādhāraṃ gaganasadṛśaṃ meghavarṇaṃ śubhāṅgam\nlakṣmīkāntaṃ kamalanayanaṃ yogibhir dhyānagamyaṃ\nvande viṣṇuṃ bhavabhayaharaṃ sarvalokaikanātham", "I bow to Vishnu: serene in form, resting on the serpent, a lotus rising from his navel, lord of the gods. He is the support of the universe, vast as the sky, dark as a rain cloud and beautiful in every limb. Beloved of Lakshmi, lotus-eyed, reached by yogis in meditation, he removes the fear of worldly existence and is the one lord of all worlds."]]
  },
  {
    id: "vanamali", name: "Vanamali Gadi Sharngi", type: "shloka", deity: "vishnu",
    moments: ["travel", "protection"], lang: "Sanskrit", author: "Vishnu Sahasranama, closing verse",
    about: "A protective verse naming Vishnu's sacred emblems, traditionally said before setting out on a journey.",
    verses: [["वनमाली गदी शार्ङ्गी शङ्खी चक्री च नन्दकी।\nश्रीमान् नारायणो विष्णुर्वासुदेवोऽभिरक्षतु॥", "vanamālī gadī śārṅgī śaṅkhī cakrī ca nandakī\nśrīmān nārāyaṇo viṣṇur vāsudevo'bhirakṣatu", "May the glorious Narayana, Vishnu, Vasudeva, who wears the garland of forest flowers and bears the mace, the bow Sharnga, the conch, the discus and the sword Nandaka, protect us on every side."]]
  },
  {
    id: "krishna-vande", name: "Vasudeva Sutam Devam", type: "shloka", deity: "krishna",
    moments: ["morning", "study"], lang: "Sanskrit", author: "Traditional, recited before the Bhagavad Gita",
    about: "A salutation to Krishna as the teacher of the world, often recited before reading the Bhagavad Gita.",
    verses: [["वसुदेवसुतं देवं कंसचाणूरमर्दनम्।\nदेवकीपरमानन्दं कृष्णं वन्दे जगद्गुरुम्॥", "vasudevasutaṃ devaṃ kaṃsacāṇūramardanam\ndevakīparamānandaṃ kṛṣṇaṃ vande jagadgurum", "I bow to Krishna, the teacher of the world: the divine son of Vasudeva, destroyer of Kamsa and Chanura, the supreme joy of his mother Devaki."]]
  },
  {
    id: "ramaya", name: "Ramaya Ramabhadraya", type: "shloka", deity: "rama",
    moments: ["morning", "protection"], lang: "Sanskrit", author: "Rama Raksha Stotra",
    about: "A verse from the Rama Raksha Stotra, the “armour of Rama”, offering salutations through his many names.",
    verses: [["रामाय रामभद्राय रामचन्द्राय वेधसे।\nरघुनाथाय नाथाय सीतायाः पतये नमः॥", "rāmāya rāmabhadrāya rāmacandrāya vedhase\nraghunāthāya nāthāya sītāyāḥ pataye namaḥ", "Salutations to Rama, the auspicious Rama, the moon-like Rama, the creator; to the lord of the Raghus, the Lord himself, the husband of Sita."]]
  },
  {
    id: "rama-rameti", name: "Shri Rama Rama Rameti", type: "shloka", deity: "rama",
    moments: ["peace", "evening"], lang: "Sanskrit", author: "Vishnu Sahasranama (Padma Purana)",
    about: "Shiva's words to Parvati: repeating the name of Rama three times equals reciting all thousand names of Vishnu.",
    verses: [["श्री राम राम रामेति रमे रामे मनोरमे।\nसहस्रनाम तत्तुल्यं रामनाम वरानने॥", "śrī rāma rāma rāmeti rame rāme manorame\nsahasranāma tat tulyaṃ rāmanāma varānane", "O lovely one, I delight in Rama, Rama, Rama. The single name of Rama is equal to the thousand names of Vishnu, O fair-faced one."]]
  },
  {
    id: "manojavam", name: "Manojavam Marutatulyavegam", type: "shloka", deity: "hanuman",
    moments: ["protection", "travel", "morning"], lang: "Sanskrit", author: "Traditional",
    about: "The classic refuge-verse to Hanuman, swift as thought and master of his senses.",
    verses: [["मनोजवं मारुततुल्यवेगं जितेन्द्रियं बुद्धिमतां वरिष्ठम्।\nवातात्मजं वानरयूथमुख्यं श्रीरामदूतं शरणं प्रपद्ये॥", "manojavaṃ mārutatulyavegaṃ jitendriyaṃ buddhimatāṃ variṣṭham\nvātātmajaṃ vānarayūthamukhyaṃ śrīrāmadūtaṃ śaraṇaṃ prapadye", "I take refuge in the messenger of Shri Rama: swift as the mind, fast as the wind, master of the senses, foremost among the wise, son of the wind god and leader of the vanara army."]]
  },
  {
    id: "ramaskandam", name: "Ramaskandam Hanumantam", type: "shloka", deity: "hanuman",
    moments: ["sleep", "protection"], lang: "Sanskrit", author: "Traditional",
    about: "A bedtime verse said to keep away bad dreams by remembering four mighty protectors.",
    verses: [["रामस्कन्दं हनूमन्तं वैनतेयं वृकोदरम्।\nशयने यः स्मरेन्नित्यं दुःस्वप्नं तस्य नश्यति॥", "rāmaskandaṃ hanūmantaṃ vainateyaṃ vṛkodaram\nśayane yaḥ smaren nityaṃ duḥsvapnaṃ tasya naśyati", "Whoever remembers Rama, Skanda, Hanuman, Garuda and Bhima every night at bedtime is freed from bad dreams."]]
  },
  {
    id: "karpura-gauram", name: "Karpura Gauram", type: "shloka", deity: "shiva",
    moments: ["evening", "lamp"], lang: "Sanskrit", author: "Traditional, sung after aarti",
    about: "Sung at the close of almost every aarti, this verse pictures Shiva, white as camphor, dwelling in the lotus of the heart with Parvati.",
    verses: [["कर्पूरगौरं करुणावतारं संसारसारं भुजगेन्द्रहारम्।\nसदा वसन्तं हृदयारविन्दे भवं भवानीसहितं नमामि॥", "karpūragauraṃ karuṇāvatāraṃ saṃsārasāraṃ bhujagendrahāram\nsadā vasantaṃ hṛdayāravinde bhavaṃ bhavānīsahitaṃ namāmi", "White as camphor, compassion itself, the essence of existence, wearing the king of serpents as a garland, ever dwelling in the lotus of the heart: to Shiva, with Bhavani, I bow."]]
  },
  {
    id: "kara-charana", name: "Kara Charana Kritam", type: "shloka", deity: "shiva",
    moments: ["sleep", "peace"], lang: "Sanskrit", author: "Shiva Aparadha Kshamapana Stotra, attributed to Adi Shankara",
    about: "A prayer for forgiveness said at night, letting go of the day's mistakes before sleep.",
    verses: [["करचरणकृतं वाक्कायजं कर्मजं वा\nश्रवणनयनजं वा मानसं वापराधम्।\nविहितमविहितं वा सर्वमेतत्क्षमस्व\nजय जय करुणाब्धे श्रीमहादेव शम्भो॥", "karacaraṇakṛtaṃ vākkāyajaṃ karmajaṃ vā\nśravaṇanayanajaṃ vā mānasaṃ vāparādham\nvihitam avihitaṃ vā sarvam etat kṣamasva\njaya jaya karuṇābdhe śrīmahādeva śambho", "Whatever wrong I have done with my hands or feet, by speech or body, by action, through my ears or eyes, or in my mind, whether knowingly or unknowingly, forgive it all. Glory, glory to you, ocean of compassion, great god Shambhu."]]
  },
  {
    id: "sarva-mangala", name: "Sarva Mangala Mangalye", type: "shloka", deity: "devi",
    moments: ["morning", "protection", "evening"], lang: "Sanskrit", author: "Devi Mahatmya 11.10",
    about: "A salutation to the Goddess as Narayani, from the Devi Mahatmya. It is one of the most widely recited verses to the Divine Mother.",
    verses: [["सर्वमङ्गलमाङ्गल्ये शिवे सर्वार्थसाधिके।\nशरण्ये त्र्यम्बके गौरि नारायणि नमोऽस्तु ते॥", "sarvamaṅgalamāṅgalye śive sarvārthasādhike\nśaraṇye tryambake gauri nārāyaṇi namo'stu te", "O auspiciousness of all that is auspicious, gracious one who fulfils every aim, refuge of all, three-eyed Gauri, Narayani: salutations to you."]]
  },
  {
    id: "ya-devi", name: "Ya Devi Sarvabhuteshu", type: "shloka", deity: "devi",
    moments: ["morning", "peace", "protection"], lang: "Sanskrit", author: "Devi Mahatmya, chapter 5",
    about: "From the hymn of the gods in the Devi Mahatmya, saluting the Goddess as she lives in every being. It is chanted throughout Navaratri.",
    verses: [
      ["या देवी सर्वभूतेषु शक्तिरूपेण संस्थिता।\nनमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः॥", "yā devī sarvabhūteṣu śaktirūpeṇa saṃsthitā\nnamas tasyai namas tasyai namas tasyai namo namaḥ", "To the Goddess who dwells in all beings as power: salutations to her, salutations to her, salutations to her, again and again."],
      ["या देवी सर्वभूतेषु मातृरूपेण संस्थिता।\nनमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः॥", "yā devī sarvabhūteṣu mātṛrūpeṇa saṃsthitā\nnamas tasyai namas tasyai namas tasyai namo namaḥ", "To the Goddess who dwells in all beings as the mother: salutations to her, again and again."],
      ["या देवी सर्वभूतेषु बुद्धिरूपेण संस्थिता।\nनमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः॥", "yā devī sarvabhūteṣu buddhirūpeṇa saṃsthitā\nnamas tasyai namas tasyai namas tasyai namo namaḥ", "To the Goddess who dwells in all beings as intelligence: salutations to her, again and again."],
      ["या देवी सर्वभूतेषु शान्तिरूपेण संस्थिता।\nनमस्तस्यै नमस्तस्यै नमस्तस्यै नमो नमः॥", "yā devī sarvabhūteṣu śāntirūpeṇa saṃsthitā\nnamas tasyai namas tasyai namas tasyai namo namaḥ", "To the Goddess who dwells in all beings as peace: salutations to her, again and again."]
    ]
  },
  {
    id: "mahalakshmi", name: "Namastestu Mahamaye", type: "shloka", deity: "lakshmi",
    moments: ["morning", "lamp", "work"], lang: "Sanskrit", author: "Mahalakshmi Ashtakam, Padma Purana",
    about: "The opening verse of the Mahalakshmi Ashtakam, recited on Fridays and at Diwali.",
    verses: [["नमस्तेऽस्तु महामाये श्रीपीठे सुरपूजिते।\nशङ्खचक्रगदाहस्ते महालक्ष्मि नमोऽस्तु ते॥", "namas te'stu mahāmāye śrīpīṭhe surapūjite\nśaṅkhacakragadāhaste mahālakṣmi namo'stu te", "Salutations to you, great Maya, seated on the throne of fortune and worshipped by the gods. You who hold the conch, discus and mace: great Lakshmi, salutations to you."]]
  },
  {
    id: "annapurna", name: "Annapurne Sadapurne", type: "shloka", deity: "devi",
    moments: ["meal"], lang: "Sanskrit", author: "Annapurna Stotram, attributed to Adi Shankara",
    about: "A prayer to Annapurna, the Goddess of nourishment, said before eating. Notice that the alms asked for are wisdom and detachment.",
    verses: [["अन्नपूर्णे सदापूर्णे शङ्करप्राणवल्लभे।\nज्ञानवैराग्यसिद्ध्यर्थं भिक्षां देहि च पार्वति॥", "annapūrṇe sadāpūrṇe śaṅkaraprāṇavallabhe\njñānavairāgyasiddhyarthaṃ bhikṣāṃ dehi ca pārvati", "O Annapurna, ever full, beloved of Shankara: Mother Parvati, grant me alms, so that I may attain wisdom and detachment."]]
  },
  {
    id: "brahmarpanam", name: "Brahmarpanam", type: "shloka", deity: "universal",
    moments: ["meal"], lang: "Sanskrit", author: "Bhagavad Gita 4.24 and 15.14",
    about: "Two verses from the Bhagavad Gita said before meals. They turn eating into an offering in which the food, the eater and the act are all seen as the Divine.",
    verses: [
      ["ब्रह्मार्पणं ब्रह्म हविर्ब्रह्माग्नौ ब्रह्मणा हुतम्।\nब्रह्मैव तेन गन्तव्यं ब्रह्मकर्मसमाधिना॥", "brahmārpaṇaṃ brahma havir brahmāgnau brahmaṇā hutam\nbrahmaiva tena gantavyaṃ brahmakarmasamādhinā", "The offering is Brahman, the oblation is Brahman, offered by Brahman into the fire that is Brahman. One who sees Brahman in every action reaches Brahman alone."],
      ["अहं वैश्वानरो भूत्वा प्राणिनां देहमाश्रितः।\nप्राणापानसमायुक्तः पचाम्यन्नं चतुर्विधम्॥", "ahaṃ vaiśvānaro bhūtvā prāṇināṃ deham āśritaḥ\nprāṇāpānasamāyuktaḥ pacāmy annaṃ caturvidham", "Krishna says: “Becoming the fire of life within the bodies of all beings, joined with the incoming and outgoing breath, I digest the four kinds of food.”"]
    ]
  },
  {
    id: "deepa-jyoti", name: "Shubham Karoti", type: "shloka", deity: "universal",
    moments: ["lamp", "evening"], lang: "Sanskrit", author: "Traditional",
    about: "Said at dusk when lighting the lamp (diya) in the home shrine, welcoming light as a form of the Divine.",
    verses: [
      ["शुभं करोति कल्याणमारोग्यं धनसम्पदा।\nशत्रुबुद्धिविनाशाय दीपज्योतिर्नमोऽस्तु ते॥", "śubhaṃ karoti kalyāṇam ārogyaṃ dhanasampadā\nśatrubuddhivināśāya dīpajyotir namo'stu te", "You bring goodness, wellbeing, health and prosperity, and you destroy hostile thoughts. O light of the lamp, I bow to you."],
      ["दीपज्योतिः परब्रह्म दीपज्योतिर्जनार्दनः।\nदीपो हरतु मे पापं दीपज्योतिर्नमोऽस्तु ते॥", "dīpajyotiḥ parabrahma dīpajyotir janārdanaḥ\ndīpo haratu me pāpaṃ dīpajyotir namo'stu te", "The light of the lamp is the Supreme Brahman; the light of the lamp is Janardana. May the lamp remove my wrongdoing. O light of the lamp, I bow to you."]
    ]
  },
  {
    id: "japa-kusuma", name: "Japa Kusuma Sankasham", type: "shloka", deity: "surya",
    moments: ["waking", "morning", "health"], lang: "Sanskrit", author: "Navagraha Stotra, attributed to Vyasa",
    about: "Said while offering water to the rising sun (arghya), honouring Surya as the dispeller of darkness.",
    verses: [["जपाकुसुमसङ्काशं काश्यपेयं महाद्युतिम्।\nतमोऽरिं सर्वपापघ्नं प्रणतोऽस्मि दिवाकरम्॥", "japākusumasaṅkāśaṃ kāśyapeyaṃ mahādyutim\ntamo'riṃ sarvapāpaghnaṃ praṇato'smi divākaram", "Red as the hibiscus flower, son of the sage Kashyapa, of great brilliance, enemy of darkness and destroyer of all wrong: I bow to the maker of the day."]]
  },
  {
    id: "navagraha", name: "Navagraha Shanti", type: "shloka", deity: "universal",
    moments: ["peace", "morning"], lang: "Sanskrit", author: "Traditional",
    about: "A single verse asking the Trimurti and the nine planetary powers (navagraha) to bring peace.",
    verses: [["ब्रह्मा मुरारिस्त्रिपुरान्तकारी भानुः शशी भूमिसुतो बुधश्च।\nगुरुश्च शुक्रः शनिराहुकेतवः सर्वे ग्रहाः शान्तिकरा भवन्तु॥", "brahmā murāris tripurāntakārī bhānuḥ śaśī bhūmisuto budhaś ca\nguruś ca śukraḥ śanirāhuketavaḥ sarve grahāḥ śāntikarā bhavantu", "May Brahma, Vishnu and Shiva, and the Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu and Ketu: may all the planets bring peace."]]
  },
  {
    id: "tvameva", name: "Tvameva Mata", type: "shloka", deity: "universal",
    moments: ["peace", "evening", "sleep"], lang: "Sanskrit", author: "Traditional (Pandava Gita)",
    about: "A prayer of complete trust, often sung at the end of aarti.",
    verses: [["त्वमेव माता च पिता त्वमेव\nत्वमेव बन्धुश्च सखा त्वमेव।\nत्वमेव विद्या द्रविणं त्वमेव\nत्वमेव सर्वं मम देवदेव॥", "tvam eva mātā ca pitā tvam eva\ntvam eva bandhuś ca sakhā tvam eva\ntvam eva vidyā draviṇaṃ tvam eva\ntvam eva sarvaṃ mama devadeva", "You alone are my mother and my father. You alone are my family and my friend. You alone are my knowledge and my wealth. You are my everything, O God of gods."]]
  },
  {
    id: "sarve-bhavantu", name: "Sarve Bhavantu Sukhinah", type: "shloka", deity: "universal",
    moments: ["peace", "health", "sleep"], lang: "Sanskrit", author: "Traditional, after the Brihadaranyaka Upanishad",
    about: "A prayer for the wellbeing of everyone, without exception.",
    verses: [["सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः।\nसर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्॥\nॐ शान्तिः शान्तिः शान्तिः॥", "sarve bhavantu sukhinaḥ sarve santu nirāmayāḥ\nsarve bhadrāṇi paśyantu mā kaścid duḥkhabhāg bhavet\noṃ śāntiḥ śāntiḥ śāntiḥ", "May all be happy. May all be free from illness. May all see what is good. May no one suffer. Om, peace, peace, peace."]]
  },
  {
    id: "asato-ma", name: "Asato Ma Sadgamaya", type: "shloka", deity: "universal",
    moments: ["peace", "study", "morning"], lang: "Sanskrit", author: "Brihadaranyaka Upanishad 1.3.28",
    about: "The Pavamana mantra, a three-line prayer for the whole spiritual journey.",
    verses: [["असतो मा सद्गमय।\nतमसो मा ज्योतिर्गमय।\nमृत्योर्मा अमृतं गमय।\nॐ शान्तिः शान्तिः शान्तिः॥", "asato mā sad gamaya\ntamaso mā jyotir gamaya\nmṛtyor mā amṛtaṃ gamaya\noṃ śāntiḥ śāntiḥ śāntiḥ", "Lead me from the unreal to the real. Lead me from darkness to light. Lead me from death to immortality. Om, peace, peace, peace."]]
  },
  {
    id: "sahana", name: "Om Saha Navavatu", type: "shloka", deity: "universal",
    moments: ["study", "meal"], lang: "Sanskrit", author: "Taittiriya Upanishad 2.2.2",
    about: "The shanti mantra shared by teacher and student before learning, also widely said before meals.",
    verses: [["ॐ सह नाववतु। सह नौ भुनक्तु।\nसह वीर्यं करवावहै।\nतेजस्वि नावधीतमस्तु मा विद्विषावहै॥\nॐ शान्तिः शान्तिः शान्तिः॥", "oṃ saha nāv avatu, saha nau bhunaktu\nsaha vīryaṃ karavāvahai\ntejasvi nāv adhītam astu mā vidviṣāvahai\noṃ śāntiḥ śāntiḥ śāntiḥ", "Om. May we be protected together; may we be nourished together. May we work together with vigour. May our study be full of light. May we never resent one another. Om, peace, peace, peace."]]
  },
  {
    id: "purnamadah", name: "Purnamadah Purnamidam", type: "shloka", deity: "universal",
    moments: ["peace", "morning"], lang: "Sanskrit", author: "Isha Upanishad, invocation",
    about: "The invocation of the Isha Upanishad, a meditation on the fullness of the infinite.",
    verses: [["ॐ पूर्णमदः पूर्णमिदं पूर्णात्पूर्णमुदच्यते।\nपूर्णस्य पूर्णमादाय पूर्णमेवावशिष्यते॥\nॐ शान्तिः शान्तिः शान्तिः॥", "oṃ pūrṇam adaḥ pūrṇam idaṃ pūrṇāt pūrṇam udacyate\npūrṇasya pūrṇam ādāya pūrṇam evāvaśiṣyate\noṃ śāntiḥ śāntiḥ śāntiḥ", "That is whole; this is whole. From wholeness, wholeness comes forth. Take wholeness from wholeness and wholeness remains. Om, peace, peace, peace."]]
  },
  {
    id: "dyauh-shanti", name: "Dyauh Shantih", type: "shloka", deity: "universal",
    moments: ["peace", "health"], lang: "Sanskrit", author: "Shukla Yajurveda 36.17",
    about: "The great Vedic peace invocation, asking for peace in every part of creation, and then in ourselves.",
    verses: [["ॐ द्यौः शान्तिरन्तरिक्षं शान्तिः पृथिवी शान्तिरापः शान्तिरोषधयः शान्तिः।\nवनस्पतयः शान्तिर्विश्वेदेवाः शान्तिर्ब्रह्म शान्तिः सर्वं शान्तिः शान्तिरेव शान्तिः सा मा शान्तिरेधि॥\nॐ शान्तिः शान्तिः शान्तिः॥", "oṃ dyauḥ śāntir antarikṣaṃ śāntiḥ pṛthivī śāntir āpaḥ śāntir oṣadhayaḥ śāntiḥ\nvanaspatayaḥ śāntir viśvedevāḥ śāntir brahma śāntiḥ sarvaṃ śāntiḥ śāntir eva śāntiḥ sā mā śāntir edhi\noṃ śāntiḥ śāntiḥ śāntiḥ", "May there be peace in the heavens, peace in the sky, peace on earth. May the waters be at peace, the healing herbs and the trees at peace. May all the gods be at peace, may Brahman be peace, may all things be peace, peace itself. May that peace come to me. Om, peace, peace, peace."]]
  },

  /* ================================================================== */
  /* STOTRAS                                                             */
  /* ================================================================== */
  {
    id: "shiva-panchakshara", name: "Shiva Panchakshara Stotram", type: "stotra", deity: "shiva",
    moments: ["morning", "evening", "peace"], lang: "Sanskrit", author: "Attributed to Adi Shankaracharya",
    about: "Five verses, each built on one syllable of “na-maḥ-śi-vā-ya”, followed by a closing blessing.",
    verses: [
      ["नागेन्द्रहाराय त्रिलोचनाय भस्माङ्गरागाय महेश्वराय।\nनित्याय शुद्धाय दिगम्बराय तस्मै नकाराय नमः शिवाय॥", "nāgendrahārāya trilocanāya bhasmāṅgarāgāya maheśvarāya\nnityāya śuddhāya digambarāya tasmai nakārāya namaḥ śivāya", "To the great Lord who wears the king of serpents as a garland, who has three eyes and whose body is smeared with sacred ash; to the eternal, the pure, clothed only in the directions: to that Shiva, the syllable “na”, I bow."],
      ["मन्दाकिनीसलिलचन्दनचर्चिताय नन्दीश्वरप्रमथनाथमहेश्वराय।\nमन्दारपुष्पबहुपुष्पसुपूजिताय तस्मै मकाराय नमः शिवाय॥", "mandākinīsalilacandanacarcitāya nandīśvarapramathanāthamaheśvarāya\nmandārapuṣpabahupuṣpasupūjitāya tasmai makārāya namaḥ śivāya", "To the great Lord anointed with the waters of the Ganga and sandalwood paste, master of Nandi and of all the ganas, worshipped with mandara and countless flowers: to that Shiva, the syllable “ma”, I bow."],
      ["शिवाय गौरीवदनाब्जवृन्दसूर्याय दक्षाध्वरनाशकाय।\nश्रीनीलकण्ठाय वृषध्वजाय तस्मै शिकाराय नमः शिवाय॥", "śivāya gaurīvadanābjavṛndasūryāya dakṣādhvaranāśakāya\nśrīnīlakaṇṭhāya vṛṣadhvajāya tasmai śikārāya namaḥ śivāya", "To the auspicious one, the sun who makes the lotus of Gauri's face bloom, who ended Daksha's sacrifice; to the blue-throated one whose banner bears the bull: to that Shiva, the syllable “shi”, I bow."],
      ["वसिष्ठकुम्भोद्भवगौतमार्यमुनीन्द्रदेवार्चितशेखराय।\nचन्द्रार्कवैश्वानरलोचनाय तस्मै वकाराय नमः शिवाय॥", "vasiṣṭhakumbhodbhavagautamāryamunīndradevārcitaśekharāya\ncandrārkavaiśvānaralocanāya tasmai vakārāya namaḥ śivāya", "To the one whose crown is worshipped by Vasishtha, Agastya, Gautama and the greatest sages and gods, whose three eyes are the moon, the sun and fire: to that Shiva, the syllable “va”, I bow."],
      ["यक्षस्वरूपाय जटाधराय पिनाकहस्ताय सनातनाय।\nदिव्याय देवाय दिगम्बराय तस्मै यकाराय नमः शिवाय॥", "yakṣasvarūpāya jaṭādharāya pinākahastāya sanātanāya\ndivyāya devāya digambarāya tasmai yakārāya namaḥ śivāya", "To the one who appeared as a yaksha, who wears matted locks and holds the bow Pinaka, the eternal one; to the radiant god clothed in the directions: to that Shiva, the syllable “ya”, I bow."],
      ["पञ्चाक्षरमिदं पुण्यं यः पठेच्छिवसन्निधौ।\nशिवलोकमवाप्नोति शिवेन सह मोदते॥", "pañcākṣaram idaṃ puṇyaṃ yaḥ paṭhec chivasannidhau\nśivalokam avāpnoti śivena saha modate", "Whoever recites this sacred five-syllable hymn in Shiva's presence reaches Shiva's realm and rejoices with Shiva.", "Phala shruti"]
    ]
  },
  {
    id: "rudrashtakam", name: "Shri Rudrashtakam", type: "stotra", deity: "shiva",
    moments: ["evening", "peace", "protection"], lang: "Sanskrit", author: "Goswami Tulsidas, Ramcharitmanas (Uttara Kanda)",
    about: "Eight verses in praise of Shiva composed by Tulsidas, sung in Shiva temples every evening and especially on Mondays and Maha Shivaratri.",
    verses: [
      ["नमामीशमीशान निर्वाणरूपं विभुं व्यापकं ब्रह्मवेदस्वरूपम्।\nनिजं निर्गुणं निर्विकल्पं निरीहं चिदाकाशमाकाशवासं भजेऽहम्॥", "namāmīśam īśāna nirvāṇarūpaṃ vibhuṃ vyāpakaṃ brahmavedasvarūpam\nnijaṃ nirguṇaṃ nirvikalpaṃ nirīhaṃ cidākāśam ākāśavāsaṃ bhaje'ham", "I bow to the Lord, the ruler, whose very form is liberation: all-powerful, all-pervading, Brahman, the Veda itself. I worship him who is the Self, beyond qualities, beyond thought, beyond desire, the sky of consciousness, dwelling in all space."],
      ["निराकारमोङ्कारमूलं तुरीयं गिरा ज्ञान गोतीतमीशं गिरीशम्।\nकरालं महाकाल कालं कृपालं गुणागार संसारपारं नतोऽहम्॥", "nirākāram oṅkāramūlaṃ turīyaṃ girā jñāna gotītam īśaṃ girīśam\nkarālaṃ mahākāla kālaṃ kṛpālaṃ guṇāgāra saṃsārapāraṃ nato'ham", "Formless, the root of Om, the fourth state beyond waking, dream and sleep; beyond speech, knowledge and the senses; the Lord of the mountains. Fearsome, the death of Death itself, yet compassionate; the abode of all virtues, beyond the cycle of birth: to him I bow."],
      ["तुषाराद्रिसङ्काशगौरं गभीरं मनोभूतकोटिप्रभाश्रीशरीरम्।\nस्फुरन्मौलिकल्लोलिनी चारुगङ्गा लसद्भालबालेन्दु कण्ठे भुजङ्गा॥", "tuṣārādrisaṅkāśagauraṃ gabhīraṃ manobhūtakoṭiprabhāśrīśarīram\nsphuranmaulikallolinī cārugaṅgā lasadbhālabālendu kaṇṭhe bhujaṅgā", "White as the snowy mountains, profound, his body more radiant than ten million gods of love. The lovely Ganga ripples on his head, the crescent moon shines on his brow, and serpents circle his throat."],
      ["चलत्कुण्डलं भ्रूसुनेत्रं विशालं प्रसन्नाननं नीलकण्ठं दयालम्।\nमृगाधीशचर्माम्बरं मुण्डमालं प्रियं शङ्करं सर्वनाथं भजामि॥", "calatkuṇḍalaṃ bhrūsunetraṃ viśālaṃ prasannānanaṃ nīlakaṇṭhaṃ dayālam\nmṛgādhīśacarmāmbaraṃ muṇḍamālaṃ priyaṃ śaṅkaraṃ sarvanāthaṃ bhajāmi", "Earrings swaying, with fine brows and wide eyes, a gentle face, a blue throat, full of mercy; wearing a lion's skin and a garland of skulls: I worship beloved Shankara, lord of all."],
      ["प्रचण्डं प्रकृष्टं प्रगल्भं परेशं अखण्डं अजं भानुकोटिप्रकाशम्।\nत्रयःशूलनिर्मूलनं शूलपाणिं भजेऽहं भवानीपतिं भावगम्यम्॥", "pracaṇḍaṃ prakṛṣṭaṃ pragalbhaṃ pareśam akhaṇḍam ajaṃ bhānukoṭiprakāśam\ntrayaḥśūlanirmūlanaṃ śūlapāṇiṃ bhaje'haṃ bhavānīpatiṃ bhāvagamyam", "Fierce, supreme, bold, the highest Lord; undivided, unborn, shining like ten million suns; trident in hand, he uproots the three kinds of suffering. I worship the husband of Bhavani, reached through love."],
      ["कलातीत कल्याण कल्पान्तकारी सदा सज्जनानन्ददाता पुरारी।\nचिदानन्दसन्दोह मोहापहारी प्रसीद प्रसीद प्रभो मन्मथारी॥", "kalātīta kalyāṇa kalpāntakārī sadā sajjanānandadātā purārī\ncidānandasandoha mohāpahārī prasīda prasīda prabho manmathārī", "Beyond time, auspicious, bringer of the end of each age, ever the giver of joy to the good, destroyer of the three cities; fullness of consciousness and bliss, remover of delusion: be gracious, be gracious, O Lord, conqueror of desire."],
      ["न यावद् उमानाथपादारविन्दं भजन्तीह लोके परे वा नराणाम्।\nन तावत्सुखं शान्ति सन्तापनाशं प्रसीद प्रभो सर्वभूताधिवासम्॥", "na yāvad umānāthapādāravindaṃ bhajantīha loke pare vā narāṇām\nna tāvat sukhaṃ śānti santāpanāśaṃ prasīda prabho sarvabhūtādhivāsam", "Until people worship the lotus feet of Uma's Lord, they find no happiness or peace, in this world or the next, and their suffering does not end. Be gracious, O Lord, who dwells in all beings."],
      ["न जानामि योगं जपं नैव पूजां नतोऽहं सदा सर्वदा शम्भु तुभ्यम्।\nजराजन्मदुःखौघ तातप्यमानं प्रभो पाहि आपन्नमामीश शम्भो॥", "na jānāmi yogaṃ japaṃ naiva pūjāṃ nato'haṃ sadā sarvadā śambhu tubhyam\njarājanmaduḥkhaugha tātapyamānaṃ prabho pāhi āpannam āmīśa śambho", "I know nothing of yoga, of japa or of worship. I simply bow to you, Shambhu, always and forever. I burn in the flood of sorrows of old age and birth. Protect me in my distress, O Lord, O Shambhu."],
      ["रुद्राष्टकमिदं प्रोक्तं विप्रेण हरतोषये।\nये पठन्ति नरा भक्त्या तेषां शम्भुः प्रसीदति॥", "rudrāṣṭakam idaṃ proktaṃ vipreṇa haratoṣaye\nye paṭhanti narā bhaktyā teṣāṃ śambhuḥ prasīdati", "This hymn of eight verses to Rudra was sung by a brahmin to please Hara. Shambhu is pleased with all who recite it with devotion.", "Phala shruti"]
    ]
  },
  {
    id: "nirvana-shatakam", name: "Nirvana Shatakam", type: "stotra", deity: "shiva",
    moments: ["peace", "morning"], lang: "Sanskrit", author: "Adi Shankaracharya",
    about: "Six verses of pure Advaita said to have been the young Shankara's answer when his guru asked, “Who are you?” Each ends: “I am consciousness and bliss. I am Shiva.”",
    verses: [
      ["मनोबुद्ध्यहङ्कारचित्तानि नाहं न च श्रोत्रजिह्वे न च घ्राणनेत्रे।\nन च व्योमभूमिर्न तेजो न वायुः चिदानन्दरूपः शिवोऽहं शिवोऽहम्॥", "manobuddhyahaṅkāracittāni nāhaṃ na ca śrotrajihve na ca ghrāṇanetre\nna ca vyomabhūmir na tejo na vāyuḥ cidānandarūpaḥ śivo'haṃ śivo'ham", "I am not the mind, intellect, ego or memory. I am not the ears, tongue, nose or eyes. I am not space, earth, fire or air. I am consciousness and bliss. I am Shiva, I am Shiva."],
      ["न च प्राणसंज्ञो न वै पञ्चवायुः न वा सप्तधातुर्न वा पञ्चकोशः।\nन वाक्पाणिपादं न चोपस्थपायू चिदानन्दरूपः शिवोऽहं शिवोऽहम्॥", "na ca prāṇasaṃjño na vai pañcavāyuḥ na vā saptadhātur na vā pañcakośaḥ\nna vākpāṇipādaṃ na copasthapāyū cidānandarūpaḥ śivo'haṃ śivo'ham", "I am not the life-breath nor its five currents, not the seven elements of the body nor its five sheaths. I am not speech, hands, feet or the organs of the body. I am consciousness and bliss. I am Shiva, I am Shiva."],
      ["न मे द्वेषरागौ न मे लोभमोहौ मदो नैव मे नैव मात्सर्यभावः।\nन धर्मो न चार्थो न कामो न मोक्षः चिदानन्दरूपः शिवोऽहं शिवोऽहम्॥", "na me dveṣarāgau na me lobhamohau mado naiva me naiva mātsaryabhāvaḥ\nna dharmo na cārtho na kāmo na mokṣaḥ cidānandarūpaḥ śivo'haṃ śivo'ham", "I have no aversion or attachment, no greed or delusion, no pride and no envy. I am not even duty, wealth, desire or liberation. I am consciousness and bliss. I am Shiva, I am Shiva."],
      ["न पुण्यं न पापं न सौख्यं न दुःखं न मन्त्रो न तीर्थं न वेदा न यज्ञाः।\nअहं भोजनं नैव भोज्यं न भोक्ता चिदानन्दरूपः शिवोऽहं शिवोऽहम्॥", "na puṇyaṃ na pāpaṃ na saukhyaṃ na duḥkhaṃ na mantro na tīrthaṃ na vedā na yajñāḥ\nahaṃ bhojanaṃ naiva bhojyaṃ na bhoktā cidānandarūpaḥ śivo'haṃ śivo'ham", "I am not virtue or sin, pleasure or pain. I am not mantra, pilgrimage, scripture or sacrifice. I am not the eating, the food or the eater. I am consciousness and bliss. I am Shiva, I am Shiva."],
      ["न मे मृत्युशङ्का न मे जातिभेदः पिता नैव मे नैव माता न जन्म।\nन बन्धुर्न मित्रं गुरुर्नैव शिष्यः चिदानन्दरूपः शिवोऽहं शिवोऽहम्॥", "na me mṛtyuśaṅkā na me jātibhedaḥ pitā naiva me naiva mātā na janma\nna bandhur na mitraṃ gurur naiva śiṣyaḥ cidānandarūpaḥ śivo'haṃ śivo'ham", "I have no fear of death and no distinctions of birth. I have no father, no mother, for I was never born. I have no relative or friend, no teacher and no student. I am consciousness and bliss. I am Shiva, I am Shiva."],
      ["अहं निर्विकल्पो निराकाररूपो विभुत्वाच्च सर्वत्र सर्वेन्द्रियाणाम्।\nसदा मे समत्वं न मुक्तिर्न बन्धः चिदानन्दरूपः शिवोऽहं शिवोऽहम्॥", "ahaṃ nirvikalpo nirākārarūpo vibhutvāc ca sarvatra sarvendriyāṇām\nsadā me samatvaṃ na muktir na bandhaḥ cidānandarūpaḥ śivo'haṃ śivo'ham", "I am free of all thought and without form. I pervade everything, everywhere, beyond all the senses. I am always the same; for me there is neither bondage nor liberation. I am consciousness and bliss. I am Shiva, I am Shiva."]
    ]
  },
  {
    id: "madhurashtakam", name: "Madhurashtakam", type: "stotra", deity: "krishna",
    moments: ["morning", "evening", "peace"], lang: "Sanskrit", author: "Shri Vallabhacharya",
    about: "“Eight verses of sweetness”: everything about Krishna, the Lord of Mathura, is sweet. It is sung especially at Janmashtami.",
    verses: [
      ["अधरं मधुरं वदनं मधुरं नयनं मधुरं हसितं मधुरम्।\nहृदयं मधुरं गमनं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "adharaṃ madhuraṃ vadanaṃ madhuraṃ nayanaṃ madhuraṃ hasitaṃ madhuram\nhṛdayaṃ madhuraṃ gamanaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "His lips are sweet, his face is sweet, his eyes are sweet, his smile is sweet. His heart is sweet, his walk is sweet. Everything about the Lord of sweetness is sweet."],
      ["वचनं मधुरं चरितं मधुरं वसनं मधुरं वलितं मधुरम्।\nचलितं मधुरं भ्रमितं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "vacanaṃ madhuraṃ caritaṃ madhuraṃ vasanaṃ madhuraṃ valitaṃ madhuram\ncalitaṃ madhuraṃ bhramitaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "His words are sweet, his deeds are sweet, his clothes are sweet, his posture is sweet. His movements are sweet, his wanderings are sweet. Everything about the Lord of sweetness is sweet."],
      ["वेणुर्मधुरो रेणुर्मधुरः पाणिर्मधुरः पादौ मधुरौ।\nनृत्यं मधुरं सख्यं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "veṇur madhuro reṇur madhuraḥ pāṇir madhuraḥ pādau madhurau\nnṛtyaṃ madhuraṃ sakhyaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "His flute is sweet, the dust of his feet is sweet, his hands are sweet, his feet are sweet. His dance is sweet, his friendship is sweet. Everything about the Lord of sweetness is sweet."],
      ["गीतं मधुरं पीतं मधुरं भुक्तं मधुरं सुप्तं मधुरम्।\nरूपं मधुरं तिलकं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "gītaṃ madhuraṃ pītaṃ madhuraṃ bhuktaṃ madhuraṃ suptaṃ madhuram\nrūpaṃ madhuraṃ tilakaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "His song is sweet, his drinking is sweet, his eating is sweet, his sleeping is sweet. His form is sweet, his tilaka is sweet. Everything about the Lord of sweetness is sweet."],
      ["करणं मधुरं तरणं मधुरं हरणं मधुरं रमणं मधुरम्।\nवमितं मधुरं शमितं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "karaṇaṃ madhuraṃ taraṇaṃ madhuraṃ haraṇaṃ madhuraṃ ramaṇaṃ madhuram\nvamitaṃ madhuraṃ śamitaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "His actions are sweet, his saving grace is sweet, his stealing of hearts is sweet, his play is sweet. His offerings are sweet, his calm is sweet. Everything about the Lord of sweetness is sweet."],
      ["गुञ्जा मधुरा माला मधुरा यमुना मधुरा वीची मधुरा।\nसलिलं मधुरं कमलं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "guñjā madhurā mālā madhurā yamunā madhurā vīcī madhurā\nsalilaṃ madhuraṃ kamalaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "His berry necklace is sweet, his garland is sweet, the Yamuna is sweet, her ripples are sweet. Her water is sweet, her lotuses are sweet. Everything about the Lord of sweetness is sweet."],
      ["गोपी मधुरा लीला मधुरा युक्तं मधुरं मुक्तं मधुरम्।\nदृष्टं मधुरं शिष्टं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "gopī madhurā līlā madhurā yuktaṃ madhuraṃ muktaṃ madhuram\ndṛṣṭaṃ madhuraṃ śiṣṭaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "The gopis are sweet, his play is sweet, being with him is sweet, his freeing is sweet. His glance is sweet, his manners are sweet. Everything about the Lord of sweetness is sweet."],
      ["गोपा मधुरा गावो मधुरा यष्टिर्मधुरा सृष्टिर्मधुरा।\nदलितं मधुरं फलितं मधुरं मधुराधिपतेरखिलं मधुरम्॥", "gopā madhurā gāvo madhurā yaṣṭir madhurā sṛṣṭir madhurā\ndalitaṃ madhuraṃ phalitaṃ madhuraṃ madhurādhipater akhilaṃ madhuram", "The cowherds are sweet, the cows are sweet, his staff is sweet, his creation is sweet. His trampling of evil is sweet, his bearing of fruit is sweet. Everything about the Lord of sweetness is sweet."]
    ]
  },
  {
    id: "bhavani-ashtakam", name: "Bhavani Ashtakam", type: "stotra", deity: "devi",
    moments: ["protection", "peace", "evening"], lang: "Sanskrit", author: "Attributed to Adi Shankaracharya",
    about: "A hymn of total surrender to the Divine Mother. Each verse ends: “You are my refuge, you alone, Bhavani.”",
    verses: [
      ["न तातो न माता न बन्धुर्न दाता न पुत्रो न पुत्री न भृत्यो न भर्ता।\nन जाया न विद्या न वृत्तिर्ममैव गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "na tāto na mātā na bandhur na dātā na putro na putrī na bhṛtyo na bhartā\nna jāyā na vidyā na vṛttir mamaiva gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "Not father nor mother, not relative nor benefactor, not son nor daughter, not servant nor master, not spouse, nor learning, nor livelihood is mine. You are my refuge, my only refuge, you alone, Bhavani."],
      ["भवाब्धावपारे महादुःखभीरुः पपात प्रकामी प्रलोभी प्रमत्तः।\nकुसंसारपाशप्रबद्धः सदाहं गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "bhavābdhāv apāre mahāduḥkhabhīruḥ papāta prakāmī pralobhī pramattaḥ\nkusaṃsārapāśaprabaddhaḥ sadāhaṃ gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "I have fallen into the endless ocean of worldly life, terrified of its great sorrows: full of desire, greed and carelessness, always bound by the snares of the world. You are my refuge, my only refuge, you alone, Bhavani."],
      ["न जानामि दानं न च ध्यानयोगं न जानामि तन्त्रं न च स्तोत्रमन्त्रम्।\nन जानामि पूजां न च न्यासयोगं गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "na jānāmi dānaṃ na ca dhyānayogaṃ na jānāmi tantraṃ na ca stotramantram\nna jānāmi pūjāṃ na ca nyāsayogaṃ gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "I know nothing of charity or meditation, nothing of tantra, hymns or mantras, nothing of worship or the rites of nyasa. You are my refuge, my only refuge, you alone, Bhavani."],
      ["न जानामि पुण्यं न जानामि तीर्थं न जानामि मुक्तिं लयं वा कदाचित्।\nन जानामि भक्तिं व्रतं वापि मातर् गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "na jānāmi puṇyaṃ na jānāmi tīrthaṃ na jānāmi muktiṃ layaṃ vā kadācit\nna jānāmi bhaktiṃ vrataṃ vāpi mātar gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "I know nothing of merit or pilgrimage, nothing of liberation or absorption. I know nothing of devotion or of vows, Mother. You are my refuge, my only refuge, you alone, Bhavani."],
      ["कुकर्मी कुसङ्गी कुबुद्धिः कुदासः कुलाचारहीनः कदाचारलीनः।\nकुदृष्टिः कुवाक्यप्रबन्धः सदाहं गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "kukarmī kusaṅgī kubuddhiḥ kudāsaḥ kulācārahīnaḥ kadācāralīnaḥ\nkudṛṣṭiḥ kuvākyaprabandhaḥ sadāhaṃ gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "I do wrong, keep bad company, think poorly and serve badly. I have abandoned good custom and fallen into bad conduct. My sight and my speech are crooked. You are my refuge, my only refuge, you alone, Bhavani."],
      ["प्रजेशं रमेशं महेशं सुरेशं दिनेशं निशीथेश्वरं वा कदाचित्।\nन जानामि चान्यत् सदाहं शरण्ये गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "prajeśaṃ rameśaṃ maheśaṃ sureśaṃ dineśaṃ niśītheśvaraṃ vā kadācit\nna jānāmi cānyat sadāhaṃ śaraṇye gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "Brahma, Vishnu, Shiva, Indra, the Sun or the Moon: I do not know them, nor anyone else, O refuge of all. You are my refuge, my only refuge, you alone, Bhavani."],
      ["विवादे विषादे प्रमादे प्रवासे जले चानले पर्वते शत्रुमध्ये।\nअरण्ये शरण्ये सदा मां प्रपाहि गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "vivāde viṣāde pramāde pravāse jale cānale parvate śatrumadhye\naraṇye śaraṇye sadā māṃ prapāhi gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "In quarrels and in grief, in error and in foreign lands, in water and in fire, on mountains and among enemies, in the forest: O refuge, always protect me. You are my refuge, my only refuge, you alone, Bhavani."],
      ["अनाथो दरिद्रो जरारोगयुक्तो महाक्षीणदीनः सदा जाड्यवक्त्रः।\nविपत्तौ प्रविष्टः प्रणष्टः सदाहं गतिस्त्वं गतिस्त्वं त्वमेका भवानि॥", "anātho daridro jarārogayukto mahākṣīṇadīnaḥ sadā jāḍyavaktraḥ\nvipattau praviṣṭaḥ praṇaṣṭaḥ sadāhaṃ gatis tvaṃ gatis tvaṃ tvam ekā bhavāni", "I am helpless and poor, worn by age and illness, exhausted and wretched, always dull of speech; I have fallen into misfortune and am lost. You are my refuge, my only refuge, you alone, Bhavani."]
    ]
  },

  /* ================================================================== */
  /* AARTIS                                                              */
  /* ================================================================== */
  {
    id: "jagdish", name: "Om Jai Jagdish Hare", type: "aarti", deity: "vishnu",
    moments: ["evening", "lamp"], lang: "Hindi", author: "Pandit Shardha Ram Phillauri, c. 1870",
    about: "The most widely sung aarti in the world. Many families close every evening's worship with it, whichever deity they have prayed to. The refrain is repeated after each verse.",
    verses: [
      ["ॐ जय जगदीश हरे, स्वामी जय जगदीश हरे।\nभक्त जनों के संकट, दास जनों के संकट, क्षण में दूर करे॥", "Om jai Jagdish Hare, Swami jai Jagdish Hare\nBhakt janon ke sankat, das janon ke sankat, kshan mein door kare", "Om, glory to you, Hari, Lord of the universe! In an instant you take away the troubles of your devotees and servants.", "Refrain"],
      ["जो ध्यावे फल पावे, दुःख बिनसे मन का, स्वामी दुःख बिनसे मन का।\nसुख सम्पत्ति घर आवे, कष्ट मिटे तन का॥", "Jo dhyave phal pave, dukh binse man ka, Swami dukh binse man ka\nSukh sampatti ghar aave, kasht mite tan ka", "Whoever meditates on you is rewarded; the sorrow of their mind melts away. Joy and plenty come to their home, and the pains of the body end."],
      ["मात पिता तुम मेरे, शरण गहूँ मैं किसकी, स्वामी शरण गहूँ मैं किसकी।\nतुम बिन और न दूजा, आस करूँ मैं जिसकी॥", "Maat pita tum mere, sharan gahoon main kiski, Swami sharan gahoon main kiski\nTum bin aur na dooja, aas karoon main jiski", "You are my mother and my father. With whom else should I take shelter? There is no one but you in whom I can place my hope."],
      ["तुम पूरण परमात्मा, तुम अन्तर्यामी, स्वामी तुम अन्तर्यामी।\nपारब्रह्म परमेश्वर, तुम सब के स्वामी॥", "Tum pooran Paramatma, tum Antaryami, Swami tum Antaryami\nParabrahm Parameshwar, tum sab ke Swami", "You are the complete Supreme Spirit, the one who knows every heart from within. You are the transcendent Brahman, the supreme Lord, the master of all."],
      ["तुम करुणा के सागर, तुम पालनकर्ता, स्वामी तुम पालनकर्ता।\nमैं मूरख फलगामी, मैं सेवक तुम स्वामी, कृपा करो भर्ता॥", "Tum karuna ke sagar, tum palankarta, Swami tum palankarta\nMain moorakh phalgami, main sevak tum Swami, kripa karo bharta", "You are an ocean of compassion, the one who sustains all things. I am foolish and always chasing rewards. I am your servant and you are my master: have mercy on me, my protector."],
      ["तुम हो एक अगोचर, सबके प्राणपति, स्वामी सबके प्राणपति।\nकिस विधि मिलूँ दयामय, तुमको मैं कुमति॥", "Tum ho ek agochar, sabke pranpati, Swami sabke pranpati\nKis vidhi miloon dayamay, tumko main kumati", "You are the One, beyond the reach of the senses, the lord of every living breath. How can someone as unwise as I am come to meet you, O merciful one?"],
      ["दीनबन्धु दुःखहर्ता, ठाकुर तुम मेरे, स्वामी रक्षक तुम मेरे।\nअपने हाथ उठाओ, अपनी शरण लगाओ, द्वार पड़ा तेरे॥", "Deenbandhu dukhharta, Thakur tum mere, Swami rakshak tum mere\nApne haath uthao, apni sharan lagao, dwar pada tere", "Friend of the helpless, remover of sorrow, you are my Lord and my protector. Raise your hand in blessing and take me into your shelter: I lie at your door."],
      ["विषय विकार मिटाओ, पाप हरो देवा, स्वामी पाप हरो देवा।\nश्रद्धा भक्ति बढ़ाओ, सन्तन की सेवा॥", "Vishay vikar mitao, paap haro Deva, Swami paap haro Deva\nShraddha bhakti badhao, santan ki seva", "Wipe away my cravings and faults; take away my wrongdoing, O God. Increase my faith and devotion, and my service to the saintly."],
      ["तन मन धन सब कुछ है तेरा, स्वामी सब कुछ है तेरा।\nतेरा तुझको अर्पण, क्या लागे मेरा॥", "Tan man dhan sab kuchh hai tera, Swami sab kuchh hai tera\nTera tujhko arpan, kya laage mera", "Body, mind and wealth: everything is yours, Lord. I offer you what is already yours. What is there that is mine?"]
    ]
  },
  {
    id: "ganesh-aarti", name: "Jai Ganesh Deva", type: "aarti", deity: "ganesha",
    moments: ["evening", "work", "lamp"], lang: "Hindi", author: "Traditional; signed “Sur Shyam”",
    about: "Ganesha's aarti, sung first in any aarti sequence because he is worshipped before every other deity. It is the heart of Ganesh Chaturthi.",
    verses: [
      ["जय गणेश जय गणेश, जय गणेश देवा।\nमाता जाकी पार्वती, पिता महादेवा॥", "Jai Ganesh jai Ganesh, jai Ganesh Deva\nMata jaki Parvati, pita Mahadeva", "Glory to Ganesha, glory to Lord Ganesha, whose mother is Parvati and whose father is the great god Shiva.", "Refrain"],
      ["एक दन्त दयावन्त, चार भुजा धारी।\nमाथे सिन्दूर सोहे, मूसे की सवारी॥", "Ek dant dayavant, char bhuja dhari\nMathe sindoor sohe, moose ki savari", "He has a single tusk and a kind heart, and four arms. Vermilion shines on his forehead, and he rides upon a mouse."],
      ["पान चढ़े फूल चढ़े, और चढ़े मेवा।\nलड्डुअन का भोग लगे, सन्त करें सेवा॥", "Paan chadhe phool chadhe, aur chadhe meva\nLadduan ka bhog lage, sant karen seva", "Betel leaves, flowers and dried fruit are offered to him. Laddus are given as his food, and the saints serve him."],
      ["अंधन को आँख देत, कोढ़िन को काया।\nबाँझन को पुत्र देत, निर्धन को माया॥", "Andhan ko aankh det, kodhin ko kaya\nBaanjhan ko putra det, nirdhan ko maya", "He gives sight to the blind and healing to the sick. He gives children to the childless and wealth to the poor."],
      ["‘सूर’ श्याम शरण आए, सफल कीजे सेवा।\nमाता जाकी पार्वती, पिता महादेवा॥", "‘Sur’ Shyam sharan aaye, safal keeje seva\nMata jaki Parvati, pita Mahadeva", "The poet Sur Shyam has come to you for refuge: make his service fruitful, O son of Parvati and the great god Shiva."]
    ]
  },
  {
    id: "shiv-aarti", name: "Om Jai Shiv Omkara", type: "aarti", deity: "shiva",
    moments: ["evening", "lamp"], lang: "Hindi", author: "Traditional; signed “Shivanand Swami”",
    about: "Shiva's aarti, sung on Mondays, Pradosh and Maha Shivaratri. It celebrates Shiva as one with Brahma and Vishnu, all three held within the sound of Om.",
    verses: [
      ["ॐ जय शिव ओंकारा, स्वामी जय शिव ओंकारा।\nब्रह्मा विष्णु सदाशिव, अर्द्धांगी धारा॥", "Om jai Shiv Omkara, Swami jai Shiv Omkara\nBrahma Vishnu Sadashiv, ardhangi dhara", "Om, glory to Shiva, who is the sacred sound Om! Brahma, Vishnu and Sadashiva are one, and he holds the Goddess as half of his own body.", "Refrain"],
      ["एकानन चतुरानन पंचानन राजे।\nहंसासन गरुड़ासन वृषवाहन साजे॥", "Ekanan chaturanan panchanan raje\nHansasan garudasan vrishvahan saje", "He shines with one face as Vishnu, four as Brahma and five as Shiva, seated on the swan, on Garuda and on the bull."],
      ["दो भुज चार चतुर्भुज दसभुज अति सोहे।\nत्रिगुण रूप निरखते त्रिभुवन जन मोहे॥", "Do bhuj char chaturbhuj dasbhuj ati sohe\nTrigun roop nirakhte tribhuvan jan mohe", "With two arms, with four, with ten, he is beautiful. All who see his form of the three qualities in the three worlds are enchanted."],
      ["अक्षमाला वनमाला मुण्डमाला धारी।\nचन्दन मृगमद सोहै भाले शशिधारी॥", "Akshamala vanamala mundamala dhari\nChandan mrigmad sohai bhale shashidhari", "He wears a rosary of rudraksha, a garland of forest flowers and a garland of skulls. Sandalwood and musk adorn him, and the moon rests on his brow."],
      ["श्वेताम्बर पीताम्बर बाघम्बर अंगे।\nसनकादिक गरुड़ादिक भूतादिक संगे॥", "Shvetambar pitambar baghambar ange\nSanakadik garudadik bhootadik sange", "He is clothed in white, in yellow and in tiger skin, surrounded by the sages led by Sanaka, by Garuda and the celestials, and by his hosts of spirits."],
      ["कर के मध्य कमण्डलु चक्र त्रिशूलधर्ता।\nजगकर्ता जगभर्ता जगसंहारकर्ता॥", "Kar ke madhya kamandalu chakra trishooldharta\nJagkarta jagbharta jagsanharkarta", "In his hands are the water pot, the discus and the trident. He creates the world, sustains the world and dissolves the world."],
      ["ब्रह्मा विष्णु सदाशिव जानत अविवेका।\nप्रणवाक्षर के मध्ये ये तीनों एका॥", "Brahma Vishnu Sadashiv janat aviveka\nPranavakshar ke madhye ye teenon eka", "The unwise think Brahma, Vishnu and Sadashiva are separate, but within the syllable Om the three are one."],
      ["त्रिगुणस्वामी जी की आरती जो कोई नर गावे।\nकहत शिवानन्द स्वामी मनवांछित फल पावे॥", "Trigunswami ji ki aarti jo koi nar gave\nKahat Shivanand Swami manvanchhit phal pave", "Whoever sings this aarti of the Lord of the three qualities, says Shivanand Swami, receives the fruit their heart desires."]
    ]
  },
  {
    id: "kunj-bihari", name: "Aarti Kunj Bihari Ki", type: "aarti", deity: "krishna",
    moments: ["evening", "lamp"], lang: "Braj Bhasha", author: "Traditional",
    about: "Krishna's evening aarti from Braj, picturing him in the groves of Vrindavan with Radha, his flute and his peacock crown. It is sung at Janmashtami and in every Krishna temple.",
    verses: [
      ["आरती कुंजबिहारी की, श्री गिरिधर कृष्णमुरारी की॥", "Aarti Kunj Bihari ki, Shri Giridhar Krishna Murari ki", "Aarti to the one who wanders the groves of Vrindavan, to glorious Krishna Murari, who lifted the mountain.", "Refrain"],
      ["गले में बैजंती माला, बजावै मुरली मधुर बाला।\nश्रवण में कुण्डल झलकाला, नंद के आनंद नंदलाला।\nगगन सम अंग कांति काली, राधिका चमक रही आली।\nलतन में ठाढ़े बनमाली; भ्रमर सी अलक, कस्तूरी तिलक,\nचंद्र सी झलक; ललित छवि श्यामा प्यारी की॥", "Gale mein baijanti mala, bajavai murali madhur bala\nShravan mein kundal jhalkala, Nand ke anand Nandlala\nGagan sam ang kanti kali, Radhika chamak rahi aali\nLatan mein thadhe Banmali; bhramar si alak, kasturi tilak,\nChandra si jhalak; lalit chhavi Shyama pyari ki", "A garland of vaijayanti flowers at his throat, the young boy plays his sweet flute. Earrings glitter in his ears: he is Nanda's joy, Nanda's darling. His body is dark as the sky, and beside him Radha shines. The forest-garlanded one stands among the vines, his curls like black bees, a musk tilaka on his brow, his face like the moon: the lovely beauty of Shyama's beloved."],
      ["कनकमय मोर मुकुट बिलसै, देवता दरसन को तरसैं।\nगगन सों सुमन रासि बरसै;\nबजे मुरचंग, मधुर मिरदंग, ग्वालिन संग;\nअतुल रति गोप कुमारी की॥", "Kanakmay mor mukut bilsai, devta darsan ko tarsain\nGagan son suman raasi barsai;\nBaje murchang, madhur mirdang, gwalin sang;\nAtul rati gop kumari ki", "His golden peacock crown gleams, and the gods long for a glimpse of him. Flowers shower down from the sky. The jaw harp and the sweet mridanga play as he dances with the cowherd girls, whose love for him is beyond compare."],
      ["जहां ते प्रकट भई गंगा, कलुष कलि हारिणि श्रीगंगा।\nस्मरन ते होत मोह भंगा;\nबसी शिव सीस, जटा के बीच, हरै अघ कीच;\nचरन छवि श्रीबनवारी की॥", "Jahan te prakat bhai Ganga, kalush kali harini Shri Ganga\nSmaran te hot moh bhanga;\nBasi Shiv sees, jata ke beech, harai agh keech;\nCharan chhavi Shri Banwari ki", "From his feet flowed the Ganga, the holy river that washes away the stains of this age; to remember her is to break free of delusion. She lives on Shiva's head among his matted locks and cleanses the mire of sin. Such is the glory of the feet of Krishna of the forest."],
      ["चमकती उज्ज्वल तट रेनू, बज रही वृंदावन बेनू।\nचहुं दिसि गोपि ग्वाल धेनू;\nहंसत मृदु मंद, चांदनी चंद, कटत भव फंद;\nटेर सुन दीन दुखारी की॥", "Chamakti ujjwal tat renu, baj rahi Vrindavan benu\nChahun disi gopi gwal dhenu;\nHansat mridu mand, chandni chand, katat bhav phand;\nTer sun deen dukhari ki", "The sand of the riverbank sparkles bright, and the flute is playing in Vrindavan, with gopis, cowherds and cows on every side. He smiles softly under the moonlight, and the snares of worldly life are cut. Hear the cry of this poor, suffering soul."]
    ]
  },
  {
    id: "ambe-aarti", name: "Jai Ambe Gauri", type: "aarti", deity: "devi",
    moments: ["evening", "lamp"], lang: "Hindi", author: "Traditional; signed “Shivanand Swami”",
    about: "The aarti of Durga, the Divine Mother, sung every evening during Navaratri and on Fridays.",
    verses: [
      ["जय अम्बे गौरी, मैया जय श्यामा गौरी।\nतुमको निशदिन ध्यावत, हरि ब्रह्मा शिवरी॥", "Jai Ambe Gauri, Maiya jai Shyama Gauri\nTumko nishdin dhyavat, Hari Brahma Shivri", "Glory to Mother Ambe, the fair one; glory, Mother, the dark and the fair. Vishnu, Brahma and Shiva meditate on you day and night.", "Refrain"],
      ["माँग सिन्दूर विराजत, टीको मृगमद को।\nउज्ज्वल से दोउ नैना, चन्द्रवदन नीको॥", "Maang sindoor virajat, tiko mrigmad ko\nUjjwal se dou naina, chandravadan neeko", "Vermilion shines in the parting of your hair, with a mark of musk on your brow. Your two eyes are radiant, and your face is lovely as the moon."],
      ["कनक समान कलेवर, रक्ताम्बर राजै।\nरक्तपुष्प गल माला, कण्ठन पर साजै॥", "Kanak saman kalevar, raktambar rajai\nRaktapushp gal mala, kanthan par sajai", "Your body glows like gold, clothed in red. A garland of red flowers adorns your neck."],
      ["केहरि वाहन राजत, खड्ग खप्पर धारी।\nसुर नर मुनि जन सेवत, तिनके दुखहारी॥", "Kehari vahan rajat, khadag khappar dhari\nSur nar muni jan sevat, tinke dukhhari", "You ride in splendour on a lion, bearing sword and bowl. Gods, people and sages serve you, and you take away their sorrows."],
      ["कानन कुण्डल शोभित, नासाग्रे मोती।\nकोटिक चन्द्र दिवाकर, सम राजत ज्योती॥", "Kanan kundal shobhit, nasagre moti\nKotik chandra divakar, sam rajat jyoti", "Earrings adorn your ears and a pearl shines at your nose. Your radiance is like ten million moons and suns."],
      ["शुम्भ निशुम्भ बिदारे, महिषासुर घाती।\nधूम्र विलोचन नैना, निशदिन मदमाती॥", "Shumbh Nishumbh bidare, Mahishasur ghati\nDhoomra vilochan naina, nishdin madmati", "You tore apart Shumbha and Nishumbha and slew Mahishasura. Your eyes, which destroyed Dhumralochana, are ever bright with divine intoxication."],
      ["चण्ड मुण्ड संहारे, शोणित बीज हरे।\nमधु कैटभ दोउ मारे, सुर भयहीन करे॥", "Chand Mund sanhare, Shonit Beej hare\nMadhu Kaitabh dou maare, sur bhayheen kare", "You destroyed Chanda and Munda and ended Raktabija. You slew Madhu and Kaitabha and freed the gods from fear."],
      ["ब्रह्माणी रुद्राणी, तुम कमला रानी।\nआगम निगम बखानी, तुम शिव पटरानी॥", "Brahmani Rudrani, tum Kamala Rani\nAagam nigam bakhani, tum Shiv patrani", "You are Brahmani and Rudrani, and you are Queen Lakshmi. The scriptures sing of you, the chief queen of Shiva."],
      ["चौंसठ योगिनी मंगल गावत, नृत्य करत भैरों।\nबाजत ताल मृदंगा, अरु बाजत डमरू॥", "Chaunsath yogini mangal gavat, nritya karat Bhairon\nBajat taal mridanga, aru bajat damru", "The sixty-four yoginis sing your praises and Bhairava dances, while cymbals, drums and the damaru resound."],
      ["तुम ही जग की माता, तुम ही हो भरता।\nभक्तन की दुख हरता, सुख सम्पति करता॥", "Tum hi jag ki mata, tum hi ho bharta\nBhaktan ki dukh harta, sukh sampati karta", "You alone are the mother of the world and its sustainer. You remove your devotees' sorrows and bring them joy and plenty."],
      ["भुजा चार अति शोभित, वरमुद्रा धारी।\nमनवांछित फल पावत, सेवत नर नारी॥", "Bhuja char ati shobhit, varmudra dhari\nManvanchhit phal pavat, sevat nar nari", "Your four arms are beautiful, one raised in blessing. The men and women who serve you receive what their hearts desire."],
      ["कंचन थाल विराजत, अगर कपूर बाती।\nश्रीमालकेतु में राजत, कोटि रतन ज्योती॥", "Kanchan thaal virajat, agar kapoor baati\nShri Malketu mein rajat, koti ratan jyoti", "On the golden tray are incense, camphor and wicks. In the shrine the light of ten million jewels shines."],
      ["श्री अम्बेजी की आरती, जो कोई नर गावे।\nकहत शिवानन्द स्वामी, सुख सम्पत्ति पावे॥", "Shri Ambeji ki aarti, jo koi nar gave\nKahat Shivanand Swami, sukh sampatti pave", "Whoever sings this aarti of Mother Ambe, says Shivanand Swami, finds happiness and prosperity."]
    ]
  },
  {
    id: "lakshmi-aarti", name: "Om Jai Lakshmi Mata", type: "aarti", deity: "lakshmi",
    moments: ["evening", "lamp"], lang: "Hindi", author: "Traditional",
    about: "Lakshmi's aarti, the centre of Diwali night's Lakshmi Puja and sung on Fridays throughout the year.",
    verses: [
      ["ॐ जय लक्ष्मी माता, मैया जय लक्ष्मी माता।\nतुमको निशदिन सेवत, हर विष्णु विधाता॥", "Om jai Lakshmi Mata, Maiya jai Lakshmi Mata\nTumko nishdin sevat, Har Vishnu Vidhata", "Om, glory to Mother Lakshmi! Shiva, Vishnu and Brahma serve you day and night.", "Refrain"],
      ["उमा रमा ब्रह्माणी, तुम ही जग माता।\nसूर्य चन्द्रमा ध्यावत, नारद ऋषि गाता॥", "Uma Rama Brahmani, tum hi jag mata\nSurya chandrama dhyavat, Narad rishi gata", "You are Uma, Rama and Brahmani, the mother of the world. The sun and moon meditate on you, and the sage Narada sings your praise."],
      ["दुर्गा रूप निरंजनि, सुख सम्पत्ति दाता।\nजो कोई तुमको ध्यावत, ऋद्धि सिद्धि धन पाता॥", "Durga roop niranjani, sukh sampatti data\nJo koi tumko dhyavat, riddhi siddhi dhan pata", "Spotless one in the form of Durga, giver of happiness and plenty: whoever meditates on you gains prosperity, accomplishment and wealth."],
      ["तुम पाताल निवासिनि, तुम ही शुभदाता।\nकर्म प्रभाव प्रकाशिनि, भवनिधि की त्राता॥", "Tum patal nivasini, tum hi shubhdata\nKarma prabhav prakashini, bhavnidhi ki trata", "You dwell even in the netherworlds and you alone bestow good fortune. You reveal the workings of karma and carry us across the ocean of existence."],
      ["जिस घर में तुम रहतीं, सब सद्गुण आता।\nसब सम्भव हो जाता, मन नहीं घबराता॥", "Jis ghar mein tum rahtin, sab sadgun aata\nSab sambhav ho jata, man nahin ghabrata", "Every virtue comes to the home where you live. Everything becomes possible, and the mind is never anxious."],
      ["तुम बिन यज्ञ न होते, वस्त्र न कोई पाता।\nखान पान का वैभव, सब तुमसे आता॥", "Tum bin yagya na hote, vastra na koi pata\nKhan paan ka vaibhav, sab tumse aata", "Without you no sacred rite could be performed and no one would have clothing. All the richness of food and drink comes from you."],
      ["शुभ गुण मन्दिर सुन्दर, क्षीरोदधि जाता।\nरत्न चतुर्दश तुम बिन, कोई नहीं पाता॥", "Shubh gun mandir sundar, kshirodadhi jata\nRatna chaturdash tum bin, koi nahin pata", "Beautiful temple of all good qualities, born of the ocean of milk: without you no one could obtain its fourteen jewels."],
      ["महालक्ष्मी जी की आरती, जो कोई जन गाता।\nउर आनन्द समाता, पाप उतर जाता॥", "Mahalakshmi ji ki aarti, jo koi jan gata\nUr anand samata, paap utar jata", "Whoever sings this aarti of the great Lakshmi is filled with joy, and their wrongdoing falls away."]
    ]
  },
  {
    id: "saraswati-aarti", name: "Om Jai Saraswati Mata", type: "aarti", deity: "saraswati",
    moments: ["evening", "study", "lamp"], lang: "Hindi", author: "Traditional",
    about: "Saraswati's aarti, sung at Vasant Panchami, in schools and before music and dance performances.",
    verses: [
      ["ॐ जय सरस्वती माता, मैया जय सरस्वती माता।\nसद्गुण वैभव शालिनी, त्रिभुवन विख्याता॥", "Om jai Saraswati Mata, Maiya jai Saraswati Mata\nSadgun vaibhav shalini, tribhuvan vikhyata", "Om, glory to Mother Saraswati, rich in every virtue and renowned in the three worlds.", "Refrain"],
      ["चन्द्रवदनि पद्मासिनि, द्युति मंगलकारी।\nसोहे शुभ हंस सवारी, अतुल तेजधारी॥", "Chandravadani padmasini, dyuti mangalkari\nSohe shubh hans savari, atul tejdhari", "Moon-faced, seated on a lotus, your radiance brings blessings. You ride the graceful swan, shining with incomparable light."],
      ["बाएँ कर में वीणा, दाएँ कर माला।\nशीश मुकुट मणि सोहे, गल मोतियन माला॥", "Baayen kar mein veena, daayen kar mala\nSheesh mukut mani sohe, gal motiyan mala", "The veena is in your left hand and a rosary in your right. A jewelled crown adorns your head and a string of pearls your neck."],
      ["देवी शरण जो आए, उनका उद्धार किया।\nपैठी मंथरा दासी, रावण संहार किया॥", "Devi sharan jo aaye, unka uddhar kiya\nPaithi Manthara dasi, Ravan sanhar kiya", "Goddess, you uplift all who come to you for shelter. You entered the mind of the maid Manthara, setting in motion the events that ended Ravana."],
      ["विद्या ज्ञान प्रदायिनि, ज्ञान प्रकाश भरो।\nमोह अज्ञान और तिमिर का, जग से नाश करो॥", "Vidya gyan pradayini, gyan prakash bharo\nMoh agyan aur timir ka, jag se naash karo", "Giver of learning and wisdom, fill us with the light of knowledge. Destroy delusion, ignorance and darkness from the world."],
      ["धूप दीप फल मेवा, माँ स्वीकार करो।\nज्ञानचक्षु दे माता, जग निस्तार करो॥", "Dhoop deep phal meva, Maa sweekar karo\nGyanchakshu de Mata, jag nistar karo", "Accept this incense, lamp, fruit and sweets, Mother. Grant us the eye of wisdom and carry the world across."],
      ["माँ सरस्वती की आरती, जो कोई जन गावे।\nहितकारी सुखकारी, ज्ञान भक्ति पावे॥", "Maa Saraswati ki aarti, jo koi jan gave\nHitkari sukhkari, gyan bhakti pave", "Whoever sings this aarti of Mother Saraswati gains wellbeing, happiness, wisdom and devotion."]
    ]
  },
  {
    id: "hanuman-aarti", name: "Aarti Keeje Hanuman Lala Ki", type: "aarti", deity: "hanuman",
    moments: ["evening", "lamp", "protection"], lang: "Awadhi", author: "Traditional",
    about: "Hanuman's aarti, sung after the Hanuman Chalisa, especially on Tuesdays and Saturdays. It retells his great deeds in the Ramayana.",
    verses: [
      ["आरती कीजै हनुमान लला की।\nदुष्ट दलन रघुनाथ कला की॥", "Aarti keejai Hanuman Lala ki\nDusht dalan Raghunath kala ki", "Offer the aarti to beloved Hanuman, destroyer of the wicked, a ray of Rama's own power.", "Refrain"],
      ["जाके बल से गिरिवर काँपे।\nरोग दोष जाके निकट न झाँके॥", "Jaake bal se girivar kaanpe\nRog dosh jaake nikat na jhaanke", "At his strength the mountains tremble; illness and misfortune dare not come near him."],
      ["अंजनि पुत्र महा बलदायी।\nसन्तन के प्रभु सदा सहाई॥", "Anjani putra maha baldayi\nSantan ke prabhu sada sahai", "Son of Anjana, giver of great strength, he is the ever-present helper of the saints."],
      ["दे बीरा रघुनाथ पठाए।\nलंका जारि सिया सुधि लाए॥", "De beera Raghunath pathaye\nLanka jaari Siya sudhi laye", "Rama gave him the betel leaf of command and sent him forth. He burned Lanka and brought back news of Sita."],
      ["लंका सो कोट समुद्र सी खाई।\nजात पवनसुत बार न लाई॥", "Lanka so kot samudra si khaai\nJaat Pavansut baar na laai", "Lanka was a fortress with the ocean for its moat, yet the son of the wind crossed it without a moment's delay."],
      ["लंका जारि असुर संहारे।\nसियारामजी के काज सँवारे॥", "Lanka jaari asur sanhare\nSiyaramji ke kaaj sanvare", "He set Lanka ablaze and destroyed the demons, accomplishing the work of Sita and Rama."],
      ["लक्ष्मण मूर्छित पड़े सकारे।\nआनि संजीवन प्राण उबारे॥", "Lakshman moorchhit pade sakare\nAani sanjeevan praan ubaare", "When Lakshmana lay unconscious on the battlefield, he brought the sanjeevani herb and saved his life."],
      ["पैठि पाताल तोरि जम कारे।\nअहिरावण की भुजा उखारे॥", "Paithi patal tori jam kaare\nAhiravan ki bhuja ukhaare", "He entered the underworld, broke through its deadly guards and tore away the arms of Ahiravana."],
      ["बाएँ भुजा असुर दल मारे।\nदाहिने भुजा सन्तजन तारे॥", "Baayen bhuja asur dal maare\nDahine bhuja santjan taare", "With his left arm he strikes down the demon hosts; with his right he carries the good to safety."],
      ["सुर नर मुनि आरती उतारें।\nजय जय जय हनुमान उचारें॥", "Sur nar muni aarti utaren\nJai jai jai Hanuman uchaaren", "Gods, people and sages wave the lamp before him, calling “Glory, glory, glory to Hanuman!”"],
      ["कंचन थार कपूर लौ छाई।\nआरती करत अंजना माई॥", "Kanchan thaar kapoor lau chhaai\nAarti karat Anjana maai", "The camphor flame glows on a golden tray as Mother Anjana herself performs his aarti."],
      ["जो हनुमानजी की आरती गावे।\nबसि बैकुण्ठ परमपद पावे॥", "Jo Hanumanji ki aarti gave\nBasi Baikunth parampad pave", "Whoever sings Hanuman's aarti dwells in Vaikuntha and attains the highest state."]
    ]
  },
  {
    id: "sukhkarta", name: "Sukhkarta Dukhharta", type: "aarti", deity: "ganesha",
    moments: ["evening", "lamp", "work"], lang: "Marathi", author: "Samarth Ramdas, 17th century",
    about: "The Marathi aarti to Ganesha composed by Samarth Ramdas after visiting the Ashtavinayaka temple at Morgaon. It is sung across Maharashtra during Ganeshotsav.",
    verses: [
      ["सुखकर्ता दुःखहर्ता वार्ता विघ्नाची।\nनुरवी पुरवी प्रेम कृपा जयाची।\nसर्वांगी सुंदर उटी शेंदुराची।\nकंठी झळके माळ मुक्ताफळांची॥", "Sukhkarta dukhharta varta vighnachi\nNurvi purvi prem kripa jayachi\nSarvangi sundar uti shendurachi\nKanthi jhalke maal muktaphalanchi", "He brings joy and takes away sorrow, and removes every trace of obstacles. His love and grace are everywhere. His whole body is beautiful, anointed with vermilion paste, and a necklace of pearls shines at his throat."],
      ["जय देव जय देव जय मंगलमूर्ती।\nदर्शनमात्रे मनकामना पुरती॥", "Jai Dev jai Dev jai Mangalmurti\nDarshanmatre mankamana purti", "Glory to the Lord, glory, glory to the embodiment of auspiciousness! The mere sight of him fulfils the heart's wishes.", "Refrain"],
      ["रत्नखचित फरा तुज गौरीकुमरा।\nचंदनाची उटी कुंकुमकेशरा।\nहिरेजडित मुकुट शोभतो बरा।\nरुणझुणती नूपुरे चरणी घागरिया॥", "Ratnakhachit phara tuj Gaurikumara\nChandanachi uti kumkumkeshara\nHirejadit mukut shobhato bara\nRunjhunati noopure charani ghagariya", "O son of Gauri, a jewelled seat is set for you, with sandalwood paste, kumkum and saffron. Your diamond-studded crown looks splendid, and the anklets on your feet jingle sweetly."],
      ["लंबोदर पीतांबर फणिवरबंधना।\nसरळ सोंड वक्रतुंड त्रिनयना।\nदास रामाचा वाट पाहे सदना।\nसंकटी पावावे निर्वाणी रक्षावे सुरवरवंदना॥", "Lambodar pitambar phanivarbandhana\nSaral sond vakratund trinayana\nDas Ramacha vaat paahe sadana\nSankati pavave nirvani rakshave survarvandana", "Big-bellied, dressed in yellow, with a serpent for a belt; with a straight trunk and a curved one, and three eyes: Ramdas, your servant, waits for you at home. Come to us in times of trouble and protect us at the very end, O one worshipped by the greatest gods."]
    ]
  },

  /* ================================================================== */
  /* CHALISAS                                                            */
  /* ================================================================== */
  {
    id: "hanuman-chalisa", name: "Shri Hanuman Chalisa", type: "chalisa", deity: "hanuman",
    moments: ["protection", "morning", "evening", "health"], lang: "Awadhi", author: "Goswami Tulsidas, 16th century",
    about: "Forty verses in praise of Hanuman by the poet-saint Tulsidas. It is perhaps the most recited Hindu prayer of all, read daily by millions and especially on Tuesdays and Saturdays for courage and protection.",
    verses: [
      ["श्रीगुरु चरन सरोज रज, निज मनु मुकुरु सुधारि।\nबरनउँ रघुबर बिमल जसु, जो दायकु फल चारि॥", "Shri Guru charan saroj raj, nij man mukur sudhari\nBaranaun Raghubar bimal jasu, jo dayak phal chari", "With the dust of my Guru's lotus feet I polish the mirror of my mind. Then I sing the pure glory of Rama, best of the Raghus, which grants the four fruits of life.", "Doha"],
      ["बुद्धिहीन तनु जानिके, सुमिरौं पवन-कुमार।\nबल बुधि बिद्या देहु मोहिं, हरहु कलेस बिकार॥", "Buddhiheen tanu janike, sumiraun Pavan Kumar\nBal buddhi vidya dehu mohin, harahu kalesh vikar", "Knowing myself to be lacking in wisdom, I remember you, son of the Wind. Give me strength, intelligence and knowledge, and take away my troubles and faults.", "Doha"],
      ["जय हनुमान ज्ञान गुन सागर।\nजय कपीस तिहुँ लोक उजागर॥", "Jai Hanuman gyan gun sagar\nJai Kapees tihun lok ujagar", "Victory to Hanuman, ocean of wisdom and virtue! Victory to the lord of the vanaras, who lights up the three worlds."],
      ["राम दूत अतुलित बल धामा।\nअंजनि-पुत्र पवनसुत नामा॥", "Ram doot atulit bal dhama\nAnjani putra Pavansut nama", "You are Rama's messenger, home of matchless strength, known as Anjana's son and the son of the Wind."],
      ["महाबीर बिक्रम बजरंगी।\nकुमति निवार सुमति के संगी॥", "Mahabir bikram Bajrangi\nKumati nivar sumati ke sangi", "Great hero, mighty one with a body like a thunderbolt, you drive away bad thoughts and keep company with good ones."],
      ["कंचन बरन बिराज सुबेसा।\nकानन कुंडल कुंचित केसा॥", "Kanchan baran biraj subesa\nKanan kundal kunchit kesa", "Your skin shines like gold and you are finely dressed, with earrings in your ears and curling hair."],
      ["हाथ बज्र औ ध्वजा बिराजै।\nकाँधे मूँज जनेऊ साजै॥", "Haath bajra au dhvaja birajai\nKaandhe moonj janeu sajai", "In your hands are the thunderbolt and the banner, and the sacred thread of munja grass rests on your shoulder."],
      ["संकर सुवन केसरीनंदन।\nतेज प्रताप महा जग बंदन॥", "Sankar suvan Kesari nandan\nTej pratap maha jag bandan", "Born of Shiva and the delight of Kesari, your radiance and glory are honoured by the whole world."],
      ["बिद्यावान गुनी अति चातुर।\nराम काज करिबे को आतुर॥", "Vidyavaan guni ati chatur\nRam kaaj karibe ko aatur", "Learned, virtuous and wise, you are always eager to do Rama's work."],
      ["प्रभु चरित्र सुनिबे को रसिया।\nराम लखन सीता मन बसिया॥", "Prabhu charitra sunibe ko rasiya\nRam Lakhan Sita man basiya", "You delight in hearing the story of the Lord, and Rama, Lakshmana and Sita live in your heart."],
      ["सूक्ष्म रूप धरि सियहिं दिखावा।\nबिकट रूप धरि लंक जरावा॥", "Sookshma roop dhari Siyahin dikhava\nBikat roop dhari Lank jarava", "Taking a tiny form, you appeared before Sita; taking a fearsome form, you set Lanka on fire."],
      ["भीम रूप धरि असुर सँहारे।\nरामचंद्र के काज सँवारे॥", "Bheem roop dhari asur sanhare\nRamachandra ke kaaj sanvare", "Taking a gigantic form, you destroyed the demons and accomplished Rama's mission."],
      ["लाय सजीवन लखन जियाये।\nश्रीरघुबीर हरषि उर लाये॥", "Laye Sanjivan Lakhan jiyaye\nShri Raghubir harashi ur laye", "You brought the life-giving herb and revived Lakshmana, and Rama, overjoyed, held you to his heart."],
      ["रघुपति कीन्ही बहुत बड़ाई।\nतुम मम प्रिय भरतहि सम भाई॥", "Raghupati keenhi bahut badai\nTum mam priya Bharatahi sam bhai", "Rama praised you greatly, saying: “You are as dear to me as my brother Bharata.”"],
      ["सहस बदन तुम्हरो जस गावैं।\nअस कहि श्रीपति कंठ लगावैं॥", "Sahas badan tumharo jas gavain\nAs kahi Shripati kanth lagavain", "“May the thousand-headed serpent sing your glory,” said the Lord of Lakshmi, and embraced you."],
      ["सनकादिक ब्रह्मादि मुनीसा।\nनारद सारद सहित अहीसा॥", "Sanakadik Brahmadi munisa\nNarad Sarad sahit Ahisa", "Sanaka and the sages, Brahma and the gods, Narada, Saraswati and the king of serpents,"],
      ["जम कुबेर दिगपाल जहाँ ते।\nकबि कोबिद कहि सके कहाँ ते॥", "Jam Kuber Digpal jahan te\nKabi kobid kahi sake kahan te", "Yama, Kubera and the guardians of the directions: if even they cannot fully describe your glory, how could any poet or scholar?"],
      ["तुम उपकार सुग्रीवहिं कीन्हा।\nराम मिलाय राज पद दीन्हा॥", "Tum upkar Sugreevahin keenha\nRam milaye raj pad deenha", "You did Sugriva a great service: you brought him to Rama, and he was restored to his throne."],
      ["तुम्हरो मंत्र बिभीषन माना।\nलंकेस्वर भए सब जग जाना॥", "Tumharo mantra Vibheeshan maana\nLankeshvar bhaye sab jag jaana", "Vibhishana heeded your counsel and became king of Lanka, as the whole world knows."],
      ["जुग सहस्र जोजन पर भानू।\nलील्यो ताहि मधुर फल जानू॥", "Jug sahastra jojan par bhanu\nLeelyo tahi madhur phal janu", "The sun, thousands of leagues away, you swallowed as a child, thinking it a sweet fruit."],
      ["प्रभु मुद्रिका मेलि मुख माहीं।\nजलधि लाँघि गये अचरज नाहीं॥", "Prabhu mudrika meli mukh mahin\nJaladhi laanghi gaye achraj nahin", "Holding the Lord's ring in your mouth, you leapt across the ocean. No wonder, for one such as you."],
      ["दुर्गम काज जगत के जेते।\nसुगम अनुग्रह तुम्हरे तेते॥", "Durgam kaaj jagat ke jete\nSugam anugrah tumhare tete", "However hard the tasks of this world, they become easy by your grace."],
      ["राम दुआरे तुम रखवारे।\nहोत न आज्ञा बिनु पैसारे॥", "Ram duare tum rakhvare\nHot na aagya binu paisare", "You guard Rama's door, and no one enters without your leave."],
      ["सब सुख लहै तुम्हारी सरना।\nतुम रच्छक काहू को डर ना॥", "Sab sukh lahai tumhari sarna\nTum rakshak kahu ko dar na", "Those who take refuge in you find every happiness. With you as protector, there is nothing to fear."],
      ["आपन तेज सम्हारो आपै।\nतीनों लोक हाँक तें काँपै॥", "Aapan tej samharo aapai\nTeenon lok haank te kaanpai", "You alone can contain your own power; the three worlds tremble at your roar."],
      ["भूत पिसाच निकट नहिं आवै।\nमहाबीर जब नाम सुनावै॥", "Bhoot pisach nikat nahin aavai\nMahabir jab naam sunavai", "Ghosts and evil spirits cannot come near when your name, Mahavira, is spoken."],
      ["नासै रोग हरै सब पीरा।\nजपत निरंतर हनुमत बीरा॥", "Nasai rog harai sab peera\nJapat nirantar Hanumat beera", "Illness is destroyed and all pain removed by constantly repeating the name of brave Hanuman."],
      ["संकट तें हनुमान छुड़ावै।\nमन क्रम बचन ध्यान जो लावै॥", "Sankat te Hanuman chhudavai\nMan kram bachan dhyan jo lavai", "Hanuman frees from trouble all who remember him in thought, word and deed."],
      ["सब पर राम तपस्वी राजा।\nतिन के काज सकल तुम साजा॥", "Sab par Ram tapasvi raja\nTin ke kaaj sakal tum saja", "Rama, the ascetic king, is above all, and you carried out all his work."],
      ["और मनोरथ जो कोई लावै।\nसोइ अमित जीवन फल पावै॥", "Aur manorath jo koi lavai\nSoi amit jeevan phal pavai", "Whoever brings any other wish to you receives the boundless fruit of life."],
      ["चारों जुग परताप तुम्हारा।\nहै परसिद्ध जगत उजियारा॥", "Charon jug partap tumhara\nHai parsiddh jagat ujiyara", "Your glory shines through all four ages, and your fame lights up the world."],
      ["साधु संत के तुम रखवारे।\nअसुर निकंदन राम दुलारे॥", "Sadhu sant ke tum rakhvare\nAsur nikandan Ram dulare", "You are the guardian of saints and sages, destroyer of demons, beloved of Rama."],
      ["अष्ट सिद्धि नौ निधि के दाता।\nअस बर दीन जानकी माता॥", "Ashta siddhi nau nidhi ke data\nAs bar deen Janaki mata", "Mother Sita granted you the boon of bestowing the eight spiritual powers and the nine treasures."],
      ["राम रसायन तुम्हरे पासा।\nसदा रहो रघुपति के दासा॥", "Ram rasayan tumhare pasa\nSada raho Raghupati ke dasa", "You hold the elixir of Rama's name, and you remain forever his servant."],
      ["तुम्हरे भजन राम को पावै।\nजनम जनम के दुख बिसरावै॥", "Tumhare bhajan Ram ko pavai\nJanam janam ke dukh bisravai", "Through devotion to you one reaches Rama and forgets the sorrows of many lifetimes."],
      ["अंत काल रघुबर पुर जाई।\nजहाँ जन्म हरि-भक्त कहाई॥", "Ant kaal Raghubar pur jaai\nJahan janm Hari bhakt kahai", "At the end of life one goes to Rama's abode, and wherever one is born after, one is known as a devotee of Hari."],
      ["और देवता चित्त न धरई।\nहनुमत सेइ सर्ब सुख करई॥", "Aur devta chitt na dharai\nHanumat sei sarb sukh karai", "Even without turning the mind to any other deity, serving Hanuman brings every happiness."],
      ["संकट कटै मिटै सब पीरा।\nजो सुमिरै हनुमत बलबीरा॥", "Sankat katai mitai sab peera\nJo sumirai Hanumat balbeera", "Troubles are cut away and all pain ends for whoever remembers mighty Hanuman."],
      ["जै जै जै हनुमान गोसाईं।\nकृपा करहु गुरुदेव की नाईं॥", "Jai jai jai Hanuman Gosain\nKripa karahu Gurudev ki nain", "Victory, victory, victory to Lord Hanuman! Bless me as my own Guru would."],
      ["जो सत बार पाठ कर कोई।\nछूटहि बंदि महा सुख होई॥", "Jo sat baar paath kar koi\nChhootahi bandi maha sukh hoi", "Whoever recites this a hundred times is freed from bondage and finds great joy."],
      ["जो यह पढ़ै हनुमान चालीसा।\nहोय सिद्धि साखी गौरीसा॥", "Jo yah padhai Hanuman Chalisa\nHoy siddhi saakhi Gaurisa", "Whoever reads this Hanuman Chalisa attains perfection; Shiva, Lord of Gauri, is witness."],
      ["तुलसीदास सदा हरि चेरा।\nकीजै नाथ हृदय महँ डेरा॥", "Tulsidas sada Hari chera\nKeejai Nath hriday mahan dera", "Tulsidas is forever Hari's servant. O Lord, make your home in my heart."],
      ["पवनतनय संकट हरन, मंगल मूरति रूप।\nराम लखन सीता सहित, हृदय बसहु सुर भूप॥", "Pavantanay sankat haran, mangal moorti roop\nRam Lakhan Sita sahit, hriday basahu sur bhoop", "Son of the Wind, remover of troubles, embodiment of blessing: with Rama, Lakshmana and Sita, dwell in my heart, O king of the gods.", "Doha"]
    ]
  },
  {
    id: "durga-chalisa", name: "Shri Durga Chalisa", type: "chalisa", deity: "devi",
    moments: ["protection", "evening", "morning"], lang: "Hindi", author: "Traditional; signed “Devidas”",
    about: "Forty verses to Durga, the invincible Mother, describing her many forms and victories. It is recited daily through both Navaratris.",
    verses: [
      ["नमो नमो दुर्गे सुख करनी।\nनमो नमो अम्बे दुःख हरनी॥", "Namo namo Durge sukh karani\nNamo namo Ambe dukh harani", "Salutations, salutations to Durga, bringer of happiness! Salutations, salutations to Mother Ambe, remover of sorrow!"],
      ["निरंकार है ज्योति तुम्हारी।\nतिहूँ लोक फैली उजियारी॥", "Nirankar hai jyoti tumhari\nTihoon lok phaili ujiyari", "Your light is formless, and its brightness fills the three worlds."],
      ["शशि ललाट मुख महाविशाला।\nनेत्र लाल भृकुटि विकराला॥", "Shashi lalat mukh mahavishala\nNetra laal bhrikuti vikrala", "The moon is on your brow and your face is majestic; your eyes are red and your brows fearsome."],
      ["रूप मातु को अधिक सुहावे।\nदरश करत जन अति सुख पावे॥", "Roop matu ko adhik suhave\nDarash karat jan ati sukh pave", "Your form, Mother, is most beautiful, and all who see it are filled with joy."],
      ["तुम संसार शक्ति लय कीना।\nपालन हेतु अन्न धन दीना॥", "Tum sansar shakti lay keena\nPalan hetu ann dhan deena", "You hold all the power of the universe, and you gave food and wealth to sustain it."],
      ["अन्नपूर्णा हुई जग पाला।\nतुम ही आदि सुन्दरी बाला॥", "Annapurna hui jag pala\nTum hi aadi sundari bala", "As Annapurna you nourish the world; you are the primeval, beautiful maiden."],
      ["प्रलयकाल सब नाशन हारी।\nतुम गौरी शिवशंकर प्यारी॥", "Pralaykaal sab nashan hari\nTum Gauri Shivshankar pyari", "At the end of time you dissolve all things; you are Gauri, beloved of Shiva."],
      ["शिव योगी तुम्हरे गुण गावें।\nब्रह्मा विष्णु तुम्हें नित ध्यावें॥", "Shiv yogi tumhare gun gaven\nBrahma Vishnu tumhen nit dhyaven", "Shiva and the yogis sing your virtues; Brahma and Vishnu meditate on you always."],
      ["रूप सरस्वती को तुम धारा।\nदे सुबुद्धि ऋषि मुनिन उबारा॥", "Roop Saraswati ko tum dhara\nDe subuddhi rishi munin ubara", "You took the form of Saraswati and uplifted the sages by giving them wisdom."],
      ["धरयो रूप नरसिंह को अम्बा।\nपरगट भई फाड़कर खम्बा॥", "Dharyo roop Narsingh ko Amba\nPargat bhai phaadkar khamba", "Mother, you took the form of Narasimha and burst forth from the pillar,"],
      ["रक्षा करि प्रह्लाद बचायो।\nहिरण्याक्ष को स्वर्ग पठायो॥", "Raksha kari Prahlad bachayo\nHiranyaksh ko swarg pathayo", "protecting and saving Prahlada, and sending the demon king to heaven."],
      ["लक्ष्मी रूप धरो जग माहीं।\nश्री नारायण अंग समाहीं॥", "Lakshmi roop dharo jag maahin\nShri Narayan ang samaahin", "You took the form of Lakshmi in the world and dwell at the side of Narayana."],
      ["क्षीरसिन्धु में करत विलासा।\nदयासिन्धु दीजै मन आसा॥", "Ksheersindhu mein karat vilasa\nDayasindhu deejai man aasa", "You delight in the ocean of milk. Ocean of compassion, fulfil the hopes of my heart."],
      ["हिंगलाज में तुम्हीं भवानी।\nमहिमा अमित न जात बखानी॥", "Hinglaj mein tumhin Bhavani\nMahima amit na jaat bakhani", "You are Bhavani of Hinglaj, and your boundless glory cannot be described."],
      ["मातंगी अरु धूमावति माता।\nभुवनेश्वरी बगला सुख दाता॥", "Matangi aru Dhoomavati Mata\nBhuvaneshvari Bagla sukh data", "You are Mother Matangi and Dhumavati, Bhuvaneshvari and Bagalamukhi, givers of happiness."],
      ["श्री भैरव तारा जग तारिणी।\nछिन्न भाल भव दुःख निवारिणी॥", "Shri Bhairav Tara jag tarini\nChhinna bhaal bhav dukh nivarini", "You are Bhairavi and Tara, who carries the world across, and Chhinnamasta, who ends the sorrow of worldly life."],
      ["केहरि वाहन सोह भवानी।\nलांगुर वीर चलत अगवानी॥", "Kehari vahan soh Bhavani\nLangur veer chalat agvani", "Bhavani, you look splendid riding the lion, with the heroic Hanuman leading the way before you."],
      ["कर में खप्पर खड्ग विराजै।\nजाको देख काल डर भाजै॥", "Kar mein khappar khadag virajai\nJaako dekh kaal dar bhaajai", "In your hands are the bowl and the sword; seeing them, even Death runs in fear."],
      ["सोहै अस्त्र और त्रिशूला।\nजाते उठत शत्रु हिय शूला॥", "Sohai astra aur trishoola\nJaate uthat shatru hiy shoola", "You bear weapons and the trident, which strike pain into the hearts of enemies."],
      ["नगरकोट में तुम्हीं विराजत।\nतिहुँलोक में डंका बाजत॥", "Nagarkot mein tumhin virajat\nTihunlok mein danka baajat", "You reside at Nagarkot, and your drum of victory resounds through the three worlds."],
      ["शुम्भ निशुम्भ दानव तुम मारे।\nरक्तबीज शंखन संहारे॥", "Shumbh Nishumbh danav tum maare\nRaktabeej shankhan sanhare", "You slew the demons Shumbha and Nishumbha and destroyed countless Raktabijas."],
      ["महिषासुर नृप अति अभिमानी।\nजेहि अघ भार मही अकुलानी॥", "Mahishasur nrip ati abhimani\nJehi agh bhaar mahi akulani", "The demon king Mahishasura was so arrogant that the earth groaned under the weight of his sins."],
      ["रूप कराल कालिका धारा।\nसेन सहित तुम तिहि संहारा॥", "Roop karaal Kalika dhara\nSen sahit tum tihi sanhara", "Taking the terrible form of Kali, you destroyed him with all his army."],
      ["परी गाढ़ सन्तन पर जब जब।\nभई सहाय मातु तुम तब तब॥", "Pari gaadh santan par jab jab\nBhai sahay matu tum tab tab", "Whenever hardship fell upon the saints, Mother, you came to their aid."],
      ["अमरपुरी अरु बासव लोका।\nतब महिमा सब रहें अशोका॥", "Amarpuri aru Basav loka\nTab mahima sab rahen ashoka", "By your glory the city of the immortals and Indra's realm remain free of sorrow."],
      ["ज्वाला में है ज्योति तुम्हारी।\nतुम्हें सदा पूजें नर-नारी॥", "Jwala mein hai jyoti tumhari\nTumhen sada poojen nar nari", "Your light burns at Jwalamukhi, and men and women worship you always."],
      ["प्रेम भक्ति से जो यश गावें।\nदुःख दारिद्र निकट नहिं आवें॥", "Prem bhakti se jo yash gaven\nDukh daridra nikat nahin aaven", "Sorrow and poverty never come near those who sing your glory with love and devotion."],
      ["ध्यावे तुम्हें जो नर मन लाई।\nजन्म-मरण ताकौ छुटि जाई॥", "Dhyave tumhen jo nar man laai\nJanm maran taakau chhuti jaai", "Whoever meditates on you with a focused mind is freed from birth and death."],
      ["जोगी सुर मुनि कहत पुकारी।\nयोग न हो बिन शक्ति तुम्हारी॥", "Jogi sur muni kahat pukari\nYog na ho bin shakti tumhari", "Yogis, gods and sages proclaim that without your power there can be no yoga."],
      ["शंकर आचारज तप कीनो।\nकाम अरु क्रोध जीति सब लीनो॥", "Shankar Acharaj tap keeno\nKaam aru krodh jeeti sab leeno", "Shankaracharya performed great austerities and conquered desire and anger."],
      ["निशिदिन ध्यान धरो शंकर को।\nकाहु काल नहिं सुमिरो तुमको॥", "Nishidin dhyan dharo Shankar ko\nKaahu kaal nahin sumiro tumko", "Day and night he meditated on Shiva, yet never once remembered you."],
      ["शक्ति रूप का मरम न पायो।\nशक्ति गई तब मन पछितायो॥", "Shakti roop ka maram na payo\nShakti gai tab man pachhitayo", "He did not grasp the secret of Shakti; when his strength left him, he regretted it."],
      ["शरणागत हुई कीर्ति बखानी।\nजय जय जय जगदम्ब भवानी॥", "Sharnagat hui kirti bakhani\nJai jai jai Jagdamb Bhavani", "Then he took refuge in you and sang your glory: “Victory, victory, victory to Bhavani, Mother of the world!”"],
      ["भई प्रसन्न आदि जगदम्बा।\nदई शक्ति नहिं कीन विलम्बा॥", "Bhai prasanna aadi Jagdamba\nDai shakti nahin keen vilamba", "The primeval Mother of the world was pleased, and without delay restored his strength."],
      ["मोको मातु कष्ट अति घेरो।\nतुम बिन कौन हरै दुःख मेरो॥", "Moko matu kasht ati ghero\nTum bin kaun harai dukh mero", "Mother, I am surrounded by great troubles. Who but you can take away my sorrow?"],
      ["आशा तृष्णा निपट सतावें।\nरिपु मूरख मोहि अति डर पावें॥", "Aasha trishna nipat sataven\nRipu moorakh mohi ati dar paaven", "Hopes and cravings torment me, and foolish enemies seek to frighten me."],
      ["शत्रु नाश कीजै महारानी।\nसुमिरौं इकचित तुम्हें भवानी॥", "Shatru naash keejai Maharani\nSumiraun ikchit tumhen Bhavani", "Destroy my enemies, great Queen; Bhavani, I remember you with a single mind."],
      ["करो कृपा हे मातु दयाला।\nऋद्धि-सिद्धि दै करहु निहाला॥", "Karo kripa he matu dayala\nRiddhi siddhi dai karahu nihala", "Have mercy, compassionate Mother; bless me with prosperity and fulfilment."],
      ["जब लगि जिऊँ दया फल पाऊँ।\nतुम्हरो यश मैं सदा सुनाऊँ॥", "Jab lagi jiyoon daya phal paaoon\nTumharo yash main sada sunaaoon", "As long as I live, may I receive the fruit of your kindness, and may I always tell of your glory."],
      ["श्री दुर्गा चालीसा जो कोई गावै।\nसब सुख भोग परमपद पावै॥", "Shri Durga Chalisa jo koi gavai\nSab sukh bhog parampad pavai", "Whoever sings the Durga Chalisa enjoys every happiness and reaches the highest state."],
      ["देवीदास शरण निज जानी।\nकरहु कृपा जगदम्ब भवानी॥", "Devidas sharan nij jaani\nKarahu kripa Jagdamb Bhavani", "Knowing Devidas to be under your shelter, have mercy on him, Bhavani, Mother of the world."]
    ]
  },
  {
    id: "shiv-chalisa", name: "Shri Shiv Chalisa", type: "chalisa", deity: "shiva",
    moments: ["evening", "protection", "peace"], lang: "Hindi", author: "Traditional; signed “Ayodhyadas”",
    about: "Forty verses to Shiva retelling his compassion: drinking the poison of the ocean, granting boons to Rama and destroying the demons who troubled the gods. It is recited on Mondays, Pradosh and Maha Shivaratri. Wording varies a little between printed editions.",
    verses: [
      ["जय गणेश गिरिजा सुवन, मंगल मूल सुजान।\nकहत अयोध्यादास तुम, देहु अभय वरदान॥", "Jai Ganesh Girija suvan, mangal mool sujan\nKahat Ayodhyadas tum, dehu abhay vardan", "Glory to Ganesha, wise son of Girija and root of all blessings. Ayodhyadas prays: grant me the boon of fearlessness.", "Doha"],
      ["जय गिरिजा पति दीन दयाला।\nसदा करत सन्तन प्रतिपाला॥", "Jai Girija pati deen dayala\nSada karat santan pratipala", "Glory to the husband of Girija, kind to the humble, who always protects the saints."],
      ["भाल चन्द्रमा सोहत नीके।\nकानन कुण्डल नागफनी के॥", "Bhaal chandrama sohat neeke\nKanan kundal naagphani ke", "The moon shines beautifully on your forehead, and your earrings are serpents' hoods."],
      ["अंग गौर शिर गंग बहाये।\nमुण्डमाल तन क्षार लगाये॥", "Ang gaur shir Gang bahaye\nMundmaal tan kshaar lagaye", "Your body is fair, the Ganga flows from your head, and you wear a garland of skulls and ash upon your skin."],
      ["वस्त्र खाल बाघम्बर सोहे।\nछवि को देखि नाग मुनि मोहे॥", "Vastra khaal baaghambar sohe\nChhavi ko dekhi naag muni mohe", "You are clothed in a tiger skin, and serpents and sages are enchanted by your form."],
      ["मैना मातु की हवै दुलारी।\nबाम अंग सोहत छवि न्यारी॥", "Maina matu ki havai dulari\nBaam ang sohat chhavi nyari", "The beloved daughter of Mother Maina, Parvati, shines at your left side with unique beauty."],
      ["कर त्रिशूल सोहत छवि भारी।\nकरत सदा शत्रुन क्षयकारी॥", "Kar trishool sohat chhavi bhari\nKarat sada shatrun kshaykari", "The trident in your hand looks magnificent and always destroys the enemies of good."],
      ["नन्दि गणेश सोहै तहँ कैसे।\nसागर मध्य कमल हैं जैसे॥", "Nandi Ganesh sohai tahan kaise\nSagar madhya kamal hain jaise", "Nandi and Ganesha look as lovely beside you as lotuses in the middle of the ocean."],
      ["कार्तिक श्याम और गणराऊ।\nया छवि को कहि जात न काऊ॥", "Kartik Shyam aur Ganrau\nYa chhavi ko kahi jaat na kaau", "No one can describe the beauty of this scene with Kartikeya, Shyama and the lord of the ganas."],
      ["देवन जबहीं जाय पुकारा।\nतब ही दुख प्रभु आप निवारा॥", "Devan jabahin jaay pukara\nTab hi dukh prabhu aap nivara", "Whenever the gods called out to you, Lord, you yourself removed their distress."],
      ["किया उपद्रव तारक भारी।\nदेवन सब मिलि तुमहिं जुहारी॥", "Kiya upadrav Taarak bhari\nDevan sab mili tumahin juhari", "When the demon Taraka caused great havoc, all the gods together came to you for help."],
      ["तुरत षडानन आप पठायउ।\nलवनिमेष महँ मारि गिरायउ॥", "Turat Shadanan aap pathayau\nLavnimesh mahan maari girayau", "At once you sent six-faced Kartikeya, who struck Taraka down in the blink of an eye."],
      ["आप जलंधर असुर संहारा।\nसुयश तुम्हार विदित संसारा॥", "Aap Jalandhar asur sanhara\nSuyash tumhar vidit sansara", "You yourself destroyed the demon Jalandhara, and your fame is known throughout the world."],
      ["त्रिपुरासुर सन युद्ध मचाई।\nसबहिं कृपा कर लीन बचाई॥", "Tripurasur san yuddh machai\nSabahin kripa kar leen bachai", "You waged war on the demons of the three cities and in your grace saved everyone."],
      ["किया तपहिं भागीरथ भारी।\nपुरब प्रतिज्ञा तासु पुरारी॥", "Kiya tapahin Bhagirath bhari\nPurab pratigya taasu Purari", "When Bhagiratha performed great austerities, you fulfilled your promise to him and brought down the Ganga."],
      ["दानिन महँ तुम सम कोउ नाहीं।\nसेवक स्तुति करत सदाहीं॥", "Daanin mahan tum sam kou naahin\nSevak stuti karat sadaahin", "Among all givers there is none like you, and your servants praise you always."],
      ["वेद नाम महिमा तव गाई।\nअकथ अनादि भेद नहिं पाई॥", "Ved naam mahima tav gaai\nAkath anaadi bhed nahin paai", "The Vedas sing the glory of your name, yet even they cannot fathom your indescribable, beginningless mystery."],
      ["प्रगटी उदधि मंथन में ज्वाला।\nजरत सुरासुर भए विहाला॥", "Pragati udadhi manthan mein jwala\nJarat surasur bhaye vihala", "When the ocean was churned, a burning poison rose up, and gods and demons alike were in agony."],
      ["कीन्ह दया तहँ करी सहाई।\nनीलकण्ठ तब नाम कहाई॥", "Keenh daya tahan kari sahai\nNeelkanth tab naam kahai", "In your compassion you came to their aid and drank it, and so you are called Neelakantha, the blue-throated."],
      ["पूजन रामचन्द्र जब कीन्हा।\nजीत के लंक विभीषण दीन्हा॥", "Poojan Ramachandra jab keenha\nJeet ke Lank Vibheeshan deenha", "When Rama worshipped you, he conquered Lanka and gave it to Vibhishana."],
      ["सहस कमल में हो रहे धारी।\nकीन्ह परीक्षा तबहिं पुरारी॥", "Sahas kamal mein ho rahe dhari\nKeenh pareeksha tabahin Purari", "As a thousand lotuses were being offered to you, you put the worshipper to the test."],
      ["एक कमल प्रभु राखेउ जोई।\nकमल नयन पूजन चहँ सोई॥", "Ek kamal prabhu raakheu joi\nKamal nayan poojan chahan soi", "You hid one lotus, Lord, and the lotus-eyed one was ready to offer his own eye in its place."],
      ["कठिन भक्ति देखी प्रभु शंकर।\nभए प्रसन्न दिए इच्छित वर॥", "Kathin bhakti dekhi prabhu Shankar\nBhaye prasanna diye ichchhit var", "Seeing such steadfast devotion, Lord Shankara was pleased and granted the boon he desired."],
      ["जय जय जय अनन्त अविनाशी।\nकरत कृपा सब के घटवासी॥", "Jai jai jai anant avinashi\nKarat kripa sab ke ghatvasi", "Victory, victory, victory to the infinite, the imperishable, who dwells in every heart and blesses all."],
      ["दुष्ट सकल नित मोहि सतावैं।\nभ्रमत रहौं मोहि चैन न आवैं॥", "Dusht sakal nit mohi sataavain\nBhramat rahaun mohi chain na aavain", "Wicked forces trouble me constantly; I wander in confusion and find no peace."],
      ["त्राहि त्राहि मैं नाथ पुकारो।\nयह अवसर मोहि आन उबारो॥", "Traahi traahi main Naath pukaro\nYah avsar mohi aan ubaaro", "“Save me, save me!” I cry to you, Lord. Come now and rescue me."],
      ["लै त्रिशूल शत्रुन को मारो।\nसंकट से मोहि आन उबारो॥", "Lai trishool shatrun ko maaro\nSankat se mohi aan ubaaro", "Take up your trident and strike down what opposes me; come and rescue me from my troubles."],
      ["मात पिता भ्राता सब होई।\nसंकट में पूछत नहिं कोई॥", "Maat pita bhraata sab hoi\nSankat mein poochhat nahin koi", "I may have mother, father and brothers, but in times of crisis no one asks after me."],
      ["स्वामी एक है आस तुम्हारी।\nआय हरहु मम संकट भारी॥", "Swami ek hai aas tumhari\nAay harahu mam sankat bhari", "Lord, my only hope is you. Come and take away my heavy troubles."],
      ["धन निर्धन को देत सदा हीं।\nजो कोई जाँचे सो फल पाहीं॥", "Dhan nirdhan ko det sada hin\nJo koi jaanche so phal paahin", "You always give wealth to the poor, and whoever asks of you receives."],
      ["अस्तुति केहि विधि करैं तुम्हारी।\nक्षमहु नाथ अब चूक हमारी॥", "Astuti kehi vidhi karain tumhari\nKshamahu Naath ab chook hamari", "How can I praise you properly? Forgive my shortcomings, Lord."],
      ["शंकर हो संकट के नाशन।\nमंगल कारण विघ्न विनाशन॥", "Shankar ho sankat ke naashan\nMangal kaaran vighna vinaashan", "Shankara, you destroy all trouble; you are the source of blessings and the end of obstacles."],
      ["योगी यति मुनि ध्यान लगावैं।\nशारद नारद शीश नवावैं॥", "Yogi yati muni dhyan lagaavain\nSharad Narad sheesh navaavain", "Yogis, ascetics and sages meditate on you; Saraswati and Narada bow their heads to you."],
      ["नमो नमो जय नमः शिवाय।\nसुर ब्रह्मादिक पार न पाय॥", "Namo namo jai namah Shivaya\nSur Brahmadik paar na paay", "Salutations, salutations, glory, Om Namah Shivaya! Even Brahma and the gods cannot find your limits."],
      ["जो यह पाठ करै मन लाई।\nता पर होत हैं शम्भु सहाई॥", "Jo yah paath karai man laai\nTa par hot hain Shambhu sahai", "Shambhu helps all who recite this with a devoted mind."],
      ["ऋनियाँ जो कोई हो अधिकारी।\nपाठ करै सो पावन हारी॥", "Riniyan jo koi ho adhikari\nPaath karai so paavan haari", "Even one weighed down by debts, reciting this, becomes pure and is freed."],
      ["पुत्र होन की इच्छा जोई।\nनिश्चय शिव प्रसाद तेहि होई॥", "Putra hon ki ichchha joi\nNishchay Shiv prasad tehi hoi", "Whoever longs for a child surely receives Shiva's grace."],
      ["पण्डित त्रयोदशी को लावे।\nध्यान पूर्वक होम करावे॥", "Pandit trayodashi ko lave\nDhyan poorvak hom karave", "Invite a priest on the thirteenth day of the lunar fortnight and have a fire ritual performed with devotion."],
      ["त्रयोदशी व्रत करै हमेशा।\nताके तन नहिं रहै कलेशा॥", "Trayodashi vrat karai hamesha\nTaake tan nahin rahai kalesha", "Whoever always keeps the Trayodashi fast remains free of bodily suffering."],
      ["धूप दीप नैवेद्य चढ़ावे।\nशंकर सम्मुख पाठ सुनावे॥", "Dhoop deep naivedya chadhave\nShankar sammukh paath sunave", "Offer incense, a lamp and food, and recite this before Shankara."],
      ["जन्म जन्म के पाप नसावे।\nअन्त धाम शिवपुर में पावे॥", "Janm janm ke paap nasaave\nAnt dhaam Shivpur mein paave", "The wrongs of many lifetimes are destroyed, and at the end one reaches Shiva's abode."],
      ["कहै अयोध्यादास आस तुम्हारी।\nजानि सकल दुख हरहु हमारी॥", "Kahai Ayodhyadas aas tumhari\nJaani sakal dukh harahu hamari", "Ayodhyadas says: my hope is in you. Knowing this, take away all our sorrows."],
      ["नित्त नेम कर प्रातः ही, पाठ करौं चालीसा।\nतुम मेरी मनोकामना, पूर्ण करो जगदीश॥", "Nitt nem kar praatah hi, paath karaun chalisa\nTum meri manokamana, poorn karo Jagdish", "Each morning, as a daily discipline, I recite this Chalisa. O Lord of the world, fulfil the wishes of my heart.", "Doha"]
    ]
  },

  /* ================================================================== */
  /* BHAJANS                                                             */
  /* ================================================================== */
  {
    id: "ramchandra-kripalu", name: "Shri Ramachandra Kripalu", type: "bhajan", deity: "rama",
    moments: ["evening", "morning", "peace"], lang: "Awadhi", author: "Goswami Tulsidas, Vinaya Patrika 45",
    about: "Tulsidas's luminous hymn describing Rama's beauty and compassion, one of the most beloved bhajans of North India.",
    verses: [
      ["श्रीरामचन्द्र कृपालु भजु मन, हरण भवभय दारुणम्।\nनवकंज लोचन कंज मुख, कर कंज पद कंजारुणम्॥", "Shri Ramachandra kripalu bhaju man, haran bhavbhay daarunam\nNavkanj lochan kanj mukh, kar kanj pad kanjarunam", "O mind, worship merciful Shri Ramachandra, who removes the terrible fear of worldly life. His eyes are like fresh lotuses, his face is a lotus, and his hands and feet are like red lotuses."],
      ["कंदर्प अगणित अमित छवि, नवनील नीरद सुन्दरम्।\nपट पीत मानहुँ तड़ित रुचि, शुचि नौमि जनक सुतावरम्॥", "Kandarp aganit amit chhavi, navneel neerad sundaram\nPat peet maanahun tadit ruchi, shuchi naumi Janak sutavaram", "His beauty surpasses countless gods of love; he is lovely as a fresh dark rain cloud. His yellow robe gleams like lightning. I bow to the pure one, the husband of Janaka's daughter."],
      ["भजु दीनबन्धु दिनेश दानव, दैत्यवंश निकन्दनम्।\nरघुनन्द आनन्दकन्द कोशलचन्द, दशरथ नन्दनम्॥", "Bhaju deenbandhu dinesh daanav, daityavansh nikandanam\nRaghunand anandkand Koshalchand, Dasharath nandanam", "Worship the friend of the humble, radiant as the sun, who uproots the race of demons; the joy of the Raghus, the source of bliss, the moon of Kosala, the son of Dasharatha."],
      ["सिर मुकुट कुण्डल तिलक चारु, उदारु अंग विभूषणम्।\nआजानुभुज शर चाप धर, संग्राम जित खरदूषणम्॥", "Sir mukut kundal tilak charu, udaru ang vibhooshanam\nAajanubhuj shar chaap dhar, sangram jit Khardooshanam", "A crown on his head, earrings and a lovely tilaka, with fine ornaments on every limb; his arms reach to his knees, he holds bow and arrows, and he conquered Khara and Dushana in battle."],
      ["इति वदति तुलसीदास शंकर, शेष मुनि मन रंजनम्।\nमम हृदय कंज निवास कुरु, कामादि खलदल गंजनम्॥", "Iti vadati Tulsidas Shankar, Shesh muni man ranjanam\nMam hriday kanj nivas kuru, kamadi khaldal ganjanam", "So says Tulsidas: O delight of the hearts of Shiva, Shesha and the sages, make your home in the lotus of my heart and destroy the host of enemies within, desire and the rest."]
    ]
  },
  {
    id: "raghupati", name: "Raghupati Raghava Raja Ram", type: "bhajan", deity: "rama",
    moments: ["evening", "peace"], lang: "Hindi", author: "Traditional Ram Dhun; the version sung by Mahatma Gandhi",
    about: "A simple, joyful chant to Rama. Mahatma Gandhi sang it on the Salt March, adding a line that names God as both Ishvara and Allah.",
    verses: [
      ["रघुपति राघव राजाराम, पतित पावन सीताराम॥", "Raghupati Raghav Raja Ram, patit paavan Sitaram", "Lord of the Raghus, King Rama, Sita's Rama, who purifies the fallen.", "Refrain"],
      ["सीताराम सीताराम, भज प्यारे तू सीताराम॥", "Sitaram Sitaram, bhaj pyare tu Sitaram", "Sita and Rama, Sita and Rama: sing, dear one, the names of Sita and Rama."],
      ["ईश्वर अल्लाह तेरो नाम, सब को सन्मति दे भगवान॥", "Ishvar Allah tero naam, sab ko sanmati de Bhagvan", "Ishvara and Allah are your names. O Lord, give everyone a good and wise mind."]
    ]
  },
  {
    id: "vaishnav-jan", name: "Vaishnava Jana To", type: "bhajan", deity: "vishnu",
    moments: ["morning", "peace"], lang: "Gujarati", author: "Narsinh Mehta, 15th century",
    about: "The Gujarati saint Narsinh Mehta's portrait of a true devotee: one who feels the pain of others. It was Mahatma Gandhi's favourite hymn.",
    verses: [
      ["वैष्णव जन तो तेने कहिये जे पीड पराई जाणे रे।\nपर दुःखे उपकार करे तो ये मन अभिमान न आणे रे॥", "Vaishnav jan to tene kahiye je peed parai jaane re\nPar dukhe upkar kare to ye man abhiman na aane re", "Call that person a true devotee of Vishnu who feels the pain of others; who helps those in sorrow and does not let pride enter the mind."],
      ["सकळ लोकमां सहुने वंदे, निंदा न करे केनी रे।\nवाच काछ मन निश्चळ राखे, धन धन जननी तेनी रे॥", "Sakal lokman sahune vande, ninda na kare keni re\nVaach kaachh man nishchal raakhe, dhan dhan janani teni re", "They respect everyone in the world and speak ill of no one; they keep their words, actions and mind steady and pure. Blessed, blessed is the mother of such a person."],
      ["समदृष्टि ने तृष्णा त्यागी, परस्त्री जेने मात रे।\nजिह्वा थकी असत्य न बोले, परधन नव झाले हाथ रे॥", "Samdrishti ne trishna tyagi, parastri jene maat re\nJihva thaki asatya na bole, pardhan nav jhaale haath re", "They see all with equal eyes and have given up craving; they regard another's wife as their mother. Their tongue never speaks untruth, and their hand never touches another's wealth."],
      ["मोह माया व्यापे नहि जेने, दृढ वैराग्य जेना मनमां रे।\nरामनाम शुं ताळी लागी, सकळ तीरथ तेना तनमां रे॥", "Moh maya vyape nahi jene, dridh vairagya jena manman re\nRamnaam shun taali laagi, sakal tirath tena tanman re", "Delusion and illusion cannot touch them; firm detachment lives in their heart. They are absorbed in the name of Rama, and all the places of pilgrimage are within their body."],
      ["वणलोभी ने कपटरहित छे, काम क्रोध निवार्या रे।\nभणे नरसैयो तेनुं दरसन करतां, कुळ एकोतेर तार्या रे॥", "Vanlobhi ne kapatrahit chhe, kaam krodh nivarya re\nBhane Narsaiyo tenun darsan kartan, kul ekoter taarya re", "They are free of greed and deceit and have overcome desire and anger. Narsinh says: simply to see such a person saves seventy-one generations of one's family."]
    ]
  },
  {
    id: "payoji", name: "Payoji Maine Ram Ratan Dhan Payo", type: "bhajan", deity: "krishna",
    moments: ["morning", "peace", "evening"], lang: "Rajasthani-Hindi", author: "Mirabai, 16th century",
    about: "The poet-princess Mirabai rejoices at receiving the priceless jewel of God's name from her guru, a treasure that can never be stolen or spent.",
    verses: [
      ["पायो जी मैंने राम रतन धन पायो॥", "Payo ji maine Ram ratan dhan payo", "I have found it! I have found the wealth of the jewel of God's name.", "Refrain"],
      ["वस्तु अमोलक दी मेरे सतगुरु, किरपा कर अपनायो॥", "Vastu amolak di mere Satguru, kirpa kar apnayo", "My true Guru gave me this priceless gift, and in his grace took me as his own."],
      ["जनम जनम की पूँजी पाई, जग में सभी खोवायो॥", "Janam janam ki poonji paai, jag mein sabhi khovayo", "I have found the treasure of many lifetimes, and let go of everything else in the world."],
      ["खरचै न खूटै, चोर न लूटै, दिन दिन बढ़त सवायो॥", "Kharchai na khootai, chor na lootai, din din badhat savayo", "Spending cannot use it up, thieves cannot steal it; day by day it grows more and more."],
      ["सत की नाव खेवटिया सतगुरु, भवसागर तर आयो॥", "Sat ki naav khevatiya Satguru, bhavsagar tar aayo", "In the boat of truth, with my true Guru at the oars, I have crossed the ocean of worldly life."],
      ["मीरा के प्रभु गिरिधर नागर, हरख हरख जस गायो॥", "Meera ke prabhu Giridhar Nagar, harakh harakh jas gaayo", "Mira's Lord is Giridhar, the lifter of the mountain, and with joy upon joy she sings his praise."]
    ]
  },
  {
    id: "achyutam", name: "Achyutam Keshavam", type: "bhajan", deity: "krishna",
    moments: ["morning", "evening", "peace"], lang: "Sanskrit", author: "Achyutashtakam, attributed to Adi Shankaracharya",
    about: "The first verse of the Achyutashtakam, a garland of names of Vishnu, Krishna and Rama, widely sung as a gentle bhajan.",
    verses: [["अच्युतं केशवं रामनारायणं कृष्णदामोदरं वासुदेवं हरिम्।\nश्रीधरं माधवं गोपिकावल्लभं जानकीनायकं रामचन्द्रं भजे॥", "acyutaṃ keśavaṃ rāmanārāyaṇaṃ kṛṣṇadāmodaraṃ vāsudevaṃ harim\nśrīdharaṃ mādhavaṃ gopikāvallabhaṃ jānakīnāyakaṃ rāmacandraṃ bhaje", "I worship the Unfailing One, Keshava, Rama and Narayana, Krishna Damodara, Vasudeva, Hari; the bearer of Lakshmi, Madhava, the beloved of the gopis, the Lord of Janaki, Ramachandra."]]
  },
  {
    id: "govinda-jaya", name: "Govinda Jaya Jaya", type: "bhajan", deity: "krishna",
    moments: ["evening", "peace"], lang: "Sanskrit", author: "Traditional kirtan",
    about: "A call-and-response kirtan of Krishna's names, easy for anyone to join.",
    verses: [["गोविन्द जय जय गोपाल जय जय।\nराधारमण हरि गोविन्द जय जय॥", "govinda jaya jaya gopāla jaya jaya\nrādhāramaṇa hari govinda jaya jaya", "Glory, glory to Govinda! Glory, glory to Gopala! Glory, glory to Hari Govinda, the delight of Radha!"]]
  },
  {
    id: "hare-murare", name: "Shri Krishna Govinda Hare Murare", type: "bhajan", deity: "krishna",
    moments: ["evening", "sleep", "peace"], lang: "Sanskrit", author: "Traditional dhun",
    about: "A soft, meditative chant of Krishna's names, often sung at the end of satsang.",
    verses: [["श्री कृष्ण गोविन्द हरे मुरारे।\nहे नाथ नारायण वासुदेव॥", "śrī kṛṣṇa govinda hare murāre\nhe nātha nārāyaṇa vāsudeva", "O Shri Krishna, Govinda, Hari, slayer of the demon Mura; O Lord, Narayana, Vasudeva."]]
  },
  {
    id: "radha-madhav", name: "Jaya Radha Madhava", type: "bhajan", deity: "krishna",
    moments: ["morning", "evening"], lang: "Sanskrit-Bengali", author: "Bhaktivinoda Thakura, 19th century",
    about: "A short, much-loved song in the Gaudiya Vaishnava tradition, describing Krishna as the lover of Radha and the joy of Vraja.",
    verses: [["जय राधा माधव कुञ्जबिहारी।\nगोपीजनवल्लभ गिरिवरधारी।\nयशोदानन्दन व्रजजनरञ्जन।\nयमुनातीरवनचारी॥", "jaya rādhā-mādhava kuñja-bihārī\ngopī-jana-vallabha giri-vara-dhārī\nyaśodā-nandana vraja-jana-rañjana\nyamunā-tīra-vana-cārī", "Glory to Radha's beloved Madhava, who wanders the forest groves; dear to the gopis, lifter of the great hill; the darling of Yashoda, delight of the people of Vraja, who roams the woods along the Yamuna."]]
  }
];
