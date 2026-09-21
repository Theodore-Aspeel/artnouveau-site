import { expect, test } from '@playwright/test';

const VIEWPORT_LABELS = {
  'chromium-mobile-390': '390',
  'chromium-tablet-768': '768',
  'chromium-desktop': 'desktop',
};

const EXPECTED_PORTFOLIO_COLUMNS = {
  'chromium-mobile-390': 2,
  'chromium-tablet-768': 12,
  'chromium-desktop': 12,
};

const REVIEW_PAGES = [
  { name: 'home', local: '/fr/', baseline: 'https://theodore-aspeel.github.io/artnouveau-site/fr/' },
  { name: 'author', local: '/fr/about/', baseline: 'https://theodore-aspeel.github.io/artnouveau-site/fr/about/' },
  {
    name: 'article-coilliot',
    local: '/fr/articles/maison-coilliot-lille-hector-guimard/',
    baseline: 'https://theodore-aspeel.github.io/artnouveau-site/fr/articles/maison-coilliot-lille-hector-guimard/',
  },
];

function columnCount(value) {
  return value.split(' ').filter(Boolean).length;
}

async function revealAndWaitForImages(page, selector) {
  const images = page.locator(selector);
  const count = await images.count();

  for (let index = 0; index < count; index += 1) {
    await images.nth(index).scrollIntoViewIfNeeded();
  }

  await expect.poll(
    () => images.evaluateAll((items) => items.every((image) => image.complete && image.naturalWidth > 0)),
    { timeout: 15_000 },
  ).toBeTruthy();
}

test('D1 produit la série comparative avant et après', async ({ page }, testInfo) => {
  test.setTimeout(90_000);
  const viewport = VIEWPORT_LABELS[testInfo.project.name] || testInfo.project.name;

  for (const reviewPage of REVIEW_PAGES) {
    let baselineResponse;
    try {
      baselineResponse = await page.goto(reviewPage.baseline, {
        waitUntil: 'domcontentloaded',
        timeout: 15_000,
      });
    } catch (error) {
      await testInfo.attach(`before-${reviewPage.name}-${viewport}-unavailable`, {
        body: String(error),
        contentType: 'text/plain',
      });
    }

    if (baselineResponse?.ok()) {
      await page.waitForTimeout(1_000);
      await testInfo.attach(`before-${reviewPage.name}-${viewport}`, {
        body: await page.screenshot({ fullPage: true }),
        contentType: 'image/png',
      });
    } else if (baselineResponse) {
      await testInfo.attach(`before-${reviewPage.name}-${viewport}-unavailable`, {
        body: `HTTP ${baselineResponse.status()}`,
        contentType: 'text/plain',
      });
    }

    const response = await page.goto(reviewPage.local, { waitUntil: 'networkidle' });
    expect(response?.ok()).toBeTruthy();
    await expect(page.locator('h1')).toBeVisible();

    if (reviewPage.name === 'author') {
      await page.locator('#portfolio').scrollIntoViewIfNeeded();
      await revealAndWaitForImages(page, '.about-studio-portfolio__grid img');
    }

    const overflow = await page.evaluate(() => ({
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
    }));
    expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth + 1);

    await testInfo.attach(`after-${reviewPage.name}-${viewport}`, {
      body: await page.screenshot({ fullPage: true }),
      contentType: 'image/png',
    });
  }

  await page.goto('/fr/about/', { waitUntil: 'networkidle' });
  await expect(page.locator('#portfolio')).toBeVisible();
  const layout = await page.evaluate(() => ({
    portfolio: getComputedStyle(document.querySelector('.about-studio-portfolio__grid')).gridTemplateColumns,
    imagesLoaded: [...document.querySelectorAll('.about-studio-portfolio__grid img')]
      .every((image) => image.complete && image.naturalWidth > 0),
  }));
  expect(columnCount(layout.portfolio)).toBe(EXPECTED_PORTFOLIO_COLUMNS[testInfo.project.name]);
  expect(layout.imagesLoaded).toBeTruthy();
  const responsiveSources = page.locator('.about-studio-portfolio__grid picture source[data-responsive-image-format]');
  await expect(responsiveSources.first()).toHaveAttribute('srcset', /assets\/generated-images\//);
  expect(await responsiveSources.count()).toBeGreaterThanOrEqual(2);
});
