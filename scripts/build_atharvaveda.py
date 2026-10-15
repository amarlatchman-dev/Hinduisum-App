#!/usr/bin/env python3
"""Build the Atharva Veda in texts/atharvaveda/: Griffith's English paired with the Sanskrit.

Usage:
  pip install indic-transliteration wordfreq
  python3 scripts/build_atharvaveda.py <ocr_dir> <dharmicdata_dir> <wikisource_av_dir> [<rigveda_html_dir>]

  ocr_dir           archive.org OCR texts (_djvu.txt) of Ralph T. H. Griffith, "The Hymns of the
                    Atharva-Veda" (Benares, 1895-96; the reprint of 1916-17 has the same pages):
                      v1a.txt, v1b.txt  Vol. I (Books 1-9), two different scans
                      v2a.txt, v2b.txt  Vol. II (Books 10-20), two different scans
  dharmicdata_dir   https://github.com/bhavykhatri/DharmicData (AtharvaVeda/, Shaunaka recension)
  wikisource_av_dir Wikisource wikitext of "Hymns of the Atharva-Veda/Book 1/Hymn 1" ... "Hymn 18",
                    file names URL-quoted, ending in .wiki: clean text, used to measure the OCR
                    pipeline and, for these 18 hymns, as the text itself
  rigveda_html_dir  optional: Wikisource pages of Griffith's Rig Veda (see build_vedas.py), used only
                    to widen the vocabulary of Griffith's words and names

How it works. Each printed page has the verses on top and Griffith's notes in smaller type below,
with running heads and page numbers around them. Every OCR text is cut into Books (their headings),
hymns (the headings 'HYMN XXV.', often garbled, chosen as an increasing sequence) and paragraphs;
each paragraph is classed as verse or note (line width, the 'N Lemma : gloss' pattern and opening
sentence of the notes, a word model, and the page layout: verses first, then notes, on every page),
and the verse lines of a hymn are cut into stanzas by their numbers (stanza 1 is unnumbered; in the
prose Books the numbers stand inside the lines). The two OCR readings of every hymn are aligned word
by word and, where they differ, the reading that is a real word of Griffith's vocabulary is kept.
Hymn titles come from Griffith's own 'Index of Hymns' at the end of each volume (both OCR readings
compared), else from the first sentence of his notes. The Sanskrit of each hymn is paired verse by
verse where the hymn and its verse count agree with Griffith's.
"""
import collections
import difflib
import glob
import html
import json
import math
import os
import re
import sys
import unicodedata
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_vedas import AV_SUB, ascii_names, av_verses, iast  # noqa: E402
from build_more_texts import write  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VOLUMES = {1: list(range(1, 10)), 2: list(range(10, 21))}
# Griffith's hymns per Book (his Index of Hymns); Book 13 has 4 hymns where the Sanskrit text has 9 suktas
HYMNS = {1: 35, 2: 36, 3: 31, 4: 40, 5: 31, 6: 142, 7: 118, 8: 10, 9: 10, 10: 10, 11: 10, 12: 5, 13: 4,
         14: 2, 15: 18, 16: 9, 17: 1, 18: 4, 19: 72, 20: 143}
SUKTAS = {1: 35, 2: 36, 3: 31, 4: 40, 5: 31, 6: 142, 7: 118, 8: 10, 9: 10, 10: 10, 11: 10, 12: 5, 13: 9,
          14: 2, 15: 18, 16: 9, 17: 1, 18: 4, 19: 72, 20: 143}


# =========================================================================== small helpers
def norm_line(l):
    l = l.replace(" ", " ").replace("\t", " ").replace(" ", " ").replace(" ", " ")
    return re.sub(r"\s+", " ", l).strip()


def load(path):
    return [norm_line(l) for l in open(path, encoding="utf-8").read().split("\n")]


ROMAN_VALS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman(s):
    if not s or not re.fullmatch(r"C{0,1}(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})", s):
        return None
    v = 0
    for i, c in enumerate(s):
        x = ROMAN_VALS[c]
        v += -x if i + 1 < len(s) and ROMAN_VALS[s[i + 1]] > x else x
    return v or None


# how the OCR misreads the letters of a Roman numeral
RLET = {"I": ["I"], "V": ["V"], "X": ["X"], "L": ["L", "I"], "C": ["C"], "l": ["I"], "1": ["I"], "|": ["I"],
        "!": ["I"], "T": ["I"], "f": ["I"], "i": ["I"], "t": ["I"], "]": ["I"], "J": ["I"], "j": ["I"],
        "v": ["V"], "y": ["V"], "Y": ["V"], "F": ["V", "I"], "x": ["X"], "K": ["X"], "c": ["C"], "G": ["C"],
        "O": ["C"], "H": ["II"], "U": ["II"], "M": ["III"], "n": ["II"], "u": ["II"], "/": ["I"], "Z": ["I"],
        "E": ["I"], "'": [""], "‘": [""], "’": [""], "`": [""], "^": [""], " ": [""]}


def roman_readings(tok):
    """{value: cost} for a possibly garbled Roman numeral."""
    opts = [("", 0)]
    for ch in tok:
        if ch not in RLET:
            return {}
        cost = 0 if ch in "IVXLC '" else 1
        opts = [(o + a, c + cost + (k > 0)) for o, c in opts for k, a in enumerate(RLET[ch])]
        opts = sorted(opts, key=lambda x: x[1])[:64]
    out = {}
    for o, c in opts:
        v = roman(o)
        if v and c < out.get(v, 99):
            out[v] = c
    return out


def fuzzy_has(text, target, cut):
    """Whether `target` (capitals) occurs in `text`, allowing OCR damage."""
    t = re.sub(r"[^A-Z]", "", text.upper())
    n = len(target)
    for i in range(0, max(1, len(t) - n + 3)):
        for w in (n - 1, n, n + 1):
            s = t[i:i + w]
            if len(s) < n - 2:
                continue
            m = difflib.SequenceMatcher(None, s, target)
            if m.real_quick_ratio() >= cut and m.quick_ratio() >= cut and m.ratio() >= cut:
                return True
    return False


def core(tok):
    """A token's word, lower case, letters and inner apostrophes/hyphens only."""
    return re.sub(r"^[^a-z]+|[^a-z]+$", "", ascii_names(tok).lower().replace("’", "'"))


# =========================================================================== vocabulary
class Vocab:
    """Word counts from clean texts of Griffith's time: his Rig Veda (Wikisource) and Sama Veda, the
    app's other English texts, and (if installed) the wordfreq list of English. A reading of the OCR
    is trusted when it is a word here."""

    def __init__(self, rv_dir=None, extra_texts=()):
        self.g = collections.Counter()   # Griffith's own vocabulary
        self.e = collections.Counter()   # general English
        if rv_dir:
            for f in glob.glob(os.path.join(rv_dir, "*.html")):
                self.add(self.g, html_text(open(f, encoding="utf-8").read()))
        for f in sorted(glob.glob(os.path.join(ROOT, "texts", "samaveda", "*.json"))):
            for s in json.load(open(f, encoding="utf-8"))["sections"]:
                for v in s["verses"]:
                    self.add(self.g, v.get("en", ""))
        for t in extra_texts:
            self.add(self.g, t)
        for sub in ("mahabharata", "ramayana", "rigveda", "upanishads", "vishnu", "yoga"):
            for f in sorted(glob.glob(os.path.join(ROOT, "texts", sub, "*.json"))):
                self.add_json(json.load(open(f, encoding="utf-8")))
        self.wf = {}
        try:
            import wordfreq
            for w in wordfreq.top_n_list("en", 400000):
                if w.isalpha():
                    self.wf[w] = wordfreq.zipf_frequency(w, "en")
        except ImportError:
            pass
        self.g.update(ARCHAIC)

    def add(self, counter, text):
        for w in re.findall(r"[A-Za-z][A-Za-z'’\-]*[A-Za-z]|[A-Za-z]", ascii_names(text)):
            w = w.lower().replace("’", "'")
            counter[w] += 1
            if "-" in w:
                for p in w.split("-"):
                    counter[p] += 1

    def add_json(self, d):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in ("en", "paras", "text", "verses", "sections", "label", "intro") or isinstance(v, (list, dict)):
                    self.add_json(v)
        elif isinstance(d, list):
            for x in d:
                if isinstance(x, str):
                    if not re.search("[ऀ-ॿ]", x) and not re.search("[āīūṛṣṇṭḍśṃ]", x):
                        self.add(self.e, x)
                else:
                    self.add_json(x)
        elif isinstance(d, str) and not re.search("[ऀ-ॿ]", d):
            self.add(self.e, d)

    def score(self, w):
        """How much a word (lower case, no punctuation) looks like a real one: 0 = unknown."""
        if not w:
            return 0.0
        g, e, z = self.g.get(w, 0), self.e.get(w, 0), self.wf.get(w, 0.0)
        if "-" in w and not g:
            parts = [p for p in w.split("-") if p]
            if parts and all(self.known(p) for p in parts):
                return 2.0 + min(self.score(p) for p in parts) / 4
        if not g and e < 2 and z < 2.5:
            return 0.0
        return 1.0 + 1.6 * math.log1p(g) + 0.5 * math.log1p(e / 10) + 0.4 * max(0.0, z - 2.0)

    def known(self, w):
        return self.score(w) > 0

    def plausible(self, w):
        """Not to be 'corrected': a known word, or one that English uses at all (wordfreq)."""
        return self.g.get(w, 0) > 0 or self.e.get(w, 0) >= 2 or self.wf.get(w, 0.0) >= 3.0


def edit_distance(a, b, cap=3):
    if abs(len(a) - len(b)) > cap:
        return cap + 1
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        if min(cur) > cap:
            return cap + 1
        prev = cur
    return prev[-1]


_BUCKETS = {}


def spell_candidates(c, vocab):
    """Griffith's words close to an unknown word c (lower case): [(distance, -count, word)]."""
    if not _BUCKETS:
        for w in set(vocab.g) | set(vocab.e):
            n = vocab.g.get(w, 0) * 5 + vocab.e.get(w, 0)
            if n >= 10 and w.isalpha() and len(w) >= 3:
                _BUCKETS.setdefault(len(w), []).append((w, n))
    cap = 1 if len(c) <= 5 else 2
    out = []
    for L in range(len(c) - cap, len(c) + cap + 1):
        for w, n in _BUCKETS.get(L, ()):
            d = edit_distance(c, w, cap)
            if d <= cap:
                out.append((d, -n, w))
    return sorted(out)


def spell(tok, vocab, other=None):
    """An OCR misreading corrected to the nearest word of Griffith's vocabulary ('Brfthman's' ->
    'Brahman's', 'heahh' -> 'health'), when the word is unknown, long enough and the nearest word is
    clearly the best; with `other`, the second OCR reading must be close to it too."""
    lead, word, trail = split_punct(tok)
    c = word.lower().replace("'s", "")
    if len(c) < 3 or not c.isalpha() or vocab.plausible(c):
        return tok
    cands = spell_candidates(c, vocab)
    if len(c) == 3:  # a short word: only a common one, one letter off
        cands = [x for x in cands if x[0] == 1 and -x[1] >= 200]
    if word[:1].isupper():  # a name: only Griffith's own words, and well attested
        cands = [x for x in cands if vocab.g.get(x[2], 0) >= 3]
    if not cands:
        return tok
    best = cands[0]
    if len(cands) > 1 and cands[1][0] == best[0] and cands[1][1] > best[1] * 0.5:
        return tok  # two candidates as close, and about as common
    if other:
        oc = re.sub(r"[^a-z]", "", other.lower())
        if edit_distance(oc, best[2], 3) > 2:
            return tok
    w = best[2]
    if word[:1].isupper():
        w = w.capitalize()
    if word.lower().endswith("'s") and not w.endswith("'s"):
        w += "'s"
    return lead + w + trail


