#!/usr/bin/env python3
"""Add the Sanskrit of the eleven principal Upanishads, verse by verse, to texts/upanishads/,
from Sanskrit Wikisource (sa.wikisource.org, CC BY-SA).

Usage:
  pip install indic-transliteration
  python3 scripts/add_upanishad_sanskrit.py <pages_dir> [--report]

  pages_dir  the wikitext of the pages below, one file each, with a titles.tsv that lists
             "<file>\\t<page title>", as saved through Special:Export on sa.wikisource.org:
               ईशोपनिषत्
               कठोपनिषत्/प्रथमोध्यायः/प्रथमवल्ली ... कठोपनिषत्/द्वितीयोध्यायः/तृतीयवल्ली (six vallis)
               केनोपनिषद्
               प्रश्न उपनिषद्
               मुण्डकोपनिषद्
               माण्डुक्योपनिषद्
               तैत्तिरीयोपनिषदत्/शिक्षावल्ली, …/ब्रह्मानन्दवल्ली, …/भृगुवल्ली
               ऐतरेयोपनिषद्
               छान्दोग्योपनिषद्/अध्यायः १ ... छान्दोग्योपनिषद्/अध्यायः ८
               बृहदारण्यक उपनिषद् 1a, बृहदारण्यक उपनिषद् 2p ... 6p   (the unaccented text)
               श्वेताश्वतरोपनिषत्/प्रथमः अध्यायः ... श्वेताश्वतरोपनिषत्/षष्ठः अध्यायः
  --report   write nothing; print every verse with the start of its English and of the Sanskrit
             given to it, to check the alignment by eye

Each verse of the English (Paramananda for the Isa, Katha and Kena, Hume for the Mandukya, Müller
for the rest) gets "sa", the Devanagari, and "tr", its IAST transliteration, and keeps every other
field. A verse is matched by its number within its section, checked against Wikisource's own
numbering, verse count and sense. Where they part: a verse the translator joins to the next
gets the Sanskrit of both, and a khanda he numbers differently is mapped whole (MOVES, KHANDAS);
where Müller divides a Sanskrit paragraph (the Taittiriya's second and third Vallis, the
Aitareya, Brihadaranyaka 5.15) the Sanskrit is cut at the matching words (CUTS). A verse that
matches nothing in Wikisource (the ritual directions Müller translates from the Aitareya
Aranyaka, say) is left without Sanskrit. The Peace Chants get the shanti patha Wikisource gives
with the text. A run prints, for each Upanishad, how many verses got Sanskrit.

The Sanskrit is cleaned: wiki markup, links, footnotes, headings, colophons and verse numbers
are taken out, Vedic accents (U+0951, U+0952, U+1CD0–U+1CFF, U+A8E0–U+A8FF) are stripped and
the Vedic anusvara ꣳ is written ं; plain misprints are put right with FIXES, each of which must
match. As in the other Sanskrit books, a verse is one half-verse per line ("line ।" … "line ॥");
prose is split at its dandas, one sentence per line.
"""
import html
import json
import os
import re
import sys

from indic_transliteration import sanscript

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts", "upanishads")
DIGITS = "०१२३४५६७८९"
NBSP = "\u00a0"


# --------------------------------------------------------------------------- pages
class Pages:
    def __init__(self, folder):
        self.folder = folder
        self.files = dict(l.rstrip("\n").split("\t")[::-1]
                          for l in open(os.path.join(folder, "titles.tsv"), encoding="utf-8"))

    def get(self, title):
        if title not in self.files:
            sys.exit(f"missing page: {title}")
        text = open(os.path.join(self.folder, self.files[title]), encoding="utf-8").read()
        for fix in FIXES.get(title, []):
            old, new, count = fix if len(fix) == 3 else fix + (1,)
            n = text.count(old)
            if n != count:
                sys.exit(f"{title}: fix {old!r} matches {n} times, not {count}")
            text = text.replace(old, new)
        return clean(text)


