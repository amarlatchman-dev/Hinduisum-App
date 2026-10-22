// The main features, used as a person would use them.
const { test, expect, open } = require("./helpers");

test("search finds a Gita verse by its English", async ({ page }) => {
  await open(page, "search?q=" + encodeURIComponent("fruit of action"));
  await expect(page.locator("#scriptureResults")).toContainText("Bhagavad Gita", { timeout: 20000 });
});

test("the reader saves your place and the verse sheet offers bookmarking", async ({ page }) => {
  await open(page, "read/gita/2");
  await page.click("#v-47");
  await page.click('[data-sheet="bm"]');
  const marks = await page.evaluate(() => JSON.parse(localStorage.getItem("dp:marks")));
  expect(Object.keys(marks).some((k) => k.includes("v47"))).toBe(true);
});

test("simple spelling changes the transliteration", async ({ page }) => {
  await open(page, "puja/gayatri");
  const before = await page.locator(".rom").first().innerText();
  await page.click("[data-simple]");
  const after = await page.locator(".rom").first().innerText();
  expect(before).not.toEqual(after);
  expect(after).not.toMatch(/[āīūṛṃḥśṣ]/);
});

test("a remembered passing gives the right shraddha tithi", async ({ page }) => {
  await page.goto("/#/home");
  await page.evaluate(() => localStorage.setItem("dp:city", JSON.stringify("georgetown")));
  await open(page, "remember");
  await page.fill("#pName", "Nana");
  await page.selectOption("#pKind", "passing");
  await page.fill("#pDate", "2015-03-12");
  await page.click("[data-person-add]");
  await expect(page.locator(".person").first()).toContainText("Chaitra Krishna Saptami");
});

test("a day page shows the daily timings", async ({ page }) => {
  await open(page, "day/2026-10-26");
  await expect(page.locator(".glance.timings")).toContainText("Rahu Kalam");
});

test("a reading plan starts, shows on the Today page, and can be stopped", async ({ page }) => {
  page.on("dialog", (d) => d.accept());
  await open(page, "plan/gita-18");
  await page.click("[data-plan-start]");
  await expect(page.locator(".plan-day")).toHaveCount(18);
  await open(page, "home");
  await expect(page.locator("#view")).toContainText("Day 1 of 18");
  await open(page, "plan/gita-18");
  await page.click("[data-plan-stop]");
  expect(await page.evaluate(() => localStorage.getItem("dp:plan:gita-18"))).toBeNull();
});

test("a quiz can be taken to the end and keeps the best score", async ({ page }) => {
  await open(page, "quiz/ganesha");
  const qs = await page.evaluate(() => window.CONTENT.quizzes.ganesha);
  for (let i = 0; i < qs.length; i++) {
    const text = await page.locator(".quiz-q").innerText();
    const item = qs.find((x) => x.q === text);
    await page.click(`[data-quiz-pick="${item.answer}"]`);
    await expect(page.locator(".quiz-why.ok")).toBeVisible();
    await page.click('[data-quiz="next"]');
  }
  await expect(page.locator(".quiz-score")).toContainText(`${qs.length}`);
  const saved = await page.evaluate(() => JSON.parse(localStorage.getItem("dp:quiz:ganesha")));
  expect(saved.best).toBe(qs.length);
});

test("Gita verses can be learned by heart", async ({ page }) => {
  await open(page, "memorise");
  await page.click("[data-mem-starters]");
  await expect(page.locator(".mem-row")).toHaveCount(12);
  await open(page, "memorise/review");
  await page.click("[data-mem-show]");
  await page.click('[data-mem-grade="good"]');
  const mem = await page.evaluate(() => JSON.parse(localStorage.getItem("dp:mem:gita")));
  expect(Object.values(mem).filter((m) => m.box === 1)).toHaveLength(1);
});

test("a rite booklet keeps its names and follow-along steps through the mantras", async ({ page }) => {
  await open(page, "booklet/vivaha");
  await page.fill('[data-bk="who"]', "Priya and Arjun");
  await expect(page.locator(".bk-who")).toHaveText("Priya and Arjun");
  await open(page, "follow/vivaha");
  await expect(page.locator(".aarti-verse")).toContainText("Mantra 1 of");
  await page.click('[data-aarti="next"]');
  await expect(page.locator(".aarti-verse")).toContainText("Mantra 2 of");
});

test("Report a mistake opens a filled-in GitHub issue", async ({ page, context }) => {
  await open(page, "read/gita/2");
  await page.click("#v-47");
  await page.click('[data-sheet="report"]');
  const [popup] = await Promise.all([context.waitForEvent("page"), page.click('[data-sheet="go"]')]);
  const url = decodeURIComponent(popup.url());
  expect(url).toContain("issues/new");
  expect(url).toContain("2.47");
});

test("a backup can be made and restored", async ({ page }) => {
  await page.goto("/#/home");
  await page.evaluate(() => localStorage.setItem("dp:favorites", JSON.stringify(["gayatri"])));
  await open(page, "backup");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click('[data-backup="save"]')]);
  const file = await dl.path();
  await page.evaluate(() => localStorage.removeItem("dp:favorites"));
  await page.setInputFiles("#bkFile", file);
  const sheet = page.locator(".sheet");
  await expect(sheet).toBeVisible();
  await page.click('[data-sheet="merge"]');
  await expect.poll(() => page.evaluate(() => localStorage.getItem("dp:favorites"))).toContain("gayatri");
});

test("a story can be read and is marked as read", async ({ page }) => {
  await open(page, "stories");
  await page.click('a[href="#/story/lion-hare"]');
  await expect(page.locator(".story-text")).toContainText("well");
  await expect(page.locator(".card.practice")).toContainText("Cleverness");
  expect(await page.evaluate(() => JSON.parse(localStorage.getItem("dp:stories:read")))).toContain("lion-hare");
});

test("a rite page shows how the rite was kept then and now", async ({ page }) => {
  await open(page, "life/vivaha");
  await expect(page.locator("#thenNow")).toContainText("Around the fire");
  await expect(page.locator("#thenNow")).toContainText("In the old manuals");
});
