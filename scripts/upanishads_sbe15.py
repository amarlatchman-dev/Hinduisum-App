#!/usr/bin/env python3
"""The Brihadaranyaka and Svetasvatara Upanishads in F. Max Müller's translation (Sacred Books of
the East, vol. XV, 1884), cleaned from the archive.org OCR of that volume for the app.

  from upanishads_sbe15 import brihadaranyaka, svetasvatara
  data = brihadaranyaka(ocr_path)      # {"sections": [...]}, the shape of texts/upanishads/*.json

  python3 scripts/upanishads_sbe15.py <ocr.txt> [out_dir]    # writes both, as .json and .txt, for review

How the scan is read:
  * pages are cut at the running heads; on each page the text comes first and the footnotes
    after it. A footnote starts with a bare number; one that runs on from the page before is
    known by its longer lines (the notes are set in smaller type). Signature marks are dropped.
  * paragraphs are numbered within each Brahmana (each Adhyaya in the Svetasvatara). A number is
    read as the next verse only if it is the one expected, so footnote digits stuck to it
    ("46." = verse 4, note 6) and numbered lists in the notes are not mistaken for verses.
  * footnote numbers in the text, line-end hyphens, the OCR's quotation marks (' read as / * 1 V)
    and Müller's transliteration are then put right, the last with the tables below: WORD_RULES
    and WORDS for the Sanskrit words, PHRASES, the per-verse corrections BU_FIXES and SU_FIXES,
    and RESTORED_BU for paragraphs the scan garbles past repair (the Sanskrit formulas Müller left
    untranslated in VI, 4 and the three lists of teachers). A correction that no longer matches
    makes the build fail, so a change to the cleaning cannot silently undo one.
Standard library only; the functions read the OCR file and return data without writing anything.
"""
import json
import os
import re
import statistics
import sys

ORD = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth",
       "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth"]

_HEAD_EVEN = re.compile(r"^[\dIlOo]{2,4}[^A-Za-z]{0,2}[A-Za-z].{4,30}P.N.SHAD\.?$", re.I)
_HEAD_ODD = re.compile(r"^[IVXLH1lv]{1,4}[.,]?AD[HI]{1,2}YAYA,", re.I)
_ADHYAYA = re.compile(r"^(FIRST|SECOND|THIRD|FOURTH|FIFTH|SIXTH)\s+ADHYAYA")
_BRAHMANA = re.compile(r"^(%s)\s+Br\S*" % "|".join(ORD), re.I)
_VNUM = re.compile(r"^((?:[\dIilOo|]\s?){1,5}?)\s?[.,](?:\s+|(?=['*\"]))(.*)$")
_NOTE = re.compile(r"^\d{1,2}\s+\S")


# Line starts the OCR garbled beyond what the parser can read (verse and list numbers).
RAW_FIXES = [
    ("2j. Then Yaf^avalkya said", "27. Then Yaf^avalkya said"),
    ("24 \\ When the child is born", "24. When the child is born"),
    ("41. The same as far as Si^iviputra", "4. The same as far as Si^iviputra"),
    ("1 3 s. He who knows him who has no beginning", "13. He who knows him who has no beginning"),
    ("* For when there is as it were duality, then one", "14. 'For when there is as it were duality, then one"),
]


PARA = "\u00b6"                     # marks a paragraph break inside a verse until the quotes are set


def _pages(lines):
    pages, cur = [], []
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in lines]
    for a, b in RAW_FIXES:
        hits = [i for i, s in enumerate(lines) if a in s]
        if len(hits) == 1:
            lines[hits[0]] = lines[hits[0]].replace(a, b)
        elif hits:
            raise ValueError(f"raw fix matches {len(hits)} lines: {a!r}")
    for s in lines:
        flat = s.replace(" ", "")
        if _HEAD_EVEN.match(flat) or _HEAD_ODD.match(flat):
            pages.append(cur)
            cur = [("HEAD", s)]
            continue
        cur.append(s)
    pages.append(cur)
    out = []
    for pg in pages:
        head = pg[0][1] if pg and isinstance(pg[0], tuple) else None
        paras, p = [], []
        for s in pg:
            if isinstance(s, tuple):
                continue
            if s:
                # a verse number at the start of a line inside a paragraph begins a new one
                if (p and re.match(r"(\d{1,2}|[il]{1,2}|io)\.\s+(?!e\.)\S", s) and not p[-1].endswith("-")
                        and max(len(x) for x in p) < 58):
                    paras.append(p)
                    p = []
                p.append(s)
            elif p:
                paras.append(p)
                p = []
        if p:
            paras.append(p)
        out.append((head, paras))
    return out


def _width(p):
    ls = [len(x) for x in p[:-1]]
    return statistics.median(ls) if ls else 0


def _junk(p):
    return len(p) == 1 and len(p[0]) <= 10 and not re.search(r"[a-z]{3}", p[0])


def _num(s):
    return s.translate(str.maketrans("Iil|Oo", "111100")).replace(" ", "")


def parse(lines, bu=True, log=lambda s: None):
    """[adhyaya, brahmana, verse, [lines], running head] for each numbered paragraph (verse 0 is an
    invocation before the first one)."""
    verses = []
    adh, br, exp = 0, 0, 1
    vamsa = False
    note_open = False                 # the last footnote of the previous page ran on
    for pi, (head, paras) in enumerate(_pages(lines)):
        in_notes = False
        queue = list(paras)
        k = -1
        last_note = None
        while queue:
            p = queue.pop(0)
            if in_notes:
                last_note = p
                continue
            if _junk(p):
                log(f"junk {p}")
                continue
            k += 1
            first = p[0]
            m = _ADHYAYA.match(first)
            if m:
                adh += 1
                br, exp, vamsa = (0 if bu else 1), 1, False
                if not bu:
                    br = 1
                if len(p) > 1:
                    queue.insert(0, p[1:])
                continue
            m = _BRAHMANA.match(first) if bu else None
            if m and len(first) < 30:
                br += 1
                exp, vamsa = 1, False
                if ORD.index(m.group(1).lower()) + 1 != br:
                    log(f"brahmana heading mismatch {first} expected {br}")
                if len(p) > 1:
                    queue.insert(0, p[1:])
                continue
            m = _VNUM.match(first)
            if m and vamsa and not re.match(r"(from|The same)\b", m.group(2)):
                verses[-1][3].extend(p)       # a numbered name in a list of teachers
                continue
            if m:
                n = _num(m.group(1))
                if n.startswith(str(exp)):
                    if exp == 1:
                        vamsa = m.group(2).startswith("Now follows the stem")
                    verses.append([adh, br, exp, [m.group(2)] + p[1:], head])
                    exp += 1
                    continue
                hit = next((k for k in range(exp + 1, exp + 4) if n.startswith(str(k))), None)
                if hit:
                    log(f"GAP {adh}.{br}: expected {exp}, got {first!r} [{head}]")
                    verses.append([adh, br, hit, [m.group(2)] + p[1:], head])
                    exp = hit + 1
                    continue
                log(f"unexpected number {first!r} (exp {exp}) at {adh}.{br}")
            if _NOTE.match(first):
                # Notes follow the text on a page: a "note" with a verse or heading after it,
                # or a second note of the same number, is text whose opening quote was read as 1.
                later_verse = any((_VNUM.match(q[0]) and _num(_VNUM.match(q[0]).group(1)).startswith(str(exp))
                                   and _width(q) < 57) or _BRAHMANA.match(q[0]) for q in queue)
                # The notes on each page are numbered from 1, so a first "note" with another
                # number is text too.
                num = first.split()[0]
                same_num = any(q[0].split()[0] == num for q in queue if _NOTE.match(q[0]))
                if not (later_verse or same_num or num != "1"):
                    if k == 0:
                        log(f"FIRSTNOTE k={k} {' / '.join(p)[:120]!r}")
                    in_notes = True
                    last_note = p
                    continue
                log(f"QUOTE-AS-DIGIT {' / '.join(p)[:100]!r}")
                p = [("O " if num == "0" else "'") + first.split(None, 1)[1]] + p[1:]
                first = p[0]
            w = _width(p) or (len(p[0]) + 2 if len(p) == 1 else 0)    # one line: its own length
            if (k == 0 and note_open and w >= 60) or (k > 0 and w >= 58 + 4 * (len(p) == 1)):
                log(f"WIDE {w} {' / '.join(p)[:110]!r}")
                in_notes = True
                last_note = p
                continue
            if exp == 1 and (bu or not verses or verses[-1][0] != adh):
                log(f"PRE {adh}.{br} {' / '.join(p)!r}")   # an invocation before the first verse
                verses.append([adh, br, 0, p, head])
                continue
            if verses:
                nxt = queue[0][0] if queue else ""
                if _NOTE.match(nxt) or not queue:
                    log(f"TAIL {verses[-1][0]}.{verses[-1][1]}.{verses[-1][2]} k={k} {' / '.join(p)[:150]!r}")
                if re.search(r"[.!?'\":;)]$", verses[-1][3][-1]):
                    verses[-1][3].append(PARA)          # a new paragraph within the verse
                verses[-1][3].extend(p)
            else:
                log(f"orphan {p}")
        note_open = bool(last_note) and not re.search(r"[.!?)]['\"]?$", last_note[-1])
    return verses



