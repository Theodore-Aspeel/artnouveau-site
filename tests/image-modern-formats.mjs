import assert from 'node:assert/strict';
import fs from 'node:fs';

const imageManifestHelper = fs.readFileSync('src/assets/scripts/image-manifest.js', 'utf8');
const galleryScript = fs.readFileSync('src/assets/scripts/gallery.js', 'utf8');
const articleTemplate = fs.readFileSync('src/assets/scripts/article-template.js', 'utf8');

assert.match(
  imageManifestHelper,
  /function responsivePictureAttributes/,
  'image manifest helper should expose picture attributes for modern formats'
);

assert.match(
  imageManifestHelper,
  /\['avif', 'webp'\]/,
  'picture sources should be ordered AVIF first, then WebP'
);

assert.match(
  imageManifestHelper,
  /if \(normalized === 'avif'\) return 'image\/avif';[\s\S]*if \(normalized === 'webp'\) return 'image\/webp';/,
  'modern picture sources should use correct MIME types'
);

assert.match(
  imageManifestHelper,
  /function applyResponsivePicture/,
  'image manifest helper should provide one reusable picture abstraction'
);

assert.match(
  imageManifestHelper,
  /querySelectorAll\('img\[data-responsive-image-source\]'\)[\s\S]*applyResponsivePicture/,
  'declarative public images should be upgraded to picture rendering through the helper'
);

assert.match(
  galleryScript,
  /typeof imageManifest\.applyResponsivePicture === 'function'/,
  'gallery and curated card rendering should use the picture helper when available'
);

assert.match(
  articleTemplate,
  /typeof imageManifest\.applyResponsivePicture === 'function'/,
  'article primary and support image rendering should use the picture helper when available'
);
