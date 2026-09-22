import assert from 'node:assert/strict';
import fs from 'node:fs';

const homeHtml = fs.readFileSync('src/pages/index.html', 'utf8');
const articleTemplate = fs.readFileSync('src/assets/scripts/article-template.js', 'utf8');
const galleryScript = fs.readFileSync('src/assets/scripts/gallery.js', 'utf8');

assert.match(
  homeHtml,
  /class="mag-lead__media mag-private-slot" id="pilot-villino-hero"/,
  'home should expose a stable private-media slot for the local lead photograph'
);
assert.doesNotMatch(homeHtml, /src="[^"]*(?:\.private-media|private-media)\//, 'private preview media must not enter public image sources');
assert.match(homeHtml, /class="mag-feature__primary"[\s\S]*?<img[^>]+loading="lazy"[^>]+decoding="async"/, 'public homepage feature images should load lazily');

assert.match(
  articleTemplate,
  /image\.loading = 'eager';\s*image\.setAttribute\('fetchpriority', 'high'\);\s*image\.setAttribute\('decoding', 'async'\);/,
  'article primary image should be explicit LCP candidate: eager, high priority, async decoding'
);

assert.match(
  articleTemplate,
  /applyArticleImageAttributes\(im, entry\.src,[\s\S]*?im\.loading = 'lazy';\s*im\.setAttribute\('decoding', 'async'\);/,
  'article support images should keep responsive manifest attributes while loading lazily'
);

assert.doesNotMatch(
  galleryScript,
  /fetchPriority = 'high'/,
  'gallery and editorial cards should not be marked as high-priority images'
);

const lazyCardImages = galleryScript.match(/img\.loading = 'lazy';\s*img\.setAttribute\('decoding', 'async'\);/g) || [];
assert.ok(
  lazyCardImages.length >= 2,
  'gallery and curated card images should load lazily with async decoding'
);
