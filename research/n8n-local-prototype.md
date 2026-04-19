# Local n8n Prototype

This is the first pedagogical n8n shape for the social-package handoff.

It is a local learning prototype, not an automation deployment. It shows how a future workflow can consume the existing `social-package` JSON contract, validate the consumer boundary, branch on candidate readiness, and prepare a compact review object for a human.

The repository remains a static editorial site. n8n is only a possible outside consumer of a read-only JSON payload.

## Prototype Goal

The first local workflow should answer four questions:

1. Can n8n obtain the same JSON payload a developer can obtain from the CLI?
2. Does the payload match the expected handoff contract?
3. Is the selected article a `candidate`, or should the workflow stop for review?
4. What small object would a human review before any future publishing step?

It should not publish, schedule, call an external service, store credentials, or write state back to the article dataset.

## Source Input

The source input is the existing Editorial Manager command:

```bash
python -m tools.editorial_manager social-package --next --locale en
```

Run it from the repository root. The command prints a single JSON payload to stdout.

For local experiments without selecting live project data, use the example fixture:

```bash
python -m tools.editorial_manager validate-social-package research/social-package-example.json
```

The fixture is useful for understanding the shape. The real prototype should still treat the CLI output as the source handoff.

## Importable Example

The repository includes an importable example workflow:

```text
research/n8n-social-package-review-workflow.json
```

Suggested local use:

1. Start n8n locally outside this repository.
2. Import `research/n8n-social-package-review-workflow.json`.
3. Open the `Run social-package CLI` node.
4. Make sure the command runs from the repository root. If your local n8n process starts elsewhere, replace the command with an absolute `cd` into the repo followed by the same Python command.
5. Execute the workflow manually.
6. Inspect the `Build local review object` output.

The workflow intentionally uses a Manual Trigger. There is no scheduler.

## Workflow Shape

### 1. Manual Trigger

Starts the prototype by hand.

Learning point: publication workflows should be explicit until the contract and review process are trusted.

### 2. Run social-package CLI

Executes:

```bash
python -m tools.editorial_manager social-package --next --locale en
```

Expected output: JSON on stdout.

Learning point: n8n consumes the same read-only handoff a developer can inspect locally.

### 3. Parse CLI JSON

Parses stdout as JSON. If stdout is not valid JSON, the workflow fails clearly.

Learning point: the automation boundary is structured data, not screen scraping.

### 4. Validate social-package contract

Checks the small consumer-facing contract:

- `contract.name` is `artnouveau.social_package`
- `contract.version` is `1`
- `contract.kind` is `read_only_social_handoff`
- `slug` is present
- `queue_status` is present
- `caption`, `media`, and `links` are objects

Learning point: n8n should validate the boundary before reading business fields.

### 5. Candidate Gate

Continues only when:

```text
queue_status == candidate
```

Anything else is routed to the local review branch.

Learning point: `needs-review` and `blocked` are valid payload states, but they are not publication candidates.

### 6. Build Local Review Object

Projects the full payload into a small review object:

```json
{
  "prototype": "local_n8n_social_review",
  "contract": "artnouveau.social_package@1",
  "status": "candidate",
  "slug": "demo",
  "requested_locale": "en",
  "source_locale": "en",
  "title": "Demo House",
  "caption": "Dek EN.",
  "cta": "Read the article on the site.",
  "hashtags": ["#ArtNouveau", "#Lille", "#Architecture", "#Patrimoine"],
  "hero": {
    "src": "assets/images/demo.png",
    "alt": "Alt EN.",
    "caption": "Caption EN."
  },
  "public_paths": {
    "fr": "/fr/articles/demo/",
    "en": "/en/articles/demo/"
  },
  "preview_paths": {
    "fr": "article.html?slug=demo",
    "en": "article.html?slug=demo&previewLocale=en",
    "nl": "article.html?slug=demo&previewLocale=nl"
  },
  "reasons": [
    "Publication checklist is ready.",
    "English content is ready.",
    "Hero image is present."
  ]
}
```

Learning point: n8n can prepare a human-readable review packet without becoming the source of truth.

### 7. Local Review Branch

For `needs-review` or `blocked`, the workflow builds a review object with:

- `status`
- `slug`
- `readiness`
- `locale_status`
- `reasons`
- `preview_paths`

Learning point: the workflow can stop safely while still giving the operator enough context to inspect the article locally.

## Field Mapping

| social-package field | n8n use |
| --- | --- |
| `contract.name` | Compatibility check |
| `contract.version` | Compatibility check |
| `contract.kind` | Confirms read-only handoff |
| `slug` | Human review identifier |
| `requested_locale` | Shows what the workflow asked for |
| `source_locale` | Shows whether fallback text was used |
| `queue_status` | Candidate gate |
| `caption.title` | Review title |
| `caption.caption` | Draft social text |
| `caption.cta` | Draft call to action |
| `caption.hashtags` | Draft hashtags |
| `media.hero` | Hero image review |
| `links.public_paths` | Future public URL candidates |
| `links.preview_paths` | Local editorial review links |
| `readiness` | Stop reason context |
| `reasons` | Human explanation |

## Deliberate Limits

This prototype does not:

- call Instagram or any external API
- store credentials
- create an n8n deployment setup
- add Docker, environment files, queues, or workers
- run on a schedule
- publish posts
- upload media
- write publication state back to `src/data/articles.json`
- edit `dist/`
- generate captions with AI

Those limits keep the handoff replaceable. A later automation tool can consume the same JSON contract without changing article data, rendering code, or static build behavior.

