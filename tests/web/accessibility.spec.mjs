import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const pages = [
  ['accueil FR', '/fr/'],
  ['Maison Coilliot FR', '/fr/articles/maison-coilliot-lille-hector-guimard/'],
  ['about FR', '/fr/about/'],
];

for (const [name, path] of pages) {
  test(`${name} n'a aucune violation axe critical ou serious`, async ({ page }, testInfo) => {
    await page.goto(path, { waitUntil: 'networkidle' });

    const results = await new AxeBuilder({ page }).analyze();
    const blocking = results.violations.filter(({ impact }) => (
      impact === 'critical' || impact === 'serious'
    ));
    const moderate = results.violations.filter(({ impact }) => impact === 'moderate');

    await testInfo.attach('axe-summary', {
      body: JSON.stringify({ blocking, moderate }, null, 2),
      contentType: 'application/json',
    });
    expect(blocking, JSON.stringify(blocking, null, 2)).toEqual([]);
  });
}
