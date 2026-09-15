# ANAD 2.0 — Orchestration Model

Date: 2026-09-15
Status: recovery / operating design

## Objective

Turn ANAD into a professional, AI-assisted editorial and distribution system built around the existing Art Nouveau / Art Deco publication and Instagram audience.

The system must improve output quality and throughput without allowing agents to silently invent facts, publish unreviewed content, break the site, or turn ANAD into a generic SEO content farm.

## System topology

### 1. ChatGPT Work — Orchestrator

Work is the project control layer.

Responsibilities:

- maintain project intent and priorities
- break goals into work packages
- route implementation to Codex/GitHub
- route research to research workflows
- route visual work to Canva / design workflows
- route video work to the Reel pipeline
- coordinate SEO, analytics and social-performance inputs
- maintain the backlog and decision log
- request human approval at defined gates

Work should not be treated as the source of truth for code or publication data. The repository remains the technical and editorial contract source.

### 2. GitHub — Technical source of truth

Repository: `Theodore-Aspeel/artnouveau-site`

GitHub owns:

- production code
- article runtime data
- research contracts and project documentation
- agent instructions / skills
- tests
- CI
- version history
- pull requests and review history

`main` remains protected conceptually as the production baseline. Recovery and larger work should occur through branches / PRs.

### 3. Codex — Implementation agent

Codex handles repository implementation work.

Expected behavior:

- read `AGENTS.md` and ANAD 2.0 recovery/orchestration documents first
- make narrow, reviewable changes
- run all relevant validation/tests
- report modified files and omissions
- prefer PR-ready work over broad speculative rewrites
- use subagents where useful for independent audit/review work

Codex may implement, refactor, test, debug and prepare migrations. It should not independently redefine editorial strategy.

## Specialized roles

Roles are logical responsibilities. They may initially be implemented as agent instructions/skills rather than separate persistent services.

### A. Heritage Research Agent

Inputs:

- subject/building/location
- existing ANAD facts and sources
- approved web/archive resources

Outputs:

- evidence packet
- confirmed facts
- disputed facts
- unresolved gaps
- source list with provenance
- candidate quotations with attribution

Hard rule: no unsupported factual completion.

### B. Editorial Agent

Inputs:

- verified research packet
- ANAD editorial style contract
- target language

Outputs:

- article draft
- dek
- sections
- meta description
- alt/caption proposals
- around/related-content suggestions

It may interpret verified material but must not transform uncertainty into fact.

### C. Localization Agent

Responsibilities:

- FR/EN/NL adaptation
- preserve names, dates and technical facts
- distinguish translation from editorial rewrite
- flag culturally awkward literal translations
- respect locale completeness checks

### D. SEO / Knowledge Agent

Responsibilities:

- keyword and intent analysis
- entity normalization
- structured data proposals
- internal linking
- city / architect / movement clusters
- title/meta testing
- indexation and Search Console analysis
- AEO / AI-search visibility review

SEO must serve editorial usefulness, not generate thin pages.

### E. Visual Agent

Responsibilities:

- image selection
- crop/aspect recommendations
- caption/alt alignment
- design-system consistency
- Canva assets, carousels and social variants
- rights/credit readiness checks

Original photography remains the preferred visual source whenever possible.

### F. Reel / Social Agent

Responsibilities:

- hook alternatives
- 15–45 s Reel story structure
- shot/image sequence
- on-screen copy
- narration script
- CTA
- caption and hashtags
- deterministic video spec / template input

The role should learn from actual retention, shares, saves and follows rather than optimize to generic “viral” clichés.

### G. QA / Publisher Agent

Checks:

- factual provenance
- article model validity
- locale readiness
- media presence
- rights / credits
- broken links
- SEO metadata
- structured data
- build/tests
- visual preview
- publication readiness

The QA agent may block publication.

## Human approval gates

Human approval remains mandatory at these boundaries during the initial ANAD 2.0 phase:

1. Research -> factual packet accepted
2. Article draft -> editorial approval
3. Preview -> publication approval
4. Reel storyboard/render -> social publication approval
5. Any new affiliate/commercial placement -> commercial/editorial approval

Automation may prepare work between gates.

## Primary content pipeline

