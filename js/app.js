(function () {
  "use strict";

  const C = window.CONTENT;
  const view = document.getElementById("view");
  const titleEl = document.getElementById("pageTitle");
  const backBtn = document.getElementById("backBtn");
  const BRAND = '<span class="om">ॐ</span> Dharma Path';

  /* ---------- Storage (safe if localStorage is unavailable) ---------- */
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
      try { localStorage.setItem("dp:" + key, JSON.stringify(value)); } catch (e) { /* ignore */ }
    }
  };

  /* ---------- Helpers ---------- */
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const byId = (list, id) => list.find((x) => x.id === id);
  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

  function dayOfYear(d) {
    return Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 86400000);
  }

  function greeting() {
    const h = new Date().getHours();
    if (h < 12) return "Suprabhatam · Good morning";
    if (h < 17) return "Namaste · Good afternoon";
    return "Shubh sandhya · Good evening";
  }

  function completed(courseId) {
    return store.get("progress:" + courseId, []);
  }

  function upcomingFestivals(count) {
    const m = new Date().getMonth() + 1;
    return [...C.festivals]
      .sort((a, b) => ((a.month - m + 12) % 12) - ((b.month - m + 12) % 12))
      .slice(0, count);
  }

  function setHeader(title, showBack) {
    titleEl.innerHTML = title ? esc(title) : BRAND;
    backBtn.hidden = !showBack;
  }

  function setActiveTab(tab) {
    document.querySelectorAll(".tabbar a").forEach((a) => {
      a.classList.toggle("active", a.dataset.tab === tab);
      if (a.dataset.tab === tab) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    });
  }

  function listCard(href, item, sub) {
    return `<a class="card list-item" href="${href}">
      <div class="badge">${item.glyph}</div>
      <div><h3>${esc(item.name || item.title)}</h3><p>${esc(sub)}</p></div>
      <span class="chev">›</span>
    </a>`;
  }

  /* ---------- Views ---------- */
  function homeView() {
    const today = new Date();
    const w = C.wisdom[dayOfYear(today) % C.wisdom.length];
    const prayer = C.prayers[dayOfYear(today) % C.prayers.length];
    const fest = upcomingFestivals(3);
    const inProgress = C.courses.filter((c) => {
      const n = completed(c.id).length;
      return n > 0 && n < c.lessons.length;
    });
    const dateStr = today.toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" });
    const gitaRef = C.gitaDaily[dayOfYear(today) % C.gitaDaily.length];

    return `
      <p class="greeting">${esc(dateStr)}<strong>${greeting()}</strong></p>

      <a class="hero" id="gitaToday" href="#/read/gita/${gitaRef[0]}?v=${gitaRef[1]}">
        <div class="eyebrow" style="color:#fff">Bhagavad Gita · verse of the day</div>
        <blockquote>Loading today's verse…</blockquote>
        <cite>— Chapter ${gitaRef[0]}, verse ${gitaRef[1]}</cite>
      </a>

      ${continueReadingCards()}

      <div class="card" style="margin-top:14px">
        <div class="eyebrow">Today's wisdom</div>
        <p style="margin:6px 0 4px;font-family:var(--serif);font-size:1.05rem">“${esc(w.text)}”</p>
        <p class="meta" style="margin:0 0 10px">— ${esc(w.source)}</p>
        <p style="margin:0">${esc(w.reflection)}</p>
      </div>

      <h2 class="section-title">Prayer of the day</h2>
      <a class="card" href="#/puja/${prayer.id}">
        <div class="eyebrow">${esc(prayer.deity)} · ${esc(prayer.time)}</div>
        <h3 style="font-family:var(--serif);margin:6px 0 4px">${prayer.glyph} ${esc(prayer.name)}</h3>
        <div class="sanskrit" style="text-align:left;font-size:1.1rem">${esc(prayer.sanskrit.split("\n").slice(0, 2).join("\n"))}…</div>
      </a>

      ${inProgress.length ? `
        <h2 class="section-title">Continue learning</h2>
        ${inProgress.map((c) => {
          const n = completed(c.id).length;
          return `<a class="card list-item" href="#/academy/${c.id}">
            <div class="badge">${c.glyph}</div>
            <div style="flex:1"><h3>${esc(c.title)}</h3><p>${n} of ${c.lessons.length} lessons</p>
            <div class="progress"><span style="width:${(n / c.lessons.length) * 100}%"></span></div></div>
          </a>`;
        }).join("")}` : ""}

      <h2 class="section-title">Coming up</h2>
      ${fest.map((f) => listCard(`#/festivals/${f.id}`, f, f.when)).join("")}

      <h2 class="section-title">Explore</h2>
      <div class="grid">
        <a class="tile g2" href="#/academy"><span class="glyph">🎓</span><h3>Academy</h3><p>${C.courses.length} courses</p></a>
        <a class="tile g4" href="#/festivals"><span class="glyph">🪔</span><h3>Festivals</h3><p>${C.festivals.length} celebrations</p></a>
        <a class="tile g3" href="#/life"><span class="glyph">🌱</span><h3>Life Events</h3><p>Rituals step by step</p></a>
        <a class="tile g1" href="#/japa"><span class="glyph">📿</span><h3>Japa</h3><p>Mantra counter</p></a>
        <a class="tile g6" href="#/read" style="grid-column:1 / -1;min-height:96px"><span class="glyph">📖</span><h3>Scriptures</h3><p>Gita, Ramayana and Mahabharata</p></a>
      </div>

      <p class="footer-note">Dharma Path is free and always will be. 🙏</p>
    `;
  }

  function academyView() {
    const active = store.get("academyFilter", "all");
    const courses = active === "all" ? C.courses : C.courses.filter((c) => c.category === active);
    return `
      <p class="lede">Short, structured courses on Hindu philosophy, deities, scripture and practice.</p>
      <div class="chip-row" role="tablist">
        ${C.categories.map((c) => `<button class="chip ${c.id === active ? "active" : ""}" data-filter="${c.id}">${esc(c.name)}</button>`).join("")}
      </div>
      <div style="margin-top:14px">
        ${courses.map((c) => {
          const n = completed(c.id).length;
          return `<a class="card" href="#/academy/${c.id}">
            <div class="list-item">
              <div class="badge">${c.glyph}</div>
              <div style="flex:1"><h3>${esc(c.title)}</h3><p>${esc(c.subtitle)}</p></div>
            </div>
            <div class="meta" style="margin-top:10px">${c.lessons.length} lessons${n ? ` · ${n} completed` : ""}</div>
            <div class="progress"><span style="width:${(n / c.lessons.length) * 100}%"></span></div>
          </a>`;
        }).join("") || `<p class="empty">No courses in this category yet.</p>`}
      </div>`;
  }

  function courseView(id) {
    const c = byId(C.courses, id);
    if (!c) return notFound();
    const done = completed(id);
    return `
      <section class="detail-hero ${c.gradient}">
        <div class="glyph">${c.glyph}</div>
        <h2>${esc(c.title)}</h2>
        <p>${esc(c.subtitle)} · ${c.lessons.length} lessons</p>
      </section>
      <div style="margin-top:16px">
        ${c.lessons.map((l, i) => `
          <details class="card lesson ${done.includes(i) ? "done" : ""}" ${i === 0 && !done.length ? "open" : ""}>
            <summary><span class="num">${done.includes(i) ? "✓" : i + 1}</span>${esc(l.title)}</summary>
            <div class="body prose">${l.body}
              <button class="btn ${done.includes(i) ? "ghost" : ""}" data-complete="${id}:${i}">
                ${done.includes(i) ? "Completed ✓" : "Mark as complete"}
              </button>
            </div>
          </details>`).join("")}
      </div>`;
  }

  function festivalsView() {
    const m = new Date().getMonth() + 1;
    const groups = {};
    upcomingFestivals(C.festivals.length).forEach((f) => {
      (groups[f.month] = groups[f.month] || []).push(f);
    });
    return `
      <p class="lede">History, meaning and how to celebrate at home. Hindu festivals follow the lunar calendar, so exact dates change each year. Check a local panchang for your region.</p>
      ${Object.keys(groups).map((month) => `
        <h2 class="section-title">${MONTHS[month - 1]}${+month === m ? " · this month" : ""}</h2>
        ${groups[month].map((f) => listCard(`#/festivals/${f.id}`, f, f.summary)).join("")}
      `).join("")}`;
  }

  function festivalView(id) {
    const f = byId(C.festivals, id);
    if (!f) return notFound();
    return `
      <section class="detail-hero ${f.gradient}">
        <div class="glyph">${f.glyph}</div>
        <h2>${esc(f.name)}</h2>
        <p>${esc(f.when)}</p>
      </section>
      <div class="card prose" style="margin-top:16px">
        <h3 style="margin-top:0">Meaning</h3>
        <p>${esc(f.meaning)}</p>
        <h3>Traditions</h3>
        <ul>${f.traditions.map((t) => `<li>${esc(t)}</li>`).join("")}</ul>
      </div>
      <div class="card prose">
        <h3 style="margin-top:0">Celebrate at home</h3>
        <ol class="steps">${f.atHome.map((t) => `<li>${esc(t)}</li>`).join("")}</ol>
      </div>`;
  }

  function lifeView() {
    return `
      <p class="lede">The samskaras are sacred rites that mark each stage of life. Follow these steps on your own, or use them to prepare for a ceremony with a priest.</p>
      ${C.lifeEvents.map((e) => listCard(`#/life/${e.id}`, e, `${e.sanskrit} · ${e.summary}`)).join("")}`;
  }

  function lifeEventView(id) {
    const e = byId(C.lifeEvents, id);
    if (!e) return notFound();
    return `
      <section class="detail-hero ${e.gradient}">
        <div class="glyph">${e.glyph}</div>
        <h2>${esc(e.name)}</h2>
        <p>${esc(e.sanskrit)}</p>
      </section>
      <div class="card prose" style="margin-top:16px">
        <h3 style="margin-top:0">About this rite</h3>
        <p>${esc(e.meaning)}</p>
      </div>
      <div class="card prose">
        <h3 style="margin-top:0">Step by step</h3>
        <ol class="steps">${e.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>
      </div>
      <div class="card prose">
        <h3 style="margin-top:0">With a priest</h3>
        <p>${esc(e.withPriest)}</p>
      </div>
      <p class="footer-note">Customs vary by region and family. Follow your family's tradition where it differs.</p>`;
  }

  function pujaView() {
    const favs = store.get("favorites", []);
    const fav = C.prayers.filter((p) => favs.includes(p.id));
    return `
      <p class="lede">Daily prayers and mantras in Sanskrit, with transliteration and meaning.</p>
      <a class="card list-item" href="#/japa" style="background:var(--saffron-soft)">
        <div class="badge" style="background:var(--surface)">📿</div>
        <div><h3>Japa counter</h3><p>Count your mantra on a 108-bead mala</p></div>
        <span class="chev">›</span>
      </a>
      ${fav.length ? `<h2 class="section-title">Your favourites</h2>${fav.map((p) => listCard(`#/puja/${p.id}`, p, `${p.deity} · ${p.time}`)).join("")}` : ""}
      <h2 class="section-title">All prayers</h2>
      ${C.prayers.map((p) => listCard(`#/puja/${p.id}`, p, `${p.deity} · ${p.time}`)).join("")}`;
  }

  function prayerView(id) {
    const p = byId(C.prayers, id);
    if (!p) return notFound();
    const isFav = store.get("favorites", []).includes(id);
    const canSpeak = "speechSynthesis" in window;
    return `
      <section class="detail-hero ${p.gradient}">
        <div class="glyph">${p.glyph}</div>
        <h2>${esc(p.name)}</h2>
        <p>${esc(p.deity)} · ${esc(p.time)}</p>
      </section>
      <div class="card" style="margin-top:16px">
        <div class="sanskrit">${esc(p.sanskrit)}</div>
        <p class="translit">${esc(p.transliteration)}</p>
      </div>
      <div class="card">
        <div class="eyebrow">Meaning</div>
        <p class="meaning">${esc(p.meaning)}</p>
        <p class="meta">Source: ${esc(p.source)}</p>
      </div>
      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <button class="btn ${isFav ? "ghost" : ""}" data-fav="${p.id}">${isFav ? "★ Saved" : "☆ Save to favourites"}</button>
        ${canSpeak ? `<button class="btn ghost" data-speak="${p.id}">🔊 Read meaning aloud</button>` : ""}
        <a class="btn ghost" href="#/japa?m=${p.id}" style="text-decoration:none">📿 Chant with counter</a>
      </div>`;
  }

  function japaView(query) {
    const mantraId = query.get("m") || store.get("japaMantra", "shiva");
    const mantra = byId(C.prayers, mantraId) || C.prayers[0];
    const count = store.get("japaCount", 0);
    const malas = store.get("japaMalas", 0);
    return `
      <div class="card japa">
        <label class="meta" for="japaSelect">Mantra</label><br>
        <select id="japaSelect" class="chip" style="margin:6px 0 4px">
          ${C.prayers.map((p) => `<option value="${p.id}" ${p.id === mantra.id ? "selected" : ""}>${esc(p.name)}</option>`).join("")}
        </select>
        <div class="sanskrit" style="font-size:1.05rem">${esc(mantra.sanskrit.split("\n")[0])}</div>
        <button class="japa-ring" id="japaBtn" aria-label="Count one repetition">${count}</button>
        <p class="meta">Tap the circle for each repetition · <span id="malaCount">${malas}</span> malas completed</p>
        <button class="btn ghost" id="japaReset">Reset</button>
      </div>
      <p class="footer-note">A mala has 108 beads. Your phone vibrates when you complete a round.</p>`;
  }

  /* ---------- Scriptures ---------- */
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

  function readerHref(bookId, part, sec) {
    return bookId === "gita" ? `#/read/gita/${part}` : `#/read/${bookId}/${part}/${sec}`;
  }

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
    const started = C.books
      .map((b) => ({ b, pos: getPos(b.id) }))
      .filter((x) => x.pos)
      .sort((a, z) => z.pos.t - a.pos.t);
    if (!started.length) return "";
    return `<h2 class="section-title">Continue reading</h2>` + started.map(({ b, pos }) => `
      <a class="card list-item" href="${readerHref(b.id, pos.part, pos.sec)}">
        <div class="badge">${b.glyph}</div>
        <div style="flex:1"><h3>${esc(b.title)}</h3><p>${esc(posLabel(b, pos))}</p>
          <div class="progress"><span data-progress="${b.id}" style="width:0"></span></div></div>
        <span class="chev">›</span>
      </a>`).join("");
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

  function fillGitaToday() {
    const el = document.getElementById("gitaToday");
    if (!el) return;
    const ref = C.gitaDaily[dayOfYear(new Date()) % C.gitaDaily.length];
    loadJSON("texts/gita.json").then((d) => {
      const v = d.chapters[ref[0] - 1].verses.find((x) => x[0] === ref[1]);
      if (!v) return;
      el.querySelector("blockquote").textContent = "“" + v[3] + "”";
      el.querySelector("cite").textContent = `— Bhagavad Gita ${ref[0]}.${ref[1]} · tap to read in context`;
    }).catch(() => {
      el.querySelector("blockquote").textContent = "Open the Gita to read today's verse.";
    });
  }

  function libraryView() {
    return `
      <p class="lede">Read the great texts at your own pace. Your place is saved automatically on this device.</p>
      ${C.books.map((b) => {
        const pos = getPos(b.id);
        return `<div class="card book-card">
          <a class="book-head ${b.gradient}" href="#/read/${b.id}">
            <span class="glyph">${b.glyph}</span>
            <div class="deva">${b.sanskritTitle}</div>
            <h3>${esc(b.title)}</h3>
            <p>${esc(b.tagline)}</p>
          </a>
          ${pos ? `
            <div class="meta" style="display:flex;justify-content:space-between;margin-top:12px">
              <span>${esc(posLabel(b, pos))}</span><span data-progress-label="${b.id}"></span>
            </div>
            <div class="progress"><span data-progress="${b.id}" style="width:0"></span></div>` : ""}
          <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap">
            ${pos
              ? `<a class="btn" href="${readerHref(b.id, pos.part, pos.sec)}">Continue reading</a>
                 <a class="btn ghost" href="#/read/${b.id}">Contents</a>`
              : `<a class="btn" href="${readerHref(b.id, 1, 1)}">Start reading</a>
                 <a class="btn ghost" href="#/read/${b.id}">Contents</a>`}
          </div>
        </div>`;
      }).join("")}
      <a class="card list-item" href="#/read/about">
        <div class="badge">ℹ️</div>
        <div><h3>About these translations</h3><p>Sources and credits</p></div>
        <span class="chev">›</span>
      </a>`;
  }

  function aboutTextsView() {
    return `
      <div class="card prose">
        ${C.books.map((b) => `<h3 style="margin-top:0">${b.glyph} ${esc(b.title)}</h3><p>${esc(b.about)}</p><p class="meta">${esc(b.translation)}</p>`).join("<hr style='border:0;border-top:1px solid var(--line);margin:18px 0'>")}
      </div>
      <div class="card prose">
        <h3 style="margin-top:0">Sources</h3>
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
      <section class="detail-hero ${book.gradient}">
        <div class="glyph">${book.glyph}</div>
        <h2>${esc(book.title)}</h2>
        <p>${esc(book.tagline)}</p>
      </section>
      <p class="meta" style="margin:14px 2px">${esc(book.translation)}</p>
      ${pos ? `<a class="card list-item" href="${readerHref(bookId, pos.part, pos.sec)}" style="background:var(--saffron-soft)">
        <div class="badge" style="background:var(--surface)">🔖</div>
        <div><h3>Continue where you left off</h3><p>${esc(posLabel(book, pos))}</p></div><span class="chev">›</span></a>` : ""}
      ${index[bookId].parts.map((p) => `
        <a class="card list-item" href="${bookId === "gita" ? readerHref("gita", p.n, 1) : `#/read/${bookId}/${p.n}`}">
          <div class="badge part-num">${p.n}</div>
          <div style="flex:1"><h3>${esc(p.name)}</h3><p>${esc(p.sub ? p.sub + " · " : "")}${p.count} ${bookId === "gita" ? "verses" : (book.sectionLabel.toLowerCase() + "s")}</p></div>
          ${pos && pos.part === p.n ? `<span class="eyebrow">Reading</span>` : `<span class="chev">›</span>`}
        </a>`).join("")}
      <button class="btn ghost" data-offline="${bookId}" style="margin-top:6px">⬇ Save whole book for offline reading</button>
      <p class="meta" id="offlineStatus"></p>`;
  }

  async function partView(bookId, part) {
    const book = byId(C.books, bookId);
    const index = await loadIndex();
    const meta = book && index[bookId].parts[part - 1];
    if (!meta) return notFound();
    const sections = await loadSections(bookId, part);
    const pos = getPos(bookId);
    return `
      <section class="detail-hero ${book.gradient}">
        <div class="glyph">${book.glyph}</div>
        <h2>${esc(meta.name)}</h2>
        <p>${esc(book.title)} · ${book.partLabel} ${part} · ${sections.length} ${book.sectionLabel.toLowerCase()}s</p>
      </section>
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

    // Previous / next section, crossing into neighbouring parts.
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
        ${next ? `<a class="btn" href="${readerHref(bookId, next[0], next[1])}">${esc(navLabel(next))} ›</a>` : `<span class="meta">The end 🙏</span>`}
      </nav>
      <div class="read-progress"><span id="readBar"></span></div>` };
  }

  /* Track the reader's place: the first verse or paragraph visible below the top bar. */
  let readerState = null;
  let saveTimer = null;

  function currentItem() {
    const top = document.querySelector(".topbar").getBoundingClientRect().bottom + 8;
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
    const doc = document.documentElement;
    const max = doc.scrollHeight - innerHeight;
    const frac = max > 0 ? Math.min(1, scrollY / max) : 0;
    store.set(posKey(readerState.bookId), {
      part: readerState.part,
      sec: readerState.sec,
      title: readerState.title,
      ref: el.dataset.ref ? +el.dataset.ref : null,
      i: el.dataset.i ? +el.dataset.i : null,
      frac,
      t: Date.now()
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
    if (el) {
      const top = document.querySelector(".topbar").getBoundingClientRect().height + 8;
      scrollTo(0, el.getBoundingClientRect().top + scrollY - top);
    }
    saveReaderPos();
  }

  window.addEventListener("scroll", () => {
    if (!readerState) return;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(saveReaderPos, 250);
  }, { passive: true });
  document.addEventListener("visibilitychange", () => { if (document.hidden) saveReaderPos(); });

  async function saveBookOffline(bookId, btn) {
    const status = document.getElementById("offlineStatus");
    const index = await loadIndex();
    const files = bookId === "gita" ? ["texts/gita.json"] : index[bookId].parts.map((p) => `texts/${bookId}/${p.n}.json`);
    btn.disabled = true;
    let done = 0;
    for (const f of files) {
      try { await loadJSON(f); } catch (e) { status.textContent = "Couldn't download everything. Check your connection and try again."; btn.disabled = false; return; }
      done++;
      status.textContent = `Downloading… ${done} of ${files.length}`;
    }
    status.textContent = "✓ Saved. This book now works without internet.";
    btn.textContent = "✓ Saved for offline reading";
  }

  function notFound() {
    return `<p class="empty">Page not found. <a href="#/home">Go home</a></p>`;
  }

  /* ---------- Router ---------- */
  const TITLES = { academy: "Academy", festivals: "Festivals", life: "Life Events", puja: "Puja", japa: "Japa", read: "Scriptures" };
  let routeSeq = 0;

  async function route() {
    const seq = ++routeSeq;
    if (readerState) saveReaderPos();
    readerState = null;

    const hash = location.hash.replace(/^#\/?/, "") || "home";
    const [path, qs] = hash.split("?");
    const [section, id, a, b] = path.split("/");
    const query = new URLSearchParams(qs || "");
    let html;
    let nextReader = null;

    if ("speechSynthesis" in window) speechSynthesis.cancel();
    setHeader(section === "home" ? "" : TITLES[section], !!id || section === "japa");
    setActiveTab(section === "japa" ? "puja" : section);

    switch (section) {
      case "academy": html = id ? courseView(id) : academyView(); break;
      case "festivals": html = id ? festivalView(id) : festivalsView(); break;
      case "life": html = id ? lifeEventView(id) : lifeView(); break;
      case "puja": html = id ? prayerView(id) : pujaView(); break;
      case "japa": html = japaView(query); break;
      case "home": html = homeView(); break;
      case "read":
        if (!id) html = libraryView();
        else if (id === "about") html = aboutTextsView();
        else {
          view.innerHTML = `<p class="empty">Opening…</p>`;
          try {
            let r = null;
            if (id === "gita" && a) r = await readerView(id, +a, 1, query);
            else if (b) r = await readerView(id, +a, +b, query);
            if (r) {
              html = typeof r === "string" ? r : r.html;
              nextReader = r.state || null;
            } else if (a) html = await partView(id, +a);
            else html = await bookView(id);
          } catch (e) {
            html = `<p class="empty">This text couldn't be loaded. Check your internet connection and try again.<br><br><a class="btn ghost" href="#/read">Back to Scriptures</a></p>`;
          }
        }
        break;
      default: html = notFound();
    }
    if (seq !== routeSeq) return; // a newer navigation won

    view.innerHTML = html;
    readerState = nextReader;
    window.scrollTo(0, 0);
    if (section === "japa") bindJapa();
    if (section === "home") fillGitaToday();
    fillProgressBars();
    if (readerState) restoreReaderPos();
  }

  /* ---------- Interactions ---------- */
  view.addEventListener("click", (e) => {
    const t = e.target.closest("button");
    if (!t) return;

    if (t.dataset.filter) {
      store.set("academyFilter", t.dataset.filter);
      route();
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
    } else if (t.dataset.complete) {
      const [cid, idx] = t.dataset.complete.split(":");
      const i = +idx;
      const done = completed(cid);
      const next = done.includes(i) ? done.filter((x) => x !== i) : [...done, i];
      store.set("progress:" + cid, next);
      const openIdx = next.includes(i) ? i + 1 : i;
      route();
      const lessons = view.querySelectorAll(".lesson");
      lessons.forEach((d, k) => { d.open = k === openIdx; });
      if (lessons[openIdx]) lessons[openIdx].scrollIntoView({ behavior: "smooth", block: "start" });
    } else if (t.dataset.fav) {
      const favs = store.get("favorites", []);
      const id = t.dataset.fav;
      store.set("favorites", favs.includes(id) ? favs.filter((x) => x !== id) : [...favs, id]);
      route();
    } else if (t.dataset.speak) {
      const p = byId(C.prayers, t.dataset.speak);
      speechSynthesis.cancel();
      speechSynthesis.speak(new SpeechSynthesisUtterance(p.name + ". " + p.meaning));
    }
  });

  function bindJapa() {
    const btn = document.getElementById("japaBtn");
    const select = document.getElementById("japaSelect");
    const malaEl = document.getElementById("malaCount");

    select.addEventListener("change", () => {
      store.set("japaMantra", select.value);
      location.hash = "#/japa?m=" + select.value;
    });
    store.set("japaMantra", select.value);

    btn.addEventListener("click", () => {
      let count = store.get("japaCount", 0) + 1;
      if (count >= 108) {
        count = 0;
        const malas = store.get("japaMalas", 0) + 1;
        store.set("japaMalas", malas);
        malaEl.textContent = malas;
        if (navigator.vibrate) navigator.vibrate([80, 60, 80]);
      } else if (navigator.vibrate) {
        navigator.vibrate(10);
      }
      store.set("japaCount", count);
      btn.textContent = count;
    });

    document.getElementById("japaReset").addEventListener("click", () => {
      store.set("japaCount", 0);
      store.set("japaMalas", 0);
      btn.textContent = 0;
      malaEl.textContent = 0;
    });
  }

  backBtn.addEventListener("click", () => {
    if (history.length > 1) history.back();
    else location.hash = "#/home";
  });

  /* ---------- Theme ---------- */
  const root = document.documentElement;
  const savedTheme = store.get("theme", null);
  const prefersDark = window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
  root.dataset.theme = savedTheme || (prefersDark ? "dark" : "light");
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
