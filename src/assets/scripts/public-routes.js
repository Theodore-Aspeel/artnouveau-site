(function attachSitePublicRoutes(global) {
  'use strict';

  const localeConfig = global.SiteLocales || {};
  const DEFAULT_LOCALE = localeConfig.defaultLocale || 'fr';
  const ROUTE_NAMES = Object.freeze({
    home: 'home',
    about: 'about',
    mentions: 'mentions',
    article: 'article',
  });

  function configuredLocaleCodes(kind, fallback) {
    const getterName = kind + 'LocaleCodes';
    if (typeof localeConfig[getterName] === 'function') {
      return localeConfig[getterName]();
    }
    return fallback.slice();
  }

  function publicLocaleCodes() {
    return configuredLocaleCodes('public', ['fr', 'en', 'nl']);
  }

  function previewLocaleCodes() {
    return configuredLocaleCodes('preview', publicLocaleCodes());
  }

  function supportedPublicLocale(locale) {
    const supported = publicLocaleCodes();
    if (typeof localeConfig.supportedLocale === 'function') {
      return localeConfig.supportedLocale(locale, { supported });
    }

    const normalized = typeof locale === 'string'
      ? locale.trim().toLowerCase().split('-')[0]
      : '';
    return supported.includes(normalized) ? normalized : '';
  }

  function normalizePublicLocale(locale) {
    const supported = supportedPublicLocale(locale);
    if (supported) return supported;

    const publicLocales = publicLocaleCodes();
    return publicLocales.includes(DEFAULT_LOCALE)
      ? DEFAULT_LOCALE
      : publicLocales[0] || DEFAULT_LOCALE;
  }

  function encodeSegment(value, fieldName) {
    const normalized = typeof value === 'string' ? value.trim() : '';
    if (!normalized) {
      throw new TypeError(fieldName + ' is required to build a public URL.');
    }
    return encodeURIComponent(normalized);
  }

  function publicPath(locale, segments) {
    const lang = normalizePublicLocale(locale);
    const cleanSegments = segments.filter(Boolean);
    return '/' + lang + '/' + (cleanSegments.length ? cleanSegments.join('/') + '/' : '');
  }

  function home(locale) {
    return publicPath(locale, []);
  }

  function about(locale) {
    return publicPath(locale, ['about']);
  }

  function mentions(locale) {
    return publicPath(locale, ['mentions']);
  }

  function article(locale, slug) {
    return publicPath(locale, ['articles', encodeSegment(slug, 'slug')]);
  }

  function route(routeName, locale, params) {
    switch (routeName) {
      case ROUTE_NAMES.home:
        return home(locale);
      case ROUTE_NAMES.about:
        return about(locale);
      case ROUTE_NAMES.mentions:
        return mentions(locale);
      case ROUTE_NAMES.article:
        return article(locale, params && params.slug);
      default:
        throw new TypeError('Unknown public route: ' + routeName);
    }
  }

  function alternates(routeName, params) {
    return publicLocaleCodes().map((locale) => ({
      lang: locale,
      hreflang: locale,
      href: route(routeName, locale, params || {}),
    }));
  }

  global.SitePublicRoutes = {
    routeNames: ROUTE_NAMES,
    defaultLocale: DEFAULT_LOCALE,
    publicLocaleCodes,
    previewLocaleCodes,
    supportedPublicLocale,
    normalizePublicLocale,
    home,
    about,
    mentions,
    article,
    route,
    alternates,
  };
})(window);
