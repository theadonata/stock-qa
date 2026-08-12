// Smoke test: the bare minimum check that a stock-frontend instance is up
// and its login page renders. This is intentionally shallow — it is not
// testing a full login flow (that needs a seeded backend/user and belongs
// in its own test), just that the deployed SPA loads and shows expected
// UI. Deeper flow tests (log a sale, log stock in/out, view P&L) belong in
// their own spec files per the design spec's testing strategy.

import { test, expect } from '@playwright/test';

test.describe('smoke', () => {
  test('login page loads and renders a login form', async ({ page }) => {
    // Navigate to the app root. Per the design spec, auth is
    // username/password + JWT, and the app has no public/anonymous view,
    // so loading "/" on a fresh session should land on (or redirect to) a
    // login screen.
    await page.goto('/');

    // Look for the essentials of a login form rather than pinning down
    // exact copy/markup, so this test doesn't break on minor UI wording
    // changes: a password field is the most reliable signal that we're
    // looking at a login page.
    await expect(page.locator('input[type="password"]')).toBeVisible();

    // There should be some kind of submit control to complete the login.
    await expect(
      page.locator('button[type="submit"], button:has-text("Log in"), button:has-text("Login")')
    ).toBeVisible();
  });
});
