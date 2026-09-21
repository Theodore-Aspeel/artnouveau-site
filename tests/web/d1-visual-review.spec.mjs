import { expect, test } from '@playwright/test';

const VIEWPORT_LABELS = {
  'chromium-mobile-390': '390',
  'chromium-tablet-768': '768',
  'chromium-desktop': 'desktop',
};

const EXPECTED_PORTFOLIO_COLUMNS = {
  'chromium-mobile-390': 2,
  'chromium-tablet-768': 2,
  'chromium-desktop': 4,
};

function columnCount(value) {
  return value.split(' ').filter(Boolean).length;
}

test('D1 capture la baseline publique et la variante B', async ({ page }, testInfo) => {
  const viewport = VIEWPORT_LABELS[testInfo.project.name] || testInfo.project.name;

  let baselineResponse;
  try {
    baselineResponse = await page.goto(
      'https://theodore-aspeel.github.io/artnouveau-site/fr/about/',
      { waitUntil: 'networkidle', timeout: 15_000 },
    );
  } catch (error) {
    await testInfo.attach(`baseline-about-${viewport}-unavailable`, {
      body: String(error),
      contentType: 'text/plain',
    });
  }
  if (baselineResponse?.ok()) {
    await testInfo.attach(`baseline-about-${viewport}`, {
      body: await page.screenshot({ fullPage: true }),
      contentType: 'image/png',
    });
  } else if (baselineResponse) {
    await testInfo.attach(`baseline-about-${viewport}-unavailable`, {
      body: `HTTP ${baselineResponse.status()}`,
      contentType: 'text/plain',
    });
  }

  const variantResponse = await page.goto('/fr/about/', { waitUntil: 'networkidle' });
  expect(variantResponse?.ok()).toBeTruthy();
  await expect(page.locator('#portfolio')).toBeVisible();
  const layout = await page.evaluate(() => ({
    portfolio: getComputedStyle(document.querySelector('.about-studio-portfolio__grid')).gridTemplateColumns,
    imagesLoaded: [...document.querySelectorAll('.about-studio-portfolio__grid img')].every((image) => image.complete && image.naturalWidth > 0),
  }));
  expect(columnCount(layout.portfolio)).toBe(EXPECTED_PORTFOLIO_COLUMNS[testInfo.project.name]);
  expect(layout.imagesLoaded).toBeTruthy();
  const responsiveSources = page.locator('.about-studio-portfolio__grid picture source[data-responsive-image-format]');
  await expect(responsiveSources.first()).toHaveAttribute('srcset', /assets\/generated-images\//);
  expect(await responsiveSources.count()).toBeGreaterThanOrEqual(2);
  await testInfo.attach(`variant-b-about-${viewport}`, {
    body: await page.screenshot({ fullPage: true }),
    contentType: 'image/png',
  });
});
