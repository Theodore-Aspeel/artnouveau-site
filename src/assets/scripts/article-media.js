(function attachArticleMedia(global) {
  'use strict';

  const access = global.ArticleAccess;

  function normalizeText(value) {
    return typeof value === 'string' ? value.trim() : '';
  }

  function normalizeImageEntry(image) {
    if (typeof image === 'string') {
      const src = normalizeText(image);
      return src ? { src, alt: '', caption: '', credit: '' } : null;
    }

    if (!image || typeof image !== 'object') {
      return null;
    }

    const src = normalizeText(image.src || image.path || image.image);
    if (!src) return null;

    return {
      src,
      alt: normalizeText(image.alt),
      caption: normalizeText(image.caption),
      credit: normalizeText(image.credit),
    };
  }

  function getImageEntries(article, locale = 'fr') {
    const articleMedia = access && typeof access.getArticleMedia === 'function'
      ? access.getArticleMedia(article, locale)
      : null;
    const entries = [];
    const heroEntry = articleMedia
      ? normalizeImageEntry(articleMedia.hero)
      : normalizeImageEntry(article && article.hero_image);

    if (heroEntry) {
      entries.push(heroEntry);
    }

    const supportImages = articleMedia
      ? articleMedia.support
      : (Array.isArray(article && article.support_images) ? article.support_images : []);

    if (Array.isArray(supportImages)) {
      supportImages.forEach((image) => {
        const normalized = normalizeImageEntry(image);
        if (normalized && !entries.some((entry) => entry.src === normalized.src)) {
          entries.push(normalized);
        }
      });
    }

    return entries;
  }

  function getImageList(article, locale = 'fr') {
    return getImageEntries(article, locale).map((entry) => entry.src);
  }

  function getPrimaryImage(article, locale = 'fr') {
    return getImageList(article, locale)[0] || '';
  }

  function getPrimaryImageEntry(article, locale = 'fr') {
    return getImageEntries(article, locale)[0] || null;
  }

  function getSecondaryImages(article, limit, locale = 'fr') {
    const secondary = getImageList(article, locale).slice(1);

    if (Number.isInteger(limit) && limit >= 0) {
      return secondary.slice(0, limit);
    }

    return secondary;
  }

  function getSecondaryImageEntries(article, limit, locale = 'fr') {
    const secondary = getImageEntries(article, locale).slice(1);

    if (Number.isInteger(limit) && limit >= 0) {
      return secondary.slice(0, limit);
    }

    return secondary;
  }

  function resolveImagePath(path, basePrefix) {
    const normalized = normalizeText(path);
    if (!normalized) return '';
    if (/^(?:https?:)?\/\//.test(normalized) || normalized.startsWith('/')) {
      return normalized;
    }

    return (basePrefix || '') + normalized;
  }

  global.ArticleMedia = {
    getImageEntries,
    getImageList,
    getPrimaryImage,
    getPrimaryImageEntry,
    getSecondaryImages,
    getSecondaryImageEntries,
    normalizeImageEntry,
    normalizeText,
    resolveImagePath,
  };
})(window);
