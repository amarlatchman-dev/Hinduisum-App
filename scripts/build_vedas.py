#!/usr/bin/env python3
"""Build the complete Rig Veda in texts/.

Usage:
  pip install indic-transliteration
  python3 scripts/build_vedas.py <dharmicdata_dir> <rigveda_html_dir>

  dharmicdata_dir      https://github.com/bhavykhatri/DharmicData (Sanskrit, ODbL)
  rigveda_html_dir     Wikisource pages "The Hymns of the Rigveda/Book N/Hymn M" saved with
                       action=render, file names URL-quoted (Ralph T. H. Griffith, 1896)

The ten hymns of the existing Dharma Path selection stay as the first part of the Rig Veda;
the ten mandalas follow as parts 2 to 11, each hymn with the Sanskrit, a transliteration and
Griffith's English, paired verse by verse. The Atharva Veda helpers here (its Sanskrit and
book titles) are used by build_atharvaveda.py.
"""
import html
import json
import os
import re
import sys
import unicodedata
import urllib.parse

from indic_transliteration import sanscript

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_more_texts import ACCENTS, build_rigveda, rig_verses, write  # noqa: E402
from rigveda_hymns import HYMNS  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")


# --------------------------------------------------------------------------- Wikisource pages
def clean_html(t):
    """A Wikisource page rendered with action=render, as plain text with line breaks.
    Footnote markers and notes, page numbers and running headers are dropped."""
    t = re.sub(r"\sdata-mw='[^']*'", "", t)
    t = re.sub(r'\sdata-mw="[^"]*"', "", t)
    t = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", t, flags=re.S)
    t = re.sub(r"<sup[^>]*class=\"[^\"]*reference[^\"]*\"[^>]*>.*?</sup>", "", t, flags=re.S)
    t = re.sub(r"<(ol|div)[^>]*class=\"[^\"]*(references|reflist|mw-references-wrap)[^\"]*\"[^>]*>.*", "", t, flags=re.S)
    t = re.sub(r"<span[^>]*class=\"[^\"]*pagenum[^\"]*\"[^>]*>.*?</span>", "", t, flags=re.S)
    t = re.sub(r"<div[^>]*class=\"[^\"]*wst-rh[^\"]*\".*?</div>\s*</div>", "", t, flags=re.S)
    t = re.sub(r"<br\b[^>]*>", "\n", t)
    t = re.sub(r"</(p|div|li|h\d|tr|dd|dt)>", "\n\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t).replace("​", "").replace("﻿", "")
    t = re.sub(r"[ \t ]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def page(cache, title):
    f = os.path.join(cache, urllib.parse.quote(title, safe="") + ".html")
    return open(f, encoding="utf-8").read() if os.path.exists(f) else None


HEADING = re.compile(r"^(THE HYMNS OF THE [A-Z\- ]+\.?|BOOK THE [A-Z]+\.?|HYMN [IVXLC]+\.?.*|[A-Z][A-Z \-]+\.)$")


def split_doubled(verses, want):
    """Where a verse number was lost in transcription, two stanzas run together. With the
    expected count known, split a stanza twice the usual length into the missing number."""
    sizes = sorted(len(v) for v in verses.values())
    mode = max(set(sizes), key=sizes.count) if sizes else 0
    for k in sorted(verses):
        if len(verses) >= want:
            break
        if k + 1 not in verses and k + 1 <= want and mode and len(verses[k]) == 2 * mode:
            verses[k], verses[k + 1] = verses[k][:mode], verses[k][mode:]
    return verses


def griffith_verses(text, title_tail, want=0):
    """Griffith's verses from a cleaned hymn page, keyed by verse number."""
    # The page body starts after the header line that names the hymn and the translator.
    at = text.rfind(title_tail)
    if at >= 0:
        text = text[at + len(title_tail):]
        text = re.sub(r"^\s*Ralph T\. ?H\. Griffith", "", text)
    def skip(l):  # headings, navigation and the transcriber's bracketed notes
        return (not l or HEADING.match(l) or l in ("←", "→") or l.startswith("sister projects")
                or l.startswith("(") and "JBH" in l)
    lines = [l for l in (l.strip() for l in text.split("\n")) if not skip(l)]
    start = re.compile(r"^(\d{1,3})[.,§]?\s+(\S.*)$")
    cands = [(i, int(m.group(1))) for i, l in enumerate(lines) for m in [start.match(l)] if m]
    starts, n = {}, 0
    for j, (i, k) in enumerate(cands):
        nxt = cands[j + 1][1] if j + 1 < len(cands) else None
        if k == n + 1 or (n == 0 and k == 2):          # the next verse; the first may be unnumbered
            starts[i] = n = k
        elif n < k <= n + 9 and nxt in (None, k + 1):  # verses Griffith left untranslated
            starts[i] = n = k
        elif nxt == n + 2:                              # a misprinted number between two good ones
            starts[i] = n = n + 1
    verses, cur, n = {}, [], None
    for i, l in enumerate(lines):
        if i in starts:
            if cur:
                verses[n or 1] = cur
            n, cur = starts[i], [start.match(l).group(2)]
        else:
            cur.append(l)
    if cur:
        verses[n or 1] = cur
    verses = split_doubled(verses, want)
    out = {}
    for k, ls in verses.items():
        s = " ".join(ls)
        s = re.sub(r"\[\d+\]|\[[a-z]\]", "", s)
        s = re.sub(r"\s+([,;:.!?])", r"\1", re.sub(r"\s+", " ", s)).strip()
        s = re.sub(r"^([A-Z]{2,})\b", lambda m: m.group(1).capitalize(), s)  # small capitals of the first word
        if s:
            out[k] = s
    return out


# --------------------------------------------------------------------------- deities
DEITIES = [  # (prefix of the Sanskrit deity in the anukramani line, English)
    ("इन्द्राग्नी", "Indra and Agni"), ("इन्द्रावरुण", "Indra and Varuna"), ("इन्द्रवायू", "Indra and Vayu"),
    ("इन्द्राविष्णू", "Indra and Vishnu"), ("इन्द्रासोम", "Indra and Soma"), ("इन्द्र", "Indra"),
    ("अग्निषोम", "Agni and Soma"), ("अग्निर्मरुत", "Agni and the Maruts"), ("अग्निर्वैश्वानर", "Agni Vaishvanara"),
    ("वैश्वानर", "Agni Vaishvanara"), ("रक्षोहा", "Agni, slayer of demons"), ("अग्नि", "Agni"),
    ("पवमान", "Soma Pavamana"), ("सोम", "Soma"), ("अश्विन", "the Ashvins"), ("विश्वे", "the All-Gods"),
    ("देवाः", "the gods"), ("मरुत", "the Maruts"), ("मित्रावरुण", "Mitra and Varuna"),
    ("वरुणमित्रार्यमण", "Varuna, Mitra and Aryaman"), ("मित्र", "Mitra"), ("वरुण", "Varuna"), ("ऋभ", "the Ribhus"),
    ("सविता", "Savitar"), ("सवितृ", "Savitar"), ("आप्री", "the Apri gods"), ("उष", "Ushas, the Dawn"),
    ("वायु", "Vayu, the Wind"), ("पूष", "Pushan"), ("ब्रह्मणस्पति", "Brahmanaspati"), ("बृहस्पति", "Brihaspati"),
    ("सूर्या", "Surya's bridal"), ("सूर्य", "Surya, the Sun"), ("द्यावापृथिवी", "Heaven and Earth"), ("आदित्य", "the Adityas"),
    ("रुद्र", "Rudra"), ("विष्णु", "Vishnu"), ("सरस्वती", "Sarasvati"), ("सरस्वान्", "Sarasvan"), ("आप", "the Waters"),
    ("यम", "Yama"), ("ग्रावाण", "the pressing stones"), ("आत्मा", "the Self"), ("कः", "Ka, the unknown god"),
    ("अश्वः", "the horse"), ("ऋतु", "the Seasons"), ("शकुन्त", "the bird of omen"), ("नद्य", "the Rivers"),
    ("दधिक्रा", "Dadhikra"), ("वास्तोष्पति", "Vastoshpati, lord of the house"), ("विश्वकर्म", "Vishvakarman"),
    ("मन्यु", "Manyu"), ("राजा", "the king"), ("पर्जन्य", "Parjanya, the rain"), ("वाक्", "Vak, Speech"),
    ("पुरुष", "Purusha"), ("श्रद्धा", "Shraddha, Faith"), ("रात्रि", "Ratri, the Night"), ("अरण्यानी", "the forest"),
    ("ज्ञान", "Knowledge"), ("दक्षिणा", "the sacrificial gift"), ("अदिति", "Aditi"), ("भग", "Bhaga"),
    ("त्वष्ट", "Tvashtar"), ("अपां नपा", "Apam Napat"), ("क्षेत्रस्य", "the lord of the field"), ("मण्डूक", "the frogs"),
    ("अक्ष", "the dice"), ("वेन", "Vena"), ("हिरण्यगर्भ", "Hiranyagarbha"), ("सरमा", "Sarama"), ("उर्वशी", "Urvashi"),
    ("पितर", "the Fathers"), ("अग्नायी", "Agnayi"), ("वाजिन", "the coursers"), ("अन्न", "Food"), ("ओषधी", "the plants"),
]
SPECIAL = {(h["ref"][0], h["ref"][1]): h["title"] for h in HYMNS}
SPECIAL.update({(10, 129): "The Hymn of Creation", (10, 90): "Purusha Sukta, the Cosmic Person",
                (10, 121): "To the Unknown God, Hiranyagarbha", (10, 125): "Vak, the voice of the divine",
                (10, 34): "The gambler's lament", (7, 103): "The frogs", (10, 191): "The hymn of unity"})
SPECIAL.update({  # hymns whose deity line names no single god, or names one misleadingly
    (1, 112): "To the Ashvins", (1, 125): "Praise of a generous patron", (1, 126): "Praise of Bhavya's bounty",
    (1, 179): "Lopamudra and Agastya", (1, 185): "To Heaven and Earth", (2, 35): "To Apam Napat, child of the waters",
    (3, 8): "To the sacrificial post", (4, 18): "The birth of Indra", (4, 57): "To the lord of the field",
    (5, 84): "To Prithivi, the Earth", (6, 15): "To Agni", (6, 31): "To Indra", (6, 44): "To Indra",
    (6, 57): "To Indra and Pushan", (6, 60): "To Indra and Agni", (6, 68): "To Indra and Varuna",
    (6, 69): "To Indra and Vishnu", (6, 70): "To Heaven and Earth", (6, 72): "To Indra and Soma",
    (6, 73): "To Brihaspati", (6, 74): "To Soma and Rudra", (6, 75): "To the weapons of war",
    (7, 39): "To the All-Gods", (7, 44): "To Dadhikra", (7, 46): "To Rudra", (7, 67): "To the Ashvins",
    (7, 88): "To Varuna", (8, 31): "Praise of sacrifice and the devoted couple", (8, 65): "To Indra",
    (8, 66): "To Indra", (10, 10): "Yama and Yami", (10, 13): "To the carts of the oblation",
    (10, 18): "A funeral hymn", (10, 58): "To call back a departing spirit", (10, 59): "For long life",
    (10, 85): "The wedding of Surya", (10, 95): "Pururavas and Urvashi", (10, 96): "To Indra's bay horses",
    (10, 97): "To the healing plants", (10, 108): "Sarama and the Panis", (10, 117): "In praise of generosity",
    (10, 130): "The weaving of the sacrifice", (10, 163): "To drive away disease", (10, 164): "Against evil dreams",
    (10, 166): "Against rivals", (10, 169): "To the cows", (10, 177): "The bird of illusion",
    (10, 178): "To Tarkshya", (10, 183): "For offspring", (10, 190): "Order and truth born of fervour",
})


def deity_label(first_line, mandala, sukta):
    if (mandala, sukta) in SPECIAL:
        return SPECIAL[(mandala, sukta)]
    parts = [p.strip() for p in re.split(r"[।|]", first_line) if p.strip()]
    for p in parts[1:3] + parts[:1]:
        d = re.sub(r"[०-९\d\-–,;:=()\[\]{}]+", " ", p).strip()
        for word in d.split()[:2]:
            for pre, en in DEITIES:
                if word.startswith(pre):
                    return f"To {en}" if not en.startswith(("The ", "the gods")) else en[0].upper() + en[1:]
    return f"Hymn {mandala}.{sukta}"


def anukramani(dharmic, veda, mandala, sukta):
    fn = os.path.join(dharmic, "Rigveda", f"rigveda_mandala_{mandala}.json")
    for h in json.load(open(fn, encoding="utf-8")):
        if h["sukta"] == sukta:
            return ACCENTS.sub("", h["text"].strip().split("\n")[0])
    return ""


def iast(dev):
    tr = sanscript.transliterate(re.sub(r"[।॥]", "", dev), sanscript.DEVANAGARI, sanscript.IAST).replace("~", "ṃ")
    return re.sub(r"\s+", " ", tr).strip()


# --------------------------------------------------------------------------- Rig Veda
MANDALA_SUB = {
    1: "Hymns of many families of seers", 2: "The family of Gritsamada", 3: "The family of Vishvamitra",
    4: "The family of Vamadeva", 5: "The family of Atri", 6: "The family of Bharadvaja",
    7: "The family of Vasishtha", 8: "The Kanvas and the Angirasas", 9: "Soma Pavamana, the purifying Soma",
    10: "The late hymns: creation, death, marriage and the cosmos",
}
HYMN_COUNT = {1: 191, 2: 43, 3: 62, 4: 58, 5: 87, 6: 75, 7: 104, 8: 103, 9: 114, 10: 191}


def rv_verses(dharmic, mandala, sukta):
    """Like rig_verses, also for the few hymns whose source text has no line breaks."""
    verses = rig_verses(dharmic, mandala, sukta)
    data = json.load(open(os.path.join(dharmic, "Rigveda", f"rigveda_mandala_{mandala}.json"), encoding="utf-8"))
    text = next(h for h in data if h["sukta"] == sukta)["text"]
    if len(verses) > 1 or len(re.findall(r"॥\s*[०-९]+\s*॥", text)) <= 1:
        return verses
    body = text.split("।", 3)[3] if text.count("।") >= 3 else text  # after the seer, deity and metre
    body = re.sub(r"(?<=[\u0900-\u097F]):", "ः", ACCENTS.sub("", body))
    out = [v.strip() for v in re.split(r"\s*॥\s*[०-९]+\s*॥\s*", body) if v.strip()]
    return [re.sub(r"\s*।\s*", " ।\n", v).strip() + "॥" for v in out]


def griffith_hymn(mandala, sukta):
    """Griffith moved the eleven Valakhilya hymns (8.49-59) to the end of the eighth book, so
    from 8.49 his numbers differ from the standard ones used here."""
    if mandala == 8 and 49 <= sukta <= 59:
        return sukta + 44
    if mandala == 8 and 60 <= sukta <= 103:
        return sukta - 11
    return sukta


def build_full_rigveda(dharmic, cache):
    parts = build_rigveda(dharmic)  # part 1: the ten selected hymns, Dharma Path's own translation
    parts[0].update({"short": "ॐ", "label": "Selection"})  # so the mandalas keep their own numbers
    report = []
    for m in range(1, 11):
        secs = []
        for s in range(1, HYMN_COUNT[m] + 1):
            raw = page(cache, f"The Hymns of the Rigveda/Book {m}/Hymn {griffith_hymn(m, s)}")
            try:
                sa = rv_verses(dharmic, m, s)
            except StopIteration:
                sa = []
            en = griffith_verses(clean_html(raw), f"— Hymn {griffith_hymn(m, s)}", len(sa)) if raw else {}
            if sa and en and len(sa) < max(en):
                # two verses under one number in the Sanskrit source (as in 1.100.11): split a verse
                # of twice the usual length
                lines = [v.split("\n") for v in sa]
                sizes = [len(l) for l in lines]
                mode, extra, out = max(set(sizes), key=sizes.count), max(en) - len(sa), []
                for l in lines:
                    if extra and len(l) == 2 * mode:
                        out += [l[:mode], l[mode:]]
                        extra -= 1
                    else:
                        out.append(l)
                if not extra:
                    sa = ["\n".join(l).rstrip(" ।") + ("" if l[-1].endswith("॥") else "॥") for l in out]
            refs = [f"{m}.{s}.{k}" for k in range(1, len(sa) + 1)]
            last = max(en) if en else 0
            if sa and last and len(sa) > last and (len(sa) + 1) // 2 == last:
                # Griffith renders each pair of two-line verses as one stanza (as in 1.65-70)
                sa = ["\n".join(sa[i:i + 2]) for i in range(0, len(sa), 2)]
                refs = [f"{m}.{s}.{i + 1}–{min(i + 2, len(refs))}" if i + 1 < len(refs) else f"{m}.{s}.{i + 1}"
                        for i in range(0, len(refs), 2)]
            elif sa and last == 2 * len(sa) and all(v.count("\n") == 1 for v in sa):
                # the source joins two one-line verses under one number (as in 8.29)
                sa = [half.strip() + ("" if half.endswith("॥") else " ॥") for v in sa for half in v.split("\n")]
                refs = [f"{m}.{s}.{k}" for k in range(1, len(sa) + 1)]
            note = None
            if not sa and raw:
                note = "The Sanskrit of this hymn is missing from our source, so only the English is given."
            elif sa and last and len(sa) != last and not (len(sa) > last and [k for k in range(1, last) if k not in en]):
                note = "The Sanskrit of this hymn in our source is divided differently, so only the English is given."
                sa, refs = [], []
            n = max(len(sa), last)
            verses = []
            for k in range(1, n + 1):
                v = {"n": k, "ref": refs[k - 1] if k <= len(refs) else f"{m}.{s}.{k}"}
                if k <= len(sa):
                    v["sa"], v["tr"] = sa[k - 1], iast(sa[k - 1])
                v["en"] = en.get(k, "")
                verses.append(v)
            sec = {"label": deity_label(anukramani(dharmic, "rig", m, s), m, s), "short": f"{m}.{s}",
                   "name": f"Mandala {m}, hymn {s}" + (" · Valakhilya" if m == 8 and 49 <= s <= 59 else "")}
            gaps = [k for k in range(1, n + 1) if k not in en]
            if raw and not en:
                sec["intro"] = ["Griffith did not translate this hymn into English; it is given here in Sanskrit "
                                "with its transliteration."]
            elif raw and gaps and len(gaps) < n:
                which = ", ".join(str(k) for k in gaps)
                sec["intro"] = [f"Griffith left verse{'s' if len(gaps) > 1 else ''} {which} untranslated."]
            if note:
                sec["intro"] = [note]
            sec["verses"] = verses
            secs.append(sec)
            if not raw:
                report.append(f"{m}.{s}: no English page")
            elif len(sa) != last or gaps:
                report.append(f"{m}.{s}: {len(sa)} Sanskrit, {len(en)} English verses (last {last}); gaps {gaps}")
        size = write(f"rigveda/{m + 1}.json", {"sections": secs})
        print(f"rigveda/{m + 1}.json", size, "bytes,", len(secs), "hymns")
        parts.append({"n": m + 1, "short": str(m), "name": f"Mandala {m}", "sub": MANDALA_SUB[m], "count": len(secs)})
    return parts, report


# --------------------------------------------------------------------------- Atharva Veda
AV_SUB = {
    1: "Charms for healing, protection and blessing", 2: "Charms of healing, long life and protection",
    3: "Charms for kings, concord and prosperity", 4: "Brahman, Varuna who sees all, the royal consecration",
    5: "Longer hymns and charms", 6: "Brief charms, mostly of three verses", 7: "The briefest charms and prayers",
    8: "Long life, and the cosmic cow Viraj", 9: "The honey-whip, the guest and the riddle of the year",
    10: "Skambha, the pillar of the universe", 11: "Prana, the Brahmacharin and the remnant",
    12: "The Hymn to the Earth", 13: "Rohita, the ruddy sun", 14: "The wedding hymns",
    15: "The Vratya, the wandering ascetic", 16: "Prose charms against evil dreams",
    17: "A prayer to Indra and the Sun", 18: "The funeral hymns", 19: "Later hymns: Time, the Cosmic Person, protection",
    20: "Hymns for the Soma ritual, mostly from the Rig Veda",
}


def av_verses(dharmic, kanda, sukta):
    """The Sanskrit verses of an Atharva Veda hymn; the title and the seer/deity/metre lines are dropped."""
    data = json.load(open(os.path.join(dharmic, "AtharvaVeda", f"atharvaveda_kaanda_{kanda}.json"), encoding="utf-8"))
    text = next(h for h in data if h["sukta"] == sukta)["text"]
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first = next((i for i, l in enumerate(lines) if re.search("[\u0951\u0952]", l)), 0)  # verses carry accents
    text = ACCENTS.sub("", "\n".join(lines[first:]))
    text = re.sub(r"(?<=[\u0900-\u097F]):", "ः", text)
    verses, buf = [], []
    for l in text.split("\n"):
        buf.append(l)
        if re.search(r"॥?\s*[०-९]+\s*॥*\s*$", l):
            joined = re.sub(r"\s*॥?\s*[०-९]+\s*॥*\s*$", "॥", "\n".join(buf)).replace("।॥", "॥")
            verses.append(joined.strip())
            buf = []
    return verses


def ascii_names(s):
    """Griffith's Atharva Veda pages keep his diacritics (Vāchaspati); the app spells names plainly."""
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    dharmic, rv_cache = sys.argv[1:3]
    path = os.path.join(OUT, "index.json")
    index = json.load(open(path, encoding="utf-8"))
    parts, report = build_full_rigveda(dharmic, rv_cache)
    index["rigveda"] = {"parts": parts}
    print("index.json", write("index.json", index), "bytes")
    print(len(report), "hymns with a verse-count difference or no English page")
    for r in report[:80]:
        print("  ", r)


if __name__ == "__main__":
    main()
