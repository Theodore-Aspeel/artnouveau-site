(function attachSiteI18n(global) {
  'use strict';

  const DEFAULT_LOCALE = 'fr';
  const PREVIEW_LOCALE_PARAM = 'previewLocale';
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
      'home.aria.footer': 'Liens de bas de page',
      'home.aria.gallery': 'Pagination de la galerie',
      'home.aria.galleryTags': 'Tags des articles',
      'home.aria.mainNav': 'Navigation principale',
      'home.aria.siteHome': 'Retour \u00e0 l\u2019accueil',
      'home.cta.articles': 'Lire les articles',
      'home.curated.first': '\u00c0 lire d\u2019abord',
      'home.curated.intro': 'Quelques sujets suffisent pour prendre la mesure du site: une fa\u00e7ade fondatrice, un contrepoint, puis un d\u00e9placement d\u2019\u00e9chelle ou de ville.',
      'home.curated.title': 'Trois entr\u00e9es pour commencer sans d\u00e9tour',
      'home.footer.body': 'Une publication d\u2019auteur consacr\u00e9e aux villes europ\u00e9ennes, \u00e0 leurs seuils, \u00e0 leurs fa\u00e7ades, et \u00e0 ce qui persiste encore dans le d\u00e9tail.',
      'home.footer.copyright': '\u00a9 2026 Art Nouveau et Art D\u00e9co en Europe.',
      'home.footer.latest': 'Derniers articles',
      'home.footer.legal': 'Mentions et contact',
      'home.footer.nav': 'Parcours',
      'home.gallery.intro': 'L\u2019ensemble du corpus reste consultable ici, avec ses rep\u00e8res de villes, de styles et de d\u00e9tails.',
      'home.gallery.note': 'L\u2019intention du site se lit <a href="about.html">\u00e0 propos</a>. Les photographies, d\u00e9tails et rep\u00e9rages se prolongent sur <a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener noreferrer">Instagram</a>.',
      'home.gallery.title': 'Tous les articles',
      'home.hero.alt': 'Fa\u00e7ades de Saint-Gilles \u00e0 Bruxelles',
      'home.hero.body': 'Le site part de cette familiarit\u00e9 discr\u00e8te. Il avance par villes, par b\u00e2timents, par rapprochements. Les images ouvrent la lecture. Le texte vient pour pr\u00e9ciser, relier, parfois retenir une m\u00e9moire, sans demander plus au lieu qu\u2019il ne donne.',
      'home.hero.caption': 'Saint-Gilles, Bruxelles. Une rue peut suffire \u00e0 remettre le regard au travail.',
      'home.hero.eyebrow': 'Publication d\u2019auteur',
      'home.hero.lede': 'En grandissant en Belgique, certains d\u00e9tails d\u2019Art Nouveau ou d\u2019Art D\u00e9co sont d\u00e9j\u00e0 l\u00e0 avant m\u00eame qu\u2019on sache les nommer. Une ferronnerie, une c\u00e9ramique, un angle de fa\u00e7ade, un seuil plus attentif que les autres.',
      'home.hero.title': 'Regarder d\u2019abord. Nommer ensuite.',
      'home.kicker.articles': 'Articles',
      'home.kicker.cities': 'Par villes',
      'home.kicker.rhythms': 'Rythmes',
      'home.curated.next': 'Puis poursuivre',
      'home.nav.about': '\u00c0 propos',
      'home.nav.articles': 'Articles',
      'home.nav.home': 'Accueil',
      'home.path.count': '{count} {articleLabel}',
      'home.path.first': 'Commencer',
      'home.path.intro': 'Le site avance par foyers urbains plus que par chronologie. Certaines villes ouvrent d\u2019embl\u00e9e plusieurs lectures.',
      'home.path.next': 'Ensuite',
      'home.path.title': 'Entrer par une ville, puis \u00e9largir le regard',
      'home.rhythm.intro': 'Certaines pages accompagnent longuement le regard. D\u2019autres tiennent en une note plus br\u00e8ve. Cette alternance fait partie de la revue.',
      'home.rhythm.long.intro': 'Des textes plus amples, quand le lieu demande plusieurs reprises du regard.',
      'home.rhythm.long.label': 'Parcours d\u00e9velopp\u00e9s',
      'home.rhythm.long.title': 'Prendre le temps d\u2019une fa\u00e7ade',
      'home.rhythm.short.intro': 'Des sujets plus courts, quand une adresse ou un d\u00e9tail suffisent \u00e0 tenir la lecture.',
      'home.rhythm.short.label': 'Notes br\u00e8ves',
      'home.rhythm.short.title': 'Rester \u00e0 la juste \u00e9chelle',
      'home.rhythm.title': 'Deux mani\u00e8res de lire',
      'home.tagline': 'Carnets de villes, fa\u00e7ades et seuils',
      'nav.close': 'Fermer',
      'nav.menu': 'Menu',
      'nav.open': 'Ouvrir le menu',
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
      'home.aria.footer': 'Footer links',
      'home.aria.gallery': 'Gallery pagination',
      'home.aria.galleryTags': 'Article tags',
      'home.aria.mainNav': 'Main navigation',
      'home.aria.siteHome': 'Back to home',
      'home.cta.articles': 'Read the articles',
      'home.curated.first': 'Start here',
      'home.curated.intro': 'A few subjects are enough to get the measure of the site: a founding facade, a counterpoint, then a shift in scale or city.',
      'home.curated.title': 'Three direct ways in',
      'home.footer.body': 'An author-led publication devoted to European cities, their thresholds, their facades, and what still persists in the detail.',
      'home.footer.copyright': '\u00a9 2026 Art Nouveau and Art Deco in Europe.',
      'home.footer.latest': 'Latest articles',
      'home.footer.legal': 'Legal notice and contact',
      'home.footer.nav': 'Routes',
      'home.gallery.intro': 'The whole corpus remains available here, with its markers of cities, styles, and details.',
      'home.gallery.note': 'The site\u2019s intention is explained <a href="about.html">about the project</a>. Photographs, details, and field notes continue on <a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener noreferrer">Instagram</a>.',
      'home.gallery.title': 'All articles',
      'home.hero.alt': 'Facades in Saint-Gilles, Brussels',
      'home.hero.body': 'The site begins from that discreet familiarity. It moves through cities, buildings, and connections. Images open the reading. Text comes in to clarify, connect, and sometimes hold a memory, without asking more from the place than it gives.',
      'home.hero.caption': 'Saint-Gilles, Brussels. One street can be enough to make the eye work again.',
      'home.hero.eyebrow': 'Author publication',
      'home.hero.lede': 'Growing up in Belgium, certain Art Nouveau or Art Deco details are already there before one knows how to name them: ironwork, ceramic, a facade corner, a threshold more attentive than the others.',
      'home.hero.title': 'Look first. Name later.',
      'home.kicker.articles': 'Articles',
      'home.kicker.cities': 'By city',
      'home.kicker.rhythms': 'Rhythms',
      'home.curated.next': 'Then continue',
      'home.nav.about': 'About',
      'home.nav.articles': 'Articles',
      'home.nav.home': 'Home',
      'home.path.count': '{count} {articleLabel}',
      'home.path.first': 'Start',
      'home.path.intro': 'The site moves through urban centres more than through chronology. Some cities immediately open several readings.',
      'home.path.next': 'Then',
      'home.path.title': 'Enter through a city, then widen the view',
      'home.rhythm.intro': 'Some pages follow the eye at length. Others hold together as a shorter note. That alternation is part of the review.',
      'home.rhythm.long.intro': 'Longer pieces for places that ask for several passes of attention.',
      'home.rhythm.long.label': 'Longer routes',
      'home.rhythm.long.title': 'Take time with a facade',
      'home.rhythm.short.intro': 'Shorter subjects, when an address or a detail is enough to hold the reading.',
      'home.rhythm.short.label': 'Brief notes',
      'home.rhythm.short.title': 'Keep the right scale',
      'home.rhythm.title': 'Two ways of reading',
      'home.tagline': 'City notes, facades, and thresholds',
      'nav.close': 'Close',
      'nav.menu': 'Menu',
      'nav.open': 'Open menu',
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

  function supportedLocale(locale) {
    const normalized = typeof locale === 'string'
      ? locale.trim().toLowerCase().split('-')[0]
      : '';

    return SUPPORTED_LOCALES.has(normalized) ? normalized : '';
  }

  function previewLocale() {
    const params = new URLSearchParams(window.location.search);
    return supportedLocale(params.get(PREVIEW_LOCALE_PARAM));
  }

  function resolveLocale(source) {
    const lang = source || previewLocale() || document.documentElement.getAttribute('lang');
    return normalizeLocale(lang || DEFAULT_LOCALE);
  }

  function withPreviewLocale(href) {
    const locale = previewLocale();
    if (!locale || typeof href !== 'string' || !href.trim()) return href;
    if (/^(?:[a-z][a-z0-9+.-]*:)?\/\//i.test(href) || /^(?:mailto|tel):/i.test(href)) return href;

    const hashIndex = href.indexOf('#');
    const beforeHash = hashIndex >= 0 ? href.slice(0, hashIndex) : href;
    const hash = hashIndex >= 0 ? href.slice(hashIndex) : '';
    const queryIndex = beforeHash.indexOf('?');
    const path = queryIndex >= 0 ? beforeHash.slice(0, queryIndex) : beforeHash;
    const query = queryIndex >= 0 ? beforeHash.slice(queryIndex + 1) : '';
    const params = new URLSearchParams(query);

    params.set(PREVIEW_LOCALE_PARAM, locale);

    const serialized = params.toString();
    return path + (serialized ? '?' + serialized : '') + hash;
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
    previewLocale,
    resolveLocale,
    t,
    articleCountLabel,
    withPreviewLocale,
  };
})(window);