ARCHAIC = {w: 50 for w in """thou thee thy thine ye hath doth dost hast art wast wert shalt wilt canst couldst
didst mayst mayest burthen meath lauds laud hymn hymns whereby wherewith whereof thereof therewith therein
hither thither yonder hence thence whence erst oft ne'er e'er o'er 'tis 'twas amulet amulets charm charms
fiend fiends demon demons sorcerer sorcerers witchcraft rishi rishis brahman brahmans""".split()}


def html_text(t):
    t = re.sub(r"\sdata-mw='[^']*'", "", t)
    t = re.sub(r'\sdata-mw="[^"]*"', "", t)
    t = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return html.unescape(t)


# =========================================================================== OCR pages
def is_furniture(l):
    """Running heads ('42 THE HYMNS OF [BOOK II.', 'HYMN 3.] THE ATHARVA-VEDA. 43' and their garbled
    forms), page numbers, signature marks and stray marks."""
    t = l.strip()
    if not t:
        return False
    letters = re.sub(r"[^A-Za-z]", "", t)
    if not letters:
        return len(t) <= 8
    if "Digitized" in t or "oogle" in t:
        return True
    if len(t) <= 5 and not re.fullmatch(r"[\"'‘“(]?[A-Za-z]+(\s[A-Za-z]+)?[.,;:!?)'’\"]*", t):
        return True
    if len(t) > 52:
        return False
    up = sum(c.isupper() for c in letters) / len(letters)
    if up < 0.45:
        return False
    if re.search(r"[\[\({/]\s?B\S{2,3}\b", t) or re.search(r"[\])}]", t[:12]):
        return True
    return fuzzy_has(t, "ATHARVAVEDA", 0.72) or fuzzy_has(t, "HYMNSOF", 0.78)


HEAD = re.compile(r"^[^A-Za-z0-9]{0,3}[HB]\s?[YVT¥]\s?[MN]\s?[MNH]S?\s?[.,']?\s*(.*)$")


def heading_readings(l, bare_ok=False):
    """{hymn number: cost} if the line is a hymn heading 'HYMN XXV.' (OCR-garbled); in Book 15 the
    headings of the paryayas after the first are bare numerals 'II.'"""
    t = l.strip()
    if len(t) > 32:
        return {}
    m = HEAD.match(t)
    if m:
        rest = re.sub(r"\(?\s*See\s+App\w*\s*\)?.*$", "", m.group(1), flags=re.I).strip()
        mm = re.match(r"^['‘’`]?([IVXLCivxlcTfFtlLjJ1|!HUMnuyYGKOZ/E ]{1,10}?)\s*[.,:;]?\s*[^A-Za-z0-9]{0,4}"
                      r"([a-z]{0,2})\W{0,3}$", rest)
        if not mm:
            return {}
        return roman_readings(mm.group(1).strip())
    if bare_ok:
        mm = re.match(r"^[^A-Za-z0-9]{0,2}([IVXLCHUl1]{1,8})\s*[.,]\s*$", t)
        if mm:
            return {v: c + 1.5 for v, c in roman_readings(mm.group(1)).items()}
    return {}


def main_range(lines, books):
    start = next(i for i, l in enumerate(lines) if re.match(r"^B\S{2,3}\s+THE\s+(FIRST|TENTH)\W*$", l))
    end = next((i for i in range(start, len(lines))
                if re.match(r"^\W{0,3}(APPENDICES|[IL1]\.? APPENDIX|II\.? INDEX OF HYMNS|IL INDEX)", lines[i])),
               len(lines))
    starts = {books[0]: start}
    i0 = start
    for b in books[1:]:
        for i in range(i0 + 1, end):
            l = lines[i]
            m = re.match(r"^[^\[({]{0,8}?\bB\S{1,3}K\.?\s*[-–—]?\s*(\S{1,6}?)\s*[.,]?\s*[-–—]?\s*$", l)
            if m and len(l) < 20 and b in roman_readings(m.group(1)):
                starts[b] = i0 = i
                break
        else:
            raise SystemExit(f"Book {b}: heading not found")
    return starts, end


class Para:
    """Consecutive text lines of the OCR, with a flag for a page break (running head) before them."""

    def __init__(self, lines, brk, pos):
        self.lines, self.brk, self.pos, self.verse = lines, brk, pos, None

    @property
    def text(self):
        return " ".join(self.lines)

    def __repr__(self):
        return f"<{'V' if self.verse else 'N'}{' |' if self.brk else ''} {self.text[:60]}>"


class Head:
    def __init__(self, readings, pos, line):
        self.readings, self.pos, self.line, self.brk = readings, pos, line, False


def book_items(lines, a, b, book):
    """The paragraphs and hymn headings of a Book, in order."""
    out, cur, brk, start = [], [], False, a
    for i in range(a, b):
        l = lines[i]
        r = heading_readings(l, bare_ok=True) if l else {}
        furn = bool(l) and not r and is_furniture(l)
        if not l or furn or r:
            if cur:
                out.append(Para(cur, brk, start))
                cur, brk = [], False
            if furn:
                brk = True
            if r:
                out.append(Head(r, i, l))
            continue
        if not cur:
            start = i
        cur.append(l)
    if cur:
        out.append(Para(cur, brk, start))
    return out


# =========================================================================== verse or note?
LEMMA = re.compile(r"^[\dlIS]{1,3}[.,]?\s+[\"'‘]?[A-Z][^:;.!?]{0,45}?\s?[:;]\s")
NOTE_START = re.compile(r"^(The|This)\s+(hymn|stanza|line|Book|verse|prose|whole|subject|first|second|"
                        r"last|two|three|four|five|name|meaning|text|refrain|charm)\b|^(Taken|Stanzas?|Verses?|"
                        r"Lines?|Hymns?|R\.\s?V\.|Cf\.|See|Compare|Repeated|Literally|Or,|According|Professor|"
                        r"Prof\.|Ludwig|Weber|Whitney|Sayana|Bloomfield|Henry|A\.\s?V\.)\b")
INTRO = re.compile(r"^(A|An|The|This)\s+(\w+\s+){0,3}?(charm|prayer|hymn|glorification|benediction|"
                   r"imprecation|incantation|accompaniment|counter-charm|expiation|expiatory|funeral|"
                   r"curative|protective|formula|continuation)\b")


def words(s):
    return re.findall(r"[a-z]+", s.lower())


class WordModel:
    """Naive Bayes over words: the verses speak to the Gods ('thou', 'thee', 'us'), the notes about
    the text ('stanza', 'Rigveda', 'Ludwig', 'cf')."""

    def __init__(self, verse_texts, note_texts):
        self.cv = collections.Counter(w for t in verse_texts for w in words(t))
        self.cn = collections.Counter(w for t in note_texts for w in words(t))
        self.nv, self.nn = sum(self.cv.values()), sum(self.cn.values())
        self.size = len(set(self.cv) | set(self.cn)) + 1

    def score(self, text, clip=4.0):
        s = sum(math.log((self.cv[w] + 1) / (self.nv + self.size)) - math.log((self.cn[w] + 1) / (self.nn + self.size))
                for w in words(text))
        return max(-clip, min(clip, s))


def width_emission(p):
    lens = [len(l) for l in p.lines]
    body = lens[:-1] if len(lens) > 1 else lens
    if len(lens) > 1:
        narrow = sum(w <= 58 for w in body) / len(body)
        wide = sum(w >= 62 for w in body) / len(body)
        e = 4.5 * (narrow - wide)
    else:
        w = lens[0]
        e = 0.8 if w <= 52 else 0.3 if w <= 58 else -1.5 if w <= 62 else -3.5
    first = p.lines[0]
    if LEMMA.match(first):
        e -= 3
    if SHORT_LEMMA.match(first):
        e -= 2
    if NOTE_START.match(first):
        e -= 2.5
    if INTRO.match(first) and len(p.lines) <= 3:
        e -= 2.5
    if re.match(r"^\d{1,3}\s+[a-z]", first):  # '3 with ...' : a misread note number, or 'I' misread
        e -= 0.5
    if re.search(r"\b(R\.\s?V\.|A\.\s?V\.|Rigveda|St\. P|Ludwig|Weber|Sayana|Whitney|Grassmann|cf\.|Cf\.|i\.\s?e\.|"
                 r"pp?\.\s?\d|literally|stanza|hymn|note|Professor|Prof\.)", p.text):
        e -= 1.5
    return e


def viterbi(items, emissions):
    """Label the paragraphs: on every page the verses come first and the notes after them, so a
    return from notes to verse costs little at a page break or a hymn heading and much elsewhere."""
    score = {True: 0.5, False: -0.5}
    back = []
    brk = True
    for it, e in zip(items, emissions):
        if isinstance(it, Head):
            brk = True
            e = 12.0
        b = brk or it.brk
        nv_cost = -0.4 if b else -5.0
        sv = max((score[True], True), (score[False] + nv_cost, False))
        sn = max((score[False], False), (score[True] - 0.4, True))
        back.append({True: sv[1], False: sn[1]})
        score = {True: sv[0] + e / 2, False: sn[0] - e / 2}
        if not isinstance(it, Head):
            brk = False
    state = max(score, key=score.get)
    labels = [state]
    for bp in reversed(back[1:]):
        state = bp[state]
        labels.append(state)
    labels.reverse()
    for it, l in zip(items, labels):
        if isinstance(it, Para):
            it.verse = l


SHORT_LEMMA = re.compile(r"^[\dlIS£]{1,3}[.,]?\s+[^\sa-z]?[A-Z][^\s:;,]*(\s[^\s:;,]+){0,4}\s?[:;]\s")


def split_at_notes(items):
    """A note that the OCR ran on from the verse lines above it ('2 Hither : the water is addressed')
    starts a paragraph of its own."""
    out = []
    for p in items:
        if not isinstance(p, Para) or len(p.lines) < 2:
            out.append(p)
            continue
        cuts = [k for k in range(1, len(p.lines))
                if SHORT_LEMMA.match(p.lines[k]) or ((INTRO.match(p.lines[k]) or NOTE_START.match(p.lines[k]))
                                                     and re.search(r"[.!?:;]['’\"]?$", p.lines[k - 1]))]
        start = 0
        for k in cuts + [len(p.lines)]:
            if k > start:
                out.append(Para(p.lines[start:k], p.brk if start == 0 else False, p.pos + start))
            start = k
    return out


def split_mixed(items):
    """A paragraph whose narrow (verse) lines give way to wide (note) lines is cut in two."""
    out = []
    for p in split_at_notes(items):
        if isinstance(p, Para) and len(p.lines) >= 4:
            kinds = ["n" if len(l) <= 58 else "w" if len(l) >= 63 else "m" for l in p.lines]
            body = kinds[:-1]
            if body.count("n") >= 2 and body.count("w") >= 2:
                best, cut = 0, None
                for k in range(2, len(kinds) - 1):
                    a, b = kinds[:k], kinds[k:-1] or kinds[k:]
                    s = a.count("n") - a.count("w") + b.count("w") - b.count("n")
                    if s > best:
                        best, cut = s, k
                if cut and best >= len(kinds) - 3:
                    out += [Para(p.lines[:cut], p.brk, p.pos), Para(p.lines[cut:], False, p.pos + cut)]
                    continue
        out.append(p)
    return out


