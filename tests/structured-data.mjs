import assert from 'node:assert/strict';
import fs from 'node:fs';
import test from 'node:test';
import {
  buildArticleStructuredData,
  renderStructuredDataScript,
  serializeStructuredData,
} from '../scripts/structured-data.mjs';

const siteOrigin = (process.env.SITE_ORIGIN || 'https://artnouveauetdeco.com').replace(/\/+$/, '');
const rawBasePath = (process.env.PUBLIC_BASE_PATH || '').trim();
const publicBasePath = rawBasePath && rawBasePath !== '/'
  ? `/${rawBasePath.replace(/^\/+|\/+$/g, '')}`
  : '';

const access = {
  isArticleLocaleReady(article, locale) {
    const content = article.content?.[locale];
    return Boolean(content?.title && content?.dek && content?.sections?.length);
  },
  getArticleTitle(article, locale) {
    return article.content?.[locale]?.title || article.content?.fr?.title || article.title || '';
  },
  getArticleMetaDescription(article, locale) {
    return article.content?.[locale]?.seo?.meta_description
      || article.content?.fr?.seo?.meta_description
      || article.meta_description
      || '';
  },
};

function articleFixture(overrides = {}) {
  return {
    schema_version: 2,
    identity: { type: 'building', canonical_name: 'Maison Démo' },
    facts: {
      location: {
        address: '14 rue de Fleurus, Lille',
        city: 'Lille',
        country: 'France',
        country_code: 'FR',
      },
    },
    editorial: { author: 'Christophe Aspel' },
    publication: { published_on: null, updated_on: null },
    content: {
      fr: {
        title: 'Maison Démo',
        dek: 'Introduction française.',
        sections: [{ heading: 'Lire', body: 'Texte.' }],
        seo: { meta_description: 'Description française.' },
      },
      en: {
        title: 'Demo House',
        dek: 'English introduction.',
        sections: [{ heading: 'Read', body: 'Text.' }],
        seo: { meta_description: 'English description.' },
      },
    },
    ...overrides,
  };
}

function build(article = articleFixture(), locale = 'en') {
  return buildArticleStructuredData({
    article,
    locale,
    canonicalUrl: `https://example.test/${locale}/articles/demo/`,
    imageUrl: 'https://example.test/assets/images/demo.png',
    access,
  });
}

test('builds a minimal Article and Place graph from stable fields', () => {
  const data = build();
  assert.equal(data['@context'], 'https://schema.org');
  assert.equal(data['@graph'].length, 2);

  const [article, place] = data['@graph'];
  assert.deepEqual(article, {
    '@type': 'Article',
    '@id': 'https://example.test/en/articles/demo/#article',
    url: 'https://example.test/en/articles/demo/',
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': 'https://example.test/en/articles/demo/',
    },
    headline: 'Demo House',
    description: 'English description.',
    inLanguage: 'en',
    image: 'https://example.test/assets/images/demo.png',
    author: { '@type': 'Person', name: 'Christophe Aspel' },
    about: { '@id': 'https://example.test/en/articles/demo/#place' },
  });
  assert.deepEqual(place, {
    '@type': 'Place',
    '@id': 'https://example.test/en/articles/demo/#place',
    name: 'Maison Démo',
    address: {
      '@type': 'PostalAddress',
      streetAddress: '14 rue de Fleurus, Lille',
      addressLocality: 'Lille',
      addressCountry: 'FR',
    },
  });
  assert.equal('datePublished' in article, false);
  assert.equal('dateModified' in article, false);
});

test('emits only valid publication dates and never reuses a building date', () => {
  const data = build(articleFixture({
    facts: { dates: { built: '1898 ; 1900' } },
    publication: {
      published_on: '2026-09-16',
      updated_on: '2026-02-31',
    },
  }));
  const article = data['@graph'][0];
  assert.equal(article.datePublished, '2026-09-16');
  assert.equal('dateModified' in article, false);
  assert.doesNotMatch(JSON.stringify(article), /1898|1900/);
});

