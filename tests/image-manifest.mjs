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
class FakeElement {
  constructor(tagName) {
    this.tagName = tagName.toUpperCase();
    this.children = [];
    this.parentNode = null;
    this.attributes = new Map();
    this.src = '';
  }

  setAttribute(name, value) {
    this.attributes.set(name, value);
  }

  getAttribute(name) {
    return this.attributes.get(name) || '';
  }

  appendChild(child) {
    if (child.parentNode) {
      child.parentNode.children = child.parentNode.children.filter((item) => item !== child);
    }
    child.parentNode = this;
    this.children.push(child);
    return child;
  }

  insertBefore(child, reference) {
    if (child.parentNode) {
      child.parentNode.children = child.parentNode.children.filter((item) => item !== child);
    }
    child.parentNode = this;
    const index = this.children.indexOf(reference);
    if (index >= 0) {
      this.children.splice(index, 0, child);
    } else {
      this.children.push(child);
    }
    return child;
  }

  querySelectorAll(selector) {
    if (selector !== 'source[data-responsive-image-format]') return [];
    return this.children.filter((child) => child.tagName === 'SOURCE' && child.attributes.has('data-responsive-image-format'));
  }

  remove() {
    if (!this.parentNode) return;
    this.parentNode.children = this.parentNode.children.filter((item) => item !== this);
    this.parentNode = null;
  }
}

const context = {
  window: {
    location: {
      href: 'https://example.test/fr/articles/demo/',
    },
    document: {
      createElement(tagName) {
        return new FakeElement(tagName);
      },
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
  version: 2,
  images: [
    {
      source_path: 'assets/images/articles/demo.png',
      source: {
        format: 'png',
        width: 1200,
        height: 800,
      },
      variants: [
        {
          format: 'png',
          width: 960,
          height: 640,
          dist_path: 'assets/generated-images/articles/demo-960w.png',
        },
        {
          format: 'webp',
          width: 960,
          height: 640,
          dist_path: 'assets/generated-images/articles/demo-960w.webp',
        },
        {
          format: 'webp',
          width: 640,
          height: 427,
          dist_path: 'assets/generated-images/articles/demo-640w.webp',
        },
        {
          format: 'avif',
          width: 960,
          height: 640,
          dist_path: 'assets/generated-images/articles/demo-960w.avif',
        },
        {
          format: 'png',
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

const webpAttrs = imageManifest.responsiveImageAttributes('assets/images/articles/demo.png', {
  basePath: '../../../',
  format: 'webp',
});

assert.equal(
  webpAttrs.srcset,
  'https://example.test/assets/generated-images/articles/demo-640w.webp 640w, https://example.test/assets/generated-images/articles/demo-960w.webp 960w',
  'srcset can be requested for a modern format when a picture-based renderer is added'
);

const pictureAttrs = imageManifest.responsivePictureAttributes('assets/images/articles/demo.png', {
  basePath: '../../../',
  sizes: '(min-width: 1100px) 42vw, 100vw',
});

assert.deepEqual(
  Array.from(pictureAttrs.sources, (source) => source.type),
  ['image/avif', 'image/webp'],
  'picture sources should prefer AVIF, then WebP with typed MIME attributes'
);
assert.equal(
  pictureAttrs.sources[0].srcset,
  'https://example.test/assets/generated-images/articles/demo-960w.avif 960w',
  'AVIF source should only include available AVIF variants'
);
assert.equal(
  pictureAttrs.sources[1].srcset,
  'https://example.test/assets/generated-images/articles/demo-640w.webp 640w, https://example.test/assets/generated-images/articles/demo-960w.webp 960w',
  'WebP source should include available WebP variants ordered by width'
);
assert.equal(
  pictureAttrs.img.srcset,
  attrs.srcset,
  'picture img fallback should keep source-format srcset'
);

const defaultVariants = imageManifest.getVariants('assets/images/articles/demo.png');
assert.deepEqual(
  Array.from(defaultVariants, (variant) => variant.format),
  ['png', 'png'],
  'default variants should stay in the source format for safe img fallback'
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

const figure = new FakeElement('figure');
const pictureImg = new FakeElement('img');
figure.appendChild(pictureImg);
const appliedPicture = imageManifest.applyResponsivePicture(pictureImg, 'assets/images/articles/demo.png', {
  basePath: '../../../',
  sizes: '100vw',
});

assert.equal(appliedPicture.element.tagName, 'PICTURE');
assert.equal(figure.children[0].tagName, 'PICTURE');
assert.deepEqual(
  Array.from(appliedPicture.element.children, (child) => child.tagName),
  ['SOURCE', 'SOURCE', 'IMG'],
  'applyResponsivePicture should wrap existing images with typed sources before the fallback img'
);
assert.equal(appliedPicture.element.children[0].getAttribute('type'), 'image/avif');
assert.equal(appliedPicture.element.children[1].getAttribute('type'), 'image/webp');
assert.equal(pictureImg.parentNode, appliedPicture.element);

const fallback = imageManifest.responsiveImageAttributes('assets/images/articles/missing.png', {
  basePath: '../../../',
  sizes: '100vw',
});

assert.equal(fallback.src, 'https://example.test/assets/images/articles/missing.png');
assert.equal(fallback.srcset, '');
assert.equal(fallback.width, '');
assert.equal(fallback.height, '');
