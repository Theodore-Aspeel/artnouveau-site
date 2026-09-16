function text(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function object(value) {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
}

function validIsoDate(value) {
  const candidate = text(value);
  if (!/^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:\d{2})?)?$/.test(candidate)) {
    return '';
  }

  const [year, month, day] = candidate.slice(0, 10).split('-').map(Number);
  const calendarDate = new Date(Date.UTC(year, month - 1, day));
  const isRealCalendarDate = calendarDate.getUTCFullYear() === year
    && calendarDate.getUTCMonth() === month - 1
    && calendarDate.getUTCDate() === day;

  return isRealCalendarDate && !Number.isNaN(Date.parse(candidate)) ? candidate : '';
}

function articleLanguage(article, locale, access) {
  const requested = text(locale).toLowerCase().split('-')[0] || 'fr';
  if (access && typeof access.isArticleLocaleReady === 'function' && access.isArticleLocaleReady(article, requested)) {
    return requested;
  }
  return 'fr';
}

function placeName(article) {
  const identity = object(article && article.identity);
  const verifiedInfo = object(article && article.verified_info);
  return text(identity.canonical_name)
    || text(identity.exact_name)
    || text(verifiedInfo.canonical_name)
    || text(verifiedInfo.exact_name);
}

function placeAddress(article) {
  const facts = object(article && article.facts);
  const location = object(facts.location);
  const streetAddress = text(location.address);
  const addressLocality = text(location.city);
  const addressCountry = text(location.country_code) || text(location.country);

  if (!streetAddress && !addressLocality && !addressCountry) return null;

  return {
    '@type': 'PostalAddress',
    ...(streetAddress ? { streetAddress } : {}),
    ...(addressLocality ? { addressLocality } : {}),
    ...(addressCountry ? { addressCountry } : {}),
  };
}

export function buildArticleStructuredData({
  article,
  locale,
  canonicalUrl,
  imageUrl = '',
  access,
}) {
  const canonical = text(canonicalUrl);
  const language = articleLanguage(article, locale, access);
  const headline = access && typeof access.getArticleTitle === 'function'
    ? text(access.getArticleTitle(article, language))
    : text(article && article.title);

  if (!canonical || !headline) return null;

  const description = access && typeof access.getArticleMetaDescription === 'function'
    ? text(access.getArticleMetaDescription(article, language))
    : text(article && article.meta_description);
  const editorial = object(article && article.editorial);
  const publication = object(article && article.publication);
  const authorName = text(editorial.author);
  const publishedOn = validIsoDate(publication.published_on);
  const updatedOn = validIsoDate(publication.updated_on);
  const resolvedPlaceName = placeName(article);
  const resolvedAddress = placeAddress(article);
  const articleId = `${canonical}#article`;
  const placeId = `${canonical}#place`;

  const articleNode = {
    '@type': 'Article',
    '@id': articleId,
    url: canonical,
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': canonical,
    },
    headline,
    ...(description ? { description } : {}),
    inLanguage: language,
    ...(text(imageUrl) ? { image: text(imageUrl) } : {}),
    ...(authorName ? { author: { '@type': 'Person', name: authorName } } : {}),
    ...(publishedOn ? { datePublished: publishedOn } : {}),
    ...(updatedOn ? { dateModified: updatedOn } : {}),
    ...(resolvedPlaceName ? { about: { '@id': placeId } } : {}),
  };

  const graph = [articleNode];
  if (resolvedPlaceName) {
    graph.push({
      '@type': 'Place',
      '@id': placeId,
      name: resolvedPlaceName,
      ...(resolvedAddress ? { address: resolvedAddress } : {}),
    });
  }

  return {
    '@context': 'https://schema.org',
    '@graph': graph,
  };
}

export function serializeStructuredData(value) {
  return JSON.stringify(value)
    .replaceAll('<', '\\u003c')
    .replaceAll('\u2028', '\\u2028')
    .replaceAll('\u2029', '\\u2029');
}

export function renderStructuredDataScript(value) {
  if (!value) return '';
  return `<script type="application/ld+json">${serializeStructuredData(value)}</script>`;
}
