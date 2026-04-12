# AGENTS.md

## Project identity

This repository is a lean static editorial site about Art Nouveau and Art Deco in Europe.

Core principles:
- vanilla HTML / CSS / JS
- deterministic static build
- `dist/` is the only publishable artifact
- no framework migration unless explicitly requested
- changes must stay readable, conservative, and reversible

The project is both:
- a real website for publication
- a learning project
- a future automation / portfolio project

Priority order:
1. preserve project clarity
2. preserve runtime stability
3. improve structure progressively
4. only then automate

---

## Source of truth

Runtime public content:
- `src/data/articles.json`

Internal non-published material:
- `research/`

Build / validation logic:
- `scripts/`

Published artifact:
- `dist/`

Never move research-only notes, prompts, workflow notes, or internal metadata into the public runtime payload unless explicitly requested.

---

## Current article model status

The repository currently supports a mixed article model:
- legacy article format: v1
- new progressive bilingual-ready format: v2

At this stage:
- some articles remain in v1
- a limited number of pilot articles are in v2
- the runtime must continue to support mixed v1/v2 safely

Do not migrate all articles at once unless explicitly asked.

---

## Migration philosophy

Use progressive migration only.

Required approach:
- add compatibility layers first
- keep fallback behavior stable
- migrate one small controlled batch at a time
- validate after each batch
- prefer small diffs over large rewrites

Avoid:
- mass refactors
- schema rewrites across the whole dataset in one pass
- aesthetic rewrites mixed with data-model work
- introducing multiple new concepts in one task

---

## v2 article model principles

All stable technical keys must be in English.

Visible reader-facing content must live under:
- `content.fr`
- `content.en`

Stable non-localized data must stay outside `content`, typically in blocks such as:
- `identity`
- `taxonomy`
- `facts`
- `media`
- `sources`
- `relations`
- `resources`
- `editorial`
- `publication`

Important rules:
- `slug` remains unique
- `id` exists as a stable identifier, even if initially equal to `slug`
- `content.en` may be empty during transition
- French fallback remains acceptable until true EN support is implemented
- do not duplicate truth unnecessarily across multiple blocks

Examples of intended separation:
- labels for UI or taxonomy should not be stored as source truth in every article
- technical keys like `style_key`, `tag_keys`, `relation_key` are preferred over display labels
- `relation_label` should be derived, not treated as primary stored truth
- avoid duplicating style text in `facts` if `taxonomy.style_key` already expresses it

---

## Practical items rule

Practical display data must use stable keys, not display labels as the main model.

Preferred shape:
- `practical_items[].key`
- `practical_items[].value`

Example keys:
- `city`
- `country`
- `style`
- `architect`
- `address`
- `date`
- `access`

Do not use language-specific labels like `Ville`, `Pays`, `Accès` as source keys.

---

## Bilingual rule

Do not bolt English on top of French ad hoc.

When touching article structure, always think:
- what is stable and language-independent?
- what is visible and must be localized?

Localized text belongs in `content.fr` / `content.en`.

Examples of localized fields:
- title
- dek
- epigraph
- sections
- SEO text
- alt text
- around notes
- visible resource labels / notes

Examples of non-localized fields:
- ids
- slugs
- technical taxonomies
- source URLs
- media paths
- editorial flags
- publication metadata

When EN is missing:
- preserve FR rendering
- do not fake full bilingual support
- do not invent translations silently

---

## Runtime access rule

Rendering code should avoid direct access to legacy flat article fields when a compatibility helper exists.

Prefer the compatibility layer, especially through:
- `article-access.js`
- media helpers
- taxonomy helpers

When updating rendering logic:
- use helper functions first
- keep v1/v2 coexistence intact
- do not break current FR output

---

## Validation discipline

Before considering a task complete, run the relevant checks.

Minimum expected checks for content/model work:
- `npm run validate`
- `npm run build`

If a task changes rendering behavior significantly, also check local preview if available.

Never claim a task is complete if validation was not run, unless you explicitly state what could not be executed.

---

## Scope control

Do only what was asked.

Do not mix these scopes unless explicitly requested:
- article data model migration
- visual redesign
- SEO overhaul
- static page localization
- automation / n8n
- Python internal tooling
- publication workflow redesign

If a task reveals adjacent technical debt:
- mention it briefly
- do not fix it opportunistically unless it blocks the requested task

---

## Changes that require extra caution

Be conservative when touching:
- `src/data/articles.json`
- `scripts/validate-content.mjs`
- `scripts/build.mjs`
- `src/assets/scripts/gallery.js`
- `src/assets/scripts/article-template.js`

For these files:
- prefer minimal diffs
- explain the impact clearly
- preserve backward compatibility where expected

---

## CSS / design guardrail

Do not change site styling during data-model or compatibility tasks unless:
- the user explicitly asks for a visual change
- or a tiny style fix is required to keep rendering correct

If a CSS file changes incidentally during a non-visual task, verify whether the diff is necessary.
If not necessary, revert it.

---

## Documentation rule

When a structural change becomes important enough to affect future tasks, update documentation.

Preferred places:
- `research/` for internal design notes
- a dedicated technical markdown file for model contracts or migration notes

Document especially:
- schema changes
- migration rules
- fallback rules
- out-of-scope decisions

---

## Output format expected from the coding agent

When completing a meaningful task, report:
1. exact files modified
2. short summary of what changed
3. validation commands run and results
4. what was intentionally not done

For migration tasks, also report:
- whether the change affects v1, v2, or both
- which articles were migrated, if any
- whether fallback FR behavior was preserved

---

## Learning-first rule

This project is also used for learning.

Therefore:
- prefer explicit and understandable code over clever abstraction
- prefer progressive migration over perfect architecture
- prefer maintainable structure over maximum automation
- do not introduce complexity just because it is technically possible

The goal is not only to make the site work.
The goal is to build a project that remains understandable, teachable, and reusable for future Python tooling and automation.
