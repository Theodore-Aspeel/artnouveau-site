---
name: article-v2-migration
description: Migrate one article or a very small batch of editorial articles from legacy v1 format to progressive v2 bilingual-ready format in this repository. Use for conservative, helper-compatible, low-risk article model migration.
---

# article-v2-migration

## Use this skill when

Use this skill when the task is to migrate one article or a very small batch from v1 to v2 without breaking mixed-mode runtime behavior.

Typical trigger phrases:
- migrate this article to v2
- convert one article to the new bilingual-ready schema
- prepare another pilot article in v2
- migrate a short-format article to v2
- update article data model conservatively

## Repository-specific rules

- Do not migrate all articles at once.
- Keep runtime compatibility with mixed v1/v2.
- Preserve FR output.
- `content.en` may remain empty or partial.
- Keep reader-visible content under `content.fr` / `content.en`.
- Keep stable technical keys outside localized content.
- Use helper-based runtime access where possible.
- Do not mix this task with visual redesign.

## Expected process

1. Inspect the target article in current JSON.
2. Map current fields to v2 blocks conservatively.
3. Preserve meaning and current FR rendering.
4. Update only the required article(s).
5. Run:
   - npm run validate
   - npm run build
6. Report:
   - files modified
   - migrated article ids/slugs
   - validation results
   - what was intentionally not done

## Expected v2 blocks

Typical blocks:
- id
- slug
- status
- format
- publication
- identity
- taxonomy
- facts
- media
- sources
- relations
- resources
- editorial
- content.fr
- content.en

## Out of scope

- global migration of all articles
- route-level FR/EN implementation
- static page localization
- styling changes
- automation / n8n work
