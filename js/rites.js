/* Dharma Path: rites of passage (samskaras), in the order of a life.
   Each rite: { id, deva, name, sanskrit, stage, art, when, where, who, length, summary, intro (HTML),
   verse?: [devanagari, roman, english, source], need: [items], steps: [[title, detail]] or phases: [{ title, steps }],
   customs: [[region, text]], withPriest, abroad, prayers: [prayer ids], links?: [[label, href]] } */
window.CONTENT.riteStages = [
  { id: "before", deva: "गर्भ", name: "Before birth", text: "Blessings for the mother and the child she carries." },
  { id: "infancy", deva: "शैशव", name: "Birth and infancy", text: "Welcoming a new soul, and the little milestones of the first years." },
  { id: "youth", deva: "बाल्य", name: "Childhood and youth", text: "Learning, discipline and growing up." },
  { id: "adult", deva: "गृहस्थ", name: "Adult life", text: "Marriage, a home of one's own, and the honour of a long life." },
  { id: "end", deva: "अन्त्य", name: "The end of life and beyond", text: "Letting go with love, and remembering those who came before." }
];
window.CONTENT.lifeEvents = [];
const rite = (r) => window.CONTENT.lifeEvents.push(r);

/* ---------------------------------------------------------------------- */
/* Before birth                                                            */
/* ---------------------------------------------------------------------- */
rite({
  id: `simanta`, deva: `सीमन्तोन्नयन`, name: `Blessing the Mother-to-be`, sanskrit: `Simantonnayana`, stage: `before`, art: `bangles`,
  when: `Usually the 7th month of pregnancy`, where: `At home, or a family hall`, who: `The women of the family, sometimes a priest`, length: `2 to 3 hours`,
  summary: `Surrounding the expectant mother with love, blessings and her favourite foods.`,
  intro: `<p>The scriptures describe three samskaras before a child is born. <strong>Garbhadhana</strong> is a prayer for a good child; <strong>Pumsavana</strong>, in the third month, asks for the baby's health and strength; and <strong>Simantonnayana</strong>, “the parting of the hair,” is performed in the later months to bless and protect mother and child.</p>
<p>In the old rite, the husband gently parted his wife's hair while verses were chanted, and musicians played, because the unborn child was believed to hear and be shaped by sound. Today the ceremony is above all a joyful gathering of women, known as <strong>Godh Bharai</strong> (“filling the lap”) in North India, <strong>Seemantham</strong> in the South and <strong>Valaikappu</strong> in Tamil Nadu. The mother is dressed in new clothes, pampered and fed, and showered with blessings for an easy birth.</p>
<p>Behind the celebration lies a beautiful idea: a child's life begins before birth, and a calm, happy and well-cared-for mother is the best gift the family can give it.</p>`,
  need: [`A decorated seat for the mother`, `A new sari or outfit for her`, `Glass bangles, often green or red`, `Fruits, dry fruits and sweets`, `A coconut`, `Flowers for her hair`, `Turmeric and kumkum`, `A lamp and incense`, `Her favourite dishes for the meal`],
  steps: [
    [`Begin with Ganesha`, `Light a lamp and offer a short prayer to Ganesha, so the ceremony and the birth go smoothly.`],
    [`Welcome the mother`, `She is dressed in her new clothes and seated in the place of honour. Elders apply haldi and kumkum to her forehead and place flowers in her hair.`],
    [`Fill her lap`, `One by one, the women place fruits, a coconut, sweets and small gifts in the folds of her sari, wishing her a full and fruitful life.`],
    [`Bangles`, `Elders slip bangles onto her wrists. In Tamil tradition the gentle sound of the glass bangles is said to soothe and protect the baby.`],
    [`Aarti and blessings`, `An aarti is waved before her, and each guest blesses her and the child to come.`],
    [`Feast and music`, `Everyone shares a meal of her favourite foods. Songs are sung, and many families play soft devotional music for the baby to hear.`]
  ],
  verse: [`सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः।`, `sarve bhavantu sukhinaḥ sarve santu nirāmayāḥ`, `May all be happy; may all be free from illness.`, `A traditional prayer of blessing`],
  customs: [
    [`North India`, `Godh Bharai is held in the seventh or eighth month, a lively gathering of women with songs, games and gifts.`],
    [`Tamil Nadu`, `Valaikappu, “the bangle ceremony,” fills the mother's arms with dozens of glass bangles.`],
    [`Andhra Pradesh, Telangana and Karnataka`, `Seemantham often includes a priest-led puja and a feast for the extended family.`],
    [`Bengal`, `In Shaadh, the mother is served the dishes she has been craving, cooked by her own mother.`],
    [`Maharashtra`, `Dohale Jevan celebrates her cravings with a meal and a swing decorated with flowers.`]
  ],
  withPriest: `A priest can perform the traditional Simantonnayana with Vedic verses and a small havan, usually in the morning, before the women's celebration.`,
  abroad: `This ceremony adapts easily to a baby shower. Many families combine both: a short puja and blessings, then a relaxed gathering with friends of every background.`,
  prayers: [`ganesha`, `sarve-bhavantu`, `sarva-mangala`]
});

