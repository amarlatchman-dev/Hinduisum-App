#!/usr/bin/env python3
"""Add more of the principal Upanishads to texts/upanishads/, after the Isa, Katha and Kena.

Usage:
  python3 scripts/build_upanishads.py <sbe_html_dir> <wikitext_dir>

  sbe_html_dir  Wikisource pages saved with action=render, file names URL-quoted:
                "Sacred Books of the East/Volume 15/Prasña-upanishad", ".../Mundaka-upanishad"
                and "Sacred Books of the East/Volume 1/Khândogya-upanishad/<First…Eighth> Prapâthaka"
                (F. Max Müller, 1879 and 1884)
  wikitext_dir  "Taittiriya Upanishad" and "Sacred Books of the East/Volume 1/Aitareya-âranyaka"
                saved with action=raw (Müller's translation, 1879 and 1884)

The Mandukya, which Müller did not translate, is R. E. Hume's version (1921), cleaned by hand
from the scan and kept in this file. Müller's transliteration (italic k for ch, italic g for j,
circumflexed vowels) is turned into the plain spelling used across the app, so that
Khândogya becomes Chandogya and Nakiketas becomes Nachiketas.
"""
import json
import os
import re
import sys
import unicodedata
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_more_texts import write  # noqa: E402
from build_vedas import clean_html  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")
ORD = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
       "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth", "seventeenth",
       "eighteenth", "nineteenth", "twentieth", "twenty-first", "twenty-second", "twenty-third",
       "twenty-fourth", "twenty-fifth", "twenty-sixth"]
ORD_RE = "|".join(sorted(ORD, key=len, reverse=True))


# --------------------------------------------------------------------------- spelling
def sbe_italics(t):
    """In the Sacred Books of the East an italic letter marks a Sanskrit sound: k is ch, g is j,
    and italic n, m, s, h, t, d and ri are the dotted letters. Only short runs of those letters
    are touched, so ordinary italic words stay as they are."""
    def fix(m):
        s = m.group(1)
        if len(s) > 5 or not re.fullmatch(r"[kKgGhnNmMsStTdDrRia]+", s) or s in ("Rik", "Rig", "rik", "rig"):
            return s
        return s.replace("k", "ch").replace("K", "Ch").replace("g", "j").replace("G", "J")
    return re.sub(r"<i\b[^>]*>([^<]*)</i>", fix, t)


def plain(s):
    """Drop diacritics from Latin letters (â to a, ṅ to n) and tidy the punctuation."""
    s = "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))
    s = s.replace("'g", "j").replace("’", "'").replace("‘", "'")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,;:.!?])", r"\1", s)
    s = re.sub(r",(?=[A-Za-z])", ", ", s).replace("theVedas", "the Vedas")
    s = re.sub(r"([:,] )' (?=\w)", r"\1'", s)        # an opening quote set apart from its word
    # a word set in small capitals at the start of a verse
    return re.sub(r"^([A-Z]{2,})\b", lambda m: m.group(1).capitalize(), s)


# --------------------------------------------------------------------------- Müller's pages
def sbe_text(cache, title):
    f = os.path.join(cache, urllib.parse.quote(title, safe="") + ".html")
    t = clean_html(sbe_italics(open(f, encoding="utf-8").read()))
    t = t.split("\n\nFootnotes", 1)[0]
    return [p.strip() for p in re.split(r"\n\s*\n", t) if p.strip()]


def parse(paras, start, section_re, sub_re=None, sub_name=None, refs=lambda sec, sub, n: f"{sec}.{n}"):
    """Numbered paragraphs grouped under section headings (Questions, Mundakas, Prapathakas)
    and, within them, sub-headings (Khandas) that become verse headings."""
    sections, sec, sub, head = [], None, 0, None
    started = False
    for p in paras:
        h = plain(p)                                  # headings are matched without diacritics
        if not started:
            started = bool(re.fullmatch(start, h, re.I))
            if not started:
                continue
        m = re.fullmatch(section_re, h, re.I)
        if m:
            sec = {"verses": [], "_n": len(sections) + 1, "_title": p}
            sections.append(sec)
            sub, head = 0, None
            continue
        if sub_re and re.fullmatch(sub_re, h, re.I):
            sub += 1
            head = sub_name(sub)
            continue
        if sec is None:
            continue
        m = re.match(r"(\d+)\.\s+(.*)", p, re.S)
        if m:
            v = {"n": len(sec["verses"]) + 1, "ref": refs(sec["_n"], sub, int(m.group(1))), "en": m.group(2)}
            if head:
                v["head"], head = head, None
            sec["verses"].append(v)
        elif sec["verses"]:
            sec["verses"][-1]["en"] += " " + p   # a paragraph continuing the verse
        else:
            sec.setdefault("_pre", []).append(plain(p))   # an invocation before the first verse
    for s in sections:
        for v in s["verses"]:
            v["en"] = plain(v["en"])
    return sections


