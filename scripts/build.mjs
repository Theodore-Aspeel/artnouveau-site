import fs from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { validateProject } from './validate-content.mjs';
import {
  collectPublishedImagePaths,
  copyPublishedImages,
  generateImageManifest,
} from './image-pipeline.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');

const PAGE_JOBS = [
  { from: 'src/pages/index.html', to: 'index.html' },
  { from: 'src/pages/about.html', to: 'about.html' },
  { from: 'src/pages/mentions.html', to: 'mentions.html' },
  { from: 'src/pages/404.html', to: '404.html' },
  { from: 'src/pages/article-redirect.html', to: 'article.html' },
  { from: 'src/pages/articles/template.html', to: 'articles/template.html' },
];

const SIMPLE_PUBLIC_PAGE_JOBS = [
  { routeName: 'home', from: 'src/pages/index.html' },
  { routeName: 'about', from: 'src/pages/about.html' },
  { routeName: 'mentions', from: 'src/pages/mentions.html' },
];

const ARTICLE_PUBLIC_PAGE = { routeName: 'article', from: 'src/pages/article-redirect.html' };

const PUBLIC_IMAGE_SOURCE_PAGES = [
  ...SIMPLE_PUBLIC_PAGE_JOBS.map((job) => job.from),
  ARTICLE_PUBLIC_PAGE.from,
];

const COPY_JOBS = [
  { from: 'src/assets/styles', to: 'assets/styles' },
  { from: 'src/assets/fonts', to: 'assets/fonts' },
  { from: 'src/assets/scripts', to: 'assets/scripts' },
  { from: 'src/data', to: 'data' },
  { from: 'public', to: '.' },
];

const OG_LOCALES = {
  fr: 'fr_FR',
  en: 'en_US',
  nl: 'nl_NL',
};

const SITE_TITLE = 'Art Nouveau et Art Déco';
const SITE_ORIGIN = normalizeSiteOrigin(process.env.SITE_ORIGIN || 'https://artnouveauetdeco.com');
const ANALYTICS = getAnalyticsConfig(process.env);

function rewritePageForDist(relativeTargetPath, content) {
  if (relativeTargetPath === 'index.html') {
    return content
      .replaceAll('../assets/styles/main.css', 'assets/styles/main.css')
      .replaceAll('../assets/images/site/', 'assets/images/site/')
      .replaceAll('../assets/scripts/', 'assets/scripts/')
      .replaceAll("../data/articles.json", 'data/articles.json');
  }

  if (relativeTargetPath === 'about.html') {
    return content
      .replaceAll('../assets/styles/main.css', 'assets/styles/main.css')
      .replaceAll('../assets/images/site/', 'assets/images/site/')
      .replaceAll('../assets/scripts/', 'assets/scripts/');
  }

  if (relativeTargetPath === 'mentions.html') {
    return content
      .replaceAll('../assets/styles/main.css', 'assets/styles/main.css')
      .replaceAll('../assets/images/site/', 'assets/images/site/')
      .replaceAll('../assets/scripts/', 'assets/scripts/');
  }

  if (relativeTargetPath === '404.html') {
    return content
      .replaceAll('../assets/styles/main.css', 'assets/styles/main.css')
      .replaceAll('../assets/scripts/', 'assets/scripts/');
  }

  if (relativeTargetPath === 'article.html') {
    return content
      .replaceAll('../assets/styles/main.css', 'assets/styles/main.css')
      .replaceAll('../assets/scripts/', 'assets/scripts/')
      .replaceAll("../data/articles.json", 'data/articles.json')
      .replaceAll('data-image-base="../"', 'data-image-base=""');
  }

  if (relativeTargetPath === 'articles/template.html') {
    return content
      .replaceAll('../../assets/styles/main.css', '../assets/styles/main.css')
      .replaceAll('../../assets/scripts/', '../assets/scripts/');
  }

  return content;
}

async function runBrowserScript(filePath, context) {
  const script = await fs.readFile(filePath, 'utf8');
  vm.runInNewContext(script, context, { filename: filePath });
}

async function getRuntimeContracts() {
  const context = { window: {} };
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/locale-config.js'), context);
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/article-access.js'), context);
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/i18n.js'), context);
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/article-media.js'), context);
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/public-routes.js'), context);

  return {
    access: context.window.ArticleAccess,
    i18n: context.window.SiteI18n,
    media: context.window.ArticleMedia,
    routes: context.window.SitePublicRoutes,
  };
}

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