/* ---------------------------------------------------------------------- */
/* Birth and infancy                                                       */
/* ---------------------------------------------------------------------- */
rite({
  id: `birth`, deva: `नामकरण`, name: `Birth and Naming`, sanskrit: `Jatakarma and Namakarana`, stage: `infancy`, art: `cradle`,
  when: `At birth, then the 11th or 12th day`, where: `At home`, who: `Parents and elders, often with a priest`, length: `1 to 2 hours`,
  summary: `Welcoming a new soul into the family, and giving the child a name.`,
  intro: `<p><strong>Jatakarma</strong>, the birth rite, welcomes the newborn. Traditionally the father touches a little honey and ghee to the baby's lips with a gold ring or spoon, and whispers blessings for wisdom and a long life into the child's ear. In some families the sacred syllable Om is traced on the tongue with honey. It is the child's first taste of sweetness and of sacred sound.</p>
<p><strong>Namakarana</strong>, the naming ceremony, follows on the 11th or 12th day, or another auspicious day soon after, once mother and baby have rested. A name is not just a label. Hindus believe it shapes the child, so names are chosen with care: a name of God, a virtue, a river, or a word of beauty. Many families ask a priest to cast the baby's horoscope, which gives the auspicious first syllable based on the <em>nakshatra</em>, the lunar mansion, at the time of birth.</p>
<p>Many communities also celebrate <strong>Chhathi</strong> on the sixth night, when it is said that the child's destiny is written, and <strong>Barahi</strong> on the twelfth day, with a feast for family and friends.</p>`,
  need: [`Honey and ghee`, `A gold ring or small spoon`, `A plate of uncooked rice`, `New clothes for the baby`, `A decorated cradle`, `A lamp, flowers and incense`, `Kumkum and turmeric`, `Sweets to share`],
  steps: [
    [`Choose the day`, `The 11th or 12th day after birth is traditional. A priest can suggest an auspicious time and the first syllable of the name.`],
    [`Purify the home`, `Mother and baby bathe and wear fresh clothes, and the house is cleaned after the days of rest.`],
    [`Begin with Ganesha`, `Light a lamp, place a kalash and offer a prayer to Ganesha and the family deity.`],
    [`Write the name`, `A parent or elder writes the chosen name, often with Om before it, in a plate of rice using a gold ring.`],
    [`Whisper the name`, `Holding the baby, the father or an elder whispers the name three times into the child's right ear, then announces it to everyone.`],
    [`The cradle`, `In many homes the baby is then laid in a decorated cradle while the women sing lullabies and swing it gently.`],
    [`Blessings`, `Elders bless the child by touching their head, sprinkling a few grains of rice, and giving small gifts.`],
    [`Share the joy`, `Sweets are distributed and a meal is shared with family and friends.`]
  ],
  verse: [`पश्येम शरदः शतं जीवेम शरदः शतम्।`, `paśyema śaradaḥ śataṃ jīvema śaradaḥ śatam`, `May we see a hundred autumns; may we live a hundred autumns.`, `Yajur Veda 36.24`],
  customs: [
    [`Maharashtra`, `At the Barsa, the baby is placed in the cradle and the father's sister, the aatya, gives the name.`],
    [`Gujarat`, `The father's sister, the foi, traditionally names the baby and is honoured with gifts.`],
    [`South India`, `The naming is often held on the 11th, 12th or 16th day, with a puja to the family deity and the name chosen to match the birth star.`],
    [`Caribbean`, `In Trinidad, Guyana and Suriname, families celebrate the Chhatti and the Barahi with prayers and a feast of curry, rice and sweets.`]
  ],
  withPriest: `A priest can perform a short havan, cast the birth chart, suggest the first syllable of the name, and lead the Vedic blessings.`,
  abroad: `If a legal name must be registered before the ceremony, many families register it first and still hold the naming rite later, as a spiritual welcome.`,
  prayers: [`ganesha`, `gayatri`, `sarve-bhavantu`]
});

rite({
  id: `nishkramana`, deva: `निष्क्रमण`, name: `First Outing`, sanskrit: `Nishkramana`, stage: `infancy`, art: `sun-moon`,
  when: `Around the 3rd or 4th month`, where: `Outdoors, then a temple`, who: `Parents and grandparents`, length: `About an hour`,
  summary: `The baby's first step out into the world, to see the sun and visit the temple.`,
  intro: `<p>For the first weeks of life, a baby is kept safe and warm at home. <strong>Nishkramana</strong>, “going out,” marks the day the child is first taken outside to greet the wider world. It usually falls in the third or fourth month, when the baby is strong enough.</p>
<p>The child is shown the <strong>sun</strong>, source of light and life, and in many families the <strong>moon</strong> that evening, with prayers that the child will grow in brightness like the sun and in gentleness like the moon. Then comes the baby's first visit to the temple, for darshan and the blessings of the deity and the priest.</p>
<p>The rite is a gentle introduction to the world, and a reminder that the child belongs not only to the family but to the whole of creation.</p>`,
  need: [`New clothes for the baby`, `A small offering for the temple: flowers, fruit, sweets`, `A shawl or covering for the baby`, `A small pot of water for the sun offering`],
  steps: [
    [`Choose the day`, `Pick a pleasant morning in the third or fourth month. Many families wait until mother and baby have rested for about forty days.`],
    [`Prepare at home`, `Bathe and dress the baby, and offer a short prayer at the home shrine.`],
    [`Greet the sun`, `At sunrise, a parent carries the baby outside and gently turns them toward the sun, while the Gayatri Mantra or Om Suryaya Namah is chanted. Some families offer a little water to the sun.`],
    [`First darshan`, `Visit the temple. The priest may bless the baby, apply a tiny tilak and offer prasad to the family.`],
    [`Greet the moon`, `Some families show the baby the moon that evening, with a prayer for a calm and gentle nature.`],
    [`Celebrate`, `Return home and share sweets with family and neighbours.`]
  ],
  customs: [
    [`Many families`, `The first temple visit is made after the forty-day period of rest for mother and baby.`],
    [`South India`, `The baby may be taken to the family deity's temple, sometimes combined with the first feeding or haircut.`]
  ],
  withPriest: `At the temple, ask the priest for an archana in the baby's name and birth star. It takes only a few minutes.`,
  abroad: `Keep the baby warm and out of harsh sun or cold. The meaning lies in the greeting, not the length of the outing.`,
  prayers: [`surya-mantra`, `gayatri`, `shuklambaradharam`]
});

