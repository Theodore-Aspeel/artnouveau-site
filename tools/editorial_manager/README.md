# Editorial Manager

Editorial Manager is a small internal Python CLI for inspecting the article dataset, running read-only editorial checks, and performing a few guarded local edits.

It lives in `tools/editorial_manager/` and reads the public runtime payload from `src/data/articles.json`. It supports the current mixed article model: legacy v1 articles and progressive v2 articles.

## Run

From the repository root:

```bash
python -m tools.editorial_manager <command>
```

Available commands:

```bash
python -m tools.editorial_manager summary
python -m tools.editorial_manager list
python -m tools.editorial_manager show <slug>
python -m tools.editorial_manager create-article --slug <slug> --title-fr "..." --dek-fr "..." --epigraph-fr "..." --meta-description-fr "..." --hero-alt-fr "..." --section-heading-fr "..." --section-body-fr "..." --hero-src assets/images/articles/example.png --city "..." --country "..." --style-key art_nouveau
python -m tools.editorial_manager check
python -m tools.editorial_manager check <slug>
python -m tools.editorial_manager publication-check
python -m tools.editorial_manager publication-check <slug>
python -m tools.editorial_manager locale-report
python -m tools.editorial_manager locale-report <slug>
python -m tools.editorial_manager locale-report --locale nl
python -m tools.editorial_manager social-brief <slug>
python -m tools.editorial_manager social-brief <slug> --json
python -m tools.editorial_manager social-caption <slug>
python -m tools.editorial_manager social-caption <slug> --locale en --json
python -m tools.editorial_manager social-package <slug>
python -m tools.editorial_manager social-package <slug> --locale en
python -m tools.editorial_manager social-package --next
python -m tools.editorial_manager social-package --next --status needs-review --locale-status fr-only --has-hero yes
python -m tools.editorial_manager social-queue
python -m tools.editorial_manager social-queue --json
python -m tools.editorial_manager social-queue --status candidate --locale-status en-ready --has-hero yes --limit 5
python -m tools.editorial_manager social-next
python -m tools.editorial_manager social-next --json
python -m tools.editorial_manager social-next --status needs-review --locale-status fr-only
python -m tools.editorial_manager social-workflow
python -m tools.editorial_manager social-workflow --locale en --status needs-review --locale-status fr-only
```

## Commands

- `summary`: prints global article counts, model counts, publication statuses, and v2 entries without English content.
- `list`: lists articles in publication order with model, status, slug, title, city, and style.
- `show <slug>`: prints a compact article card for one article.
- `create-article`: prepares one new v2 draft article from explicit French source fields. By default it is a dry run and prints the JSON article. Add `--write` to append it to `src/data/articles.json`; the command then runs project validation and rolls back if validation fails.
- `check`: runs simple read-only checks across all articles.
- `check <slug>`: runs the same checks for one article.
- `publication-check`: runs a publication preparation checklist across all articles.
- `publication-check <slug>`: runs the publication checklist for one article.
- `locale-report`: shows the read-only source/target locale editorial status for all articles. It defaults to English.
- `locale-report <slug>`: shows the same locale status for one article.
- `locale-report --locale nl`: shows internal Dutch readiness for all articles without making NL public.
- `social-brief <slug>`: prepares a simple read-only publication brief for one article, with FR/EN titles and dek, locale status, quote, practical items, image presence, and a readiness summary.
- `social-brief <slug> --json`: prints the same brief as a structured JSON payload for future automation workflows.
- `social-caption <slug>`: prepares a simple read-only social caption proposal for one article, with title, hook, short caption, CTA, hashtags, and locale status.
- `social-caption <slug> --locale fr|en --json`: prints the same caption proposal as a small structured JSON payload. When English is requested but unavailable, the proposal explicitly reports `source_locale: fr` instead of inventing a translation.
- `social-package <slug> --locale fr|en`: prints one JSON payload for later social automation, combining the existing brief, caption, media block, image summary, readiness, queue status, and reasons. It is read-only and always outputs JSON.
- `social-package --next --locale fr|en`: selects the first matching article through the same queue logic as `social-next`, then prints the same package payload as the slug mode.
- `social-package --next` filters: accepts `--status candidate|needs-review|blocked`, `--locale-status en-ready|en-partial|fr-only`, and `--has-hero yes|no`. These filters apply only to automatic selection. `--status` defaults to `candidate`.
- `social-queue`: shows a batch queue of articles for future social publication planning, with FR/EN titles, locale status, publication readiness, hero image presence, and a simple queue status.
- `social-queue --json`: prints the same queue as a structured JSON payload for future automation workflows.
- `social-queue` filters: accepts `--status candidate|needs-review|blocked`, `--locale-status en-ready|en-partial|fr-only`, `--has-hero yes|no`, and `--limit N`.
- `social-next`: shows the first matching social publication candidate in publication order. It defaults to `--status candidate`.
- `social-next --json`: prints the same next item as a small structured JSON payload for future automation workflows.
- `social-next` filters: accepts `--status candidate|needs-review|blocked`, `--locale-status en-ready|en-partial|fr-only`, and `--has-hero yes|no`.
- `social-workflow`: prepares a small local handoff for the first matching social publication candidate. It reuses `social-next` selection and `social-package` payload building, then prints the selected article, caption draft, media paths, article links, reasons, and follow-up local commands.
- `social-workflow` filters: accepts `--status candidate|needs-review|blocked`, `--locale-status en-ready|en-partial|fr-only`, and `--has-hero yes|no`. It also accepts `--locale fr|en` for the caption/package locale.

