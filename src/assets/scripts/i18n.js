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
      'article.map.open': 'Ouvrir dans Google Maps',
      'article.map.openFor': 'Ouvrir cette adresse dans Google Maps : {address}',
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
      'about.aside.aria': 'Position \u00e9ditoriale',
      'about.aside.text': 'Ce que j\u2019essaie de pr\u00e9server ici, c\u2019est une pr\u00e9cision calme. Assez de contexte pour orienter le regard, assez de retenue pour laisser au lieu sa propre densit\u00e9.',
      'about.card.corrections.body': 'Un signalement factuel utile, une pr\u00e9cision sourc\u00e9e, un cr\u00e9dit d\u2019image \u00e0 compl\u00e9ter peuvent \u00eatre transmis via Instagram. Le point de contact \u00e9ditorial du projet reste volontairement simple: <a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener noreferrer">@artnouveauetdeco</a>.',
      'about.card.corrections.label': 'Corrections',
      'about.card.corrections.title': 'Corriger sans alourdir',
      'about.card.limits.body': 'Certaines donn\u00e9es restent partielles. Dans ce cas, elles demeurent signal\u00e9es comme \u00e0 confirmer. Le site pr\u00e9f\u00e8re une lacune explicite \u00e0 une pr\u00e9cision incertaine.',
      'about.card.limits.label': 'Limites',
      'about.card.limits.title': 'Ne pas combler ce qui manque',
      'about.card.method.body': 'Les textes partent d\u2019abord d\u2019une lecture de rue, d\u2019une fa\u00e7ade, d\u2019un seuil, d\u2019un d\u00e9tail qui tient r\u00e9ellement devant l\u2019\u0153il. Les rep\u00e8res factuels visibles dans les articles sont ajout\u00e9s quand ils peuvent \u00eatre maintenus avec nettet\u00e9.',
      'about.card.method.label': 'M\u00e9thode',
      'about.card.method.title': 'Partir du terrain, puis cadrer',
      'about.card.sources.body': 'Quand une citation, une datation, un nom d\u2019auteur ou une adresse sont suffisamment \u00e9tablis, ils sont int\u00e9gr\u00e9s au corpus. Les r\u00e9f\u00e9rences les plus utiles apparaissent dans les articles; le reste n\u2019est pas surjou\u00e9.',
      'about.card.sources.label': 'Sources',
      'about.card.sources.title': 'Des appuis choisis, pas un appareil de notes',
      'about.cta.aria': 'Contacter le projet sur Instagram',
      'about.cta.label': 'Contact \u00e9ditorial',
      'about.cta.text': 'Instagram prolonge le site par les photographies, les rep\u00e9rages et les notations de terrain. C\u2019est aussi le canal de contact \u00e9ditorial le plus direct pour une correction, une pr\u00e9cision factuelle ou un cr\u00e9dit \u00e0 compl\u00e9ter.',
      'about.footer.body': 'Une publication d\u2019auteur consacr\u00e9e aux fa\u00e7ades, aux mati\u00e8res et aux formes qui persistent dans les villes europ\u00e9ennes.',
      'about.footer.facades': 'Fa\u00e7ades',
      'about.footer.landmarks': 'Rep\u00e8res',
      'about.footer.navigation': 'Navigation',
      'about.hero.paragraph1': 'Ce site vient d\u2019une habitude de regard plus que d\u2019un programme. En grandissant en Belgique, certains signes \u00e9taient d\u00e9j\u00e0 l\u00e0. Une porte plus travaill\u00e9e qu\u2019ailleurs, une verri\u00e8re aper\u00e7ue depuis le trottoir, un angle de fa\u00e7ade qui retenait la lumi\u00e8re d\u2019une mani\u00e8re singuli\u00e8re. Longtemps, ils ont pr\u00e9c\u00e9d\u00e9 les noms.',
      'about.hero.paragraph2': 'L\u2019Art Nouveau et l\u2019Art D\u00e9co sont entr\u00e9s ainsi, non comme des cat\u00e9gories savantes, mais comme une pr\u00e9sence diffuse dans la ville. Le site prolonge cette exp\u00e9rience. Il rassemble des lieux, des images et des notes qui essaient de rester fid\u00e8les au terrain, au rythme de la marche, \u00e0 ce que l\u2019\u0153il comprend avant m\u00eame que la documentation soit compl\u00e8te.',
      'about.hero.paragraph3': 'Il ne s\u2019agit pas de tout couvrir ni de transformer chaque sujet en d\u00e9monstration. Certaines pages tiennent par un b\u00e2timent majeur, d\u2019autres par une simple fa\u00e7ade ou par un d\u00e9tail qui r\u00e9oriente la rue. Cette variation fait partie du projet. Elle permet de garder une \u00e9chelle juste, et de ne pas demander plus aux images qu\u2019elles ne donnent r\u00e9ellement.',
      'about.hero.paragraph4': 'Le texte intervient alors pour clarifier, pour relier, parfois pour laisser une m\u00e9moire s\u2019installer. Pas pour combler. Quand une donn\u00e9e manque, elle reste \u00e0 confirmer. Quand un lieu r\u00e9siste, il garde sa part d\u2019ombre. C\u2019est \u00e0 ce prix que la voix du site peut rester stable.',
      'about.hero.title': 'Partir du d\u00e9tail, puis revenir \u00e0 la ville',
      'about.image.alt': 'Portrait de l\u2019auteur du projet Art Nouveau et Art D\u00e9co',
      'about.meta.description': 'Pourquoi ce site existe, comment il regarde les villes, et ce qu\u2019il cherche \u00e0 pr\u00e9server dans les d\u00e9tails d\u2019Art Nouveau et d\u2019Art D\u00e9co.',
      'about.meta.title': '\u00c0 propos \u00b7 Art Nouveau et Art D\u00e9co en Europe',
      'about.trust.label': 'M\u00e9thode \u00e9ditoriale',
      'about.trust.lede': 'Le site reste une publication d\u2019auteur. Il ne cherche pas \u00e0 mimer une institution, mais \u00e0 rendre visibles quelques rep\u00e8res simples: ce qui est observ\u00e9, ce qui est v\u00e9rifi\u00e9, ce qui reste encore \u00e0 confirmer.',
      'about.trust.title': 'Une rigueur factuelle discr\u00e8te, sans appareil inutile',
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
      'nav.language': 'Langue de preview',
      'nav.menu': 'Menu',
      'nav.open': 'Ouvrir le menu',
      'mentions.contact.body': 'Pour une pr\u00e9cision factuelle, une correction utile ou un signalement li\u00e9 \u00e0 une image, le canal de contact \u00e9ditorial est <a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener noreferrer">@artnouveauetdeco</a>.',
      'mentions.contact.label': 'Contact',
      'mentions.contact.title': 'Point de contact \u00e9ditorial',
      'mentions.content.body': 'Le site publie des textes d\u2019auteur, des photographies et des rep\u00e9rages consacr\u00e9s \u00e0 l\u2019Art Nouveau et \u00e0 l\u2019Art D\u00e9co. Les informations factuelles sont int\u00e9gr\u00e9es avec prudence et signal\u00e9es comme telles lorsqu\u2019elles restent \u00e0 confirmer.',
      'mentions.content.label': 'Contenu',
      'mentions.content.title': 'Textes et images',
      'mentions.hero.title': 'Un cadre simple, lisible, sans appareil inutile',
      'mentions.meta.description': 'Informations minimales de publication, contact \u00e9ditorial et cadre d\u2019usage du site Art Nouveau et Art D\u00e9co en Europe.',
      'mentions.meta.title': 'Mentions et contact \u00b7 Art Nouveau et Art D\u00e9co en Europe',
      'mentions.nav.label': 'Mentions',
      'mentions.publication.body': 'Art Nouveau et Art D\u00e9co en Europe est une publication d\u2019auteur port\u00e9e par Antoine Aspeel.',
      'mentions.publication.label': 'Publication',
      'mentions.publication.title': '\u00c9diteur du site',
      'mentions.usage.body': 'Pour toute demande relative \u00e0 un texte, \u00e0 une image ou \u00e0 un cr\u00e9dit, merci d\u2019utiliser le contact \u00e9ditorial ci-dessus afin qu\u2019un \u00e9change direct soit possible.',
      'mentions.usage.label': 'Usage',
      'mentions.usage.title': 'Reprises et signalements',
      'error404.body': 'La page demand\u00e9e n\u2019est pas disponible ou l\u2019adresse n\u2019est plus la bonne.',
      'error404.cta': 'Revenir \u00e0 l\u2019accueil',
      'error404.meta.description': 'Cette page n\u2019existe pas ou n\u2019est plus disponible.',
      'error404.meta.title': 'Page introuvable \u00b7 Art Nouveau et Art D\u00e9co',
      'error404.title': 'Page introuvable',
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
      'article.map.open': 'Open in Google Maps',
      'article.map.openFor': 'Open this address in Google Maps: {address}',
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
      'about.aside.aria': 'Editorial position',
      'about.aside.text': 'What I try to preserve here is a calm precision: enough context to guide the eye, enough restraint to let the place keep its own density.',
      'about.card.corrections.body': 'Useful factual notes, sourced corrections, or image credits to complete can be sent through Instagram. The project\u2019s editorial contact point remains deliberately simple: <a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener noreferrer">@artnouveauetdeco</a>.',
      'about.card.corrections.label': 'Corrections',
      'about.card.corrections.title': 'Correct without weighing things down',
      'about.card.limits.body': 'Some information remains partial. In that case, it stays marked as needing confirmation. The site prefers an explicit gap to uncertain precision.',
      'about.card.limits.label': 'Limits',
      'about.card.limits.title': 'Do not fill what is missing',
      'about.card.method.body': 'The texts begin with a street reading, a facade, a threshold, a detail that actually holds before the eye. The factual markers visible in the articles are added when they can be maintained clearly.',
      'about.card.method.label': 'Method',
      'about.card.method.title': 'Start from the field, then frame',
      'about.card.sources.body': 'When a quotation, date, author name, or address is sufficiently established, it is integrated into the corpus. The most useful references appear in the articles; the rest is not overstated.',
      'about.card.sources.label': 'Sources',
      'about.card.sources.title': 'Selected supports, not an apparatus of notes',
      'about.cta.aria': 'Contact the project on Instagram',
      'about.cta.label': 'Editorial contact',
      'about.cta.text': 'Instagram extends the site through photographs, field notes, and observations. It is also the most direct editorial contact channel for a correction, a factual precision, or an image credit to complete.',
      'about.footer.body': 'An author-led publication devoted to the facades, materials, and forms that persist in European cities.',
      'about.footer.facades': 'Facades',
      'about.footer.landmarks': 'Markers',
      'about.footer.navigation': 'Navigation',
      'about.hero.paragraph1': 'This site comes from a habit of looking more than from a program. Growing up in Belgium, certain signs were already there: a doorway more worked than others, a glass canopy glimpsed from the pavement, a facade corner holding the light in a singular way. For a long time, they came before the names.',
      'about.hero.paragraph2': 'Art Nouveau and Art Deco entered in that way, not as scholarly categories, but as a diffuse presence in the city. The site extends that experience. It gathers places, images, and notes that try to stay faithful to the ground, to the rhythm of walking, to what the eye understands before the documentation is complete.',
      'about.hero.paragraph3': 'The aim is not to cover everything or turn every subject into a demonstration. Some pages are held by a major building, others by a simple facade or by a detail that redirects the street. That variation is part of the project. It keeps the scale right, and avoids asking more from the images than they can really give.',
      'about.hero.paragraph4': 'Text then steps in to clarify, to connect, sometimes to let a memory settle. Not to fill gaps. When a fact is missing, it remains to be confirmed. When a place resists, it keeps its shadow. That is how the site\u2019s voice can remain steady.',
      'about.hero.title': 'Start from the detail, then return to the city',
      'about.image.alt': 'Portrait of the author of the Art Nouveau and Art Deco project',
      'about.meta.description': 'Why this site exists, how it looks at cities, and what it tries to preserve in Art Nouveau and Art Deco details.',
      'about.meta.title': 'About \u00b7 Art Nouveau and Art Deco in Europe',
      'about.trust.label': 'Editorial method',
      'about.trust.lede': 'The site remains an author-led publication. It does not try to imitate an institution, but to make a few simple markers visible: what is observed, what is verified, and what still needs confirmation.',
      'about.trust.title': 'Discreet factual rigor, without unnecessary apparatus',
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
      'nav.language': 'Preview language',
      'nav.menu': 'Menu',
      'nav.open': 'Open menu',
      'mentions.contact.body': 'For a factual clarification, a useful correction, or a note about an image, the editorial contact channel is <a href="https://www.instagram.com/artnouveauetdeco" target="_blank" rel="noopener noreferrer">@artnouveauetdeco</a>.',
      'mentions.contact.label': 'Contact',
      'mentions.contact.title': 'Editorial contact point',
      'mentions.content.body': 'The site publishes author-written texts, photographs, and field notes devoted to Art Nouveau and Art Deco. Factual information is added with care and marked as such when it still needs confirmation.',
      'mentions.content.label': 'Content',
      'mentions.content.title': 'Texts and images',
      'mentions.hero.title': 'A simple, readable frame, without unnecessary apparatus',
      'mentions.meta.description': 'Minimal publication information, editorial contact, and usage frame for the Art Nouveau and Art Deco in Europe site.',
      'mentions.meta.title': 'Legal notice and contact \u00b7 Art Nouveau and Art Deco in Europe',
      'mentions.nav.label': 'Legal',
      'mentions.publication.body': 'Art Nouveau and Art Deco in Europe is an author-led publication by Antoine Aspeel.',
      'mentions.publication.label': 'Publication',
      'mentions.publication.title': 'Site publisher',
      'mentions.usage.body': 'For any request about a text, an image, or a credit, please use the editorial contact above so a direct exchange remains possible.',
      'mentions.usage.label': 'Use',
      'mentions.usage.title': 'Reuse and notices',
      'error404.body': 'The requested page is not available, or the address is no longer correct.',
      'error404.cta': 'Back to home',
      'error404.meta.description': 'This page does not exist or is no longer available.',
      'error404.meta.title': 'Page not found \u00b7 Art Nouveau and Art Deco',
      'error404.title': 'Page not found',
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

  function previewLocaleHref(locale) {
    const requested = supportedLocale(locale);
    const url = new URL(window.location.href);

    if (requested && requested !== DEFAULT_LOCALE) {
      url.searchParams.set(PREVIEW_LOCALE_PARAM, requested);
    } else {
      url.searchParams.delete(PREVIEW_LOCALE_PARAM);
    }

    const page = url.pathname.split('/').pop() || 'index.html';
    return page + url.search + url.hash;
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
    previewLocaleHref,
    resolveLocale,
    t,
    articleCountLabel,
    withPreviewLocale,
  };
})(window);