# --------------------------------------------------------------------------- cleaning
_PROTECT = "\x00"


def _vocab(all_lines):
    """Words and hyphenated compounds that occur inside a line anywhere in the volume, to decide
    whether a hyphen at the end of a line belongs to the word."""
    words, hyph = set(), set()
    for ln in all_lines:
        for t in ln.split()[:-1]:
            t = re.sub(r"^\W+|[\W\d]+$", "", t).lower()
            if "-" in t:
                hyph.add(t)
            elif t.isalpha():
                words.add(t)
    return words, hyph


def _join(lines, vocab):
    hyph = vocab[1]
    out = ""
    for ln in lines:
        if not out:
            out = ln
            continue
        if ln == PARA:
            out += " " + PARA
            continue
        m = re.search(r"(\S*?)-$", out)
        if m and m.group(1) and re.match(r"[a-z]", ln):
            left = re.sub(r"^.*[^\w&^/#£]", "", m.group(1))
            right = re.match(r"[\w&^/#£]*", ln).group(0)
            l2, r2 = re.sub(r"\d+$", "", left).lower(), re.sub(r"\d+$", "", right).lower()
            keep = f"{l2}-{r2}" in hyph or l2 in KEEP_HYPHEN_LEFT or f"{l2}-{r2}" in KEEP_HYPHEN
            out = out + ln if keep else out[:-1] + ln
        else:
            out += " " + ln
    return out


# A hyphen at the end of a line is kept when the compound occurs inside a line elsewhere in the
# volume, or is listed here; otherwise the word is joined.
KEEP_HYPHEN_LEFT = {"self"}
KEEP_HYPHEN = {"half-months", "meeting-place", "kidney-beans", "back-breathing"}


def _footnotes(t, vamsa=False):
    """Drop the footnote numbers (and the odd sign standing for one) from the English."""
    keep = []

    def protect(x):
        keep.append(x)
        return f"{_PROTECT}{len(keep) - 1}{_PROTECT}"
    t = re.sub(r"\((?:Rv|No)\. [^)]*\)", lambda m: protect(m.group(0)), t)   # (Rv. I, 189, 1.), (No. 36)
    t = re.sub(r"\(([1-9il])\)", lambda m: protect("(%s)" % m.group(1).replace("i", "1").replace("l", "1")), t)
    t = re.sub(PARA + r" \d{1,2}\.(?= ')", lambda m: protect(m.group(0)), t)  # stanzas numbered in a verse
    if vamsa:                                                                 # the numbered teachers
        t = re.sub(r"(?:^|(?<=, )|(?<=\. )|(?<=: ))\d{1,2}(?=\. [A-Z(])", lambda m: protect(m.group(0)), t)
    t = re.sub(r"(?<=[^\W\d_]|[)\]'\".,;:!?/*\\])\d{1,2}(?=[\s,.;:!?'\")\]/*]|$)", "", t)  # word1 / ,2
    t = re.sub(r"(?:^|(?<=\s))\d{1,2}(?=[\s,.;:!?'\")\]/]|$)", "", t)                      # word 1
    t = re.sub(r"(?<=\w)\s*\*(?=[\s,.;:!?)]|$)", "", t)                                     # word *
    t = re.sub(r"\s\\(?=\s|$)|\\$", "", t)                                                   # moon \
    t = re.sub(r"\s[xl](?=[\s,.;:!?)]|$)", "", t)                                           # lords x, / Abhyaroha l
    return re.sub(_PROTECT + r"(\d+)" + _PROTECT, lambda m: keep[int(m.group(1))], t)


# --------------------------------------------------------------------------- Sanskrit words
def _sanskrit_core(c):
    """Müller's transliteration as the OCR mangled it, turned into the app's plain spelling."""
    for x in (c, _generic(c)):
        if x in WORDS:
            return WORDS[x]
        for pat, rep in WORD_RULES:
            if re.fullmatch(pat, x):
                return rep
    return _generic(c)


def _generic(c):
    if (re.fullmatch(r"[A-Za-z'-]+", c) and "rz" not in c) or c == "&c":
        return c
    c = c.replace("&", "a")
    c = re.sub(r"^(?:\.|•|■|>|»|\*|v|i|f|,)S(?=[a-z&^/])", "S", c)        # .Sakalya, vSloka
    c = re.sub(r"^6(?=[a-z&])", "S", c)                                     # 6akalya
    c = re.sub(r"^(?:i\?z|i\?/|7\?z|JZ|Rz|R/)", "Ri", c)                    # i?zshi, i?/g-veda
    c = re.sub(r"^Wz", "Vri", c)
    c = re.sub(r"(?<=[A-Za-z])rz(?=[a-z]|$)", "ri", c)                      # Savitrz, Brzhaspati
    c = re.sub(r"(?<=[A-Za-z])r/(?=[a-z]|$)", "ri", c)
    c = re.sub(r"(?<=[A-Za-z])/z(?=[a-z]|$)", "n", c)                        # pra/za
    return c


def _sanskrit(t):
    def tok(m):
        lead, core, trail = re.match(r"^([\"'(\[]*)(.*?)([\"'),.;:!?/*\]\d\\]*)$", m.group(0)).groups()
        if not core:
            return m.group(0)
        if re.fullmatch(r"\d+", core):
            return m.group(0)
        if core.endswith("'s") and len(core) > 3:
            return lead + _sanskrit_core(core[:-2]) + "'s" + trail
        return lead + _sanskrit_core(core) + trail
    t = re.sub(r"\S+", tok, t)
    for a, b in PHRASES:
        t = t.replace(a, b)
    return t


# --------------------------------------------------------------------------- quotes and spacing
_QUESTION = re.compile(r"(?:(?:And|But|Then|Now|O \w+,)\s+)?(?:(?:in|by|for|to|from|on|with|of|at)\s+)?"
                       r"(?:what|who|whom|whose|which|where|whither|whence|how|why|is|are|was|were|do|does|"
                       r"did|dost|didst|can|canst|shall|will|wilt|hast|hath|art|knowest|has|have|whether)\b",
                       re.I)


_SAID = r"(?:he|she|they|said|replied|answered|asked|says|saying|thus|quoth)\b"


def _prequotes(t):
    """Opening quotes the scan read as a digit or letter (before footnote numbers are dropped)."""
    t = re.sub(r"(?<=[:;,] )[\dli] (?=[A-Z])", "'", t)                     # : 1 Thou art -> : 'Thou art
    t = re.sub(r"(?<=[.?!] )[li] (?=[A-Z])", "'", t)
    return re.sub(r"^1 (?=[A-Z])", "'", t)


def _quotes(t):
    t = re.sub(r"(^|\s)[*•]\s*(?=[A-Z'\"(])", r"\1'", t)                 # * as an opening quote
    t = re.sub(r"(^|\s)\*\s*(?=[a-z])", r"\1'", t)
    t = re.sub(r"\s•\s", " ", t)

    t = re.sub(r"(?<=\S) V(?=\s+[A-Z'(]|$)", "/", t)                       # V read for /

    def slash(m):                                                          # word/ -> word.' or word,'
        word, after = m.group(1), t[m.end():]
        if word[-1] in ".?!,;:":
            return word + "'"
        if re.match(r"\s*[a-z]", after):
            return word + ",'"
        start = max(t.rfind(" '", 0, m.start()) + 2, max(t.rfind(x, 0, m.start()) for x in (". ", "? ", "! ")) + 2)
        sentence = t[start:m.start()].lstrip("'\"")
        if _QUESTION.match(sentence) and not re.match(r"Do (thou|ye|not|this|that)\b", sentence):
            return word + "?'"
        return word + ".'"
    t = re.sub(r"(\S)/(?=\s|$|['\"])", slash, t)

    def inside(before, q):                  # is a quotation of this kind open at this point?
        n = len(re.findall(r"(?<![A-Za-z])%s|%s(?![A-Za-z])" % (q, q), before))
        return n % 2 == 1

    def lone(m):                                                           # a quote standing alone
        before, q, after = t[:m.start()].rstrip(), m.group(1), t[m.end():]
        p = before[-1:] if before else ""
        if after.startswith(PARA):
            return q + " "                                                 # ends a paragraph
        if not p or p in ":;(—'\"" + PARA or re.search(r"\(\d\)$", before):
            return " " + q                                                 # opening
        if after[:1] in "'\"":
            return q + " "                                                 # closing, another opens
        if q == "'" and re.match(_SAID, after):
            return ("" if p in ".?!," else ",") + q + " "                  # Yajnavalkya,' he said
        if p in ".?!,":                    # closing only before "X said"
            if re.match(r"[A-Z][\w-]*\s(?:[\w-]+\s){0,2}(?:said|replied|asked|answered|spoke|thought)\b", after):
                return q + " "
            return " " + q                 # Müller opens every paragraph of a long speech anew
        if inside(before, q):
            return q + " "                                                 # closing
        return " " + q
    t = re.sub(r"(?:^|\s+)(['\"])\s+", lone, t)
    return t


