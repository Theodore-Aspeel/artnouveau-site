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
      'home.rhythm.long.intro': 'Des textes plus amples, quand le lieu demande plusieurs reprises du regard.',
      'home.rhythm.long.label': 'Parcours d\u00e9velopp\u00e9s',
      'home.rhythm.long.title': 'Prendre le temps d\u2019une fa\u00e7ade',
      'home.rhythm.short.intro': 'Des sujets plus courts, quand une adresse ou un d\u00e9tail suffisent \u00e0 tenir la lecture.',
      'home.rhythm.short.label': 'Notes br\u00e8ves',
      'home.rhythm.short.title': 'Rester \u00e0 la juste \u00e9chelle',
      'nav.close': 'Fermer',
      'nav.menu': 'Menu',
      'overlay.image.aria': 'Image en plein \u00e9cran',
      'overlay.close': 'Fermer',
    },
    en: {
      'article.around': 'Around',
      'article.author': 'Author',
      'article.breadcrumb.aria': 'Breadcrumb',
      'article.breadcrumb.articles': 'Articles',
      'article.breadcrumb.home': 'Home',
      'article.continue': 'Continue reading',
      'article.editorial.frame': 'Editorial frame',
      'article.editorial.rigorNote': 'The factual markers shown here rely on verified corpus data. When information remains uncertain, it is still identified as such.',
      'article.facts': 'Key facts',
      'article.imageCredit': 'Image credit',
      'article.instagram': 'Instagram',
      'article.instagram.aria': 'Open Instagram @artnouveauetdeco',
      'article.instagram.prefix': 'Photographs and field notes on ',
      'article.method': 'Method',
      'article.next': 'Next article',
      'article.notFound.description': 'The requested slug does not match any published article. ',
      'article.notFound.home': 'Back to home',
      'article.notFound.title': 'Article not found',
      'article.previous': 'Previous article',
      'article.publication': 'Publication',
      'article.quote': 'Quote',
      'article.resources': 'Resources',
      'article.resources.more': 'To go further',
      'article.revision': 'Revision',
      'article.sidebar.aria': 'Additional information',
      'article.source': 'Source',
      'article.toConfirm': 'To confirm',
      'gallery.activeTag': 'Active tag',
      'gallery.all': 'All',
      'gallery.empty.filtered': 'No article matches this tag yet.',
      'gallery.empty.load': 'Articles cannot be loaded right now.',
      'gallery.filteredIntro': '{count} {articleLabel} to read from this marker.',
      'gallery.filteredTitle': 'Around {tag}',
      'gallery.nextPage': 'Next',
      'gallery.nextPage.aria': 'Next page',
      'gallery.page.aria': 'Page {page}',
      'gallery.placeholder': 'Article',
      'gallery.previousPage': 'Prev.',
      'gallery.previousPage.aria': 'Previous page',
      'gallery.readArticle.aria': 'Read the article: {title}',
      'gallery.reset': 'View all articles',
      'home.curated.first': 'Start here',
      'home.curated.next': 'Then continue',
      'home.path.count': '{count} {articleLabel}',
      'home.path.first': 'Start',
      'home.path.next': 'Then',
      'home.rhythm.long.intro': 'Longer pieces for places that ask for several passes of attention.',
      'home.rhythm.long.label': 'Longer routes',
      'home.rhythm.long.title': 'Take time with a facade',
      'home.rhythm.short.intro': 'Shorter subjects, when an address or a detail is enough to hold the reading.',
      'home.rhythm.short.label': 'Brief notes',
      'home.rhythm.short.title': 'Keep the right scale',
      'nav.close': 'Close',
      'nav.menu': 'Menu',
      'overlay.image.aria': 'Full-screen image',
      'overlay.close': 'Close',
    },
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
  MESSAGES.en['unit.article'] = 'article';
  MESSAGES.en['unit.articles'] = 'articles';

  global.SiteI18n = {
    defaultLocale: DEFAULT_LOCALE,
    normalizeLocale,
    resolveLocale,
    t,
    articleCountLabel,
  };
})(window);
