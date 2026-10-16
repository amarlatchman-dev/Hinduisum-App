#!/usr/bin/env python3
"""Add the Puranas that have no free English translation, in Sanskrit, to texts/.

Usage:
  pip install indic-transliteration
  python3 scripts/build_sanskrit_puranas.py <gretil_dir> <varaha.txt>

  gretil_dir  GRETIL's TEI files (sa_*.xml) of the Puranas, as in the archive.org item
              "dharmic-hinduism-corpus-collection" (gretil-buddhist-hinduism-xml-IAST.zip);
              the folders 06_Epics_Puranas and 03_Hindu_Shaiva_Tantra are searched
  varaha.txt  the Varaha Purana in ITRANS, made from Sanskrit Wikisource, as on archive.org
              ("varaha-purana-itrans-sanskrit-all-218-chapters")

Every verse is given in Devanagari with its IAST transliteration; the English is left empty
until a free translation is found. The words that open a speech ("suta uvaca", Suta said)
become the heading of the verse that follows. GRETIL's texts come from different printed
editions, typed by many people; they are kept as they are, with the verse numbers of their
editions.
"""
import html
import json
import os
import re
import sys

from indic_transliteration import sanscript

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_more_texts import write  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")

# id, title, files (each a part, or several files that number their own parts), part names
PURANAS = [
    ("bhagavata", "Bhagavata Purana", ["sa_bhAgavatapurANa.xml"], "Skandha"),
    ("narada", "Narada Purana", ["sa_nAradapurANa.xml"], {(1,): "Purva Bhaga", (2,): "Uttara Bhaga"}),
    ("brahmanda", "Brahmanda Purana", ["sa_brahmANDapurANa.xml"],
     {(1,): "Purva Bhaga", (2,): "Madhya Bhaga", (3,): "Uttara Bhaga, with the Lalitopakhyana"}),
    ("brahma", "Brahma Purana", ["sa_brahmapurANa-1-246.xml"], None),
    ("kurma", "Kurma Purana", ["sa_kUrmapurANa.xml"], {(1,): "Purva Bhaga", (2,): "Uttara Bhaga"}),
    ("linga", "Linga Purana", ["sa_liGgapurANa1-108.xml", "sa_liGgapurANa2,1-55.xml"],
     {(1,): "Purva Bhaga", (2,): "Uttara Bhaga"}),
    ("vamana", "Vamana Purana", ["sa_vAmanapurANa1-69.xml"], None),
    ("varaha", "Varaha Purana", ["varaha"], None),
    ("shiva", "Shiva Purana", ["sa_zivapurANabooks-1-and-7.xml"],
     {(1,): "Vidyeshvara Samhita", (7, 1): "Vayaviya Samhita, first part", (7, 2): "Vayaviya Samhita, second part"}),
    ("skanda", "Skanda Purana", ["sa_skandapurANa-revAkhaNDa-rks.xml"], None),
]
SPEAKER = re.compile(r"^[\w\s'āīūṛṝḷṅñṭḍṇśṣṃḥ-]{1,50}(uvāca|ūcuḥ|ūcatuḥ|ūce)\s*[|/।]?\s*$")


def deva(iast):
    t = iast.replace("//", "||").replace("/", "|")
    t = sanscript.transliterate(t, sanscript.IAST, sanscript.DEVANAGARI)
    # a no-break space keeps each danda with the word before it
    t = re.sub(r"\s*\|\|\s*", "\u00a0॥", re.sub(r"\s*\|(?!\|)\s*", "\u00a0। ", t))
    return re.sub(r"\u00a0। \n", "\u00a0।\n", t).strip()


def tidy(line):
    """Stray marks of the e-texts: "_*", verse numbers typed into the line, footnote digits."""
    line = line.replace("_*", " ").replace("~", "ṃ")     # ITRANS ~ for the nasal
    line = re.sub(r"\(\d+\)\)?|\b\d+[ab]\b", "", line)         # sub-numbers and edition pages (502a)
    line = re.sub(r"(?<=[^\s\d])\d+(?=[^\s\d/])", "", line)     # digits typed inside a word
    line = re.sub(r"(/\s*){2,}\d*", "/ ", line)
    line = re.sub(r"^\s*\d+(\.\d+)+\s+", "", line)
    line = re.sub(r"(?<=[^\s\d/])\d+(?=\s|$)|(?<=\s)\d+(?=\s|$)", "", line)
    return re.sub(r"\s+", " ", line).strip()


