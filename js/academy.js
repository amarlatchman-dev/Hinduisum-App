/* Dharma Path Academy: illustrated courses.
   Each lesson: { title, art, caption?, body (HTML), terms?: [[term, meaning]], practice?, links?: [[label, href]] }
   art names an illustration in img/learn/ (or a path to any image). Reading time is worked out from the text. */
window.CONTENT.categories = [
  { id: "all", name: "All" },
  { id: "philosophy", name: "Philosophy" },
  { id: "deities", name: "Deities" },
  { id: "scripture", name: "Scripture" },
  { id: "practice", name: "Practice" },
  { id: "temples", name: "Temples and places" }
];
window.CONTENT.courses = [];
const course = (c) => window.CONTENT.courses.push(c);

/* ---------------------------------------------------------------------- */
/* Philosophy                                                              */
/* ---------------------------------------------------------------------- */
course({
  id: `foundations`, deva: `सनातन`, category: `philosophy`, art: `om`,
  title: `Foundations of Hinduism`,
  subtitle: `The key ideas behind the tradition`,
  intro: `Begin here. Six lessons on the ideas most Hindus share: the eternal way, the Self, karma, the goals and stages of life, and the paths of yoga.`,
  lessons: [
    {
      title: `Sanatana Dharma: the eternal way`, art: `om`,
      caption: `Om, the sacred sound that many Hindus say holds the whole of reality.`,
      body: `<p>Ask Hindus what their religion is called and many will give an older name: <strong>Sanatana Dharma</strong>, the “eternal way” or “timeless order.” The word <em>Hindu</em> came later. It began as a Persian name for the people living beyond the river Sindhu, the Indus, and only slowly became the name of a religion.</p>
<p>Sanatana Dharma has no single founder, no single holy book and no central authority. It is better understood as a great family of traditions that grew over more than three thousand years across South Asia, carried by sages and poets, temple priests and wandering teachers, and above all by ordinary households. Today more than a billion people around the world are Hindu.</p>
<h3>Unity in variety</h3>
<p>A Hindu in Chennai and a Hindu in Trinidad, London or Kathmandu may worship different deities, keep different festivals and pray in different languages. Yet most share a common thread of ideas: one ultimate reality behind all things, the eternal soul, karma and rebirth, reverence for the Vedas and for the guru, and the hope of liberation.</p>
<p>This variety is a strength, not a weakness. The Rig Veda says, “Truth is one; the wise call it by many names” (1.164.46). People are encouraged to approach the divine in the way that suits their nature, whether through devotion, knowledge, selfless action or meditation.</p>
<h3>A way of life</h3>
<p>Many people describe Hinduism less as a set of beliefs than as a way of living. Dharma touches everything: how you greet your elders, what you eat, how you work, and how you mark birth, marriage and death. A lamp lit at dawn, a mantra whispered before a journey and a kindness shown to a stranger are as much a part of it as philosophy or pilgrimage.</p>`,
      terms: [[`Sanatana Dharma`, `“The eternal way”, the traditional name for Hinduism.`], [`Dharma`, `The order that sustains the universe, and the right way to live within it.`], [`Sindhu`, `The river Indus, which gave us the word “Hindu”.`]],
      practice: `Light a lamp or a candle and sit with it for one minute. One flame can light a thousand others and lose nothing. Many teachers use this image for the divine.`,
      links: [[`Om, the sacred sound`, `#/academy/symbols/1`]]
    },
    {
      title: `Brahman and Atman`, art: `sun-pots`,
      caption: `One sun, many reflections: a classic image of Brahman and the souls.`,
      body: `<p>At the heart of Hindu philosophy are two words. <strong>Brahman</strong> is the ultimate reality: infinite, unchanging and beyond every name and form, yet the ground of everything that exists. <strong>Atman</strong> is the true Self within each being. It is not the body and not the restless mind, but the pure awareness that witnesses them both.</p>
<p>The Upanishads return again and again to how the two are related. In the Chandogya Upanishad, the sage Uddalaka teaches his son Shvetaketu by dissolving salt in a cup of water. The salt can no longer be seen, yet every sip tastes of it. “That subtle essence is the Self of all this,” he says. “That is the truth. <em>Tat tvam asi</em>: you are that.”</p>
<h3>One truth, three readings</h3>
<p>The great schools of Vedanta understand this teaching in different ways:</p>
<ul><li><strong>Advaita</strong> (non-dualism), taught by Adi Shankaracharya, holds that Atman and Brahman are one. Our sense of being separate is a mistake, like taking a rope for a snake in dim light.</li><li><strong>Vishishtadvaita</strong> (qualified non-dualism), taught by Ramanujacharya, sees souls as real parts of God, as rays belong to the sun: one with him, yet distinct.</li><li><strong>Dvaita</strong> (dualism), taught by Madhvacharya, holds that the soul and God are eternally distinct, united by love and devotion.</li></ul>
<p>Many Hindus also speak of <strong>Ishvara</strong>: Brahman as a personal God who creates, sustains and cares for the world, and who may be worshipped as Vishnu, Shiva, the Goddess or another beloved form.</p>
<h3>The sun in the water pots</h3>
<p>A favourite teaching image is the sun reflected in many pots of water. Each pot holds its own bright reflection, and if the water is muddy or stirred up, the reflection is dim or broken. Yet there is only one sun. Spiritual practice is like letting the water grow clear and still, until the light shines through undisturbed.</p>`,
      terms: [[`Brahman`, `The ultimate, infinite reality.`], [`Atman`, `The true Self in every being.`], [`Tat tvam asi`, `“You are that”, from the Chandogya Upanishad (6.8.7).`], [`Ishvara`, `God as a personal Lord who can be worshipped and loved.`]],
      practice: `Sit quietly and notice that you can watch your thoughts come and go. Ask gently: who is watching? Don't look for an answer in words. Simply rest in the watching for a few breaths.`,
      links: [[`Read the Upanishads`, `#/read/upanishads`], [`Course: The Six Schools of Philosophy`, `#/academy/schools`]]
    },
    {
      title: `Karma and rebirth`, art: `wheel`,
      caption: `The wheel of samsara, and the seed of action that ripens into fruit.`,
      body: `<p><strong>Karma</strong> literally means “action.” It also means the results that follow from action, the way a seed grows into a tree. Every intentional thought, word and deed leaves an impression (<em>samskara</em>) on the mind and sets consequences in motion. Kindness tends to ripen into happiness; harm tends to ripen into suffering.</p>
<p>Karma is often misunderstood as fate or punishment. It is neither. It is closer to a moral law of cause and effect, as natural as gravity. No one sits in judgement; we shape our own experience. And because our choices are free, karma is a teaching of hope. Whatever our past, we can begin to change direction today.</p>
<h3>Samsara, the wheel of rebirth</h3>
<p>Hindus traditionally believe that the soul does not die with the body. In <strong>samsara</strong>, the cycle of birth, death and rebirth, it takes on new lives, carrying forward the impressions of its past actions. The Bhagavad Gita compares this to changing clothes: “As a person casts off worn-out garments and puts on new ones, so the embodied Self casts off worn-out bodies and enters new ones” (2.22).</p>
<h3>Three kinds of karma</h3>
<ul><li><strong>Sanchita</strong>: the great store of past karma not yet ripened.</li><li><strong>Prarabdha</strong>: the portion that has begun to bear fruit in this life, shaping our circumstances.</li><li><strong>Kriyamana</strong>: the new karma we create now, through present choices.</li></ul>
<p>We cannot always change the cards we are dealt, but we choose how we play them.</p>
<h3>Freedom from the wheel</h3>
<p>The final goal is not simply good karma but freedom from bondage altogether, called <strong>moksha</strong>. The Gita teaches that action done without selfish attachment, and offered to the divine, does not bind. The deed is done, but the doer stays free.</p>`,
      terms: [[`Karma`, `Action, and the results that follow from it.`], [`Samskara`, `An impression left on the mind by action and experience.`], [`Samsara`, `The cycle of birth, death and rebirth.`], [`Moksha`, `Liberation from that cycle.`]],
      practice: `Tonight, look back over your day. Choose one action whose effects you can still feel, good or bad. Without blame, ask what seed it planted, and what seed you would like to plant tomorrow.`,
      links: [[`Bhagavad Gita 2.22: changing clothes`, `#/read/gita/2?v=22`]]
    },
    {
      title: `The four goals of life`, art: `four-goals`,
      caption: `Dharma, artha, kama and moksha: the four aims of a full life.`,
      body: `<p>Hindu thought does not ask people to reject the world. Instead it names four <strong>purusharthas</strong>, the rightful aims of a full human life, and shows how they fit together.</p>
<ul><li><strong>Dharma</strong>: righteousness, duty and ethical living. Dharma is the foundation that keeps the other goals healthy.</li><li><strong>Artha</strong>: prosperity, security and meaningful work. Earning a living, supporting a family and contributing to society are honourable.</li><li><strong>Kama</strong>: love, pleasure, beauty and the enjoyment of life, from music and art to a good meal and a happy marriage.</li><li><strong>Moksha</strong>: liberation, freedom from the cycle of rebirth and the realisation of one's true nature.</li></ul>
<h3>Holding them in balance</h3>
<p>The first three goals are often pictured as the legs of a stool. Wealth pursued without dharma becomes greed, and pleasure without dharma becomes addiction. But wealth and pleasure guided by dharma are blessings, and they make generosity, family life and culture possible.</p>
<p>Moksha stands apart as the highest aim. It does not cancel the others; it gives them direction. A person can work hard, love deeply and enjoy life, while remembering that none of these is the final answer to the soul's longing.</p>
<h3>In everyday life</h3>
<p>The four goals offer a simple way to weigh a decision. Is it right? Does it support my livelihood and my family? Will it bring real joy? Does it bring me closer to inner freedom, or further from it? A choice that honours all four is usually a wise one.</p>`,
      terms: [[`Purushartha`, `An aim of human life; there are four.`], [`Artha`, `Prosperity and meaningful work.`], [`Kama`, `Love, pleasure and beauty.`]],
      practice: `Write the four goals in four columns and add one honest line under each about how it is going in your life. Notice which one is neglected, and choose one small step toward balance this week.`
    },
    {
      title: `The four stages of life`, art: `ashramas`,
      caption: `Student, householder, forest-dweller and renunciate: four seasons of a life.`,
      body: `<p>Alongside the four goals, traditional teaching describes four <strong>ashramas</strong>, or stages of life, each with its own duties and joys. They were described for an ideal life of about a hundred years, but their wisdom still speaks to modern lives.</p>
<ul><li><strong>Brahmacharya</strong>, the student. Youth is for learning, discipline and building character. Traditionally a student lived with a guru and studied the Vedas; today it is any time given to education and self-control.</li><li><strong>Grihastha</strong>, the householder. Marriage, work, raising children and serving the community. The scriptures praise this stage highly, because householders support everyone else: students, elders, monks and guests.</li><li><strong>Vanaprastha</strong>, the forest-dweller. When the children are grown, one gradually steps back from worldly responsibilities, hands over the running of the household and turns toward reflection, pilgrimage and guiding others.</li><li><strong>Sannyasa</strong>, the renunciate. The final stage is complete dedication to the spiritual life, letting go of possessions and position. Few take formal vows of sannyasa today, but many elders embrace its spirit of simplicity.</li></ul>
<h3>A dharma for every season</h3>
<p>The ashramas teach that every season of life has its own dharma. The ambitions of a young professional are right for that stage; clinging to them at eighty would be out of season. Each stage prepares for the next, and none should be rushed.</p>
<p>In many families this is still easy to see: grandparents who spend more time in prayer and at the temple, who pass on stories and prayers to the young, and who gently let go of control. That letting go is a spiritual practice too.</p>`,
      terms: [[`Ashrama`, `A stage of life.`], [`Grihastha`, `The householder stage.`], [`Sannyasa`, `Renunciation; the stage of the wandering monk.`]],
      practice: `Which stage of life are you in? Write down one duty and one gift of this stage. If you can, ask an elder in your family what they learned from the stage they have left behind.`
    },
    {
      title: `Four paths of yoga`, art: `mountain-paths`,
      caption: `Many paths up one mountain, meeting at the summit.`,
      body: `<p>The word <strong>yoga</strong> means “union” or “joining.” Long before it meant exercise classes, it meant the disciplines that unite the individual soul with the divine. The Bhagavad Gita, and later teachers such as Swami Vivekananda, describe four great paths:</p>
<ul><li><strong>Bhakti yoga</strong>, the path of devotion: loving God through prayer, song, worship and remembrance. It suits the heart.</li><li><strong>Jnana yoga</strong>, the path of knowledge: study, reflection and inquiry into who we really are. It suits the questioning mind.</li><li><strong>Karma yoga</strong>, the path of action: doing one's duty and serving others without selfish attachment to the results. It suits the active temperament.</li><li><strong>Raja yoga</strong>, the path of meditation: training body, breath and mind toward stillness, as taught in Patanjali's Yoga Sutras. It suits the contemplative.</li></ul>
<h3>Many paths, one summit</h3>
<p>A traditional image is a mountain with many paths winding up its sides. They start in different places and look different along the way, but they meet at the top. No path is ranked above the others, and none is closed to anyone.</p>
<p>In practice the paths are intertwined. Devotion deepens with understanding; knowledge without love turns dry; service is purified by meditation; and meditation rests on an ethical life. Most people lead with one path and let the others support it.</p>
<h3>Which is yours?</h3>
<p>If you are moved by music and prayer, begin with bhakti. If you love ideas, read the Gita and the Upanishads slowly. If you are happiest helping, offer seva at a temple or in your community. If you long for quiet, start a daily sitting. Whichever you choose, the Gita reassures us: on this path “no effort is ever lost” (2.40).</p>`,
      terms: [[`Bhakti`, `Loving devotion.`], [`Jnana`, `Spiritual knowledge and insight.`], [`Seva`, `Selfless service.`]],
      practice: `Spend ten minutes today on the path you are least drawn to. If you usually pray, sit in silence; if you usually think, sing; if you usually serve, read a verse slowly. Notice what it teaches you.`,
      links: [[`Read Bhagavad Gita, chapter 2`, `#/read/gita/2`], [`Chant on the mala`, `#/japa`]]
    }
  ]
});

course({
  id: `schools`, deva: `दर्शन`, category: `philosophy`, art: `darshanas`,
  title: `The Six Schools of Philosophy`,
  subtitle: `Six ways of seeing the truth`,
  intro: `Hindu philosophy is a long conversation between six classical schools. Each asks how we know what we know, what the world is made of and how the soul is set free.`,
  lessons: [
    {
      title: `What is a darshana?`, art: `darshanas`,
      caption: `Six lamps around one light: six schools, one search for truth.`,
      body: `<p>The Sanskrit word for a school of philosophy is <strong>darshana</strong>, from the root <em>drish</em>, “to see.” A darshana is a way of seeing. The same word is used when a devotee goes to “take darshan” of a deity in a temple. In both cases the aim is not just to think about truth but to see it directly.</p>
<p>Over many centuries six classical schools took shape. Each began with a short collection of sutras, terse memorable statements, which were then explained in great commentaries. They are usually grouped in pairs:</p>
<ul><li><strong>Nyaya and Vaisheshika</strong>: logic, and the analysis of the world into its elements.</li><li><strong>Samkhya and Yoga</strong>: spirit and matter, and the practical discipline of the mind.</li><li><strong>Mimamsa and Vedanta</strong>: the interpretation of the Vedas, their ritual teaching and their teaching on Brahman.</li></ul>
<h3>Debate as a sacred tradition</h3>
<p>These six are called <em>astika</em>, because they accept the authority of the Vedas. Buddhism, Jainism and the materialist Charvaka school, which do not, are called <em>nastika</em>. All of them argued fiercely with one another, and those arguments sharpened every side. A philosopher was expected to state the opponent's view fairly, often better than the opponent could, before answering it.</p>
<p>That habit of respectful debate is one of the treasures of Hindu thought. It is why the tradition can hold very different views of God and the soul, and still recognise them all as paths toward the same truth.</p>
<h3>A shared goal</h3>
<p>Despite their differences, the schools agree on the purpose of philosophy. It is not a game of ideas. It is medicine for suffering, a way to remove the ignorance that binds us and to reach freedom, moksha.</p>`,
      terms: [[`Darshana`, `A school of philosophy; literally “a way of seeing”.`], [`Sutra`, `A short, memorable teaching statement; literally “thread”.`], [`Astika`, `A school that accepts the authority of the Vedas.`]],
      practice: `Think of a belief you disagree with. Try to explain it in its best and fairest form, as its strongest supporter would. Notice how this changes your own view.`
    },
    {
      title: `Samkhya and Yoga`, art: `three-strands`,
      caption: `The three gunas, woven together in everything that exists.`,
      body: `<p><strong>Samkhya</strong>, traditionally founded by the sage Kapila, may be the oldest of the schools. It explains the world through two eternal principles. <strong>Purusha</strong> is pure consciousness: the silent witness, unchanging and untouched. <strong>Prakriti</strong> is nature or matter: everything that changes, from rocks and rivers to thoughts and feelings.</p>
<p>Prakriti is woven from three strands, the <strong>gunas</strong>. <em>Sattva</em> is clarity, harmony and light. <em>Rajas</em> is energy, passion and restlessness. <em>Tamas</em> is heaviness, inertia and darkness. Every object, every food and every mood is a mixture of the three, and the balance is always shifting.</p>
<h3>Why we suffer</h3>
<p>Our trouble, Samkhya says, is a case of mistaken identity. Consciousness forgets itself and identifies with the body and mind, which belong to prakriti. Liberation comes through discrimination (<em>viveka</em>): clearly seeing the difference between the witness and what is witnessed.</p>
<h3>Yoga: the practice</h3>
<p>If Samkhya is the map, <strong>Yoga</strong> is the journey. Patanjali's Yoga Sutras, compiled between about 1,600 and 2,000 years ago, define yoga in their second verse: <em>yogash chitta vritti nirodhah</em>, “yoga is the stilling of the movements of the mind.” When the waves settle, the Self is seen as it is, like the bottom of a clear lake.</p>
<p>Patanjali sets out eight limbs (<em>ashtanga</em>): ethical restraints, personal observances, posture, breath control, withdrawal of the senses, concentration, meditation and absorption (<em>samadhi</em>). Unlike Samkhya, Yoga also includes devotion to <em>Ishvara</em>, the Lord, as a powerful aid on the way.</p>
<p>The Bhagavad Gita draws deeply on both schools. Its teaching on the three gunas, in chapters 14 and 17, is pure Samkhya, and its sixth chapter on meditation is pure Yoga.</p>`,
      terms: [[`Purusha`, `Pure consciousness, the witness.`], [`Prakriti`, `Nature, matter and mind: all that changes.`], [`Gunas`, `The three qualities of nature: sattva, rajas and tamas.`], [`Samadhi`, `Deep meditative absorption.`]],
      practice: `Through the day, notice the three gunas in yourself: a clear, calm hour (sattva), a driven, restless one (rajas), a heavy, dull one (tamas). Ask what food, company and activity came before each.`,
      links: [[`Read the Yoga Sutras`, `#/read/yoga/1/1`], [`Bhagavad Gita, chapter 14: the three gunas`, `#/read/gita/14`]]
    },
    {
      title: `Nyaya and Vaisheshika`, art: `scales`,
      caption: `The scales of reason: how we weigh what is true.`,
      body: `<p><strong>Nyaya</strong>, founded on the sutras of the sage Gautama, is the school of logic. Its great question is: how do we know anything at all? Before arguing about God or the soul, Nyaya insists, we must agree on what counts as valid knowledge.</p>
<p>It names four <strong>pramanas</strong>, or reliable means of knowing:</p>
<ul><li><strong>Perception</strong> (<em>pratyaksha</em>): what we know directly through the senses.</li><li><strong>Inference</strong> (<em>anumana</em>): reasoning from what we see to what we cannot see.</li><li><strong>Comparison</strong> (<em>upamana</em>): learning something new by its likeness to something known.</li><li><strong>Testimony</strong> (<em>shabda</em>): the word of a trustworthy source, including scripture.</li></ul>
<p>The classic example of inference is famous across India: “There is fire on the hill, because there is smoke on the hill; wherever there is smoke there is fire, as in a kitchen.” Nyaya's careful rules of argument shaped debate in every other school, and its logicians later used them to argue for the existence of God as the intelligent maker of the world.</p>
<h3>Vaisheshika: the elements of reality</h3>
<p>Its partner school, <strong>Vaisheshika</strong>, founded by the sage Kanada, asks what the world is made of. Its answer is remarkably modern: everything physical is built from tiny, indivisible, eternal particles called <em>paramanu</em>, atoms, which combine to form all the objects we see.</p>
<p>Vaisheshika sorts everything that exists into categories (<em>padarthas</em>): substance, quality, action, universals, particularity and inherence, with non-existence added later. Its aim was not only science, though. By understanding the world clearly, one stops confusing the soul with the body, and that understanding leads to freedom.</p>`,
      terms: [[`Pramana`, `A valid means of knowledge.`], [`Anumana`, `Inference, reasoning from evidence.`], [`Paramanu`, `An indivisible atom, in Vaisheshika thought.`]],
      practice: `Take one thing you believe strongly. Ask Nyaya's question: how do I know it? By seeing it, by reasoning, by comparison, or by trusting someone? How reliable is that source?`
    },
    {
      title: `Mimamsa: the meaning of the Veda`, art: `yajna`,
      caption: `The sacred fire of the yajna, at the heart of Vedic ritual.`,
      body: `<p><strong>Mimamsa</strong> means “inquiry” or “reflection.” It began with the sutras of the sage Jaimini, and its subject is the Vedas themselves, especially their instructions for ritual. It is sometimes called <em>Purva Mimamsa</em>, the earlier inquiry, because it studies the earlier, ritual part of the Vedas.</p>
<p>For Mimamsa, dharma is known through the Veda. Human reason can tell us much about the world, but it cannot tell us with certainty what is right. The Vedic injunctions, the commands to perform this offering or keep that vow, are the source of dharma, and they are eternal and authorless.</p>
<h3>Why the ritual works</h3>
<p>How can a ritual performed today bring a result years later? Mimamsa philosophers answered with the idea of <strong>apurva</strong>, an unseen power created by a correctly performed act, which carries its fruit forward in time. It is an early, careful way of thinking about what we now call karma.</p>
<h3>The art of interpretation</h3>
<p>Mimamsa's lasting gift is its rules of interpretation. How do you read a sacred text that seems to contradict itself? Which words are commands and which are explanation or praise? When two rules clash, which one wins? The great Mimamsa teachers Kumarila Bhatta and Prabhakara worked out precise answers.</p>
<p>These rules were so useful that they shaped how Hindu law was read for centuries, and they still influence how scholars read scripture today. Every time a priest decides how a ritual should be adapted for a modern home, he is walking in Mimamsa's footsteps.</p>
<p>Mimamsa also kept alive a deep respect for daily duty. Its message is that sincere, careful action, done because it is right, is itself a sacred thing.</p>`,
      terms: [[`Mimamsa`, `“Inquiry”: the school that interprets the Vedas.`], [`Yajna`, `A sacred offering, especially into the fire.`], [`Apurva`, `The unseen power by which a ritual bears fruit later.`]],
      practice: `Choose one small daily duty, such as making tea for your family or lighting the lamp. Do it today with full care and attention, as if it were a ritual offering.`
    },
    {
      title: `Vedanta: the end of the Veda`, art: `rivers-ocean`,
      caption: `Three rivers, one ocean: the schools of Vedanta.`,
      body: `<p><strong>Vedanta</strong> means “the end of the Veda,” both the final part of the Vedas, the Upanishads, and their ultimate purpose. Also called <em>Uttara Mimamsa</em>, the later inquiry, it asks: what is Brahman, and how is the soul related to it? Today it is the most influential school of Hindu philosophy.</p>
<p>Every Vedanta teacher wrote commentaries on three foundational texts, the <strong>Prasthana Trayi</strong>: the Upanishads, the Brahma Sutras of Badarayana, and the Bhagavad Gita. From the same texts, they drew different conclusions.</p>
<h3>The three great schools</h3>
<ul><li><strong>Advaita</strong> (non-dualism). Adi Shankaracharya, around the eighth century, taught that Brahman alone is real and the Self is Brahman. The world of many things is <em>maya</em>, an appearance, like a dream that seems real until we wake. Liberation is knowledge: realising what we always were.</li><li><strong>Vishishtadvaita</strong> (qualified non-dualism). Ramanujacharya, in the eleventh and twelfth centuries, taught that Brahman is a personal God, Vishnu, and that souls and the world are real, forming his body. We are one with God as a body is one with its soul, yet we remain distinct. Liberation comes through loving surrender.</li><li><strong>Dvaita</strong> (dualism). Madhvacharya, in the thirteenth century, taught that God, souls and matter are eternally distinct. The soul's highest joy is to serve and adore God by his grace.</li></ul>
<p>Other teachers added further schools, such as Nimbarka's Dvaitadvaita, Vallabha's Shuddhadvaita and Chaitanya's Achintya Bhedabheda, “inconceivable oneness and difference.”</p>
<h3>Different rivers, one ocean</h3>
<p>Swami Vivekananda suggested that these schools are not rivals but stages, each true from its own standpoint. The devotee who says “I am your servant,” the one who says “I am a part of you” and the sage who says “I am you” may be climbing the same mountain.</p>`,
      terms: [[`Vedanta`, `“The end of the Veda”: the philosophy of the Upanishads.`], [`Maya`, `The power of appearance that makes the one seem many.`], [`Prasthana Trayi`, `The three foundational texts: the Upanishads, Brahma Sutras and Gita.`]],
      practice: `Read the Isha Upanishad, only eighteen verses long. Ask how each of the three schools might read its first verse, “All this is pervaded by the Lord.”`,
      links: [[`Read the Isha Upanishad`, `#/read/upanishads/1/1`], [`Nirvana Shatakam by Adi Shankaracharya`, `#/puja/nirvana-shatakam`]]
    }
  ]
});

