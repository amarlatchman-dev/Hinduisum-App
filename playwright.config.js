// Browser tests for Dharma Path. Run with `npm test` (see tests/README.md).
const { defineConfig } = require("@playwright/test");

const PORT = 8123;

module.exports = defineConfig({
  testDir: "tests",
  timeout: 60000,
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["github"]] : "list",
  use: {
    baseURL: `http://localhost:${PORT}/`,
    viewport: { width: 390, height: 844 },
    serviceWorkers: "block",
    timezoneId: "America/Guyana",
    // In a development session with its own Chromium, point CHROME at it; CI uses Playwright's.
    launchOptions: process.env.CHROME ? { executablePath: process.env.CHROME, args: ["--headless=new"] } : {}
  },
  webServer: {
    command: `python3 -m http.server ${PORT}`,
    url: `http://localhost:${PORT}/`,
    reuseExistingServer: true
  }
});