def _tidy(t):
    t = re.sub(r"\s+", " ", t.replace(PARA, " ")).strip()
    t = re.sub(r"''\s*(?=[A-Z])", "' '", t)                                # ?'' Those -> ?' 'Those
    t = re.sub(r"(?<=')\"\s+(?=\w)", '"', t)                                # '" He -> '"He
    t = re.sub(r"\.\s\.\s\.", "...", t)
    t = re.sub(r"\s*—\s*|\s+-\s+|--", "—", t)
    t = re.sub(r"\s+([,.;:!?)\]])", r"\1", t)
    t = re.sub(r"([(\[])\s+", r"\1", t)
    t = re.sub(r"\s+(['\"])(?=[\s,.;:!?)]|$)", r"\1", t)                    # closing quotes
    t = re.sub(r"(?<=[,;:])(?=[A-Za-z(])", " ", t)
    t = re.sub(r"&c(?![.])", "&c.", t)
    t = re.sub(r"\bi\. ?e\.?(?=[\s,)])", "i.e.", t)
    t = re.sub(r"(?<!\.)\.\.(?!\.)", ".", t)
    return t


# Paragraphs restored whole. Müller left the ritual formulas of VI, 4 in Sanskrit; the scan
# garbles nearly every word of them, so they are given here in his reading (his notes on those
# pages name it: a sa strinam with Sankara, nishthaya with A. and B.), spelled the app's way.
RESTORED_BU = {
    "6.4.3": "Tasya vedir upastho, lomani barhis, charmadhishavane, samiddho madhyatas, tau mushkau. Sa "
             "yavan ha vai vajapeyena yajamanasya loko bhavati tavan asya loko bhavati ya evam vidvan "
             "adhopahasam charaty a sa strinam sukritam vrinkte 'tha ya idam avidvan adhopahasam charaty asya "
             "striyah sukritam vrinjate.",
    "6.4.4": "Etad dha sma vai tadvidvan Uddalaka Arunir ahaitad dha sma vai tadvidvan Nako Maudgalya "
             "ahaitad dha sma vai tadvidvan Kumaraharita aha, bahavo marya brahmanayana nirindriya visukrito "
             "'smal lokat prayanti ya idam avidvamso 'dhopahasam charantiti. Bahu va idam suptasya va jagrato "
             "va retah skandati,",
    "6.4.5": "Tad abhimrised anu va mantrayeta yan me 'dya retah prithivim askantsid yad oshadhir apy asarad "
             "yad apah, idam aham tad reta adade punar mam aitv indriyam punas tejah punar bhagah, punar agnayo "
             "dhishnya yathasthanam kalpantam, ity anamikangushthabhyam adayantarena stanau va bhruvau va "
             "nimrijyat.",
    "6.4.9": "Sa yam ichchhet kamayeta meti tasyam artham nishthaya mukhena mukham sandhayopastham asya "
             "abhimrisya japed angadangat sambhavasi hridayad adhi jayase, sa tvam angakashayo 'si "
             "digdhaviddham iva madayemam amum mayiti.",
    "6.4.10": "Atha yam ichchhen na garbham dadhiteti tasyam artham nishthaya mukhena mukham "
              "sandhayabhipranyapanyad indriyena te retasa reta adada ity areta eva bhavati.",
    "6.4.11": "Atha yam ichchhed garbham dadhiteti tasyam artham nishthaya mukhena mukham "
              "sandhayapanyabhipranyad indriyena te retasa reta adadhamiti garbhiny eva bhavati.",
    "6.4.21": "Athasya uru vihapayati, vijihitham dyavaprithivi iti tasyam artham nishthaya mukhena mukham "
              "sandhaya trir enam anulomam anumarshti, Vishnur yonim kalpayatu, Tvashta rupani pimsatu, "
              "asinchatu Prajapatir Dhata garbham dadhatu te. Garbham dhehi Sinivali, garbham dhehi "
              "prithushtuke, garbham te Asvinau devav adhattam pushkarasrajau.",
    "6.4.22": "Hiranmayi arani yabhyam nirmanthatam asvinau, tam te garbham havamahe dasame masi sutave. "
              "Yathagnigarbha prithivi, yatha dyaur indrena garbhini, vayur disam yatha garbha evam garbham "
              "dadhami te 'sav iti.",
    "6.4.23": "Soshyantim adbhir abhyukshati. Yatha vayuh pushkarinim samingayati sarvatah, eva te garbha "
              "ejatu sahavaitu jarayuna. Indrasyayam vrajah kritah sargalah saparisrayah, tam indra nirjahi "
              "garbhena savaram saheti.",
}

# The lists of teachers (II, 6; IV, 6; VI, 5). The scan breaks the numbering and most names, so
# each list is given in full: (verse, opening words, first item number, items). A verse that
# begins inside an item ("8. Gautama | 2. from Agnivesya") opens with that item's "from ...".
_V26 = ["Pautimashya from Gaupavana", "Gaupavana from Pautimashya", "Pautimashya from Gaupavana",
        "Gaupavana from Kausika", "Kausika from Kaundinya", "Kaundinya from Sandilya",
        "Sandilya from Kausika and Gautama", "Gautama|from Agnivesya",
        "Agnivesya from Sandilya and Anabhimlata", "Sandilya and Anabhimlata from Anabhimlata",
        "Anabhimlata from Anabhimlata", "Anabhimlata from Gautama", "Gautama from Saitava and Prachinayogya",
        "Saitava and Prachinayogya from Parasarya", "Parasarya from Bharadvaja",
        "Bharadvaja from Bharadvaja and Gautama", "Gautama from Bharadvaja", "Bharadvaja from Parasarya",
        "Parasarya from Vaijavapayana", "Vaijavapayana from Kausikayani", "Kausikayani|from Ghritakausika"]
_TAIL = ["Asurayana and Yaska from Traivani", "Traivani from Aupajandhani", "Aupajandhani from Asuri",
         "Asuri from Bharadvaja", "Bharadvaja from Atreya", "Atreya from Manti", "Manti from Gautama",
         "Gautama from Gautama", "Gautama from Vatsya", "Vatsya from Sandilya", "Sandilya from Kaisorya Kapya",
         "Kaisorya Kapya from Kumaraharita", "Kumaraharita from Galava", "Galava from Vidarbhi-kaundinya",
         "Vidarbhi-kaundinya from Vatsanapat Babhrava", "Vatsanapat Babhrava from Pathi Saubhara",
         "Pathi Saubhara from Ayasya Angirasa", "Ayasya Angirasa from Abhuti Tvashtra",
         "Abhuti Tvashtra from Visvarupa Tvashtra", "Visvarupa Tvashtra from Asvinau",
         "Asvinau from Dadhyach Atharvana", "Dadhyach Atharvana from Atharvan Daiva",
         "Atharvan Daiva from Mrityu Pradhvamsana", "Mrityu Pradhvamsana from Pradhvamsana",
         "Pradhvamsana from Ekarshi", "Ekarshi from Viprachitti", "Viprachitti from Vyashti",
         "Vyashti from Sanaru", "Sanaru from Sanatana", "Sanatana from Sanaga", "Sanaga from Parameshthin",
         "Parameshthin from Brahman", "Brahman is Svayambhu, self-existent. Adoration to Brahman."]
_V26 += ["Ghritakausika from Parasaryayana", "Parasaryayana from Parasarya", "Parasarya from Jatukarnya",
         "Jatukarnya from Asurayana and Yaska"] + _TAIL[:]