function escapeAttribute(value) {
  return escapeHtml(value).replaceAll('"', '&quot;');
}

function escapeXml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&apos;');
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function normalizeSiteOrigin(value) {
  const origin = typeof value === 'string' ? value.trim().replace(/\/+$/, '') : '';
  if (!/^https?:\/\/[^/]+$/i.test(origin)) {
    throw new TypeError('SITE_ORIGIN must be an absolute http(s) origin.');
  }
  return origin;
}

function getAnalyticsConfig(env) {
  const domain = typeof env.PLAUSIBLE_DOMAIN === 'string' ? env.PLAUSIBLE_DOMAIN.trim() : '';

  if (!domain) {
    return null;
  }

  if (!/^[a-z0-9.-]+$/i.test(domain) || domain.includes('..')) {
    throw new TypeError('PLAUSIBLE_DOMAIN must be a bare domain, for example artnouveauetdeco.com.');
  }

  return {
    domain,
    scriptSrc: 'https://plausible.io/js/script.js',
  };
}

function absolutePublicUrl(route) {
  return SITE_ORIGIN + route;
}

function setAttributeInTag(tag, attribute, value) {
  const escapedValue = escapeAttribute(value);
  const attributePattern = new RegExp(`\\s${escapeRegExp(attribute)}="[^"]*"`);

  if (attributePattern.test(tag)) {
    return tag.replace(attributePattern, ` ${attribute}="${escapedValue}"`);
  }

  return tag.replace(/>$/, ` ${attribute}="${escapedValue}">`);
}

function setTagContentById(content, tagName, id, value) {
  const pattern = new RegExp(`(<${tagName}[^>]*\\sid="${escapeRegExp(id)}"[^>]*>)([\\s\\S]*?)(</${tagName}>)`);
  return content.replace(pattern, `$1${escapeHtml(value)}$3`);
}

function setMetaContentById(content, id, value) {
  const pattern = new RegExp(`<meta[^>]*\\sid="${escapeRegExp(id)}"[^>]*>`);
  return content.replace(pattern, (tag) => setAttributeInTag(tag, 'content', value));
}

function insertOrReplaceOgImage(content, imagePath) {
  if (!imagePath) return content;

  const tag = `<meta property="og:image" content="${escapeAttribute(imagePath)}">`;

  if (/<meta property="og:image" content="[^"]*">/.test(content)) {
    return content.replace(/<meta property="og:image" content="[^"]*">/, tag);
  }

  return content.replace(
    /(<meta id="og-description" property="og:description" content="[^"]*">)/,
    `$1\n  ${tag}`
  );
}

function buildSeoLinks(routeName, locale, routeParams, contracts) {
  const { routes } = contracts;
  const params = routeParams || {};
  const canonicalRoute = routes.route(routeName, locale, params);
  const defaultRoute = routes.route(routeName, routes.defaultLocale, params);
  const alternateLinks = routes.alternates(routeName, params)
    .map((alternate) => `<link rel="alternate" hreflang="${escapeAttribute(alternate.hreflang)}" href="${escapeAttribute(absolutePublicUrl(alternate.href))}">`);

  return [
    `<link rel="canonical" href="${escapeAttribute(absolutePublicUrl(canonicalRoute))}">`,
    ...alternateLinks,
    `<link rel="alternate" hreflang="x-default" href="${escapeAttribute(absolutePublicUrl(defaultRoute))}">`,
  ].join('\n  ');
}

function applyPublicSeoLinks(content, routeName, locale, routeParams, contracts) {
  return content.replace(
    /(<meta name="robots" content="[^"]*">)/,
    `$1\n  ${buildSeoLinks(routeName, locale, routeParams, contracts)}`
  );
}

function renderAnalyticsScript() {
  if (!ANALYTICS) {
    return '';
  }

  return `<script defer data-domain="${escapeAttribute(ANALYTICS.domain)}" src="${escapeAttribute(ANALYTICS.scriptSrc)}"></script>`;
}

function applyPublicAnalytics(content) {
  const analyticsScript = renderAnalyticsScript();

  if (!analyticsScript || content.includes(analyticsScript)) {
    return content;
  }

  return content.replace('</head>', `  ${analyticsScript}\n</head>`);
}

