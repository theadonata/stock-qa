# stock-qa

> Automated tests that check the Stock/HPP app actually works.

## About the project

**Stock/HPP** is a small web app that replaces an Excel spreadsheet for
tracking a small business's sales, stock, expenses, and cost of goods
sold. It's split across several repos — this one holds the tests that
check the other pieces behave correctly, from the outside, the same way a
real user or a real API client would.

Nothing in here starts the app itself. These tests point at an *already
running* backend and/or frontend (started from their own repos) and poke
at them over the network — they never read those repos' source code.

### Part of a bigger project

Stock/HPP is split into six repos, each one buildable and deployable on
its own:

| Repo | What it does |
|---|---|
| [stock-frontend](https://github.com/theadonata/stock-frontend) | The web app people use day to day |
| [stock-backend](https://github.com/theadonata/stock-backend) | The API and database — stores data, does the math |
| [stock-infrastructure](https://github.com/theadonata/stock-infrastructure) | Deploys and runs everything on a server |
| **stock-qa** (this repo) | Automated tests that check everything works |
| [stock-business-analyst](https://github.com/theadonata/stock-business-analyst) | The original business requirements this is built from |
| [stock-platform](https://github.com/theadonata/stock-platform) | An internal dashboard for the team building this project |

## What's here

Two independent test suites:

- **`api-tests/`** — tests the backend's HTTP API directly (pytest + httpx)
- **`e2e/`** — tests the frontend in a real browser, clicking around like a
  user would ([Playwright](https://playwright.dev/))

## Getting started

### Running the API tests

Requires Python 3.11+, and a running
[stock-backend](https://github.com/theadonata/stock-backend) instance.

```bash
cd api-tests
python -m venv .venv && source .venv/bin/activate   # .venv\Scripts\activate on Windows
pip install -e .

export API_BASE_URL=http://localhost:8000   # wherever your backend is running

pytest
```

If no backend is reachable at that address, the tests skip themselves
instead of failing — so the suite still runs fine without one.

### Running the E2E tests

Requires Node.js 18+, and a running
[stock-frontend](https://github.com/theadonata/stock-frontend) instance.

```bash
cd e2e
npm install
npx playwright install   # downloads browser binaries, first run only

npm test
```

Defaults to `http://localhost:8080` (stock-frontend's usual Docker port).
Point it elsewhere with `BASE_URL`:

```bash
BASE_URL=http://localhost:5173 npm test
```
