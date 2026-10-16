// Offline support: cache the app shell, then serve cache-first and refresh in the background.
const CACHE = "dharma-path-v16";
const DATA = "dp-data"; // reminder settings written by the app; kept across updates
const SHELL = [
  "./", "index.html", "css/styles.css", "js/content.js", "js/academy.js", "js/rites.js", "js/rite-mantras.js", "js/prayers.js", "js/app.js",
  "manifest.json", "icons/icon.svg", "icons/icon-192.png", "texts/index.json", "texts/gita.json", "calendar/index.json", "audio/index.json"
];

self.addEventListener("install", (e) => {
  // Fetch fresh copies, bypassing the browser cache, so an update is never built from stale files.
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL.map((u) => new Request(u, { cache: "reload" })))).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE && k !== DATA).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request).then((cached) => {
      const network = fetch(e.request)
        .then((res) => {
          if (res.ok && new URL(e.request.url).origin === location.origin) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(e.request, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});

/* ---------- Reminders ---------- */
// The app stores the coming days and the person's choices; this shows any notice that is due.
const pad = (n) => String(n).padStart(2, "0");
const ymd = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

async function remind() {
  const store = await caches.open(DATA);
  const url = new URL("reminders.json", self.registration.scope).href;
  const res = await store.match(url);
  if (!res) return;
  const data = await res.json();
  if (!data.notify) return;
  const now = new Date();
  const today = ymd(now);
  const tomorrow = ymd(new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1));
  const mins = now.getHours() * 60 + now.getMinutes();
  const shown = new Set(data.shown || []);
  const due = [];
  for (const ev of data.events || []) {
    if (data.eve && ev.date === tomorrow && mins >= 15 * 60) due.push({ key: `eve:${ev.date}:${ev.id}`, title: `Tomorrow: ${ev.title}`, body: ev.body, url: ev.url });
    if (ev.date === today && mins >= 4 * 60 && (data.morn || !shown.has(`eve:${ev.date}:${ev.id}`))) due.push({ key: `day:${ev.date}:${ev.id}`, title: `Today: ${ev.title}`, body: ev.body, url: ev.url });
  }
  if (data.daily && mins >= data.dailyMin && mins < data.dailyMin + 6 * 60) {
    due.push({ key: `daily:${today}`, title: "Time for your daily prayer", body: "A few quiet minutes for prayer, japa or reading.", url: "#/puja" });
  }
  let changed = false;
  for (const n of due) {
    if (shown.has(n.key)) continue;
    await self.registration.showNotification(n.title, { body: n.body, icon: "icons/icon-192.png", badge: "icons/badge.png", tag: n.key, data: { url: n.url } });
    shown.add(n.key);
    changed = true;
  }
  if (changed) {
    data.shown = [...shown].slice(-80);
    await store.put(url, new Response(JSON.stringify(data), { headers: { "Content-Type": "application/json" } }));
  }
}

self.addEventListener("periodicsync", (e) => { if (e.tag === "dp-reminders") e.waitUntil(remind()); });
self.addEventListener("message", (e) => { if (e.data && e.data.type === "dp-remind") e.waitUntil(remind()); });

self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  const target = new URL((e.notification.data && e.notification.data.url) || "#/home", self.registration.scope).href;
  e.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((wins) => {
      for (const w of wins) {
        if ("focus" in w) return w.focus().then(() => w.navigate ? w.navigate(target) : null);
      }
      return self.clients.openWindow(target);
    })
  );
});