rite({
  id: `annaprashan`, deva: `अन्नप्राशन`, name: `First Solid Food`, sanskrit: `Annaprashana`, stage: `infancy`, art: `rice-bowl`,
  when: `About the 6th month`, where: `At home or at a temple`, who: `Parents, grandparents or a maternal uncle`, length: `1 to 2 hours`,
  summary: `The baby's first taste of grain, blessed as a gift from God.`,
  intro: `<p><strong>Annaprashana</strong>, “feeding of grain,” is the baby's first taste of solid food. It is usually held around the sixth month, when the child is ready to eat more than milk. Traditionally boys have it in an even month, often the sixth or eighth, and girls in an odd month, the fifth or seventh.</p>
<p>The first food is usually a little <strong>kheer</strong> or <strong>payasam</strong>, rice cooked in milk with sugar, first offered to God and then fed to the baby, often with a silver spoon. In Hindu thought, food is sacred, <em>annam brahma</em>, “food is Brahman,” and this rite teaches that every meal is a gift to be received with gratitude.</p>
<p>A favourite part of the day comes afterwards: the baby is placed before a few objects, such as a book, a pen, money, jewellery and a little soil, and the family watches with delight to see which one the child reaches for, as a playful hint of what life holds.</p>`,
  need: [`A small silver bowl and spoon, if you have them`, `Kheer or soft rice with ghee`, `New clothes for the baby`, `A lamp, flowers and incense`, `Objects for the choosing game: a book, a pen, a coin, jewellery, soil`, `Sweets for guests`],
  steps: [
    [`Prepare the food`, `Cook a small amount of kheer or soft rice. Make it plain and safe for a baby.`],
    [`Begin with Ganesha`, `Light a lamp and offer a prayer to Ganesha and the family deity.`],
    [`Offer it to God`, `Place the food before the deity with a short prayer such as Annapurne Sadapurne, so that it becomes prasad.`],
    [`The first spoonful`, `A grandparent, a parent or, in many families, the maternal uncle feeds the baby a tiny first taste.`],
    [`Blessings`, `Each elder offers a taste in turn, with blessings for health and strength.`],
    [`The choosing game`, `Place the objects in front of the baby and see which one they pick up first.`],
    [`Share a meal`, `Family and guests enjoy a festive meal together.`]
  ],
  verse: [`अन्नपूर्णे सदापूर्णे शङ्करप्राणवल्लभे।`, `annapūrṇe sadāpūrṇe śaṅkara-prāṇa-vallabhe`, `O Annapurna, ever full, beloved of Shiva: grant us the gift of food.`, `Prayer to the goddess of nourishment`],
  customs: [
    [`Bengal`, `Mukhe Bhaat is a grand feast; the baby is offered a taste of many dishes, and the maternal uncle feeds the first bite.`],
    [`Kerala`, `Choroonu is often held at the Guruvayur temple, where hundreds of babies are fed their first rice before Krishna.`],
    [`North India`, `Annaprashan is usually held at home with a puja, kheer and a family meal.`]
  ],
  withPriest: `A priest can chant Vedic verses for health and add a short havan before the first feeding.`,
  abroad: `Check with your doctor about when your baby is ready for solids. The rite can be held on any day close to that time.`,
  prayers: [`annapurna`, `brahmarpanam`, `ganesha`]
});

rite({
  id: `karnavedha`, deva: `कर्णवेध`, name: `Ear Piercing`, sanskrit: `Karnavedha`, stage: `infancy`, art: `earrings`,
  when: `Between 6 months and 5 years`, where: `At home or at a temple`, who: `A trained piercer, with the family`, length: `About an hour`,
  summary: `Piercing the ears, to open them to sacred sound.`,
  intro: `<p><strong>Karnavedha</strong>, “piercing of the ears,” is one of the traditional samskaras of childhood. It is often performed in the first, third or fifth year, and in many South Indian families together with the first haircut.</p>
<p>The rite has both a spiritual and a practical meaning. The ears are opened, symbolically, to receive sacred sound: the names of God, the teachings of the scriptures and the words of the guru. Traditionally it was also believed to support health, and the earrings themselves are a protective ornament.</p>
<p>The right ear is usually pierced first for boys and the left for girls, and the child is given small gold earrings. Families make the day festive, so that the little one remembers the treats more than the pinch.</p>`,
  need: [`Small gold earrings or studs`, `A trained piercer with sterile equipment`, `A lamp and flowers`, `Turmeric or sandalwood paste`, `A sweet and a favourite toy for the child`],
  steps: [
    [`Choose the day`, `Pick an auspicious day, perhaps with the help of a priest or the family calendar.`],
    [`Pray first`, `Offer a short prayer to Ganesha and the family deity, asking for the child's wellbeing.`],
    [`Comfort the child`, `The child sits in a parent's lap, often with a sweet in hand or a favourite song playing.`],
    [`The piercing`, `A trained piercer, using sterile equipment, pierces the ears and places the earrings.`],
    [`Blessings and treats`, `Elders bless the child, and everyone shares sweets.`],
    [`Care afterwards`, `Keep the ears clean as the piercer advises until they heal.`]
  ],
  customs: [
    [`South India`, `Often performed at the family deity's temple, together with the first haircut, with the uncle holding the child.`],
    [`Many families`, `A goldsmith traditionally pierced the ears with a fine gold wire; today trained professionals are usually preferred.`]
  ],
  withPriest: `A priest can recite blessings and a short prayer, but the piercing itself should be done by a trained professional.`,
  abroad: `Choose a licensed piercer or clinic. The prayers and blessings can be done at home before or after.`,
  prayers: [`ganesha`, `shuklambaradharam`]
});

rite({
  id: `mundan`, deva: `चूडाकरण`, name: `First Haircut`, sanskrit: `Chudakarana (Mundan)`, stage: `infancy`, art: `hair-offering`,
  when: `In the 1st or 3rd year`, where: `At home, a temple or a holy river`, who: `A barber, with parents and a priest`, length: `1 to 2 hours`,
  summary: `Shaving the first hair, a fresh start for the growing child.`,
  intro: `<p><strong>Chudakarana</strong>, widely known as <strong>Mundan</strong>, is the child's first haircut. The baby's hair, which grew in the womb, is shaved off completely, usually in the first or third year, as odd years are considered auspicious.</p>
<p>The rite is understood in several ways. It is a cleansing, letting go of any impressions carried from past lives. It is a prayer for healthy, strong hair and a long life. And it marks the end of babyhood, as the child steps into a new stage. Traditionally a small tuft, the <strong>shikha</strong>, is left at the crown of the head, which is considered especially sacred.</p>
<p>Many families perform mundan at a famous temple or a holy river: Tirupati in Andhra Pradesh, where devotees of every age offer their hair to Lord Venkateswara, or at Haridwar on the Ganga. The hair is offered to the deity or to the river as a gift.</p>`,
  need: [`A barber or trusted person with a clean razor`, `Water, and turmeric or sandalwood paste`, `A cloth to collect the hair`, `New clothes for the child`, `A lamp, flowers and sweets`],
  steps: [
    [`Choose the day and place`, `Pick an auspicious date and decide whether to hold it at home, a temple or a river.`],
    [`Pray`, `Offer prayers to Ganesha and the family deity, often with a short havan.`],
    [`Prepare the child`, `The child sits on a parent's lap, often facing east or toward the deity. The maternal uncle sometimes holds the child.`],
    [`The first cut`, `The father or priest may cut the first lock of hair with a prayer, then the barber gently shaves the head, sometimes leaving the shikha.`],
    [`Soothe the scalp`, `Apply turmeric or sandalwood paste to cool and protect the skin.`],
    [`Offer the hair`, `Collect the hair in a cloth and offer it at the temple, or float it in a river.`],
    [`Bath and blessings`, `The child bathes, wears new clothes and is blessed by the elders. Sweets are shared.`]
  ],
  customs: [
    [`Tirupati`, `Families from all over the world offer a child's first hair to Lord Venkateswara.`],
    [`North India`, `Mundan is often held at Haridwar, Varanasi or another holy place on the Ganga.`],
    [`South India`, `It is frequently combined with the ear piercing, at the family deity's temple.`],
    [`Caribbean`, `The mundan is still kept by many Indo-Caribbean families, often at the mandir with a priest.`]
  ],
  withPriest: `Many temples offer a mundan service with a barber and a priest. At home, a priest can perform the havan and the first cut.`,
  abroad: `Some families visit India or a major temple for the mundan; others hold it at their local mandir and later offer the hair at a river.`,
  prayers: [`ganesha`, `ganga-snana`]
});

