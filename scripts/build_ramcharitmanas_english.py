#!/usr/bin/env python3
"""Add F. S. Growse's English translation of the Ramcharitmanas (public domain) to texts/ramcharitmanas.

Usage:
  python3 scripts/build_ramcharitmanas_english.py GROWSE_1922.txt GROWSE_1914.txt

The two files are the Internet Archive's OCR text of two printings of Growse's translation
(archive.org/details/ramayanaoftulsid0000unse, 1922, and archive.org/details/rmyanaoftuls00tulauoft,
1914). The 1922 scan is the cleaner and is the one used; where it has a misread word and the 1914 scan
has a likelier one at the same place, the 1914 reading is taken.

Growse translates in prose, a paragraph or two for each chaupai group and its closing doha, under
headings ("Chaupai", "Doha 12") that do not always follow the standard numbering. Each passage is
matched to the app's sections ("Doha N") by its length and the names in it, in order, and stored as
the section's "trans" paragraphs. Page headings, footnotes and footnote marks are dropped.
"""
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher, get_close_matches

TEXTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")
HEADERS = re.compile(r"^\W*\d*\s*(?:[A-Z][A-Za-z]{0,3}\s+)?(?:[COZ]?[HB]?ILDHOOD|OHILDHOOD|OBILDHOOD|CHILDHOOD|AYOD\w*|THE\s+FOREST|KISH\w*|"
                     r"THE\s+BEA\w*|LAN\w*|TH\w\s+S\w+|THE\s+RAMAYANA|INTRODUCTION)\W*\d*\W*$")
MARK = re.compile(r"^\W{0,4}(?P<kind>Chaup|Chaap|Ohaup|Chap|Doh|Dob|Sor|Chhan|Ohhan|Chban)\S*(?P<rest>.{0,14})$")
SANSKRIT = re.compile(r"^\W{0,3}Sanskrit\s+\S*nvocation\W*$")


def norm(w):
    w = unicodedata.normalize("NFKD", w)
    return re.sub(r"[^a-z]", "", w.lower())


# ---------------------------------------------------------------------------------------------
# Cleaning the OCR text

def paragraphs(text):
    """The body text as paragraphs, with page headings and footnotes removed."""
    paras, cur = [], []
    for raw in text.split("\n"):
        line = raw.strip()
        if not line:
            if cur:
                paras.append(cur)
                cur = []
            continue
        if HEADERS.match(line) and len(line) < 34 and not MARK.match(line):
            if cur:
                paras.append(cur)
                cur = []
            paras.append(["<page>"])
            continue
        if re.match(r"^R\W{0,3}\d+\s*$", line) or not re.search(r"[A-Za-z]{2}", line):
            continue
        cur.append(line)
    if cur:
        paras.append(cur)
    return paras


