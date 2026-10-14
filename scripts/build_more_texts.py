#!/usr/bin/env python3
"""Add the Vedas, Upanishads, Vishnu Purana and Yoga Sutras to texts/.

Usage:
  pip install indic-transliteration
  python3 scripts/build_more_texts.py <kathaveda_gutenberg_json_gz> <dharmicdata_dir> <upanishads_txt> <yoga_sutras_txt>

  kathaveda_gutenberg_json_gz  data/extra-parts/gutenberg-sources/part-* from
                               https://github.com/jagdishak-hub/Kathaveda, concatenated
                               (Vishnu Purana, M. N. Dutt after H. H. Wilson, Gutenberg #66208)
  dharmicdata_dir              https://github.com/bhavykhatri/DharmicData
                               (Sama Veda, Griffith 1895; Rig Veda Sanskrit)
  upanishads_txt               3283.txt from https://github.com/GITenberg/The-Upanishads_3283
                               (Swami Paramananda, 1919)
  yoga_sutras_txt              2526.txt from
                               https://github.com/GITenberg/The-Yoga-Sutras-of-Patanjali--The-Book-of-the-Spiritual-Man_2526
                               (Charles Johnston, 1912)

Run scripts/build_texts.py first; this script adds to the index it writes.
"""
import gzip
import json
import os
import re
import sys

from indic_transliteration import sanscript

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rigveda_hymns import HYMNS  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")
ROMAN = re.compile(r"^[IVXL]+$")


# Obvious scanning errors in the Project Gutenberg transcriptions.
OCR_FIXES = [
    ("restless senses nave been re and imaginings", "restless senses and imaginings"),
    ("His illuminations is sevenfold, rising In successive", "His illumination is sevenfold, rising in successive"),
    ("are these: nom injury,", "are these: non-injury,"),
    ("though young, yet resected:", "though young, yet reflected:"),
]


def fix_ocr(text):
    for a, b in OCR_FIXES:
        text = text.replace(a, b)
    return text


def write(path, data):
    path = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    return os.path.getsize(path)


def paragraphs(lines):
    return [fix_ocr(p) for p in _paragraphs(lines)]


def _paragraphs(lines):
    out, buf = [], []
    for line in lines:
        s = line.strip()
        if s:
            buf.append(s)
        elif buf:
            out.append(re.sub(r"\s+", " ", " ".join(buf)))
            buf = []
    if buf:
        out.append(re.sub(r"\s+", " ", " ".join(buf)))
    return out


def split_long(p, size=650):
    """Break a long paragraph at sentence ends, preferring a new speaker."""
    if len(p) <= size * 1.4:
        return [p]
    parts = re.split(r'(?<=[.!?"”’])\s+(?=[A-Z“"(])', p)
    out, buf = [], ""
    for s in parts:
        if buf and (len(buf) > size or (len(buf) > size / 2 and re.match(r"^[A-Z][a-zāīūçṛ]+ said", s))):
            out.append(buf)
            buf = ""
        buf = (buf + " " + s).strip()
    if buf:
        out.append(buf)
    return out


