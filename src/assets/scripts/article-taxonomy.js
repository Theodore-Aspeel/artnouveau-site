(function attachArticleTags(global) {
  'use strict';

  const access = global.ArticleAccess;

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

  const LEGACY_TAG_SLUGS_BY_KEY = {
    art_nouveau: ['art-nouveau'],
    art_deco: ['art-deco'],
    public_building: ['batiment-public'],
    commerce: ['commerce'],
    facade: ['facade'],
    habitat: ['habitat'],
    liberty: ['liberty'],
    floral_motif: ['motif-floral'],
    threshold: ['seuil'],
    vienna_secession: ['secession-viennoise'],
    urban_lettering: ['ecriture-urbaine'],
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

  function tagKeyToSlug(key) {
    return slugifyTag(String(key || '').replace(/_/g, '-'));
  }

  function uniqueEntries(entries) {
    const seen = new Set();

    return entries.filter((entry) => {
      const identity = entry.key || entry.slug;
      if (!identity || seen.has(identity)) return false;
      seen.add(identity);
      return true;
    });
  }

  function getTagLegacySlugs(label, key) {
    return [label].concat(LEGACY_TAG_SLUGS_BY_KEY[key] || [])
      .map((value) => slugifyTag(value))
      .filter(Boolean)
      .filter((slug, index, slugs) => slugs.indexOf(slug) === index);
  }

  function getArticleStyle(article, locale = 'fr') {
    if (!article || typeof article !== 'object') return '';

    if (access && typeof access.getArticleTaxonomy === 'function') {
      const articleTaxonomy = access.getArticleTaxonomy(article, locale);
      if (articleTaxonomy.styleLabel) return articleTaxonomy.styleLabel;
    }

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

  function getArticleTagEntries(article, locale = 'fr') {
    if (access && typeof access.getArticleTaxonomy === 'function') {
      const articleTaxonomy = access.getArticleTaxonomy(article, locale);
      if (Array.isArray(articleTaxonomy.tagKeys) && articleTaxonomy.tagKeys.length) {
        return uniqueEntries(articleTaxonomy.tagKeys.map((key, index) => {
          const label = normalizeText(articleTaxonomy.tagLabels && articleTaxonomy.tagLabels[index]) || key;
          const slug = tagKeyToSlug(key);
          return {
            key,
            label,
            slug,
            legacySlugs: getTagLegacySlugs(label, key),
          };
        }));
      }
    }

    if (!Array.isArray(article && article.tags)) return [];

    return uniqueEntries(article.tags.map((tag) => {
      const label = normalizeTag(tag);
      const slug = slugifyTag(label);
      return {
        key: slug,
        label,
        slug,
        legacySlugs: getTagLegacySlugs(label, slug),
      };
    }));
  }

  function getArticleTags(article, locale = 'fr') {
    return getArticleTagEntries(article, locale).map((entry) => entry.label);
  }

  function getArticleTagKeys(article) {
    return getArticleTagEntries(article).map((entry) => entry.key);
  }

  function collectTags(articles, locale = 'fr') {
    const bySlug = new Map();

    (Array.isArray(articles) ? articles : []).forEach((article) => {
      getArticleTagEntries(article, locale).forEach((tag) => {
        const slug = tag.slug;
        const entry = bySlug.get(slug) || {
          key: tag.key,
          slug,
          label: tag.label,
          legacySlugs: tag.legacySlugs || [],
          count: 0,
        };
        entry.count += 1;
        bySlug.set(slug, entry);
      });
    });

    return Array.from(bySlug.values()).sort((left, right) => {
      if (right.count !== left.count) return right.count - left.count;
      return left.label.localeCompare(right.label, locale);
    });
  }

  function getTagSlug(tag) {
    if (tag && typeof tag === 'object') return normalizeText(tag.slug) || tagKeyToSlug(tag.key) || slugifyTag(tag.label);
    return slugifyTag(tag);
  }

  function buildTagHref(tag, basePath) {
    const slug = getTagSlug(tag);
    if (!slug) return basePath || 'index.html';
    return (basePath || 'index.html') + '?tag=' + encodeURIComponent(slug) + '#galerie';
  }

  function findTagBySlug(articles, slug, locale = 'fr') {
    const normalized = slugifyTag(slug);
    if (!normalized) return null;
    return collectTags(articles, locale).find((tag) => {
      if (tag.slug === normalized) return true;
      return Array.isArray(tag.legacySlugs) && tag.legacySlugs.includes(normalized);
    }) || null;
  }

  global.ArticleTags = {
    buildTagHref,
    collectTags,
    findTagBySlug,
    getArticleStyle,
    getArticleTagEntries,
    getArticleTagKeys,
    getArticleTags,
    normalizeStyle,
    normalizeTag,
    normalizeText,
    slugifyTag,
  };
})(window);
