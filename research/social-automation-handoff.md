# Social Automation Handoff

This note defines the first minimal foundation for future n8n / Instagram work.

The project remains a static editorial site. Automation starts outside the runtime site and outside `dist/`. The current boundary is a read-only JSON handoff produced by the local Editorial Manager:

```bash
python -m tools.editorial_manager social-package --next --locale en
python -m tools.editorial_manager social-package <slug> --locale fr
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

A future n8n workflow can treat the CLI output as its input payload:

1. Run `python -m tools.editorial_manager social-package --next --locale en`.
2. Parse stdout as JSON.
3. Continue only when `contract.name` and `contract.version` match.
4. Require `queue_status: "candidate"` before preparing any public action.
5. Use `links.public_paths` for public article URLs.
6. Use `media` and `caption` as a draft package for human review or a later publishing step.

This keeps n8n replaceable. Another automation tool can consume the same JSON without changing article data or site rendering.

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
