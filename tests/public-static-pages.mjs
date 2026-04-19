import assert from 'node:assert/strict';
import fs from 'node:fs';

const articleData = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const publicLocales = ['fr', 'en', 'nl'];

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

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll('"', '&quot;');
}

function localeContent(article, locale) {
  return article.content?.[locale] || article.content?.fr || {};
}

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

for (const locale of publicLocales) {
  for (const article of articleData.articles) {
    const filePath = `dist/${locale}/articles/${article.slug}/index.html`;
    assert.ok(fs.existsSync(filePath), `${filePath} should be generated`);
  }
}

const sampleArticle = articleData.articles.find((article) => article.slug === 'maison-coilliot-lille-hector-guimard');
assert.ok(sampleArticle, 'sample article should exist');

for (const locale of publicLocales) {
  const filePath = `dist/${locale}/articles/${sampleArticle.slug}/index.html`;
  const html = fs.readFileSync(filePath, 'utf8');
  const content = localeContent(sampleArticle, locale);
  const expectedTitle = `${content.title} · Art Nouveau et Art Déco`;
  const expectedDescription = content.seo.meta_description;

  assert.match(html, new RegExp(`<html lang="${locale}">`), `${filePath} should set article HTML language`);
  assert.ok(html.includes(`<title id="page-title">${escapeHtml(expectedTitle)}</title>`), `${filePath} should include final title`);
  assert.ok(
    html.includes(`<meta id="page-description" name="description" content="${escapeAttribute(expectedDescription)}">`),
    `${filePath} should include final meta description`
  );
  assert.ok(
    html.includes(`<meta id="og-title" property="og:title" content="${escapeAttribute(expectedTitle)}">`),
    `${filePath} should include final og:title`
  );
  assert.ok(
    html.includes(`<meta id="og-description" property="og:description" content="${escapeAttribute(expectedDescription)}">`),
    `${filePath} should include final og:description`
  );
  assert.ok(
    html.includes(`<meta id="twitter-title" name="twitter:title" content="${escapeAttribute(expectedTitle)}">`),
    `${filePath} should include final twitter:title`
  );
  assert.ok(
    html.includes(`<meta id="twitter-description" name="twitter:description" content="${escapeAttribute(expectedDescription)}">`),
    `${filePath} should include final twitter:description`
  );
  assert.match(html, /<meta property="og:image" content="\.\.\/\.\.\/\.\.\/assets\/images\/articles\/maison-coilliot-lille-hector-guimard\.png">/);
  assert.ok(html.includes(`data-article-slug="${sampleArticle.slug}"`), `${filePath} should pass the slug without query parameters`);
  assert.ok(html.includes(`href="/${locale}/articles/${sampleArticle.slug}/"`), `${filePath} should link to its public route`);
  assert.doesNotMatch(html, /Chargement/, `${filePath} should not keep loading SEO title text`);
  assert.doesNotMatch(html, /previewLocale=/, `${filePath} should not use previewLocale links`);
}