_V46 = ["(We) from Pautimashya", "Pautimashya from Gaupavana", "Gaupavana from Pautimashya",
        "Pautimashya from Gaupavana", "Gaupavana from Kausika", "Kausika from Kaundinya",
        "Kaundinya from Sandilya", "Sandilya from Kausika and Gautama", "Gautama|from Agnivesya",
        "Agnivesya from Gargya", "Gargya from Gargya", "Gargya from Gautama", "Gautama from Saitava",
        "Saitava from Parasaryayana", "Parasaryayana from Gargyayana", "Gargyayana from Uddalakayana",
        "Uddalakayana from Jabalayana", "Jabalayana from Madhyandinayana", "Madhyandinayana from Saukarayana",
        "Saukarayana from Kashayana", "Kashayana from Sayakayana", "Sayakayana from Kausikayani",
        "Kausikayani|from Ghritakausika", "Ghritakausika from Parasaryayana", "Parasaryayana from Parasarya",
        "Parasarya from Jatukarnya", "Jatukarnya from Asurayana and Yaska", "Asurayana from Traivani"] + _TAIL[1:]
_V65 = ["Pautimashiputra from Katyayaniputra", "Katyayaniputra from Gotamiputra",
        "Gotamiputra from Bharadvajiputra", "Bharadvajiputra from Parasariputra",
        "Parasariputra from Aupasvatiputra", "Aupasvatiputra from Parasariputra",
        "Parasariputra from Katyayaniputra", "Katyayaniputra from Kausikiputra",
        "Kausikiputra from Alambiputra and Vaiyaghrapadiputra",
        "Alambiputra and Vaiyaghrapadiputra from Kanviputra", "Kanviputra from Kapiputra",
        "Kapiputra|from Atreyiputra", "Atreyiputra from Gautamiputra", "Gautamiputra from Bharadvajiputra",
        "Bharadvajiputra from Parasariputra", "Parasariputra from Vatsiputra", "Vatsiputra from Parasariputra",
        "Parasariputra from Varkaruniputra", "Varkaruniputra from Varkaruniputra",
        "Varkaruniputra from Artabhagiputra", "Artabhagiputra from Saungiputra",
        "Saungiputra from Sankritiputra", "Sankritiputra from Alambayaniputra",
        "Alambayaniputra from Alambiputra", "Alambiputra from Jayantiputra",
        "Jayantiputra from Mandukayaniputra", "Mandukayaniputra from Mandukiputra",
        "Mandukiputra from Sandiliputra", "Sandiliputra from Rathitariputra",
        "Rathitariputra from Bhalukiputra", "Bhalukiputra from Kraunchikiputrau",
        "Kraunchikiputrau from Vaidabhatiputra", "Vaidabhatiputra from Karsakeyiputra",
        "Karsakeyiputra from Prachinayogiputra", "Prachinayogiputra from Sanjiviputra",
        "Sanjiviputra from Prasniputra Asurivasin", "Prasniputra Asurivasin from Asurayana",
        "Asurayana from Asuri", "Asuri|from Yajnavalkya", "Yajnavalkya from Uddalaka", "Uddalaka from Aruna",
        "Aruna from Upavesi", "Upavesi from Kusri", "Kusri from Vajasravas",
        "Vajasravas from Jihvavat Vadhyoga", "Jihvavat Vadhyoga from Asita Varshagana",
        "Asita Varshagana from Harita Kasyapa", "Harita Kasyapa from Silpa Kasyapa",
        "Silpa Kasyapa from Kasyapa Naidhruvi", "Kasyapa Naidhruvi from Vach", "Vach from Ambhini",
        "Ambhini from Aditya, the Sun"]
_V65b = ["Sanjiviputra from Mandukayani", "Mandukayani from Mandavya", "Mandavya from Kautsa",
         "Kautsa from Mahitthi", "Mahitthi from Vamakakshayana", "Vamakakshayana from Sandilya",
         "Sandilya from Vatsya", "Vatsya from Kusri", "Kusri from Yajnavachas Rajastambayana",
         "Yajnavachas Rajastambayana from Tura Kavasheya", "Tura Kavasheya from Prajapati",
         "Prajapati from Brahman", "Brahman is Svayambhu, self-existent. Adoration to Brahman!"]


def _stem(items, first=1, lead="Now follows the stem:", end=""):
    """Split a numbered list of teachers into Müller's paragraphs at the items marked a|b."""
    paras, cur = [], [lead] if lead else []
    for n, it in enumerate(items, first):
        a, _, b = it.partition("|")
        cur.append(f"{n}. {a}" + ("" if b else ","))
        if b:
            paras.append(" ".join(cur))
            cur = [b + ","]
    paras.append(" ".join(cur))
    paras[-1] = paras[-1].rstrip(",") + end
    return paras


for _ref, _paras in (("2.6", _stem(_V26)), ("4.6", _stem(_V46)), ("6.5", _stem(_V65, end=".") + _stem(
        _V65b, 36, "The same as far as Sanjiviputra (No. 36), then"))):
    for _i, _t in enumerate(_paras, 1):
        RESTORED_BU[f"{_ref}.{_i}"] = _t
RESTORED_BU["6.5.3"] += (" As coming from Aditya, the Sun, these pure Yajus verses have been proclaimed by "
                         "Yajnavalkya Vajasaneya.")

_MISSED = []                       # verse fixes that no longer match: the build fails on them


def clean(lines, ref, vocab, vamsa=False, fixes=None):
    t = _join(lines, vocab)
    t = re.sub(r"\s+", " ", t)
    t = _sanskrit(t)
    t = _prequotes(t)
    t = _footnotes(t, vamsa)
    t = _quotes(t)
    t = _tidy(t)
    for a, b in (fixes or {}).get(ref, []):
        if a not in t:
            _MISSED.append(f"{ref}: {a!r}")
        t = t.replace(a, b)
    return t


# --------------------------------------------------------------------------- replacement tables
# Garbled words seen in the OCR (or what the generic rules in _sanskrit_core make of them),
# with Müller's word in the app's spelling: no diacritics, his italic k as ch and italic g as j,
# s for both sibilants, sh for the retroflex one, n for every nasal and ri for the vowel r.
# The scan reads his italic letters as ^ # / £ * w z and the like, â as &, Ś as 6, .S or *S.
WORD_RULES = [                     # families with many spellings (the whole word must match)
    (r"Y\S{0,8}valkya", "Yajnavalkya"),
    (r"Y\S{0,8}valkyasaid", "Yajnavalkya said"),
    (r"\S{0,4}kalya", "Sakalya"),                                  # .Sakalya, 6%kalya, ££kalya
    (r"A\S{1,6}atru", "Ajatasatru"),
    (r"Pr\S{1,4}pati", "Prajapati"),
    (r"Pr\S{1,4}patir", "Prajapatir"),
    (r"Br\S{1,2}hma[\^#]a", "Brahmana"),
    (r"Br\S{1,2}hma[\^#]as", "Brahmanas"),
    (r"Y\S{0,2}ur-veda", "Yajur-veda"),
    (r"(?:Ganaka|kanaka|\(kanaka|\(Ganaka)", "Janaka"),
    (r"G\S?rg[lfti]", "Gargi"),
    (r"Maitrey[lt]", "Maitreyi"),
]