/* ---------------------------------------------------------------------- */
/* Childhood and youth                                                     */
/* ---------------------------------------------------------------------- */
rite({
  id: `vidyarambha`, deva: `विद्यारम्भ`, name: `Beginning to Learn`, sanskrit: `Vidyarambha`, stage: `youth`, art: `rice-om`,
  when: `Age 2 to 5; often on Vijayadashami or Vasant Panchami`, where: `At home, a temple or a school`, who: `A parent, grandparent, teacher or priest`, length: `About an hour`,
  summary: `Writing the first letters, with the blessing of Saraswati.`,
  intro: `<p><strong>Vidyarambha</strong>, “the beginning of learning,” marks a child's first step into education. It is usually held between the ages of two and five, and it is one of the sweetest of all the rites: a small child, sitting in an elder's lap, writes their first letters in a plate of rice.</p>
<p>The ceremony is dedicated to <strong>Saraswati</strong>, goddess of knowledge, and to <strong>Ganesha</strong>, lord of beginnings. Its message is that learning is sacred: every letter is a form of the divine, and the teacher, the guru, is to be honoured like God.</p>
<p>Two days of the year are especially loved for it. In the South, and above all in Kerala, children begin on <strong>Vijayadashami</strong>, the last day of Navaratri. In the North and East, many choose <strong>Vasant Panchami</strong>, Saraswati's spring festival.</p>`,
  need: [`A plate of uncooked rice`, `A gold ring, and a little honey`, `A new slate, notebook or book`, `Images of Saraswati and Ganesha`, `A lamp, flowers and sweets`, `A small gift for the teacher (guru dakshina)`],
  steps: [
    [`Choose the day`, `Vijayadashami, Vasant Panchami, or another auspicious morning.`],
    [`Worship Saraswati and Ganesha`, `Place books, pens and instruments before the deities, light a lamp, and say Saraswati Namastubhyam.`],
    [`Sit with the teacher`, `The child sits on the lap of the guru, a priest, a grandparent or a parent.`],
    [`The first letters`, `Holding the child's index finger, the teacher traces Om, or Om Hari Shri Ganapataye Namah, or the first letter of the alphabet, in the rice.`],
    [`Letters on the tongue`, `In Kerala, the teacher gently writes a letter on the child's tongue with a gold ring dipped in honey, so that learning will be sweet.`],
    [`A new book`, `The child receives a slate or a new book, and bows to the teacher, offering a small gift.`],
    [`Celebrate`, `Share sweets, and let the child scribble and play with the rice.`]
  ],
  verse: [`सरस्वति नमस्तुभ्यं वरदे कामरूपिणि।`, `sarasvati namastubhyaṃ varade kāmarūpiṇi`, `Salutations to you, Saraswati, giver of boons: as I begin my studies, may I always succeed.`, `Prayer before study`],
  customs: [
    [`Kerala`, `Ezhuthinu Iruthal on Vijayadashami draws thousands of children to temples such as the Saraswati temple at Panachikkadu.`],
    [`Andhra Pradesh and Telangana`, `Aksharabhyasam is often held at the Saraswati temple at Basar.`],
    [`Bengal and the North`, `Hate Khori, “chalk in hand,” is celebrated on Saraswati Puja, Vasant Panchami.`]
  ],
  withPriest: `Many temples hold a vidyarambha ceremony on Vijayadashami, with a priest or teacher guiding each child.`,
  abroad: `Hold it at home on the day your child begins nursery or school, and keep the first slate or page as a treasured memento.`,
  prayers: [`saraswati`, `ya-kundendu`, `guru`, `sahana`],
  links: [[`Vasant Panchami`, `#/festival/vasant-panchami`], [`Navaratri and Vijayadashami`, `#/festival/navaratri`]]
});

