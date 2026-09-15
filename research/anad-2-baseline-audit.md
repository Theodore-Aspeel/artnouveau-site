# ANAD 2.0 - Live, Visual and Technical SEO Baseline Audit

Date: 2026-09-15  
Baseline: `main` at `afe9b1b8b013c4716e423c7ec24a851fcceb2516`  
Audit branch: `anad-2.0/audit-baseline`  
Live target: `https://theodore-aspeel.github.io/artnouveau-site/`

## Scope and method

The audit combined:

- live browser inspection of the root, canonical French homepage and one long
  French article at a 1363 x 936 desktop viewport;
- DOM, metadata, heading, image-loading and horizontal-overflow inspection;
- representative color-contrast measurements;
- deterministic build inspection with the GitHub Pages deployment environment;
- source review of responsive CSS, routing, sitemap, metadata, article status,
  media alternatives and credits;
- the existing Node test suite against the deployment build profile.

The browser environment did not permit a genuine mobile viewport capture. Mobile
coverage in this audit is therefore based on responsive-source inspection, not a
completed visual device audit. The Recovery mobile visual criterion remains open.

## Executive conclusion

The live site has a credible and distinctive editorial identity. Desktop rendering
is calm, coherent and readable, and the canonical locale routes are substantially
stronger than the compatibility root suggests.

Recovery should not proceed directly to JSON-LD. Publication control and basic
metadata correctness need to be fixed first. The most consequential finding is
that all 14 articles are marked `draft` while all 14 are still built, linked and
included in the public sitemap. The repository currently has a readiness warning,
not an actual publication gate.

## What is already strong

- The homepage and article use a coherent premium visual language.
- Typography, photography, spacing and restrained color support the author-led
  positioning.
- The inspected desktop pages had no horizontal overflow.
- The canonical French homepage and article each expose one clear H1 and a logical
  heading hierarchy.
- Canonical locale routes have correct absolute canonical links.
- FR, EN, NL and `x-default` hreflang links are present on canonical public routes.
- The generated sitemap contains 51 canonical locale URLs: 3 locales multiplied by
  3 static pages and 14 articles.
- The GitHub Pages build generates a correct deployed sitemap reference in
  `robots.txt`.
- Hero images use responsive generated formats; the inspected article hero is eager
  and supporting images are lazy.
- Core body text contrast is strong: 14.91:1 for primary copy and approximately
  7.6:1 for secondary copy in the inspected theme.

## Findings by priority

### P0 - Publication state is not enforced

Evidence:

- all 14 runtime articles have `status: draft`;
- `scripts/build.mjs` builds every article without filtering on status;
- the gallery and article sequence use every article;
- the sitemap includes every article in all three locales;
- the same articles are live publicly.

Impact:

- the documented human publication gate is not technically real;
- a future draft can become public merely by entering the runtime dataset;
- publication readiness and actual distribution can diverge silently.

Decision recorded on 2026-09-15: keep the 14 existing articles online during
Recovery. Before enforcing the production filter, audit rights, credits and
editorial readiness, then mark the approved existing set as `published`. Once that
migration is complete, the production build, gallery and sitemap must exclude all
future drafts.

No bulk status change belongs in an audit PR, and no currently live article should
disappear as a side effect of introducing the gate.

### P0 - Image rights and credit gate is not demonstrable

Measured corpus state:

- 14 hero credits present: 0;
- support-image credits present: 0;
- editorial image credits present: 0;
- 8 support images are currently attached across the corpus.

Null credit fields do not prove that images are unlicensed, especially when they
may be original photography. They do prove that the repository cannot currently
demonstrate the rights/credit decision required by the publication rules.

Required follow-up:

- define whether `original_photo`, author ownership, explicit credit, licensed
  source or public-domain evidence is the stable rights contract;
- block final publication when the applicable evidence is absent.

### P1 - Compatibility pages create indexable duplicates

There are 57 generated HTML files but only 51 canonical public pages. The six
compatibility files are:

- `index.html`;
- `about.html`;
- `mentions.html`;
- `article.html`;
- `404.html`;
- `articles/template.html`.

The 404 and legacy template are correctly `noindex`. The root homepage, about,
mentions and dynamic article compatibility pages remain `index,follow` without a
canonical or hreflang contract. The live root duplicates the French homepage.

