#!/usr/bin/env python3
"""Compute the Hindu lunar calendar (panchang) and festival dates.

Usage:
  pip install pyswisseph
  python3 scripts/build_calendar.py [first_year] [last_year]

Writes calendar/index.json and calendar/<city>.json. Dates are calculated
separately for each city, because a tithi (lunar day) is reckoned from local
sunrise and can fall on different civil dates in different places.

Method (drik ganita, as used by most modern panchangs):
  * tithi = (moon longitude - sun longitude) / 12 degrees
  * months are amanta (new moon to new moon), named by the sidereal (Lahiri)
    sign of the sun at the opening new moon; a month with no solar ingress
    is adhika (leap)
  * each observance is set on the day its tithi prevails at the traditional
    time of worship (sunrise, forenoon, midday, afternoon, evening, midnight
    or moonrise). If the tithi covers that time on two days the first is
    used; if on neither, the day on which most of the tithi falls.
"""
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import swisseph as swe

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "calendar")

CITIES = [
    # id, name, country, lat, lon, IANA time zone
    ("delhi", "New Delhi", "India", 28.6139, 77.2090, "Asia/Kolkata"),
    ("kathmandu", "Kathmandu", "Nepal", 27.7172, 85.3240, "Asia/Kathmandu"),
    ("dubai", "Dubai", "UAE", 25.2048, 55.2708, "Asia/Dubai"),
    ("singapore", "Singapore", "Singapore", 1.3521, 103.8198, "Asia/Singapore"),
    ("sydney", "Sydney", "Australia", -33.8688, 151.2093, "Australia/Sydney"),
    ("suva", "Suva", "Fiji", -18.1416, 178.4419, "Pacific/Fiji"),
    ("port-louis", "Port Louis", "Mauritius", -20.1609, 57.5012, "Indian/Mauritius"),
    ("durban", "Durban", "South Africa", -29.8587, 31.0218, "Africa/Johannesburg"),
    ("nairobi", "Nairobi", "Kenya", -1.2921, 36.8219, "Africa/Nairobi"),
    ("london", "London", "United Kingdom", 51.5074, -0.1278, "Europe/London"),
    ("toronto", "Toronto", "Canada", 43.6532, -79.3832, "America/Toronto"),
    ("new-york", "New York", "United States", 40.7128, -74.0060, "America/New_York"),
    ("chicago", "Chicago", "United States", 41.8781, -87.6298, "America/Chicago"),
    ("houston", "Houston", "United States", 29.7604, -95.3698, "America/Chicago"),
    ("los-angeles", "Los Angeles", "United States", 34.0522, -118.2437, "America/Los_Angeles"),
    ("port-of-spain", "Port of Spain", "Trinidad and Tobago", 10.6603, -61.5086, "America/Port_of_Spain"),
    ("georgetown", "Georgetown", "Guyana", 6.8013, -58.1551, "America/Guyana"),
    ("paramaribo", "Paramaribo", "Suriname", 5.8520, -55.2038, "America/Paramaribo"),
]

MONTHS = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada",
          "Ashvin", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"]

# Ekadashi names by amanta month: [shukla, krishna]
EKADASHI = [
    ("Kamada", "Varuthini"), ("Mohini", "Apara"), ("Nirjala", "Yogini"),
    ("Devshayani", "Kamika"), ("Shravana Putrada", "Aja"), ("Parsva", "Indira"),
    ("Papankusha", "Rama"), ("Prabodhini", "Utpanna"), ("Mokshada", "Saphala"),
    ("Pausha Putrada", "Shattila"), ("Jaya", "Vijaya"), ("Amalaki", "Papmochani"),
]
ADHIKA_EKADASHI = ("Padmini", "Parama")