rite({
  id: `upanayana`, deva: `उपनयन`, name: `Sacred Thread`, sanskrit: `Upanayana`, stage: `youth`, art: `sacred-thread`,
  when: `Traditionally between ages 7 and 12`, where: `At home, a hall or a temple, around a sacred fire`, who: `A priest, with the father or a guru`, length: `Half a day`,
  summary: `Receiving the sacred thread and the Gayatri Mantra, and becoming a student.`,
  intro: `<p><strong>Upanayana</strong> means “leading near”: bringing the child close to the guru, to begin the study of sacred knowledge. It is one of the most important samskaras, and the child is called <em>dvija</em>, “twice-born,” because this is understood as a second, spiritual birth.</p>
<p>At its heart are two gifts. The first is the <strong>yajnopavita</strong>, the sacred thread: three strands, each made of three fine threads, joined by a special knot, the <em>brahma granthi</em>. It is worn over the left shoulder and across the body, and its three strands are often said to stand for three debts we owe: to the gods, to the sages and to our ancestors. The second gift is the <strong>Gayatri Mantra</strong>, whispered by the father or guru into the child's ear, often under a covering cloth, as the start of a lifelong practice.</p>
<p>Traditionally the rite was for boys of certain communities, but in Vedic times some girls also received it, and many families and reform movements today offer it, or a similar initiation, to children of any gender.</p>`,
  need: [`The sacred thread (yajnopavita)`, `New clothes: a dhoti and an upper cloth`, `A staff (danda) and a girdle of grass (mekhala), in traditional rites`, `Materials for the havan: ghee, wood, rice, sesame`, `A lamp, flowers, fruits and sweets`, `A small bowl for the alms (bhiksha)`, `Gifts for the priest and guests`],
  steps: [
    [`Preparation`, `The day before, the family performs a Ganesha puja and invites the ancestors' blessings. In many families the child's head is shaved.`],
    [`Bath and new clothes`, `On the morning of the rite, the child bathes and wears new clothes, often after a last meal with the mother as a little child.`],
    [`The sacred fire`, `The priest lights the havan, and offerings are made with Vedic verses.`],
    [`Receiving the thread`, `The yajnopavita is placed over the child's left shoulder while the priest chants the mantra for the sacred thread.`],
    [`The Gayatri Mantra`, `Under a cloth, the father or guru teaches the child the Gayatri Mantra, line by line. This is called brahmopadesha.`],
    [`Staff and vows`, `The child receives a staff and takes the vows of a student: to study, to be truthful, and to respect teachers and elders.`],
    [`Asking for alms`, `The child approaches the mother first, saying “Bhavati bhiksham dehi,” “Lady, please give alms,” and then other women of the family, learning humility and gratitude.`],
    [`Blessings`, `The elders bless the new student, and everyone shares a festive meal.`]
  ],
  verse: [`ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं भर्गो देवस्य धीमहि धियो यो नः प्रचोदयात्॥`, `oṃ bhūr bhuvaḥ svaḥ tat savitur vareṇyaṃ bhargo devasya dhīmahi dhiyo yo naḥ pracodayāt`, `We meditate on the glorious light of the divine Sun. May it inspire our minds.`, `The Gayatri Mantra, Rig Veda 3.62.10`],
  customs: [
    [`Tamil Nadu and Kerala`, `The poonal ceremony; the thread is renewed each year on Avani Avittam, the full moon of Shravana.`],
    [`Maharashtra`, `The munj, often followed by a playful moment when the boy pretends to set off for Kashi to study.`],
    [`Gujarat and the North`, `The janoi or janeu ceremony, usually with a large family gathering.`],
    [`Bengal`, `The paita ceremony, after which the boy stays indoors for three days in study and quiet.`]
  ],
  withPriest: `This rite is almost always led by a priest, because of the many Vedic recitations. Ask in advance about the date, the items needed and the role of each family member.`,
  abroad: `Many temples outside India hold group upanayana ceremonies. Afterwards, help the child keep up a simple daily practice, such as saying the Gayatri Mantra each morning.`,
  prayers: [`gayatri`, `guru`, `sahana`],
  links: [[`Course: The Sacred Texts`, `#/academy/vedas`]]
});

rite({
  id: `coming-of-age`, deva: `ऋतुशुद्धि`, name: `Coming of Age`, sanskrit: `Keshanta, Ritu Shuddhi and Samavartana`, stage: `youth`, art: `lotus`,
  when: `Around the teenage years, and at the end of studies`, where: `At home or a family hall`, who: `The family, often with a priest`, length: `A few hours`,
  summary: `Celebrating the step from childhood into young adulthood.`,
  intro: `<p>The ancient lists of samskaras include rites for the passage from child to young adult. <strong>Keshanta</strong>, “the end of the hair,” was a young man's first shave, around the age of sixteen. <strong>Samavartana</strong>, “returning home,” marked the end of studies: the student took a ceremonial bath, thanked the teacher, and returned home ready to enter adult life. It is the ancestor of every graduation.</p>
<p>In many communities, especially in South India, a girl's coming of age is also celebrated, with a gathering of family, new clothes, gifts and blessings. In Tamil Nadu this is called <strong>Manjal Neerattu Vizha</strong>, the turmeric bath ceremony; in Andhra Pradesh and Telangana the <strong>Langa Voni</strong> or <strong>half-saree ceremony</strong>, when a girl first wears a half-saree. In Odisha, the festival of Raja celebrates womanhood every summer.</p>
<p>These rites say the same thing in different ways: growing up is to be honoured, not hidden. A young person is welcomed with love into a new stage of responsibility, and reminded that the family stands behind them. Many modern families mark this moment for any child, with a simple puja, blessings and a celebration.</p>`,
  need: [`New traditional clothes`, `Flowers, fruits and sweets`, `Turmeric and kumkum`, `A lamp and incense`, `Gifts from the family`, `A meal for guests`],
  steps: [
    [`Choose the moment`, `A birthday, the end of school or university, or the traditional time in your community.`],
    [`Puja`, `Begin with Ganesha, and offer prayers to the family deity and to Saraswati for wisdom.`],
    [`New clothes`, `The young person wears new traditional clothes, often given by the maternal uncle or grandparents.`],
    [`Blessings`, `Elders apply tilak, offer akshata and share words of advice for the years ahead.`],
    [`Gratitude`, `The young person bows to parents and teachers and thanks them, as the graduating student once did.`],
    [`Celebrate`, `A meal and a gathering with family and friends.`]
  ],
  verse: [`असतो मा सद्गमय। तमसो मा ज्योतिर्गमय।`, `asato mā sad gamaya, tamaso mā jyotir gamaya`, `Lead me from the unreal to the real; lead me from darkness to light.`, `Brihadaranyaka Upanishad 1.3.28`],
  customs: [
    [`Tamil Nadu`, `Manjal Neerattu Vizha, with a turmeric bath, a silk sari and a large family gathering.`],
    [`Andhra Pradesh and Telangana`, `The Langa Voni or half-saree ceremony, a joyful milestone for girls.`],
    [`Odisha`, `Raja Parba, a festival celebrating womanhood and the earth, with swings, songs and sweets.`],
    [`Many families today`, `A puja and blessings at graduation, echoing the ancient Samavartana.`]
  ],
  withPriest: `A priest can perform a short puja or havan. For Samavartana-style graduation blessings, a simple home puja is enough.`,
  abroad: `Choose what feels right for your family and your child. A quiet blessing from the grandparents can mean as much as a big celebration.`,
  prayers: [`saraswati`, `asato-ma`, `sarva-mangala`]
});

