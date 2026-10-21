#!/usr/bin/env python3
"""Add Tulsidas's Ramcharitmanas, in Awadhi with a transliteration, to texts/.

Usage:
  pip install indic-transliteration
  git clone --depth 1 https://github.com/bhavykhatri/DharmicData /tmp/dharmic
  python3 scripts/build_ramcharitmanas.py /tmp/dharmic/Ramcharitmanas

The source has each kand as a list of blocks (shloka, chaupai, doha/soratha, chhand), from the IIT
Kanpur Ramcharitmanas project. The text is laid out as it is read: each doha closes a group of
chaupais, and that group is one section here, "Doha N", with the standard (Gita Press) numbers.
The shlokas and sorathas that open a kand before its first chaupai make an "Invocation" section,
and any verses after the last doha a closing one.

Writes texts/ramcharitmanas/<k>.json for the seven kands, texts/sundarkand/1.json (the Sundar Kand
on its own, as many families read it), and their entries in texts/index.json. The transliteration
is IAST, with the silent final "a" of Awadhi words dropped (bacan, not bacana), as it is sung.
"""
import json
import os
import re
import sys

from indic_transliteration import sanscript

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_more_texts import write  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "texts")
KANDS = ["Bal Kand", "Ayodhya Kand", "Aranya Kand", "Kishkindha Kand", "Sundar Kand", "Lanka Kand", "Uttar Kand"]
KANDS_SA = ["बालकाण्ड", "अयोध्याकाण्ड", "अरण्यकाण्ड", "किष्किन्धाकाण्ड", "सुन्दरकाण्ड", "लङ्काकाण्ड", "उत्तरकाण्ड"]
HEADS = {"श्लोक": "श्लोक", "चौपाई": "चौपाई", "छंद": "छंद"}
NUM = re.compile(r"।+\s*([०-९\d]+)\s*(?:\(?\s*([क-ह])\s*\)?)?\s*।*\s*$")   # "।।106।।", "। 165।।", "।।181।"
VOWELS = "aāiīuūṛṝḷeo"


def number(s):
    return int(s.translate(str.maketrans("०१२३४५६७८९", "0123456789")))


def lines_of(content):
    return [re.sub(r"\s+", " ", l).strip() for l in content.split("\n") if l.strip()]


def drop_schwa(word):
    """The silent final "a" of an Awadhi word of two or more syllables: bacana -> bacan."""
    syllables = len(re.findall(rf"[{VOWELS}]+", word))
    if syllables >= 2 and re.search(rf"[^{VOWELS}ṃḥ']a$", word) and not word.endswith("ya"):
        return word[:-1]
    return word


