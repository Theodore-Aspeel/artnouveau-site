# ANAD 2.0 — Recovery State

Date: 2026-09-15
Current audit branch: `anad-2.0/audit-baseline`
Merged Recovery baseline: `main` at `afe9b1b8b013c4716e423c7ec24a851fcceb2516`

## Purpose

This document is the canonical technical recovery snapshot for ANAD 2.0. It records what already exists, what should be preserved, what is now outdated, and the order in which the project should be professionalized.

ANAD 2.0 is not a blank-slate rewrite. The current repository is a viable editorial platform with a substantial amount of reusable work. The goal is to retain the proven foundations while upgrading the operating model around them: ChatGPT Work as orchestration layer, Codex/GitHub for implementation, specialized agent skills, structured research and editorial handoffs, stronger CI/QA, SEO/AEO, social-video production, analytics, and controlled automation.

## Current baseline

The project is a deterministic static editorial website about Art Nouveau and Art Deco in Europe.

Current technical foundations:

- vanilla HTML/CSS/JS runtime
- deterministic build to `dist/`
- Node 20 build toolchain
- `npm run validate`, `npm run build`, `npm run preview`
- image pipeline based on Sharp
- generated multilingual public routes
- canonical and hreflang generation
- sitemap generation
- Open Graph image support
- optional Plausible injection at build time
- GitHub Pages deployment through GitHub Actions
- mixed v1/v2 article compatibility layer
- structured v2 article model with stable and localized blocks
- FR/EN public model plus NL editorial readiness support
- internal `research/` material excluded from publication
- Python Editorial Manager with guarded article creation, checks, locale reports, publication readiness, social queueing, social packages and an editor server
- initial n8n handoff contract and local review workflow
- repository-level agent instructions and one migration skill
- a non-trivial automated test corpus under `tests/`

The latest `main` deployment workflow is known to have succeeded. The baseline is therefore recoverable and should not be treated as a broken prototype.

## Existing product direction worth preserving

ANAD should remain a visually authored heritage publication rather than a generic SEO blog.

Core differentiators to preserve:

- photography-led editorial identity
- European Art Nouveau / Art Deco focus
- strong sense of place, street, facade, threshold and detail
- source-backed factual material
- explicit separation between verified fact, editorial interpretation and unresolved gaps
- multilingual capability
- links between buildings, cities, architects, styles and nearby subjects
- a calm, premium editorial visual language
- the Instagram account as an existing audience and distribution engine

The site should increasingly become the durable knowledge and search layer behind the social audience.

## Keep as-is unless evidence shows otherwise

The following are assets, not technical debt:

1. Deterministic static publication model.
2. `dist/` as the deployable artifact.
3. Separation of public runtime data and internal research.
4. Article-access compatibility layer while migration remains incomplete.
5. Structured v2 data model and stable technical taxonomy keys.
6. Editorial Manager as an internal control surface.
7. Existing image pipeline and publication checks.
8. Git history and current public baseline.
9. Existing design language as the starting point for visual refinement.
10. Human review before publication.

No framework migration should be undertaken merely for novelty. A migration is justified only if an audit demonstrates a material advantage for SEO, authoring, maintainability or automation that cannot be obtained progressively.

## Outdated assumptions to revisit

Several repository instructions reflect an earlier learning phase and are no longer fully aligned with the user's current goal of building a professional production system.

Revisit rather than blindly preserve:

- the hard-coded Codex model pin (`gpt-5.4`)
- the old automation-last framing
- the learning-first priority when it conflicts with production quality
- the assumption that automation should stay only pedagogical
- the absence of a single CI command covering the existing test corpus
- the GitHub Pages workflow debug step
- reliance on one large CSS file and several large runtime JS files if this starts constraining maintainability
- the mixed v1/v2 state once a safe migration process is proven

Production quality must remain conservative and reversible, but automation is now a first-class project objective.

## Immediate audit findings

### Strong foundations

- The build layer already handles more SEO infrastructure than a superficial audit would suggest: public routes, canonical links, hreflang, sitemap and OG images.
- The Editorial Manager already exposes useful machine-readable contracts and readiness gates.
- n8n integration was designed around a replaceable JSON boundary instead of coupling automation directly to the article store.
- Tests exist for analytics, image behavior, static pages, locale behavior, social-package behavior and editorial tooling.