function applyStaticI18n(content, locale, i18n) {
  let localized = content.replace(
    /<([a-zA-Z][\w:-]*)([^>]*\sdata-i18n-html="([^"]+)"[^>]*)>([\s\S]*?)<\/\1>/g,
    (match, tagName, attributes, key) => `<${tagName}${attributes}>${i18n.t(key, null, locale)}</${tagName}>`
  );

  localized = localized.replace(
    /<([a-zA-Z][\w:-]*)([^>]*\sdata-i18n="([^"]+)"[^>]*)>([\s\S]*?)<\/\1>/g,
    (match, tagName, attributes, key) => `<${tagName}${attributes}>${escapeHtml(i18n.t(key, null, locale))}</${tagName}>`
  );

  localized = localized.replace(
    /<([a-zA-Z][\w:-]*)([^>]*\sdata-i18n-attr="([^"]+)"[^>]*)>/g,
    (match, tagName, attributes, instructions) => {
      let tag = `<${tagName}${attributes}>`;
      instructions.split(';').forEach((entry) => {
        const [attribute, key] = entry.split(':').map((part) => part && part.trim());
        if (attribute && key) {
          tag = setAttributeInTag(tag, attribute, i18n.t(key, null, locale));
        }
      });
      return tag;
    }
  );

  return localized
    .replace(/<html lang="[^"]*">/, `<html lang="${locale}">`)
    .replace(/<meta property="og:locale" content="[^"]*">/, `<meta property="og:locale" content="${OG_LOCALES[locale] || OG_LOCALES.fr}">`);
}

function routeToDistPath(route) {
  const cleanRoute = route.replace(/^\/+|\/+$/g, '');
  return cleanRoute ? path.posix.join(cleanRoute, 'index.html') : 'index.html';
}

function relativeRootFromDistPath(relativeTargetPath) {
  const depth = relativeTargetPath.split('/').length - 1;
  return depth > 0 ? '../'.repeat(depth) : '';
}

function replaceSimplePublicLinks(content, locale, routeName, contracts, routeParams = {}) {
  const { i18n, routes } = contracts;
  const currentRoute = routes.route(routeName, locale, routeParams);
  const languageLinks = routes.publicLocaleCodes().map((targetLocale) => {
    const href = routes.route(routeName, targetLocale, routeParams);
    const active = targetLocale === locale ? ' is-active" aria-current="true' : '';
    return `<a href="${href}" class="site-nav__lang-link${active}" lang="${targetLocale}">${targetLocale.toUpperCase()}</a>`;
  }).join('\n          <span aria-hidden="true">/</span>\n          ');
  const languageLabel = escapeAttribute(i18n.t('nav.language.public', null, locale));

  return content
    .replace(
      /<div class="site-nav__language"[^>]*>[\s\S]*?<\/div>/,
      `<div class="site-nav__language" aria-label="${languageLabel}">\n          ${languageLinks}\n        </div>`
    )
    .replaceAll('href="index.html#galerie"', `href="${routes.home(locale)}#galerie"`)
    .replaceAll('href="index.html"', `href="${routes.home(locale)}"`)
    .replaceAll('href="about.html"', `href="${routes.about(locale)}"`)
    .replaceAll('href="mentions.html"', `href="${routes.mentions(locale)}"`)
    .replaceAll('href="' + currentRoute + '#galerie"', `href="${currentRoute}#galerie"`);
}

function rewritePublicPageForDist(routeName, relativeTargetPath, content, locale, contracts) {
  const relativeRoot = relativeRootFromDistPath(relativeTargetPath);
  let rewritten = applyStaticI18n(content, locale, contracts.i18n);

  rewritten = replaceSimplePublicLinks(rewritten, locale, routeName, contracts)
    .replaceAll('../assets/styles/main.css', `${relativeRoot}assets/styles/main.css`)
    .replaceAll('../assets/images/site/', `${relativeRoot}assets/images/site/`)
    .replaceAll('../assets/scripts/', `${relativeRoot}assets/scripts/`)
    .replaceAll("../data/articles.json", `${relativeRoot}data/articles.json`);

  rewritten = applyPublicSeoLinks(rewritten, routeName, locale, {}, contracts);
  rewritten = applyPublicAnalytics(rewritten);

  if (routeName === 'home') {
    rewritten = rewritten.replace(
      '<body class="page-home">',
      `<body class="page-home" data-article-data-url="${relativeRoot}data/articles.json" data-asset-base="${relativeRoot}">`
    );
  }

  return rewritten;
}

