(function attachSiteI18n(global) {
  'use strict';

  const DEFAULT_LOCALE = 'fr';
  const SUPPORTED_LOCALES = new Set(['fr', 'en']);

  const MESSAGES = {
    fr: {
      'article.around': 'Autour',
      'article.author': 'Auteur',
      'article.breadcrumb.aria': 'Fil d\u2019Ariane',
      'article.breadcrumb.articles': 'Articles',
      'article.breadcrumb.home': 'Accueil',
      'article.continue': 'Continuer la lecture',
      'article.editorial.frame': 'Cadre \u00e9ditorial',
      'article.editorial.rigorNote': 'Les rep\u00e8res factuels visibles ici s\u2019appuient sur les donn\u00e9es v\u00e9rifi\u00e9es du corpus. Quand une information reste incertaine, elle demeure signal\u00e9e comme telle.',
      'article.facts': 'Rep\u00e8res',
      'article.imageCredit': 'Cr\u00e9dit image',
      'article.instagram': 'Instagram',
      'article.instagram.aria': 'Ouvrir Instagram @artnouveauetdeco',
      'article.instagram.prefix': 'Photographies et rep\u00e9rages sur ',
      'article.method': 'M\u00e9thode',
      'article.next': 'Article suivant',
      'article.notFound.description': 'Le slug demand\u00e9 ne correspond \u00e0 aucun article publi\u00e9. ',
      'article.notFound.home': 'Retour \u00e0 l\u2019accueil',
      'article.notFound.title': 'Article introuvable',
      'article.previous': 'Article pr\u00e9c\u00e9dent',
      'article.publication': 'Publication',
      'article.quote': 'Citation',
      'article.resources': 'Ressources',
      'article.resources.more': 'Pour prolonger',
      'article.revision': 'R\u00e9vision',
      'article.sidebar.aria': 'Informations compl\u00e9mentaires',
      'article.source': 'Source',
      'article.toConfirm': '\u00c0 confirmer',
      'gallery.activeTag': 'Tag actif',
      'gallery.all': 'Tous',
      'gallery.empty.filtered': 'Aucun article ne correspond \u00e0 ce tag pour le moment.',
      'gallery.empty.load': 'Les articles ne peuvent pas \u00eatre charg\u00e9s pour le moment.',
      'gallery.filteredIntro': '{count} {articleLabel} \u00e0 lire \u00e0 partir de ce rep\u00e8re.',
      'gallery.filteredTitle': 'Autour de {tag}',
      'gallery.nextPage': 'Suiv.',
      'gallery.nextPage.aria': 'Page suivante',
      'gallery.page.aria': 'Page {page}',
      'gallery.placeholder': 'Article',
      'gallery.previousPage': 'Prec.',
      'gallery.previousPage.aria': 'Page pr\u00e9c\u00e9dente',
      'gallery.readArticle.aria': 'Lire l\u2019article : {title}',
      'gallery.reset': 'Voir tous les articles',
      'home.curated.first': '\u00c0 lire d\u2019abord',
      'home.curated.next': 'Puis poursuivre',
      'home.path.count': '{count} {articleLabel}',
      'home.path.first': 'Commencer',
      'home.path.next': 'Ensuite',
      'nav.close': 'Fermer',
      'nav.menu': 'Menu',
      'overlay.image.aria': 'Image en plein \u00e9cran',
      'overlay.close': 'Fermer',
    },
    en: {},
  };

  function normalizeLocale(locale) {
    const normalized = typeof locale === 'string'
      ? locale.trim().toLowerCase().split('-')[0]
      : '';

    return SUPPORTED_LOCALES.has(normalized) ? normalized : DEFAULT_LOCALE;
  }

  function resolveLocale(source) {
    const lang = source || document.documentElement.getAttribute('lang');
    return normalizeLocale(lang || DEFAULT_LOCALE);
  }

  function interpolate(message, params) {
    if (!params || typeof params !== 'object') return message;

    return message.replace(/\{([a-zA-Z0-9_]+)\}/g, (match, key) => (
      Object.prototype.hasOwnProperty.call(params, key) ? String(params[key]) : match
    ));
  }

  function t(key, params, locale) {
    const lang = resolveLocale(locale);
    const message = (MESSAGES[lang] && MESSAGES[lang][key])
      || MESSAGES[DEFAULT_LOCALE][key]
      || key;

    return interpolate(message, params);
  }

  function articleCountLabel(count, locale) {
    return Number(count) > 1 ? t('unit.articles', null, locale) : t('unit.article', null, locale);
  }

  MESSAGES.fr['unit.article'] = 'article';
  MESSAGES.fr['unit.articles'] = 'articles';

  global.SiteI18n = {
    defaultLocale: DEFAULT_LOCALE,
    normalizeLocale,
    resolveLocale,
    t,
    articleCountLabel,
  };
})(window);