def clean(t):
    """Wikitext to plain Devanagari text, one Wikisource line per line."""
    t = re.sub(r"<ref[^>]*?/>|<ref.*?</ref>|<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<inputbox>.*?</inputbox>", "", t, flags=re.S)
    for _ in range(4):
        t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"\[\[(?:वर्गः|Category|File|सञ्चिका|चित्रम्)\s*:[^\]]*\]\]", "", t)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[https?://\S+\s+([^\]]*)\]", r"\1", t)
    t = re.sub(r"\[https?://[^\]]*\]", "", t)
    t = html.unescape(re.sub(r"<[^>]+>|'''?|&nbsp;", " ", t))
    t = re.sub(r"\ua8f3\s+(?=स्त[^ो]|श्च)", "\ua8f3", t)    # "उद्यꣳ स्तमो": the s of sandhi goes with the word before
    t = t.replace("\ua8f3", "\u0902").replace("\ua8f2", "\u0901")      # the Vedic anusvara and candrabindu
    t = re.sub("[\u0951\u0952\u1cd0-\u1cff\ua8e0-\ua8ff\u200c\u200d\ufeff]", "", t)  # accents, joiners
    t = t.replace("||", "॥").replace("|", "।")
    t = re.sub(r"।\s*।", "॥", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"^\s*=+\s*(.*?)\s*=+\s*$", r"\1", t, flags=re.M)      # "== ॥ द्वितीयोऽनुवाकः ॥=="
    return "\n".join(l.strip() for l in t.split("\n"))


def between(text, start, end=None, title=""):
    """The text from `start` (included) to `end` (left out)."""
    i = text.find(start)
    if i < 0:
        sys.exit(f"{title}: start {start!r} not found")
    j = len(text) if end is None else text.find(end, i + len(start))
    if j < 0:
        sys.exit(f"{title}: end {end!r} not found")
    return text[i:j]


# --------------------------------------------------------------------------- verses
NUM = re.compile(rf"(?:॥\s*(?:बृह\s*\.?\s*)?|।\s*बृह\s*\.?\s*)([{DIGITS}]+(?:\s*[.,]\s*[{DIGITS}]+)*)\s*(?:॥|(?=\s*\n)|$)")
# headings: "प्रथमः खण्डः", "द्वितीय मुण्डके प्रथमः खण्डः", "प्रथमं ब्राह्मणम्", "षष्ठोऽनुवाकः", "अथ प्रथमोऽध्यायः"
HEAD = re.compile(r"""^[\s॥।()\d.०-९]*(?:अथ\s+)?(?:
      \S*(?:ऽ|ो|ॊ)ध्यायः
    | (?:\S+\s+){1,3}खण्डः
    | \S+\s+ब्राह्मण(?:म्|ं)
    | \S*(?:ऽ|ॊ)(?:नु)?(?:वाकः|वकः)
    | (?:\S+\s+)?(?:\S+\s+)?\S*वल्ली
    | (?:अथ\s+)?\S*(?:उ|ो)पनिष(?:त्|द्)
    | शान्तिपाठः | श्रीः | अनुक्रमणिका
    )[\s॥।()\d.०-९]*$""", re.X)
COLOPHON = re.compile(r"^[\s॥।]*इति\s+(?:\S*(?:उ|ो)पनिष(?:दि|त्|द्)|\S*वल्ल?्?यां|\S*भाष्यम्|\S+\s+\S*वल्ली"
                      r"|\S+\s+ब्राह्मणम्)|^[\s॥।]*इति\s.*समाप्ता[\s॥।]*$|^संबंधित कड़िया")


def body_lines(text):
    """A passage without its headings, colophons and editors' notes in brackets (blank lines kept)."""
    out = []
    for l in text.split("\n"):
        s = re.sub(r"\s*\([^()]{1,200}\)\s*", " ", l).strip()     # "(शतपथब्राह्मणम् १०.६.४.१)", "(रथन्तरोपरि टिप्पणी)"
        if l.strip() and (not s or HEAD.match(s) or COLOPHON.match(s)
                          or not re.search(r"[\u0900-\u097f]", s)):   # "== 2 ==", "<poem>"
            continue
        out.append(s)
    return "\n".join(out)


def number(s):
    return tuple(int(x.translate(str.maketrans(DIGITS, "0123456789")))
                 for x in re.split(r"\s*[.,]\s*", s.strip()))


def split_verses(text, title=""):
    """[(number tuple, raw text)] of a passage whose verses end in "॥ N ॥" (or "॥ 1.2.3 ॥").
    A verse that has lost its number is found where the numbers jump: the text before the next
    number is then cut at the end of a verse ("॥") or a blank line."""
    text = body_lines(text)
    out, pos, last = [], 0, 0
    for m in NUM.finditer(text):
        raw, num = text[pos:m.start()], number(m.group(1))
        pos = m.end()
        if not re.search(r"[\u0900-\u0963]", raw):
            continue
        n = num[-1]
        expected = 1 if n <= last else last + 1
        if n > expected:
            parts = [p for p in re.split(r"॥\s*\n|\n\s*\n", raw) if re.search(r"[\u0900-\u0963]", p)]
            if len(parts) == n - expected + 1:
                for k, p in enumerate(parts[:-1]):
                    out.append((num[:-1] + (expected + k,), p))
                raw = parts[-1]
            else:
                print(f"  {title}: verse {expected} to {n - 1} missing before {num}", file=sys.stderr)
        out.append((num, raw))
        last = n
    rest = text[pos:]
    if re.search(r"[\u0900-\u0963]{3}", rest):
        print(f"  {title}: text after the last verse: {rest.strip()[:80]!r}", file=sys.stderr)
    return out


def khandas(verses):
    """Verses grouped where the numbering starts again: [[(n, raw), ...], ...]."""
    out, last = [], 0
    for num, raw in verses:
        if num[-1] <= last or not out:
            out.append([])
        out[-1].append((num[-1], raw))
        last = num[-1]
    return out


# --------------------------------------------------------------------------- lines
ENDS = re.compile(r"^[\s।॥,]+|[\s।॥,]+$")


def groups(raw):
    """A passage as verse groups (cut at "॥"), each a list of lines. Wikisource's line breaks are
    kept where a line ends in a danda; a line that does not (the first quarter of a long verse,
    a prose line wrapped anywhere) runs on into the next, and prose is cut at every danda."""
    raw = re.sub(r"(?<=[\u0900-\u097f])-\s*(?=[\u0900-\u097f])", "", raw)    # "प्रेय-\nस्ते" is one word
    raw = re.sub(r"ऽ\s*\n\s*", "ऽ", raw)                                        # and "निमग्नोऽ\nनीशया"
    raw = re.sub(r"(?<![।॥])\s*\n\s*(?![।॥])", " ", raw.strip())
    out = []
    for g in re.split(r"॥", raw):
        lines = [ENDS.sub("", re.sub(r"[,.]", "", l)) for l in re.split(r"[।\n]", g)]   # editors' commas
        lines = [re.sub(r"\s+", " ", re.sub(r"^ऽ", "अ", re.sub(r"(?<=[\u0900-\u0963])[रस]्$", "ः", l)))
                 for l in lines if re.search(r"[\u0900-\u0963]", l)]          # "योनिर् ।": योनिः
        if lines:
            out.append(lines)
    return out


def iast(line):
    t = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.IAST)
    return re.sub(r"\s+", " ", t.replace("~", "m̐")).strip()


def entry_fields(gs):
    sa = "\n".join(f"{NBSP}।\n".join(g) + f"{NBSP}॥" for g in gs)
    tr = "\n".join(iast(l) for g in gs for l in g)
    return sa, tr


# --------------------------------------------------------------------------- the Wikisource texts
# Each reader returns {key: raw text}: the key is the verse's place in Wikisource's own numbering,
# a tuple such as (valli, verse) or (prapathaka, khanda, verse), or ("shanti", name) for a peace chant.
SHANTI_END = "शान्तिः ॥"


def numbered(text, title, prefix=(), levels=1):
    """{prefix + number: raw} for a passage; `levels` > 1 when the numbering restarts in parts
    that the passage does not number itself (khandas), which are then counted from 1."""
    out = {}
    vs = split_verses(text, title)
    if levels == 1:
        for num, raw in vs:
            key = prefix + num
            if key in out:
                print(f"  {title}: verse {key} twice", file=sys.stderr)
            out[key] = raw
    else:
        for k, kh in enumerate(khandas(vs), 1):
            for n, raw in kh:
                out[prefix + (k, n)] = raw
    return out


def read_isa(pages):
    t = pages.get("ईशोपनिषत्")
    out = numbered(between(t, "ॐ ईशा वास्यमिदँ", "॥ इति ईशोपनिषत् ॥"), "Isa")
    out[("shanti", "start")] = between(t, "ॐ पूर्णमदः", "॥ अथ ईशोपनिषत् ॥")
    return out


