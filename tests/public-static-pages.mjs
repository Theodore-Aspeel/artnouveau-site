import assert from 'node:assert/strict';
import fs from 'node:fs';

const EXPECTED_PAGES = [
  ['fr', 'home', 'dist/fr/index.html', 'Regarder d\u2019abord. Nommer ensuite.'],
  ['en', 'home', 'dist/en/index.html', 'Look first. Name later.'],
  ['nl', 'home', 'dist/nl/index.html', 'Eerst kijken. Daarna benoemen.'],
  ['fr', 'about', 'dist/fr/about/index.html', 'Partir du d\u00e9tail, puis revenir \u00e0 la ville'],
  ['en', 'about', 'dist/en/about/index.html', 'Start from the detail, then return to the city'],
  ['nl', 'about', 'dist/nl/about/index.html', 'Van het detail vertrekken en daarna terugkeren naar de stad'],
  ['fr', 'mentions', 'dist/fr/mentions/index.html', 'Un cadre simple, lisible, sans appareil inutile'],
  ['en', 'mentions', 'dist/en/mentions/index.html', 'A simple, readable frame, without unnecessary apparatus'],
  ['nl', 'mentions', 'dist/nl/mentions/index.html', 'Een eenvoudig en leesbaar kader, zonder overbodig apparaat'],
];

for (const [locale, routeName, filePath, expectedText] of EXPECTED_PAGES) {
  assert.ok(fs.existsSync(filePath), `${filePath} should be generated`);

  const html = fs.readFileSync(filePath, 'utf8');
  assert.match(html, new RegExp(`<html lang="${locale}">`), `${filePath} should set the HTML language`);
  assert.ok(html.includes(expectedText), `${filePath} should include localized ${locale} ${routeName} content`);
  assert.doesNotMatch(html, /previewLocale=/, `${filePath} should not use previewLocale links`);
}

assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /data-article-data-url="\.\.\/data\/articles\.json"/);
assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /data-asset-base="\.\.\/"/);
assert.match(fs.readFileSync('dist/fr/about/index.html', 'utf8'), /href="\/fr\/"/);
assert.match(fs.readFileSync('dist/en/about/index.html', 'utf8'), /href="\/en\/mentions\/"/);
assert.match(fs.readFileSync('dist/nl/mentions/index.html', 'utf8'), /href="\/nl\/about\/"/);
