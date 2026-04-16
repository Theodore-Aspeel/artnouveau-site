# Editorial Manager

Editorial Manager is a small internal Python CLI for inspecting the article dataset and running read-only editorial checks.

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
python -m tools.editorial_manager check
python -m tools.editorial_manager check <slug>
python -m tools.editorial_manager publication-check
python -m tools.editorial_manager publication-check <slug>
python -m tools.editorial_manager locale-report
python -m tools.editorial_manager locale-report <slug>
python -m tools.editorial_manager social-brief <slug>
python -m tools.editorial_manager social-brief <slug> --json
python -m tools.editorial_manager social-queue
python -m tools.editorial_manager social-queue --json
python -m tools.editorial_manager social-queue --status candidate --locale-status en-ready --has-hero yes --limit 5
python -m tools.editorial_manager social-next
python -m tools.editorial_manager social-next --json
python -m tools.editorial_manager social-next --status needs-review --locale-status fr-only
```

## Commands

- `summary`: prints global article counts, model counts, publication statuses, and v2 entries without English content.
- `list`: lists articles in publication order with model, status, slug, title, city, and style.
- `show <slug>`: prints a compact article card for one article.
- `check`: runs simple read-only checks across all articles.
- `check <slug>`: runs the same checks for one article.
- `publication-check`: runs a publication preparation checklist across all articles.
- `publication-check <slug>`: runs the publication checklist for one article.
- `locale-report`: shows the read-only FR/EN editorial status for all articles.
- `locale-report <slug>`: shows the same locale status for one article.
- `social-brief <slug>`: prepares a simple read-only publication brief for one article, with FR/EN titles and dek, locale status, quote, practical items, image presence, and a readiness summary.
- `social-brief <slug> --json`: prints the same brief as a structured JSON payload for future automation workflows.
- `social-queue`: shows a batch queue of articles for future social publication planning, with FR/EN titles, locale status, publication readiness, hero image presence, and a simple queue status.
- `social-queue --json`: prints the same queue as a structured JSON payload for future automation workflows.
- `social-queue` filters: accepts `--status candidate|needs-review|blocked`, `--locale-status en-ready|en-partial|fr-only`, `--has-hero yes|no`, and `--limit N`.
- `social-next`: shows the first matching social publication candidate in publication order. It defaults to `--status candidate`.
- `social-next --json`: prints the same next item as a small structured JSON payload for future automation workflows.
- `social-next` filters: accepts `--status candidate|needs-review|blocked`, `--locale-status en-ready|en-partial|fr-only`, and `--has-hero yes|no`.

`check` and `publication-check` return a non-zero exit code when they find errors.

`locale-report` uses a deliberately simple status rule:

- `fr-only`: no real English text is present under `content.en`.
- `en-partial`: some English text exists, but one or more main fields are missing.
- `en-ready`: English title, dek, meta description, hero alt text, and section heading/body coverage are present.

`social-queue` uses a deliberately small status rule:

- `blocked`: the publication checklist has one or more errors, or the article has no hero image.
- `needs-review`: there are no blocking errors, but the publication checklist has warnings or the locale status is not `en-ready`.
- `candidate`: the publication checklist has no errors or warnings, the locale status is `en-ready`, and a hero image is present.

When multiple `social-queue` filters are used together, they are combined as AND filters. `--limit` is applied after filtering and keeps the existing publication order.

`social-next` reuses the same queue status and filter rules as `social-queue`, then returns only the first matching item. By default, it selects the first `candidate` article in publication order.

## Deliberate Limits

Editorial Manager V1 is intentionally read-only. It does not migrate articles, rewrite `src/data/articles.json`, generate translations, edit images, build the website, or replace the Node validation/build pipeline.

It is a repo-local editorial helper, not a publishing workflow manager.

## Tests

Run the Python tests from the repository root:

```bash
python -m unittest discover tests
```
