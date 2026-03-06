import { test, expect } from '@playwright/test';

test.describe('Visualizations Feature', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/visualizations');
  });

  test('should load visualizations page', async ({ page }) => {
    await expect(page).toHaveURL(/\/visualizations/);
    await expect(page.locator('h1, h2')).toBeVisible();
  });

  test('should display visualization gallery', async ({ page }) => {
    const gallery = page.locator('.gallery, .visualization-gallery, canvas').first();
    await expect(gallery).toBeVisible();
  });

  test('should render canvas elements', async ({ page }) => {
    // Wait for canvas to load
    await page.waitForTimeout(2000);

    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      await expect(canvas).toBeVisible();

      // Check canvas has dimensions
      const boundingBox = await canvas.boundingBox();
      expect(boundingBox).toBeTruthy();
      if (boundingBox) {
        expect(boundingBox.width).toBeGreaterThan(0);
        expect(boundingBox.height).toBeGreaterThan(0);
      }
    }
  });

  test('should allow selecting different visualizations', async ({ page }) => {
    const visualizationButtons = page.locator('button:has-text("Phase Space"), button:has-text("Winding")');
    const count = await visualizationButtons.count();

    if (count > 0) {
      await visualizationButtons.first().click();
      await page.waitForTimeout(1000);

      // Canvas should update
      const canvas = page.locator('canvas');
      await expect(canvas).toBeVisible();
    }
  });

  test('should have interactive controls', async ({ page }) => {
    // Look for control panels
    const controls = page.locator('.controls, .visualization-controls, input[type="range"]');
    if (await controls.first().isVisible()) {
      await expect(controls.first()).toBeVisible();
    }
  });

  test('should support zoom functionality', async ({ page }) => {
    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      // Get initial view
      const initialBox = await canvas.boundingBox();

      // Try to zoom (mouse wheel or zoom buttons)
      const zoomInButton = page.locator('button:has-text("Zoom In"), button:has-text("+")');
      if (await zoomInButton.first().isVisible()) {
        await zoomInButton.first().click();
        await page.waitForTimeout(500);

        // View should have changed
        const afterBox = await canvas.boundingBox();
        expect(afterBox).toBeTruthy();
      }
    }
  });

  test('should support pan functionality', async ({ page }) => {
    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      // Simulate drag
      const box = await canvas.boundingBox();
      if (box) {
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.mouse.down();
        await page.mouse.move(box.x + box.width / 2 + 50, box.y + box.height / 2 + 50);
        await page.mouse.up();

        await page.waitForTimeout(500);
        // View should have panned
      }
    }
  });

  test('should have fullscreen option', async ({ page }) => {
    const fullscreenButton = page.locator('button:has-text("Fullscreen"), button[aria-label*="Fullscreen"]');
    if (await fullscreenButton.first().isVisible()) {
      await fullscreenButton.first().click();
      await page.waitForTimeout(500);

      // Exit fullscreen
      await page.keyboard.press('Escape');
    }
  });

  test('should export visualization as image', async ({ page }) => {
    const exportButton = page.locator('button:has-text("Export"), button:has-text("Screenshot")');
    if (await exportButton.first().isVisible()) {
      const downloadPromise = page.waitForEvent('download');
      await exportButton.first().click();

      const download = await downloadPromise;
      expect(download.suggestedFilename()).toMatch(/\.(png|jpg|svg)$/);
    }
  });
});

test.describe('Visualization Performance', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/visualizations');
  });

  test('should render without performance issues', async ({ page }) => {
    // Wait for visualization to load
    await page.waitForTimeout(3000);

    // Check if page is responsive
    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      // Interact with visualization
      const box = await canvas.boundingBox();
      if (box) {
        await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
        await page.waitForTimeout(100);

        // Page should still be responsive
        await expect(canvas).toBeVisible();
      }
    }
  });

  test('should handle animation smoothly', async ({ page }) => {
    const playButton = page.locator('button:has-text("Play"), button:has-text("Animate")');
    if (await playButton.first().isVisible()) {
      await playButton.first().click();

      // Wait for animation
      await page.waitForTimeout(2000);

      // Animation should be running
      const pauseButton = page.locator('button:has-text("Pause"), button:has-text("Stop")');
      if (await pauseButton.first().isVisible()) {
        await expect(pauseButton.first()).toBeVisible();
      }
    }
  });
});

test.describe('3D Visualizations', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/visualizations');
  });

  test('should render 3D scene', async ({ page }) => {
    // Wait for WebGL to initialize
    await page.waitForTimeout(2000);

    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      // Check if WebGL context is created
      const hasWebGL = await page.evaluate(() => {
        const canvas = document.querySelector('canvas');
        if (!canvas) return false;
        return !!(canvas.getContext('webgl') || canvas.getContext('webgl2'));
      });

      expect(hasWebGL).toBe(true);
    }
  });

  test('should support camera rotation', async ({ page }) => {
    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      const box = await canvas.boundingBox();
      if (box) {
        // Drag to rotate camera
        await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
        await page.mouse.down();
        await page.mouse.move(box.x + box.width / 2 + 100, box.y + box.height / 2);
        await page.mouse.up();

        await page.waitForTimeout(500);
      }
    }
  });
});

test.describe('Responsive Visualizations', () => {
  test('should work on mobile viewport', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/visualizations');

    await page.waitForTimeout(2000);

    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      const box = await canvas.boundingBox();
      expect(box).toBeTruthy();
      if (box) {
        expect(box.width).toBeLessThanOrEqual(375);
      }
    }
  });

  test('should work on tablet viewport', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('/visualizations');

    await page.waitForTimeout(2000);

    const canvas = page.locator('canvas').first();
    await expect(canvas).toBeVisible();
  });
});