### Gaps / professionalization targets

- No JSON-LD implementation was found during the recovery audit. Structured data should be designed deliberately for Article, CreativeWork, Place, Person/Organization and Breadcrumb use cases where appropriate.
- Existing test files are not exposed through a single obvious `npm test` / CI quality gate in `package.json`.
- The Pages workflow builds successfully but still contains a diagnostic build-input step that should be removed after recovery validation.
- The current production/development hosting story should be reviewed. GitHub Pages can remain the baseline, while branch/PR previews should be considered for safer visual review.
- Analytics, Search Console and social-performance data are not yet part of one recurring decision loop.
- The current social automation stops at a read-only handoff. It should evolve only after the creative format and review gates are proven.
- Affiliate and commercial layers do not yet exist and should not be inserted before editorial/SEO foundations are solid.

## Recovery rules

During the recovery phase:

- do not work directly on `main`
- prefer small pull requests
- do not mass-migrate article data and redesign the site in the same change
- do not remove compatibility paths until usage is measured and covered by tests
- any automated content generation must preserve provenance and clearly distinguish verified facts from generated prose
- image rights / credits remain a publication gate
- social publishing and site publishing require a human approval gate until the pipeline has demonstrated reliability
- changes to article schema, build logic, routes or publication rules require explicit tests

## Recovery exit criteria

Recovery is complete when:

- the project has one up-to-date orchestration document and roadmap
- agent instructions reflect the ANAD 2.0 production goal
- the existing test suite can be executed through a documented quality command and in CI
- a branch/PR preview path is available or deliberately rejected with rationale
- the live/static baseline has been visually audited on desktop and mobile
- SEO technical baseline has been audited, including JSON-LD, crawlability, canonicals, hreflang, sitemap, performance and metadata
- the article corpus has a measured v1/v2/locale/readiness inventory
- one article can move through research -> editorial -> QA -> preview -> publish -> social package with explicit gates
- one Reel can move through brief -> storyboard -> media selection -> render -> human review without ad-hoc steps

After these conditions are met, ANAD 2.0 can move from recovery to controlled production and automation.

## Recovery progress

Measured on 2026-09-15 after Recovery PR #1 was merged:

- canonical recovery and orchestration documents: complete
- Plus-aware model routing and Terra repository default: complete
- article corpus inventory: complete; see `research/anad-2-corpus-inventory.md`
- local quality command and pull-request CI gate: merged to `main`
- missing Editorial Manager backup module: restored and covered by the existing test suite
- obsolete GitHub Pages diagnostic step: removed
- desktop live/static baseline audit: complete; see `research/anad-2-baseline-audit.md`
- technical SEO baseline audit: complete; see `research/anad-2-baseline-audit.md`
- branch/PR previews: deterministic Netlify preview contract merged, with `dist/`
  as the only published artifact; GitHub Pages remains production
- mobile editorial pilot: implemented on `anad-2.0/mobile-editorial-pilot` with
  automated responsive guardrails; real-phone validation remains the human merge
  gate
- minimal Article + Place structured data: merged to `main`, with evidence boundaries
  and double-profile tests
- publication strategy decided: keep the current live set online, audit it, migrate
  approved articles to `published`, then exclude future drafts from production
- image rights/credit contract and corpus audit: complete; 21/21 runtime assets cleared
- end-to-end article pilot: Maison Coilliot accessibility merged; factual review and
  final human editorial/visual approval remain
- deterministic Reel pilot: pending
- current runtime media-rights inventory: complete on
  `anad-2.0/rights-and-review-flow`; 21/21 assets cleared from the explicit
  project-owner confirmation, with no wildcard inheritance
- single-article publication preflight: implemented on
  `anad-2.0/rights-and-review-flow`; the Maison Coilliot pilot passes content,
  locale and rights checks, with its existing `draft` status correctly
  preventing a ready-for-human-review result

With the mobile pilot applied, the clean quality baseline covers content validation,
media-rights validation, a deterministic build, 19 Node checks and 167 Python tests.
