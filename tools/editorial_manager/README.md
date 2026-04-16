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

`check` and `publication-check` return a non-zero exit code when they find errors.

`locale-report` uses a deliberately simple status rule:

- `fr-only`: no real English text is present under `content.en`.
- `en-partial`: some English text exists, but one or more main fields are missing.
- `en-ready`: English title, dek, meta description, hero alt text, and section heading/body coverage are present.

## Deliberate Limits

Editorial Manager V1 is intentionally read-only. It does not migrate articles, rewrite `src/data/articles.json`, generate translations, edit images, build the website, or replace the Node validation/build pipeline.

It is a repo-local editorial helper, not a publishing workflow manager.

## Tests

Run the Python tests from the repository root:

```bash
python -m unittest discover tests
```
