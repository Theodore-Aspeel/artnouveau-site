import assert from 'node:assert/strict';
import fs from 'node:fs';

const data = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const completed = [
  'maison-coilliot-lille-hector-guimard',
  'lhuitriere-lille-art-deco',
  'maison-des-hiboux-saint-gilles',
  'maison-strauven-avenue-van-cutsem-2729-tournai-1904',
  'den-tijd-le-temps-anvers'
];

for (const slug of completed) {
  const article = data.articles.find((item) => item.slug === slug);
  assert.ok(article, `${slug} should exist`);

  const supportImages = article.media?.support || [];
  assert.ok(supportImages.length > 0, `${slug} should keep its support images`);

  for (const locale of ['fr', 'en', 'nl']) {
    const alternatives = article.content?.[locale]?.media?.support_alt || [];
    assert.equal(
      alternatives.length,
      supportImages.length,
      `${slug} ${locale} should describe every support image`
    );
    alternatives.forEach((alternative, index) => {
      assert.ok(
        typeof alternative === 'string' && alternative.trim().length >= 40,
        `${slug} ${locale} support image ${index + 1} should have a useful alternative`
      );
    });
  }
}
