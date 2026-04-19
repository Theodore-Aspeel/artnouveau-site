(function attachImageManifest(global) {
  'use strict';

  const DEFAULT_MANIFEST_PATH = 'assets/generated-images/manifest.json';
  let manifestPromise = null;
  let imageIndex = new Map();

  function normalizeText(value) {
    return typeof value === 'string' ? value.trim() : '';
  }

  function normalizeRuntimePath(value) {
    const text = normalizeText(value).replaceAll('\\', '/');
    if (!text) return '';

    const assetsIndex = text.indexOf('assets/');
    if (assetsIndex >= 0) {
      return text.slice(assetsIndex).replace(/^\/+/, '');
    }

    return text
      .replace(/^(\.\/)+/, '')
      .replace(/^(\.\.\/)+/, '')
      .replace(/^\/+/, '');
  }

  function isExternalPath(value) {
    return /^(?:https?:)?\/\//i.test(value) || value.startsWith('data:');
  }

  function resolveRuntimePath(runtimePath, basePath) {
    const normalized = normalizeRuntimePath(runtimePath);
    if (!normalized || isExternalPath(normalized) || normalized.startsWith('/')) {
      return normalized;
    }

    return (basePath || '') + normalized;
  }

  function absoluteRuntimeUrl(runtimePath, basePath) {
    const resolved = resolveRuntimePath(runtimePath, basePath);
    return resolved ? new URL(resolved, global.location.href).href : '';
  }

  function indexManifest(manifest) {
    const nextIndex = new Map();

    if (manifest && Array.isArray(manifest.images)) {
      manifest.images.forEach((entry) => {
        const sourcePath = normalizeRuntimePath(entry && entry.source_path);
        if (sourcePath) {
          nextIndex.set(sourcePath, entry);
        }
      });
    }

    imageIndex = nextIndex;
    return manifest || null;
  }

  function setManifest(manifest) {
    manifestPromise = Promise.resolve(indexManifest(manifest));
    return imageIndex;
  }

  function load(options = {}) {
    if (manifestPromise) {
      return manifestPromise;
    }

    const basePath = normalizeText(options.basePath);
    const manifestPath = normalizeText(options.path) || DEFAULT_MANIFEST_PATH;
    const manifestUrl = absoluteRuntimeUrl(manifestPath, basePath);

    if (!manifestUrl || typeof global.fetch !== 'function') {
      manifestPromise = Promise.resolve(indexManifest(null));
      return manifestPromise;
    }

    manifestPromise = global.fetch(manifestUrl)
      .then((response) => {
        if (!response.ok) throw new Error('image manifest fetch ' + response.status);
        return response.json();
      })
      .then(indexManifest)
      .catch(() => indexManifest(null));

    return manifestPromise;
  }

  function getEntry(sourcePath) {
    return imageIndex.get(normalizeRuntimePath(sourcePath)) || null;
  }

  function responsiveImageAttributes(sourcePath, options = {}) {
    const sourceKey = normalizeRuntimePath(sourcePath);
    const basePath = normalizeText(options.basePath);
    const attrs = {
      src: absoluteRuntimeUrl(sourceKey, basePath),
      srcset: '',
      sizes: normalizeText(options.sizes),
      width: '',
      height: '',
    };
    const entry = getEntry(sourceKey);

    if (!entry) {
      return attrs;
    }

    if (entry.source && Number.isInteger(entry.source.width) && Number.isInteger(entry.source.height)) {
      attrs.width = String(entry.source.width);
      attrs.height = String(entry.source.height);
    }

    const variants = Array.isArray(entry.variants)
      ? entry.variants
        .filter((variant) => variant && Number.isInteger(variant.width) && variant.dist_path)
        .sort((left, right) => left.width - right.width)
      : [];

    attrs.srcset = variants
      .map((variant) => `${absoluteRuntimeUrl(variant.dist_path, basePath)} ${variant.width}w`)
      .join(', ');

    return attrs;
  }

  function applyResponsiveImage(img, sourcePath, options = {}) {
    if (!img || !sourcePath) return null;

    const attrs = responsiveImageAttributes(sourcePath, options);

    if (attrs.src) {
      img.src = attrs.src;
    }

    if (attrs.srcset) {
      img.setAttribute('srcset', attrs.srcset);
    }

    if (attrs.sizes) {
      img.setAttribute('sizes', attrs.sizes);
    }

    if (attrs.width && attrs.height) {
      img.setAttribute('width', attrs.width);
      img.setAttribute('height', attrs.height);
    }

    return attrs;
  }

  function applyDeclarativeImages(root, options = {}) {
    const scope = root && typeof root.querySelectorAll === 'function' ? root : global.document;
    if (!scope || typeof scope.querySelectorAll !== 'function') return;

    scope.querySelectorAll('img[data-responsive-image-source]').forEach((img) => {
      applyResponsiveImage(img, img.getAttribute('data-responsive-image-source'), {
        basePath: options.basePath,
        sizes: img.getAttribute('data-responsive-image-sizes') || options.sizes || '',
      });
    });
  }

  global.SiteImageManifest = {
    applyDeclarativeImages,
    applyResponsiveImage,
    getEntry,
    load,
    normalizeRuntimePath,
    responsiveImageAttributes,
    setManifest,
  };
})(window);