course({
  id: `dharma`, deva: `धर्म`, category: `philosophy`, art: `banyan`,
  title: `Dharma in Daily Life`,
  subtitle: `Ethics, duty and kindness, every day`,
  intro: `Dharma is not only for temples and scriptures. These lessons show how Hindu ethics shapes the way we speak, work, give and care for one another.`,
  lessons: [
    {
      title: `What dharma means`, art: `banyan`,
      caption: `Like a great banyan, dharma shelters and holds up everything around it.`,
      body: `<p><strong>Dharma</strong> comes from the root <em>dhri</em>, “to hold” or “to support.” Dharma is what holds the world together: the natural order of the universe, the moral law and the right way to live within it. There is no single English word for it. It means duty, righteousness, virtue, law and truth, all at once.</p>
<p>A well-known saying puts it simply: <em>dharmo rakshati rakshitah</em>, “dharma protects those who protect it.” A society in which people keep their word, care for the weak and do their work honestly holds together. When dharma is neglected, things fall apart.</p>
<h3>Universal and personal dharma</h3>
<p>Some duties apply to everyone. These are <strong>sadharana dharma</strong>, the common virtues: truthfulness, non-violence, honesty, self-control, patience, generosity and compassion. The Manusmriti lists ten marks of dharma, among them patience, forgiveness, self-restraint, purity, wisdom, truth and freedom from anger.</p>
<p>Other duties depend on who we are and where we stand in life. This is <strong>svadharma</strong>, one's own dharma. The duties of a parent differ from those of a child, a teacher's from a soldier's, a young student's from an elder's. The Bhagavad Gita says it is better to follow your own dharma imperfectly than another's perfectly (3.35).</p>
<h3>Dharma is subtle</h3>
<p>Real life is complicated, and duties sometimes collide. Should I tell a painful truth or keep the peace? Should I put my family or my principles first? The epics are full of such dilemmas, and the Mahabharata admits that “the truth of dharma is hidden in a cave.”</p>
<p>The tradition offers guidance for such moments: the scriptures, the example of good people, and finally one's own conscience, the inner sense of what is right. When in doubt, choose the action that causes the least harm and serves the greater good.</p>`,
      terms: [[`Dharma`, `That which holds up the world: duty, virtue and the moral order.`], [`Sadharana dharma`, `The virtues expected of everyone.`], [`Svadharma`, `One's own duty, according to one's stage and role in life.`]],
      practice: `Write down your roles in life: child, parent, friend, worker, citizen. Next to each, write one duty you are keeping well and one you could keep better.`,
      links: [[`Bhagavad Gita, chapter 3: action and duty`, `#/read/gita/3`]]
    },
    {
      title: `Ahimsa and truth`, art: `lotus`,
      caption: `Ahimsa: living gently, harming as little as we can.`,
      body: `<p>Patanjali's Yoga Sutras open the path of yoga not with postures or breathing but with ethics. The first limb is the five <strong>yamas</strong>, restraints that are “the great vow, valid at all times and places” (2.31):</p>
<ul><li><strong>Ahimsa</strong>: non-violence, not harming any being in thought, word or deed.</li><li><strong>Satya</strong>: truthfulness.</li><li><strong>Asteya</strong>: not stealing, including not taking credit, time or trust that isn't ours.</li><li><strong>Brahmacharya</strong>: self-control and faithfulness in our desires.</li><li><strong>Aparigraha</strong>: not grasping; living simply, without greed or hoarding.</li></ul>
<h3>Ahimsa, the highest dharma</h3>
<p>The Mahabharata calls ahimsa <em>paramo dharmah</em>, the highest duty. It is the reason many Hindus are vegetarian, why cows and all animals are treated with care, and why a kolam of rice flour at the door also feeds the ants. Mahatma Gandhi made ahimsa a force that changed the world.</p>
<p>Ahimsa begins in the mind. Harsh words, resentment and contempt are also forms of violence. It does not mean being passive in the face of injustice; the Gita itself is set on a battlefield. It means never harming out of anger, greed or hatred, and protecting the vulnerable.</p>
<h3>Truth that is kind</h3>
<p>Satya is more than not lying. A verse often quoted from the Manusmriti gives a gentle rule: “Speak the truth, speak what is pleasant; do not speak an unpleasant truth, nor a pleasant falsehood” (4.138). The ideal is truth spoken with kindness, at the right time, for the good of the listener.</p>
<p>Patanjali promises that when a person is firmly established in truthfulness, their words gain power, and when they are established in non-violence, even hostility fades in their presence (2.35–36).</p>`,
      terms: [[`Yama`, `An ethical restraint; there are five.`], [`Ahimsa`, `Non-violence toward all beings.`], [`Satya`, `Truthfulness.`], [`Aparigraha`, `Non-grasping; simplicity.`]],
      practice: `For one day, before you speak, ask three questions: is it true, is it kind, is it necessary? Notice how often you pause.`,
      links: [[`Read Yoga Sutras, book II`, `#/read/yoga/2/1`]]
    },
    {
      title: `Purity, contentment and discipline`, art: `lamp-book`,
      caption: `Self-study by lamplight: one of the five niyamas.`,
      body: `<p>After the yamas, which govern how we treat others, Patanjali gives five <strong>niyamas</strong>, observances that shape how we treat ourselves (Yoga Sutras 2.32):</p>
<ul><li><strong>Shaucha</strong>: purity and cleanliness, of body, home, food and mind.</li><li><strong>Santosha</strong>: contentment, being at peace with what one has.</li><li><strong>Tapas</strong>: discipline and austerity; the inner fire that burns away weakness.</li><li><strong>Svadhyaya</strong>: self-study, through reading scripture, chanting and reflection.</li><li><strong>Ishvara pranidhana</strong>: surrender to God; offering our life and its results to the divine.</li></ul>
<h3>In a Hindu home</h3>
<p>Many everyday customs grow from these observances. Shoes are left at the door and the shrine is kept spotless (shaucha). Fasting on Ekadashi, rising early or keeping a vow are forms of tapas. Reading a chapter of the Gita or singing the Hanuman Chalisa is svadhyaya. Offering food before eating, and saying “as God wills,” is Ishvara pranidhana.</p>
<h3>Contentment is not laziness</h3>
<p>Santosha is sometimes mistaken for a lack of ambition. It is really freedom from the constant feeling that we need more to be happy. Patanjali says that from contentment comes the highest happiness (2.42). We can still work hard and aim high, but our peace no longer depends on the outcome.</p>
<p>Tapas, likewise, is not punishment. The word means heat, like the fire that refines gold. Small, steady disciplines build strength of character, so that when life tests us, we are ready.</p>
<p>Together the yamas and niyamas form the foundation of a spiritual life. Without them, Patanjali warns, meditation has nothing firm to stand on.</p>`,
      terms: [[`Niyama`, `A personal observance; there are five.`], [`Shaucha`, `Purity and cleanliness.`], [`Santosha`, `Contentment.`], [`Tapas`, `Discipline; literally “heat”.`]],
      practice: `Choose one niyama for this week. For shaucha, clear one cluttered space; for tapas, give up one small comfort; for svadhyaya, read one page of scripture a day.`
    },
    {
      title: `Seva and dana: service and giving`, art: `hands-offering`,
      caption: `Open hands: giving is a form of worship.`,
      body: `<p><strong>Seva</strong> means selfless service, and <strong>dana</strong> means giving. In Hindu life they are not optional extras; they are part of worship itself. Serving people is serving God, who lives in every heart.</p>
<h3>Three kinds of gift</h3>
<p>The Bhagavad Gita describes three qualities of giving (17.20–22). The best, <em>sattvic</em> gift is given simply because it is right to give, at the proper time and place, to a worthy person who cannot repay it. A <em>rajasic</em> gift is given reluctantly, or in the hope of a return or recognition. A <em>tamasic</em> gift is given with contempt, to the wrong person, at the wrong time.</p>
<p>The lesson is that the spirit of the gift matters as much as its size. A small gift given with love is worth more than a large one given for show.</p>
<h3>Five daily offerings</h3>
<p>The scriptures describe five daily duties of a householder, the <strong>pancha maha yajnas</strong>, or great offerings:</p>
<ul><li>to the gods, through prayer and worship;</li><li>to the sages, through study of the scriptures;</li><li>to the ancestors, by remembering and honouring them;</li><li>to fellow human beings, by feeding guests and the needy;</li><li>to all creatures, by feeding animals and birds.</li></ul>
<p>Traditionally, a portion of each meal was set aside for a cow, a dog, birds and a guest. The idea is that we live in a web of debts, to the divine, to our teachers, to our families and to nature, and every day we repay a little.</p>
<h3>Seva today</h3>
<p>Seva can be cooking in a temple kitchen, cleaning after a festival, visiting the sick, teaching children or volunteering in your community. Many temples run free kitchens open to all. The spirit is always the same: give your best, expect nothing, and see the divine in the one you serve.</p>`,
      terms: [[`Seva`, `Selfless service.`], [`Dana`, `Giving, charity.`], [`Pancha maha yajna`, `The five daily offerings of a householder.`]],
      practice: `This week, give something without telling anyone: an hour of help, a donation, or a meal. Notice how it feels to give with no thanks expected.`,
      links: [[`Bhagavad Gita, chapter 17`, `#/read/gita/17?v=20`]]
    },
    {
      title: `Family, elders and guests`, art: `family`,
      caption: `Namaste: the divine in me honours the divine in you.`,
      body: `<p>The Taittiriya Upanishad ends its teaching to students with words that many Hindu children still learn by heart: <em>matru devo bhava, pitru devo bhava, acharya devo bhava, atithi devo bhava</em>. “Let your mother be a god to you. Let your father be a god to you. Let your teacher be a god to you. Let your guest be a god to you” (1.11.2).</p>
<h3>Honouring elders</h3>
<p>Respect for elders runs through Hindu family life. Children touch the feet of parents and grandparents to receive blessings, especially at festivals, birthdays and before exams or journeys. The elder places a hand on the child's head and says a blessing. The gesture expresses humility, and gratitude for all that has been given.</p>
<p>Caring for parents in old age is seen as a sacred duty, and remembering ancestors after they pass, especially during Pitru Paksha, keeps the bond alive across generations.</p>
<h3>The guest is God</h3>
<p><em>Atithi</em> literally means “one who comes without a fixed date.” In the old ideal, any guest who arrived, expected or not, was to be welcomed with water, a seat, food and kind words. Hindu hospitality is famous for this reason: no one leaves a Hindu home hungry.</p>
<h3>Namaste</h3>
<p>The everyday greeting <strong>namaste</strong>, palms pressed together at the heart with a slight bow, carries the same idea. <em>Namah te</em> means “I bow to you.” Many explain it as “the divine in me honours the divine in you.” It is a reminder, many times a day, that every person we meet is sacred.</p>
<p>These customs are not about rank or formality. They are a training in reverence, so that respect for parents, teachers and strangers grows into respect for all life.</p>`,
      terms: [[`Atithi devo bhava`, `“Let the guest be a god to you.”`], [`Namaste`, `“I bow to you”: the greeting with joined palms.`], [`Pitru Paksha`, `The fortnight for honouring ancestors.`]],
      practice: `Call or visit an elder in your family this week. Ask them to tell you a story from their childhood, and ask for their blessing before you leave.`,
      links: [[`Pitru Paksha`, `#/festival/pitru-paksha`], [`Om Saha Navavatu: prayer of teacher and student`, `#/puja/sahana`]]
    }
  ]
});

/* ---------------------------------------------------------------------- */
/* Deities                                                                 */
/* ---------------------------------------------------------------------- */
course({
  id: `trimurti`, deva: `त्रिमूर्ति`, category: `deities`, art: `trimurti`,
  title: `The Trimurti`,
  subtitle: `Brahma, Vishnu and Shiva`,
  intro: `One divine reality, three cosmic roles: creating, preserving and transforming. Meet each of the three, and learn how Hindus choose the form of God they love most.`,
  lessons: [
    {
      title: `One reality, many forms`, art: `trimurti`,
      caption: `Lotus, discus and trident: the emblems of Brahma, Vishnu and Shiva.`,
      body: `<p>Visitors to a Hindu temple are often struck by how many deities they see. Yet most Hindus will tell you that God is one. The many forms are like the many facets of a single diamond, or like one person who is at once a parent, a child, a teacher and a friend.</p>
<p>The <strong>Trimurti</strong>, “three forms,” is one way of expressing this. It shows the one divine reality performing three great cosmic functions:</p>
<ul><li><strong>Brahma</strong> creates the universe.</li><li><strong>Vishnu</strong> preserves and protects it.</li><li><strong>Shiva</strong> dissolves it, so that it can be renewed.</li></ul>
<p>Creation, preservation and dissolution follow one another in endless cycles, like the seasons of a year or the breath going in and out. Dissolution is not something to fear. Without it, nothing new could ever be born.</p>
<h3>Different centres, one circle</h3>
<p>Different Hindu traditions place a different deity at the centre. For <strong>Vaishnavas</strong>, Vishnu, or his avatar Krishna, is the Supreme, and Brahma and Shiva serve him. For <strong>Shaivas</strong>, Shiva is the Supreme, who performs all three functions himself. For <strong>Shaktas</strong>, the Goddess, Devi, is the source of all power, and the three gods act through her.</p>
<p>These views do not usually lead to conflict. A Vaishnava family will happily visit a Shiva temple on Maha Shivaratri, and a Shaiva will join in at Janmashtami. Many people simply worship several forms, each at the right time.</p>
<h3>The feminine half</h3>
<p>Each god of the Trimurti has a divine consort, who is his power, or <em>shakti</em>. Brahma is paired with Saraswati, goddess of knowledge; Vishnu with Lakshmi, goddess of prosperity; Shiva with Parvati, the Divine Mother. Together they are sometimes called the <em>Tridevi</em>. Without his shakti, it is said, a god could not act at all.</p>`,
      terms: [[`Trimurti`, `“Three forms”: Brahma, Vishnu and Shiva.`], [`Vaishnava`, `A devotee of Vishnu.`], [`Shaiva`, `A devotee of Shiva.`], [`Shakta`, `A devotee of the Goddess.`]],
      practice: `If you have a home shrine, look at the images in it. Which forms of God are there, and why did your family choose them? Ask an elder if you don't know.`
    },
    {
      title: `Brahma, the creator`, art: `brahma`,
      caption: `Brahma's lotus seat, the Vedas, his water pot and his swan.`,
      body: `<p><strong>Brahma</strong> is the creator, the one who shapes the universe at the start of each cosmic cycle. One beautiful story tells how, as Vishnu lay resting on the cosmic ocean, a lotus grew from his navel, and Brahma appeared seated upon it, ready to create.</p>
<h3>Reading the image</h3>
<ul><li><strong>Four faces</strong> look out in the four directions. They are linked with the four Vedas, which are said to have come from his mouths, and with his all-seeing awareness.</li><li><strong>Four arms</strong> hold a manuscript of the Vedas (knowledge), a water pot (the source of life), a string of prayer beads (time) and sometimes a ladle used in fire offerings.</li><li>His vehicle is the <strong>hamsa</strong>, a swan or goose. In poetry the hamsa can separate milk from water, a symbol of the power to tell truth from falsehood.</li><li>He is often shown with a white beard, as the grandfather of all beings, <em>Pitamaha</em>.</li></ul>
<p>His consort is <strong>Saraswati</strong>, goddess of learning, music and the arts. It is fitting: creation needs knowledge and inspiration.</p>
<h3>Why so few temples?</h3>
<p>Although Brahma is honoured in prayers and rituals, very few temples are dedicated to him. The best known is at <strong>Pushkar</strong> in Rajasthan, beside a sacred lake. Puranic stories explain this with curses; in one, Brahma claims falsely to have found the top of Shiva's endless pillar of light. A philosophical explanation is also given: Brahma's work of creation is already done, while Vishnu and Shiva continue to protect and free us.</p>
<p>Brahma's life is said to last a hundred of his own years, each day of which, a <em>kalpa</em>, spans billions of human years. Hindu cosmology thinks in vast cycles of time, and Brahma reminds us of the grandeur of that vision.</p>`,
      terms: [[`Hamsa`, `The swan or goose, Brahma's vehicle.`], [`Pitamaha`, `“Grandfather”, a name of Brahma.`], [`Kalpa`, `A day of Brahma, an immense span of cosmic time.`]],
      practice: `Before starting something new today, a meal, a piece of work or a drawing, pause for a moment and offer it as an act of creation, as Brahma does.`,
      links: [[`Saraswati Namastubhyam`, `#/puja/saraswati`]]
    },
    {
      title: `Vishnu, the preserver`, art: `vishnu`,
      caption: `Conch, discus, mace and lotus: the four emblems of Vishnu.`,
      body: `<p><strong>Vishnu</strong> sustains and protects the universe and keeps it in order. His name is often explained as “the all-pervading one.” He is usually shown with blue-black skin, the colour of the infinite sky and the deep ocean, wearing yellow silk and a garland of forest flowers.</p>
<p>Between cycles of creation he rests on the coils of the great serpent <strong>Shesha</strong>, who floats on the cosmic ocean. When he wakes, the universe begins again. His heavenly home is <strong>Vaikuntha</strong>, his vehicle is <strong>Garuda</strong>, the eagle, and his consort is <strong>Lakshmi</strong>, goddess of prosperity and grace.</p>
<h3>The four emblems</h3>
<ul><li><strong>Shankha</strong>, the conch: the primordial sound from which creation unfolds, and a call to dharma.</li><li><strong>Chakra</strong>, the Sudarshana discus: the spinning wheel of time and the mind, which cuts through evil and ignorance.</li><li><strong>Gada</strong>, the mace: strength and the power of knowledge.</li><li><strong>Padma</strong>, the lotus: purity, beauty and liberation.</li></ul>
<h3>He comes when he is needed</h3>
<p>Vishnu is the god who descends. Whenever dharma declines and the world is in danger, he takes form on earth as an <strong>avatar</strong>, “one who comes down.” In the Bhagavad Gita, Krishna says: “To protect the good, to destroy evil and to establish dharma, I come into being age after age” (4.8). The best known of his ten avatars are Rama and Krishna.</p>
<p>Many prayers are addressed to Vishnu. The Vishnu Sahasranama, his thousand names, taught by Bhishma in the Mahabharata, is chanted in homes and temples every day, and Thursday is traditionally his day. Ekadashi, the eleventh day of each lunar fortnight, is sacred to him.</p>`,
      terms: [[`Avatar`, `“One who descends”: a form taken by God on earth.`], [`Vaikuntha`, `Vishnu's heavenly abode.`], [`Garuda`, `The divine eagle, Vishnu's vehicle.`]],
      practice: `Learn the short prayer Shantakaram Bhujagashayanam, which describes Vishnu resting on the serpent. Say it slowly and picture each part of the image.`,
      links: [[`Shantakaram Bhujagashayanam`, `#/puja/shantakaram`], [`Om Jai Jagdish Hare`, `#/puja/jagdish`], [`Course: The Ten Avatars of Vishnu`, `#/academy/avatars`]]
    },
    {
      title: `Shiva, the transformer`, art: `shiva`,
      caption: `Trident and drum, crescent moon and the river Ganga.`,
      body: `<p><strong>Shiva</strong>, “the auspicious one,” is the great yogi and the lord of transformation. He dissolves the universe at the end of each cycle, and in our own lives he destroys ignorance, ego and attachment so that something truer can grow. He is both fierce and utterly gentle, easy to please and generous with blessings.</p>
<h3>Reading the image</h3>
<ul><li>He sits in meditation on <strong>Mount Kailash</strong>, his body smeared with sacred ash, a reminder that all bodies return to dust.</li><li>A <strong>crescent moon</strong> rests in his matted hair, and the river <strong>Ganga</strong> flows from it. He caught the mighty river in his locks as it fell from heaven, so that its force would not shatter the earth.</li><li>His <strong>third eye</strong> sees beyond appearances; when it opens, it burns away illusion.</li><li>His throat is blue. When the gods and demons churned the ocean, a deadly poison rose up, and Shiva drank it to save the world. Parvati held his throat so it went no further, and he is called <em>Neelakantha</em>, the blue-throated one.</li><li>He holds a <strong>trishula</strong>, a trident, and a small <strong>damaru</strong> drum, whose beat is the rhythm of creation.</li></ul>
<p>His vehicle is <strong>Nandi</strong>, the bull, whose statue faces the shrine in every Shiva temple. His consort is <strong>Parvati</strong>, and their sons are <strong>Ganesha</strong> and <strong>Kartikeya</strong>, also called Murugan or Skanda.</p>
<h3>Nataraja and the lingam</h3>
<p>As <strong>Nataraja</strong>, lord of dance, Shiva dances within a ring of fire, creating and destroying the universe in one movement, crushing the dwarf of ignorance beneath his foot. In temples he is most often worshipped as the <strong>lingam</strong>, a smooth rounded pillar, a sign of the formless infinite.</p>
<p>Mondays are sacred to Shiva, and his great night is Maha Shivaratri. His five-syllable mantra, <em>Om Namah Shivaya</em>, is one of the most loved in all of Hinduism.</p>`,
      terms: [[`Neelakantha`, `“Blue-throated”, a name of Shiva.`], [`Nataraja`, `Shiva as lord of the cosmic dance.`], [`Lingam`, `The formless pillar-symbol of Shiva.`], [`Nandi`, `The bull, Shiva's vehicle and doorkeeper.`]],
      practice: `On Monday, chant Om Namah Shivaya 108 times on the mala, slowly. With each repetition, let go of one worry.`,
      links: [[`Om Namah Shivaya`, `#/puja/shiva`], [`Maha Shivaratri`, `#/festival/maha-shivaratri`], [`Chant on the mala`, `#/japa?m=shiva`]]
    },
    {
      title: `Choosing your ishta devata`, art: `shrine`,
      caption: `A home shrine: where a family's chosen forms of God are honoured.`,
      body: `<p>With so many forms of God, where should a person begin? Hindu tradition gives a gentle answer: choose the form that draws your heart. This is your <strong>ishta devata</strong>, your “chosen” or “beloved” deity.</p>
<p>Your ishta devata might be Krishna, whose playfulness and love you adore; Shiva, whose stillness calls to you; the Goddess, whose motherly care comforts you; Hanuman, whose courage inspires you; or another form entirely. Choosing one does not deny the others. It is simply the face of the divine you know best, the way you might feel closest to one particular friend.</p>
<h3>Family and village deities</h3>
<p>Many Hindus also have a <strong>kula devata</strong>, a family deity worshipped by their ancestors for generations, often at a particular temple that the family visits for important events such as a child's first haircut or a wedding. Villages and towns have their own <strong>grama devata</strong>, protective deities, often a form of the Goddess.</p>
<h3>Worshipping five as one</h3>
<p>Adi Shankaracharya encouraged a practice called <strong>panchayatana puja</strong>, the worship of five deities together: Vishnu, Shiva, the Goddess, Ganesha and Surya, the sun. One of them is placed in the centre as the ishta devata, with the other four around. Kartikeya was later added to make six. The practice expresses a simple truth: all these forms point to one reality.</p>
<h3>How to begin</h3>
<p>If you don't yet feel drawn to a form, start with what your family worships, or with Ganesha, who is honoured first in every puja. Read the stories, learn a prayer and visit a temple. Over time, many people find that one form begins to feel like home. Ramakrishna Paramahamsa used to say that God can be reached through any form, as long as the longing is sincere.</p>`,
      terms: [[`Ishta devata`, `One's chosen, beloved form of God.`], [`Kula devata`, `A family's ancestral deity.`], [`Panchayatana puja`, `Worship of five deities together.`]],
      practice: `Read about one deity you know little about. Learn one prayer to that form and say it each morning for a week. Notice whether it speaks to you.`,
      links: [[`Browse prayers by deity`, `#/puja#browse`], [`Course: Daily Puja at Home`, `#/academy/puja`]]
    }
  ]
});

course({
  id: `devi`, deva: `देवी`, category: `deities`, art: `sri-yantra`,
  title: `The Divine Mother`,
  subtitle: `Shakti, Durga, Kali, Lakshmi and Saraswati`,
  intro: `In Hinduism, God is also Mother. Meet the Goddess as cosmic power, as fierce protector, and as the giver of prosperity and wisdom.`,
  lessons: [
    {
      title: `Shakti: divine energy`, art: `sri-yantra`,
      caption: `The Sri Yantra, a sacred diagram of the Goddess and the cosmos.`,
      body: `<p><strong>Shakti</strong> means power or energy. In Hindu thought, Shakti is the dynamic power of the divine: the force that creates, sustains and dissolves the universe. If Shiva is pure consciousness, still and silent, Shakti is the energy that makes everything move. A well-known saying puts it playfully: without Shakti, Shiva is <em>shava</em>, a corpse, unable even to stir.</p>
<p>For <strong>Shaktas</strong>, devotees of the Goddess, Shakti is not merely the consort of a god. She is the supreme reality itself, <strong>Mahadevi</strong>, the Great Goddess, from whom all gods draw their power. She is the mother of the universe, and her children can turn to her with the trust of a child running to its mother.</p>
<h3>The Devi Mahatmya</h3>
<p>The central scripture of Goddess worship is the <strong>Devi Mahatmya</strong>, “the glory of the Goddess,” also called the Durga Saptashati because of its seven hundred verses. It tells how the Goddess defeats demons that the gods could not overcome, and it is recited across India, especially during Navaratri. One famous refrain praises her as the one who dwells in all beings: as consciousness, as intelligence, as sleep, as hunger, as forgiveness and as mother.</p>
<h3>Many forms, one Mother</h3>
<p>The Goddess has countless forms. She is <strong>Parvati</strong>, gentle wife of Shiva; <strong>Durga</strong>, the invincible warrior; <strong>Kali</strong>, the fierce power of time; <strong>Lakshmi</strong>, the giver of prosperity; <strong>Saraswati</strong>, the source of wisdom. She is also worshipped as rivers like Ganga, as the earth, Bhudevi, and as countless village goddesses who protect their communities.</p>
<p>Her worship honours the feminine as sacred. In many homes, young girls are worshipped as forms of the Goddess during Navaratri, and the earth, rivers and cows are all honoured as mothers.</p>`,
      terms: [[`Shakti`, `Divine power or energy, worshipped as the Goddess.`], [`Mahadevi`, `The Great Goddess.`], [`Devi Mahatmya`, `The great scripture of the Goddess, also called Durga Saptashati.`]],
      practice: `Learn the verse Ya Devi Sarvabhuteshu, which praises the Goddess in all beings. Whenever you see kindness, strength or wisdom today, remember her in it.`,
      links: [[`Ya Devi Sarvabhuteshu`, `#/puja/ya-devi`], [`Sarva Mangala Mangalye`, `#/puja/sarva-mangala`]]
    },
    {
      title: `Durga, the invincible`, art: `durga`,
      caption: `Durga's many arms, each holding a gift from the gods.`,
      body: `<p><strong>Durga</strong>, whose name means “the invincible” or “the one hard to reach,” is the warrior form of the Divine Mother. She rides a lion or tiger, has eight or ten arms, and holds weapons given to her by the gods: Shiva's trident, Vishnu's discus, Indra's thunderbolt, a bow and arrows, a sword, a conch and a lotus. Yet her face is calm and smiling.</p>
<h3>The victory over Mahishasura</h3>
<p>The Devi Mahatmya tells how the buffalo demon <strong>Mahishasura</strong> won a boon that no man or god could kill him. He conquered heaven and drove out the gods. Furious, the gods poured out their combined radiance, and from that light the Goddess was born, more powerful than all of them together. After a great battle, she defeated Mahishasura and restored order.</p>
<p>The story is also read as an inner battle. Mahishasura, who keeps changing shape, stands for ego, ignorance and the restless, untamed mind. The Goddess is the divine power within us that can conquer them, when every good quality we have is gathered together.</p>
<h3>Navaratri and Durga Puja</h3>
<p>Durga is celebrated above all at <strong>Navaratri</strong>, the “nine nights” in autumn, when she is worshipped in nine forms, the Navadurga, one each night. The tenth day, <strong>Vijayadashami</strong>, celebrates victory.</p>
<p>In Bengal and among Bengalis everywhere, this is <strong>Durga Puja</strong>, the greatest festival of the year. Magnificent images of Durga with her children, Lakshmi, Saraswati, Ganesha and Kartikeya, are installed in decorated pavilions, worshipped for five days, and finally carried to the river to be immersed, as the Mother returns to her home on Mount Kailash.</p>
<p>Durga is the protector of the good. Devotees turn to her in times of danger, fear or struggle, trusting her strength.</p>`,
      terms: [[`Durga`, `“The invincible”: the warrior form of the Goddess.`], [`Mahishasura`, `The buffalo demon defeated by Durga.`], [`Navadurga`, `The nine forms of Durga worshipped at Navaratri.`]],
      practice: `Name one inner “demon” you struggle with, such as anger, fear or laziness. During the next Navaratri, or for nine days starting now, take one small step each day to overcome it.`,
      links: [[`Navaratri`, `#/festival/navaratri`], [`Jai Ambe Gauri`, `#/puja/ambe-aarti`], [`Shri Durga Chalisa`, `#/puja/durga-chalisa`]]
    },
    {
      title: `Kali, the power of time`, art: `kali`,
      caption: `The red hibiscus, Kali's flower, with her sword and the crescent moon.`,
      body: `<p><strong>Kali</strong> is one of the most striking forms of the Goddess, and one of the most misunderstood. Her name comes from <em>kala</em>, which means both “black” and “time.” She is the power of time itself, which in the end swallows everything, and she is pictured dark as the night sky, with wild hair and a fierce expression.</p>
<h3>Her story</h3>
<p>In the Devi Mahatmya, as Durga battles the demon armies, her face darkens with anger and Kali springs from her brow. She defeats the demons Chanda and Munda, and then <strong>Raktabija</strong>, who could create a copy of himself from every drop of his blood that touched the ground. Kali drinks every drop before it can fall, and so the demon is finally overcome.</p>
<p>Some stories add that, carried away in her dance of victory, she could not be calmed, until Shiva lay down in her path. When she stepped on him, she recognised her beloved and came to rest.</p>
<h3>Reading the symbols</h3>
<p>Kali's fearsome image is full of meaning. Her sword cuts through ignorance and attachment. Her garland of heads is often read as the letters of the alphabet, the sounds from which all creation is made, or as the egos she has freed. Her outstretched tongue, in some traditions, shows her surprise or modesty on stepping on Shiva. Two of her hands bless and reassure: “Do not be afraid.”</p>
<h3>The loving Mother</h3>
<p>To her devotees, Kali is not frightening at all. She is the most loving of mothers, who destroys only what harms her children. The nineteenth-century saint <strong>Ramakrishna Paramahamsa</strong>, priest of the Kali temple at Dakshineswar near Kolkata, spoke to her as a child speaks to its mother, and his love for her inspired millions.</p>
<p>Kali is worshipped especially in Bengal, where Kali Puja is celebrated on the new-moon night of Diwali. She teaches that fear itself can be faced and transformed, because the Mother is with us even in the dark.</p>`,
      terms: [[`Kali`, `The Goddess as the power of time.`], [`Kala`, `Time; also “black”.`], [`Raktabija`, `The demon who multiplied from his own blood, defeated by Kali.`]],
      practice: `Think of something you fear. Picture handing it to the Mother, who is stronger than any fear. Breathe slowly and let her hold it for you.`
    },
    {
      title: `Lakshmi, goddess of prosperity`, art: `lakshmi`,
      caption: `Lakshmi's lotus, rising from the water amid falling gold.`,
      body: `<p><strong>Lakshmi</strong> is the goddess of prosperity, good fortune and beauty, and the consort of Vishnu. Wherever there is abundance, harmony and grace, there is Lakshmi. She is usually shown seated or standing on a pink lotus, dressed in red and gold, with gold coins flowing from one hand. Elephants often stand beside her, pouring water over her from their trunks.</p>
<h3>Born from the ocean</h3>
<p>Lakshmi rose from the <strong>churning of the ocean</strong>, when the gods and demons churned the cosmic sea for the nectar of immortality. Among the treasures that emerged, she appeared seated on a lotus, radiant, holding a garland. She chose Vishnu as her eternal husband, and she accompanies him in each of his avatars: as Sita with Rama, and as Rukmini with Krishna.</p>
<h3>More than money</h3>
<p>Lakshmi brings material wealth, but not only that. Devotees speak of the <strong>Ashtalakshmi</strong>, her eight forms, which include wealth, grain and food, courage, children, victory, knowledge and good health. True prosperity is a full and balanced life.</p>
<p>The lotus she sits on is also a teaching. It grows in muddy water yet stays clean. Wealth is a blessing when it is earned honestly and used generously, but it should not stain the soul. Lakshmi is said to stay where there is honesty, cleanliness, hard work and gratitude, and to leave homes filled with quarrels, laziness or greed.</p>
<h3>Welcoming Lakshmi</h3>
<p>Lakshmi is honoured above all on <strong>Diwali</strong>, the festival of lights. Families clean and decorate their homes, draw rangoli at the door, light lamps in every window and perform Lakshmi Puja on the new-moon night, so that she will enter and bless the year ahead. Businesses open new account books. Fridays are also sacred to her, and in Bengal she is worshipped on the full moon after Durga Puja.</p>`,
      terms: [[`Lakshmi`, `The goddess of prosperity and grace, consort of Vishnu.`], [`Ashtalakshmi`, `The eight forms of Lakshmi.`], [`Lakshmi Puja`, `Worship of Lakshmi on the night of Diwali.`]],
      practice: `Clean one corner of your home today as an offering, and light a lamp there this evening. Give thanks for three blessings you already have.`,
      links: [[`Diwali`, `#/festival/diwali`], [`Om Jai Lakshmi Mata`, `#/puja/lakshmi-aarti`], [`Namastestu Mahamaye`, `#/puja/mahalakshmi`]]
    },
    {
      title: `Saraswati, goddess of wisdom`, art: `saraswati`,
      caption: `The veena, the book and the swan of Saraswati.`,
      body: `<p><strong>Saraswati</strong> is the goddess of knowledge, music, art, speech and wisdom, and the consort of Brahma. Her name is linked to a sacred river, the Sarasvati, praised in the Rig Veda as the best of mothers, rivers and goddesses. Like a river, knowledge flows, purifies and gives life.</p>
<h3>Reading the image</h3>
<ul><li>She wears <strong>white</strong>, the colour of purity and clear understanding, and sits on a white lotus or beside a river.</li><li>She plays the <strong>veena</strong>, a stringed instrument, showing that all the arts are sacred.</li><li>She holds a <strong>book</strong>, the Vedas or knowledge in general, and a <strong>mala</strong> of prayer beads, for meditation.</li><li>Her vehicle is the <strong>hamsa</strong>, the swan, which can tell milk from water, as wisdom tells truth from falsehood. Sometimes a peacock appears beside her too.</li></ul>
<h3>Students' goddess</h3>
<p>Students all over the Hindu world pray to Saraswati before exams, and musicians and artists honour her before performances. Many children's first lessons begin with her prayer, <em>Saraswati Namastubhyam</em>: “Salutations to you, Saraswati, giver of boons. As I begin my studies, may I always succeed.”</p>
<h3>Her festivals</h3>
<p>On <strong>Vasant Panchami</strong>, the fifth day of spring, Saraswati is worshipped in schools and homes. People wear yellow, the colour of mustard flowers, and children often write their first letters. In South India, Saraswati Puja falls at the end of Navaratri, when books and musical instruments are placed before her and left untouched for a day. On Vijayadashami, little children begin their education in a ceremony called <em>vidyarambham</em>, tracing letters in rice.</p>
<p>Saraswati reminds us that learning is a form of worship, and that knowledge is most precious when it is joined with humility.</p>`,
      terms: [[`Saraswati`, `The goddess of knowledge and the arts.`], [`Veena`, `A classical stringed instrument.`], [`Vasant Panchami`, `The spring festival of Saraswati.`], [`Vidyarambham`, `A child's ceremony of beginning to learn.`]],
      practice: `Before you next study, read or practise an art, say Saraswati Namastubhyam and offer your effort to her. Notice whether your focus changes.`,
      links: [[`Saraswati Namastubhyam`, `#/puja/saraswati`], [`Ya Kundendu`, `#/puja/ya-kundendu`], [`Vasant Panchami`, `#/festival/vasant-panchami`]]
    }
  ]
});

