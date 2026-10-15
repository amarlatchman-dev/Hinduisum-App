#!/usr/bin/env python3
"""Record every prayer, verse by verse, with ElevenLabs text to speech.

Usage:
  python3 scripts/build_audio.py [prayer-id ...]

Writes audio/<id>/<verse>.mp3 for each verse of each prayer in js/prayers.js and lists the
files in audio/index.json, so the app plays them and highlights each verse as it is chanted.
Verses already recorded are kept; delete a file to record it again. With prayer ids, only
those prayers are recorded.

The ElevenLabs key is read from ELEVENLABS_API_KEY. In a session whose network adds the
xi-api-key header itself, the variable can be left unset.

Voice: "Brian", a deep and calm premade voice, on the Multilingual v2 model, which reads
Devanagari with Indian pronunciation and stays steady across long texts. It is slowed a
little and kept even, to suit chanting.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
VOICE = "nPczCjzI2devNBz1zQrb"  # Brian
MODEL = "eleven_multilingual_v2"
SETTINGS = {"stability": 0.7, "similarity_boost": 0.75, "style": 0.0, "use_speaker_boost": True, "speed": 0.85}
URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_64"


def prayers():
    out = subprocess.run(["node", "-e", "global.window={};require('./js/prayers.js');"
                          "process.stdout.write(JSON.stringify(window.PRAYERS))"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def chant_text(deva):
    """The Devanagari of a verse, with its punctuation turned into the pauses of a chant."""
    t = re.sub(r"॥\s*[०-९\d]+\s*॥", "॥", deva)          # verse numbers
    t = t.replace("ॐ", "ओम्")                             # read the sacred syllable as Om
    t = re.sub(r"\s*॥\s*", ". ", t)
    t = re.sub(r"\s*।\s*", ", ", t)
    t = re.sub(r"\s*\n\s*", ", ", t)
    t = re.sub(r"(,\s*)+\.", ".", re.sub(r"(,\s*){2,}", ", ", t))
    return t.strip(" ,")


def speak(text):
    body = json.dumps({"text": text, "model_id": MODEL, "voice_settings": SETTINGS}).encode()
    headers = {"Content-Type": "application/json", "Accept": "audio/mpeg"}
    if os.environ.get("ELEVENLABS_API_KEY"):
        headers["xi-api-key"] = os.environ["ELEVENLABS_API_KEY"]
    for wait in (5, 20, 60, 0):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL, body, headers), timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:300]
            if e.code in (401, 402) or "quota" in detail:
                raise SystemExit(f"ElevenLabs refused the request ({e.code}): {detail}")
            if not wait:
                raise SystemExit(f"ElevenLabs error {e.code}: {detail}")
        except urllib.error.URLError:
            if not wait:
                raise
        time.sleep(wait)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout
    return float(out or 0)


def main():
    only = set(sys.argv[1:])
    index_path = os.path.join(ROOT, "audio", "index.json")
    index = json.load(open(index_path, encoding="utf-8")) if os.path.exists(index_path) else {}
    used = 0
    for p in prayers():
        if only and p["id"] not in only:
            continue
        files = []
        for k, v in enumerate(p["verses"], 1):
            rel = f"audio/{p['id']}/{k}.mp3"
            path = os.path.join(ROOT, rel)
            text = chant_text(v[0])
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                data = speak(text)
                with open(path, "wb") as f:
                    f.write(data)
                used += len(text)
                # A clip far shorter or longer than its text suggests a garbled reading.
                secs, expect = duration(path), len(text) / 11
                flag = "  <- check" if not (0.4 * expect < secs < 2.5 * expect + 2) else ""
                print(f"{rel}: {len(text)} chars, {secs:.1f} s{flag}", flush=True)
            files.append(rel)
        index[p["id"]] = files
        with open(index_path, "w", encoding="utf-8") as f:   # saved as we go, so a stop loses nothing
            json.dump(index, f, ensure_ascii=False, indent=1)
    print(f"done; {used} characters sent to ElevenLabs this run")


if __name__ == "__main__":
    main()