def finish(sections, labels, names=None, intro=None):
    out = []
    for i, s in enumerate(sections):
        sec = {"label": labels[i], "short": str(i + 1)}
        if names:
            sec["name"] = names[i]
        pre = (intro if i == 0 and intro else []) + s.get("_pre", []) + s.get("_intro", [])
        if pre:
            sec["intro"] = pre
        sec["verses"] = s["verses"]
        out.append(sec)
    return {"sections": out}


def prasna(cache):
    paras = sbe_text(cache, "Sacred Books of the East/Volume 15/Prasña-upanishad")
    secs = parse(paras, r"PRASNA-UPANISHAD\.?", rf"({ORD_RE}) QUESTION\.?")
    names = ["Whence are creatures born?", "Which powers uphold the body?", "Whence comes breath?",
             "What sleeps and what wakes in man?", "Meditation on Om", "The Person of sixteen parts"]
    return finish(secs, [f"{o.capitalize()} Question" for o in ORD[:6]], names, intro=[
        "Six seekers of Brahman come to the sage Pippalada, fuel in hand, and after a year of "
        "discipline each asks him one question: where creatures come from, which powers hold up "
        "the body, how breath enters it, what sleeps and what keeps awake in sleep, what comes of "
        "meditating on Om, and who is the Person of sixteen parts. The Prasna belongs to the "
        "Atharva Veda."])


def mundaka(cache):
    paras = sbe_text(cache, "Sacred Books of the East/Volume 15/Mundaka-upanishad")
    secs = parse(paras, r"MUNDAKA-UPANISHAD\.?", rf"({ORD_RE}) MUNDAKA\.?", rf"({ORD_RE}) Khanda\.?",
                 lambda k: f"{ORD[k - 1].capitalize()} Khanda", lambda s, k, n: f"{s}.{k}.{n}")
    names = ["The higher and the lower knowledge", "The Imperishable, like sparks from a fire",
             "Two birds on one tree"]
    return finish(secs, [f"{o.capitalize()} Mundaka" for o in ORD[:3]], names, intro=[
        "The sage Angiras tells the householder Saunaka of two kinds of knowledge: the lower, "
        "which is the Vedas and their sciences, and the higher, by which the Imperishable is "
        "known. Its images have travelled far: the spider spinning out its thread, the sparks "
        "that leap from a fire, the two birds on one tree, and the rivers losing their names in "
        "the sea. India's national motto, Satyameva jayate, 'Truth alone conquers', comes from "
        "its third Mundaka (3.1.6)."])


