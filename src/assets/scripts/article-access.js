(function attachArticleAccess(global) {
  'use strict';

  const STYLE_LABELS = {
    art_nouveau: { fr: 'Art Nouveau', en: 'Art Nouveau', nl: 'Art nouveau' },
    art_nouveau_geometric: { fr: 'Art Nouveau géométrique', en: 'Geometric Art Nouveau', nl: 'Geometrische art nouveau' },
    art_deco: { fr: 'Art Déco', en: 'Art Deco', nl: 'Art deco' },
    liberty_art_nouveau: { fr: 'Liberty / Art Nouveau', en: 'Liberty / Art Nouveau', nl: 'Liberty / art nouveau' },
    vienna_secession: { fr: 'Sécession viennoise', en: 'Vienna Secession', nl: 'Weense Secessie' },
  };

  const TAG_LABELS = {
    art_nouveau: { fr: 'Art Nouveau', en: 'Art Nouveau', nl: 'Art nouveau' },
    art_deco: { fr: 'Art Déco', en: 'Art Deco', nl: 'Art deco' },
    public_building: { fr: 'Bâtiment public', en: 'Public building', nl: 'Openbaar gebouw' },
    commerce: { fr: 'Commerce', en: 'Commerce', nl: 'Handel' },
    facade: { fr: 'Façade', en: 'Facade', nl: 'Gevel' },
    habitat: { fr: 'Habitat', en: 'Housing', nl: 'Wonen' },
    liberty: { fr: 'Liberty', en: 'Liberty', nl: 'Liberty' },
    floral_motif: { fr: 'Motif floral', en: 'Floral motif', nl: 'Bloemmotief' },
    threshold: { fr: 'Seuil', en: 'Threshold', nl: 'Drempel' },
    vienna_secession: { fr: 'Sécession viennoise', en: 'Vienna Secession', nl: 'Weense Secessie' },
    urban_lettering: { fr: 'Écriture urbaine', en: 'Urban lettering', nl: 'Stedelijke belettering' },
  };

  const RELATION_LABELS = {
    same_city: { fr: 'Même ville', en: 'Same city', nl: 'Zelfde stad' },
    counterpoint: { fr: 'Contrepoint', en: 'Counterpoint', nl: 'Contrapunt' },
    other_scale: { fr: 'Autre échelle', en: 'Another scale', nl: 'Andere schaal' },
  };

  const PRACTICAL_LABELS = {
    exact_name: { fr: 'Nom exact', en: 'Exact name', nl: 'Exacte naam' },
    city: { fr: 'Ville', en: 'City', nl: 'Stad' },
    country: { fr: 'Pays', en: 'Country', nl: 'Land' },
    style: { fr: 'Style', en: 'Style', nl: 'Stijl' },
    architect: { fr: 'Architecte', en: 'Architect', nl: 'Architect' },
    address: { fr: 'Adresse', en: 'Address', nl: 'Adres' },
    date: { fr: 'Datation', en: 'Date', nl: 'Datering' },
    access: { fr: 'Accès', en: 'Access', nl: 'Toegang' },
  };

  const PRACTICAL_KEY_BY_V1_LABEL = {
    Ville: 'city',
    Pays: 'country',
    Style: 'style',
    Architecte: 'architect',
    Adresse: 'address',
    Datation: 'date',
    Accès: 'access',
  };
  const localeConfig = global.SiteLocales || {};
  const DEFAULT_LOCALE = localeConfig.defaultLocale || 'fr';
  const FALLBACK_LOCALES = Array.isArray(localeConfig.fallbackLocales)
    ? localeConfig.fallbackLocales
    : ['fr', 'en'];

  function isPlainObject(value) {
    return Boolean(value) && typeof value === 'object' && !Array.isArray(value);
  }

  function normalizeText(value) {
    return typeof value === 'string' ? value.trim() : '';
  }

  function normalizeLocale(locale) {
    if (typeof localeConfig.normalizeLocale === 'function') {
      return localeConfig.normalizeLocale(locale);
    }
    return normalizeText(locale || DEFAULT_LOCALE).toLowerCase().split('-')[0] || DEFAULT_LOCALE;
  }

  function localizedValue(value, locale, fallbackValue) {
    if (typeof value === 'string') return normalizeText(value);
    if (!isPlainObject(value)) return normalizeText(fallbackValue);

    const lang = normalizeLocale(locale);
    const direct = normalizeText(value[lang]);
    if (direct) return direct;

    for (const fallbackLocale of FALLBACK_LOCALES) {
      const fallbackText = normalizeText(value[fallbackLocale]);
      if (fallbackText) return fallbackText;
    }

    for (const candidate of Object.values(value)) {
      const text = normalizeText(candidate);
      if (text) return text;
    }

    return normalizeText(fallbackValue);
  }

  function localizedLabel(labels, key, locale, fallbackValue) {
    return localizedValue(labels[key], locale, fallbackValue || key);
  }

  function getLocaleContent(article, locale) {
    if (!isPlainObject(article)) return {};
    const content = isPlainObject(article.content) ? article.content : null;
    if (!content) return {};

    const lang = normalizeLocale(locale);
    if (isPlainObject(content[lang])) return content[lang];
    for (const fallbackLocale of FALLBACK_LOCALES) {
      if (isPlainObject(content[fallbackLocale])) return content[fallbackLocale];
    }
    return {};
  }

  function getArticleContent(article, locale = DEFAULT_LOCALE) {
    const selected = getLocaleContent(article, locale);
    const required = getLocaleContent(article, DEFAULT_LOCALE);

    return Object.assign({}, required, selected);
  }

  function hasNonEmptySection(sections) {
    return Array.isArray(sections) && sections.some((section) => (
      isPlainObject(section)
      && (normalizeText(section.heading) || normalizeText(section.body))
    ));
  }

  function isArticleLocaleReady(article, locale) {
    const content = isPlainObject(article && article.content) ? article.content : {};
    const lang = normalizeLocale(locale);
    const localeContent = isPlainObject(content[lang]) ? content[lang] : {};

    return Boolean(
      normalizeText(localeContent.title)
      && normalizeText(localeContent.dek)
      && hasNonEmptySection(localeContent.sections)
    );
  }

  function getArticleTitle(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    return normalizeText(content.title) || normalizeText(article && article.title);
  }

  function getArticleDek(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    return normalizeText(content.dek || content.chapeau) || normalizeText(article && article.chapeau);
  }

  function getArticleEpigraph(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    return normalizeText(content.epigraph) || normalizeText(article && article.epigraph);
  }

  function getArticleMetaDescription(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    const seo = isPlainObject(content.seo) ? content.seo : {};
    return normalizeText(seo.meta_description || content.meta_description) || normalizeText(article && article.meta_description);
  }

  function getArticleSections(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    const sections = Array.isArray(content.sections) && content.sections.length
      ? content.sections
      : article && article.sections;

    return (Array.isArray(sections) ? sections : [])
      .filter((section) => isPlainObject(section))
      .map((section) => ({
        heading: normalizeText(section.heading),
        body: normalizeText(section.body),
      }))
      .filter((section) => section.heading || section.body);
  }

  function normalizeImageEntry(image) {
    if (typeof image === 'string') {
      const src = normalizeText(image);
      return src ? { src, alt: '', caption: '', credit: '' } : null;
    }

    if (!isPlainObject(image)) return null;

    const src = normalizeText(image.src || image.path || image.image);
    if (!src) return null;

    return {
      src,
      alt: normalizeText(image.alt),
      caption: normalizeText(image.caption),
      credit: normalizeText(image.credit),
    };
  }

  function getArticleMedia(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    const contentMedia = isPlainObject(content.media) ? content.media : {};
    const sourceMedia = isPlainObject(article && article.media) ? article.media : {};

    const hero = normalizeImageEntry(sourceMedia.hero || (article && article.hero_image));
    const supportSource = Array.isArray(sourceMedia.support)
      ? sourceMedia.support
      : (Array.isArray(article && article.support_images) ? article.support_images : []);
    const supportAlt = Array.isArray(contentMedia.support_alt) ? contentMedia.support_alt : [];

    if (hero && !hero.alt) {
      hero.alt = normalizeText(contentMedia.hero_alt) || normalizeText(article && article.alt_text);
    }

    const support = supportSource
      .map((entry, index) => {
        const normalized = normalizeImageEntry(entry);
        if (normalized && !normalized.alt) {
          normalized.alt = normalizeText(supportAlt[index]);
        }
        return normalized;
      })
      .filter(Boolean);

    return { hero, support };
  }

  function getArticleHeroAlt(article, locale = DEFAULT_LOCALE) {
    const media = getArticleMedia(article, locale);
    return normalizeText(media.hero && media.hero.alt) || getArticleTitle(article, locale);
  }

  function getArticleTaxonomy(article, locale = DEFAULT_LOCALE) {
    const taxonomy = isPlainObject(article && article.taxonomy) ? article.taxonomy : {};
    const facts = isPlainObject(article && article.facts) ? article.facts : {};
    const location = isPlainObject(facts.location) ? facts.location : {};

    const styleKey = normalizeText(taxonomy.style_key);
    const tagKeys = Array.isArray(taxonomy.tag_keys)
      ? taxonomy.tag_keys.map(normalizeText).filter(Boolean)
      : [];

    return {
      styleKey,
      styleLabel: styleKey
        ? localizedLabel(STYLE_LABELS, styleKey, locale, styleKey)
        : normalizeText(article && article.style),
      tagKeys,
      tagLabels: tagKeys.length
        ? tagKeys.map((key) => localizedLabel(TAG_LABELS, key, locale, key))
        : (Array.isArray(article && article.tags) ? article.tags.map(normalizeText).filter(Boolean) : []),
      city: normalizeText(location.city) || normalizeText(article && article.city),
      country: normalizeText(location.country) || normalizeText(article && article.country),
      countryCode: normalizeText(location.country_code),
    };
  }

  function getArticlePublicationOrder(article) {
    const publication = isPlainObject(article && article.publication) ? article.publication : {};
    const order = publication.order ?? (article && article.publication_order_recommended);
    return Number.isFinite(order) ? order : Number.MAX_SAFE_INTEGER;
  }

  function getArticleFormat(article) {
    const format = normalizeText(article && article.format);
    if (format === 'short') return 'article-court';
    if (format === 'long') return 'article-complet';
    return format;
  }

  function getArticlePracticalItems(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    const facts = isPlainObject(article && article.facts) ? article.facts : {};
    const location = isPlainObject(facts.location) ? facts.location : {};
    const dates = isPlainObject(facts.dates) ? facts.dates : {};
    const identity = isPlainObject(article && article.identity) ? article.identity : {};
    const taxonomy = getArticleTaxonomy(article, locale);

    const valuesByKey = {
      exact_name: normalizeText(identity.exact_name),
      city: taxonomy.city,
      country: taxonomy.country,
      style: taxonomy.styleLabel,
      address: normalizeText(location.address),
      date: normalizeText(dates.built || dates.created),
      architect: Array.isArray(facts.people)
        ? facts.people.filter((person) => person && person.role === 'architect').map((person) => normalizeText(person.name)).filter(Boolean).join(', ')
        : '',
    };

    if (Array.isArray(content.practical_items)) {
      return content.practical_items
        .filter((item) => isPlainObject(item))
        .map((item) => {
          const key = normalizeText(item.key);
          const value = localizedValue(item.value, locale, valuesByKey[key]);
          return {
            key,
            label: localizedLabel(PRACTICAL_LABELS, key, locale, normalizeText(item.label) || key),
            value,
          };
        })
        .filter((item) => item.key && item.value);
    }

    if (isPlainObject(article && article.practical)) {
      return Object.entries(article.practical)
        .map(([label, value]) => {
          const key = PRACTICAL_KEY_BY_V1_LABEL[label] || label;
          return {
            key,
            label: localizedLabel(PRACTICAL_LABELS, key, locale, label),
            value: normalizeText(value),
          };
        })
        .filter((item) => item.value);
    }

    return Object.entries(valuesByKey)
      .map(([key, value]) => ({
        key,
        label: localizedLabel(PRACTICAL_LABELS, key, locale, key),
        value,
      }))
      .filter((item) => item.value);
  }

  function normalizeAddressForChecks(value) {
    return normalizeText(value)
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function usableMapAddress(value) {
    const address = normalizeText(value);
    if (!address || address.length < 8) return '';

    const normalized = normalizeAddressForChecks(address);
    if (!/[a-z]/i.test(normalized) || !/\d/.test(normalized)) return '';
    if (/^(?:a confirmer|adresse a confirmer|non renseigne(?:e)?|unknown|n\/a|sans adresse|-)$/.test(normalized)) return '';

    return address;
  }

  function appendDistinctLocationPart(parts, value) {
    const text = normalizeText(value);
    if (!text) return;

    const normalizedText = normalizeAddressForChecks(text);
    const alreadyPresent = parts.some((part) => normalizeAddressForChecks(part).includes(normalizedText));
    if (!alreadyPresent) {
      parts.push(text);
    }
  }

  function getArticleMapLink(article, locale = DEFAULT_LOCALE) {
    const addressItem = getArticlePracticalItems(article, locale).find((item) => item.key === 'address');
    const address = usableMapAddress(addressItem && addressItem.value);
    if (!address) return null;

    const articleTaxonomy = getArticleTaxonomy(article, locale);
    const queryParts = [address];
    appendDistinctLocationPart(queryParts, articleTaxonomy.city);
    appendDistinctLocationPart(queryParts, articleTaxonomy.country);
    const query = queryParts.join(', ');

    return {
      address,
      href: `https://www.google.com/maps/search/${encodeURIComponent(query)}`,
      embedHref: `https://www.google.com/maps?q=${encodeURIComponent(query)}&output=embed`,
    };
  }

  function getArticleAround(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    const relation = isPlainObject(article && article.relations) && isPlainObject(article.relations.around)
      ? article.relations.around
      : {};
    const legacy = isPlainObject(article && article.around) ? article.around : null;
    const contentAround = isPlainObject(content.around) ? content.around : {};
    const relationKey = normalizeText(relation.relation_key);
    const articleSlug = normalizeText(relation.article_id || relation.article_slug || (legacy && legacy.article_slug));

    if (!legacy && !relationKey && !articleSlug) return null;

    return {
      relationKey,
      relationLabel: relationKey
        ? localizedLabel(RELATION_LABELS, relationKey, locale, relationKey)
        : normalizeText(legacy && legacy.relation_label),
      articleSlug,
      articleTitle: normalizeText(legacy && legacy.article_title),
      note: normalizeText(contentAround.note) || normalizeText(legacy && legacy.note),
    };
  }

  function getArticleResources(article, locale = DEFAULT_LOCALE) {
    const content = getArticleContent(article, locale);
    const resources = Array.isArray(content.resources) ? content.resources : article && article.resources;

    return (Array.isArray(resources) ? resources : [])
      .filter((item) => isPlainObject(item) && normalizeText(item.href))
      .map((item) => ({
        href: normalizeText(item.href),
        title: localizedValue(item.title, locale),
        kind: localizedValue(item.kind, locale),
        note: localizedValue(item.note, locale),
      }))
      .filter((item) => item.title);
  }

  function getArticleGaps(article) {
    const editorial = isPlainObject(article && article.editorial) ? article.editorial : {};
    const gaps = Array.isArray(editorial.gaps) ? editorial.gaps : article && article.gaps;
    return (Array.isArray(gaps) ? gaps : []).map(normalizeText).filter(Boolean);
  }

  global.ArticleAccess = {
    getArticleAround,
    getArticleContent,
    getArticleDek,
    getArticleEpigraph,
    getArticleFormat,
    getArticleGaps,
    getArticleMapLink,
    getArticleHeroAlt,
    getArticleMedia,
    getArticleMetaDescription,
    getArticlePracticalItems,
    getArticlePublicationOrder,
    getArticleResources,
    getArticleSections,
    getArticleTaxonomy,
    getArticleTitle,
    isArticleLocaleReady,
    localizedValue,
    normalizeLocale,
    normalizeText,
  };
})(window);