def read_katha(pages):
    out = {}
    for a, adh in enumerate(["प्रथमोध्यायः", "द्वितीयोध्यायः"]):
        for v, valli in enumerate(["प्रथमवल्ली", "द्वितीयवल्ली", "तृतीयवल्ली"]):
            title = f"कठोपनिषत्/{adh}/{valli}"
            t = pages.get(title)
            if (a, v) == (0, 0):
                out[("shanti", "start")] = between(t, "ॐ सह नाववतु", "ॐ उशन्", title)
                t = between(t, "ॐ उशन्", None, title)
            if (a, v) == (1, 2):
                end = t.index("इति काठकोपनिषदि")
                out[("shanti", "end")] = between(t[end:], "ॐ सह नाववतु", "ॐ तत् सत्", title)
                t = t[:t.index("सह नाववतु")]                  # given there as a nineteenth verse
            out.update(numbered(t, title, (3 * a + v + 1,)))
    return out


def read_kena(pages):
    t = pages.get("केनोपनिषद्")
    out = numbered(between(t, "ॐ केनेषितं", "ॐ आप्यायन्तु"), "Kena", levels=2)
    out[("shanti", "start")] = between(t, "ॐ आप्यायन्तु", "प्रथमः खण्डः")
    return out


def read_prasna(pages):
    t = pages.get("प्रश्न उपनिषद्")
    out = numbered(between(t, "ॐ सुकेशा च", "इति प्रश्नोपनिषदि षष्ठः प्रश्नः"), "Prasna", levels=2)
    out[("shanti", "start")] = between(t, "ॐ भद्रं कर्णेभिः", SHANTI_END) + SHANTI_END
    return out


def read_mundaka(pages):
    t = pages.get("मुण्डकोपनिषद्")
    out = numbered(between(t, "ॐ ब्रह्मा देवानां", "॥ इत्यथर्ववेदीय"), "Mundaka")
    out[("shanti", "start")] = between(t, "ॐ भद्रं कर्णेभिः", SHANTI_END) + SHANTI_END
    return out


def read_mandukya(pages):
    t = pages.get("माण्डुक्योपनिषद्")
    out = numbered(between(t, "ओमित्येतदक्षरमिदँ", "॥ इति माण्डुक्योपनिषत्"), "Mandukya")
    out[("shanti", "start")] = between(t, "ॐ भद्रं कर्णेभिः", SHANTI_END) + SHANTI_END
    return out


ANUVAKA = re.compile(r"^॥\s*\S+?(?:ऽ|ॊऽ|ॊ)(?:नु)?(?:वाकः|वकः)\s*॥\s*$", re.M)   # "षष्ठोऽनुवकः" too
COMMENTARY_VERSES = ("ज्ञानात्मने नमः", "प्रणतोऽस्म्यहं", "व्याख्येयं संप्रणीयते")


def read_taittiriya(pages):
    """The three Vallis, by anuvaka. Wikisource gives Shankara's commentary between the
    paragraphs of the Brahmananda and Bhrigu Vallis; only the numbered paragraphs of the text
    are kept."""
    out = {}
    for v, valli in enumerate(["शिक्षावल्ली", "ब्रह्मानन्दवल्ली", "भृगुवल्ली"], 1):
        title = f"तैत्तिरीयोपनिषदत्/{valli}"
        t = pages.get(title)
        heads = list(ANUVAKA.finditer(t))
        for a, h in enumerate(heads, 1):
            seg = t[h.end():heads[a].start() if a < len(heads) else len(t)]
            if (v, a) == (1, 1):            # the peace chant, numbered only in the colophon after it
                out[(1, 1, 1)] = between(seg, "ॐ शं नो", "इति शिक्षावल्यां", title)
                continue
            if v == 3 and a == len(heads):
                out[("shanti", "end")] = between(seg, "ॐ सह नाववतु", SHANTI_END, title) + SHANTI_END
                seg = seg[:seg.index("ॐ सह नाववतु")]
            paras = [p for p in re.split(r"\n\s*\n", seg)
                     if NUM.search(p) and not any(c in p for c in COMMENTARY_VERSES)]
            out.update(numbered("\n\n".join(paras), f"{title} {a}", (v, a)))
        if v == 2:
            out[("shanti", "start")] = between(t, "ॐ सह नाववतु", SHANTI_END, title) + SHANTI_END
    return out


def read_aitareya(pages):
    t = pages.get("ऐतरेयोपनिषद्")
    out = {}
    parts = re.split(r"॥\s*अथ\s+\S+\s+(?:प्रथमाध्याये\s+\S+\s+खण्डः|\S+ध्यायः)\s*॥", t)
    # parts[0] the peace chant, 1-3 the khandas of the first adhyaya, 4 and 5 the second and third
    for k, (a, kh) in enumerate([(1, 1), (1, 2), (1, 3), (2, 1), (3, 1)], 1):
        out.update(numbered(parts[k].split("इति ऎतरेयोपनिषत्")[0], f"Aitareya {a}.{kh}", (a, kh)))
    out[("shanti", "start")] = between(parts[0], "वाङ् मे मनसि", "शान्तिः॥") + "शान्तिः॥"
    return out


def read_chandogya(pages):
    out = {}
    for p in range(1, 9):
        title = f"छान्दोग्योपनिषद्/अध्यायः {DIGITS[p]}"
        t = pages.get(title)
        t = t[t.index("प्रथमः खण्डः"):]                    # after the contents list and peace chant
        t = t.split("संबंधित कड़िया")[0]                 # before the links at the foot
        if p == 8:
            t = t[:t.index("ॐ आप्यायन्तु")]
        out.update(numbered(t, title, (p,), levels=2))
    t = pages.get("छान्दोग्योपनिषद्/अध्यायः १")
    out[("shanti", "start")] = between(t, "ॐ आप्यायन्तु", SHANTI_END) + SHANTI_END
    return out


def read_brihadaranyaka(pages):
    out = {}
    for a, title in enumerate(["बृहदारण्यक उपनिषद् 1a"] + [f"बृहदारण्यक उपनिषद् {i}p" for i in range(2, 7)], 1):
        t = pages.get(title)
        t = t[t.index("षष्ठोऽध्यायः") + len("षष्ठोऽध्यायः"):]         # after the list of adhyayas
        if a == 1:
            t = between(t, "उषा वा अश्वस्य", None, title)                  # after the peace chant
        for num, raw in split_verses(t, title):
            if len(num) not in (3, 4) or num[0] != a:        # 3.9.28 has seven verses, 3.9.28.1-7
                print(f"  {title}: verse numbered {num}", file=sys.stderr)
            out[(a,) + num[1:]] = raw
    return out


