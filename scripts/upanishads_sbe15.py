#!/usr/bin/env python3
"""Draft parser (stage 1)."""
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
    ("* For when there is as it were duality, then one", "14. For when there is as it were duality, then one"),
]


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


def parse(lines, bu=True, log=print):
    """Return list of (adhyaya, brahmana, verse, [lines])."""
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
            w = _width(p)
            if (k == 0 and note_open and w >= 60) or (k > 0 and w >= 58):
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
    words, hyph = vocab
    out = ""
    for ln in lines:
        if not out:
            out = ln
            continue
        m = re.search(r"(\S*?)-$", out)
        if m and m.group(1) and re.match(r"[a-z]", ln):
            left = re.sub(r"^.*[^\w&^/#£]", "", m.group(1))
            right = re.match(r"[\w&^/#£]*", ln).group(0)
            l2, r2 = re.sub(r"\d+$", "", left).lower(), re.sub(r"\d+$", "", right).lower()
            keep = (f"{l2}-{r2}" in hyph or l2 in KEEP_HYPHEN_LEFT or f"{l2}-{r2}" in KEEP_HYPHEN) and \
                f"{l2}{r2}" not in JOIN_HYPHEN
            _HYPHENS.append((l2, r2, keep))
            out = out + ln if keep else out[:-1] + ln
        else:
            out += " " + ln
    return out


_HYPHENS = []                      # (left, right, kept) for every line-end hyphen, for review
KEEP_HYPHEN_LEFT = {"self"}
KEEP_HYPHEN = {"half-months", "meeting-place", "kidney-beans", "back-breathing"}
JOIN_HYPHEN = set()


def _footnotes(t, vamsa=False):
    """Drop the footnote numbers (and the odd sign standing for one) from the English."""
    keep = []

    def protect(x):
        keep.append(x)
        return f"{_PROTECT}{len(keep) - 1}{_PROTECT}"
    t = re.sub(r"\((?:Rv|No)\. [^)]*\)", lambda m: protect(m.group(0)), t)   # (Rv. I, 189, 1.), (No. 36)
    t = re.sub(r"\(([1-9il])\)", lambda m: protect("(%s)" % m.group(1).replace("i", "1").replace("l", "1")), t)
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
        t = re.sub(a, b, t)
    return t


# --------------------------------------------------------------------------- quotes and spacing
_QUESTION = re.compile(r"(?:(?:And|But|Then|Now|O \w+,)\s+)?(?:(?:in|by|for|to|from|on|with|of|at)\s+)?"
                       r"(?:what|who|whom|whose|which|where|whither|whence|when|how|why|is|are|was|were|do|does|"
                       r"did|dost|didst|can|canst|shall|will|wilt|hast|hath|art|knowest|has|have|may|whether)\b",
                       re.I)


_SAID = r"(?:he|she|they|it|said|replied|answered|asked|says|saying|thus|quoth|so|with|thinking)\b"


def _prequotes(t):
    """Opening quotes the scan read as a digit or letter (before footnote numbers are dropped)."""
    t = re.sub(r"(?<=[:;,] )[1li] (?=[A-Z])", "'", t)                      # : 1 Thou art -> : 'Thou art
    return re.sub(r"^1 (?=[A-Z])", "'", t)


def _quotes(t):
    t = re.sub(r"(^|\s)[*•]\s*(?=[A-Z'\"(])", r"\1'", t)                 # * as an opening quote
    t = re.sub(r"(^|\s)\*\s*(?=[a-z])", r"\1'", t)
    t = re.sub(r"\s•\s", " ", t)

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
        if not p or p in ":;(—'\"" or re.search(r"\(\d\)$", before):
            return " " + q                                                 # opening
        if re.match(_SAID, after):
            return ("" if p in ".?!," else ",") + q + " "                  # Yajnavalkya,' he said
        if inside(before, q):
            return q + " "                                                 # closing
        return " " + q
    t = re.sub(r"(?:^|\s+)(['\"])\s+", lone, t)
    return t