/* ---------------------------------------------------------------------- */
/* Adult life                                                              */
/* ---------------------------------------------------------------------- */
rite({
  id: `vivaha`, deva: `विवाह`, name: `Wedding`, sanskrit: `Vivaha`, stage: `adult`, art: `mandap`,
  when: `On an auspicious date (muhurat)`, where: `A mandap: a decorated canopy`, who: `A priest, with both families`, length: `The ceremony takes 2 to 4 hours; celebrations last days`,
  summary: `Two families, two souls, one sacred fire and seven steps.`,
  intro: `<p><strong>Vivaha</strong> is the most celebrated of all the samskaras. A Hindu wedding is not only a contract between two people. It unites two families and joins the couple as partners in dharma, who will support each other in every one of life's four goals.</p>
<p>Customs vary enormously across regions and communities, but almost every Hindu wedding shares a few sacred moments. <strong>Agni</strong>, the sacred fire, is the divine witness. The couple's hands are joined and their garments tied together. They walk around the fire, and they take the <strong>saptapadi</strong>, the seven steps, each with a promise. After the seventh step, they are married.</p>
<p>The seven vows are often explained as prayers for nourishment, strength, prosperity, happiness, children, long life together, and above all lifelong friendship.</p>`,
  need: [`An auspicious date (muhurat) from a priest`, `A mandap with four pillars and a canopy`, `A havan kund and materials for the fire`, `Garlands (jaimala) for the bride and groom`, `A kalash, coconut, rice, flowers, kumkum and turmeric`, `Puffed rice (laja) for the fire offering`, `Mangalsutra and sindoor, or the customs of your community`, `Clothes and gifts for both families`],
  phases: [
    { title: `Before the wedding`, steps: [
      [`Engagement`, `The families formally agree to the match, often with a Roka, Sagai or Nischitartham ceremony, prayers and an exchange of rings or gifts.`],
      [`Ganesha puja`, `A puja to Ganesha, and often to the family deities and ancestors, asks for the wedding to go smoothly.`],
      [`Haldi`, `Turmeric paste is applied to the bride and groom by their families, for a glow and for blessings.`],
      [`Mehndi and sangeet`, `The bride's hands and feet are decorated with henna, and the families gather for music and dance.`]
    ] },
    { title: `The ceremony`, steps: [
      [`The arrival`, `The groom arrives in a joyful procession, the baraat, and is welcomed by the bride's family.`],
      [`Jaimala`, `The bride and groom exchange flower garlands, accepting each other.`],
      [`Kanyadaan`, `The bride's parents place her hand in the groom's, entrusting her to him, a deeply emotional moment.`],
      [`Joining of hands`, `In Panigrahana or Hasta Milap, the groom holds the bride's hand and promises to care for her, and the priest ties the ends of their garments together.`],
      [`Offerings to the fire`, `The couple make offerings into the sacred fire. In the laja homa, the bride's brother pours puffed rice into her hands for the offering.`],
      [`Mangal pheras`, `The couple walk around the fire, usually four or seven times, each round a prayer for one of life's aims.`],
      [`Saptapadi`, `They take seven steps together, each with a vow. With the seventh, they become husband and wife.`],
      [`Sindoor and mangalsutra`, `The groom applies sindoor in the parting of the bride's hair and ties the mangalsutra, the sacred necklace of marriage.`],
      [`Blessings`, `The couple bow to their elders and receive blessings, often showered with flowers and rice.`]
    ] },
    { title: `After the ceremony`, steps: [
      [`Vidaai`, `A tearful farewell as the bride leaves her parents' home, often throwing rice behind her as a blessing for the home she leaves.`],
      [`Welcome home`, `At the groom's home, the bride gently tips over a pot of rice at the threshold with her right foot and steps in, bringing prosperity.`],
      [`Games and reception`, `Light-hearted games, such as finding a ring in a bowl of milky water, help the new family bond.`]
    ] }
  ],
  verse: [`सखा सप्तपदा भव।`, `sakhā saptapadā bhava`, `With these seven steps, become my friend.`, `Words of the seventh step`],
  customs: [
    [`Bengal`, `In Shubho Drishti, the bride hides her face behind betel leaves until the couple's first look; the groom applies sindoor in Sindoor Daan.`],
    [`South India`, `In Kashi Yatra, the groom pretends to leave to become a scholar-ascetic until the bride's father persuades him to marry; the couple sit on a swing (oonjal); the mangalsutra is tied with three knots.`],
    [`Gujarat`, `The couple usually take four pheras, for dharma, artha, kama and moksha, and the maternal uncle brings gifts, the mameru.`],
    [`Punjab`, `The bride wears red and ivory chooda bangles, with golden kaleere hanging from them.`],
    [`Maharashtra`, `A cloth, the antarpat, is held between the couple until the mangalashtak verses are sung.`],
    [`Caribbean`, `In Trinidad, Guyana and Suriname, women gather for the Matikor, a joyful pre-wedding ceremony honouring Mother Earth, and the laawa, puffed rice, is offered with the bride's brother.`]
  ],
  withPriest: `A priest leads the Vedic recitations and guides the families through each step. Many priests offer shorter ceremonies with explanations in English for guests of every background.`,
  abroad: `If you need a civil ceremony for legal reasons, it can be held separately. A printed or projected guide to the rituals helps guests follow and share in the meaning.`,
  prayers: [`ganesha`, `sarva-mangala`, `sarve-bhavantu`, `jagdish`]
});