Recommended correction:

- make compatibility documents `noindex,follow`;
- provide a direct redirect where GitHub Pages permits it;
- keep only canonical locale routes in the sitemap.

### P1 - Social metadata images are incomplete or invalid

- All 42 localized article pages have an `og:image`, but its value is relative.
- Static public pages have no Open Graph image.
- `og:url` is absent.
- Twitter cards use `summary` and have no dedicated image metadata.
- `og:image:alt`, image dimensions and MIME metadata are absent.

The first correction should generate absolute article image URLs from the same
deployment origin/base-path contract used for canonical URLs. A single approved
site-level sharing image can then cover homepage and static pages.

### P1 - Structured data is absent

All 57 generated HTML files contain zero JSON-LD blocks. The first implementation
should be narrow and evidence-backed:

- `WebSite` or `Organization` only when the publisher identity is settled;
- `Article` plus the represented `Place` or `CreativeWork` for article pages;
- `BreadcrumbList` for public pages with visible breadcrumbs.

Do not emit an architect, date, address or authorship claim in JSON-LD unless it is
derived from the stable verified article fields.

### P2 - The PR quality workflow covers only the root deployment profile

The static-page test already understands `PUBLIC_BASE_PATH`. A manual GitHub
Pages-profile build followed by the correctly configured Node suite passes all 9
checks. The pull-request quality workflow nevertheless runs only the default root
profile, while the Pages workflow builds the project-site profile without running
the Node suite.

Add the GitHub Pages profile as a second CI check before changing routing or preview
hosting. This is a coverage improvement, not evidence of a broken live route.

### P2 - Site icons ignore the GitHub Pages base path

All 57 generated pages retain root-relative icon references such as `/favicon.ico`
and `/icon.svg`. On project-site hosting these resolve at the GitHub user-domain
root rather than under `/artnouveau-site/`.

The build should rewrite these URLs through the deployment base-path contract.

### P2 - Supporting images lack localized alternatives

The corpus contains 8 supporting images. Non-empty supporting-image alternatives:

- FR: 0;
- EN: 0;
- NL: 2.

The browser confirms that blank values render as empty `alt` attributes. This is
valid only for genuinely decorative images. The current galleries communicate
article-related visual information, so each image needs either an explicit
localized alternative or an explicit decorative classification.

### P2 - Gold microcopy contrast is marginal

The inspected gold eyebrow text measured approximately 3.85:1 against the page
background at roughly 12 px. Normal small text should reach 4.5:1. Main copy and
navigation contrast are otherwise strong.

Use a slightly darker accent for small text while preserving the current gold for
rules, borders and large decorative elements.

### P3 - The homepage is long but intentionally structured

The live French homepage was approximately 8,278 CSS pixels tall at the inspected
desktop viewport. This is not automatically a defect: editorial entry points,
city paths and the full corpus are clearly separated. Revisit pagination or an
archive page only if analytics show weak discovery or excessive abandonment.

## Responsive source assessment

The current CSS has sensible structural breakpoints:

- article and home hero layouts become one column below 960 px;
- galleries become one column below 700 px;
- navigation collapses below 600 px;
- mobile root font size remains 17 px;
- grid tracks use `minmax(0, 1fr)`, reducing overflow risk;
- reduced-motion preferences are respected.

This supports confidence in the implementation but does not replace a real mobile
visual pass. The next visual audit must cover at least 390 px and 768 px widths,
menu open/closed states, a long title, gallery cards, an article support gallery and
the footer.

## Recommended execution order

1. Define the image-rights/credit contract and audit all current images.
2. Review the current live set, mark approved articles as `published`, then enforce
   the production publication-status contract for future drafts.
3. Add GitHub Pages deployment-profile tests.
4. Fix compatibility indexation, absolute social URLs and base-path icons.
5. Complete real mobile visual QA.
6. Add a minimal tested JSON-LD baseline.
7. Decide whether PR previews justify an additional host.
8. Run one article through the complete human-gated publication pipeline.

## Intentionally out of scope

- no article status was changed;
- no CSS or design was modified;
- no content, translation or image credit was invented;
- no JSON-LD was emitted;
- no hosting platform was added;
- no compatibility path was removed.
