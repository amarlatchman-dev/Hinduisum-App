#!/usr/bin/env python3
"""Add the Padma and Bhavishya Puranas, in Sanskrit, from Sanskrit Wikisource, to texts/.

Usage:
  pip install indic-transliteration
  python3 scripts/build_wikisource_puranas.py <pages_dir>

  pages_dir  the wikitext of the books' contents pages and of every chapter page they link
             to (and the targets of any redirects among them), one file each, with a titles.tsv
             that lists "<file>\\t<page title>", as saved through Special:Export on
             sa.wikisource.org; the contents pages are:
               पद्मपुराणम्/खण्डः १ (सृष्टिखण्डम्) ... पद्मपुराणम्/खण्डः ७ (क्रियाखण्डः)
               भविष्यपुराणम् /पर्व १ (ब्राह्मपर्व) ... भविष्यपुराणम् /पर्व ४ (उत्तरपर्व)

Wikisource types each half verse on its own line, and ends each verse with its number
("...श्रुतवानसि३।"). Every verse is given in Devanagari with its IAST transliteration; the
English is left empty until a free translation is found. The words that open a speech
("सूत उवाच", Suta said) become the heading of the verse that follows. The closing line of
each chapter ("इति श्रीपद्मपुराणे...") is left out, as in the other Sanskrit Puranas.
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

# id, title, parts: (the part's contents page, its name, its Sanskrit name)
BOOKS = [
    ("padma", "Padma Purana", [
        ("पद्मपुराणम्/खण्डः १ (सृष्टिखण्डम्)", "Srishti Khanda", "सृष्टिखण्डम्"),
        ("पद्मपुराणम्/खण्डः २ (भूमिखण्डः)", "Bhumi Khanda", "भूमिखण्डम्"),
        ("पद्मपुराणम्/खण्डः ३ (स्वर्गखण्ड)", "Svarga Khanda", "स्वर्गखण्डम्"),
        ("पद्मपुराणम्/खण्डः ४ (ब्रह्मखण्ड)", "Brahma Khanda", "ब्रह्मखण्डम्"),
        ("पद्मपुराणम्/खण्डः ५ (पातालखण्ड)", "Patala Khanda", "पातालखण्डम्"),
        ("पद्मपुराणम्/खण्डः ६ (उत्तरखण्डः)", "Uttara Khanda", "उत्तरखण्डम्"),
        ("पद्मपुराणम्/खण्डः ७ (क्रियाखण्डः)", "Kriyayoga Sara Khanda", "क्रियायोगसारखण्डम्"),
    ]),
    ("bhavishya", "Bhavishya Purana", [
        ("भविष्यपुराणम् /पर्व १ (ब्राह्मपर्व)", "Brahma Parva", "ब्राह्मपर्व"),
        ("भविष्यपुराणम् /पर्व २ (मध्यमपर्व)/भागः १", "Madhyama Parva, part 1", "मध्यमपर्व, भागः १"),
        ("भविष्यपुराणम् /पर्व २ (मध्यमपर्व)/भागः २", "Madhyama Parva, part 2", "मध्यमपर्व, भागः २"),
        ("भविष्यपुराणम् /पर्व २ (मध्यमपर्व)/भागः ३", "Madhyama Parva, part 3", "मध्यमपर्व, भागः ३"),
        ("भविष्यपुराणम् /पर्व ३ (प्रतिसर्गपर्व)/खण्डः १", "Pratisarga Parva, part 1", "प्रतिसर्गपर्व, खण्डः १"),
        ("भविष्यपुराणम् /पर्व ३ (प्रतिसर्गपर्व)/खण्डः २", "Pratisarga Parva, part 2", "प्रतिसर्गपर्व, खण्डः २"),
        ("भविष्यपुराणम् /पर्व ३ (प्रतिसर्गपर्व)/खण्डः ३", "Pratisarga Parva, part 3", "प्रतिसर्गपर्व, खण्डः ३"),
        ("भविष्यपुराणम् /पर्व ३ (प्रतिसर्गपर्व)/खण्डः ४", "Pratisarga Parva, part 4", "प्रतिसर्गपर्व, खण्डः ४"),
        ("भविष्यपुराणम् /पर्व ४ (उत्तरपर्व)", "Uttara Parva", "उत्तरपर्व"),
    ]),
]
DIGIT = "०-९0-9"
N = rf"[{DIGIT}](?:[{DIGIT} ]*[{DIGIT}])?"                                     # "११५", "१ १५"
NUM = re.compile(rf"[\s।॥|.]*({N}(?:\s*[.,]\s*{N})*)\s*[।॥|.]*\s*$")   # "...तत्२।", "॥१.४०.१००।"
SPEAKER = re.compile(r"^[\s।॥|]*[\u0900-\u0963\u0970-\u097f\s]{1,60}([उु]वाच|[ोा]वाच|[ऊू]चुः|[ऊू]चतुः|[ऊू]चे)ः?[\s\-:।॥|]*$")
COLOPHON = re.compile(r"^\s*इति\s*श्री")
HEADING = re.compile(rf"^(?:अथ\s*)?[\u0900-\u097f]*ऽध्यायः[\s।॥|.{DIGIT}]*$")             # "सप्तपञ्चाशत्तमोऽध्यायः।"
AFTER = re.compile(rf"[।॥|]\s*[{DIGIT}]+(?:\s*\.\s*[{DIGIT}]+)*\s*$")      # "... । । ४", "॥ 1.62.१०"
BEFORE = re.compile(rf"[\u0900-\u0963]\s*[{DIGIT}]+\s*[।॥|]+\s*$")          # "...तत्२।"
FOOTNOTE = re.compile(rf"\s*[{DIGIT}]+")
REDIRECT = re.compile(r"#(?:पुनर्निदेशन|REDIRECT)\s*\[\[([^\]|]+)", re.I)
ENDS = re.compile(r"^[\s।॥|.,?\-]+|[\s।॥|.,?\-]+$")


def number(s):
    return int(s.translate(str.maketrans("०१२३४५६७८९", "0123456789")))


def iast(line):
    t = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.IAST)
    return re.sub(r"\s+", " ", t.replace("~", "m̐")).strip()         # the library writes ँ as "~"


def text_lines(wiki):
    """The lines of a page, templates, markup and links taken out: those before the verse
    (inside <poem>) begins, and those of the verse."""
    t = re.sub(r"<ref[^>]*?/>|<ref.*?</ref>", "", wiki, flags=re.S)
    t = html.unescape(re.sub(r"<!--.*?-->", "", t, flags=re.S))       # some pages type "&#2404;" for "।"
    for _ in range(4):                                   # {{header ... [[..]] ...}} and nested ones
        t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\[\[(?:वर्गः|Category|सञ्चिका|File):[^\]]*\]\]", "", t)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    head, _, verse = t.partition("<poem>") if "<poem>" in t else ("", "", t)
    out = []
    for t in (head, verse):
        t = re.sub(r"<[^>]+>|'''?|&nbsp;", " ", t)
        t = re.sub(r"\*?\[[^\]\n]*\]|\*", " ", t)                   # editors' notes: "*[कहीं-(शिवस्य)]"
        t = re.sub(rf"([{DIGIT}]\s*[।॥|]+)[ \t]+(?=[\u0900-\u0963])", "\\1\n", t)  # a verse number inside a line
        t = re.sub(r"\{\||\|\}|^\s*[|!].*$", "", t, flags=re.M)    # stray table markup
        t = re.sub(r"।\s*।", "॥", t.replace("\u200c", "").replace("\u200d", ""))
        out.append([re.sub(r"\s+", " ", l).strip(" *:#") for l in t.split("\n")])
    return out


def intro(wiki):
    """The subject of the chapter, where Wikisource gives it above the verse."""
    lines = [l for l in text_lines(wiki)[0] if re.search(r"[\u0900-\u0963]", l)
             and not HEADING.match(l) and not re.search(r"नम[ःो]", l)]          # nor "नमो भगवते..."
    return [" ".join(lines)] if lines and len(" ".join(lines)) < 300 else []


def verses(wiki):
    """[(verse number or None, [Devanagari lines], speaker)] of one chapter."""
    lines = text_lines(wiki)[1]
    # Most pages end a verse with its number before the danda ("...तत्२।"); some put it after
    # a double danda ("... । । ४"), and then a digit before a danda marks a footnote.
    after = sum(bool(AFTER.search(l)) for l in lines) > sum(bool(BEFORE.search(l)) for l in lines)
    # A few pages have no numbers at all; there each verse ends with a double danda.
    bare = 4 * sum(bool(NUM.search(l)) for l in lines) < sum(l.endswith("॥") for l in lines)
    out, block, speaker, last = [], [], None, 0
    for l in lines:
        if not re.search(rf"[\u0900-\u0963{DIGIT}]", l):     # blank, or only dandas
            continue
        if COLOPHON.match(l):
            break
        if SPEAKER.match(l):
            if block:                                    # a speaker who takes up the verse half way
                block.append(l)
            else:
                speaker = ENDS.sub("", l)
            continue
        if not out and not block and HEADING.match(l):
            continue
        m = NUM.search(l)
        if m:
            n = number(re.split(r"[.,]", m.group(1))[-1].replace(" ", ""))
            # a number after a danda ("।१।", "॥ ४"), or in "1.62.10", surely ends a verse; one
            # straight after a word is a footnote mark on a page that numbers verses after the
            # danda, or when it is out of turn on the verse's first line
            sure = "." in m.group(1) or re.search(r"[।॥|]\s*$", l[:m.start(1)])
            if not sure and (after and re.search(r"[।॥|]", l[m.end(1):]) or not block and not last < n <= last + 3):
                m = None
        text = FOOTNOTE.sub("", l[:m.start()] if m else l)
        if m and (block or re.search(r"[\u0900-\u0963]", text)):   # a number may stand on its own line
            if re.search(r"[\u0900-\u0963]", text):
                block.append(text)
            out.append((n, block, speaker))
            block, speaker, last = [], None, n
        elif bare and text.endswith("॥") and not SPEAKER.match(text):
            block.append(text)
            out.append((None, block, speaker))
            block, speaker = [], None
        elif not out and not block and re.search(r"नमः\s*[।॥|]*$", text) and len(text.split()) <= 4:
            continue                                     # "श्रीगणेशाय नमः" before the first verse
        elif re.search(r"[\u0900-\u0963]", text):
            block.append(text)
    if block:
        out.append((None, block, speaker))
    return out


def entry(n, ref, lines, speaker):
    lines = [ENDS.sub("", l) for l in lines]
    lines = [l for i, l in enumerate(lines) if l and (i == 0 or l != lines[i - 1])]
    sa = "\u00a0।\n".join(lines) + "\u00a0॥"
    e = {"n": n, "ref": ref, "sa": sa, "tr": "\n".join(iast(l) for l in lines), "en": ""}
    if speaker:
        e["head"] = speaker
    return e


class Pages:
    """The saved pages, by title, with redirects followed."""

    def __init__(self, folder):
        self.folder = folder
        self.files = dict(l.rstrip("\n").split("\t")[::-1]
                          for l in open(os.path.join(folder, "titles.tsv"), encoding="utf-8"))

    def get(self, title):
        for _ in range(3):
            if title not in self.files:
                return title, None
            text = open(os.path.join(self.folder, self.files[title]), encoding="utf-8").read()
            m = REDIRECT.match(text)
            if not m:
                return title, text
            title = m.group(1).strip()
        return title, None

    def chapters(self, contents):
        """The chapter pages a contents page links to, in order, with their numbers."""
        title, text = self.get(contents)
        out = []
        for link in re.findall(r"\[\[([^\]|]+)", text):
            link = link.strip().replace("_", " ")
            link = title + link if link.startswith("/") else link
            m = re.search(rf"अध्यायः\s*([{DIGIT}]+)$", link)
            if m and link not in (t for _, t in out):
                out.append((number(m.group(1)), link))
        return out


def build(folder):
    pages = Pages(folder)
    index_path = os.path.join(OUT, "index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    for bid, title, parts in BOOKS:
        index_parts, total, chapters_total = [], 0, 0
        for i, (contents, name, sanskrit) in enumerate(parts, 1):
            secs = []
            for chap, link in pages.chapters(contents):
                _, text = pages.get(link)
                vs = verses(text) if text else []
                if not vs:
                    print("  no verses:", link)
                    continue
                items, last = [], 0
                for k, (num, lines, speaker) in enumerate(vs, 1):
                    if num is None or not last < num <= last + 30:     # a missing or misprinted number
                        num = last + 1
                    items.append(entry(k, f"{i}.{chap}.{num}", lines, speaker))
                    last = num
                sec = {"label": f"Adhyaya {chap}", "short": str(chap), "name": f"{len(items)} verses"}
                if intro(text):
                    sec["intro"] = intro(text)
                secs.append({**sec, "verses": items})
                total += len(items)
            write(f"{bid}/{i}.json", {"sections": secs})
            index_parts.append({"n": i, "name": name, "sub": sanskrit, "count": len(secs)})
            chapters_total += len(secs)
        index[bid] = {"parts": index_parts}
        print(f"{bid}: {len(parts)} parts, {chapters_total} chapters, {total} verses")
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    build(sys.argv[1])