rite({
  id: `griha-pravesh`, deva: `गृहप्रवेश`, name: `Housewarming`, sanskrit: `Griha Pravesha`, stage: `adult`, art: `threshold`,
  when: `On an auspicious day before moving in`, where: `The new home`, who: `The family, often with a priest`, length: `2 to 3 hours`,
  summary: `Blessing a new home and inviting peace and prosperity inside.`,
  intro: `<p><strong>Griha Pravesha</strong>, “entering the home,” is the ceremony for a new house. In Hindu thought, a home is not just a building but a living space with its own energies, and the place where the family's daily worship happens. Before living in it, the family purifies it, honours the deities of the land and the directions, and invites Lakshmi, prosperity, and Ganesha, protection, inside.</p>
<p>The texts describe three kinds: <em>apoorva</em>, entering a brand-new home; <em>sapoorva</em>, returning to a home after a long absence; and <em>dvandvah</em>, re-entering after renovation or after a disaster. The same spirit guides all three.</p>
<p>The most famous custom is boiling milk in the new kitchen until it overflows: a sign that the home will always have more than enough.</p>`,
  need: [`An auspicious date and time from the calendar or a priest`, `A kalash with water, mango leaves and a coconut`, `A toran of mango leaves for the door`, `Rangoli colours`, `Milk, rice and a new pot for the kitchen`, `Images of Ganesha and Lakshmi`, `A lamp, incense, flowers and fruits`, `Materials for a havan, if a priest is performing one`],
  steps: [
    [`Prepare the house`, `Clean every room, hang a toran of mango leaves over the main door, and draw a rangoli at the entrance. Many draw an auspicious swastika or Om in kumkum on the door.`],
    [`Break a coconut`, `Before entering, a coconut is broken at the threshold, offering the ego and asking for obstacles to be removed.`],
    [`Enter with the right foot`, `The family steps inside right foot first, the woman of the house often carrying the kalash, or an image of Lakshmi.`],
    [`Vastu and Ganesha puja`, `A priest may perform the Vastu Shanti puja and a havan, honouring the spirit of the land and the deities of the eight directions.`],
    [`Boil the milk`, `Boil milk in a new pot on the new stove until it overflows. Then cook a little kheer or sweet rice as the first food of the home.`],
    [`Bless every room`, `Carry a lamp through the house, sprinkle holy water in each room, and let the sound of a bell or conch fill it.`],
    [`Share a meal`, `Offer food to the priest, family and friends. Traditionally the family sleeps in the new home that first night.`]
  ],
  verse: [`समुद्रवसने देवि पर्वतस्तनमण्डिते।`, `samudra-vasane devi parvata-stana-maṇḍite`, `O Goddess Earth, clothed in oceans and adorned with mountains: forgive us for touching you with our feet.`, `Prayer to Mother Earth`],
  customs: [
    [`South India`, `Many families bring a cow and calf into the house first, a symbol of Lakshmi and abundance.`],
    [`North India`, `A Satyanarayan Katha is often held in the new home soon after moving in.`],
    [`Gujarat and Rajasthan`, `Kumkum handprints and an auspicious swastika are made at the entrance.`]
  ],
  withPriest: `A priest can perform the Vastu Shanti, Navagraha and Ganesha pujas with a havan. Ask how much space the fire needs, and open the windows.`,
  abroad: `In apartments, use a small electric lamp or a sealed havan kund, and check fire-safety rules. Boiling milk and a lamp-lit prayer keep the heart of the ceremony.`,
  prayers: [`ganesha`, `mahalakshmi`, `bhumi`, `jagdish`]
});

rite({
  id: `shashtipurti`, deva: `षष्टिपूर्ति`, name: `Sixtieth Birthday`, sanskrit: `Shashtipurti`, stage: `adult`, art: `calendar-wheel`,
  when: `The 60th birthday, by the Hindu calendar`, where: `At home, a hall or a temple`, who: `The couple's children, with a priest`, length: `Half a day`,
  summary: `Honouring a long life: the completion of a full cycle of sixty years.`,
  intro: `<p><strong>Shashtipurti</strong>, “the completion of sixty,” celebrates a person's sixtieth birthday. The traditional Hindu calendar names its years in a cycle of sixty, so at sixty a person has lived through every year of the cycle, and a new one begins. It marks the step from active family life toward a quieter, more spiritual stage.</p>
<p>The celebration is usually arranged by the children, as a way to thank their parents. Often the couple renew their wedding vows, in a ceremony that echoes their own wedding, surrounded by children and grandchildren. Prayers are offered for health and a long life, especially to Shiva in his healing form, with the <strong>Mahamrityunjaya Mantra</strong>.</p>
<p>Further milestones follow in some communities: the seventieth birthday, and the <strong>Sathabhishekam</strong> around the age of eighty, when a person is said to have seen a thousand full moons.</p>`,
  need: [`A date based on the birth star or birthday`, `New clothes for the couple`, `Garlands, a kalash, flowers and fruits`, `Materials for a havan`, `A mangalsutra or ring, if vows are renewed`, `Gifts and a meal for guests`],
  steps: [
    [`Plan together`, `The children consult a priest to set the date, usually on the birth star closest to the sixtieth birthday.`],
    [`Prayers for long life`, `The day begins with Ganesha puja, a kalash puja and a havan, often with the Mahamrityunjaya Mantra.`],
    [`Sacred bath`, `In many families, water from the kalash is poured over the couple as a blessing.`],
    [`Renewal of vows`, `The couple exchange garlands, and the husband ties a new mangalsutra or the couple exchange rings, as at their wedding.`],
    [`Honouring the parents`, `Children and grandchildren bow to the couple and receive their blessings, and often wash their feet in gratitude.`],
    [`Celebrate`, `Family and friends share a feast and stories from sixty years of life.`]
  ],
  verse: [`ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्।`, `oṃ tryambakaṃ yajāmahe sugandhiṃ puṣṭi-vardhanam`, `We worship the three-eyed Lord, fragrant, who nourishes and strengthens all.`, `The Mahamrityunjaya Mantra, Rig Veda 7.59.12`],
  customs: [
    [`Tamil Nadu`, `Shashtiabdapoorthi, often held at a temple such as Thirukadaiyur, famous for prayers for long life.`],
    [`Andhra Pradesh and Karnataka`, `Shashtipurti with a renewal of the wedding rites, followed by Bhimaratha Shanti at seventy.`],
    [`North India`, `Milestone birthdays are often marked with a Satyanarayan Katha or a havan at home.`]
  ],
  withPriest: `A priest can perform the Ayushya homa for long life and guide the renewal of vows.`,
  abroad: `This is a lovely occasion to gather the whole family, near and far. Share a recorded message from relatives who can't attend.`,
  prayers: [`mahamrityunjaya`, `sarve-bhavantu`, `jagdish`]
});