def roman(n):
    vals = [(50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
    s = ""
    for v, r in vals:
        while n >= v:
            s += r
            n -= v
    return s


# --------------------------------------------------------------------------- Vishnu Purana
VISHNU_BOOKS = [
    "Creation of the universe",
    "The earth, the heavens and the hells",
    "The Vedas, the ages of Manu and the duties of life",
    "The royal dynasties",
    "The life of Krishna",
    "The ages of the world and liberation",
]


def build_vishnu(gz):
    d = json.load(gzip.open(gz))
    passages = [p for p in d["passages"] if p["work_id"] == "vishnu-english"]
    parts = []
    for b in range(1, 7):
        secs = []
        for p in sorted((x for x in passages if x["section"] == b), key=lambda x: x["chapter"]):
            text = re.sub(r"\[\d+\]", "", p["original"])
            paras = [q for para in paragraphs(text.split("\n")) for q in split_long(para)]
            secs.append({"label": f"Chapter {p['chapter']}", "short": str(p["chapter"]), "paras": paras})
        size = write(f"vishnu/{b}.json", {"sections": secs})
        print(f"vishnu/{b}.json", size, "bytes,", len(secs), "chapters")
        parts.append({"n": b, "name": f"Book {roman(b)}", "sub": VISHNU_BOOKS[b - 1], "count": len(secs)})
    return parts


# --------------------------------------------------------------------------- Sama Veda
def build_samaveda(dharmic):
    d = json.load(open(os.path.join(dharmic, "Samaveda", "Samaveda.json"), encoding="utf-8"))
    books = []
    for v in d["verses"]:
        key = (v["part"], v["book"])
        if not books or books[-1]["key"] != key:
            books.append({"key": key, "chapters": []})
        chs = books[-1]["chapters"]
        if not chs or chs[-1]["name"] != v["chapter"]:
            chs.append({"name": v["chapter"], "verses": []})
        chs[-1]["verses"].append(v)
    parts = []
    for i, bk in enumerate(books, 1):
        part, book = bk["key"]
        arch = "Purvarchika" if part.startswith("FIRST") else "Uttararchika"
        secs = []
        for ch in bk["chapters"]:
            verses, last = [], None
            for k, v in enumerate(ch["verses"], 1):
                head = None
                group = (v.get("section"), v["hymn"])
                if group != last:
                    bits = [b for b in (v.get("section"), f"Hymn {v['hymn']}", v.get("deity")) if b]
                    head = " · ".join(bits)
                    last = group
                verses.append({"n": k, "ref": f"{v['hymn']}.{v['verse']}", "en": v["text"].strip(), **({"head": head} if head else {})})
            secs.append({"label": ch["name"], "short": ch["name"].replace("Chapter ", ""), "verses": verses})
        size = write(f"samaveda/{i}.json", {"sections": secs})
        print(f"samaveda/{i}.json", size, "bytes,", len(secs), "chapters")
        parts.append({"n": i, "name": f"{arch} · {book}", "sub": "First part: the verses" if arch == "Purvarchika" else "Second part: the chants", "count": len(secs)})
    return parts


# --------------------------------------------------------------------------- Rig Veda (selected hymns)
ACCENTS = re.compile(r"[॒॑॓॔᳐-᳿꣠-ꣿ]")


def rig_verses(dharmic, mandala, sukta):
    data = json.load(open(os.path.join(dharmic, "Rigveda", f"rigveda_mandala_{mandala}.json"), encoding="utf-8"))
    text = next(h for h in data if h["sukta"] == sukta)["text"]
    text = ACCENTS.sub("", text)
    text = re.sub(r"(?<=[\u0900-\u097F]):", "ः", text)  # the source sometimes types visarga as a colon
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    lines = lines[1:] if not re.search(r"॥\s*[०-९]+", lines[0]) else lines  # drop the seer/deity/metre line
    lines = [l for l in lines if not re.fullmatch(r"[^\s]+ सूक्त", l)]
    verses, buf = [], []
    for l in lines:
        buf.append(l)
        m = re.search(r"॥?\s*([०-९]+)\s*॥*\s*$", l)
        if m:
            joined = "\n".join(buf)
            joined = re.sub(r"\s*॥?\s*[०-९]+\s*॥*\s*$", "॥", joined).replace("।॥", "॥")
            verses.append(joined.strip())
            buf = []
    return verses


def build_rigveda(dharmic):
    secs = []
    for h in HYMNS:
        m, s = h["ref"]
        sa = rig_verses(dharmic, m, s)
        lo, hi = h.get("verses", (1, len(sa)))
        sa = sa[lo - 1:hi]
        assert len(sa) == len(h["en"]), (h["ref"], len(sa), len(h["en"]))
        verses = []
        for k, (dev, en) in enumerate(zip(sa, h["en"]), lo):
            tr = sanscript.transliterate(re.sub(r"[।॥]", "", dev), sanscript.DEVANAGARI, sanscript.IAST).replace("~", "ṃ")
            verses.append({"n": k, "ref": f"{m}.{s}.{k}", "sa": dev, "tr": re.sub(r"[ \t]+", " ", tr).strip(), "en": en})
        secs.append({"label": h["title"], "short": h["short"], "name": f"Mandala {m}, hymn {s}", "intro": [h["about"]], "verses": verses})
    size = write("rigveda/1.json", {"sections": secs})
    print("rigveda/1.json", size, "bytes,", len(secs), "hymns")
    return [{"n": 1, "name": "Selected hymns", "sub": "Ten of the most beloved hymns", "count": len(secs)}]


# --------------------------------------------------------------------------- Upanishads
def numbered_blocks(lines):
    """Split lines into (marker, paragraphs) blocks at Peace Chant and Roman-numeral lines."""
    blocks, cur, marker = [], [], None
    for line in lines:
        s = line.strip()
        if s.lower() == "peace chant" or ROMAN.match(s):
            blocks.append((marker, paragraphs(cur)))
            marker, cur = ("Peace Chant" if s.lower() == "peace chant" else s), []
        else:
            cur.append(line)
    blocks.append((marker, paragraphs(cur)))
    return blocks


def verses_from(blocks):
    intro, verses = [], []
    for marker, paras in blocks:
        if marker is None:
            intro += paras
            continue
        if not paras:
            continue
        if marker == "Peace Chant":
            k = next((i for i, p in enumerate(paras) if p.upper().startswith("OM! PEACE") or p.upper().startswith("OM!  PEACE")), 0)
            text, notes = " ".join(paras[:k + 1]), paras[k + 1:]
        else:
            text, notes = paras[0], paras[1:]
        v = {"n": len(verses) + 1, "ref": marker, "en": text}
        if notes:
            v["note"] = notes
        verses.append(v)
    return intro, verses


def build_upanishads(path):
    L = open(path, encoding="utf-8", errors="replace").read().replace("\r", "").split("\n")
    end = next(i for i, l in enumerate(L) if l.startswith("End of the Project Gutenberg"))
    heads = [i for i, l in enumerate(L) if l.strip() in ("Isa-Upanishad", "Katha-Upanishad", "Kena-Upanishad", "KENA-UPANISHAD") and i > 200]
    # Each Upanishad: a title line followed by the translator's introduction, then a second title line and the text.
    spans = {
        "Isa": (heads[0], heads[1], heads[2]),
        "Katha": (heads[2], heads[3], heads[4]),
        "Kena": (heads[4], heads[5], end),
    }
    subs = {"Isa": "“All this is covered by the Lord”", "Katha": "Nachiketas and the teaching of Death", "Kena": "“By whom?” The power behind the senses"}
    parts = []
    for n, name in enumerate(("Isa", "Katha", "Kena"), 1):
        a, b, c = spans[name]
        intro = paragraphs(L[a + 1:b])
        body = L[b + 1:c]
        part_idx = [i for i, l in enumerate(body) if re.fullmatch(r"\s+Part (First|Second|Third|Fourth|Fifth|Sixth|fourth)\s*", l)]
        chunks = []
        if part_idx:
            bounds = part_idx + [len(body)]
            pre = body[:part_idx[0]]
            for j in range(len(part_idx)):
                chunks.append((body[part_idx[j]].strip().title(), (pre if j == 0 else []) + body[part_idx[j] + 1:bounds[j + 1]]))
        else:
            chunks.append(("", body))
        secs = []
        for j, (label, lines) in enumerate(chunks):
            sec_intro, verses = verses_from(numbered_blocks(lines))
            sec = {"label": label or f"{name} Upanishad", "short": str(j + 1), "verses": verses}
            if j == 0:
                sec["intro"] = intro + sec_intro
            elif sec_intro:
                sec["intro"] = sec_intro
            secs.append(sec)
        size = write(f"upanishads/{n}.json", {"sections": secs})
        print(f"upanishads/{n}.json", size, "bytes,", len(secs), "sections,", sum(len(s["verses"]) for s in secs), "verses")
        parts.append({"n": n, "name": f"{name} Upanishad", "sub": subs[name], "count": len(secs)})
    return parts


# --------------------------------------------------------------------------- Yoga Sutras
YOGA_BOOKS = ["Samadhi Pada · On contemplation", "Sadhana Pada · On practice", "Vibhuti Pada · On powers", "Kaivalya Pada · On liberation"]


def build_yoga(path):
    L = open(path, encoding="utf-8", errors="replace").read().replace("\r", "").split("\n")
    end = next(i for i, l in enumerate(L) if re.match(r"\*\*\* ?END OF", l) or "End of Project Gutenberg" in l or "End of the Project Gutenberg" in l)
    books = [i for i, l in enumerate(L) if re.fullmatch(r"BOOK (I|II|III|IV)", l.strip())]
    intros = [i for i, l in enumerate(L) if re.fullmatch(r"INTRODUCTION TO BOOK (I|II|III|IV)", l.strip())]
    parts = []
    for k, b in enumerate(books):
        stop = intros[k + 1] if k + 1 < len(intros) else end
        paras = paragraphs(L[b + 1:stop])
        intro = paragraphs(L[intros[k] + 1:b])
        verses, expect = [], 1
        for p in paras:
            m = re.match(r"^(\d+)\.\s+(.*)$", p)
            # The source occasionally skips a sutra number (II.5, III.34), so allow a small gap.
            if m and expect <= int(m.group(1)) <= expect + 2:
                num = int(m.group(1))
                verses.append({"n": num, "ref": f"{k + 1}.{num}", "en": m.group(2)})
                expect = num + 1
            elif verses:
                verses[-1].setdefault("note", []).append(p)
            else:
                intro.append(p)
        sec = {"label": f"Book {roman(k + 1)}", "short": str(k + 1), "verses": verses}
        if intro:
            sec["intro"] = intro
        size = write(f"yoga/{k + 1}.json", {"sections": [sec]})
        print(f"yoga/{k + 1}.json", size, "bytes,", len(verses), "sutras")
        parts.append({"n": k + 1, "name": f"Book {roman(k + 1)}", "sub": YOGA_BOOKS[k], "count": 1})
    return parts


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    gz, dharmic, upan, yoga = sys.argv[1:]
    path = os.path.join(OUT, "index.json")
    index = json.load(open(path, encoding="utf-8"))
    index["rigveda"] = {"parts": build_rigveda(dharmic)}
    index["samaveda"] = {"parts": build_samaveda(dharmic)}
    index["upanishads"] = {"parts": build_upanishads(upan)}
    index["vishnu"] = {"parts": build_vishnu(gz)}
    index["yoga"] = {"parts": build_yoga(yoga)}
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    main()