WORDS = {
    # people
    "-rclnaki": "Janaki", "G^naki": "Janaki", "Ayasthfina": "Ayasthuna", "Ayasthtoa": "Ayasthuna",
    ".SVetaketu": "Svetaketu", "6Vetaketu": "Svetaketu", "V.SVetaketu": "Svetaketu",
    "^aivali": "Jaivali", "Caivali": "Jaivali", "Aaikitaneya": "Chaikitaneya", "Alkitana": "Chikitana",
    "A\"lila": "Chula", "Ajftla": "Chula", "Aakraya^a": "Chakrayana", "AUkraya^a": "Chakrayana",
    "iTakr^ya^a": "Chakrayana", "Aanaala": "Chandala", "KandaXdi": "Chandala",
    "Gamadagni": "Jamadagni", "GaMla": "Jabala", "Gctbala": "Jabala", "Gclrgyasaid": "Gargya said",
    "Gdrgya": "Gargya", "Girgya": "Gargya", "Artabhdga": "Artabhaga", "Saratk£rava": "Jaratkarava",
    "SaratMrava": "Jaratkarava", "Bhu^yu": "Bhujyu", "Lihy£yani": "Lahyayani", "Pata^ala": "Patanchala",
    "Pata^iala": "Patanchala", "Kipya": "Kapya", "Anmi": "Aruni", "Arumr": "Aruni", "Aru;zi": "Aruni",
    "Va/£aknavi": "Vachaknavi", "Va^aknavl": "Vachaknavi", "Va£aknavt": "Vachaknavi", "Vi^aknavt": "Vachaknavi",
    "Va/£aknavt": "Vachaknavi", "£itvan": "Jitvan", "SaulMyana": "Saulbayana", "Kaushltakeya": "Kaushitakeya",
    "Bhdradvd^a": "Bharadvaja", "Bhiradvi^a": "Bharadvaja", "Gardabhivibhfta": "Gardabhivibhita",
    "Gardabhlvibhfta": "Gardabhivibhita", "Varsh^a": "Varshna", "Buafila": "Budila", "A^vatara^vi": "Asvatarasvi",
    "Pravaha^a": "Pravahana", "Kityayanf": "Katyayani", "Kityayant": "Katyayani", "Katyayant": "Katyayani",
    "Mithild": "Mithila", "Vasish/^a": "Vasishtha", "Vasish^a": "Vasishtha", "Ka^yapa": "Kasyapa",
    "I/a": "Ila", "Maitravaru^i": "Maitravaruni", "Fitri": "Pitri", "Tdpasa": "Tapasa", "Srama^a": "Sramana",
    "^rama^a": "Sramana",
    # the lists of teachers (II, 6; IV, 6; VI, 5)
    "Kaurika": "Kausika", "Kaimka": "Kausika", "Kau^inya": "Kaundinya", "Kaimdinya": "Kaundinya",
    "Sandi\\ya": "Sandilya", "Sbndilya": "Sandilya", "SandilyB": "Sandilya", "Sanaftlya": "Sandilya",
    "vSa/zaftlya": "Sandilya", "Agniverya": "Agnivesya", "Pra^inayogya": "Prachinayogya",
    "Pra/£inayogya": "Prachinayogya", "Pdra^arya": "Parasarya", "Parlrarya": "Parasarya", "Parararya": "Parasarya",
    "Pirasarya": "Parasarya", "Para^arya": "Parasarya", "Paraiarya": "Parasarya", "Bharadva^a": "Bharadvaja",
    "Bharadvafa": "Bharadvaja", "Bhdradva^a": "Bharadvaja", "Bhdradvi^a": "Bharadvaja",
    "Bharadv&^a": "Bharadvaja", "Bh&radv&^a": "Bharadvaja", "Bh&radva^a": "Bharadvaja",
    "Vai^avApdyana": "Vaijavapayana", "Vai£*avapayana": "Vaijavapayana", "Kaimkayani": "Kausikayani",
    "Kau^ikdyani": "Kausikayani", "Kaiuikayani": "Kausikayani", "Ghritakaosika": "Ghritakausika",
    "Ghritakaurika": "Ghritakausika", "Ghritakau^ika": "Ghritakausika", "Ghritakauiika": "Ghritakausika",
    "P^rd^arydyana": "Parasaryayana", "Para^aryaya^a": "Parasaryayana", "Parasaryaya^a": "Parasaryayana",
    "Parlsaryayana": "Parasaryayana", "Gattikarizya": "Jatukarnya", "Gatftkanzya": "Jatukarnya",
    "Gatukarizya": "Jatukarnya", "Satukarizya": "Jatukarnya", "Asuraya^a": "Asurayana", "Traivam": "Traivani",
    "Travam": "Traivani", "Travani": "Traivani", "Aupa^andhani": "Aupajandhani", "Ma^i": "Manti",
    "Ma/^i": "Manti", "Mi/z/i": "Manti", "KaLrorya": "Kaisorya", "Kumclraharita": "Kumaraharita",
    "Kumarahdrita": "Kumaraharita", "Gilava": "Galava", "Vidarbhl": "Vidarbhi", "kau/^inya": "kaundinya",
    "kau^inya": "kaundinya", "kau^nya": "kaundinya", "kaunafinya": "kaundinya",
    "Vidarbhl-kau^inya": "Vidarbhi-kaundinya", "Vidarbhi-kau^nya": "Vidarbhi-kaundinya",
    "Aydsya": "Ayasya", "Ayisya": "Ayasya", "Abhtiti": "Abhuti", "Abhfiti": "Abhuti", "Abhilti": "Abhuti",
    "Tvash/ra": "Tvashtra", "Tvashfra": "Tvashtra", "Tvash/fra": "Tvashtra", "Visvarfipa": "Visvarupa",
    "Visvarllpa": "Visvarupa", "Visvarftpa": "Visvarupa", "VLrvartipa": "Visvarupa", "A^vinau": "Asvinau",
    "Dadhya^": "Dadhyach", "Dadhya/£": "Dadhyach", "Dadhya>£": "Dadhyach", "Dadhya>§": "Dadhyach",
    "Atharva^a": "Atharvana", "Atharva/za": "Atharvana", "Mmyu": "Mrityu", "Mntyu": "Mrityu",
    "Pradhva^sana": "Pradhvamsana", "Pradhvawsana": "Pradhvamsana", "Vipra^itti": "Viprachitti",
    "Vipraatti": "Viprachitti", "Vyash^i": "Vyashti", "Vyash/i": "Vyashti", "Sanim": "Sanaru",
    "ParameshMin": "Parameshthin", "Paramesh/^in": "Parameshthin", "Paramesh^in": "Parameshthin",
    "Saukariya^a": "Saukarayana", "Saukaraya^a": "Saukarayana", "Kashaya^a": "Kashayana",
    "Uddalakiyana": "Uddalakayana", "Udd^llakayana": "Uddalakayana", "^ibaliyana": "Jabalayana",
    "GaMlayana": "Jabalayana", "Midhyandinayana": "Madhyandinayana", "Gclrgyayana": "Gargyayana",
    "Pautimashfputra": "Pautimashiputra", "Bharadva^iputra": "Bharadvajiputra", "Para^ariputra": "Parasariputra",
    "Parlrariputra": "Parasariputra", "Aupasvatlputra": "Aupasvatiputra", "Vaiyaghrapadlputra": "Vaiyaghrapadiputra",
    "Kdnviputra": "Kanviputra", "Varkaru/dputra": "Varkaruniputra", "Varkaru^iputra": "Varkaruniputra",
    ",5aungiputra": "Saungiputra", ".5aungiputra": "Saungiputra", "Gayantiputra": "Jayantiputra",
    "Ma;^ukayaniputra": "Mandukayaniputra", "Ma^ukiyaniputra": "Mandukayaniputra",
    "Ma/^iikiputra": "Mandukiputra", "Md^takiputra": "Mandukiputra", "Sa^iliputra": "Sandiliputra",
    ".Sa/zdiliputra": "Sandiliputra", "BMlukiputra": "Bhalukiputra", "Krau?X£iklputrau": "Kraunchikiputrau",
    "Kraiw^ikiputrau": "Kraunchikiputrau", "Vai//abhatiputra": "Vaidabhatiputra",
    "Vai^abhatlputra": "Vaidabhatiputra", "Karsakeylputra": "Karsakeyiputra", "Kanrakeyiputra": "Karsakeyiputra",
    "Pra/§inayogiputra": "Prachinayogiputra", "Pra^inayogiputra": "Prachinayogiputra",
    "Sa^iviputra": "Sanjiviputra", "Sa^tviputra": "Sanjiviputra", "Si^iviputra": "Sanjiviputra",
    "S£%1viputra": "Sanjiviputra", "Pra^iputra": "Prasniputra", "Prawiputra": "Prasniputra",
    "Anma": "Aruna", "Upave^i": "Upavesi", "Ku^ri": "Kusri", "Kum": "Kusri", "Kimi": "Kusri",
    "Va^asravas": "Vajasravas", "^ihvavat": "Jihvavat", "Cihvavat": "Jihvavat", "vSllpa": "Silpa",
    "^ilpa": "Silpa", "Katyapa": "Kasyapa", "Vai": "Vach", "Va/£": "Vach", "Ambhkl": "Ambhini",
    "Ambhi/d": "Ambhini", "Ya^ois": "Yajus", "Va^asaneya": "Vajasaneya", "Va£*asaneya": "Vajasaneya",
    "Ma/2aftkayani": "Mandukayani", "Md^6kdyani": "Mandukayani", "Ma^avya": "Mandavya", "Manaavya": "Mandavya",
    "Mihitthi": "Mahitthi", "Vdmakakshayana": "Vamakakshayana", "Vamakakshaya^a": "Vamakakshayana",
    "Vdtsya": "Vatsya", "Ya^ava^as": "Yajnavachas", "Ri^astambayana": "Rajastambayana",
    "R^astamMyana": "Rajastambayana",
    # gods, beings, places
    "Hira^yagarbha": "Hiranyagarbha", "Par^anya": "Parjanya", "Varu^a": "Varuna", "Vanma": "Varuna",
    "l^ana": "Isana", "Pfishan": "Pushan", "Pftshan": "Pushan", "Ptishan": "Pushan", "Vira^": "Viraj",
    "Vira^*": "Viraj", "Vir^*": "Viraj", "Vairvanara": "Vaisvanara", "VaLsvanara": "Vaisvanara",
    "A^vins": "Asvins", "Aivins": "Asvins", "Arvins": "Asvins", "Vii'vedevas": "Visvedevas",
    "VLrvedevas": "Visvedevas", "Vaiku^/^a": "Vaikuntha", "Aandra": "Chandra", "A\"andra": "Chandra",
    "Aandramas": "Chandramas", "A\"andramas": "Chandramas", "iTandramas": "Chandramas", "Pmhivi": "Prithivi",
    "Przthivi": "Prithivi", "Vfiyu": "Vayu", "vclyu": "vayu", "Tai^asa": "Taijasa", "Kuru-Pa^alas": "Kuru-Panchalas",
    "Pa^alas": "Panchalas", "Pa^ilas": "Panchalas", "Satar(ipa": "Satarupa", "Sarasvatl": "Sarasvati",
    # classes, rites, texts
    "K?iidra": "Sudra", "Sfidra": "Sudra", "Sftdra": "Sudra", "Sildra": "Sudra", "Vauya": "Vaisya",
    "Wzshala": "Vrishala", "Wzshali": "Vrishali", "Ra^anya": "Rajanya", "Ra^asftya": "Rajasuya",
    "A^vamedha": "Asvamedha", "A^va-medha": "Asva-medha", "A^vamedha-sacrifice": "Asvamedha-sacrifice",
    "Gyotish/oma": "Jyotishtoma", "A^ya": "Ajya", "c^ya": "ajya", "£t^ya": "ajya", "Svish^akret": "Svishtakrit",
    "Darvt-offering": "Darvi-offering", "Brahma>£arins": "Brahmacharins", "Brahma^aspati": "Brahmanaspati",
    "Grzhasthas": "Grihasthas", "Dfkshd": "Diksha", "Dikshd": "Diksha", "Dlksha": "Diksha",
    "Dakshi^a": "Dakshina", "Dakshind": "Dakshina", "Dakshini": "Dakshina", "Dakshma": "Dakshina",
    "Puronuvakyd": "Puronuvakya", "Puronuvakyi": "Puronuvakya", "Puronuvdkyi": "Puronuvakya",
    "Ya^-yi": "Yajya", "Y^yi": "Yajya", "Ya^ya": "Yajya", "Yagya": "Yajya", "SasyaZ": "Sasya", "Sasyd": "Sasya",
    "£asya": "Sasya", "»5asya": "Sasya", "Ya^us": "Yajus", "Ya^us-verses": "Yajus-verses", "Riky": "Rik,", "SAman": "Saman",
    "Sciman": "Saman", "Sctma-veda": "Sama-veda", "Sima-veda": "Sama-veda", "Ya^/^shi": "Yajumshi", "Itihisa": "Itihasa",
    "Pura^a": "Purana", "Vidyd": "Vidya", "SAtras": "Sutras", "Stitras": "Sutras",
    "Anuvyakhyinas": "Anuvyakhyanas", "Atharvingirasas": "Atharvangirasas", "61oka": "Sloka",
    "61okas": "Slokas", "vSlokas": "Slokas", "Gayatrf": "Gayatri", "Gayatrl": "Gayatri", "Savitrl": "Savitri",
    "Anush/ubh": "Anushtubh", "Udgttha": "Udgitha", "udgftha": "udgitha", "Gttha": "githa", "gltha": "githa",
    "Udgatrt": "Udgatri", "pavaminas": "pavamanas", "Pavamina": "Pavamana", "Atigriha": "Atigraha",
    "madhu-vidyd": "madhu-vidya", "madhu-vidyi": "madhu-vidya", "Stkratman": "Sutratman",
    "Svahd": "Svaha", "Svahi": "Svaha", "Svcthi": "Svaha", "Svdhd": "Svaha", "Svihd": "Svaha", "Sv£ha": "Svaha",
    "SvSM": "Svaha", "SvAhal": "Svaha!", "Vasha/": "Vashat", "Vasha^": "Vashat",
    "Bhdr": "Bhuh", "Bhtir": "Bhuh", "BhM": "Bhuh", "Bhuva^": "Bhuvah", "Bhuva>£": "Bhuvah",
    "Sva^": "Svah", "Sva/£": "Svah", "Sva>£": "Svah", "Hari/£": "Harih",
    # words in brackets and the Sanskrit Müller left untranslated
    "/£akshus": "chakshus", ">£amasa": "chamasa", ">£aturtha": "chaturtha", "^*ahdti": "jahati",
    "^ahati": "jahati", "^andra-tarakam": "chandra-tarakam", "^anendriyas": "jnanendriyas",
    "^iva": "jiva", "frvara": "isvara", "fra": "isa", "an-faa": "an-isa", "^raddhi": "sraddha",
    "^rotra": "srotra", "vi^anatma": "vijnanatma", "gu^a": "guna", "Gu^as": "Gunas", "guns": "gunas",
    "miyin": "mayin", "aklsa": "akasa", "iklsa": "akasa", "dua^": "disah", "disa^": "disah",
    "te^as": "tejas", "dharma^": "dharmah", "ihuti": "ahuti", "itman": "atman", "dtman": "atman",
    "dsye": "asye", "Dtir": "Dur", "dtiran": "duran", "ptirva": "purva", "pti^artham": "pujartham",
    "ish^i": "ishti", "atrznada": "atrinada", "atrz/zada": "atrinada", "ariate": "archate",
    "antaryimin": "antaryamin", "adhibhiitam": "adhibhutam", "devatcl": "devata", "devatd": "devata",
    "devati": "devata", "ddadana^": "adadanah", "danrata": "darsata", "dar^atam": "darsatam",
    "parora^as": "parorajas", "kshamto^": "kshanitoh", "tatre": "tatre", "va/£": "vach", "ya£": "vach",
    "Dayadham": "Dayadhvam", "pra^a": "prana", "Pra^a": "Prana", "PrA^a": "Prana", "pri^a": "prana",
    "Prina": "Prana", "prina": "prana", "pra?za": "prana", "pra^as": "pranas", "Pra^as": "Pranas",
    "pri^as": "pranas", "prinas": "pranas", "prd^as": "pranas", "prdnas": "pranas", "prfi^as": "pranas",
    "pr^as": "pranas", "pr£/zas": "pranas", "prazzas": "pranas", "pr&zzas": "pranas", "Udina": "Udana",
    "Brdhma^a": "Brahmana", "Brihma^a": "Brahmana", "Brihma^as": "Brahmanas", "Brahma#as": "Brahmanas",
    "Brahma^a": "Brahmana", "Brahma^as": "Brahmanas", "ra^an": "rajan", "vish/ani": "vishtani",
    "pratish/M": "pratishtha", "Rishx": "Rishi", "jRzshi": "Rishi", "JZtshi": "Rishi", "Rtshi": "Rishi",
    "Rzshi": "Rishi", "Ya^*ur-veda": "Yajur-veda", "Catavedas": "Jatavedas", "Hira^mayl": "Hiranmayi",
    "dhtmahi": "dhimahi", "na^": "nah", "pro^odayat": "prachodayat", "kidneybeans": "kidney-beans",
    "brthiyavas": "vrihiyavas", "amipriyangavas": "anupriyangavas", "godhilmas": "godhumas",
    "masfiras": "masuras", "prishadajya": "prishadajya", "p/Vshada^ya": "prishadajya",
    "pWshada^ya": "prishadajya", "Ta.mz": "Tam", "Xz.m": "Tam", "tarn": "tam", "pra^^a^": "prancham",
    "abhyasrz^at": "abhyasrijat", "Tasyi": "Tasya", "barhi^": "barhih", "^armadhishavane": "charmadhishavane",
    "va^apeyena": "vajapeyena", "ya^amanasya": "yajamanasya", "eva/^": "evam", "eva^": "evam",
    "adhopahctsa;^": "adhopahasam", "adhopahasaw": "adhopahasam", "^araty": "charaty", "/£araty": "charaty",
    "striya/k": "striyah", "vringaXe": "vrinkte", "brahma^iyana": "brahmanayana", "nirindriyi": "nirindriya",
    "visukrito'smal": "visukrito 'smal", "avidvd;^so": "avidvamso", "dhopahasa^": "dhopahasam",
    "^arantfti": "charantiti", "reta/£": "retah", "reta^": "retah", "abhimrzVed": "abhimrised",
    "abhimrised": "abhimrised", "prethivlm": "prithivim", "apa^": "apah", "aha^": "aham", "tegah": "tejah",
    "bhaga^": "bhagah", "anamikangushMabhyam": "anamikangushthabhyam", "Vcl": "va", "nimrzVz^yat": "nimrijyat",
    "nimrishyat": "nimrijyat", "\\kkhzX": "ichchhet", "\\kkha\\": "ichchhen", "iaMed": "ichchhed",
    "artha^": "artham", "arthaw": "artham", "nish/dya": "nishthaya", "nish/iya": "nishthaya",
    "nish/aya": "nishthaya", "nish^iya": "nishthaya", "mukha^": "mukham", "mukha/^": "mukham",
    "mukhaw": "mukham", "abhimrzVya": "abhimrisya", "abhimrisya": "abhimrisya", "^aped": "japed",
    "^ayase": "jayase", "arigakashayo": "angakashayo", "amftm": "amum", "mayfti": "mayiti",
    "garbhaw": "garbham", "Garbhaw": "Garbham", "garbha^": "garbham", "garbha/^": "garbham",
    "sandhayabhipraTzyapanyid": "sandhayabhipranyapanyat", "indriye^a": "indriyena", "ddada": "adadha",
    "areti": "areta", "retasS": "retasa", "sandhayapanyabhipra^yad": "sandhayapanyabhipranyad",
    "ddadhamtti": "adadhamiti", "garbhi^y": "garbhiny", "tirta": "uru", "vi^ihithaw": "vijihitham",
    "dyavaprithivl": "dyavaprithivi", "sandhiya": "sandhaya", "anumirshrf": "anumarshti",
    "Vish/mr": "Vishnur", "yomm": "yonim", "Tvash^l": "Tvashta", "rftpam": "rupani", "pi^iatu": "pimsatu",
    "asia£atu": "asinchatu", "DhitS": "Dhata", "prz'thush/uke": "prithushtuke",
    "prithush/uke": "prithushtuke", "adhattdm": "adhattam", "pushkarasra^au": "pushkarasrajau",
    "ara/^1": "arani", "ara/^": "arani", "yabhya^": "yabhyam", "da^ame": "dasame", "mdsi": "masi",
    "stitave": "sutave", "Yathagnigarbhd": "Yathagnigarbha", "prrthivt": "prithivi", "indre^a": "indrena",
    "garbhmf": "garbhini", "viyur": "vayur", "d\\sain": "disam", "Soshyantlm6adbhirabhyukshati":
    "Soshyantim adbhir abhyukshati", "Yathivayu^7": "Yatha vayuh", "Yathivayu^": "Yatha vayuh",
    "pushkari^i^": "pushkarinim", "sami^ayati": "samingayati", "sarvata^": "sarvatah", "e^atu": "ejatu",
    "^arayuna": "jarayuna", "Indrasyiya^": "Indrasyayam", "vra^a^": "vrajah", "kritak": "kritah",
    "Sclrga/a^": "sargalah", "sapari^raya^": "saparisrayah", "nir^ahi": "nirjahi", "garbhe^a": "garbhena",
    "sivari^": "savaram", "upaslta": "upasita", "skandati": "skandati",
    # English words the scan broke
    "orno": "or no", "bytouch": "by touch", "calledturtya": "called turiya", "wrorld": "world", "wTas": "was",
    "bf": "of", "halfmonths": "half-months", "fAnd": "'And", "Tf": "'If", "2The": "The", "and^": "and",
    "t(i": "ti", "Viyu": "Vayu", "SvaM": "Svaha", "Gabala": "Jabala", "Silrya": "Surya", "Gafgi": "Gargi", "Vir^": "Viraj", "srish/vadha": "srishtvadha", "askdntsid": "askantsid",
    "yathasthanaw": "yathasthanam", "Puri^a-vidyi": "Purana-vidya",
}

