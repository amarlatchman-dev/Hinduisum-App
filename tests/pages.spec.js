// Every page opens and shows something, with no errors.
const { test, expect, open } = require("./helpers");

const PAGES = [
  "home", "calendar", "day/2026-11-08", "festival/holi", "festival/navaratri", "festivals", "location", "remember",
  "puja", "puja/hanuman-chalisa", "puja/gayatri", "aarti/jagdish", "japa", "recordings",
  "read", "read/gita", "read/gita/2", "read/upanishads/1/1", "read/ramcharitmanas/5/2", "read/sundarkand/1/61",
  "read/mahabharata", "read/rigveda/1", "read/about", "saved", "search?q=krishna",
  "learn", "academy/foundations", "academy/foundations/1", "academy/caribbean/4", "rites", "life/vivaha",
  "booklet/vivaha", "follow/vivaha", "stories", "story/monkey-crocodile", "story/doves-net", "quiz/gita", "memorise", "plans", "plan/manas-30", "plan/sundar-weekly",
  "practice", "reminders", "backup", "sync"
];

for (const p of PAGES) {
  test(`#/${p} opens`, async ({ page }) => {
    await open(page, p);
    const text = await page.locator("#view").innerText();
    expect(text.trim().length).toBeGreaterThan(20);
    expect(text).not.toContain("Page not found");
    expect(text).not.toContain("needs an internet connection");
  });
}
