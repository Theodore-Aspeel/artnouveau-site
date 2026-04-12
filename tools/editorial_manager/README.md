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
```

## Commands

- `summary`: prints global article counts, model counts, publication statuses, and v2 entries without English content.
- `list`: lists articles in publication order with model, status, slug, title, city, and style.
- `show <slug>`: prints a compact article card for one article.
- `check`: runs simple read-only checks across all articles.
- `check <slug>`: runs the same checks for one article.
- `publication-check`: runs a publication preparation checklist across all articles.
- `publication-check <slug>`: runs the publication checklist for one article.

`check` and `publication-check` return a non-zero exit code when they find errors.

## Deliberate Limits

Editorial Manager V1 is intentionally read-only. It does not migrate articles, rewrite `src/data/articles.json`, generate translations, edit images, build the website, or replace the Node validation/build pipeline.

It is a repo-local editorial helper, not a publishing workflow manager.

## Tests

Run the Python tests from the repository root:

```bash
python -m unittest discover tests
```
