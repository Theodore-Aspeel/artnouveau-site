# ANAD 2.0 - Publication readiness audit

Date: 2026-09-16
Baseline: `main` at `55f332c`
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
- 14/14 hero images and every runtime support image have localized alternative text.
- All `published_on` and `updated_on` values remain null.
- 14/14 subjects have an entry in `research/verified-facts.json`; 13 have no known
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
| `READY_STRUCTURE` | Maison Coilliot, Lille | Resolve the two documented wording points, final visual approval, publication date |
| `READY_STRUCTURE` | L’Huitrière, Lille | Final multilingual read, image framing approval, publication date |
| `READY_STRUCTURE` | Maison des Hiboux, Saint-Gilles | Final multilingual read, image framing approval, publication date |
| `READY_STRUCTURE` | Maison Strauven, Tournai | Final multilingual read, image framing approval, publication date |
| `READY_STRUCTURE` | Den Tijd, Anvers | Final multilingual read, image framing approval, publication date |
| `READY_STRUCTURE` | Maison aux Tulipes, Bratislava | Approve the cautious architect attribution and editorial title, final multilingual and visual review, publication date |
| `READY_STRUCTURE` | Maison-atelier d’Ernest Delune, Ixelles | Final multilingual and visual review, publication date |
| `BLOCKED` | Façade Art Déco, Charleroi | Identify the building and resolve address/date/architect, or explicitly retire the page |

The accessibility gap is now closed across every runtime article. The Maison aux
Tulipes fact review confirms its address, 1903 date, registered name and style from
the official Slovak heritage open data. The article keeps Jenő Schiller as an
explicit attribution because the register does not identify an architect. Details
and source boundaries are recorded in
`research/pilots/maison-aux-tulipes-fact-review.md`.

The Delune fact review removes the misleading implication that the 1902 annex was
commissioned for Clas Grüner Sterner. The official inventory confirms Victor
Marchal as commissioner and Sterner as a later long-term occupant who used the
building as his dwelling and workshop. The two-phase 1893/1902 history and the
editorial corrections are recorded in
`research/pilots/maison-ernest-delune-fact-review.md`.

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
`research/pilots/maison-coilliot-fact-review.md`. It identifies two formulations for
human editorial reconsideration and keeps the publication-status change outside the
research lot.
