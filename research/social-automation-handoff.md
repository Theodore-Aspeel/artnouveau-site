# Social Automation Handoff

This note defines the first minimal foundation for future n8n / Instagram work.

The project remains a static editorial site. Automation starts outside the runtime site and outside `dist/`. The current boundary is a read-only JSON handoff produced by the local Editorial Manager:

```bash
python -m tools.editorial_manager social-package --next --locale en
python -m tools.editorial_manager social-package <slug> --locale fr
```

For learning and validation, the repository also contains a machine-readable example:

```bash
python -m tools.editorial_manager validate-social-package research/social-package-example.json
```

## Current Contract

The stable payload is `artnouveau.social_package` version `1`.

It is intentionally a handoff contract, not a publishing workflow. The payload includes:

- the selected article slug
- requested and source locales
- queue status and review reasons
- readiness and locale status
- deterministic caption draft
- hero and support image paths with localized/fallback text
- local preview links for editorial review
- public article paths for automation consumers

The `contract` block is the automation compatibility marker:

```json
{
  "name": "artnouveau.social_package",
  "version": 1,
  "kind": "read_only_social_handoff"
}
```

## n8n Use Later

A first local n8n prototype should treat the CLI output as its only input payload:

1. Run `python -m tools.editorial_manager social-package --next --locale en`.
2. Parse stdout as JSON.
3. Continue only when `contract.name` and `contract.version` match.
4. Require `queue_status: "candidate"` before preparing any public action.
5. Use `links.public_paths` for public article URLs.
6. Use `media` and `caption` as a draft package for human review or a later publishing step.

This keeps n8n replaceable. Another automation tool can consume the same JSON without changing article data or site rendering.

## First Local n8n Prototype

The first prototype is a learning workflow, not a publishing workflow. It should be possible to run it on a local machine, inspect each node, and delete it without changing the website.

Concrete local prototype artifacts:

- `research/n8n-local-prototype.md`: step-by-step pedagogical workflow spec.
- `research/n8n-social-package-review-workflow.json`: importable example workflow for local experimentation.

Recommended workflow shape:

1. Manual Trigger.
2. Execute Command node:
   - command: `python -m tools.editorial_manager social-package --next --locale en`
   - working directory: repository root
3. Code or JSON Parse node:
   - parse the command stdout as JSON
   - fail clearly if stdout is not JSON
4. IF node:
   - require `contract.name == "artnouveau.social_package"`
   - require `contract.version == 1`
5. IF node:
   - continue only when `queue_status == "candidate"`
   - send `needs-review` and `blocked` payloads to a local review branch
6. Set node:
   - keep a small review object with `slug`, `caption.caption`, `caption.hashtags`, `media.hero.src`, and `links.public_paths`
7. Final local output:
   - display the review object in the execution log, or write it to a temporary local file outside `src/` and `dist/`

The workflow should deliberately avoid credentials and external services. The useful learning goal is understanding how n8n consumes a CLI JSON contract, validates compatibility, branches on business rules, and prepares a human-readable handoff.

## Consumer Contract

The consumer should rely on the top-level contract and a small set of stable fields:

- `contract.name`: must be `artnouveau.social_package`
- `contract.version`: must be `1`
- `contract.kind`: must be `read_only_social_handoff`
- `slug`: stable article slug
- `requested_locale`: locale requested from the CLI
- `source_locale`: locale actually used for visible caption/media text
- `queue_status`: `candidate`, `needs-review`, or `blocked`
- `caption`: deterministic draft text and hashtags
- `media`: hero/support image paths and text
- `links.public_paths`: public multilingual article paths
- `readiness` and `reasons`: human explanation for review

The consumer should not rely on private source structure in `src/data/articles.json`, generated files in `dist/`, internal research notes, or the current visual JavaScript rendering details.

## Local Validation Helper

Use the validation helper when testing exported payloads or n8n fixtures:

```bash
python -m tools.editorial_manager validate-social-package research/social-package-example.json
```

The helper checks the handoff boundary: contract marker, required top-level blocks, queue/readiness values, media/link shapes, and basic type expectations. It intentionally does not replace the article validator, validate every nested editorial field, or decide whether an article should be published.

## Deliberate Limits

This foundation does not:

- call the Instagram API
- store credentials or tokens
- schedule or publish posts
- write publication state back to `src/data/articles.json`
- generate captions with AI
- rewrite article content
- edit `dist/`

Those choices keep the static-site architecture simple and avoid turning early automation into hidden workflow state.