def is_footnote(lines, body_width):
    first = lines[0]
    if re.match(r"^[*‘'“\W]{0,3}\d{1,2}\s+[A-Z“‘\"'(]", first) or re.match(r"^[*†‡§]\s", first):
        return True
    # Footnotes are set in smaller type, so their lines are longer than the body's.
    full = [len(l) for l in lines[:-1]] or [len(lines[0])]
    return len(lines) >= 2 and sorted(full)[len(full) // 2] > body_width + 7


def join_lines(lines):
    out = ""
    for l in lines:
        if not out:
            out = l
        elif out.endswith("-") and re.match(r"[a-z]", l):
            out = out[:-1] + "­" + l          # a soft hyphen, settled later against the vocabulary
        else:
            out += " " + l
    return re.sub(r"\s+", " ", out).strip()


def blocks_of(text):
    """[(kind, label, [paragraph])], kind being chaupai, doha, chhand, invocation, end or text."""
    paras = paragraphs(text)
    widths = sorted(len(l) for p in paras for l in p if len(p) > 3 for _ in [0])
    body_width = widths[int(len(widths) * 0.6)] if widths else 60
    blocks = [("text", "", [])]
    for p in paras:
        if p == ["<page>"]:
            blocks[-1][2].append("<page>")
            continue
        m = MARK.match(p[0]) if len(p[0]) < 24 else None
        if m:
            k = m.group("kind").lower()
            kind = "chaupai" if k.startswith(("chau", "chaa", "ohau", "chap")) else "chhand" if "hhan" in k or "hban" in k else "doha"
            blocks.append((kind, m.group("rest").strip(), []))
            p = p[1:]
            if not p:
                continue
        elif SANSKRIT.match(p[0]):
            blocks.append(("invocation", "", []))
            continue
        elif re.match(r"^\W{0,3}[TL]hus\s+end", p[0]):
            blocks.append(("end", "", [join_lines(p)]))
            blocks.append(("text", "", []))
            continue
        if is_footnote(p, body_width):
            continue
        blocks[-1][2].append(join_lines(p))
    # A paragraph broken by a page (and the footnotes at its foot) is joined up again.
    out = []
    for kind, label, ps in blocks:
        merged = []
        for x in ps:
            if x == "<page>":
                merged.append(x)
                continue
            # (a scrap of a footnote left between the two halves is dropped)
            if len(merged) >= 3 and merged[-1] == "<page>" and len(merged[-2]) < 45 and not re.search(r"[.!?:;’”'\"]\W*$", merged[-3]) and re.match(r"[a-z]", x):
                merged.pop()
                merged.pop()
                merged[-1] += " " + x
            elif len(merged) >= 2 and merged[-1] == "<page>" and not re.search(r"[.!?:;’”'\"]\W*$", merged[-2]) and re.match(r"[a-z]", x):
                merged.pop()
                merged[-1] += " " + x
            else:
                if merged and merged[-1] == "<page>":
                    merged.pop()
                merged.append(x)
        out.append((kind, label, [m for m in merged if m != "<page>"]))
    return out


def books_of(blocks):
    """Split where each book's Sanskrit invocation begins; the introduction before Book I, the
    closing line of each book and its title are dropped."""
    books, closed = [], True
    for b in blocks:
        if b[0] == "invocation":
            books.append([])
            closed = False
        if b[0] == "end":
            closed = True          # the title pages, plates and printer's notes that follow are not text
        elif not closed:
            books[-1].append(b)
    for book in books:
        while book and book[-1][0] == "text" and all(re.match(r"^\W*BOOK\b", p) or len(p) < 30 for p in book[-1][2]):
            book.pop()
    return books


# ---------------------------------------------------------------------------------------------
# Filling pages missing from the 1922 scan from the 1914 one

FOOTNOTE_CUES = re.compile(r"Professor|dictionary|etymology|\bcf\.|derived from", re.I)


def events_of(book):
    ev = []
    for kind, label, ps in book:
        ev.append(("mark", kind, label))
        ev.extend(("para", p) for p in ps)
    return ev


def blocks_from(ev):
    blocks = []
    for e in ev:
        if e[0] == "mark":
            blocks.append((e[1], e[2], []))
        elif blocks:
            blocks[-1][2].append(e[1])
    return blocks


def fill_gaps(book, other):
    """Where the 1914 text has a long passage (60 words or more) that the 1922 scan lacks, a page
    missing from the scan, put it in, with the headings it carries. Footnotes are left out."""
    ev, ev14 = events_of(book), events_of(other)
    toks = [(e, t) for e, x in enumerate(ev) if x[0] == "para" for t in TOKEN.findall(x[1])]
    toks14 = [(e, t) for e, x in enumerate(ev14) if x[0] == "para" for t in TOKEN.findall(x[1])]
    a = [norm(core(t)) for _, t in toks]
    b = [norm(core(t)) for _, t in toks14]
    inserts, dropped = {}, set()
    for op, i1, i2, j1, j2 in SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op not in ("insert", "replace") or (j2 - j1) - (i2 - i1) < 60:
            continue
        text = " ".join(t for _, t in toks14[j1:j2])
        if FOOTNOTE_CUES.search(text):
            continue
        new, last = [], None
        for e, t in toks14[j1:j2]:
            if e != last:
                prev = ev14[e - 1] if e else None
                first_tok = toks14.index((e, t)) == next(k for k, x in enumerate(toks14) if x[0] == e)
                if prev and prev[0] == "mark" and first_tok:
                    new.append(prev)
                new.append(["para", []])
                last = e
            new[-1][1].append(t)
        inserts[i1] = [x if x[0] == "mark" else ("para", " ".join(x[1])) for x in new]
        dropped.update(range(i1, i2))
    if not inserts:
        return book
    out, k = [], 0
    for e, x in enumerate(ev):
        if x[0] == "mark":
            out.append(x)
            continue
        cur = []
        for t in TOKEN.findall(x[1]):
            if k in inserts:
                if cur:
                    out.append(("para", " ".join(cur)))
                    cur = []
                out.extend(inserts[k])
            if k not in dropped:
                cur.append(t)
            k += 1
        if cur:
            out.append(("para", " ".join(cur)))
    if k in inserts:
        out.extend(inserts[k])
    return blocks_from(out)


# ---------------------------------------------------------------------------------------------
# Correcting misread words from the second scan

TOKEN = re.compile(r"\S+")


def core(tok):
    return re.sub(r"^[^\w­]+|[^\w­]+$", "", tok)


def strip_refs(tok):
    """A footnote mark printed after a word: honoured.! bards2 Magadhé? -> honoured. bards Magadhé"""
    t = re.sub(r"(?<=[A-Za-z.,;:’'”])[!?¹²³⁴\d*†]+$", "", tok) if len(tok) > 2 else tok
    return t or tok


def correct(paras, other_tokens, freq):
    toks = [strip_refs(t) for p in paras for t in TOKEN.findall(p)]
    a = [norm(core(t)) for t in toks]
    b = [norm(core(t)) for t in other_tokens]
    sm = SequenceMatcher(None, a, b, autojunk=False)
    fixes = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "replace" or i2 - i1 != j2 - j1:
            continue
        for i, j in zip(range(i1, i2), range(j1, j2)):
            x, y = a[i], b[j]
            if not y or x == y or freq[y] <= max(2, freq[x] * 4):
                continue
            if SequenceMatcher(None, x, y).ratio() < 0.6:
                continue
            fixes[i] = core(other_tokens[j])
    out, k = [], 0
    for p in paras:
        words = []
        for t in TOKEN.findall(p):
            t = strip_refs(t)
            if k in fixes:
                c = core(t)
                rep = fixes[k]
                if c and c[0].isupper() and rep[:1].islower():
                    rep = rep[0].upper() + rep[1:]
                t = t.replace(c, rep, 1) if c else t
            words.append(t)
            k += 1
        out.append(" ".join(words))
    return out


def settle_hyphens(p, freq):
    def fix(m):
        a, b = m.group(1), m.group(2)
        return a + b if freq[norm(a + b)] >= freq[norm(a)] + freq[norm(b)] or freq[norm(a + b)] > 0 else f"{a}-{b}"
    return re.sub(r"(\w+)­(\w+)", fix, p)


def word_counts(text):
    return Counter(re.sub(r"^[^A-Za-z\u00c0-\u024f]+|[^A-Za-z\u00c0-\u024f]+$", "", t) for t in TOKEN.findall(text))


def plain(w):
    return "".join(c for c in unicodedata.normalize("NFKD", w) if not unicodedata.combining(c))


ACCENT_MISREADS = "dé&i4áâàäëèêíìóôòúJ"


def polish(p, words, common):
    """Misread names put right from the rest of the text. Growse's long a (Ráma) is often read as
    d, é, & or i (Rdma, Réma, R&ma, Rima): where putting an a there gives a much commoner word,
    it is used. A rare word close to a common name is that name (Lakshraan, Vibhlshan). Growse's
    accents are dropped (Sítá -> Sita)."""
    def fix(m):
        w = m.group(0)
        n = words[w]
        if w[0].isupper():
            best, bc = None, 0
            for i, ch in enumerate(w):
                if ch in ACCENT_MISREADS:
                    for rep in ("a", "an"[:1]):
                        v = w[:i] + rep + w[i + 1:]
                        if words[v] > max(2 * n, 9) and words[v] > bc:
                            best, bc = v, words[v]
            if best:
                return plain(best)
            if n < 5 and len(w) >= 5:
                near = get_close_matches(w, common["cap"], 1, 0.8 if len(w) >= 7 else 0.85)
                if near and abs(len(near[0]) - len(w)) <= 1 and words[near[0]] >= 10 * max(n, 1):
                    return plain(near[0])
        return plain(w)
    return re.sub(r"[A-Za-z\u00c0-\u024f&]*[A-Za-z\u00c0-\u024f][A-Za-z\u00c0-\u024f&]*", fix, p)


def tidy(p):
    p = p.replace("­", "")
    p = re.sub(r"\s+([;:!?])", r"\1", p)            # Growse's spaced punctuation, closed up
    p = re.sub(r"\s+([,.])", r"\1", p)
    p = re.sub(r"‘‘|“", "“", p).replace("’’", "”")
    p = re.sub(r"([‘“'\"])\s*[*©¢]+\s*", r"\1", p)       # an opening quote misread with a speck after it
    p = re.sub(r"(^|\s)([‘“])\s+", r"\1\2", p)            # “ Go -> “Go
    p = re.sub(r"\s+([’”])(?=\s|$)", r"\1", p)
    p = re.sub(r"\s+", " ", p).strip()
    return p


# ---------------------------------------------------------------------------------------------
# Passages, and matching them to the sections

def passages(book):
    """Growse's passages, each a chaupai group and the doha(s) closing it: a new one begins with the
    first prose after a doha. A doha is one paragraph, so more paragraphs under a doha heading are
    the next chaupais, whose heading the scan has lost."""
    out, prev = [], None
    for kind, label, ps in book:
        if kind == "doha" and len(ps) > 1:
            parts = [("doha", label, ps[:1]), ("text", "", ps[1:])]
        else:
            parts = [(kind, label, ps)]
        for kd, lb, pp in parts:
            if not out or kd == "invocation" or (kd != "doha" and prev == "doha"):
                out.append({"paras": [], "kinds": [], "labels": [], "pk": []})
            out[-1]["paras"].extend(pp)
            out[-1]["pk"].extend([kd] * len(pp))
            out[-1]["kinds"].append(kd)
            out[-1]["labels"].append(lb)
            if pp:
                prev = kd
    return [p for p in out if p["paras"]]


IAST_PLAIN = str.maketrans("āīūṛṝḷēōṃṁḥñṅṇṭḍśṣ", "aiurrleommhnnntdss")


def names_en(text):
    words = re.findall(r"(?<![.!?“‘\"] )\b([A-Z][a-zà-ÿ\-]{3,})", text)
    return {norm(w)[:5] for w in words if norm(w) not in STOP}


def names_aw(verses):
    out = set()
    for v in verses:
        for w in v.get("tr", "").lower().translate(IAST_PLAIN).split():
            w = re.sub(r"[^a-z]", "", w)
            if len(w) >= 4:
                out.add(w[:5])
    return out


STOP = {"then", "when", "there", "with", "this", "that", "they", "their", "what", "though", "thus", "while", "where", "after",
        "como", "lord", "sire", "father", "mother", "brother", "king", "queen", "behold", "hear", "even", "again",
        "from", "your", "have", "like", "some", "said", "all", "come", "glory", "blessed", "oh", "who", "whose", "since",
        "would", "were", "being", "seeing", "having", "hearing", "know", "here", "every", "these", "those", "great"}


def align(G, O, ratio):
    """Match passages G to sections O in order. Each step pairs 1 or 2 passages with 1 or 2 sections,
    or leaves one of either unmatched. Returns, for each section, the passages given to it."""
    n, m = len(G), len(O)
    idf = Counter(x for g in G for x in g["names"])
    def score(gs, os_):
        e = sum(g["len"] for g in gs)
        a = sum(o["len"] for o in os_) * ratio
        c = abs(math.log((e + 40) / (a + 40)))
        common = set().union(*(g["names"] for g in gs)) & set().union(*(o["names"] for o in os_))
        c -= sum(1.0 / math.log(2 + idf[x]) for x in common) * 0.35
        return c + 0.5 * (len(gs) + len(os_) - 2)
    INF = float("inf")
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if D[i][j] == INF:
                continue
            for di, dj in ((1, 1), (1, 2), (2, 1), (3, 1), (1, 3), (1, 0), (0, 1)):
                ii, jj = i + di, j + dj
                if ii > n or jj > m:
                    continue
                c = 2.2 if di == 0 or dj == 0 else score(G[i:ii], O[j:jj])
                if D[i][j] + c < D[ii][jj]:
                    D[ii][jj] = D[i][j] + c
                    P[ii][jj] = (i, j)
    pairs, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj = P[i][j]
        pairs.append((list(range(pi, i)), list(range(pj, j))))
        i, j = pi, pj
    return pairs[::-1]


def readable(p, freq):
    """Whether a paragraph is prose rather than OCR noise from a picture or a blot."""
    toks = [norm(core(t)) for t in TOKEN.findall(p)]
    toks = [t for t in toks if t]
    return len(toks) >= 3 and sum(freq[t] >= 3 for t in toks) / len(toks) >= 0.75


def split_paras(paras, kinds, sections, ratio):
    """Divide one passage's paragraphs among consecutive sections: each share should be as long as
    its section warrants, and should end with a doha, as a section does."""
    n, k = len(paras), len(sections)
    if n < k:
        return [paras] + [[] for _ in range(k - 1)]
    best = None
    def cost(chunk, chunk_kinds, o):
        e = sum(len(x) for x in chunk)
        c = abs(math.log((e + 40) / (o["len"] * ratio + 40)))
        return c - (0.6 if chunk_kinds[-1] == "doha" else 0)
    from itertools import combinations
    for cuts in combinations(range(1, n), k - 1):
        b = (0,) + cuts + (n,)
        c = sum(cost(paras[b[i]:b[i + 1]], kinds[b[i]:b[i + 1]], sections[i]) for i in range(k))
        if best is None or c < best[0]:
            best = (c, b)
    b = best[1]
    return [paras[b[i]:b[i + 1]] for i in range(k)]


def write(path, data):
    with open(os.path.join(TEXTS, path), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))