PHRASES = [("./?zg-veda", "Rig-veda"), ("S valid", "Svaha"), ("(Janaka", "Janaka"),
           ("(-rclnaki", "Janaki"), ("(Janaki", "Janaki")]

# Corrections to single verses, made on the cleaned text: (wrong, right) pairs that must match.
SU_FIXES = {
    "2.2": [("Savitre", "Savitri")],
    "2.11": [("a crystal moon", "a crystal moon.")],
    "2.15": [("natures l> he", "natures, he")],
    "4.20": [("immortal.)", "immortal.")],
    "5.6": [("Brahmi (Hiranyagarbha)", "Brahma (Hiranyagarbha)")],
    "5.9": [("hundredth part. of", "hundredth part of")],
    "6.21": [("Svetas, vatara", "Svetasvatara")],
}
BU_FIXES = {
    "1.3.17": [("entered all into, him", "entered all into him")],
    "1.3.27": [("When he says, (Lead me", "When he says, 'Lead me")],
    "1.4.7": [("can say.' He, called", "can say, 'He, called"), ("Let men j worship", "Let men worship"),
              ("are one.' This Self", "are one. This Self")],
    "1.5.21": [("called after him 'breaths'", "called after him, 'breaths'")],
    "1.4.17": [("with the, body", "with the body"), ("sacrifice, for,' fivefold", "sacrifice, for fivefold")],
    "1.5.2": [("that he eats food with his face,'", "that 'he eats food with his face,'")],
    "2.1.3": [("as Brahman,' hga~ tasatru said", "as Brahman.' Ajatasatru said")],
    "3.1": [("(Paramatman)! u", "(Paramatman)!")],
    "3.1.2": [("'O glory of the Saman / and drove", "'O glory of the Saman,' and drove"), ("Then A^vala", "Then Asvala")],
    "3.1.6": [("(staircase.)", "(staircase).")],
    "3.1.7": [("by them?' All whatsoever", "by them?' 'All whatsoever")],
    "3.1.8": [("sink down /' What does", "sink down.' 'What does"), ("(noisy) By those", "(noisy). By those")],
    "3.1.9": [("'And which is it?' i The mind", "'And which is it?' 'The mind")],
    "3.1.10": [("by the Sasya After", "by the Sasya.' After")],
    "3.2.1": [("asked. 'Yagifar valkya,'", "asked. 'Yajnavalkya,'")],
    "3.3.1": [("We asked him.' Who art thou?'", "We asked him: 'Who art thou?'")],
    "3.4.2": [("Everything also is of evil.", "Everything else is of evil.")],
    "3.8.11": [("'That Brahman.' O Gargi,", "'That Brahman,' O Gargi,")],
    "3.9.1": [("^v< One,' he said", "'One,' he said")],
    "3.9.3": [("'Who are the Vasus.'", "'Who are the Vasus?'")],
    "3.9.13": [("of whom thou speakest The person", "of whom thou speakest. The person")],
    "3.9.27": [("all of you. But those", "all of you.' But those")],
    "3.9.28": [('"from seed.\'\' for', '"from seed," for'), ("again?' brahman,", "again? 'Brahman,")],
    "3.6.1": [("to ask too much Do not", "to ask too much. Do not")],
    "3.7.10": [("the immortal'", "the immortal.'")],
    "4.1.3": [("Yajnavalkya said: c Let us", "Yajnavalkya said: 'Let us"),
              ("said: (He did not tell me?'", "said: 'He did not tell me.'"), ("dear); 'because", "dear); because")],
    "4.1.5": [("Yajnavalkya said; 'The ear", "Yajnavalkya said: 'The ear")],
    "4.3.11": [("these verses; 'After", "these verses: 'After")],
    "4.3.14": [("when asleep.' No, here", "when asleep.\" No, here")],
    "4.3.15": [("to dream And whatever", "to dream. And whatever"), ("attached o anything", "attached to anything")],
    "4.3.20": [("\"I am this altogether.'' that", "\"I am this altogether,\" that")],
    "4.4.1": [("into the heart When", "into the heart. When")],
    "4.4.6": [("a mans own mind", "a man's own mind")],
    "4.5.4": [("tell that clearly to me?'", "tell that clearly to me.'")],
    "4.5.14": [("But he replied: (O Maitreyi", "But he replied: 'O Maitreyi")],
    "5.5.1": [("another ti), the third", "another ti, the third")],
    "5.8.1": [("Svaha, Vasha/, Hanta, and Svadha The gods", "Svaha, Vashat, Hanta, and Svadha. The gods")],
    "5.12.1": [("Pratrida. said", "Pratrida said")],
    "5.13.2": [("breath is Yajnas", "breath is Yajus")],
    "5.14.6": [("above the skies', cannot", "above the skies,' cannot")],
    "5.14.8": [("and earnest me?", "and carriest me?")],
    "6.1.13": [("might tare up", "might tear up")],
    "6.1.14": [("He said: (What shall", "He said: 'What shall")],
    "6.2.1": [("taught by your father'", "taught by your father?'")],
    "6.2.15": [("(ar- >£is)", "(archis)")],
    "6.2.16": [("(see §)", "(see § 11)")],
    "6.3.1": [("according to rule prepares", "according to rule, prepares")],
    "6.3.6": [("Svah (heaven) Svaha I'", "Svah (heaven) Svaha!'")],
    "6.3.12": [("Satyakama Arabella", "Satyakama Jabala")],
    "6.3.13": [("clarified butter (ag ya)", "clarified butter (ajya)")],
    "6.4.6": [("whose garments are pure Therefore", "whose garments are pure. Therefore")],
    "6.4.12": [("I here V f Thou", "I here.' 'Thou")],
    "6.4.13": [("make her pound rice", "make her pound rice.")],
    "6.2.3": [("and said -:", "and said:")],
    "6.4.20": [("says: T am Ama", "says: 'I am Ama"), ("thou art S, (speech)", "thou art Sa (speech)")],
    "2.1.16": [("did not know this?", "did not know this.")],
    "2.1.17": [("in the heart When", "in the heart. When")],
    "2.2.3": [("Sloka: c There", "Sloka: 'There")],
    "2.3.5": [("are Indefinite", "are indefinite")],
    "2.3.6": [("the name the True of the True,'", "the name 'the True of the True,'")],
    "2.4.3": [("tell that to me?'", "tell that to me.'")],
    "2.4.5": [("the Self, / therefore", "the Self, therefore"), ("the Devas are dear, 'Verily", "the Devas are dear. 'Verily"),
              ("everything is not dear that", "everything is not dear, that")],
    "2.4.6": [("all is that Self,", "all is that Self.")],
    "2.4.14": [("salute n another", "salute another")],
    "2.5.17": [("(Rv. 1, 117, 22)", "(Rv. I, 117, 22)"), ("that of Tvash/r,' and", "that of Tvashtri and")],
    "2.5.18": [("the puri- ^raya,", "the purisaya,")],
    "2.5.19": [("(Rv. VI, 47,18)", "(Rv. VI, 47, 18)"), ("many and endless This", "many and endless. This")],
}


