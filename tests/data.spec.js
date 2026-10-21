// Checks on the app's data: every link, picture, book, quiz and plan points at something real.
const fs = require("fs");
const path = require("path");
const { test, expect } = require("@playwright/test");
const { appData } = require("./helpers");

const { C, P, root } = appData();
const exists = (rel) => fs.existsSync(path.join(root, rel));
const index = JSON.parse(fs.readFileSync(path.join(root, "texts/index.json"), "utf8"));
const prayerIds = new Set(P.map((p) => p.id));
const art = (a) => (a.includes("/") ? a : `img/learn/${a}.webp`);

test("every book has its index and text files", () => {
  for (const b of C.books) {
    if (b.id === "gita") { expect(exists("texts/gita.json")).toBe(true); continue; }
    expect(index[b.id], `index entry for ${b.id}`).toBeTruthy();
    for (const p of index[b.id].parts) expect(exists(`texts/${b.id}/${p.n}.json`), `${b.id}/${p.n}`).toBe(true);
  }
});

test("prayer ids are unique and every verse has Devanagari, transliteration and English", () => {
  expect(prayerIds.size).toBe(P.length);
  for (const p of P) for (const v of p.verses) expect(v.slice(0, 3).every((x) => typeof x === "string" && x.length > 0), p.id).toBe(true);
});

test("every course and lesson painting exists", () => {
  for (const c of C.courses) {
    expect(exists(art(c.art)), c.id).toBe(true);
    for (const l of c.lessons) expect(exists(art(l.art)), `${c.id}: ${l.title}`).toBe(true);
  }
});

test("links inside lessons, rites and festivals lead somewhere real", () => {
  const hrefs = [];
  for (const c of C.courses) for (const l of c.lessons) {
    (l.links || []).forEach(([, h]) => hrefs.push([`${c.id}: ${l.title}`, h]));
    (l.body.match(/href="(#\/[^"]+)"/g) || []).forEach((m) => hrefs.push([`${c.id}: ${l.title}`, m.slice(6, -1)]));
  }
  for (const r of C.lifeEvents) (r.links || []).forEach(([, h]) => hrefs.push([r.id, h]));
  for (const f of C.festivals) if (f.caribbean) hrefs.push([f.id, f.caribbean[1]]);
  const courses = Object.fromEntries(C.courses.map((c) => [c.id, c]));
  for (const [where, h] of hrefs) {
    const [section, id, n] = h.replace(/^#\//, "").split("?")[0].split("/");
    if (section === "puja" && id) expect(prayerIds.has(id), `${where} → ${h}`).toBe(true);
    if (section === "academy" && id) {
      expect(courses[id], `${where} → ${h}`).toBeTruthy();
      if (n) expect(+n <= courses[id].lessons.length, `${where} → ${h}`).toBe(true);
    }
    if (section === "festival") expect(C.festivals.some((f) => f.id === id), `${where} → ${h}`).toBe(true);
    if (section === "life") expect(C.lifeEvents.some((r) => r.id === id), `${where} → ${h}`).toBe(true);
    if (section === "read" && id && id !== "about" && id !== "gita") expect(index[id], `${where} → ${h}`).toBeTruthy();
  }
});

test("prayers named by festivals, rites and weekdays exist", () => {
  for (const f of C.festivals) (f.prayers || []).forEach((id) => expect(prayerIds.has(id), `${f.id} → ${id}`).toBe(true));
  for (const r of C.lifeEvents) (r.prayers || []).forEach((id) => expect(prayerIds.has(id), `${r.id} → ${id}`).toBe(true));
  for (const w of C.weekdays) (w.prayers || []).forEach((id) => expect(prayerIds.has(id), `${w.name} → ${id}`).toBe(true));
});

test("every quiz question has four options, one answer and a real lesson", () => {
  for (const [id, qs] of Object.entries(C.quizzes)) {
    const c = C.courses.find((x) => x.id === id);
    expect(c, id).toBeTruthy();
    expect(qs.length).toBeGreaterThanOrEqual(4);
    for (const q of qs) {
      expect(q.options.length, q.q).toBe(4);
      expect(new Set(q.options).size, q.q).toBe(4);
      expect(q.answer >= 0 && q.answer < 4, q.q).toBe(true);
      expect(q.lesson >= 1 && q.lesson <= c.lessons.length, q.q).toBe(true);
      expect(q.why.length).toBeGreaterThan(10);
    }
  }
  for (const c of C.courses) expect(C.quizzes[c.id], `quiz for ${c.id}`).toBeTruthy();
});

test("reading plans point at real parts and sections", () => {
  for (const p of C.plans) {
    if (p.weekly) continue;
    const parts = p.book === "gita" ? null : index[p.book].parts;
    for (const [part, from, to] of p.days || []) {
      if (!parts) { expect(part >= 1 && part <= 18).toBe(true); continue; }
      expect(part <= parts.length, p.id).toBe(true);
      expect(from >= 1 && to <= parts[part - 1].count && from <= to, `${p.id} ${part}:${from}-${to}`).toBe(true);
    }
    for (const [part, doha] of p.breaks || []) {
      expect(part <= parts.length, p.id).toBe(true);
      if (doha !== "end") expect(doha + 1 <= parts[part - 1].count, `${p.id} ${part}:${doha}`).toBe(true);
    }
  }
});

test("every rite mantra set belongs to a rite and is complete", () => {
  for (const [id, set] of Object.entries(C.riteMantras)) {
    expect(C.lifeEvents.some((r) => r.id === id), id).toBe(true);
    for (const g of set.groups) for (const m of g.mantras) expect(m.sa && m.tr && m.en && m.src, `${id}: ${m.at}`).toBeTruthy();
  }
});

test("the calendar covers every city in its index", () => {
  const cal = JSON.parse(fs.readFileSync(path.join(root, "calendar/index.json"), "utf8"));
  for (const c of cal.cities) expect(exists(`calendar/${c.id}.json`), c.id).toBe(true);
  expect(exists("calendar/tithi.json")).toBe(true);
});

test("the offline cache lists only files that exist", () => {
  const sw = fs.readFileSync(path.join(root, "sw.js"), "utf8");
  const list = sw.match(/\[([^\]]+)\]/)[1].match(/"([^"]+)"/g).map((s) => s.slice(1, -1));
  for (const f of list) if (f !== "./") expect(exists(f), f).toBe(true);
});