def mandukya():
    lines = [
        ("The mystic symbolism of the word Om: identified with the fourfold Brahman",
         "Om!—This syllable is this whole world. Its further explanation is:—The past, the present, "
         "the future—everything is just the word Om. And whatever else that transcends threefold "
         "time—that, too, is just the word Om."),
        (None, "For truly, everything here is Brahma; this self (atman) is Brahma. This same self has "
               "four fourths."),
        ("The word Om, in its sounds, as the four states of the Self",
         "The waking state (jagarita-sthana), outwardly cognitive, having seven limbs, having "
         "nineteen mouths, enjoying the gross (sthula-bhuj), the Common-to-all-men (vaisvanara), "
         "is the first fourth."),
        (None, "The dreaming state (svapna-sthana), inwardly cognitive, having seven limbs, having "
               "nineteen mouths, enjoying the exquisite (pravivikta-bhuj), the Brilliant (taijasa), is "
               "the second fourth."),
        (None, "If one asleep desires no desire whatsoever, sees no dream whatsoever, that is deep sleep "
               "(sushupta). The deep-sleep state (sushupta-sthana), unified (eki-bhuta), just (eva) a "
               "cognition-mass (prajnana-ghana), consisting of bliss (ananda-maya), enjoying bliss "
               "(ananda-bhuj), whose mouth is thought (cetas-), the Cognitional (prajna), is the third "
               "fourth."),
        (None, "This is the lord of all (sarvesvara). This is the all-knowing (sarva-jna). This is the "
               "inner controller (antaryamin). This is the source (yoni) of all, for this is the origin "
               "and the end (prabhavapyayau) of beings."),
        (None, "Not inwardly cognitive (antah-prajna), not outwardly cognitive (bahih-prajna), not "
               "both-wise cognitive (ubhayatah-prajna), not a cognition-mass (prajnana-ghana), not "
               "cognitive (prajna), not non-cognitive (a-prajna), unseen (a-drishta), with which there "
               "can be no dealing (a-vyavaharya), ungraspable (a-grahya), having no distinctive mark "
               "(a-lakshana), non-thinkable (a-cintya), that cannot be designated (a-vyapadesya), the "
               "essence of the assurance of which is the state of being one with the Self "
               "(ekatmya-pratyaya-sara), the cessation of development (prapancopasama), tranquil "
               "(santa), benign (siva), without a second (a-dvaita)—[such] they think is the fourth. He "
               "is the Self (Atman). He should be discerned."),
        (None, "This is the Self with regard to the word Om, with regard to its elements. The elements "
               "(matra) are the fourths; the fourths, the elements: the letter a, the letter u, the "
               "letter m."),
        (None, "The waking state, the Common-to-all-men, is the letter a, the first element, from apti "
               "('obtaining') or from adimatva ('being first'). He obtains, verily, indeed, all desires, "
               "he becomes first—he who knows this."),
        (None, "The sleeping state, the Brilliant, is the letter u, the second element, from utkarsha "
               "('exaltation') or from ubhayatva ('intermediateness'). He exalts, verily, indeed, the "
               "continuity of knowledge; and he becomes equal (samana); no one ignorant of Brahma is "
               "born in the family of him who knows this."),
        (None, "The deep-sleep state, the Cognitional, is the letter m, the third element, from miti "
               "('erecting') or from apiti ('immerging'). He, verily, indeed, erects (minoti) this whole "
               "world, and he becomes its immerging—he who knows this."),
        (None, "The fourth is without an element, with which there can be no dealing, the cessation of "
               "development, benign, without a second. Thus Om is the Self (Atman) indeed. He who knows "
               "this, with his self enters the Self—yea, he who knows this!"),
    ]
    verses = []
    for i, (head, en) in enumerate(lines, 1):
        v = {"n": i, "ref": str(i), "en": en}
        if head:
            v["head"] = head
        verses.append(v)
    return {"sections": [{
        "label": "The Mandukya", "short": "1", "name": "Om and the four states of the Self",
        "intro": ["The shortest of the principal Upanishads, twelve verses long, and to many the "
                  "deepest. It reads the sacred syllable Om as a map of consciousness: its sounds a, "
                  "u and m are waking, dreaming and deep sleep, and the silence after it is the "
                  "Fourth (turiya), the Self beyond them all. The great teacher Gaudapada wrote his "
                  "Karika on it, and Shankara commented on both. Translated by Robert Ernest Hume "
                  "(1921)."],
        "verses": verses}]}


