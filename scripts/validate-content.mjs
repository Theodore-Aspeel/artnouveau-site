import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DEFAULT_ROOT = path.resolve(__dirname, '..');

const REQUIRED_SOURCE_FILES = [
  'src/pages/index.html',
  'src/pages/about.html',
  'src/pages/mentions.html',
  'src/pages/404.html',
  'src/pages/article-redirect.html',
  'src/pages/articles/template.html',
  'src/assets/styles/main.css',
  'src/assets/scripts/article-access.js',
  'src/assets/scripts/main.js',
  'src/assets/scripts/gallery.js',
  'src/assets/scripts/article-media.js',
  'src/assets/scripts/article-taxonomy.js',
  'src/assets/scripts/article-template.js',
  'src/data/articles.json',
  'public/favicon.ico',
  'public/icon.svg',
  'public/icon.png',
  'public/robots.txt',
  'public/site.webmanifest',
];

const REQUIRED_DIST_FILES = [
  'index.html',
  'about.html',
  'mentions.html',
  '404.html',
  'article.html',
  'articles/template.html',
  'assets/styles/main.css',
  'assets/scripts/article-access.js',
  'assets/scripts/main.js',
  'assets/scripts/gallery.js',
  'assets/scripts/article-media.js',
  'assets/scripts/article-taxonomy.js',
  'assets/scripts/article-template.js',
  'data/articles.json',
  'favicon.ico',
  'icon.svg',
  'icon.png',
  'robots.txt',
  'site.webmanifest',
];

const CONTROLLED_FORMATS = new Set([
  'article-complet',
  'article-court',
]);

const CONTROLLED_STYLES = new Set([
  'Art Nouveau',
  'Art Nouveau géométrique',
  'Art Déco',
  'Liberty / Art Nouveau',
  'Sécession viennoise',
]);

const CONTROLLED_TAGS = new Set([
  'Art Nouveau',
  'Art Déco',
  'Bâtiment public',
  'Commerce',
  'Façade',
  'Habitat',
  'Liberty',
  'Motif floral',
  'Seuil',
  'Sécession viennoise',
  'Écriture urbaine',
]);

const CONTROLLED_AROUND_RELATIONS = new Set([
  'Même ville',
  'Contrepoint',
  'Autre échelle',
]);

const CONTROLLED_STYLE_KEYS = new Set([
  'art_nouveau',
  'art_nouveau_geometric',
  'art_deco',
  'liberty_art_nouveau',
  'vienna_secession',
]);

const CONTROLLED_TAG_KEYS = new Set([
  'art_nouveau',
  'art_deco',
  'public_building',
  'commerce',
  'facade',
  'habitat',
  'liberty',
  'floral_motif',
  'threshold',
  'vienna_secession',
  'urban_lettering',
]);

const CONTROLLED_RELATION_KEYS = new Set([
  'same_city',
  'counterpoint',
  'other_scale',
]);

const CONTROLLED_PRACTICAL_KEYS = new Set([
  'exact_name',
  'city',
  'country',
  'style',
  'architect',
  'address',
  'date',
  'access',
]);

const SOURCE_TEXT_FILES = [
  'src/pages/index.html',
  'src/pages/about.html',
  'src/pages/mentions.html',
  'src/pages/404.html',
  'src/pages/article-redirect.html',
  'src/pages/articles/template.html',
  'src/assets/scripts/article-access.js',
  'src/assets/scripts/main.js',
  'src/assets/scripts/gallery.js',
  'src/assets/scripts/article-media.js',
  'src/assets/scripts/article-taxonomy.js',
  'src/assets/scripts/article-template.js',
];

function normalizeText(value) {
  return typeof value === 'string' ? value.trim() : '';
}