# --------------------------------------------------------------------------- the two Upanishads
def _read(path):
    return open(path, encoding="utf-8").read().split("\n")


def _slice(L, start, end, after=None):
    i0 = next(i for i, s in enumerate(L) if re.search(after, s)) if after else 0
    a = next(i for i in range(i0, len(L)) if re.search(start, L[i]))
    b = next(i for i in range(a + 1, len(L)) if re.search(end, L[i]))
    return L[a:b]


def _sections(verses, vocab, bu, labels, names, intro, log=lambda s: None):
    del _MISSED[:]
    secs = []
    for adh, br, n, lines, head in verses:
        if adh > len(secs):
            sec = {"label": labels[adh - 1], "short": str(adh), "name": names[adh - 1]}
            if adh == 1:
                sec["intro"] = intro
            sec["verses"] = []
            secs.append(sec)
        ref = f"{adh}.{br}.{n}" if bu else f"{adh}.{n}"
        vamsa = bu and (adh, br) in ((2, 6), (4, 6), (6, 5))
        v = {"n": len(secs[-1]["verses"]) + 1, "ref": ref,
             "en": clean(lines, ref if n else ref.rsplit(".", 1)[0], vocab, vamsa, BU_FIXES if bu else SU_FIXES)}
        if bu and ref in RESTORED_BU:
            log(f"RESTORED {ref}: {v['en']}")
            v["en"] = RESTORED_BU[ref]
        if n == 0:
            v["ref"] = f"{adh}.{br}" if bu else str(adh)
        if bu and (n == 0 or (n == 1 and not (secs[-1]["verses"] and secs[-1]["verses"][-1]["ref"] == f"{adh}.{br}"))):
            v["head"] = f"{ORD[br - 1].capitalize()} Brahmana"
        secs[-1]["verses"].append(v)
    if _MISSED and os.environ.get("SBE15_LENIENT") != "1":
        raise ValueError("verse fixes not found:\n" + "\n".join(_MISSED))
    for m in _MISSED:
        log("MISSED " + m)
    return {"sections": secs}


