#!/usr/bin/env python3
"""Add more Puranas to texts/, from public-domain English translations.

Usage:
  pip install wordfreq
  python3 scripts/build_puranas.py garuda <garuda.txt>
  python3 scripts/build_puranas.py devi <devi.txt>

  garuda.txt  the text of Ernest Wood and S. V. Subrahmanyam, The Garuda Purana (Saroddhara),
              1911, as on archive.org ("the-garuda-purana-ernest-wood-s.-v.-subrahmanyam",
              the _djvu.txt file of the Global Grey edition)
  devi.txt    Swami Vijnanananda, The Srimad Devi Bhagawatam, 1921-23, as on archive.org
              ("the-srimad-devi-bhagawatam-swami-vijnanananda", the _djvu.txt file)

Each Purana is a book of its own in the library. Verses keep the translators' numbering
(single verses and runs such as 19-21); the footnote markers and notes are dropped, and
Sanskrit names are spelled as elsewhere in the app (Vishnu, Krishna, Rishi).
"""
import json
import os
import re
import sys

from wordfreq import zipf_frequency

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_more_texts import write  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")

# The scans drop the dots and macrons of Sanskrit, leaving s for sh and ri as r.
NAMES = {
    "Visnu": "Vishnu", "Krsna": "Krishna", "Laksman": "Lakshman", "Laksmana": "Lakshmana", "Laksmi": "Lakshmi",
    "Upanisad": "Upanishad", "Upanisads": "Upanishads", "Rsi": "Rishi", "Rsis": "Rishis", "risis": "rishis",
    "Tarksya": "Tarkshya", "Naimisa": "Naimisha", "Visnu's": "Vishnu's", "Krsna's": "Krishna's",
    "Brhaspati": "Brihaspati", "Rgveda": "Rigveda", "Purusa": "Purusha", "Isvara": "Ishvara", "Vaisnava": "Vaishnava",
    "Ganesa": "Ganesha", "Sesa": "Shesha", "Dharmaraja": "Dharmaraja", "Sraddha": "Shraddha", "sraddha": "shraddha",
    "Sraddhas": "Shraddhas", "sraddhas": "shraddhas", "Kasi": "Kashi", "Gaya": "Gaya", "Paramatman": "Paramatman",
    "Rgveda's": "Rigveda's", "Rama": "Rama", "Prajapati": "Prajapati", "Yamaraja": "Yamaraja",
}

NAMES.update({
    "Krisna": "Krishna", "Sastras": "Shastras", "Sastra": "Shastra", "Kesava": "Keshava", "Vaisya": "Vaishya",
    "Vaisyas": "Vaishyas", "Ksattriya": "Kshatriya", "Ksattriyas": "Kshatriyas", "Kasyapa": "Kashyapa",
    "Riksa": "Riksha", "Susumna": "Sushumna", "Iswara": "Ishvara", "Payovarsana": "Payovarshana",
    "Savisa": "Savisha", "Vaidic": "Vedic", "Siva": "Shiva", "Sudra": "Shudra", "Sudras": "Shudras",
})
FIXES = [  # single misreadings in the scans
    ("Fatherl'-again", "Father!—again"), ("Haying", "Having"), ("foeces", "faeces"), ("Kud mala", "Kudmala"),
    ("Saiighata", "Sanghata"), ("Shail agama", "Shailagama"), ("Bahwapad a", "Bahwapada"),
    ("Bah ubhiti", "Bahubhiti"),
]


def word_ok(w):
    return zipf_frequency(w.lower(), "en") >= 1.5


