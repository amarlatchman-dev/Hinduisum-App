#!/usr/bin/env python3
"""Build the White Yajurveda (Vajasaneyi Samhita, Madhyandina recension) in texts/yajurveda/.

Usage:
  pip install indic-transliteration wordfreq
  python3 scripts/build_yajurveda.py <griffith_1899_djvu_txt> <griffith_1927_djvu_txt> <dharmicdata_dir> [<rigveda_html_dir>]

  griffith_1899_djvu_txt  archive.org OCR (_djvu.txt) of Ralph T. H. Griffith, "The Texts of the White
                          Yajurveda", Benares 1899 (the Google scan)
  griffith_1927_djvu_txt  archive.org OCR of the second edition, 1927 (Digital Library of India
                          item 2015.126078): the same translation, set again, with other OCR errors
  dharmicdata_dir         https://github.com/bhavykhatri/DharmicData (Yajurveda/vajasneyi_madhyadina_samhita.json)
  rigveda_html_dir        optional: Wikisource pages of Griffith's Rig Veda (see build_vedas.py), only
                          used to widen the vocabulary of Griffith's spellings and names

Each printed page of Griffith's book has the verses at the top and his notes in smaller type below,
with running heads and page numbers around them. Both OCR texts are split into pages and paragraphs,
every paragraph is classed as verse or note (line length, the "N Lemma : gloss" pattern of the notes,
a word model, and for the 1927 text the overlap with the 1899 verses), and the verse paragraphs are cut
into verses by their numbers, which restart at 1 in every Book. The two readings of each Book are then
aligned word by word and, where they differ, the reading that is a real word in Griffith's vocabulary
is kept. The Sanskrit of each mantra is paired with the verse of the same number.
"""
import collections
import difflib
import json
import os
import re
import sys
import unicodedata

from indic_transliteration import sanscript

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_more_texts import ACCENTS, write  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

ORD = ("FIRST SECOND THIRD FOURTH FIFTH SIXTH SEVENTH EIGHTH NINTH TENTH ELEVENTH TWELFTH THIRTEENTH "
       "FOURTEENTH FIFTEENTH SIXTEENTH SEVENTEENTH EIGHTEENTH NINETEENTH TWENTIETH").split()
ORDINALS = ORD + [f"TWENTY-{o}" for o in ORD[:9]] + ["THIRTIETH"] + [f"THIRTY-{o}" for o in ORD[:9]] + ["FORTIETH"]


# --------------------------------------------------------------------------- pages and paragraphs
BOOK_HEADING = re.compile(r"(?i)^\W*\S{0,3}[o0()c]{1,3}k\s*t\S{1,2}\s*([a-z][a-z\-., ]+?)\W*$")


def book_starts(lines):
    """Line numbers of the 40 headings 'BOOK THE FIRST.' ... 'BOOK THE FORTIETH.' (OCR-garbled)."""
    out = []
    for i, l in enumerate(lines):
        s = l.strip()
        if len(out) == 40 or not 8 <= len(s) <= 40 or re.search(r"[\d\[\]]", s):
            continue
        m = BOOK_HEADING.match(s)
        if m and difflib.SequenceMatcher(None, m.group(1).upper().replace(" ", ""), ORDINALS[len(out)]).ratio() >= 0.6:
            out.append(i)
    assert len(out) == 40, f"found only {len(out)} Book headings"
    return out


def fuzzy_in(s, target, cut):
    """Best similarity of `target` to a window of `s` (both letters only)."""
    n, best = len(target), 0.0
    for i in range(0, max(1, len(s) - n + 3)):
        for w in (n - 2, n, n + 2):
            m = difflib.SequenceMatcher(None, s[i:i + w], target)
            if len(s[i:i + w]) >= n - 3 and m.real_quick_ratio() >= cut and m.quick_ratio() >= cut:
                best = max(best, m.ratio())
    return best


def furniture(line):
    """'head' for running heads ('2 THE TEXTS OF THE [BOOK I.', 'VERSE 11.] WHITE YAJURVEDA. 3' and
    their garbled forms) and page numbers, 'junk' for stray marks, None for text."""
    t = line.strip()
    letters = re.sub(r"[^A-Za-z]", "", t)
    if not letters:
        return "head" if re.fullmatch(r"\d{1,3}\W?", t) else "junk" if len(t) <= 12 else None
    if len(letters) <= 2 and len(t) <= 8 and not re.fullmatch(r"[\"'(]?[A-Za-z]{1,2}[.,;:!?)'\"]*", t):
        return "junk"
    if len(t) > 56:
        return None
    if len(letters) < 0.4 * len(t) and re.search(r"[■•«»]", t):
        return "junk"
    up = sum(c.isupper() for c in letters) / len(letters)
    caps = letters.upper()
    if ("[" in t or "{" in t or "\\" in t) and up > 0.5 and len(t) < 45:
        return "head"
    if re.search(r"[\[\]{\\]", t) and len(t) < 45 and up >= 0.3:
        return "head"  # 'n98 the texts of THE \\BOOK X.'
    if up > 0.5 or "]" in t:
        if fuzzy_in(caps, "WHITEYAJURVEDA", 0.6) >= 0.6 or fuzzy_in(caps, "TEXTSOFTHE", 0.65) >= 0.65:
            return "head"
    elif fuzzy_in(caps, "WHITEYAJURVEDA", 0.7) >= 0.72:
        return "head"
    if up >= 0.6 and re.search(r"\b[WM]\S{3,5}\s+\S{6,11}(\s+\S{1,3})?$", t) and re.search(r"[\d\]]", t):
        return "head"  # 'tBRSlS lOJ WSlTS YA^URVMBA. 261'
    if re.match(r"^\W?[A-Z\W\d]{4,9}\s?\d{1,2}\s?[.,:]?\s?['\\\])1}J]", t) and up > 0.7 and len(t) < 16:
        return "head"  # 'VERSE 47.]' on a line of its own
    return None


class Para:
    """A paragraph of the OCR text: its lines, whether a page break precedes it, and its class."""

    def __init__(self, lines, page_break):
        self.lines, self.page_break, self.verse = lines, page_break, None

    @property
    def text(self):
        return " ".join(self.lines)

    def width(self):
        """Longest line but the last (a paragraph's last line is usually short)."""
        lens = [len(l) for l in self.lines]
        return max(lens[:-1]) if len(lens) > 1 else lens[0]


def paragraphs(lines):
    out, cur, brk = [], [], False
    for l in lines:
        furn = furniture(l) if l.strip() else None
        if furn == "junk":
            continue
        if not l.strip() or furn:
            if cur:
                out.append(Para(cur, brk))
                cur, brk = [], False
            brk = brk or furn == "head"
            continue
        cur.append(re.sub(r"\s+", " ", l).strip())
    if cur:
        out.append(Para(cur, brk))
    return out


def read_books(path):
    """{book: [Para]} for one OCR text."""
    lines = open(path, encoding="utf-8").read().split("\n")
    starts = book_starts(lines)
    end = next(i for i in range(starts[-1], len(lines)) if re.search(r"INDEX OF H", lines[i].upper()))
    bounds = starts[1:] + [end]
    return {b + 1: paragraphs(lines[starts[b] + 1:bounds[b]]) for b in range(40)}


# --------------------------------------------------------------------------- verse or note?
LEMMA = re.compile(r"^[\dlIS]{1,3}[.,]?\s+\S[^:;.!?]{0,40}?\s?:\s")  # "2 Strainer of Vasu : cleanser"


NOTE_SIGNS = re.compile(r"\b(R\. ?V\.|A\. ?V\.|S\. ?B\. ?E|Taken from|Repeated from|Varied from|Cf\.|Mah[iíî]dhara|"
                        r"Eggeling|Weber|Sayana|according to|that is,|i\. ?e\.|literally|understood\.)")


def note_signs(p):
    """Notes quote the Rig Veda ('R. V. II. 14'), the commentators, and gloss one lemma after another."""
    lemmas = sum(lemma_score(l) <= -3 for l in p.lines[1:])
    return -2.5 * min(2, len(NOTE_SIGNS.findall(p.text))) - 2 * min(2, lemmas)


def lemma_score(line):
    """A note starts with the verse number and a short quotation from the verse, then ' : '."""
    m = LEMMA.match(line)
    if not m:
        return 0
    return -3 if len(m.group(0).split()) <= 6 else -1.5


def words(s):
    return re.findall(r"[a-z]+", s.lower())


def grams(s, n=3):
    w = words(s)
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


class WordModel:
    """Naive Bayes over words: the verses speak to gods ('thou', 'thee', 'homage'), the notes about
    the ritual ('Adhvaryu', 'Mahidhara', 'addresses', 'cf')."""

    def __init__(self, verse_texts, note_texts):
        self.cv = collections.Counter(w for t in verse_texts for w in words(t))
        self.cn = collections.Counter(w for t in note_texts for w in words(t))
        self.nv, self.nn = sum(self.cv.values()), sum(self.cn.values())
        self.size = len(set(self.cv) | set(self.cn))

    def score(self, text, clip=4.0):
        import math
        s = sum(math.log((self.cv[w] + 1) / (self.nv + self.size)) - math.log((self.cn[w] + 1) / (self.nn + self.size))
                for w in words(text))
        return max(-clip, min(clip, s))


