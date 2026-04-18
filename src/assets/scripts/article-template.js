(async function initArticleTemplate() {
  'use strict';

  const media = window.ArticleMedia;
  const taxonomy = window.ArticleTags;
  const access = window.ArticleAccess;
  const i18n = window.SiteI18n;
  const instagramUrl = 'https://www.instagram.com/artnouveauetdeco';
  const root = document.getElementById('article-root');
  const script = document.currentScript;
  const dataset = script && script.dataset ? script.dataset : {};
  const articleJsonPath = script?.dataset.articleJson || '../../data/articles.json';
  const imageBase = dataset.imageBase ?? '../../';
  const homeHref = script?.dataset.homeHref || '../index.html';
  const galleryHref = script?.dataset.galleryHref || '../index.html#galerie';
  const articleHrefBase = script?.dataset.articleHrefBase || 'article.html?slug=';
  const searchParams = new URLSearchParams(window.location.search);
  const slug = searchParams.get('slug');

  if (!root || !access) return;

  function make(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  }

  function imgSrc(path) {
    if (!path) return '';

    const candidate = media && typeof media.resolveImagePath === 'function'
      ? media.resolveImagePath(path, imageBase)
      : (path.startsWith('http') || path.startsWith('/') ? path : imageBase + path);

    return new URL(candidate, window.location.href).href;
  }

  function articleTagHref(tag) {
    const href = taxonomy && typeof taxonomy.buildTagHref === 'function'
      ? taxonomy.buildTagHref(tag, homeHref)
      : galleryHref;

    return i18n && typeof i18n.withPreviewLocale === 'function' ? i18n.withPreviewLocale(href) : href;
  }

  function currentLocale() {
    if (i18n && typeof i18n.resolveLocale === 'function') {
      return i18n.resolveLocale();
    }

    const lang = (document.documentElement.lang || 'fr').trim().toLowerCase();
    return lang.split('-')[0] || 'fr';
  }

  function t(key, params) {
    return i18n && typeof i18n.t === 'function' ? i18n.t(key, params, currentLocale()) : key;
  }

  function previewHref(href) {
    return i18n && typeof i18n.withPreviewLocale === 'function' ? i18n.withPreviewLocale(href) : href;
  }

  function localizedValue(value) {
    if (typeof value === 'string') return value.trim();
    if (!value || typeof value !== 'object') return '';

    const locale = currentLocale();
    const direct = typeof value[locale] === 'string' ? value[locale].trim() : '';
    if (direct) return direct;

    const french = typeof value.fr === 'string' ? value.fr.trim() : '';
    if (french) return french;

    const english = typeof value.en === 'string' ? value.en.trim() : '';
    if (english) return english;

    for (const candidate of Object.values(value)) {
      if (typeof candidate === 'string' && candidate.trim()) {
        return candidate.trim();
      }
    }

    return '';
  }

  function cleanText(value) {
    return typeof value === 'string' && value.trim() ? value.trim() : '';
  }

  function capitalizeLeadingText(value) {
    const text = cleanText(value);
    if (!text) return '';
    return text.charAt(0).toLocaleUpperCase(currentLocale()) + text.slice(1);
  }

  function formatQuoteText(value) {
    const text = cleanText(value);
    if (!text) return '';

    const capitalized = text.charAt(0).toLocaleUpperCase(currentLocale()) + text.slice(1);
    return /["»”]$/.test(capitalized) ? capitalized : capitalized + '”';
  }

  function compactExactName(rawValue, articleData) {
    const raw = cleanText(rawValue);
    if (!raw) return '';

    const fallbackTitle = cleanText(articleData && articleData.title)
      .replace(/\s*\([^)]*\)\s*$/u, '')
      .replace(/\s*,\s*[^,]+$/u, '')
      .trim();

    let compact = raw
      .replace(/^(?:n[°ºo]\s*\d+[a-z]?\s*[\.\-:]?\s*)/iu, '')
      .replace(/^(?:poissonnerie|ancienne?\s+poissonnerie)\s+(?:a|à|au|aux|de|du|des|d['’])\s*/iu, '')
      .replace(/^(?:maison\s+et\s+atelier\s+de\s+l['’]architecte\s+)/iu, 'Maison ')
      .replace(/^(?:ancien(?:ne)?\s+atelier\s+et\s+habitation\s+de\s+)/iu, 'Maison de ')
      .replace(/\s{2,}/gu, ' ')
      .trim();

    const looksAddressLike = /\b(?:rue|avenue|boulevard|place|via|viale|straat|laan|weg|square|cours|chemin)\b/iu.test(compact);
    const remainsTooLong = fallbackTitle && compact.length > fallbackTitle.length + 18;

    if ((!compact || looksAddressLike || remainsTooLong) && fallbackTitle) {
      compact = fallbackTitle;
    }

    return capitalizeLeadingText(compact || raw);
  }

  function normalizedCompactExactName(rawValue, articleData) {
    const raw = cleanText(rawValue);
    if (!raw) return '';

    const fallbackTitle = cleanText(articleData && articleData.title)
      .replace(/\s*\([^)]*\)\s*$/u, '')
      .replace(/\s*,\s*[^,]+$/u, '')
      .trim();

    let compact = raw
      .replace(/^(?:n[\u00b0\u00bao]\s*\d+[a-z]?\s*[\.\-:]?\s*)/iu, '')
      .replace(/^(?:poissonnerie|ancienne?\s+poissonnerie)\s+(?:a|\u00e0|au|aux|de|du|des|d['\u2019])\s*/iu, '')
      .replace(/^(?:maison\s+et\s+atelier\s+de\s+l['\u2019]architecte\s+)/iu, 'Maison ')
      .replace(/^(?:ancien(?:ne)?\s+atelier\s+et\s+habitation\s+de\s+)/iu, 'Maison de ')
      .replace(/\s{2,}/gu, ' ')
      .trim();

    const looksAddressLike = /\b(?:rue|avenue|boulevard|place|via|viale|straat|laan|weg|square|cours|chemin)\b/iu.test(compact);
    const remainsTooLong = fallbackTitle && compact.length > fallbackTitle.length + 18;

    if ((!compact || looksAddressLike || remainsTooLong) && fallbackTitle) {
      compact = fallbackTitle;
    }

    return capitalizeLeadingText(compact || raw);
  }

  function normalizedQuoteText(value) {
    const text = cleanText(value);
    if (!text) return '';

    const normalized = text.replace(/^[\s"'`\u00ab\u00bb\u201c\u201d]+|[\s"'`\u00ab\u00bb\u201c\u201d]+$/gu, '');
    return capitalizeLeadingText(normalized);
  }

  function makeImageCaption(entry) {
    if (!entry || (!entry.caption && !entry.credit)) {
      return null;
    }

    const caption = make('figcaption', 'article-media-caption');

    if (entry.caption) {
      caption.appendChild(make('span', 'article-media-caption__text', entry.caption));
    }

    if (entry.credit) {
      if (caption.childNodes.length) {
        caption.appendChild(document.createTextNode(' '));
      }
      caption.appendChild(make('span', 'article-media-caption__credit', entry.credit));
    }

    return caption;
  }

  function sectionIdFromHeading(heading, index) {
    const base = cleanText(heading)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');

    return base ? `section-${index + 1}-${base}` : `section-${index + 1}`;
  }

  function renderNotFound() {
    document.title = t('article.notFound.title') + ' · Art Nouveau et Art Déco';
    const wrap = make('div', 'article-tpl__not-found');
    const h1 = make('h1', '', t('article.notFound.title'));
    const p = make('p', '', t('article.notFound.description'));
    const a = make('a', '', t('article.notFound.home'));
    a.href = previewHref(homeHref);
    p.appendChild(a);
    wrap.appendChild(h1);
    wrap.appendChild(p);
    root.appendChild(wrap);
  }

  function editorDraftStorageKey(articleSlug) {
    return `artnouveau:editor-draft-preview:${articleSlug}`;
  }

  function cloneJson(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function applyDraftPath(target, path, value) {
    const parts = String(path || '').split('.').filter(Boolean);
    if (!parts.length) return false;

    let cursor = target;
    for (let index = 0; index < parts.length - 1; index += 1) {
      const part = parts[index];
      if (part === '__proto__' || part === 'constructor' || part === 'prototype') return false;
      cursor = Array.isArray(cursor) ? cursor[Number(part)] : cursor && cursor[part];
      if (!cursor || typeof cursor !== 'object') return false;
    }

    const last = parts[parts.length - 1];
    if (last === '__proto__' || last === 'constructor' || last === 'prototype') return false;
    if (Array.isArray(cursor)) {
      const itemIndex = Number(last);
      if (!Number.isInteger(itemIndex) || itemIndex < 0 || itemIndex >= cursor.length) return false;
      cursor[itemIndex] = value;
      return true;
    }
    if (!cursor || typeof cursor !== 'object' || !(last in cursor)) return false;
    cursor[last] = value;
    return true;
  }

  function articleWithEditorDraft(article) {
    if (searchParams.get('editorDraft') !== '1') return article;

    let draft;
    try {
      draft = JSON.parse(window.localStorage.getItem(editorDraftStorageKey(slug)) || 'null');
    } catch (error) {
      return article;
    }

    if (!draft || draft.slug !== slug || !Array.isArray(draft.changes)) return article;
    if (Number(draft.expires_at) && Number(draft.expires_at) < Date.now()) {
      try {
        window.localStorage.removeItem(editorDraftStorageKey(slug));
      } catch (error) {
        return article;
      }
      return article;
    }

    const candidate = cloneJson(article);
    draft.changes.forEach((change) => {
      if (!change || typeof change !== 'object') return;
      applyDraftPath(candidate, change.field, typeof change.value === 'string' ? change.value : '');
    });
    return candidate;
  }

  if (!slug) {
    renderNotFound();
    return;
  }

  let data;
  try {
    const res = await fetch(articleJsonPath);
    if (!res.ok) throw new Error('fetch ' + res.status);
    data = await res.json();
  } catch (error) {
    renderNotFound();
    return;
  }

  let article = data.articles.find((item) => item.slug === slug);
  if (!article) {
    renderNotFound();
    return;
  }
  article = articleWithEditorDraft(article);

  const locale = currentLocale();
  const articleTitle = access.getArticleTitle(article, locale);
  const articleDek = access.getArticleDek(article, locale);
  const articleEpigraph = access.getArticleEpigraph(article, locale);
  const articleMetaDescription = access.getArticleMetaDescription(article, locale);
  const articleFormat = access.getArticleFormat(article);

  const orderedArticles = data.articles
    .filter((item) => item && item.slug)
    .slice()
    .sort((left, right) => {
      const leftOrder = access.getArticlePublicationOrder(left);
      const rightOrder = access.getArticlePublicationOrder(right);

      if (leftOrder !== rightOrder) return leftOrder - rightOrder;
      const leftTitle = access.getArticleTitle(left, locale);
      const rightTitle = access.getArticleTitle(right, locale);
      return leftTitle.localeCompare(rightTitle, locale);
    });
  const articleIndex = orderedArticles.findIndex((item) => item.slug === article.slug);
  const previousArticle = articleIndex > 0 ? orderedArticles[articleIndex - 1] : null;
  const nextArticle = articleIndex >= 0 && articleIndex < orderedArticles.length - 1
    ? orderedArticles[articleIndex + 1]
    : null;

  document.getElementById('page-title').textContent = articleTitle + ' · Art Nouveau et Art Déco';
  const metaEl = document.getElementById('page-description');
  if (metaEl && articleMetaDescription) {
    metaEl.setAttribute('content', articleMetaDescription);
  }

  const ogTitleEl = document.getElementById('og-title');
  if (ogTitleEl) {
    ogTitleEl.setAttribute('content', articleTitle + ' · Art Nouveau et Art Déco');
  }

  const ogDescriptionEl = document.getElementById('og-description');
  if (ogDescriptionEl && articleMetaDescription) {
    ogDescriptionEl.setAttribute('content', articleMetaDescription);
  }

  const twitterTitleEl = document.getElementById('twitter-title');
  if (twitterTitleEl) {
    twitterTitleEl.setAttribute('content', articleTitle + ' · Art Nouveau et Art Déco');
  }

  const twitterDescriptionEl = document.getElementById('twitter-description');
  if (twitterDescriptionEl && articleMetaDescription) {
    twitterDescriptionEl.setAttribute('content', articleMetaDescription);
  }

  const shell = make('article', 'container');
  root.appendChild(shell);

  const breadcrumb = document.createElement('nav');
  breadcrumb.className = 'breadcrumb';
  breadcrumb.setAttribute('aria-label', t('article.breadcrumb.aria'));
  breadcrumb.innerHTML = `
    <ol>
      <li><a href="${previewHref(homeHref)}">${t('article.breadcrumb.home')}</a></li>
      <li><a href="${previewHref(galleryHref)}">${t('article.breadcrumb.articles')}</a></li>
      <li aria-current="page"></li>
    </ol>
  `;
  breadcrumb.querySelector('[aria-current="page"]').textContent = articleTitle;
  shell.appendChild(breadcrumb);

  const primaryImageEntry = media && typeof media.getPrimaryImageEntry === 'function'
    ? media.getPrimaryImageEntry(article, locale)
    : null;
  const primaryImage = primaryImageEntry ? primaryImageEntry.src : '';
  const supportImageEntries = media && typeof media.getSecondaryImageEntries === 'function'
    ? media.getSecondaryImageEntries(article, 2, locale)
    : [];
  const articleTagEntries = taxonomy && typeof taxonomy.getArticleTagEntries === 'function'
    ? taxonomy.getArticleTagEntries(article, locale)
    : [];
  const articleTags = articleTagEntries.length
    ? articleTagEntries.map((tag) => tag.label)
    : taxonomy && typeof taxonomy.getArticleTags === 'function'
      ? taxonomy.getArticleTags(article, locale)
      : [];
  const articleTagFilters = articleTagEntries.length
    ? articleTagEntries
    : articleTags;
  const articleStyle = taxonomy && typeof taxonomy.getArticleStyle === 'function'
    ? taxonomy.getArticleStyle(article, locale)
    : access.getArticleTaxonomy(article, locale).styleLabel;
  const sourceQuote = article.sources && article.sources.quote ? article.sources.quote : article.quote;
  const verifiedQuote = sourceQuote && sourceQuote.verified && localizedValue(sourceQuote.text) ? sourceQuote : null;
  const editorial = article.editorial && typeof article.editorial === 'object' ? article.editorial : {};
  const bylineText = cleanText(editorial.author);
  const publishedOn = cleanText(editorial.published_on);
  const updatedOn = cleanText(editorial.updated_on);
  const imageCredit = cleanText(editorial.image_credit);
  const sourceNote = cleanText(editorial.source_note);
  const methodNote = cleanText(editorial.method_note);
  const factualDateItem = access && typeof access.getArticlePracticalItems === 'function'
    ? access.getArticlePracticalItems(article, locale).find((item) => item.key === 'date')
    : null;
  const factualDate = factualDateItem ? factualDateItem.value : '';
  const hasEditorialMeta = Boolean(bylineText || publishedOn || updatedOn || factualDate || imageCredit || sourceNote || methodNote);
  const sections = access.getArticleSections(article, locale);

  const intake = make('div', 'article-intake' + (primaryImage ? '' : ' article-intake--no-image'));
  if (articleFormat === 'article-court') {
    intake.classList.add('article-intake--compact');
  }

  const intakeHeader = make('header', 'article-intake__header article-header');

  const category = make('span', 'article-header__category');
  const articleTaxonomy = access && typeof access.getArticleTaxonomy === 'function'
    ? access.getArticleTaxonomy(article, locale)
    : { city: '', country: '' };
  category.textContent = [articleTaxonomy.city, articleTaxonomy.country].filter(Boolean).join(' · ');
  intakeHeader.appendChild(category);

  intakeHeader.appendChild(make('h1', 'article-header__title', articleTitle));

  const headerMetaValues = [articleStyle, articleTaxonomy.country]
    .filter(Boolean)
    .map((label) => ({ label, filter: label }))
    .concat(articleTagFilters.map((tag) => (tag && typeof tag === 'object'
      ? { label: tag.label, filter: tag }
      : { label: tag, filter: tag })))
    .filter((value) => value.label)
    .filter((value, index, values) => values.findIndex((item) => item.label === value.label) === index);

  if (headerMetaValues.length) {
    const meta = make('div', 'article-header__meta tag-list');
    headerMetaValues.forEach((value) => {
      const chip = make('a', 'tag-chip tag-chip--muted article-header__chip', value.label);
      chip.href = articleTagHref(value.filter);
      meta.appendChild(chip);
    });
    intakeHeader.appendChild(meta);
  }

  if (articleDek) {
    const intro = make('div', 'article-intro');
    intro.appendChild(make('p', '', articleDek));
    intakeHeader.appendChild(intro);
  }

  if (articleEpigraph && !verifiedQuote) {
    intakeHeader.appendChild(make('div', 'article-epigraph', articleEpigraph));
  }

  intake.appendChild(intakeHeader);

  if (primaryImage) {
    const figure = make('figure', 'article-intake__figure');
    const image = document.createElement('img');
    image.className = 'article-intake__image';
    image.src = imgSrc(primaryImage);
    image.alt = primaryImageEntry && primaryImageEntry.alt
      ? primaryImageEntry.alt
      : access.getArticleHeroAlt(article, locale);
    image.loading = 'eager';
    image.addEventListener('error', () => {
      figure.remove();
      intake.classList.add('article-intake--no-image');
    }, { once: true });
    figure.appendChild(image);

    const caption = makeImageCaption(primaryImageEntry);
    if (caption) {
      figure.appendChild(caption);
    }

    intake.appendChild(figure);
  }

  shell.appendChild(intake);

  const layout = make('div', 'article-layout');
  if (articleFormat === 'article-court') {
    layout.classList.add('article-layout--compact');
  }

  const content = make('div', 'article-content');
  const body = make('div', 'article-body');
  const sidebar = make('aside', 'article-sidebar');
  sidebar.setAttribute('aria-label', t('article.sidebar.aria'));
  layout.appendChild(content);
  layout.appendChild(sidebar);
  content.appendChild(body);
  shell.appendChild(layout);

  if (verifiedQuote) {
    const quoteBlock = make('section', 'article-verified-quote');
    quoteBlock.appendChild(make('p', 'article-verified-quote__label', t('article.quote')));

    const figure = document.createElement('figure');
    figure.className = 'article-verified-quote__figure';

    const blockquote = document.createElement('blockquote');
    blockquote.className = 'article-verified-quote__text';
    blockquote.textContent = normalizedQuoteText(localizedValue(verifiedQuote.text));
    figure.appendChild(blockquote);

    const authorText = localizedValue(verifiedQuote.author);
    if (authorText) {
      const caption = make('figcaption', 'article-verified-quote__caption');
      caption.appendChild(make('span', 'article-verified-quote__author', authorText));
      figure.appendChild(caption);
    }

    quoteBlock.appendChild(figure);
    content.insertBefore(quoteBlock, body);
  }

  function appendSupportGallery() {
    if (!supportImageEntries.length) {
      return;
    }

    const grid = make('div', 'article-gallery');
    supportImageEntries.forEach((entry, index) => {
      const fig = document.createElement('figure');
      if (index === 0 && supportImageEntries.length === 1) {
        fig.className = 'article-gallery__figure article-gallery__figure--single';
      }

      const im = document.createElement('img');
      im.src = imgSrc(entry.src);
      im.alt = entry.alt || '';
      im.loading = 'lazy';
      im.addEventListener('error', () => {
        fig.remove();
        if (!grid.children.length) {
          grid.remove();
        }
      }, { once: true });
      fig.appendChild(im);

      const caption = makeImageCaption(entry);
      if (caption) {
        fig.appendChild(caption);
      }

      grid.appendChild(fig);
    });

    body.appendChild(grid);
  }

  if (sections.length) {
    sections.forEach((section, index) => {
      const sec = make('section', 'article-body__section');
      sec.id = sectionIdFromHeading(section.heading, index);
      sec.appendChild(make('h2', '', section.heading));
      section.body.split(/\n{2,}/).forEach((txt) => {
        const trimmed = txt.trim();
        if (trimmed) sec.appendChild(make('p', '', trimmed));
      });
      body.appendChild(sec);

      if (index === 0 && articleFormat !== 'article-court') {
        appendSupportGallery();
      }
    });
  }

  if (!sections.length || articleFormat === 'article-court') {
    appendSupportGallery();
  }

  const resources = access.getArticleResources(article, locale);

  if (resources.length) {
    const resourcesBlock = make('section', 'article-resources');
    resourcesBlock.appendChild(make('p', 'article-resources__label', t('article.resources')));
    resourcesBlock.appendChild(make('h2', 'article-resources__title', t('article.resources.more')));

    const list = make('div', 'article-resources__list');

    resources.slice(0, 4).forEach((resource) => {
      const item = make('article', 'article-resources__item');
      const link = make('a', 'article-resources__link', resource.title);
      link.href = resource.href;

      if (/^https?:/i.test(resource.href)) {
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
      }

      item.appendChild(link);

      if (resource.kind) {
        item.appendChild(make('p', 'article-resources__kind', resource.kind));
      }

      if (resource.note) {
        item.appendChild(make('p', 'article-resources__note', resource.note));
      }

      list.appendChild(item);
    });

    resourcesBlock.appendChild(list);
    content.appendChild(resourcesBlock);
  }

  if (previousArticle || nextArticle) {
    const continuation = make('nav', 'article-sequence');
    continuation.setAttribute('aria-label', t('article.continue'));
    continuation.appendChild(make('p', 'article-sequence__label', t('article.continue')));

    const links = make('div', 'article-sequence__grid');

    function buildSequenceCard(item, direction) {
      const link = make('a', 'article-sequence__card');
      link.href = previewHref(articleHrefBase + encodeURIComponent(item.slug));

      const eyebrow = make('span', 'article-sequence__eyebrow', direction);
      const sequenceTitle = access.getArticleTitle(item, locale);
      const sequenceTaxonomy = access.getArticleTaxonomy(item, locale);
      const title = make('span', 'article-sequence__title', sequenceTitle);
      const metaText = [sequenceTaxonomy.city, sequenceTaxonomy.country].filter(Boolean).join(' · ');

      link.appendChild(eyebrow);
      link.appendChild(title);

      if (metaText) {
        link.appendChild(make('span', 'article-sequence__meta', metaText));
      }

      return link;
    }

    if (previousArticle) {
      links.appendChild(buildSequenceCard(previousArticle, t('article.previous')));
    }

    if (nextArticle) {
      links.appendChild(buildSequenceCard(nextArticle, t('article.next')));
    }

    continuation.appendChild(links);
    content.appendChild(continuation);
  }

  const practicalItems = access.getArticlePracticalItems(article, locale);

  if (practicalItems.length) {
    const block = make('div', 'article-tpl__facts');
    block.appendChild(make('p', 'article-tpl__block-label', t('article.facts')));
    const dl = document.createElement('dl');
    practicalItems.forEach((item) => {
      const value = item.key === 'exact_name' ? normalizedCompactExactName(item.value, article) : item.value;
      dl.appendChild(make('dt', '', item.label));
      dl.appendChild(make('dd', '', value));
    });
    block.appendChild(dl);

    sidebar.appendChild(block);
  }

  function appendEditorialBlock() {
    if (!hasEditorialMeta) {
      return;
    }

    const editorialBlock = make('div', 'article-tpl__facts article-tpl__facts--editorial');
    editorialBlock.appendChild(make('p', 'article-tpl__block-label', t('article.editorial.frame')));
    const dl = document.createElement('dl');

    if (bylineText) {
      dl.appendChild(make('dt', '', t('article.author')));
      dl.appendChild(make('dd', '', bylineText));
    }

    if (publishedOn) {
      dl.appendChild(make('dt', '', t('article.publication')));
      dl.appendChild(make('dd', '', publishedOn));
    }

    if (updatedOn) {
      dl.appendChild(make('dt', '', t('article.revision')));
      dl.appendChild(make('dd', '', updatedOn));
    }

    if (imageCredit) {
      dl.appendChild(make('dt', '', t('article.imageCredit')));
      dl.appendChild(make('dd', '', imageCredit));
    }

    if (sourceNote) {
      dl.appendChild(make('dt', '', t('article.source')));
      dl.appendChild(make('dd', '', sourceNote));
    }

    if (methodNote) {
      dl.appendChild(make('dt', '', t('article.method')));
      dl.appendChild(make('dd', '', methodNote));
    }

    if (dl.childElementCount) {
      editorialBlock.appendChild(dl);
    }

    editorialBlock.appendChild(make('p', 'article-tpl__rigor-note', t('article.editorial.rigorNote')));
    sidebar.appendChild(editorialBlock);
  }

  const aroundItem = access.getArticleAround(article, locale);
  const aroundTarget = aroundItem && aroundItem.articleSlug
    ? data.articles.find((item) => item.slug === aroundItem.articleSlug)
    : null;
  const articleGaps = access.getArticleGaps(article);

  if (aroundItem || articleGaps.length || instagramUrl) {
    const block = make('div', 'article-tpl__around');
    const hasEditorialAside = Boolean(aroundItem) || articleGaps.length;
    block.appendChild(make('p', 'article-tpl__block-label', hasEditorialAside ? t('article.around') : t('article.instagram')));

    if (aroundItem) {
      if (aroundItem.relationLabel) {
        block.appendChild(make('p', 'article-tpl__around-relation', aroundItem.relationLabel));
      }

      if (aroundTarget) {
        const aroundTitle = access.getArticleTitle(aroundTarget, locale);
        const aroundLink = make('a', 'article-tpl__around-link', aroundTitle);
        aroundLink.href = previewHref(articleHrefBase + encodeURIComponent(aroundTarget.slug));
        block.appendChild(aroundLink);
      } else if (aroundItem.articleTitle) {
        block.appendChild(make('p', 'article-tpl__around-link article-tpl__around-link--static', aroundItem.articleTitle));
      }

      if (aroundItem.note) {
        block.appendChild(make('p', 'article-tpl__around-text', aroundItem.note));
      }
    }

    if (articleGaps.length) {
      const note = make('p', 'article-tpl__subhead', t('article.toConfirm'));
      block.appendChild(note);
      const ul = document.createElement('ul');
      ul.className = 'article-tpl__gaps-list';
      articleGaps.forEach((gap) => ul.appendChild(make('li', '', gap)));
      block.appendChild(ul);
    }

    const sidebarInstagram = make('p', 'article-tpl__instagram-inline');
    sidebarInstagram.appendChild(document.createTextNode(t('article.instagram.prefix')));
    const sidebarInstagramLink = make('a', 'article-tpl__instagram-link', '@artnouveauetdeco');
    sidebarInstagramLink.href = instagramUrl;
    sidebarInstagramLink.target = '_blank';
    sidebarInstagramLink.rel = 'noopener noreferrer';
    sidebarInstagramLink.setAttribute('aria-label', t('article.instagram.aria'));
    sidebarInstagram.appendChild(sidebarInstagramLink);
    block.appendChild(sidebarInstagram);

    sidebar.appendChild(block);
  }

})();
