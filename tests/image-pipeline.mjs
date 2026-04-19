import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {
  collectArticleImagePaths,
  collectSiteImagePaths,
  IMAGE_MANIFEST_PATH,
} from '../scripts/image-pipeline.mjs';

const articleData = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const expectedArticleImages = collectArticleImagePaths(articleData.articles);
const expectedSiteImages = await collectSiteImagePaths(process.cwd(), [
  'src/pages/index.html',
  'src/pages/about.html',
  'src/pages/mentions.html',
  'src/pages/article-redirect.html',
]);
const expectedImages = [...new Set([...expectedArticleImages, ...expectedSiteImages])]
  .sort((left, right) => left.localeCompare(right));

assert.deepEqual(
  expectedSiteImages,
  [
    'assets/images/site/author/author-portrait-2026.jpg',
    'assets/images/site/saint-gilles-brussels.png',
  ],
  'site image collection should stay limited to images referenced by public pages'
);

const manifestPath = path.join('dist', IMAGE_MANIFEST_PATH);
assert.ok(fs.existsSync(manifestPath), 'image manifest should be generated in dist');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
assert.equal(manifest.version, 2, 'manifest should expose its schema version');
assert.equal(manifest.generated_dir, 'assets/generated-images', 'manifest should expose generated image directory');
assert.deepEqual(
  manifest.generated_formats,
  ['source', 'webp', 'avif'],
  'manifest should expose the generated output format families'
);

const manifestSources = manifest.images
  .map((image) => image.source_path)
  .sort((left, right) => left.localeCompare(right));

assert.deepEqual(manifestSources, expectedImages, 'manifest should include exactly the published runtime images');

for (const image of manifest.images) {
  assert.ok(image.source_path.startsWith('assets/images/'), `${image.source_path} should be a runtime image path`);
  assert.ok(Number.isInteger(image.source.width) && image.source.width > 0, `${image.source_path} should record source width`);
  assert.ok(Number.isInteger(image.source.height) && image.source.height > 0, `${image.source_path} should record source height`);
  assert.ok(Number.isInteger(image.source.bytes) && image.source.bytes > 0, `${image.source_path} should record source byte size`);
  assert.ok(image.source.format, `${image.source_path} should record source format`);
  assert.deepEqual(
    [...new Set(image.variants.map((variant) => variant.format))].sort(),
    ['avif', image.source.format, 'webp'].sort(),
    `${image.source_path} should generate source, WebP and AVIF variants`
  );
  assert.ok(Array.isArray(image.variants) && image.variants.length > 0, `${image.source_path} should have generated variants`);

  for (const variant of image.variants) {
    assert.ok(variant.dist_path.startsWith('assets/generated-images/'), `${image.source_path} variant should stay under generated-images`);
    assert.ok(fs.existsSync(path.join('dist', variant.dist_path)), `${variant.dist_path} should exist`);
    assert.ok(Number.isInteger(variant.width) && variant.width > 0, `${variant.dist_path} should record width`);
    assert.ok(Number.isInteger(variant.height) && variant.height > 0, `${variant.dist_path} should record height`);
    assert.ok(Number.isInteger(variant.bytes) && variant.bytes > 0, `${variant.dist_path} should record byte size`);
    assert.ok(variant.format, `${variant.dist_path} should record format`);
  }
}