def emission_1899(p, model):
    """Log-odds that a paragraph of the 1899 text is verse. Its notes are set much wider (68-80
    characters a line) than the verses (50-64)."""
    body = [len(l) for l in p.lines[:-1]] or [len(p.lines[0])]
    narrow = sum(w <= 63 for w in body) / len(body)
    wide = sum(w >= 67 for w in body) / len(body)
    if len(p.lines) > 1:
        e = 4 * (narrow - wide) + (0.5 if max(body) <= 61 else 0)
    else:
        e = 0.5 if body[0] <= 64 else -0.5 if body[0] <= 66 else -3
    e += lemma_score(p.lines[0]) + note_signs(p)
    return e + (0.35 * model.score(p.text, 3) if model else 0)


def split_mixed(paras):
    """The 1899 OCR sometimes runs verse lines and note lines into one paragraph: split it where
    narrow lines give way to wide ones (or the reverse)."""
    out = []
    for p in paras:
        kinds = ["n" if len(l) <= 63 else "w" if len(l) >= 67 else "m" for l in p.lines[:-1]]
        if kinds.count("n") >= 2 and kinds.count("w") >= 2:
            best, cut = 0, None
            for k in range(1, len(kinds)):
                a, b = kinds[:k], kinds[k:]
                s = max(a.count("n") - a.count("w") + b.count("w") - b.count("n"),
                        a.count("w") - a.count("n") + b.count("n") - b.count("w"))
                if s > best:
                    best, cut = s, k
            if cut and best >= len(kinds) - 1:
                out += [Para(p.lines[:cut], p.page_break), Para(p.lines[cut:], False)]
                continue
        out.append(p)
    return out


def emission_1927(p, model, ref):
    """The same for the 1927 text, whose notes are hardly wider than its verses: here the overlap
    with the verses and the notes read from the 1899 text decides."""
    e = 0.0
    g = grams(p.text) or grams(p.text, 2)
    if g:
        fv, fn = len(g & ref[0]) / len(g), len(g & ref[1]) / len(g)
        e += 8 * (fv - fn)
    e += lemma_score(p.lines[0]) + note_signs(p)
    if len(p.lines) > 1:
        e += 1 if p.width() <= 52 else -1.5 if p.width() >= 66 else 0
    return e + 0.35 * model.score(p.text, 3)


def viterbi(paras, emissions):
    """Label the paragraphs of a Book. On a page the verses come first and the notes after them,
    so a return from notes to verse costs little at a page break and much elsewhere."""
    NEG = -1e9
    score = {True: 1.0 + emissions[0] / 2, False: -1.0 - emissions[0] / 2}
    back = []
    for p, e in zip(paras[1:], emissions[1:]):
        nv_cost = -0.3 if p.page_break else -4.0
        sv = max((score[True], True), (score[False] + nv_cost, False))
        sn = max((score[False], False), (score[True] - 0.3, True))
        back.append({True: sv[1], False: sn[1]})
        score = {True: sv[0] + e / 2, False: sn[0] - e / 2}
    state = max(score, key=score.get)
    labels = [state]
    for b in reversed(back):
        state = b[state]
        labels.append(state)
    labels.reverse()
    for p, l, e in zip(paras, labels, emissions):
        p.verse, p.e = l, e
    return paras


def lead_number(line):
    """The verse number heading a line, if it is read exactly."""
    m = NUMBER_START.match(line)
    r = number_readings(m.group(1)) if m and lemma_score(line) > -3 else {}
    exact = [v for v, (c, _) in r.items() if c == 0]
    return exact[0] if len(exact) == 1 else None


def rescue(paras, max_width=99):
    """The last verse of a page is sometimes taken for the first note. The notes of a page run in
    the order of the verses, so a 'note' numbered k, just after verse k-1 or k-2, that is followed
    on its page by a note numbered k or less is the verse k (with any unnumbered paragraphs
    between them)."""
    seen = {1}
    for i, p in enumerate(paras):
        if p.verse:
            seen |= {n for n in map(lead_number, p.lines) if n}
        if p.verse or i == 0 or not paras[i - 1].verse:
            continue
        k = lead_number(p.lines[0])
        if not k or k in seen or not {k - 1, k - 2} & seen or p.width() > max_width:
            continue
        for j in range(i + 1, len(paras)):
            q = paras[j]
            if q.page_break:
                break
            if q.verse:  # verse again on the same page: the whole run was verse
                for r in paras[i:j]:
                    r.verse = True
                break
            m = re.match(r"^(\d{1,3})\b", q.lines[0])
            m = int(m.group(1)) if m else None
            if m:
                if m <= k:
                    paras[i].verse = True
                    for r in paras[i + 1:j]:
                        r.verse = r.e > -1  # the verse's own continuation, not an introduction
                break


def sandwiched(paras, strong_note):
    """A short run of 'notes' between two verse paragraphs of the same page is verse."""
    i, seen = 0, {1}
    while i < len(paras):
        if paras[i].verse or i == 0:
            seen |= {n for n in map(lead_number, paras[i].lines) if n}
            i += 1
            continue
        j = i
        while j < len(paras) and not paras[j].verse and not paras[j].page_break:
            j += 1
        m = NUMBER_START.match(paras[i].lines[0])
        expected = m and any(v - 1 in seen and c <= 1 for v, (c, _) in number_readings(m.group(1)).items())
        if (j < len(paras) and paras[j].verse and not paras[j].page_break and not paras[i].page_break
                and j - i <= 6 and not any(map(strong_note, paras[i:j]))
                and (expected or min(p.e for p in paras[i:j]) > -4)):
            for r in paras[i:j]:
                r.verse = True
        i = max(j, i + 1)


def demote(paras):
    """Two kinds of 'verse' that are notes: a last paragraph before the notes numbered well below
    the verses before it (the note on an earlier verse), and a lone unnumbered paragraph between
    notes."""
    top = 0
    for i, p in enumerate(paras):
        k = lead_number(p.lines[0])
        if p.verse and k:
            last = i + 1 == len(paras) or not paras[i + 1].verse or paras[i + 1].page_break
            if k <= top - 2 and len(str(k)) == len(str(top)) and last:
                p.verse = False
                continue
            if top < k <= top + 3:
                top = k
    for i in range(1, len(paras) - 1):
        p, a, b = paras[i], paras[i - 1], paras[i + 1]
        if p.verse and not a.verse and not b.verse and not p.page_break and not b.page_break \
                and not lead_number(p.lines[0]):
            p.verse = False


MODEL = None  # the word model of verse and notes, set by classify()
VOCAB = NAMER = None  # Griffith's vocabulary and names, set by main()


def classify(books_1899, books_1927):
    # 1899: bootstrap a word model from the paragraphs whose width leaves no doubt
    sure_v = [p.text for ps in books_1899.values() for p in ps
              if len(p.lines) > 2 and p.width() <= 60 and not LEMMA.match(p.lines[0])]
    sure_n = [p.text for ps in books_1899.values() for p in ps if len(p.lines) > 2 and p.width() >= 69]
    model = WordModel(sure_v, sure_n)
    for b in books_1899:
        books_1899[b] = split_mixed(books_1899[b])
    for ps in books_1899.values():
        viterbi(ps, [emission_1899(p, model) for p in ps])
        sandwiched(ps, lambda p: lemma_score(p.lines[0]) <= -3 or (len(p.lines) > 2 and p.width() >= 68))
        rescue(ps, 70)
        demote(ps)
    global MODEL
    model = MODEL = WordModel([p.text for ps in books_1899.values() for p in ps if p.verse],
                              [p.text for ps in books_1899.values() for p in ps if not p.verse])
    for b, ps in books_1927.items():
        ref = (set().union(*[grams(p.text) | grams(p.text, 2) for p in books_1899[b] if p.verse]),
               set().union(*[grams(p.text) | grams(p.text, 2) for p in books_1899[b] if not p.verse]))
        viterbi(ps, [emission_1927(p, model, ref) for p in ps])
        sandwiched(ps, lambda p: lemma_score(p.lines[0]) <= -3)
        rescue(ps)
        demote(ps)
    return model


# --------------------------------------------------------------------------- verses by number
# How the OCR misreads the verse numbers: letters and marks for digits, and digits for one another.
DIGIT_LIKE = {"l": "1", "I": "1", "i": "1", "|": "1", "!": "1", "]": "1", "[": "1", "t": "1", "o": "0", "O": "0",
              "Q": "0", "D": "0", "S": "58", "s": "58", "B": "8", "Z": "2", "z": "2", "g": "9", "?": "7",
              "T": "7", "€": "6", "b": "6", "J": "3"}
CONFUSED = {"0": "689", "1": "47", "2": "37", "3": "258", "4": "1", "5": "6389", "6": "5809", "7": "12",
            "8": "35609", "9": "580"}
NOT_NUMBERS = {"O", "o", "I", "A", "a", "i", "Lo", "So", "Is", "Ill", "Id"}
NUMBER_START = re.compile(r"^(\S{1,4}?|\d \d|\d{1,3}\s?[,—–-]?\s?\d{1,3})[.,:]?\s+(?=\W{0,2}[A-Za-z])")


