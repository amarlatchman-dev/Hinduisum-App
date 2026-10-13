(function () {
  "use strict";

  const C = window.CONTENT;
  const P = window.PRAYERS;
  const PM = window.PRAYER_META;
  const view = document.getElementById("view");
  const titleEl = document.getElementById("pageTitle");
  const backBtn = document.getElementById("backBtn");
  const topbar = document.getElementById("topbar");
  const BRAND = '<span class="mark">ॐ</span><span>Dharma Path</span>';

  /* ====================================================================== */
  /* Utilities                                                               */
  /* ====================================================================== */
  const store = {
    get(key, fallback) {
      try {
        const v = localStorage.getItem("dp:" + key);
        return v === null ? fallback : JSON.parse(v);
      } catch (e) {
        return fallback;
      }
    },
    set(key, value) {
      try { localStorage.setItem("dp:" + key, JSON.stringify(value)); } catch (e) { /* storage unavailable */ }
    }
  };

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const byId = (list, id) => list.find((x) => x.id === id);
  const prayer = (id) => byId(P, id);

  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  const MON = MONTHS.map((m) => m.slice(0, 3));
  const WEEKDAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const LUNAR = ["Chaitra", "Vaishakha", "Jyeshtha", "Ashadha", "Shravana", "Bhadrapada", "Ashvin", "Kartika", "Margashirsha", "Pausha", "Magha", "Phalguna"];
  const TITHI = ["Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi"];

  const pad = (n) => String(n).padStart(2, "0");
  const ymd = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  function parseYmd(s) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || "");
    return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
  }
  const utcDay = (d) => Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000;
  const today = () => { const d = new Date(); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); };
  const dayOfYear = (d) => Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 86400000);
  const longDate = (d) => `${WEEKDAYS[d.getDay()]}, ${d.getDate()} ${MONTHS[d.getMonth()]}`;

  function sealClass(text) {
    const n = [...String(text)].length;
    return n <= 3 ? "" : n <= 6 ? "m" : "s";
  }
  const seal = (text, extra = "") => `<span class="seal ${sealClass(text)} ${extra}" aria-hidden="true">${esc(text)}</span>`;

  function mandala() {
    let p = "";
    for (let i = 0; i < 16; i++) p += `<ellipse cx="100" cy="50" rx="11" ry="36" transform="rotate(${i * 22.5} 100 100)"/>`;
    for (let i = 0; i < 8; i++) p += `<ellipse cx="100" cy="68" rx="9" ry="24" transform="rotate(${i * 45 + 22.5} 100 100)"/>`;
    return `<svg class="mandala" viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="0.7" aria-hidden="true">${p}<circle cx="100" cy="100" r="97"/><circle cx="100" cy="100" r="91"/><circle cx="100" cy="100" r="20"/><circle cx="100" cy="100" r="9"/></svg>`;
  }

  function greeting() {
    const h = new Date().getHours();
    if (h >= 4 && h < 12) return "Suprabhatam";
    if (h >= 12 && h < 17) return "Namaste";
    return "Shubh sandhya";
  }

  const cache = {};
  function loadJSON(path) {
    if (!cache[path]) {
      cache[path] = fetch(path).then((r) => {
        if (!r.ok) throw new Error(r.status);
        return r.json();
      });
      cache[path].catch(() => delete cache[path]);
    }
    return cache[path];
  }

  /* ====================================================================== */
  /* Calendar engine                                                         */
  /* ====================================================================== */
  let cal = null;

  function tzOffset(tz, at) {
    const local = new Date(at.toLocaleString("en-US", { timeZone: tz }));
    const utc = new Date(at.toLocaleString("en-US", { timeZone: "UTC" }));
    return (local - utc) / 60000;
  }

  function guessCity(cities) {
    let tz = "";
    try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; } catch (e) { /* ignore */ }
    const exact = cities.find((c) => c.tz === tz);
    if (exact) return exact.id;
    try {
      const now = new Date();
      const mine = -now.getTimezoneOffset();
      let best = cities[0], diff = Infinity;
      for (const c of cities) {
        const d = Math.abs(tzOffset(c.tz, now) - mine);
        if (d < diff) { diff = d; best = c; }
      }
      return best.id;
    } catch (e) {
      return cities[0].id;
    }
  }

  async function loadCalendar() {
    const index = await loadJSON("calendar/index.json");
    let id = store.get("city", null);
    if (!index.cities.some((c) => c.id === id)) id = guessCity(index.cities);
    if (cal && cal.id === id) return cal;
    const data = await loadJSON(`calendar/${id}.json`);
    // A named full-moon or new-moon festival replaces the generic Purnima / Amavasya entry that day.
    const MOON_FESTS = {
      purnima: ["guru-purnima", "sharad-purnima", "kartik-purnima", "hanuman-jayanti", "raksha-bandhan", "holika-dahan"],
      amavasya: ["mahalaya", "diwali"]
    };
    const ids = new Map();
    for (const e of data.events) ids.set(e[0], (ids.get(e[0]) || []).concat(e[1]));
    data.events = data.events.filter((e) => !(MOON_FESTS[e[1]] && MOON_FESTS[e[1]].some((f) => ids.get(e[0]).includes(f))));
    const byDay = new Map();
    for (const e of data.events) {
      if (!byDay.has(e[0])) byDay.set(e[0], []);
      byDay.get(e[0]).push(e);
    }
    const start = parseYmd(data.start);
    cal = { ...data, index, start, startDay: utcDay(start), byDay };
    return cal;
  }

  const calIdx = (d) => Math.round(utcDay(d) - cal.startDay);
  const calDate = (i) => new Date(cal.start.getFullYear(), cal.start.getMonth(), cal.start.getDate() + i);
  const inCal = (i) => cal && i >= 0 && i < cal.days.length;

  const FEST = (id) => byId(C.festivals, id);
  const isFestival = (id) => !!FEST(id);
  const EKADASHI_EXTRA = {
    Prabodhini: "Dev Uthani",
    Mokshada: "Gita Jayanti",
    Devshayani: "Chaturmas begins",
    Nirjala: "the strictest fast"
  };

  function obsInfo(ev) {
    const [, id, label] = ev;
    const f = FEST(id);
    if (f) {
      const parent = f.parent ? FEST(f.parent) : null;
      return {
        id, kind: "festival", name: f.dayName || f.name, deva: f.deva, summary: f.summary, meaning: f.meaning,
        guide: parent ? parent.id : f.id, guideName: parent ? parent.name : f.name,
        prayers: f.prayers || (parent && parent.prayers) || []
      };
    }
    const v = C.vrats[id];
    if (!v) return null;
    let name = v.name;
    if (label && id === "ekadashi") name = `${label} Ekadashi`;
    if (label && (id === "purnima" || id === "amavasya")) name = `${label} ${v.name}`;
    let summary = v.summary;
    if (id === "ekadashi" && EKADASHI_EXTRA[label]) summary = `${EKADASHI_EXTRA[label]}. ${v.summary}`;
    return { id, kind: id, name, deva: v.deva, summary, meaning: v.meaning, prayers: v.prayers, guide: null };
  }

  function hinduDate(i) {
    const row = cal.days[i];
    if (!row) return null;
    const [t, mi, adhika, rise, set] = row;
    const shukla = t <= 15;
    const tithi = t === 15 ? "Purnima" : t === 30 ? "Amavasya" : TITHI[(t - 1) % 15];
    // Krishna paksha is named by the following month, as in North Indian (purnimanta) calendars.
    const month = (adhika ? "Adhika " : "") + LUNAR[shukla || adhika ? mi : (mi + 1) % 12];
    const d = calDate(i);
    const ugadi = cal.events.find((e) => e[1] === "ugadi" && calDate(e[0]).getFullYear() === d.getFullYear());
    const samvat = d.getFullYear() + (ugadi && i >= ugadi[0] ? 57 : 56);
    return {
      tithi, month, samvat,
      paksha: t === 15 || t === 30 ? "" : shukla ? "Shukla" : "Krishna",
      line: `${month} · ${t === 15 || t === 30 ? "" : (shukla ? "Shukla " : "Krishna ")}${tithi}`,
      sunrise: fmtTime(rise), sunset: fmtTime(set)
    };
  }

  function fmtTime(mins) {
    const h = Math.floor(mins / 60), m = mins % 60;
    return `${((h + 11) % 12) + 1}:${pad(m)} ${h < 12 ? "am" : "pm"}`;
  }

  function relDay(i) {
    const diff = i - calIdx(today());
    if (diff === 0) return "Today";
    if (diff === 1) return "Tomorrow";
    if (diff === -1) return "Yesterday";
    if (diff < 0) return `${-diff} days ago`;
    if (diff > 1 && diff < 7) return WEEKDAYS[calDate(i).getDay()];
    return `in ${diff} days`;
  }

  function whenText(i) {
    const wd = WEEKDAYS[calDate(i).getDay()], rel = relDay(i);
    return rel === wd ? wd : `${wd} · ${rel}`;
  }

  function upcoming(fromIdx, n, filter) {
    const out = [];
    for (const e of cal.events) {
      if (e[0] < fromIdx || (filter && !filter(e))) continue;
      out.push(e);
      if (out.length >= n) break;
    }
    return out;
  }

  const cityName = () => {
    const c = cal && cal.index.cities.find((x) => x.id === cal.id);
    return c ? `${c.name}, ${c.country}` : "";
  };

  const CAL_FILTERS = [
    { id: "all", name: "All", test: () => true },
    { id: "festivals", name: "Festivals", test: (e) => isFestival(e[1]) },
    { id: "ekadashi", name: "Ekadashi", test: (e) => e[1] === "ekadashi" },
    { id: "moon", name: "Moon", test: (e) => e[1] === "purnima" || e[1] === "amavasya" },
    { id: "vrats", name: "Vrats", test: (e) => ["sankashti", "pradosh", "shivaratri"].includes(e[1]) }
  ];

  function monthGrid(y, m, mode) {
    const first = new Date(y, m, 1);
    const ndays = new Date(y, m + 1, 0).getDate();
    const t = calIdx(today());
    const lunar = new Set();
    let cells = "";
    for (let k = 0; k < first.getDay(); k++) cells += `<span class="cell out"></span>`;
    for (let d = 1; d <= ndays; d++) {
      const date = new Date(y, m, d);
      const i = calIdx(date);
      const evs = cal.byDay.get(i) || [];
      const fest = evs.some((e) => isFestival(e[1]));
      const hd = inCal(i) ? hinduDate(i) : null;
      if (hd) lunar.add(hd.month);
      const moon = evs.some((e) => e[1] === "purnima") ? "○" : evs.some((e) => e[1] === "amavasya") ? "●" : "";
      const dots = [];
      if (fest) dots.push('<i class="f"></i>');
      if (evs.some((e) => !isFestival(e[1]) && e[1] !== "purnima" && e[1] !== "amavasya")) dots.push("<i></i>");
      const cls = ["cell", i === t ? "today" : i < t ? "past" : "", fest ? "fest" : ""].join(" ");
      const label = `${d} ${MONTHS[m]}${evs.length ? ": " + evs.map((e) => obsInfo(e).name).join(", ") : ""}`;
      cells += `<a class="${cls}" href="#/day/${ymd(date)}" aria-label="${esc(label)}">${moon ? `<span class="moon">${moon}</span>` : ""}<span class="n">${d}</span><span class="dots">${dots.join("")}</span></a>`;
    }
    const prev = new Date(y, m - 1, 1), next = new Date(y, m + 1, 1);
    const canPrev = inCal(calIdx(new Date(y, m, 0)));
    const canNext = inCal(calIdx(next));
    const navAttr = (d) => mode === "page"
      ? `href="#/calendar/${d.getFullYear()}-${pad(d.getMonth() + 1)}"`
      : `href="#" data-home-month="${d.getFullYear()}-${pad(d.getMonth() + 1)}"`;
    return `
      <div class="cal-head">
        <div class="title"><h3>${MONTHS[m]} ${y}</h3><div class="meta">${esc([...lunar].join(" · "))}</div></div>
        <a class="cal-nav ${canPrev ? "" : "off"}" ${navAttr(prev)} aria-label="Previous month"><svg class="ico" viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg></a>
        <a class="cal-nav ${canNext ? "" : "off"}" ${navAttr(next)} aria-label="Next month"><svg class="ico" viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></a>
      </div>
      <div class="cal-grid">
        ${["S", "M", "T", "W", "T", "F", "S"].map((w) => `<span class="wd">${w}</span>`).join("")}
        ${cells}
      </div>
      <div class="cal-legend"><span><i class="f"></i>Festival</span><span><i></i>Vrat</span><span>○ Purnima</span><span>● Amavasya</span></div>`;
  }

  function eventRow(e, sub) {
    const info = obsInfo(e);
    const d = calDate(e[0]);
    return `<a class="row" href="#/day/${ymd(d)}">
      <span class="dateblock"><span class="d">${d.getDate()}</span><span class="m">${MON[d.getMonth()]}</span></span>
      <span class="body"><h3>${esc(info.name)}</h3><p>${esc(sub || `${relDay(e[0])} · ${info.summary}`)}</p></span>
      <span class="chev">›</span>
    </a>`;
  }

  /* ====================================================================== */
  /* Prayer helpers                                                          */
  /* ====================================================================== */
  const typeOf = (id) => byId(PM.types, id);
  const deityOf = (id) => byId(PM.deities, id);
  const prayerSub = (p) => `${typeOf(p.type).one} · ${deityOf(p.deity).name}${p.lang && p.lang !== "Sanskrit" ? " · " + p.lang : ""}`;

  function prayerRow(p) {
    return `<a class="row" href="#/puja/${p.id}">
      ${seal(deityOf(p.deity).deva)}
      <span class="body"><h3>${esc(p.name)}</h3><p>${esc(prayerSub(p))}</p></span>
      <span class="chev">›</span>
    </a>`;
  }

  function momentNow(d) {
    const h = d.getHours() + d.getMinutes() / 60;
    if (h >= 4 && h < 9) return { label: "Early morning", title: "Greet the day", text: "Prayers for waking, bathing and greeting the rising sun.", ids: ["morning", "bhumi", "japa-kusuma", "gayatri"] };
    if (h >= 9 && h < 11.5) return { label: "Morning", title: "Begin your work", text: "Ask Ganesha and Saraswati to bless what you begin today.", ids: ["ganesha", "saraswati", "ganesh-mantra", "guru"] };
    if (h >= 11.5 && h < 14.5) return { label: "Midday", title: "Before your meal", text: "Offer your food before eating, so that the meal becomes prasad.", ids: ["brahmarpanam", "annapurna", "sahana"] };
    if (h >= 14.5 && h < 17.5) return { label: "Afternoon", title: "A pause for peace", text: "A few quiet verses to steady the mind in the middle of the day.", ids: ["sarve-bhavantu", "asato-ma", "shantakaram", "lokah"] };
    if (h >= 17.5 && h < 19.5) return { label: "Dusk", title: "Light the lamp", text: "Sandhya, the meeting of day and night, is the time for the evening lamp and aarti.", ids: ["deepa-jyoti", "jagdish", "karpura-gauram"] };
    if (h >= 19.5 && h < 21.5) return { label: "Evening", title: "Evening prayer", text: "Close the day with aarti, and offer your evening meal with gratitude.", ids: ["jagdish", "brahmarpanam", "tvameva"] };
    return { label: "Night", title: "Before sleep", text: "Let go of the day's mistakes and rest in the care of the Divine.", ids: ["kara-charana", "ramaskandam", "shantakaram", "lokah"] };
  }

  /* ====================================================================== */
  /* Header & navigation chrome                                              */
  /* ====================================================================== */
  function setHeader(title, showBack) {
    titleEl.innerHTML = title ? `<span>${esc(title)}</span>` : BRAND;
    backBtn.hidden = !showBack;
  }

  function setActiveTab(tab) {
    document.querySelectorAll(".tabbar a").forEach((a) => {
      const on = a.dataset.tab === tab;
      a.classList.toggle("active", on);
      if (on) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  /* ====================================================================== */
  /* Today                                                                   */
  /* ====================================================================== */
  let homeMonth = null;

  async function homeView() {
    const now = new Date();
    const d0 = today();
    const w = C.wisdom[dayOfYear(d0) % C.wisdom.length];
    const ref = C.gitaDaily[dayOfYear(d0) % C.gitaDaily.length];
    let calHtml = "", hindu = "", eventsHtml = "", todayEvents = [];
    try {
      await loadCalendar();
      const i = calIdx(d0);
      if (inCal(i)) {
        const hd = hinduDate(i);
        hindu = `${hd.line} · Vikram Samvat ${hd.samvat}`;
        todayEvents = (cal.byDay.get(i) || []).map(obsInfo).filter(Boolean)
          .sort((a, b) => (a.kind === "festival" ? 0 : 1) - (b.kind === "festival" ? 0 : 1));
      }
      if (!homeMonth) homeMonth = [d0.getFullYear(), d0.getMonth()];
      calHtml = `<div class="card" id="homeCal">${monthGrid(homeMonth[0], homeMonth[1], "home")}</div>`;
      const next = upcoming(i, 5, (e) => isFestival(e[1]) || e[1] === "ekadashi");
      eventsHtml = next.length ? `<div class="list">${next.map((e) => eventRow(e)).join("")}</div>` : "";
    } catch (e) {
      calHtml = `<div class="card empty">The calendar needs an internet connection the first time it opens.</div>`;
    }

    const mo = momentNow(now);
    const first = prayer(mo.ids[0]);

    return `
      <div class="greeting fade-in">
        <div class="date">${esc(longDate(d0))}</div>
        <h2>${greeting()}</h2>
        ${hindu ? `<div class="hindu">${esc(hindu)}</div>` : ""}
      </div>

      ${todayEvents.length ? `
        <div class="section" style="margin-top:18px">
          <div class="list">${todayEvents.map((o) => `
            <a class="row" href="#/day/${ymd(d0)}">${seal(o.deva)}
              <span class="body"><span class="eyebrow">Today</span><h3>${esc(o.name)}</h3><p>${esc(o.summary)}</p></span><span class="chev">›</span></a>`).join("")}
          </div>
        </div>` : ""}

      <a class="night verse-hero fade-in" id="gitaToday" href="#/read/gita/${ref[0]}?v=${ref[1]}" style="margin-top:${todayEvents.length ? 0 : 20}px">
        ${mandala()}
        <div class="eyebrow">Bhagavad Gita · Verse of the day</div>
        <div class="deva-text">&nbsp;</div>
        <blockquote>Loading today's verse…</blockquote>
        <div class="cite">Chapter ${ref[0]} · Verse ${ref[1]}</div>
      </a>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Sacred calendar</h2><a href="#/calendar">Full calendar</a></div>
        ${cal ? `<div class="loc-line">Dates for ${esc(cityName())} · <a href="#/location">Change</a></div>` : ""}
        ${calHtml}
        ${eventsHtml}
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">For this moment</h2><a href="#/puja">Puja room</a></div>
        <a class="card" href="#/puja/${first.id}">
          <div class="eyebrow">${esc(mo.label)} · ${esc(mo.title)}</div>
          <h3 style="font-family:var(--display);font-weight:600;font-size:1.4rem;margin:6px 0 2px">${esc(first.name)}</h3>
          <div class="meta">${esc(prayerSub(first))}</div>
          <p style="font-family:var(--deva);color:var(--gold);margin:12px 0 0;white-space:pre-line;line-height:1.85">${esc(first.verses[0][0].split("\n").slice(0, 2).join("\n"))}</p>
        </a>
      </div>

      ${continueReadingCards()}

      <div class="section">
        <div class="card">
          <div class="eyebrow">Today's wisdom</div>
          <p style="font-family:var(--display);font-size:1.3rem;line-height:1.35;margin:10px 0 6px">“${esc(w.text)}”</p>
          <p class="meta" style="margin:0 0 12px">${esc(w.source)}</p>
          <p style="margin:0;color:var(--ink-2)">${esc(w.reflection)}</p>
        </div>
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Explore</h2></div>
        <div class="tiles">
          <a class="tile" href="#/read"><span class="dv">ग्रन्थ</span><div><h3>Scriptures</h3><p>Gita, Ramayana, Mahabharata</p></div></a>
          <a class="tile" href="#/learn"><span class="dv">शिक्षा</span><div><h3>Academy</h3><p>${C.courses.length} short courses</p></div></a>
          <a class="tile" href="#/learn#rites"><span class="dv">संस्कार</span><div><h3>Rites of passage</h3><p>Step-by-step guidance</p></div></a>
          <a class="tile" href="#/japa"><span class="dv">जप</span><div><h3>Japa · Chanting</h3><p>Chant a mantra on a mala of 108 beads</p></div></a>
        </div>
      </div>

      <div class="orn"><span></span></div>
      <p class="footer-note">Dharma Path is free, private and always will be.</p>`;
  }

  function fillGitaToday() {
    const el = document.getElementById("gitaToday");
    if (!el) return;
    const ref = C.gitaDaily[dayOfYear(today()) % C.gitaDaily.length];
    loadJSON("texts/gita.json").then((d) => {
      const v = d.chapters[ref[0] - 1].verses.find((x) => x[0] === ref[1]);
      if (!v) return;
      el.querySelector(".deva-text").textContent = v[1].replace(/^.*उवाच\n/, "");
      el.querySelector("blockquote").textContent = "“" + v[3] + "”";
    }).catch(() => {
      el.querySelector("blockquote").textContent = "Open the Bhagavad Gita to read today's verse.";
    });
  }

  /* ====================================================================== */
  /* Calendar, day and festival guides                                       */
  /* ====================================================================== */
  async function calendarView(monthStr) {
    await loadCalendar();
    const t = today();
    const [y, m] = monthStr && /^\d{4}-\d{2}$/.test(monthStr) ? monthStr.split("-").map(Number) : [t.getFullYear(), t.getMonth() + 1];
    const filter = byId(CAL_FILTERS, store.get("calFilter", "all")) || CAL_FILTERS[0];
    const from = calIdx(new Date(y, m - 1, 1)), to = calIdx(new Date(y, m, 0));
    const evs = cal.events.filter((e) => e[0] >= from && e[0] <= to && filter.test(e));
    return `
      <h2 class="page-title">Calendar</h2>
      <div class="loc-line">Dates for ${esc(cityName())} · <a href="#/location">Change location</a></div>
      <div class="card">${monthGrid(y, m - 1, "page")}</div>
      <div class="chips" style="margin-top:4px;margin-bottom:12px">
        ${CAL_FILTERS.map((f) => `<button class="chip ${f.id === filter.id ? "active" : ""}" data-cal-filter="${f.id}">${f.name}</button>`).join("")}
      </div>
      ${evs.length
        ? `<div class="list">${evs.map((e) => eventRow(e, `${WEEKDAYS[calDate(e[0]).getDay()]} · ${obsInfo(e).summary}`)).join("")}</div>`
        : `<div class="card empty">No ${filter.id === "all" ? "" : filter.name.toLowerCase() + " "}observances this month.</div>`}

      <div class="section">
        <div class="section-head"><h2 class="section-title">Festival guides</h2><a href="#/festivals">All guides</a></div>
        <div class="list">${guideRows(4)}</div>
      </div>
      <p class="footer-note">Dates follow the Hindu lunar calendar, calculated astronomically for your chosen city. Local temples may observe some days a day earlier or later.</p>`;
  }

  // Next date of a festival or any of its related days (Dussehra counts for Navaratri).
  function nextOccurrence(fid, from) {
    const ids = new Set([fid, ...C.festivals.filter((x) => x.parent === fid).map((x) => x.id)]);
    const e = cal.events.find((x) => x[0] >= from && ids.has(x[1]));
    return e || null;
  }

  function guideRows(limit) {
    const from = calIdx(today());
    const majors = C.festivals.filter((f) => !f.parent).map((f) => ({ f, next: cal ? nextOccurrence(f.id, from) : null }));
    majors.sort((a, b) => (a.next ? a.next[0] : 1e9) - (b.next ? b.next[0] : 1e9));
    return majors.slice(0, limit || majors.length).map(({ f, next }) => {
      const when = next ? `${relDay(next[0])} · ${calDate(next[0]).getDate()} ${MON[calDate(next[0]).getMonth()]} ${calDate(next[0]).getFullYear()}` : f.when;
      return `<a class="row" href="#/festival/${f.id}">${seal(f.deva)}<span class="body"><h3>${esc(f.name)}</h3><p>${esc(when)}</p></span><span class="chev">›</span></a>`;
    }).join("");
  }

  async function guidesView() {
    try { await loadCalendar(); } catch (e) { /* show without dates */ }
    return `
      <h2 class="page-title">Festival guides</h2>
      <p class="page-sub">The meaning of each festival, its traditions and how to celebrate at home.</p>
      <div class="list">${guideRows()}</div>`;
  }

  async function dayView(dateStr) {
    await loadCalendar();
    const d = parseYmd(dateStr);
    if (!d) return notFound();
    const i = calIdx(d);
    if (!inCal(i)) return `<p class="empty">The calendar covers ${esc(cal.index.start.slice(0, 4))} to ${esc(cal.index.end.slice(0, 4))}.</p>`;
    const hd = hinduDate(i);
    const evs = (cal.byDay.get(i) || []).map(obsInfo).filter(Boolean)
      .sort((a, b) => (a.kind === "festival" ? 0 : 1) - (b.kind === "festival" ? 0 : 1));
    const wd = C.weekdays[d.getDay()];
    const prev = calDate(i - 1), next = calDate(i + 1);
    const suggested = [...new Set([...evs.flatMap((o) => o.prayers), ...wd.prayers])].map(prayer).filter(Boolean).slice(0, 6);

    return `
      <div class="night day-hero fade-in">
        ${mandala()}
        ${inCal(i - 1) ? `<a class="nav prev" href="#/day/${ymd(prev)}" aria-label="Previous day"><svg class="ico" viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg></a>` : ""}
        ${inCal(i + 1) ? `<a class="nav next" href="#/day/${ymd(next)}" aria-label="Next day"><svg class="ico" viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg></a>` : ""}
        <div class="eyebrow">${WEEKDAYS[d.getDay()]} · ${esc(wd.name)}</div>
        <div class="big">${d.getDate()}</div>
        <div class="month">${MONTHS[d.getMonth()]} ${d.getFullYear()}</div>
        <div class="hindu">${esc(hd.line)}<br>Vikram Samvat ${hd.samvat}</div>
        <div class="sun"><span>Sunrise ${hd.sunrise}</span><span>Sunset ${hd.sunset}</span></div>
      </div>
      <div class="loc-line">${esc(cityName())} · Tithi at sunrise · <a href="#/location">Change</a></div>

      ${evs.length ? evs.map((o) => `
        <div class="card">
          <div class="detail-head" style="margin:0 0 14px">${seal(o.deva, "lg")}<div><span class="tag gold">${o.kind === "festival" ? "Festival" : "Vrat"}</span><h2>${esc(o.name)}</h2><p>${esc(o.summary)}</p></div></div>
          <div class="prose"><p>${esc(o.meaning)}</p></div>
          ${o.guide ? `<div class="btn-row"><a class="btn" href="#/festival/${o.guide}">Read the ${esc(o.guideName)} guide</a></div>` : ""}
        </div>`).join("") : `
        <div class="card">
          <div class="eyebrow">An ordinary day</div>
          <p style="margin:8px 0 0">No major festival or vrat falls today. ${esc(wd.note)}</p>
        </div>`}

      <div class="section">
        <div class="section-head"><h2 class="section-title">Prayers for this day</h2></div>
        <div class="list">${suggested.map(prayerRow).join("")}</div>
      </div>`;
  }

  async function festivalView(id) {
    const f = FEST(id);
    if (!f) return notFound();
    if (f.parent) return festivalView(f.parent);
    let dates = "";
    try {
      await loadCalendar();
      const from = calIdx(today());
      const children = C.festivals.filter((x) => x.parent === f.id).map((x) => x.id);
      const ids = new Set([f.id, ...children]);
      const next = cal.events.find((e) => e[0] >= from - 12 && e[1] === f.id && cal.events.some((x) => ids.has(x[1]) && x[0] >= from && Math.abs(x[0] - e[0]) <= 12)) || nextOccurrence(f.id, from);
      if (next) {
        // The festival and its related days within the same season.
        const related = cal.events.filter((e) => ids.has(e[1]) && e[0] >= next[0] - 3 && e[0] <= next[0] + 16);
        dates = `
          <div class="section-head" style="margin-top:6px"><h2 class="section-title">${calDate(next[0]).getFullYear()} dates</h2></div>
          <div class="list">${related.map((e) => eventRow(e, whenText(e[0]))).join("")}</div>
          <div class="loc-line">Calculated for ${esc(cityName())} · <a href="#/location">Change</a></div>`;
      }
    } catch (e) { /* offline: show the guide without dates */ }
    const prs = (f.prayers || []).map(prayer).filter(Boolean);
    return `
      <div class="detail-head">${seal(f.deva, "lg")}<div><div class="eyebrow">Festival guide</div><h2>${esc(f.name)}</h2><p>${esc(f.when)}</p></div></div>
      ${dates}
      <div class="card prose">
        <h3>Meaning</h3>
        <p>${esc(f.meaning)}</p>
        ${f.traditions ? `<h3>Traditions</h3><ul>${f.traditions.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>` : ""}
      </div>
      ${f.atHome ? `<div class="card prose"><h3>Celebrate at home</h3><ol class="steps">${f.atHome.map((t) => `<li>${esc(t)}</li>`).join("")}</ol></div>` : ""}
      ${prs.length ? `<div class="section"><div class="section-head"><h2 class="section-title">Prayers for ${esc(f.name.split(" ·")[0])}</h2></div><div class="list">${prs.map(prayerRow).join("")}</div></div>` : ""}`;
  }

  async function locationView() {
    await loadCalendar();
    const cur = cal.id;
    return `
      <h2 class="page-title">Location</h2>
      <p class="page-sub">Each tithi is reckoned from local sunrise, so festivals can fall on different dates in different countries. Choose the city nearest you.</p>
      <div class="list">
        ${cal.index.cities.map((c) => `
          <a class="row" href="#" data-city="${c.id}">
            <span class="body"><h3>${esc(c.name)}</h3><p>${esc(c.country)}</p></span>
            ${c.id === cur ? `<span class="tag gold">Selected</span>` : ""}
          </a>`).join("")}
      </div>`;
  }

  /* ====================================================================== */
  /* Puja                                                                    */
  /* ====================================================================== */
  async function pujaView(query) {
    const now = new Date();
    const mo = momentNow(now);
    const wd = C.weekdays[now.getDay()];
    let todayObs = [];
    try {
      await loadCalendar();
      todayObs = (cal.byDay.get(calIdx(today())) || []).map(obsInfo).filter(Boolean)
        .sort((a, b) => (a.kind === "festival" ? 0 : 1) - (b.kind === "festival" ? 0 : 1));
    } catch (e) { /* calendar offline */ }

    const ids = [...new Set([...todayObs.flatMap((o) => o.prayers.slice(0, 2)), ...mo.ids, wd.prayers[0]])];
    const picks = ids.map(prayer).filter(Boolean).slice(0, 5);
    const first = picks[0];

    const t = query.get("t") || "", dei = query.get("d") || "", mom = query.get("m") || "";
    const q = (query.get("q") || "").trim();
    const href = (o) => {
      const p = new URLSearchParams({ t, d: dei, m: mom, ...o });
      [...p.keys()].forEach((k) => { if (!p.get(k)) p.delete(k); });
      const s = p.toString();
      return "#/puja#browse" + (s ? "?" + s : "");
    };
    const favs = store.get("favorites", []);
    const filtering = t || dei || mom || query.get("fav");

    return `
      <h2 class="page-title">Puja</h2>
      <p class="page-sub">${P.length} prayers, mantras, aartis, chalisas and bhajans, each with meaning.</p>

      <div class="night moment-card fade-in">
        ${mandala()}
        <div class="eyebrow">${esc(mo.label)} · ${WEEKDAYS[now.getDay()]}</div>
        <div class="title">${esc(todayObs.length ? todayObs[0].name : mo.title)}</div>
        <div class="meta">${esc(todayObs.length ? todayObs[0].summary : mo.text)}</div>
        <div class="deva-line">${esc(first.verses[0][0].split("\n").slice(0, 2).join("\n"))}</div>
        <div class="mini-list">
          ${picks.map((p) => `<a href="#/puja/${p.id}"><span>${esc(p.name)}</span><span>${esc(typeOf(p.type).one)}</span></a>`).join("")}
        </div>
      </div>
      <p class="meta" style="margin:-4px 4px 18px">${esc(wd.note)}</p>

      <div class="section-head"><h2 class="section-title">Moments</h2></div>
      <div class="chips">
        ${PM.moments.map((m) => `<a class="chip ${mom === m.id ? "active" : ""}" href="${href({ m: mom === m.id ? "" : m.id })}">${esc(m.name)}</a>`).join("")}
      </div>

      <div class="tiles" style="margin:16px 0 4px">
        <a class="tile" href="#/japa"><span class="dv">जप</span><div><h3>Japa · Chanting</h3><p>Mantra chanting with a mala counter</p></div></a>
        <a class="tile" href="${href({ fav: "1" })}" data-favs><span class="dv">प्रिय</span><div><h3>Favourites</h3><p>${favs.length} saved</p></div></a>
      </div>

      <div class="section" id="browse">
        <div class="section-head"><h2 class="section-title">Browse</h2>${filtering ? `<a href="#/puja#browse">Clear filters</a>` : ""}</div>
        <div class="chips">
          <a class="chip ${!t ? "active" : ""}" href="${href({ t: "" })}">All types</a>
          ${PM.types.map((x) => `<a class="chip ${t === x.id ? "active" : ""}" href="${href({ t: t === x.id ? "" : x.id })}">${esc(x.name)}</a>`).join("")}
        </div>
        <div class="chips" style="margin-top:4px;margin-bottom:12px">
          <a class="chip ${!dei ? "active" : ""}" href="${href({ d: "" })}">Every deity</a>
          ${PM.deities.map((x) => `<a class="chip ${dei === x.id ? "active" : ""}" href="${href({ d: dei === x.id ? "" : x.id })}"><span class="dv">${esc(x.deva)}</span>${esc(x.name)}</a>`).join("")}
        </div>
        <div class="search-wrap">
          <svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg>
          <input class="search" id="prayerSearch" type="search" placeholder="Search prayers" value="${esc(q)}" autocomplete="off">
        </div>
        <div id="prayerResults">${prayerResults(t, dei, mom, q, query.get("fav") === "1")}</div>
      </div>`;
  }

  function prayerResults(t, dei, mom, q, favOnly) {
    if (!t && !dei && !mom && !q && !favOnly) {
      return `<div class="tiles">${PM.types.map((ty) => {
        const n = P.filter((p) => p.type === ty.id).length;
        return `<a class="tile" href="#/puja#browse?t=${ty.id}"><span class="dv">${esc(ty.deva)}</span><div><h3>${esc(ty.name)}</h3><p>${n} · ${esc(ty.about)}</p></div></a>`;
      }).join("")}</div>`;
    }
    const favs = store.get("favorites", []);
    const needle = q.toLowerCase();
    const list = P.filter((p) =>
      (!t || p.type === t) && (!dei || p.deity === dei) && (!mom || p.moments.includes(mom)) &&
      (!favOnly || favs.includes(p.id)) &&
      (!needle || (p.name + " " + p.about + " " + deityOf(p.deity).name + " " + p.verses.map((v) => v[1]).join(" ")).toLowerCase().includes(needle)));
    if (!list.length) return `<div class="card empty">${favOnly ? "No favourites yet. Tap ☆ on any prayer to save it here." : "No prayers match these filters."}</div>`;
    const groups = PM.types.map((ty) => ({ ty, items: list.filter((p) => p.type === ty.id) })).filter((g) => g.items.length);
    return groups.map((g) => `
      <div class="eyebrow" style="margin:18px 4px 8px">${esc(g.ty.name)} · ${g.items.length}</div>
      <div class="list">${g.items.map(prayerRow).join("")}</div>`).join("");
  }

  function prayerView(id) {
    const p = prayer(id);
    if (!p) return notFound();
    const isFav = store.get("favorites", []).includes(id);
    const show = store.get("prayerShow", { dev: true, rom: true, en: true });
    const scale = store.get("prayerScale", 1);
    const related = P.filter((x) => x.deity === p.deity && x.id !== p.id).slice(0, 4);
    const hide = ["dev", "rom", "en"].filter((k) => !show[k]).map((k) => "hide-" + k).join(" ");
    return `
      <div class="detail-head">${seal(deityOf(p.deity).deva, "lg")}<div><div class="eyebrow">${esc(typeOf(p.type).one)} · ${esc(deityOf(p.deity).name)}</div><h2>${esc(p.name)}</h2><p>${esc(p.author)}</p></div></div>
      <div class="card"><p style="margin:0;color:var(--ink-2)">${esc(p.about)}</p>
        <div class="btn-row" style="margin-top:14px">
          <button class="btn ${isFav ? "" : "ghost"}" data-fav="${p.id}">${isFav ? "★ Saved" : "☆ Save"}</button>
          ${p.japa ? `<a class="btn ghost" href="#/japa?m=${p.id}">Chant on the mala</a>` : ""}
          ${"speechSynthesis" in window ? `<button class="btn ghost" data-speak="${p.id}">Read meaning aloud</button>` : ""}
        </div>
      </div>
      <div class="chips wrap" style="margin:6px 0 12px">
        <button class="chip ${show.dev ? "active" : ""}" data-show="dev">देवनागरी</button>
        <button class="chip ${show.rom ? "active" : ""}" data-show="rom">Roman</button>
        <button class="chip ${show.en ? "active" : ""}" data-show="en">Meaning</button>
        <button class="chip" data-pscale="-1" aria-label="Smaller text">A−</button>
        <button class="chip" data-pscale="1" aria-label="Larger text">A+</button>
      </div>
      <div class="card ${hide}" id="stanzas" style="--scale:${scale}">
        ${p.verses.map((v) => `
          <div class="stanza ${v[3] === "Refrain" ? "refrain" : ""}">
            ${v[3] ? `<span class="eyebrow label">${esc(v[3])}</span>` : ""}
            <p class="dev">${esc(v[0])}</p>
            <p class="rom">${esc(v[1])}</p>
            <p class="en">${esc(v[2])}</p>
          </div>`).join("")}
      </div>
      <p class="meta" style="margin:0 4px">${esc(p.lang)}${p.verses.length > 1 ? ` · ${p.verses.length} verses` : ""}. Translation by Dharma Path.</p>
      ${related.length ? `<div class="section"><div class="section-head"><h2 class="section-title">More for ${esc(deityOf(p.deity).name)}</h2><a href="#/puja#browse?d=${p.deity}">See all</a></div><div class="list">${related.map(prayerRow).join("")}</div></div>` : ""}`;
  }

  // Turn scholarly IAST into an easy reading for chanting: "oṃ namaḥ śivāya" → "Om Namah Shivaya".
  function readable(iast) {
    return iast
      .replace(/[śṣ]/g, "sh").replace(/[ŚṢ]/g, "Sh")
      .replace(/ṛ/g, "ri").replace(/[ṃṁ]/g, "m").replace(/ḥ/g, "h")
      .replace(/ā/g, "a").replace(/ī/g, "i").replace(/ū/g, "u")
      .replace(/[ñṅṇ]/g, "n").replace(/ṭ/g, "t").replace(/ḍ/g, "d")
      .replace(/c(?!h)/g, "ch").replace(/'/g, "")
      .replace(/(^|[\s-])([a-z])/g, (m, sp, ch) => sp + ch.toUpperCase());
  }

  const japaKey = (id) => "japa:" + id;
  const japaState = (id) => store.get(japaKey(id), { count: 0, malas: 0 });

  function japaView(query) {
    const mantras = P.filter((p) => p.japa);
    const id = query.get("m") || store.get("japaMantra", "shiva");
    const m = byId(mantras, id) || mantras[0];
    const { count, malas } = japaState(m.id);
    const R = 100, CIRC = 2 * Math.PI * R;
    return `
      <div class="eyebrow" style="margin:14px 2px 0">Mantra chanting · Mala counter</div>
      <h2 class="page-title" style="margin-top:4px">Japa</h2>
      <p class="page-sub">Japa is the quiet, repeated chanting of a mantra, traditionally counted on a mala of 108 beads. Choose a mantra, then tap the circle each time you chant it.</p>
      <div class="card japa" data-mantra="${m.id}">
        <div class="eyebrow">Now chanting</div>
        <p class="japa-dev">${esc(m.verses[0][0])}</p>
        <p class="japa-say">${esc(readable(m.verses[0][1]))}</p>
        <p class="japa-mean">${esc(m.verses[0][2])}</p>
        <button class="chip" data-scroll="mantras">Choose a different mantra</button>
        <button class="japa-ring" id="japaBtn" aria-label="Count one chant">
          <svg viewBox="0 0 220 220"><circle cx="110" cy="110" r="${R}" stroke="rgba(212,176,106,0.18)"/><circle id="japaArc" cx="110" cy="110" r="${R}" stroke="#d4b06a" stroke-linecap="round" stroke-dasharray="${CIRC}" stroke-dashoffset="${CIRC * (1 - count / 108)}"/></svg>
          <span class="count" id="japaCount">${count}</span><span class="of">OF 108 BEADS</span>
        </button>
        <p class="meta"><span id="malaCount">${malas}</span> full ${malas === 1 ? "mala" : "malas"} chanted</p>
        <button class="btn ghost" id="japaReset">Start again</button>
      </div>
      <p class="footer-note" style="margin-top:6px">Each mantra keeps its own count. Your phone vibrates gently when you finish a mala.</p>

      <div class="section" id="mantras">
        <div class="section-head"><h2 class="section-title">Choose a mantra</h2></div>
        <div class="list">
          ${mantras.map((p) => {
            const st = japaState(p.id);
            const line = readable(p.verses[0][1].split("\n")[0]);
            const same = line.toLowerCase().replace(/[^a-z]/g, "") === p.name.toLowerCase().replace(/[^a-z]/g, "");
            return `<a class="row" href="#/japa?m=${p.id}">
              ${seal(deityOf(p.deity).deva)}
              <span class="body"><h3>${esc(p.name)}</h3>${same ? "" : `<p style="font-style:italic;color:var(--ink-2)">${esc(line)}${p.verses[0][1].includes("\n") ? " …" : ""}</p>`}<p>${esc(p.gist)}</p>${st.malas ? `<p>${st.malas} ${st.malas === 1 ? "mala" : "malas"} chanted</p>` : ""}</span>
              ${p.id === m.id ? `<span class="tag gold">Chanting</span>` : `<span class="chev">›</span>`}
            </a>`;
          }).join("")}
        </div>
      </div>`;
  }

  function bindJapa() {
    const card = view.querySelector(".japa");
    const id = card.dataset.mantra;
    const btn = document.getElementById("japaBtn");
    const arc = document.getElementById("japaArc");
    const countEl = document.getElementById("japaCount");
    const malaEl = document.getElementById("malaCount");
    const CIRC = 2 * Math.PI * 100;
    const paint = (st) => {
      countEl.textContent = st.count;
      arc.setAttribute("stroke-dashoffset", CIRC * (1 - st.count / 108));
      malaEl.textContent = st.malas;
      malaEl.nextSibling.textContent = ` full ${st.malas === 1 ? "mala" : "malas"} chanted`;
    };

    store.set("japaMantra", id);
    btn.addEventListener("click", () => {
      const st = japaState(id);
      st.count += 1;
      if (st.count >= 108) {
        st.count = 0;
        st.malas += 1;
        if (navigator.vibrate) navigator.vibrate([80, 60, 80]);
      } else if (navigator.vibrate) {
        navigator.vibrate(8);
      }
      store.set(japaKey(id), st);
      paint(st);
    });
    document.getElementById("japaReset").addEventListener("click", () => {
      const st = { count: 0, malas: 0 };
      store.set(japaKey(id), st);
      paint(st);
    });
    card.querySelector("[data-scroll]").addEventListener("click", () => {
      document.getElementById("mantras").scrollIntoView({ behavior: "smooth" });
    });
  }

  /* ====================================================================== */
  /* Learn                                                                   */
  /* ====================================================================== */
  const completed = (courseId) => store.get("progress:" + courseId, []);

  function learnView() {
    const active = store.get("academyFilter", "all");
    const courses = active === "all" ? C.courses : C.courses.filter((c) => c.category === active);
    return `
      <h2 class="page-title">Learn</h2>
      <p class="page-sub">Short courses on Hindu thought and practice, and guides to the sacred rites of life.</p>
      <div class="section-head"><h2 class="section-title">Academy</h2></div>
      <div class="chips" style="margin-bottom:12px">
        ${C.categories.map((c) => `<button class="chip ${c.id === active ? "active" : ""}" data-filter="${c.id}">${esc(c.name)}</button>`).join("")}
      </div>
      <div class="list">
        ${courses.map((c) => {
          const n = completed(c.id).length;
          return `<a class="row" href="#/academy/${c.id}">${seal(c.deva)}
            <span class="body"><h3>${esc(c.title)}</h3><p>${esc(c.subtitle)} · ${c.lessons.length} lessons${n ? ` · ${n} done` : ""}</p>
            ${n ? `<div class="progress"><span style="width:${(n / c.lessons.length) * 100}%"></span></div>` : ""}</span>
            <span class="chev">›</span></a>`;
        }).join("") || `<p class="empty">No courses in this category yet.</p>`}
      </div>

      <div class="section" id="rites">
        <div class="section-head"><h2 class="section-title">Rites of passage</h2></div>
        <p class="lede">The samskaras mark each stage of life. Follow the steps yourself, or use them to prepare for a ceremony with a priest.</p>
        <div class="list">
          ${C.lifeEvents.map((e) => `<a class="row" href="#/life/${e.id}">${seal(e.deva)}<span class="body"><h3>${esc(e.name)}</h3><p>${esc(e.sanskrit)} · ${esc(e.summary)}</p></span><span class="chev">›</span></a>`).join("")}
        </div>
      </div>`;
  }

  function courseView(id) {
    const c = byId(C.courses, id);
    if (!c) return notFound();
    const done = completed(id);
    return `
      <div class="detail-head">${seal(c.deva, "lg")}<div><div class="eyebrow">Academy · ${c.lessons.length} lessons</div><h2>${esc(c.title)}</h2><p>${esc(c.subtitle)}</p></div></div>
      <div class="list">
        ${c.lessons.map((l, i) => `
          <details class="lesson ${done.includes(i) ? "done" : ""}" ${i === 0 && !done.length ? "open" : ""}>
            <summary><span class="num">${done.includes(i) ? "✓" : i + 1}</span><h3>${esc(l.title)}</h3></summary>
            <div class="body prose">${l.body}
              <button class="btn ${done.includes(i) ? "ghost" : ""}" data-complete="${id}:${i}">${done.includes(i) ? "Completed ✓" : "Mark as complete"}</button>
            </div>
          </details>`).join("")}
      </div>`;
  }

  function lifeEventView(id) {
    const e = byId(C.lifeEvents, id);
    if (!e) return notFound();
    return `
      <div class="detail-head">${seal(e.deva, "lg")}<div><div class="eyebrow">Rite of passage</div><h2>${esc(e.name)}</h2><p>${esc(e.sanskrit)}</p></div></div>
      <div class="card prose"><h3>About this rite</h3><p>${esc(e.meaning)}</p></div>
      <div class="card prose"><h3>Step by step</h3><ol class="steps">${e.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol></div>
      <div class="card prose"><h3>With a priest</h3><p>${esc(e.withPriest)}</p></div>
      <p class="footer-note">Customs vary by region and family. Where your family's tradition differs, follow it.</p>`;
  }

  /* ====================================================================== */
  /* Scriptures                                                              */
  /* ====================================================================== */
  const loadIndex = () => loadJSON("texts/index.json");

  // Every book is parts → sections. The Gita has one section per chapter.
  function loadSections(bookId, part) {
    if (bookId === "gita") {
      return loadJSON("texts/gita.json").then((d) => {
        const ch = d.chapters[part - 1];
        return ch ? [{ label: ch.name, verses: ch.verses }] : null;
      });
    }
    return loadJSON(`texts/${bookId}/${part}.json`).then((d) => d.sections);
  }

  function sectionTitle(book, part, sec, s) {
    if (book.id === "gita") return `Chapter ${part}`;
    if (book.id === "ramayana") return `Sarga ${s && s.n ? s.n : sec}`;
    return s ? s.label : `Section ${sec}`;
  }

  const readerHref = (bookId, part, sec) => bookId === "gita" ? `#/read/gita/${part}` : `#/read/${bookId}/${part}/${sec}`;
  const posKey = (bookId) => "read:pos:" + bookId;
  const getPos = (bookId) => store.get(posKey(bookId), null);

  function bookProgress(index, bookId, pos) {
    if (!index || !pos) return 0;
    const parts = index[bookId].parts;
    const total = parts.reduce((a, p) => a + p.count, 0);
    const before = parts.slice(0, pos.part - 1).reduce((a, p) => a + p.count, 0);
    return Math.min(100, Math.round(((before + pos.sec - 1 + (pos.frac || 0)) / total) * 100));
  }

  function posLabel(book, pos) {
    if (!pos) return "";
    if (book.id === "gita") return `Chapter ${pos.part}${pos.ref ? `, verse ${pos.ref}` : ""}`;
    return `${book.partLabel} ${pos.part} · ${pos.title || book.sectionLabel + " " + pos.sec}`;
  }

  function continueReadingCards() {
    const started = C.books.map((b) => ({ b, pos: getPos(b.id) })).filter((x) => x.pos).sort((a, z) => z.pos.t - a.pos.t);
    if (!started.length) return "";
    return `<div class="section"><div class="section-head"><h2 class="section-title">Continue reading</h2><a href="#/read">Library</a></div><div class="list">` +
      started.map(({ b, pos }) => `
        <a class="row" href="${readerHref(b.id, pos.part, pos.sec)}">${seal(b.sanskritTitle)}
          <span class="body"><h3>${esc(b.title)}</h3><p>${esc(posLabel(b, pos))}</p>
          <div class="progress"><span data-progress="${b.id}" style="width:0"></span></div></span>
          <span class="chev">›</span>
        </a>`).join("") + `</div></div>`;
  }

  function fillProgressBars() {
    const bars = view.querySelectorAll("[data-progress]");
    if (!bars.length) return;
    loadIndex().then((index) => {
      bars.forEach((el) => {
        const pct = bookProgress(index, el.dataset.progress, getPos(el.dataset.progress));
        el.style.width = Math.max(pct, 1) + "%";
        const label = view.querySelector(`[data-progress-label="${el.dataset.progress}"]`);
        if (label) label.textContent = pct + "% read";
      });
    }).catch(() => {});
  }

  function libraryView() {
    return `
      <h2 class="page-title">Scriptures</h2>
      <p class="page-sub">Read the great texts at your own pace. Your place in each book is saved on this device.</p>
      ${C.books.map((b) => {
        const pos = getPos(b.id);
        return `<div class="card book">
          <a class="night cover" href="#/read/${b.id}">
            ${mandala()}
            <div class="dv">${b.sanskritTitle}</div>
            <h3>${esc(b.title)}</h3>
            <p>${esc(b.tagline)}</p>
          </a>
          <div class="foot">
            ${pos ? `<div class="meta" style="display:flex;justify-content:space-between;gap:10px"><span>${esc(posLabel(b, pos))}</span><span data-progress-label="${b.id}"></span></div>
              <div class="progress"><span data-progress="${b.id}" style="width:0"></span></div>` : `<div class="meta">${esc(b.translation)}</div>`}
            <div class="btn-row" style="margin-top:14px">
              <a class="btn" href="${pos ? readerHref(b.id, pos.part, pos.sec) : readerHref(b.id, 1, 1)}">${pos ? "Continue reading" : "Begin reading"}</a>
              <a class="btn ghost" href="#/read/${b.id}">Contents</a>
            </div>
          </div>
        </div>`;
      }).join("")}
      <div class="list"><a class="row" href="#/read/about">${seal("स्रोत")}<span class="body"><h3>About these translations</h3><p>Sources and credits</p></span><span class="chev">›</span></a></div>`;
  }

  function aboutTextsView() {
    return `
      <h2 class="page-title">About the texts</h2>
      <div class="card prose">
        ${C.books.map((b) => `<h3>${esc(b.title)}</h3><p>${esc(b.about)}</p><p class="meta">${esc(b.translation)}</p>`).join("")}
      </div>
      <div class="card prose">
        <h3>Sources</h3>
        <ul>
          <li>Bhagavad Gita Sanskrit: the open <em>gita/gita</em> dataset (public domain). English: Annie Besant, <em>The Bhagavad-Gîtâ</em>, 4th ed., 1922 (public domain).</li>
          <li>Ramayana Sanskrit: critical-edition e-text (M. Tokunaga, rev. J. Smith). English: M. N. Dutt (1891–94), aligned in the Itihāsa corpus (Aralikatte et al., 2021).</li>
          <li>Mahabharata: K. M. Ganguli (1883–96). Scanned at sacred-texts.com; proofed at Distributed Proofing (Juliet Sutherland, project manager) and by Mantra Caitanya; additional proofing and formatting at sacred-texts.com by J. B. Hare.</li>
          <li>Verse pairings for the Gita and Ramayana were compiled by the open-source Katha project.</li>
        </ul>
        <p class="meta">These translations are over a century old and use archaic English (“thou”, “doth”). All texts are in the public domain.</p>
      </div>`;
  }

  async function bookView(bookId) {
    const book = byId(C.books, bookId);
    if (!book) return notFound();
    const index = await loadIndex();
    const pos = getPos(bookId);
    return `
      <div class="night book-hero fade-in">
        ${mandala()}
        <div class="eyebrow">${esc(book.partLabel)}s</div>
        <div style="font-family:var(--deva);font-size:1.5rem;color:var(--night-gold);margin-top:10px">${book.sanskritTitle}</div>
        <h2 style="font-family:var(--display);font-weight:600;font-size:2rem;margin:4px 0 2px">${esc(book.title)}</h2>
        <p class="meta" style="margin:0">${esc(book.tagline)}</p>
        ${pos ? `<div class="btn-row"><a class="btn gold" href="${readerHref(bookId, pos.part, pos.sec)}">Continue · ${esc(posLabel(book, pos))}</a></div>` : ""}
      </div>
      <p class="meta" style="margin:0 4px 14px">${esc(book.translation)}</p>
      <div class="list">
        ${index[bookId].parts.map((p) => `
          <a class="row" href="${bookId === "gita" ? readerHref("gita", p.n, 1) : `#/read/${bookId}/${p.n}`}">
            <span class="dateblock"><span class="d">${p.n}</span></span>
            <span class="body"><h3>${esc(p.name)}</h3><p>${esc(p.sub ? p.sub + " · " : "")}${p.count} ${bookId === "gita" ? "verses" : (book.sectionLabel.toLowerCase() + "s")}</p></span>
            ${pos && pos.part === p.n ? `<span class="tag gold">Reading</span>` : `<span class="chev">›</span>`}
          </a>`).join("")}
      </div>
      <button class="btn ghost" data-offline="${bookId}">Save the whole book for offline reading</button>
      <p class="meta" id="offlineStatus" style="margin:10px 4px"></p>`;
  }

  async function partView(bookId, part) {
    const book = byId(C.books, bookId);
    const index = await loadIndex();
    const meta = book && index[bookId].parts[part - 1];
    if (!meta) return notFound();
    const sections = await loadSections(bookId, part);
    const pos = getPos(bookId);
    return `
      <div class="detail-head"><span class="dateblock"><span class="d">${part}</span><span class="m">${esc(book.partLabel)}</span></span><div><div class="eyebrow">${esc(book.title)}</div><h2>${esc(meta.name)}</h2><p>${sections.length} ${book.sectionLabel.toLowerCase()}s</p></div></div>
      <div class="section-grid">
        ${sections.map((s, i) => {
          const here = pos && pos.part === part && pos.sec === i + 1;
          const label = bookId === "ramayana" ? s.n : (s.label.replace(/^Section /, "") || i + 1);
          return `<a class="sec-tile ${here ? "here" : ""}" href="${readerHref(bookId, part, i + 1)}" title="${esc(s.name || s.label)}">${esc(label)}</a>`;
        }).join("")}
      </div>`;
  }

  function renderVerse(v, prefix, showSa) {
    const [n, sa, tr, en] = v;
    return `<div class="verse" id="v-${n}" data-ref="${n}">
      <div class="vnum">${prefix}${n}</div>
      ${showSa && sa ? `<div class="sanskrit">${esc(sa)}</div><p class="translit">${esc(tr)}</p>` : ""}
      <p class="vtext">${esc(en)}</p>
    </div>`;
  }

  function renderPara(p, i) {
    const cls = /^\d+\.\s/.test(p) ? "para fn" : /^\(.{3,80}\)$/.test(p) ? "para sub" : "para";
    return `<p class="${cls}" data-i="${i}">${esc(p)}</p>`;
  }

  async function readerView(bookId, part, sec, query) {
    const book = byId(C.books, bookId);
    const index = await loadIndex();
    const meta = book && index[bookId].parts[part - 1];
    const sections = meta && await loadSections(bookId, part);
    const s = sections && sections[sec - 1];
    if (!s) return notFound();

    const showSa = store.get("read:sanskrit", true);
    const title = sectionTitle(book, part, sec, s);
    const subtitle = bookId === "gita" ? `${s.label} · ${index.gita.parts[part - 1].sub}` : bookId === "ramayana" ? `${meta.name}${s.name ? " · " + s.name : ""}` : meta.name;
    const parts = index[bookId].parts;
    const prev = sec > 1 ? [part, sec - 1] : part > 1 ? [part - 1, parts[part - 2].count] : null;
    const next = sec < sections.length ? [part, sec + 1] : part < parts.length ? [part + 1, 1] : null;
    const navLabel = (pq) => bookId === "gita" ? `Chapter ${pq[0]}` : pq[0] === part ? `${book.sectionLabel} ${pq[1]}` : `${book.partLabel} ${pq[0]}`;
    const state = { bookId, part, sec, title, target: query.get("v") };
    const body = s.verses
      ? s.verses.map((v) => renderVerse(v, bookId === "gita" ? `${part}.` : "", showSa)).join("")
      : s.paras.map(renderPara).join("");

    return { state, html: `
      <div class="reader-head">
        <div class="eyebrow">${esc(book.title)}</div>
        <h2>${esc(title)}</h2>
        <p class="meta">${esc(subtitle)}</p>
        ${bookId === "ramayana" ? `<p class="meta" style="margin-top:6px">Verse numbers skip where the old translation couldn't be matched reliably to the Sanskrit.</p>` : ""}
        <div class="reader-tools">
          <button class="chip" data-font="-1" aria-label="Smaller text">A−</button>
          <button class="chip" data-font="1" aria-label="Larger text">A+</button>
          ${book.verses ? `<button class="chip ${showSa ? "active" : ""}" data-sanskrit>संस्कृत</button>` : ""}
          <a class="chip" href="${bookId === "gita" ? "#/read/gita" : `#/read/${bookId}/${part}`}">Contents</a>
        </div>
      </div>
      <article class="reader" style="--read-scale:${store.get("read:font", 1)}">${body}</article>
      <nav class="reader-nav">
        ${prev ? `<a class="btn ghost" href="${readerHref(bookId, prev[0], prev[1])}">‹ ${esc(navLabel(prev))}</a>` : "<span></span>"}
        ${next ? `<a class="btn" href="${readerHref(bookId, next[0], next[1])}">${esc(navLabel(next))} ›</a>` : `<span class="meta">The end</span>`}
      </nav>
      <div class="read-progress"><span id="readBar"></span></div>` };
  }

  /* Track the reader's place: the first verse or paragraph visible below the top bar. */
  let readerState = null;
  let saveTimer = null;

  function currentItem() {
    const top = topbar.getBoundingClientRect().bottom + 8;
    const items = view.querySelectorAll(".reader > *");
    for (const el of items) {
      if (el.getBoundingClientRect().bottom > top + 40) return el;
    }
    return items[items.length - 1];
  }

  function saveReaderPos() {
    if (!readerState) return;
    const el = currentItem();
    if (!el) return;
    const max = document.documentElement.scrollHeight - innerHeight;
    const frac = max > 0 ? Math.min(1, scrollY / max) : 0;
    store.set(posKey(readerState.bookId), {
      part: readerState.part, sec: readerState.sec, title: readerState.title,
      ref: el.dataset.ref ? +el.dataset.ref : null,
      i: el.dataset.i ? +el.dataset.i : null,
      frac, t: Date.now()
    });
    const bar = document.getElementById("readBar");
    if (bar) bar.style.width = frac * 100 + "%";
  }

  function restoreReaderPos() {
    const st = readerState;
    let el = null;
    if (st.target) {
      el = document.getElementById("v-" + st.target);
      if (el) el.classList.add("highlight");
    } else {
      const pos = getPos(st.bookId);
      if (pos && pos.part === st.part && pos.sec === st.sec) {
        el = pos.ref != null ? document.getElementById("v-" + pos.ref)
          : pos.i != null ? view.querySelector(`.reader [data-i="${pos.i}"]`) : null;
      }
    }
    if (el) scrollTo(0, el.getBoundingClientRect().top + scrollY - topbar.getBoundingClientRect().height - 8);
    saveReaderPos();
  }

  async function saveBookOffline(bookId, btn) {
    const status = document.getElementById("offlineStatus");
    const index = await loadIndex();
    const files = bookId === "gita" ? ["texts/gita.json"] : index[bookId].parts.map((p) => `texts/${bookId}/${p.n}.json`);
    btn.disabled = true;
    let done = 0;
    for (const f of files) {
      try {
        await loadJSON(f);
      } catch (e) {
        status.textContent = "Couldn't download everything. Check your connection and try again.";
        btn.disabled = false;
        return;
      }
      done++;
      status.textContent = `Downloading… ${done} of ${files.length}`;
    }
    status.textContent = "Saved. This book now works without internet.";
    btn.textContent = "Saved for offline reading";
  }

  function notFound() {
    return `<p class="empty">This page could not be found. <a class="link" href="#/home">Return to Today</a></p>`;
  }

  /* ====================================================================== */
  /* Router                                                                  */
  /* ====================================================================== */
  const TITLES = { calendar: "Calendar", day: "Calendar", festival: "Calendar", festivals: "Calendar", location: "Calendar", puja: "Puja", japa: "Puja", read: "Scriptures", learn: "Learn", academy: "Learn", life: "Learn" };
  const TAB = { day: "calendar", festival: "calendar", festivals: "calendar", location: "calendar", japa: "puja", academy: "learn", life: "learn" };
  let routeSeq = 0;

  async function route() {
    const seq = ++routeSeq;
    if (readerState) saveReaderPos();
    readerState = null;

    const raw = location.hash.replace(/^#\/?/, "") || "home";
    const [pathAnchor, qs] = raw.split("?");
    const [path, anchor] = pathAnchor.split("#");
    let [section, id, a, b] = path.split("/");
    const query = new URLSearchParams(qs || "");
    if (section === "festivals" && id) { section = "festival"; }
    if (section === "academy" && !id) section = "learn";
    if (section === "life" && !id) section = "learn";

    if ("speechSynthesis" in window) speechSynthesis.cancel();
    const detail = (!!id && section !== "calendar") || ["japa", "location", "day", "festival", "festivals"].includes(section);
    setHeader(detail ? TITLES[section] || "" : "", detail);
    setActiveTab(TAB[section] || section);

    let html, nextReader = null;
    try {
      switch (section) {
        case "home": html = await homeView(); break;
        case "calendar": html = await calendarView(id); break;
        case "day": html = await dayView(id); break;
        case "festival": html = await festivalView(id); break;
        case "festivals": html = await guidesView(); break;
        case "location": html = await locationView(); break;
        case "puja": html = id ? prayerView(id) : await pujaView(query); break;
        case "japa": html = japaView(query); break;
        case "learn": html = learnView(); break;
        case "academy": html = courseView(id); break;
        case "life": html = lifeEventView(id); break;
        case "read":
          if (!id) html = libraryView();
          else if (id === "about") html = aboutTextsView();
          else {
            view.innerHTML = `<p class="empty">Opening…</p>`;
            let r = null;
            if (id === "gita" && a) r = await readerView(id, +a, 1, query);
            else if (b) r = await readerView(id, +a, +b, query);
            if (r) { html = typeof r === "string" ? r : r.html; nextReader = r.state || null; }
            else if (a) html = await partView(id, +a);
            else html = await bookView(id);
          }
          break;
        default: html = notFound();
      }
    } catch (e) {
      html = `<p class="empty">This page needs an internet connection the first time it opens. Please check your connection and try again.</p>`;
    }
    if (seq !== routeSeq) return; // a newer navigation won

    view.innerHTML = html;
    readerState = nextReader;
    if (anchor && document.getElementById(anchor)) document.getElementById(anchor).scrollIntoView();
    else window.scrollTo(0, 0);
    if (section === "japa") bindJapa();
    if (section === "home") fillGitaToday();
    if (section === "puja" && !id) bindPrayerSearch(query);
    fillProgressBars();
    if (readerState) restoreReaderPos();
  }

  function bindPrayerSearch(query) {
    const input = document.getElementById("prayerSearch");
    if (!input) return;
    input.addEventListener("input", () => {
      document.getElementById("prayerResults").innerHTML =
        prayerResults(query.get("t") || "", query.get("d") || "", query.get("m") || "", input.value.trim(), query.get("fav") === "1");
    });
  }

  /* ====================================================================== */
  /* Interactions                                                            */
  /* ====================================================================== */
  view.addEventListener("click", (e) => {
    const link = e.target.closest("a[data-home-month], a[data-city]");
    if (link) {
      e.preventDefault();
      if (link.dataset.homeMonth) {
        homeMonth = link.dataset.homeMonth.split("-").map(Number);
        homeMonth[1] -= 1;
        document.getElementById("homeCal").innerHTML = monthGrid(homeMonth[0], homeMonth[1], "home");
      } else {
        store.set("city", link.dataset.city);
        cal = null;
        if (history.length > 1) history.back();
        else location.hash = "#/calendar";
      }
      return;
    }

    const t = e.target.closest("button");
    if (!t) return;
    if (t.dataset.filter) {
      store.set("academyFilter", t.dataset.filter);
      route();
    } else if (t.dataset.calFilter) {
      store.set("calFilter", t.dataset.calFilter);
      route();
    } else if (t.dataset.complete) {
      const [cid, idx] = t.dataset.complete.split(":");
      const i = +idx;
      const done = completed(cid);
      const next = done.includes(i) ? done.filter((x) => x !== i) : [...done, i];
      store.set("progress:" + cid, next);
      const openIdx = next.includes(i) ? i + 1 : i;
      route().then(() => {
        const lessons = view.querySelectorAll(".lesson");
        lessons.forEach((d, k) => { d.open = k === openIdx; });
        if (lessons[openIdx]) lessons[openIdx].scrollIntoView({ behavior: "smooth", block: "center" });
      });
    } else if (t.dataset.fav) {
      const favs = store.get("favorites", []);
      const id = t.dataset.fav;
      store.set("favorites", favs.includes(id) ? favs.filter((x) => x !== id) : [...favs, id]);
      const on = !favs.includes(id);
      t.textContent = on ? "★ Saved" : "☆ Save";
      t.classList.toggle("ghost", !on);
    } else if (t.dataset.speak) {
      const p = prayer(t.dataset.speak);
      speechSynthesis.cancel();
      speechSynthesis.speak(new SpeechSynthesisUtterance(p.name + ". " + p.verses.map((v) => v[2]).join(" ")));
    } else if (t.dataset.show) {
      const show = store.get("prayerShow", { dev: true, rom: true, en: true });
      show[t.dataset.show] = !show[t.dataset.show];
      if (!show.dev && !show.rom && !show.en) show.en = true;
      store.set("prayerShow", show);
      const box = document.getElementById("stanzas");
      ["dev", "rom", "en"].forEach((k) => box.classList.toggle("hide-" + k, !show[k]));
      view.querySelectorAll("[data-show]").forEach((c) => c.classList.toggle("active", !!show[c.dataset.show]));
    } else if (t.dataset.pscale) {
      const s = Math.min(1.5, Math.max(0.85, store.get("prayerScale", 1) + 0.1 * t.dataset.pscale));
      store.set("prayerScale", Math.round(s * 100) / 100);
      document.getElementById("stanzas").style.setProperty("--scale", s);
    } else if (t.dataset.font) {
      const scale = Math.min(1.6, Math.max(0.85, store.get("read:font", 1) + 0.1 * t.dataset.font));
      store.set("read:font", Math.round(scale * 100) / 100);
      const anchor = currentItem();
      view.querySelector(".reader").style.setProperty("--read-scale", scale);
      if (anchor) anchor.scrollIntoView();
    } else if ("sanskrit" in t.dataset) {
      saveReaderPos();
      store.set("read:sanskrit", !store.get("read:sanskrit", true));
      route();
    } else if (t.dataset.offline) {
      saveBookOffline(t.dataset.offline, t);
    }
  });

  window.addEventListener("scroll", () => {
    topbar.classList.toggle("scrolled", scrollY > 4);
    if (!readerState) return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveReaderPos, 250);
  }, { passive: true });
  document.addEventListener("visibilitychange", () => { if (document.hidden) saveReaderPos(); });

  backBtn.addEventListener("click", () => {
    if (history.length > 1) history.back();
    else location.hash = "#/home";
  });

  /* ---------- Theme ---------- */
  const root = document.documentElement;
  document.getElementById("themeBtn").addEventListener("click", () => {
    root.dataset.theme = root.dataset.theme === "dark" ? "light" : "dark";
    store.set("theme", root.dataset.theme);
  });

  /* ---------- Boot ---------- */
  window.addEventListener("hashchange", route);
  route();

  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  }
})();
