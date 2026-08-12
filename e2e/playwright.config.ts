// Playwright configuration for the stock-qa E2E suite.
//
// These tests treat stock-frontend as a black box: they load pages over
// HTTP from a deployed/running instance and never import or read
// stock-frontend's source, per the multi-repo convention (see
// stock-qa/CLAUDE.md).

import { defineConfig, devices } from '@playwright/test';

// Base URL of the stock-frontend instance under test. Defaults to
// stock-frontend's own docker-compose port (see that repo's
// docker-compose.yml) so `npx playwright test` "just works" without
// needing to export BASE_URL by hand every time -- override the env var
// only when pointing at something else (Vite dev server on 5173, a
// staging URL, etc.).
const BASE_URL = process.env.BASE_URL ?? 'http://localhost:8080';

export default defineConfig({
  testDir: './tests',

  // Fail the build on CI if someone accidentally leaves .only in a test.
  forbidOnly: !!process.env.CI,

  // Retry a couple of times on CI where flakiness is more likely (network,
  // shared staging environment), but not locally where a failure should be
  // immediately visible.
  retries: process.env.CI ? 2 : 0,

  reporter: 'list',

  use: {
    baseURL: BASE_URL,
    // Capture a trace only on the first retry of a failing test, to help
    // debug without slowing down every run.
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