def number_readings(tok, next_upper=True):
    """{value: (cost, span)} for the token heading a verse line: cost 0 if read exactly, 1 for a
    likely misreading, 1.5 for any other wrong, extra or unreadable digit, 2 for a dropped digit;
    span 1 for Griffith's '40, 41' (two verses given as one)."""
    tok = tok.strip()
    m = re.fullmatch(r"(\d{1,3})\s?[,—–-]?\s?(\d{1,3})", tok)
    if m and len(m.group(1)) + len(m.group(2)) > 2 and int(m.group(2)) == int(m.group(1)) + 1:
        return {int(m.group(1)): (0, 1)}
    tok = tok.replace(" ", "")
    if tok in NOT_NUMBERS or not any(c.isdigit() or c in DIGIT_LIKE for c in tok):
        return {}
    odd = [c for c in tok if not c.isdigit() and c not in DIGIT_LIKE]
    if (tok.isalpha() and len(tok) > 2) or len(odd) > 1 or (odd and not any(c.isdigit() for c in tok)):
        return {}
    exact = tok.isdigit()
    opts = [("", 0)]
    for c in tok:
        if c.isdigit():
            alts = [(c, 0)]
        elif c in DIGIT_LIKE:
            alts = [(a, 1) for a in DIGIT_LIKE[c]]
        else:  # a stray mark or letter: nothing, or an unreadable digit
            alts = [("", 1.5)] + [(a, 1.5) for a in "0123456789"]
        opts = [(o + a, max(k, ka)) for o, k in opts for a, ka in alts]
    out = {}

    def put(v, cost):
        if 0 < v < 200 and cost < out.get(v, (9,))[0]:
            out[v] = (cost, 0)
    for o, k in opts:
        if not o:
            continue
        put(int(o), k)
        for i, d in enumerate(o):
            for a in "0123456789":  # one digit misread
                if a != d:
                    put(int(o[:i] + a + o[i + 1:]), max(k, 1 if a in CONFUSED[d] else 1.5))
            if len(o) == 3:  # one digit too many: '710' for 71
                put(int(o[:i] + o[i + 1:]), max(k, 1.5))
        if len(o) == 1:  # a dropped digit: '1' for 10-19 or 21, 31 ...
            for a in "123456789":
                put(int(a + o), max(k, 2))
                put(int(o + a), max(k, 2))
    if not next_upper:  # '48 ever-moving' (its 'O' lost): accept only a plain number
        out = {v: (c + 1, sp) for v, (c, sp) in out.items() if exact and c == 0}
    return out


def assign_numbers(cands, top):
    """Choose the verse starts among the candidate lines: an increasing run of numbers 2..top,
    preferring exact readings and as few missing numbers as possible (DP over candidates)."""
    best = {1: (0.0, None)}  # last verse number covered -> (score, back pointer)
    for i, readings in enumerate(cands):
        new = {}
        for v, (cost, span) in readings.items():
            if v < 2 or v + span > top:
                continue
            opts = [(sc - 0.8 * (v - u - 1) + 3 - cost - 2 * max(0, v + span - max(u, top - 3)), u)
                    for u, (sc, _) in best.items() if u < v]
            if opts:
                sc, u = max(opts)
                end = v + span
                if sc > new.get(end, (-1e9,))[0] and sc > best.get(end, (-1e9,))[0]:
                    new[end] = (sc, (u, best[u][1], i, v))
        best.update(new)
    end = max(best, key=lambda k: best[k][0] - 0.8 * max(0, top - k))
    chosen, node = {}, best[end][1]
    while node:
        u, prev, i, v = node
        chosen[i] = v
        node = prev
    return chosen


def split_verses(paras, top):
    """{number: text} from the verse paragraphs of one Book, and {first: last} for verses that
    Griffith gives together."""
    lines = [l for p in paras if p.verse for l in p.lines]
    cands, idx = [], []
    for k, l in enumerate(lines):
        m = NUMBER_START.match(l)
        if m:
            nxt = re.sub(r"^\W+", "", l[m.end():])
            r = number_readings(m.group(1), nxt[:1].isupper())
            if r:
                cands.append(r)
                idx.append(k)
    chosen = assign_numbers(cands, top)
    starts = {idx[i]: v for i, v in chosen.items()}
    verses, merged, cost, n = {1: []}, {}, {1: 0}, 1
    for k, l in enumerate(lines):
        if k in starts:
            n = starts[k]
            cost[n], span = cands[idx.index(k)][n]
            if span:
                merged[n] = n + span
            verses[n] = []
            l = NUMBER_START.sub("", l, count=1)
        verses[n].append(l)
    return verses, merged, cost


# --------------------------------------------------------------------------- Sanskrit
DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
MARKER = re.compile(r"[॥।|]{1,2}\s*([०-९\d](?:\s{0,2}[०-९\d]){0,2})\s*[॥।|]{1,2}")


def sanskrit(dharmic):
    """{book: [Devanagari mantra, ...]} from DharmicData, without accents and verse numbers, and the
    places where the printed mantra number is not the running one."""
    data = json.load(open(os.path.join(dharmic, "Yajurveda", "vajasneyi_madhyadina_samhita.json"), encoding="utf-8"))
    out, odd = {}, []
    for rec in data:
        t = rec["text"].replace("ᳪ", "ं")  # the Yajurveda's gm̐, an anusvara
        t = re.sub(r"(?<=[\u0900-\u097F])[jk](?=[\u0900-\u097F\s])", "ं", t)  # typed for the same
        t = ACCENTS.sub("", t).replace("¬", "")
        t = re.sub(r"(?<=[\u0900-\u097F])\s*:", "ः", t)  # visarga typed as a colon
        t = re.sub(r"\s*[–—]\s*", "-", t)  # वने – वने: a repeated word
        t = re.sub(r"[।|]\s*[।|]", "॥", t)
        mantras, pos = [], 0
        for m in MARKER.finditer(t):
            printed = int(re.sub(r"\s", "", m.group(1)).translate(DEV_DIGITS))
            if printed != len(mantras) + 1:
                odd.append((rec["adhyaya"], len(mantras) + 1, printed))
            body = re.sub(r"\s*[|।]\s*", "। ", t[pos:m.start()].strip())
            body = re.sub(r"\s*॥\s*", "॥ ", body)
            mantras.append(re.sub(r"\s+", " ", body).strip(" ।॥") + "॥")
            pos = m.end()
        out[rec["adhyaya"]] = mantras
    return out, odd


def iast(dev):
    tr = sanscript.transliterate(re.sub(r"[।॥]", "", dev), sanscript.DEVANAGARI, sanscript.IAST).replace("~", "ṃ")
    return re.sub(r"[ \t]+", " ", tr).strip()


# --------------------------------------------------------------------------- vocabulary
WORD = re.compile(r"[A-Za-z]+(?:['’-][A-Za-z]+)*")
NON_ENGLISH = re.compile(r"[Ā-ɏḀ-ỿऀ-ॿ]")

# Names of the Yajurveda in the plain spelling of the app's Rig Veda (Griffith's diacritics dropped).
NAMES = """Agni Soma Indra Vishnu Savitar Pushan Asvins Asvin Sarasvati Sarasvan Brihaspati Prajapati Rudra
Rudras Matarisvan Visvakarman Aditi Adityas Aditya Gandharva Gandharvas Visvavasu Mitra Varuna Juhu Upabhrit
Dhruva Surya Ida Indrani Gharma Gayatra Gayatri Trishtup Jagati Anushtup Pankti Brihati Viraj Ushnih Vasus
Vasu Maruts Kapardin Yatudhanis Yatudhanas Bhava Sarva Pasupati Mahadeva Isana Narasamsa Tanunapat Vayu
Dyaus Prithivi Aryaman Bhaga Tvashtar Ribhus Vritra Angirases Angiras Atharvan Manu Purusha Hiranyagarbha
Svaha Svadha Vashat Agnidhra Ahavaniya Garhapatya Dakshina Adhvaryu Adhvaryus Hotar Brahman Udgatar
Prastara Mahavira Sautramani Asvamedha Rajasuya Vajapeya Agnihotra Yama Yami Nirriti Namuchi Kutsa Kanva
Vasishtha Visvamitra Jamadagni Kasyapa Bharadvaja Gotama Atri Dadhyach Dadhikravan Apam Napat Ahi Budhnya
Aja Ekapad Ila Sinivali Raka Kuhu Anumati Dhatar Vidhatar Pavamana Vaisvanara Jatavedas Narasamsa Usha Ushas
Ratri Apris Apri Sudra Vaisya Rajanya Kshatriya Brahmanaspati Indra-Agni Agni-Soma Mitra-Varuna Indra-Vayu
Kesin Sakvari Sakvaris Revati Revatis Mahanamni Mahanamnis Sama Samans Rathantara Brihat Vairupa Vairaja
Raivata Yajnayajniya Vamadevya Nidhana Ukthya Shodasin Atiratra Agnishtoma Svar Bhuh Bhuvah Om Amrit
Ghrita Sura Parisrut Kumbhi Ukha Ukhya Purishya Asandi Aupasana Kurus Panchalas Panchala Bharatas Bharata
Kamboja Gandharis Mujavat Mujavats Krishna Sita Arjuna Pururavas Urvasi Vena Tarkshya Nagnahu Masara
Dhishana Samudra Saramas Sarama Panis Asuras Asura Rakshas Rakshases Araru Trita Dvita Ekata Kesava
Visvayu Visvadhayas Bharati Hotra Mahi Varunani Agnayi Upamsu Antaryama Aindravayava Maitravaruna Sukra Manthin
Agrayana Ritu Aindragna Vaisvadeva Marutvatiya Mahendra Savitra Patnivata Hariyojana Pravargya Tarkshya
Arishtanemi Rathaprota Asamaratha Pramlochanti Anumlochanti Visvachi Ghritachi Menaka Sahajanya Purvachitti
Rathagritsa Rathaujas Senajit Sushena Punjikasthala Kratusthala Ugrasena Suryavarchas Apsarases Apsaras
Kavyavahana Nabhas Nabhasya Isha Urja Madhu Madhava Suchi Sahas Sahasya Tapas Tapasya Trivrit Panchadasa
Saptadasa Ekavimsa Trinava Trayastrimsa Chatushtoma Sakvara Ajya Prauga Nishkevalya Agnimaruta Amsa Daksha
Vala Sambara Bhrigus Bhrigu Navagvas Vivasvan Vivasvat Kakshivan Dirghatamas Nilagriva Sitikantha Girisa
Girisanta Rakshasas Rakshasa Yatudhana Yatudhanas Brahmanicide Kshatra Vaisvanara Uttaravedi Dhishnya
Dhishnyas Havirdhana Sadas Udumbara Asvattha Parna Khadira Palasa Vikankata Nyagrodha Salmali Darbha Kusa
Vrata Diksha Upasad Upasads Avabhritha Agnishvattas Barhishads Somavat Pitaras Manes Kavya Vena Gungu Subhadra
Kampila Ambika Ambalika Ambi Tryambaka Mujavant Sarvamedha Purushamedha Mahiman Brahmodya Isavasya
Saras Rishi Rishis Richas Sadhyas Sadhya Prana Sambhava Asambhava Sambhuti Asambhuti Vinasa Vidya Avidya Kakup Marka Tutha Svishtakrit Havishkrit Parivatsara Idvatsara Samvatsara Anuvatsara Idavatsara Dvipad Chatushpad Kulipaya""".split()


