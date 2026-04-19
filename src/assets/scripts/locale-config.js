(function attachLocaleConfig(global) {
  'use strict';

  const LOCALES = [
    { code: 'fr', label: 'FR', required: true, public: true, preview: true },
    { code: 'en', label: 'EN', required: false, public: true, preview: true },
    { code: 'nl', label: 'NL', required: false, public: true, preview: true },
  ];
  const DEFAULT_LOCALE = 'fr';
  const FALLBACK_LOCALES = ['fr', 'en'];

  function localeCodes(filter) {
    return LOCALES
      .filter((locale) => (typeof filter === 'function' ? filter(locale) : true))
      .map((locale) => locale.code);
  }

  function normalizeLocale(locale, options) {
    const supported = options && Array.isArray(options.supported)
      ? new Set(options.supported)
      : new Set(localeCodes());
    const fallback = options && typeof options.defaultLocale === 'string'
      ? options.defaultLocale
      : DEFAULT_LOCALE;
    const normalized = typeof locale === 'string'
      ? locale.trim().toLowerCase().split('-')[0]
      : '';

    return supported.has(normalized) ? normalized : fallback;
  }

  function supportedLocale(locale, options) {
    const supported = options && Array.isArray(options.supported)
      ? new Set(options.supported)
      : new Set(localeCodes());
    const normalized = typeof locale === 'string'
      ? locale.trim().toLowerCase().split('-')[0]
      : '';

    return supported.has(normalized) ? normalized : '';
  }

  global.SiteLocales = {
    defaultLocale: DEFAULT_LOCALE,
    fallbackLocales: FALLBACK_LOCALES.slice(),
    locales: LOCALES.map((locale) => Object.assign({}, locale)),
    supportedLocaleCodes: localeCodes,
    publicLocaleCodes: () => localeCodes((locale) => locale.public),
    previewLocaleCodes: () => localeCodes((locale) => locale.preview),
    normalizeLocale,
    supportedLocale,
  };
})(window);
