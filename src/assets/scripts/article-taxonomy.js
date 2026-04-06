(function attachArticleTags(global) {
  'use strict';

  const CANONICAL_STYLES = {
    'art nouveau': 'Art Nouveau',
    'art nouveau geometrique': 'Art Nouveau géométrique',
    'art deco': 'Art Déco',
    'liberty art nouveau': 'Liberty / Art Nouveau',
    'secession viennoise': 'Sécession viennoise',
  };

  const CANONICAL_TAGS = {
    'art nouveau': 'Art Nouveau',
    'art deco': 'Art Déco',
    'batiment public': 'Bâtiment public',
    commerce: 'Commerce',
    facade: 'Façade',
    habitat: 'Habitat',
    liberty: 'Liberty',
    'motif floral': 'Motif floral',
    seuil: 'Seuil',
    'secession viennoise': 'Sécession viennoise',
    'ecriture urbaine': 'Écriture urbaine',
  };

  function normalizeText(value) {
    return typeof value === 'string' ? value.trim() : '';
  }

  function slugifyTag(value) {
    return normalizeText(value)
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function normalizeControlledLabel(value, controlledMap) {
    const raw = normalizeText(value);
    if (!raw) return '';

    const slug = slugifyTag(raw).replace(/-/g, ' ');
    return controlledMap[slug] || raw;
  }

  function normalizeTag(value) {
    return normalizeControlledLabel(value, CANONICAL_TAGS);
  }

  function normalizeStyle(value) {
    return normalizeControlledLabel(value, CANONICAL_STYLES);
  }

  function getArticleStyle(article) {
    if (!article || typeof article !== 'object') return '';

    const directStyle = normalizeStyle(article.style);
    if (directStyle) return directStyle;

    if (article.verified_info && typeof article.verified_info === 'object') {
      const verifiedStyle = normalizeStyle(article.verified_info.style);
      if (verifiedStyle) return verifiedStyle;
    }

    if (article.practical && typeof article.practical === 'object') {
      return normalizeStyle(article.practical.Style);
    }

    return '';
  }

  function getArticleTags(article) {
    if (!Array.isArray(article && article.tags)) return [];

    const seen = new Set();
    return article.tags
      .map((tag) => normalizeTag(tag))
      .filter((tag) => {
        const slug = slugifyTag(tag);
        if (!tag || !slug || seen.has(slug)) return false;
        seen.add(slug);
        return true;
      });
  }

  function collectTags(articles) {
    const bySlug = new Map();

    (Array.isArray(articles) ? articles : []).forEach((article) => {
      getArticleTags(article).forEach((label) => {
        const slug = slugifyTag(label);
        const entry = bySlug.get(slug) || { slug, label, count: 0 };
        entry.count += 1;
        bySlug.set(slug, entry);
      });
    });

    return Array.from(bySlug.values()).sort((left, right) => {
      if (right.count !== left.count) return right.count - left.count;
      return left.label.localeCompare(right.label, 'fr');
    });
  }

  function buildTagHref(tagLabel, basePath) {
    const slug = slugifyTag(tagLabel);
    if (!slug) return basePath || 'index.html';
    return (basePath || 'index.html') + '?tag=' + encodeURIComponent(slug) + '#galerie';
  }

  function findTagBySlug(articles, slug) {
    const normalized = slugifyTag(slug);
    if (!normalized) return null;
    return collectTags(articles).find((tag) => tag.slug === normalized) || null;
  }

  global.ArticleTags = {
    buildTagHref,
    collectTags,
    findTagBySlug,
    getArticleStyle,
    getArticleTags,
    normalizeStyle,
    normalizeTag,
    normalizeText,
    slugifyTag,
  };
})(window);
