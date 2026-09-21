import { expect, test } from '@playwright/test';

const ORIGIN = 'https://artnouveauetdeco.com';
const COILLIOT_PATH = '/fr/articles/maison-coilliot-lille-hector-guimard/';
const COILLIOT_SLUG = 'maison-coilliot-lille-hector-guimard';

const pages = [
  { name: 'accueil FR', path: '/fr/', canonical: '/fr/' },
  { name: 'accueil EN', path: '/en/', canonical: '/en/' },
  { name: 'Maison Coilliot FR', path: COILLIOT_PATH, canonical: COILLIOT_PATH },
  { name: 'about FR', path: '/fr/about/', canonical: '/fr/about/' },
  { name: 'about EN', path: '/en/about/', canonical: '/en/about/' },
  { name: 'about NL', path: '/nl/about/', canonical: '/nl/about/' },
];

const authorPathways = [
  { locale: 'fr', aria: 'Liens vers le portfolio et le contact de l’auteur', portfolio: 'Voir le portfolio', contact: 'Contacter' },
  { locale: 'en', aria: 'Links to the author’s portfolio and contact', portfolio: 'View the portfolio', contact: 'Contact' },
  { locale: 'nl', aria: 'Links naar het portfolio en het contact van de auteur', portfolio: 'Bekijk het portfolio', contact: 'Contact' },
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
    if (await toggle.isVisible()) {
      await expect(toggle).toBeVisible();
      await toggle.click();
      await expect(toggle).toHaveAttribute('aria-expanded', 'true');
      await expect(nav).toBeVisible();
    } else {
      await expect(nav).toBeVisible();
    }
  });
}

test('la preview legacy conserve la langue dans les liens auteur', async ({ page }) => {
  await page.goto(`/article.html?slug=${COILLIOT_SLUG}&previewLocale=en`, { waitUntil: 'networkidle' });

  await expect(page.locator('.article-tpl__byline-link')).toHaveAttribute('href', 'about.html?previewLocale=en');
  const links = page.locator('.article-tpl__author-links');
  await expect(links.getByText('View the portfolio', { exact: true })).toHaveAttribute('href', 'about.html?previewLocale=en#portfolio');
  await expect(links.getByText('Contact', { exact: true })).toHaveAttribute('href', 'about.html?previewLocale=en#contact');
});

test('Maison Coilliot conserve son hero et son noindex', async ({ page }) => {
  await page.goto(COILLIOT_PATH, { waitUntil: 'networkidle' });

  await expect(page.locator('.article-intake__image')).toBeVisible();
  await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', 'noindex,follow');
});

for (const pathway of authorPathways) {
  test(`Maison Coilliot expose les parcours auteur en ${pathway.locale}`, async ({ page }) => {
    const aboutPath = `/${pathway.locale}/about/`;
    await page.goto(`/${pathway.locale}/articles/${COILLIOT_SLUG}/`, { waitUntil: 'networkidle' });

    await expect(page.locator('.article-tpl__byline-link')).toHaveAttribute('href', aboutPath);
    const links = page.locator('.article-tpl__author-links');
    await expect(links).toHaveAttribute('aria-label', pathway.aria);
    await expect(links.getByText(pathway.portfolio, { exact: true })).toHaveAttribute('href', `${aboutPath}#portfolio`);
    await expect(links.getByText(pathway.contact, { exact: true })).toHaveAttribute('href', `${aboutPath}#contact`);
  });
}

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
