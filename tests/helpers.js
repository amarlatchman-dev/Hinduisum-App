// Shared set-up for the browser tests.
const { test: base, expect } = require("@playwright/test");

// Every page is opened with web fonts stubbed out (they are not needed to test and may be offline),
// and fails the test if the app throws an error.
const test = base.extend({
  page: async ({ page }, use) => {
    const errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
    await page.route("https://fonts.gstatic.com/**", (r) => r.fulfill({ status: 404, body: "" }));
    await use(page);
    expect(errors, "errors thrown by the page").toEqual([]);
  }
});

// Open a route and wait for the app to draw it.
async function open(page, hash) {
  await page.goto("/#/" + hash);
  await page.waitForFunction(() => {
    const v = document.getElementById("view");
    return v && v.children.length > 0 && !/^\s*Opening…\s*$/.test(v.textContent);
  });
}

// The app's data files, read in Node: content.js, academy.js and the others fill window.CONTENT.
function appData() {
  const fs = require("fs"), path = require("path"), vm = require("vm");
  const root = path.join(__dirname, "..");
  const ctx = { window: {} };
  vm.createContext(ctx);
  for (const f of ["config", "content", "academy", "rites", "rite-mantras", "prayers", "plans", "quizzes", "stories"]) {
    vm.runInContext(fs.readFileSync(path.join(root, "js", f + ".js"), "utf8"), ctx);
  }
  return { C: ctx.window.CONTENT, P: ctx.window.PRAYERS, root };
}

module.exports = { test, expect, open, appData };