function getArticleSlug(article) {
  return contractsSafeText(article && article.slug);
}

function contractsSafeText(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function buildArticleHeadMeta(article, locale, contracts, relativeRoot) {
  const title = contracts.access.getArticleTitle(article, locale);
  const pageTitle = `${title} · ${SITE_TITLE}`;
  const description = contracts.access.getArticleMetaDescription(article, locale);
  const heroImage = contracts.media && typeof contracts.media.getPrimaryImage === 'function'
    ? contracts.media.getPrimaryImage(article, locale)
    : '';

  return {
    title: pageTitle,
    description,
    ogImage: heroImage ? `${relativeRoot}${heroImage}` : '',
  };
}

function rewritePublicArticlePageForDist(relativeTargetPath, content, locale, article, contracts) {
  const relativeRoot = relativeRootFromDistPath(relativeTargetPath);
  const slug = getArticleSlug(article);
  const routeParams = { slug };
  const { routes } = contracts;
  const metadata = buildArticleHeadMeta(article, locale, contracts, relativeRoot);

  let rewritten = applyStaticI18n(content, locale, contracts.i18n);

  rewritten = replaceSimplePublicLinks(rewritten, locale, ARTICLE_PUBLIC_PAGE.routeName, contracts, routeParams)
    .replaceAll('../assets/styles/main.css', `${relativeRoot}assets/styles/main.css`)
    .replaceAll('../assets/scripts/', `${relativeRoot}assets/scripts/`)
    .replaceAll("../data/articles.json", `${relativeRoot}data/articles.json`)
    .replaceAll('data-article-json="../data/articles.json"', `data-article-json="${relativeRoot}data/articles.json"`)
    .replaceAll('data-image-base="../"', `data-image-base="${relativeRoot}"`)
    .replaceAll('data-home-href="index.html"', `data-home-href="${routes.home(locale)}"`)
    .replaceAll('data-gallery-href="index.html#galerie"', `data-gallery-href="${routes.home(locale)}#galerie"`)
    .replace(
      'data-article-href-base="article.html?slug="',
      `data-article-href-base="${routes.article(locale, '__ARTICLE_SLUG__').replace('__ARTICLE_SLUG__/', '')}" data-article-href-suffix="/" data-article-slug="${escapeAttribute(slug)}"`
    );

  rewritten = setTagContentById(rewritten, 'title', 'page-title', metadata.title);
  rewritten = setMetaContentById(rewritten, 'page-description', metadata.description);
  rewritten = setMetaContentById(rewritten, 'og-title', metadata.title);
  rewritten = setMetaContentById(rewritten, 'og-description', metadata.description);
  rewritten = setMetaContentById(rewritten, 'twitter-title', metadata.title);
  rewritten = setMetaContentById(rewritten, 'twitter-description', metadata.description);
  rewritten = insertOrReplaceOgImage(rewritten, metadata.ogImage);
  rewritten = applyPublicSeoLinks(rewritten, ARTICLE_PUBLIC_PAGE.routeName, locale, routeParams, contracts);
  rewritten = applyPublicAnalytics(rewritten);

  return rewritten;
}

async function readArticles() {
  const raw = await fs.readFile(path.join(ROOT, 'src/data/articles.json'), 'utf8');
  const data = JSON.parse(raw);
  return Array.isArray(data.articles) ? data.articles : [];
}

async function ensureParentDir(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

async function copyDir(relativeFrom, relativeTo) {
  const source = path.join(ROOT, relativeFrom);
  const target = path.join(DIST, relativeTo);
  await fs.mkdir(path.dirname(target), { recursive: true });
  await fs.cp(source, target, { recursive: true, force: true });
}

function buildSitemapUrlEntry(routeName, locale, routeParams, contracts) {
  const { routes } = contracts;
  const params = routeParams || {};
  const route = routes.route(routeName, locale, params);
  const defaultRoute = routes.route(routeName, routes.defaultLocale, params);
  const alternateLinks = routes.alternates(routeName, params)
    .map((alternate) => `    <xhtml:link rel="alternate" hreflang="${escapeXml(alternate.hreflang)}" href="${escapeXml(absolutePublicUrl(alternate.href))}" />`);

  return [
    '  <url>',
    `    <loc>${escapeXml(absolutePublicUrl(route))}</loc>`,
    ...alternateLinks,
    `    <xhtml:link rel="alternate" hreflang="x-default" href="${escapeXml(absolutePublicUrl(defaultRoute))}" />`,
    '  </url>',
  ].join('\n');
}

function buildSitemapXml(articles, contracts) {
  const entries = [];

  for (const locale of contracts.routes.publicLocaleCodes()) {
    for (const job of SIMPLE_PUBLIC_PAGE_JOBS) {
      entries.push(buildSitemapUrlEntry(job.routeName, locale, {}, contracts));
    }

    for (const article of articles) {
      const slug = getArticleSlug(article);
      if (!slug) continue;
      entries.push(buildSitemapUrlEntry(ARTICLE_PUBLIC_PAGE.routeName, locale, { slug }, contracts));
    }
  }

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ...entries,
    '</urlset>',
    '',
  ].join('\n');
}

async function writeSitemap(articles, contracts) {
  await fs.writeFile(path.join(DIST, 'sitemap.xml'), buildSitemapXml(articles, contracts), 'utf8');
}

async function writeRobotsTxt() {
  const robots = [
    'User-agent: *',
    'Disallow:',
    'Allow: /',
    '',
    `Sitemap: ${absolutePublicUrl('/sitemap.xml')}`,
    '',
  ].join('\n');

  await fs.writeFile(path.join(DIST, 'robots.txt'), robots, 'utf8');
}

async function build() {
  const validation = await validateProject({ rootDir: ROOT });

  if (!validation.ok) {
    for (const error of validation.errors) {
      console.error(`ERROR\n${error}\n`);
    }
    process.exitCode = 1;
    return;
  }

  await fs.rm(DIST, { recursive: true, force: true });
  await fs.mkdir(DIST, { recursive: true });
  const contracts = await getRuntimeContracts();
  const articles = await readArticles();
  const publishedImagePaths = await collectPublishedImagePaths({
    rootDir: ROOT,
    articles,
    sitePagePaths: PUBLIC_IMAGE_SOURCE_PAGES,
  });

  for (const job of COPY_JOBS) {
    await copyDir(job.from, job.to);
  }

  await copyPublishedImages({
    rootDir: ROOT,
    distDir: DIST,
    imagePaths: publishedImagePaths,
  });
  await generateImageManifest({
    rootDir: ROOT,
    distDir: DIST,
    imagePaths: publishedImagePaths,
  });

  for (const job of PAGE_JOBS) {
    const source = path.join(ROOT, job.from);
    const target = path.join(DIST, job.to);
    const raw = await fs.readFile(source, 'utf8');
    const rewritten = rewritePageForDist(job.to, raw);
    await ensureParentDir(target);
    await fs.writeFile(target, rewritten, 'utf8');
  }

  for (const locale of contracts.routes.publicLocaleCodes()) {
    for (const job of SIMPLE_PUBLIC_PAGE_JOBS) {
      const publicRoute = contracts.routes.route(job.routeName, locale);
      const relativeTargetPath = routeToDistPath(publicRoute);
      const source = path.join(ROOT, job.from);
      const target = path.join(DIST, relativeTargetPath);
      const raw = await fs.readFile(source, 'utf8');
      const rewritten = rewritePublicPageForDist(job.routeName, relativeTargetPath, raw, locale, contracts);
      await ensureParentDir(target);
      await fs.writeFile(target, rewritten, 'utf8');
    }

    for (const article of articles) {
      const slug = getArticleSlug(article);
      if (!slug) continue;

      const publicRoute = contracts.routes.route(ARTICLE_PUBLIC_PAGE.routeName, locale, { slug });
      const relativeTargetPath = routeToDistPath(publicRoute);
      const source = path.join(ROOT, ARTICLE_PUBLIC_PAGE.from);
      const target = path.join(DIST, relativeTargetPath);
      const raw = await fs.readFile(source, 'utf8');
      const rewritten = rewritePublicArticlePageForDist(relativeTargetPath, raw, locale, article, contracts);
      await ensureParentDir(target);
      await fs.writeFile(target, rewritten, 'utf8');
    }
  }

  await writeSitemap(articles, contracts);
  await writeRobotsTxt();

  const distValidation = await validateProject({
    rootDir: ROOT,
    requireDist: true,
  });

  if (!distValidation.ok) {
    for (const error of distValidation.errors) {
      console.error(`ERROR\n${error}\n`);
    }
    process.exitCode = 1;
    return;
  }

  console.log('Build completed: dist is the publishable artifact.');
}

await build();