course({
  id: `ganesha`, deva: `गणेश`, category: `deities`, art: `elephant`,
  title: `Ganesha`,
  subtitle: `Lord of beginnings, remover of obstacles`,
  intro: `The best-loved deity in the Hindu world. Learn why Ganesha is honoured first, the stories of his birth and wisdom, and what his form teaches.`,
  lessons: [
    {
      title: `Why Ganesha comes first`, art: `puja-items`,
      caption: `Bell, conch and kalash: every puja begins by invoking Ganesha.`,
      body: `<p>Before a wedding, a housewarming, an exam, a new business or even a long journey, Hindus pray to <strong>Ganesha</strong>. Every puja, whatever deity it is for, begins by invoking him. Books and letters were once begun with the words <em>Shri Ganeshaya Namah</em>, “salutations to Lord Ganesha.”</p>
<p>Ganesha is <strong>Vighneshvara</strong>, lord of obstacles, and <strong>Vinayaka</strong>, the supreme leader. He removes the obstacles in our path, but he can also place obstacles in front of us when we need to slow down, rethink or learn something. Either way, he guides us toward success that is real and lasting.</p>
<h3>The race around the world</h3>
<p>A favourite story explains why he is worshipped first. Shiva and Parvati once offered a divine fruit to whichever of their sons could first travel around the whole world. Kartikeya, the swift warrior, leapt onto his peacock and flew off. Ganesha, with his round body and tiny mouse for a vehicle, simply walked around his parents three times and bowed. “You are my whole world,” he said. Delighted by his wisdom and devotion, Shiva declared that Ganesha would be honoured before all others.</p>
<h3>Many names</h3>
<p>Ganesha has many names, and devotees chant 108 or even 1,008 of them. A few you will hear often:</p>
<ul><li><strong>Ganapati</strong>: lord of the ganas, Shiva's attendants.</li><li><strong>Ekadanta</strong>: the one with a single tusk.</li><li><strong>Lambodara</strong>: the one with a large belly, which holds the whole universe.</li><li><strong>Gajanana</strong>: the elephant-faced one.</li></ul>
<p>He is worshipped by Hindus of every tradition, and also by many Buddhists and Jains. Wednesdays and the fourth day of each lunar fortnight, Chaturthi, are especially his.</p>`,
      terms: [[`Vighneshvara`, `Lord of obstacles.`], [`Ganapati`, `Lord of the ganas, Shiva's attendants.`], [`Shri Ganeshaya Namah`, `“Salutations to Lord Ganesha”, said before beginning anything.`]],
      practice: `Before you start your next important task, pause and say “Om Gam Ganapataye Namah” three times, asking for a clear path, or the patience to learn from obstacles.`,
      links: [[`Vakratunda Mahakaya`, `#/puja/ganesha`], [`Om Gam Ganapataye Namah`, `#/puja/ganesh-mantra`]]
    },
    {
      title: `The story of the elephant head`, art: `modak`,
      caption: `Modak sweets, Ganesha's favourite, with his little mouse.`,
      body: `<p>The best-known story of Ganesha's birth comes from the Shiva Purana. One day, while Shiva was away meditating, the goddess Parvati wished to bathe in peace. She took the turmeric paste she had used to cleanse herself and shaped from it a fine boy. She breathed life into him and told him to guard her door and let no one in.</p>
<p>When Shiva returned, the boy, who had never seen him, blocked his way. Shiva insisted; the boy refused. A great fight followed, and in anger Shiva struck off the boy's head.</p>
<h3>A new beginning</h3>
<p>Parvati was heartbroken, and her grief shook the universe. To console her, Shiva sent his attendants to bring the head of the first living creature they found facing north. They came back with the head of a noble elephant. Shiva set it on the boy's body and brought him back to life. He embraced him as his own son, named him <strong>Ganapati</strong>, leader of his ganas, and blessed him to be worshipped first, before every other god.</p>
<h3>What the story teaches</h3>
<p>Like many sacred stories, this one can be read on several levels. Some teachers see in it the ego, our small sense of self, being cut away and replaced by something greater and wiser, the elephant head, symbol of vast intelligence. Others see the reconciliation of a family, and the truth that loss can lead to a new and better beginning.</p>
<h3>Ganesha the scribe</h3>
<p>Another loved story tells how the sage Vyasa needed someone to write down the Mahabharata as he composed it. Ganesha agreed, on one condition: Vyasa must never pause. Vyasa added his own condition: Ganesha must understand every verse before writing it. When Ganesha's pen broke, he snapped off one of his own tusks and carried on writing. That is why he is shown with a broken tusk, a symbol of sacrifice for the sake of knowledge.</p>`,
      terms: [[`Ganas`, `Shiva's band of attendants.`], [`Ekadanta`, `“One-tusked”, a name of Ganesha.`], [`Modak`, `A sweet dumpling, Ganesha's favourite food.`]],
      practice: `Tell the story of Ganesha's birth to a child, or to a friend who doesn't know it. Ask them what they think it means.`
    },
    {
      title: `Reading Ganesha's form`, art: `elephant`,
      caption: `The elephant head of Ganesha: wisdom, patience and strength.`,
      body: `<p>Almost every part of Ganesha's form carries a teaching. Images vary, but these are the meanings most often given:</p>
<ul><li><strong>The large elephant head</strong>: wisdom and intelligence. Think big.</li><li><strong>Large ears</strong>: listen more than you speak, and take in good teachings.</li><li><strong>Small eyes</strong>: concentration and focus.</li><li><strong>The trunk</strong>: an elephant's trunk can uproot a tree or pick up a needle. True intelligence is both powerful and delicate, and adapts to every task.</li><li><strong>The broken tusk</strong>: sacrifice for the sake of knowledge, and the willingness to let go of what is imperfect.</li><li><strong>The large belly</strong>: the capacity to digest all of life's experiences, good and bad, with calm.</li><li><strong>The axe and noose</strong> in his hands: cutting attachments, and drawing the devotee closer to the goal.</li><li><strong>The modak</strong>, a sweet: the sweetness of spiritual reward.</li><li><strong>The raised hand</strong>: blessing and protection.</li></ul>
<h3>The mouse</h3>
<p>Ganesha's vehicle is a tiny mouse, <strong>Mushika</strong>. How can such a large god ride such a small creature? The mouse stands for restless desire, which nibbles away at everything. Ganesha sitting calmly on it shows desire brought under the control of wisdom. It also teaches that even the smallest creature has a place in the divine order.</p>
<h3>His family</h3>
<p>In many traditions Ganesha is accompanied by <strong>Riddhi</strong> and <strong>Siddhi</strong>, prosperity and spiritual accomplishment, often described as his consorts. In South India he is often seen as a lifelong bachelor, sitting under a tree at the edge of a village or temple, always ready to help.</p>
<p>Every image of Ganesha is like a little book of wisdom. Next time you see one, see how many of its teachings you can read.</p>`,
      terms: [[`Mushika`, `The mouse, Ganesha's vehicle.`], [`Riddhi and Siddhi`, `Prosperity and accomplishment, often shown with Ganesha.`]],
      practice: `Pick one quality from Ganesha's form, such as big ears for listening. Practise it deliberately for a whole day.`,
      links: [[`Jai Ganesh Deva`, `#/puja/ganesh-aarti`], [`Sukhkarta Dukhharta`, `#/puja/sukhkarta`]]
    },
    {
      title: `Ganesh Chaturthi`, art: `ghats`,
      caption: `At the end of the festival, Ganesha is carried to the water and bid farewell.`,
      body: `<p><strong>Ganesh Chaturthi</strong>, Ganesha's birthday, falls on the fourth day of the bright half of the month of Bhadrapada, usually in late August or September. It is celebrated everywhere, but nowhere more joyfully than in Maharashtra, Goa and Karnataka, and in Mumbai the whole city comes alive.</p>
<h3>Welcoming Ganesha home</h3>
<p>Families bring home a clay image of Ganesha, and in towns and cities huge images are installed in public pavilions. A priest or the head of the family performs <em>prana pratishtha</em>, inviting Ganesha's presence into the image. For the next one and a half, three, five, seven or ten days, he is treated as an honoured guest: offered flowers, red hibiscus, durva grass and, of course, modaks, with aarti every morning and evening. Songs like <em>Sukhkarta Dukhharta</em> fill the air.</p>
<h3>Farewell and return</h3>
<p>At the end, Ganesha is carried in a joyful procession, with drums and dancing, to a river, lake or the sea, and immersed. This is <strong>visarjan</strong>. People call out <em>Ganpati Bappa Morya, pudhchya varshi lavkar ya</em>: “O father Ganesha, come again soon next year!” The immersion is a reminder that every form returns to the formless, and that the divine is never really gone.</p>
<p>Today many families choose natural clay images and plant-based colours, or immerse the image in a bucket at home, to protect rivers and seas. It is a modern way of honouring an old truth: Ganesha loves all creation.</p>
<h3>A public festival</h3>
<p>Public celebrations of Ganesh Chaturthi were popularised in 1893 by the freedom fighter <strong>Lokmanya Tilak</strong>, who saw them as a way to bring people together across caste and class. They remain a great festival of community.</p>
<p>Each month, many devotees also keep <strong>Sankashti Chaturthi</strong>, the fourth day after the full moon, fasting until moonrise and praying to Ganesha to remove difficulties.</p>`,
      terms: [[`Prana pratishtha`, `The rite of inviting the divine presence into an image.`], [`Visarjan`, `Immersion of the image in water at the end of the festival.`], [`Sankashti Chaturthi`, `A monthly fast for Ganesha, broken at moonrise.`]],
      practice: `Check the Calendar for the next Sankashti Chaturthi. If you can, keep a light fast that day, and offer a sweet to Ganesha when the moon rises.`,
      links: [[`Ganesh Chaturthi`, `#/festival/ganesh-chaturthi`], [`Calendar`, `#/calendar`]]
    }
  ]
});

course({
  id: `avatars`, deva: `दशावतार`, category: `deities`, art: `vishnu`,
  title: `The Ten Avatars of Vishnu`,
  subtitle: `How the divine comes down to help`,
  intro: `Whenever the world is in danger, Vishnu descends in a new form. Six lessons on the Dashavatara, from the fish who saved the Vedas to Kalki, who is yet to come.`,
  lessons: [
    {
      title: `Why the divine descends`, art: `vishnu`,
      caption: `Vishnu's conch, discus, mace and lotus.`,
      body: `<p>An <strong>avatar</strong> is a “descent”: a form in which God comes down into the world. The idea is closely linked with Vishnu, the preserver, whose task is to protect the universe and keep dharma alive.</p>
<p>In the Bhagavad Gita, Krishna explains why he comes:</p>
<blockquote><span class="deva">परित्राणाय साधूनां विनाशाय च दुष्कृताम्।<br>धर्मसंस्थापनार्थाय सम्भवामि युगे युगे॥</span>“To protect the good, to destroy wrongdoing and to establish dharma, I come into being age after age.” (4.8)</blockquote>
<p>An avatar is not an ordinary soul born because of karma. Vishnu takes form freely, out of compassion, and his life on earth becomes a source of stories, teachings and devotion for all who come after.</p>
<h3>The Dashavatara</h3>
<p>The Puranas describe many avatars, but ten are especially famous, the <strong>Dashavatara</strong>:</p>
<ul><li><strong>Matsya</strong>, the fish</li><li><strong>Kurma</strong>, the turtle</li><li><strong>Varaha</strong>, the boar</li><li><strong>Narasimha</strong>, the man-lion</li><li><strong>Vamana</strong>, the dwarf</li><li><strong>Parashurama</strong>, Rama with the axe</li><li><strong>Rama</strong>, the prince of Ayodhya</li><li><strong>Krishna</strong>, the cowherd and teacher of the Gita</li><li><strong>Buddha</strong>, or in some lists <strong>Balarama</strong>, Krishna's elder brother</li><li><strong>Kalki</strong>, who is yet to come</li></ul>
<p>The lists vary between regions and texts, which is normal in Hindu tradition. The twelfth-century poet Jayadeva praised the ten in a famous hymn in his <em>Gita Govinda</em>, and they are often carved around temple doorways.</p>
<h3>A ladder of life?</h3>
<p>Some modern readers have noticed that the order seems to follow the story of life on earth: from a creature of the water, to one of land and water, to a land animal, to a half-human, to a small human, and on to full human beings. Whether or not it was intended, it is a striking pattern, and a reminder that the divine is present at every stage of life.</p>`,
      terms: [[`Avatar`, `A descent of God into the world.`], [`Dashavatara`, `The ten famous avatars of Vishnu.`], [`Yuga`, `One of the four ages of the world.`]],
      practice: `Read Bhagavad Gita 4.7 and 4.8 slowly, in Sanskrit if you can. Learn verse 4.8 by heart this week.`,
      links: [[`Bhagavad Gita 4.8`, `#/read/gita/4?v=8`], [`Om Namo Narayanaya`, `#/puja/narayana`]]
    },
    {
      title: `Matsya, the fish`, art: `matsya`,
      caption: `Matsya, the great fish, guiding the boat through the flood.`,
      body: `<p>The first avatar, <strong>Matsya</strong>, tells one of the world's great flood stories. It appears in the ancient Shatapatha Brahmana and is retold in the Puranas.</p>
<h3>The little fish</h3>
<p>One morning, as the wise king <strong>Manu</strong> stood in a river offering water to the sun, a tiny fish swam into his cupped hands. “Protect me,” it said, “and one day I will protect you.” Manu put it in a small pot, but by the next day it had outgrown it. He moved it to a pond, then a lake, then a river, and finally to the ocean, and each time it grew to fill its new home.</p>
<p>Manu realised this was no ordinary fish. Then it spoke again: in seven days a great flood would cover the world. Manu should build a boat and gather on board seeds of every plant, pairs of animals and the seven great sages.</p>
<h3>The flood</h3>
<p>When the waters rose, the fish appeared, now vast and shining, with a single great horn. Manu tied the boat to its horn using the serpent Vasuki as a rope, and Matsya towed them safely through the storms until the waters fell. Through the long night, Matsya taught Manu the deepest truths of the spirit. In some versions he also rescues the Vedas, stolen by a demon from Brahma as he slept.</p>
<p>Manu became the father of a new humanity. The word “manushya,” human being, means “descendant of Manu.”</p>
<h3>What it teaches</h3>
<p>Matsya teaches that small acts of kindness matter: Manu saved a tiny fish, and the fish saved the world. It also shows God protecting knowledge, life and wisdom through the darkest times, so that the world can begin again.</p>`,
      terms: [[`Matsya`, `The fish avatar.`], [`Manu`, `The first man of a new age, ancestor of humanity.`], [`Pralaya`, `The great dissolution, or flood, at the end of an age.`]],
      practice: `Do one small kindness today for a creature that cannot repay you, like Manu with the fish: feed birds, rescue an insect or water a plant.`
    },
    {
      title: `Kurma and the churning of the ocean`, art: `kurma`,
      caption: `Kurma, the turtle, holding up the mountain as the ocean is churned.`,
      body: `<p>The second avatar, <strong>Kurma</strong>, the turtle, belongs to one of the most dramatic stories in Hindu tradition: <strong>Samudra Manthan</strong>, the churning of the ocean of milk.</p>
<h3>The search for nectar</h3>
<p>Weakened by a sage's curse, the gods, or <em>devas</em>, were losing their battle with the demons, the <em>asuras</em>. Vishnu advised them to churn the cosmic ocean to obtain <strong>amrita</strong>, the nectar of immortality. The task was too great for them alone, so they made a truce with the asuras and worked together.</p>
<p>They used <strong>Mount Mandara</strong> as the churning rod and the great serpent <strong>Vasuki</strong> as the rope, the gods holding its tail and the demons its head. But as they began to churn, the mountain started to sink into the ocean floor. Vishnu took the form of a giant turtle, dived beneath it and held the mountain steady on his back.</p>
<h3>Poison and treasures</h3>
<p>The first thing to rise from the ocean was <strong>halahala</strong>, a deadly poison that threatened to destroy all life. Shiva drank it to save the world, and his throat turned blue. Then came wonders: the wish-fulfilling cow Kamadhenu, the white elephant Airavata, the wish-granting tree, the goddess <strong>Lakshmi</strong>, who chose Vishnu as her husband, and finally <strong>Dhanvantari</strong>, the physician of the gods, holding the pot of amrita.</p>
<p>The asuras seized the pot, but Vishnu appeared as the enchanting <strong>Mohini</strong> and shared the nectar among the gods. Drops of it are said to have fallen at four places on earth, Prayagraj, Haridwar, Ujjain and Nashik, where the Kumbh Mela is held to this day.</p>
<h3>What it teaches</h3>
<p>The churning is often read as the spiritual life. When we churn the ocean of the mind, poison may rise first: anger, fear and painful memories. With faith and patience, treasures follow, and at last the nectar of peace. And through it all, the divine supports us from beneath, like the turtle under the mountain.</p>`,
      terms: [[`Samudra Manthan`, `The churning of the cosmic ocean.`], [`Amrita`, `The nectar of immortality.`], [`Halahala`, `The poison that rose first, drunk by Shiva.`]],
      practice: `When something difficult “rises up” in you this week, remember the churning. Breathe, stay steady, and trust that it will pass and something good will follow.`,
      links: [[`Course: Sacred Places, the Kumbh Mela`, `#/academy/pilgrimage/5`]]
    },
    {
      title: `Varaha, Narasimha and Vamana`, art: `vamana`,
      caption: `Vamana's parasol and water pot, and his three great strides.`,
      body: `<h3>Varaha, the boar</h3>
<p>When the demon <strong>Hiranyaksha</strong> dragged the earth, the goddess Bhudevi, down to the bottom of the cosmic ocean, Vishnu took the form of a mighty boar. He dived into the depths, defeated the demon after a long battle, and lifted the earth up on his tusks, as gently as a lotus, setting her back in her place. Varaha is loved as the rescuer of the earth, and a reminder to care for her.</p>
<h3>Narasimha, the man-lion</h3>
<p>Hiranyaksha's brother, <strong>Hiranyakashipu</strong>, wanted revenge. Through fierce austerities he won a boon that seemed to make him immortal: he could not be killed by man or beast, by day or night, indoors or outdoors, on earth or in the sky, by any weapon. He then demanded to be worshipped as God.</p>
<p>But his little son <strong>Prahlada</strong> was a devoted lover of Vishnu. Nothing could shake his faith, not even his father's attempts to kill him. Hiranyakashipu's sister Holika, who could not be burned, sat with Prahlada in a fire, but she was consumed and the boy was saved. This is remembered at Holika Dahan, the bonfire on the eve of Holi.</p>
<p>At last, the king pointed to a pillar and sneered, “Is your Vishnu in there too?” He struck it, and out burst <strong>Narasimha</strong>, half man and half lion, neither man nor beast. At dusk, neither day nor night, on the threshold, neither inside nor outside, holding the king on his lap, neither earth nor sky, he slew him with his claws, no weapon at all. Every condition of the boon was kept, and the devotee was protected.</p>
<h3>Vamana, the dwarf</h3>
<p>The generous demon king <strong>Bali</strong> had conquered the three worlds. Vishnu came to his sacrifice as <strong>Vamana</strong>, a small boy priest, and asked for just three steps of land. Bali gladly agreed. Then Vamana grew to cosmic size. With one step he covered the earth, with the second the heavens. There was nowhere left for the third, so Bali humbly offered his own head. Vishnu sent him to rule the underworld, blessing him for his generosity, and allowed him to visit his people once a year. Kerala celebrates that visit as <strong>Onam</strong>.</p>`,
      terms: [[`Varaha`, `The boar avatar, rescuer of the earth.`], [`Narasimha`, `The man-lion avatar, protector of Prahlada.`], [`Vamana`, `The dwarf avatar who took three steps.`]],
      practice: `Prahlada kept his faith when everyone around him opposed it. Think of one good value you hold even when it is unpopular, and reaffirm it today.`,
      links: [[`Holi and Holika Dahan`, `#/festival/holi`]]
    },
    {
      title: `Parashurama, Rama and Krishna`, art: `bow`,
      caption: `The bow of Rama, the ideal king.`,
      body: `<h3>Parashurama, Rama with the axe</h3>
<p><strong>Parashurama</strong> was a brahmin sage, the son of the rishi Jamadagni, who received a divine axe from Shiva. When arrogant kings abused their power and killed his father, he rose against them and humbled the warrior class again and again. He is a fierce reminder that power must serve dharma. He is said to be <em>chiranjivi</em>, still living, and in the Mahabharata he is the teacher of the great warriors Bhishma, Drona and Karna.</p>
<h3>Rama, the ideal man</h3>
<p><strong>Rama</strong>, prince of Ayodhya and hero of the Ramayana, is called <em>Maryada Purushottama</em>, the perfect man who keeps every bound of dharma. As a son, he accepts fourteen years of exile to keep his father's word. As a husband, he crosses the ocean to rescue Sita. As a brother, a friend and a king, he is the model of loyalty, courage and fairness. His name alone, <em>Ram</em>, is a mantra, and Diwali in North India celebrates his return home.</p>
<h3>Krishna, the complete avatar</h3>
<p><strong>Krishna</strong> is the most loved of all avatars, and many devotees consider him not just an avatar but the Supreme Lord himself. His life has every flavour: the mischievous child of Vrindavan who steals butter, the cowherd whose flute enchants all creatures, the beloved of Radha, the wise statesman, and the teacher of the Bhagavad Gita on the battlefield of Kurukshetra.</p>
<p>Where Rama shows the beauty of dharma kept perfectly, Krishna shows the playfulness and freedom of divine love. Rama walks the straight path; Krishna dances. Between them, they have inspired more poetry, music, art and devotion than perhaps any other figures in Indian history.</p>
<p>Their birthdays, <strong>Ram Navami</strong> in spring and <strong>Janmashtami</strong> in late summer, are among the great festivals of the year.</p>`,
      terms: [[`Chiranjivi`, `An immortal; one who lives until the end of the age.`], [`Maryada Purushottama`, `“The perfect man who keeps every bound”: a title of Rama.`]],
      practice: `Rama kept his word at great cost. Is there a promise you have made and not yet kept? Keep it this week.`,
      links: [[`Course: The Great Epics`, `#/academy/epics`], [`Course: Krishna`, `#/academy/krishna`], [`Ram Navami`, `#/festival/ram-navami`]]
    },
    {
      title: `Buddha, Balarama and Kalki`, art: `sun-arc`,
      caption: `A new dawn: Kalki will bring the age of truth again.`,
      body: `<h3>The ninth avatar</h3>
<p>The ninth place in the Dashavatara is given to different figures in different traditions. Many Puranic lists name the <strong>Buddha</strong>, honoured for his compassion, which ended cruel animal sacrifices. Other lists, especially in South India and among some Vaishnava communities, name <strong>Balarama</strong>, Krishna's elder brother, a figure of great strength who carries a plough, symbol of farming and abundance. In such lists Krishna is often seen as the source of all the avatars rather than one of them. Jayadeva's hymn does exactly this: it names both Balarama and the Buddha, and praises Krishna as the one who takes all ten forms.</p>
<p>The variation is a good example of how Hindu tradition works: many voices, many local customs, and no single list that everyone must follow.</p>
<h3>The four ages</h3>
<p>Hindu cosmology describes time as moving through four ages, or <strong>yugas</strong>, which repeat in great cycles:</p>
<ul><li><strong>Satya Yuga</strong>, the age of truth, when dharma stands firm on four legs.</li><li><strong>Treta Yuga</strong>, when dharma stands on three. Rama lived in this age.</li><li><strong>Dvapara Yuga</strong>, when dharma stands on two. Krishna lived at its end.</li><li><strong>Kali Yuga</strong>, our present age, when dharma stands on just one leg, and quarrels, greed and confusion grow.</li></ul>
<h3>Kalki, who is to come</h3>
<p>At the end of the Kali Yuga, the Puranas say, Vishnu will appear as <strong>Kalki</strong>, riding a white horse and bearing a blazing sword. He will end the age of darkness and begin a new Satya Yuga, and the cycle will turn again.</p>
<h3>Hope in a dark age</h3>
<p>The tradition does not leave us without help in the Kali Yuga. Several scriptures say that in this age, the simplest path is the most powerful: remembering and chanting the name of God. A sincere prayer today is said to carry as much merit as long years of austerity in earlier ages. Every kind act and every prayer helps to bring the dawn a little closer.</p>`,
      terms: [[`Yuga`, `An age of the world; there are four.`], [`Kali Yuga`, `The present, darkest age.`], [`Kalki`, `The avatar who will end the Kali Yuga.`]],
      practice: `Choose a name of God that you love and repeat it quietly whenever you wait today: in a queue, at a traffic light, while the kettle boils.`,
      links: [[`Hare Krishna Maha Mantra`, `#/puja/hare-krishna`], [`Shri Ram Jai Ram`, `#/puja/rama-mantra`]]
    }
  ]
});