`check` and `publication-check` return a non-zero exit code when they find errors.

## Creating One New Article

Article creation is intentionally small and explicit. It is not a CMS and it does not generate editorial text, translate content, upload images, or publish the site.

The first creation command writes only a v2 draft article. It requires the minimum French source content that the public runtime schema already validates:

- stable identity: `--slug`
- French visible content: `--title-fr`, `--dek-fr`, `--epigraph-fr`, `--meta-description-fr`, `--hero-alt-fr`
- first French section: `--section-heading-fr`, `--section-body-fr`
- existing image: `--hero-src`, pointing to a file already under `src/assets/images`
- basic facts/taxonomy: `--city`, `--country`, `--style-key`

Optional fields can be supplied immediately when known: `--tag-key`, `--canonical-name`, `--exact-name`, `--address`, `--architect`, `--date`, `--access`, `--author`, `--format`, and `--order`.

If `--order` is omitted, the next publication order is selected. The command scaffolds empty `content.en` and `content.nl` blocks with the same first section and practical item slots, so translation can be filled later through the existing editor without changing article shape. Empty EN/NL content is allowed at creation time; it will appear as `fr-only` / `nl-missing` in locale reports.

Recommended flow:

```bash
python -m tools.editorial_manager create-article --slug nouvel-article-demo --title-fr "Nouvel article demo" --dek-fr "Chapeau FR." --epigraph-fr "Epigraphe FR." --meta-description-fr "Description SEO FR." --hero-alt-fr "Texte alternatif FR." --section-heading-fr "Premier regard" --section-body-fr "Premier texte FR." --hero-src assets/images/articles/example.png --city "Lille" --country "France" --style-key art_nouveau
```

Review the printed JSON. When it is correct, rerun the same command with `--write`:

```bash
python -m tools.editorial_manager create-article --slug nouvel-article-demo --title-fr "Nouvel article demo" --dek-fr "Chapeau FR." --epigraph-fr "Epigraphe FR." --meta-description-fr "Description SEO FR." --hero-alt-fr "Texte alternatif FR." --section-heading-fr "Premier regard" --section-body-fr "Premier texte FR." --hero-src assets/images/articles/example.png --city "Lille" --country "France" --style-key art_nouveau --write
```

Guardrails:

- the slug must be lowercase letters/numbers/hyphens and unique
- the publication order must be unique
- the style and tag keys must be controlled keys
- the hero image must already exist under `src/assets/images`
- no placeholder article is written if required French source fields are empty
- after writing, `npm run validate` must pass or the JSON file is restored

`locale-report` uses a deliberately simple status rule:

- `fr-only`: no real English text is present under `content.en`.
- `en-partial`: some English text exists, but one or more main fields are missing.
- `en-ready`: English title, dek, meta description, hero alt text, and section heading/body coverage are present.
- `nl-missing`: no real Dutch text is present under `content.nl`.
- `nl-partial`: some Dutch text exists, but one or more main fields are missing.
- `nl-ready`: Dutch title, dek, meta description, hero alt text, and section heading/body coverage are present.

`social-queue` uses a deliberately small status rule:

- `blocked`: the publication checklist has one or more errors, or the article has no hero image.
- `needs-review`: there are no blocking errors, but the publication checklist has warnings or the locale status is not `en-ready`.
- `candidate`: the publication checklist has no errors or warnings, the locale status is `en-ready`, and a hero image is present.

When multiple `social-queue` filters are used together, they are combined as AND filters. `--limit` is applied after filtering and keeps the existing publication order.

`social-next` reuses the same queue status and filter rules as `social-queue`, then returns only the first matching item. By default, it selects the first `candidate` article in publication order.

`social-package --next` reuses `social-next` selection, then builds the usual package for the selected article. The JSON structure is the same as `social-package <slug>`.

`social-workflow` is intentionally a human-facing local entry point. It does not create files, update article data, call APIs, or publish anything. Use `social-package <slug> --locale <locale>` when the full JSON payload is needed.

## `social-package` JSON Contract

`social-package` is the stable read-only payload intended for future social/editorial automation. It combines existing helper outputs; it does not add private workflow state and does not modify `src/data/articles.json`.

Top-level structure:

- `slug`: stable article slug.
- `requested_locale`: locale requested by the caller, currently `fr` or `en`.
- `source_locale`: locale actually used for visible caption/media text. If English is requested but no English title or dek exists, this is `fr`.
- `locale_status`: brief locale readiness summary, with `status` and `missing_fields`.
- `queue_status`: social queue decision, one of `candidate`, `needs-review`, or `blocked`.
- `brief`: the full `social-brief` payload for the article.
- `caption`: the full `social-caption` payload for the selected source locale.
- `media`: hero and support images prepared for social use.
- `links`: relative article links for the published FR page and EN preview.
- `image_summary`: compact image presence summary copied from `brief`.
- `readiness`: publication checklist summary copied from `brief`.
- `reasons`: human-readable queue reasons explaining `queue_status`.

