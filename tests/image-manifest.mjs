import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const attributes = new Map();
const img = {
  src: '',
  setAttribute(name, value) {
    attributes.set(name, value);
  },
};
const context = {
  window: {
    location: {
      href: 'https://example.test/fr/articles/demo/',
    },
  },
  URL,
  Map,
};

vm.runInNewContext(fs.readFileSync('src/assets/scripts/image-manifest.js', 'utf8'), context);

const imageManifest = context.window.SiteImageManifest;

assert.ok(imageManifest, 'image manifest helper should attach to window');
assert.equal(
  imageManifest.normalizeRuntimePath('../../assets/images/articles/demo.png'),
  'assets/images/articles/demo.png',
  'runtime paths should normalize to manifest source keys'
);

imageManifest.setManifest({
  version: 1,
  images: [
    {
      source_path: 'assets/images/articles/demo.png',
      source: {
        width: 1200,
        height: 800,
      },
      variants: [
        {
          width: 960,
          height: 640,
          dist_path: 'assets/generated-images/articles/demo-960w.png',
        },
        {
          width: 640,
          height: 427,
          dist_path: 'assets/generated-images/articles/demo-640w.png',
        },
      ],
    },
  ],
});

const attrs = imageManifest.responsiveImageAttributes('assets/images/articles/demo.png', {
  basePath: '../../../',
  sizes: '(min-width: 1100px) 42vw, 100vw',
});

assert.equal(attrs.src, 'https://example.test/assets/images/articles/demo.png');
assert.equal(attrs.width, '1200');
assert.equal(attrs.height, '800');
assert.equal(attrs.sizes, '(min-width: 1100px) 42vw, 100vw');
assert.equal(
  attrs.srcset,
  'https://example.test/assets/generated-images/articles/demo-640w.png 640w, https://example.test/assets/generated-images/articles/demo-960w.png 960w',
  'srcset should use generated variants ordered by width'
);

imageManifest.applyResponsiveImage(img, 'assets/images/articles/demo.png', {
  basePath: '../../../',
  sizes: '100vw',
});

assert.equal(img.src, 'https://example.test/assets/images/articles/demo.png');
assert.equal(attributes.get('srcset'), attrs.srcset);
assert.equal(attributes.get('sizes'), '100vw');
assert.equal(attributes.get('width'), '1200');
assert.equal(attributes.get('height'), '800');

const fallback = imageManifest.responsiveImageAttributes('assets/images/articles/missing.png', {
  basePath: '../../../',
  sizes: '100vw',
});

assert.equal(fallback.src, 'https://example.test/assets/images/articles/missing.png');
assert.equal(fallback.srcset, '');
assert.equal(fallback.width, '');
assert.equal(fallback.height, '');