course({
  id: `krishna`, deva: `कृष्ण`, category: `deities`, art: `flute`,
  title: `Krishna`,
  subtitle: `The divine child, lover and teacher`,
  intro: `From a prison cell in Mathura to the battlefield of Kurukshetra, the life of Krishna holds every flavour of the divine. Five lessons on his life and his love.`,
  lessons: [
    {
      title: `Born at midnight`, art: `moon-phases`,
      caption: `Krishna was born at midnight on the eighth day of the waning moon.`,
      body: `<p>The story of Krishna begins in darkness. The cruel king <strong>Kamsa</strong> of Mathura heard a voice from the sky foretell that the eighth child of his sister <strong>Devaki</strong> would kill him. He threw Devaki and her husband <strong>Vasudeva</strong> into prison and killed each of their children as soon as they were born.</p>
<h3>The night of the birth</h3>
<p>Krishna, the eighth child, was born at midnight on the eighth day, Ashtami, of the dark half of the month, in the middle of a stormy monsoon night. He appeared to his parents in his four-armed divine form, then became an ordinary baby. At that moment the guards fell into a deep sleep, the chains fell away and the prison doors swung open.</p>
<p>Vasudeva placed the baby in a basket on his head and set out into the storm. When he reached the swollen river Yamuna, the waters parted to let him pass, and the great serpent Shesha rose up behind him, spreading his hoods like an umbrella over the child. In the village of Gokul, Vasudeva exchanged Krishna for the newborn daughter of the cowherd chief <strong>Nanda</strong> and his wife <strong>Yashoda</strong>, and returned to the prison before dawn.</p>
<p>When Kamsa came to kill the baby girl, she slipped from his hands and rose into the sky as the Goddess, warning him that the one who would destroy him was already safe.</p>
<h3>Janmashtami</h3>
<p>Krishna's birth is celebrated at <strong>Janmashtami</strong>, usually in August or September. Devotees fast all day and keep vigil until midnight, when the baby Krishna is bathed, dressed and rocked in a decorated cradle, with bells, conch shells, songs and joyful cries of “Nand ke anand bhayo, jai Kanhaiya Lal ki!” In Maharashtra, teams of young people build human pyramids to break a pot of curd hung high above the street, the <em>dahi handi</em>, recalling the child Krishna's love of butter.</p>
<p>The story's message is one of hope: even in the darkest prison, at the darkest hour, the divine can be born, and every locked door can open.</p>`,
      terms: [[`Janmashtami`, `The festival of Krishna's birth.`], [`Ashtami`, `The eighth day of a lunar fortnight.`], [`Dahi handi`, `The custom of breaking a pot of curd hung high, at Janmashtami.`]],
      practice: `On the next Janmashtami, try keeping the midnight vigil. Until then, sing or listen to a Krishna bhajan before bed one evening this week.`,
      links: [[`Janmashtami`, `#/festival/janmashtami`], [`Vasudeva Sutam Devam`, `#/puja/krishna-vande`]]
    },
    {
      title: `The child of Vrindavan`, art: `butter-pot`,
      caption: `The pot of butter that the little Krishna could never resist.`,
      body: `<p>Krishna grew up among the cowherds of Gokul and Vrindavan, beside the river Yamuna, loved by everyone. Stories of his childhood, told in the Bhagavata Purana, are some of the most joyful in all of Hindu literature.</p>
<h3>The butter thief</h3>
<p>The little Krishna adored fresh butter. With his brother Balarama and his friends, he would sneak into the village houses, climb on each other's shoulders to reach the pots hung from the rafters, and feast, sharing generously with the monkeys. The gopis, the village women, complained to Yashoda, but they secretly loved his visits. He is called <strong>Makhan Chor</strong>, the butter thief, and devotees say he still steals the most precious thing of all: the heart.</p>
<h3>The universe in his mouth</h3>
<p>One day his friends told Yashoda that Krishna had eaten mud. She made him open his mouth to check, and inside it she saw the whole universe: the earth, the stars, the planets, and even herself and her village. Overwhelmed, she understood for a moment who her son really was. Then, through his loving power, she forgot again and simply held him as her child.</p>
<h3>Lifting Govardhan</h3>
<p>The cowherds used to offer a great yearly worship to Indra, king of the gods and giver of rain. Krishna persuaded them instead to honour Govardhan Hill, which fed their cows, and the land around them. Indra, offended, sent a terrible storm. Krishna lifted the whole of Govardhan Hill on his little finger and held it up like an umbrella for seven days, sheltering every person and animal beneath it, until Indra admitted defeat.</p>
<p>This is remembered at <strong>Govardhan Puja</strong>, the day after Diwali, when devotees make a hill of food, the <em>annakut</em>, and offer it to Krishna. Other stories tell how he defeated the serpent Kaliya, who poisoned the Yamuna, and danced on its hoods.</p>
<p>These stories show a God who is not distant or frightening, but close enough to play with, scold and love like a child.</p>`,
      terms: [[`Makhan Chor`, `“Butter thief”, a loving name of the child Krishna.`], [`Gopis`, `The cowherd women of Vrindavan.`], [`Annakut`, `A “mountain of food” offered at Govardhan Puja.`]],
      practice: `Krishna sheltered everyone under the hill. Think of someone who needs shelter or support right now, and offer them a small kindness this week.`,
      links: [[`Madhurashtakam`, `#/puja/madhurashtakam`], [`Achyutam Keshavam`, `#/puja/achyutam`]]
    },
    {
      title: `Radha and the path of love`, art: `flute`,
      caption: `Krishna's flute and peacock feather: the call of divine love.`,
      body: `<p>As a youth in Vrindavan, Krishna played his bamboo flute on moonlit nights, and its music drew the gopis from their homes to dance with him by the Yamuna. This is the <strong>rasa lila</strong>, the “dance of divine love.” In the most famous telling, Krishna multiplied himself so that every gopi felt he was dancing with her alone.</p>
<h3>Radha</h3>
<p>The dearest of all the gopis was <strong>Radha</strong>. For many devotees, Radha is not only Krishna's beloved but his own inner power of love, his hladini shakti, the power of bliss. Krishna and Radha are inseparable, and many temples worship them together as <strong>Radha-Krishna</strong>. Devotees often greet each other with “Radhe Radhe.”</p>
<h3>What the love stories mean</h3>
<p>Teachers read these stories as a picture of the soul's love for God. The gopis left everything when they heard the flute, just as the soul, hearing the call of the divine, leaves behind its smaller attachments. Their love was selfless: they wanted only Krishna's happiness, not their own. When Krishna left Vrindavan, their longing for him became itself a form of union.</p>
<p>This is the heart of <strong>bhakti</strong>, the path of devotion. It approaches God not only as master or father but in every kind of loving relationship: as a friend, as a child, and as the beloved.</p>
<h3>The poets of love</h3>
<p>The love of Radha and Krishna inspired some of India's greatest poetry. Jayadeva's <em>Gita Govinda</em> in the twelfth century, the songs of <strong>Surdas</strong> and the princess-saint <strong>Mirabai</strong>, who left a royal palace to sing for Krishna, are still sung today. In the sixteenth century, <strong>Chaitanya Mahaprabhu</strong> of Bengal spread the joyful chanting of the Hare Krishna mantra, a movement that has since circled the globe.</p>`,
      terms: [[`Rasa lila`, `The dance of divine love in Vrindavan.`], [`Radha`, `Krishna's beloved, the embodiment of devotion.`], [`Bhakti`, `Loving devotion to God.`]],
      practice: `Listen to or sing Payoji Maine Ram Ratan Dhan Payo by Mirabai, or a Hare Krishna kirtan. Let the music carry your attention to the divine.`,
      links: [[`Jaya Radha Madhava`, `#/puja/radha-madhav`], [`Hare Krishna Maha Mantra`, `#/puja/hare-krishna`], [`Aarti Kunj Bihari Ki`, `#/puja/kunj-bihari`]]
    },
    {
      title: `Friend and teacher at Kurukshetra`, art: `chariot`,
      caption: `The chariot Krishna drove for Arjuna on the field of Kurukshetra.`,
      body: `<p>When Krishna grew up, he left Vrindavan for good. He returned to Mathura, freed his parents and defeated the tyrant Kamsa, fulfilling the prophecy. Later he founded the city of <strong>Dwarka</strong> by the western sea and ruled there as a wise and beloved king.</p>
<h3>The friend of the Pandavas</h3>
<p>Krishna was a cousin and close friend of the five Pandava brothers, the heroes of the Mahabharata, and especially of <strong>Arjuna</strong>. When the Pandavas' wife Draupadi was humiliated in the royal court after a rigged game of dice, and an attempt was made to strip her, she cried out to Krishna. Her sari became endless, and her honour was protected.</p>
<p>When war loomed between the Pandavas and their cousins the Kauravas, Krishna went as a peace envoy, asking for just five villages for the Pandavas. Duryodhana refused to give even as much land as could fit on the point of a needle. War became certain.</p>
<h3>The charioteer</h3>
<p>Krishna offered both sides a choice: his vast army, or himself, unarmed and not fighting. Duryodhana chose the army. Arjuna chose Krishna, who became his charioteer. On the first morning of battle, when Arjuna saw his teachers, cousins and elders ranged against him and dropped his bow in despair, Krishna spoke the teachings we know as the <strong>Bhagavad Gita</strong>.</p>
<p>In the Gita, the playful cowherd of Vrindavan reveals himself as the Lord of the universe. He teaches Arjuna about the eternal Self, selfless action, knowledge, devotion and surrender, and finally shows him his cosmic form.</p>
<h3>God as charioteer</h3>
<p>The image of Krishna holding the reins is one of the most loved in Hinduism. It suggests that when we let the divine guide us, we can face even life's hardest battles. Krishna does not fight Arjuna's battle for him. He stays beside him, guides him and gives him courage to act.</p>`,
      terms: [[`Dwarka`, `Krishna's city by the sea, in Gujarat.`], [`Kurukshetra`, `The battlefield of the Mahabharata war.`], [`Parthasarathi`, `“Charioteer of Arjuna”, a name of Krishna.`]],
      practice: `Before a difficult decision this week, sit quietly and imagine handing the reins to a wise, loving guide. What would they advise?`,
      links: [[`Course: Bhagavad Gita Essentials`, `#/academy/gita`], [`Read Bhagavad Gita, chapter 1`, `#/read/gita/1`]]
    },
    {
      title: `Krishna's friends and his devotees today`, art: `aarti-lamp`,
      caption: `Evening aarti for Krishna, offered in homes and temples worldwide.`,
      body: `<h3>Sudama's gift</h3>
<p>One of the most touching stories of Krishna is about his childhood friend <strong>Sudama</strong>, a poor brahmin. Urged by his wife, Sudama walked all the way to Dwarka to see his old friend, now a king, carrying the only gift he could afford: a handful of flattened rice tied in a cloth. He was too ashamed to offer it. But Krishna ran out to embrace him, washed his feet with his own hands, found the little bundle and ate the rice with delight. Sudama asked for nothing. When he returned home, he found his hut had become a palace.</p>
<p>The story captures something essential about Krishna: he values love, not riches. As he says in the Gita, he accepts with joy whatever is offered with devotion, even a leaf, a flower, a fruit or a little water (9.26).</p>
<h3>Krishna in the world today</h3>
<p>Krishna is worshipped in countless forms. At <strong>Puri</strong> in Odisha he is Jagannath, Lord of the universe, whose great chariot festival, the Rath Yatra, draws vast crowds. At <strong>Guruvayur</strong> in Kerala and <strong>Udupi</strong> in Karnataka he is worshipped as a child. At <strong>Nathdwara</strong> in Rajasthan he is Shrinathji, holding up Govardhan Hill, and at <strong>Pandharpur</strong> in Maharashtra he is Vithoba, standing on a brick, waiting for his devotees.</p>
<p>In 1966, A. C. Bhaktivedanta Swami Prabhupada founded the International Society for Krishna Consciousness, ISKCON, in New York. Its temples, kirtans and free vegetarian meals have brought the Hare Krishna mantra to almost every country on earth.</p>
<h3>Loving Krishna at home</h3>
<p>Many families keep a small image of baby Krishna, Laddu Gopal, and care for him like a member of the household: waking him gently, bathing and dressing him, offering him food and putting him to rest at night. It is a beautiful way to make love for God part of everyday life.</p>`,
      terms: [[`Sudama`, `Krishna's poor childhood friend.`], [`Jagannath`, `“Lord of the universe”: Krishna as worshipped at Puri.`], [`Laddu Gopal`, `The child Krishna, lovingly cared for at home.`]],
      practice: `Offer something small but sincere today: a flower, a fruit or a glass of water, at your shrine or to someone in need, remembering Sudama's rice.`,
      links: [[`Bhagavad Gita 9.26`, `#/read/gita/9?v=26`], [`Rath Yatra`, `#/festival/rath-yatra`], [`Govinda Jaya Jaya`, `#/puja/govinda-jaya`]]
    }
  ]
});

course({
  id: `hanuman`, deva: `हनुमान`, category: `deities`, art: `mace`,
  title: `Hanuman`,
  subtitle: `Strength, courage and devotion`,
  intro: `The mighty son of the wind and the perfect servant of Rama. Four lessons on Hanuman's life, his great leap, and why millions turn to him for courage.`,
  lessons: [
    {
      title: `Son of the wind`, art: `mace`,
      caption: `Hanuman's mace, with the mountain of healing herbs he carried.`,
      body: `<p><strong>Hanuman</strong> is one of the most loved deities in the Hindu world, worshipped for his strength, courage, wisdom and above all his devotion to Rama. He was born to <strong>Anjana</strong>, a celestial being born on earth as a vanara, and her husband <strong>Kesari</strong>, and he was blessed by <strong>Vayu</strong>, the god of the wind. That is why he is called <em>Pavanputra</em> or <em>Maruti</em>, son of the wind, and <em>Anjaneya</em>, son of Anjana.</p>
<h3>The child who leapt at the sun</h3>
<p>As a baby, Hanuman woke up hungry and saw the rising sun. Thinking it was a ripe red fruit, he leapt into the sky to eat it. The gods were alarmed, and Indra, king of the gods, struck him with his thunderbolt. The child fell to earth, his jaw, <em>hanu</em>, injured. That is how he got his name.</p>
<p>Vayu was so upset at his son's injury that he withdrew all the air from the world, and every creature began to suffocate. The gods rushed to heal the child and showered him with blessings: strength beyond measure, protection from every weapon, wisdom, and the power to change his size at will.</p>
<h3>Forgetting his strength</h3>
<p>Young Hanuman was so mischievous with his powers, playing pranks on the sages in the forest, that they gently cursed him to forget his strength until someone reminded him of it at the right moment. That moment would come much later, at the edge of the ocean.</p>
<p>Many people find this part of the story very human. We, too, often forget the strength we have, until a friend, a teacher or a crisis reminds us. Hanuman's devotees pray to him to awaken that hidden courage.</p>
<p>Hanuman is said to be a <em>chiranjivi</em>, one who lives until the end of the age. Tradition says that wherever the story of Rama is told, Hanuman is present, listening with tears of joy.</p>`,
      terms: [[`Pavanputra`, `“Son of the wind”, a name of Hanuman.`], [`Anjaneya`, `“Son of Anjana”, a name of Hanuman.`], [`Vanara`, `The forest people of the Ramayana, often pictured as monkeys.`]],
      practice: `Think of a strength you have forgotten or doubted. Write it down, and ask a friend to remind you of it when you need it, as Jambavan reminded Hanuman.`,
      links: [[`Om Shri Hanumate Namah`, `#/puja/hanuman-mantra`], [`Hanuman Jayanti`, `#/festival/hanuman-jayanti`]]
    },
    {
      title: `The servant of Rama`, art: `bow`,
      caption: `Rama's bow: the master Hanuman served with his whole heart.`,
      body: `<p>Hanuman first met <strong>Rama</strong> in the forests of Kishkindha. Rama and his brother Lakshmana were searching for Sita, who had been carried off by Ravana, king of Lanka. Hanuman was the minister of <strong>Sugriva</strong>, the exiled monkey king. Sent to find out who the strangers were, he approached them disguised as a wandering brahmin.</p>
<p>The moment he recognised Rama, Hanuman fell at his feet, and Rama embraced him. From that day, Hanuman's whole life belonged to Rama. He brought Rama and Sugriva together as allies, and Sugriva's armies of vanaras joined the search for Sita.</p>
<h3>Dasya bhakti</h3>
<p>Hanuman is the model of <strong>dasya bhakti</strong>, devotion as a servant. This does not mean weakness or humiliation. Hanuman was the strongest and wisest of all, yet he never sought anything for himself. His joy was simply to serve.</p>
<p>A famous saying, often attributed to Hanuman, explains his relationship with Rama on three levels: “When I think I am the body, I am your servant. When I think I am a soul, I am a part of you. When I know I am the Self, I am you.” In a few words it holds the three great schools of Vedanta.</p>
<h3>Rama in his heart</h3>
<p>After Rama's victory and coronation, Sita gave Hanuman a precious pearl necklace. He began biting each pearl and peering inside. When the courtiers asked why, he said he was looking for Rama, and anything without Rama was worthless to him. When they mocked him, asking whether Rama was in his own body, Hanuman tore open his chest, and there, in his heart, were Rama and Sita.</p>
<p>This image, Hanuman holding open his chest to reveal Rama and Sita, is one of the best-loved in Hindu art. It shows that the true devotee carries God in their heart wherever they go.</p>`,
      terms: [[`Dasya bhakti`, `Devotion in the spirit of a loving servant.`], [`Sugriva`, `The vanara king, Rama's ally.`], [`Kishkindha`, `The forest kingdom of the vanaras.`]],
      practice: `Do one task today purely as service, for your family, your temple or a neighbour, without seeking credit. Offer it silently to God.`,
      links: [[`Ramaskandam Hanumantam`, `#/puja/ramaskandam`], [`Course: The Great Epics`, `#/academy/epics`]]
    },
    {
      title: `The leap to Lanka`, art: `leap`,
      caption: `Hanuman's great leap across the ocean to Lanka.`,
      body: `<p>The search parties of vanaras spread out in every direction, looking for Sita. The southern party, which included Hanuman, finally reached the shore of the ocean. They learned that Sita was held captive in <strong>Lanka</strong>, an island kingdom far across the sea. No one could jump so far. The vanaras sat down in despair.</p>
<h3>Remembering his strength</h3>
<p>Then the wise old bear king <strong>Jambavan</strong> turned to Hanuman, who was sitting quietly apart. He reminded him of his birth, his blessings and his forgotten strength. As he listened, Hanuman began to grow, until he towered over the mountains. With Rama's name on his lips, he leapt into the sky and flew across the ocean.</p>
<h3>Sundara Kanda</h3>
<p>This part of the Ramayana is called the <strong>Sundara Kanda</strong>, the “beautiful book,” and many families read it in times of difficulty. On his flight Hanuman overcame many obstacles. In Lanka he made himself tiny and searched the whole city by night, until he found Sita in the <strong>Ashoka grove</strong>, sad but unbroken, surrounded by guards. He gave her Rama's ring as a token and comforted her with the news that Rama was coming.</p>
<p>Hanuman then let himself be captured and brought before Ravana, to warn him to return Sita. Ravana ordered his tail to be set on fire. Hanuman leapt from roof to roof, setting Lanka ablaze, then cooled his tail in the sea and returned to Rama with the news.</p>
<h3>The mountain of herbs</h3>
<p>Later, in the great battle, Lakshmana was gravely wounded. The only cure was a herb that grew on a distant Himalayan mountain. Hanuman flew there overnight, and when he could not tell which herb was the right one, he lifted the whole mountain and carried it back. Lakshmana was saved before dawn.</p>
<p>Hanuman's leap is the leap of faith. With devotion, he did what everyone thought impossible.</p>`,
      terms: [[`Sundara Kanda`, `The “beautiful book” of the Ramayana, telling of Hanuman's journey.`], [`Jambavan`, `The wise bear king who reminded Hanuman of his strength.`], [`Sanjeevani`, `The life-restoring herb Hanuman brought for Lakshmana.`]],
      practice: `Face one thing this week that you have been avoiding because it feels too big. Begin with Hanuman's name, and take the first step.`,
      links: [[`Read the Ramayana: Sundara Kanda`, `#/read/ramayana/5`], [`Manojavam Marutatulyavegam`, `#/puja/manojavam`]]
    },
    {
      title: `Hanuman in daily life`, art: `hands-offering`,
      caption: `Strength offered in service: the spirit of Hanuman's devotees.`,
      body: `<p>Hanuman is everywhere in Hindu life. His shrines stand at crossroads, at the edge of villages, in gyms and wrestling grounds, and in almost every temple. Truck drivers, students, soldiers and athletes all turn to him for protection and strength.</p>
<h3>The Hanuman Chalisa</h3>
<p>The most famous prayer to Hanuman is the <strong>Hanuman Chalisa</strong>, forty verses in the Awadhi language by the poet-saint <strong>Tulsidas</strong>, who also wrote the Ramcharitmanas, a beloved retelling of the Ramayana, in the sixteenth century. It tells Hanuman's story and praises his qualities: “ocean of wisdom and virtue,” “remover of fear and sorrow.” Millions recite it every day, and many know it by heart from childhood.</p>
<p>The Chalisa promises that “ghosts and evil spirits do not come near when the name of the great hero is spoken,” and that Hanuman removes disease and pain. Many people chant it when they feel afraid, before a journey or an exam, or at night.</p>
<h3>Tuesdays and Saturdays</h3>
<p>Tuesdays and Saturdays are especially sacred to Hanuman. Devotees visit his temple, offer red or orange sindoor, flowers and sweets such as besan laddoos, and some keep a fast. On Saturdays, many also pray to Hanuman for protection from the difficult influence of the planet Shani, Saturn. <strong>Hanuman Jayanti</strong>, his birthday, is celebrated in spring.</p>
<h3>What Hanuman teaches</h3>
<ul><li><strong>Strength should serve.</strong> Hanuman's power was never used for himself.</li><li><strong>Humility and greatness go together.</strong> The mightiest of heroes called himself only a servant.</li><li><strong>Faith overcomes fear.</strong> With Rama's name, Hanuman crossed the ocean.</li><li><strong>Devotion is active.</strong> Hanuman didn't only pray; he acted, tirelessly, for what was right.</li></ul>`,
      terms: [[`Hanuman Chalisa`, `Forty verses in praise of Hanuman, by Tulsidas.`], [`Tulsidas`, `The sixteenth-century poet-saint of Rama.`], [`Sindoor`, `Vermilion, offered to Hanuman.`]],
      practice: `Recite the Hanuman Chalisa this Tuesday or Saturday. Use Aarti mode in the app so the whole family can sing along.`,
      links: [[`Shri Hanuman Chalisa`, `#/puja/hanuman-chalisa`], [`Hanuman Chalisa in Aarti mode`, `#/aarti/hanuman-chalisa`], [`Aarti Keeje Hanuman Lala Ki`, `#/puja/hanuman-aarti`]]
    }
  ]
});

/* ---------------------------------------------------------------------- */
/* Scripture                                                               */
/* ---------------------------------------------------------------------- */
course({
  id: `vedas`, deva: `वेद`, category: `scripture`, art: `manuscript`,
  title: `The Sacred Texts`,
  subtitle: `Vedas, Upanishads, Puranas and more`,
  intro: `A map of the Hindu scriptures: what the Vedas are, what lies inside them, how the Upanishads, epics and Puranas fit around them, and where to begin reading.`,
  lessons: [
    {
      title: `Shruti and smriti`, art: `manuscript`,
      caption: `A palm-leaf manuscript: for centuries, scripture was written on leaves like these.`,
      body: `<p>Hinduism has no single holy book. Instead it has a vast library of sacred texts, composed over thousands of years in Sanskrit and many other languages. They fall into two broad families.</p>
<h3>Shruti: what was heard</h3>
<p><strong>Shruti</strong> means “that which is heard.” It refers to the <strong>Vedas</strong>, including the Upanishads. Tradition holds that the Vedas were not written by any human author. They are eternal truths that the ancient <strong>rishis</strong>, or seers, “heard” or “saw” in deep meditation and passed on. For this reason they are called <em>apaurusheya</em>, not of human origin. Shruti is the highest authority in Hindu tradition.</p>
<h3>Smriti: what is remembered</h3>
<p><strong>Smriti</strong> means “that which is remembered.” It includes everything composed later by sages and poets to explain, apply and illustrate the Vedic truths:</p>
<ul><li>the <strong>Itihasas</strong>, the great epics, the Ramayana and the Mahabharata, which contains the Bhagavad Gita;</li><li>the <strong>Puranas</strong>, collections of sacred history, stories of the gods and guidance for worship;</li><li>the <strong>Dharma Shastras</strong>, texts on law, duty and ethics, such as the Manusmriti;</li><li>the <strong>Sutras</strong> of the philosophical schools, and texts on grammar, astronomy, medicine and the arts.</li></ul>
<p>Alongside these are the <strong>Agamas</strong> and <strong>Tantras</strong>, which guide temple worship, and the vast devotional poetry of the saints in Tamil, Hindi, Marathi, Bengali, Kannada and many other languages.</p>
<h3>An oral tradition</h3>
<p>For most of their history, the Vedas were not read but chanted, passed from teacher to student by memory. Students learned them in several patterns, forwards, in pairs and in complex weaves, so that not a single syllable could change. This method was so successful that the Rig Veda has come down to us essentially unchanged for more than three thousand years. UNESCO recognises Vedic chanting as a masterpiece of the intangible heritage of humanity.</p>`,
      terms: [[`Shruti`, `“What is heard”: the Vedas, the highest scripture.`], [`Smriti`, `“What is remembered”: epics, Puranas, law books and more.`], [`Rishi`, `A seer who received the Vedic hymns.`], [`Apaurusheya`, `“Not of human origin”, said of the Vedas.`]],
      practice: `Listen to a recording of Vedic chanting, such as the Gayatri Mantra or a Shanti Mantra. Notice the precise rise and fall of the voice, unchanged for thousands of years.`,
      links: [[`Gayatri Mantra`, `#/puja/gayatri`], [`About the scriptures in this app`, `#/read/about`]]
    },
    {
      title: `The four Vedas`, art: `yajna`,
      caption: `The Vedic fire altar, around which the hymns were chanted.`,
      body: `<p><strong>Veda</strong> means “knowledge,” from the same root as the English word “wisdom” and the Latin <em>videre</em>, to see. There are four Vedas, each with its own character and purpose. Scholars date the oldest hymns to around 1500 BCE; tradition considers them timeless.</p>
<ul><li><strong>Rig Veda</strong>: the oldest and most important, a collection of 1,028 hymns in ten books, or mandalas. They praise the forces of nature as gods, Agni (fire), Indra (the storm and strength), Varuna (cosmic order), Surya and Savitr (the sun), Ushas (the dawn), and they rise to deep questions about the origin of everything. The Gayatri Mantra comes from the Rig Veda (3.62.10).</li><li><strong>Sama Veda</strong>: the Veda of song. Most of its verses come from the Rig Veda, set to elaborate melodies for chanting in rituals. Indian classical music traces its roots to it. In the Gita, Krishna says, “Among the Vedas, I am the Sama Veda” (10.22).</li><li><strong>Yajur Veda</strong>: the Veda of ritual, containing the prose formulas and verses recited by priests while performing sacrifices. It exists in two main branches, the White and the Black Yajur Veda. The Shri Rudram, a great hymn to Shiva, comes from it.</li><li><strong>Atharva Veda</strong>: the Veda of daily life, with hymns for healing, protection, marriage, harmony at home and prosperity, as well as profound philosophy. Two of the best-known Upanishads, the Mundaka and the Mandukya, belong to it.</li></ul>
<h3>The world of the Vedas</h3>
<p>Vedic religion centred on the <strong>yajna</strong>, the fire sacrifice. Offerings of ghee, grain and soma were poured into the sacred fire while hymns were chanted, and Agni, the fire, carried them to the gods. The idea was one of exchange and harmony: humans nourish the gods, and the gods sustain the world.</p>
<p>The fire offering lives on in Hindu weddings, where the couple walks around the sacred fire, in the havan performed at housewarmings and other ceremonies, and in the simple lamp lit every day at the home shrine.</p>`,
      terms: [[`Veda`, `“Knowledge”: the four oldest scriptures.`], [`Mandala`, `One of the ten books of the Rig Veda.`], [`Yajna`, `A sacred fire offering.`], [`Agni`, `The god of fire, messenger between humans and gods.`]],
      practice: `Read one of the selected Rig Veda hymns in the app, such as the hymn to Agni or the hymn of creation. Read it aloud, slowly.`,
      links: [[`Rig Veda: hymn to Agni`, `#/read/rigveda/1/1`], [`Rig Veda: the hymn of creation`, `#/read/rigveda/1/8`], [`Read the Sama Veda`, `#/read/samaveda`]]
    },
    {
      title: `Inside a Veda`, art: `banyan`,
      caption: `Like a banyan, each Veda grows from hymn to ritual to forest teaching.`,
      body: `<p>Each of the four Vedas is not a single book but a whole collection, built up in layers over many centuries. Each layer has its own purpose, and together they trace a journey from outward ritual to inward realisation.</p>
<ul><li><strong>Samhitas</strong>: the oldest layer, the collections of mantras and hymns themselves. When people speak of “the Rig Veda,” they usually mean its Samhita.</li><li><strong>Brahmanas</strong>: prose texts that explain the rituals in detail, what to do, when and why, along with stories and the meaning behind the ceremonies.</li><li><strong>Aranyakas</strong>: the “forest texts,” meant for those who had withdrawn to the forest for reflection. They begin to interpret the rituals symbolically, turning the outer sacrifice into an inner one.</li><li><strong>Upanishads</strong>: the philosophical teachings at the very end of each Veda, exploring Brahman, the Self, and the path to liberation.</li></ul>
<h3>From the outer fire to the inner</h3>
<p>As you move through the layers, the focus shifts. The early hymns praise the gods and ask for blessings. The Brahmanas perfect the ritual. The Aranyakas ask what the ritual really means. And the Upanishads say the true fire is within: the breath, the mind and the light of awareness itself.</p>
<p>This movement maps neatly onto the four stages of life. The student learns the hymns, the householder performs the rituals, the forest-dweller reflects on their meaning, and the renunciate seeks the truth the Upanishads reveal.</p>
<h3>Two parts of the Veda</h3>
<p>Traditional teachers divide the Vedas into two portions. The <strong>karma kanda</strong>, the section on action, covers the hymns and rituals. The <strong>jnana kanda</strong>, the section on knowledge, is the Upanishads. The two schools of Mimamsa specialise in each: Purva Mimamsa in the ritual, and Vedanta in the knowledge.</p>`,
      terms: [[`Samhita`, `The collection of hymns and mantras.`], [`Brahmana`, `A prose text explaining the rituals.`], [`Aranyaka`, `A “forest text” of symbolic reflection.`], [`Jnana kanda`, `The knowledge portion of the Vedas: the Upanishads.`]],
      practice: `Think of a ritual you do, such as lighting a lamp, offering water or bowing. Ask what it means to you. Then try doing it once with full attention to that meaning.`
    },
    {
      title: `The Upanishads`, art: `guru`,
      caption: `A teacher and student in the forest, where the Upanishads were taught.`,
      body: `<p>The word <strong>Upanishad</strong> is often explained as “sitting down near”: a student sitting close to a teacher to receive a secret teaching. Tradition counts 108 Upanishads, and about a dozen are considered the principal ones, among them the Isha, Kena, Katha, Prashna, Mundaka, Mandukya, Taittiriya, Aitareya, Chandogya and Brihadaranyaka.</p>
<p>The Upanishads are not a systematic treatise. They are dialogues, stories, riddles and bursts of poetry, in which teachers and students, kings and sages, husbands and wives, ask the deepest questions. What is real? Who am I? What happens at death? What is the one thing which, when known, makes everything known?</p>
<h3>The great sayings</h3>
<p>Four short sentences, one from each Veda, are called the <strong>Mahavakyas</strong>, the great sayings. Each points to the unity of the Self and Brahman:</p>
<ul><li><em>Prajnanam Brahma</em>: “Consciousness is Brahman” (Aitareya Upanishad, Rig Veda).</li><li><em>Aham Brahmasmi</em>: “I am Brahman” (Brihadaranyaka Upanishad, Yajur Veda).</li><li><em>Tat tvam asi</em>: “You are that” (Chandogya Upanishad, Sama Veda).</li><li><em>Ayam Atma Brahma</em>: “This Self is Brahman” (Mandukya Upanishad, Atharva Veda).</li></ul>
<h3>Nachiketas and Death</h3>
<p>The Katha Upanishad tells of a boy, <strong>Nachiketas</strong>, who goes to the house of Yama, the god of death. Yama offers him three wishes. For the third, Nachiketas asks what happens after death. Yama tries to tempt him away with riches, long life and pleasures, but the boy refuses them all. Impressed, Yama teaches him that the Self is never born and never dies, and that it is found by those who choose the good over the merely pleasant.</p>
<h3>Prayers from the Upanishads</h3>
<p>Some of the best-loved Hindu prayers come from the Upanishads, such as <em>Asato ma sadgamaya</em>: “Lead me from the unreal to the real, from darkness to light, from death to immortality” (Brihadaranyaka 1.3.28), and the peace chants that begin and end their study, such as <em>Om saha navavatu</em> and <em>Purnamadah purnamidam</em>.</p>`,
      terms: [[`Upanishad`, `A philosophical teaching at the end of the Vedas.`], [`Mahavakya`, `One of the four “great sayings” of the Upanishads.`], [`Nachiketas`, `The boy who questioned Death in the Katha Upanishad.`]],
      practice: `Read the first part of the Katha Upanishad in the app. Then think: in your own life, where are you choosing between the good and the merely pleasant?`,
      links: [[`Read the Katha Upanishad`, `#/read/upanishads/2/1`], [`Asato Ma Sadgamaya`, `#/puja/asato-ma`], [`Purnamadah Purnamidam`, `#/puja/purnamadah`]]
    },
    {
      title: `Epics, Puranas and Agamas`, art: `lamp-book`,
      caption: `The stories that carry the Vedas' wisdom into every home.`,
      body: `<p>The Upanishads are profound, but they are not easy. Over the centuries, the sages found ways to bring their truths to everyone, through stories. The Bhagavata Purana says that Vyasa composed the Mahabharata out of compassion, so that the wisdom of the Vedas could reach all people, whatever their background.</p>
<h3>The Itihasas</h3>
<p>The two great epics, the <strong>Ramayana</strong> and the <strong>Mahabharata</strong>, are called <em>itihasa</em>, “so indeed it was,” sacred history. They teach dharma not through rules but through living characters facing real dilemmas. The Mahabharata, which contains the Bhagavad Gita, boasts: “What is found here may be found elsewhere; what is not found here is found nowhere.”</p>
<h3>The Puranas</h3>
<p>The <strong>Puranas</strong>, “ancient tales,” are great collections of stories about creation, the gods, the avatars, the sages and kings, along with instructions for worship, pilgrimage and festivals. There are eighteen major Puranas. Among the best known are:</p>
<ul><li>the <strong>Bhagavata Purana</strong>, which tells the life of Krishna and is the heart of Krishna devotion;</li><li>the <strong>Vishnu Purana</strong>, an early and systematic account of Vishnu, creation and the avatars;</li><li>the <strong>Shiva Purana</strong>, which tells the stories of Shiva, Parvati and their sons;</li><li>the <strong>Markandeya Purana</strong>, which contains the Devi Mahatmya, the great scripture of the Goddess.</li></ul>
<p>Most of the stories you hear at festivals, from Ganesha's elephant head to Prahlada and Narasimha, come from the Puranas.</p>
<h3>Agamas and Tantras</h3>
<p>The <strong>Agamas</strong> are the scriptures of temple worship. They describe how to build a temple, consecrate an image, and perform daily and festival worship, and they shape what happens in temples to this day. There are Shaiva Agamas, Vaishnava texts called the Pancharatra, and Shakta Tantras. They also teach meditation and the use of mantras and yantras.</p>
<p>Together with the poetry of the saints, these texts made the Vedic vision a living, breathing tradition, sung in villages, acted out in dramas and celebrated in temples.</p>`,
      terms: [[`Itihasa`, `“So it was”: the epics, sacred history.`], [`Purana`, `An “ancient tale”: a sacred story collection.`], [`Agama`, `A scripture of temple worship.`]],
      practice: `Choose one story you know only vaguely, such as the churning of the ocean or Prahlada, and read or listen to it properly this week.`,
      links: [[`Read the Vishnu Purana`, `#/read/vishnu`], [`Read the Mahabharata`, `#/read/mahabharata`]]
    },
    {
      title: `Where to begin reading`, art: `om`,
      caption: `Om, chanted at the start of every reading of scripture.`,
      body: `<p>With so many scriptures, where should you begin? Teachers' advice varies, but here is a path many have found helpful. Every book named below can be read in the Read tab of this app.</p>
<h3>A suggested path</h3>
<ul><li><strong>Start with the Bhagavad Gita.</strong> It is short, about seven hundred verses, and it gathers the essence of the Upanishads into one practical dialogue. Read a chapter a week, or follow the verse of the day on the Today page.</li><li><strong>Then the Ramayana.</strong> Its story is moving and easy to follow, and it shows dharma lived out in every relationship. The Sundara Kanda, Hanuman's journey, is a good place to dip in.</li><li><strong>Then the Isha and Katha Upanishads.</strong> The Isha is only eighteen verses; the Katha tells the story of Nachiketas and Death. Both are beautiful and profound.</li><li><strong>Then the Yoga Sutras</strong>, if you are drawn to meditation, and the <strong>Mahabharata</strong> or the <strong>Vishnu Purana</strong> when you are ready for a longer journey.</li></ul>
<h3>How to read scripture</h3>
<p>Scripture is not read like a newspaper. A few suggestions:</p>
<ul><li><strong>Begin with a prayer</strong>, such as Om or the Saha Navavatu peace chant, and a moment of silence.</li><li><strong>Read slowly</strong>, a little at a time. One verse, deeply understood, is worth more than a chapter skimmed.</li><li><strong>Read aloud</strong> when you can. These texts were made to be heard.</li><li><strong>Reflect and apply.</strong> Ask what the verse means for your life today. Use the app's notes feature to write down your thoughts.</li><li><strong>Learn from a teacher</strong>, or read with family or a study group. Many temples hold Gita classes.</li></ul>
<p>The tradition speaks of three steps: <em>shravana</em>, hearing the teaching; <em>manana</em>, reflecting on it until doubts are cleared; and <em>nididhyasana</em>, meditating on it until it becomes part of you.</p>`,
      terms: [[`Shravana`, `Hearing or reading the teaching.`], [`Manana`, `Reflecting on it deeply.`], [`Nididhyasana`, `Meditating on it until it becomes one's own.`]],
      practice: `Begin today: open the Bhagavad Gita in the app and read the first ten verses of chapter 2. Tap a verse you like and save a note about it.`,
      links: [[`Read the Bhagavad Gita`, `#/read/gita`], [`Read the Isha Upanishad`, `#/read/upanishads/1/1`], [`Om Saha Navavatu`, `#/puja/sahana`]]
    }
  ]
});

