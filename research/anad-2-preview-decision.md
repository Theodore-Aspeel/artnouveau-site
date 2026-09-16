# ANAD 2.0 - Pull-request preview contract

Date: 2026-09-16
Decision: use the existing Netlify integration as an isolated review surface

## Context

The site remains deployed to GitHub Pages from `main`, with GitHub and the repository
as the technical source of truth. During Recovery, automatic Netlify comments were
discovered on pull requests. No new host or account is required to obtain isolated
preview URLs.

The discovered preview initially returned Netlify's 404 page even though its bot
reported a successful deployment. The repository did not declare a Netlify build or
publish directory, so the preview contract was implicit and unreliable.

## Decision

Keep GitHub Pages as production. Use Netlify only for ephemeral pull-request previews,
with the following repository-owned contract:

- run `npm run build`;
- publish only `dist/`;
- use Node 20;
- never publish source files, internal research or editorial tooling;
- treat the preview as a review aid, never as a second production origin or content
  source.

The contract lives in `netlify.toml` and is protected by
`tests/netlify-preview.mjs`.

## Review flow

- Non-visual changes: review the diff and require green CI. A preview is optional.
- Visual changes: keep the PR in draft until the Netlify preview is successful and a
  real-device check completes the documented checklist.
- Verify that the preview URL resolves to the ANAD site, not Netlify's 404 page,
  before asking for visual approval.
- If the preview and local build disagree, stop and diagnose the deployment instead
  of approving from either one alone.
- Never use a preview to bypass factual, rights, editorial or publication gates.

## Boundaries

Netlify must not become:

- a CMS or content database;
- the production host while GitHub Pages remains the recorded production contract;
- a place for secrets or unpublished research;
- a reason to change the deterministic `dist/` build;
- an analytics source of record.

If the integration later introduces billing, account ownership, permission or privacy
risk, disable previews and return to local/device validation until a new decision is
recorded.