def classify(books):
    """books: {(ocr, book): items}. Width and patterns first, then a word model trained on the
    confident paragraphs, then the page-layout smoothing."""
    for k in books:
        books[k] = split_mixed(books[k])
    paras = [p for its in books.values() for p in its if isinstance(p, Para)]
    sure_v = [p.text for p in paras if len(p.lines) >= 3 and width_emission(p) >= 3.5]
    sure_n = [p.text for p in paras if len(p.lines) >= 3 and width_emission(p) <= -3.5]
    model = WordModel(sure_v, sure_n)
    for its in books.values():
        viterbi(its, [0 if isinstance(p, Head) else width_emission(p) + 0.4 * model.score(p.text, 4) for p in its])
    model = WordModel([p.text for p in paras if p.verse], [p.text for p in paras if not p.verse])
    for its in books.values():
        viterbi(its, [0 if isinstance(p, Head) else width_emission(p) + 0.5 * model.score(p.text, 4) for p in its])
    return model


# =========================================================================== hymns
def assign_hymns(items, n):
    """Choose the hymn headings of a Book: an increasing run of numbers 1..n, preferring exact
    readings, consecutive numbers and few missing headings. {item index: hymn number}"""
    heads = [k for k, it in enumerate(items) if isinstance(it, Head)]
    best = {0: (0.0, None)}
    for k in heads:
        r = items[k].readings
        new = {}
        for u, (sc, _) in best.items():
            cands = {v: c for v, c in r.items() if u < v <= n}
            if u + 1 <= n and u + 1 not in cands:
                cands[u + 1] = 2.6  # an unreadable numeral in its expected place
            for v, c in cands.items():
                s = sc + 3 - c - 1.6 * (v - u - 1)
                if s > new.get(v, (-1e9,))[0]:
                    new[v] = (s, (u, k))
        for v, x in new.items():
            if x[0] > best.get(v, (-1e9,))[0]:
                best[v] = (x[0], x[1] + (best[x[1][0]][1],))
    end = max(best, key=lambda v: best[v][0] - 1.6 * (n - v))
    out, node = {}, best[end][1]
    v = end
    while node:
        u, k, prev = node
        out[k] = v
        v, node = u, prev
    return out


def hymns_of_book(items, n):
    """{hymn: [items]} from a Book's items (the items before the first heading are dropped)."""
    chosen = assign_hymns(items, n)
    out, cur = {}, None
    for k, it in enumerate(items):
        if k in chosen:
            cur = chosen[k]
            out[cur] = []
            continue
        if cur is not None and not isinstance(it, Head):
            out[cur].append(it)
    for h, its in out.items():  # a one-line hymn whose line was taken for a note ('Gayatri, Ushnih, ...')
        paras = [p for p in its if isinstance(p, Para)]
        if paras and not any(p.verse for p in paras) and len(paras[0].lines) <= 3:
            paras[0].verse = True
    return out


# =========================================================================== stanzas
DIGIT_LIKE = {"l": "1", "I": "1", "i": "1", "|": "1", "!": "1", "]": "1", "t": "1", "o": "0", "O": "0",
              "Q": "0", "D": "0", "S": "58", "s": "58", "B": "8", "Z": "2", "z": "2", "g": "9", "?": "7",
              "T": "7", "€": "6", "b": "6", "J": "3", "&": "8", "$": "5", "#": "2", "*": ""}
CONFUSED = {"0": "689", "1": "47", "2": "37", "3": "2589", "4": "1", "5": "6389", "6": "5809", "7": "12",
            "8": "35609", "9": "3580"}
NOT_NUMBERS = {"O", "o", "I", "A", "a", "i", "Lo", "So", "Is", "Ill", "Id", "Io", "In", "Be", "To", "Do", "Go",
               "Of", "So,", "Lo,", "O,", "I,"}


def number_readings(tok, exact_only=False):
    """{value: cost} for the token that heads a stanza: cost 0 when read exactly, 1 for a likely
    misreading of a digit, 1.5 for another single wrong digit, 2 for a dropped digit."""
    tok = tok.strip().rstrip(".,:;")
    if not tok or tok in NOT_NUMBERS or len(tok) > 4:
        return {}
    exact = tok.isdigit()
    if exact_only and not exact:
        return {}
    if not exact and (sum(c.isalpha() and c not in DIGIT_LIKE for c in tok) or (tok.isalpha() and len(tok) > 2)
                      or not any(c.isdigit() for c in tok) and len(tok) > 1):
        return {}
    opts = [""]
    for c in tok:
        alts = c if c.isdigit() else DIGIT_LIKE.get(c)
        if alts is None:
            return {}
        if alts:
            opts = [o + a for o in opts for a in alts]
    out = {}

    def put(v, cost):
        if 0 < v < 400 and cost < out.get(v, 9):
            out[v] = cost
    for o in opts:
        if not o:
            continue
        put(int(o), 0 if exact else 1)
        for i, d in enumerate(o):
            for a in "0123456789":
                if a != d:
                    put(int(o[:i] + a + o[i + 1:]), 1 if a in CONFUSED[d] else 1.5)
        if len(o) == 1:
            for a in "123456789":
                put(int(a + o), 2)
                put(int(o + a), 2)
    return out


def tokenize_lines(lines):
    """[(token, starts_line)] for the verse lines of a hymn."""
    out = []
    for l in lines:
        for k, t in enumerate(l.split()):
            out.append([t, k == 0])
    return out


def stanza_candidates(toks):
    """Possible stanza numbers: at the start of a line (any reading), or inside a line when an exact
    number follows the end of a phrase and precedes a capital (the prose hymns)."""
    cands = []
    for i, (t, ls) in enumerate(toks):
        nxt = toks[i + 1][0] if i + 1 < len(toks) else ""
        nxt_cap = bool(re.match(r"^[\"'‘“(]?[A-Z]", nxt))
        span = 0
        m2 = re.fullmatch(r"(\d{1,3}),?", t)
        if m2 and re.fullmatch(r"\d{1,3}\.?", nxt) and int(nxt.rstrip(".")) == int(m2.group(1)) + 1:
            span = 1
            nn = toks[i + 2][0] if i + 2 < len(toks) else ""
            nxt_cap = bool(re.match(r"^[\"'‘“(]?[A-Z]", nn))
        if ls:
            if t in NOT_NUMBERS:
                continue
            r = number_readings(t)
            if r and not nxt_cap:
                r = {v: c + 1.5 for v, c in r.items() if t.isdigit()}
            if r:
                cands.append((i, r, span))
        elif i > 0 and re.fullmatch(r"\d{1,3}", t if not span else m2.group(1)) and nxt_cap:
            prev = toks[i - 1][0]
            if re.search(r"[.,;:!?'’\")—-]$", prev):
                cands.append((i, {int(t if not span else m2.group(1)): 0.6}, span))
    return cands


def assign_stanzas(cands, expect, top):
    """An increasing run of stanza numbers 2..top (DP over the candidates)."""
    best = {1: (0.0, None)}
    for ci, (i, readings, span) in enumerate(cands):
        new = {}
        for v, cost in readings.items():
            if v < 2 or v + span > top:
                continue
            over = 2.5 * (v + span - expect) if expect and v + span > expect and cost > 0 else 0
            opts = [(sc - 0.9 * (v - u - 1) + 3 - cost - over, u) for u, (sc, _) in best.items() if u < v]
            if opts:
                sc, u = max(opts)
                e = v + span
                if sc > new.get(e, (-1e9,))[0]:
                    new[e] = (sc, (u, best[u][1], ci, v))
        for e, x in new.items():
            if x[0] > best.get(e, (-1e9,))[0]:
                best[e] = x
    end = max(best, key=lambda k: best[k][0] - 0.9 * max(0, expect - k))
    chosen, node = {}, best[end][1]
    while node:
        u, prev, ci, v = node
        chosen[ci] = v
        node = prev
    return chosen


def split_stanzas(lines, expect):
    """{number: [tokens]} and {first: last} for stanzas Griffith numbers together ('40, 41')."""
    toks = tokenize_lines(lines)
    cands = stanza_candidates(toks)
    chosen = assign_stanzas(cands, expect, max(expect + 12, 30))
    starts = {}
    for ci, v in chosen.items():
        i, r, span = cands[ci]
        starts[i] = (v, span)
    out, merged, n, skip = {1: []}, {}, 1, 0
    for i, (t, ls) in enumerate(toks):
        if skip:
            skip -= 1
            continue
        if i in starts:
            n, span = starts[i]
            out[n] = []
            if span:
                merged[n] = n + span
                skip = 1
            continue
        out[n].append((t, ls))
    return out, merged


# =========================================================================== Wikisource ground truth
def read_wikisource(d):
    """{hymn: (title, {n: text})} for Book 1 from the Wikisource wikitext files."""
    out = {}
    for f in glob.glob(os.path.join(d, "*.wiki")):
        name = urllib.parse.unquote(os.path.basename(f))
        m = re.search(r"Book 1/Hymn (\d+)\.wiki$", name)
        if not m:
            continue
        t = open(f, encoding="utf-8").read()
        title = re.search(r"'''(.*?)'''", t).group(1).strip()
        body = re.search(r"<pre>(.*?)</pre>|<div class=\"verse\">(.*?)</div>", t, re.S)
        body = re.sub(r"\s*p\. a\d+\s*$", "", body.group(1) or body.group(2), flags=re.M).replace("</pre>", "")
        verses, n = {}, 0
        for part in re.split(r"(?:^|\s)(\d{1,2})\.\s", " " + body.replace("\n", " \n ")):
            if re.fullmatch(r"\d{1,2}", part) and int(part) == n + 1:
                n = int(part)
                verses[n] = ""
            elif n:
                verses[n] += " " + part
        out[int(m.group(1))] = (ascii_names(title), {k: ascii_names(re.sub(r"\s+", " ", v)) for k, v in verses.items()})
    return out


def wer(hyp, ref, punct=False):
    """Word error rate of hyp against ref (edit distance over words / words of ref)."""
    def toks(s):
        if punct:
            return s.split()
        return [w for w in (re.sub(r"[^\w'-]", "", x).lower() for x in s.split()) if w]
    h, r = toks(hyp), toks(ref)
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i] + [0] * len(h)
        for j, hw in enumerate(h, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw))
        prev = cur
    return prev[-1], len(r)


# =========================================================================== tokens
JUNK = re.compile(r"[|^«»*•§¥~_<>{}\\#@%=+]")


def preclean_tokens(toks):
    """The tokens of one OCR reading, cleaned (see preclean); dashes stand alone, stray digits are
    dropped and a lone stop joins the word before it."""
    out = []
    for t in toks:
        for part in re.split("(\u2014+)", t):
            if not part:
                continue
            c = preclean(part)
            if not c or re.fullmatch(r"\d+[.,;:]?", c):
                continue
            if re.fullmatch(r"[,.;:!?]+", c) and out and not out[-1].startswith("\x00"):
                if not re.search(r"[,.;:!?]$", out[-1]):
                    out[-1] += c[0]
                continue
            out.append(c)
    return out


def preclean(t):
    """One OCR token, before the readings are compared: Griffith's accents dropped, the second scan's
    stand-ins for accented vowels ('V&chaspati', 'Y£tudh£nas', 'VAchaspati') read as vowels, '0' as 'O'."""
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("„", '"')
    t = t.replace("–", "-")
    t = ascii_names(t)
    if re.fullmatch(r"0[,.!:;]?", t):
        return "O" + t[1:]
    if re.fullmatch(r"1[,.!:;]?", t):
        return "I" + t[1:]
    t = re.sub(r"(?<=[A-Za-z])[&£4](?=[a-z])", "a", t)
    t = re.sub(r"(?<=[a-z])[&£](?=\W|$)", "a", t)
    t = re.sub(r"^([A-Z])[&£4](?=[a-z])", r"\1a", t)
    if re.fullmatch(r"[A-Z][a-z]*[AIU][a-z]{2,}\W*", t):  # 'VAchaspati': a capital for an accented vowel
        t = t[0] + t[1:].lower()
    t = JUNK.sub("", t)
    t = re.sub(r"^[,.;:]+(?=[A-Za-z\"'])", "", t)
    t = re.sub(r"([,;:!?])[.,]+$", r"\1", t)
    t = re.sub(r"\.,$", ",", t)
    t = re.sub(r",,+", ",", t)
    return t


