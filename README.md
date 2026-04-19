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

```bash
npm run validate
npm run build
npm run preview
```

- `validate`: checks required files and runtime asset references
- `build`: recreates `dist/`, copies the public runtime, rewrites page paths, then validates the published artifact
- `preview`: serves `dist/` locally on `http://localhost:4173`

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

- `tools/editorial_manager/`: read-only Python helper for inspecting and checking the article dataset. See `tools/editorial_manager/README.md`.

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