course({
  id: `gita`, deva: `गीता`, category: `scripture`, art: `chariot`,
  title: `Bhagavad Gita Essentials`,
  subtitle: `The Song of God in eight lessons`,
  intro: `The Bhagavad Gita is the best-loved scripture in Hinduism. These lessons walk through its key teachings, with links to read every chapter in the app.`,
  lessons: [
    {
      title: `The setting`, art: `chariot`,
      caption: `Arjuna's chariot, with Hanuman on its banner, drawn up between two armies.`,
      body: `<p>The <strong>Bhagavad Gita</strong>, “the Song of God,” is a dialogue of about seven hundred verses in eighteen chapters. It is part of the Mahabharata, in the Bhishma Parva, but it has long been treasured as a scripture of its own. Mahatma Gandhi called it his “eternal mother,” and it has been translated into almost every language on earth.</p>
<h3>Two armies</h3>
<p>The scene is the battlefield of <strong>Kurukshetra</strong>, just before the great war between the Pandavas and their cousins the Kauravas. The story is told by <strong>Sanjaya</strong>, who has been given divine sight, to the blind king <strong>Dhritarashtra</strong>, father of the Kauravas. The Gita opens with the king's anxious question: “On the field of dharma, at Kurukshetra, what did my sons and the sons of Pandu do?”</p>
<h3>Arjuna's despair</h3>
<p>The Pandava prince <strong>Arjuna</strong>, the greatest archer of his age, asks his charioteer, <strong>Krishna</strong>, to drive between the two armies so he can see whom he must fight. There he sees his grandfather Bhishma, his teacher Drona, his cousins, uncles and friends. Overcome with grief and confusion, his body trembling, his bow slipping from his hand, he sits down in the chariot and says he will not fight.</p>
<p>Arjuna's crisis is our own. We all face moments when duty and emotion pull in opposite directions, when we don't know what is right and feel unable to act. Arjuna does the wise thing: he admits his confusion and asks for guidance. “I am your disciple. Teach me, I have taken refuge in you” (2.7).</p>
<h3>An inner battlefield</h3>
<p>Many teachers read the Gita on two levels. It is a real conversation at a real moment in history. It is also a picture of the inner life: the body is the chariot, the senses are the horses, the mind holds the reins, and the divine Self is the charioteer. The battle is the struggle between our higher and lower tendencies, and Krishna's teaching is for anyone who must act in a confusing world.</p>`,
      terms: [[`Bhagavad Gita`, `“The Song of God”, a 700-verse dialogue in the Mahabharata.`], [`Kurukshetra`, `The battlefield where the Gita was spoken.`], [`Sanjaya`, `The narrator, who sees the battle with divine sight.`]],
      practice: `Read chapter 1 of the Gita in the app. Notice which of Arjuna's feelings you recognise from moments in your own life.`,
      links: [[`Read Bhagavad Gita, chapter 1`, `#/read/gita/1`], [`Bhagavad Gita 2.7: Arjuna asks for guidance`, `#/read/gita/2?v=7`]]
    },
    {
      title: `The eternal Self`, art: `sun-pots`,
      caption: `The Self in every being, untouched as the sun in its reflections.`,
      body: `<p>Krishna begins his teaching, in chapter 2, with the deepest truth of all: who we really are. Arjuna grieves because he thinks of his elders and teachers as bodies that will die. Krishna gently tells him he is grieving for what should not be grieved.</p>
<h3>Never born, never dying</h3>
<p>The true Self, the <strong>Atman</strong>, was never born and will never die. “It is not born, nor does it ever die. Having come to be, it will never cease to be. Unborn, eternal, ever-existing and ancient, it is not slain when the body is slain” (2.20). And again: “Weapons do not cut it, fire does not burn it, water does not wet it, and the wind does not dry it” (2.23).</p>
<p>The body changes from childhood to youth to old age, and the Self passes on to another body at death, just as we change clothes (2.22). The wise are not shaken by this.</p>
<h3>Steady in joy and sorrow</h3>
<p>Krishna also teaches equanimity. Heat and cold, pleasure and pain come and go; they are temporary, so bear them patiently (2.14). The person who stays balanced in success and failure, he says, is fit for immortality.</p>
<h3>The person of steady wisdom</h3>
<p>Arjuna asks: what is such a person like? How do they speak, sit and walk? Krishna's answer, at the end of chapter 2, describes the <strong>sthitaprajna</strong>, the one of steady wisdom. Such a person is free from craving, fear and anger; not elated by good fortune nor crushed by bad; and able to withdraw the senses from distractions as a tortoise draws in its limbs. Into them all desires flow like rivers into the ocean, which is filled yet stays still. Gandhi recited these verses every evening.</p>
<p>This teaching does not make us cold. Knowing that the Self is eternal frees us from panic, so that we can act with courage and compassion.</p>`,
      terms: [[`Atman`, `The eternal Self.`], [`Sthitaprajna`, `A person of steady wisdom.`], [`Equanimity`, `Remaining balanced in pleasure and pain, success and failure.`]],
      practice: `Next time you feel shaken by good or bad news, pause and recall Gita 2.14: “These come and go; they are not permanent. Bear them patiently.”`,
      links: [[`Read Bhagavad Gita, chapter 2`, `#/read/gita/2`], [`Gita 2.20: never born, never dying`, `#/read/gita/2?v=20`], [`Gita 2.55: the person of steady wisdom`, `#/read/gita/2?v=55`]]
    },
    {
      title: `Action without attachment`, art: `lotus`,
      caption: `Like a lotus leaf untouched by water, the karma yogi acts without being bound.`,
      body: `<p>If the Self is eternal and the world passing, should we simply withdraw from it? Arjuna asks exactly this. Krishna's answer, in chapters 3 to 5, is one of the Gita's great gifts to the world: <strong>karma yoga</strong>, the yoga of action.</p>
<h3>You cannot not act</h3>
<p>No one can remain without action even for a moment, Krishna says (3.5). Even keeping the body alive needs action. So the question is not whether to act, but how. Do your duty, he tells Arjuna: action is better than inaction (3.8).</p>
<h3>The famous verse</h3>
<blockquote><span class="deva">कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।</span>“You have a right to your actions, but never to their fruits. Let not the fruits of action be your motive, nor let yourself be attached to inaction.” (2.47)</blockquote>
<p>This does not mean we shouldn't care about results or plan well. It means we give our full effort and then let go of anxious clinging to the outcome, which was never fully in our control. Freed from that anxiety, we often act better.</p>
<h3>Offering every act</h3>
<p>The secret of karma yoga is to act as an offering. Do your work as worship, dedicating it to the divine, and accept whatever comes as a gift. Then, Krishna says, action does not bind us: “One who acts, offering all actions to Brahman and giving up attachment, is not touched by sin, as a lotus leaf is not wet by water” (5.10).</p>
<h3>For the good of the world</h3>
<p>Krishna also asks Arjuna to act for <em>loka sangraha</em>, the welfare of the world (3.20). Good people set an example that others follow. Even Krishna, who needs nothing, keeps acting so that the world does not fall into confusion.</p>
<p>Karma yoga turns everyday life, cooking, working, caring for family, into spiritual practice. It is perhaps the Gita's most practical teaching.</p>`,
      terms: [[`Karma yoga`, `The yoga of selfless action.`], [`Nishkama karma`, `Action without selfish desire for its fruits.`], [`Loka sangraha`, `Acting for the welfare of the world.`]],
      practice: `Choose one task today, at work or at home. Before it, say inwardly, “I offer this.” Do it as well as you can, and then let go of how it turns out.`,
      links: [[`Read Bhagavad Gita, chapter 3`, `#/read/gita/3`], [`Gita 2.47: your right is to action`, `#/read/gita/2?v=47`], [`Gita 5.10: the lotus leaf`, `#/read/gita/5?v=10`]]
    },
    {
      title: `The yoga of meditation`, art: `flame`,
      caption: `“As a lamp in a windless place does not flicker”: the still mind of the yogi.`,
      body: `<p>Chapter 6 of the Gita is Krishna's teaching on <strong>dhyana yoga</strong>, the yoga of meditation. It is one of the clearest, most practical guides to meditation in any scripture.</p>
<h3>How to sit</h3>
<p>Krishna describes the practice simply. Find a clean, quiet place. Make a firm seat, neither too high nor too low. Sit with the body, head and neck straight and still. Gaze steadily, without looking around, and bring the mind to rest on the divine (6.11–14).</p>
<h3>Not too much, not too little</h3>
<p>Yoga is not for one who eats too much or too little, sleeps too much or too little, Krishna says. It is for one who is moderate in food, rest, work and recreation (6.16–17). The Gita's way is balance, not extremes.</p>
<h3>The windless lamp</h3>
<blockquote><span class="deva">यथा दीपो निवातस्थो नेङ्गते सोपमा स्मृता।</span>“As a lamp in a windless place does not flicker: that is the image of the yogi whose mind is controlled.” (6.19)</blockquote>
<h3>The restless mind</h3>
<p>Arjuna, honest as ever, protests: the mind is restless, turbulent and strong, as hard to control as the wind (6.34). Krishna agrees. But, he says, it can be tamed by two things: <strong>abhyasa</strong>, steady practice, and <strong>vairagya</strong>, detachment (6.35). Whenever the mind wanders, bring it back, gently, again and again (6.26).</p>
<h3>Lift yourself</h3>
<p>Chapter 6 also contains a verse many people carry with them: “Lift yourself by your own self; do not let yourself sink. The self alone is your friend, and the self alone is your enemy” (6.5). And Krishna reassures Arjuna that anyone who sincerely tries, even if they fall short in this life, is never lost: their effort carries them forward (6.40).</p>`,
      terms: [[`Dhyana`, `Meditation.`], [`Abhyasa`, `Steady, repeated practice.`], [`Vairagya`, `Detachment, letting go.`]],
      practice: `Sit for five minutes as Gita 6.11 to 6.14 describes. Each time your mind wanders, gently bring it back, without scolding. Each return is the practice.`,
      links: [[`Read Bhagavad Gita, chapter 6`, `#/read/gita/6`], [`Gita 6.19: the windless lamp`, `#/read/gita/6?v=19`], [`Course: Meditation and Mantra`, `#/academy/meditation`]]
    },
    {
      title: `The path of devotion`, art: `leaf-flower-fruit`,
      caption: `A leaf, a flower, a fruit and water, offered with love.`,
      body: `<p>In the middle chapters of the Gita, 7 to 12, Krishna speaks more and more openly about himself as the Supreme, and about <strong>bhakti</strong>, loving devotion, as the most direct path to him.</p>
<h3>The simplest offering</h3>
<blockquote><span class="deva">पत्रं पुष्पं फलं तोयं यो मे भक्त्या प्रयच्छति।</span>“Whoever offers me with devotion a leaf, a flower, a fruit or water, that offering of love from a pure heart I accept.” (9.26)</blockquote>
<p>God does not need anything from us. What matters is the love with which we give. The next verse goes further: whatever you do, whatever you eat, whatever you offer or give, do it as an offering to me (9.27). All of life can become worship.</p>
<h3>He carries what we lack</h3>
<p>To those who worship him with single-minded love, Krishna promises: “I carry what they lack and preserve what they have” (9.22). This verse, <em>yoga kshemam vahamyaham</em>, is the motto of countless Hindu institutions.</p>
<h3>The divine in all things</h3>
<p>In chapter 10, Krishna describes his glories, the <em>vibhutis</em>: among lights he is the radiant sun, among rivers the Ganga, among mountains the Himalaya, among words the syllable Om. Wherever there is anything glorious, beautiful or powerful, know that it comes from a spark of his splendour (10.41).</p>
<h3>The qualities of a devotee</h3>
<p>Chapter 12, the shortest, is devoted to bhakti. Krishna describes the devotee who is dear to him: one who hates no being, who is friendly and compassionate, free from selfishness and pride, balanced in pleasure and pain, forgiving and content; one who is not a source of fear to the world and does not fear the world (12.13–15). These verses are a portrait of a beautiful human being.</p>`,
      terms: [[`Bhakti`, `Loving devotion.`], [`Vibhuti`, `A divine glory or manifestation.`], [`Yoga kshema`, `Gaining what is needed and keeping what is gained.`]],
      practice: `Offer something small today, a flower, a fruit or a glass of water, with love. Then read the qualities of a devotee in Gita 12.13 to 12.20, and choose one to practise.`,
      links: [[`Read Bhagavad Gita, chapter 9`, `#/read/gita/9`], [`Read Bhagavad Gita, chapter 12`, `#/read/gita/12`], [`Gita 9.26: a leaf, a flower`, `#/read/gita/9?v=26`]]
    },
    {
      title: `The cosmic form`, art: `cosmos`,
      caption: `The universal form: all worlds and all time within the divine.`,
      body: `<p>In chapter 11, Arjuna, deeply moved by all he has heard, makes a bold request: “If you think I am able to see it, show me your imperishable universal form” (11.4). Krishna grants him divine eyes, because no human eye could bear what he is about to see.</p>
<h3>The vision</h3>
<p>Arjuna sees the <strong>Vishvarupa</strong>, the cosmic form. If a thousand suns rose at once in the sky, their light might resemble the splendour of that being (11.12). Within Krishna's body he sees the entire universe: all the gods, all beings, the sages, rivers and mountains, with countless arms, faces and eyes, without beginning, middle or end.</p>
<p>Then the vision turns terrifying. Arjuna sees the warriors of both armies rushing into Krishna's flaming mouths, like moths into a fire or rivers into the sea. Krishna declares: “I am Time, the mighty destroyer of worlds” (11.32). The outcome of the battle is already decided; Arjuna is only to be the instrument.</p>
<h3>Arjuna's fear and love</h3>
<p>Trembling, Arjuna praises Krishna and begs forgiveness for every time he treated him casually as a friend, joking with him or calling him by name. He asks to see again the gentle, familiar form he loves. Krishna returns to his four-armed form and then to his human form, and Arjuna is calm again.</p>
<h3>What the vision teaches</h3>
<p>The cosmic form shows that God is not small. The divine includes everything: beauty and terror, creation and destruction, birth and death, all of time. Yet the same infinite reality chooses to sit beside us as a friend and charioteer.</p>
<p>Krishna ends the chapter by saying that this form cannot be seen by study, austerity, charity or ritual alone, but only by single-minded devotion (11.53–54). The vastness of God and the intimacy of love belong together.</p>`,
      terms: [[`Vishvarupa`, `The universal or cosmic form of God.`], [`Divya chakshu`, `The divine eye given to Arjuna.`], [`Kala`, `Time, the destroyer of worlds.`]],
      practice: `Look at the night sky, or a photograph of a galaxy. Then think of the verse “if a thousand suns rose at once.” Sit with that sense of vastness, and of being held within it.`,
      links: [[`Read Bhagavad Gita, chapter 11`, `#/read/gita/11`], [`Gita 11.12: a thousand suns`, `#/read/gita/11?v=12`]]
    },
    {
      title: `The three gunas`, art: `three-strands`,
      caption: `Three strands woven together: sattva, rajas and tamas.`,
      body: `<p>In chapters 14, 17 and 18, the Gita offers a practical tool for understanding ourselves and the world: the three <strong>gunas</strong>, the qualities of nature, drawn from Samkhya philosophy.</p>
<ul><li><strong>Sattva</strong>: purity, light, harmony and knowledge. It binds through attachment to happiness and understanding.</li><li><strong>Rajas</strong>: passion, energy, desire and restless activity. It binds through attachment to action and its fruits.</li><li><strong>Tamas</strong>: heaviness, darkness, inertia and confusion. It binds through carelessness, laziness and sleep.</li></ul>
<p>All three are present in everything and everyone, in shifting proportions. Each, in turn, rises and overpowers the others (14.10).</p>
<h3>The gunas in daily life</h3>
<p>Chapter 17 applies the gunas to food, worship, austerity and giving. Sattvic food is fresh, wholesome and nourishing; rajasic food is very spicy, salty or bitter and leads to agitation; tamasic food is stale, overcooked or spoiled (17.8–10). This teaching is one reason many Hindus value a simple vegetarian diet.</p>
<p>Chapter 18 does the same for knowledge, action, understanding and happiness. Sattvic happiness, for example, “seems like poison at first but is like nectar in the end,” such as the joy of discipline; rajasic happiness is nectar at first and poison in the end, such as overindulgence (18.37–38).</p>
<h3>Beyond the gunas</h3>
<p>The goal is not just to increase sattva, though that helps, but finally to go beyond all three. Krishna describes the one who has risen above the gunas: they watch the qualities come and go without being disturbed, “the gunas are acting on the gunas,” and remain the same in honour and dishonour, pleasure and pain (14.22–25). The way beyond, he says, is unwavering devotion (14.26).</p>`,
      terms: [[`Sattva`, `Purity, clarity and harmony.`], [`Rajas`, `Passion and restless activity.`], [`Tamas`, `Inertia, heaviness and darkness.`], [`Gunatita`, `One who has gone beyond the three gunas.`]],
      practice: `For three days, notice how what you eat affects your mood and energy. Try choosing one more sattvic meal each day and see what changes.`,
      links: [[`Read Bhagavad Gita, chapter 14`, `#/read/gita/14`], [`Read Bhagavad Gita, chapter 17`, `#/read/gita/17`]]
    },
    {
      title: `Surrender`, art: `hands-offering`,
      caption: `Open hands: the Gita's final teaching is surrender to the divine.`,
      body: `<p>The eighteenth and longest chapter gathers together the whole teaching of the Gita: renunciation, the three gunas, duty and devotion. And then, near the end, Krishna gives what he calls his most secret teaching.</p>
<h3>The final word</h3>
<blockquote><span class="deva">सर्वधर्मान्परित्यज्य मामेकं शरणं व्रज।<br>अहं त्वा सर्वपापेभ्यो मोक्षयिष्यामि मा शुचः॥</span>“Setting aside all duties, take refuge in me alone. I will free you from all sins. Do not grieve.” (18.66)</blockquote>
<p>This verse is called the <em>charama shloka</em>, the ultimate verse, by many Vaishnava teachers. It is the Gita's deepest consolation: after all the effort, discipline and understanding, the final step is to let go and trust. We are not alone. The divine is ready to carry us, if we allow it.</p>
<h3>Surrender is not giving up</h3>
<p>Surrender, <strong>sharanagati</strong>, does not mean doing nothing. Arjuna surrenders and then picks up his bow. It means acting fully while trusting completely, giving up the burden of the ego that thinks everything depends on us.</p>
<h3>Freedom to choose</h3>
<p>Remarkably, Krishna does not command Arjuna. Having taught him everything, he says: “Reflect on this fully, and then do as you wish” (18.63). The Gita respects human freedom. Truth is offered, never forced.</p>
<h3>Arjuna's answer</h3>
<p>Arjuna replies: “My delusion is gone. I have regained my memory through your grace. I stand firm, free from doubt. I will do as you say” (18.73). The confusion of chapter 1 has become clarity and courage.</p>
<p>The Gita closes with Sanjaya's words: “Wherever there is Krishna, the lord of yoga, and wherever there is Arjuna, the archer, there will surely be fortune, victory, prosperity and sound judgement” (18.78). Where the divine and the human work together, all is well.</p>
<p>The day the Gita was spoken is celebrated as <strong>Gita Jayanti</strong>, on Mokshada Ekadashi in the month of Margashirsha.</p>`,
      terms: [[`Sharanagati`, `Surrender; taking refuge in God.`], [`Charama shloka`, `“The ultimate verse”: Gita 18.66.`], [`Gita Jayanti`, `The anniversary of the Gita, on Mokshada Ekadashi.`]],
      practice: `Write down a worry you cannot control. Read Gita 18.66, then symbolically hand the worry over, by placing the paper at your shrine or simply saying, “I leave this with you.”`,
      links: [[`Read Bhagavad Gita, chapter 18`, `#/read/gita/18`], [`Gita 18.66: take refuge in me`, `#/read/gita/18?v=66`], [`Tvameva Mata`, `#/puja/tvameva`]]
    }
  ]
});