/* ---------------------------------------------------------------------- */
/* The end of life and beyond                                              */
/* ---------------------------------------------------------------------- */
rite({
  id: `antyeshti`, deva: `अन्त्येष्टि`, name: `Last Rites`, sanskrit: `Antyeshti`, stage: `end`, art: `lamp-river`,
  when: `At death, and in the following 13 days`, where: `Home, a crematorium and a river`, who: `The family, led by a priest`, length: `Rites continue for 10 to 13 days`,
  summary: `Honouring the departed and helping the soul on its journey.`,
  intro: `<p><strong>Antyeshti</strong>, “the last sacrifice,” is the final samskara. Hindus believe that the soul, the Atman, does not die; it leaves the worn-out body and continues its journey. The last rites return the body to the five elements, help the soul move on peacefully, and give the family a way to grieve, remember and be supported by the community.</p>
<p>Fire is central. Just as offerings are made into the sacred fire throughout life, at the end the body itself is offered to Agni. Cremation is the usual practice, though infants, young children and some holy people are traditionally buried.</p>
<p>A period of mourning follows, usually ten to thirteen days, ending with the <strong>shraddha</strong> rites, in which the departed is honoured and joins the ancestors. The family then continues to remember them every year.</p>`,
  need: [`Ganga water (Ganga jal) and tulsi leaves`, `Clean clothes or a white shroud`, `Flowers and garlands`, `Sandalwood paste and ghee`, `A lamp to keep burning in the home`, `Contact details for a priest and a funeral home`],
  phases: [
    { title: `At the time of death`, steps: [
      [`Gather with love`, `If possible, family gather around and chant the name of God, read from the Bhagavad Gita, or play the Mahamrityunjaya Mantra or a favourite bhajan.`],
      [`Ganga water and tulsi`, `A few drops of Ganga water and a tulsi leaf are placed in the mouth of the dying or the departed.`],
      [`A lamp`, `A lamp is lit near the head and kept burning, and the body may be laid with the head toward the south.`]
    ] },
    { title: `The funeral`, steps: [
      [`Preparation`, `The body is washed, dressed in clean clothes, and adorned with sandalwood, flowers and tilak. Married women are often dressed in red; others in white.`],
      [`The procession`, `Family and friends carry the body, chanting “Ram naam satya hai,” “the name of Rama is truth.”`],
      [`Cremation`, `The chief mourner, often the eldest son but any close family member may serve, walks around the pyre and lights it with prayers. In crematoria abroad, the family may start the cremation themselves.`],
      [`The ashes`, `The ashes are collected and later immersed in a holy river or the sea, with prayers.`]
    ] },
    { title: `The days of mourning`, steps: [
      [`A quiet home`, `For ten to thirteen days, the family keeps the home simple: a lamp burns, festivities are paused, and simple food is eaten. Many read the Garuda Purana or the Gita.`],
      [`Shraddha and joining the ancestors`, `Around the 10th to 13th day, the shraddha is performed with rice-ball offerings (pinda), and the departed is united with the ancestors.`],
      [`The thirteenth day`, `The mourning ends with a gathering, a meal and acts of charity in the departed's name. Some families then hold a monthly remembrance for the first year.`]
    ] }
  ],
  verse: [`न जायते म्रियते वा कदाचिन् नायं भूत्वा भविता वा न भूयः।`, `na jāyate mriyate vā kadācin nāyaṃ bhūtvā bhavitā vā na bhūyaḥ`, `It is not born, nor does it ever die. Having been, it will never cease to be.`, `Bhagavad Gita 2.20`],
  customs: [
    [`Varanasi`, `Many Hindus hope to be cremated at Manikarnika Ghat, believing that death in Kashi brings liberation.`],
    [`South India`, `A large part of the rites takes place at home, with the chief mourner guided closely by the priest.`],
    [`Caribbean and diaspora`, `Cremations are often held at open-air cremation sites or crematoria, and ashes are scattered at sea or carried to India.`]
  ],
  withPriest: `A priest guides the family through every stage, from the prayers at home to the cremation and the shraddha. Most funeral homes can arrange a Hindu priest.`,
  abroad: `Contact a funeral director early and ask about a Hindu service, viewing at home, and a crematorium that allows the family to be present. Ashes can be scattered at sea or sent to India for immersion.`,
  prayers: [`mahamrityunjaya`, `rama-rameti`, `asato-ma`],
  links: [[`Bhagavad Gita, chapter 2`, `#/read/gita/2`], [`Pitru Paksha`, `#/festival/pitru-paksha`]]
});

rite({
  id: `shraddha`, deva: `श्राद्ध`, name: `Remembering the Ancestors`, sanskrit: `Shraddha and Tarpana`, stage: `end`, art: `sun-arc`,
  when: `Each year on the day of passing, and in Pitru Paksha`, where: `At home, a river or a holy place`, who: `Children and descendants, often with a priest`, length: `1 to 3 hours`,
  summary: `Honouring those who came before, with water, food and gratitude.`,
  intro: `<p><strong>Shraddha</strong> comes from <em>shraddha</em>, faith or sincerity: it is an act of loving faith toward one's ancestors, the <strong>pitrs</strong>. Hindus believe that our ancestors remain connected to us, and that remembering them with offerings and prayers brings them peace and brings blessings to the family.</p>
<p>Shraddha is performed every year on the lunar day, the tithi, on which a parent or grandparent passed away. All ancestors are also remembered together during <strong>Pitru Paksha</strong>, the fortnight of the ancestors in early autumn, which ends on <strong>Mahalaya Amavasya</strong>.</p>
<p>The rites include <strong>tarpana</strong>, offering water mixed with black sesame seeds, and <strong>pinda daan</strong>, offering balls of rice. Food is shared with crows, cows and dogs, and the needy are fed, because what is given in the ancestors' name is believed to reach them.</p>`,
  need: [`Water, black sesame seeds and kusha grass`, `Cooked rice for the pinda offerings`, `A photograph of the departed`, `A lamp, incense and white flowers`, `A simple vegetarian meal, including dishes they loved`, `Food or donations for those in need`],
  steps: [
    [`Find the date`, `Find the tithi of passing in the Hindu calendar, or choose a day in Pitru Paksha.`],
    [`Prepare`, `Bathe, wear clean clothes, and set up a photograph of the departed with a lamp and flowers.`],
    [`Tarpana`, `Facing south, pour water mixed with black sesame through the fingers, three times for each ancestor, saying their names.`],
    [`Pinda offerings`, `With a priest, offer balls of cooked rice to the ancestors, with prayers for their peace.`],
    [`Feed others`, `Set aside food for crows and other creatures, then feed a priest, guests or people in need.`],
    [`Remember`, `Share stories and memories of the departed, and offer a quiet prayer of thanks.`]
  ],
  customs: [
    [`Gaya`, `Pinda daan at Gaya in Bihar, on the river Phalgu, is considered especially meritorious.`],
    [`Bengal`, `On Mahalaya, families offer tarpan at the river at dawn, as the radio plays the famous Mahishasura Mardini.`],
    [`Many families`, `Ancestors are remembered on every Amavasya, the new moon.`]
  ],
  withPriest: `A priest can perform the full shraddha with pinda daan. Many temples hold collective shraddha ceremonies during Pitru Paksha.`,
  abroad: `If a full rite isn't possible, light a lamp before a photograph, offer water with sesame, cook a favourite dish, and give to charity in their name.`,
  prayers: [`mahamrityunjaya`, `ganga-snana`, `sarve-bhavantu`],
  links: [[`Pitru Paksha`, `#/festival/pitru-paksha`], [`Open the Calendar`, `#/calendar`]]
});
