// Render SVG layers to transparent PNGs with Chromium. Usage: node render.js <svgDir> <pngDir> [name ...]
// Set PLAYWRIGHT to the playwright module path and CHROME to a Chromium binary if needed.
const { chromium } = require(process.env.PLAYWRIGHT || "playwright");
const fs = require("fs");
const path = require("path");

(async () => {
  const [inDir, outDir, ...names] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const list = names.length ? names : fs.readdirSync(inDir).filter((f) => f.endsWith(".svg")).map((f) => f.slice(0, -4));
  const browser = await chromium.launch({ executablePath: process.env.CHROME || undefined, args: ["--headless=new"] });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
  for (const name of list) {
    const svg = fs.readFileSync(path.join(inDir, name + ".svg"), "utf8");
    await page.setContent(`<!doctype html><style>html,body{margin:0;background:transparent}svg{display:block}</style>${svg}`);
    await page.waitForTimeout(40);
    await page.screenshot({ path: path.join(outDir, name + ".png"), omitBackground: true, clip: { x: 0, y: 0, width: 1600, height: 1000 } });
  }
  await browser.close();
  console.log("rendered", list.length, "layers");
})();