course({
  id: `epics`, deva: `इतिहास`, category: `scripture`, art: `bow`,
  title: `The Great Epics`,
  subtitle: `The Ramayana and the Mahabharata`,
  intro: `Two of the longest and best-loved poems in the world. Six lessons on their stories, their unforgettable characters and what they teach about living rightly.`,
  lessons: [
    {
      title: `The story of the Ramayana`, art: `bow`,
      caption: `Rama's bow, which only he could string.`,
      body: `<p>The <strong>Ramayana</strong>, “the journey of Rama,” is attributed to the sage <strong>Valmiki</strong>, honoured as the <em>adi kavi</em>, the first poet. It has about 24,000 verses in seven books, or kandas. Its story is known to almost every Hindu child.</p>
<h3>Ayodhya and exile</h3>
<p><strong>Rama</strong> is the eldest son of King Dasharatha of Ayodhya, loved by all. As a young man he wins the hand of princess <strong>Sita</strong> by lifting and stringing the mighty bow of Shiva, which no one else could even move. On the eve of Rama's coronation, his stepmother Kaikeyi, using two boons the king once promised her, demands that her own son <strong>Bharata</strong> be crowned instead, and that Rama be exiled to the forest for fourteen years. Bound by his word, the king agrees, and dies of grief. Rama accepts calmly and goes, with Sita and his devoted brother <strong>Lakshmana</strong>.</p>
<h3>The abduction</h3>
<p>Years later, in the forest, the demon king <strong>Ravana</strong> of Lanka sends a magical golden deer to lure Rama and Lakshmana away. Disguised as a holy man, Ravana carries Sita off in his flying chariot. The old vulture Jatayu fights to save her and is mortally wounded.</p>
<h3>Allies and victory</h3>
<p>Searching for Sita, Rama befriends the vanara king Sugriva and his minister <strong>Hanuman</strong>, who leaps across the ocean, finds Sita in Lanka and brings back news. The vanara army builds a bridge of floating stones across the sea, the Rama Setu, and a great battle follows. Rama finally defeats Ravana, Sita is freed, and after fourteen years they return to Ayodhya, where Rama is crowned. His reign, <strong>Rama Rajya</strong>, becomes the ideal of a just and happy kingdom.</p>
<h3>A living story</h3>
<p>The Ramayana has been retold in every Indian language and across Asia: Tulsidas's <em>Ramcharitmanas</em> in Hindi, Kamban's Tamil Ramayana, the Thai <em>Ramakien</em>, and versions in Indonesia, Cambodia and beyond. Every autumn it is acted out in the <strong>Ram Lila</strong>, ending at Dussehra with the burning of Ravana's effigy. In North India, Diwali celebrates Rama's homecoming, when the people of Ayodhya lit lamps to welcome him.</p>`,
      terms: [[`Kanda`, `A book or section of the Ramayana.`], [`Rama Setu`, `The bridge built across the sea to Lanka.`], [`Rama Rajya`, `The just and happy reign of Rama, an ideal of good government.`]],
      practice: `Retell the story of the Ramayana in five sentences, to yourself or a child. Then pick the one moment that moves you most, and ask why.`,
      links: [[`Read the Ramayana`, `#/read/ramayana`], [`Shri Ramachandra Kripalu`, `#/puja/ramchandra-kripalu`], [`Diwali`, `#/festival/diwali`]]
    },
    {
      title: `The people of the Ramayana`, art: `sandals`,
      caption: `Rama's sandals on the throne, where Bharata placed them.`,
      body: `<p>The Ramayana is above all a story about character. Each figure shows a different face of dharma, and each is still held up as a model, or a warning.</p>
<h3>Bharata and the sandals</h3>
<p>When <strong>Bharata</strong> learned that he had been made king through his mother's scheming, he was horrified. He went to the forest and begged Rama to return. Rama refused to break their father's word. So Bharata took Rama's wooden sandals, his <em>paduka</em>, placed them on the throne and ruled for fourteen years only as Rama's servant, living simply in a village outside the capital. The sandals on the throne are a lasting symbol of selfless love and loyalty.</p>
<h3>Lakshmana</h3>
<p><strong>Lakshmana</strong> left his comfortable life and his wife to serve Rama and Sita in the forest, guarding them day and night. He stands for devotion between brothers and tireless service.</p>
<h3>Sita</h3>
<p><strong>Sita</strong> chose to share Rama's exile rather than stay in the palace. Held captive in Lanka, she refused all of Ravana's threats and temptations, sustained by her love and faith. She is honoured as a figure of great inner strength, courage and dignity. Many readers also find in her later sufferings a call to think deeply about fairness and the treatment of women, and the tradition has always held both her strength and her pain with reverence.</p>
<h3>Shabari, Jatayu and Vibhishana</h3>
<p><strong>Shabari</strong>, an old forest woman of humble birth, waited years for Rama and offered him berries she had tasted first, to be sure they were sweet. Rama ate them with joy, showing that God looks only at love. <strong>Jatayu</strong>, the aged vulture, gave his life trying to save Sita. <strong>Vibhishana</strong>, Ravana's own brother, urged him to return Sita and, when refused, left Lanka to join Rama, choosing dharma over family loyalty.</p>
<h3>Ravana</h3>
<p><strong>Ravana</strong> was not simply a monster. He was a great scholar, a mighty king and a devotee of Shiva. His downfall came from pride and desire. His story warns that learning and power without self-control lead to ruin.</p>`,
      terms: [[`Paduka`, `Wooden sandals; Rama's, placed on the throne by Bharata.`], [`Shabari`, `The forest devotee who offered Rama berries.`], [`Vibhishana`, `Ravana's brother, who joined Rama for the sake of dharma.`]],
      practice: `Which character in the Ramayana are you most like, and which would you like to be more like? Write down one quality of theirs to practise this week.`,
      links: [[`Read the Ramayana: Ayodhya Kanda`, `#/read/ramayana/2`], [`Ramaya Ramabhadraya`, `#/puja/ramaya`]]
    },
    {
      title: `The story of the Mahabharata`, art: `dice`,
      caption: `The fateful game of dice that set the great war in motion.`,
      body: `<p>The <strong>Mahabharata</strong>, attributed to the sage <strong>Vyasa</strong>, is one of the longest poems ever composed: about 100,000 verses in eighteen books, or parvas, nearly ten times the length of the Iliad and Odyssey together. It tells the story of a royal family torn apart.</p>
<h3>Two sets of cousins</h3>
<p>In the kingdom of Hastinapura, two brothers had sons. The five sons of Pandu, the <strong>Pandavas</strong>, were Yudhishthira, the just; Bhima, the strong; Arjuna, the great archer; and the twins Nakula and Sahadeva. The hundred sons of the blind king Dhritarashtra, the <strong>Kauravas</strong>, were led by the jealous <strong>Duryodhana</strong>. From childhood, Duryodhana resented the Pandavas and tried again and again to destroy them.</p>
<h3>The game of dice</h3>
<p>The Pandavas married <strong>Draupadi</strong> and built a magnificent kingdom at Indraprastha. Consumed by envy, Duryodhana and his uncle Shakuni invited Yudhishthira to a game of dice, played by the cunning Shakuni, who could not lose. Yudhishthira lost everything: his wealth, his kingdom, his brothers, himself and finally Draupadi. Draupadi was dragged into the court and the Kauravas tried to strip her, but Krishna protected her with an endless sari. The Pandavas were sent into exile for thirteen years.</p>
<h3>The war</h3>
<p>When the exile ended, Duryodhana refused to return their kingdom, or even five villages. War became inevitable. The armies met at <strong>Kurukshetra</strong>, and before the first arrow flew, Krishna spoke the Bhagavad Gita to Arjuna. The battle lasted eighteen days. Almost every warrior on both sides was killed, including Bhishma, Drona, Karna and all hundred Kaurava brothers. The Pandavas won, but at a terrible cost.</p>
<h3>After the war</h3>
<p>The dying <strong>Bhishma</strong>, lying on a bed of arrows, taught Yudhishthira about dharma, kingship and liberation, including the thousand names of Vishnu. Yudhishthira ruled justly for many years. At last the Pandavas set out on a final journey to the Himalayas, followed by a faithful dog. One by one the others fell, until only Yudhishthira and the dog remained. He refused to enter heaven without the dog, which then revealed itself as Dharma, the god of righteousness, in disguise.</p>`,
      terms: [[`Parva`, `A book of the Mahabharata; there are eighteen.`], [`Pandavas`, `The five sons of Pandu, heroes of the epic.`], [`Kauravas`, `The hundred sons of Dhritarashtra, led by Duryodhana.`]],
      practice: `Read the opening of the Mahabharata in the app, or the story of Yudhishthira and the dog. Ask yourself what loyalty means to you.`,
      links: [[`Read the Mahabharata`, `#/read/mahabharata`], [`Course: Bhagavad Gita Essentials`, `#/academy/gita`]]
    },
    {
      title: `The people of the Mahabharata`, art: `conch`,
      caption: `The conch shells blown by the heroes at the start of the battle.`,
      body: `<p>The Mahabharata's characters are deeply human: brave and flawed, noble and torn. That is why the epic still feels so true. Here are a few of them.</p>
<h3>Bhishma</h3>
<p><strong>Bhishma</strong>, the grand-uncle of both sides, took a terrible vow as a young man never to marry or claim the throne, so that his father could marry again. He kept it all his life, and was granted the power to choose the hour of his own death. Yet his rigid loyalty to the throne kept him fighting on the Kaurava side, against those he knew were right.</p>
<h3>Karna</h3>
<p><strong>Karna</strong> was secretly the eldest son of Kunti, the Pandavas' mother, abandoned at birth and raised by a charioteer. Mocked for his low status, he was befriended by Duryodhana and stayed loyal to him to the end, even after learning the truth of his birth. Famous for his generosity, he never refused anyone who asked him for a gift. He is perhaps the epic's most tragic hero.</p>
<h3>Draupadi</h3>
<p><strong>Draupadi</strong>, born from a sacrificial fire, was fierce, intelligent and proud. In the royal court, she challenged the elders with a question none could answer: if her husband had already lost himself, what right did he have to stake her? Her courage and her demand for justice drive much of the story.</p>
<h3>Yudhishthira and Arjuna</h3>
<p><strong>Yudhishthira</strong>, the eldest Pandava, was called Dharmaraja, king of righteousness, and was said never to lie. Yet his weakness for gambling cost his family everything. When a mysterious spirit, a yaksha, tested him with riddles at a lake, his wise answers saved his brothers' lives. <strong>Arjuna</strong>, the peerless archer, was so focused that, as a student, he saw only the eye of the target bird. It was his doubt and despair that drew out the Gita.</p>
<h3>Gandhari and Vidura</h3>
<p><strong>Gandhari</strong>, wife of the blind king, chose to blindfold herself for life to share his darkness, yet told her son Duryodhana, “Where there is dharma, there is victory.” <strong>Vidura</strong>, the king's wise half-brother, spoke truth to power again and again, though he was rarely heeded.</p>`,
      terms: [[`Bhishma`, `The grand-uncle who kept a lifelong vow.`], [`Karna`, `The generous, tragic warrior, Kunti's eldest son.`], [`Yaksha prashna`, `The riddles of the yaksha, answered by Yudhishthira.`]],
      practice: `Karna, Bhishma and Yudhishthira all had great virtues and serious flaws. Think of a virtue of yours that can turn into a flaw when overdone, and how to keep it in balance.`,
      links: [[`Read the Mahabharata`, `#/read/mahabharata`]]
    },
    {
      title: `Dharma is subtle`, art: `scales`,
      caption: `The scales of dharma, never as simple as they seem.`,
      body: `<p>If the Ramayana shows dharma in its clear, ideal form, the Mahabharata shows how hard dharma can be to see. Its characters face situations where every choice seems to break some duty. Again and again, the epic says: <em>dharmasya tattvam nihitam guhayam</em>, “the truth of dharma is hidden in a cave.”</p>
<h3>Hard cases</h3>
<ul><li><strong>Bhishma's vow.</strong> Keeping one's word is dharma. But Bhishma's vow bound him to defend a throne that had become unjust. Was keeping it right?</li><li><strong>Yudhishthira's half-truth.</strong> To stop the invincible Drona, the Pandavas spread word that Drona's son Ashvatthama was dead. In fact an elephant of that name had been killed. Yudhishthira, who never lied, said, “Ashvatthama is dead,” and then quietly, “the elephant.” Drona laid down his arms. Even this half-truth cost Yudhishthira: his chariot, which had always floated above the ground, sank to earth.</li><li><strong>Karna's loyalty.</strong> Gratitude and loyalty are virtues. But they kept Karna on the side of injustice, against his own brothers.</li></ul>
<h3>How to decide</h3>
<p>The tradition does not pretend these questions are easy, but it offers guidance. The Mahabharata gives a golden rule: “Do not do to others what you would not want done to yourself; this is the essence of dharma.” It also points to the scriptures, to the example of good and wise people, to one's own conscience, and to a principle that runs through the whole epic: protect the vulnerable, and choose what serves the greater good.</p>
<p>When Arjuna is paralysed by such a dilemma, Krishna does not give him a simple rule. He teaches him to see more deeply: to act from duty rather than self-interest, without hatred, and as an offering.</p>
<h3>Why it matters</h3>
<p>Life rarely presents clean choices between good and evil. The Mahabharata prepares us for real moral life, with compassion for those who struggle and stumble. It is said that whatever is found in it can be found elsewhere, and what is not found in it cannot be found anywhere.</p>`,
      terms: [[`Dharma sankata`, `A moral dilemma, where duties conflict.`], [`Ahimsa`, `Non-violence, often weighed against other duties.`]],
      practice: `Think of a time you faced two duties that pulled in different directions. How did you decide? Would you decide the same way now?`,
      links: [[`Course: Dharma in Daily Life`, `#/academy/dharma`]]
    },
    {
      title: `Lessons for today`, art: `lamp-book`,
      caption: `The epics, still read by lamplight in homes around the world.`,
      body: `<p>The Ramayana and the Mahabharata are thousands of years old, but their lessons are as fresh as today's news. Families have read them aloud for generations, and every reading reveals something new.</p>
<h3>From the Ramayana</h3>
<ul><li><strong>Keep your word, even when it costs you.</strong> Rama gave up a kingdom rather than let his father break a promise.</li><li><strong>Love is shown in service.</strong> Lakshmana, Bharata and Hanuman all served without seeking anything.</li><li><strong>Devotion makes us stronger than we know.</strong> Hanuman crossed the ocean with Rama's name on his lips.</li><li><strong>Pride and desire can ruin even the greatest.</strong> Ravana had learning, power and wealth, and lost everything.</li><li><strong>God values love, not status.</strong> Rama ate Shabari's tasted berries with joy.</li></ul>
<h3>From the Mahabharata</h3>
<ul><li><strong>Envy destroys families.</strong> Duryodhana's jealousy led to the deaths of almost everyone he loved.</li><li><strong>Silence in the face of injustice is a choice.</strong> The elders who said nothing while Draupadi was humiliated shared the blame.</li><li><strong>Addictions can cost everything.</strong> Yudhishthira's love of gambling lost a kingdom.</li><li><strong>Seek wise counsel in a crisis.</strong> Arjuna turned to Krishna, and found clarity.</li><li><strong>Victory has a cost.</strong> The Pandavas won the war but wept over the dead.</li></ul>
<h3>Reading them as a family</h3>
<p>The epics are wonderful to share. Many families read a section each evening, watch the classic television series together, or attend the Ram Lila in autumn. Children love the adventures; adults find depths they missed before. Asking simple questions, such as “What would you have done?”, can open the best conversations.</p>
<p>In the end, both epics ask the same question in different ways: how can a person live with courage, kindness and integrity in a complicated world? Their answer is not a rule but a way of seeing, learned through stories.</p>`,
      terms: [[`Ram Lila`, `The traditional dramatic performance of the Ramayana.`], [`Itihasa`, `“So it was”: the epics as sacred history.`]],
      practice: `This week, read one episode of the Ramayana or Mahabharata with someone else, and ask each other: “What would you have done?”`,
      links: [[`Read the Ramayana`, `#/read/ramayana`], [`Read the Mahabharata`, `#/read/mahabharata`]]
    }
  ]
});

/* ---------------------------------------------------------------------- */
/* Practice                                                                */
/* ---------------------------------------------------------------------- */
course({
  id: `puja`, deva: `पूजा`, category: `practice`, art: `shrine`,
  title: `Daily Puja at Home`,
  subtitle: `A simple, heartfelt practice`,
  intro: `You don't need a priest or a temple to worship. Five lessons on setting up a home shrine and offering a simple daily puja, step by step.`,
  lessons: [
    {
      title: `The home shrine`, art: `shrine`,
      caption: `A small home shrine, the heart of a Hindu home.`,
      body: `<p>Almost every Hindu home has a shrine, a <strong>mandir</strong> or puja room. It may be a whole room, a carved wooden cabinet, a shelf, or a small corner with a single picture and a lamp. Its size doesn't matter. What matters is that it is a place set apart for the divine, kept clean and visited with love every day.</p>
<h3>Where to place it</h3>
<p>Traditional guidance, drawn from Vastu Shastra, suggests the north-east corner of the home, the direction of sunrise and auspicious beginnings, with the images facing east or west, so that you face east or north while praying. Shrines are traditionally kept out of bedrooms and away from bathrooms. But don't worry if your home doesn't allow this. A clean, quiet, respectful spot is what counts.</p>
<h3>What to put in it</h3>
<ul><li><strong>Images</strong>: a murti (statue) or pictures of your ishta devata and family deities. Ganesha is almost always included.</li><li><strong>A lamp</strong>, or diya, with ghee or oil and a cotton wick.</li><li><strong>An incense holder</strong>, and a small bell.</li><li><strong>A small water pot</strong> (kalash or lota) and spoon.</li><li><strong>Small bowls</strong> for kumkum, sandalwood paste, turmeric and rice.</li><li><strong>A plate</strong> (thali) for offerings, and fresh flowers when you can.</li></ul>
<p>Many people also keep a copy of the Bhagavad Gita or the Hanuman Chalisa, a conch, and photographs of departed elders, though these are often kept slightly apart from the deities.</p>
<h3>Keeping it sacred</h3>
<p>Keep the shrine clean and uncluttered. Replace flowers before they wilt and offer fresh water daily. Some families cover the shrine or close its doors at night, as a way of letting the deities rest. Above all, treat the shrine as a living presence, not a decoration: a place where the divine is welcomed as a beloved guest.</p>`,
      terms: [[`Mandir`, `A temple, or the shrine in a home.`], [`Murti`, `A sacred image or statue of a deity.`], [`Vastu Shastra`, `The traditional science of architecture and space.`]],
      practice: `Look at your shrine, or choose a spot for one. Clean it today, place a fresh flower and a lamp, and sit there quietly for two minutes.`
    },
    {
      title: `Preparing for puja`, art: `puja-items`,
      caption: `Bell, conch and kalash, ready for worship.`,
      body: `<p>Puja begins before the first flower is offered. A little preparation helps the mind settle and turns an ordinary moment into a sacred one.</p>
<h3>When to worship</h3>
<p>The most traditional times are at dawn and at dusk, the meeting points of night and day, called <strong>sandhya</strong>. The hour and a half before sunrise, <strong>brahma muhurta</strong>, is considered especially peaceful and powerful for prayer. But any regular time works. Consistency matters more than the exact hour.</p>
<h3>Preparing yourself</h3>
<ul><li><strong>Bathe</strong>, or at least wash your hands, feet and face, and rinse your mouth.</li><li><strong>Wear clean clothes</strong>. Many people keep simple cotton clothes just for puja.</li><li><strong>Calm the mind</strong>. Take a few slow breaths before you begin.</li></ul>
<h3>Preparing the space</h3>
<ul><li>Remove yesterday's flowers and offerings, and wipe the shrine.</li><li>Fill the water pot with fresh water.</li><li>Prepare the lamp, incense, flowers and a small offering of food, such as fruit, sweets, or a portion of the meal before it is served.</li><li>Arrange everything on the puja thali within easy reach, so you won't need to get up.</li></ul>
<h3>The sankalpa</h3>
<p>Formal pujas begin with a <strong>sankalpa</strong>, a statement of intention, in which the worshipper names the time, the place, themselves and the purpose of the puja. At home this can be very simple. Hold a little water and a few grains of rice in your right palm, and say in your own words what you are offering this puja for: perhaps gratitude, peace in the family, or a loved one's health. Then let the water flow onto a plate.</p>
<h3>Acamana and Ganesha</h3>
<p>Many people sip a few drops of water from the right palm three times, a purification called <strong>acamana</strong>. Then, before anything else, they invoke Ganesha, remover of obstacles, with a short prayer such as <em>Vakratunda Mahakaya</em>.</p>`,
      terms: [[`Sandhya`, `Twilight, dawn and dusk: the junctions of the day.`], [`Brahma muhurta`, `The peaceful hour and a half before sunrise.`], [`Sankalpa`, `A statement of intention at the start of worship.`]],
      practice: `Tomorrow morning, before your usual routine, wash, light a lamp and make a simple sankalpa in your own words. Notice how it shapes your day.`,
      links: [[`Vakratunda Mahakaya`, `#/puja/ganesha`], [`Karagre Vasate: the morning prayer`, `#/puja/morning`]]
    },
    {
      title: `A simple puja, step by step`, art: `thali`,
      caption: `The puja thali: lamp, kumkum, rice, flowers and incense.`,
      body: `<p>A full formal puja may include sixteen offerings, the <strong>shodashopachara</strong>, from inviting the deity and offering a seat to bathing, dressing and decorating the image. For daily worship at home, most families use five, the <strong>panchopachara</strong>. Here is a simple form you can follow in ten minutes.</p>
<h3>The five offerings</h3>
<ol><li><strong>Gandha</strong>, fragrance: apply a little sandalwood paste or kumkum to the deity, with the ring finger of your right hand. You may also offer a few grains of unbroken rice, <em>akshata</em>.</li><li><strong>Pushpa</strong>, flowers: offer fresh flowers or petals, at the feet of the deity. Each deity has favourites: hibiscus for Ganesha and the Goddess, bilva leaves for Shiva, tulsi for Vishnu and Krishna.</li><li><strong>Dhupa</strong>, incense: wave a lit incense stick slowly in clockwise circles before the deity.</li><li><strong>Dipa</strong>, light: wave the lamp in clockwise circles, perhaps while ringing the bell.</li><li><strong>Naivedya</strong>, food: place the food offering before the deity, sprinkle a little water around it, and silently invite the deity to accept it. After a few moments it becomes <strong>prasad</strong>, blessed food.</li></ol>
<h3>Prayers and mantras</h3>
<p>Between the offerings, or after them, chant the prayers you know: the Gayatri Mantra, a short shloka, the name of your deity, or simply speak from the heart. The words matter less than the feeling behind them. Many families end with an aarti and the prayer <em>Karpura Gauram</em>.</p>
<h3>Closing</h3>
<p>Finish by bowing, either a simple namaste or a full prostration, and asking forgiveness for any mistakes, with a prayer such as <em>Kara Charana Kritam</em>. Then sit quietly for a moment before you rise.</p>
<p>Don't worry about doing everything perfectly. Hindu tradition says that the Lord looks at the heart. A single flower offered with love is a complete puja.</p>`,
      terms: [[`Panchopachara`, `The five offerings: fragrance, flowers, incense, light and food.`], [`Naivedya`, `Food offered to the deity.`], [`Prasad`, `Blessed food, received back after offering.`], [`Akshata`, `Unbroken rice grains used in worship.`]],
      practice: `Offer the five offerings once this week, slowly, using what you have. If you don't have sandalwood, offer water; if you don't have flowers, offer a leaf.`,
      links: [[`Gayatri Mantra`, `#/puja/gayatri`], [`Karpura Gauram`, `#/puja/karpura-gauram`], [`Kara Charana Kritam`, `#/puja/kara-charana`]]
    },
    {
      title: `Aarti and prasad`, art: `aarti-lamp`,
      caption: `The aarti lamp, waved before the deity with song.`,
      body: `<p><strong>Aarti</strong> is the high point of puja in many homes and temples. A lamp with one or more wicks, or burning camphor, is waved in circles before the deity while everyone sings, claps and rings bells. It is joyful, simple and loved by children and elders alike.</p>
<h3>How to perform aarti</h3>
<ul><li>Light the aarti lamp, with ghee wicks or a piece of camphor.</li><li>Ring the bell with your left hand and hold the lamp in your right.</li><li>Wave the lamp in <strong>clockwise circles</strong> before the deity: traditionally a few circles at the feet, then the middle, then the face, and then the whole form.</li><li>Sing an aarti song, such as <em>Om Jai Jagdish Hare</em>, or the aarti of your deity.</li><li>Afterwards, offer the flame to everyone present. Each person cups their hands over the flame, then touches their eyes and head, drawing its blessing toward them.</li></ul>
<h3>Why camphor?</h3>
<p>Camphor burns completely, leaving no trace. It is a symbol of the ego burning away in the light of the divine, leaving nothing behind. The light itself represents knowledge, which dispels the darkness of ignorance.</p>
<h3>Prasad</h3>
<p>After the aarti, the food offered to the deity is shared as <strong>prasad</strong>, which means “grace.” It is received with the right hand, or with both hands cupped, and eaten with gratitude, never thrown away. In temples you may be given a sweet, a fruit, a spoonful of sweetened milk or a pinch of sacred ash.</p>
<p>Sharing prasad is a reminder that everything we have comes from the divine and returns to it, and that food offered with love becomes a blessing for all who eat it. Many families offer every meal at the shrine before eating, and say a prayer such as <em>Brahmarpanam</em> before taking the first bite.</p>
<h3>Aarti together</h3>
<p>Aarti is wonderful for families. Even small children can ring the bell, clap or hold the plate with help. Use Aarti mode in this app to show the words in large type, so everyone can sing together.</p>`,
      terms: [[`Aarti`, `The waving of lights before a deity, with song.`], [`Karpura`, `Camphor, burned in aarti.`], [`Prasad`, `“Grace”: food blessed by being offered to God.`]],
      practice: `Perform aarti with your family this evening. Open Om Jai Jagdish Hare in Aarti mode so everyone can follow the words.`,
      links: [[`Om Jai Jagdish Hare in Aarti mode`, `#/aarti/jagdish`], [`Brahmarpanam: prayer before meals`, `#/puja/brahmarpanam`], [`Browse all aartis`, `#/puja#browse?t=aarti`]]
    },
    {
      title: `A daily rhythm`, art: `sun-arc`,
      caption: `Offering water to the rising sun, one of the oldest daily rites.`,
      body: `<p>Hindu tradition fills the whole day with small moments of remembrance, so that prayer is not confined to the shrine. Here is a simple daily rhythm many families follow. Take whatever suits your life.</p>
<h3>On waking</h3>
<p>Before getting out of bed, look at the palms of your hands and say <em>Karagre vasate Lakshmi</em>: “At the tip of the hand dwells Lakshmi, in the middle Saraswati, at the base Govinda.” It is a reminder that our hands, and the work we do with them, are sacred. As your feet touch the floor, ask forgiveness of Mother Earth for stepping on her, with the prayer <em>Samudra Vasane Devi</em>.</p>
<h3>Morning</h3>
<p>After bathing, many people offer water to the rising sun, called <strong>arghya</strong>, pouring it from a small pot while chanting the Gayatri Mantra or <em>Om Suryaya Namah</em>. Then comes the morning puja at the shrine, even a short one, and perhaps japa or a few verses of the Gita.</p>
<h3>Meals</h3>
<p>Before eating, offer the food to God, mentally or at the shrine, and say a prayer of gratitude such as <em>Brahmarpanam</em>, from the Gita, or <em>Annapurne Sadapurne</em>, to the goddess of food.</p>
<h3>Evening</h3>
<p>At dusk, many homes light a lamp at the shrine and at the door. Families sing <em>Shubham Karoti</em>, a prayer to the light, and perhaps an aarti or the Hanuman Chalisa. In the old tradition of <strong>sandhya vandanam</strong>, prayers are offered at dawn, noon and dusk.</p>
<h3>Before sleep</h3>
<p>Before sleeping, reflect on the day and ask forgiveness for any wrong done, knowingly or unknowingly, with the prayer <em>Kara Charana Kritam</em>. Then rest in the name of God.</p>
<p>The For this moment card on the Today page and the Puja tab suggest prayers for each time of day, to help you build this rhythm.</p>`,
      terms: [[`Arghya`, `An offering of water, especially to the sun.`], [`Sandhya vandanam`, `Prayers at the junctions of the day.`], [`Shubham Karoti`, `The evening prayer to the lamp.`]],
      practice: `Choose one moment from this rhythm that you don't yet keep, such as the waking prayer, and add it to your day for a week. The Practice page will help you keep track.`,
      links: [[`Karagre Vasate`, `#/puja/morning`], [`Samudra Vasane Devi`, `#/puja/bhumi`], [`Shubham Karoti`, `#/puja/deepa-jyoti`], [`Your practice`, `#/practice`]]
    }
  ]
});

course({
  id: `meditation`, deva: `ध्यान`, category: `practice`, art: `meditator`,
  title: `Meditation and Mantra`,
  subtitle: `A beginner's daily practice`,
  intro: `A gentle introduction to the inner practices of Hinduism: preparing a space, breathing, chanting on the mala and sitting in meditation, with tips for making it a habit.`,
  lessons: [
    {
      title: `Preparing your space`, art: `flame`,
      caption: `A single steady flame: all you need to begin.`,
      body: `<p>Meditation can be done anywhere, but a dedicated place makes it much easier. Over time, the place itself begins to help: as soon as you sit there, the mind remembers what to do.</p>
<h3>The place</h3>
<ul><li>Choose a quiet corner where you won't be disturbed, ideally the same spot every day.</li><li>Keep it clean and simple. A small lamp, a picture of your chosen deity, a flower or nothing at all is enough.</li><li>Sit on a folded blanket, a cushion or a mat, so that your hips are slightly higher than your knees. A chair is perfectly fine too, with your feet flat on the floor.</li></ul>
<h3>The time</h3>
<p>Dawn and dusk are traditionally the best times, when the world is quiet and the mind is fresh or ready to settle. The early morning, before the day's business begins, works well for most people. Try to sit at the same time every day, before a meal rather than just after one.</p>
<h3>The posture</h3>
<p>The Bhagavad Gita describes the posture simply: keep the body, head and neck erect and still (6.13). You don't need to sit in the full lotus position. Sit cross-legged in <em>sukhasana</em>, the easy pose, or on a chair, with a straight but relaxed spine. Rest your hands on your knees or in your lap, palms up, perhaps with the tips of thumb and index finger touching. Relax your shoulders, jaw and forehead, and gently close your eyes.</p>
<h3>Before you begin</h3>
<p>Many people begin with a short prayer, a few rounds of Om, or a moment of gratitude, to mark the change from ordinary activity to practice. You might light the lamp, ring a bell or bow. These small rituals tell the mind: now we are going inward.</p>
<p>Turn off notifications, and let people at home know you'll be unavailable for a few minutes. The world can wait.</p>`,
      terms: [[`Sukhasana`, `The “easy pose”, sitting cross-legged.`], [`Asana`, `A posture or seat for meditation.`], [`Dhyana`, `Meditation.`]],
      practice: `Prepare your meditation space today, however small. Sit in it for three minutes with your eyes closed, simply noticing your breath.`
    },
    {
      title: `Breath and pranayama`, art: `breath`,
      caption: `Breathing in, breathing out: the doorway to a calm mind.`,
      body: `<p>The breath is the bridge between body and mind. When we are anxious, it becomes fast and shallow; when we are calm, it is slow and deep. The yogis discovered that the reverse is also true: by calming the breath, we can calm the mind. The practice of working with the breath is called <strong>pranayama</strong>, from <em>prana</em>, life energy, and <em>ayama</em>, extension.</p>
<h3>Simple breath awareness</h3>
<p>Before any technique, simply watch the breath. Feel the cool air entering the nose and the warm air leaving. Don't control it; just notice it. Let the out-breath become a little longer than the in-breath. After a few minutes, most people feel noticeably calmer.</p>
<h3>Alternate-nostril breathing</h3>
<p><strong>Nadi shodhana</strong>, “cleansing the channels,” is a gentle, balancing practice:</p>
<ol><li>Sit tall. Rest your left hand in your lap. Raise your right hand and fold the index and middle fingers into the palm.</li><li>Close the right nostril with your thumb and breathe in slowly through the left.</li><li>Close the left nostril with your ring finger, release the thumb, and breathe out through the right.</li><li>Breathe in through the right, close it, and breathe out through the left. That is one round.</li><li>Do five to ten rounds slowly, without straining.</li></ol>
<h3>Humming bee breath</h3>
<p><strong>Bhramari</strong> is wonderful for calming the mind before sleep or meditation. Breathe in deeply, then breathe out slowly while making a soft humming sound like a bee, with the lips closed. Feel the vibration in your head and chest. Repeat five to seven times, then sit in silence.</p>
<h3>A word of care</h3>
<p>Pranayama should always be gentle. Never hold the breath to the point of strain, and stop if you feel dizzy. If you are pregnant, or have heart, lung or blood-pressure conditions, keep to simple breath awareness, and learn more advanced practices from an experienced teacher.</p>`,
      terms: [[`Prana`, `Life energy, carried by the breath.`], [`Pranayama`, `Breathing practices that steady the life energy and the mind.`], [`Nadi shodhana`, `Alternate-nostril breathing.`], [`Bhramari`, `The humming bee breath.`]],
      practice: `Before your next meal or before bed, do five rounds of alternate-nostril breathing, followed by three rounds of humming bee breath. Notice how you feel afterwards.`
    },
    {
      title: `Japa: repeating a mantra`, art: `mala`,
      caption: `A mala of 108 beads, with the larger guru bead.`,
      body: `<p><strong>Japa</strong> is the repetition of a mantra or a name of God. It is one of the simplest and most powerful spiritual practices, open to everyone, and it can be done anywhere: at the shrine, on a walk, or lying awake at night.</p>
<h3>The mala</h3>
<p>Japa is traditionally counted on a <strong>mala</strong>, a string of 108 beads, often made of rudraksha seeds (for Shiva), tulsi wood (for Vishnu and Krishna) or sandalwood. A larger bead, the <strong>meru</strong> or guru bead, marks the beginning and end of the circle.</p>
<p>Why 108? Many explanations are given: there are 27 lunar mansions with four quarters each, and 12 signs of the zodiac with nine planets, both making 108. Whatever the reason, it is a sacred number in Hindu, Buddhist and Jain traditions.</p>
<h3>How to do japa</h3>
<ol><li>Hold the mala in your right hand, draped over the middle or ring finger. Traditionally the index finger, linked with the ego, is not used.</li><li>Start at the bead next to the guru bead. Repeat the mantra once, then use your thumb to move to the next bead.</li><li>Continue all the way around. When you reach the guru bead, don't cross it; turn the mala around and go back the other way.</li></ol>
<h3>Three ways to chant</h3>
<p>Japa can be <strong>spoken</strong> aloud, <strong>whispered</strong> so only you can hear, or <strong>silent</strong>, repeated only in the mind. The tradition says each is more powerful than the one before, but begin aloud if it helps you concentrate.</p>
<h3>Choosing a mantra</h3>
<p>Choose a mantra connected to your ishta devata: <em>Om Namah Shivaya</em>, <em>Om Namo Narayanaya</em>, <em>Hare Krishna</em>, <em>Shri Ram Jai Ram</em> or simply <em>Om</em>. Many people receive a personal mantra from a guru at initiation, and keep it private. The japa counter on the Puja tab can count for you, and even chant along.</p>`,
      terms: [[`Japa`, `Repetition of a mantra or divine name.`], [`Mala`, `A string of 108 prayer beads.`], [`Meru`, `The guru bead, marking the start and end of the mala.`]],
      practice: `Choose a mantra and chant one full mala, 108 times, today. Use a mala if you have one, or the japa counter in the app.`,
      links: [[`Chant on the mala`, `#/japa`], [`Om Namah Shivaya`, `#/puja/shiva`], [`Om Namo Narayanaya`, `#/puja/narayana`]]
    },
    {
      title: `Dhyana: sitting in meditation`, art: `meditator`,
      caption: `Seated in stillness: the practice of dhyana.`,
      body: `<p>Patanjali's Yoga Sutras define yoga as <em>chitta vritti nirodhah</em>, “the stilling of the movements of the mind” (1.2). Meditation, <strong>dhyana</strong>, is the heart of that practice: an unbroken flow of attention toward one object, until the mind becomes clear and still, like a calm lake that reflects the sky.</p>
<h3>The eight limbs</h3>
<p>Patanjali places meditation within an eight-limbed path, <strong>ashtanga yoga</strong>: ethical restraints (<em>yama</em>), observances (<em>niyama</em>), posture (<em>asana</em>), breath (<em>pranayama</em>), withdrawal of the senses (<em>pratyahara</em>), concentration (<em>dharana</em>), meditation (<em>dhyana</em>) and absorption (<em>samadhi</em>). Each supports the next. An ethical life and a steady body make a quiet mind possible.</p>
<h3>Ways to meditate</h3>
<p>There are many methods. Try one for a few weeks before switching.</p>
<ul><li><strong>Breath</strong>: rest your attention on the natural flow of breath at the nostrils.</li><li><strong>Mantra</strong>: repeat a mantra silently, letting it become slower and softer.</li><li><strong>Form</strong>: picture your ishta devata in detail, from the feet upward, with love.</li><li><strong>Light</strong>: gaze at a steady flame for a minute, then close your eyes and hold its afterglow in your mind, a practice called <em>trataka</em>.</li><li><strong>Inquiry</strong>: as Ramana Maharshi taught, ask “Who am I?” and trace each thought back to the sense of “I.”</li></ul>
<h3>When the mind wanders</h3>
<p>It will wander, constantly. This is not failure; it is how minds work. The practice is simply to notice and return, gently, without frustration. Krishna tells Arjuna to bring the mind back each time it strays (Gita 6.26). Every return strengthens your attention, like lifting a weight.</p>
<h3>Ending well</h3>
<p>Finish by sitting quietly for a moment without any technique. Then chant Om or a peace prayer, and open your eyes slowly. Carry a little of the stillness into the next thing you do.</p>`,
      terms: [[`Dhyana`, `Meditation: a steady flow of attention.`], [`Dharana`, `Concentration, holding the mind on one point.`], [`Pratyahara`, `Withdrawing the senses from distraction.`], [`Trataka`, `Meditation on a steady flame.`]],
      practice: `Sit for ten minutes using one method above. Count how many times you notice your mind has wandered, and congratulate yourself each time you return.`,
      links: [[`Read the Yoga Sutras`, `#/read/yoga/1/1`], [`Bhagavad Gita, chapter 6`, `#/read/gita/6`]]
    },
    {
      title: `Building a daily habit`, art: `lotus`,
      caption: `The lotus grows slowly from the mud, opening a little each day.`,
      body: `<p>The benefits of meditation come from regular practice, not occasional effort. A few minutes every day will do far more than an hour once a month. The Gita says the restless mind is tamed by <strong>abhyasa</strong>, steady practice, and <strong>vairagya</strong>, letting go (6.35). Here is how to make practice part of your life.</p>
<h3>Start small</h3>
<p>Begin with just five minutes a day. It is better to sit for five minutes every day than for thirty minutes once a week. When five minutes feels easy, add a minute or two. Many people find twenty minutes, once or twice a day, a good long-term goal.</p>
<h3>Anchor it</h3>
<p>Link your practice to something you already do every day: after brushing your teeth, before your morning tea, after lighting the evening lamp. The existing habit becomes the cue for the new one.</p>
<h3>Expect ups and downs</h3>
<p>Some days you'll feel peaceful; others, restless or sleepy. Both are normal. Don't judge a session by how it felt. The benefit of steady practice accumulates quietly, like a lotus slowly rising from the mud toward the light.</p>
<h3>If you miss a day</h3>
<p>Simply start again the next day. Don't let one missed day become a reason to give up. As the Gita promises, no sincere effort on the spiritual path is ever wasted (2.40).</p>
<h3>Keep good company</h3>
<p>The tradition values <strong>satsang</strong>, the company of truth: spending time with people who inspire your practice, at a temple, a meditation group or a study circle. Reading a little scripture each day keeps the inspiration fresh.</p>
<h3>Notice the fruits</h3>
<p>After a few weeks, look back. Are you a little calmer, more patient, more aware of your reactions? These small changes, not dramatic experiences, are the real signs of progress. The Practice page in this app records your chanting and reading, so you can see your streak grow.</p>`,
      terms: [[`Abhyasa`, `Steady, repeated practice.`], [`Vairagya`, `Detachment; letting go.`], [`Satsang`, `“The company of truth”: spiritual fellowship.`]],
      practice: `Commit to five minutes of meditation or japa every day for the next seven days, at the same time. Check your streak on the Practice page at the end of the week.`,
      links: [[`Your practice`, `#/practice`], [`Set a daily prayer reminder`, `#/reminders`]]
    }
  ]
});

