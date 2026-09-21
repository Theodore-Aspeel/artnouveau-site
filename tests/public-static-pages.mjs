import assert from 'node:assert/strict';
import fs from 'node:fs';

const articleData = JSON.parse(fs.readFileSync('src/data/articles.json', 'utf8'));
const publicLocales = ['fr', 'en', 'nl'];
const galleryScript = fs.readFileSync('src/assets/scripts/gallery.js', 'utf8');
const articleTemplateScript = fs.readFileSync('src/assets/scripts/article-template.js', 'utf8');
const publicBasePath = normalizePublicBasePath(process.env.PUBLIC_BASE_PATH || '');
const siteOrigin = (process.env.SITE_ORIGIN || 'https://artnouveauetdeco.com').replace(/\/+$/, '');

const EXPECTED_PAGES = [
  ['fr', 'home', 'dist/fr/index.html', 'Regarder d\u2019abord. Nommer ensuite.'],
  ['en', 'home', 'dist/en/index.html', 'Look first. Name later.'],
  ['nl', 'home', 'dist/nl/index.html', 'Eerst kijken. Daarna benoemen.'],
  ['fr', 'about', 'dist/fr/about/index.html', 'Christophe Aspel, un regard d\u2019auteur sur les villes'],
  ['en', 'about', 'dist/en/about/index.html', 'Christophe Aspel, an author\u2019s eye on cities'],
  ['nl', 'about', 'dist/nl/about/index.html', 'Christophe Aspel, een auteursblik op steden'],
  ['fr', 'mentions', 'dist/fr/mentions/index.html', 'Un cadre simple, lisible, sans appareil inutile'],
  ['en', 'mentions', 'dist/en/mentions/index.html', 'A simple, readable frame, without unnecessary apparatus'],
  ['nl', 'mentions', 'dist/nl/mentions/index.html', 'Een eenvoudig en leesbaar kader, zonder overbodig apparaat'],
];

const PORTFOLIO_ITEMS = [
  { slug: 'maison-coilliot-lille-hector-guimard', image: 'maison-coilliot-facade-complete-christophe-aspel.jpg' },
  { slug: 'maison-aux-tulipes-bratislava-jeno-schiller', image: 'maison-aux-tulipes-bratislava-jeno-schiller.png' },
  { slug: 'aquarium-de-milan-1906', image: 'aquarium-de-milan-1906.png' },
];

const ABOUT_METADATA = {
  fr: ['Christophe Aspel, auteur-photographe \u00b7 Portfolio', 'Christophe Aspel, auteur-photographe, pr\u00e9sente son portfolio de fa\u00e7ades et de d\u00e9tails d\u2019Art Nouveau et d\u2019Art D\u00e9co en Europe.'],
  en: ['Christophe Aspel, author-photographer \u00b7 Portfolio', 'Christophe Aspel, author-photographer, presents his portfolio of Art Nouveau and Art Deco facades and details across Europe.'],
  nl: ['Christophe Aspel, auteur-fotograaf \u00b7 Portfolio', 'Christophe Aspel, auteur-fotograaf, presenteert zijn portfolio met gevels en details van art nouveau en art deco in Europa.'],
};

assert.ok(
  fs.readFileSync('dist/about.html', 'utf8').includes('data-asset-base=""'),
  'legacy About should resolve responsive assets from the dist root'
);

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll('"', '&quot;');
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function normalizePublicBasePath(value) {
  const normalized = typeof value === 'string' ? value.trim() : '';
  if (!normalized || normalized === '/') return '';
  return '/' + normalized.replace(/^\/+|\/+$/g, '');
}

function publicRoute(pathname) {
  return `${publicBasePath}${pathname}`;
}

function absolutePublicUrl(pathname) {
  return `${siteOrigin}${publicRoute(pathname)}`;
}

function localeContent(article, locale) {
  return article.content?.[locale] || article.content?.fr || {};
}

