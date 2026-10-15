#!/usr/bin/env python3
"""Build the complete Rig Veda (and, when its pages are present, the Atharva Veda) in texts/.

Usage:
  pip install indic-transliteration
  python3 scripts/build_vedas.py <dharmicdata_dir> <rigveda_html_dir> [<atharvaveda_html_dir>]

  dharmicdata_dir      https://github.com/bhavykhatri/DharmicData (Sanskrit, ODbL)
  rigveda_html_dir     Wikisource pages "The Hymns of the Rigveda/Book N/Hymn M" saved with
                       action=render, file names URL-quoted (Ralph T. H. Griffith, 1896)
  atharvaveda_html_dir the same for "Hymns of the Atharva-Veda/Book N/Hymn M" (Griffith, 1895-96)

The ten hymns of the existing Dharma Path selection stay as the first part of the Rig Veda;
the ten mandalas follow as parts 2 to 11, each hymn with the Sanskrit, a transliteration and
Griffith's English, paired verse by verse.
"""
import html
import json
import os
import re
import sys
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


def griffith_verses(text, title_tail):
    """Griffith's verses from a cleaned hymn page, keyed by verse number."""
    # The page body starts after the header line that names the hymn and the translator.
    at = text.rfind(title_tail)
    if at >= 0:
        text = text[at + len(title_tail):]
        text = re.sub(r"^\s*Ralph T\. ?H\. Griffith", "", text)
    lines = [l.strip() for l in text.split("\n")]
    verses, cur, n = {}, [], None
    for l in lines:
        if not l or HEADING.match(l) or l in ("←", "→") or l.startswith("sister projects"):
            continue
        m = re.match(r"^(\d{1,3})\.?\s+(.*)$", l)
        if m and (n is None and int(m.group(1)) in (1, 2) or n is not None and int(m.group(1)) == n + 1):
            if cur:
                verses[n or 1] = cur
            n, cur = int(m.group(1)), [m.group(2)]
        else:
            cur.append(l)
    if cur:
        verses[n or 1] = cur
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


def build_full_rigveda(dharmic, cache):
    parts = build_rigveda(dharmic)  # part 1: the ten selected hymns, Dharma Path's own translation
    report = []
    for m in range(1, 11):
        secs = []
        for s in range(1, HYMN_COUNT[m] + 1):
            raw = page(cache, f"The Hymns of the Rigveda/Book {m}/Hymn {s}")
            en = griffith_verses(clean_html(raw), f"— Hymn {s}") if raw else {}
            try:
                sa = rig_verses(dharmic, m, s)
            except StopIteration:
                sa = []
            n = max(len(sa), max(en) if en else 0)
            verses = []
            for k in range(1, n + 1):
                v = {"n": k, "ref": f"{m}.{s}.{k}"}
                if k <= len(sa):
                    v["sa"], v["tr"] = sa[k - 1], iast(sa[k - 1])
                v["en"] = en.get(k, "")
                verses.append(v)
            if not raw:
                report.append(f"{m}.{s}: no English page")
            elif len(sa) != len(en):
                report.append(f"{m}.{s}: {len(sa)} Sanskrit, {len(en)} English verses")
            label = deity_label(anukramani(dharmic, "rig", m, s), m, s)
            secs.append({"label": label, "short": f"{m}.{s}", "name": f"Mandala {m}, hymn {s}", "verses": verses})
        size = write(f"rigveda/{m + 1}.json", {"sections": secs})
        print(f"rigveda/{m + 1}.json", size, "bytes,", len(secs), "hymns")
        parts.append({"n": m + 1, "name": f"Mandala {m}", "sub": MANDALA_SUB[m], "count": len(secs)})
    return parts, report


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