course({
  id: `festivals`, deva: `उत्सव`, category: `practice`, art: `calendar-wheel`,
  title: `Festivals and the Hindu Calendar`,
  subtitle: `The sacred rhythm of the year`,
  intro: `How the Hindu calendar works, why festival dates move every year, and the meaning and customs of the great festivals: Diwali, Holi, Navaratri and the festivals of the sun and harvest.`,
  lessons: [
    {
      title: `How the Hindu calendar works`, art: `calendar-wheel`,
      caption: `Sun, moon and months: the circle of the Hindu year.`,
      body: `<p>Why does Diwali fall in October one year and November the next? Because most Hindu festivals follow a <strong>lunisolar</strong> calendar, which tracks both the moon and the sun. The Calendar tab in this app works these dates out for your city.</p>
<h3>Tithis: lunar days</h3>
<p>The basic unit is the <strong>tithi</strong>, a lunar day. It is the time the moon takes to move twelve degrees ahead of the sun in the sky. There are thirty tithis in a lunar month. Because the moon's speed varies, a tithi can be shorter or longer than a solar day, so occasionally a tithi is skipped or repeated. A day is usually named after the tithi in force at sunrise, which is why dates can differ slightly between cities.</p>
<h3>Pakshas: the two fortnights</h3>
<p>Each month has two halves, or <strong>pakshas</strong>. <strong>Shukla paksha</strong>, the bright fortnight, runs from new moon to full moon as the moon waxes. <strong>Krishna paksha</strong>, the dark fortnight, runs from full moon back to new moon. The tithis in each are numbered: Pratipada (first), Dwitiya (second), and so on, up to Ekadashi (eleventh), ending with <strong>Purnima</strong>, the full moon, or <strong>Amavasya</strong>, the new moon.</p>
<h3>The months</h3>
<p>There are twelve lunar months, beginning with Chaitra in spring: Chaitra, Vaishakha, Jyeshtha, Ashadha, Shravana, Bhadrapada, Ashvin, Kartika, Margashirsha, Pausha, Magha and Phalguna. In South and West India, months usually end at the new moon (<em>amanta</em>); in North India, at the full moon (<em>purnimanta</em>). The festival falls on the same day either way, but the month name for the dark fortnight can differ.</p>
<p>Twelve lunar months are about eleven days shorter than a solar year. To keep festivals in their seasons, an extra month, <strong>adhika masa</strong>, is added roughly every three years.</p>
<h3>Eras and solar calendars</h3>
<p>Years are often counted in the <strong>Vikram Samvat</strong> era, which is about 57 years ahead of the common era, or the <strong>Shaka</strong> era, used for India's national calendar. Some regions, including Tamil Nadu, Kerala, Bengal, Odisha and Punjab, follow solar calendars for their new year, which is why Puthandu, Vishu, Pohela Boishakh and Vaisakhi all fall in mid-April.</p>`,
      terms: [[`Tithi`, `A lunar day, one of thirty in a month.`], [`Paksha`, `A lunar fortnight: shukla (waxing) or krishna (waning).`], [`Adhika masa`, `An extra month added to keep the calendar in step with the seasons.`], [`Vikram Samvat`, `A traditional Hindu era, about 57 years ahead of the common era.`]],
      practice: `Open the Calendar tab and find today's tithi and paksha. Then look up the next Purnima and Amavasya, and notice how many days apart they are.`,
      links: [[`Open the Calendar`, `#/calendar`], [`Choose your city`, `#/location`]]
    },
    {
      title: `Ekadashi and sacred fasts`, art: `moon-phases`,
      caption: `The phases of the moon mark the fasting days of the month.`,
      body: `<p>Many Hindus keep regular fasts, called <strong>vratas</strong>, vows. A fast is not only about food. It is a way to strengthen the will, simplify life for a day, and give more time and attention to God.</p>
<h3>Ekadashi</h3>
<p>The most widely kept fast is <strong>Ekadashi</strong>, the eleventh day of each lunar fortnight, twice a month. It is sacred to Vishnu. Devotees avoid grains and beans, eating fruit, milk, nuts and certain root vegetables, or fast completely. Some keep a <em>nirjala</em> fast, without even water, on Nirjala Ekadashi in early summer. The fast is broken on the next day, Dwadashi, after sunrise, within a set window called <em>parana</em>.</p>
<p>Each of the twenty-four Ekadashis of the year has its own name and story. Mokshada Ekadashi in winter is also Gita Jayanti; Devshayani Ekadashi in Ashadha marks the start of Chaturmas, the four holy months when Vishnu rests; and Prabodhini Ekadashi in Kartika marks his awakening.</p>
<h3>Other regular fasts</h3>
<ul><li><strong>Purnima</strong>, the full moon: often kept with the Satyanarayan Katha, a family puja to Vishnu.</li><li><strong>Amavasya</strong>, the new moon: a day for remembering ancestors.</li><li><strong>Pradosh</strong>: the thirteenth day of each fortnight, at twilight, for Shiva.</li><li><strong>Sankashti Chaturthi</strong>: the fourth day after the full moon, for Ganesha, broken at moonrise.</li><li><strong>Weekly fasts</strong>: Monday for Shiva, Tuesday for Hanuman, Thursday for Vishnu or the guru, Friday for the Goddess, Saturday for Hanuman and Shani.</li></ul>
<h3>Fasting wisely</h3>
<p>The tradition is clear that fasting should never harm health. Children, the elderly, pregnant women and anyone who is ill or on medication are not expected to fast strictly. They can keep a lighter fast, eat simply or offer prayer and charity instead. The inner fast, from anger, gossip and harmful habits, is the most important of all.</p>`,
      terms: [[`Vrata`, `A vow, often including a fast.`], [`Ekadashi`, `The eleventh lunar day, a fast sacred to Vishnu.`], [`Parana`, `The proper time to break a fast.`], [`Chaturmas`, `The four holy months of the monsoon.`]],
      practice: `Find the next Ekadashi in the Calendar. Try a simple fast that suits your health, perhaps avoiding grains, and spend some of the time saved in prayer or reading.`,
      links: [[`See upcoming Ekadashis`, `#/calendar`], [`Set an Ekadashi reminder`, `#/reminders`]]
    },
    {
      title: `Diwali, the festival of lights`, art: `diyas`,
      caption: `Rows of diyas and a rangoli at the door on Diwali night.`,
      body: `<p><strong>Diwali</strong>, or Deepavali, “a row of lamps,” is the best-known Hindu festival. It falls on the new-moon night at the end of Ashvin (or Kartika in the North Indian reckoning), usually in October or November, the darkest night of the month, which is filled with light.</p>
<h3>Its stories</h3>
<ul><li>In North India, Diwali celebrates <strong>Rama's return</strong> to Ayodhya after fourteen years of exile and his victory over Ravana. The people lit lamps all along the way to welcome him home.</li><li>It is the night of <strong>Lakshmi Puja</strong>, when the goddess of prosperity visits clean, bright homes.</li><li>In South India, Deepavali is usually celebrated a day earlier, on Naraka Chaturdashi, recalling <strong>Krishna's victory over the demon Narakasura</strong>, with an oil bath before dawn.</li><li>In Bengal, the night is devoted to <strong>Kali Puja</strong>.</li></ul>
<p>Jains celebrate Mahavira's liberation at the same time, and Sikhs celebrate Bandi Chhor Divas. The common thread is the victory of light over darkness, knowledge over ignorance and good over evil.</p>
<h3>Five days of celebration</h3>
<ol><li><strong>Dhanteras</strong>: honouring Dhanvantari, the divine physician, and Lakshmi; buying something new, often metal.</li><li><strong>Naraka Chaturdashi</strong>, or Choti Diwali: an early oil bath and the first lamps.</li><li><strong>Diwali</strong> itself: Lakshmi Puja in the evening, lamps everywhere, sweets and fireworks.</li><li><strong>Govardhan Puja</strong>: remembering Krishna lifting the hill, with a mountain of food, the annakut. For many Gujaratis, this is New Year's Day.</li><li><strong>Bhai Dooj</strong>: sisters pray for their brothers' long life, and brothers give gifts.</li></ol>
<h3>Customs</h3>
<p>Weeks before, homes are cleaned and repaired. Families draw <strong>rangoli</strong> at the door, light <strong>diyas</strong>, wear new clothes, make and share sweets, visit relatives and friends, and remember those in need. Businesses close their old account books and open new ones with a puja.</p>
<p>The inner meaning of Diwali is to light the lamp of wisdom within, and to clean the house of the heart as carefully as we clean our homes.</p>`,
      terms: [[`Deepavali`, `“A row of lamps”: the festival of Diwali.`], [`Diya`, `A small clay oil lamp.`], [`Annakut`, `The “mountain of food” offered at Govardhan Puja.`]],
      practice: `Before the next Diwali, clean one place in your home that has been neglected, and one “corner of the heart”: an old grudge you can let go.`,
      links: [[`Diwali`, `#/festival/diwali`], [`Om Jai Lakshmi Mata`, `#/puja/lakshmi-aarti`], [`Shubham Karoti: prayer to the lamp`, `#/puja/deepa-jyoti`]]
    },
    {
      title: `Holi, the festival of colours`, art: `holi`,
      caption: `Clouds of colour fill the air at Holi.`,
      body: `<p><strong>Holi</strong> is the joyful spring festival of colours, celebrated on the full moon of Phalguna, usually in March. For a day, ordinary rules are set aside: people of every age and background throw coloured powder and water at each other, sing, dance and embrace.</p>
<h3>Holika Dahan</h3>
<p>On the night before, communities light a great bonfire, <strong>Holika Dahan</strong>. It recalls the story of the boy <strong>Prahlada</strong>, devotee of Vishnu, and his aunt <strong>Holika</strong>, who could not be harmed by fire. At her brother Hiranyakashipu's command, she sat in a fire holding Prahlada, meaning to burn him. But Holika was consumed, and Prahlada walked out unharmed, protected by his faith. The bonfire celebrates the victory of devotion over cruelty, and people throw grain and coconuts into it as offerings.</p>
<h3>Krishna and Radha</h3>
<p>The colours come from Krishna. As a child, the story goes, Krishna complained to his mother Yashoda that he was dark while Radha was fair. Yashoda playfully suggested he colour Radha's face any colour he liked. So he did, and the playful splashing of colour became a celebration of love. In <strong>Braj</strong>, the land of Krishna around Mathura and Vrindavan, Holi lasts for days, with famous celebrations at Barsana, where women playfully chase the men with sticks.</p>
<h3>A festival of renewal</h3>
<p>Holi marks the end of winter and the arrival of spring and the new harvest. It is also a festival of forgiveness: old quarrels are forgotten, and enemies become friends again. People greet each other with “Holi hai!” and share sweets like gujiya and the cool drink thandai.</p>
<h3>Celebrating with care</h3>
<p>Use natural, skin-safe colours made from flowers and herbs, and avoid harsh chemical powders. Respect people who don't wish to play, and be gentle with animals. The spirit of Holi is joy that includes everyone.</p>`,
      terms: [[`Holika Dahan`, `The bonfire on the eve of Holi.`], [`Prahlada`, `The boy devotee protected from the fire.`], [`Braj`, `The region of Krishna's childhood, around Mathura and Vrindavan.`]],
      practice: `Holi is a time to forgive. Think of one person you have drifted from or argued with, and reach out to them with a kind message.`,
      links: [[`Holi`, `#/festival/holi`], [`Course: The Ten Avatars, Narasimha and Prahlada`, `#/academy/avatars/4`]]
    },
    {
      title: `Navaratri and Dussehra`, art: `garba`,
      caption: `The garbo pot with its lamp, and dandiya sticks for the dance.`,
      body: `<p><strong>Navaratri</strong>, “nine nights,” honours the Divine Mother. There are several Navaratris in the year, but the greatest is <strong>Sharad Navaratri</strong> in autumn, in the month of Ashvin, usually in September or October. Chaitra Navaratri in spring is also widely kept, and ends with Ram Navami.</p>
<h3>Nine nights, nine forms</h3>
<p>Each night the Goddess is worshipped in one of her nine forms, the <strong>Navadurga</strong>: Shailaputri, Brahmacharini, Chandraghanta, Kushmanda, Skandamata, Katyayani, Kalaratri, Mahagauri and Siddhidatri. Many devotees fast, eating only fruit or simple foods, and read the Devi Mahatmya. On the eighth or ninth day, young girls are worshipped as forms of the Goddess, fed and given gifts, in <em>kanya puja</em>.</p>
<h3>Across India</h3>
<ul><li>In <strong>Gujarat</strong>, people dance <strong>garba</strong> in great circles around a lamp in a pierced clay pot, the garbo, a symbol of the womb and of life, and <strong>dandiya raas</strong> with decorated sticks, late into the night.</li><li>In <strong>Bengal</strong>, the last days become <strong>Durga Puja</strong>, with magnificent images of Durga in decorated pavilions, ending with their immersion in the river.</li><li>In <strong>South India</strong>, families arrange <strong>golu</strong>, steps displaying dolls of gods, saints and village life, and visit each other's homes. Tools, books and instruments are worshipped on Ayudha Puja.</li><li>In <strong>North India</strong>, the <strong>Ram Lila</strong> is performed each night, telling the Ramayana.</li></ul>
<h3>Dussehra</h3>
<p>The tenth day is <strong>Vijayadashami</strong>, or Dussehra, the day of victory. It celebrates both Durga's victory over Mahishasura and Rama's victory over Ravana. In the North, huge effigies of Ravana and his brothers, filled with fireworks, are burned at dusk. In the South, children begin their education on this day. It is considered one of the most auspicious days of the year to begin anything new.</p>
<p>The nine nights are often read as an inner journey: three nights to Durga, to destroy our impurities; three to Lakshmi, to cultivate good qualities; and three to Saraswati, to gain wisdom. Victory follows.</p>`,
      terms: [[`Navaratri`, `“Nine nights” of worship of the Goddess.`], [`Garba`, `The circle dance of Gujarat around a lamp.`], [`Golu`, `A display of dolls on steps, in South India.`], [`Vijayadashami`, `The tenth day, the festival of victory.`]],
      practice: `During the next Navaratri, choose one quality to work on for nine days: three days removing a bad habit, three days building a good one, three days learning something new.`,
      links: [[`Navaratri`, `#/festival/navaratri`], [`Course: The Divine Mother`, `#/academy/devi`], [`Jai Ambe Gauri in Aarti mode`, `#/aarti/ambe-aarti`]]
    },
    {
      title: `Festivals of the sun and harvest`, art: `kite`,
      caption: `Kites over the winter sun at Makar Sankranti.`,
      body: `<p>Many Hindu festivals are tied to the farming year and to the sun. They give thanks for the harvest, for the cattle that help with farming, and for the sun that makes all life possible.</p>
<h3>Makar Sankranti</h3>
<p><strong>Makar Sankranti</strong> marks the sun's entry into the sign of Capricorn, Makara. Because it follows the sun rather than the moon, it falls on almost the same date every year, around 14 January. It is celebrated across India under many names:</p>
<ul><li><strong>Pongal</strong> in Tamil Nadu: a four-day festival. On Thai Pongal, families boil new rice with milk and jaggery until it overflows, shouting “Pongalo Pongal!” The next day, Mattu Pongal, honours cattle.</li><li><strong>Uttarayan</strong> in Gujarat: the sky fills with kites from dawn to dusk.</li><li><strong>Lohri</strong> in Punjab, the night before: bonfires, songs and dancing.</li><li><strong>Magh Bihu</strong> in Assam, and <strong>Khichdi</strong> in parts of North India.</li></ul>
<p>Sweets of sesame and jaggery are shared. In Maharashtra, people exchange them saying <em>tilgul ghya, god god bola</em>: “take this sweet, and speak sweetly.” Many take a holy dip in rivers, and at Prayagraj the Magh Mela begins.</p>
<h3>Onam</h3>
<p><strong>Onam</strong>, Kerala's great harvest festival in late summer, welcomes back the beloved King <strong>Bali</strong>, whom Vishnu as Vamana sent to the underworld but allowed to visit his people once a year. Homes are decorated with flower carpets, pookalam, families share a grand vegetarian feast on banana leaves, the sadya, and snake-boat races are held on the rivers.</p>
<h3>Chhath</h3>
<p><strong>Chhath</strong>, celebrated especially in Bihar and eastern Uttar Pradesh, six days after Diwali, is devoted to the sun god <strong>Surya</strong> and Chhathi Maiya. Devotees, mostly women, keep a strict fast and stand in rivers and ponds to offer prayers to the setting and then the rising sun.</p>
<h3>Thanking the sun</h3>
<p>Every day, in a small way, many Hindus keep this spirit by offering water to the rising sun and chanting the Gayatri Mantra or <em>Om Suryaya Namah</em>, giving thanks for light and life.</p>`,
      terms: [[`Makar Sankranti`, `The sun's entry into Capricorn, a harvest festival in January.`], [`Pongal`, `The Tamil harvest festival; also the sweet rice dish cooked for it.`], [`Onam`, `Kerala's harvest festival, welcoming King Bali.`], [`Chhath`, `A festival of fasting and prayer to the sun.`]],
      practice: `Tomorrow at sunrise, step outside or face a window, and offer a moment of thanks to the sun, with Om Suryaya Namah or the Gayatri Mantra.`,
      links: [[`Makar Sankranti`, `#/festival/makar-sankranti`], [`Chhath`, `#/festival/chhath`], [`Om Suryaya Namah`, `#/puja/surya-mantra`]]
    }
  ]
});

course({
  id: `symbols`, deva: `प्रतीक`, category: `practice`, art: `om`,
  title: `Sacred Symbols`,
  subtitle: `Om, the lotus, tilak and more`,
  intro: `Hindu life is full of symbols. Five lessons on what they mean: Om, the lotus, the marks on the forehead, the objects of worship, and the auspicious signs drawn at the door.`,
  lessons: [
    {
      title: `Om, the sacred sound`, art: `om`,
      caption: `Om: the sound that holds the whole of reality.`,
      body: `<p><strong>Om</strong>, also written Aum, is the most sacred sound and symbol in Hinduism. It is chanted at the beginning and end of prayers, mantras and readings of scripture, written at the top of letters and wedding invitations, and drawn above the doors of homes and temples. It is called the <strong>pranava</strong>, the primal sound.</p>
<h3>The sound of everything</h3>
<p>The Upanishads say that Om is the sound of Brahman itself. “Om is this whole world,” begins the Mandukya Upanishad. The Katha Upanishad says it is the word that all the Vedas proclaim, and in the Bhagavad Gita Krishna says, “Among words, I am the one syllable, Om” (10.25).</p>
<h3>A, U, M and the silence</h3>
<p>The Mandukya Upanishad explains Om through its parts. The sound has three letters, A, U and M, followed by silence:</p>
<ul><li><strong>A</strong> stands for the waking state, the world we see and touch.</li><li><strong>U</strong> stands for the dreaming state, the inner world of the mind.</li><li><strong>M</strong> stands for deep, dreamless sleep, when all is quiet.</li><li>The <strong>silence</strong> after the sound stands for the fourth state, <em>turiya</em>: pure awareness, which underlies and goes beyond the other three.</li></ul>
<p>So chanting Om is a journey through every level of experience to the silence beyond.</p>
<h3>The written symbol</h3>
<p>The written form ॐ is also explained this way. The large lower curve is waking, the upper curve deep sleep, the curve to the right dreaming. The crescent above is <em>maya</em>, illusion, which separates us from the dot, the bindu, which is the absolute. The dot stands apart, untouched.</p>
<h3>Chanting Om</h3>
<p>Sit comfortably and breathe in deeply. As you breathe out, chant “Aaa,” opening the mouth, feeling it in the belly; “Ooo,” rounding the lips, feeling it in the chest; and “Mmm,” closing the lips, feeling the vibration in the head. Then rest in the silence before the next breath. Three or more rounds of Om at the start of meditation or puja quiet the mind beautifully.</p>`,
      terms: [[`Om`, `The sacred syllable, the sound of Brahman.`], [`Pranava`, `“The primal sound”, a name for Om.`], [`Turiya`, `The fourth state: pure awareness beyond waking, dream and sleep.`]],
      practice: `Chant Om slowly three times, then sit in the silence for one minute. Do this each morning this week before anything else.`,
      links: [[`Bhagavad Gita 10.25`, `#/read/gita/10?v=25`], [`Course: Meditation and Mantra`, `#/academy/meditation`]]
    },
    {
      title: `The lotus`, art: `lotus`,
      caption: `The lotus rises from the mud and blooms untouched by it.`,
      body: `<p>The <strong>lotus</strong>, <em>padma</em> or <em>kamala</em> in Sanskrit, is perhaps the most beloved image in Hindu art and poetry. It is the national flower of India, and almost every deity is connected with it.</p>
<h3>Pure in the mud</h3>
<p>The lotus grows in muddy ponds, yet its flower rises above the water, clean and beautiful. Its leaves repel water, so drops roll off them without leaving a mark. This makes it a perfect symbol of the spiritual life: living in the world, among its struggles, without being stained by them.</p>
<p>The Bhagavad Gita uses exactly this image. One who acts without attachment, offering every action to the divine, “is not touched by sin, as a lotus leaf is not wet by water” (5.10).</p>
<h3>The seat of the gods</h3>
<ul><li><strong>Brahma</strong> is born from a lotus growing from Vishnu's navel, at the start of creation.</li><li><strong>Vishnu</strong> holds a lotus in one hand, and is called <em>Padmanabha</em>, lotus-navelled, and <em>Kamalanayana</em>, lotus-eyed.</li><li><strong>Lakshmi</strong> sits and stands on a lotus and holds lotuses in her hands. One of her names is Padma.</li><li><strong>Saraswati</strong> sits on a white lotus.</li></ul>
<p>Devotees speak of the deity's “lotus feet” and “lotus eyes,” describing a beauty that is gentle, pure and full of grace.</p>
<h3>The lotus within</h3>
<p>In yoga, the energy centres of the subtle body, the <strong>chakras</strong>, are pictured as lotuses with different numbers of petals, from the four-petalled lotus at the base of the spine to the thousand-petalled lotus at the crown of the head. The heart, too, is often described as a lotus, in which the divine dwells.</p>
<p>The way a lotus opens, slowly, petal by petal, toward the sun, is a picture of the soul unfolding toward the light. Even the meditation posture, <em>padmasana</em>, is named after it.</p>`,
      terms: [[`Padma`, `The lotus.`], [`Padmanabha`, `“Lotus-navelled”, a name of Vishnu.`], [`Chakra`, `An energy centre of the subtle body, pictured as a lotus.`], [`Padmasana`, `The lotus posture for meditation.`]],
      practice: `When you meet a difficult situation today, picture a lotus leaf with water rolling off it. Act as well as you can, and let the result roll off you.`,
      links: [[`Bhagavad Gita 5.10`, `#/read/gita/5?v=10`]]
    },
    {
      title: `Tilak, bindi and sacred ash`, art: `tilak`,
      caption: `Three sacred marks: the Vaishnava namam, the Shaiva tripundra and the bindi.`,
      body: `<p>Many Hindus wear a sacred mark on the forehead, especially during worship, at festivals or every day. The general name is <strong>tilak</strong>, or tilaka. It is placed between the eyebrows, at the point called the <strong>ajna chakra</strong>, the seat of wisdom and the “third eye,” as a reminder to see with spiritual vision.</p>
<h3>Marks of the traditions</h3>
<p>The shape of the tilak often shows which tradition a person follows:</p>
<ul><li><strong>Vaishnavas</strong>, devotees of Vishnu and Krishna, wear the <strong>urdhva pundra</strong>, an upward mark in a U or V shape made with white clay, often with a red or yellow line in the middle. It is said to represent the feet of Vishnu, or the path rising to God. Different Vaishnava communities have their own variations, such as the namam in South India.</li><li><strong>Shaivas</strong>, devotees of Shiva, wear the <strong>tripundra</strong>: three horizontal lines of sacred ash, <em>vibhuti</em> or bhasma, across the forehead, often with a red dot in the middle. Ash reminds us that all bodies return to dust, and the three lines are linked with many triads: the three gunas, the three worlds and the three syllables of Om.</li><li><strong>Shaktas</strong>, devotees of the Goddess, often wear a red dot or vertical line of <strong>kumkum</strong>.</li></ul>
<h3>The bindi</h3>
<p>The <strong>bindi</strong>, from <em>bindu</em>, a dot, is a small mark, traditionally red, worn by women. A red bindi and <strong>sindoor</strong>, red powder in the parting of the hair, have traditionally been signs of a married woman in many communities. Today bindis come in every colour and shape, and girls and women of all ages wear them as a mark of beauty and identity.</p>
<h3>Receiving a tilak</h3>
<p>At festivals, at the temple and at the end of a puja, a priest or elder often applies a tilak of kumkum or sandalwood paste, sometimes with a few grains of rice. Sisters apply a tilak to their brothers at Raksha Bandhan and Bhai Dooj. It is a sign of blessing, protection and honour.</p>`,
      terms: [[`Tilak`, `A sacred mark on the forehead.`], [`Tripundra`, `The three horizontal lines of ash worn by Shaivas.`], [`Urdhva pundra`, `The upward mark worn by Vaishnavas.`], [`Vibhuti`, `Sacred ash.`]],
      practice: `After your next puja, apply a small tilak of kumkum or sandalwood paste between your eyebrows, and take a moment to remember the divine within.`,
      links: [[`Raksha Bandhan`, `#/festival/raksha-bandhan`]]
    },
    {
      title: `Lamp, bell, conch and kalash`, art: `puja-items`,
      caption: `The objects of worship, each with its own meaning.`,
      body: `<p>Every object used in puja carries a meaning. Knowing them turns ritual from habit into understanding.</p>
<h3>The lamp</h3>
<p>The <strong>diya</strong>, a small lamp of ghee or oil, stands for the light of knowledge that removes the darkness of ignorance. The Upanishadic prayer <em>tamaso ma jyotir gamaya</em>, “lead me from darkness to light,” is lived every time a lamp is lit. The flame always points upward, as the soul should. Lighting a lamp at dawn and dusk is one of the oldest Hindu practices.</p>
<h3>The bell</h3>
<p>The <strong>ghanta</strong>, a small hand bell, is rung at the start of worship and during aarti. Its sound is said to resemble Om, to invite the divine presence, to drive away negative influences, and to call the wandering mind back to the present. Temple bells are rung by devotees as they enter.</p>
<h3>The conch</h3>
<p>The <strong>shankha</strong>, or conch shell, is held by Vishnu. Its deep, resonant sound is the sound of creation and of victory; in the Gita, the heroes blow their conches at the start of the battle. In homes and temples, the conch is blown to begin worship and at auspicious moments, and in Bengal it is blown at dusk and at weddings.</p>
<h3>The kalash</h3>
<p>The <strong>kalash</strong>, or purna kumbha, is a pot filled with water, its mouth covered with five or more mango leaves and topped with a coconut, often wrapped in red cloth and tied with sacred thread. It represents fullness, abundance and the womb of creation, and the deity is often invited to dwell in it during ceremonies. A kalash is placed at the start of weddings, housewarmings and festival pujas.</p>
<h3>And more</h3>
<ul><li><strong>Coconut</strong>: breaking it before a deity symbolises breaking the hard shell of the ego to reveal the pure, sweet heart inside.</li><li><strong>Flowers</strong>: the beauty of a life offered to God.</li><li><strong>Incense</strong>: as its fragrance fills the room, our good qualities should spread to others.</li><li><strong>Camphor</strong>: burns without trace, like the ego dissolving in the divine.</li><li><strong>Rice</strong>, unbroken (<em>akshata</em>): wholeness and prosperity.</li></ul>`,
      terms: [[`Ghanta`, `The sacred bell.`], [`Shankha`, `The conch shell.`], [`Kalash`, `A sacred pot of water crowned with mango leaves and a coconut.`]],
      practice: `At your next puja, pause before using each object, and recall its meaning. Light the lamp thinking of knowledge, ring the bell to call the mind home.`,
      links: [[`Asato Ma Sadgamaya: lead me to the light`, `#/puja/asato-ma`], [`Course: Daily Puja at Home`, `#/academy/puja`]]
    },
    {
      title: `Swastika, yantra and rangoli`, art: `rangoli`,
      caption: `A rangoli at the door, drawn to welcome guests and blessings.`,
      body: `<h3>The swastika</h3>
<p>The <strong>swastika</strong> is one of the oldest symbols of good fortune in the world. Its name comes from the Sanskrit <em>su</em>, good, and <em>asti</em>, it is: “may all be well.” For thousands of years it has been drawn at the thresholds of Hindu homes, on account books at Diwali, on wedding invitations and at the start of ceremonies. It is sacred also to Jains and Buddhists.</p>
<p>The Hindu swastika is usually drawn upright, in red or saffron, with its arms turning to the right, often with four dots between them. It is linked with Ganesha, with the sun and with the four directions, the four Vedas and the four goals of life. In the twentieth century, a tilted black version was taken and misused as the emblem of Nazism. Hindus around the world have worked to explain that their sacred symbol of well-being is entirely different from that hateful misuse, and many continue to use it proudly in its true meaning.</p>
<h3>Yantras</h3>
<p>A <strong>yantra</strong> is a sacred geometric diagram that serves as a dwelling place or form of a deity, used in worship and meditation. The most famous is the <strong>Sri Yantra</strong>, the yantra of the Goddess: nine interlocking triangles radiating from a central dot, the bindu, surrounded by lotus petals and a square enclosure with four gates. It is a map of the cosmos and of the journey inward to the centre.</p>
<h3>Rangoli and kolam</h3>
<p><strong>Rangoli</strong> are designs drawn on the floor at the entrance to a home, to welcome guests, the gods and good fortune. In South India, many women draw a <strong>kolam</strong> every morning with rice flour: an intricate pattern of dots and flowing lines. The rice flour also feeds ants and birds, a small daily act of kindness to all creatures. At Diwali, Pongal and Onam, rangolis become large and colourful, made with powders, rice and flower petals.</p>
<p>A rangoli is temporary. It is swept away by feet, wind and rain, and drawn again the next day, a gentle lesson in impermanence and in the joy of making something beautiful anyway.</p>`,
      terms: [[`Swastika`, `An ancient symbol of well-being; from su (good) and asti (it is).`], [`Yantra`, `A sacred geometric diagram.`], [`Kolam`, `A daily threshold pattern of rice flour, in South India.`]],
      practice: `Draw a simple rangoli or kolam at your door, with chalk, rice flour or flower petals. Begin with a grid of dots and connect them with flowing lines.`,
      links: [[`Diwali`, `#/festival/diwali`]]
    }
  ]
});

