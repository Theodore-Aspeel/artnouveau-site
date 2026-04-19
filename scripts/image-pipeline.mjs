import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

export const GENERATED_IMAGE_DIR = 'assets/generated-images';
export const IMAGE_MANIFEST_PATH = `${GENERATED_IMAGE_DIR}/manifest.json`;

const GENERATED_WIDTHS = [640, 960, 1280, 1600];
const SUPPORTED_EXTENSIONS = new Set(['.jpg', '.jpeg', '.png']);
const GENERATED_FORMATS = ['source', 'webp', 'avif'];

function normalizeImagePath(value) {
  return typeof value === 'string' ? value.trim().replaceAll('\\', '/') : '';
}

export function getImagePath(entry) {
  if (typeof entry === 'string') {
    return normalizeImagePath(entry);
  }

  if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
    return '';
  }

  return normalizeImagePath(entry.src || entry.path || entry.image);
}

export function getArticleImageEntries(article) {
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

function addRuntimeImagePath(paths, candidate) {
  const imagePath = normalizeImagePath(candidate);
  if (!imagePath || imagePath.startsWith('/') || /^(?:https?:)?\/\//i.test(imagePath)) {
    return;
  }

  if (imagePath.startsWith('assets/images/')) {
    paths.add(imagePath);
  }
}

export function collectArticleImagePaths(articles) {
  const paths = new Set();

  for (const article of Array.isArray(articles) ? articles : []) {
    for (const image of getArticleImageEntries(article)) {
      addRuntimeImagePath(paths, getImagePath(image));
    }
  }

  return Array.from(paths).sort((left, right) => left.localeCompare(right));
}

export async function collectSiteImagePaths(rootDir, pagePaths) {
  const paths = new Set();
  const imageRefPattern = /(?:src|srcset|href|content)=["']([^"']*assets\/images\/site\/[^"']+)["']/g;

  for (const pagePath of pagePaths) {
    const raw = await fs.readFile(path.join(rootDir, pagePath), 'utf8');
    for (const match of raw.matchAll(imageRefPattern)) {
      const ref = normalizeImagePath(match[1]).replace(/^(\.\.\/)+/, '');
      addRuntimeImagePath(paths, ref);
    }
  }

  return Array.from(paths).sort((left, right) => left.localeCompare(right));
}

export async function collectPublishedImagePaths({ rootDir, articles, sitePagePaths }) {
  const paths = new Set(collectArticleImagePaths(articles));
  const sitePaths = await collectSiteImagePaths(rootDir, sitePagePaths);

  for (const imagePath of sitePaths) {
    paths.add(imagePath);
  }

  return Array.from(paths).sort((left, right) => left.localeCompare(right));
}

function generatedRelativePath(sourcePath, width, extension) {
  const normalized = normalizeImagePath(sourcePath);
  const relativeImagePath = normalized.replace(/^assets\/images\//, '');
  const parsed = path.posix.parse(relativeImagePath);
  const outputName = `${parsed.name}-${width}w${extension}`;
  return path.posix.join(GENERATED_IMAGE_DIR, parsed.dir, outputName);
}

async function ensureParentDir(filePath) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
}

function outputOptions(format) {
  if (format === 'jpeg' || format === 'jpg') {
    return { mozjpeg: true, quality: 82 };
  }

  if (format === 'png') {
    return { compressionLevel: 9, palette: true, quality: 82 };
  }

  if (format === 'webp') {
    return { quality: 84, smartSubsample: true };
  }

  if (format === 'avif') {
    return { quality: 60, effort: 4, chromaSubsampling: '4:4:4' };
  }

  return {};
}

function normalizedSourceFormat(sourceMetadata, sourcePath) {
  const format = sourceMetadata.format || path.extname(sourcePath).toLowerCase().replace('.', '');
  return format === 'jpg' ? 'jpeg' : format;
}

function outputExtensionForFormat(format, sourcePath) {
  if (format === 'source') {
    return path.extname(sourcePath).toLowerCase();
  }

  if (format === 'jpeg') {
    return '.jpg';
  }

  return `.${format}`;
}

function outputFormatForVariant(format, sourceMetadata, sourcePath) {
  return format === 'source' ? normalizedSourceFormat(sourceMetadata, sourcePath) : format;
}

async function generatedVariantRecord({ rootDir, distDir, sourcePath, sourceMetadata, width, format }) {
  const sourceAbsolutePath = path.join(rootDir, 'src', sourcePath);
  const outputFormat = outputFormatForVariant(format, sourceMetadata, sourcePath);
  const distRelativePath = generatedRelativePath(sourcePath, width, outputExtensionForFormat(format, sourcePath));
  const distAbsolutePath = path.join(distDir, distRelativePath);

  await ensureParentDir(distAbsolutePath);
  await sharp(sourceAbsolutePath)
    .rotate()
    .resize({ width, withoutEnlargement: true })
    .toFormat(outputFormat, outputOptions(outputFormat))
    .toFile(distAbsolutePath);

  const [metadata, stats] = await Promise.all([
    sharp(distAbsolutePath).metadata(),
    fs.stat(distAbsolutePath),
  ]);

  return {
    format: outputFormat,
    width: metadata.width,
    height: metadata.height,
    bytes: stats.size,
    dist_path: distRelativePath,
  };
}

async function buildManifestEntry({ rootDir, distDir, sourcePath }) {
  const sourceAbsolutePath = path.join(rootDir, 'src', sourcePath);
  const extension = path.extname(sourcePath).toLowerCase();

  if (!SUPPORTED_EXTENSIONS.has(extension)) {
    return null;
  }

  const [sourceMetadata, sourceStats] = await Promise.all([
    sharp(sourceAbsolutePath).metadata(),
    fs.stat(sourceAbsolutePath),
  ]);

  const sourceWidth = sourceMetadata.width;
  const widths = GENERATED_WIDTHS.filter((width) => Number.isInteger(sourceWidth) && width <= sourceWidth);
  const generatedWidths = widths.length ? widths : [sourceWidth].filter(Number.isInteger);
  const variants = [];

  for (const width of generatedWidths) {
    for (const format of GENERATED_FORMATS) {
      variants.push(await generatedVariantRecord({
        rootDir,
        distDir,
        sourcePath,
        sourceMetadata,
        width,
        format,
      }));
    }
  }

  return {
    source_path: sourcePath,
    source: {
      format: normalizedSourceFormat(sourceMetadata, sourcePath),
      width: sourceMetadata.width,
      height: sourceMetadata.height,
      bytes: sourceStats.size,
    },
    generated_formats: GENERATED_FORMATS.map((format) => outputFormatForVariant(format, sourceMetadata, sourcePath)),
    variants,
  };
}

export async function copyPublishedImages({ rootDir, distDir, imagePaths }) {
  for (const imagePath of imagePaths) {
    const source = path.join(rootDir, 'src', imagePath);
    const target = path.join(distDir, imagePath);
    await ensureParentDir(target);
    await fs.copyFile(source, target);
  }
}

export async function generateImageManifest({ rootDir, distDir, imagePaths }) {
  const images = [];

  for (const imagePath of imagePaths) {
    const entry = await buildManifestEntry({ rootDir, distDir, sourcePath: imagePath });
    if (entry) {
      images.push(entry);
    }
  }

  const manifest = {
    version: 2,
    generated_dir: GENERATED_IMAGE_DIR,
    generated_formats: ['source', 'webp', 'avif'],
    images,
  };
  const manifestPath = path.join(distDir, IMAGE_MANIFEST_PATH);
  await ensureParentDir(manifestPath);
  await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, 'utf8');

  return manifest;
}
