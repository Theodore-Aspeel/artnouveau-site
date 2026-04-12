import fs from 'node:fs/promises';
import path from 'node:path';
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

const COPY_JOBS = [
  { from: 'src/assets/styles', to: 'assets/styles' },
  { from: 'src/assets/scripts', to: 'assets/scripts' },
  { from: 'src/data', to: 'data' },
  { from: 'public', to: '.' },
];

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
