import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync('src/assets/scripts/article-access.js', 'utf8');
const context = { window: {} };
vm.runInNewContext(source, context);

const access = context.window.ArticleAccess;

assert.equal(typeof access.getArticleMapLink, 'function');

const articleWithAddress = {
  taxonomy: { style_key: 'art_nouveau' },
  facts: { location: { city: 'Lille', country: 'France' } },
  content: {
    fr: {
      practical_items: [
        { key: 'city', value: 'Lille' },
        { key: 'address', value: '14 rue de Fleurus' },
      ],
    },
  },
};

const mapLink = access.getArticleMapLink(articleWithAddress, 'fr');
assert.equal(mapLink.address, '14 rue de Fleurus');
assert.equal(mapLink.href, 'https://www.google.com/maps/search/14%20rue%20de%20Fleurus%2C%20Lille%2C%20France');
assert.equal(mapLink.embedHref, 'https://www.google.com/maps?q=14%20rue%20de%20Fleurus%2C%20Lille%2C%20France&output=embed');

const articleWithoutAddress = {
  facts: { location: { city: 'Charleroi', country: 'Belgique' } },
  content: { fr: { practical_items: [{ key: 'city', value: 'Charleroi' }] } },
};

assert.equal(access.getArticleMapLink(articleWithoutAddress, 'fr'), null);

const articleWithUnconfirmedAddress = {
  facts: { location: { city: 'Charleroi', country: 'Belgique' } },
  content: { fr: { practical_items: [{ key: 'address', value: 'A confirmer' }] } },
};

assert.equal(access.getArticleMapLink(articleWithUnconfirmedAddress, 'fr'), null);

const articleWithTooShortAddress = {
  content: { fr: { practical_items: [{ key: 'address', value: 'Lille' }] } },
};

assert.equal(access.getArticleMapLink(articleWithTooShortAddress, 'fr'), null);