def _tidy(t):
    t = re.sub(r"\s+", " ", t).strip()
    t = re.sub(r"\s*—\s*|\s+-\s+|--", "—", t)
    t = re.sub(r"\s+([,.;:!?)\]])", r"\1", t)
    t = re.sub(r"([(\[])\s+", r"\1", t)
    t = re.sub(r"\s+(['\"])(?=[\s,.;:!?)]|$)", r"\1", t)                    # closing quotes
    t = re.sub(r"(?<=[,;:])(?=[A-Za-z(])", " ", t)
    t = re.sub(r"&c(?![.])", "&c.", t)
    t = re.sub(r"\bi\. ?e\.?(?=[\s,)])", "i.e.", t)
    t = re.sub(r"\.\.(?!\.)", ".", t)
    return t


def _english(t):
    for a, b in ENGLISH:
        t = re.sub(a, b, t)
    return t


def clean(lines, ref, vocab, vamsa=False, fixes=None):
    t = _join(lines, vocab)
    t = re.sub(r"\s+", " ", t)
    t = _sanskrit(t)
    t = _prequotes(t)
    t = _footnotes(t, vamsa)
    t = _quotes(t)
    t = _english(t)
    t = _tidy(t)
    for a, b in (fixes or {}).get(ref, []):
        if a not in t:
            raise ValueError(f"{ref}: fix not found: {a!r}")
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
    "t(i": "ti", "Gafgi": "Gargi", "Vir^": "Viraj", "srish/vadha": "srishtvadha", "askdntsid": "askantsid",
    "yathasthanaw": "yathasthanam", "Puri^a-vidyi": "Purana-vidya",
}

PHRASES = []
ENGLISH = []

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
    secs = []
    for adh, br, n, lines, head in verses:
        if adh > len(secs):
            secs.append({"label": labels[adh - 1], "short": str(adh), "name": names[adh - 1], "verses": []})
            if adh == 1:
                secs[0]["intro"] = intro
                secs[0]["verses"] = []
        ref = f"{adh}.{br}.{n}" if bu else f"{adh}.{n}"
        vamsa = bu and (adh, br) in ((2, 6), (4, 6), (6, 5))
        v = {"n": len(secs[-1]["verses"]) + 1, "ref": ref,
             "en": clean(lines, ref if n else ref.rsplit(".", 1)[0], vocab, vamsa, BU_FIXES if bu else SU_FIXES)}
        if n == 0:
            v["ref"] = f"{adh}.{br}" if bu else str(adh)
        if bu and (n == 0 or (n == 1 and not (secs[-1]["verses"] and secs[-1]["verses"][-1]["ref"] == f"{adh}.{br}"))):
            v["head"] = f"{ORD[br - 1].capitalize()} Brahmana"
        secs[-1]["verses"].append(v)
    return {"sections": secs}


ADHYAYAS = [f"{o.capitalize()} Adhyaya" for o in ORD[:6]]

BU_NAMES = ["The horse of the sacrifice; the Self alone in the beginning",
            "Gargya and Ajatasatru; Yajnavalkya and Maitreyi",
            "Yajnavalkya at Janaka's court",
            "Yajnavalkya teaches Janaka; the Self that is not this, not this",
            "The full and the full; Da, Da, Da",
            "The five fires; the teachers"]
BU_INTRO = ["..."]
SU_NAMES = ["", "", "", "", "", ""]
SU_INTRO = ["..."]


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
        sys.exit("usage: upanishads_sbe15.py <ocr.txt> [out_dir]")
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.environ.get("S", os.path.dirname(os.path.abspath(path))), "sbe15_review")
    os.makedirs(out, exist_ok=True)
    for name, fn in (("brihadaranyaka", brihadaranyaka), ("svetasvatara", svetasvatara)):
        data = fn(path)
        with open(os.path.join(out, name + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
        with open(os.path.join(out, name + ".txt"), "w", encoding="utf-8") as f:
            for s in data["sections"]:
                f.write(f"\n=== {s['label']} — {s['name']}\n")
                for v in s["verses"]:
                    f.write(("\n[%s]\n" % v["head"] if v.get("head") else "") + f"{v['ref']}  {v['en']}\n")
        counts = [len(s["verses"]) for s in data["sections"]]
        print(f"{name}: {counts} = {sum(counts)} verses -> {out}")


if __name__ == "__main__":
    main()
