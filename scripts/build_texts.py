#!/usr/bin/env python3
"""Build the scripture files in texts/ from public-domain sources.

Usage:
  python3 scripts/build_texts.py <katha_data_dir> <ganguli_txt_dir>

  katha_data_dir   assets/data from https://github.com/radhepa/Katha
                   (gita.json, ramayana.json: public-domain Sanskrit paired
                   verse by verse with Besant's and Dutt's English)
  ganguli_txt_dir  text/KMGanguli from https://github.com/rahulnyk/mahabharata
                   (K. M. Ganguli's complete Mahabharata, 01.txt .. 18.txt)

Only the public-domain scripture text is used; editorial explanations from the
source projects are not copied.
"""
import json
import os
import re
import sys
import unicodedata

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")

PARVAS = [
    "Adi Parva", "Sabha Parva", "Vana Parva", "Virata Parva", "Udyoga Parva",
    "Bhishma Parva", "Drona Parva", "Karna Parva", "Shalya Parva", "Sauptika Parva",
    "Stri Parva", "Shanti Parva", "Anushasana Parva", "Ashvamedhika Parva",
    "Ashramavasika Parva", "Mausala Parva", "Mahaprasthanika Parva", "Svargarohana Parva",
]
PARVA_SUBTITLES = [
    "The Book of the Beginning", "The Book of the Assembly Hall", "The Book of the Forest",
    "The Book of Virata", "The Book of the Effort", "The Book of Bhishma", "The Book of Drona",
    "The Book of Karna", "The Book of Shalya", "The Book of the Sleeping Warriors",
    "The Book of the Women", "The Book of Peace", "The Book of Instructions",
    "The Book of the Horse Sacrifice", "The Book of the Hermitage", "The Book of the Clubs",
    "The Book of the Great Journey", "The Book of the Ascent to Heaven",
]
GITA_SUBTITLES = [
    "Arjuna's Despair", "The Yoga of Knowledge", "The Yoga of Action",
    "Knowledge and Renunciation of Action", "The Yoga of Renunciation", "The Yoga of Meditation",
    "Knowledge and Realisation", "The Imperishable Brahman", "The Royal Secret",
    "Divine Glories", "The Vision of the Universal Form", "The Yoga of Devotion",
    "The Field and its Knower", "The Three Gunas", "The Supreme Person",
    "Divine and Demonic Natures", "The Three Kinds of Faith", "Liberation through Renunciation",
]

SECTION_RE = re.compile(r"^SECTION ([IVXLCDM]+(?:-[IVXLCDM]+)?)\.?$")
NUMBER_RE = re.compile(r"^(\d+)$")


def write(path, data):
    path = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    return os.path.getsize(path)


def clean(s):
    return (s or "").strip()


OCR_FIXES = str.maketrans({"ſ": "s", "ı": "i", "О": "O", "о": "o"})


def plain_english(s):
    """Dutt's English (via the Itihasa corpus) has inconsistent, OCR-damaged diacritics
    (Hanumăn, Cařaņas). Reduce names to plain letters so they read cleanly."""
    s = clean(s).translate(OCR_FIXES)
    s = unicodedata.normalize("NFD", s)
    return unicodedata.normalize("NFC", "".join(ch for ch in s if not unicodedata.combining(ch)))


def build_gita(src):
    data = json.load(open(os.path.join(src, "gita.json"), encoding="utf-8"))
    chapters = []
    for ch in data["chapters"]:
        n = ch["number"]
        verses = [
            [v["verse"], clean(v["sanskrit"]), clean(v["transliteration"]), clean(v["translations"]["english"])]
            for v in data["verses"] if v["chapter"] == n
        ]
        verses.sort(key=lambda x: x[0])
        chapters.append({"n": n, "name": ch["name"], "sub": GITA_SUBTITLES[n - 1], "verses": verses})
    size = write("gita.json", {"chapters": chapters})
    print("gita.json", size, "bytes,", sum(len(c["verses"]) for c in chapters), "verses")
    return [{"n": c["n"], "name": c["name"], "sub": c["sub"], "count": len(c["verses"])} for c in chapters]


def build_ramayana(src):
    data = json.load(open(os.path.join(src, "ramayana.json"), encoding="utf-8"))
    parts = []
    for k in data["chapters"]:
        kn = k["number"]
        sargas = {}
        for v in data["verses"]:
            if v["kanda"] != kn:
                continue
            s = sargas.setdefault(v["sarga"], {"n": v["sarga"], "name": clean(v.get("sarga_name")), "verses": []})
            s["verses"].append([v["verse"], clean(v["sanskrit"]), clean(v["transliteration"]), plain_english(v["translations"]["english"])])
        ordered = [sargas[n] for n in sorted(sargas)]
        for s in ordered:
            s["verses"].sort(key=lambda x: x[0])
        size = write("ramayana/%d.json" % kn, {"sections": ordered})
        print("ramayana/%d.json" % kn, size, "bytes,", len(ordered), "sargas")
        parts.append({"n": kn, "name": k["name"], "count": len(ordered)})
    return parts


def parse_ganguli(text, book):
    lines = text.replace("\r", "").split("\n")
    numbered = book in (8, 9, 10, 11, 16, 17, 18)
    sections, front, cur = [], [], None
    for line in lines:
        s = line.strip()
        m = SECTION_RE.match(s) or (NUMBER_RE.match(s) if numbered else None)
        if m:
            cur = {"label": "Section " + m.group(1), "lines": []}
            sections.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
        else:
            front.append(line)

    def paras(ls):
        out, buf = [], []
        for l in ls:
            if l.strip():
                buf.append(l.strip())
            # A blank line, or a short line ending a sentence in hard-wrapped text, ends a paragraph.
            if buf and (not l.strip() or (len(l.rstrip()) < 55 and re.search(r'[.!?\'"]$', l.rstrip()))):
                out.append(" ".join(buf))
                buf = []
        if buf:
            out.append(" ".join(buf))
        return out

    result = []
    if book == 1:
        pre = "\n".join(front)
        i = pre.find("TRANSLATOR'S PREFACE")
        if i >= 0:
            result.append({"label": "Translator's Preface", "paras": paras(pre[i + len("TRANSLATOR'S PREFACE"):].split("\n"))})
    result += [{"label": s["label"], "paras": paras(s["lines"])} for s in sections]
    # Split any remaining very long paragraphs at sentence boundaries for easier reading.
    for sec in result:
        sec["paras"] = [q for p in sec["paras"] for q in (split_long(p) if len(p) > 2000 else [p])]
    return result


def split_long(p):
    sentences = re.split(r'(?<=[.!?\'"])\s+(?=["\'A-Z(])', p)
    out, buf = [], ""
    for s in sentences:
        buf = (buf + " " + s).strip()
        if len(buf) > 700:
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return out


def build_mahabharata(src):
    parts = []
    for b in range(1, 19):
        text = open(os.path.join(src, "%02d.txt" % b), encoding="utf-8", errors="replace").read()
        sections = parse_ganguli(text, b)
        size = write("mahabharata/%d.json" % b, {"sections": sections})
        print("mahabharata/%d.json" % b, size, "bytes,", len(sections), "sections")
        parts.append({"n": b, "name": PARVAS[b - 1], "sub": PARVA_SUBTITLES[b - 1], "count": len(sections)})
    return parts


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    katha, ganguli = sys.argv[1], sys.argv[2]
    index = {
        "gita": {"parts": build_gita(katha)},
        "ramayana": {"parts": build_ramayana(katha)},
        "mahabharata": {"parts": build_mahabharata(ganguli)},
    }
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    main()