def read_svetasvatara(pages):
    out = {}
    for a, o in enumerate(["प्रथमः", "द्वितीयः", "तृतीयः", "चतुर्थः", "पञ्चमः", "षष्ठः"], 1):
        title = f"श्वेताश्वतरोपनिषत्/{o} अध्यायः"
        t = pages.get(title)
        if a == 1:
            out[("shanti", "start")] = between(t, "ॐ सहनाववतु", SHANTI_END, title) + SHANTI_END
            t = between(t, "ॐ ब्रह्मवादिनो", None, title)
        if a == 6:
            t = t[:t.index("ॐ सह नाववतु")]
        out.update(numbered(t, title, (a,)))
    return out


READERS = [read_isa, read_katha, read_kena, read_prasna, read_mundaka, read_mandukya,
           read_taittiriya, read_aitareya, read_chandogya, read_brihadaranyaka, read_svetasvatara]


# --------------------------------------------------------------------------- corrections
# FIXES[page]: (misprint, correction[, times]) put right in the wikitext before it is read. Each
# must match exactly that many times, so that a later change on Wikisource shows up here.
FIXES = {
    "केनोपनिषद्": [
        ("मीमाँस्येमेव", "मीमाँस्यमेव"), ("सह्येनन्नेदिष्ठं", "स ह्येनन्नेदिष्ठं"),
        ("यद्देतद्गच्छतीव", "यदेतद्गच्छतीव"), ("तसै तपो", "तस्यै तपो"),
    ],
    "प्रश्न उपनिषद्": [
        ("भद्रम् पष्येमाक्षभिर्यजत्राः", "भद्रं पश्येमाक्षभिर्यजत्राः"),
        ("स्थिरैरङ्गैस्तुष्तुवाँसस्", "स्थिरैरङ्गैस्तुष्टुवाँसस्", 2),
        ("तन् ह स ऋषिरुवच", "तान् ह स ऋषिरुवाच"), ("कबन्धी कत्यायन", "कबन्धी कात्यायन"),
        ("भगवन् कुते ह वा", "भगवन् कुतो ह वा"), ("रयिं च प्रणं", "रयिं च प्राणं"),
        ("वैश्वानरो विश्वरुपः", "वैश्वानरो विश्वरूपः"), ("शुक्लः प्रणस्तस्मादेत", "शुक्लः प्राणस्तस्मादेत"),
        ("सत्यं\nप्रतिष्टितम्", "सत्यं\nप्रतिष्ठितम्"),
        ("प्रचां दिधारयन्ते कतर एतत् प्रकशयन्ते", "प्रजां विधारयन्ते कतर एतत् प्रकाशयन्ते"),
        ("तस्मि/श्च प्रतिष्ठमाने", "तस्मिंश्च प्रतिष्ठमाने"), ("एवोत्क्रमन्ते", "एवोत्क्रामन्ते"),
        ("तस्मि/ष्च प्रत्ष्ठमाने सर्व एव प्रतिष्टन्त एवम्", "तस्मिंश्च प्रतिष्ठमाने सर्व एव प्रातिष्ठन्त एवं"),
        ("वाङ्मनष्चक्षुः", "वाङ्मनश्चक्षुः"), ("यः प्रणैः", "यः प्राणैः"),
        ("प्राणैकर्षरत्ता", "प्राणैकर्षिरत्ता"), ("शिवां तां कुरू", "शिवां तां कुरु"),
        ("कौशल्यष्चाश्वलायनः", "कौसल्यश्चाश्वलायनः"), ("कथं बह्यमभिधते", "कथं बाह्यमभिधत्ते"),
        ("होउवाचातिप्रष्चान्", "होवाचातिप्रश्नान्"), ("सम्रादेवाधिकृतान्", "सम्राडेवाधिकृतान्"),
        ("एतन् ग्रामानोतान्", "एतान् ग्रामानेतान्"),
        ("ग्रामानधितिष्टस्वेत्येवमेवैष", "ग्रामानधितिष्ठस्वेत्येवमेवैष"),
        ("प्रातिष्टते", "प्रातिष्ठते"), ("नाडीनं", "नाडीनां"), ("सम्पध्यमानैः", "सम्पद्यमानैः"),
        ("तदेषः श्लोकः", "तदेष श्लोकः"), ("सम्प्रतिष्टिता", "सम्प्रतिष्ठिता"),
        ("तस्मै स होवच ।\nयथ गार्ग्य", "तस्मै स होवाच ।\nयथा गार्ग्य"),
        ("स्च्चासच्च", "सच्चासच्च"), ("सर्वः\nपस्यति", "सर्वः\nपश्यति"),
        ("सोभ्य", "सोम्य", 2), ("वसोवृक्षं", "वासोवृक्षं"), ("ग्राणं च", "घ्राणं च"),
        ("यादौ च गन्तव्यं", "पादौ च गन्तव्यं"), ("बोद्धिव्यं", "बोद्धव्यं"),
        ("विद्यारयितव्यं", "विधारयितव्यं"), ("तदच्छायमशरीरम्लोहितं", "तदच्छायमशरीरमलोहितं"),
        ("प्राणा भुतानि", "प्राणा भूतानि"), ("स यध्येकमात्रमभिध्यायीत", "स यद्येकमात्रमभिध्यायीत"),
        ("जगत्याभिसंपध्यते", "जगत्यामभिसम्पद्यते"), ("विभुतिमनुभूय", "विभूतिमनुभूय"),
        ("पुरुशयं", "पुरिशयं"), ("कुमारम्ब्रुवं", "कुमारमब्रुवं"), ("यध्यहमिममवेदिषं", "यद्यहमिममवेदिषं"),
        ("तस्मान्नार्हम्यनृतं", "तस्मान्नार्हाम्यनृतं"), ("इहैइवान्तःशरीरे", "इहैवान्तःशरीरे"),
        ("यस्मिन्नताः", "यस्मिन्नेताः"), ("प्रतिष्टिते प्रतिष्टस्यामीति", "प्रतिष्ठिते प्रतिष्ठास्यामीति"),
        ("नध्यः", "नद्यः"), ("भिध्येते", "भिद्येते", 2), ("नामरुपे", "नामरूपे", 2),
        ("कला यस्मिन्प्रतिष्टिताः", "कला यस्मिन्प्रतिष्ठिताः"),
        ("तं वेध्यं पुरुषं वेद यथ मा", "तं वेद्यं पुरुषं वेद यथा मा"),
        ("योऽस्माकमविध्यायाः", "योऽस्माकमविद्यायाः"),
    ],
    "मुण्डकोपनिषद्": [
        ("श्रुणुयाम", "शृणुयाम"), ("ज्ञानमयं तापः", "ज्ञानमयं तपः"), ("च जायाते", "च जायते"),
        ("तां तत्वतो", "तां तत्त्वतो"), ("एतस्माज्जायते प्रणो", "एतस्माज्जायते प्राणो"),
        ("अग्नीर्मूर्धा", "अग्निर्मूर्धा"), ("वायुः प्रणो हृदयं", "वायुः प्राणो हृदयं"),
        ("श्रद्ध सत्यं", "श्रद्धा सत्यं"), ("शारो ह्यात्मा", "शरो ह्यात्मा"),
        ("ज्योतिषं ज्योतिस्तद्", "ज्योतिषां ज्योतिस्तद्"), ("प्रणो ह्येष", "प्राणो ह्येष"),
        ("कर्मण वा", "कर्मणा वा"),
    ],
    "माण्डुक्योपनिषद्": [
        ("मिदँसर्वं", "मिदँ सर्वं"),
        ("सोऽयमात्माध्यक्षरमोङ्करोऽधिमात्रं", "सोऽयमात्माऽध्यक्षरमोङ्कारोऽधिमात्रं"),
        ("मात्रोत्कर्षात् उभयत्वाद्वोत्कर्षति", "मात्रोत्कर्षादुभयत्वाद्वोत्कर्षति"),
    ],
    "तैत्तिरीयोपनिषदत्/शिक्षावल्ली": [
        ("अथाधिजौतिषम्", "अथाधिज्यौतिषम्"), ("प्रवचनँसन्धानम्", "प्रवचनँ सन्धानम्"),
        ("प्रजननँसन्धानम्", "प्रजननँ सन्धानम्"), ("इत्यधिप्रजलम्", "इत्यधिप्रजम्"),
        ("माँसँस्नावास्थिमज्जा", "माँसँ स्नावास्थिमज्जा"), ("ओमितीदँसर्वम्", "ओमितीदँ सर्वम्"),
        ("ओँशोमिति", "ओँ शोमिति"), ("द्रविणँसवर्चसम्", "द्रविणँ सवर्चसम्"), ("धर्मकायाः", "धर्मकामाः"),
    ],
    "तैत्तिरीयोपनिषदत्/ब्रह्मानन्दवल्ली": [
        ("बहुभ्यां प्रजायेयेति", "बहु स्यां प्रजायेयेति"),
        # the Fathers' step in the measure of bliss is missing
        ("स एकः पितृणां चिरलोकलोकानामानन्दः । \nस एक आजानजानां",
         "स एकः पितृणां चिरलोकलोकानामानन्दः । श्रोत्रियस्य चाकामहतस्य । "
         "ते ये शतं पितृणां चिरलोकलोकानामानन्दाः । स एक आजानजानां"),
        ("न बिभेत कुतश्चनेति", "न बिभेति कुतश्चनेति"),
    ],
    "तैत्तिरीयोपनिषदत्/भृगुवल्ली": [
        ("आनन्दाध्येव", "आनन्दाद्ध्येव"), ("ऽन्नँराद्धम्", "ऽन्नँ राद्धम्", 3),
        ("अन्नँराध्यते", "अन्नँ राध्यते", 3), ("एदद्वा अन्ततो", "एतद्वा अन्ततो"),
        ("इमाँल्लोकन्कामान्नी", "इमाँल्लोकान्कामान्नी"), ("ऽअहमन्नादः", "ऽहमन्नादः"),
    ],
    "ऐतरेयोपनिषद्": [
        ("नान्यत्किञ्चचन", "नान्यत्किञ्चन मिषत्"), ("मरीचीर्मापोऽदोऽम्भः", "मरीचीर्मरमापोऽदोऽम्भः"),
        ("नासिके निरभिद्येतं", "नासिके निरभिद्येतां"), ("निरभिद्येतमक्षिभ्यां", "निरभिद्येतामक्षिभ्यां"),
        ("श्रोत्रद्दिशस्त्वङ्", "श्रोत्राद्दिशस्त्वङ्"), ("ता एता देवता सृष्टा", "ता एता देवताः सृष्टा"),
        ("पराङ्त्यजिघांसत्", "पराङत्यजिघांसत्"), ("हैवानमत्रप्स्यत्", "हैवान्नमत्रप्स्यत्", 2),
        ("ग्रहैष्यद्वित्सृज्य", "ग्रहैष्यद्विसृज्य"), ("द्वास्तदेतन्नाऽन्दनम्", "द्वास्तदेतन्नान्दनम्"),
        ("इदमदर्शनमिती ३", "इदमदर्शमिती३"), ("मात्मन्येवऽऽत्मानं", "मात्मन्येवात्मानं"),
        ("तं स्त्री गर्भ बिभर्ति", "तं स्त्री गर्भं बिभर्ति"), ("अथास्यायामितर", "अथास्यायमितर"),
        ("दृष्टिधृर्तिमतिर्मनीषा", "दृष्टिर्धृतिर्मतिर्मनीषा"),
    ],
    "श्वेताश्वतरोपनिषत्/प्रथमः अध्यायः": [
        ("क्लेशेर्जन्म", "क्लेशैर्जन्म"), ("मूर्तिनर्दृश्यते", "मूर्तिर्न दृश्यते"),
        ("तद्ब्रह्मॊपनिषत्परमिति", "तद्ब्रह्मोपनिषत्परमिति"),
    ],
    "श्वेताश्वतरोपनिषत्/द्वितीयः अध्यायः": [("यो देवॊऽग्नौ", "यो देवोऽग्नौ")],
    "श्वेताश्वतरोपनिषत्/तृतीयः अध्यायः": [
        ("यामिषुं गिरिशतं", "यामिषुं गिरिशन्त"), ("यस्मान्नणीयो", "यस्मान्नाणीयो"),
        ("सत्वस्यैष", "सत्त्वस्यैष"), ("एवेदँसर्वं", "एवेदँ सर्वं"),
    ],
    "श्वेताश्वतरोपनिषत्/चतुर्थः अध्यायः": [
        ("तस्यवयवभूतैस्तु", "तस्यावयवभूतैस्तु"), ("न सन्नचासच्छिव", "न सन्न चासच्छिव"),
    ],
    "श्वेताश्वतरोपनिषत्/पञ्चमः अध्यायः": [("तेने तेने स युज्यते", "तेन तेन स युज्यते")],
    "श्वेताश्वतरोपनिषत्/षष्ठः अध्यायः": [
        ("एको हंसः भुवनस्यास्य", "एको हंसो भुवनस्यास्य"), ("निष्क्रियंशान्तं", "निष्क्रियं शान्तं"),
        ("परंसेतुं", "परं सेतुं"), ("दग्धेन्दनमिवानलम्", "दग्धेन्धनमिवानलम्"),
        ("प्रकाशन्ते महात्मनः ॥ २३ ॥\nप्रकाशन्ते महात्मन इति ।",
         "प्रकाशन्ते महात्मनः ।\nप्रकाशन्ते महात्मन इति ॥ २३ ॥"),
    ],
    "कठोपनिषत्/प्रथमोध्यायः/तृतीयवल्ली": [("विषयाँ स्तेषु", "विषयाँस्तेषु")],
    "छान्दोग्योपनिषद्/अध्यायः २": [
        ("स प्रतिहार ॥ ४ ॥\n\nउद्गृह्णाति तन्निधनं वर्षति",
         "स प्रतिहार उद्गृह्णाति तन्निधनम् ॥ १ ॥\n\nवर्षति"),
    ],
    "छान्दोग्योपनिषद्/अध्यायः ३": [("तावदाधिपत्य्\ua8f3स्वाराज्यं", "तावदाधिपत्य\ua8f3स्वाराज्यं")],
    "छान्दोग्योपनिषद्/अध्यायः ७": [("तन्मर्त्य्ँ स भगवः", "तन्मर्त्यँ स भगवः")],
    "छान्दोग्योपनिषद्/अध्यायः ६": [
        ("एषोऽणिमैतदात्म्यमिदद्ँ सर्वं", "एषोऽणिमैतदात्म्यमिदँ सर्वं"),
        ("वागिति भूय एव मा भगवान्विज्ञापयत्विति तथा सोम्येति होवाच ॥ ६ ॥",
         "वागिति भूय एव मा भगवान्विज्ञापयत्विति तथा सोम्येति होवाच ॥ ५ ॥"),
        ("स उर्ध्वः समुदीषति", "स ऊर्ध्वः समुदीषति", 4), ("अपाँसोम्य", "अपाँ सोम्य"),
        ("समुदीषति सा प्राणो भवति", "समुदीषति स प्राणो भवति"),
    ],
    "बृहदारण्यक उपनिषद् 4p": [("लोकमतिक्रामति अद्द्. मृत्यो", "लोकमतिक्रामति मृत्यो"),
                               ("हिरण्मयःपुरुष", "हिरण्मयः पुरुष")],
    "बृहदारण्यक उपनिषद् 5p": [
        ("ते नमौक्तिं विधेम", "ते नमउक्तिं विधेम"),
    ],
    "बृहदारण्यक उपनिषद् 6p": [
        ("उक्त्वोव  अचापि", "उक्त्वोवाचापि"), ("राजेशनोऽधिपतिं", "राजेशानोऽधिपतिं"),
    ],
    "बृहदारण्यक उपनिषद् 3p": [
        ("॥ ३,८.९ ॥वा अक्षरस्य्", "॥ ३,८.९ ॥"),
        ("वर्षसहस्राण्यन्तवदेवास्य तद्भवति\nयो वा एतदक्षरमविदित्वा गार्ग्यविदित्वास्माल्लोकात्प्रैति",
         "वर्षसहस्राण्यन्तवदेवास्य तद्भवति ।\nयो वा एतदक्षरं गार्ग्यविदित्वास्माल्लोकात्प्रैति"),
        ("लोका अद्द्. अष्टौ देवा", "लोका अष्टौ देवा"),
        # the seven verses of 3.9.28 are numbered 29 to 35, and the end of the last is given twice
        ("॥ ३,९.२९ ॥", "॥ ३,९.२८.१ ॥"), ("॥ बृह. ३,९.३०॥", "॥ ३,९.२८.२ ॥"), ("॥ ३,९.३१॥", "॥ ३,९.२८.३ ॥"),
        ("॥ ३,९.३२ ॥", "॥ ३,९.२८.४ ॥"), ("॥ ३,९.३३॥", "॥ ३,९.२८.५ ॥"), ("॥ ३,९.३४॥", "॥ ३,९.२८.६ ॥"),
        ("रातिर्दातुः परायणम् ॥ बृह. ३,९.३५ ॥\n\n\nजात एव न जायते को न्वेनं जनयेत्पुनः ।\n"
         "विज्ञानमानन्दं ब्रह्म रातिर्दातुः परायणम् ॥\n\nतिष्ठमानस्य तद्विद इति ॥ ३,९.३६॥",
         "रातिर्दातुः परायणम् ।\nतिष्ठमानस्य तद्विद इति ॥ ३,९.२८.७ ॥"),
    ],
}


