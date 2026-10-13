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

    return `
      <p class="greeting">${esc(dateStr)}<strong>${greeting()}</strong></p>

      <section class="hero">
        <div class="eyebrow" style="color:#fff">Today's wisdom</div>
        <blockquote>“${esc(w.text)}”</blockquote>
        <cite>— ${esc(w.source)}</cite>
      </section>

      <div class="card" style="margin-top:14px">
        <div class="eyebrow">Reflect</div>
        <p style="margin:6px 0 0">${esc(w.reflection)}</p>
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

  function notFound() {
    return `<p class="empty">Page not found. <a href="#/home">Go home</a></p>`;
  }

  /* ---------- Router ---------- */
  const TITLES = { academy: "Academy", festivals: "Festivals", life: "Life Events", puja: "Puja", japa: "Japa" };

  function route() {
    const hash = location.hash.replace(/^#\/?/, "") || "home";
    const [path, qs] = hash.split("?");
    const [section, id] = path.split("/");
    const query = new URLSearchParams(qs || "");
    let html;

    switch (section) {
      case "academy": html = id ? courseView(id) : academyView(); break;
      case "festivals": html = id ? festivalView(id) : festivalsView(); break;
      case "life": html = id ? lifeEventView(id) : lifeView(); break;
      case "puja": html = id ? prayerView(id) : pujaView(); break;
      case "japa": html = japaView(query); break;
      case "home": html = homeView(); break;
      default: html = notFound();
    }

    if ("speechSynthesis" in window) speechSynthesis.cancel();
    view.innerHTML = html;
    setHeader(section === "home" ? "" : TITLES[section], !!id || section === "japa");
    setActiveTab(section === "japa" ? "puja" : section);
    window.scrollTo(0, 0);
    if (section === "japa") bindJapa();
  }

  /* ---------- Interactions ---------- */
  view.addEventListener("click", (e) => {
    const t = e.target.closest("button");
    if (!t) return;

    if (t.dataset.filter) {
      store.set("academyFilter", t.dataset.filter);
      route();
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
