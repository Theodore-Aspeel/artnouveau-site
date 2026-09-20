# Unified article pipeline status

Date: 2026-09-20
Owner: Christophe Aspel
Status: read-only dashboard implemented

## Purpose

The Editorial Manager now exposes one command that answers where an article is
in the complete ANAD flow and what must happen next:

```bash
python -m tools.editorial_manager pipeline-status <slug>
python -m tools.editorial_manager pipeline-status <slug> --json
```

The command aggregates existing contracts and checks. It does not duplicate
publication logic, change article data, render media, connect Instagram or store
workflow state outside Git.

## Contract

The machine-readable compatibility marker is:

```json
{
  "name": "artnouveau.pipeline_status",
  "version": 1,
  "kind": "read_only_pipeline_dashboard"
}
```

The ordered stages are:

1. `editorial_qa`
2. `localization`
3. `media_rights`
4. `publication`
5. `social_package`
6. `reel_pilot`
7. `distribution`
8. `measurement`

Each stage reports a status, evidence, whether human approval is required and
one next action. The top-level `current_stage` is the first unfinished stage;
`next_action` is therefore the single instruction the operator needs now.

## Maison Coilliot checkpoint

On 2026-09-20, the real Maison Coilliot payload reports:

- editorial QA: ready;
- English and Dutch localization: ready;
- media rights and file integrity: 3/3 ready;
- current stage: publication;
- next action: Christophe reviews FR/EN/NL previews, then a real publication
  date is chosen and the guarded dry run is executed;
- social package, Reel distribution and measurement remain downstream.

This deliberately preserves the human publication gate. The article remains a
draft and the current public legacy-visible behaviour is unchanged.

## Reel planning decision

The normal-chat creative review recommended the article epigraph as the default
Maison Coilliot hook:

> Certaines façades changent tout de suite la tenue d’une rue.

`reel-pilot` now selects an available article epigraph as its default hook while
keeping all three source-bound alternatives in the contract. This is a planning
default only: Christophe must still approve the hook, storyboard, rendered
video and Instagram publication.

## Deliberate limits

The dashboard does not:

- approve or publish an article;
- infer that a human review happened;
- write status into `src/data/articles.json`;
- render or upload a Reel;
- connect Instagram, Canva, Metricool, Search Console or analytics;
- claim distribution or performance without imported evidence.