def iast(line, sanskrit=False):
    t = sanscript.transliterate(line, sanscript.DEVANAGARI, sanscript.IAST).replace("~", "m̐")
    t = re.sub(r"[|.]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t if sanskrit else " ".join(drop_schwa(w) for w in t.split(" "))


def halves(line):
    """A chaupai line "a। b।।" as its two halves."""
    line = re.sub(r"।।\s*$", "", line).strip()
    parts = [p.strip() for p in re.split(r"।(?!।)", line) if p.strip()]
    return parts if parts else [line]


def verse(lines, head, sanskrit=False):
    clean = [re.sub(r"\s*।+\s*([०-९\d]+\s*(?:\(?[क-ह]\)?)?)?\s*।*\s*$", "", l).strip() for l in lines]
    clean = [c for c in clean if c]
    v = {"sa": " ।\n".join(clean) + " ॥", "tr": "\n".join(iast(c, sanskrit) for c in clean), "en": ""}
    if head:
        v["head"] = head
    return v


def block_verses(block):
    kind = block["type"]
    ls = lines_of(block["content"])
    out = []
    if kind == "चौपाई":
        for l in ls:
            out.append(verse(halves(l), None))
    else:
        cur = []
        for l in ls:
            cur.append(l)
            if l.endswith("।।") or NUM.search(l):
                out.append(verse(cur, None, sanskrit=(kind == "श्लोक")))
                cur = []
        if cur:
            out.append(verse(cur, None, sanskrit=(kind == "श्लोक")))
    head = "दोहा" if kind.startswith("दोहा") else HEADS.get(kind, kind)
    if out:
        out[0]["head"] = head
    return out


def doha_number(block):
    nums = [m for m in (NUM.search(l) for l in lines_of(block["content"])) if m]
    return number(nums[-1].group(1)) if nums else None


def sections_of(blocks):
    secs, cur, seen_chaupai = [], [], False
    label = lambda n: {"label": f"Doha {n}", "short": str(n)}
    last = 0
    for i, b in enumerate(blocks):
        cur.append(b)
        if b["type"] == "चौपाई":
            seen_chaupai = True
        if b["type"].startswith("दोहा") and seen_chaupai:
            n = doha_number(b)
            if n is None:
                # A doha typed without its number closes a group only if the next numbered one skips
                # a number (Ayodhya 107); otherwise it is a second doha of the coming group.
                nxt = next((doha_number(x) for x in blocks[i + 1:] if x["type"].startswith("दोहा") and doha_number(x)), None)
                if nxt != last + 2:
                    continue
                n = last + 1
            secs.append((label(n), cur))
            cur, last = [], n
        elif b["type"].startswith("दोहा") and not seen_chaupai and not secs:
            pass                  # the opening sorathas: part of the invocation
    if cur:
        secs.append(({"label": "Closing verses", "short": "॥"}, cur))
    # the invocation: whatever comes before the first chaupai
    first = secs[0][1] if secs else []
    k = next((i for i, b in enumerate(first) if b["type"] == "चौपाई"), 0)
    if k:
        secs[0] = (secs[0][0], first[k:])
        secs.insert(0, ({"label": "Invocation", "short": "ॐ"}, first[:k]))
    return secs


def build(src):
    files = sorted(f for f in os.listdir(src) if f.endswith(".json"))
    index = json.load(open(os.path.join(OUT, "index.json"), encoding="utf-8"))
    parts = []
    for k, f in enumerate(files, 1):
        blocks = json.load(open(os.path.join(src, f), encoding="utf-8"))
        secs = []
        for meta, bl in sections_of(blocks):
            vs = [v for b in bl for v in block_verses(b)]
            for i, v in enumerate(vs, 1):
                v["n"] = i
                v["ref"] = f"{k}.{meta['short'] if meta['short'].isdigit() else meta['label'][0]}.{i}"
            doha = next((v for v in vs if v.get("head") in ("दोहा",)), vs[-1])
            first = doha["sa"].split(" ")[0].split("\n")[0]
            secs.append({**meta, "name": first, "verses": [{"n": v.pop("n"), "ref": v.pop("ref"), **v} for v in vs]})
        nums = [int(s["short"]) for s in secs if s["short"].isdigit()]
        missing = sorted(set(range(1, max(nums) + 1)) - set(nums))
        write(f"ramcharitmanas/{k}.json", {"sections": secs})
        if k == 5:
            write("sundarkand/1.json", {"sections": secs})
        parts.append({"n": k, "name": KANDS[k - 1], "sub": KANDS_SA[k - 1], "count": len(secs)})
        print(f"{KANDS[k - 1]}: {len(secs)} sections, {sum(len(s['verses']) for s in secs)} verses,"
              f" dohas {min(nums)}-{max(nums)}" + (f", missing {missing}" if missing else ""))
    index["ramcharitmanas"] = {"parts": parts}
    index["sundarkand"] = {"parts": [{"n": 1, "name": "Sundar Kand", "sub": "सुन्दरकाण्ड", "count": parts[4]["count"]}]}
    print("index.json", write("index.json", index), "bytes")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    build(sys.argv[1])