def build(src22, src14):
    t22 = open(src22, encoding="utf-8").read()
    t14 = open(src14, encoding="utf-8").read()
    b22, b14 = books_of(blocks_of(t22)), books_of(blocks_of(t14))
    print("books:", len(b22), len(b14))
    b22 = [fill_gaps(b22[k], b14[k]) for k in range(7)]
    all_tokens = [norm(core(strip_refs(t))) for t in TOKEN.findall(t22 + "\n" + t14)]
    freq = Counter(all_tokens)
    words = word_counts(t22 + "\n" + t14)
    common = {"cap": [w for w, c in words.items() if c >= 20 and w[:1].isupper() and w.isalpha()],
              "low": [w for w, c in words.items() if c >= 30 and w.islower() and w.isalpha()]}
    report = []
    for k, book in enumerate(b22[:7], 1):
        other = [strip_refs(t) for b in (b14[k - 1] if k - 1 < len(b14) else []) for p in b[2] for t in TOKEN.findall(p)]
        G = [g for g in passages(book)]
        for g in G:
            fixed = [polish(polish(tidy(settle_hyphens(p, freq)), words, common), words, common) for p in correct(g["paras"], other, freq)]
            keep = [i for i, p in enumerate(fixed) if readable(p, freq)]
            g["paras"], g["pk"] = [fixed[i] for i in keep], [g["pk"][i] for i in keep]
            g["len"] = sum(len(p) for p in g["paras"])
            g["names"] = names_en(" ".join(g["paras"]))
        path = os.path.join(TEXTS, "ramcharitmanas", f"{k}.json")
        data = json.load(open(path, encoding="utf-8"))
        # The Sanskrit verses that close the poem are not in Growse.
        shloka_only = lambda s: s["label"] == "Closing verses" and all(v.get("head", "श्लोक") == "श्लोक" for v in s["verses"])
        for s in data["sections"]:
            if shloka_only(s):
                s.pop("trans", None)
        idx = [j for j, s in enumerate(data["sections"]) if not shloka_only(s)]
        O = [{"len": sum(len(v.get("tr", "")) for v in data["sections"][j]["verses"]), "names": names_aw(data["sections"][j]["verses"])} for j in idx]
        G = [g for g in G if g["paras"]]
        ratio = sum(g["len"] for g in G) / max(1, sum(o["len"] for o in O))
        pairs = [(gs, [idx[j] for j in os_]) for gs, os_ in align(G, O, ratio)]
        O = {idx[j]: o for j, o in enumerate(O)}
        for gs, os_ in pairs:
            for j in os_:
                data["sections"][j].pop("trans", None)
            for j in os_:
                data["sections"][j].pop("trans_with", None)
            if gs and os_:
                paras = [p for i in gs for p in G[i]["paras"]]
                kinds = [x for i in gs for x in G[i]["pk"]]
                shares = split_paras(paras, kinds, [O[j] for j in os_], ratio)
                for j, share in zip(os_, shares):
                    if share:
                        data["sections"][j]["trans"] = share
                    else:
                        data["sections"][j]["trans_with"] = data["sections"][os_[0]]["short"]
        report.append((k, len(G), len(O), pairs))
        yield k, data, G, pairs


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    for k, data, G, pairs in build(sys.argv[1], sys.argv[2]):
        secs = data["sections"]
        have = sum(1 for x in secs if x.get("trans"))
        shared = sum(1 for x in secs if x.get("trans_with"))
        left = [i for gs, os_ in pairs if not os_ for i in gs]
        print(f"Kand {k}: {have} of {len(secs)} sections translated, {shared} share the one before;"
              f" {len(left)} passages unmatched" + (f" (the last: {G[left[-1]]['paras'][0][:60]}…)" if left else ""))
        write(f"ramcharitmanas/{k}.json", data)
        if k == 5:
            write("sundarkand/1.json", data)
