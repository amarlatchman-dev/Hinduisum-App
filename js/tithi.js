/* Dharma Path: the tithi of any date from 1930 to 2060, and the day it returns in later years.
   Reads calendar/tithi.json (made by scripts/build_tithi_table.py): the minute each tithi begins,
   and the amanta month of each lunation. Times are minutes since 1970-01-01 UTC. A place is
   { lat, lon, offset }, offset being its UTC offset in minutes (used only to name the local day). */
(function () {
  const RAD = Math.PI / 180;

  // Sunrise (upper limb, with refraction) in UTC minutes on a local calendar date at a place, by the
  // standard sunrise equation, set 1.5 minutes earlier to agree with the Swiss Ephemeris times of the
  // city calendars (it then gives the same tithi at sunrise on 19,726 of their 19,728 days).
  function sunrise(y, m, d, lat, lon) {
    const days = Date.UTC(y, m - 1, d) / 86400000 + 2440587.5 - 2451545.0;
    const jStar = Math.round(days) + 0.0008 - lon / 360;
    const M = (357.5291 + 0.98560028 * jStar) % 360;
    const C = 1.9148 * Math.sin(M * RAD) + 0.02 * Math.sin(2 * M * RAD) + 0.0003 * Math.sin(3 * M * RAD);
    const lam = (M + C + 180 + 102.9372) % 360;
    const transit = 2451545.0 + jStar + 0.0053 * Math.sin(M * RAD) - 0.0069 * Math.sin(2 * lam * RAD);
    const sinD = Math.sin(lam * RAD) * Math.sin(23.4397 * RAD);
    const cosD = Math.cos(Math.asin(sinD));
    const cosW = (Math.sin(-0.833 * RAD) - Math.sin(lat * RAD) * sinD) / (Math.cos(lat * RAD) * cosD);
    const w = Math.acos(Math.max(-1, Math.min(1, cosW))) / RAD;
    return Math.round((transit - w / 360 - 2440587.5) * 1440 - 1.5);
  }

  const ymdOf = (ms) => { const t = new Date(ms); return { y: t.getUTCFullYear(), m: t.getUTCMonth() + 1, d: t.getUTCDate() }; };

  function make(table) {
    const starts = new Array(table.d.length + 1);
    starts[0] = table.start;
    for (let i = 0; i < table.d.length; i++) starts[i + 1] = starts[i] + table.d[i];
    const first = starts[0], last = starts[starts.length - 1];

    // The tithi in force at a moment: { t: 1..30, month: 0..11 (amanta, 0 = Chaitra), adhika, i }
    function at(minute) {
      if (!(minute >= first && minute < last)) return null;
      let lo = 0, hi = starts.length - 1;
      while (hi - lo > 1) { const mid = (lo + hi) >> 1; if (starts[mid] <= minute) lo = mid; else hi = mid; }
      const code = table.months[Math.floor(lo / 30)];
      return { t: (lo % 30) + 1, month: code >> 1, adhika: !!(code & 1), i: lo };
    }

    // The tithi of a local date: at its sunrise, or at a local time (minutes after midnight).
    function ofDate(y, m, d, place, localMinutes) {
      return at(localMinutes == null ? sunrise(y, m, d, place.lat, place.lon)
        : Date.UTC(y, m - 1, d) / 60000 + localMinutes - (place.offset || 0));
    }

    // The day tithi number i (an index into the table) is kept: the day it is in force at sunrise,
    // the first if there are two; a tithi that begins and ends between two sunrises (kshaya) is
    // kept on the day it begins.
    function keptOn(i, place) {
      const s = starts[i], e = starts[i + 1];
      const local = ymdOf((s + (place.offset || 0)) * 60000);
      for (let k = -1; k <= 2; k++) {
        const day = ymdOf(Date.UTC(local.y, local.m - 1, local.d + k));
        const r = sunrise(day.y, day.m, day.d, place.lat, place.lon);
        if (r >= s && r < e) return day;
      }
      return local;
    }

    // The days in a given year on which tithi t of amanta month `month` is kept. An adhika month is
    // passed over for the regular month of the same name.
    function datesOf(year, month, t, place) {
      const lo = Date.UTC(year - 1, 10, 1) / 60000, hi = Date.UTC(year + 1, 1, 1) / 60000;
      const out = [];
      for (let lun = 0; lun < table.months.length; lun++) {
        const s0 = starts[lun * 30];
        if (s0 < lo) continue;
        if (s0 > hi) break;
        const code = table.months[lun];
        if (code >> 1 !== month || code & 1) continue;
        const day = keptOn(lun * 30 + t - 1, place);
        if (day.y === year) out.push(day);
      }
      return out;
    }

    // When tithi number i (an index into the table) begins and ends.
    const bounds = (i) => [starts[i], starts[i + 1]];

    return { at, ofDate, keptOn, datesOf, bounds, first, last };
  }

  window.Tithi = { sunrise, make };
})();
