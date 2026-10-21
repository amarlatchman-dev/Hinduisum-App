// Sync between two devices, with Google sign-in and Google Drive stood in for by fakes.
const { test, expect } = require("@playwright/test");

async function device(browser, drive) {
  const ctx = await browser.newContext({ baseURL: "http://localhost:8123/", serviceWorkers: "block", viewport: { width: 390, height: 844 } });
  await ctx.route("https://fonts.googleapis.com/**", (r) => r.fulfill({ contentType: "text/css", body: "" }));
  await ctx.route("**/js/config.js", (r) => r.fulfill({ contentType: "application/javascript", body: 'window.DP_CONFIG = { googleClientId: "test.apps.googleusercontent.com" };' }));
  await ctx.route("https://accounts.google.com/gsi/client", (r) => r.fulfill({ contentType: "application/javascript",
    body: 'window.google={accounts:{oauth2:{initTokenClient:(c)=>({requestAccessToken:()=>setTimeout(()=>c.callback({access_token:"tok",expires_in:3600}),10)})}}};' }));
  await ctx.route("https://www.googleapis.com/**", async (r) => {
    const req = r.request(), url = req.url(), m = req.method();
    if (req.headers().authorization !== "Bearer tok") return r.fulfill({ status: 401, body: "" });
    if (m === "GET" && url.includes("/files?")) return r.fulfill({ contentType: "application/json", body: JSON.stringify({ files: drive.file ? [{ id: "f1" }] : [] }) });
    if (m === "GET" && url.includes("/files/f1?alt=media")) return r.fulfill({ contentType: "application/json", body: drive.file });
    if (m === "PATCH") { drive.file = req.postData(); return r.fulfill({ contentType: "application/json", body: '{"id":"f1"}' }); }
    if (m === "POST") {
      const parts = req.postData().split(/--dp[a-z0-9]+/);
      drive.file = parts[2].split("\r\n\r\n").slice(1).join("\r\n\r\n").trim();
      return r.fulfill({ contentType: "application/json", body: '{"id":"f1"}' });
    }
    return r.fulfill({ status: 404, body: "" });
  });
  const page = await ctx.newPage();
  page.on("dialog", (d) => d.accept());
  return page;
}

const tap = async (page, act) => {
  await page.goto("/#/sync");
  await page.evaluate(() => { const t = document.getElementById("toast"); if (t) t.remove(); });
  await page.click(`[data-sync="${act}"]`);
  await expect(page.locator("#toast")).toContainText("Synced");
};
const value = (page, k) => page.evaluate((k) => JSON.parse(localStorage.getItem("dp:" + k)), k);

test("two devices share, merge and delete through Drive", async ({ browser }) => {
  const drive = { file: null };
  const A = await device(browser, drive), B = await device(browser, drive);
  await A.goto("/#/plan/gita-18"); await A.click("[data-plan-start]");
  await A.evaluate(() => localStorage.setItem("dp:favorites", JSON.stringify(["gayatri"])));
  await B.goto("/#/plan/sundar-7"); await B.click("[data-plan-start]");
  await B.evaluate(() => localStorage.setItem("dp:favorites", JSON.stringify(["hanuman-chalisa"])));

  await tap(A, "on");
  await tap(B, "on");
  expect(await value(B, "plan:gita-18")).toBeTruthy();
  expect((await value(B, "favorites")).sort()).toEqual(["gayatri", "hanuman-chalisa"]);
  await tap(A, "now");
  expect(await value(A, "plan:sundar-7")).toBeTruthy();

  await B.goto("/#/plan/gita-18"); await B.click("[data-plan-stop]");
  await tap(B, "now");
  await tap(A, "now");
  expect(await value(A, "plan:gita-18")).toBeNull();
});
