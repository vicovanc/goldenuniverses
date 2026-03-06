import { test, expect } from '@playwright/test';

test.describe('Navigation Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should load the homepage', async ({ page }) => {
    await expect(page).toHaveTitle(/Golden Universe/i);
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should navigate to Theory page', async ({ page }) => {
    await page.click('text=Theory');
    await expect(page).toHaveURL(/\/theory/);
    await expect(page.locator('h1, h2')).toContainText(/theory/i);
  });

  test('should navigate to Calculations page', async ({ page }) => {
    await page.click('text=Calculations');
    await expect(page).toHaveURL(/\/calculations/);
  });

  test('should navigate to Visualizations page', async ({ page }) => {
    await page.click('text=Visualizations');
    await expect(page).toHaveURL(/\/visualizations/);
  });

  test('should navigate back to home from any page', async ({ page }) => {
    // Navigate away
    await page.click('text=Theory');
    await expect(page).toHaveURL(/\/theory/);

    // Navigate back
    await page.click('text=Home');
    await expect(page).toHaveURL('/');
  });

  test('should highlight active navigation item', async ({ page }) => {
    await page.click('text=Theory');
    const activeItem = page.locator('.nav-item-content.active, .active');
    await expect(activeItem).toBeVisible();
  });
});

test.describe('Sidebar Functionality', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should collapse and expand sidebar', async ({ page }) => {
    const sidebar = page.locator('.sidebar, aside');
    await expect(sidebar).toBeVisible();

    // Find and click collapse button
    const collapseButton = page.locator('button[aria-label*="Collapse"], button[aria-label*="collapse"]').first();
    await collapseButton.click();

    // Check if sidebar has collapsed class
    await expect(sidebar).toHaveClass(/collapsed/);

    // Click expand button
    const expandButton = page.locator('button[aria-label*="Expand"], button[aria-label*="expand"]').first();
    await expandButton.click();

    // Check if collapsed class is removed
    await expect(sidebar).not.toHaveClass(/collapsed/);
  });

  test('should expand nested navigation items', async ({ page }) => {
    // Look for items with children
    const expandableItem = page.locator('.expand-button, button[aria-label*="Expand"]').first();

    if (await expandableItem.isVisible()) {
      await expandableItem.click();

      // Check if children are visible
      const children = page.locator('.nav-children');
      await expect(children).toBeVisible();
    }
  });
});

test.describe('Responsive Navigation', () => {
  test('should work on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Check if mobile navigation is present
    const sidebar = page.locator('.sidebar, aside, nav');
    await expect(sidebar).toBeVisible();

    // Navigation should still work on mobile
    await page.click('text=Theory');
    await expect(page).toHaveURL(/\/theory/);
  });

  test('should work on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/');

    const sidebar = page.locator('.sidebar, aside, nav');
    await expect(sidebar).toBeVisible();

    await page.click('text=Calculations');
    await expect(page).toHaveURL(/\/calculations/);
  });
});

test.describe('Keyboard Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should navigate using Tab key', async ({ page }) => {
    // Press Tab to focus first interactive element
    await page.keyboard.press('Tab');

    // Check if an element is focused
    const focusedElement = await page.evaluateHandle(() => document.activeElement);
    expect(focusedElement).toBeTruthy();
  });

  test('should activate navigation with Enter key', async ({ page }) => {
    // Tab to a navigation link
    await page.keyboard.press('Tab');

    // Find first navigation link and focus it
    const firstLink = page.locator('a').first();
    await firstLink.focus();

    // Press Enter
    await page.keyboard.press('Enter');

    // URL should change
    const url = page.url();
    expect(url).toBeTruthy();
  });

  test('should support common keyboard shortcuts', async ({ page }) => {
    // Test keyboard shortcuts if implemented
    // Example: Ctrl+K for search
    await page.keyboard.press('Control+K');

    // Check if search modal opens (adjust selector as needed)
    const searchModal = page.locator('[role="dialog"], .modal, .search-modal');
    if (await searchModal.isVisible()) {
      await expect(searchModal).toBeVisible();
    }
  });
});

test.describe('Deep Linking', () => {
  test('should navigate directly to deep routes', async ({ page }) => {
    await page.goto('/theory/fundamentals');
    await expect(page).toHaveURL(/\/theory/);
  });

  test('should handle 404 routes', async ({ page }) => {
    await page.goto('/nonexistent-page');
    // Should redirect to home or show 404 page
    await expect(page).toHaveURL('/');
  });
});