# Festivals: id -> (amanta month index, tithi 1-30, time of observance)
FESTIVALS = {
    "ugadi": (0, 1, "sunrise"),
    "ram-navami": (0, 9, "midday"),
    "hanuman-jayanti": (0, 15, "sunrise"),
    "akshaya-tritiya": (1, 3, "forenoon"),
    "ganga-dussehra": (2, 10, "sunrise"),
    "rath-yatra": (3, 2, "sunrise"),
    "guru-purnima": (3, 15, "sunrise"),
    "nag-panchami": (4, 5, "sunrise"),
    "raksha-bandhan": (4, 15, "afternoon"),
    "janmashtami": (4, 23, "midnight"),
    "hartalika-teej": (5, 3, "sunrise"),
    "ganesh-chaturthi": (5, 4, "midday"),
    "anant-chaturdashi": (5, 14, "sunrise"),
    "pitru-paksha": (5, 16, "sunrise"),
    "mahalaya": (5, 30, "sunrise"),
    "navaratri": (6, 1, "sunrise"),
    "durga-ashtami": (6, 8, "sunrise"),
    "maha-navami": (6, 9, "sunrise"),
    "dussehra": (6, 10, "afternoon"),
    "sharad-purnima": (6, 15, "evening"),
    "karva-chauth": (6, 19, "moonrise"),
    "dhanteras": (6, 28, "evening"),
    "naraka-chaturdashi": (6, 29, "dawn"),
    "diwali": (6, 30, "evening"),
    "govardhan-puja": (7, 1, "sunrise"),
    "bhai-dooj": (7, 2, "afternoon"),
    "chhath": (7, 6, "sunrise"),
    "tulsi-vivah": (7, 12, "sunrise"),
    "kartik-purnima": (7, 15, "sunrise"),
    "vasant-panchami": (10, 5, "forenoon"),
    "maha-shivaratri": (10, 29, "midnight"),
    "holika-dahan": (11, 15, "evening"),
}

# Recurring observances: id -> (tithi numbers, time)
RECURRING = {
    "ekadashi": ((11, 26), "sunrise"),
    "purnima": ((15,), "sunrise"),
    "amavasya": ((30,), "sunrise"),
    "sankashti": ((19,), "moonrise"),
    "pradosh": ((13, 28), "evening"),
    "shivaratri": ((29,), "midnight"),
}

FLAGS = swe.FLG_SWIEPH  # falls back to the built-in Moshier ephemeris when no files are present


def lon(jd, body, sidereal=False):
    return swe.calc_ut(jd, body, FLAGS | (swe.FLG_SIDEREAL if sidereal else 0))[0][0]


def elongation(jd):
    return (lon(jd, swe.MOON) - lon(jd, swe.SUN)) % 360