# --------------------------------------------------------------------------- alignment
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50}


def roman(s):
    n = 0
    for a, b in zip(s, s[1:] + " "):
        n += -ROMAN[a] if ROMAN.get(b, 0) > ROMAN[a] else ROMAN[a]
    return n


def default_key(u, sec, ref):
    """The Wikisource key of an English verse, by the Upanishad's numbering."""
    if ref == "Peace Chant":
        return None
    if re.fullmatch(r"[IVXL]+", ref):
        return (roman(ref),) if u == 1 else (sec, roman(ref))
    return tuple(int(x) for x in ref.split("."))


def is_cut(src):
    return isinstance(src[0], tuple) and len(src) == 3


def plan(u, app, sk):
    """{(section index, verse n): [source, ...]}, a source being a key of `sk` or a cut of one,
    (key, start words, end words); the Sanskrit of the sources is given in turn."""
    out = {}
    for si, s in enumerate(app["sections"]):
        for v in s["verses"]:
            ref = v["ref"]
            if ref == "Peace Chant":
                where = "start" if s is app["sections"][0] or v is s["verses"][0] else "end"
                if ("shanti", where) not in sk:
                    where = "start"                      # the same chant, given once
                out[(si, v["n"])] = [("shanti", where)]
                continue
            moves = MOVES.get(u, {})
            key = moves.get((si + 1, v["n"]), moves.get((si + 1, ref)))
            if key is None:
                key = default_key(u, si + 1, ref)
                head = ref.rsplit(".", 1)[0]
                if (si + 1, head) in KHANDAS.get(u, {}):        # a khanda Müller numbers differently
                    key = KHANDAS[u][(si + 1, head)] + (key[-1],)
            if key == "none":
                continue
            out[(si, v["n"])] = key if isinstance(key, list) else [key]
    for (sec, n), srcs in CUTS.get(u, {}).items():
        out[(sec - 1, n)] = srcs
    # a number Wikisource does not have (Müller's "2.1" for a part of an anuvaka) matches nothing
    return {k: srcs for k, srcs in out.items()
            if all((src[0] if is_cut(src) else src) in sk for src in srcs)}