for (const [locale, routeName, filePath, expectedText] of EXPECTED_PAGES) {
  assert.ok(fs.existsSync(filePath), `${filePath} should be generated`);

  const html = fs.readFileSync(filePath, 'utf8');
  assert.match(html, new RegExp(`<html lang="${locale}">`), `${filePath} should set the HTML language`);
  assert.ok(html.includes(expectedText), `${filePath} should include localized ${locale} ${routeName} content`);
  assert.match(html, /<meta name="robots" content="index,follow">/, `${filePath} should be indexable`);
  assert.ok(
    html.includes(`<link rel="canonical" href="${absolutePublicUrl(`/${locale}/${routeName === 'home' ? '' : `${routeName}/`}`)}">`),
    `${filePath} should expose an absolute canonical URL`
  );
  assert.ok(
    html.includes(`<meta property="og:url" content="${absolutePublicUrl(`/${locale}/${routeName === 'home' ? '' : `${routeName}/`}`)}">`),
    `${filePath} should expose an absolute og:url`
  );
  assert.ok(html.includes(`href="${publicRoute('/favicon.ico')}"`), `${filePath} should use the deployment path for favicon.ico`);
  assert.ok(html.includes(`href="${publicRoute('/icon.svg')}"`), `${filePath} should use the deployment path for icon.svg`);
  assert.ok(html.includes(`href="${publicRoute('/icon.png')}"`), `${filePath} should use the deployment path for icon.png`);
  assert.doesNotMatch(html, /previewLocale=/, `${filePath} should not use previewLocale links`);
}

for (const filePath of ['dist/index.html', 'dist/about.html', 'dist/mentions.html', 'dist/article.html']) {
  const html = fs.readFileSync(filePath, 'utf8');
  assert.match(html, /<meta name="robots" content="noindex,follow">/, `${filePath} should not compete with public routes`);
  assert.doesNotMatch(html, /rel="canonical"/, `${filePath} should not claim a canonical public route`);
  assert.ok(html.includes(`href="${publicRoute('/favicon.ico')}"`), `${filePath} should use the deployment path for favicon.ico`);
  assert.ok(html.includes(`href="${publicRoute('/icon.svg')}"`), `${filePath} should use the deployment path for icon.svg`);
  assert.ok(html.includes(`href="${publicRoute('/icon.png')}"`), `${filePath} should use the deployment path for icon.png`);
}

assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /data-article-data-url="\.\.\/data\/articles\.json"/);
assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /data-asset-base="\.\.\/"/);
assert.match(fs.readFileSync('dist/fr/about/index.html', 'utf8'), new RegExp(`href="${escapeRegExp(publicRoute('/fr/'))}"`));
assert.match(fs.readFileSync('dist/en/about/index.html', 'utf8'), new RegExp(`href="${escapeRegExp(publicRoute('/en/mentions/'))}"`));
assert.match(fs.readFileSync('dist/nl/mentions/index.html', 'utf8'), new RegExp(`href="${escapeRegExp(publicRoute('/nl/about/'))}"`));
assert.ok(
  fs.readFileSync('dist/fr/mentions/index.html', 'utf8').includes(
    'Les photographies publiées sont des œuvres originales de Christophe Aspel.'
  ),
  'French legal notice should identify the original text and photography author'
);
assert.ok(
  fs.readFileSync('dist/en/mentions/index.html', 'utf8').includes(
    'The published photographs are original works by Christophe Aspel.'
  ),
  'English legal notice should identify the original text and photography author'
);
assert.ok(
  fs.readFileSync('dist/nl/mentions/index.html', 'utf8').includes(
    'De gepubliceerde foto’s zijn originele werken van Christophe Aspel.'
  ),
  'Dutch legal notice should identify the original text and photography author'
);

assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /<script src="\.\.\/assets\/scripts\/public-routes\.js"><\/script>/);
assert.ok(
  fs.readFileSync('dist/fr/index.html', 'utf8').includes(
    `<script>window.SiteDeployment=${JSON.stringify({ publicBasePath })};</script>`
  ),
  'public home should expose the deployment base path before route helpers'
);
assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /<script src="\.\.\/assets\/scripts\/image-manifest\.js"><\/script>/);
assert.match(fs.readFileSync('dist/fr/index.html', 'utf8'), /data-responsive-image-source="assets\/images\/site\/saint-gilles-brussels\.png"/);
assert.match(galleryScript, /publicRoutes\.article\(currentLocale\(\), normalizedSlug\)/);
assert.match(galleryScript, /publicRoutes\.home\(currentLocale\(\)\)/);
assert.match(galleryScript, /SiteImageManifest/);
assert.match(articleTemplateScript, /bylineLink\.href = previewHref\(aboutHref\)/);
assert.match(articleTemplateScript, /aboutHref \+ '#portfolio'/);
assert.match(articleTemplateScript, /aboutHref \+ '#contact'/);

for (const locale of publicLocales) {
  const homeHtml = fs.readFileSync(`dist/${locale}/index.html`, 'utf8');
  assert.ok(homeHtml.includes(`href="${publicRoute(`/${locale}/`)}"`), `dist/${locale}/index.html should link to localized home`);
  assert.ok(homeHtml.includes(`href="${publicRoute(`/${locale}/about/`)}"`), `dist/${locale}/index.html should link to localized about`);
  assert.ok(homeHtml.includes(`href="${publicRoute(`/${locale}/mentions/`)}"`), `dist/${locale}/index.html should link to localized mentions`);
  assert.doesNotMatch(homeHtml, /href="(?:index|about|mentions)\.html/, `dist/${locale}/index.html should not target legacy page links`);
}

for (const locale of publicLocales) {
  const aboutHtml = fs.readFileSync(`dist/${locale}/about/index.html`, 'utf8');
  const [metaTitle, metaDescription] = ABOUT_METADATA[locale];
  assert.ok(aboutHtml.includes('id="portfolio"'), `dist/${locale}/about/index.html should expose the portfolio anchor`);
  assert.ok(aboutHtml.includes('id="demarche"'), `dist/${locale}/about/index.html should expose the process anchor`);
  assert.ok(aboutHtml.includes('id="contact"'), `dist/${locale}/about/index.html should expose the contact anchor`);
  assert.ok(aboutHtml.includes(`<title data-i18n="about.meta.title">${metaTitle}</title>`), `dist/${locale}/about/index.html should identify the author-photographer in its title`);
  assert.ok(aboutHtml.includes(`<meta name="description" content="${metaDescription}"`), `dist/${locale}/about/index.html should describe the photographic portfolio`);

  for (const anchor of ['portfolio', 'demarche', 'contact']) {
    assert.ok(
      aboutHtml.includes(`href="#${anchor}"`),
      `dist/${locale}/about/index.html should link its local navigation to #${anchor}`
    );
  }

  assert.ok(aboutHtml.includes('src="../../assets/scripts/image-manifest.js"'), `dist/${locale}/about/index.html should load the responsive image helper`);
  assert.ok(aboutHtml.includes('data-asset-base="../../"'), `dist/${locale}/about/index.html should expose the localized asset base`);

  for (const item of PORTFOLIO_ITEMS) {
    assert.ok(
      aboutHtml.includes(`href="${publicRoute(`/${locale}/articles/${item.slug}/`)}"`),
      `dist/${locale}/about/index.html should link ${item.slug} to its localized article route`
    );
    assert.ok(
      aboutHtml.includes(`src="../../assets/images/articles/${item.image}"`),
      `dist/${locale}/about/index.html should emit the localized portfolio image URL for ${item.image}`
    );
    assert.ok(
      aboutHtml.includes(`data-responsive-image-source="assets/images/articles/${item.image}"`),
      `dist/${locale}/about/index.html should register ${item.image} for responsive rendering`
    );
  }
}

for (const locale of publicLocales) {
  for (const article of articleData.articles) {
    const filePath = `dist/${locale}/articles/${article.slug}/index.html`;
    assert.ok(fs.existsSync(filePath), `${filePath} should be generated`);
  }
}

const sampleArticle = articleData.articles.find((article) => article.slug === 'maison-coilliot-lille-hector-guimard');
assert.ok(sampleArticle, 'sample article should exist');

for (const locale of publicLocales) {
  const filePath = `dist/${locale}/articles/${sampleArticle.slug}/index.html`;
  const html = fs.readFileSync(filePath, 'utf8');
  const content = localeContent(sampleArticle, locale);
  const expectedTitle = `${content.title} · Art Nouveau et Art Déco`;
  const expectedDescription = content.seo.meta_description;

  assert.match(html, new RegExp(`<html lang="${locale}">`), `${filePath} should set article HTML language`);
  assert.ok(html.includes(`<title id="page-title">${escapeHtml(expectedTitle)}</title>`), `${filePath} should include final title`);
  assert.ok(
    html.includes(`<meta id="page-description" name="description" content="${escapeAttribute(expectedDescription)}">`),
    `${filePath} should include final meta description`
  );
  assert.ok(
    html.includes(`<meta id="og-title" property="og:title" content="${escapeAttribute(expectedTitle)}">`),
    `${filePath} should include final og:title`
  );
  assert.ok(
    html.includes(`<meta id="og-description" property="og:description" content="${escapeAttribute(expectedDescription)}">`),
    `${filePath} should include final og:description`
  );
  assert.ok(
    html.includes(`<meta id="twitter-title" name="twitter:title" content="${escapeAttribute(expectedTitle)}">`),
    `${filePath} should include final twitter:title`
  );
  assert.ok(
    html.includes(`<meta id="twitter-description" name="twitter:description" content="${escapeAttribute(expectedDescription)}">`),
    `${filePath} should include final twitter:description`
  );
  assert.ok(
    html.includes(`<meta property="og:image" content="${absolutePublicUrl('/assets/images/articles/maison-coilliot-facade-complete-christophe-aspel.jpg')}">`),
    `${filePath} should expose an absolute og:image URL`
  );
  assert.ok(
    html.includes(`<meta property="og:url" content="${absolutePublicUrl(`/${locale}/articles/${sampleArticle.slug}/`)}">`),
    `${filePath} should expose an absolute og:url`
  );
  assert.match(
    html,
    new RegExp(`<meta name="robots" content="${sampleArticle.status === 'published' ? 'index,follow' : 'noindex,follow'}">`),
    `${filePath} robots directive should follow the article publication status`
  );
  assert.ok(html.includes(`href="${publicRoute('/favicon.ico')}"`), `${filePath} should use the deployment path for favicon.ico`);
  assert.ok(html.includes(`data-article-slug="${sampleArticle.slug}"`), `${filePath} should pass the slug without query parameters`);
  assert.ok(
    html.includes(`data-about-href="${publicRoute(`/${locale}/about/`)}"`),
    `${filePath} should pass the localized author and portfolio route to the renderer`
  );
  assert.ok(html.includes(`href="${publicRoute(`/${locale}/articles/${sampleArticle.slug}/`)}"`), `${filePath} should link to its public route`);
  assert.ok(html.includes(`src="../../../assets/scripts/image-manifest.js"`), `${filePath} should load the image manifest helper`);
  assert.ok(html.includes(`href="${publicRoute(`/fr/articles/${sampleArticle.slug}/`)}"`), `${filePath} should keep article context for FR language link`);
  assert.ok(html.includes(`href="${publicRoute(`/en/articles/${sampleArticle.slug}/`)}"`), `${filePath} should keep article context for EN language link`);
  assert.ok(html.includes(`href="${publicRoute(`/nl/articles/${sampleArticle.slug}/`)}"`), `${filePath} should keep article context for NL language link`);
  assert.doesNotMatch(html, /Chargement/, `${filePath} should not keep loading SEO title text`);
  assert.doesNotMatch(html, /previewLocale=/, `${filePath} should not use previewLocale links`);
}
