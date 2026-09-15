# ANAD 2.0 - Corpus Inventory

Date: 2026-09-15  
Branch: `anad-2.0/recovery`  
Scope: `src/data/articles.json`

## Measured baseline

| Measure | Result |
| --- | ---: |
| Total articles | 14 |
| v1 articles | 0 |
| v2 articles | 14 |
| Draft status | 14 |
| English ready | 14 |
| English partial | 0 |
| Dutch ready | 14 |
| Dutch partial or missing | 0 |
| Publication-check errors | 0 |
| Publication-check warnings | 14 |

All 14 publication warnings have the same cause: the article is still marked as
`draft`. The checklist otherwise reports 109 passing items and no errors.

## Interpretation

- The corpus migration itself is complete: the public dataset no longer contains
  a v1 article.
- The v1 compatibility layer should remain until regression coverage and the
  import/history strategy justify its removal.
- FR, EN and NL content are structurally complete according to the current locale
  checker. This is a structural result, not proof that every translation has
  received final human editorial approval.
- Publication status is the remaining corpus-wide readiness blocker. Statuses
  must not be changed in bulk during Recovery; each article needs an explicit
  editorial and factual approval gate.
- NL is editorially ready in the dataset but is not automatically assumed to be
  a public locale. Runtime publication policy remains a separate decision.

## Reproduction commands

```bash
python -m tools.editorial_manager summary
python -m tools.editorial_manager locale-report --locale en
python -m tools.editorial_manager locale-report --locale nl
python -m tools.editorial_manager publication-check
```

## Next controlled use

Select one representative article for the first end-to-end pilot. Verify its
research provenance and rights, complete human editorial review, then exercise
preview, publication approval, build/deploy and social-package generation without
changing the other 13 draft statuses.