def taittiriya(wikidir):
    t = open(os.path.join(wikidir, urllib.parse.quote("Taittiriya Upanishad", safe="") + ".wiki"),
             encoding="utf-8").read()
    t = t.split("==Taittiryaka Upanishad==", 1)[1]
    t = re.sub(r"\{\{[^{}]*\}\}|\[\[[^\]]*\]\]", "", t)
    t = re.sub(r"\(\d+(-\d+)?\)\s*", "", t)          # the old Sanskrit section marks, "(1-5)"
    t = t.replace("Anuvaku", "Anuvaka").replace("Eight Anuvaka", "Eighth Anuvaka")
    # this transcription dropped Müller's italics, so his g for j and k for ch are fixed by hand
    for a, b in [("Pragapati", "Prajapati"), ("Yagus", "Yajus"), ("Agana", "Ajana"), ("virag", "viraj"),
                 ("Satyavakas", "Satyavachas"), ("vignana", "vijnana"), ("Prakinayogya", "Prachinayogya"),
                 ("Mahakamasya", "Mahachamasya"), ("cats food", "eats food")]:
        t = re.sub(rf"\b{a}\b", b, t)
    sections, sec, anu, head, numbered = [], None, 0, None, False
    for p in [p.strip() for p in re.split(r"\n\s*\n|\n(?=[=\d])|(?<==)\n", t) if p.strip()]:
        if re.fullmatch(r"===\s*(\w+) Valli\s*===", p):
            sec = {"verses": [], "_n": len(sections) + 1}
            sections.append(sec)
            anu, head = 0, None
            continue
        m = re.fullmatch(r"====\s*([\w-]+) Anuvaka\.?\s*====", p)
        if m:
            anu, head, numbered = ORD.index(m.group(1).lower()) + 1, f"{m.group(1)} Anuvaka", False
            continue
        if re.fullmatch(r"(OR, )?THE CHAPTER [A-Z ,()]+\.?", p):
            continue                                  # chapter titles; the section names say the same
        m = re.match(r"(\d+)\.\s+(.*)", p, re.S)
        if m:
            numbered = True
            ref, p = f"{sec['_n']}.{anu}.{m.group(1)}", m.group(2)
        elif anu == 0:
            ref = "Peace Chant"                       # the invocation that opens each Valli
        elif numbered or (not head and sec["verses"] and sec["verses"][-1]["en"].endswith(":")):
            sec["verses"][-1]["en"] += " " + p        # continuing a numbered verse, or the Sloka announced
            continue
        else:
            ref = f"{sec['_n']}.{anu}"                # the later Anuvakas have unnumbered paragraphs
        v = {"n": len(sec["verses"]) + 1, "ref": ref, "en": p}
        if head:
            v["head"], head = head, None
        sec["verses"].append(v)
    for s in sections:
        for v in s["verses"]:
            v["en"] = plain(v["en"])
    names = ["Siksha Valli · on recitation and the teacher", "Brahmananda Valli · the bliss of Brahman",
             "Bhrigu Valli · Bhrigu learns from his father"]
    out = finish(sections, ["First Valli", "Second Valli", "Third Valli"], names, intro=[
        "The Taittiriya belongs to the Black Yajur Veda. Its first part is a teacher's guide, ending "
        "with the famous farewell to the graduating student: 'Speak the truth. Do your duty. Let "
        "your mother be a god to you, your father, your teacher and your guest.' The second "
        "unfolds the five sheaths of the Self, from the body of food to the body of bliss; in the "
        "third, Bhrigu discovers them for himself, step by step, through tapas."])
    return out


def aitareya(wikidir):
    """The Aitareya Upanishad is the fourth to sixth Adhyayas of the second Aranyaka of the
    Aitareya-aranyaka; the seventh is its closing peace chant."""
    f = os.path.join(wikidir, urllib.parse.quote("Sacred Books of the East/Volume 1/Aitareya-âranyaka", safe="") + ".wiki")
    t = open(f, encoding="utf-8").read()
    t = t.split("===SECOND ARANYAKA===", 1)[1].split("===THIRD ARANYAKA===", 1)[0]
    t = t.split("====FOURTH ADHYAYA====", 1)[1]
    t = re.sub(r"\{\{[^{}]*\}\}|\[\[[^\]]*\]\]", "", t)
    t = re.sub(r"\s*\(\d+\)", "", t)                  # the Upanishad's own verse marks
    t = re.sub(r"(?m)^:", "", t)
    for a, b in [("ditya", "Aditya"), ("Marikis", "Marichis"), ("Mariki", "Marichi"), ("Pragapati", "Prajapati"), ("mutrti", "murti"),
                 ("Hari, Om", "Harih, Om")]:
        t = re.sub(rf"(?<![A-Za-z]){a}\b", b, t)
    chapters = [("FOURTH", t.split("====FIFTH ADHYAYA====")[0]),
                ("FIFTH", t.split("====FIFTH ADHYAYA====")[1].split("====SIXTH ADHYAYA====")[0]),
                ("SIXTH", t.split("====SIXTH ADHYAYA====")[1].split("====SEVENTH ADHYAYA====")[0])]
    peace = t.split("====SEVENTH ADHYAYA====")[1]
    sections = []
    for ch, (_, body) in enumerate(chapters, 1):
        sec, khanda, head = {"verses": [], "_pre": []}, 0, None
        for p in [p.strip() for p in re.split(r"\n\s*\n|\n(?=[=\d])|(?<==)\n", body) if p.strip()]:
            m = re.fullmatch(r"=====\s*([A-Z]+) KHANDA:?\s*=====", p)
            if m:
                khanda = ORD.index(m.group(1).lower()) + 1
                head = f"{m.group(1).capitalize()} Khanda" if ch == 1 else None
                continue
            m = re.match(r"(\d+)\.\s+(.*)", p, re.S)
            if m:
                v = {"n": len(sec["verses"]) + 1, "ref": f"{ch}.{khanda}.{m.group(1)}", "en": m.group(2)}
                if head:
                    v["head"], head = head, None
                sec["verses"].append(v)
            elif sec["verses"]:
                sec["verses"][-1]["en"] += " " + p
            else:
                sec["_pre"].append(plain(p))
        sections.append(sec)
    chant = re.sub(r"=+[^=]+=+", "", peace).strip()
    chant = re.sub(r"^1\.\s+", "", chant)
    sections[-1]["verses"].append({"n": len(sections[-1]["verses"]) + 1, "ref": "Peace Chant", "en": chant})
    for s in sections:
        for v in s["verses"]:
            v["en"] = plain(v["en"])
    names = ["The Self sends forth the worlds and the Person", "The three births of the Self",
             "Consciousness is Brahman"]
    return finish(sections, ["First Adhyaya", "Second Adhyaya", "Third Adhyaya"], names, intro=[
        "The Aitareya belongs to the Rig Veda, where it forms part of the Aitareya Aranyaka. In the "
        "beginning, it says, there was only the Self, which sent forth the worlds, the cosmic Person "
        "and the powers of the senses, and then entered the body through the crown of the head to "
        "dwell in it. It ends in one of the four great sayings of the Vedanta: 'Consciousness is "
        "Brahman' (prajnanam brahma)."])


