import assert from 'node:assert/strict';
import fs from 'node:fs';

const plausibleDomain = process.env.PLAUSIBLE_DOMAIN || '';
const expectedScript = plausibleDomain
  ? `<script defer data-domain="${plausibleDomain}" src="https://plausible.io/js/script.js"></script>`
  : '';

const publicPages = [
  'dist/fr/index.html',
  'dist/en/about/index.html',
  'dist/nl/mentions/index.html',
  'dist/fr/articles/maison-coilliot-lille-hector-guimard/index.html',
];

const compatibilityPages = [
  'dist/index.html',
  'dist/about.html',
  'dist/mentions.html',
  'dist/article.html',
  'dist/articles/template.html',
];

for (const filePath of publicPages) {
  assert.ok(fs.existsSync(filePath), `${filePath} should be generated`);
  const html = fs.readFileSync(filePath, 'utf8');

  if (expectedScript) {
    assert.ok(html.includes(expectedScript), `${filePath} should include the Plausible analytics script`);
  } else {
    assert.doesNotMatch(html, /plausible\.io\/js\/script\.js/, `${filePath} should not include analytics by default`);
  }
}

for (const filePath of compatibilityPages) {
  assert.ok(fs.existsSync(filePath), `${filePath} should be generated`);
  const html = fs.readFileSync(filePath, 'utf8');
  assert.doesNotMatch(html, /plausible\.io\/js\/script\.js/, `${filePath} should not include public analytics`);
}