def join_hyphens(toks, vocab):
    """Words broken at a line end ('bow-' 'string') are joined, unless Griffith writes them with a
    hyphen ('far-' 'extended', 'Hotar-' 'priest')."""
    out = []
    i = 0
    while i < len(toks):
        t, ls = toks[i]
        if (t.endswith("-") and len(t) > 2 and t[-2].isalpha() and i + 1 < len(toks) and toks[i + 1][1]
                and re.match(r"^[a-zA-Z]", toks[i + 1][0])):
            nxt = toks[i + 1][0]
            m = re.match(r"^([A-Za-z'\-]+)(.*)$", nxt)
            head, tail = t[:-1], m.group(2)
            joined, hyph = head + m.group(1), head + "-" + m.group(1)
            sj, sh = vocab.score(core(joined)), vocab.g.get(core(hyph), 0)
            if sh and sh >= vocab.g.get(core(joined), 0):
                w = hyph
            elif sj:
                w = joined
            elif vocab.known(core(head)) and vocab.known(core(m.group(1))) and len(core(m.group(1))) > 2:
                w = hyph
            else:
                w = joined
            out.append((w + tail, ls))
            i += 2
            continue
        out.append((t, ls))
        i += 1
    return out


def key(t):
    """What two readings of a word must share to be aligned."""
    if t.startswith("\x00"):
        return t
    k = re.sub(r"[^a-z]", "", t.lower())
    return k or t


def tok_score(t, vocab):
    """How good a reading is: a known word scores high; digits and stray marks inside a word low."""
    if t.startswith("\x00"):
        return 5.0
    c = core(t)
    if not c:
        return 0.5 if re.fullmatch(r"[—\-.,;:!?\"'()]+", t) else -1.0
    s = vocab.score(c)
    if re.search(r"[0-9&£$]", t):
        s -= 3
    if re.search(r"[a-z][A-Z]", t):
        s -= 1.5
    if re.search(r"[^A-Za-z0-9'\"—\-.,;:!?()]", t):
        s -= 2
    inner = re.sub(r"^\W+|\W+$", "", t)
    if re.search(r"[^A-Za-z'\-]", inner):
        s -= 2
    return s


PUNCT_RE = re.compile(r"^(.*?[A-Za-z0-9)])?([^A-Za-z0-9]*)$")


def split_punct(t):
    m = re.match(r"^([\"'(]*)(.*?)([.,;:!?\"')—\-]*)$", t)
    return m.group(1), m.group(2), m.group(3)


def choose(a, b, vocab, pref="a"):
    """The better of two readings of one word: the known word; for punctuation, the first reading
    unless it has none where the second has a stop."""
    sa, sb = tok_score(a, vocab), tok_score(b, vocab)
    if a == b:
        return a
    if key(a) == key(b):
        # same letters: case, accents or punctuation differ
        la, wa, ra = split_punct(a)
        lb, wb, rb = split_punct(b)
        w = wa if tok_score(wa, vocab) >= tok_score(wb, vocab) else wb
        if w.isupper() and len(w) > 1:
            w = wa if not wa.isupper() else wb if not wb.isupper() else w
        r = ra if pref == "a" else rb
        if not ra and rb in (";", ":", "!", "?", "."):
            r = rb
        if not rb and ra in (";", ":", "!", "?", ".") and pref == "b":
            r = ra
        l = la or lb
        return l + w + r
    if sa > sb + 0.01:
        return a
    if sb > sa + 0.01:
        return b
    return a if pref == "a" else b


def block_score(toks, vocab):
    if not toks:
        return 0.0
    return sum(tok_score(t, vocab) for t in toks) / len(toks)


def fuse(A, B, vocab, pref="a", model=None, foreign=None):
    """Merge two readings (token lists) of the same text. Words found in one reading only are kept
    when they are real words, and, for longer runs, read like verse rather than notes."""
    ka, kb = [key(t) for t in A], [key(t) for t in B]
    sm = difflib.SequenceMatcher(None, ka, kb, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        a, b = A[i1:i2], B[j1:j2]
        if op == "equal":
            out += [choose(x, y, vocab, pref) for x, y in zip(a, b)]
        elif op == "replace":
            if len(a) == len(b):
                for x, y in zip(a, b):
                    if x.startswith("\x00") and y.startswith("\x00"):
                        out.append(x + "/" + y[1:])  # the two texts number a stanza differently
                    else:
                        out.append(choose(x, y, vocab, pref))
            else:
                # a word split or joined differently ('hither ward' / 'hitherward'), or junk
                ja, jb = "".join(key(t) for t in a), "".join(key(t) for t in b)
                if ja == jb and ja:
                    # the same letters: the reading in fewer pieces if it is a word
                    short, other = (a, b) if len(a) < len(b) else (b, a)
                    ok = all(tok_score(t, vocab) > 1 for t in short)
                    out += short if ok else other
                    continue
                else:
                    sa, sb = block_score(a, vocab), block_score(b, vocab)
                    sa -= 0.3 * sum(t.startswith("\x00") for t in b)
                win = a if (sa > sb or (sa == sb and pref == "a")) else b
                lose = b if win is a else a
                if foreign and len(win) >= 6 + len(lose) and foreign([t for t in win if not t.startswith("\x00")]):
                    win, lose = lose, win
                out += win + [t for t in lose if t.startswith("\x00") and t not in win]
        else:
            extra = a or b
            keep = [t for t in extra if t.startswith("\x00")]
            words_ = [t for t in extra if not t.startswith("\x00")]
            good = [t for t in words_ if tok_score(t, vocab) > 1.5]
            if len(words_) == 1 and words_[0] in ("I", "l", "1") and out and out[-1].endswith("!"):
                good = []  # '!' read as 'I' in the other text
            if model and len(words_) >= 4 and model.score(" ".join(words_)) < -1.0:
                good = []
            if foreign and len(words_) >= 6 and foreign(words_):
                good = []  # verse of the hymn before or after, run into this one in one text
            if words_ and len(good) >= 0.6 * len(words_) and not (len(words_) == 1 and not core(words_[0])):
                out += extra
            elif not words_:
                out += keep
    return out


# =========================================================================== one OCR text, hymn by hymn
def verse_lines(items):
    return [l for p in items if isinstance(p, Para) and p.verse for l in p.lines]


def first_line_match(lines, probe):
    """Index of the line of `lines` that best matches `probe` (the first line of a hymn in the other
    OCR text), with its similarity."""
    pk = re.sub(r"[^a-z]", "", probe.lower())[:40]
    best, at = 0.0, None
    for j, l in enumerate(lines):
        lk = re.sub(r"[^a-z]", "", l.lower())[:len(pk) + 5]
        r = difflib.SequenceMatcher(None, lk, pk).ratio()
        if r > best:
            best, at = r, j
    return at, best


def repair_missing(hy, other):
    """A hymn whose heading the OCR lost is found at the end of the hymn before it, by its first
    line in the other OCR text."""
    fixed = []
    for h in sorted(other):
        if h in hy or h - 1 not in hy or not verse_lines(other[h]):
            continue
        ov = verse_lines(other[h])
        lines = verse_lines(hy[h - 1])
        j, r = first_line_match(lines[1:], ov[0])
        if r < 0.6:
            # the first lines may be garbled, or lost with a page of this scan: the first line of the
            # other text's hymn that is found here marks where the hymn begins
            for k, probe in enumerate(ov[1:12], 1):
                if len(probe) < 25:
                    continue
                jk, rk = first_line_match(lines[1:], probe)
                if jk is not None and rk >= 0.8:
                    j, r = jk, rk
                    break
        if j is not None and r >= 0.6:
            j += 1
            k = 0
            new_prev, new_cur = [], []
            for p in hy[h - 1]:
                if isinstance(p, Para) and p.verse:
                    if k + len(p.lines) <= j:
                        new_prev.append(p)
                    elif k >= j:
                        new_cur.append(p)
                    else:
                        cut = j - k
                        new_prev.append(Para(p.lines[:cut], p.brk, p.pos))
                        q = Para(p.lines[cut:], False, p.pos + cut)
                        q.verse = True
                        new_cur.append(q)
                    k += len(p.lines)
                elif new_cur:
                    new_cur.append(p)
                else:
                    new_prev.append(p)
            hy[h - 1], hy[h] = new_prev, new_cur
            fixed.append(h)
    return fixed


def hymn_tokens(items, expect, vocab):
    """The verse of one hymn in one OCR text as a token list, with a marker before stanzas 2, 3 ..."""
    st, merged = split_stanzas(verse_lines(items), expect)
    out = []
    for n in sorted(st):
        toks = join_hyphens(st[n], vocab)
        if n > 1 or out:
            out.append(f"\x00{n}" + (f"-{merged[n]}" if n in merged else ""))
        out += preclean_tokens([t for t, _ in toks])
    return out


def trim_foreign(big, small, foreign):
    """Where one scan's hymn runs on into the next hymn (or begins inside the one before) and the
    other scan's does not, the run-on part, found in a neighbouring hymn, is cut away."""
    words_b = [i for i, t in enumerate(big) if not t.startswith("\x00")]
    if len(small) < 15 or len(words_b) < 1.25 * len(small):
        return big
    sm = difflib.SequenceMatcher(None, [key(t) for t in big], [key(t) for t in small], autojunk=False)
    blocks = [m for m in sm.get_matching_blocks() if m.size >= 3]
    if not blocks:
        return big
    a0, a1 = blocks[0].a, blocks[-1].a + blocks[-1].size
    head, tail = big[:a0], big[a1:]
    if len([t for t in tail if not t.startswith("\x00")]) >= 8 and foreign([t for t in tail if not t.startswith("\x00")]):
        big = big[:a1]
    if len([t for t in head if not t.startswith("\x00")]) >= 8 and foreign([t for t in head if not t.startswith("\x00")]):
        big = big[a0:]
    return big


def split_markers(toks):
    """{n: text} and {n: last} from a fused token list."""
    out, merged, n = {1: []}, {}, 1
    for t in toks:
        if t.startswith("\x00"):
            alts = [re.match(r"(\d+)(?:-(\d+))?", x) for x in t[1:].split("/")]
            alts = [m for m in alts if int(m.group(1)) > n]
            if not alts:
                continue
            m = next((m for m in alts if int(m.group(1)) == n + 1), min(alts, key=lambda m: int(m.group(1))))
            v = int(m.group(1))
            n = v
            out[n] = []
            if m.group(2):
                merged[n] = int(m.group(2))
            continue
        out[n].append(t)
    return {k: " ".join(v) for k, v in out.items()}, merged


# =========================================================================== finishing the text
def finish(text):
    """Spacing and capitals of a fused stanza: no space before a stop or around a dash, small capitals
    of a hymn's first word ('THIS', 'VasHAT') in lower case."""
    toks = text.split()
    out = []
    for i, t in enumerate(toks):
        letters = re.sub(r"[^A-Za-z]", "", t)
        if len(letters) >= 2 and (letters.isupper() or re.fullmatch(r"[A-Z][a-z]+[A-Z]+[a-z]*", letters)) \
                and not re.fullmatch(r"[IVXLC]+", letters):
            first = re.search(r"[A-Za-z]", t).start()
            t = t[:first + 1] + t[first + 1:].lower()
        out.append(t)
    s = " ".join(out)
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"\s*—\s*", "—", s)
    s = re.sub(r"([,;:])(?=[A-Za-z])", r"\1 ", s)
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r"\s+\)", ")", s)
    s = re.sub(r"\s{2,}", " ", s).strip()
    return s


