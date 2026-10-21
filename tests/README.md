# Tests

Browser tests for Dharma Path, run with [Playwright](https://playwright.dev). GitHub runs them on
every push (see `.github/workflows/tests.yml`); a red cross next to a commit means something broke.

| File | What it checks |
| --- | --- |
| `data.spec.js` | The app's data: every book's files, lesson paintings, links between pages, prayers named by festivals and rites, quizzes, reading plans, rite mantras, calendar cities and the offline file list. |
| `pages.spec.js` | Every kind of page opens and shows something, without errors. |
| `features.spec.js` | The main features, used as a person would: search, bookmarks, simple spelling, remembered dates, daily timings, reading plans, quizzes, learning verses by heart, rite booklets and follow-along, reporting a mistake, backup and restore. |
| `sync.spec.js` | Sync between two devices, with Google sign-in and Drive replaced by fakes. |

Every test also fails if the page throws an error.

## Running them yourself

```sh
npm install
npx playwright install chromium
npm test
```

The tests start a small local web server (`python3 -m http.server 8123`) themselves. To use a
Chromium already on the machine instead of Playwright's, set `CHROME` to its path.