def chandogya(cache):
    sections = []
    for i, o in enumerate(ORD[:8], 1):
        paras = sbe_text(cache, f"Sacred Books of the East/Volume 1/Khândogya-upanishad/{o.capitalize()} Prapâthaka")
        secs = parse(paras, rf"{o} PRAPATHAKA\.?", rf"{o} PRAPATHAKA\.?", rf"({ORD_RE}) Khanda\.?",
                     lambda k: f"{ORD[k - 1].capitalize()} Khanda", lambda s, k, n, i=i: f"{i}.{k}.{n}")
        assert len(secs) == 1, (o, len(secs))
        sections += secs
    names = ["Om and the Udgitha", "The Saman chant and the stages of life", "The honey of the sun; "
             "Sandilya's teaching", "Satyakama and Upakosala", "The five fires and the universal Self",
             "Tat tvam asi · Uddalaka teaches Svetaketu", "Narada learns the infinite from Sanatkumara",
             "The city of Brahman; Indra and Prajapati"]
    return finish(sections, [f"{o.capitalize()} Prapathaka" for o in ORD[:8]], names, intro=[
        "One of the oldest and longest Upanishads, belonging to the Sama Veda. It begins with the "
        "meditation on Om as the essence of the sacred chant and rises to some of the most "
        "celebrated teachings in Indian thought: Sandilya's 'All this is Brahman', the honest "
        "Satyakama accepted as a student for his truthfulness, and, in the sixth Prapathaka, the "
        "sage Uddalaka showing his son Svetaketu, with salt dissolved in water and the seed of a "
        "fig, that the subtle essence of all things is the Self: 'That thou art' (tat tvam asi)."])


# Parts 1-3 (Isa, Katha, Kena, Paramananda) are built by build_more_texts.py.
PARTS = [
    (4, "Prasna Upanishad", "Six questions to Pippalada", prasna),
    (5, "Mundaka Upanishad", "The higher knowledge", mundaka),
    (6, "Mandukya Upanishad", "Om and the four states", None),
    (7, "Taittiriya Upanishad", "The five sheaths of the Self", None),
    (8, "Aitareya Upanishad", "Consciousness is Brahman", None),
    (9, "Chandogya Upanishad", "That thou art", chandogya),
]


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cache, wikidir = sys.argv[1], sys.argv[2]
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    parts = [p for p in index["upanishads"]["parts"] if p["n"] <= 3]
    for n, name, sub, fn in PARTS:
        data = mandukya() if n == 6 else taittiriya(wikidir) if n == 7 else aitareya(wikidir) if n == 8 else fn(cache)
        size = write(f"upanishads/{n}.json", data)
        verses = sum(len(s["verses"]) for s in data["sections"])
        print(f"upanishads/{n}.json  {name}: {len(data['sections'])} sections, {verses} verses, {size // 1024} KB")
        parts.append({"n": n, "name": name, "sub": sub, "count": len(data["sections"])})
    index["upanishads"]["parts"] = parts
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    main()