# =========================================================================== Sanskrit
ACCENT = re.compile(r"[॒॑॓॔᳐-᳿꣠-ꣿ]")
METRE = re.compile(r"अनुष्टु|त्रिष्टु|गायत्री|जगती|पङ्क्ति|बृहती|उष्णि|पर्याय|एकावसान|त्रिपदा|द्विपदा|एकपदा")


def header_line(l):
    """A seer/deity/metre line or a paryaya number that the source runs into the verses."""
    l = l.strip()
    return (not re.search("[\u0900-\u0963\u0972-\u097F]", l)
            or bool(re.match(r"^\(?[०-९]+[\s,\-)]", l))
            or (bool(METRE.search(l)) and ", " in l))


def sanskrit_variants(dharmic, kanda, sukta):
    """Two readings of the verses of a sukta: av_verses() of build_vedas as it is, and the same with
    the verses split that it runs together where the source types the number marks '।।४।।' (any
    metre lines between them dropped). Both keep a last verse that the source leaves unnumbered."""
    vs = av_verses(dharmic, kanda, sukta)
    split = []
    for v in vs:
        for part in re.split(r"\s*[।॥]{1,2}\s*[०-९]{1,3}\s*[।॥]{1,2}\s*(?:\([०-९0-9]+\))?", v):
            lines = [l for l in part.split("\n") if l.strip() and not header_line(l)]
            if lines:
                t = re.sub(r"[।॥\s]+$", "", "\n".join(l.strip() for l in lines)) + "॥"
                split.append(t)
    data = json.load(open(os.path.join(dharmic, "AtharvaVeda", f"atharvaveda_kaanda_{kanda}.json"), encoding="utf-8"))
    raw = ACCENT.sub("", next(h for h in data if h["sukta"] == sukta)["text"])
    tail = re.split(r"[।॥]\s*[०-९]{1,3}\s*[।॥]*[^\n]*\n", raw + "\n")[-1]
    tail = [l.strip() for l in tail.split("\n") if l.strip() and not header_line(l)]
    out = []
    for variant in (list(vs), split):
        if variant and tail and len(re.findall("[\u0900-\u097F]", "".join(tail))) >= 12:
            variant.append(re.sub(r"[।॥\s]+$", "", "\n".join(tail)) + "॥")
        if variant and variant not in out:
            out.append(variant)
    return out


# =========================================================================== titles: Griffith's Index of Hymns
INDEX_NUM = re.compile(r"^((?:\d|[SOGCTt>•*'’Il](?=[\dSO>•*'’]|\s))[\dSOGCTt>•*'’Il]{0,3}(?:\s?[-–—^,]\s?\d{1,3})*)\s+(?=[\"'(]?[A-Z])")


def index_section(lines):
    """The lines of the Index of Hymns (after the main text), up to the next index."""
    for i, l in enumerate(lines):
        if i > len(lines) * 0.75 and re.search(r"INDEX\s+OF\s+HYMNS", l) and not re.search(r"[\[\]]|\d{3}", l) \
                and any(re.match(r"^\W{0,2}B\S{2,3}\s+[IVXL]", x) for x in lines[i + 1:i + 8]):
            end = next((k for k in range(i + 1, len(lines))
                        if re.search(r"INDEX\s+OF\s+NAMES|GENERAL\s+LIST", lines[k])), len(lines))
            return lines[i + 1:end]
    return []


def index_entries(lines, books, numbered):
    """{book: [(first, last, text)]} from an Index of Hymns. In a text that prints the hymn numbers,
    an entry starts with its number(s) ('8,9,10', '129-132'); the numbers are taken as a check only,
    the entries being numbered in order."""
    raw, cur = {}, None
    want = list(books)
    for l in lines:
        t = l.strip()
        if not t:
            continue
        m = re.match(r"^\W{0,2}B\S{2,3}\s+([IVXLHFfl/1]{1,6})\S{0,2}\.?\s*$", t)
        if m and want:
            r = roman_readings(m.group(1))
            hit = next((b for b in want[:2] if b in r), None)
            if hit:
                while want and want[0] != hit:
                    want.pop(0)
                cur = want.pop(0)
                raw[cur] = []
                continue
        if cur is None or (len(t) < 60 and (fuzzy_has(t, "INDEXOFHYMNS", 0.6) or re.search(r"HYMN\W*\s*P|HYMN\W*$", t.upper())
                                            or re.match(r"^[4-5]\S\S\s", t))):
            continue
        t = re.sub(r"(\s*[.,_\-—~'\"*^»•„]{1,3}\s*){2,}", " ", t)  # dot leaders
        # an entry run on after the page number of the one before ('... 62 20—23 Repetitions of ...')
        parts = re.split(r"(?<=\s\d{2})\s+(?=\d{1,3}\s?[-–—^]\s?\d{1,3}\s+[A-Z])|(?<=\s\d{2})\s+(?=\d{1,2}[iIl]-?\s+[A-Z])", t)
        for part in parts:
            raw[cur].append(part)
    out = {}
    for b, ls in raw.items():
        entries = []
        for t in ls:
            m = INDEX_NUM.match(t) if numbered else None
            starts = bool(m) if numbered else (not entries or re.search(r"\d{1,3}\s*$", entries[-1][1]) and t[:1].isupper())
            if starts:
                entries.append([m.group(1) if m else "", t[m.end():] if m else t])
            elif entries:
                entries[-1][1] += " " + t
        nums, k = [], 1
        for n, text in entries:
            rng = re.fullmatch(r"(\d{1,3})\s?[-–—^]\s?(\d{1,3})", n.replace(" ", ""))
            lst = re.fullmatch(r"\d{1,3}(,\d{1,3})+", n.replace(" ", ""))
            if rng and int(rng.group(1)) in (k, k + 1, k + 2):
                first, last = int(rng.group(1)), int(rng.group(2))
            elif lst and int(n.split(",")[0]) in (k, k + 1, k + 2):
                first, last = int(n.split(",")[0]), int(n.split(",")[-1])
            elif n.isdigit() and k - 2 <= int(n) <= k + 6 and int(n) >= 1:
                first = last = int(n)
            else:
                first = last = k
            nums.append((first, last, text))
            k = last + 1
        out[b] = nums
    return out


def clean_title(t, vocab):
    t = ascii_names(t)
    t = re.sub(r"(\w)- (\w)", r"\1\2", t)
    t = re.sub(r"(\s+[\d&>/.,'*]{1,4}){1,3}\s*$", "", t)  # page numbers
    toks = [x for x in (preclean(x) for x in t.split()) if x]
    while toks and (re.fullmatch(r"\W+|\d+\W*", toks[-1]) or (len(core(toks[-1])) <= 2 and core(toks[-1]) not in
                                                                ("of", "to", "in", "on", "ox"))):
        toks.pop()
    t = " ".join(spell(x, vocab) for x in toks)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t).strip(" ,.;:-")
    return t


def fuse_titles(primary, other, vocab):
    """Correct each title of the numbered Index word by word from the other OCR text of the Index
    (only words read differently are replaced; nothing is added)."""
    out = {}
    for b, entries in primary.items():
        pool = [x for x in (preclean(t) for e in other.get(b, []) for t in e[2].split()) if x]
        pk = [key(t) for t in pool]
        for first, last, text in entries:
            text = re.sub(r"(?<!Hymn)(?<!of)\s+[\d&]{2,3}\b.*$", "", text)  # a page number, and anything run on
            toks = [x for x in (preclean(t) for t in text.split()) if x]
            tk = [key(t) for t in toks]
            best, at, n = 0.0, None, len(toks)
            for j in range(0, max(1, len(pk) - n + 1)):
                r = difflib.SequenceMatcher(None, tk, pk[j:j + n + 2], autojunk=False).ratio()
                if r > best:
                    best, at = r, j
            if at is not None and best >= 0.6:
                sm = difflib.SequenceMatcher(None, tk, pk[at:at + n + 2], autojunk=False)
                for op, i1, i2, j1, j2 in sm.get_opcodes():
                    if op in ("equal", "replace") and i2 - i1 == j2 - j1:
                        for x in range(i2 - i1):
                            toks[i1 + x] = choose(toks[i1 + x], pool[at + j1 + x], vocab)
            while toks and len(core(toks[-1])) <= 3 and not vocab.g.get(core(toks[-1])) and core(toks[-1]) not in ("ox",):
                toks.pop()
            out[(b, first)] = (last, clean_title(" ".join(toks), vocab))
    return out


def best_window(tk, pk, lo=0):
    """Where the key list tk matches best in pk (from lo): (start, end, ratio)."""
    best, at, n = 0.0, None, len(tk)
    for j in range(lo, max(lo + 1, len(pk) - n + 1)):
        r = difflib.SequenceMatcher(None, tk, pk[j:j + n], autojunk=False).ratio()
        if r > best:
            best, at = r, j
    return (at, at + n, best) if at is not None else (None, None, 0.0)


def fill_gaps(titles, sections, vocab):
    """A title missing from the numbered Index (its line lost or run into another) is read from the
    other OCR text of the Index, between the titles of the hymns before and after it."""
    for b, pool in sections.items():
        pk = [key(t) for t in pool]
        for h in range(2, HYMNS[b]):
            if titles.get((b, h)) or not titles.get((b, h - 1)) or not titles.get((b, h + 1)):
                continue
            prev_k = [key(t) for t in titles[(b, h - 1)].split()][-4:]
            next_k = [key(t) for t in titles[(b, h + 1)].split()][:4]
            _, e1, r1 = best_window(prev_k, pk)
            s2, _, r2 = best_window(next_k, pk, e1 or 0)
            if r1 >= 0.7 and r2 >= 0.7 and e1 is not None and 2 <= s2 - e1 <= 30:
                t = clean_title(" ".join(pool[e1:s2]), vocab)
                if len(t) >= 8:
                    titles[(b, h)] = t


def read_titles(ocr, vocab):
    """{(book, hymn): title} from the Index of Hymns of both volumes."""
    titles = {}
    for vol, (num, other) in ((1, ("v1b", "v1a")), (2, ("v2b", "v2a"))):
        P = index_entries(index_section(load(ocr[num])), VOLUMES[vol], True)
        O = index_entries(index_section(load(ocr[other])), VOLUMES[vol], False)
        for (b, first), (last, t) in fuse_titles(P, O, vocab).items():
            for h in range(first, last + 1):
                titles[(b, h)] = t
        for src in (O, P):
            sections = {b: [x for x in (preclean(t) for e in es for t in re.sub(r"\s\d{1,3}\b", " ", e[2]).split()) if x]
                        for b, es in src.items()}
            fill_gaps(titles, sections, vocab)
    return titles


# =========================================================================== titles: Griffith's notes
INTRO_SENT = re.compile(r"^(?:(?:The|This)\s+(?:hymn|Book|stanza|prose hymn)(?:,[^.]*?,)?\s+(?:is|contains|consists of)\s+)?"
                        r"([Tt]aken(?:,? in continuation,?)? from R\.\s?V\.\s?[IVXL]+\.?\s?\d+|"
                        r"(?:a|an|the)\s+[^.]{6,200}?|(?:A|An)\s[^.]{6,200}?)[.,;](?:\s|$)")


