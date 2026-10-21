#!/usr/bin/env python3
"""Write calendar/tithi.json: every tithi from 1930 to 2060, for finding the tithi of any date.

Usage:
  pip install pyswisseph
  python3 scripts/build_tithi_table.py [first_year] [last_year]

The city calendars cover only a few years; remembering a loved one needs the tithi of a date long
past (a death or a birth) and its return in years to come. This table holds the moment each tithi
begins, so the app can find the tithi prevailing at local sunrise (or at a given time) anywhere,
and the amanta month (and adhika flag) of each lunation. It uses the same astronomy and month
rules as scripts/build_calendar.py, so the two agree.

Format (times in whole minutes since 1970-01-01 UTC):
  start   the minute the first listed tithi begins; it is always Shukla Pratipada (tithi 1)
  d       the length in minutes of each tithi in turn (tithi numbers cycle 1..30)
  months  for each lunation in turn, month index (0 = Chaitra) * 2 + 1 if adhika
  cities  id, latitude and longitude of the app's cities, for sunrise
"""
import json
import os
import sys

import swisseph as swe

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_calendar import CITIES, lunar_months, tithi_intervals  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "calendar", "tithi.json")
UNIX_JD = 2440587.5


def minutes(jd):
    return round((jd - UNIX_JD) * 1440)


def main(first=1930, last=2060):
    jd0 = swe.julday(first - 1, 12, 1, 0)
    jd1 = swe.julday(last + 1, 2, 1, 0)
    ivs = tithi_intervals(jd0, jd1)
    while ivs[0][0] != 1:            # begin with a new moon, so every lunation is whole
        ivs.pop(0)
    while ivs[-1][0] != 30:          # and end with one
        ivs.pop()
    months = lunar_months(ivs)
    starts = [minutes(iv[1]) for iv in ivs] + [minutes(ivs[-1][2])]
    out = {
        "start": starts[0],
        "d": [b - a for a, b in zip(starts, starts[1:])],
        "months": [m[0] * 2 + (1 if m[1] else 0) for iv, m in zip(ivs, months) if iv[0] == 1],
        "cities": [{"id": c[0], "lat": c[3], "lon": c[4]} for c in CITIES],
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, separators=(",", ":"))
    print(f"{len(out['d'])} tithis, {len(out['months'])} lunations, {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main(*map(int, sys.argv[1:3]))
