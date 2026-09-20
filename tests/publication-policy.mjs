import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { collectArticleImagePaths } from '../scripts/image-pipeline.mjs';
import {
  articleRobotsDirective,
  PUBLICATION_MODES,
  resolvePublicationMode,
  selectIndexableArticles,
  selectPublicArticles,
} from '../scripts/publication-policy.mjs';

assert.equal(resolvePublicationMode(), PUBLICATION_MODES.LEGACY_VISIBLE);
assert.equal(resolvePublicationMode('published-only'), PUBLICATION_MODES.PUBLISHED_ONLY);
assert.throws(
  () => resolvePublicationMode('drafts-too'),
  /PUBLICATION_MODE must be/,
  'unknown publication modes must fail closed'
);

const fixture = [
  { slug: 'draft-demo', status: 'draft' },
  { slug: 'published-demo', status: 'published' },
  { slug: 'ready-demo', status: 'ready' },
];

assert.deepEqual(
  selectPublicArticles(fixture, PUBLICATION_MODES.LEGACY_VISIBLE).map((article) => article.slug),
  ['draft-demo', 'published-demo', 'ready-demo']
);
assert.deepEqual(
  selectPublicArticles(fixture, PUBLICATION_MODES.PUBLISHED_ONLY).map((article) => article.slug),
  ['published-demo']
);
assert.deepEqual(
  selectIndexableArticles(fixture).map((article) => article.slug),
  ['published-demo'],
  'only published articles may be submitted through the sitemap'
);
assert.equal(articleRobotsDirective(fixture[0]), 'noindex,follow');
assert.equal(articleRobotsDirective(fixture[1]), 'index,follow');
assert.equal(articleRobotsDirective(fixture[2]), 'noindex,follow');

const mode = resolvePublicationMode(process.env.PUBLICATION_MODE);
const sourceData = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const publicData = JSON.parse(fs.readFileSync('dist/data/articles.json', 'utf8'));
const expectedArticles = selectPublicArticles(sourceData.articles, mode);
const expectedSlugs = expectedArticles.map((article) => article.slug);
const expectedIndexableSlugs = selectIndexableArticles(expectedArticles).map((article) => article.slug);
const publicSlugs = publicData.articles.map((article) => article.slug);

assert.deepEqual(publicSlugs, expectedSlugs, 'public article data must follow the selected policy');
assert.ok(sourceData.articles.length > 0, 'the source corpus must remain available');
assert.ok(
  sourceData.articles.some((article) => article.status === 'draft'),
  'the strict-profile regression must exercise at least one draft article'
);

const sitemap = fs.readFileSync('dist/sitemap.xml', 'utf8');
for (const article of sourceData.articles) {
  const included = expectedSlugs.includes(article.slug);
  for (const locale of ['fr', 'en', 'nl']) {
    const articlePath = path.join('dist', locale, 'articles', article.slug, 'index.html');
    assert.equal(
      fs.existsSync(articlePath),
      included,
      `${article.slug} route visibility must follow ${mode}`
    );
  }
  assert.equal(
    sitemap.includes(`/articles/${article.slug}/`),
    expectedIndexableSlugs.includes(article.slug),
    `${article.slug} sitemap visibility must follow its publication status in ${mode}`
  );

  if (included) {
    for (const locale of ['fr', 'en', 'nl']) {
      const articlePath = path.join('dist', locale, 'articles', article.slug, 'index.html');
      const articleHtml = fs.readFileSync(articlePath, 'utf8');
      assert.ok(
        articleHtml.includes(`<meta name="robots" content="${articleRobotsDirective(article)}">`),
        `${article.slug} robots directive must follow its publication status in ${mode}`
      );
    }
  }
}

const manifest = JSON.parse(fs.readFileSync('dist/assets/generated-images/manifest.json', 'utf8'));
const manifestSources = new Set(manifest.images.map((image) => image.source_path));
const expectedArticleImages = new Set(collectArticleImagePaths(expectedArticles));
const allArticleImages = collectArticleImagePaths(sourceData.articles);

for (const imagePath of allArticleImages) {
  assert.equal(
    manifestSources.has(imagePath),
    expectedArticleImages.has(imagePath),
    `${imagePath} generated-image visibility must follow ${mode}`
  );
}