ADHYAYAS = [f"{o.capitalize()} Adhyaya" for o in ORD[:6]]

BU_NAMES = ["The horse of the sacrifice; the Self alone in the beginning",
            "Gargya and Ajatasatru; Yajnavalkya and Maitreyi",
            "Yajnavalkya at Janaka's court",
            "Yajnavalkya teaches Janaka; the Self that is not this, not this",
            "The full and the full; Da, Da, Da",
            "The senses and breath; the five fires; the teachers"]
BU_INTRO = [
    "The longest of the principal Upanishads and among the oldest, the Brihadaranyaka, 'the great "
    "forest teaching', belongs to the White Yajur Veda and forms the closing part of the Satapatha "
    "Brahmana. At its heart stands the sage Yajnavalkya: his contest with Gargi and the other "
    "learned Brahmanas at the court of King Janaka, his teaching of Janaka himself, and his parting "
    "words to his wife Maitreyi on the Self for whose sake all things are dear. Here the Self is "
    "described only as 'not this, not this' (neti, neti, which Müller renders 'No, no!'), and here "
    "is the prayer 'Lead me from the unreal to the real, from darkness to light, from death to "
    "immortality' (1.3.27 in Müller's numbering, 1.3.28 in most editions)."]
SU_NAMES = ["What is the cause? The wheel of Brahman",
            "The practice of Yoga",
            "Rudra, the one God; the Person beyond darkness",
            "The one who rules every womb; two birds on one tree",
            "Knowledge and ignorance; the soul and its bodies",
            "The greatness of God; the highest devotion"]
SU_INTRO = [
    "The Svetasvatara belongs to the Black Yajur Veda and is the most theistic of the principal "
    "Upanishads: it names Rudra, the blessed Siva, as the one God who creates and rules the world, "
    "dwells hidden in all beings and is known in the heart. Beside the Vedanta it draws on early "
    "ideas of Sankhya, gives one of the oldest descriptions of the practice of Yoga, and in its "
    "last verse speaks of the highest devotion (bhakti) to God, and to one's Guru as to God."]


def brihadaranyaka(ocr_path, log=lambda s: None):
    L = _read(ocr_path)
    lines = _slice(L, r"^FIRST\s+ADHYAYA", r"^SVETASVATARA-", after=r"HADARA.VYAKA-\s*$")
    verses = parse(lines, True, log)
    return _sections(verses, _vocab(L), True, ADHYAYAS, BU_NAMES, BU_INTRO, log)


def svetasvatara(ocr_path, log=lambda s: None):
    L = _read(ocr_path)
    lines = _slice(L, r"^FIRST\s+ADHYAYA", r"^PRA\S{1,3}A-UPANISHAD", after=r"^SVETASVATARA-")
    verses = parse(lines, False, log)
    return _sections(verses, _vocab(L), False, ADHYAYAS, SU_NAMES, SU_INTRO, log)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    if len(sys.argv) > 2:
        out = sys.argv[2]
    elif os.environ.get("S"):
        out = os.path.join(os.environ["S"], "sbe15_review")
    else:
        sys.exit("give an output directory (or set $S)")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("brihadaranyaka", brihadaranyaka), ("svetasvatara", svetasvatara)):
        data = fn(path)
        with open(os.path.join(out, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        with open(os.path.join(out, name + ".txt"), "w", encoding="utf-8") as f:
            for sec in data["sections"]:
                f.write(f"\n=== {sec['label']}: {sec['name']}\n")
                for line in sec.get("intro", []):
                    f.write(line + "\n")
                for v in sec["verses"]:
                    f.write(("\n[%s]\n" % v["head"] if v.get("head") else "") + f"{v['ref']}  {v['en']}\n")
        counts = [len(sec["verses"]) for sec in data["sections"]]
        print(f"{name}: {counts} = {sum(counts)} verses -> {out}")


if __name__ == "__main__":
    main()
