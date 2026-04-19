# FR Source Translation Sync Foundation

## Current State

The public article corpus lives in `src/data/articles.json`. The current runtime
payload is v2-shaped: each article keeps stable article data outside localized
content, and visible reader-facing text lives under `content.fr`, `content.en`,
and `content.nl`.

French is the editorial source language. The local editor already treats French
as required and EN/NL as optional editable localized layers. The editor can edit
existing localized fields, existing section fields, existing practical item
values, and existing image slots, but it does not change article shape.

## Design Decision

The synchronization foundation should live in internal tooling, not in public
runtime rendering code and not as private workflow notes inside article content.

For now, the foundation is read-only:

- enumerate French source units with stable paths
- compute a deterministic hash for each French source unit
- compare each target locale by field presence
- optionally compare against a previous source hash supplied by future internal
  state

This gives future tooling enough structure to identify that a French source unit
changed since translation without deciding today how translations are generated.

## Stable Source Units

The first supported units are deliberately limited to existing reader-facing
article fields:

- `title`
- `dek`
- `epigraph`
- `seo.meta_description`
- `media.hero_alt`
- `around.note`
- `sections[N].heading`
- `sections[N].body`
- `practical_items.<key>.value`

Section paths are index-based because the current editor does not add, remove,
or reorder sections. Practical item paths use the stable practical key rather
than the array index.

## Status Semantics

For one source unit and one target locale:

- `missing`: French source exists, but the target field is empty or absent.
- `localized-untracked`: target text exists, but no previous source hash was
  supplied. This preserves manual corrections by default.
- `current`: target text exists and the supplied previous source hash matches
  the current French source hash.
- `source-changed`: target text exists, but the supplied previous source hash no
  longer matches the current French source hash.

`source-changed` is a signal for review or selective relaunch. It is not an
instruction to overwrite target text.

## Future State Location

If the project later stores synchronization state, keep it internal and
non-public. A possible shape is an internal JSON file under `research/` or a
future editorial tooling state directory, keyed by article slug, target locale,
and source-unit path:

```json
{
  "maison-coilliot-lille-hector-guimard": {
    "en": {
      "title": "sha256-of-last-translated-french-title"
    }
  }
}
```

Do not store this private workflow state in `content.en`, `content.nl`, or other
public reader-facing article fields.

## Deliberate Limits

This foundation does not:

- call a translation API
- create translations
- overwrite EN/NL text
- add per-field metadata to `src/data/articles.json`
- redesign the editor
- change the runtime article renderer

The goal is only to make future synchronization logic explicit, testable, and
small enough to explain.
