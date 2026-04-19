import fs from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
import { validateProject } from './validate-content.mjs';

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

const COPY_JOBS = [
  { from: 'src/assets/styles', to: 'assets/styles' },
  { from: 'src/assets/scripts', to: 'assets/scripts' },
  { from: 'src/data', to: 'data' },
  { from: 'public', to: '.' },
];

const OG_LOCALES = {
  fr: 'fr_FR',
  en: 'en_US',
  nl: 'nl_NL',
};

function getImagePath(entry) {
  if (typeof entry === 'string') {
    return entry.trim();
  }

  if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
    return '';
  }

  const candidate = entry.src || entry.path || entry.image;
  return typeof candidate === 'string' ? candidate.trim() : '';
}

function getArticleImageEntries(article) {
  const entries = [];
  const media = article && typeof article === 'object' && !Array.isArray(article)
    ? article.media
    : null;

  if (media && typeof media === 'object' && !Array.isArray(media)) {
    entries.push(media.hero);
    if (Array.isArray(media.support)) {
      entries.push(...media.support);
    }
    return entries;
  }

  entries.push(article?.hero_image);
  if (Array.isArray(article?.support_images)) {
    entries.push(...article.support_images);
  }

  return entries;
}

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
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/i18n.js'), context);
  await runBrowserScript(path.join(ROOT, 'src/assets/scripts/public-routes.js'), context);

  return {
    i18n: context.window.SiteI18n,
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

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function setAttributeInTag(tag, attribute, value) {
  const escapedValue = escapeAttribute(value);
  const attributePattern = new RegExp(`\\s${escapeRegExp(attribute)}="[^"]*"`);

  if (attributePattern.test(tag)) {
    return tag.replace(attributePattern, ` ${attribute}="${escapedValue}"`);
  }

  return tag.replace(/>$/, ` ${attribute}="${escapedValue}">`);
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

function replaceSimplePublicLinks(content, locale, routeName, contracts) {
  const { i18n, routes } = contracts;
  const currentRoute = routes.route(routeName, locale);
  const languageLinks = routes.publicLocaleCodes().map((targetLocale) => {
    const href = routes.route(routeName, targetLocale);
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

  if (routeName === 'home') {
    rewritten = rewritten.replace(
      '<body class="page-home">',
      `<body class="page-home" data-article-data-url="${relativeRoot}data/articles.json" data-asset-base="${relativeRoot}">`
    );
  }

  return rewritten;
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

async function copyFile(relativeFrom, relativeTo) {
  const source = path.join(ROOT, relativeFrom);
  const target = path.join(DIST, relativeTo);
  await ensureParentDir(target);
  await fs.copyFile(source, target);
}

async function copyRuntimeImages() {
  await copyDir('src/assets/images/site', 'assets/images/site');

  const raw = await fs.readFile(path.join(ROOT, 'src/data/articles.json'), 'utf8');
  const data = JSON.parse(raw);
  const runtimeImagePaths = new Set();

  for (const article of Array.isArray(data.articles) ? data.articles : []) {
    for (const image of getArticleImageEntries(article)) {
      const imagePath = getImagePath(image);
      if (imagePath) {
        runtimeImagePaths.add(imagePath);
      }
    }
  }

  for (const imagePath of runtimeImagePaths) {
    await copyFile(path.join('src', imagePath), imagePath);
  }
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

  for (const job of COPY_JOBS) {
    await copyDir(job.from, job.to);
  }

  await copyRuntimeImages();

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
  }

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
