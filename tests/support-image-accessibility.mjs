import assert from 'node:assert/strict';
import fs from 'node:fs';

const data = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const articlesWithSupportImages = data.articles.filter(
  (article) => (article.media?.support || []).length > 0
);

for (const article of articlesWithSupportImages) {
  const { slug } = article;
  const supportImages = article.media?.support || [];

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