def cut(raw, start, end):
    """The part of `raw` from the words `start` (None: its beginning) to the words `end`
    (None: its end; left out)."""
    i = 0 if start is None else raw.find(start)
    j = len(raw) if end is None else raw.find(end, i + 1)
    if i < 0 or j < 0:
        sys.exit(f"cut {start!r} .. {end!r} not found in {raw[:60]!r}")
    piece = raw[i:j]
    return re.sub(r"[सश]्\s*$", "ः", piece) if end and end[0] in "तच" else piece   # "लोकास्|तदस्य": लोकाः


def text_of(src, sk):
    if is_cut(src):
        key, a, b = src
        return cut(sk[key], a, b)
    if src not in sk:
        sys.exit(f"no Sanskrit verse {src}")
    return sk[src]


def sanskrit_for(srcs, sk):
    gs = []
    for src in srcs:
        gs += groups(text_of(src, sk))
    return gs


# --------------------------------------------------------------------------- alignment tables
# MOVES[upanishad][(section, English ref or verse n)]: the Wikisource verses (or cuts of them) for
# an English verse whose number does not lead to them, or "none" where nothing in Wikisource
# matches it.
MOVES = {
    9: {  # Chandogya: where Müller gives two verses as one paragraph
        (1, "1.3.11"): [(1, 3, 11), (1, 3, 12)],
        # the second "2.10" is 2.11; Müller's "2.22.1-2" is the one verse 2.23.1
        (2, 35): (2, 11, 1), (2, 36): (2, 11, 2),
        (2, "2.22.1"): [((2, 23, 1), None, "तप एव द्वितीयो")], (2, "2.22.2"): [((2, 23, 1), "तप एव द्वितीयो", None)],
        (2, "2.22.3"): (2, 23, 2), (2, "2.22.4"): (2, 23, 3),
        (3, "3.10.2"): [(3, 10, 2), (3, 10, 3)], (3, "3.11.5"): [(3, 11, 5), (3, 11, 6)],
        (3, "3.12.6"): [(3, 12, 6), (3, 12, 7)],
        (4, "4.2.4"): [(4, 2, 4), (4, 2, 5)], (4, "4.8.3"): [(4, 8, 3), (4, 8, 4)],
        (4, "4.17.9"): [(4, 17, 9), (4, 17, 10)],
        (5, "5.24.4"): [(5, 24, 4), (5, 24, 5)],
        (6, "6.15.2"): [(6, 15, 2), (6, 15, 3)], (6, "6.16.2"): [(6, 16, 2), (6, 16, 3)],
        (8, "8.2.9"): [(8, 2, 9), (8, 2, 10)], (8, "8.5.3"): [(8, 5, 3), (8, 5, 4)],
        (8, "8.6.5"): [(8, 6, 5), (8, 6, 6)], (8, "8.7.3"): [(8, 7, 3), (8, 7, 4)],
        (8, "8.12.5"): [(8, 12, 5), (8, 12, 6)],
    },
    10: {  # Brihadaranyaka: Müller gives 3.9.28 as one paragraph and 5.15.1 as four
        (3, "3.9.28"): [(3, 9, 28, k) for k in range(1, 8)],
        (5, "5.15.1"): [((5, 15, 1), None, "पूषन्नेकर्षे")],
        (5, "5.15.2"): [((5, 15, 1), "पूषन्नेकर्षे", "वायुरनिलम")],
        (5, "5.15.3"): [((5, 15, 1), "वायुरनिलम", "अग्ने नय")],
        (5, "5.15.4"): [((5, 15, 1), "अग्ने नय", None)],
    },
    8: {  # Aitareya: ritual directions of the Aranyaka that the Upanishad does not have
        (2, "2.1.1"): "none", (3, "3.1.1"): "none",
    },
    3: {  # Kena: Paramananda's third verse is Wikisource's third and fourth
        (1, "III"): [(1, 3), (1, 4)], (1, "IV"): (1, 5), (1, "V"): (1, 6), (1, "VI"): (1, 7),
        (1, "VII"): (1, 8), (1, "VIII"): (1, 9),
    },
}