def tithi_at(jd):
    return int(elongation(jd) // 12) + 1


def find_crossing(f, a, b, target, period=360):
    """Bisect for f(jd) == target between a and b (f increasing modulo period)."""
    for _ in range(40):
        m = (a + b) / 2
        if (f(m) - target) % period < period / 2:
            b = m
        else:
            a = m
    return (a + b) / 2


def tithi_intervals(jd0, jd1):
    """All tithis between jd0 and jd1 as (number, start, end)."""
    out = []
    t = jd0
    cur = tithi_at(t)
    start = None
    while t < jd1:
        nt = t + 0.1
        n = tithi_at(nt)
        if n != cur:
            boundary = find_crossing(elongation, t, nt, ((cur) * 12) % 360)
            if start is not None:
                out.append([cur, start, boundary])
            start = boundary
            cur = cur % 30 + 1
            # Two boundaries inside 0.1 day never happens (a tithi lasts > 19 h).
        t = nt
    return out


def lunar_months(intervals):
    """Assign an amanta month (index, adhika) to each tithi interval."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    new_moons = [iv[1] for iv in intervals if iv[0] == 1]
    signs = [int(lon(jd, swe.SUN, True) // 30) for jd in new_moons]
    month_of_newmoon = []
    for i, s in enumerate(signs):
        nxt = signs[i + 1] if i + 1 < len(signs) else (s + 1) % 12
        month_of_newmoon.append(((s + 1) % 12, nxt == s))
    result = []
    k = -1
    for iv in intervals:
        if iv[0] == 1:
            k += 1
        result.append(month_of_newmoon[k] if k >= 0 else None)
    return result


class Place:
    def __init__(self, lat, lon_, tzname):
        self.geo = (lon_, lat, 0)
        self.tz = ZoneInfo(tzname)

    def local_midnight_jd(self, d):
        dt = datetime(d.year, d.month, d.day, tzinfo=self.tz).astimezone(timezone.utc)
        return swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute / 60 + dt.second / 3600)

    def rise_set(self, jd, body, rise=True):
        flag = swe.CALC_RISE if rise else swe.CALC_SET
        res = swe.rise_trans(jd, body, flag, self.geo, 1013.25, 15)
        return res[1][0] if res[0] == 0 else None

    def to_local(self, jd):
        y, m, d, h = swe.revjul(jd)
        dt = datetime(y, m, d, tzinfo=timezone.utc) + timedelta(hours=h)
        return dt.astimezone(self.tz)


def build_city(city, first, last):
    cid, name, country, lat, lng, tzname = city
    place = Place(lat, lng, tzname)
    start = date(first, 1, 1) - timedelta(days=40)
    end = date(last, 12, 31) + timedelta(days=40)
    ndays = (end - start).days + 1

    # Times of observance for each civil day.
    days = []
    for i in range(ndays):
        d = start + timedelta(days=i)
        m0 = place.local_midnight_jd(d)
        rise = place.rise_set(m0, swe.SUN, True)
        sset = place.rise_set(rise, swe.SUN, False)
        nrise = place.rise_set(sset, swe.SUN, True)
        length = sset - rise
        moon = place.rise_set(rise, swe.MOON, True)
        days.append({
            "date": d,
            "sunrise": rise, "sunset": sset,
            "dawn": rise - 0.067,              # arunodaya, ~96 minutes before sunrise
            "forenoon": rise + 0.3 * length,   # purvahna
            "midday": rise + 0.5 * length,     # madhyahna
            "afternoon": rise + 0.7 * length,  # aparahna
            "evening": sset + 0.05,            # pradosh, ~72 minutes after sunset
            "midnight": (sset + nrise) / 2,    # nishita
            "moonrise": moon if moon is not None and moon < nrise else None,
            "next_sunrise": nrise,
        })

    intervals = tithi_intervals(days[0]["sunrise"] - 2, days[-1]["next_sunrise"] + 2)
    months = lunar_months(intervals)

    def interval_at(jd):
        lo, hi = 0, len(intervals) - 1
        while lo <= hi:
            m = (lo + hi) // 2
            if intervals[m][2] <= jd:
                lo = m + 1
            elif intervals[m][1] > jd:
                hi = m - 1
            else:
                return m
        return None

    def observance_day(k, when):
        """Index of the civil day on which tithi interval k is observed."""
        _, s, e = intervals[k]
        hits = [i for i, d in enumerate(days) if d[when] is not None and s <= d[when] < e]
        if hits:
            return hits[0]
        # The tithi misses the time of worship entirely: use the day holding most of it.
        mid = (s + e) / 2
        for i, d in enumerate(days):
            if d["sunrise"] <= mid < d["next_sunrise"]:
                return i
        return None

    # Restrict the day search to a window around each interval for speed.
    def observance_day_fast(k, when):
        _, s, e = intervals[k]
        i0 = max(0, int(s - days[0]["sunrise"]) - 2)
        sub = days[i0:i0 + 5]
        hits = [i0 + i for i, d in enumerate(sub) if d[when] is not None and s <= d[when] < e]
        if hits:
            return hits[0]
        mid = (s + e) / 2
        for i, d in enumerate(sub):
            if d["sunrise"] <= mid < d["next_sunrise"]:
                return i0 + i
        return observance_day(k, when)

    first_idx = (date(first, 1, 1) - start).days
    last_idx = (date(last, 12, 31) - start).days

    events = []

    def add(i, eid, label=None):
        if i is not None and first_idx <= i <= last_idx:
            e = [i - first_idx, eid]
            if label:
                e.append(label)
            events.append(e)

    for k, (t, s, e) in enumerate(intervals):
        if months[k] is None:
            continue
        mi, adhika = months[k]
        for fid, (fm, ft, when) in FESTIVALS.items():
            if not adhika and fm == mi and ft == t:
                i = observance_day_fast(k, when)
                if fid == "raksha-bandhan" and i is not None:
                    # The first half of Purnima is Bhadra (Vishti karana), when rakhi is not tied.
                    # If Bhadra covers the afternoon and Purnima lasts three muhurtas past the
                    # next sunrise, Raksha Bandhan moves to the next day.
                    bhadra_end = (s + e) / 2
                    if days[i]["afternoon"] < bhadra_end and e - days[i + 1]["sunrise"] >= 0.1:
                        i += 1
                add(i, fid)
                if fid == "holika-dahan" and i is not None:
                    add(i + 1, "holi")
                if fid == "janmashtami" and i is not None:
                    # Vaishnava (ISKCON) reckoning: Ashtami at sunrise, never before the Smarta day.
                    v = observance_day_fast(k, "sunrise")
                    if v is not None and v > i:
                        add(v, "janmashtami-vaishnava")
        for rid, (ts, when) in RECURRING.items():
            if t not in ts:
                continue
            label = None
            # Krishna-paksha days are named by the purnimanta month (the next amanta month),
            # as in most North Indian and diaspora calendars.
            disp = mi if t <= 15 else (mi + 1) % 12
            if rid == "ekadashi":
                names = ADHIKA_EKADASHI if adhika else EKADASHI[mi]
                label = names[0 if t == 11 else 1]
            elif rid in ("purnima", "amavasya"):
                label = ("Adhika " if adhika else "") + MONTHS[disp]
            add(observance_day_fast(k, when), rid, label)

    # Makar Sankranti: the sun enters sidereal Capricorn (observed next day if after sunset).
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    for y in range(first, last + 1):
        a = place.local_midnight_jd(date(y, 1, 10))
        jd = find_crossing(lambda x: lon(x, swe.SUN, True), a, a + 10, 270)
        local = place.to_local(jd).date()
        i = (local - start).days
        if jd > days[i]["sunset"]:
            i += 1
        add(i, "makar-sankranti")

    events.sort(key=lambda e: (e[0], e[1]))

    # Per-day panchang for the published range: tithi at sunrise, amanta month, adhika,
    # sunrise and sunset as local minutes after midnight.
    panchang = []
    for i in range(first_idx, last_idx + 1):
        d = days[i]
        k = interval_at(d["sunrise"])
        t = intervals[k][0]
        mi, adhika = months[k]
        r = place.to_local(d["sunrise"])
        st = place.to_local(d["sunset"])
        panchang.append([t, mi, 1 if adhika else 0, r.hour * 60 + r.minute, st.hour * 60 + st.minute])

    return {
        "id": cid, "name": name, "country": country, "tz": tzname,
        "start": date(first, 1, 1).isoformat(),
        "days": panchang,
        "events": events,
    }


def main():
    first = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
    last = int(sys.argv[2]) if len(sys.argv) > 2 else 2028
    os.makedirs(OUT, exist_ok=True)
    index = {"start": f"{first}-01-01", "end": f"{last}-12-31", "cities": []}
    only = os.environ.get("CITY")
    for c in CITIES:
        if only and c[0] != only:
            continue
        data = build_city(c, first, last)
        with open(os.path.join(OUT, c[0] + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, separators=(",", ":"))
        index["cities"].append({"id": c[0], "name": c[1], "country": c[2], "tz": c[5]})
        print(c[0], len(data["events"]), "events")
    if not only:
        with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
            json.dump(index, f, separators=(",", ":"))


if __name__ == "__main__":
    main()
