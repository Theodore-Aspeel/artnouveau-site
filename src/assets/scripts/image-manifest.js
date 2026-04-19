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

  function normalizeFormat(value) {
    const format = normalizeText(value).toLowerCase();
    return format === 'jpg' ? 'jpeg' : format;
  }

  function variantFormat(entry, options) {
    const requested = normalizeFormat(options.format || options.variantFormat);
    if (requested) return requested;

    return normalizeFormat(entry && entry.source && entry.source.format);
  }

  function getVariants(sourcePath, options = {}) {
    const entry = getEntry(sourcePath);
    if (!entry || !Array.isArray(entry.variants)) {
      return [];
    }

    const format = variantFormat(entry, options);

    return entry.variants
      .filter((variant) => {
        if (!variant || !Number.isInteger(variant.width) || !variant.dist_path) {
          return false;
        }

        return !format || normalizeFormat(variant.format) === format;
      })
      .sort((left, right) => left.width - right.width);
  }

  function mimeTypeForFormat(format) {
    const normalized = normalizeFormat(format);
    if (normalized === 'avif') return 'image/avif';
    if (normalized === 'webp') return 'image/webp';
    if (normalized === 'jpeg') return 'image/jpeg';
    if (normalized === 'png') return 'image/png';
    return normalized ? `image/${normalized}` : '';
  }

  function srcsetForVariants(variants, basePath) {
    return variants
      .map((variant) => `${absoluteRuntimeUrl(variant.dist_path, basePath)} ${variant.width}w`)
      .join(', ');
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

    const variants = getVariants(sourceKey, options);

    attrs.srcset = srcsetForVariants(variants, basePath);

    return attrs;
  }

  function responsivePictureAttributes(sourcePath, options = {}) {
    const basePath = normalizeText(options.basePath);
    const sourceKey = normalizeRuntimePath(sourcePath);
    const imageOptions = Object.assign({}, options);
    delete imageOptions.format;
    delete imageOptions.variantFormat;
    const attrs = responsiveImageAttributes(sourceKey, imageOptions);
    const sources = ['avif', 'webp']
      .map((format) => {
        const srcset = srcsetForVariants(getVariants(sourceKey, { format }), basePath);
        return srcset ? {
          format,
          type: mimeTypeForFormat(format),
          srcset,
          sizes: attrs.sizes,
        } : null;
      })
      .filter(Boolean);

    return {
      img: attrs,
      sources,
    };
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

  function applyResponsivePicture(img, sourcePath, options = {}) {
    if (!img || !sourcePath) return null;

    const attrs = responsivePictureAttributes(sourcePath, options);
    applyResponsiveImage(img, sourcePath, options);

    if (!attrs.sources.length || !global.document || typeof global.document.createElement !== 'function') {
      attrs.element = img;
      return attrs;
    }

    const currentParent = img.parentNode;
    const picture = currentParent && currentParent.tagName && currentParent.tagName.toLowerCase() === 'picture'
      ? currentParent
      : global.document.createElement('picture');

    picture.querySelectorAll('source[data-responsive-image-format]').forEach((source) => source.remove());

    attrs.sources.forEach((sourceAttrs) => {
      const source = global.document.createElement('source');
      source.setAttribute('type', sourceAttrs.type);
      source.setAttribute('srcset', sourceAttrs.srcset);
      source.setAttribute('data-responsive-image-format', sourceAttrs.format);
      if (sourceAttrs.sizes) {
        source.setAttribute('sizes', sourceAttrs.sizes);
      }
      if (picture === currentParent) {
        picture.insertBefore(source, img);
      } else {
        picture.appendChild(source);
      }
    });

    if (picture !== currentParent) {
      if (currentParent) {
        currentParent.insertBefore(picture, img);
      }
      picture.appendChild(img);
    }

    attrs.element = picture;
    return attrs;
  }

  function applyDeclarativeImages(root, options = {}) {
    const scope = root && typeof root.querySelectorAll === 'function' ? root : global.document;
    if (!scope || typeof scope.querySelectorAll !== 'function') return;

    scope.querySelectorAll('img[data-responsive-image-source]').forEach((img) => {
      applyResponsivePicture(img, img.getAttribute('data-responsive-image-source'), {
        basePath: options.basePath,
        sizes: img.getAttribute('data-responsive-image-sizes') || options.sizes || '',
      });
    });
  }

  global.SiteImageManifest = {
    applyDeclarativeImages,
    applyResponsiveImage,
    applyResponsivePicture,
    getEntry,
    getVariants,
    load,
    normalizeRuntimePath,
    responsivePictureAttributes,
    responsiveImageAttributes,
    setManifest,
  };
})(window);
