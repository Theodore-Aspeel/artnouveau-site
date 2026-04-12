# Article Model v2

This project currently accepts a progressive mix of article entries:

- v1: the original flat article shape used by the first runtime.
- v2: the bilingual-ready article shape introduced progressively.

Only a few articles should be migrated at a time. The runtime compatibility layer lives in `src/assets/scripts/article-access.js` and must remain the main read API for gallery and article rendering.

## Runtime Rule

Rendering code should not read reader-facing article fields directly from the flat v1 shape. It should use `ArticleAccess` helpers such as:

- `getArticleTitle(article, locale)`
- `getArticleDek(article, locale)`
- `getArticleSections(article, locale)`
- `getArticleMedia(article, locale)`
- `getArticleTaxonomy(article, locale)`
- `getArticlePracticalItems(article, locale)`
- `getArticleAround(article, locale)`

The helpers read v2 first, then fall back to v1. This keeps the site working while `articles.json` contains both shapes.

## v2 Blocks

`id` and `slug` are stable identifiers for the article. During the progressive phase, `id` must match `slug`.

`publication` contains publication metadata such as ordering and publication dates.

`identity` contains stable identity fields for the subject, such as type, canonical name, and exact name.

`taxonomy` contains stable technical keys, not displayed labels. Examples: `style_key`, `tag_keys`, `place_keys`.

`facts` contains verified or structured factual data, such as location, dates, people, and notes. Do not duplicate style here when `taxonomy.style_key` is sufficient.

`media` contains stable image references and non-localized credits. Reader-facing alt text belongs in `content.<locale>.media`.

`sources` contains source-backed material such as verified quotes and URLs.

`relations` contains stable relation data, such as `relation_key` and target article id. Localized relation labels are derived by taxonomy/UI code, not stored in content.

`editorial` contains internal editorial metadata, gaps, flags, method notes, and author information.

`content.fr` and `content.en` contain reader-facing localized content.

## Localized Content

All reader-visible editorial strings should be able to live under `content.fr` and `content.en`:

- title
- dek
- epigraph
- sections
- SEO description
- image alt text
- practical item values intended for display
- localized resource titles, kinds, and notes
- around notes

`content.en` may be empty during this phase. The access layer falls back to French when the requested locale is missing or incomplete.

## Practical Items

Practical items must use stable keys, not displayed labels:

```json
{
  "key": "city",
  "value": "Lille"
}
```

Labels such as `Ville` or `City` are derived by the UI/access layer.

## Out Of Scope For This Phase

- Migrating every article.
- Creating separate FR/EN routes.
- Localizing static pages.
- Splitting `articles.json` into multiple files.
- Reworking visual design.
- Building the future Python migration tool.

