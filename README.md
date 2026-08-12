# stock-qa

Test plans and test automation for the Stock/HPP business-finance project.

Part of the `stock-*` multi-repo project. See CLAUDE.md for scope and
sibling-repo relationships. Not yet pushed to GitHub.

This repo holds two independent black-box test suites that exercise the
*deployed/running* outputs of the sibling repos over the network — never
their source trees:

- **`api-tests/`** — pytest + httpx tests against a running `stock-backend`
  instance (its HTTP API).
- **`e2e/`** — Playwright end-to-end tests against a running `stock-frontend`
  instance (the built SPA, loaded in a real browser).

This repo does **not** start `stock-backend` or `stock-frontend` itself.
Each of those repos owns its own `Dockerfile` and `docker-compose.yml` for
local dev (see the design spec). Start them there first, then point these
test suites at the running instances via env vars.

## Running the API tests (pytest + httpx)

Requires Python 3.11+.

```bash
cd api-tests
python -m venv .venv && source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -e .

# Point at a running stock-backend instance (defaults to
# http://localhost:8000, a typical local docker-compose port, if unset).
export API_BASE_URL=http://localhost:8000

pytest
```

If no backend is reachable at `API_BASE_URL`, the tests skip themselves
(rather than error) so the suite stays runnable without a live backend.

## Running the E2E tests (Playwright)

Requires Node.js 18+.

```bash
cd e2e
npm install
npx playwright install   # downloads browser binaries, first run only

npm test
```

Defaults to `http://localhost:8080`, matching `stock-frontend`'s own
docker-compose port, so no env var needs to be set for the common case.
Only override `BASE_URL` when pointing at something else (e.g. a Vite dev
server on `5173`, or a staging URL):

```bash
BASE_URL=http://localhost:5173 npm test
```

These tests require a real, reachable `stock-frontend` instance — start
`stock-frontend`'s own docker-compose (or `npm run dev`/`preview`) setup
first, per that repo's own README/CLAUDE.md.

## Design reference

See `stock-business-analyst/docs/superpowers/specs/2026-08-12-stack-architecture-design.md`
for the full stack/testing-strategy design that these suites implement.
