# Art Nouveau Editorial Site

Static editorial website about Art Nouveau and Art Deco in Europe.

The project stays intentionally lean:
- vanilla HTML/CSS/JS
- deterministic static publication build
- `dist/` as the only publishable artifact
- no framework layer

## Stack

- HTML pages under `src/pages/`
- CSS under `src/assets/styles/`
- vanilla JavaScript under `src/assets/scripts/`
- editorial runtime data in `src/data/articles.json`
- static public root files in `public/`
- research and verification material in `research/`

## Structure

```text
src/
  pages/                Source HTML pages
  assets/
    styles/             Source CSS
    scripts/            Source JS
    images/             Runtime images
  data/                 Runtime JSON data
public/                 Files copied to dist root
research/               Internal research, never published
scripts/                Build / validate / preview scripts
tools/                  Internal Python tools, including Editorial Manager
dist/                   Generated publication artifact
```

## Install

This project does not require framework dependencies for runtime.

```bash
npm install
```

## Commands

Run the complete local quality gate before opening or updating a pull request:

```bash
npm ci
npm run quality
```

The quality gate validates and builds the publishable `dist/` artifact, then runs
the Node and Python test suites. Individual commands remain available as
`npm run validate`, `npm run build`, `npm run test:node`, and
`npm run test:python`.

```bash
npm run validate
npm run build
npm run preview
npm run editor
```

- `validate`: checks required files and runtime asset references
- `build`: recreates `dist/`, copies the public runtime, rewrites page paths, then validates the published artifact
- `preview`: serves `dist/` locally on `http://localhost:4173`
- `editor`: opens the local Editorial Manager with previews, guarded edits and
  the human publication preflight

The default publication policy remains `legacy-visible`, so the current public
corpus does not change. The future strict profile can be tested explicitly:

```bash
PUBLICATION_MODE=published-only npm run build
npm run test:publication-filter
```

On PowerShell:

```powershell
$env:PUBLICATION_MODE = 'published-only'
npm run build
npm run test:publication-filter
```

Strict mode writes only articles whose status is `published` to the public JSON,
article routes, sitemap and generated-image manifest. It is exercised in CI but
is not enabled by the production deployment workflow.

### Guarded publication pull request

The GitHub Actions workflow `Prepare article publication PR` connects the
approved editorial transition to the existing pull-request and deployment
gates. Run it manually from the Actions tab with an article slug and a real
publication date.

- `dry-run` is the default and creates nothing.
- `create-pr` requires the exact confirmation `PUBLISH`, repeats the preflight,
  writes the transition, commits only `src/data/articles.json`, runs all three
  existing quality profiles on that branch, and opens a review pull request
  only if they pass.
- The workflow never merges a pull request and never pushes `main`.
- GitHub Pages deploys only after the publication PR is reviewed and merged.

If repository settings prevent GitHub Actions from opening pull requests, the
workflow stops safely after pushing its dedicated publication branch. Enable
the repository option allowing Actions to create pull requests before retrying;
do not bypass the normal PR checks.

## Analytics

Public multilingual pages can include Plausible Analytics at build time.

Analytics is disabled by default. To enable it for a production build, set `PLAUSIBLE_DOMAIN` to the public site domain before running `npm run build`.

```bash
PLAUSIBLE_DOMAIN=artnouveauetdeco.com npm run build
```

On PowerShell:

```powershell
$env:PLAUSIBLE_DOMAIN = 'artnouveauetdeco.com'
npm run build
```

The build injects only the Plausible script tag. No cookie banner, consent system, or event tracking layer is included.

## Internal Tools

- `tools/editorial_manager/`: guarded Python helper for inspecting, checking,
  editing and preparing publication of the article dataset. See
  `tools/editorial_manager/README.md`.

## Publication Model

- Source lives under `src/` and `public/`
- `dist/` is rebuilt from scratch on each build
- only `dist/` should be deployed
- `research/` is intentionally excluded from the published artifact

## Data And Assets

- `src/data/articles.json` is the public runtime payload used by the gallery, article template, and compatibility route
- internal prompts, workflow notes, and research-only metadata must stay out of the published JSON
- runtime asset names should stay UTF-8 safe and portable; normalized names use lowercase ASCII with hyphens
- do not rename or delete historical backlog assets without validating references first

## Notes

- Files are expected to be UTF-8 with LF endings
- the build is static and deterministic by design
- remaining technical debt should be tracked explicitly rather than hidden in the runtime payload
