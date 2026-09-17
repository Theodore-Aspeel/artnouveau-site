# ANAD Reel pilot contract

Date: 2026-09-17
Owner: Christophe Aspel
Status: deterministic review handoff implemented; no rendering or publication

## Purpose

The Editorial Manager can now turn an existing article social package into one
reviewable Reel pilot plan:

```bash
python -m tools.editorial_manager reel-pilot \
  maison-coilliot-lille-hector-guimard \
  --locale fr
```

For a deployment under a subpath, pass the complete public base URL:

```bash
python -m tools.editorial_manager reel-pilot \
  maison-coilliot-lille-hector-guimard \
  --locale en \
  --public-base-url https://theodore-aspeel.github.io/artnouveau-site
```

The command prints JSON only. It reads the article and the existing
`artnouveau.social_package@1` contract; it does not write article data or
produce a media file.

An exported payload can be checked independently before a future consumer uses
it:

```bash
python -m tools.editorial_manager validate-reel-pilot path/to/reel-pilot.json
```

## Stable boundary

The compatibility marker is:

```json
{
  "name": "artnouveau.reel_pilot",
  "version": 1,
  "kind": "read_only_reel_pilot_handoff"
}
```

The payload includes:

- one 1080 x 1920, 9:16, 24-second format target;
- three hook alternatives sourced from existing reviewed article text;
- a five-scene storyboard and on-screen text;
- the existing caption and a voice-over draft;
- explicit primary-subject and contextual-image roles;
- a locale-aware public destination with one UTM convention;
- Instagram and site metrics for the learning loop;
- human gates for storyboard, framing, render and publication;
- explicit negative capabilities proving that the command cannot render,
  upload, publish, store credentials or modify the article.

## Maison Coilliot finding

The Maison Coilliot article has one image of the primary building. Its two
supporting images show L'Huîtrière and the Lumière du Nord lodge. The default
storyboard therefore uses the Maison Coilliot hero only and suggests restrained
crop motion. Contextual images stay excluded unless a human deliberately
approves a comparison sequence.

The current pilot status is `needs_upstream_review` because the article is still
`draft`. This is expected and preserves the existing publication gate.

## UTM convention

The first convention is deliberately small:

| Field | Value |
| --- | --- |
| `utm_source` | `instagram` |
| `utm_medium` | `organic_social` |
| `utm_campaign` | `anad_reel_<article-slug>` |
| `utm_content` | `<source-locale>_pilot` |

The tracked URL is intended for the profile link or a Story sticker. Instagram
captions are not treated as a dependable clickable-link surface.

## Human sequence

1. Choose one of the three hooks.
2. Approve the storyboard and 9:16 crops.
3. Render one pilot outside this command.
4. Review the actual video, subtitles and safe areas.
5. Approve Instagram publication explicitly.
6. Compare results with the account's recent median.

No deterministic video template should be declared stable before this pilot has
been rendered, reviewed and measured.

## Deliberate limits

This lot does not:

- connect an Instagram account;
- call Meta, Canva, Metricool, Remotion or n8n;
- invent new factual or editorial text;
- generate synthetic imagery;
- render or upload video;
- publish or schedule content;
- change the Maison Coilliot publication status.