def split_at(key, first, markers):
    """{n: [cut]}: the verse `key` cut before each of `markers`, its pieces going to the English
    verses first, first + 1, ..."""
    bounds = [None] + markers + [None]
    return {first + i: [(key, bounds[i], bounds[i + 1])] for i in range(len(bounds) - 1)}


def section_cuts(sec, parts):
    return {(sec, n): srcs for part in parts for n, srcs in part.items()}


# KHANDAS[upanishad][(section, English khanda)]: Wikisource's number for a khanda of the English
KHANDAS = {
    # Chandogya II: the English has no 2.13 (the Vamadevya Saman); from Müller's 2.11 on, its
    # khandas are Wikisource's 2.12 to 2.24 (Müller's "2.12" being missing, "2.13" is 2.14)
    9: {(2, "2.11"): (2, 12), **{(2, f"2.{k}"): (2, k + 1) for k in range(13, 24)}},
}

# CUTS[upanishad][(section, verse n)]: the pieces of Wikisource's verses that make up an English
# verse, where Müller's paragraphs are shorter than Wikisource's.
TA_REFRAIN = "तदप्येष श्लोको"
CUTS = {
    7: {  # Taittiriya: Müller divides each anuvaka of the second and third Vallis
        **section_cuts(2, [
            split_at((2, 1, 1), 2, ["तस्माद्वा एतस्मादात्मन", TA_REFRAIN]),
            split_at((2, 2, 1), 5, ["सर्वं वै तेऽन्नमाप्नुवन्ति", "तस्माद्वा एतस्मादन्नरसमयात्", TA_REFRAIN]),
            split_at((2, 3, 1), 9, ["सर्वमेव त आयुर्यन्ति", "तस्माद्वा एतस्मात् प्राणमयात्", TA_REFRAIN]),
            split_at((2, 4, 1), 13, ["तस्माद्वा एतस्मान्मनोमयात्", TA_REFRAIN]),
            split_at((2, 5, 1), 16, ["तस्माद्वा एतस्माद्विज्ञानमयात्", TA_REFRAIN]),
            split_at((2, 6, 1), 19, ["अथातोऽनुप्रश्नाः", "सोऽकामयत", TA_REFRAIN]),
            split_at((2, 7, 1), 23, ["यदा ह्येवैष एतस्मिन्नदृश्ये", TA_REFRAIN]),
            split_at((2, 8, 1), 26, ["सैषाऽऽनन्दस्य", "ते ये शतं मानुषा", "ते ये शतं मनुष्यगन्धर्वाणा",
                                     "ते ये शतं देवगन्धर्वाणा", "ते ये शतं पितृणां", "ते ये शतमाजानजानां",
                                     "ते ये शतं कर्मदेवानां", "ते ये शतं देवानामानन्दाः", "ते ये शतमिन्द्रस्या",
                                     "ते ये शतं बृहस्पतेर", "ते ये शतं प्रजापतेर", "स यश्चायं पुरुषे",
                                     "स य एवंवित्"]),
            split_at((2, 9, 1), 40, ["एतँ ह वाव न तपति"]),
        ]),
        **section_cuts(3, [
            split_at((3, 1, 1), 2, ["तँ होवाच", "स तपोऽतप्यत"]),
            *[split_at((3, a, 1), 3 * a - 1, ["तद्विज्ञाय", "स तपोऽतप्यत"]) for a in range(2, 6)],
            split_at((3, 6, 1), 17, ["सैषा भार्गवी"]),
            split_at((3, 7, 1), 19, ["प्राणो वा अन्नम्"]),
            {21: [(3, 8, 1)], 22: [(3, 9, 1)]},
        ]),
    },
    8: {  # Aitareya: Müller's paragraphs (Aitareya Aranyaka II, 4-6) are shorter than the verses
        (1, 1): [((1, 1, 1), None, "स ईक्षत")],
        (1, 2): [((1, 1, 1), "स ईक्षत", None), ((1, 1, 2), None, "अम्भो")],
        (1, 3): [((1, 1, 2), "अम्भो", "ऽदोऽम्भः")],
        (1, 4): [((1, 1, 2), "ऽदोऽम्भः", None)],
        (1, 5): [(1, 1, 3)],
        (1, 6): [(1, 1, 4)],
        (1, 7): [((1, 2, 1), None, "ता एनमब्रुवन्")],
        (1, 8): [((1, 2, 1), "ता एनमब्रुवन्", None), (1, 2, 2), ((1, 2, 3), None, "ता अब्रवीद्")],
        (1, 9): [((1, 2, 3), "ता अब्रवीद्", None)],
        (1, 10): [(1, 2, 4)],
        (1, 11): [(1, 2, 5)],
        (1, 12): [(1, 3, 1), (1, 3, 2)],
        (1, 13): [(1, 3, k) for k in range(3, 10)] + [((1, 3, 10), None, "सैषोऽन्नस्य")],
        (1, 14): [((1, 3, 10), "सैषोऽन्नस्य", None)],
        **section_cuts(1, [split_at((1, 3, 11), 15, ["स ईक्षत कतरेण", "स ईक्षत यदि"]),
                           split_at((1, 3, 12), 18, ["सैषा विदृतिर्नाम", "तस्य त्रय"])]),
        (1, 21): [(1, 3, 13)],
        (1, 22): [(1, 3, 14)],
        **section_cuts(2, [split_at((2, 1, 1), 2, ["तदेतत्सर्वेभ्यो"])]),
        **section_cuts(2, [split_at((2, 1, 3), 5, ["तं स्त्री", "स यत्कुमारं", "एवं सन्तता", "तदस्य द्वितीयं"])]),
        (2, 4): [((2, 1, 2), None, "साऽस्यैतमात्मान")],
        (2, 5): [((2, 1, 2), "साऽस्यैतमात्मान", None), ((2, 1, 3), None, "तं स्त्री")],
        **section_cuts(2, [split_at((2, 1, 4), 10, ["अथास्यायमितर", "स इतः प्रयन्नेव"]),
                           split_at((2, 1, 5), 13, ["गर्भे नु", "गर्भ एवैतच्छयानो"])]),
        (2, 15): [((2, 1, 5), "गर्भ एवैतच्छयानो", None), (2, 1, 6)],
        **section_cuts(3, [split_at((3, 1, 1), 2, ["येन वा पश्यति"])]),
        (3, 3): [((3, 1, 1), "येन वा पश्यति", None), ((3, 1, 2), None, "सर्वाण्येवैतानि")],
        (3, 4): [((3, 1, 2), "सर्वाण्येवैतानि", None)],
        **section_cuts(3, [split_at((3, 1, 3), 5, ["प्रज्ञाने प्रतिष्ठितं", "प्रज्ञानं ब्रह्म"])]),
        (3, 8): [(3, 1, 4)],
    },
}


