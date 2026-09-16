import assert from 'node:assert/strict';
import fs from 'node:fs';

const data = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const article = data.articles.find((item) => item.slug === 'maison-coilliot-lille-hector-guimard');

assert.ok(article, 'Maison Coilliot pilot should exist');

const supportImages = article.media?.support || [];
assert.equal(supportImages.length, 2, 'Maison Coilliot pilot should keep its two support images');

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