def note_intros(items):
    """The opening sentences of the notes in a Book's items, with their positions."""
    out = []
    for k, p in enumerate(items):
        if isinstance(p, Para) and not p.verse:
            t = re.sub(r"\s+", " ", " ".join(p.lines))
            t = re.sub(r"(\w)- (\w)", r"\1\2", t)
            if re.match(r"^(The|This)\s+(hymn|prose hymn)\b|^(A|An)\s+(\w+\s+){0,3}?(charm|prayer|hymn|glorification|"
                        r"benediction|imprecation|incantation|accompaniment|counter-charm|continuation|expiat\w+|"
                        r"funeral|curative|protective|formula)|^Taken\b|^(Stanzas?\s[\d,\u2014-]+\s(are|is)\s)?[Tt]aken from R", t):
                m = INTRO_SENT.match(t)
                if m:
                    out.append((k, m.group(1)))
    return out


def intro_title(sent, vocab):
    t = " ".join(x for x in (preclean(w) for w in sent.split()) if x)
    t = re.sub(r"\s+([,.;:!?])", r"\1", t)
    t = re.sub(r"^(the|a|an)\b", lambda m: m.group(1).capitalize(), t)
    m = re.match(r"^[Tt]aken(?:,? in continuation,?)? from R\.\s?V\.\s?([IVXL]+)\.?\s?(\d+)", t)
    if m:
        return f"From Rig Veda {m.group(1)}.{m.group(2)}"
    return t.strip(" ,;:")


CONTENT_STOP = set("a an the of to and or for in on with by from at as his her its their this that is be "
                   "charm prayer hymn glorification benediction against".split())


def overlap(a, b):
    wa = {w for w in re.findall(r"[a-z]+", a.lower()) if w not in CONTENT_STOP and len(w) > 2}
    wb = {w for w in re.findall(r"[a-z]+", b.lower()) if w not in CONTENT_STOP and len(w) > 2}
    return len(wa & wb), len(wa), len(wb)


def shorten(t, limit=72):
    """A long title cut at a clause boundary."""
    if len(t) <= limit:
        return t
    for sep in (", with ", ", and ", "; ", ", for ", ", ", " with ", " for ", " by ", " and "):
        k = t.rfind(sep, 0, limit + 1)
        while k > 24:
            cand = t[:k].rstrip(" ,;")
            if len(cand) <= limit and not re.search(r"\b(and|or|of|the|a|an|to|in|on|for|with|by)$", cand):
                return cand
            k = t.rfind(sep, 0, k)
    cut = t[:limit].rsplit(" ", 1)[0]
    while re.search(r"\b(and|or|of|the|a|an|to|in|on|for|with|by)$", cut):
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip(" ,;")


# =========================================================================== stanzas Griffith does not translate
LATIN = "[Griffith gives {} only in a Latin version, in the Appendix to his translation{}]"
SPECIAL = {
    # (book, hymn): [(first stanza, last stanza or None for the end of the hymn, English)]; the
    # English is Griffith's own note on the passage, or a statement that he gives it only in Latin
    (1, 11): [(3, None, LATIN.format("stanzas 3-6", ": 'The details given in stanzas 3-6 are strictly obstetric "
                                     "and not presentable in English.'"))],
    (2, 20): [(1, None, "[Griffith does not print this hymn. His note on Hymn 19: 'A non-metrical charm invoking "
                        "Agni's aid against an enemy. Hymns XX-XXIII are exactly similar except that other deities, "
                        "Vayu, Surya, Chandra or the Moon, and the Waters, are addressed instead of Agni.' Here "
                        "Vayu is addressed.]")],
    (2, 21): [(1, None, "[Griffith does not print this hymn: it is Hymn 19 with Surya addressed instead of "
                        "Agni.]")],
    (2, 22): [(1, None, "[Griffith does not print this hymn: it is Hymn 19 with Chandra, the Moon, addressed "
                        "instead of Agni.]")],
    (2, 23): [(1, None, "[Griffith does not print this hymn: it is Hymn 19 with the Waters addressed instead "
                        "of Agni.]")],
    (4, 4): [(3, None, LATIN.format("stanzas 3 to the end", "."))],
    (5, 15): [(3, None, "[Griffith: 'Stanzas 3-11 of the hymn, which is a charm for general prosperity, are "
                        "exactly the same with the exception of the numbers which increase by eleven in each stanza "
                        "(thirty and three, forty and four, and so on) up to one hundred and ten in stanza 10, "
                        "stanza 11 concluding with one thousand and one hundred.']")],
    (5, 16): [(2, None, "[Griffith: 'The hymn, which is a charm for the increase and prosperity of cattle, "
                        "contains ten other similar lines, the only difference being that in the place of "
                        "ekavrishah, single bull, dvivrishah, double bull, or, worth two bulls, trivrishah, triple "
                        "bull, or, worth three bulls, and so on, follow in regular order up to ekadasah, "
                        "eleven-fold, in stanza 11, in which apodakah, waterless, stands instead of the arasah, "
                        "sapless, of the preceding lines.']")],
    (6, 16): [(4, 4, "[Griffith: 'The fourth verse, consisting of one line, is untranslatable: Thou art Alasala "
                     "in front, thou art Silanjala (a weed growing in corn) behind: Nilagalasala (probably a weed "
                     "of similar kind).']")],
    (6, 72): [(1, None, LATIN.format("this hymn", "."))],
    (6, 101): [(1, None, LATIN.format("this hymn", "."))],
    (6, 138): [(4, None, LATIN.format("stanzas 4 and 5", "."))],
    (7, 35): [(2, None, LATIN.format("stanzas 2 and 3", ": 'Stanzas 2 and 3 have a totally different object.'"))],
    (7, 90): [(3, None, LATIN.format("stanza 3", "."))],
    (20, 126): [(16, 17, LATIN.format("stanzas 16 and 17", ": 'I pass over stanzas 16 and 17, which cannot be "
                                      "decently translated.'"))],
    (20, 136): [(1, None, LATIN.format("this hymn", "."))],
}

# Book 20 repeats stanzas of its own earlier hymns, and Griffith then prints only a reference
# ('Stanzas 1-4 are repeated from A. V. XX. 14'): those stanzas are given his English from there.
REPEATS = {
    (20, 47): {4: (38, 4), 5: (38, 5), 6: (38, 6), 7: (38, 1), 8: (38, 2), 9: (38, 3)},
    (20, 57): {11: (53, 1), 12: (53, 2), 13: (53, 3)},
    (20, 59): {1: (10, 1), 2: (10, 2)},
    (20, 62): {1: (14, 1), 2: (14, 2), 3: (14, 3), 4: (14, 4)},
    (20, 68): {1: (57, 1), 2: (57, 2), 3: (57, 3)},
    (20, 70): {7: (38, 4), 8: (38, 5), 9: (38, 6)},
    (20, 71): {4: (60, 4), 5: (60, 5), 6: (60, 6)},
}


# =========================================================================== pairing with the Sanskrit
def sa_length(v):
    return len(re.findall("[क-ह]", v))