function slugifyTaxon(value) {
  return normalizeText(value)
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

function getImagePath(entry) {
  if (typeof entry === 'string') {
    return normalizeText(entry);
  }

  if (!entry || typeof entry !== 'object' || Array.isArray(entry)) {
    return '';
  }

  return normalizeText(entry.src || entry.path || entry.image);
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
}

function isLocalizedString(value) {
  if (typeof value === 'string') {
    return Boolean(value.trim());
  }

  if (!isPlainObject(value)) {
    return false;
  }

  return Object.values(value).some((item) => typeof item === 'string' && item.trim());
}

function hasMojibake(value) {
  return typeof value === 'string' && /(?:Ã.|Â.|â(?:€™|€|€“|€”|€¦)|�)/.test(value);
}

function hasSuspiciousQuestionMark(value) {
  return typeof value === 'string' && (/[A-Za-zÀ-ÿ]\?[A-Za-zÀ-ÿ]/.test(value) || /^\?\s/.test(value));
}

function getExpectedStyleTags(style) {
  switch (style) {
    case 'Art Déco':
      return ['Art Déco'];
    case 'Liberty / Art Nouveau':
      return ['Liberty', 'Art Nouveau'];
    case 'Sécession viennoise':
      return ['Sécession viennoise'];
    case 'Art Nouveau':
    case 'Art Nouveau géométrique':
      return ['Art Nouveau'];
    default:
      return [];
  }
}

async function pathExists(targetPath) {
  try {
    await fs.access(targetPath);
    return true;
  } catch {
    return false;
  }
}

async function collectMissing(rootDir, relativePaths) {
  const missing = [];

  for (const relativePath of relativePaths) {
    const fullPath = path.join(rootDir, relativePath);
    if (!(await pathExists(fullPath))) {
      missing.push(relativePath);
    }
  }

  return missing.sort((left, right) => left.localeCompare(right));
}

function collectArticleAssetRefs(articles) {
  const refs = [];

  articles.forEach((article, index) => {
    if (!article || typeof article !== 'object') return;

    const articleLabel = typeof article.slug === 'string' && article.slug.trim()
      ? article.slug.trim()
      : `article#${index + 1}`;

    const articleMedia = isPlainObject(article.media) ? article.media : null;
    const heroImagePath = getImagePath(articleMedia ? articleMedia.hero : article.hero_image);
    if (heroImagePath) {
      refs.push({
        article: articleLabel,
        field: articleMedia ? 'media.hero' : 'hero_image',
        path: heroImagePath,
      });
    }

    const supportImages = articleMedia && Array.isArray(articleMedia.support)
      ? articleMedia.support
      : article.support_images;

    if (Array.isArray(supportImages)) {
      supportImages.forEach((item, supportIndex) => {
        const imagePath = getImagePath(item);
        if (imagePath) {
          refs.push({
            article: articleLabel,
            field: articleMedia ? `media.support[${supportIndex}]` : `support_images[${supportIndex}]`,
            path: imagePath,
          });
        }
      });
    }
  });

  return refs;
}

async function readArticlesJson(rootDir, relativePath) {
  const raw = await fs.readFile(path.join(rootDir, relativePath), 'utf8');
  const parsed = JSON.parse(raw);
  return Array.isArray(parsed.articles) ? parsed.articles : [];
}

async function collectMissingAssetRefs(rootDir, relativeDataPath, baseDirRelativeToRoot) {
  const articles = await readArticlesJson(rootDir, relativeDataPath);
  const refs = collectArticleAssetRefs(articles);
  const missing = [];

  for (const ref of refs) {
    const absoluteTarget = path.join(rootDir, baseDirRelativeToRoot, ref.path);
    if (!(await pathExists(absoluteTarget))) {
      missing.push(ref);
    }
  }

  return missing.sort((left, right) => {
    const byPath = left.path.localeCompare(right.path);
    if (byPath !== 0) return byPath;
    const byArticle = left.article.localeCompare(right.article);
    if (byArticle !== 0) return byArticle;
    return left.field.localeCompare(right.field);
  });
}

async function collectUnreferencedArticleAssets(rootDir, relativeDataPath, baseDirRelativeToRoot) {
  const articles = await readArticlesJson(rootDir, relativeDataPath);
  const refs = new Set(
    collectArticleAssetRefs(articles)
      .map((ref) => ref.path)
      .filter((ref) => ref.startsWith('assets/images/articles/'))
  );
  const articleAssetsRoot = path.join(rootDir, baseDirRelativeToRoot, 'assets', 'images', 'articles');
  const unreferenced = [];

  async function walk(currentPath) {
    const entries = await fs.readdir(currentPath, { withFileTypes: true });

    for (const entry of entries) {
      const absolutePath = path.join(currentPath, entry.name);
      if (entry.isDirectory()) {
        await walk(absolutePath);
        continue;
      }

      const relativePath = path.relative(path.join(rootDir, baseDirRelativeToRoot), absolutePath).replaceAll('\\', '/');
      if (!refs.has(relativePath)) {
        unreferenced.push(relativePath);
      }
    }
  }

  if (await pathExists(articleAssetsRoot)) {
    await walk(articleAssetsRoot);
  }

  return unreferenced.sort((left, right) => left.localeCompare(right));
}

async function collectCorruptedTextInFiles(rootDir, relativePaths) {
  const hits = [];

  for (const relativePath of relativePaths) {
    const raw = await fs.readFile(path.join(rootDir, relativePath), 'utf8');
    const lines = raw.split(/\r?\n/);

    lines.forEach((line, index) => {
      if (hasMojibake(line)) {
        hits.push(`${relativePath}:${index + 1}: suspicious mojibake sequence`);
      }
    });
  }

  return hits;
}

function formatMissingAssetRefs(title, refs) {
  return [
    title,
    ...refs.map((ref) => `- ${ref.path} (${ref.article} -> ${ref.field})`),
  ].join('\n');
}

function validateImageEntry(entry, fieldLabel, articleLabel, errors) {
  if (typeof entry === 'string') {
    if (!entry.trim()) {
      errors.push(`${articleLabel}: ${fieldLabel} must not be empty.`);
    }
    return;
  }

  if (!isPlainObject(entry)) {
    errors.push(`${articleLabel}: ${fieldLabel} must be a string path or an image object.`);
    return;
  }

  if (!getImagePath(entry)) {
    errors.push(`${articleLabel}: ${fieldLabel} image object must define src, path or image.`);
  }

  for (const key of ['alt', 'caption', 'credit']) {
    if (key in entry && entry[key] !== null && typeof entry[key] !== 'string') {
      errors.push(`${articleLabel}: ${fieldLabel}.${key} must be a string when provided.`);
    }
  }
}

function validateArticleSchemaV2(article, articleLabel, errors, publicationOrders, slugSet) {
  const slug = normalizeText(article.slug);
  if (!slug) {
    errors.push(`${articleLabel}: slug is required.`);
  } else if (slugSet.has(slug)) {
    errors.push(`${articleLabel}: slug must be unique.`);
  } else {
    slugSet.add(slug);
  }

  const id = normalizeText(article.id);
  if (!id) {
    errors.push(`${articleLabel}: id is required for v2 articles.`);
  } else if (id !== slug) {
    errors.push(`${articleLabel}: id must match slug during the progressive v2 migration.`);
  }

  if (!['long', 'short', 'article-complet', 'article-court'].includes(normalizeText(article.format))) {
    errors.push(`${articleLabel}: format must be long/short or a legacy article format during migration.`);
  }

  const publication = isPlainObject(article.publication) ? article.publication : {};
  if (!Number.isInteger(publication.order) || publication.order < 1) {
    errors.push(`${articleLabel}: publication.order must be a positive integer.`);
  } else if (publicationOrders.has(publication.order)) {
    errors.push(`${articleLabel}: publication.order duplicates ${publicationOrders.get(publication.order)}.`);
  } else {
    publicationOrders.set(publication.order, articleLabel);
  }

  if ('taxonomy' in article && article.taxonomy !== null) {
    if (!isPlainObject(article.taxonomy)) {
      errors.push(`${articleLabel}: taxonomy must be an object when provided.`);
    } else {
      const styleKey = normalizeText(article.taxonomy.style_key);
      if (styleKey && !CONTROLLED_STYLE_KEYS.has(styleKey)) {
        errors.push(`${articleLabel}: taxonomy.style_key must be one of ${Array.from(CONTROLLED_STYLE_KEYS).join(', ')}.`);
      }

      if ('tag_keys' in article.taxonomy) {
        if (!Array.isArray(article.taxonomy.tag_keys)) {
          errors.push(`${articleLabel}: taxonomy.tag_keys must be an array when provided.`);
        } else {
          article.taxonomy.tag_keys.forEach((tagKey, tagIndex) => {
            if (!CONTROLLED_TAG_KEYS.has(normalizeText(tagKey))) {
              errors.push(`${articleLabel}: taxonomy.tag_keys[${tagIndex}] must be one of ${Array.from(CONTROLLED_TAG_KEYS).join(', ')}.`);
            }
          });
        }
      }
    }
  }

  if (!isPlainObject(article.media) && !getImagePath(article.hero_image)) {
    errors.push(`${articleLabel}: media.hero is required for v2 articles unless a legacy hero_image fallback is present.`);
  } else if (isPlainObject(article.media)) {
    validateImageEntry(article.media.hero || article.hero_image, 'media.hero', articleLabel, errors);
    if (!Array.isArray(article.media.support)) {
      errors.push(`${articleLabel}: media.support must be an array.`);
    } else {
      article.media.support.forEach((entry, imageIndex) => {
        validateImageEntry(entry, `media.support[${imageIndex}]`, articleLabel, errors);
      });
    }
  }

  const content = isPlainObject(article.content) ? article.content : {};
  const fr = isPlainObject(content.fr) ? content.fr : {};
  if (!isPlainObject(content.fr)) {
    errors.push(`${articleLabel}: content.fr is required for v2 articles.`);
  }

  if (!normalizeText(fr.title)) errors.push(`${articleLabel}: content.fr.title is required.`);
  if (!normalizeText(fr.dek)) errors.push(`${articleLabel}: content.fr.dek is required.`);
  if (!normalizeText(fr.epigraph)) errors.push(`${articleLabel}: content.fr.epigraph is required.`);
  if (!isPlainObject(fr.seo) || !normalizeText(fr.seo.meta_description)) {
    errors.push(`${articleLabel}: content.fr.seo.meta_description is required.`);
  }
  if (!isPlainObject(fr.media) || !normalizeText(fr.media.hero_alt)) {
    errors.push(`${articleLabel}: content.fr.media.hero_alt is required.`);
  }
  if (!Array.isArray(fr.sections) || !fr.sections.length) {
    errors.push(`${articleLabel}: content.fr.sections must contain at least one section.`);
  } else {
    fr.sections.forEach((section, sectionIndex) => {
      if (!isPlainObject(section)) {
        errors.push(`${articleLabel}: content.fr.sections[${sectionIndex}] must be an object.`);
        return;
      }
      if (!normalizeText(section.heading)) errors.push(`${articleLabel}: content.fr.sections[${sectionIndex}].heading is required.`);
      if (!normalizeText(section.body)) errors.push(`${articleLabel}: content.fr.sections[${sectionIndex}].body is required.`);
    });
  }

  if (Array.isArray(fr.practical_items)) {
    fr.practical_items.forEach((item, itemIndex) => {
      if (!isPlainObject(item)) {
        errors.push(`${articleLabel}: content.fr.practical_items[${itemIndex}] must be an object.`);
        return;
      }
      if (!CONTROLLED_PRACTICAL_KEYS.has(normalizeText(item.key))) {
        errors.push(`${articleLabel}: content.fr.practical_items[${itemIndex}].key must be a stable practical key.`);
      }
      if (!normalizeText(item.value)) {
        errors.push(`${articleLabel}: content.fr.practical_items[${itemIndex}].value is required.`);
      }
    });
  }

  const around = isPlainObject(article.relations) ? article.relations.around : null;
  if (around !== undefined && around !== null) {
    if (!isPlainObject(around)) {
      errors.push(`${articleLabel}: relations.around must be null or an object.`);
    } else if (!CONTROLLED_RELATION_KEYS.has(normalizeText(around.relation_key))) {
      errors.push(`${articleLabel}: relations.around.relation_key must be one of ${Array.from(CONTROLLED_RELATION_KEYS).join(', ')}.`);
    }
  }

  if (isPlainObject(article.sources) && isPlainObject(article.sources.quote)) {
    const quote = article.sources.quote;
    if (!isLocalizedString(quote.text)) errors.push(`${articleLabel}: sources.quote.text must contain at least one localized string.`);
    if (!isLocalizedString(quote.author)) errors.push(`${articleLabel}: sources.quote.author must contain at least one localized string.`);
    if ('url' in quote && quote.url !== null && (typeof quote.url !== 'string' || !/^https?:\/\//i.test(quote.url.trim()))) {
      errors.push(`${articleLabel}: sources.quote.url must be an absolute http(s) URL when provided.`);
    }
    if (typeof quote.verified !== 'boolean') errors.push(`${articleLabel}: sources.quote.verified must be a boolean.`);
  }

  for (const value of [
    fr.title,
    fr.dek,
    fr.epigraph,
    fr.seo?.meta_description,
    article.sources?.quote?.text?.fr,
    article.sources?.quote?.author?.fr,
    article.sources?.quote?.attribution?.fr,
  ]) {
    if (hasMojibake(value)) {
      errors.push(`${articleLabel}: contains mojibake-corrupted text.`);
    }
    if (hasSuspiciousQuestionMark(value)) {
      errors.push(`${articleLabel}: contains suspicious replacement "?" in editorial text.`);
    }
  }
}

function validateArticleSchema(articles) {
  const errors = [];
  const warnings = [];
  const slugSet = new Set();
  const publicationOrders = new Map();

  articles.forEach((article, index) => {
    const articleLabel = typeof article?.slug === 'string' && article.slug.trim()
      ? article.slug.trim()
      : `article#${index + 1}`;

    if (!isPlainObject(article)) {
      errors.push(`${articleLabel}: article entry must be an object.`);
      return;
    }

    if (article.schema_version === 2 || isPlainObject(article.content)) {
      validateArticleSchemaV2(article, articleLabel, errors, publicationOrders, slugSet);
      return;
    }

    const slug = normalizeText(article.slug);
    if (!slug) {
      errors.push(`${articleLabel}: slug is required.`);
    } else if (slugSet.has(slug)) {
      errors.push(`${articleLabel}: slug must be unique.`);
    } else {
      slugSet.add(slug);
    }

    const format = normalizeText(article.format);
    if (!CONTROLLED_FORMATS.has(format)) {
      errors.push(`${articleLabel}: format must be one of ${Array.from(CONTROLLED_FORMATS).join(', ')}.`);
    }

    const style = normalizeText(article.style);
    if (!CONTROLLED_STYLES.has(style)) {
      errors.push(`${articleLabel}: style must be one of ${Array.from(CONTROLLED_STYLES).join(', ')}.`);
    }

    if (!normalizeText(article.title)) errors.push(`${articleLabel}: title is required.`);
    if (!normalizeText(article.city)) errors.push(`${articleLabel}: city is required.`);
    if (!normalizeText(article.country)) errors.push(`${articleLabel}: country is required.`);
    if (!normalizeText(article.chapeau)) errors.push(`${articleLabel}: chapeau is required.`);
    if (!normalizeText(article.meta_description)) errors.push(`${articleLabel}: meta_description is required.`);
    if (!normalizeText(article.alt_text)) errors.push(`${articleLabel}: alt_text is required.`);
    if (!normalizeText(article.epigraph)) errors.push(`${articleLabel}: epigraph is required.`);

    validateImageEntry(article.hero_image, 'hero_image', articleLabel, errors);

    if (!Array.isArray(article.support_images)) {
      errors.push(`${articleLabel}: support_images must be an array.`);
    } else {
      article.support_images.forEach((entry, imageIndex) => {
        validateImageEntry(entry, `support_images[${imageIndex}]`, articleLabel, errors);
      });
    }

    if (!Array.isArray(article.sections) || !article.sections.length) {
      errors.push(`${articleLabel}: sections must contain at least one section.`);
    } else {
      article.sections.forEach((section, sectionIndex) => {
        if (!isPlainObject(section)) {
          errors.push(`${articleLabel}: sections[${sectionIndex}] must be an object.`);
          return;
        }

        if (!normalizeText(section.heading)) {
          errors.push(`${articleLabel}: sections[${sectionIndex}].heading is required.`);
        }

        if (!normalizeText(section.body)) {
          errors.push(`${articleLabel}: sections[${sectionIndex}].body is required.`);
        }
      });
    }

    if (!Array.isArray(article.tags) || !article.tags.length) {
      errors.push(`${articleLabel}: tags must contain at least one controlled tag.`);
    } else {
      const seenTags = new Set();
      article.tags.forEach((tag, tagIndex) => {
        const tagLabel = normalizeText(tag);
        const tagSlug = slugifyTaxon(tagLabel);

        if (!tagLabel) {
          errors.push(`${articleLabel}: tags[${tagIndex}] must not be empty.`);
          return;
        }

        if (!CONTROLLED_TAGS.has(tagLabel)) {
          errors.push(`${articleLabel}: tags[${tagIndex}] must be one of ${Array.from(CONTROLLED_TAGS).join(', ')}.`);
        }

        if (seenTags.has(tagSlug)) {
          errors.push(`${articleLabel}: tags must not contain duplicates.`);
        } else {
          seenTags.add(tagSlug);
        }
      });

      const expectedStyleTags = getExpectedStyleTags(style);
      if (expectedStyleTags.length && !article.tags.some((tag) => expectedStyleTags.includes(normalizeText(tag)))) {
        errors.push(`${articleLabel}: tags must include one of ${expectedStyleTags.join(', ')} for style "${style}".`);
      }
    }

    if (!Array.isArray(article.gaps)) {
      errors.push(`${articleLabel}: gaps must be an array.`);
    } else if (article.gaps.some((gap) => !normalizeText(gap))) {
      errors.push(`${articleLabel}: gaps entries must be non-empty strings.`);
    }

    if (!isPlainObject(article.quote)) {
      errors.push(`${articleLabel}: quote must be an object.`);
    } else {
      if (!isLocalizedString(article.quote.text)) {
        errors.push(`${articleLabel}: quote.text must contain at least one localized string.`);
      }

      if (!isLocalizedString(article.quote.author)) {
        errors.push(`${articleLabel}: quote.author must contain at least one localized string.`);
      }

      if ('attribution' in article.quote && article.quote.attribution !== null && !isLocalizedString(article.quote.attribution)) {
        errors.push(`${articleLabel}: quote.attribution must be a localized string when provided.`);
      }

      if ('source' in article.quote && article.quote.source !== null && typeof article.quote.source !== 'string') {
        errors.push(`${articleLabel}: quote.source must be a string when provided.`);
      }

      if ('source_type' in article.quote && article.quote.source_type !== null && typeof article.quote.source_type !== 'string') {
        errors.push(`${articleLabel}: quote.source_type must be a string when provided.`);
      }

      if ('source_url' in article.quote && article.quote.source_url !== null) {
        if (typeof article.quote.source_url !== 'string' || !/^https?:\/\//i.test(article.quote.source_url.trim())) {
          errors.push(`${articleLabel}: quote.source_url must be an absolute http(s) URL when provided.`);
        }
      }

      if (typeof article.quote.verified !== 'boolean') {
        errors.push(`${articleLabel}: quote.verified must be a boolean.`);
      }
    }

    for (const value of [
      article.title,
      article.chapeau,
      article.epigraph,
      article.meta_description,
      article.quote?.text?.fr,
      article.quote?.author?.fr,
      article.quote?.attribution?.fr,
    ]) {
      if (hasMojibake(value)) {
        errors.push(`${articleLabel}: contains mojibake-corrupted text.`);
      }

      if (hasSuspiciousQuestionMark(value)) {
        errors.push(`${articleLabel}: contains suspicious replacement "?" in editorial text.`);
      }
    }

    if (!isPlainObject(article.verified_info)) {
      errors.push(`${articleLabel}: verified_info must be an object.`);
    } else {
      for (const key of ['exact_name', 'architect', 'date', 'style', 'city', 'country', 'address', 'notes']) {
        if (key in article.verified_info && article.verified_info[key] !== null && typeof article.verified_info[key] !== 'string') {
          errors.push(`${articleLabel}: verified_info.${key} must be a string or null.`);
        }
      }

      if (normalizeText(article.verified_info.style) && normalizeText(article.verified_info.style) !== style) {
        errors.push(`${articleLabel}: verified_info.style must match top-level style.`);
      }

      if (normalizeText(article.verified_info.city) && normalizeText(article.verified_info.city) !== normalizeText(article.city)) {
        errors.push(`${articleLabel}: verified_info.city must match top-level city.`);
      }

      if (normalizeText(article.verified_info.country) && normalizeText(article.verified_info.country) !== normalizeText(article.country)) {
        errors.push(`${articleLabel}: verified_info.country must match top-level country.`);
      }
    }

    if (!isPlainObject(article.practical)) {
      errors.push(`${articleLabel}: practical must be an object.`);
    } else {
      for (const key of ['Ville', 'Pays', 'Style', 'Architecte', 'Datation', 'Adresse', 'Accès']) {
        if (key in article.practical && article.practical[key] !== null && typeof article.practical[key] !== 'string') {
          errors.push(`${articleLabel}: practical.${key} must be a string or null.`);
        }
      }

      if (normalizeText(article.practical.Ville) && normalizeText(article.practical.Ville) !== normalizeText(article.city)) {
        errors.push(`${articleLabel}: practical.Ville must match top-level city.`);
      }

      if (normalizeText(article.practical.Pays) && normalizeText(article.practical.Pays) !== normalizeText(article.country)) {
        errors.push(`${articleLabel}: practical.Pays must match top-level country.`);
      }

      if (normalizeText(article.practical.Style) && normalizeText(article.practical.Style) !== style) {
        errors.push(`${articleLabel}: practical.Style must match top-level style.`);
      }
    }

    if (!isPlainObject(article.editorial)) {
      errors.push(`${articleLabel}: editorial must be an object.`);
    } else {
      for (const key of ['author', 'published_on', 'updated_on', 'image_credit', 'source_note', 'method_note']) {
        if (key in article.editorial && article.editorial[key] !== null && typeof article.editorial[key] !== 'string') {
          errors.push(`${articleLabel}: editorial.${key} must be a string or null.`);
        }
      }
    }

    if (article.around !== null) {
      if (!isPlainObject(article.around)) {
        errors.push(`${articleLabel}: around must be null or an object.`);
      } else {
        if (!CONTROLLED_AROUND_RELATIONS.has(normalizeText(article.around.relation_label))) {
          errors.push(`${articleLabel}: around.relation_label must be one of ${Array.from(CONTROLLED_AROUND_RELATIONS).join(', ')}.`);
        }

        if (!normalizeText(article.around.article_slug)) {
          errors.push(`${articleLabel}: around.article_slug is required when around is present.`);
        } else if (normalizeText(article.around.article_slug) === slug) {
          errors.push(`${articleLabel}: around.article_slug must not reference the same article.`);
        }

        if ('note' in article.around && article.around.note !== null && typeof article.around.note !== 'string') {
          errors.push(`${articleLabel}: around.note must be a string or null.`);
        }
      }
    }

    if (!Number.isInteger(article.publication_order_recommended) || article.publication_order_recommended < 1) {
      errors.push(`${articleLabel}: publication_order_recommended must be a positive integer.`);
    } else if (publicationOrders.has(article.publication_order_recommended)) {
      errors.push(
        `${articleLabel}: publication_order_recommended duplicates ${publicationOrders.get(article.publication_order_recommended)}.`
      );
    } else {
      publicationOrders.set(article.publication_order_recommended, articleLabel);
    }
  });

  articles.forEach((article, index) => {
    const articleLabel = typeof article?.slug === 'string' && article.slug.trim()
      ? article.slug.trim()
      : `article#${index + 1}`;

    if (isPlainObject(article?.around)) {
      const targetSlug = normalizeText(article.around.article_slug);
      if (targetSlug && !slugSet.has(targetSlug)) {
        errors.push(`${articleLabel}: around.article_slug must reference an existing article slug.`);
      }
    }

    if (isPlainObject(article?.relations?.around)) {
      const targetSlug = normalizeText(article.relations.around.article_id || article.relations.around.article_slug);
      if (targetSlug && !slugSet.has(targetSlug)) {
        errors.push(`${articleLabel}: relations.around.article_id must reference an existing article slug.`);
      }
    }
  });

  return { errors, warnings };
}

function validateCanonicalRoutes(rootDir) {
  const errors = [];

  return Promise.all([
    fs.readFile(path.join(rootDir, 'src/assets/scripts/gallery.js'), 'utf8'),
    fs.readFile(path.join(rootDir, 'src/assets/scripts/article-template.js'), 'utf8'),
    fs.readFile(path.join(rootDir, 'src/pages/articles/template.html'), 'utf8'),
  ]).then(([galleryScript, articleTemplateScript, compatibilityPage]) => {
    if (!galleryScript.includes("return 'article.html?slug=' + encodeURIComponent(normalizedSlug);")) {
      errors.push('Gallery cards must link to the canonical article.html?slug= route.');
    }

    if (articleTemplateScript.includes('template.html?slug=')) {
      errors.push('Article template runtime must not hardcode the legacy template.html?slug= route.');
    }

    if (!compatibilityPage.includes("../article.html?slug=' + encodeURIComponent(slug)")) {
      errors.push('articles/template.html must redirect legacy requests to ../article.html?slug=...');
    }

    return errors;
  });
}

export async function validateProject(options = {}) {
  const rootDir = options.rootDir || DEFAULT_ROOT;
  const requireDist = options.requireDist === true;
  const sourceArticles = await readArticlesJson(rootDir, 'src/data/articles.json');

  const missingSourceFiles = await collectMissing(rootDir, REQUIRED_SOURCE_FILES);
  const missingSourceAssetRefs = await collectMissingAssetRefs(rootDir, 'src/data/articles.json', 'src');
  const missingDistFiles = requireDist
    ? await collectMissing(path.join(rootDir, 'dist'), REQUIRED_DIST_FILES)
    : [];
  const missingDistAssetRefs = requireDist
    ? await collectMissingAssetRefs(path.join(rootDir, 'dist'), 'data/articles.json', '.')
    : [];
  const corruptedSourceText = await collectCorruptedTextInFiles(rootDir, SOURCE_TEXT_FILES);
  const unreferencedDistArticleAssets = requireDist
    ? await collectUnreferencedArticleAssets(path.join(rootDir, 'dist'), 'data/articles.json', '.')
    : [];
  const routeErrors = await validateCanonicalRoutes(rootDir);

  const errors = [];
  const warnings = [];
  const schemaResult = validateArticleSchema(sourceArticles);

  if (missingSourceFiles.length) {
    errors.push(
      'Missing required source files:\n' + missingSourceFiles.map((item) => `- ${item}`).join('\n')
    );
  }

  if (missingSourceAssetRefs.length) {
    errors.push(
      formatMissingAssetRefs(
        'Missing runtime source assets referenced by src/data/articles.json:',
        missingSourceAssetRefs
      )
    );
  }

  if (missingDistFiles.length) {
    errors.push(
      'Missing required published files in dist:\n' + missingDistFiles.map((item) => `- ${item}`).join('\n')
    );
  }

  if (missingDistAssetRefs.length) {
    errors.push(
      formatMissingAssetRefs(
        'Missing published runtime assets referenced by dist/data/articles.json:',
        missingDistAssetRefs
      )
    );
  }

  if (corruptedSourceText.length) {
    errors.push(
      'Corrupted source text detected:\n' + corruptedSourceText.map((item) => `- ${item}`).join('\n')
    );
  }

  if (unreferencedDistArticleAssets.length) {
    errors.push(
      'Published article image assets are not referenced by dist/data/articles.json:\n'
      + unreferencedDistArticleAssets.map((item) => `- ${item}`).join('\n')
    );
  }

  if (schemaResult.errors.length) {
    errors.push(
      'Schema or taxonomy validation failed for src/data/articles.json:\n'
      + schemaResult.errors.map((item) => `- ${item}`).join('\n')
    );
  }

  if (routeErrors.length) {
    errors.push(
      'Canonical route validation failed:\n' + routeErrors.map((item) => `- ${item}`).join('\n')
    );
  }

  warnings.push(...schemaResult.warnings);

  return {
    ok: errors.length === 0,
    errors,
    warnings,
    missingSourceFiles,
    missingDistFiles,
    missingSourceAssetRefs,
    missingDistAssetRefs,
    publicationContract: {
      source: REQUIRED_SOURCE_FILES,
      dist: REQUIRED_DIST_FILES,
    },
  };
}

async function main() {
  const result = await validateProject({
    rootDir: DEFAULT_ROOT,
    requireDist: process.argv.includes('--require-dist'),
  });

  if (!result.ok) {
    for (const error of result.errors) {
      console.error(`ERROR\n${error}\n`);
    }
    process.exitCode = 1;
    return;
  }

  console.log('Validation passed.');
}

if (process.argv[1] && path.resolve(process.argv[1]) === __filename) {
  await main();
}
