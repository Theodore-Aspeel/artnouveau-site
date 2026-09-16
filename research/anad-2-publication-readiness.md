# ANAD 2.0 - Publication readiness audit

Date: 2026-09-16  
Baseline: `main` at `326ef24`  
Scope: 14 runtime articles, no web re-research and no status change

## Decision

Do not switch all current articles to `published` and do not enable the production
draft filter yet.

The runtime structure, languages, author identity and image rights are in good
condition, but publication status would currently overstate factual and
accessibility readiness. The transition must happen in reviewed batches.

## Corpus-wide findings

- 14/14 articles use the v2 model.
- 14/14 contain structurally complete FR, EN and NL content.
- 14/14 identify `Christophe Aspel` as author.
- 21/21 runtime images are present and cleared in the explicit rights registry.
- 14/14 hero images have localized alternative text.
- All `published_on` and `updated_on` values remain null.
- 12 subjects have an entry in `research/verified-facts.json`; 11 have no known
  contradiction in that internal packet.
- Public resource links mainly support quotations. They do not yet expose the full
  factual provenance packet to readers.

## Classification

| Class | Article | Required action before `published` |
|---|---|---|
| `READY_STRUCTURE` | Maison Fernand Lefever, Bruxelles | Final FR read, quick EN/NL check, image framing approval, publication date |
| `READY_STRUCTURE` | Maison Lotus, Anvers | Final FR read, quick EN/NL check, image framing approval, publication date |
| `READY_STRUCTURE` | Palais de la Sécession, Vienne | Final FR read, quick EN/NL check, image framing approval, publication date |
| `READY_STRUCTURE` | Maison des Majoliques, Vienne | Final FR read, quick EN/NL check, image framing approval, publication date |
| `READY_STRUCTURE` | Casa Campanini, Milan | Final FR read, quick EN/NL check, image framing approval, publication date |
| `READY_STRUCTURE` | Aquarium de Milan | Final FR read, quick EN/NL check, image framing approval, publication date |
| `NEEDS_ACCESSIBILITY` | Maison Coilliot, Lille | Add and review six localized support-image alternatives, then final approval |
| `NEEDS_ACCESSIBILITY` | L’Huitrière, Lille | Add and review six localized support-image alternatives, then final approval |
| `NEEDS_ACCESSIBILITY` | Maison des Hiboux, Saint-Gilles | Add and review FR/EN alternative for its support image |
| `NEEDS_ACCESSIBILITY` | Maison Strauven, Tournai | Add and review three localized support-image alternatives |
| `NEEDS_ACCESSIBILITY` | Den Tijd, Anvers | Add and review FR/EN alternative for its support image |
| `NEEDS_FACT_REVIEW` | Maison aux Tulipes, Bratislava | Build a verified fact packet, resolve the pending date and add three image alternatives |
| `NEEDS_FACT_REVIEW` | Maison d’Ernest Delune | Remove or prove the implied direct commission “pour un maître verrier” |
| `BLOCKED` | Façade Art Déco, Charleroi | Identify the building and resolve address/date/architect, or explicitly retire the page |

There are 22 missing localized alternative texts across the eight support images.

## Why the draft filter remains disabled

The current production site intentionally keeps all 14 pages visible. Enabling a
strict `published` filter now would remove every article, including the unresolved
Charleroi page, and contradict the recorded no-disappearance decision.

The safe order is:

1. approve and date a small article batch;
2. move only that batch to `published`;
3. resolve or explicitly retire every remaining live exception;
4. confirm that no intended public page remains `draft`;
5. enable the filter in build, gallery, article sequences and sitemap together;
6. add regression tests proving that future drafts stay private.

## Recommended pilot adjustment

Maison Coilliot remains the best end-to-end subject because its content, rights and
factual packet already pass. The six FR/EN/NL alternatives for its two supporting
photographs were merged in PR #8. The remaining gate is the final multilingual
editorial and visual review, followed by an explicit publication date and approval.

The detailed source and claims review is recorded in
`research/pilots/maison-coilliot-fact-review.md`. It identifies one French sentence
for human editorial reconsideration and keeps the publication-status change outside
the research lot.