def pair(en, merged, variants):
    """Map Griffith's stanzas (by his numbers) to the Sanskrit verses: stanza n covers the verses
    from n to the next stanza's number (a number the OCR or the print lost leaves two stanzas in
    one), and the last stanza the rest. Accepted when the numbers fit the verse count and the
    lengths agree; or, with as many stanzas as verses, one to one (a misprinted number).
    Returns ({n: (first, last)}, verses, how) or None."""
    nums = sorted(en)
    if not nums:
        return None
    for sa in variants:
        S = len(sa)
        if not S:
            continue
        tries = []
        if nums[-1] <= S:
            rng = {}
            for i, n in enumerate(nums):
                rng[n] = (n, max(n, (nums[i + 1] - 1) if i + 1 < len(nums) else S, merged.get(n, n)))
            tries.append((rng, "numbers"))
        if len(nums) == S and nums != list(range(1, S + 1)):
            tries.append(({n: (k + 1, k + 1) for k, n in enumerate(nums)}, "renumbered"))
        for rng, how in tries:
            if how == "numbers" and nums == list(range(1, S + 1)) and not merged:
                return rng, sa, how  # every verse numbered, as many as in the Sanskrit
            ratios = []
            for n, (a, b) in rng.items():
                if en[n].startswith("["):
                    continue
                L = sum(sa_length(sa[i - 1]) for i in range(a, b + 1))
                ratios.append((len(re.sub(r"[^A-Za-z]", "", en[n])) / max(L, 1), b - a + 1))
            if not ratios:
                return rng, sa, how
            med = sorted(r for r, _ in ratios)[len(ratios) // 2]
            bad = [r for r, k in ratios if (k > 1 and r < 0.6 * med) or (how == "renumbered" and (r < 0.4 * med or r > 2.6 * med))]
            if sum(k > 1 for _, k in ratios) > max(1, len(ratios) // 4):
                bad.append(0)  # too many numbers lost to place the verses
            if len(ratios) <= 2 or not bad:
                return rng, sa, how
    return None


# =========================================================================== explicit corrections
# Titles damaged in both OCR texts of the Index of Hymns (read from the page images' wording).
TITLE_FIXES = {
    (2, 11): "Counter-charm, with an amulet, against an enemy's spell",
    (2, 13): "A youth's Investiture ceremony (godanam)",
    (2, 16): "A prayer for general protection",
    (2, 20): "Repetition of Hymn 19, addressed to Vayu instead of Agni",
    (2, 21): "Repetition of Hymn 19, addressed to Surya instead of Agni",
    (2, 22): "Repetition of Hymn 19, addressed to Chandra, the Moon, instead of Agni",
    (2, 23): "Repetition of Hymn 19, addressed to the Waters instead of Agni",
    (2, 28): "A prayer for a boy's long and happy life",
    (3, 2): "A rifaccimento or recension of Hymn 1",
    (3, 8): "A charm to secure the submission, loyalty and fidelity of kinsmen",
    (3, 19): "A glorification of the office of a King's household priest",
    (4, 24): "A hymn of prayer and praise to Indra",
    (6, 25): "A charm to remove pustules or scrofulous swellings (apachitas)",
    (6, 83): "A charm against sores and pustules (apachitas)",
    (6, 121): "A prayer for happiness in heaven",
    (7, 50): "A gambler's prayer for success in gaming",
    (6, 87): "A benediction addressed to a newly elected King",
    (6, 88): "A benediction addressed to a newly elected King",
    (6, 92): "A charm to strengthen and inspirit a war-horse",
    (7, 12): "A prayer for influence at deliberative and religious meetings",
    (7, 66): "A prayer to Vak",
    (8, 10): "A glorification of the mystical abstraction Viraj",
    (9, 9): "Enunciation of mystico-theological and cosmological doctrine",
    (10, 7): "Skambha, the Pillar or Fulcrum of all existence",
    (13, 3): "A glorification of Rohita, with a malediction on the man who wrongs a Brahman",
    (19, 6): "The Purusha-Sukta, on the mystical Sacrifice of Purusha",
    (19, 8): "A prayer to the Lunar Mansions and other Powers for protection and prosperity",
    (19, 21): "A single line giving the names of the chief Vedic metres",
    (19, 25): "A charm to be used when a young ox is first yoked",
    (19, 34): "A protective charm addressed to the panacea called Jangida",
    (19, 35): "A similar charm, addressed to the same",
    (19, 46): "A charm accompanying investiture with an amulet that ensures safety and victory",
    (19, 56): "A hymn to Sleep",
    (19, 61): "A prayer for long life, prosperity and final happiness in heaven",
    (19, 62): "A prayer for the love of Gods and men",
    (19, 66): "A hymn to Agni identified with the Sun",
    (19, 72): "A hymn, accompanying libations, for wealth and prosperity",
    (4, 30): "A glorification of Vak or Speech",
    (4, 31): "A hymn to Manyu or Wrath",
    (6, 60): "The wooing of a bride",
    (6, 61): "A prayer for prosperity and greatness",
    (6, 62): "A prayer for purification and riches",
    (6, 128): "A charm for fair weather",
    (6, 129): "A charm for success and happiness",
    (7, 94): "A charm to ensure the obedience of subjects",
    (7, 95): "An incantation against an undetected thief",
    (7, 96): "An incantation against an undetected thief",
    (8, 3): "A prayer for the destruction of demons",
    (9, 10): "Continuation of Hymn 9",
    (13, 4): "A glorification of the Sun as the one only Deity",
    (16, 1): "On the preparation and use of holy water, with a prayer for purification",
    (18, 2): "A funeral hymn, taken mainly from the Rigveda",
    (19, 11): "A continuation of Hymn 10",
    (19, 29): "A continuation of Hymn 28",
    (19, 65): "A hymn to Agni as the Sun",
}

# Frequent misreadings left after the two texts are compared (both texts wrong, or the word not
# in the vocabulary), as (wrong, right) for whole words.
REPLACEMENTS = {
    "Sdrya": "Surya", "Varnna": "Varuna", "Varupa": "Varuna", "Graht": "Grahi", "Kiondinis": "Kimidinis",
    "Sddra": "Sudra", "hyinn": "hymn", "miloh-kine": "milch-kine", "erushing": "crushing", "Gugguld": "Guggulu",
    "Ajasringt": "Ajasringi", "Jearned": "learned", "g'ory": "glory", "Mitra-varuga": "Mitra-Varuna",
    "Mabavrishas": "Mahavrishas", "Vishkaridha-j": "Vishkandha", "Ardyis": "Arayis", "Ardyts": "Arayis",
    "Kuh": "Kuhu", "Patae": "Patha", "Pauchaudana": "Panchaudana", "Sbrabhaka": "Serabhaka", "Slra": "Sira",
    "Khapvakha": "Khanvakha", "Khaimakhd": "Khaimakha", "Tadurt": "Taduri", "Thixxk": "Think",
    "JLightning-Flasher": "Lightning-Flasher", "Thislowly": "This lowly",
}

# Whole phrases (the OCR split or ran together words), and passages restored where both scans fail.
PHRASES = {
    "Kush ilia's": "Kushtha's", "EUe where": "Elsewhere", "Mahaa- vrishas": "Mahavrishas",
    "Mahaa-vrishas": "Mahavrishas", "Brihati, Trishtup, Jagat,": "Brihati, Trishtup, Jagati.",
}


# Last misreadings, found in the list of suspicious words and read against the page images; applied
# to the finished text and titles.
FINAL = [
    (r"\bMitra-varu[gpy]a\b", "Mitra-Varuna"), (r"\bSbrabhaka\b", "Serabhaka"), (r"\bYajuayajuiya\b", "Yajnayajniya"),
    (r"\bAffiicb\b", "Afflict"), (r"\bAauai\b", "Agni"), (r"\bher\. afterbirth", "her afterbirth"), (r"\beontractest\b", "contractest"),
    (r"\baecordantly\b", "accordantly"), (r"\bhjrmn\b", "hymn"), (r"\bTrdyawana\b", "Trayamana"),
    (r"\bNitatnt\b", "Nitatni"), (r"\bPraxr\b", "Prastara"), (r"\beattle\b", "cattle"), (r"\bRakft I\b", "Raka!"),
    (r"\binflietest\b", "inflictest"), (r"\ball-rbounteous I\b", "all-bounteous!"), (r"\blightnmg\b", "lightning"),
    (r"\bSvftm\b", "Svaha"), (r"\bBhatapati\b", "Bhutapati"), (r"\bdefied Earth\b", "deified Earth"),
    (r"^A hymn to Kama or Time$", "A hymn to Kala or Time"), (r'\\"paid', '"paid'), (r'reverence be "paid!', "reverence be paid!"),
]


def final_fix(t):
    for a, b in FINAL:
        t = re.sub(a, b, t)
    return t


# =========================================================================== the build
# How the OCR reads the small capitals of a hymn's first word ('THE' as 'Tux', 'THEE' as 'Tare'):
# (misread letter, true letter) pairs that cost little in small_caps_word().
SMALL_CAPS = {("u", "h"), ("a", "h"), ("x", "h"), ("n", "h"), ("b", "h"), ("e", "h"), ("x", "e"), ("z", "e"),
              ("r", "e"), ("b", "e"), ("s", "e"), ("k", "e"), ("c", "e"), ("o", "e"), ("p", "d"), ("r", "f"),
              ("b", "r"), ("n", "r"), ("r", "y"), ("o", "u"), ("a", "g"), ("i", "l"), ("l", "i"), ("r", "t"),
              ("e", "i"), ("c", "e"), ("g", "c"), ("w", "m"), ("p", "f"), ("t", "f")}


def caps_distance(a, b):
    prev = [float(j) for j in range(len(b) + 1)]
    for i, ca in enumerate(a, 1):
        cur = [float(i)] + [0.0] * len(b)
        for j, cb in enumerate(b, 1):
            sub = 0.0 if ca == cb else 0.35 if (ca, cb) in SMALL_CAPS else 1.0
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + sub)
        prev = cur
    return prev[-1]


_COMMON = []


FIRST_WORDS = {(6, 81): "Thou", (10, 2): "Who", (20, 57): "As a", (20, 68): "As a", (20, 82): "If", (20, 135): "Bang!"}  # beyond small_caps_word()


def small_caps_word(tok, readings, vocab):
    """The first word of a hymn, printed in small capitals and often misread by both scans, read as
    the common word of Griffith's that one of its readings fits best."""
    lead, word, trail = split_punct(tok)
    c = word.lower()
    if not c.isalpha() or vocab.g.get(c, 0) >= 5:
        return tok
    cores = {core(r) for r in readings if r}
    if len(cores) == 1 and c in cores and vocab.plausible(c):
        return tok  # both scans agree on a real word
    if not _COMMON:
        _COMMON.extend(w for w, n in vocab.g.items() if n >= 15 and w.isalpha())
    best = None
    for r in [c] + [core(x) for x in readings if x]:
        if not r or len(r) < 2:
            continue
        if vocab.g.get(r, 0) >= 5:
            cand = (0.0, -vocab.g[r], r)
            best = min(best, cand) if best else cand
            continue
        for w in _COMMON:
            if w[0] != r[0] or abs(len(w) - len(r)) > 1:
                continue
            d = caps_distance(r, w)
            if d <= 1.05 and (best is None or (d, -vocab.g[w]) < best[:2]):
                best = (d, -vocab.g[w], w)
    if not best:
        return tok
    return lead + best[2].capitalize() + trail


def deity_of(text):
    """The God a Book 20 hymn addresses: Indra wherever he is named (the Soma of these hymns is
    mostly the drink offered to him), else the God named most often."""
    names = {"Indra": "Indra", "Agni": "Agni", "Asvins": "the Asvins", "Surya": "Surya", "Maruts": "the Maruts",
             "Dawn": "Dawn", "Brihaspati": "Brihaspati", "Varuna": "Varuna", "Vishnu": "Vishnu", "Soma": "Soma"}
    counts = {n: len(re.findall(r"\b" + n + r"\b", text)) for n in names}
    if counts["Indra"] and counts["Indra"] >= max(counts[n] for n in names if n != "Soma") / 2:
        return "Indra"
    counts["Soma"] = 0  # in Book 20 the Soma is the drink offered to Indra
    best = max(counts, key=counts.get)
    return names[best] if counts[best] else None


def clean_stanza(text, vocab):
    toks = []
    for t in text.split():
        lead, w, trail = split_punct(t)
        if w in REPLACEMENTS:
            t = lead + REPLACEMENTS[w] + trail
        elif w and not vocab.plausible(core(w)) and core(w) and "-" not in w:
            t = spell(t, vocab)
        toks.append(t)
    while toks and len(core(toks[-1])) <= 2 and not vocab.known(core(toks[-1])) and core(toks[-1]) not in ("o", "i"):
        toks.pop()  # a stray mark or letter left at the end of a stanza ('Rh')
    text = finish(" ".join(toks))
    for a, b in PHRASES.items():
        text = text.replace(a, b)
    return text


def build(ocr_dir, dharmic, ws_dir, rv_dir=None, log=print):
    ocr = {f: os.path.join(ocr_dir, f + ".txt") for f in ("v1a", "v1b", "v2a", "v2b")}
    ws = read_wikisource(ws_dir)
    vocab = Vocab(rv_dir, extra_texts=[v for _, vs in ws.values() for v in vs.values()])
    report = collections.defaultdict(list)

    # ---- every OCR text: Books, paragraphs, verse or note
    books = {}
    for f, vol in (("v1a", 1), ("v1b", 1), ("v2a", 2), ("v2b", 2)):
        lines = load(ocr[f])
        starts, end = main_range(lines, VOLUMES[vol])
        bl = VOLUMES[vol]
        bounds = [starts[b] for b in bl] + [end]
        for k, b in enumerate(bl):
            books[(f[-1], b)] = book_items(lines, bounds[k] + 1, bounds[k + 1], b)
    model = classify(books)

    # ---- hymns, and the Sanskrit
    hymns, variants = {}, {}
    for b in range(1, 21):
        hy = {o: hymns_of_book(books[(o, b)], HYMNS[b]) for o in "ab"}
        for o, p in (("a", "b"), ("b", "a")):
            for h in repair_missing(hy[o], hy[p]):
                report["heading found by the other text"].append(f"{b}.{h} ({o})")
        hymns[b] = hy
        for h in range(1, HYMNS[b] + 1):
            if b == 13 and h == 4:  # Griffith's 13.4 = suktas 4-9, numbered on through them
                variants[(b, h)] = [[v for s in range(4, 10) for v in sanskrit_variants(dharmic, 13, s)[0]]]
            else:
                variants[(b, h)] = sanskrit_variants(dharmic, b, h)

    # ---- the two readings, word by word
    toks = {}
    for b in range(1, 21):
        for h in range(1, HYMNS[b] + 1):
            expect = max([len(v) for v in variants[(b, h)]] or [0])
            toks[(b, h)] = [hymn_tokens(hymns[b][o].get(h, []), expect, vocab) for o in "ab"]
    agreed = collections.Counter()
    for ta, tb in toks.values():
        sm = difflib.SequenceMatcher(None, [key(t) for t in ta], [key(t) for t in tb], autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                for x, y in zip(ta[i1:i2], tb[j1:j2]):
                    c = core(x)
                    if x == y and c.isalpha() and len(c) >= 3:
                        agreed[c] += 1
    for c, n in agreed.items():
        vocab.g[c] += n  # a word both scans read alike is taken as a real one
    _BUCKETS.clear()

    def foreign_for(b, h):
        near = [k for x in (h - 1, h + 1) if (b, x) in toks for t in toks[(b, x)] for k in [key(w) for w in t]]
        near_s = " ".join(near)

        def test(words_):
            ks = [key(w) for w in words_ if not w.startswith("\x00")]
            hits = sum(" ".join(ks[i:i + 4]) in near_s for i in range(0, max(1, len(ks) - 3)))
            return hits >= 0.6 * max(1, len(ks) - 3)
        return test

    english = {}
    wer_before = {"a": [0, 0], "b": [0, 0]}
    wer_after = [0, 0]
    for (b, h), (ta, tb) in toks.items():
        foreign = foreign_for(b, h)
        ta, tb = trim_foreign(ta, tb, foreign), trim_foreign(tb, ta, foreign)
        fused = fuse(ta, tb, vocab, model=model, foreign=foreign)
        expect = max([len(v) for v in variants[(b, h)]] or [0])
        if expect and len(split_markers(fused)[0]) < 0.5 * expect:
            plain = fuse(ta, tb, vocab, model=model)  # the text found 'foreign' is this hymn's own
            if len(split_markers(plain)[0]) > len(split_markers(fused)[0]):
                fused = plain
        if b == 1 and h in ws:
            wt = []
            for n, v in sorted(ws[h][1].items()):
                if h == 11 and n >= 3:
                    break
                if n > 1:
                    wt.append(f"\x00{n}")
                wt += preclean_tokens(v.split())
            for name, t in (("a", ta), ("b", tb)):
                st, _ = split_markers(t)
                for n, ref in ws[h][1].items():
                    if not (h == 11 and n >= 3):
                        e, m = wer(clean_stanza(st.get(n, ""), vocab), ref)
                        wer_before[name][0] += e
                        wer_before[name][1] += m
            st, _ = split_markers(fused)
            for n, ref in ws[h][1].items():
                if not (h == 11 and n >= 3):
                    e, m = wer(clean_stanza(st.get(n, ""), vocab), ref)
                    wer_after[0] += e
                    wer_after[1] += m
            fused = fuse(fused, wt, vocab)  # Wikisource as a third reading
        st, merged = split_markers(fused)
        if st.get(1):
            first, rest = (st[1].split(None, 1) + [""])[:2]
            fixed = FIRST_WORDS.get((b, h)) or small_caps_word(first, [t[0] if t else "" for t in (ta, tb)], vocab)
            if fixed != first:
                report["first word in small capitals read as"].append(f"{b}.{h}: {first} -> {fixed}")
            st[1] = fixed + " " + rest
        english[(b, h)] = ({n: clean_stanza(t, vocab) for n, t in st.items()}, merged)
    report["wer"] = (wer_before, wer_after)

    # ---- stanzas Griffith refers to elsewhere or does not translate
    for (b, h), table in REPEATS.items():
        en, merged = english[(b, h)]
        for n, (h2, n2) in table.items():
            if not en.get(n) and english[(b, h2)][0].get(n2):
                en[n] = english[(b, h2)][0][n2]
                report["stanzas given from the hymn Griffith refers to"].append(f"{b}.{h}.{n} = {b}.{h2}.{n2}")
    for (b, h), entries in SPECIAL.items():
        en, merged = english[(b, h)]
        for first, last, text in entries:
            for n in [k for k in en if k >= first and (last is None or k <= last)]:
                if n != first and en[n]:
                    report["text dropped for a special entry"].append(f"{b}.{h}.{n}: {en[n][:60]}")
                del en[n]
            en[first] = text
            if last != first:
                merged[first] = last or 0
    return english, variants, hymns, books, vocab, report, ocr


def hymn_intros(books, b, idx):
    """{hymn: opening sentence of Griffith's notes}. The notes of a hymn are printed under its last
    verses, so its opening sentence stands after its heading and before the heading of the hymn
    after the next one; within that freedom the sentences are matched to the hymns in order,
    preferring those that share words with the hymn's title in the Index."""
    out = {}
    for o in "ab":
        hy = hymns_of_book(books[(o, b)], HYMNS[b])
        found = [(h, sent) for h in sorted(hy) for _, sent in note_intros(hy[h])]
        n, m = HYMNS[b], len(found)
        # DP over (hymn, sentence): best[i][k] = best score using hymns < i and sentences < k
        best = [[0.0] * (m + 1) for _ in range(n + 2)]
        back = {}
        for i in range(1, n + 1):
            for k in range(0, m + 1):
                opts = [(best[i - 1][k], (i - 1, k, None))]
                if k:
                    opts.append((best[i][k - 1], (i, k - 1, None)))
                    hk, sent = found[k - 1]
                    if hk in (i, i + 1):
                        sc = 1 + overlap(idx.get((b, i), ""), sent)[0]
                        opts.append((best[i - 1][k - 1] + sc, (i - 1, k - 1, i)))
                best[i][k], back[(i, k)] = max(opts, key=lambda x: x[0])
        i, k = n, m
        while i > 0 and (i, k) in back:
            pi, pk, h = back[(i, k)]
            if h is not None:
                out.setdefault(h, found[k - 1][1])
            i, k = pi, pk
    return out


RV_CACHE = {}


def rig_source(dharmic, sent, sa):
    """'From Rig Veda III.40' when the note names a Rig Veda hymn that the Sanskrit of the
    Atharva hymn really comes from (its first verse is found in that hymn)."""
    m = re.match(r"From Rig Veda ([IVXL]+)\.(\d+)", sent)
    if not m or not sa:
        return ""
    mandala, sukta = roman(m.group(1)), int(m.group(2))
    if not mandala or mandala > 10:
        return ""
    if mandala not in RV_CACHE:
        f = os.path.join(dharmic, "Rigveda", f"rigveda_mandala_{mandala}.json")
        RV_CACHE[mandala] = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []
    hymn = next((x for x in RV_CACHE[mandala] if x.get("sukta") == sukta), None)
    if not hymn:
        return ""
    def norm(t):
        return re.sub(r"[^\u0905-\u0939\u093e-\u094d]", "", ACCENT.sub("", t))
    rv = norm(hymn["text"])
    first = norm(sa[0])[:40]
    if len(first) >= 12 and difflib.SequenceMatcher(None, first, rv, autojunk=False).find_longest_match(
            0, len(first), 0, len(rv)).size >= 0.7 * len(first):
        return f"Rig Veda {m.group(1)}.{sukta}"
    return ""


def make_titles(books, english, variants, ocr, dharmic, ws, vocab, report):
    idx = read_titles(ocr, vocab)
    titles = {}
    for b in range(1, 21):
        intros = hymn_intros(books, b, idx)
        prev = ""
        for h in range(1, HYMNS[b] + 1):
            t = idx.get((b, h), "")
            if b == 1 and h in ws:  # Wikisource gives Griffith's titles from his Index
                t = ws[h][0][:1].upper() + ws[h][0][1:].replace("the waters", "the Waters")
            intro = intro_title(intros[h], vocab) if h in intros else ""
            bad = not t or any(not vocab.plausible(core(w)) for w in t.split() if core(w)) or len(t) < 8
            if b == 20 and (h <= 126 or h >= 137):
                text = " ".join(english[(b, h)][0].values())
                d = deity_of(text)
                sa = (variants[(b, h)] or [[]])[0]
                src = rig_source(dharmic, intro, sa)
                if h >= 137 and t and not bad:
                    pass
                else:
                    t = (f"To {d}" if d else "To Indra") + (f" (from {src})" if src else "")
            elif b == 15 and h > 1:
                t = "The glorification of the Vratya, continued"
            elif re.match(r"^(The same|On the same subject|A prayer for the same|Theame)\b", t) and prev:
                t = prev + (", continued" if "continued" in t else "")
            elif bad and intro and not intro.startswith("From") and (
                    not t or overlap(t, intro)[0] >= max(1, min(overlap(t, intro)[1:]) // 2)):
                report["title from the notes (Index garbled)"].append(f"{b}.{h}: {t!r} -> {intro!r}")
                t = intro
            t = TITLE_FIXES.get((b, h), t)
            t = ascii_names(t).replace("lovecharm", "love-charm")
            t = re.sub(r"\s+", " ", t).strip(" .,;:")
            t = t[:1].upper() + t[1:]
            if not t:
                t = f"Hymn {h}"
                report["no title"].append(f"{b}.{h}")
            titles[(b, h)] = shorten(t)
            prev = titles[(b, h)]
    return titles


def assemble(english, variants, titles, report):
    out = {}
    counts = {}
    for b in range(1, 21):
        secs = []
        for h in range(1, HYMNS[b] + 1):
            en, merged = english[(b, h)]
            empty = [n for n, t in en.items() if not t.strip()]
            for n in empty:
                del en[n]
            if empty:
                report["empty stanzas dropped"].append(f"{b}.{h}: {empty}")
            if not en:
                report["hymn without English"].append(f"{b}.{h}")
                en = {1: "[Griffith's English for this hymn could not be recovered from the scans.]"}
            pr = pair(en, merged, variants[(b, h)])
            verses = []
            if pr:
                rng, sa, how = pr
                if how == "renumbered":
                    report["paired one to one, Griffith's numbers differ"].append(f"{b}.{h}: {sorted(en)}")
                if sorted(en)[-1] < len(sa) or any(a != c for a, c in rng.values()):
                    report["stanzas paired with more than one verse"].append(
                        f"{b}.{h}: " + ", ".join(f"{n}->{a}-{c}" for n, (a, c) in sorted(rng.items()) if a != c))
                for n in sorted(en):
                    a, c = rng[n]
                    s_ = "\n".join(sa[a - 1:c])
                    verses.append({"n": a, "ref": f"{b}.{h}.{a}" + (f"-{c}" if c != a else ""),
                                   "sa": s_, "tr": iast(s_), "en": en[n]})
            else:
                ns = [len(v) for v in variants[(b, h)]] or [0]
                report["English only (verse numbers or lengths do not fit the Sanskrit)"].append(
                    f"{b}.{h}: Griffith {max(en)} stanzas ({len(en)} numbered), Sanskrit {'/'.join(map(str, ns))}")
                for n in sorted(en):
                    last = merged.get(n)
                    verses.append({"n": n, "ref": f"{b}.{h}.{n}" + (f"-{last}" if last and last != n else ""),
                                   "en": en[n]})
            secs.append({"label": titles[(b, h)], "short": f"{b}.{h}", "name": f"Hymn {h}",
                         "verses": verses})
        out[b] = {"sections": secs}
        counts[b] = len(secs)
    return out, counts


def suspicious(out, vocab):
    c = collections.Counter()
    for d in out.values():
        for s in d["sections"]:
            for v in s["verses"]:
                if v["en"].startswith("["):
                    continue
                for t in re.split(r"[\s\u2014]+", v["en"]):
                    w = re.sub(r"'s$", "", core(t))
                    if w and not vocab.known(w) and not vocab.known(w.rstrip("s")):
                        c[split_punct(t)[1]] += 1
    return c


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    english, variants, hymns, books, vocab, report, ocr = build(*sys.argv[1:5])
    titles = make_titles(books, english, variants, ocr, sys.argv[2], read_wikisource(sys.argv[3]), vocab, report)
    out, counts = assemble(english, variants, titles, report)
    for d in out.values():
        for sec in d["sections"]:
            sec["label"] = final_fix(sec["label"])
            for v in sec["verses"]:
                v["en"] = final_fix(v["en"])
    for b, d in out.items():
        print(f"atharvaveda/{b}.json", write(f"atharvaveda/{b}.json", d), "bytes,", counts[b], "hymns")
    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts", "index.json")
    index = json.load(open(index_path, encoding="utf-8"))
    index["atharvaveda"] = {"parts": [{"n": b, "name": f"Book {b}", "sub": AV_SUB[b], "count": counts[b]}
                                      for b in range(1, 21)]}
    print("index.json", write("index.json", index), "bytes")
    (wa, wb), (fe, fn) = (report["wer"][0]["a"], report["wer"][0]["b"]), report["wer"][1]
    print(f"word error rate on Book 1, hymns 1-18 (Wikisource): OCR a {wa[0] / wa[1]:.4f}, OCR b {wb[0] / wb[1]:.4f}, "
          f"both compared {fe / fn:.4f} ({fe} of {fn} words)")
    for k, v in report.items():
        if k != "wer":
            print(f"{k}: {len(v)}")
            for x in v:
                print("   ", x)
    sus = suspicious(out, vocab)
    print("suspicious tokens (not in the vocabulary):", sum(sus.values()), "in", len(sus), "kinds")
    print("   ", ", ".join(f"{w} {n}" for w, n in sus.most_common(80)))
    print({b: (AV_SUB[b], counts[b]) for b in range(1, 21)})


if __name__ == "__main__":
    main()