# --------------------------------------------------------------------------- writing
def add(folder, report=False):
    pages = Pages(folder)
    names = json.load(open(os.path.join(OUT, "..", "index.json"), encoding="utf-8"))["upanishads"]["parts"]
    for u, reader in enumerate(READERS, 1):
        path = os.path.join(OUT, f"{u}.json")
        app = json.load(open(path, encoding="utf-8"))
        sk = reader(pages)
        sources = plan(u, app, sk)
        used, total, given = set(), 0, 0
        for si, sec in enumerate(app["sections"]):
            if report:
                print(f"## {u}.{si + 1} {sec['label']}")
            for i, v in enumerate(sec["verses"]):
                total += 1
                rest = {k: x for k, x in v.items() if k not in ("n", "ref", "sa", "tr")}
                srcs = sources.get((si, v["n"]))
                if not srcs:
                    sec["verses"][i] = {"n": v["n"], "ref": v["ref"], **rest}
                    if report:
                        print(f"  {v['ref']:>11}  --  {v.get('en', '')[:70]}")
                    continue
                sa, tr = entry_fields(sanskrit_for(srcs, sk))
                sec["verses"][i] = {"n": v["n"], "ref": v["ref"], "sa": sa, "tr": tr, **rest}
                used.update(src[0] if is_cut(src) else src for src in srcs)
                given += 1
                if report:
                    print(f"  {v['ref']:>11}  EN {v.get('en', '')[:70]}\n{'':15}SA {' '.join(tr.split())[:70]}")
        left = [k for k in sk if k not in used and k[0] != "shanti"]
        print(f"{u:>2} {names[u - 1]['name']:25} {given:4} of {total:4} verses with Sanskrit"
              + (f"; Wikisource verses not used: {', '.join('.'.join(map(str, k)) for k in left)}" if left else ""))
        if not report:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(app, f, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--report"]
    if len(args) != 1:
        sys.exit(__doc__)
    add(args[0], report="--report" in sys.argv)
