# ANAD 2.0 - Pull-request preview decision

Date: 2026-09-16  
Decision: deliberately defer a third-party preview host during Recovery

## Context

The site is a deterministic static build deployed to GitHub Pages from `main`.
Pull requests already run the root and GitHub Pages build profiles, but GitHub Pages
does not provide an isolated live URL for every branch in this repository.

## Decision and rationale

Do not add Vercel, Cloudflare Pages, Netlify, a CMS or a second hosting source during
Recovery only to obtain preview URLs.

Current reasons:

- the release cadence and contributor count remain low;
- GitHub is already the single technical source of truth;
- a second host introduces account, permission, environment and domain maintenance;
- current build and deployment checks are deterministic;
- no evidence yet shows that preview hosting saves more effort than it adds.

This is a deliberate rejection for the Recovery exit criterion, not a permanent
ban on previews.

## Interim review contract

- Non-visual changes: review the PR diff, require both CI jobs, merge only after the
  documented human gate when one applies.
- Visual changes: keep the PR in draft, use automated layout assertions and an
  explicit device checklist, then perform a short real-device check after an
  authorized reversible deployment.
- If the live visual check fails, revert the isolated commit instead of stacking
  unrelated fixes on production.
- Never mix content publication approval with a visual or hosting experiment.

This interim contract is less convenient than a true branch preview. It is accepted
only while visual releases remain infrequent and small.

## Reconsideration triggers

Evaluate an isolated preview host when any of these becomes true:

- more than one visual/content release is prepared per week;
- another regular contributor needs browser review;
- a commercial or newsletter flow raises the cost of a production defect;
- repeated mobile issues escape source and automated checks;
- the Reel/social pipeline needs a stable campaign landing-page preview.

At that point compare only lightweight static-preview options. The selected service
must build from the GitHub PR, expose no internal research files, require no second
content database and preserve `dist/` as the deployable contract.