def tidy(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(?<=[a-z])T\b|(?<=[A-Za-z])T(?=[a-z])", "i", s)  # a long i read as T (VaitaranT, KumbhTpaka)
    s = re.sub(r"(?<=[a-z])G(?=[a-z])", "u", s)      # and a long u as G (ManipGraka)
    s = re.sub(r"\b([A-Z][a-z]+)I\b", r"\1i", s)      # or as I (LaksmI, GaurI)
    s = re.sub(r"\bDev!", "Devi", s).replace("SIta", "Sita")
    s = re.sub(r"\bOe (?=[A-Z])", "Of ", s)
    for a, b in FIXES:
        s = s.replace(a, b)
    s = re.sub(r"\s+([,;:.!?])", r"\1", s)
    s = re.sub(r",,+", ",", s)
    s = re.sub(r"([.:;,])-(?=[A-Za-z])", r"\1—", s)  # the scan's dash after punctuation
    s = re.sub(r"(?<=[a-z]),-(?=[a-z])", ",—", s)
    s = re.sub(r":--?\s*", ": ", s)
    s = re.sub(r"\b[A-Z][a-z]+(?:'s)?\b", lambda m: NAMES.get(m.group(0), m.group(0)), s)
    return re.sub(r"\b[A-Z][a-zA-Z]+\b", sanskrit_name, s)


def sanskrit_name(m):
    """The scans print the retroflex s as a plain s. In Sanskrit an s after i, u, r or k is that
    retroflex sh, so Maharsi, Nahusa and Moksa become Maharshi, Nahusha and Moksha; English words
    (Visit, Russia) are left alone, as is a final s, which is usually an English plural."""
    w = m.group(0)
    if zipf_frequency(w.lower(), "en") >= 2.0:
        return w
    w = re.sub(r"sV(?=[a-z])", "shv", w)              # VisVamitra
    w = re.sub(r"(?<=[iurk])s(?=[aeiounk])", "sh", w)
    return re.sub(r"ajh(?=a)", "ajn", w).replace("Yoyana", "Yojana")


def join_lines(lines):
    """Join a paragraph's lines, undoing end-of-line hyphenation where the joined word is a word."""
    out = ""
    for l in lines:
        l = l.strip()
        if not out:
            out = l
        elif out.endswith("-") and not out.endswith("--"):
            head = re.search(r"(\w+)-$", out)
            tail = re.match(r"(\w+)", l)
            if head and tail and word_ok(head.group(1) + tail.group(1)) and not word_ok(tail.group(1)):
                out = out[:-1] + l
            else:
                out += l
        else:
            out += " " + l
    return out


def furniture(line):
    """Footnote markers on lines of their own (12, 87-34), and Sanskrit printed in Devanagari,
    which the scan turned into strings like "qfcra?n niff i" or "11 v 11"."""
    if not line:
        return False
    if re.fullmatch(r"[\d\s_,.;:'`\-kl]*", line) and re.search(r"\d", line):
        return True
    if re.search(r"[\^*«»\\|`<>{}=%$]|[a-z][A-Z]{2}|\s(II|11|ll|n|i|I|l)\s*$", line):
        words = [w for w in re.findall(r"[A-Za-z]+", line) if len(w) > 1]
        real = [w for w in words if len(w) > 2 and zipf_frequency(w.lower(), "en") >= 3.5]
        return len(real) < 0.6 * len(words) or not words
    return False


def number_verses(paras, chapter):
    """Paragraphs that open with a verse number (3., 3-5. or a misprinted 3-5) start a verse; the
    rest continue the one before. A number that breaks the sequence but sits between two good
    ones is a misreading (40 for 49); each verse runs up to the one after it."""
    start = re.compile(r"(\d{1,3})(?:\s*-\s*\.?(\d{1,3}))?\.?\s+(?=[A-Z'\"(\[])")
    marks = [(j, int(m.group(1)), int(m.group(2)) if m.group(2) else None, m.end())
             for j, p in enumerate(paras) for m in [start.match(p)] if m]
    accepted, last = [], 0                              # last: the last verse number covered so far
    for x, (j, lo, hi, end) in enumerate(marks):
        nxt = marks[x + 1][1] if x + 1 < len(marks) else None
        good_hi = hi if hi and last < hi <= last + 20 else None
        if last < lo <= last + 9 or hi and 0 < hi - lo < 12 and last < lo <= last + 20:
            accepted.append([j, lo, hi, end])
            last = hi if hi and 0 < hi - lo < 12 else lo
        elif good_hi:
            # the first number misread (88-41 for 38-41); after a long gap (verses this
            # translation gives only in Sanskrit) it stands alone
            accepted.append([j, last + 1 if good_hi - last <= 8 else good_hi, good_hi, end])
            last = good_hi
        elif nxt is not None and last + 1 < nxt <= last + 10:
            accepted.append([j, last + 1, None, end])     # a misread number between two good ones
            last += 1
    verses = []
    first = accepted[0][0] if accepted else len(paras)
    if first > 0:                                     # paragraphs before the first number
        verses.append({"lo": 0, "hi": 0, "en": "\n".join(paras[:first])})
    for x, (j, lo, hi, end) in enumerate(accepted):
        until = accepted[x + 1][0] if x + 1 < len(accepted) else len(paras)
        nxt_lo = accepted[x + 1][1] if x + 1 < len(accepted) else None
        if hi is not None and 0 <= hi - lo < 12 and (not nxt_lo or hi < nxt_lo):
            pass                                          # the printed range
        else:
            hi = min(nxt_lo - 1, lo + 11) if nxt_lo else lo
        verses.append({"lo": lo, "hi": max(hi, lo), "en": "\n".join([paras[j][end:]] + paras[j + 1:until])})
    # one entry per paragraph: the first of a verse carries its number, the rest none
    out = []
    for v in verses:
        for q, para in enumerate(v["en"].split("\n")):
            ref = f"{chapter}.{v['lo']}" + (f"–{v['hi']}" if v["hi"] > v["lo"] else "") if q == 0 and v["lo"] else ""
            out.append({"n": len(out) + 1, "ref": ref, "en": para})
    return out


# --------------------------------------------------------------------------- Garuda Purana
GARUDA_CHAPTERS = [
    "The miseries of the sinful in this world and the next", "The Way of Yama", "The torments of Yama",
    "The kinds of sin that lead to hell", "The signs of sins", "The miseries of birth of the sinful",
    "Babhruvahana's rite for the departed", "The gifts for the dying", "The rites for the dying",
    "Gathering the bones from the fire", "The ten days' ceremonies", "The rite of the eleventh day",
    "The ceremony for all the ancestors", "The city of the King of Righteousness",
    "The birth of those who return from heaven", "The law of liberation",
]


def garuda(path):
    t = open(path, encoding="utf-8").read()
    t = t.split("\nNotes", 1)[0]
    starts = [m.start() for m in re.finditer(r"(?m)^Chapter (\d+)\. ", t)]
    starts = starts[16:]                              # the first sixteen are the table of contents
    assert len(starts) == 16, len(starts)
    sections = []
    for i, a in enumerate(starts):
        body = t[a:starts[i + 1] if i + 1 < 16 else len(t)]
        body = body.split("\n\n", 1)[1]               # drop the chapter heading
        lines = [l.strip() for l in body.split("\n") if not furniture(l.strip())]
        paras = [join_lines(p.split("\n")) for p in re.split(r"\n\s*\n", "\n".join(lines)) if p.strip()]
        verses = number_verses(paras, i + 1)
        for v in verses:
            v["en"] = re.sub(r"\s+", " ", tidy(v["en"]))
        sections.append({"label": GARUDA_CHAPTERS[i], "short": str(i + 1), "name": f"Chapter {i + 1}",
                         "verses": verses})
    sections[0]["intro"] = [
        "The Garuda Purana is told by Vishnu to his mount Garuda, king of birds. This Saroddhara, "
        "'the essence extracted', gathers its teaching on death and what follows: the soul's road to "
        "the city of Yama, the fruits of good and evil deeds, the rites by which the living help the "
        "departed, and, in its last chapter, the way to liberation. It is traditionally read in "
        "Hindu homes during the days of mourning after a death. Translated by Ernest Wood and "
        "S. V. Subrahmanyam (1911)."]
    return {"sections": sections}


# --------------------------------------------------------------------------- Devi Bhagavatam
BOOKS = ["FIRST", "SECOND", "THIRD", "FOURTH", "FIFTH", "SIXTH", "SEVENTH", "EIGHTH", "NINTH", "TENTH",
         "ELEVENTH", "TWELFTH"]
DEVI_SUB = [
    "The glory of the Purana; Madhu and Kaitabha; Shuka", "The birth of Vyasa and the Kuru line",
    "The Devi appears to the Trinity; Sudarshana; Navaratri", "Krishna's birth; Nara and Narayana",
    "The Devi slays Mahishasura, Shumbha and Nishumbha", "Vritra, Nahusha and the Haihayas",
    "The solar and lunar kings; Harishchandra; the Devi Gita", "The description of the worlds",
    "Prakriti and her forms: Radha, Durga, Lakshmi, Sarasvati", "The Manus and the Devi's deeds",
    "Daily worship and right conduct", "Gayatri and the Jewel Island",
]
SMALL = {"of", "the", "and", "to", "in", "on", "by", "for", "with", "a", "an", "at", "from", "into", "as"}


TITLE_FIXES = [  # chapter titles set in small capitals, which the scan garbled
    ("HAVAGRivA", "Hayagriva"), ("BnAGAVATi", "Bhagavati"), ("SAXYAVAxi", "Satyavati"), ("PARiKSiT", "Parikshit"),
    ("V iSNU", "Vishnu"), ("V iBHUTis", "Vibhutis"), ("ViRASENA", "Virasena"), ("MANDODARi", "Mandodari"),
    ("Kaus^ik!", "Kaushiki"), ("S’ACHi’s", "Shachi’s"), ("Mitra V arena", "Mitra-Varuna"), ("EKAVALi", "Ekavali"),
    ("Right T o", "Right to"), ("PARVATi", "Parvati"), ("SuMERU", "Sumeru"), ("SARASVAxi", "Sarasvati"),
    ("SARASvAxi", "Sarasvati"), ("Saras vat!", "Sarasvati"), ("TuLAsi", "Tulasi"), ("SA viTRi", "Savitri"),
    ("S’Ri", "Shri"), ("_ ^", ""),
]


def chapter_label(title):
    for a, b in TITLE_FIXES:
        title = title.replace(a, b)
    title = re.sub(r"(?<=[A-Za-z])!", "i", title)      # a long i read as ! (Gayatr!, Devak!)
    title = re.sub(r"(?<=[a-z])I(?=[a-z])|(?<=[A-Z])I(?=[a-z]{2})", "i", title)   # or as I (TIrthas, DvIpa)
    t = re.sub(r"^On\s+", "", tidy(title)).rstrip(" .")
    words = t.split()
    return " ".join(w if i == 0 or w.lower() not in SMALL else w.lower() for i, w in enumerate(words))


def devi_bhagavatam(path):
    t = open(path, encoding="utf-8").read()
    t = t[[m.start() for m in re.finditer(r"(?m)^THE FIRST BOOK\s*$", t)][1]:]   # after the contents
    t = re.sub(r"([Ss])['’](?=[a-z])", r"\1h", t)   # s' marks the palatal s: S'aunaka is Shaunaka
    books = re.split(r"(?m)^THE (?:%s) BOOK\s*$" % "|".join(BOOKS), t)[1:]
    assert len(books) == 12, len(books)
    out = []
    for b, body in enumerate(books, 1):
        heads = list(re.finditer(r"(?m)^Chapter (\d+)\s*\. (.*(?:\n(?!\n).*)*)", body))
        sections = []
        for i, h in enumerate(heads):
            text = body[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(body)]
            lines = [l.strip() for l in text.split("\n") if not furniture(l.strip())]
            paras = [join_lines(p.split("\n")) for p in re.split(r"\n\s*\n", "\n".join(lines)) if p.strip()]
            notes, body_paras = {}, []
            for p in paras:                            # the translator's notes go under their verse
                if re.match(r"Note\b[\s.:—-]*", p) and body_paras:
                    notes.setdefault(len(body_paras) - 1, []).append(re.sub(r"^Note\b[\s.:—-]*", "", p))
                else:
                    body_paras.append(p)
            verses = number_verses(body_paras, f"{b}.{i + 1}")
            assert len(verses) == len(body_paras), (b, i + 1, len(verses), len(body_paras))
            for j, v in enumerate(verses):
                v["en"] = re.sub(r"\s+", " ", tidy(v["en"]))
                if j in notes:
                    v["note"] = [tidy(n) for n in notes[j]]
            title = re.sub(r"\s+", " ", h.group(2))
            sections.append({"label": chapter_label(title), "short": str(i + 1), "name": f"Chapter {i + 1}",
                             "verses": verses})
        out.append({"sections": sections})
    out[0]["sections"][0]["intro"] = [
        "The Devi Bhagavatam is the great Purana of the Goddess, the Supreme Shakti, who creates, "
        "sustains and dissolves the worlds and is worshipped as the Mother of all. Told by the bard "
        "Suta to the sages of the Naimisha forest, it ranges from the birth of Vyasa and the wars of "
        "the gods with the demons to the Devi Gita, the Goddess's own teaching on the Self, and her "
        "Jewel Island beyond the worlds. Translated by Swami Vijnanananda (Hari Prasanna Chatterji), "
        "1921 to 1923."]
    return out


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    which, src = sys.argv[1], sys.argv[2]
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    if which == "garuda":
        data = garuda(src)
        size = write("garuda/1.json", data)
        verses = sum(len(s["verses"]) for s in data["sections"])
        print(f"garuda/1.json {size // 1024} KB, {len(data['sections'])} chapters, {verses} verses")
        index["garuda"] = {"parts": [{"n": 1, "name": "Saroddhara", "sub": "Death, the afterlife and liberation",
                                      "count": len(data["sections"])}]}
    if which == "devi":
        parts = []
        for b, data in enumerate(devi_bhagavatam(src), 1):
            size = write(f"devibhagavatam/{b}.json", data)
            verses = sum(len(s["verses"]) for s in data["sections"])
            print(f"devibhagavatam/{b}.json {size // 1024} KB, {len(data['sections'])} chapters, {verses} verses")
            parts.append({"n": b, "name": f"Book {b}", "sub": DEVI_SUB[b - 1], "count": len(data["sections"])})
        index["devibhagavatam"] = {"parts": parts}
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    main()