```text
Idea
 -> Research packet
 -> Fact verification gate
 -> Article draft
 -> Localization
 -> SEO/entity enrichment
 -> Visual package
 -> QA
 -> Web preview
 -> Human publication approval
 -> Build/deploy
 -> Social package
 -> Reel/carousel generation
 -> Human social approval
 -> Publish/schedule
 -> Analytics ingestion
 -> Learning report
```

## Primary automation principle

Automate contracts, not improvisation.

Preferred automation boundaries are structured payloads with explicit versioning, validation and status fields. The existing `artnouveau.social_package@1` contract is the model to follow.

Potential future contracts:

- `artnouveau.research_packet@1`
- `artnouveau.article_draft@1`
- `artnouveau.visual_package@1`
- `artnouveau.reel_package@1`
- `artnouveau.publish_check@1`
- `artnouveau.performance_report@1`

## MCP / plugin priorities

### Tier 1 — immediate

- GitHub: repository, PRs, source of truth
- Canva: reusable brand/social design system
- Metricool: social analytics, posting-time data and eventual scheduling
- Google Search Console / GA4 connector: SEO and traffic feedback

### Tier 2 — after recovery

- Vercel or equivalent preview/deployment layer if PR previews materially improve review
- Figma if a substantial UI redesign is undertaken
- Semrush / Ahrefs / SE Ranking if keyword/backlink/competitive work justifies paid tooling

### Tier 3 — only with a demonstrated need

- Airtable / Notion as an additional operational database
- WordPress / Webflow migration
- heavy external CMS

Do not add a second source of truth merely because an integration exists.

## Video production direction

Use a repeatable ANAD Reel system rather than one-off AI videos.

Initial target:

- 9:16
- 15–45 seconds
- original photography / selected archival visuals
- restrained motion
- strong first-frame hook
- minimal typography
- optional narration
- subtitles
- one visual payoff/detail
- discreet CTA

A Remotion-based deterministic template should be evaluated during the Reel Lab so the same article package can produce repeatable previews and renders.

## SEO / knowledge direction

ANAD should evolve toward an entity-rich publication graph.

Key entity families:

- building / work
- architect / designer
- city
- country
- style / movement
- date / period
- material / motif / technique where editorially useful

The article remains the core editorial unit, while entity indexes can later generate meaningful discovery pages and internal links.

Structured data should be implemented deliberately rather than sprayed across every page.

## Metrics loop

Web metrics:

- indexed pages
- impressions
- clicks
- CTR
- query clusters
- landing pages
- organic sessions
- engaged sessions / time proxies where useful
- referrals from AI assistants when measurable

Social metrics:

- 3-second hold
- average watch time
- completion rate
- shares
- saves
- profile visits
- follows attributable to content

Business metrics later:

- newsletter subscribers
- affiliate clicks / conversion
- partner inquiries
- direct product / guide revenue if introduced

## First execution sequence

### Sprint 0 — Recovery

- inventory repository and deployments
- establish canonical recovery docs
- update agent/Codex operating rules
- expose complete test/quality commands
- audit runtime visually
- audit SEO baseline
- inventory article model/readiness

### Sprint 1 — Production foundation

- PR preview strategy
- CI quality gate
- JSON-LD / structured-data baseline
- editorial pipeline contract
- one end-to-end article pilot

### Sprint 2 — Reel Lab

- define ANAD Reel design grammar
- create 3 template concepts
- render/test 10 pieces
- measure Instagram outcomes
- choose the winning format(s)

### Sprint 3 — SEO graph

- entity normalization
- city/architect/style cluster plan
- internal-link rules
- Search Console feedback loop
- first scalable discovery pages

### Sprint 4 — Controlled automation

- automate research scaffolding
- automate validated handoffs
- automate preview/package creation
- schedule approved social content
- recurring performance review

### Sprint 5 — Monetization

- affiliate taxonomy and disclosure rules
- commercial-fit audit
- newsletter / audience capture
- partnerships / guides / products only where brand-aligned

## Definition of professional

ANAD 2.0 is professional when it is not dependent on one long ChatGPT conversation to remember how the project works.

A new competent agent should be able to enter the repository, read the contracts, understand the current state, perform a bounded task, validate it, and hand back a reviewable result without inventing hidden conventions.