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
        try:
            import wordfreq
            for w in wordfreq.top_n_list("en", 60000):
                if w.isalpha():
                    self.e[w] += int(wordfreq.zipf_frequency(w, "en") * 10)
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
        g, e = self.g.get(w, 0), self.e.get(w, 0)
        if "-" in w and not g:
            parts = [p for p in w.split("-") if p]
            if parts and all(self.known(p) for p in parts):
                return 2.0 + min(self.score(p) for p in parts) / 4
        if not g and not e:
            return 0.0
        return 1.0 + 1.6 * math.log1p(g) + 0.5 * math.log1p(e / 10)

    def known(self, w):
        return self.score(w) > 0


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


HEAD = re.compile(r"^[^A-Za-z0-9]{0,3}[HB]\s?[YVT¥]\s?[MN]\s?[MNH]\s?[.,']?\s*(.*)$")


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
        mm = re.match(r"^[^A-Za-z0-9]{0,2}([IVXLCHUl1]{1,7})\s*[.,]\s*$", t)
        if mm:
            return {v: c + 1 for v, c in roman_readings(mm.group(1)).items()}
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
        r = heading_readings(l, bare_ok=(book == 15)) if l else {}
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


SHORT_LEMMA = re.compile(r"^[\dlIS]{1,3}[.,]?\s+[\"'‘]?[A-Z][\w'’\-]*(\s[\w'’\-.]+){0,4}\s?[:;]\s")


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
            opts = [(sc - 0.9 * (v - u - 1) + 3 - cost, u) for u, (sc, _) in best.items() if u < v]
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


def fuse(A, B, vocab, pref="a", model=None):
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
                out += [choose(x, y, vocab, pref) for x, y in zip(a, b)]
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
        probe = verse_lines(other[h])[0]
        lines = verse_lines(hy[h - 1])
        j, r = first_line_match(lines[1:], probe)
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


def split_markers(toks):
    """{n: text} and {n: last} from a fused token list."""
    out, merged, n = {1: []}, {}, 1
    for t in toks:
        if t.startswith("\x00"):
            m = re.match(r"\x00(\d+)(?:-(\d+))?", t)
            v = int(m.group(1))
            if v <= n or v in out:
                continue
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
            t = re.sub(r"[A-Za-z]+", lambda m: m.group(0)[0] + m.group(0)[1:].lower(), t, count=1)
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
