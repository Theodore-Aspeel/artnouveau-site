import { expect, test } from '@playwright/test';

const ORIGIN = 'https://artnouveauetdeco.com';
const COILLIOT_PATH = '/fr/articles/maison-coilliot-lille-hector-guimard/';

const pages = [
  { name: 'accueil FR', path: '/fr/', canonical: '/fr/' },
  { name: 'accueil EN', path: '/en/', canonical: '/en/' },
  { name: 'Maison Coilliot FR', path: COILLIOT_PATH, canonical: COILLIOT_PATH },
  { name: 'about FR', path: '/fr/about/', canonical: '/fr/about/' },
];

for (const pageCase of pages) {
  test(`${pageCase.name} rend sans débordement horizontal`, async ({ page }, testInfo) => {
    const response = await page.goto(pageCase.path, { waitUntil: 'networkidle' });

    expect(response?.ok()).toBeTruthy();
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute(
      'href',
      `${ORIGIN}${pageCase.canonical}`,
    );

    const overflow = await page.evaluate(() => ({
      clientWidth: document.documentElement.clientWidth,
      scrollWidth: document.documentElement.scrollWidth,
    }));
    expect(overflow.scrollWidth).toBeLessThanOrEqual(overflow.clientWidth + 1);

    const nav = page.locator('#main-menu');
    const toggle = page.locator('.site-nav__toggle');
    if (testInfo.project.name === 'chromium-mobile-390') {
      await expect(toggle).toBeVisible();
      await toggle.click();
      await expect(toggle).toHaveAttribute('aria-expanded', 'true');
      await expect(nav).toBeVisible();
    } else {
      await expect(nav).toBeVisible();
    }
  });
}

test('Maison Coilliot conserve son hero et son noindex', async ({ page }) => {
  await page.goto(COILLIOT_PATH, { waitUntil: 'networkidle' });

  await expect(page.locator('.article-intake__image')).toBeVisible();
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex,follow');
});

test('les pages statiques publiques restent indexables', async ({ page }) => {
  for (const path of ['/fr/', '/fr/about/']) {
    await page.goto(path, { waitUntil: 'networkidle' });
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'index,follow');
  }
});

test('captures de revue sur les vues stables candidates', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name === 'chromium-tablet-768', 'Le lot demande quatre captures 390/desktop.');

  const viewport = testInfo.project.name === 'chromium-mobile-390' ? '390' : 'desktop';
  for (const [name, path] of [['accueil', '/fr/'], ['coilliot', COILLIOT_PATH]]) {
    await page.goto(path, { waitUntil: 'networkidle' });
    await testInfo.attach(`${name}-${viewport}`, {
      body: await page.screenshot({ fullPage: true }),
      contentType: 'image/png',
    });
  }
});