test('omits absent author and supports partial addresses', () => {
  const data = build(articleFixture({
    editorial: {},
    facts: { location: { city: 'Charleroi', country: 'Belgique', country_code: 'BE' } },
  }));
  const [article, place] = data['@graph'];
  assert.equal('author' in article, false);
  assert.deepEqual(place.address, {
    '@type': 'PostalAddress',
    addressLocality: 'Charleroi',
    addressCountry: 'BE',
  });
});

test('declares French when a requested locale is not editorially ready', () => {
  const data = build(articleFixture(), 'nl');
  const article = data['@graph'][0];
  assert.equal(article.inLanguage, 'fr');
  assert.equal(article.headline, 'Maison Démo');
  assert.equal(article.description, 'Description française.');
});

test('supports a legacy verified place without inventing one', () => {
  const legacy = {
    title: 'Legacy article',
    meta_description: 'Legacy description.',
    verified_info: { exact_name: 'Legacy place' },
  };
  const data = buildArticleStructuredData({
    article: legacy,
    locale: 'fr',
    canonicalUrl: 'https://example.test/fr/articles/legacy/',
    access,
  });
  assert.equal(data['@graph'][1].name, 'Legacy place');

  const withoutVerifiedPlace = buildArticleStructuredData({
    article: { title: 'Unverified legacy article' },
    locale: 'fr',
    canonicalUrl: 'https://example.test/fr/articles/unverified/',
    access,
  });
  assert.equal(withoutVerifiedPlace['@graph'].length, 1);
  assert.equal('about' in withoutVerifiedPlace['@graph'][0], false);
});

test('serializes safely and deterministically inside a script element', () => {
  const value = { text: '</script><script>alert(1)</script>\u2028next\u2029line' };
  const first = serializeStructuredData(value);
  const second = serializeStructuredData(value);
  assert.equal(first, second);
  assert.doesNotMatch(first, /</);
  assert.match(first, /\\u003c\/script>/);
  assert.match(first, /\\u2028/);
  assert.match(first, /\\u2029/);
  assert.equal(JSON.parse(first).text, value.text);
  assert.equal(renderStructuredDataScript(null), '');
});

test('generates one parseable graph on every canonical article page only', () => {
  const locales = ['fr', 'en', 'nl'];
  const articles = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8')).articles;

  for (const locale of locales) {
    for (const article of articles) {
      const filePath = `dist/${locale}/articles/${article.slug}/index.html`;
      const html = fs.readFileSync(filePath, 'utf8');
      const matches = [...html.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
      assert.equal(matches.length, 1, `${filePath} should contain exactly one JSON-LD graph`);
      const data = JSON.parse(matches[0][1]);
      const articleNode = data['@graph'][0];
      const canonicalUrl = `${siteOrigin}${publicBasePath}/${locale}/articles/${article.slug}/`;
      const heroPath = article.media?.hero?.src || article.hero_image || '';
      assert.equal(articleNode['@type'], 'Article');
      assert.equal(articleNode.author?.name, 'Christophe Aspel');
      assert.equal(articleNode.inLanguage, locale);
      assert.equal(articleNode.url, canonicalUrl);
      assert.equal(articleNode['@id'], `${canonicalUrl}#article`);
      assert.equal(articleNode.mainEntityOfPage?.['@id'], canonicalUrl);
      if (heroPath) {
        assert.equal(articleNode.image, `${siteOrigin}${publicBasePath}/${heroPath.replace(/^\/+/, '')}`);
      }
      assert.equal('datePublished' in articleNode, false);
      assert.equal('dateModified' in articleNode, false);
    }
  }

  for (const filePath of ['dist/article.html', 'dist/articles/template.html']) {
    const html = fs.readFileSync(filePath, 'utf8');
    assert.doesNotMatch(html, /application\/ld\+json/, `${filePath} should not expose article structured data`);
  }
});
