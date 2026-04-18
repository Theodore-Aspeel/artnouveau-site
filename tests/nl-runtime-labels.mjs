import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

function runBrowserScript(filePath, context) {
  vm.runInNewContext(fs.readFileSync(filePath, 'utf8'), context);
}

function plain(value) {
  return JSON.parse(JSON.stringify(value));
}

const context = {
  URLSearchParams,
  window: {
    location: {
      search: '?previewLocale=nl',
      href: 'https://example.test/index.html?previewLocale=nl',
    },
  },
  document: {
    documentElement: {
      getAttribute(name) {
        return name === 'lang' ? 'fr' : '';
      },
    },
  },
};

runBrowserScript('src/assets/scripts/locale-config.js', context);
runBrowserScript('src/assets/scripts/article-access.js', context);
runBrowserScript('src/assets/scripts/i18n.js', context);

const locales = context.window.SiteLocales;
const access = context.window.ArticleAccess;
const i18n = context.window.SiteI18n;

assert.deepEqual(plain(locales.previewLocaleCodes()), ['fr', 'en', 'nl']);
assert.equal(locales.supportedLocale('nl-BE'), 'nl');
assert.equal(i18n.previewLocale(), 'nl');
assert.equal(i18n.resolveLocale(), 'nl');

assert.equal(i18n.t('article.facts'), 'Kerngegevens');
assert.equal(i18n.t('gallery.all'), 'Alle');
assert.equal(i18n.articleCountLabel(1, 'nl'), 'artikel');
assert.equal(i18n.articleCountLabel(2, 'nl'), 'artikelen');
assert.equal(i18n.t('about.hero.title', null, 'nl'), 'Partir du d\u00e9tail, puis revenir \u00e0 la ville');

const v2Article = {
  taxonomy: {
    style_key: 'vienna_secession',
    tag_keys: ['public_building', 'urban_lettering', 'floral_motif'],
  },
  facts: {
    location: {
      city: 'Brussel',
      country: 'Belgi\u00eb',
      address: '1 Teststraat',
    },
    dates: { built: '1901' },
    people: [{ role: 'architect', name: 'Demo Architect' }],
  },
  relations: {
    around: {
      relation_key: 'same_city',
      article_slug: 'demo',
    },
  },
  content: {
    fr: {
      title: 'Titre de test',
      practical_items: [
        { key: 'city', value: 'Brussel' },
        { key: 'style' },
        { key: 'architect' },
        { key: 'address' },
        { key: 'date' },
      ],
      around: { note: 'Note fran\u00e7aise' },
    },
  },
};

assert.deepEqual(plain(access.getArticleTaxonomy(v2Article, 'nl')), {
  styleKey: 'vienna_secession',
  styleLabel: 'Weense Secessie',
  tagKeys: ['public_building', 'urban_lettering', 'floral_motif'],
  tagLabels: ['Openbaar gebouw', 'Stedelijke belettering', 'Bloemmotief'],
  city: 'Brussel',
  country: 'Belgi\u00eb',
  countryCode: '',
});

assert.deepEqual(
  plain(access.getArticlePracticalItems(v2Article, 'nl').map((item) => [item.key, item.label, item.value])),
  [
    ['city', 'Stad', 'Brussel'],
    ['style', 'Stijl', 'Weense Secessie'],
    ['architect', 'Architect', 'Demo Architect'],
    ['address', 'Adres', '1 Teststraat'],
    ['date', 'Datering', '1901'],
  ]
);

assert.equal(access.getArticleAround(v2Article, 'nl').relationLabel, 'Zelfde stad');
assert.equal(access.getArticleAround(v2Article, 'nl').note, 'Note fran\u00e7aise');

const v1Article = {
  style: 'Art Nouveau',
  tags: ['Art Nouveau'],
  practical: {
    Ville: 'Lille',
    Pays: 'France',
    Adresse: '14 rue de Fleurus',
    Acc\u00e8s: 'Ext\u00e9rieur',
  },
};

assert.deepEqual(
  plain(access.getArticlePracticalItems(v1Article, 'nl').map((item) => [item.key, item.label])),
  [
    ['city', 'Stad'],
    ['country', 'Land'],
    ['address', 'Adres'],
    ['access', 'Toegang'],
  ]
);

assert.equal(access.localizedValue({ fr: 'Texte fran\u00e7ais' }, 'nl'), 'Texte fran\u00e7ais');