/* ---------------------------------------------------------------------- */
/* Temples and places                                                      */
/* ---------------------------------------------------------------------- */
course({
  id: `temples`, deva: `मन्दिर`, category: `temples`, art: `temple`,
  title: `Understanding the Temple`,
  subtitle: `Architecture, worship and etiquette`,
  intro: `A Hindu temple is a model of the cosmos and a home for the divine. Learn how temples are designed, the great regional styles, what happens inside, and how to visit with respect.`,
  lessons: [
    {
      title: `The temple as cosmos`, art: `temple`,
      caption: `The shikhara rises like a sacred mountain above the inner sanctum.`,
      body: `<p>A Hindu temple, <strong>mandir</strong> or <strong>devalaya</strong>, “home of the god,” is far more than a building where people gather. It is designed according to ancient texts, the Agamas and the Shilpa Shastras, as a model of the universe and a dwelling for the divine on earth.</p>
<h3>The sacred plan</h3>
<p>The temple's ground plan is based on a sacred grid called the <strong>vastu purusha mandala</strong>, a square divided into smaller squares, each governed by a deity, with Brahma at the centre. The temple is usually oriented to the east, toward the rising sun.</p>
<h3>Journey to the centre</h3>
<p>Walking into a temple is like a journey from the outer world to the inner self:</p>
<ul><li>You pass through a <strong>gateway</strong> and often a courtyard, where you may see a tall flagstaff, the dhvaja stambha, and the deity's vehicle facing the shrine: Nandi the bull for Shiva, Garuda for Vishnu, a lion for the Goddess.</li><li>You enter the <strong>mandapa</strong>, a pillared hall where devotees gather, sing and wait for darshan.</li><li>At the heart is the <strong>garbhagriha</strong>, the “womb chamber,” a small, dark, plain sanctum that holds the main image. It is deliberately simple and enclosed, like the cave of the heart where the divine is found.</li></ul>
<p>Moving from the bright, busy outer areas to the quiet, dim sanctum mirrors the inward turn of meditation.</p>
<h3>The sacred mountain</h3>
<p>Above the sanctum rises the tower, the <strong>shikhara</strong> (“mountain peak”) in the north or <strong>vimana</strong> in the south. It represents Mount Meru, the axis of the universe, or Mount Kailash, Shiva's home. At its top sits a ribbed stone disc, the amalaka, and a pot-shaped finial, the <strong>kalasha</strong>. The vertical line from the image in the sanctum, up through the tower to the sky, connects earth and heaven.</p>
<h3>A body for the divine</h3>
<p>Many texts describe the temple as a body. The sanctum is the head or heart, the tower the crown, and the deity within is the soul. The carvings on the walls, of gods, sages, dancers, animals and scenes of daily life, show the whole of creation gathered around its source.</p>`,
      terms: [[`Garbhagriha`, `The “womb chamber”: the inner sanctum.`], [`Shikhara`, `The tower above the sanctum, in northern temples.`], [`Mandapa`, `A pillared hall.`], [`Vastu purusha mandala`, `The sacred grid on which a temple is planned.`]],
      practice: `Next time you visit a temple, notice the path from the entrance to the sanctum. Walk it slowly, as a journey inward, and notice how the light and sound change.`
    },
    {
      title: `The great temple styles`, art: `temple-styles`,
      caption: `A northern Nagara shikhara beside a southern Dravida vimana and gopuram.`,
      body: `<p>Across India and beyond, temple builders developed several great styles over more than fifteen centuries. The two main ones are named after the regions where they flourished.</p>
<h3>Nagara: the northern style</h3>
<p>Nagara temples have a tall, curving <strong>shikhara</strong> that rises like a mountain peak, often surrounded by smaller towers clustered around it, and crowned with an amalaka and kalasha. They are usually built on a raised platform. Famous examples include:</p>
<ul><li>the temples of <strong>Khajuraho</strong> in Madhya Pradesh, famous for their sculpture;</li><li>the great temples of <strong>Odisha</strong>, such as the Lingaraja at Bhubaneswar and the Jagannath temple at Puri;</li><li>the <strong>Sun Temple at Konark</strong>, built as a giant stone chariot with carved wheels.</li></ul>
<h3>Dravida: the southern style</h3>
<p>Dravida temples have a stepped, pyramid-shaped tower, the <strong>vimana</strong>, over the sanctum. They are often enclosed by high walls with enormous, brightly painted gateway towers, the <strong>gopurams</strong>, which can be taller than the shrine itself. Large temple tanks and pillared halls are common. Famous examples include:</p>
<ul><li>the <strong>Brihadeeswarar Temple</strong> at Thanjavur, built by the Chola king Rajaraja I over a thousand years ago;</li><li>the <strong>Meenakshi Temple</strong> at Madurai, with its fourteen dazzling gopurams;</li><li>the <strong>Ranganathaswamy Temple</strong> at Srirangam, one of the largest working temple complexes in the world.</li></ul>
<h3>Other styles</h3>
<p>In the Deccan, the <strong>Vesara</strong> style blended northern and southern features, as in the intricately carved Hoysala temples of Belur and Halebidu. Kerala's temples have sloping tiled roofs suited to the monsoon. Bengal developed terracotta temples with curved roofs like village huts. The <strong>Kailasa Temple</strong> at Ellora was carved downward from a single rock face, a marvel of engineering.</p>
<p>Beyond India, <strong>Angkor Wat</strong> in Cambodia, built in the twelfth century for Vishnu, is the largest religious monument on earth, and Bali's temples continue a living Hindu tradition.</p>`,
      terms: [[`Nagara`, `The northern temple style, with a curving shikhara.`], [`Dravida`, `The southern temple style, with a stepped vimana and gopurams.`], [`Gopuram`, `A monumental gateway tower in South Indian temples.`], [`Vesara`, `A Deccan style blending northern and southern features.`]],
      practice: `Look at a photograph of your local temple, or one you have visited. Can you tell whether it follows the northern or southern style, or a blend?`
    },
    {
      title: `Murti and darshan`, art: `darshan`,
      caption: `The lamp-lit sanctum, where devotees come for darshan.`,
      body: `<p>At the heart of every temple is the <strong>murti</strong>, the sacred image of the deity. Visitors sometimes call it an idol, but Hindus understand it very differently. A murti is not God trapped in stone. It is a form through which the formless divine chooses to make itself present and approachable, so that people can see, love and serve it.</p>
<h3>Bringing the image to life</h3>
<p>A murti is carved or cast according to precise rules for its proportions, posture, gestures and symbols. When it is installed, priests perform <strong>prana pratishtha</strong>, “establishing the life-breath,” inviting the deity's presence into the image. Its eyes are opened last, and the first sight of them is considered very powerful.</p>
<h3>Darshan: seeing and being seen</h3>
<p>Hindus go to the temple for <strong>darshan</strong>, “sight.” It is not just looking at the deity. It is a mutual exchange: the devotee sees the divine, and is seen and blessed by it in return. This is why the eyes of murtis are often large and striking, and why devotees stand quietly before the sanctum, hands joined, simply gazing.</p>
<h3>A day in the life of the deity</h3>
<p>In many temples, the deity is treated as a royal and beloved guest, following a daily schedule:</p>
<ul><li>woken before dawn with music and prayers, such as the <em>suprabhatam</em>;</li><li>bathed in a ritual called <strong>abhisheka</strong>, with water, milk, yogurt, honey and other offerings;</li><li>dressed and adorned with clothes, jewels and garlands, called <em>alankara</em>;</li><li>offered food several times a day, and honoured with aarti;</li><li>finally put to rest at night, when the sanctum doors close.</li></ul>
<p>The priests who perform these services are often called <em>pujaris</em> or <em>archakas</em>, and in many temples the role passes down through families for generations.</p>
<h3>Why images?</h3>
<p>Hindu teachers explain that most of us find it hard to love what we cannot see. The murti is a meeting point, like a photograph of a beloved person, but more: a place where God, out of love, makes room for our devotion.</p>`,
      terms: [[`Murti`, `A sacred image in which the deity is present.`], [`Darshan`, `“Sight”: seeing the deity and being seen.`], [`Abhisheka`, `The ritual bathing of the image.`], [`Prana pratishtha`, `The rite that invites the deity into the image.`]],
      practice: `At your next darshan, at a temple or your home shrine, stand quietly for a minute and simply look, without asking for anything. Feel yourself being seen with love.`
    },
    {
      title: `Visiting a temple`, art: `pradakshina`,
      caption: `Walking clockwise around the shrine: pradakshina.`,
      body: `<p>Hindu temples welcome visitors, and a few simple customs will help you feel at ease and show respect. Practices vary between regions and temples, so watch what others do, and don't hesitate to ask.</p>
<h3>Before entering</h3>
<ul><li><strong>Dress modestly</strong>, covering shoulders and knees. Some South Indian temples, especially in Kerala, ask men to remove their shirts and wear a dhoti, and women to wear a sari or long skirt.</li><li><strong>Remove your shoes</strong> before entering, usually at a stand near the gate. Socks are also removed in many temples.</li><li><strong>Wash your hands and feet</strong> if water is provided.</li><li>Bring a small offering if you wish: flowers, fruit, a coconut or sweets, often sold near the gate.</li></ul>
<h3>Inside</h3>
<ul><li>Many devotees ring the <strong>bell</strong> as they enter, to announce their arrival and focus the mind.</li><li>Walk around the shrine <strong>clockwise</strong>, keeping the deity on your right. This is <strong>pradakshina</strong>, an act of reverence that places God at the centre of your life.</li><li>Stand before the sanctum with joined hands for darshan. Avoid pointing your feet toward the deity, and don't touch the murti unless invited.</li><li>When the priest offers the <strong>aarti flame</strong>, pass your hands over it and touch your eyes. Accept holy water, <strong>tirtha</strong>, and <strong>prasad</strong> with your right hand.</li><li>Keep your voice low and switch off your phone. Ask before taking photographs; they are not allowed in many sanctums.</li></ul>
<h3>Who may enter</h3>
<p>Most temples, especially outside India, welcome people of all faiths. A few historic temples, such as the Jagannath temple at Puri, admit only Hindus to the inner areas, following their ancient traditions. If you are unsure, ask at the entrance.</p>
<h3>Before leaving</h3>
<p>Many people sit for a few moments in the temple before leaving, to let the experience settle. You might make a donation in the <strong>hundi</strong>, the offering box, if you wish. Some devotees walk backwards for the first few steps out of the sanctum, so as not to turn their back on the deity.</p>`,
      terms: [[`Pradakshina`, `Walking clockwise around a shrine.`], [`Tirtha`, `Holy water, given as a blessing.`], [`Hundi`, `The temple offering box.`]],
      practice: `Visit a temple this month. Follow these customs, take darshan, and sit quietly for five minutes before you leave.`
    },
    {
      title: `Temples around the world`, art: `skyline`,
      caption: `A Hindu temple among the towers of a modern city.`,
      body: `<p>Over the last two centuries, Hindus have settled in every part of the world: as indentured labourers in the Caribbean, Fiji, Mauritius and South Africa in the nineteenth century, and as students, workers and families in Britain, North America, the Gulf, Australia and Southeast Asia in the twentieth. Wherever they went, they built temples.</p>
<h3>A home away from home</h3>
<p>For communities far from India, the temple became much more than a place of worship. It is where children learn prayers, languages, music and dance; where festivals are celebrated together; where weddings, naming ceremonies and funerals take place; and where newcomers find friends, food and help. Many temples run free community kitchens, language schools and youth groups.</p>
<h3>Some remarkable temples</h3>
<ul><li>In <strong>Trinidad</strong>, the <strong>Temple in the Sea</strong> at Waterloo was built by Sewdass Sadhu, a labourer who, refused land for a temple, spent years building one out in the sea by hand. It stands today as a symbol of devotion and determination.</li><li>In <strong>Mauritius</strong>, hundreds of thousands of pilgrims walk to the crater lake of <strong>Ganga Talao</strong> each Maha Shivaratri.</li><li>In <strong>Malaysia</strong>, the Murugan shrine in the <strong>Batu Caves</strong>, reached by 272 steps, draws vast crowds for Thaipusam.</li><li>In <strong>London</strong>, the hand-carved BAPS Shri Swaminarayan Mandir in Neasden, opened in 1995, was built with stone carved in India and assembled like a giant puzzle.</li><li>In the <strong>United States</strong>, the Sri Venkateswara Temple in Pittsburgh, consecrated in 1977, was one of the first traditional temples in the country, and there are now hundreds more.</li><li>In <strong>Bali</strong>, Indonesia, a distinct Hindu culture has flourished for over a thousand years, with temples in every village.</li></ul>
<h3>Your local temple</h3>
<p>If you live outside India, your local temple may follow a particular tradition, such as North Indian, South Indian, Gujarati, Bengali or Caribbean, or bring several together under one roof, with many deities side by side. Visit, join a festival, volunteer in the kitchen or attend a class. Temples thrive on the seva of their communities, and they are a wonderful way to stay connected to your heritage.</p>`,
      terms: [[`Diaspora`, `Communities living outside their ancestral homeland.`], [`Thaipusam`, `A festival of Murugan, celebrated widely in Malaysia and Singapore.`]],
      practice: `Find out the history of your nearest temple: who built it, when, and which traditions it follows. If you can, offer an hour of seva there this month.`
    }
  ]
});

course({
  id: `pilgrimage`, deva: `तीर्थ`, category: `temples`, art: `pilgrim`,
  title: `Sacred Places and Pilgrimage`,
  subtitle: `Rivers, mountains and holy cities`,
  intro: `Hindus have walked to sacred places for thousands of years. Five lessons on the meaning of pilgrimage and the great holy sites of India, from Varanasi to the Kumbh Mela.`,
  lessons: [
    {
      title: `Why pilgrimage?`, art: `pilgrim`,
      caption: `The pilgrim's path into the mountains.`,
      body: `<p>A Hindu place of pilgrimage is called a <strong>tirtha</strong>, which literally means a “ford” or “crossing place,” a shallow point where a river can be crossed. A tirtha is a place where the boundary between the earthly and the divine is thin, where it is easier to cross over from the ordinary world toward liberation.</p>
<p>Many tirthas are on rivers, especially the Ganga, or at their sources, confluences and meeting points with the sea. Others are on mountains, in forests or in cities sanctified by the presence of a deity, a saint or a great event in sacred history.</p>
<h3>Why people go</h3>
<ul><li><strong>For darshan</strong>, to see and be seen by the deity in a famous temple.</li><li><strong>For purification</strong>, by bathing in a sacred river.</li><li><strong>To fulfil a vow</strong>, made in gratitude or in a time of need.</li><li><strong>For the ancestors</strong>, performing rites for the departed at places like Gaya and Varanasi.</li><li><strong>For the journey itself</strong>, which teaches patience, simplicity, humility and trust.</li></ul>
<h3>The journey matters</h3>
<p>Traditionally, pilgrims travelled on foot, often for weeks or months, living simply, sleeping in rest houses, and depending on the kindness of strangers. Even today, many walk the last stretch, climb the steps on their knees or carry water from one holy river to another. The hardships are part of the pilgrimage: they loosen our attachment to comfort and open the heart.</p>
<p>Pilgrimage also unites. At a great tirtha, rich and poor, young and old, people from every region and language stand side by side, sharing the same river and the same darshan.</p>
<h3>The inner tirtha</h3>
<p>The tradition also warns that outer pilgrimage is not enough on its own. A well-known saying holds that the greatest tirtha is a pure mind, and that bathing in a river cannot wash away the stain of a heart full of anger or greed. The saints remind us that God dwells within, and that the journey to a holy place is, at its best, a journey to the holy place inside ourselves.</p>`,
      terms: [[`Tirtha`, `A place of pilgrimage; literally a “ford” or crossing.`], [`Yatra`, `A pilgrimage journey.`]],
      practice: `Plan a small pilgrimage: a visit to a temple, river or sacred place near you. Go with a simple intention, travel mindfully, and notice how the journey itself affects you.`
    },
    {
      title: `Varanasi and the Ganga`, art: `ghats`,
      caption: `The ghats of Varanasi at dusk, with lamps floating on the Ganga.`,
      body: `<p><strong>Varanasi</strong>, also called <strong>Kashi</strong>, “the city of light,” and Benares, is one of the oldest continuously inhabited cities in the world and the holiest city of Hinduism. It stands on the banks of the river <strong>Ganga</strong>, and it is said to be Shiva's own city, resting on the tip of his trident.</p>
<h3>Mother Ganga</h3>
<p>The Ganga is worshipped as a goddess, <strong>Ganga Ma</strong>. According to the Puranas, she once flowed only in heaven. King Bhagiratha performed long austerities to bring her down to earth, to purify the ashes of his ancestors. Her descent was so powerful that it would have shattered the earth, so Shiva caught her in his matted hair and released her gently. Bathing in the Ganga is believed to wash away sins, and many Hindu homes keep a small vessel of Ganga water, <em>Ganga jal</em>, for blessings and for the dying.</p>
<h3>The ghats</h3>
<p>Varanasi's riverfront is lined with more than eighty <strong>ghats</strong>, wide stone steps leading down to the water. At dawn, pilgrims bathe, offer water to the rising sun, meditate and perform rituals. At <strong>Dashashwamedh Ghat</strong>, the evening <strong>Ganga Aarti</strong> is performed every night: priests wave great multi-tiered lamps in unison to the sound of bells, conches and chanting, while thousands watch and float small leaf-boats of flowers and lamps on the river.</p>
<h3>A place to die</h3>
<p>Many Hindus believe that to die in Kashi brings liberation, because Shiva himself whispers the mantra of release into the ear of the dying. At <strong>Manikarnika Ghat</strong>, cremation fires have burned continuously for centuries. The sight can be startling, but it carries a calm message: death is part of life, and the soul goes on.</p>
<h3>Kashi Vishwanath</h3>
<p>At the heart of the city is the <strong>Kashi Vishwanath Temple</strong>, one of the twelve Jyotirlingas of Shiva. Varanasi is also a great centre of learning, music and the Sanskrit tradition, and the Buddha gave his first teaching nearby at Sarnath.</p>`,
      terms: [[`Kashi`, `“City of light”: Varanasi.`], [`Ghat`, `Stone steps leading down to a river.`], [`Ganga jal`, `Holy water from the Ganga.`], [`Ganga Aarti`, `The evening worship of the river with lamps.`]],
      practice: `Learn the prayer Gange Cha Yamune, which invokes the sacred rivers. Say it the next time you bathe, imagining the water as the Ganga.`,
      links: [[`Gange Cha Yamune`, `#/puja/ganga-snana`], [`Ganga Dussehra`, `#/festival/ganga-dussehra`]]
    },
    {
      title: `The Char Dham`, art: `char-dham`,
      caption: `Four sacred abodes at the four corners of India.`,
      body: `<p>The <strong>Char Dham</strong>, the “four abodes,” are four holy sites at the four corners of India. The tradition is associated with <strong>Adi Shankaracharya</strong>, the great eighth-century teacher, who travelled the length and breadth of India and is said to have encouraged pilgrimage to these four places, uniting the land in a single sacred circle. Visiting all four in one lifetime is considered a great blessing.</p>
<h3>The four abodes</h3>
<ul><li><strong>Badrinath</strong>, in the north, high in the Himalayas of Uttarakhand, is dedicated to Vishnu as Badrinarayan, beside the Alaknanda river. The temple is open only from about May to November; in winter it is buried in snow.</li><li><strong>Puri</strong>, in the east, on the coast of Odisha, is home to <strong>Jagannath</strong>, Lord of the universe, worshipped with his brother Balabhadra and sister Subhadra. Its great chariot festival, the Rath Yatra, draws vast crowds every summer.</li><li><strong>Rameswaram</strong>, in the south, on an island off Tamil Nadu, is where Rama is said to have worshipped Shiva before crossing to Lanka. The Ramanathaswamy temple is famous for its immensely long pillared corridors and its twenty-two sacred wells.</li><li><strong>Dwarka</strong>, in the west, on the coast of Gujarat, is the city of Krishna, who ruled here as king. The Dwarkadhish temple rises above the sea.</li></ul>
<p>Three of the four are dedicated to forms of Vishnu and one to Shiva, a reminder of the unity of the traditions. Shankaracharya also founded four monasteries, or mathas, near these directions, at Sringeri, Dwarka, Puri and Jyotirmath, which still guide the Advaita tradition today.</p>
<h3>The Himalayan Char Dham</h3>
<p>There is also the <strong>Chota Char Dham</strong>, the “little four abodes,” in the Himalayas of Uttarakhand: <strong>Yamunotri</strong> and <strong>Gangotri</strong>, the sources of the Yamuna and Ganga rivers; <strong>Kedarnath</strong>, a Jyotirlinga of Shiva; and Badrinath. Hundreds of thousands make this mountain pilgrimage each season, many on foot along steep trails.</p>`,
      terms: [[`Char Dham`, `The four sacred abodes at the corners of India.`], [`Matha`, `A monastery and centre of teaching.`], [`Rath Yatra`, `The chariot festival of Jagannath at Puri.`]],
      practice: `Find the four Char Dham sites on a map of India. Read a little about one of them, and if you can, look at photographs or a video of its temple.`,
      links: [[`Rath Yatra`, `#/festival/rath-yatra`]]
    },
    {
      title: `Jyotirlingas and Shakti Peethas`, art: `lingam`,
      caption: `The jyotirlinga: Shiva as an endless pillar of light.`,
      body: `<h3>The pillar of light</h3>
<p>A Puranic story tells how Brahma and Vishnu once argued about which of them was greater. Suddenly an immense pillar of fire appeared between them, with no beginning and no end. Vishnu, as a boar, dug down to find its base, and Brahma, as a swan, flew up to find its top. Neither succeeded. Vishnu humbly admitted it; Brahma falsely claimed he had reached the top. The pillar split open and Shiva appeared, revealing himself as the infinite. This is the origin of the <strong>lingam</strong>, and it is celebrated on Maha Shivaratri.</p>
<h3>The twelve Jyotirlingas</h3>
<p>Twelve shrines across India are revered as <strong>Jyotirlingas</strong>, places where Shiva manifested as this pillar of light:</p>
<ul><li><strong>Somnath</strong> and <strong>Nageshvara</strong> in Gujarat;</li><li><strong>Mallikarjuna</strong> at Srisailam in Andhra Pradesh;</li><li><strong>Mahakaleshwar</strong> at Ujjain and <strong>Omkareshwar</strong> in Madhya Pradesh;</li><li><strong>Kedarnath</strong> in the Himalayas;</li><li><strong>Bhimashankar</strong>, <strong>Trimbakeshwar</strong> near Nashik, and <strong>Grishneshwar</strong> near Ellora, in Maharashtra;</li><li><strong>Kashi Vishwanath</strong> in Varanasi;</li><li><strong>Vaidyanath</strong>, most often identified with Deoghar in Jharkhand;</li><li><strong>Rameswaram</strong> in Tamil Nadu.</li></ul>
<p>Some locations are claimed by more than one town, a sign of how deeply loved these shrines are.</p>
<h3>The Shakti Peethas</h3>
<p>The Goddess has her own sacred geography. When Sati, Shiva's first wife, gave up her life in protest at her father Daksha's insult to Shiva, the grieving Shiva carried her body across the universe. To end his grief, Vishnu's discus divided it, and the places where parts of her body fell became the <strong>Shakti Peethas</strong>, seats of the Goddess. Traditions count 51, 52 or even 108 of them, across India and in Nepal, Bangladesh, Pakistan and Sri Lanka.</p>
<p>Among the best known are <strong>Kamakhya</strong> in Assam, <strong>Kalighat</strong> in Kolkata, <strong>Jwalamukhi</strong> in Himachal Pradesh, where natural flames burn from the rock, and <strong>Hinglaj</strong> in Pakistan. The cave shrine of <strong>Vaishno Devi</strong> in Jammu, though not always counted among them, draws millions of pilgrims each year.</p>`,
      terms: [[`Jyotirlinga`, `A shrine where Shiva appeared as a pillar of light.`], [`Shakti Peetha`, `A seat of the Goddess, where part of Sati's body fell.`], [`Sati`, `Shiva's first wife, reborn as Parvati.`]],
      practice: `Choose one Jyotirlinga or Shakti Peetha and read its story. On the next Maha Shivaratri or Navaratri, remember it in your prayers.`,
      links: [[`Maha Shivaratri`, `#/festival/maha-shivaratri`], [`Om Namah Shivaya`, `#/puja/shiva`]]
    },
    {
      title: `The Kumbh Mela and great gatherings`, art: `kumbh`,
      caption: `The pot of nectar above the meeting of sacred rivers.`,
      body: `<p>The <strong>Kumbh Mela</strong> is the largest religious gathering on earth. Over a few weeks, tens of millions of pilgrims, and at the greatest gatherings well over a hundred million, come to bathe in a sacred river at an astrologically auspicious time. UNESCO recognises it as part of the intangible cultural heritage of humanity.</p>
<h3>The pot of nectar</h3>
<p><em>Kumbh</em> means “pot.” The festival recalls the churning of the ocean, when the gods and demons fought over the pot of <strong>amrita</strong>, the nectar of immortality. As the pot was carried away, four drops fell to earth, at <strong>Prayagraj</strong>, <strong>Haridwar</strong>, <strong>Ujjain</strong> and <strong>Nashik</strong>. The Kumbh Mela rotates between these four cities, returning to each roughly every twelve years, when the planets are in the right positions.</p>
<h3>The four sites</h3>
<ul><li><strong>Prayagraj</strong>, at the <strong>Triveni Sangam</strong>, where the Ganga and Yamuna meet the hidden, mythical Sarasvati. Its Maha Kumbh is the greatest of all.</li><li><strong>Haridwar</strong>, where the Ganga leaves the mountains for the plains.</li><li><strong>Ujjain</strong>, on the Shipra river, home of the Mahakaleshwar Jyotirlinga.</li><li><strong>Nashik</strong>, on the Godavari river.</li></ul>
<h3>The sadhus</h3>
<p>One of the most striking sights of the Kumbh is the great processions of sadhus, holy men and women of the ascetic orders, called <em>akharas</em>, some covered only in ash, who lead the way into the river for the royal bath, the <em>shahi snan</em>. Around them a temporary city springs up, with tents, kitchens, hospitals and endless discourses, songs and prayers.</p>
<h3>Other great gatherings</h3>
<ul><li><strong>Tirupati</strong> in Andhra Pradesh, home of Lord Venkateswara, is one of the most visited pilgrimage sites in the world; many devotees offer their hair there in gratitude.</li><li><strong>Sabarimala</strong> in Kerala draws millions of devotees of Ayyappa, who keep a strict 41-day vow before climbing the hill.</li><li>The <strong>Pandharpur Wari</strong> in Maharashtra sees hundreds of thousands walk for weeks, singing, to the shrine of Vithoba.</li><li>The <strong>Amarnath</strong> cave in Kashmir, with its natural ice lingam, and <strong>Mount Kailash</strong> in Tibet, Shiva's abode, are among the most demanding journeys of all.</li></ul>`,
      terms: [[`Kumbh Mela`, `The great gathering at the four sites of the nectar.`], [`Triveni Sangam`, `The meeting of the Ganga, Yamuna and Sarasvati at Prayagraj.`], [`Akhara`, `An order of sadhus.`]],
      practice: `Watch a short documentary or photo essay about the Kumbh Mela. Notice the faces of the pilgrims, and think about what draws so many people together.`,
      links: [[`Course: Kurma and the churning of the ocean`, `#/academy/avatars/3`]]
    }
  ]
});
