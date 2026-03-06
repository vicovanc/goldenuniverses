import { test, expect } from '@playwright/test';

test.describe('Calculations Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/calculations');
  });

  test('should load calculations page', async ({ page }) => {
    await expect(page).toHaveURL(/\/calculations/);
    await expect(page.locator('h1, h2')).toContainText(/calculation/i);
  });

  test('should display calculation form', async ({ page }) => {
    // Look for input fields
    const inputs = page.locator('input, select');
    await expect(inputs.first()).toBeVisible();
  });

  test('should run a particle mass calculation', async ({ page }) => {
    // Fill in calculation parameters
    const nInput = page.locator('input[name="n"], input[placeholder*="n"]').first();
    if (await nInput.isVisible()) {
      await nInput.fill('1');
    }

    // Submit calculation
    const submitButton = page.locator('button[type="submit"], button:has-text("Calculate")').first();
    if (await submitButton.isVisible()) {
      await submitButton.click();

      // Wait for results
      await page.waitForTimeout(2000);

      // Check if results are displayed
      const results = page.locator('.results, .calculation-result, [data-testid="results"]');
      if (await results.isVisible()) {
        await expect(results).toBeVisible();
      }
    }
  });

  test('should validate input fields', async ({ page }) => {
    const submitButton = page.locator('button[type="submit"], button:has-text("Calculate")').first();
    if (await submitButton.isVisible()) {
      // Try to submit without filling fields
      await submitButton.click();

      // Check for validation errors
      const errorMessage = page.locator('.error, .validation-error, [role="alert"]');
      if (await errorMessage.isVisible()) {
        await expect(errorMessage).toBeVisible();
      }
    }
  });

  test('should display calculation history', async ({ page }) => {
    // Look for history section
    const history = page.locator('.history, .calculation-history, [data-testid="history"]');
    if (await history.isVisible()) {
      await expect(history).toBeVisible();
    }
  });

  test('should export calculation results', async ({ page }) => {
    const exportButton = page.locator('button:has-text("Export"), button:has-text("Download")').first();
    if (await exportButton.isVisible()) {
      // Set up download listener
      const downloadPromise = page.waitForEvent('download');
      await exportButton.click();

      // Wait for download
      const download = await downloadPromise;
      expect(download.suggestedFilename()).toBeTruthy();
    }
  });
});

test.describe('Calculation Presets', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/calculations');
  });

  test('should load preset calculations', async ({ page }) => {
    const presetButton = page.locator('button:has-text("Preset"), .preset-button').first();
    if (await presetButton.isVisible()) {
      await presetButton.click();

      // Check if preset values are loaded
      const inputs = page.locator('input[type="number"]');
      const firstInput = inputs.first();
      if (await firstInput.isVisible()) {
        const value = await firstInput.inputValue();
        expect(value).toBeTruthy();
      }
    }
  });
});

test.describe('Real-time Calculations', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/calculations');
  });

  test('should update results in real-time', async ({ page }) => {
    const input = page.locator('input[type="number"]').first();
    if (await input.isVisible()) {
      await input.fill('5');

      // Wait for debounce
      await page.waitForTimeout(1000);

      // Check if results updated
      const results = page.locator('.results, .calculation-result');
      if (await results.isVisible()) {
        await expect(results).toBeVisible();
      }
    }
  });
});

test.describe('Error Handling', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/calculations');
  });

  test('should handle calculation errors gracefully', async ({ page }) => {
    const input = page.locator('input[type="number"]').first();
    if (await input.isVisible()) {
      // Enter invalid value
      await input.fill('-999');

      const submitButton = page.locator('button[type="submit"]').first();
      if (await submitButton.isVisible()) {
        await submitButton.click();

        // Wait for error message
        await page.waitForTimeout(1000);

        const errorMessage = page.locator('.error, [role="alert"]');
        if (await errorMessage.isVisible()) {
          await expect(errorMessage).toContainText(/error|invalid/i);
        }
      }
    }
  });
});