def plain_lines(xml):
    body = xml[xml.find("<body"):]
    body = re.sub(r"<lb\s*/>", " ", body)
    body = re.sub(r"</(l|p|head|lg)>", "\n", body)
    return [html.unescape(re.sub(r"\s+", " ", l)).strip() for l in re.sub(r"<[^>]+>", "", body).split("\n")]


def verses_from_lines(lines):
    """Verses from GRETIL's plain layout: each ends "// BhP_01.01.009 //" (or, line by line,
    "// SivP_1,1.1ab/"); lines without a number belong to the verse that is being built."""
    out, buf, speaker = [], [], None
    mark = re.compile(r"//\s*([^\s/]+?_)(\d[\d.,]*(?:\s+\d+)?)([a-f]*)\*?\s*/{1,2}")
    for l in lines:
        # The Bhagavata marks the feet of long metres with $ and %, and the half verse with &
        l = re.sub(r"\s*[$%]\s*", " ", l.replace("&", " /")).strip()
        l = re.sub(r"//\s*\S+_[^\s/]*[a-z]+_[a-f]*\s*/{1,2}", "//", l)   # numbers like SivP_1,mang_ab
        if not l or l.startswith("iti ") or re.match(r"^(Chapter|Adhyāya)\s*\d", l) or re.fullmatch(r"[\W_]+", l):
            continue
        m = re.match(r"^\S+_[\d.,]+/\d+\s+(.*)$", l)   # a speaker given a number of his own (BhP_01.01.006/0)
        if m:
            l = m.group(1).strip()
        if SPEAKER.match(l) and not buf:
            speaker = re.sub(r"\s*[|/।]\s*$", "", l)
            continue
        at = 0
        for m in mark.finditer(l):                    # prose can hold several numbered verses a line
            nums = tuple(int(x) for x in re.split(r"[.,\s]+", m.group(2)) if x)
            text = tidy(l[at:m.start()])
            at = m.end()
            if m.group(3) and out and out[-1]["key"] == nums and m.group(3)[0] > "b":
                out[-1]["lines"].append(text + " //")   # the second half of a verse given in halves
                continue
            buf.append(text + (" /" if m.group(3) in ("ab", "a", "b") else " //"))
            out.append({"key": nums, "lines": [x for x in buf if x.strip(" /")], "speaker": speaker})
            buf, speaker = [], None
        rest = tidy(l[at:])
        if rest:
            buf.append(rest)
    # A number typed with a part missing or doubled, unlike the verses on both sides of it,
    # takes the chapter of the verse before.
    i = 1
    while i < len(out) - 1:
        before = out[i - 1]["key"]
        j = i
        while j < len(out) and j - i < 3 and len(out[j]["key"]) != len(before):
            j += 1
        if j > i and j < len(out) and len(out[j]["key"]) == len(before):
            for q in range(i, j):          # e.g. NarP_1,36.42,1 is verse 42 of chapter 36
                k = out[q]["key"]
                out[q]["key"] = before[:-1] + ((k[len(before) - 1],) if len(k) > len(before) else k[-1:])
        i = max(j, i + 1)
    return out


def verses_from_tei(xml):
    """Verses from GRETIL's TEI layout: <lg xml:id="LiP_1.1.1"> with a line per <l>."""
    out, speaker = [], None
    for m in re.finditer(r"<lg xml:id=\"[^_\"]+_([\d.,]+)\">(.*?)</lg>|<p>(.*?)</p>", xml, re.S):
        if m.group(3) is not None:
            t = html.unescape(re.sub(r"<[^>]+>", "", m.group(3))).strip()
            if SPEAKER.match(t):
                speaker = re.sub(r"\s*[|/]\s*$", "", t)
            continue
        nums = tuple(int(x) for x in re.split(r"[.,]", m.group(1)) if x)
        ls = [html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", l))).strip()
              for l in re.findall(r"<l\b[^>]*>(.*?)</l>", m.group(2), re.S)]
        ls = [l for l in ls if l]
        if not ls:
            continue
        ls = [l.rstrip(" /") + (" //" if i == len(ls) - 1 else " /") for i, l in enumerate(ls)]
        out.append({"key": nums, "lines": ls, "speaker": speaker})
        speaker = None
    return out


