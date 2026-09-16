# ANAD 2.0 - Publication gate flow

## Goal

Turn the final human decision into one short review without claiming that
software can certify historical interpretation or visual taste.

## Automated preflight

The publication-gate command checks one article and emits both a readable
summary and a versioned JSON report.

It combines:

1. article status and required French publication fields;
2. complete English locale readiness;
3. presence of hero and support image files;
4. explicit media-rights coverage and clearance;
5. preview links for FR, EN and NL;
6. a mandatory human-approval marker.

The possible automated results are:

- blocked: at least one objective error;
- needs-review: no objective error, but a warning remains;
- ready-for-human-review: every automated check passed, while publication still
  requires a human decision.

The command never publishes, changes an article status or writes to the corpus.
It does not replace the complete project-level npm quality gate, which remains
mandatory before merge and deployment.

## Pilot

Maison Coilliot is the first pilot because it exercises one hero image, two
shared support images, three locale blocks and a verified quotation.

Current measured result:

- article fields: pass;
- English locale: en-ready;
- media rights: 3/3 cleared;
- localized support-image alternatives: 6/6 present;
- human approval: required;
- overall status: needs-review, solely because the article is still draft.

No status changes are made during this lot. This preserves the current public
site until the factual and visual review of the pilot is complete.

## Final human review

For the pilot, the reviewer should only need to:

1. open the FR and EN previews;
2. confirm the text, image order and crops;
3. approve or request a correction;
4. allow the controlled status change in a separate small pull request.

After several successful pilots, the same gate can become the basis for a
single review screen in the Editorial Manager.

## Corpus activation plan

`publication-plan` applies the individual gate to the whole corpus and compares
the current `legacy-visible` behaviour with the future `published-only` policy.
It is deliberately read-only: it does not change statuses and it does not enable
the build filter.

The `artnouveau.publication_plan@1` JSON contract records:

- current and strict visibility for every article;
- the exact set of pages that strict mode would hide;
- individual automated-gate results and publication dates;
- a corpus-level activation status;
- the mandatory final human approval.

The command exits successfully when the report is generated, even if activation
is blocked. Automation must read `activation_status`; generating a truthful
blocked plan is not itself a command failure.

## Strict build profile

`PUBLICATION_MODE=published-only` applies the candidate policy to the complete
published artifact: runtime JSON, gallery input, canonical article pages,
sitemap and generated article images. The default remains `legacy-visible`, so
adding and testing the filter does not remove any existing public page.

CI builds the strict profile separately and verifies that draft articles do not
leak into any of those surfaces. Production must not set this variable until the
publication plan is ready and a human explicitly approves activation.
