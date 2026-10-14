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
  /* Audio                                                                   */
  /* A recording listed in audio/index.json is used when one exists.         */
  /* Otherwise the device's own Hindi voice chants the Devanagari text.      */
  /* ====================================================================== */
  const synth = "speechSynthesis" in window ? window.speechSynthesis : null;
  let voices = [];
  let recordings = {};
  let playToken = 0;
  let currentAudio = null;
  let wakeLock = null;
  const utterances = []; // keep references so the browser does not drop them mid-speech

  if (synth) {
    const loadVoices = () => { voices = synth.getVoices() || []; };
    loadVoices();
    if (synth.addEventListener) synth.addEventListener("voiceschanged", loadVoices);
    else synth.onvoiceschanged = loadVoices;
  }
  let mine = {}; // recordings made on this device: id -> { url, type, dur, t }
  const recordingsReady = Promise.all([
    loadJSON("audio/index.json").then((r) => { recordings = r || {}; }).catch(() => {}),
    loadMine()
  ]);

  const canSpeak = () => !!synth;
  // Your own recording comes first, then one published with the app, then the device voice.
  const recordingFor = (id) => (mine[id] && mine[id].url) || recordings[id] || null;
  const hasAudio = (id) => !!recordingFor(id) || canSpeak();

  // Rank the device's voices so the most natural, gentle-sounding one is used by default.
  const NOVELTY = /espeak|fred|albert|zarvox|bad news|bahh|bells|boing|bubbles|cellos|deranged|good news|hysterical|jester|junior|organ|superstar|trinoids|whisper|wobble|ralph|kathy|grandpa|grandma|rocko|shelley|eddy|reed|sandy|flo/i;
  const WARM = /neerja|veena|aria|jenny|sonia|libby|natasha|samantha|karen|moira|tessa|serena|kate|ava|allison|susan|zira|swara|lekha|kalpana|heera|kiyara/i;
  function voiceScore(v) {
    const n = v.name || "";
    let s = 0;
    if (/natural|neural/i.test(n)) s += 6;
    if (/premium|enhanced|wavenet|studio/i.test(n)) s += 5;
    if (WARM.test(n)) s += 3;
    if (/google/i.test(n)) s += 2;
    if (/[-_]IN$/i.test(v.lang)) s += 2; // Indian English pronounces Sanskrit names best
    if (/compact/i.test(n)) s -= 2;
    if (NOVELTY.test(n)) s -= 20;
    return s;
  }
  function voicePool(kind) {
    const re = kind === "en" ? /^en([-_]|$)/i : /^hi([-_]|$)/i;
    let pool = voices.filter((v) => re.test(v.lang));
    if (kind === "hi" && !pool.length) pool = voices.filter((v) => /^(mr|ne|sa)([-_]|$)/i.test(v.lang));
    return pool.sort((a, b) => voiceScore(b) - voiceScore(a));
  }
  function pickVoice(kind) {
    const pool = voicePool(kind);
    const chosen = store.get("voice:" + kind, "");
    return (chosen && pool.find((v) => v.name === chosen)) || pool[0] || null;
  }
  const indicVoice = () => pickVoice("hi");
  const englishVoice = () => pickVoice("en");

  // Speak one piece of text. Resolves when it finishes or is cancelled.
  function say(text, { rate = 0.85, english = false } = {}) {
    return new Promise((resolve) => {
      if (!synth) return resolve();
      const u = new SpeechSynthesisUtterance(text);
      // Without a Hindi voice, chantText() supplies romanised words, which read best in English.
      if (!english && voices.length && !indicVoice()) english = true;
      const v = english ? englishVoice() : indicVoice();
      if (v) { u.voice = v; u.lang = v.lang; } else { u.lang = english ? "en-IN" : "hi-IN"; }
      u.rate = rate;
      u.pitch = english ? 0.95 : 0.9;
      u.onend = u.onerror = () => { utterances.splice(utterances.indexOf(u), 1); resolve(); };
      utterances.push(u);
      synth.speak(u);
    });
  }

  // Text for one verse: Devanagari when a Hindi voice exists, otherwise the plain reading.
  function chantText(v, p) {
    const text = indicVoice() || !voices.length ? v[0] : (p.lang === "Sanskrit" ? readable(v[1]) : v[1]);
    return text.replace(/[।॥\n]+/g, ", ").replace(/(\s*,\s*)+/g, ", ").replace(/^,\s*|,\s*$/g, "");
  }

  function playRecording(src) {
    return new Promise((resolve) => {
      const a = new Audio(src);
      currentAudio = a;
      a.onended = a.onerror = () => { if (currentAudio === a) currentAudio = null; resolve(); };
      a.play().catch(() => resolve());
    });
  }

  // One full chant of a prayer or mantra.
  function chantOnce(p, rate) {
    if (recordingFor(p.id)) return playRecording(recordingFor(p.id));
    return say(p.verses.map((v) => chantText(v, p)).join(", "), { rate });
  }

  function stopAudio() {
    playToken++;
    // Cancelling an idle synthesiser can make Chrome drop the next utterance.
    if (synth && (synth.speaking || synth.pending)) synth.cancel();
    if (currentAudio) { currentAudio.pause(); currentAudio = null; }
    Drone.stop();
    if (wakeLock) { wakeLock.release().catch(() => {}); wakeLock = null; }
    document.querySelectorAll(".stanza.playing").forEach((el) => el.classList.remove("playing"));
    document.querySelectorAll("[data-listen], #chantAlong").forEach((b) => b.classList.remove("on"));
    const l = document.querySelector("[data-listen]");
    if (l) l.innerHTML = PLAY_ICON + "Listen";
    const mb = document.querySelector("[data-meaning]");
    if (mb) { mb.classList.remove("on"); mb.textContent = "Hear the meaning"; }
    const c = document.getElementById("chantAlong");
    if (c) c.innerHTML = PLAY_ICON + "Chant along";
  }

  function keepAwake() {
    if (navigator.wakeLock && !wakeLock) {
      navigator.wakeLock.request("screen").then((l) => {
        wakeLock = l;
        l.addEventListener("release", () => { if (wakeLock === l) wakeLock = null; });
      }).catch(() => {});
    }
  }

  const PLAY_ICON = '<svg class="ico" viewBox="0 0 24 24"><path d="M8 5.5v13l10-6.5z" fill="currentColor" stroke="none"/></svg>';
  const STOP_ICON = '<svg class="ico" viewBox="0 0 24 24"><rect x="7" y="7" width="10" height="10" rx="1.5" fill="currentColor" stroke="none"/></svg>';

  function voiceNote(p) {
    if (mine[p.id]) return "Playing your own recording.";
    if (recordings[p.id]) return "Recorded chant.";
    if (!canSpeak()) return "Audio isn't supported in this browser.";
    if (voices.length && !indicVoice()) return "No Hindi voice was found on this device, so the words are read with an English voice. For a better pronunciation, add Hindi in your phone's text-to-speech settings.";
    return "Chanted by your device's Hindi voice.";
  }

  /* A soft tanpura drone (Pa, Sa, Sa, low Sa), synthesised in the browser. */
  const Drone = {
    ctx: null, master: null, timer: null,
    on: () => store.get("audio:drone", true),
    start() {
      if (this.timer || !this.on()) return;
      const AC = window.AudioContext || window.webkitAudioContext;
      if (!AC) return;
      this.ctx = this.ctx || new AC();
      if (this.ctx.resume) this.ctx.resume();
      const ctx = this.ctx;
      this.master = ctx.createGain();
      this.master.gain.setValueAtTime(0, ctx.currentTime);
      this.master.gain.linearRampToValueAtTime(0.55, ctx.currentTime + 2);
      this.master.connect(ctx.destination);
      const sa = 130.81;
      const pattern = [sa * 1.5, sa * 2, sa * 2, sa];
      let i = 0;
      const pluck = () => {
        const f = pattern[i++ % pattern.length];
        const t = ctx.currentTime;
        [1, 1.003, 2.001].forEach((mult, k) => {
          const o = ctx.createOscillator();
          o.type = k === 2 ? "triangle" : "sawtooth";
          o.frequency.value = f * mult;
          const lp = ctx.createBiquadFilter();
          lp.type = "lowpass";
          lp.Q.value = 4;
          lp.frequency.setValueAtTime(2600, t);
          lp.frequency.exponentialRampToValueAtTime(420, t + 3.5);
          const g = ctx.createGain();
          g.gain.setValueAtTime(0.0001, t);
          g.gain.exponentialRampToValueAtTime(k === 2 ? 0.012 : 0.03, t + 0.04);
          g.gain.exponentialRampToValueAtTime(0.0001, t + 4.8);
          o.connect(lp).connect(g).connect(this.master);
          o.start(t);
          o.stop(t + 5);
        });
      };
      pluck();
      this.timer = setInterval(pluck, 1150);
    },
    stop() {
      if (!this.timer) return;
      clearInterval(this.timer);
      this.timer = null;
      const m = this.master, ctx = this.ctx;
      m.gain.cancelScheduledValues(ctx.currentTime);
      m.gain.setValueAtTime(m.gain.value, ctx.currentTime);
      m.gain.linearRampToValueAtTime(0, ctx.currentTime + 1.2);
      setTimeout(() => m.disconnect(), 1400);
    }
  };

  // Listen to a whole prayer, verse by verse, highlighting the verse being chanted.
  async function listen(p, btn) {
    if (btn.classList.contains("on")) return stopAudio();
    stopAudio();
    const token = playToken;
    btn.classList.add("on");
    btn.innerHTML = STOP_ICON + "Stop";
    keepAwake();
    Drone.start();
    logPractice("prayers", p.id);
    if (recordingFor(p.id)) {
      await playRecording(recordingFor(p.id));
    } else {
      const els = [...document.querySelectorAll("#stanzas .stanza")];
      for (let i = 0; i < p.verses.length; i++) {
        if (token !== playToken) return;
        els.forEach((el, k) => el.classList.toggle("playing", k === i));
        if (els[i] && p.verses.length > 1) els[i].scrollIntoView({ behavior: "smooth", block: "center" });
        await say(chantText(p.verses[i], p), { rate: 0.85 });
      }
    }
    if (token === playToken) stopAudio();
  }

  const pause = (ms) => new Promise((r) => setTimeout(r, ms));
  const sentences = (t) => (t.match(/[^.!?;:]+[.!?;:]*["”’)]*\s*/g) || [t]).map((x) => x.trim()).filter(Boolean);

  // Read the English meaning slowly, sentence by sentence, with gentle pauses.
  async function listenMeaning(p, btn) {
    if (btn.classList.contains("on")) return stopAudio();
    stopAudio();
    const token = playToken;
    btn.classList.add("on");
    btn.innerHTML = STOP_ICON + "Stop";
    keepAwake();
    Drone.start();
    const els = [...document.querySelectorAll("#stanzas .stanza")];
    logPractice("prayers", p.id);
    await say(p.name, { rate: 0.86, english: true });
    for (let i = 0; i < p.verses.length; i++) {
      if (token !== playToken) return;
      els.forEach((el, k) => el.classList.toggle("playing", k === i));
      if (els[i] && p.verses.length > 1) els[i].scrollIntoView({ behavior: "smooth", block: "center" });
      await pause(650);
      for (const line of sentences(p.verses[i][2])) {
        if (token !== playToken) return;
        await say(line, { rate: 0.86, english: true });
        await pause(380);
      }
    }
    if (token === playToken) stopAudio();
  }

  // Voice settings: lets people pick from the voices installed on their own device.
  function voiceControls() {
    if (!canSpeak()) return "";
    return `<div class="card voice-panel" id="voicePanel" hidden>
      <label class="eyebrow" for="voiceEn">Voice for meanings</label>
      <div class="vrow"><select class="chip" id="voiceEn" data-voice-select="en"></select><button class="chip" data-voice-preview="en">Preview</button></div>
      <label class="eyebrow" for="voiceHi">Voice for chanting</label>
      <div class="vrow"><select class="chip" id="voiceHi" data-voice-select="hi"></select><button class="chip" data-voice-preview="hi">Preview</button></div>
      <p class="meta" style="margin:4px 0 0">These voices come from your phone. Ones marked Natural, Enhanced or Premium sound the most lifelike, and you can download more in your phone's text-to-speech settings.</p>
    </div>`;
  }

  function fillVoicePanel() {
    view.querySelectorAll("[data-voice-select]").forEach((sel) => {
      const kind = sel.dataset.voiceSelect;
      const pool = voicePool(kind);
      const chosen = store.get("voice:" + kind, "");
      sel.innerHTML = `<option value="">${pool.length ? `Automatic · ${esc(pool[0].name)}` : "No voices found on this device"}</option>` +
        pool.map((v) => `<option value="${esc(v.name)}" ${v.name === chosen ? "selected" : ""}>${esc(v.name)}</option>`).join("");
    });
  }

  const PREVIEW = { en: "May all beings everywhere be happy, and may all be at peace.", hi: "ॐ नमः शिवाय" };

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
    let calHtml = "", hindu = "", eventsHtml = "", todayEvents = [], tomorrow = "";
    try {
      await loadCalendar();
      const i = calIdx(d0);
      if (inCal(i)) {
        const hd = hinduDate(i);
        hindu = `${hd.line} · Vikram Samvat ${hd.samvat}`;
        todayEvents = (cal.byDay.get(i) || []).map(obsInfo).filter(Boolean)
          .sort((a, b) => (a.kind === "festival" ? 0 : 1) - (b.kind === "festival" ? 0 : 1));
      }
      tomorrow = tomorrowRows();
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

      ${todayEvents.length || tomorrow ? `
        <div class="section" style="margin-top:18px">
          <div class="list">${todayEvents.map((o) => `
            <a class="row" href="#/day/${ymd(d0)}">${seal(o.deva)}
              <span class="body"><span class="eyebrow">Today</span><h3>${esc(o.name)}</h3><p>${esc(o.summary)}</p></span><span class="chev">›</span></a>`).join("")}${tomorrow}
          </div>
        </div>` : ""}

      <div class="hero-wrap" style="margin-top:${todayEvents.length || tomorrow ? 0 : 20}px">
        <a class="night verse-hero fade-in" id="gitaToday" href="#/read/gita/${ref[0]}?v=${ref[1]}">
          ${mandala()}
          <div class="eyebrow">Bhagavad Gita · Verse of the day</div>
          <div class="deva-text">&nbsp;</div>
          <blockquote>Loading today's verse…</blockquote>
          <div class="cite">Chapter ${ref[0]} · Verse ${ref[1]}</div>
        </a>
        <button class="hero-share" data-share-gita aria-label="Share today's verse as an image"><svg class="ico" viewBox="0 0 24 24"><path d="M12 15V3M7.5 7.5L12 3l4.5 4.5"/><path d="M5 12v7a2 2 0 002 2h10a2 2 0 002-2v-7"/></svg></button>
      </div>

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

      <div class="section">${practiceCard()}</div>

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
          <a class="tile" href="#/read"><span class="dv">ग्रन्थ</span><div><h3>Scriptures</h3><p>Gita, Vedas, Upanishads and epics</p></div></a>
          <a class="tile" href="#/learn"><span class="dv">शिक्षा</span><div><h3>Academy</h3><p>${C.courses.length} illustrated courses</p></div></a>
          <a class="tile" href="#/learn#rites"><span class="dv">संस्कार</span><div><h3>Rites of passage</h3><p>Step-by-step guidance</p></div></a>
          <a class="tile" href="#/japa"><span class="dv">जप</span><div><h3>Japa · Chanting</h3><p>Chant a mantra on a mala of 108 beads</p></div></a>
        </div>
      </div>

      <div class="orn"><span></span></div>
      <p class="footer-note">Dharma Path is free, private and always will be.</p>
      <p class="credit">Made with devotion by Amar Latchman</p>`;
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
        <a class="tile" href="#/puja#browse?t=aarti"><span class="dv">आरती</span><div><h3>Aarti mode</h3><p>Big words for the whole family to sing</p></div></a>
        <a class="tile" href="#/recordings"><span class="dv">नाद</span><div><h3>Your recordings</h3><p>Chants in your own voice</p></div></a>
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
          <button class="btn ghost" data-aarti-open="${p.id}">${p.type === "aarti" ? "Aarti mode" : "Full screen"}</button>
        </div>
      </div>
      ${hasAudio(p.id) ? `
      <div class="player">
        <button class="btn" data-listen="${p.id}">${PLAY_ICON}Listen</button>
        ${canSpeak() ? `<button class="btn ghost" data-meaning="${p.id}">Hear the meaning</button>` : ""}
        <button class="chip ${Drone.on() ? "active" : ""}" data-drone>Tanpura</button>
        ${canSpeak() ? `<button class="chip" data-voice-toggle>Voice</button>` : ""}
      </div>
      ${voiceControls()}
      <p class="meta" id="audioNote" style="margin:-4px 4px 14px">${esc(voiceNote(p))}</p>` : ""}
      ${canRecord() ? `<div class="card recorder" id="recorder" data-id="${p.id}">${recorderHtml(p.id)}</div>` : ""}
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
        <div class="btn-row" style="justify-content:center">
          ${hasAudio(m.id) ? `<button class="btn" id="chantAlong">${PLAY_ICON}Chant along</button>
          <button class="chip ${Drone.on() ? "active" : ""}" data-drone>Tanpura</button>` : ""}
          ${canSpeak() ? `<button class="chip" data-voice-toggle>Voice</button>` : ""}
          <button class="btn ghost" id="japaReset">Start again</button>
        </div>
        <div style="text-align:left">${voiceControls()}</div>
        ${hasAudio(m.id) ? `<p class="meta" id="audioNote" style="margin:12px 0 0">Chant along plays the mantra again and again and moves the counter with each repetition. ${esc(voiceNote(m))}</p>` : ""}
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

    // Count one repetition. Returns true when it completes a mala.
    const step = () => {
      const st = japaState(id);
      st.count += 1;
      const full = st.count >= 108;
      logPractice("japa", null, 1);
      if (full) logPractice("malas", null, 1);
      if (full) {
        st.count = 0;
        st.malas += 1;
        if (navigator.vibrate) navigator.vibrate([80, 60, 80]);
      } else if (navigator.vibrate) {
        navigator.vibrate(8);
      }
      store.set(japaKey(id), st);
      paint(st);
      return full;
    };

    store.set("japaMantra", id);
    btn.addEventListener("click", step);
    document.getElementById("japaReset").addEventListener("click", () => {
      stopAudio();
      const st = { count: 0, malas: 0 };
      store.set(japaKey(id), st);
      paint(st);
    });

    const along = document.getElementById("chantAlong");
    if (along) {
      const m = prayer(id);
      along.addEventListener("click", async () => {
        if (along.classList.contains("on")) return stopAudio();
        stopAudio();
        const token = playToken;
        along.classList.add("on");
        along.innerHTML = STOP_ICON + "Stop chanting";
        keepAwake();
        Drone.start();
        while (token === playToken) {
          await chantOnce(m, 0.8);
          if (token !== playToken) break;
          if (step()) break; // stop at the end of a full mala
          await new Promise((r) => setTimeout(r, 450));
        }
        if (token === playToken) stopAudio();
        const note = along.isConnected && document.getElementById("audioNote");
        if (note) note.textContent = `Chant along plays the mantra again and again and moves the counter with each repetition. ${voiceNote(m)}`;
      });
    }
    card.querySelector("[data-scroll]").addEventListener("click", () => {
      document.getElementById("mantras").scrollIntoView({ behavior: "smooth" });
    });
  }

  /* ====================================================================== */
  /* Aarti mode: big words, one verse at a time, for the whole family        */
  /* ====================================================================== */
  let aarti = null; // { p, seq, i, done }

  // Verse order for singing. In an aarti the refrain comes back after every verse.
  function aartiSeq(p) {
    const r = p.verses.findIndex((v) => v[3] === "Refrain");
    const repeat = r >= 0 && store.get("aarti:repeat", true);
    const seq = [];
    p.verses.forEach((v, i) => { seq.push(i); if (repeat && i > r) seq.push(r); });
    return seq;
  }

  function aartiView(id) {
    const p = prayer(id);
    if (!p) return notFound();
    const show = store.get("aartiShow", { dev: true, rom: true, en: true });
    const hasRefrain = p.verses.some((v) => v[3] === "Refrain");
    const opt = (key, label, on) => `<button class="chip ${on ? "active" : ""}" data-aopt="${key}">${label}</button>`;
    return `
      <div class="aarti ${["dev", "rom", "en"].filter((k) => !show[k]).map((k) => "hide-" + k).join(" ")}" id="aarti" data-id="${p.id}">
        <div class="aarti-glow" aria-hidden="true"></div>
        <header class="aarti-top">
          <button class="aarti-icon" data-aarti="close" aria-label="Close">
            <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>
          </button>
          <div class="aarti-title"><div class="eyebrow">${esc(typeOf(p.type).one)} · ${esc(deityOf(p.deity).name)}</div><h2>${esc(p.name)}</h2></div>
          <button class="aarti-icon" data-aarti="opts" aria-label="Display options" aria-expanded="false">
            <svg viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/></svg>
          </button>
        </header>
        <div class="aarti-opts" id="aartiOpts" hidden>
          ${opt("dev", "देवनागरी", show.dev)}${opt("rom", "Roman", show.rom)}${opt("en", "Meaning", show.en)}
          ${hasRefrain ? opt("repeat", "Repeat refrain", store.get("aarti:repeat", true)) : ""}
          ${hasAudio(p.id) ? opt("drone", "Tanpura", Drone.on()) : ""}
          <button class="chip" data-aopt="smaller" aria-label="Smaller text">A−</button>
          <button class="chip" data-aopt="larger" aria-label="Larger text">A+</button>
        </div>
        <div class="diya" aria-hidden="true"><span class="halo"></span><span class="flame"></span><span class="wick"></span><span class="bowl"></span></div>
        <div class="aarti-stage" id="aartiStage" aria-live="polite"></div>
        <div class="aarti-foot">
          <div class="aarti-progress" aria-hidden="true"><span id="aartiBar"></span></div>
          <div class="aarti-controls">
            <button class="aarti-icon lg" data-aarti="prev" aria-label="Previous verse"><svg viewBox="0 0 24 24"><path d="M15 18l-6-6 6-6"/></svg></button>
            ${hasAudio(p.id) ? `<button class="btn aarti-play" data-aarti="play">${PLAY_ICON}Chant</button>` : `<span class="aarti-hint">Tap or swipe to move on</span>`}
            <button class="aarti-icon lg" data-aarti="next" aria-label="Next verse"><svg viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg></button>
          </div>
        </div>
      </div>`;
  }

  // Shrink the text until the whole verse fits on the screen.
  function fitAarti() {
    const stage = document.getElementById("aartiStage");
    const inner = stage && stage.firstElementChild;
    if (!inner) return;
    const scale = store.get("aarti:scale", 1);
    let fs = Math.max(20, Math.min(64, Math.min(innerWidth / 12.5, innerHeight / 15) * scale));
    stage.style.setProperty("--fs", fs + "px");
    while (inner.scrollHeight > stage.clientHeight && fs > 13) {
      fs -= 1.5;
      stage.style.setProperty("--fs", fs + "px");
    }
  }

  function paintAarti() {
    const box = document.getElementById("aarti");
    if (!box || !aarti) return;
    const { p, seq, i } = aarti;
    const stage = document.getElementById("aartiStage");
    const bar = document.getElementById("aartiBar");
    bar.style.width = (aarti.done ? 100 : (i / seq.length) * 100) + "%";
    if (aarti.done) {
      stage.innerHTML = `<div class="aarti-verse aarti-end">
        <p class="dev">ॐ शान्तिः शान्तिः शान्तिः</p>
        <p class="rom">Om Shanti, Shanti, Shanti</p>
        <p class="en">Peace within, peace around, peace everywhere.</p>
        <div class="btn-row"><button class="btn" data-aarti="again">Begin again</button><button class="btn ghost" data-aarti="close">Close</button></div>
      </div>`;
    } else {
      const k = seq[i];
      const v = p.verses[k];
      // Labelled lines (refrain, doha) show their label; the rest are numbered among themselves.
      const verseNo = p.verses.filter((x, n) => n <= k && !x[3]).length;
      const total = p.verses.filter((x) => !x[3]).length;
      const label = v[3] || (total > 1 ? `Verse ${verseNo} of ${total}` : "");
      stage.innerHTML = `<div class="aarti-verse ${v[3] === "Refrain" ? "refrain" : ""}">
        ${label ? `<div class="eyebrow">${esc(label)}</div>` : ""}
        <p class="dev">${esc(v[0])}</p>
        <p class="rom">${esc(v[1])}</p>
        <p class="en">${esc(v[2])}</p>
      </div>`;
    }
    fitAarti();
  }

  function aartiGo(delta) {
    if (!aarti) return;
    if (aarti.done) { if (delta < 0) { aarti.done = false; aarti.i = aarti.seq.length - 1; paintAarti(); } return; }
    const n = aarti.i + delta;
    if (n < 0) return;
    if (n >= aarti.seq.length) {
      aarti.done = true;
      if (!aarti.logged) { aarti.logged = true; logPractice("aarti", aarti.p.id); }
    } else aarti.i = n;
    paintAarti();
  }

  async function aartiPlay(btn) {
    if (btn.classList.contains("on")) { stopAudio(); keepAwake(); return; }
    stopAudio();
    keepAwake();
    const token = playToken;
    btn.classList.add("on");
    btn.innerHTML = STOP_ICON + "Stop";
    Drone.start();
    const { p } = aarti;
    if (aarti.done) { aarti.done = false; aarti.i = 0; paintAarti(); }
    const rec = recordingFor(p.id);
    if (rec) {
      // A recording covers the whole prayer, so the verses stay under the family's control.
      await playRecording(rec);
    } else {
      while (token === playToken && aarti && !aarti.done) {
        await say(chantText(p.verses[aarti.seq[aarti.i]], p), { rate: 0.85 });
        if (token !== playToken) return;
        await pause(500);
        if (token !== playToken) return;
        aartiGo(1);
      }
    }
    if (token === playToken) { stopAudio(); keepAwake(); }
    if (btn.isConnected) { btn.classList.remove("on"); btn.innerHTML = PLAY_ICON + "Chant"; }
  }

  function closeAarti() {
    const id = aarti && aarti.p.id;
    if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(() => {});
    if (navCount > 1) history.back();
    else location.replace("#/puja/" + id);
  }

  function bindAarti() {
    const box = document.getElementById("aarti");
    if (!box) { aarti = null; return; }
    const p = prayer(box.dataset.id);
    aarti = { p, seq: aartiSeq(p), i: 0, done: false };
    keepAwake();
    paintAarti();
    let x0 = null, y0 = 0, swiped = false;
    const stage = document.getElementById("aartiStage");
    stage.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; swiped = false; }, { passive: true });
    stage.addEventListener("touchend", (e) => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) { swiped = true; aartiGo(dx < 0 ? 1 : -1); }
      x0 = null;
    });
    stage.addEventListener("click", (e) => {
      if (swiped) { swiped = false; return; }
      if (e.target.closest("button") || aarti.done) return;
      aartiGo(e.clientX < innerWidth * 0.3 ? -1 : 1);
    });
  }

  document.addEventListener("keydown", (e) => {
    if (!aarti || !document.getElementById("aarti") || e.altKey || e.ctrlKey || e.metaKey) return;
    if (["ArrowRight", "ArrowDown", "PageDown", " ", "Enter"].includes(e.key)) { e.preventDefault(); aartiGo(1); }
    else if (["ArrowLeft", "ArrowUp", "PageUp"].includes(e.key)) { e.preventDefault(); aartiGo(-1); }
    else if (e.key === "Escape" && !document.fullscreenElement && !document.querySelector(".sheet-backdrop")) closeAarti();
  });
  window.addEventListener("resize", () => { if (aarti) fitAarti(); });

  /* ====================================================================== */
  /* Practice tracker                                                        */
  /* Each day keeps what was done: mantras and malas chanted, sections read, */
  /* prayers heard, aartis sung, lessons finished and personal check-ins.    */
  /* ====================================================================== */
  const COUNTS = ["japa", "malas"];
  const CHECKINS = [["pray", "Prayed"], ["meditate", "Meditated"], ["fast", "Fasted"], ["temple", "Visited a temple"], ["seva", "Did seva"]];
  const practiceLog = () => store.get("practice", {});

  // Record one practice for today. List kinds count each key once a day.
  function logPractice(kind, key, n = 1) {
    const log = practiceLog();
    const d = ymd(new Date());
    const day = log[d] || (log[d] = {});
    if (COUNTS.includes(kind)) day[kind] = (day[kind] || 0) + n;
    else {
      const list = day[kind] || (day[kind] = []);
      if (list.includes(key)) return false;
      list.push(key);
    }
    const keys = Object.keys(log).sort();
    keys.slice(0, Math.max(0, keys.length - 800)).forEach((k) => delete log[k]);
    store.set("practice", log);
    return true;
  }

  function unlogPractice(kind, key) {
    const log = practiceLog();
    const day = log[ymd(new Date())];
    if (!day || !day[kind]) return;
    day[kind] = day[kind].filter((x) => x !== key);
    store.set("practice", log);
  }

  const len = (a) => (a ? a.length : 0);
  const dayPoints = (d) => !d ? 0 : (d.japa || 0) / 27 + len(d.read) * 2 + len(d.prayers) + len(d.aarti) * 2 + len(d.lessons) * 2 + len(d.done) * 2;
  const dayLevel = (d) => { const x = dayPoints(d); return x <= 0 ? 0 : x < 2 ? 1 : x < 4 ? 2 : x < 8 ? 3 : 4; };
  const addDays = (d, n) => new Date(d.getFullYear(), d.getMonth(), d.getDate() + n);
  const plural = (n, one, many) => `${n.toLocaleString()} ${n === 1 ? one : many || one + "s"}`;

  function dayParts(d) {
    if (!d) return [];
    const out = [];
    if (d.malas) out.push(plural(d.malas, "mala"));
    if (d.japa) out.push(plural(d.japa, "mantra") + " chanted");
    if (len(d.read)) out.push(plural(len(d.read), "reading"));
    if (len(d.aarti)) out.push(plural(len(d.aarti), "aarti"));
    if (len(d.prayers)) out.push(plural(len(d.prayers), "prayer") + " heard");
    if (len(d.lessons)) out.push(plural(len(d.lessons), "lesson"));
    (d.done || []).forEach((k) => { const c = CHECKINS.find((x) => x[0] === k); if (c) out.push(c[1].toLowerCase()); });
    return out;
  }

  function practiceStats() {
    const log = practiceLog();
    const t = today();
    const active = (date) => dayPoints(log[ymd(date)]) > 0;
    let streak = 0;
    let d = active(t) ? t : addDays(t, -1);
    while (active(d)) { streak++; d = addDays(d, -1); }
    const days = Object.keys(log).filter((k) => dayPoints(log[k]) > 0).sort();
    let best = 0, run = 0, prev = null;
    days.forEach((k) => {
      const cur = parseYmd(k);
      run = prev && Math.round((cur - prev) / 86400000) === 1 ? run + 1 : 1;
      best = Math.max(best, run);
      prev = cur;
    });
    const weekAgo = ymd(addDays(t, -6));
    const total = (f, since) => Object.keys(log).filter((k) => !since || k >= since).reduce((a, k) => a + f(log[k]), 0);
    const kinds = {
      malas: (x) => x.malas || 0, japa: (x) => x.japa || 0, read: (x) => len(x.read),
      aarti: (x) => len(x.aarti) + len(x.prayers), lessons: (x) => len(x.lessons)
    };
    const all = {}, week = {};
    Object.entries(kinds).forEach(([k, f]) => { all[k] = total(f); week[k] = total(f, weekAgo); });
    return { log, t, streak, best, days: days.length, todayDone: active(t), all, week };
  }

  // The last seven days as dots, today last.
  function weekDots(st) {
    return `<div class="week-dots">${[6, 5, 4, 3, 2, 1, 0].map((n) => {
      const d = addDays(st.t, -n);
      const on = dayPoints(st.log[ymd(d)]) > 0;
      return `<span class="wd ${on ? "on" : ""} ${n === 0 ? "today" : ""}" title="${esc(longDate(d))}${on ? ": practised" : ""}"><i></i><b>${WEEKDAYS[d.getDay()][0]}</b></span>`;
    }).join("")}</div>`;
  }

  function streakLine(st) {
    if (st.todayDone) return st.streak > 1 ? "Today's practice is done. Well kept." : "Today's practice is done.";
    if (st.streak) return "Chant, read or pray today to keep it going.";
    return "Chant a mala, read a chapter or sing an aarti to begin.";
  }

  function practiceCard() {
    const st = practiceStats();
    return `<a class="card practice-card" href="#/practice">
      <div class="pc-num"><strong>${st.streak}</strong><span>day${st.streak === 1 ? "" : "s"}</span></div>
      <div class="pc-body"><div class="eyebrow">Your practice</div>${weekDots(st)}<p class="meta">${esc(streakLine(st))}</p></div>
      <span class="chev">›</span></a>`;
  }

  function heatmap(st) {
    const WEEKS = 12;
    const start = addDays(st.t, -st.t.getDay() - (WEEKS - 1) * 7);
    // The column holding the 1st of a month carries its name; the first column is named too unless a 1st is close by.
    const firstIn = (w) => [...Array(7)].map((_, k) => addDays(start, w * 7 + k)).find((d) => d.getDate() === 1 && d <= st.t);
    let cols = "", months = "";
    for (let w = 0; w < WEEKS; w++) {
      const top = addDays(start, w * 7);
      const f = firstIn(w);
      const label = f ? MON[f.getMonth()] : w === 0 && !firstIn(1) && !firstIn(2) ? MON[top.getMonth()] : "";
      months += `<span>${label}</span>`;
      cols += `<div class="hm-col">`;
      for (let k = 0; k < 7; k++) {
        const d = addDays(top, k);
        if (d > st.t) { cols += `<span class="hm-cell future"></span>`; continue; }
        const key = ymd(d);
        const parts = dayParts(st.log[key]);
        const desc = `${longDate(d)}: ${parts.length ? parts.join(", ") : "no practice logged"}`;
        cols += `<button class="hm-cell l${dayLevel(st.log[key])} ${d - st.t === 0 ? "today" : ""}" data-hm="${esc(desc)}" aria-label="${esc(desc)}"></button>`;
      }
      cols += `</div>`;
    }
    return `<div class="card heatmap">
      <div class="hm-months">${months}</div>
      <div class="hm-body"><div class="hm-days"><span></span><span>Mon</span><span></span><span>Wed</span><span></span><span>Fri</span><span></span></div><div class="hm-grid">${cols}</div></div>
      <div class="hm-foot"><p class="hm-readout" id="hmReadout">Tap a day to see what you did.</p>
        <div class="hm-key" aria-hidden="true">Less<span class="hm-cell l0"></span><span class="hm-cell l1"></span><span class="hm-cell l2"></span><span class="hm-cell l3"></span><span class="hm-cell l4"></span>More</div></div>
    </div>`;
  }

  function practiceView() {
    const st = practiceStats();
    const doneToday = (st.log[ymd(st.t)] || {}).done || [];
    const tile = (value, label, week, sub) => `<div class="stat"><div class="stat-v">${value.toLocaleString()}</div><div class="stat-l">${label}</div><div class="stat-s">${week ? "+" + week.toLocaleString() + " this week" : sub || "&nbsp;"}</div></div>`;
    const recent = Object.keys(st.log).filter((k) => dayPoints(st.log[k]) > 0).sort().reverse().slice(0, 7);
    return `
      <h2 class="page-title">Your practice</h2>
      <p class="page-sub">A quiet record of your sadhana. It stays private, on this device.</p>
      <div class="night practice-hero">
        ${mandala()}
        <div class="eyebrow">Current streak</div>
        <div class="streak-num">${st.streak}<span>day${st.streak === 1 ? "" : "s"}</span></div>
        <p class="meta">${esc(streakLine(st))}${st.best > 1 ? ` Best streak: ${st.best} days.` : ""}</p>
        ${weekDots(st)}
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Today I…</h2></div>
        <div class="chips wrap">${CHECKINS.map(([k, label]) => `<button class="chip ${doneToday.includes(k) ? "active" : ""}" data-checkin="${k}">${doneToday.includes(k) ? "✓ " : ""}${label}</button>`).join("")}</div>
        <p class="meta" style="margin:10px 2px 0">Chanting, reading and aartis in the app are counted for you.</p>
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">All time</h2></div>
        <div class="stats">
          ${tile(st.all.malas, st.all.malas === 1 ? "Mala" : "Malas", st.week.malas, plural(st.all.japa, "mantra") + " chanted")}
          ${tile(st.all.read, st.all.read === 1 ? "Reading" : "Readings", st.week.read, "Chapters and sections")}
          ${tile(st.all.aarti, "Aartis and prayers", st.week.aarti, "")}
          ${tile(st.days, st.days === 1 ? "Day of practice" : "Days of practice", 0, st.all.lessons ? plural(st.all.lessons, "lesson") + " finished" : "")}
        </div>
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Last 12 weeks</h2></div>
        ${heatmap(st)}
      </div>

      ${recent.length ? `<div class="section">
        <div class="section-head"><h2 class="section-title">Recent days</h2></div>
        <div class="list">${recent.map((k) => `<div class="row static"><span class="body"><h3>${esc(longDate(parseYmd(k)))}</h3><p>${esc(dayParts(st.log[k]).join(" · "))}</p></span></div>`).join("")}</div>
      </div>` : ""}

      <div class="section">
        <div class="list">
          <a class="row" href="#/reminders">${seal("स्मर")}<span class="body"><h3>Reminders</h3><p>Festival alerts and a daily prayer nudge</p></span><span class="chev">›</span></a>
          <a class="row" href="#/saved">${seal("ग्रन्थ")}<span class="body"><h3>Bookmarks and notes</h3><p>Verses you have saved while reading</p></span><span class="chev">›</span></a>
          <a class="row" href="#/recordings">${seal("नाद")}<span class="body"><h3>Your recordings</h3><p>Chants recorded in your own voice</p></span><span class="chev">›</span></a>
        </div>
      </div>`;
  }

  function bindPractice() {
    const out = document.getElementById("hmReadout");
    if (!out) return;
    const show = (e) => { const c = e.target.closest("[data-hm]"); if (c) out.textContent = c.dataset.hm; };
    const grid = view.querySelector(".hm-grid");
    grid.addEventListener("pointerover", show);
    grid.addEventListener("focusin", show);
    grid.addEventListener("click", show);
  }

  // A section counts as read once its end has been on screen and it has been open for twenty seconds.
  function markIfRead() {
    const st = readerState;
    if (!st || st.counted || Date.now() - st.opened < 20000) return;
    const r = view.querySelector(".reader");
    if (!r || r.getBoundingClientRect().bottom > innerHeight + 60) return;
    st.counted = true;
    logPractice("read", `${st.bookId}|${st.part}|${st.sec}`);
  }

  /* ====================================================================== */
  /* Reminders                                                               */
  /* A calendar file gives exact alerts from the phone's own calendar app.  */
  /* Where the browser allows it, the app can also show notices itself.     */
  /* ====================================================================== */
  const REMIND_TYPES = CAL_FILTERS.filter((f) => f.id !== "all");
  const REMIND_NAMES = { festivals: "Festivals", ekadashi: "Ekadashi", moon: "Purnima and Amavasya", vrats: "Sankashti, Pradosh and Shivaratri" };
  const remindPrefs = () => ({
    types: ["festivals", "ekadashi"], eve: true, eveTime: "19:00", morn: false, mornTime: "06:00",
    daily: false, dailyTime: "06:30", notify: false, ...store.get("reminders", {})
  });
  const toMin = (t) => { const [h, m] = String(t).split(":").map(Number); return (h || 0) * 60 + (m || 0); };
  const fmtHM = (t) => fmtTime(toMin(t));

  // Selected observances between two calendar indexes, one entry per event.
  function remindEvents(from, to, prefs) {
    const tests = REMIND_TYPES.filter((f) => prefs.types.includes(f.id));
    return cal.events.filter((e) => e[0] >= from && e[0] < to && tests.some((f) => f.test(e)))
      .map((e) => ({ e, o: obsInfo(e) })).filter((x) => x.o);
  }

  // What tomorrow holds, for the Today page. Ekadashi gets the sunrise time, when the fast begins.
  function tomorrowRows() {
    if (!cal) return "";
    const i = calIdx(today()) + 1;
    if (!inCal(i)) return "";
    const prefs = remindPrefs();
    const list = remindEvents(i, i + 1, prefs.types.length ? prefs : { types: ["festivals", "ekadashi"] });
    const hd = hinduDate(i);
    return list.map(({ o }) => `
      <a class="row tomorrow" href="#/day/${ymd(calDate(i))}">${seal(o.deva)}
        <span class="body"><span class="eyebrow">Tomorrow</span><h3>${esc(o.name)}</h3><p>${o.id === "ekadashi" ? `The fast begins at sunrise, ${esc(hd.sunrise)}. ` : ""}${esc(o.summary)}</p></span><span class="chev">›</span></a>`).join("");
  }

  const icsText = (t) => String(t).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n");
  // Lines longer than 75 bytes are folded, as the calendar format requires.
  function icsFold(line) {
    const out = [];
    let cur = "", bytes = 0;
    for (const ch of line) {
      const b = new TextEncoder().encode(ch).length;
      if (bytes + b > (out.length ? 74 : 75)) { out.push(cur); cur = ""; bytes = 0; }
      cur += ch; bytes += b;
    }
    out.push(cur);
    return out.join("\r\n ");
  }
  const icsDate = (d) => `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}`;
  const icsOffset = (mins) => `${mins < 0 ? "-" : ""}PT${Math.floor(Math.abs(mins) / 60)}H${Math.abs(mins) % 60}M`;

  async function downloadIcs() {
    await loadCalendar();
    const prefs = remindPrefs();
    const t0 = calIdx(today());
    const appUrl = location.href.split("#")[0];
    const stamp = new Date().toISOString().replace(/[-:]/g, "").replace(/\.\d+/, "");
    const L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Dharma Path//Reminders//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
      "X-WR-CALNAME:Dharma Path", `X-WR-CALDESC:${icsText("Hindu festivals and fasting days for " + cityName())}`];
    const alarm = (trigger, text) => ["BEGIN:VALARM", "ACTION:DISPLAY", `DESCRIPTION:${icsText(text)}`, `TRIGGER:${trigger}`, "END:VALARM"];
    const events = remindEvents(t0, Math.min(cal.days.length, t0 + 366), prefs);
    events.forEach(({ e, o }) => {
      const d = calDate(e[0]);
      const hd = hinduDate(e[0]);
      const desc = `${o.summary}${o.id === "ekadashi" ? ` The fast begins at sunrise (${hd.sunrise}).` : ""}\n${hd.line}. Sunrise ${hd.sunrise}, sunset ${hd.sunset} in ${cityName()}.\n\n${appUrl}#/day/${ymd(d)}`;
      L.push("BEGIN:VEVENT", `UID:${ymd(d)}-${e[1]}@dharma-path`, `DTSTAMP:${stamp}`, `DTSTART;VALUE=DATE:${icsDate(d)}`, `DTEND;VALUE=DATE:${icsDate(addDays(d, 1))}`,
        `SUMMARY:${icsText(o.name)}`, `DESCRIPTION:${icsText(desc)}`, "TRANSP:TRANSPARENT", "CATEGORIES:Dharma Path");
      if (prefs.eve) L.push(...alarm(icsOffset(toMin(prefs.eveTime) - 1440), `Tomorrow: ${o.name}`));
      if (prefs.morn) L.push(...alarm(icsOffset(toMin(prefs.mornTime)), `Today: ${o.name}`));
      L.push("END:VEVENT");
    });
    if (prefs.daily) {
      const d = addDays(today(), 1);
      const [h, m] = prefs.dailyTime.split(":");
      L.push("BEGIN:VEVENT", "UID:daily-prayer@dharma-path", `DTSTAMP:${stamp}`, `DTSTART:${icsDate(d)}T${pad(+h)}${pad(+m)}00`, "DURATION:PT15M",
        "RRULE:FREQ=DAILY", "SUMMARY:Daily prayer", `DESCRIPTION:${icsText("A few quiet minutes for prayer, japa or reading.\n\n" + appUrl + "#/puja")}`,
        "TRANSP:TRANSPARENT", ...alarm("PT0M", "Time for your daily prayer"), "END:VEVENT");
    }
    L.push("END:VCALENDAR");
    const blob = new Blob([L.map(icsFold).join("\r\n") + "\r\n"], { type: "text/calendar;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "dharma-path-reminders.ics";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    toast(`${events.length} dates${prefs.daily ? " and a daily prayer" : ""} ready to add`);
    return events.length;
  }

  /* Notices shown by the app itself. The service worker reads this list on a periodic background sync. */
  const canNotify = () => "Notification" in window && "serviceWorker" in navigator;
  const REMIND_URL = () => new URL("reminders.json", location.href).href;

  async function syncReminderData() {
    if (!canNotify() || !("caches" in window)) return;
    const prefs = remindPrefs();
    const c = await caches.open("dp-data");
    const old = await c.match(REMIND_URL()).then((r) => r && r.json()).catch(() => null);
    if (!prefs.notify) { await c.delete(REMIND_URL()); return; }
    await loadCalendar();
    const t0 = calIdx(today());
    const events = remindEvents(t0, t0 + 45, prefs).map(({ e, o }) => ({
      date: ymd(calDate(e[0])), id: e[1], title: o.name, body: o.summary, url: `#/day/${ymd(calDate(e[0]))}`
    }));
    const data = {
      notify: true, eve: prefs.eve, morn: prefs.morn, daily: prefs.daily, dailyMin: toMin(prefs.dailyTime),
      events, shown: (old && old.shown) || []
    };
    await c.put(REMIND_URL(), new Response(JSON.stringify(data), { headers: { "Content-Type": "application/json" } }));
  }

  async function enableNotices() {
    if (!canNotify()) return "unsupported";
    const perm = await Notification.requestPermission();
    if (perm !== "granted") return perm;
    const reg = await navigator.serviceWorker.ready;
    let periodic = false;
    if ("periodicSync" in reg) {
      try {
        const st = await navigator.permissions.query({ name: "periodic-background-sync" });
        if (st.state === "granted") { await reg.periodicSync.register("dp-reminders", { minInterval: 6 * 3600 * 1000 }); periodic = true; }
      } catch (e) { /* not available for this install */ }
    }
    store.set("reminders", { ...remindPrefs(), notify: true });
    store.set("reminders:periodic", periodic);
    await syncReminderData();
    reg.showNotification("Reminders are on", { body: "Dharma Path will let you know about the days you chose.", icon: "icons/icon-192.png", badge: "icons/badge.png", tag: "dp-welcome" });
    return "granted";
  }

  async function disableNotices() {
    store.set("reminders", { ...remindPrefs(), notify: false });
    try { const reg = await navigator.serviceWorker.ready; if (reg.periodicSync) await reg.periodicSync.unregister("dp-reminders"); } catch (e) { /* ignore */ }
    await syncReminderData();
  }

  function noticeStatus(prefs) {
    if (!canNotify()) return "This browser can't show notices. The calendar file above works everywhere.";
    if (Notification.permission === "denied") return "Notices are blocked for this site. You can allow them in your browser's site settings.";
    if (!prefs.notify || Notification.permission !== "granted") return "Get a notice from Dharma Path the evening before, without adding anything to your calendar. Works best when the app is installed on your home screen.";
    return store.get("reminders:periodic", false)
      ? "Notices are on. Your phone checks in a few times a day, so a notice may arrive a little early or late. For exact times, use the calendar file."
      : "Notices are on while Dharma Path is open. To get them when the app is closed, install it on your home screen, or use the calendar file.";
  }

  async function remindersView() {
    const prefs = remindPrefs();
    let next = "";
    try {
      await loadCalendar();
      const t0 = calIdx(today());
      const soon = remindEvents(t0 + 1, t0 + 120, prefs).slice(0, 4);
      next = soon.length
        ? `<div class="list">${soon.map(({ e, o }) => eventRow(e)).join("")}</div>`
        : `<div class="card empty">Choose at least one kind of day below.</div>`;
    } catch (e) { next = `<div class="card empty">The calendar needs an internet connection the first time it opens.</div>`; }
    const chip = (attr, on, label) => `<button class="chip ${on ? "active" : ""}" ${attr}>${on ? "✓ " : ""}${label}</button>`;
    return `
      <h2 class="page-title">Reminders</h2>
      <p class="page-sub">Never miss a fast or a festival. Choose what matters to you, then add the reminders to your phone.</p>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Remind me about</h2></div>
        <div class="chips wrap">${REMIND_TYPES.map((f) => chip(`data-rtype="${f.id}"`, prefs.types.includes(f.id), REMIND_NAMES[f.id])).join("")}</div>
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">When</h2></div>
        <div class="card remind-times">
          <label class="rt"><input type="checkbox" data-rpref="eve" ${prefs.eve ? "checked" : ""}><span>The evening before</span><input type="time" class="time-input" data-rtime="eveTime" value="${prefs.eveTime}"></label>
          <label class="rt"><input type="checkbox" data-rpref="morn" ${prefs.morn ? "checked" : ""}><span>On the morning itself</span><input type="time" class="time-input" data-rtime="mornTime" value="${prefs.mornTime}"></label>
          <label class="rt"><input type="checkbox" data-rpref="daily" ${prefs.daily ? "checked" : ""}><span>A daily prayer reminder</span><input type="time" class="time-input" data-rtime="dailyTime" value="${prefs.dailyTime}"></label>
        </div>
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Coming up</h2><a href="#/calendar">Calendar</a></div>
        ${next}
      </div>

      <div class="section">
        <div class="section-head"><h2 class="section-title">Get the reminders</h2></div>
        <div class="card">
          <div class="eyebrow">Recommended</div>
          <h3 class="card-h">Add to your calendar</h3>
          <p class="meta" style="margin:0">Your calendar app will alert you at the times above, even when Dharma Path is closed. It covers the next twelve months for ${esc(cityName() || "your city")}.</p>
          <div class="btn-row"><button class="btn" data-ics>Download calendar file</button></div>
          <p class="meta small-note">On iPhone, tap <b>Add all</b>. On Android, open the file with your calendar app, or import it at calendar.google.com under Settings, then Import. Download a new file whenever you change these choices.</p>
        </div>
        <div class="card">
          <h3 class="card-h">Notices from Dharma Path</h3>
          <p class="meta" style="margin:0" id="noticeStatus">${esc(noticeStatus(prefs))}</p>
          ${canNotify() && Notification.permission !== "denied" ? `<div class="btn-row"><button class="btn ghost" data-notices="${prefs.notify && Notification.permission === "granted" ? "off" : "on"}">${prefs.notify && Notification.permission === "granted" ? "Turn off notices" : "Turn on notices"}</button></div>` : ""}
        </div>
      </div>`;
  }

  // While the app is open, show tonight's or this morning's notice if the background check hasn't.
  async function checkNoticesNow() {
    const prefs = remindPrefs();
    if (!prefs.notify || !canNotify() || Notification.permission !== "granted") return;
    try {
      await syncReminderData();
      const reg = await navigator.serviceWorker.ready;
      if (reg.active) reg.active.postMessage({ type: "dp-remind" });
    } catch (e) { /* ignore */ }
  }

  /* ====================================================================== */
  /* Record your own chant                                                   */
  /* Recordings stay on this device in IndexedDB and can be shared as files. */
  /* ====================================================================== */
  function idb() {
    if (!idb.p) {
      idb.p = new Promise((resolve, reject) => {
        const r = indexedDB.open("dharma-path", 1);
        r.onupgradeneeded = () => r.result.createObjectStore("recordings", { keyPath: "id" });
        r.onsuccess = () => resolve(r.result);
        r.onerror = () => reject(r.error);
      });
    }
    return idb.p;
  }

  async function idbRun(mode, fn) {
    const db = await idb();
    return new Promise((resolve, reject) => {
      const tx = db.transaction("recordings", mode);
      const req = fn(tx.objectStore("recordings"));
      tx.oncomplete = () => resolve(req && req.result);
      tx.onerror = tx.onabort = () => reject(tx.error);
    });
  }

  async function loadMine() {
    try {
      const all = await idbRun("readonly", (st) => st.getAll());
      (all || []).forEach((r) => { mine[r.id] = { url: URL.createObjectURL(r.blob), type: r.blob.type, size: r.blob.size, dur: r.dur, t: r.t }; });
    } catch (e) { /* storage unavailable, for example in a private window */ }
  }

  async function saveMine(id, blob, dur) {
    const t = Date.now();
    await idbRun("readwrite", (st) => st.put({ id, blob, dur, t }));
    if (mine[id]) URL.revokeObjectURL(mine[id].url);
    mine[id] = { url: URL.createObjectURL(blob), type: blob.type, size: blob.size, dur, t };
    if (navigator.storage && navigator.storage.persist) navigator.storage.persist().catch(() => {});
  }

  async function deleteMine(id) {
    await idbRun("readwrite", (st) => st.delete(id));
    if (mine[id]) URL.revokeObjectURL(mine[id].url);
    delete mine[id];
  }

  const canRecord = () => !!(window.MediaRecorder && navigator.mediaDevices && navigator.mediaDevices.getUserMedia && window.indexedDB);
  const fmtDur = (sec) => `${Math.floor(sec / 60)}:${pad(Math.floor(sec % 60))}`;
  const extFor = (type) => /mp4|aac|m4a/.test(type) ? ".m4a" : /ogg/.test(type) ? ".ogg" : /mpeg|mp3/.test(type) ? ".mp3" : ".webm";
  const MAX_REC = 20 * 60;
  let rec = null; // the recording in progress

  function recorderHtml(id) {
    const p = prayer(id);
    if (rec && rec.id === id) {
      return `<div class="rec-live"><span class="rec-dot" aria-hidden="true"></span><div><div class="eyebrow">Recording</div><strong id="recTime">${fmtDur((Date.now() - rec.t0) / 1000)}</strong></div></div>
        <p class="meta" style="margin:10px 0 0">${p.japa ? "Chant one repetition, then stop. Chant along on the mala repeats it for you." : "Chant at your own pace. Stop when you have finished."}</p>
        <div class="btn-row"><button class="btn" data-rec="stop">${STOP_ICON}Stop and save</button><button class="btn ghost" data-rec="cancel">Cancel</button></div>`;
    }
    const m = mine[id];
    if (m) {
      return `<div class="eyebrow">Your recording</div>
        <audio controls preload="metadata" src="${m.url}"></audio>
        <p class="meta" style="margin:8px 0 0">${fmtDur(m.dur)} · recorded ${esc(new Date(m.t).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" }))}. It plays whenever you tap Listen, even offline.</p>
        <div class="btn-row"><button class="btn ghost" data-rec="share">Share or send</button><button class="btn ghost" data-rec="start">Record again</button><button class="btn ghost danger" data-rec="delete">Delete</button></div>`;
    }
    return `<div class="eyebrow">Your own voice</div>
      <h3 class="card-h">Record this ${esc(typeOf(p.type).one.toLowerCase())}</h3>
      <p class="meta" style="margin:0">Record it yourself, or ask a parent, grandparent or priest. The recording plays here instead of the device voice.${p.japa ? " For the mala, record a single repetition." : ""}</p>
      <div class="btn-row"><button class="btn ghost" data-rec="start"><span class="rec-dot sm" aria-hidden="true"></span>Record</button></div>`;
  }

  function paintRecorder() {
    const box = document.getElementById("recorder");
    if (box) box.innerHTML = recorderHtml(box.dataset.id);
    const note = document.getElementById("audioNote");
    if (note && box) note.textContent = voiceNote(prayer(box.dataset.id));
  }

  async function startRecording(id) {
    if (rec) return;
    stopAudio();
    let stream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: true } });
    } catch (e) {
      toast(e && e.name === "NotAllowedError" ? "Microphone access wasn't allowed" : "No microphone was found");
      return;
    }
    const type = ["audio/webm;codecs=opus", "audio/mp4", "audio/webm", "audio/ogg;codecs=opus"].find((t) => MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(t));
    let mr;
    try { mr = new MediaRecorder(stream, type ? { mimeType: type, audioBitsPerSecond: 96000 } : undefined); }
    catch (e) { mr = new MediaRecorder(stream); }
    rec = { id, mr, stream, chunks: [], t0: Date.now(), keep: true };
    mr.ondataavailable = (e) => { if (e.data && e.data.size) rec && rec.chunks.push(e.data); };
    mr.onstop = () => finishRecording();
    mr.start(1000);
    keepAwake();
    rec.timer = setInterval(() => {
      const el = document.getElementById("recTime");
      const sec = (Date.now() - rec.t0) / 1000;
      if (el) el.textContent = fmtDur(sec);
      if (sec >= MAX_REC) stopRecording(true);
    }, 500);
    paintRecorder();
  }

  function stopRecording(keep) {
    if (!rec || rec.mr.state === "inactive") return;
    rec.keep = keep;
    rec.mr.stop();
  }

  async function finishRecording() {
    const r = rec;
    if (!r) return;
    clearInterval(r.timer);
    r.stream.getTracks().forEach((t) => t.stop());
    const dur = (Date.now() - r.t0) / 1000;
    const blob = new Blob(r.chunks, { type: (r.mr.mimeType || "audio/webm").split(";")[0] });
    rec = null;
    if (wakeLock && !aarti) { wakeLock.release().catch(() => {}); wakeLock = null; }
    if (r.keep) {
      if (dur < 1 || !blob.size) toast("That was too short to keep");
      else {
        try { await saveMine(r.id, blob, dur); toast("Saved. Tap Listen to hear it"); }
        catch (e) { toast("Couldn't save the recording on this device"); }
      }
    }
    paintRecorder();
    if (location.hash.startsWith("#/recordings")) route();
  }

  async function shareMine(id) {
    const m = mine[id];
    const p = prayer(id);
    if (!m) return;
    const blob = await fetch(m.url).then((r) => r.blob());
    const file = new File([blob], `${id}${extFor(m.type)}`, { type: m.type || "audio/webm" });
    try {
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: p.name, text: `${p.name}, recorded for Dharma Path` });
        return;
      }
    } catch (e) { if (e && e.name === "AbortError") return; }
    const a = document.createElement("a");
    a.href = m.url; a.download = file.name;
    document.body.appendChild(a); a.click(); a.remove();
    toast("Recording saved to your downloads");
  }

  async function confirmDelete(id) {
    const p = prayer(id);
    const res = await openSheet({
      eyebrow: "Delete recording", preview: `Delete your recording of ${p.name}? This can't be undone.`,
      actions: [{ id: "delete", label: "Delete recording", primary: true }, { id: "keep", label: "Keep it" }]
    });
    if (!res || res.id !== "delete") return false;
    await deleteMine(id);
    toast("Recording deleted");
    return true;
  }

  // Chrome writes recordings without a duration, which leaves the player's timeline blank until it is read once.
  document.addEventListener("loadedmetadata", (e) => {
    const a = e.target;
    if (a.tagName !== "AUDIO" || a.duration !== Infinity) return;
    a.addEventListener("timeupdate", function reset() { a.removeEventListener("timeupdate", reset); a.currentTime = 0; });
    a.currentTime = 1e101;
  }, true);

  function recordingsView() {
    const ids = Object.keys(mine).filter((id) => prayer(id)).sort((a, b) => mine[b].t - mine[a].t);
    const published = Object.keys(recordings).filter((id) => prayer(id));
    return `
      <h2 class="page-title">Your recordings</h2>
      <p class="page-sub">Chants recorded in your own voice, or by family or a priest. They stay on this device and play instead of the device voice.</p>
      ${ids.length ? `<div class="list">${ids.map((id) => {
        const p = prayer(id), m = mine[id];
        return `<div class="row rec-row">${seal(deityOf(p.deity).deva)}
          <span class="body"><a href="#/puja/${id}"><h3>${esc(p.name)}</h3></a><p>${esc(typeOf(p.type).one)} · ${fmtDur(m.dur)}</p>
            <audio controls preload="metadata" src="${m.url}"></audio>
            <span class="rec-actions"><button class="chip" data-rec-share="${id}">Share or send</button><button class="chip" data-rec-delete="${id}">Delete</button></span>
          </span></div>`;
      }).join("")}</div>` : `<div class="card empty">${canRecord() ? "No recordings yet. Open any prayer or mantra and tap <b>Record</b>." : "This browser can't record audio. Try Chrome on Android or Safari on iPhone."}</div>`}

      <div class="section">
        <div class="card">
          <div class="eyebrow">For everyone</div>
          <h3 class="card-h">Offer a recording to Dharma Path</h3>
          <p class="meta" style="margin:0 0 10px">A clear recording by a priest, a teacher or a devoted family member is a gift to everyone who uses the app. Tap <b>Share or send</b> and send the file to Amar Latchman, who made Dharma Path. Once it's added, everyone will hear it.</p>
          <p class="meta" style="margin:0">For the best sound, record in a quiet room with the phone a hand's width away. Only share recordings you made yourself or have permission to share.</p>
        </div>
      </div>

      ${published.length ? `<div class="section"><div class="section-head"><h2 class="section-title">Recorded for everyone</h2></div>
        <div class="list">${published.map((id) => prayerRow(prayer(id))).join("")}</div></div>` : ""}`;
  }

  /* ====================================================================== */
  /* Learn                                                                   */
  /* ====================================================================== */
  const completed = (courseId) => store.get("progress:" + courseId, []);

  // The 2026 Academy rewrite reordered some lessons; carry finished lessons over to their new places once.
  if (!store.get("academy:v2", false)) {
    const moved = { foundations: { 4: 5 }, devi: { 2: 3 }, gita: { 4: 5, 5: 7 }, epics: { 1: 2, 2: 5 }, meditation: { 3: 4 }, temples: { 1: 3, 2: null } };
    Object.entries(moved).forEach(([cid, map]) => {
      const done = completed(cid);
      if (done.length) store.set("progress:" + cid, [...new Set(done.map((i) => (i in map ? map[i] : i)).filter((i) => i != null))]);
    });
    store.set("academy:v2", true);
  }

  const lessonWords = (l) => stripTags(l.body + " " + (l.practice || "")).split(/\s+/).length;
  const lessonMins = (l) => Math.max(2, Math.round(lessonWords(l) / 200));
  const artSrc = (art) => /\.(jpe?g|png|webp|svg)$/i.test(art) ? art : `img/learn/${art}.svg`;
  const plate = (art, alt, cls = "") => art ? `<figure class="plate ${cls}"><img src="${artSrc(art)}" alt="${esc(alt || "")}" loading="lazy" decoding="async"></figure>` : "";
  const lessonHref = (cid, i) => `#/academy/${cid}/${i + 1}`;

  // The next lesson to open in a course: the first one not yet completed.
  function nextLesson(c) {
    const done = completed(c.id);
    const i = c.lessons.findIndex((l, k) => !done.includes(k));
    return i < 0 ? null : i;
  }

  function learnView() {
    const active = store.get("academyFilter", "all");
    const order = C.categories.map((c) => c.id);
    const courses = (active === "all" ? C.courses : C.courses.filter((c) => c.category === active))
      .slice().sort((a, b) => order.indexOf(a.category) - order.indexOf(b.category));
    const last = store.get("academy:last", null);
    const lc = last && byId(C.courses, last.c);
    const li = lc ? (completed(lc.id).includes(last.i) ? nextLesson(lc) : last.i) : null;
    const total = C.courses.reduce((n, c) => n + c.lessons.length, 0);
    return `
      <h2 class="page-title">Learn</h2>
      <p class="page-sub">${C.courses.length} illustrated courses and ${total} lessons on Hindu thought and practice, and guides to the sacred rites of life.</p>
      ${lc && li != null ? `
        <a class="night continue-lesson" href="${lessonHref(lc.id, li)}">
          ${plate(lc.lessons[li].art, "", "mini")}
          <span class="body"><span class="eyebrow">Continue learning</span><h3>${esc(lc.lessons[li].title)}</h3><span class="meta">${esc(lc.title)} · Lesson ${li + 1} of ${lc.lessons.length}</span></span>
          <span class="chev">›</span></a>` : ""}
      <div class="section-head"><h2 class="section-title">Academy</h2></div>
      <div class="chips" style="margin-bottom:12px">
        ${C.categories.map((c) => `<button class="chip ${c.id === active ? "active" : ""}" data-filter="${c.id}">${esc(c.name)}</button>`).join("")}
      </div>
      <div class="list">
        ${courses.map((c) => {
          const n = completed(c.id).length;
          const mins = c.lessons.reduce((m, l) => m + lessonMins(l), 0);
          return `<a class="row course-row" href="#/academy/${c.id}">${plate(c.art, "", "thumb")}
            <span class="body"><h3>${esc(c.title)}</h3><p>${esc(c.subtitle)}</p><p class="course-meta">${c.lessons.length} lessons · ${mins} min${n ? ` · ${n === c.lessons.length ? "completed" : n + " done"}` : ""}</p>
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
    const next = nextLesson(c);
    const mins = c.lessons.reduce((m, l) => m + lessonMins(l), 0);
    const cat = byId(C.categories, c.category);
    return `
      ${plate(c.art, c.title, "course-hero")}
      <div class="course-head">
        <div class="eyebrow">${esc(cat ? cat.name : "Academy")} · ${c.lessons.length} lessons · ${mins} min</div>
        <h2 class="page-title">${esc(c.title)}</h2>
        <p class="page-sub">${esc(c.subtitle)}</p>
        ${c.intro ? `<p class="lede">${esc(c.intro)}</p>` : ""}
        ${done.length ? `<div class="progress course-progress"><span style="width:${(done.length / c.lessons.length) * 100}%"></span></div><p class="meta">${done.length} of ${c.lessons.length} lessons completed</p>` : ""}
        <div class="btn-row" style="margin-top:12px"><a class="btn" href="${lessonHref(id, next == null ? 0 : next)}">${next == null ? "Read again" : done.length ? "Continue" : "Begin the course"}</a></div>
      </div>
      <div class="list lesson-list">
        ${c.lessons.map((l, i) => `
          <a class="row lesson-row ${done.includes(i) ? "done" : ""}" href="${lessonHref(id, i)}">
            <span class="num">${done.includes(i) ? "✓" : i + 1}</span>
            <span class="body"><h3>${esc(l.title)}</h3><p>${lessonMins(l)} min read</p></span>
            <span class="chev">›</span></a>`).join("")}
      </div>`;
  }

  function lessonView(id, n) {
    const c = byId(C.courses, id);
    const i = n - 1;
    const l = c && c.lessons[i];
    if (!l) return notFound();
    store.set("academy:last", { c: id, i });
    const done = completed(id).includes(i);
    const prev = c.lessons[i - 1], next = c.lessons[i + 1];
    return `
      <article class="lesson-page">
        <a class="eyebrow course-link" href="#/academy/${id}">${esc(c.title)}</a>
        <h2 class="lesson-title">${esc(l.title)}</h2>
        <p class="meta lesson-meta">Lesson ${n} of ${c.lessons.length} · ${lessonMins(l)} min read${done ? " · Completed" : ""}</p>
        ${plate(l.art, l.caption || l.title, "lesson-art")}
        ${l.caption ? `<p class="caption">${esc(l.caption)}</p>` : ""}
        <div class="prose lesson-body">${l.body}</div>
        ${l.terms && l.terms.length ? `<div class="card terms"><div class="eyebrow">Key terms</div><dl>${l.terms.map(([t, d]) => `<dt>${esc(t)}</dt><dd>${esc(d)}</dd>`).join("")}</dl></div>` : ""}
        ${l.practice ? `<div class="card practice"><div class="eyebrow">Try this</div><p>${esc(l.practice)}</p></div>` : ""}
        ${l.links && l.links.length ? `<div class="lesson-links">${l.links.map(([label, href]) => `<a class="row" href="${href}"><span class="body"><h3>${esc(label)}</h3></span><span class="chev">›</span></a>`).join("")}</div>` : ""}
        <div class="lesson-done">
          <button class="btn ${done ? "ghost" : ""}" data-lesson-done="${id}:${i}">${done ? "Completed ✓" : next ? "Mark complete and continue" : "Complete the course"}</button>
        </div>
        <nav class="lesson-nav">
          ${prev ? `<a href="${lessonHref(id, i - 1)}"><span class="meta">Previous</span><span>${esc(prev.title)}</span></a>` : `<span></span>`}
          ${next ? `<a class="next" href="${lessonHref(id, i + 1)}"><span class="meta">Next</span><span>${esc(next.title)}</span></a>` : `<a class="next" href="#/academy/${id}"><span class="meta">Finished</span><span>Back to the course</span></a>`}
        </nav>
      </article>`;
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
    if (book.singlePart) return pos.title || `${book.sectionLabel} ${pos.sec}`;
    if (pos.single && pos.partName) return pos.partName;
    return `${pos.partName || book.partLabel + " " + pos.part} · ${pos.title || book.sectionLabel + " " + pos.sec}`;
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
    const bookRow = (b) => {
      const pos = getPos(b.id);
      return `<a class="row" href="${pos ? readerHref(b.id, pos.part, pos.sec) : `#/read/${b.id}`}">${seal(b.sanskritTitle)}
        <span class="body"><h3>${esc(b.title)}</h3><p>${esc(pos ? "Continue · " + posLabel(b, pos) : b.tagline)}</p>
        ${pos ? `<div class="progress"><span data-progress="${b.id}" style="width:0"></span></div>` : ""}</span>
        <span class="chev">›</span></a>`;
    };
    const gita = byId(C.books, "gita");
    const gpos = getPos("gita");
    return `
      <h2 class="page-title">Scriptures</h2>
      <p class="page-sub">The great texts of Hinduism, from the Vedas to the Puranas. Your place in each book is saved on this device.</p>
      <div class="card book">
        <a class="night cover" href="#/read/gita">
          ${mandala()}
          <div class="dv">${gita.sanskritTitle}</div>
          <h3>${esc(gita.title)}</h3>
          <p>${esc(gita.tagline)}</p>
        </a>
        <div class="foot">
          ${gpos ? `<div class="meta" style="display:flex;justify-content:space-between;gap:10px"><span>${esc(posLabel(gita, gpos))}</span><span data-progress-label="gita"></span></div>
            <div class="progress"><span data-progress="gita" style="width:0"></span></div>` : `<div class="meta">${esc(gita.translation)}</div>`}
          <div class="btn-row" style="margin-top:14px">
            <a class="btn" href="${gpos ? readerHref("gita", gpos.part, gpos.sec) : readerHref("gita", 1, 1)}">${gpos ? "Continue reading" : "Begin reading"}</a>
            <a class="btn ghost" href="#/read/gita">Contents</a>
          </div>
        </div>
      </div>
      ${C.bookCategories.filter((c) => c.id !== "gita").map((c) => {
        const books = C.books.filter((b) => b.category === c.id);
        return books.length ? `<div class="section-head" style="margin-top:22px"><h2 class="section-title">${esc(c.name)}</h2></div><div class="list">${books.map(bookRow).join("")}</div>` : "";
      }).join("")}
      <div class="list" style="margin-top:22px">
        <a class="row" href="#/saved">${seal("चिह्न")}<span class="body"><h3>Bookmarks and notes</h3><p>${Object.keys(getMarks()).length} saved · tap any verse while reading</p></span><span class="chev">›</span></a>
        <a class="row" href="#/read/about">${seal("स्रोत")}<span class="body"><h3>About these translations</h3><p>Sources and credits</p></span><span class="chev">›</span></a></div>`;
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
          <li>Rig Veda Sanskrit: Vedic Heritage Portal, via the DharmicData project (Open Database License). English translation of the selected hymns: Dharma Path.</li>
          <li>Sama Veda: Ralph T. H. Griffith, <em>The Hymns of the Sama-Veda</em>, 1895, via the DharmicData project.</li>
          <li>Upanishads: Swami Paramananda, <em>The Upanishads</em>, 1919 (Project Gutenberg #3283).</li>
          <li>Vishnu Purana: Manmatha Nath Dutt, after H. H. Wilson (Project Gutenberg #66208), as prepared by the open-source Tattvika (Kathaveda) project.</li>
          <li>Yoga Sutras: Charles Johnston, <em>The Yoga Sutras of Patanjali</em>, 1912 (Project Gutenberg #2526).</li>
        </ul>
        <p class="meta">Most of these translations are a century or more old and use archaic English (“thou”, “doth”). Apart from the Rig Veda selection's English, which is new, they are in the public domain.</p>
      </div>`;
  }

  async function bookView(bookId) {
    const book = byId(C.books, bookId);
    if (!book) return notFound();
    const index = await loadIndex();
    const parts = index[bookId].parts;
    const pos = getPos(bookId);
    let rows;
    if (parts.length === 1 && bookId !== "gita") {
      const sections = await loadSections(bookId, 1);
      rows = sections.map((sec, i) => `
          <a class="row" href="${readerHref(bookId, 1, i + 1)}">
            <span class="dateblock"><span class="d" style="font-size:${String(sec.short || i + 1).length > 3 ? "1.05rem" : "1.7rem"}">${esc(sec.short || i + 1)}</span></span>
            <span class="body"><h3>${esc(sec.label)}</h3><p>${esc(sec.name ? sec.name + " · " : "")}${(sec.verses || sec.paras).length} ${sec.verses ? "verses" : "paragraphs"}</p></span>
            ${pos && pos.sec === i + 1 ? `<span class="tag gold">Reading</span>` : `<span class="chev">›</span>`}
          </a>`).join("");
    } else {
      rows = parts.map((p) => `
          <a class="row" href="${bookId === "gita" || p.count === 1 ? readerHref(bookId, p.n, 1) : `#/read/${bookId}/${p.n}`}">
            <span class="dateblock"><span class="d">${p.n}</span></span>
            <span class="body"><h3>${esc(p.name)}</h3><p>${esc(p.sub || "")}${p.count > 1 || bookId === "gita" ? `${p.sub ? " · " : ""}${p.count} ${bookId === "gita" ? "verses" : (book.sectionLabel.toLowerCase() + "s")}` : ""}</p></span>
            ${pos && pos.part === p.n ? `<span class="tag gold">Reading</span>` : `<span class="chev">›</span>`}
          </a>`).join("");
    }
    return `
      <div class="night book-hero fade-in">
        ${mandala()}
        <div class="eyebrow">${esc(byId(C.bookCategories, book.category).name)}</div>
        <div style="font-family:var(--deva);font-size:1.5rem;color:var(--night-gold);margin-top:10px">${book.sanskritTitle}</div>
        <h2 style="font-family:var(--display);font-weight:600;font-size:2rem;margin:4px 0 2px">${esc(book.title)}</h2>
        <p class="meta" style="margin:0">${esc(book.tagline)}</p>
        ${pos ? `<div class="btn-row"><a class="btn gold" href="${readerHref(bookId, pos.part, pos.sec)}">Continue · ${esc(posLabel(book, pos))}</a></div>` : ""}
      </div>
      <div class="card"><p style="margin:0;color:var(--ink-2)">${esc(book.about)}</p><p class="meta" style="margin:10px 0 0">${esc(book.translation)}</p></div>
      <div class="list">${rows}</div>
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
          const label = s.short || (bookId === "ramayana" ? s.n : (s.label.replace(/^Section /, "") || i + 1));
          return `<a class="sec-tile ${here ? "here" : ""}" href="${readerHref(bookId, part, i + 1)}" title="${esc(s.name || s.label)}">${esc(label)}</a>`;
        }).join("")}
      </div>`;
  }

  function renderVerse(v, prefix, showSa) {
    const o = Array.isArray(v) ? { n: v[0], sa: v[1], tr: v[2], en: v[3], ref: prefix + v[0] } : v;
    return `${o.head ? `<div class="vhead" data-i="${-1000 - o.n}">${esc(o.head)}</div>` : ""}<div class="verse" id="v-${o.n}" data-ref="${o.n}">
      <div class="vnum">${esc(o.ref || prefix + o.n)}</div>
      ${showSa && o.sa ? `<div class="sanskrit">${esc(o.sa)}</div><p class="translit">${esc(o.tr || "")}</p>` : ""}
      <p class="vtext">${esc(o.en)}</p>
      ${o.note ? `<div class="vnote">${o.note.map((n) => `<p>${esc(n)}</p>`).join("")}</div>` : ""}
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
    const subtitle = bookId === "gita" ? `${s.label} · ${index.gita.parts[part - 1].sub}`
      : meta.name === title ? (meta.sub || book.title) : `${meta.name}${s.name ? " · " + s.name : ""}`;
    const parts = index[bookId].parts;
    const prev = sec > 1 ? [part, sec - 1] : part > 1 ? [part - 1, parts[part - 2].count] : null;
    const next = sec < sections.length ? [part, sec + 1] : part < parts.length ? [part + 1, 1] : null;
    const navLabel = (pq) => {
      if (bookId === "gita") return `Chapter ${pq[0]}`;
      if (pq[0] !== part) return parts[pq[0] - 1].name.length < 22 ? parts[pq[0] - 1].name : `${book.partLabel} ${pq[0]}`;
      const t = sections[pq[1] - 1];
      return `${book.sectionLabel} ${t.short || t.n || pq[1]}`;
    };
    const showNotes = store.get("read:notes", true);
    const hasNotes = !!(s.verses && s.verses.some((v) => v.note));
    const contentsHref = bookId === "gita" || book.singlePart || meta.count === 1 ? `#/read/${bookId}` : `#/read/${bookId}/${part}`;
    const state = { bookId, part, sec, title, target: query.get("v"), targetP: query.get("p"), partName: meta.name, single: meta.count === 1 };
    const intro = (s.intro || []).map((p, k) => `<p class="para intro" data-i="${-1 - k}">${esc(p)}</p>`).join("");
    const body = intro + (s.verses
      ? s.verses.map((v) => renderVerse(v, bookId === "gita" ? `${part}.` : "", showSa)).join("")
      : s.paras.map(renderPara).join(""));

    return { state, html: `
      <div class="reader-head">
        <div class="eyebrow">${esc(book.title)}</div>
        <h2>${esc(title)}</h2>
        <p class="meta">${esc(subtitle)}</p>
        ${bookId === "ramayana" ? `<p class="meta" style="margin-top:6px">Verse numbers skip where the old translation couldn't be matched reliably to the Sanskrit.</p>` : ""}
        <div class="reader-tools">
          <button class="chip" data-font="-1" aria-label="Smaller text">A−</button>
          <button class="chip" data-font="1" aria-label="Larger text">A+</button>
          ${book.sanskrit ? `<button class="chip ${showSa ? "active" : ""}" data-sanskrit>संस्कृत</button>` : ""}
          ${hasNotes ? `<button class="chip ${showNotes ? "active" : ""}" data-notes>Commentary</button>` : ""}
          <a class="chip" href="${contentsHref}">Contents</a>
        </div>
      </div>
      <article class="reader ${showNotes ? "" : "hide-notes"}" style="--read-scale:${store.get("read:font", 1)}">${body}</article>
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
      partName: readerState.partName, single: readerState.single,
      ref: el.dataset.ref ? +el.dataset.ref : null,
      i: el.dataset.i ? +el.dataset.i : null,
      frac, t: Date.now()
    });
    const bar = document.getElementById("readBar");
    if (bar) bar.style.width = frac * 100 + "%";
    markIfRead();
  }

  function restoreReaderPos() {
    const st = readerState;
    let el = null;
    if (st.target || st.targetP != null) {
      el = st.target ? document.getElementById("v-" + st.target) : view.querySelector(`.reader [data-i="${st.targetP}"]`);
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
  /* Toasts, sheets, sharing                                                 */
  /* ====================================================================== */
  function toast(msg) {
    let t = document.getElementById("toast");
    if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => t.classList.remove("show"), 2200);
  }

  function closeSheet() {
    const b = document.querySelector(".sheet-backdrop");
    if (!b) return;
    b.classList.remove("open");
    setTimeout(() => b.remove(), 220);
  }

  // A bottom sheet with a preview and a column of actions.
  function openSheet({ eyebrow, preview, deva, actions, note }) {
    closeSheet();
    const wrap = document.createElement("div");
    wrap.className = "sheet-backdrop";
    wrap.innerHTML = `<div class="sheet" role="dialog" aria-modal="true" aria-label="${esc(eyebrow || "Options")}">
      <div class="grip"></div>
      ${eyebrow ? `<div class="eyebrow">${esc(eyebrow)}</div>` : ""}
      ${deva ? `<p class="sheet-deva">${esc(deva)}</p>` : ""}
      ${preview ? `<p class="sheet-preview">${esc(preview)}</p>` : ""}
      ${note !== undefined ? `<textarea class="sheet-note" id="sheetNote" rows="3" placeholder="Write a note or reflection…">${esc(note || "")}</textarea>` : ""}
      <div class="sheet-actions">${actions.map((a) => `<button class="${a.primary ? "btn" : "btn ghost"}" data-sheet="${a.id}">${a.label}</button>`).join("")}</div>
    </div>`;
    document.body.appendChild(wrap);
    requestAnimationFrame(() => wrap.classList.add("open"));
    return new Promise((resolve) => {
      wrap.addEventListener("click", (e) => {
        const b = e.target.closest("[data-sheet]");
        if (b) { const n = document.getElementById("sheetNote"); resolve({ id: b.dataset.sheet, note: n ? n.value.trim() : undefined }); closeSheet(); }
        else if (e.target === wrap) { resolve(null); closeSheet(); }
      });
    });
  }
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeSheet(); });

  async function copyText(text) {
    try { await navigator.clipboard.writeText(text); toast("Copied"); }
    catch (e) {
      const ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); toast("Copied"); } catch (e2) { toast("Couldn't copy on this device"); }
      ta.remove();
    }
  }

  function wrapLines(ctx, text, width) {
    const out = [];
    String(text).split("\n").forEach((para) => {
      let line = "";
      para.split(/\s+/).forEach((w) => {
        const t = line ? line + " " + w : w;
        if (ctx.measureText(t).width > width && line) { out.push(line); line = w; } else line = t;
      });
      out.push(line);
    });
    return out;
  }

  // Draw a verse onto a 1080 × 1350 card in the app's night style, then share or save it.
  async function shareCard({ eyebrow, deva, text, cite }) {
    toast("Preparing image…");
    const fonts = ['500 italic 56px "Cormorant Garamond"', '600 56px "Cormorant Garamond"', '500 44px "Noto Serif Devanagari"', '600 26px "Inter"'];
    try { await Promise.all(fonts.map((f) => document.fonts.load(f, f.includes("Devanagari") ? "ॐ अ" : "A"))); } catch (e) { /* fall back to system fonts */ }
    const W = 1080, H = 1350, pad = 96;
    const cv = document.createElement("canvas");
    cv.width = W; cv.height = H;
    const g = cv.getContext("2d");
    const bg = g.createLinearGradient(0, 0, W * 0.4, H);
    bg.addColorStop(0, "#2a2219"); bg.addColorStop(1, "#120e0b");
    g.fillStyle = bg; g.fillRect(0, 0, W, H);
    const glow = g.createRadialGradient(W * 0.85, 0, 0, W * 0.85, 0, W);
    glow.addColorStop(0, "rgba(212,176,106,0.22)"); glow.addColorStop(1, "rgba(212,176,106,0)");
    g.fillStyle = glow; g.fillRect(0, 0, W, H);
    const glow2 = g.createRadialGradient(0, H, 0, 0, H, W * 0.9);
    glow2.addColorStop(0, "rgba(142,43,32,0.28)"); glow2.addColorStop(1, "rgba(142,43,32,0)");
    g.fillStyle = glow2; g.fillRect(0, 0, W, H);
    // Line mandala
    g.save(); g.translate(W - 120, 150); g.strokeStyle = "rgba(212,176,106,0.16)"; g.lineWidth = 1.6;
    for (let i = 0; i < 16; i++) { g.save(); g.rotate((i * Math.PI) / 8); g.beginPath(); g.ellipse(0, -170, 38, 125, 0, 0, Math.PI * 2); g.stroke(); g.restore(); }
    [330, 310, 70, 30].forEach((r) => { g.beginPath(); g.arc(0, 0, r, 0, Math.PI * 2); g.stroke(); });
    g.restore();
    // Eyebrow
    g.fillStyle = "#d4b06a"; g.font = '600 26px "Inter", sans-serif';
    if ("letterSpacing" in g) g.letterSpacing = "6px";
    g.fillText(String(eyebrow || "").toUpperCase(), pad, 190);
    if ("letterSpacing" in g) g.letterSpacing = "0px";
    const maxW = W - pad * 2;
    let dl = [];
    if (deva) { g.font = '500 42px "Noto Serif Devanagari", serif'; dl = wrapLines(g, deva, maxW).slice(0, 6); }
    const devaH = dl.length ? dl.length * 74 + 30 : 0;
    // Fit the English to the remaining space, then centre the whole block between the eyebrow and the citation.
    const top = 240, bottom = H - 220;
    let size = 64, lines;
    do {
      g.font = `italic 500 ${size}px "Cormorant Garamond", Georgia, serif`;
      lines = wrapLines(g, `“${text}”`, maxW);
      if (devaH + lines.length * size * 1.3 <= bottom - top) break;
      size -= 3;
    } while (size > 30);
    let y = top + Math.max(0, (bottom - top - devaH - lines.length * size * 1.3) / 2);
    g.textBaseline = "top";
    if (dl.length) {
      g.font = '500 42px "Noto Serif Devanagari", serif'; g.fillStyle = "#d4b06a";
      dl.forEach((l) => { g.fillText(l, pad, y); y += 74; });
      y += 30;
    }
    g.font = `italic 500 ${size}px "Cormorant Garamond", Georgia, serif`;
    g.fillStyle = "#f3ead9";
    lines.forEach((l) => { g.fillText(l, pad, y); y += size * 1.3; });
    g.textBaseline = "alphabetic";
    // Citation and mark
    g.font = '500 30px "Inter", sans-serif'; g.fillStyle = "#b8a88f";
    g.fillText(cite || "", pad, H - 150);
    g.strokeStyle = "rgba(212,176,106,0.35)"; g.lineWidth = 1.5; g.beginPath(); g.moveTo(pad, H - 112); g.lineTo(W - pad, H - 112); g.stroke();
    g.fillStyle = "#d4b06a"; g.font = '500 34px "Noto Serif Devanagari", serif'; g.fillText("ॐ", pad, H - 62);
    g.font = '600 34px "Cormorant Garamond", Georgia, serif'; g.fillText("Dharma Path", pad + 50, H - 64);
    const blob = await new Promise((r) => cv.toBlob(r, "image/png"));
    const file = new File([blob], "dharma-path-verse.png", { type: "image/png" });
    try {
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({ files: [file], title: cite || "Dharma Path", text: `${text} (${cite})` });
        return;
      }
    } catch (e) { if (e && e.name === "AbortError") return; }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob); a.download = file.name;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    toast("Image saved");
  }

  /* ====================================================================== */
  /* Bookmarks, highlights and notes                                         */
  /* ====================================================================== */
  const getMarks = () => store.get("marks", {});
  const markHref = (m) => readerHref(m.book, m.part, m.sec) + (m.kind === "v" ? `?v=${m.num}` : `?p=${m.num}`);

  function itemInfo(el) {
    const st = readerState;
    const isVerse = el.classList.contains("verse");
    const num = isVerse ? el.dataset.ref : el.dataset.i;
    const book = byId(C.books, st.bookId);
    const ref = isVerse ? el.querySelector(".vnum").textContent : "";
    return {
      id: `${st.bookId}|${st.part}|${st.sec}|${isVerse ? "v" : "p"}${num}`,
      book: st.bookId, part: st.part, sec: st.sec, kind: isVerse ? "v" : "p", num,
      where: `${st.single || book.singlePart || st.bookId === "gita" ? st.title : (st.partName || "") + " · " + st.title}${ref ? " · " + ref : ""}`,
      text: (isVerse ? el.querySelector(".vtext").textContent : el.textContent).trim(),
      deva: isVerse && el.querySelector(".sanskrit") ? el.querySelector(".sanskrit").textContent.trim() : "",
      bookTitle: book.title
    };
  }

  function applyMarks() {
    if (!readerState) return;
    view.querySelectorAll(".reader .mnote").forEach((n) => n.remove());
    view.querySelectorAll(".reader .is-hl, .reader .is-bm").forEach((n) => n.classList.remove("is-hl", "is-bm"));
    const st = readerState;
    Object.values(getMarks()).forEach((m) => {
      if (m.book !== st.bookId || m.part !== st.part || m.sec !== st.sec) return;
      const el = m.kind === "v" ? document.getElementById("v-" + m.num) : view.querySelector(`.reader .para[data-i="${m.num}"]`);
      if (!el) return;
      el.classList.toggle("is-hl", !!m.hl);
      el.classList.toggle("is-bm", !!m.bm);
      if (m.note) {
        const n = document.createElement(m.kind === "v" ? "div" : "aside");
        n.className = "mnote";
        n.textContent = m.note;
        if (m.kind === "v") el.appendChild(n);
        else { n.dataset.i = m.num; el.after(n); }
      }
    });
  }

  async function itemSheet(el) {
    const info = itemInfo(el);
    const marks = getMarks();
    const m = marks[info.id] || {};
    const res = await openSheet({
      eyebrow: `${info.bookTitle} · ${info.where}`,
      deva: info.deva,
      preview: info.text.length > 280 ? info.text.slice(0, 280) + "…" : info.text,
      note: m.note || "",
      actions: [
        { id: "note", label: "Save note", primary: true },
        { id: "bm", label: m.bm ? "Remove bookmark" : "Bookmark" },
        { id: "hl", label: m.hl ? "Remove highlight" : "Highlight" },
        { id: "share", label: "Share as image" },
        { id: "copy", label: "Copy text" }
      ]
    });
    if (!res) return;
    const next = { ...m, ...info, text: info.text.slice(0, 600), t: Date.now() };
    if (res.id === "share") return shareCard({ eyebrow: info.bookTitle, deva: info.deva, text: info.text.length > 520 ? info.text.slice(0, 520) + "…" : info.text, cite: `${info.bookTitle} · ${info.where}` });
    if (res.id === "copy") return copyText(`${info.deva ? info.deva + "\n\n" : ""}${info.text}\n\n${info.bookTitle} · ${info.where}`);
    if (res.id === "bm") { next.bm = !m.bm; toast(next.bm ? "Bookmarked" : "Bookmark removed"); }
    if (res.id === "hl") { next.hl = !m.hl; toast(next.hl ? "Highlighted" : "Highlight removed"); }
    if (res.id === "note") { next.note = res.note || ""; toast(next.note ? "Note saved" : m.note ? "Note removed" : "Nothing to save"); }
    if (res.id !== "note" && res.note !== undefined && res.note !== (m.note || "")) next.note = res.note;
    if (next.bm || next.hl || next.note) marks[info.id] = next; else delete marks[info.id];
    store.set("marks", marks);
    applyMarks();
  }

  async function stanzaSheet(el) {
    const p = prayer(location.hash.split("/")[2]);
    if (!p) return;
    const i = [...el.parentNode.querySelectorAll(".stanza")].indexOf(el);
    const v = p.verses[i];
    const res = await openSheet({
      eyebrow: `${p.name}${p.verses.length > 1 ? " · verse " + (i + 1) : ""}`, deva: v[0], preview: v[2],
      actions: [{ id: "share", label: "Share as image", primary: true }, { id: "copy", label: "Copy text" }, { id: "close", label: "Close" }]
    });
    if (!res) return;
    if (res.id === "share") shareCard({ eyebrow: `${typeOf(p.type).one} · ${deityOf(p.deity).name}`, deva: v[0], text: v[2], cite: `${p.name}${p.verses.length > 1 ? " · verse " + (i + 1) : ""}` });
    if (res.id === "copy") copyText(`${v[0]}\n\n${v[1]}\n\n${v[2]}\n\n${p.name}`);
  }

  function savedView(query) {
    const f = query.get("f") || "all";
    const all = Object.values(getMarks()).sort((a, b) => b.t - a.t);
    const list = all.filter((m) => f === "all" || (f === "bm" && m.bm) || (f === "hl" && m.hl) || (f === "note" && m.note));
    const tabs = [["all", "All"], ["bm", "Bookmarks"], ["hl", "Highlights"], ["note", "Notes"]];
    return `
      <h2 class="page-title">Bookmarks and notes</h2>
      <p class="page-sub">Tap any verse or paragraph while reading to bookmark it, highlight it or write a note.</p>
      <div class="chips" style="margin-bottom:12px">${tabs.map(([id, name]) => `<a class="chip ${f === id ? "active" : ""}" href="#/saved${id === "all" ? "" : "?f=" + id}">${name}</a>`).join("")}</div>
      ${list.length ? `<div class="list">${list.map((m) => {
        const book = byId(C.books, m.book);
        return `<a class="row saved-row" href="${markHref(m)}">${seal(book ? book.sanskritTitle : "ॐ")}
          <span class="body"><h3>${esc(m.bookTitle)}</h3><p class="where">${esc(m.where)}${m.bm ? " · Bookmark" : ""}${m.hl ? " · Highlight" : ""}</p>
          <p class="snip ${m.hl ? "hl-snip" : ""}">${esc(m.text.length > 180 ? m.text.slice(0, 180) + "…" : m.text)}</p>
          ${m.note ? `<p class="note-snip">${esc(m.note)}</p>` : ""}</span><span class="chev">›</span></a>`;
      }).join("")}</div>` : `<div class="card empty">${all.length ? "Nothing here yet." : "Nothing saved yet. Open any scripture and tap a verse to begin."}</div>`}`;
  }

  /* ====================================================================== */
  /* Search                                                                  */
  /* ====================================================================== */
  // Fold scholarly spellings into everyday ones so "Kṛṣṇa", "Krishna" and "KRISHNA" all match.
  const fold = (t) => String(t || "").normalize("NFC")
    .replace(/[ṛṝ]/g, "ri").replace(/[ṚṜ]/g, "Ri").replace(/[śṣç]/g, "sh").replace(/[ŚṢÇ]/g, "Sh")
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  const keyOf = (...parts) => fold(parts.join(" ")).toLowerCase();
  const stripTags = (h) => String(h).replace(/<[^>]+>/g, " ");
  const SMALL_BOOKS = ["gita", "rigveda", "samaveda", "upanishads", "yoga", "vishnu"];
  const LARGE_BOOKS = ["ramayana", "mahabharata"];
  const searchBooks = {};
  const searchJobs = {};
  let searchToken = 0;

  function appEntries() {
    if (appEntries.cache) return appEntries.cache;
    const out = [];
    P.forEach((p) => out.push({ group: "Prayers", href: `#/puja/${p.id}`, title: p.name, where: prayerSub(p), text: p.verses.map((v) => v[2]).join(" "),
      key: keyOf(p.name, p.about, deityOf(p.deity).name, typeOf(p.type).name, ...p.verses.map((v) => v[1] + " " + v[2])) + " " + p.verses.map((v) => v[0]).join(" ") }));
    C.festivals.forEach((f) => out.push({ group: "Festivals", href: `#/festival/${f.parent || f.id}`, title: f.name, where: f.when || "Festival", text: f.meaning,
      key: keyOf(f.name, f.summary, f.meaning, ...(f.traditions || []), ...(f.atHome || [])) + " " + (f.deva || "") }));
    C.courses.forEach((c) => c.lessons.forEach((l, i) => out.push({ group: "Learn", href: lessonHref(c.id, i), title: l.title, where: c.title, text: stripTags(l.body),
      key: keyOf(c.title, l.title, stripTags(l.body), ...(l.terms || []).flat()) })));
    C.lifeEvents.forEach((e) => out.push({ group: "Learn", href: `#/life/${e.id}`, title: e.name, where: e.sanskrit, text: e.meaning,
      key: keyOf(e.name, e.sanskrit, e.meaning, ...e.steps, e.withPriest) }));
    return (appEntries.cache = out);
  }

  function indexBook(bookId) {
    if (searchBooks[bookId]) return Promise.resolve(searchBooks[bookId]);
    if (searchJobs[bookId]) return searchJobs[bookId];
    searchJobs[bookId] = (async () => {
      const book = byId(C.books, bookId);
      const index = await loadIndex();
      const entries = [];
      for (const part of index[bookId].parts) {
        const sections = await loadSections(bookId, part.n);
        sections.forEach((sec, si) => {
          const n = si + 1;
          const where = bookId === "gita" ? `Chapter ${part.n}` : book.singlePart ? sectionTitle(book, part.n, n, sec) : `${part.name} · ${sectionTitle(book, part.n, n, sec)}`;
          const base = readerHref(bookId, part.n, n);
          if (sec.verses) {
            sec.verses.forEach((v) => {
              const o = Array.isArray(v) ? { n: v[0], sa: v[1], en: v[3], ref: bookId === "gita" ? `${part.n}.${v[0]}` : `Verse ${v[0]}` } : v;
              entries.push({ href: `${base}?v=${o.n}`, title: book.title, where: `${where} · ${o.ref || o.n}`, text: o.en || "",
                key: keyOf(o.en, ...(o.note || [])) + " " + (o.sa || "") });
            });
          } else {
            sec.paras.forEach((t, i) => entries.push({ href: `${base}?p=${i}`, title: book.title, where, text: t, key: keyOf(t) }));
          }
        });
      }
      searchBooks[bookId] = entries;
      delete searchJobs[bookId];
      return entries;
    })();
    searchJobs[bookId].catch(() => delete searchJobs[bookId]);
    return searchJobs[bookId];
  }

  const termsOf = (q) => keyOf(q).split(/\s+/).filter((t) => t.length >= 2 || /[ऀ-ॿ]/.test(t));
  const matches = (e, terms) => terms.every((t) => e.key.includes(t));
  const escRe = (t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

  function snippet(text, terms, len = 170) {
    const f = fold(text);
    const low = f.toLowerCase();
    let at = -1;
    for (const t of terms) { at = low.indexOf(t); if (at >= 0) break; }
    const start = Math.max(0, at - 60);
    let html = esc(f.slice(start, start + len));
    terms.forEach((t) => { if (!/[ऀ-ॿ]/.test(t)) html = html.replace(new RegExp(escRe(esc(t)), "gi"), (m) => `<mark>${m}</mark>`); });
    return (start > 0 ? "…" : "") + html + (start + len < f.length ? "…" : "");
  }

  function resultGroup(name, items, terms, id) {
    if (!items.length) return "";
    const shown = items.slice(0, 6);
    const row = (e) => `<a class="row" href="${e.href}"><span class="body"><h3>${esc(e.title)}</h3><p class="where">${esc(e.where)}</p><p class="snip">${snippet(e.text, terms)}</p></span><span class="chev">›</span></a>`;
    return `<div class="section-head" style="margin-top:20px"><h2 class="section-title">${esc(name)}</h2><span class="meta">${items.length >= 200 ? "200+" : items.length} ${items.length === 1 ? "result" : "results"}</span></div>
      <div class="list" id="grp-${id}">${shown.map(row).join("")}
      ${items.length > shown.length ? `<button class="row more" data-more="${id}">Show ${Math.min(items.length, 200) - shown.length} more</button>` : ""}</div>
      <template id="tpl-${id}">${items.slice(6, 200).map(row).join("")}</template>`;
  }

  async function runSearch(q) {
    const token = ++searchToken;
    const out = document.getElementById("searchResults");
    if (!out) return;
    const terms = termsOf(q);
    if (!terms.length) { out.innerHTML = searchSuggestions(); return; }
    const app = appEntries().filter((e) => matches(e, terms));
    const groups = ["Prayers", "Festivals", "Learn"].map((g) => resultGroup(g, app.filter((e) => e.group === g), terms, g.toLowerCase())).join("");
    out.innerHTML = groups + `<div id="scriptureResults"><p class="meta" style="margin:20px 4px">Searching the scriptures…</p></div>`;
    const epics = store.get("search:epics", false);
    const books = SMALL_BOOKS.concat(epics ? LARGE_BOOKS : []);
    let html = "", found = app.length;
    for (const id of books) {
      let entries;
      try { entries = await indexBook(id); } catch (e) { continue; }
      if (token !== searchToken) return;
      const hits = [];
      for (const e of entries) { if (matches(e, terms)) { hits.push(e); if (hits.length >= 200) break; } }
      found += hits.length;
      html += resultGroup(byId(C.books, id).title, hits, terms, "b-" + id);
      const box = document.getElementById("scriptureResults");
      if (box) box.innerHTML = html + `<p class="meta" style="margin:20px 4px">Searching the scriptures…</p>`;
    }
    const box = document.getElementById("scriptureResults");
    if (!box || token !== searchToken) return;
    box.innerHTML = html + (epics ? "" : `
      <div class="card" style="margin-top:20px"><p style="margin:0 0 12px;color:var(--ink-2)">The Ramayana and Mahabharata are very large. Searching them downloads about 23 MB the first time, then works offline.</p>
      <button class="btn ghost" data-search-epics>Also search the Ramayana and Mahabharata</button></div>`) +
      (found ? "" : `<div class="card empty">Nothing found for “${esc(q)}”. Try a shorter word or a different spelling.</div>`);
  }

  function searchSuggestions() {
    const ideas = ["Krishna", "Hanuman", "Om Namah Shivaya", "Diwali", "karma", "Nachiketas", "peace", "Gayatri", "Ekadashi", "meditation"];
    return `<p class="meta" style="margin:16px 4px 10px">Try searching for</p>
      <div class="chips wrap">${ideas.map((t) => `<button class="chip" data-suggest="${esc(t)}">${esc(t)}</button>`).join("")}</div>`;
  }

  function searchView(query) {
    return `
      <h2 class="page-title">Search</h2>
      <div class="search-wrap">
        <svg class="ico" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg>
        <input class="search" id="globalSearch" type="search" placeholder="Prayers, festivals and scriptures" value="${esc(query.get("q") || "")}" autocomplete="off" enterkeyhint="search">
      </div>
      <div id="searchResults"></div>`;
  }

  function bindSearch() {
    const input = document.getElementById("globalSearch");
    let timer = null;
    const go = () => {
      const q = input.value.trim();
      history.replaceState(null, "", "#/search" + (q ? "?q=" + encodeURIComponent(q) : ""));
      runSearch(q);
    };
    input.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(go, 250); });
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") { clearTimeout(timer); input.blur(); go(); } });
    if (!input.value) input.focus();
    runSearch(input.value.trim());
  }

  /* ====================================================================== */
  /* Router                                                                  */
  /* ====================================================================== */
  const TITLES = { search: "Search", saved: "Scriptures", practice: "Practice", reminders: "Reminders", recordings: "Puja", calendar: "Calendar", day: "Calendar", festival: "Calendar", festivals: "Calendar", location: "Calendar", puja: "Puja", japa: "Puja", read: "Scriptures", learn: "Learn", academy: "Learn", life: "Learn" };
  const TAB = { practice: "home", reminders: "home", recordings: "puja", saved: "read", day: "calendar", festival: "calendar", festivals: "calendar", location: "calendar", japa: "puja", academy: "learn", life: "learn" };
  let routeSeq = 0;
  let navCount = 0;

  async function route() {
    const seq = ++routeSeq;
    navCount++;
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

    stopAudio();
    if (rec) stopRecording(true);
    aarti = null;
    document.body.classList.toggle("immersive", section === "aarti");
    const detail = (!!id && section !== "calendar") || ["japa", "location", "day", "festival", "festivals", "search", "saved", "practice", "reminders", "recordings"].includes(section);
    setHeader(detail ? TITLES[section] || "" : "", detail);
    setActiveTab(TAB[section] || section);

    let html, nextReader = null;
    try {
      switch (section) {
        case "home": html = await homeView(); break;
        case "search": html = searchView(query); break;
        case "saved": html = savedView(query); break;
        case "practice": html = practiceView(); break;
        case "reminders": html = await remindersView(); break;
        case "recordings": await recordingsReady; html = recordingsView(); break;
        case "calendar": html = await calendarView(id); break;
        case "day": html = await dayView(id); break;
        case "festival": html = await festivalView(id); break;
        case "festivals": html = await guidesView(); break;
        case "location": html = await locationView(); break;
        case "puja": if (id) await recordingsReady; html = id ? prayerView(id) : await pujaView(query); break;
        case "japa": await recordingsReady; html = japaView(query); break;
        case "aarti": await recordingsReady; html = aartiView(id); break;
        case "learn": html = learnView(); break;
        case "academy": html = a ? lessonView(id, +a) : courseView(id); break;
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
    if (section === "aarti") bindAarti();
    if (section === "practice") bindPractice();
    if (section === "home") fillGitaToday();
    if (section === "puja" && !id) bindPrayerSearch(query);
    if (section === "search") bindSearch();
    fillProgressBars();
    if (readerState) {
      applyMarks();
      restoreReaderPos();
      readerState.opened = Date.now();
      const st = readerState;
      setTimeout(() => { if (readerState === st) markIfRead(); }, 20500);
    }
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
    if (readerState && !e.target.closest("a, button, textarea") && !String(getSelection())) {
      const item = e.target.closest(".reader .verse, .reader .para:not(.intro)");
      if (item) { itemSheet(item); return; }
    }
    const stanza = !e.target.closest("a, button") && !String(getSelection()) && e.target.closest("#stanzas .stanza");
    if (stanza) { stanzaSheet(stanza); return; }
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
    if (t.dataset.more) {
      const tpl = document.getElementById("tpl-" + t.dataset.more);
      t.insertAdjacentHTML("beforebegin", tpl.innerHTML);
      t.remove();
      return;
    }
    if (t.dataset.suggest) {
      const input = document.getElementById("globalSearch");
      input.value = t.dataset.suggest;
      input.dispatchEvent(new Event("input"));
      return;
    }
    if ("shareGita" in t.dataset) {
      const el = document.getElementById("gitaToday");
      const ref = C.gitaDaily[dayOfYear(today()) % C.gitaDaily.length];
      shareCard({ eyebrow: "Bhagavad Gita · Verse of the day", deva: el.querySelector(".deva-text").textContent.trim(), text: el.querySelector("blockquote").textContent.replace(/^“|”$/g, ""), cite: `Bhagavad Gita ${ref[0]}.${ref[1]} · tr. Annie Besant` });
      return;
    }
    if (t.dataset.aartiOpen) {
      const el = document.documentElement;
      if (el.requestFullscreen && matchMedia("(pointer: coarse)").matches) el.requestFullscreen({ navigationUI: "hide" }).catch(() => {});
      location.hash = "#/aarti/" + t.dataset.aartiOpen;
      return;
    }
    if (t.dataset.aarti) {
      const act = t.dataset.aarti;
      if (act === "prev") aartiGo(-1);
      else if (act === "next") aartiGo(1);
      else if (act === "play") aartiPlay(t);
      else if (act === "close") closeAarti();
      else if (act === "again") { aarti.done = false; aarti.i = 0; paintAarti(); }
      else if (act === "opts") {
        const o = document.getElementById("aartiOpts");
        o.hidden = !o.hidden;
        t.setAttribute("aria-expanded", String(!o.hidden));
        t.classList.toggle("active", !o.hidden);
        fitAarti();
      }
      return;
    }
    if (t.dataset.aopt) {
      const k = t.dataset.aopt;
      const box = document.getElementById("aarti");
      if (k === "dev" || k === "rom" || k === "en") {
        const show = store.get("aartiShow", { dev: true, rom: true, en: true });
        show[k] = !show[k];
        if (!show.dev && !show.rom && !show.en) show.rom = true;
        store.set("aartiShow", show);
        ["dev", "rom", "en"].forEach((x) => box.classList.toggle("hide-" + x, !show[x]));
        box.querySelectorAll("[data-aopt]").forEach((c) => { if (c.dataset.aopt in show) c.classList.toggle("active", !!show[c.dataset.aopt]); });
      } else if (k === "repeat") {
        const on = !store.get("aarti:repeat", true);
        store.set("aarti:repeat", on);
        t.classList.toggle("active", on);
        // Stay on the same verse: find the last numbered verse reached, then step onto its refrain if one was showing.
        const r = aarti.p.verses.findIndex((v) => v[3] === "Refrain");
        const old = aarti.seq, cur = old[aarti.i];
        let lastV = -1;
        for (let n = aarti.i; n >= 0; n--) if (old[n] !== r) { lastV = old[n]; break; }
        aarti.seq = aartiSeq(aarti.p);
        let at = lastV >= 0 ? aarti.seq.indexOf(lastV) : 0;
        if (cur === r && lastV >= 0 && aarti.seq[at + 1] === r) at += 1;
        aarti.i = at;
      } else if (k === "drone") {
        const on = !Drone.on();
        store.set("audio:drone", on);
        t.classList.toggle("active", on);
        if (!on) Drone.stop();
        else if (document.querySelector('[data-aarti="play"].on')) Drone.start();
      } else if (k === "smaller" || k === "larger") {
        const sc = Math.min(1.6, Math.max(0.6, store.get("aarti:scale", 1) + (k === "larger" ? 0.1 : -0.1)));
        store.set("aarti:scale", Math.round(sc * 100) / 100);
      }
      paintAarti();
      return;
    }
    if (t.dataset.rec) {
      const id = document.getElementById("recorder").dataset.id;
      const act = t.dataset.rec;
      if (act === "start") startRecording(id);
      else if (act === "stop") stopRecording(true);
      else if (act === "cancel") stopRecording(false);
      else if (act === "share") shareMine(id);
      else if (act === "delete") confirmDelete(id).then((done) => { if (done) paintRecorder(); });
      return;
    }
    if (t.dataset.recShare) { shareMine(t.dataset.recShare); return; }
    if (t.dataset.recDelete) { confirmDelete(t.dataset.recDelete).then((done) => { if (done) route(); }); return; }
    if (t.dataset.rtype) {
      const prefs = remindPrefs();
      const k = t.dataset.rtype;
      prefs.types = prefs.types.includes(k) ? prefs.types.filter((x) => x !== k) : [...prefs.types, k];
      store.set("reminders", prefs);
      syncReminderData();
      const y = scrollY;
      route().then(() => scrollTo(0, y));
      return;
    }
    if ("ics" in t.dataset) {
      downloadIcs();
      return;
    }
    if (t.dataset.notices) {
      const on = t.dataset.notices === "on";
      t.disabled = true;
      (on ? enableNotices() : disableNotices()).then((res) => {
        if (on && res !== "granted") toast(res === "unsupported" ? "Notices aren't supported here" : "Notices weren't allowed");
        const y = scrollY;
        route().then(() => scrollTo(0, y));
      });
      return;
    }
    if (t.dataset.checkin) {
      const k = t.dataset.checkin;
      const day = practiceLog()[ymd(new Date())] || {};
      if ((day.done || []).includes(k)) unlogPractice("done", k); else logPractice("done", k);
      const y = scrollY;
      route().then(() => scrollTo(0, y));
      return;
    }
    if ("searchEpics" in t.dataset) {
      store.set("search:epics", true);
      t.disabled = true;
      t.textContent = "Searching…";
      runSearch(document.getElementById("globalSearch").value.trim());
      return;
    }
    if (t.dataset.filter) {
      store.set("academyFilter", t.dataset.filter);
      route();
    } else if (t.dataset.calFilter) {
      store.set("calFilter", t.dataset.calFilter);
      route();
    } else if (t.dataset.lessonDone) {
      const [cid, idx] = t.dataset.lessonDone.split(":");
      const i = +idx;
      const done = completed(cid);
      const c = byId(C.courses, cid);
      if (done.includes(i)) {
        store.set("progress:" + cid, done.filter((x) => x !== i));
        unlogPractice("lessons", `${cid}:${i}`);
        route();
      } else {
        store.set("progress:" + cid, [...done, i]);
        logPractice("lessons", `${cid}:${i}`);
        if (c.lessons[i + 1]) location.hash = lessonHref(cid, i + 1);
        else { toast(`Course complete: ${c.title}`); location.hash = `#/academy/${cid}`; }
      }
    } else if (t.dataset.fav) {
      const favs = store.get("favorites", []);
      const id = t.dataset.fav;
      store.set("favorites", favs.includes(id) ? favs.filter((x) => x !== id) : [...favs, id]);
      const on = !favs.includes(id);
      t.textContent = on ? "★ Saved" : "☆ Save";
      t.classList.toggle("ghost", !on);
    } else if (t.dataset.listen) {
      const p = prayer(t.dataset.listen);
      listen(p, t);
      const note = document.getElementById("audioNote");
      if (note) setTimeout(() => { if (note.isConnected) note.textContent = voiceNote(p); }, 600);
    } else if (t.dataset.meaning) {
      listenMeaning(prayer(t.dataset.meaning), t);
    } else if ("voiceToggle" in t.dataset) {
      const panel = document.getElementById("voicePanel");
      panel.hidden = !panel.hidden;
      t.classList.toggle("active", !panel.hidden);
      if (!panel.hidden) fillVoicePanel();
    } else if (t.dataset.voicePreview) {
      const kind = t.dataset.voicePreview;
      stopAudio();
      say(PREVIEW[kind], { rate: kind === "en" ? 0.86 : 0.85, english: kind === "en" });
    } else if ("drone" in t.dataset) {
      const on = !Drone.on();
      store.set("audio:drone", on);
      t.classList.toggle("active", on);
      if (!on) Drone.stop();
      else if (document.querySelector("[data-listen].on, #chantAlong.on")) Drone.start();
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
    } else if ("notes" in t.dataset) {
      const on = !store.get("read:notes", true);
      store.set("read:notes", on);
      t.classList.toggle("active", on);
      const anchor = currentItem();
      view.querySelector(".reader").classList.toggle("hide-notes", !on);
      if (anchor) anchor.scrollIntoView();
    } else if ("sanskrit" in t.dataset) {
      saveReaderPos();
      store.set("read:sanskrit", !store.get("read:sanskrit", true));
      route();
    } else if (t.dataset.offline) {
      saveBookOffline(t.dataset.offline, t);
    }
  });

  view.addEventListener("change", (e) => {
    const rp = e.target.closest("[data-rpref], [data-rtime]");
    if (rp) {
      const prefs = remindPrefs();
      if (rp.dataset.rpref) prefs[rp.dataset.rpref] = rp.checked;
      else if (rp.value) { prefs[rp.dataset.rtime] = rp.value; rp.closest(".rt").querySelector("[data-rpref]").checked = true; prefs[rp.dataset.rtime.replace("Time", "")] = true; }
      store.set("reminders", prefs);
      syncReminderData();
      return;
    }
    const sel = e.target.closest("[data-voice-select]");
    if (!sel) return;
    store.set("voice:" + sel.dataset.voiceSelect, sel.value);
    stopAudio();
    say(PREVIEW[sel.dataset.voiceSelect], { rate: 0.86, english: sel.dataset.voiceSelect === "en" });
  });

  window.addEventListener("scroll", () => {
    topbar.classList.toggle("scrolled", scrollY > 4);
    if (!readerState) return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveReaderPos, 250);
  }, { passive: true });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) saveReaderPos();
    else if (aarti) keepAwake();
  });

  document.getElementById("searchBtn").addEventListener("click", () => { location.hash = "#/search"; });

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
  setTimeout(checkNoticesNow, 4000);

  if ("serviceWorker" in navigator && location.protocol !== "file:") {
    navigator.serviceWorker.register("sw.js").catch(() => {});
  }
})();
