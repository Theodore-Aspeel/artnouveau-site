(async function initGallery() {
  'use strict';

  const media = window.ArticleMedia;
  const taxonomy = window.ArticleTags;
  const grid = document.getElementById('gallery-grid');
  const paginationEl = document.getElementById('gallery-pagination');
  const stateEl = document.getElementById('gallery-state');
  const tagsEl = document.getElementById('gallery-tags');
  const curatedGrid = document.getElementById('home-curated-grid');
  const pathsGrid = document.getElementById('home-paths-grid');
  const rhythmGrid = document.getElementById('home-rhythm-grid');
  const titleEl = document.getElementById('journal-title');
  const introEl = document.getElementById('gallery-intro');

  if (!grid) return;

  const PAGE_SIZE = 12;
  const defaultTitle = titleEl ? titleEl.textContent : '';
  const defaultIntro = introEl ? introEl.textContent : '';
  const searchParams = new URLSearchParams(window.location.search);
  const articleDataUrl = new URL('data/articles.json', window.location.href);
  const requestedTag = taxonomy && typeof taxonomy.slugifyTag === 'function'
    ? taxonomy.slugifyTag(searchParams.get('tag'))
    : '';

  let currentPage = 0;
  let activeTag = null;
  let galleryItems = [];
  let allTags = [];

  function buildArticleHref(slug) {
    const normalizedSlug = normalizeText(slug);
    if (!normalizedSlug) return 'article.html';
    return 'article.html?slug=' + encodeURIComponent(normalizedSlug);
  }

  function normalizeText(value) {
    if (taxonomy && typeof taxonomy.normalizeText === 'function') {
      return taxonomy.normalizeText(value);
    }

    return typeof value === 'string' ? value.trim() : '';
  }

  function getCardExcerpt(article) {
    const chapeau = normalizeText(article.chapeau);
    if (chapeau) return chapeau;

    const metaDescription = normalizeText(article.meta_description);
    if (metaDescription) return metaDescription;

    return '';
  }

  function getCardImage(article) {
    if (media && typeof media.getPrimaryImage === 'function') {
      return media.getPrimaryImage(article);
    }

    return normalizeText(article.hero_image);
  }

  function resolveCardImageSrc(imagePath) {
    const normalizedPath = normalizeText(imagePath);
    if (!normalizedPath) return '';

    const candidate = media && typeof media.resolveImagePath === 'function'
      ? media.resolveImagePath(normalizedPath, '')
      : normalizedPath;

    return new URL(candidate, window.location.href).href;
  }

  function getCardTags(article) {
    if (taxonomy && typeof taxonomy.getArticleTags === 'function') {
      return taxonomy.getArticleTags(article);
    }

    return [];
  }

  function getCardStyle(article) {
    if (taxonomy && typeof taxonomy.getArticleStyle === 'function') {
      return taxonomy.getArticleStyle(article);
    }

    return normalizeText(article && article.style);
  }

  function getArticleDate(article) {
    if (article && article.verified_info && typeof article.verified_info.date === 'string' && article.verified_info.date.trim()) {
      return article.verified_info.date.trim();
    }

    if (article && article.practical && typeof article.practical.Datation === 'string' && article.practical.Datation.trim()) {
      return article.practical.Datation.trim();
    }

    return '';
  }

  function deriveGalleryItems(articles) {
    const seenSlugs = new Set();

    return articles
      .filter((article) => {
        const slug = normalizeText(article.slug);
        const title = normalizeText(article.title);

        if (!slug || !title || seenSlugs.has(slug)) return false;
        seenSlugs.add(slug);
        return true;
      })
      .sort((left, right) => {
        const leftOrder = Number.isFinite(left.publication_order_recommended) ? left.publication_order_recommended : Number.MAX_SAFE_INTEGER;
        const rightOrder = Number.isFinite(right.publication_order_recommended) ? right.publication_order_recommended : Number.MAX_SAFE_INTEGER;

        if (leftOrder !== rightOrder) return leftOrder - rightOrder;
        return normalizeText(left.title).localeCompare(normalizeText(right.title), 'fr');
      })
      .map((article) => ({
        slug: article.slug,
        title: article.title,
        country: article.country || '',
        city: article.city || '',
        style: getCardStyle(article),
        format: article.format || '',
        date: getArticleDate(article),
        excerpt: getCardExcerpt(article),
        image: getCardImage(article),
        tags: getCardTags(article),
      }));
  }

  function addPlaceholder(imageWrapper, item) {
    imageWrapper.classList.add('card__image-wrapper--empty');

    if (imageWrapper.querySelector('.card__placeholder')) return;

    const placeholder = document.createElement('span');
    placeholder.className = 'card__placeholder';
    placeholder.textContent = item.city || item.country || item.style || 'Article';
    imageWrapper.appendChild(placeholder);
  }

  function buildTagChip(tag, className, isActive) {
    const link = document.createElement('a');
    link.className = className + (isActive ? ' tag-chip--active' : '');
    link.href = taxonomy && typeof taxonomy.buildTagHref === 'function'
      ? taxonomy.buildTagHref(tag, 'index.html')
      : 'index.html#galerie';
    link.textContent = tag;
    return link;
  }

  function buildCard(item) {
    const article = document.createElement('article');
    article.className = 'card';

    const link = document.createElement('a');
    link.className = 'card__link';
    link.href = buildArticleHref(item.slug);
    link.setAttribute('aria-label', 'Lire l’article : ' + item.title);

    const imageWrapper = document.createElement('div');
    imageWrapper.className = 'card__image-wrapper';

    if (item.image) {
      const img = document.createElement('img');
      img.src = resolveCardImageSrc(item.image);
      img.alt = item.title;
      img.loading = 'lazy';
      img.addEventListener('error', () => {
        img.remove();
        addPlaceholder(imageWrapper, item);
      }, { once: true });
      imageWrapper.appendChild(img);
    } else {
      addPlaceholder(imageWrapper, item);
    }

    if (item.style) {
      const tag = document.createElement('span');
      tag.className = 'card__tag';
      tag.textContent = item.style;
      imageWrapper.appendChild(tag);
    }

    const body = document.createElement('div');
    body.className = 'card__body';

    if (item.country) {
      const meta = document.createElement('p');
      meta.className = 'card__meta';
      meta.textContent = item.country;
      body.appendChild(meta);
    }

    const title = document.createElement('h3');
    title.className = 'card__title';
    title.textContent = item.title;
    body.appendChild(title);

    if (item.excerpt) {
      const excerpt = document.createElement('p');
      excerpt.className = 'card__excerpt';
      excerpt.textContent = item.excerpt;
      body.appendChild(excerpt);
    }

    if (item.city) {
      const city = document.createElement('p');
      city.className = 'card__city';
      city.textContent = item.city;
      body.appendChild(city);
    }

    link.appendChild(imageWrapper);
    link.appendChild(body);
    article.appendChild(link);

    if (item.tags.length) {
      const tagList = document.createElement('div');
      tagList.className = 'tag-list card__tags';
      item.tags.slice(0, 3).forEach((tag) => {
        const isActive = activeTag && taxonomy && taxonomy.slugifyTag(tag) === activeTag.slug;
        tagList.appendChild(buildTagChip(tag, 'tag-chip tag-chip--muted', isActive));
      });
      article.appendChild(tagList);
    }

    return article;
  }

  function buildEditorialLink(item, className) {
    const link = document.createElement('a');
    link.className = className;
    link.href = buildArticleHref(item.slug);
    return link;
  }

  function buildCuratedCard(item, index) {
    const article = document.createElement('article');
    article.className = 'home-curated__card' + (index === 0 ? ' home-curated__card--lead' : '');
    const link = buildEditorialLink(item, 'home-curated__link');

    const mediaWrap = document.createElement('div');
    mediaWrap.className = 'home-curated__media';

    if (item.image) {
      const img = document.createElement('img');
      img.className = 'home-curated__image';
      img.src = resolveCardImageSrc(item.image);
      img.alt = item.title;
      img.loading = 'lazy';
      mediaWrap.appendChild(img);
    } else {
      const placeholder = document.createElement('div');
      placeholder.className = 'home-curated__placeholder';
      placeholder.textContent = item.city || item.country || 'Article';
      mediaWrap.appendChild(placeholder);
    }

    const body = document.createElement('div');
    body.className = 'home-curated__body';

    const eyebrow = document.createElement('p');
    eyebrow.className = 'home-curated__eyebrow';
    eyebrow.textContent = index === 0 ? 'À lire d’abord' : 'Puis poursuivre';
    body.appendChild(eyebrow);

    const title = document.createElement('h3');
    title.className = 'home-curated__title';
    title.textContent = item.title;
    body.appendChild(title);

    const meta = document.createElement('p');
    meta.className = 'home-curated__meta';
    meta.textContent = [item.city, item.country, item.date].filter(Boolean).join(' · ');
    body.appendChild(meta);

    if (item.excerpt) {
      const excerpt = document.createElement('p');
      excerpt.className = 'home-curated__excerpt';
      excerpt.textContent = item.excerpt;
      body.appendChild(excerpt);
    }

    link.appendChild(mediaWrap);
    link.appendChild(body);
    article.appendChild(link);
    return article;
  }

  function buildPathCard(cityEntry) {
    const article = document.createElement('article');
    article.className = 'home-paths__card';

    const header = document.createElement('div');
    header.className = 'home-paths__card-head';

    const title = document.createElement('h3');
    title.className = 'home-paths__city';
    title.textContent = cityEntry.city;
    header.appendChild(title);

    const count = document.createElement('p');
    count.className = 'home-paths__count';
    count.textContent = cityEntry.items.length + ' article' + (cityEntry.items.length > 1 ? 's' : '');
    header.appendChild(count);

    article.appendChild(header);

    if (cityEntry.styles.length) {
      const styles = document.createElement('p');
      styles.className = 'home-paths__styles';
      styles.textContent = cityEntry.styles.slice(0, 2).join(' / ');
      article.appendChild(styles);
    }

    const list = document.createElement('div');
    list.className = 'home-paths__list';

    cityEntry.items.slice(0, 3).forEach((item, index) => {
      const link = buildEditorialLink(item, 'home-paths__item');

      const label = document.createElement('span');
      label.className = 'home-paths__item-label';
      label.textContent = index === 0 ? 'Commencer' : 'Ensuite';

      const itemTitle = document.createElement('span');
      itemTitle.className = 'home-paths__item-title';
      itemTitle.textContent = item.title;

      const itemMeta = document.createElement('span');
      itemMeta.className = 'home-paths__item-meta';
      itemMeta.textContent = [item.style, item.date].filter(Boolean).join(' · ');

      link.appendChild(label);
      link.appendChild(itemTitle);
      if (itemMeta.textContent) {
        link.appendChild(itemMeta);
      }

      list.appendChild(link);
    });

    article.appendChild(list);
    return article;
  }

  function buildRhythmCard(group) {
    const article = document.createElement('article');
    article.className = 'home-rhythm__card';

    const label = document.createElement('p');
    label.className = 'home-rhythm__label';
    label.textContent = group.label;
    article.appendChild(label);

    const title = document.createElement('h3');
    title.className = 'home-rhythm__title';
    title.textContent = group.title;
    article.appendChild(title);

    const intro = document.createElement('p');
    intro.className = 'home-rhythm__intro';
    intro.textContent = group.intro;
    article.appendChild(intro);

    const list = document.createElement('div');
    list.className = 'home-rhythm__list';

    group.items.slice(0, 3).forEach((item) => {
      const link = buildEditorialLink(item, 'home-rhythm__item');

      const itemTitle = document.createElement('span');
      itemTitle.className = 'home-rhythm__item-title';
      itemTitle.textContent = item.title;

      const itemMeta = document.createElement('span');
      itemMeta.className = 'home-rhythm__item-meta';
      itemMeta.textContent = [item.city, item.style].filter(Boolean).join(' · ');

      link.appendChild(itemTitle);
      if (itemMeta.textContent) {
        link.appendChild(itemMeta);
      }

      list.appendChild(link);
    });

    article.appendChild(list);
    return article;
  }

  function renderCurated(items) {
    if (!curatedGrid) return;
    curatedGrid.innerHTML = '';
    items.slice(0, 3).forEach((item, index) => {
      curatedGrid.appendChild(buildCuratedCard(item, index));
    });
  }

  function renderPaths(items) {
    if (!pathsGrid) return;
    pathsGrid.innerHTML = '';

    const cities = new Map();
    items.forEach((item) => {
      if (!item.city) return;
      const entry = cities.get(item.city) || { city: item.city, items: [], styles: [] };
      entry.items.push(item);
      if (item.style && !entry.styles.includes(item.style)) {
        entry.styles.push(item.style);
      }
      cities.set(item.city, entry);
    });

    [...cities.values()]
      .filter((entry) => entry.items.length >= 2)
      .sort((left, right) => {
        if (right.items.length !== left.items.length) return right.items.length - left.items.length;
        return left.city.localeCompare(right.city, 'fr');
      })
      .slice(0, 3)
      .forEach((entry) => {
        pathsGrid.appendChild(buildPathCard(entry));
      });
  }

  function renderRhythm(items) {
    if (!rhythmGrid) return;
    rhythmGrid.innerHTML = '';

    const longReads = items.filter((item) => item.format === 'article-complet');
    const shortNotes = items.filter((item) => item.format === 'article-court');

    [
      {
        label: 'Parcours développés',
        title: 'Prendre le temps d’une façade',
        intro: 'Des textes plus amples, quand le lieu demande plusieurs reprises du regard.',
        items: longReads,
      },
      {
        label: 'Notes brèves',
        title: 'Rester à la juste échelle',
        intro: 'Des sujets plus courts, quand une adresse ou un détail suffisent à tenir la lecture.',
        items: shortNotes,
      },
    ].forEach((group) => {
      if (group.items.length) {
        rhythmGrid.appendChild(buildRhythmCard(group));
      }
    });
  }

  function renderTagNav() {
    if (!tagsEl) return;

    tagsEl.innerHTML = '';

    const allLink = document.createElement('a');
    allLink.className = 'tag-chip tag-chip--ghost' + (activeTag ? '' : ' tag-chip--active');
    allLink.href = 'index.html#galerie';
    allLink.textContent = 'Tous';
    tagsEl.appendChild(allLink);

    allTags.forEach((tag) => {
      const isActive = activeTag && tag.slug === activeTag.slug;
      tagsEl.appendChild(buildTagChip(tag.label, 'tag-chip tag-chip--ghost', isActive));
    });
  }

  function renderState() {
    if (titleEl) {
      titleEl.textContent = activeTag ? 'Autour de ' + activeTag.label : defaultTitle;
    }

    if (introEl) {
      introEl.textContent = activeTag
        ? galleryItems.length + ' article' + (galleryItems.length > 1 ? 's' : '') + ' à lire à partir de ce repère.'
        : defaultIntro;
    }

    if (!stateEl) return;

    if (!activeTag) {
      stateEl.hidden = true;
      stateEl.innerHTML = '';
      return;
    }

    stateEl.hidden = false;
    stateEl.innerHTML = '';

    const eyebrow = document.createElement('span');
    eyebrow.className = 'gallery-state__label';
    eyebrow.textContent = 'Tag actif';

    const title = document.createElement('p');
    title.className = 'gallery-state__title';
    title.textContent = activeTag.label;

    const meta = document.createElement('p');
    meta.className = 'gallery-state__meta';
    meta.textContent = galleryItems.length + ' article' + (galleryItems.length > 1 ? 's' : '');

    const reset = document.createElement('a');
    reset.className = 'gallery-state__reset';
    reset.href = 'index.html#galerie';
    reset.textContent = 'Voir tous les articles';

    stateEl.appendChild(eyebrow);
    stateEl.appendChild(title);
    stateEl.appendChild(meta);
    stateEl.appendChild(reset);
  }

  function renderPagination(activePage) {
    if (!paginationEl) return;

    paginationEl.innerHTML = '';
    const totalPages = Math.ceil(galleryItems.length / PAGE_SIZE);
    if (totalPages <= 1) return;

    function makeBtn(label, ariaLabel, clickHandler, disabled, active) {
      const btn = document.createElement('button');
      btn.className = 'gallery__pagination__btn' + (active ? ' gallery__pagination__btn--active' : '');
      btn.textContent = label;
      btn.setAttribute('aria-label', ariaLabel);
      if (active) btn.setAttribute('aria-current', 'page');
      btn.disabled = disabled;
      btn.addEventListener('click', clickHandler);
      return btn;
    }

    paginationEl.appendChild(
      makeBtn('Prec.', 'Page précédente', () => goTo(currentPage - 1), activePage === 0, false)
    );

    for (let i = 0; i < totalPages; i += 1) {
      const page = i;
      paginationEl.appendChild(
        makeBtn(String(i + 1), 'Page ' + (i + 1), () => goTo(page), false, i === activePage)
      );
    }

    paginationEl.appendChild(
      makeBtn('Suiv.', 'Page suivante', () => goTo(currentPage + 1), activePage === totalPages - 1, false)
    );
  }

  function renderEmpty(messageText) {
    grid.innerHTML = '';
    const message = document.createElement('p');
    message.className = 'gallery__empty';
    message.textContent = messageText;
    grid.appendChild(message);
    if (paginationEl) paginationEl.innerHTML = '';
  }

  function renderPage(page) {
    const start = page * PAGE_SIZE;
    const items = galleryItems.slice(start, start + PAGE_SIZE);
    grid.innerHTML = '';
    items.forEach((item) => grid.appendChild(buildCard(item)));
    renderPagination(page);
  }

  function goTo(page) {
    currentPage = page;
    renderPage(currentPage);
    const section = grid.closest('section');
    if (section) section.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  try {
    const response = await fetch(articleDataUrl);
    if (!response.ok) throw new Error('fetch ' + response.status);

    const data = await response.json();
    const articles = Array.isArray(data.articles) ? data.articles : [];
    allTags = taxonomy && typeof taxonomy.collectTags === 'function' ? taxonomy.collectTags(articles) : [];
    activeTag = requestedTag && taxonomy && typeof taxonomy.findTagBySlug === 'function'
      ? taxonomy.findTagBySlug(articles, requestedTag)
      : null;
    const allItems = deriveGalleryItems(articles);

    const filteredArticles = activeTag
      ? articles.filter((article) => getCardTags(article).some((tag) => taxonomy.slugifyTag(tag) === activeTag.slug))
      : articles;

    galleryItems = deriveGalleryItems(filteredArticles);

    if (!activeTag) {
      renderCurated(allItems);
      renderPaths(allItems);
      renderRhythm(allItems);
    } else {
      if (curatedGrid) curatedGrid.innerHTML = '';
      if (pathsGrid) pathsGrid.innerHTML = '';
      if (rhythmGrid) rhythmGrid.innerHTML = '';
    }

    renderTagNav();
    renderState();

    if (!galleryItems.length) {
      renderEmpty(activeTag
        ? 'Aucun article ne correspond à ce tag pour le moment.'
        : 'Les articles ne peuvent pas être chargés pour le moment.');
      return;
    }

    renderPage(currentPage);
  } catch (error) {
    renderTagNav();
    renderState();
    renderEmpty('Les articles ne peuvent pas être chargés pour le moment.');
  }
})();