Optional or empty values are explicit rather than omitted:

- `brief.title_en`, `brief.dek_en`, quote fields, media `alt`, and media `caption` may be empty strings.
- `brief.quote` may be `null` when the article has no usable quote.
- `brief.locale_status.missing_fields`, `brief.practical_items`, `media.support`, `caption.hashtags`, `readiness.notes`, and `reasons` may be empty arrays.
- `media.hero.src` may be empty when no hero image exists; in that case `image_summary.has_hero` is `false` and `queue_status` is `blocked`.

Status fields have different roles:

- `readiness.status` comes from the publication checklist: `ready`, `needs review`, or `blocked`.
- `queue_status` is the social queue decision: `candidate` requires a ready checklist, `en-ready` locale status, and a hero image; `needs-review` means no blocker but warnings or incomplete English; `blocked` means checklist errors or a missing hero.
- `reasons` explains the queue decision. For candidates it records the positive checks; for review/blocking states it lists the relevant warnings, errors, missing English content, or missing hero image.

`media`, `links`, `brief`, and `caption` are deliberately separate:

- `media` contains image paths plus localized/fallback alt and caption text for the selected `source_locale`.
- `links` contains relative site paths only; it does not publish externally.
- `brief` is the editorial context block: FR/EN title and dek, locale status, quote, practical items, image summary, and checklist readiness.
- `caption` is a deterministic draft for social copy: title, hook, short caption, CTA, and hashtags.

Small example:

```json
{
  "slug": "demo",
  "requested_locale": "en",
  "source_locale": "en",
  "locale_status": {
    "status": "en-ready",
    "missing_fields": []
  },
  "queue_status": "candidate",
  "brief": {
    "slug": "demo",
    "locale_status": {
      "status": "en-ready",
      "missing_fields": []
    },
    "title_fr": "Maison Demo",
    "title_en": "Demo House",
    "dek_fr": "Dek FR.",
    "dek_en": "Dek EN.",
    "quote": null,
    "practical_items": [
      {
        "key": "city",
        "value": "Lille"
      },
      {
        "key": "style",
        "value": "Art Nouveau"
      }
    ],
    "image_summary": {
      "has_hero": true,
      "hero_src": "assets/images/demo.png",
      "support_count": 1
    },
    "readiness": {
      "status": "ready",
      "ok_count": 8,
      "error_count": 0,
      "warning_count": 0,
      "notes": []
    }
  },
  "caption": {
    "slug": "demo",
    "requested_locale": "en",
    "source_locale": "en",
    "locale_status": "en-ready",
    "title": "Demo House",
    "hook": "Look closer: Demo House",
    "caption": "Dek EN.",
    "cta": "Read the article on the site.",
    "hashtags": [
      "#ArtNouveau",
      "#Lille",
      "#Architecture",
      "#Patrimoine"
    ]
  },
  "media": {
    "hero": {
      "src": "assets/images/demo.png",
      "alt": "Alt EN.",
      "caption": "Caption EN."
    },
    "support": [
      {
        "src": "assets/images/support.png",
        "alt": "Support alt EN.",
        "caption": "Support caption EN."
      }
    ]
  },
  "links": {
    "article_fr_path": "article.html?slug=demo",
    "article_en_preview_path": "article.html?slug=demo&previewLocale=en"
  },
  "image_summary": {
    "has_hero": true,
    "hero_src": "assets/images/demo.png",
    "support_count": 1
  },
  "readiness": {
    "status": "ready",
    "ok_count": 8,
    "error_count": 0,
    "warning_count": 0,
    "notes": []
  },
  "reasons": [
    "Publication checklist is ready.",
    "English content is ready.",
    "Hero image is present."
  ]
}
```

`social-caption` uses deliberately simple deterministic rules:

- `--locale` defaults to `fr`.
- the hook is a short fixed prefix plus the selected title.
- the caption uses the selected dek when available, otherwise the title, and is capped to a short text.
- the CTA is a fixed locale-aware sentence.
- hashtags are derived from practical items or taxonomy values, then completed with broad editorial tags.
- if `--locale en` has no English title or dek, the output keeps `requested_locale: en` but uses `source_locale: fr` so the fallback is visible.

## Deliberate Limits

Editorial Manager V1 keeps the inspection commands read-only, and the local browser editor deliberately small. The editor can update only whitelisted article fields, including `media.hero.src` and existing `media.support[*].src` slots by selecting an existing image under `src/assets/images`. The `create-article` command can append one guarded v2 draft when called with `--write`, but it does not generate text, upload image files, edit image binaries, add, remove, or reorder support images, migrate existing articles, generate translations, build the website, or replace the Node validation/build pipeline.

It is a repo-local editorial helper, not a publishing workflow manager.

## Tests

Run the Python tests from the repository root:

```bash
python -m unittest discover tests
```