def verses_from_varaha(path):
    """The Varaha Purana in ITRANS: chapters start ">>>001", verses end "|| 1.2 ||"."""
    lines, chapter = [], 0
    for l in open(path, encoding="utf-8").read().split("\n"):
        l = l.strip()
        if l.startswith(">>>"):
            chapter = int(l[3:6])
            continue
        if not l or not chapter or l.startswith("("):     # the uploader's note comes before chapter 1
            continue
        m = re.search(r"\|\|\s*(?:(\d+)\.)?(\d+)\s*\|\|\s*$", l)   # "|| 12 ||" or "|| 1.12 ||"
        iast = sanscript.transliterate(l[:m.start()] if m else l, sanscript.ITRANS, sanscript.IAST)
        iast = iast.replace("|", " /").strip()
        lines.append(f"{iast} // V_{chapter}.{m.group(2)} //" if m else iast)
    return verses_from_lines(lines)


def parts_of(verses, two_level):
    """Group verses into parts and chapters by their numbers: the last two are the chapter and
    the verse, any before them name the part, as in (part, chapter, verse) or (book, part,
    chapter, verse)."""
    parts = {}
    for v in verses:
        k = v["key"]
        part, chap, num = (k[:-2], k[-2], k[-1]) if two_level and len(k) >= 3 else ((1,), k[0], k[-1])
        parts.setdefault(part, {}).setdefault(chap, []).append((num, v))
    return parts


def section(pid, part, chap, items, single):
    verses = []
    for n, (num, v) in enumerate(items, 1):
        lines = [l for i, l in enumerate(v["lines"]) if i == 0 or l != v["lines"][i - 1]]  # a line typed twice
        iast = "\n".join(re.sub(r"\s+", " ", l).strip() for l in lines)
        entry = {"n": n, "ref": (f"{chap}.{num}" if single else f"{part}.{chap}.{num}"),
                 "sa": deva(iast), "tr": re.sub(r"\s*//\s*$", "", iast.replace(" /\n", "\n")).strip(" /"), "en": ""}
        if v.get("speaker"):
            entry["head"] = deva(v["speaker"])
        verses.append(entry)
    return {"label": f"Adhyaya {chap}", "short": str(chap), "name": f"{len(verses)} verses", "verses": verses}


def build(gretil, varaha):
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    for pid, title, files, names in PURANAS:
        verses = []
        for f in files:
            if f == "varaha":
                verses += verses_from_varaha(varaha)
                continue
            path = next(os.path.join(d, f) for d in (os.path.join(gretil, "06_Epics_Puranas"),
                                                     os.path.join(gretil, "03_Hindu_Shaiva_Tantra"))
                        if os.path.exists(os.path.join(d, f)))
            xml = open(path, encoding="utf-8").read()
            got = verses_from_tei(xml) if "<lg " in xml else verses_from_lines(plain_lines(xml))
            verses += got
        two = names is not None
        parts = parts_of(verses, two)
        index_parts = []
        for i, (part, chapters) in enumerate(sorted(parts.items()), 1):
            secs = [section(pid, ".".join(map(str, part)), c, items, not two) for c, items in sorted(chapters.items())]
            write(f"{pid}/{i}.json", {"sections": secs})
            name = (names.get(part, f"Part {part[0]}") if isinstance(names, dict)
                    else f"{names} {part[0]}" if isinstance(names, str) else title)
            index_parts.append({"n": i, "name": name, "sub": "", "count": len(secs)})
        index[pid] = {"parts": index_parts}
        total = sum(len(s) for c in parts.values() for s in c.values())
        print(f"{pid}: {len(parts)} parts, {sum(len(c) for c in parts.values())} chapters, {total} verses")
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    build(sys.argv[1], sys.argv[2])