class Vocab:
    """Griffith's vocabulary: words counted in the app's other English texts (Griffith's Sama Veda
    and Rig Veda among them), with the word frequencies of `wordfreq` as a fallback."""

    def __init__(self, texts_dir, rigveda_html=None, ocr_texts=()):
        self.count = collections.Counter()
        self.caps = collections.Counter()  # capitalised words in Griffith's own Sama and Rig Veda
        self.pairs = collections.Counter()  # pairs of words in Griffith's own Sama and Rig Veda
        for path in self._json_files(texts_dir):
            griffith = os.sep + "samaveda" + os.sep in path
            for s in self._strings(json.load(open(path, encoding="utf-8"))):
                self._add(s, griffith)
        if rigveda_html and os.path.isdir(rigveda_html):
            for f in sorted(os.listdir(rigveda_html)):
                t = open(os.path.join(rigveda_html, f), encoding="utf-8").read()
                self._add(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", "", t, flags=re.S)), True)
        for n in NAMES:
            self.count[n.lower()] += 5
            self.caps[n] += 5
        # words that both OCR texts read alike, again and again, are real (mostly Griffith's Sanskrit terms)
        a, b = (collections.Counter(WORD.findall(t)) for t in ocr_texts) if ocr_texts else ({}, {})
        # (lower-case only: both scans garble a long vowel of a name alike, 'Prajdpati')
        self.agreed = {w for w in a if a[w] >= 2 and b.get(w, 0) >= 2 and len(w) > 2 and w.islower()}
        try:
            from wordfreq import zipf_frequency
            self.zipf = lambda w: zipf_frequency(w, "en")
        except ImportError:
            self.zipf = lambda w: 0.0

    @staticmethod
    def _json_files(texts_dir):
        for sub in ("samaveda", "rigveda", "mahabharata", "ramayana"):
            d = os.path.join(texts_dir, sub)
            for f in sorted(os.listdir(d)) if os.path.isdir(d) else []:
                yield os.path.join(d, f)

    def _strings(self, node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k not in ("sa", "tr"):
                    yield from self._strings(v)
        elif isinstance(node, list):
            for v in node:
                yield from self._strings(v)
        elif isinstance(node, str) and not NON_ENGLISH.search(node):
            yield node

    def _add(self, text, griffith=False):
        prev = None
        for w in WORD.findall(text.replace("’", "'")):
            self.count[w.lower()] += 1
            if griffith:
                if w[0].isupper():
                    self.caps[w] += 1
                if prev:
                    self.pairs[prev, w.lower()] += 1
                prev = w.lower()

    # misreadings of the letters of an English word ('hann' harm, 'disoerners', 'ju' in, 'tbe')
    CONFUSIONS = [("nn", "rm"), ("rn", "m"), ("m", "rn"), ("b", "h"), ("h", "b"), ("li", "h"), ("cl", "d"),
                  ("ii", "u"), ("tb", "th"), ("c", "e"), ("e", "c"), ("o", "c"), ("u", "n"), ("n", "u"),
                  ("f", "t"), ("t", "f"), ("l", "i"), ("i", "l"), ("a", "o"), ("o", "a"), ("j", "i"),
                  ("ju", "in"), ("y", "v"), ("v", "y"), ("s", "a"), ("r", "t"), ("t", "r"), ("e", "o")]

    def repair(self, w):
        """The common word one misread letter (or one stray letter) away from an unknown word."""
        low = w.lower()
        if len(low) < 2 or self.count[low] >= 2 or self.zipf(low) >= 2.5:
            return None
        cands, frontier = set(), {low}
        for _ in range(2):  # up to two misread letters ('beginuiug')
            new = set()
            for word in frontier:
                for a, b in self.CONFUSIONS:
                    i = word.find(a)
                    while i >= 0:
                        new.add(word[:i] + b + word[i + len(a):])
                        i = word.find(a, i + 1)
            cands |= new
            frontier = new
        if len(low) > 4:
            cands |= {low[:i] + low[i + 1:] for i in range(len(low))}
        scored = sorted(((self.count[c], c) for c in cands if self.count[c] >= 10), reverse=True)
        if not scored or len(scored) > 1 and scored[1][0] * 3 > scored[0][0]:
            return None
        best = scored[0][1]
        return best.capitalize() if w[0].isupper() else best

    def fits(self, prev, w, nxt):
        """How often Griffith has this word between these neighbours."""
        w = w.lower()
        return self.pairs[prev.lower(), w] + self.pairs[w, nxt.lower()] if prev or nxt else 0

    def score(self, w):
        """How surely `w` (letters, maybe with ' and -) is a real word of the text."""
        core = w.strip("'")
        if not core:
            return 0.0
        low = core.lower()
        base = re.sub(r"'s$", "", low)
        n = self.count[low] + (self.count[base] if base != low else 0)
        if n >= 3:
            return 3.0 + min(1.0, n / 1000)
        if "-" in core:
            parts = [self.score(p) for p in core.split("-") if p]
            return min(parts) - 0.5 if parts else 0.0
        z = self.zipf(base)
        zs = 2.5 if z >= 3 else 1.5 if z >= 1.5 else 0.5 if z > 0 else 0.0
        if n:
            return max(2.0, zs)
        for stem in (base[:-3], base[:-3] + "e", base[:-2], base[:-4]) if re.search(r"(est|eth|st)$", base) else ():
            if len(stem) > 2 and self.count[stem] >= 3:
                return 2.6  # Griffith's 'welcomest', 'sweeteneth'

        if core in self.agreed:
            return 2.5
        return zs

    def known(self, w):
        return self.score(w) >= 2.5


# --------------------------------------------------------------------------- tokens of one reading
SOFT = "­"  # a hyphen at a line end: a broken word or a compound, decided later
HOLE = "¿"  # a mark the OCR could not read, standing for '?' or '!'
PUNCT = set(".,;:!?\"'()—…-" + HOLE)
QUESTION = re.compile(r"(?i)^(who|whom|whose|what|which|where|whence|whither|when|why|how|is|are|art|hast|"
                      r"dost|didst|doth|hath|shall|will|can|wilt|canst)\b")


def verse_tokens(lines):
    """The words of one verse in one OCR reading, OCR marks cleaned, standalone punctuation
    attached to the word before it."""
    text = ""
    for l in lines:
        l = re.sub(r"^[\s■•«»*^~`]+", "", l).strip()
        if re.search(r"[A-Za-z]-$", text) and l[:1].isalpha():
            text = text[:-1] + SOFT + l
        else:
            text += " " + l
    text = text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"').replace("„", '"')
    text = re.sub(r"(?<=[A-Za-z])-\s(?=[a-z])", SOFT, text)  # 'God- devoted'
    text = re.sub(r"(?<=[A-Za-z])-\s(?=[A-Z])", "-", text)  # 'Agni- Soma'
    text = re.sub(r"(?<=[A-Za-z])[«»](?=[A-Za-z])", "-", text)  # 'Agni«Soma'
    text = re.sub(r"\s*(--|—|–)\s*", "— ", text)
    text = re.sub(r"\bSaras(\W?) (v[a-z!]{1,3})(?=\W|$)", "Sarasvati", text)  # 'Saras vati', a name broken in two
    toks, out = text.split(), []
    for i, t in enumerate(toks):
        nxt = toks[i + 1] if i + 1 < len(toks) else ""
        if t in ("0", "0,") :
            t = "O" + t[1:]
        prev_tok = out[-1] if out else ""
        if t in ("1", "I") and prev_tok[-1:] in ("!", "?"):
            continue  # 'things! I homage': the mark read twice
        if t == "1" and nxt[:1].islower() and not prev_tok[:1].isupper():
            t = "I"  # 'the earth 1 place thee'
        elif t == "I" and nxt[:1].isupper() and out and out[-1][-1:].isalpha():
            t = HOLE  # 'come I Havishkrit': a '!'

        elif t in ("1", "\\", "%", "t", "f", "l", "}", "]", "|", "1:", "?", "!") or re.fullmatch(r"[\\%]+", t):
            if not out and t not in ("?", "!"):
                continue
            t = HOLE if t not in ("?", "!") else t
        t = re.sub(r"^[*^■•«»~`]+|[*^■•«»~`]+$", "", t)
        if not t:
            continue
        if re.fullmatch(r"\.{1,}", t) and (out and out[-1] == "…" or nxt.startswith(".")):
            if not out or out[-1] != "…":
                out.append("…")
            continue
        if re.fullmatch(r"\d+[.,:;)]*", t) and not (out and re.fullmatch(
                r"\(?([IVXL]+[.,]?|verses?|Book|\d+[,—–-])", re.sub(r"[^\w.,—–-]", "", out[-1]), re.I)):
            continue  # a stray verse or page number, not a reference ('as in XIII. 25', 'verse 9')
        if all(c in PUNCT for c in t) and t != "…":
            if out:
                out[-1] += t
            continue
        if not re.search(r"[A-Za-z0-9…]", t):
            continue
        if re.search(r"[A-Za-z][&^$§*4]|[&^$§*][A-Za-z]", t):
            lead, core, trail = split_token(t)
            core = demark(core + re.match(r"[&^$§]*", trail).group(0), VOCAB) if VOCAB else core
            t = lead + core + re.sub(r"^[&^$§]+", "", trail)
        if not out and re.fullmatch(r"[A-Z]{3,}", re.sub(r"\W", "", t)) and len(toks) > 1:
            t = t[0] + t[1:].lower()  # 'PURUSHA hath': small capitals
        if re.fullmatch(r"[B-HJ-NP-Zb-hj-np-z][.,;:!?]?", t) or re.fullmatch(r"[IVXLl1]{1,4}\)", t):
            continue  # a stray letter ('G Thou', 'r This') or a misread number ('IX) Now')
        out.append(t)
    if out and out[-1] == "I" and len(out) > 1:
        out[-1] = HOLE  # 'and Adityas! I' at the end of a verse: a mark, not the pronoun
    return out


def split_token(t):
    m = re.match(r"^([^A-Za-z0-9]*)(.*?)([^A-Za-z0-9]*)$", t)
    return m.groups()


def key(t):
    if isinstance(t, tuple):  # a verse mark
        return "\x01"
    return re.sub(r"[^a-z0-9]", "", t.lower())


# --------------------------------------------------------------------------- fusion of the two readings
def odd_chars(core):
    return len(re.findall(r"[^A-Za-z'\-" + SOFT + "]", core)) + len(re.findall(r"[a-z][A-Z]", core))


def better_core(a, b, vocab, prev="", nxt=""):
    """Of two readings of a word, the one that is a word of Griffith's (or has fewer odd marks);
    between two real words, the one Griffith uses more often between the same neighbours."""
    if a == b or not b:
        return a
    if not a:
        return b
    if key(a) != key(b) and SOFT not in a + b and vocab.known(a) and vocab.known(b):
        fa, fb = vocab.fits(prev, a, nxt), vocab.fits(prev, b, nxt)
        if fa != fb:
            return a if fa > fb else b
    if key(a) == key(b):  # only case or hyphens differ: a hyphen in mid-line beats one at a line end
        if SOFT in a and SOFT not in b:
            return b
        return a
    sa = vocab.score(a.replace(SOFT, "")) - odd_chars(a)
    sb = vocab.score(b.replace(SOFT, "")) - odd_chars(b)
    if a[:1].isupper() and b[:1].isalpha() and NAMER and a not in NAMER.names and b not in NAMER.names:
        ma, mb = NAMER.mend(a), NAMER.mend(b)  # 'Bharas' and 'Bbavas': Bhavas
        if (ma or mb) and ma != a:
            return ma or mb
    if NAMER and (a in NAMER.names or b in NAMER.names):
        return a if a in NAMER.names else b
    if sa < 1.5 and sb < 1.5:  # neither is a word: one may be a letter away from one
        ra, rb = vocab.repair(re.sub(r"[^A-Za-z]", "", a)), vocab.repair(re.sub(r"[^A-Za-z]", "", b))
        if ra or rb:
            return ra or rb
    if SOFT in a or SOFT in b:  # a word broken at a line end: score the parts joined or hyphenated
        sa = max(sa, vocab.score(a.replace(SOFT, "-")) - odd_chars(a))
        sb = max(sb, vocab.score(b.replace(SOFT, "-")) - odd_chars(b))
    return b if sb > sa else a


def better_punct(a, b):
    if a == b or not b:
        return a
    if not a:
        return b
    good = lambda p: all(c in ".,;:!?\"'()—…-" for c in p)  # noqa: E731
    if good(a) != good(b):
        return a if good(a) else b
    if HOLE in a and HOLE not in b:
        return b
    return a


def better_punct_pair(a, b):
    """A quotation mark that only one reading has is a speck: Griffith's verses hardly quote."""
    if not a and re.fullmatch(r"['\"]+", b) or not b and re.fullmatch(r"['\"]+", a):
        return ""
    return better_punct(a, b)


NO_STOP = {"a", "an", "the", "to", "of", "and", "with", "for", "by", "in", "on", "at", "from", "my", "thy", "our",
           "your", "his", "her", "its", "their", "o", "unto", "into", "upon", "art", "be", "is"}


def choose(a, b, vocab, stats, prev="", nxt=""):
    """One word from the two readings a (1899) and b (1927), either of which may be None."""
    if b is None or a == b:
        return a
    if a is None:
        return b
    la, ca, ta = split_token(a)
    lb, cb, tb = split_token(b)
    core = better_core(ca, cb, vocab, re.sub(r"\W", "", prev or ""), re.sub(r"\W", "", nxt or ""))
    if key(ca) != key(cb):
        stats["fused"] += 1
    trail = better_punct_pair(ta, tb)
    if {ta, tb} == {".", ","} and (nxt or "")[:1].islower():
        trail = ","  # 'One. only doing Karma'
    if core.lower() in NO_STOP and not (ta and tb) and trail in (".", ","):
        trail = ""  # 'agreeable to. Agni', 'A, wooden stone'
    lead = better_punct_pair(la, lb)
    return (lead if re.fullmatch(r"[\"'(]*", lead) else "") + core + trail


def similarity(a, b):
    ka, kb = key(a), key(b)
    if ka == kb:
        return 1.0 if ka else 0.5
    if not ka or not kb or ka == "\x01" or kb == "\x01":
        return 0.0
    ga, gb = {ka[i:i + 2] for i in range(len(ka) - 1)} or {ka}, {kb[i:i + 2] for i in range(len(kb) - 1)} or {kb}
    dice = 2 * len(ga & gb) / (len(ga) + len(gb))
    if min(len(ka), len(kb)) <= 5:  # 'Oue' for 'One'
        dice = max(dice, difflib.SequenceMatcher(None, ka, kb).ratio())
    return dice


def align_tokens(xs, ys):
    """Needleman-Wunsch pairing of two token runs by similarity."""
    n, m = len(xs), len(ys)
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    sim = [[similarity(x, y) - 0.4 for y in ys] for x in xs]
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0 or j == 0:
                dp[i][j] = -0.2 * (i + j)
            else:
                dp[i][j] = max(dp[i - 1][j - 1] + sim[i - 1][j - 1], dp[i - 1][j] - 0.2, dp[i][j - 1] - 0.2)
    out, i, j = [], n, m
    while i or j:
        if i and j and dp[i][j] == dp[i - 1][j - 1] + sim[i - 1][j - 1]:
            out.append((xs[i - 1], ys[j - 1]))
            i, j = i - 1, j - 1
        elif i and (not j or dp[i][j] == dp[i - 1][j] - 0.2):
            out.append((xs[i - 1], None))
            i -= 1
        else:
            out.append((None, ys[j - 1]))
            j -= 1
    return out[::-1]


def align_book(seq_a, seq_b, n=5):
    """Pair the tokens of two readings of a Book. Runs of n words that occur once in each reading
    anchor the alignment (the longest chain of them in the same order, as in a patience diff);
    between anchors a Needleman-Wunsch alignment keeps repeated formulas ('For Makha thee, thee
    for the head of Makha!') in step."""
    import bisect
    ka, kb = [key(t) for t in seq_a], [key(t) for t in seq_b]

    def positions(k):
        d = collections.defaultdict(list)
        for i in range(len(k) - n + 1):
            g = tuple(k[i:i + n])
            if all(g) and "\x01" not in g:
                d[g].append(i)
        return d
    pa, pb = positions(ka), positions(kb)
    points = sorted((pa[g][0], pb[g][0]) for g in pa if len(pa[g]) == 1 and len(pb.get(g, ())) == 1)
    # longest chain increasing in both readings
    tails, tail_idx, prev = [], [], [None] * len(points)
    for k, (i, j) in enumerate(points):
        x = bisect.bisect_left(tails, j)
        if x == len(tails):
            tails.append(j)
            tail_idx.append(k)
        else:
            tails[x], tail_idx[x] = j, k
        prev[k] = tail_idx[x - 1] if x else None
    chain, k = [], tail_idx[-1] if tail_idx else None
    while k is not None:
        chain.append(points[k])
        k = prev[k]
    chain.reverse()
    pairs, pi, pj = [], 0, 0
    for i, j in chain + [(len(ka), len(kb))]:
        if i < pi or j < pj:
            continue
        pairs += align_tokens(seq_a[pi:i], seq_b[pj:j])
        size = n if i < len(ka) else 0
        pairs += list(zip(seq_a[i:i + size], seq_b[j:j + size]))
        pi, pj = i + size, j + size
    return pairs


TWO_LETTER = {"of", "to", "in", "on", "at", "by", "be", "he", "me", "we", "ye", "my", "so", "no", "or", "an", "as", "is",
              "it", "us", "up", "do", "go", "lo", "oh", "if"}


def whole_word(t):
    core = split_token(t)[1].replace(SOFT, "")
    return VOCAB.known(core) and (len(core) > 2 or core.lower() in TWO_LETTER or core in ("O", "I", "A", "a"))


def join_split_words(pairs):
    """'thy self' read against 'thyself': pair the two halves with the whole word. The 1899
    division is kept ('thyself', 'for sake of') unless it breaks a word ('wor ship', 'th ine') or
    joins two at a line end ('have-strength')."""
    out, k = [], 0
    word = lambda t: t is not None and not isinstance(t, tuple) and key(t)  # noqa: E731
    while k < len(pairs):
        if k + 1 < len(pairs):
            (a1, b1), (a2, b2) = pairs[k], pairs[k + 1]
            for whole, x, y, a_whole in ((a2, b1, b2, True) if a1 is None else (None,) * 4,
                                         (a1, b1, b2, True) if a2 is None else (None,) * 4,
                                         (b2, a1, a2, False) if b1 is None else (None,) * 4,
                                         (b1, a1, a2, False) if b2 is None else (None,) * 4):
                if whole is None or not (word(whole) and word(x) and word(y)) or key(x) + key(y) != key(whole):
                    continue
                parts_ok = whole_word(x) and whole_word(y)
                if a_whole:
                    split = SOFT in whole and parts_ok
                else:
                    split = parts_ok or not whole_word(whole)
                out += [(x, x), (y, y)] if split else [(whole, whole)]
                k += 2
                break
            else:
                out.append(pairs[k])
                k += 1
            continue
        out.append(pairs[k])
        k += 1
    return out


def keep_one_sided(run, at_start, vocab, other_notes):
    """Words read by one OCR only: a word the other dropped, junk, a verse the other took for a
    note, or a line of notes this one took for verse."""
    words = [t for t in run if key(t)]
    if not words:
        return [t for t in run if "…" in t]
    if len(words) <= 3:
        return [t for t in run if not key(t) or vocab.score(split_token(t)[1].replace(SOFT, "")) >= 2.5
                or split_token(t)[1] in ("O", "I")]
    known = sum(vocab.score(split_token(t)[1].replace(SOFT, "")) >= 2.5 for t in words)
    if known < 0.6 * len(words):
        return []
    text = " ".join(words)
    if len(words) > 15 and (MODEL.score(text, 8) < -4 or len(NOTE_SIGNS.findall(text)) >= 2):
        return []  # a long stretch of notes ('Cf. the creation-myth of the world-giant Ymir ...')
    g = grams(" ".join(words))
    in_notes = g and len(g & other_notes) > 0.5 * len(g)
    if in_notes and MODEL.score(" ".join(words), 6) < (-2 if at_start else 0):
        return []  # notes that this reading took for verse
    return run


def fuse_book(va, vb, vocab, notes_a, notes_b, stats, log=None, limit=999):
    """Fuse the verses of a Book read from the two OCR texts: {n: (tokens, cost of the number)} each.
    Verse marks are aligned like words; where the readings disagree on a number, the run of
    numbers that is most nearly 1, 2, 3 ... wins."""
    seq_a = [t for n in sorted(va) for t in [("\x01", n, va[n][1])] + va[n][0]]
    seq_b = [t for n in sorted(vb) for t in [("\x01", n, vb[n][1])] + vb[n][0]]
    pairs = align_book(seq_a, seq_b)
    mark = lambda t: isinstance(t, tuple)  # noqa: E731
    pairs = join_split_words(pairs)
    stream, k = [], 0  # words, and candidate verse marks as (n, score)
    while k < len(pairs):
        a, b = pairs[k]
        if mark(a) or mark(b):
            ms = [t for t in (a, b) if mark(t)]
            agree = len(ms) == 2 and ms[0][1] == ms[1][1]
            stream.append(("mark", {t[1]: 3 - t[2] + (1.5 if agree else 0) for t in ms}))
            k += 1
            continue
        if a is not None and b is not None:
            prev = next((v for kind, v in reversed(stream) if kind == "word"), "")
            nxt = next((x for x in (pairs[k + 1] if k + 1 < len(pairs) else (None, None)) if isinstance(x, str)), "")
            stream.append(("word", choose(a, b, vocab, stats, prev, nxt)))
            k += 1
            continue
        side = 0 if b is None else 1
        at_start = bool(stream) and stream[-1][0] == "mark"
        run = []
        while k < len(pairs) and pairs[k][1 - side] is None and not mark(pairs[k][side]):
            run.append(pairs[k][side])
            k += 1
        kept = keep_one_sided(run, at_start, vocab, notes_b if side == 0 else notes_a)
        stats["one_sided_kept" if kept else "one_sided_dropped"] += len(run)
        if log is not None and len([t for t in run if key(t)]) > 3:
            log.append(("AB"[side], at_start, bool(kept), " ".join(run)))
        stream += [("word", t) for t in kept]
    # choose the verse marks: increasing numbers, as few gaps as possible (as in assign_numbers)
    marks = [(i, opts) for i, (kind, opts) in enumerate(stream) if kind == "mark"]
    best = {0: (0.0, None)}
    for mi, (i, opts) in enumerate(marks):
        new = {}
        opts = dict(opts)
        for u in list(best):  # a verse mark read with another number may be the next verse
            opts.setdefault(u + 1, 1.0)
        for n, sc in opts.items():
            cands = [(s0 - 0.8 * (n - u - 1) + sc - 2 * max(0, n - max(u, limit)), u) for u, (s0, _) in best.items() if u < n]
            if cands:
                s1, u = max(cands)
                if s1 > new.get(n, (-1e9,))[0] and s1 > best.get(n, (-1e9,))[0]:
                    new[n] = (s1, (u, best[u][1], mi))
        best.update(new)
    n = max(best, key=lambda u: best[u][0])
    chosen, node = {}, best[n][1]
    while node:
        u, prev, mi = node
        chosen[marks[mi][0]] = n
        n, node = u, prev
    verses, n = {}, None
    for i, (kind, val) in enumerate(stream):
        if i in chosen:
            n = chosen[i]
            verses[n] = []
        elif kind == "word" and n is not None:
            verses[n].append(val)
    return verses


# --------------------------------------------------------------------------- the finished English
class Namer:
    """Sanskrit names whose diacritics the OCR garbled ('Mataiisvan', 'MSiari§van', 'Pfishan'),
    mended to the closest name in Griffith's plain spelling when that is clear."""

    def __init__(self, vocab):
        names = {w for w, c in vocab.caps.items()  # words Griffith writes with a capital, not English ones
                 if c >= 2 and len(w) >= 4 and w[1:].islower() and vocab.zipf(w.lower()) < 2.5
                 and c >= 0.8 * vocab.count[w.lower()]}
        names |= {n for n in NAMES if "-" not in n}
        names |= {n + "s" for n in names if not n.endswith("s")}  # 'Sarvas', 'Bhavas'
        self.names = names
        self.by_len = collections.defaultdict(list)
        for n in names:
            self.by_len[len(n)].append(n)

    # letters the OCR reads for a vowel with a macron ('Pdshan', 'Prajipati', 'Mataiisvan')
    GARBLE = {("d", "u"), ("i", "a"), ("i", "u"), ("l", "a"), ("t", "i"), ("f", "u"), ("i", "r"), ("y", "r"),
              ("k", "a"), ("o", "n"), ("u", "n"), ("s", "a"), ("h", "a"), ("e", "a"), ("j", "a"), ("l", "i")}
    GARBLE_SEQ = [("ii", "u"), ("fi", "u"), ("il", "u"), ("il", "a"), ("ll", "a"), ("sl", "a"), ("ft", "a"), ("ij", "n"),
                  ("ri", "n"), ("rl", "n"), ("pj", "n")]

    def mend(self, core):
        base, suffix = (core[:-2], "'s") if core.endswith("'s") else (core, "")
        if len(base) < 4:
            return None
        low = (base[0] + "".join(c if c.islower() and c != WILD else "?" for c in base[1:])).lower()  # 'SArya': s?rya
        variants = {low} | {low.replace(a, b, 1) for a, b in self.GARBLE_SEQ if a in low}
        best = {}
        for v in variants:
            for ln in range(len(v) - 1, len(v) + 2):
                for n in self.by_len.get(ln, ()):
                    r = difflib.SequenceMatcher(None, v, n.lower()).ratio()
                    if ln == len(v):  # a mark or a wrong letter in place of a long vowel: 'A$vins', 'Pdshan'
                        w = [1 if a == b else 0.8 if not a.isalpha() else 0.6 if (a, b) in self.GARBLE
                             or (i == 0 and (a, b) == ("y", "v")) else 0 for i, (a, b) in enumerate(zip(v, n.lower()))]
                        if sum(x > 0 for x in w) >= 0.8 * ln:
                            r = max(r, sum(w) / ln)
                    r += 0.03 if n in NAMES else 0
                    if r >= 0.7 and r > best.get(n, 0):
                        best[n] = r
        scored = sorted(((r, n) for n, r in best.items()), reverse=True)
        if scored and scored[0][0] >= (0.8 if len(base) < 7 else 0.75) and \
                (len(scored) == 1 or scored[1][0] < scored[0][0] - 0.05 or scored[1][1] == scored[0][1]
                 or scored[0][1] in NAMES and scored[1][1] not in NAMES):
            return scored[0][1] + suffix
        return None


# Garbles that survive both readings, found in the list of words outside the vocabulary that
# this script prints, and mended here by hand: (pattern, replacement), applied to the finished text.
FIXES = [
    (r"\bAll-?hail\b", "All-hail"), (r"\bAllhail\b", "All-hail"),
    (r"\bSv[^\sdh]{0,2}h[^\s\w]?(?=[\s!?.,;:]|$)", "Svaha"), (r"\bSv[a-z^&4]{0,2}dh[^\s\w]?(?=[\s!?.,;:]|$)", "Svadha"),
    (r"\bSvadh(?=[\s!?.,;:]|$)", "Svadha"), (r"\bSvah(?=[\s!?.,;:]|$)", "Svaha"),
    (r"\bCrja\b", "Urja"), (r"\bishi\b", "Rishi"), (r"\bB\^ishi's", "Rishi's"),
    (r"\bSaras,? vat[it]?\b", "Sarasvati"), (r"\bSaras vatt\b", "Sarasvati"), (r"\bSarasvat\b(?!-)", "Sarasvati"),
    (r"\bSaras\?", "Sarasvati,"), (r"\bId[\\£(]+(?=[\s,.;:!?])", "Ida"), (r"\bVisfedevas\b", "Visvedevas"),
    (r"\boma juice", "Soma juice"), (r"\bhann us not\b", "harm us not"), (r"\bju thy hands\b", "in thy hands"),
    (r"\byou who he and\b", "you who lie and"), (r"\ban to thy bow", "and to thy bow"), (r"\bwear% ", "wears "),
    (r"\barva and to Pasupati", "Sarva and to Pasupati"), (r"\bPufijishtbas\b", "Punjishthas"), (r"Lord of the fied Steeds", "Lord of the Red Steeds"), (r"\beta\b", "etc."),
    (r"\bono-thoughted\b", "one-thoughted"), (r"\b(Brihati|Jagati)! metre", r"\1 metre"),
]


WILD = "ª"  # a letter the OCR could not read (a letter, for the tokenizer)


def demark(core, vocab):
    """Odd marks inside a word: a letter with a diacritic ('Svah&', 'S&man's', 'A$vins') or a
    hyphen, apostrophe or space the OCR misread ('Soma*bringing', 'ne*er', 'and^with')."""
    m = re.fullmatch(r"([A-Za-z]+)[*^«]([A-Za-z']+)", core)
    if m:
        a, b = m.groups()
        if a.lower() in ("ne", "o", "e"):
            return a + "'" + b
        a, b = vocab.repair(a) or a, vocab.repair(b) or b  # 'bair*tufts'
        if vocab.known(a) and vocab.known(b) and len(b) > 1:
            return a + ("-" if a[0].isupper() or b[0].isupper() else " ") + b
    core = re.sub(r"(?<=[a-z])[*^]s$", "'s", core)  # 'Sacrificer^s'
    mapped = re.sub(r"[$§]", "s", core)
    plain = re.sub(r"(?<=[A-Za-z])[&^4]|[&^4](?=[a-z])", "a", mapped)
    if vocab.known(plain) or NAMER and plain in NAMER.names:
        return plain
    return re.sub(r"(?<=[A-Za-z])[&^4]|[&^4](?=[a-z])", WILD, mapped)  # a long vowel: let the names decide


# Places in Books 31 and 40 (read in full) where both scans fail, mended from the sense of the
# verse and the Sanskrit: {book: [(pattern, replacement)]}.
BOOK_FIXES = {
    31: [(r"\bBichas\b", "Richas"), (r"\bPrdj\b", "Prana"), (r"\bSalhyat\b", "Sadhyas"),
         (r"east be beyond", "east beyond"), (r"When the divided Purusha", "When they divided Purusha"),
         (r"\bVisvakarmans essence", "Visvakarman's essence"), (r"\bSadhya, Gods of old", "Sadhyas, Gods of old")],
    40: [(r"sink to dirk darkness", "sink to darkness"), (r"\bAsambhati's\b", "Asambhuti's"),
         (r"\bSombhikti\b", "Sambhuti"), (r"from Sambara, another from Sambhava", "from Sambhava, another from Asambhava"),
         (r"^The mail who knows .*endless life\.$",
          "The man who knows Sambhuti and Vinasa simultaneously, He, by Vinasa passing death, gains by Sambhuti endless life."),
         (r"Nescience\. I Thus", "Nescience. Thus"), (r"clearly knows\. Self", "clearly knows, Self"), (r"lead as to riches", "lead us to riches")],
}


def finish(tokens, vocab, namer, stats):
    """Tokens of a fused verse to clean text."""
    out = []
    for t in tokens:
        lead, core, trail = split_token(t)
        if SOFT in core:  # a line-end hyphen: one word, or a compound?
            parts = core.split(SOFT)
            joined, hyph = "".join(parts), "-".join(parts)
            if vocab.known(joined) and not (parts[-1][:1].isupper()):
                core = joined
            elif vocab.known(hyph) or parts[-1][:1].isupper() or \
                    all(vocab.score(p) >= 2.5 and len(p) >= 3 for p in parts):
                core = hyph
            else:
                core = joined
        if trail.startswith("!") and core + "i" in NAMES:
            core, trail = core + "i", trail[1:]  # 'Sarasvat!': the long i read as '!'
        if re.search(r"[A-Za-z][&^$§4*]|[&^$§*][A-Za-z]", trail[:1] + core + lead[-1:]):
            core = demark(core + re.match(r"[&^$§4]*", trail).group(0), vocab)
            trail = re.sub(r"^[&^$§4]+", "", trail)
        garbled = re.search(r"[A-Za-z][A-Z][a-z]|[^A-Za-z'\-" + SOFT + " ]", core)
        if core and (garbled or not vocab.known(core.replace("-", "")) and not vocab.known(core)):
            plain = re.sub(r"[^A-Za-z'\-]", "", core)
            if plain != core and vocab.known(plain):
                core = plain  # 'tha^t'
            elif core[:1].isupper() or not core[:1].isalpha():
                fixed = namer.mend(core)
                if fixed:
                    stats["names"] += 1
                    core = fixed
            if core[:1].islower() and "-" not in core and vocab.score(core) < 1.5:
                fixed = vocab.repair(core)
                if fixed:
                    stats["spelling"] += 1
                    core = fixed
        out.append(lead + core + trail)
    text = " ".join(out)
    # a mark standing for '?' or '!': a question if the sentence opens with a question word
    while HOLE in text:
        i = text.index(HOLE)
        after, before = text[i + 1:].lstrip(), text[:i].rstrip().split(" ")[-1]
        if after[:1].islower() and before[:1].islower():
            text = text[:i] + text[i + 1:]  # a speck in mid-sentence ('in a place? remote')
            continue
        start = max(text.rfind(". ", 0, i), text.rfind("! ", 0, i), text.rfind("? ", 0, i))
        text = text[:i] + ("?" if QUESTION.match(text[start + 2 if start >= 0 else 0:]) else "!") + text[i + 1:]
    text = text.replace(WILD, "a")
    if text.count("(") != text.count(")"):  # a lone bracket is a speck
        text = text.replace("(", "").replace(")", "")
    for pat, rep in FIXES:
        text, n = re.subn(pat, rep, text)
        stats["table"] += n
    text = re.sub(r"(?<=[.!?,;:])[\s—\-.\d^|]*[—-]{2}[\s—\-.\d^|]*(?=\s|$)", " ", text)  # '!—--——-.1'
    text = re.sub(r"(?<=[a-z])\?(?= [a-z])", "", text)  # 'in a place? remote'
    text = re.sub(r"(?<=[a-z])(?<!etc)\.(?= [a-z])", "", text)  # 'him who. sees'
    text = re.sub(r"(?<=\w) -(?=\w)", "-", text)  # 'self -existent'
    text = re.sub(r"(?<=[!?.]) …", "", text)
    text = re.sub(r"([!?]) I ([a-z])", lambda m: f"{m.group(1)} {m.group(2).upper()}", text)  # 'things! I homage'
    text = re.sub(r"(?<=[a-z])A(?=\b|'s)", "a", text)  # 'PratimA', 'DikshA's'
    text = re.sub(r"(?<=\w)-(?=[\s,.;:!?]|$)", "", text)  # 'unsteady.-'
    text = re.sub(r"\s-\s", " ", text)
    text = re.sub(r"\s*—\s*", "—", text)
    text = re.sub(r"\s+([,;:.!?)])", r"\1", text)
    text = re.sub(r"([,;:!?])(?=[A-Za-z])", r"\1 ", text)
    text = re.sub(r"([,;:.!?])\1+", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:1].upper() + text[1:]


def suspicious_words(text, vocab, counter):
    """Words of the finished text that are neither in the vocabulary nor common English."""
    for w in WORD.findall(text):
        if vocab.score(w) < 1.5 and not all(vocab.score(p) >= 1.5 for p in w.split("-")):
            counter[w] += 1
    for w in re.findall(r"\S*[^\sA-Za-z0-9,.;:!?'\"()—…-]\S*", text):  # odd marks left in a word
        counter[w] += 1


# --------------------------------------------------------------------------- Books
BOOK_NAMES = {  # after Griffith's CONTENTS
    1: "New and Full Moon sacrifices",
    2: "New and Full Moon rites; offerings to the Fathers",
    3: "The sacred fires, Agnihotra and the Four-monthly rites",
    4: "The Soma sacrifice: consecration and purchase of Soma",
    5: "Soma's reception, the altar and the Soma sheds",
    6: "The sacrificial stake and victim; the Soma pressing",
    7: "The cups of Soma at the morning and midday pressings",
    8: "The evening pressing, the purifying bath and Soma rites",
    9: "The Vajapeya (draught of strength) and the Rajasuya",
    10: "The king's consecration (Rajasuya concluded)",
    11: "Building the fire altar: the fire-pan of clay",
    12: "The fire altar: the Garhapatya hearth and the Plants",
    13: "The fire altar: the first layer of bricks",
    14: "The fire altar: the second, third and fourth layers",
    15: "The fire altar: the fifth layer",
    16: "The Satarudriya, homage to Rudra",
    17: "The completed fire altar; prayers to Agni and Indra",
    18: "Agni's consecration as king; the Stream of Riches",
    19: "The Sautramani; offerings to the Fathers",
    20: "The Sautramani continued: the Sacrificer's blessing",
    21: "The Sautramani concluded: prayers to Varuna and Indra",
    22: "The Asvamedha, or Horse Sacrifice",
    23: "The Horse Sacrifice continued; the priests' riddles",
    24: "The victims of the Horse Sacrifice enumerated",
    25: "The Horse Sacrifice concluded; eulogy of the Horse",
    26: "Supplementary texts for various sacrifices",
    27: "Supplementary texts and formulas continued",
    28: "Supplementary texts of the Sautramani",
    29: "Supplementary texts of the Horse Sacrifice",
    30: "The Purushamedha, or Human Sacrifice",
    31: "The Purushasukta, hymn of the Cosmic Person",
    32: "The Sarvamedha; prayer for wisdom and glory",
    33: "The Sarvamedha continued; praise of Agni, Indra, Surya",
    34: "The Sivasankalpa Upanishad and other prayers",
    35: "Funeral formulas: the sacrifice to the Fathers",
    36: "Preliminary formulas of the Pravargya; prayers for peace",
    37: "The Pravargya rite: the three caldrons",
    38: "The Pravargya continued: milking the cow",
    39: "Expiatory formulas of the Pravargya",
    40: "The Isa Upanishad",
}
# Griffith numbers XII. 97 (a verse repeated as XII. 102) where the Madhyandina text has no mantra:
# from there on his verse n is mantra n-1. {book: first Griffith verse without a mantra of its own}
EXTRA_VERSE = {12: 97}
UNTRANSLATED = {(23, n) for n in range(20, 32)}  # Griffith: 'not reproducible even in the semi-obscurity
UNTRANSLATED_NOTE = "[Not translated by Griffith.]"  # of a learned European language' (note on XXIII. 20)


REF_ONLY = re.compile(r"^(?:=\s*|Repeated from\s+)?([IVXL]+)\.\s*(\d+)(?:\s*,\s*(\d+))?\.?$", re.I)


def from_roman(r):
    vals = {"I": 1, "V": 5, "X": 10, "L": 50}
    return sum(-vals[c] if vals[c] < vals.get(r[i + 1:i + 2], 0) else vals[c] for i, c in enumerate(r))


def expand_references(english, stats):
    """Where Griffith gives no more than the place of a verse already translated ('= IX. 40',
    'Repeated from XII. 54'), give that translation, with his reference after it."""
    for b, (en, merged) in english.items():
        for n, text in list(en.items()):
            m = REF_ONLY.match(text)
            if not m:
                continue
            book, nums = from_roman(m.group(1).upper()), [int(x) for x in m.groups()[1:] if x]
            last = merged.get(n, n)
            src = english.get(book, ({}, {}))[0]
            if len(nums) != last - n + 1 or not all(k in src and not REF_ONLY.match(src[k]) for k in nums):
                continue
            for i, k in enumerate(nums):
                en[n + i] = f"{src[k]} (= {m.group(1).upper()}. {k})"
            merged.pop(n, None)
            stats["references"] += 1


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    p1899, p1927, dharmic = sys.argv[1:4]
    rv_html = sys.argv[4] if len(sys.argv) > 4 else None
    books_a, books_b = read_books(p1899), read_books(p1927)
    classify(books_a, books_b)
    sa, odd_numbers = sanskrit(dharmic)
    vocab = Vocab(os.path.join(ROOT, "texts"), rv_html,
                  [open(p, encoding="utf-8").read() for p in (p1899, p1927)])
    global VOCAB, NAMER
    VOCAB = vocab
    namer = NAMER = Namer(vocab)
    stats, suspicious, report, summary, runs = collections.Counter(), collections.Counter(), [], {}, []
    english = {}
    for b in range(1, 41):
        top = len(sa[b]) + 3
        va, ma, ca = split_verses(books_a[b], top)
        vb, mb, cb = split_verses(books_b[b], top)
        notes_a = set().union(*[grams(p.text) for p in books_a[b] if not p.verse])
        notes_b = set().union(*[grams(p.text) for p in books_b[b] if not p.verse])
        fused = fuse_book({n: (verse_tokens(ls), ca[n]) for n, ls in va.items()},
                          {n: (verse_tokens(ls), cb[n]) for n, ls in vb.items()}, vocab, notes_a, notes_b, stats, runs,
                          len(sa[b]))
        english[b] = ({n: finish(t, vocab, namer, stats) for n, t in fused.items() if t}, {**mb, **ma})
        for n, text in english[b][0].items():
            for pat, rep in BOOK_FIXES.get(b, ()):
                text, k = re.subn(pat, rep, text)
                stats["table"] += k
            english[b][0][n] = text
        for text in english[b][0].values():
            suspicious_words(text, vocab, suspicious)
    expand_references(english, stats)
    for b in range(1, 41):
        en, merged = english[b]
        n_max = max(max(en), len(sa[b]))
        verses, covered = [], set()
        for n in range(1, n_max + 1):
            if n in covered:
                continue
            last = merged.get(n, n)
            covered.update(range(n, last + 1))
            text = en.get(n, UNTRANSLATED_NOTE if (b, n) in UNTRANSLATED else "")
            shift = EXTRA_VERSE.get(b)
            nums = [k - (shift is not None and k > shift) for k in range(n, last + 1) if k != shift]
            dev = " ".join(sa[b][k - 1] for k in nums if k <= len(sa[b]))
            v = {"n": n, "ref": f"{b}.{n}" if last == n else f"{b}.{n}-{last}"}
            if dev:
                v["sa"], v["tr"] = dev, iast(dev)
            v["en"] = text
            verses.append(v)
            if not text:
                report.append(f"{b}.{n}: no English")
            if not dev:
                report.append(f"{b}.{n}: no Sanskrit")
        size = write(f"yajurveda/{b}.json", {"sections": [{"label": f"Book {b}", "short": str(b),
                                                              "name": BOOK_NAMES[b], "verses": verses}]})
        g_count = max(en)
        print(f"yajurveda/{b}.json {size} bytes: {len(verses)} verses (Griffith {g_count}, Sanskrit {len(sa[b])})")
        summary[b] = (BOOK_NAMES[b], len(verses))
    print("\nwords mended by comparing the two readings:", stats["fused"], "| names mended:", stats["names"],
          "| table fixes:", stats["table"], "| spellings mended:", stats["spelling"],
          "| references expanded:", stats["references"],
          "| one-sided words kept/dropped:", stats["one_sided_kept"], "/", stats["one_sided_dropped"])
    print("Sanskrit mantra numbers printed out of sequence:", odd_numbers)
    if os.environ.get("YV_DEBUG"):
        for r in runs:
            print("  one-sided", r)
    print(len(report), "verses without English or Sanskrit:")
    for r in report:
        print("  ", r)
    print("\nwords not in the vocabulary (top 80):")
    print("  ", ", ".join(f"{w} {c}" for w, c in suspicious.most_common(80)))
    print("\n" + repr(summary))


if __name__ == "__main__":
    main()
