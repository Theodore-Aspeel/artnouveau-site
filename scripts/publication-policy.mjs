export const PUBLICATION_MODES = Object.freeze({
  LEGACY_VISIBLE: 'legacy-visible',
  PUBLISHED_ONLY: 'published-only',
});

export function resolvePublicationMode(value = '') {
  const normalized = typeof value === 'string' ? value.trim() : '';
  const mode = normalized || PUBLICATION_MODES.LEGACY_VISIBLE;

  if (!Object.values(PUBLICATION_MODES).includes(mode)) {
    throw new TypeError(
      `PUBLICATION_MODE must be ${Object.values(PUBLICATION_MODES).join(' or ')}.`
    );
  }

  return mode;
}

export function selectPublicArticles(articles, mode = PUBLICATION_MODES.LEGACY_VISIBLE) {
  const normalizedMode = resolvePublicationMode(mode);
  const source = Array.isArray(articles) ? articles : [];

  if (normalizedMode === PUBLICATION_MODES.PUBLISHED_ONLY) {
    return source.filter((article) => article && article.status === 'published');
  }

  return [...source];
}

export function selectIndexableArticles(articles) {
  const source = Array.isArray(articles) ? articles : [];
  return source.filter((article) => article && article.status === 'published');
}

export function articleRobotsDirective(article) {
  return article && article.status === 'published' ? 'index,follow' : 'noindex,follow';
}
