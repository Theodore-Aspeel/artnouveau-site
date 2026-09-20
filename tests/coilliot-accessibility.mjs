import assert from 'node:assert/strict';
import fs from 'node:fs';

const data = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const article = data.articles.find((item) => item.slug === 'maison-coilliot-lille-hector-guimard');

assert.ok(article, 'Maison Coilliot pilot should exist');
assert.equal(article.status, 'draft', 'Maison Coilliot must remain a draft');
assert.equal(
  article.media?.hero?.src,
  'assets/images/articles/maison-coilliot-facade-complete-christophe-aspel.jpg',
  'Maison Coilliot should use the selected full-facade hero photograph'
);

const supportImages = article.media?.support || [];
assert.equal(supportImages.length, 2, 'Maison Coilliot pilot should keep its two support images');

assert.deepEqual(
  supportImages.map((image) => image.src),
  [
    'assets/images/articles/maison-coilliot-enseigne-signature-hector-guimard.jpg',
    'assets/images/articles/maison-coilliot-enseigne-ceramique-lave-emaillee.jpg',
  ],
  'Maison Coilliot should use only its selected support photographs'
);

for (const locale of ['fr', 'en', 'nl']) {
  const alternatives = article.content?.[locale]?.media?.support_alt || [];
  assert.equal(
    alternatives.length,
    supportImages.length,
    `Maison Coilliot ${locale} should describe every support image`
  );
  alternatives.forEach((alternative, index) => {
    assert.ok(
      typeof alternative === 'string' && alternative.trim().length >= 40,
      `Maison Coilliot ${locale} support image ${index + 1} should have a useful alternative`
    );
  });
}
