# Checkpoint D1 - direction image-first

Date : 2026-09-22  
Statut : **PRÊT POUR REVUE HUMAINE**
Branche : `anad-2.0/d1-image-first`
Base : PR #43 au commit `9f725dc97099503f8d46df82648f104ec6667b81`
PR draft : #44
HEAD vérifié : `523c23dbad6b1656f18078c4f84122fc3e287029`
Workflow final : Quality #90, exécution `35718416185`, succès complet

## Reprise déterministe

La PR #43 est rejetée artistiquement mais conservée comme base technique. La nouvelle direction image-first est implémentée dans la PR draft #44. Ne pas relancer BMAD, ne pas créer de variante concurrente et ne pas modifier C1.

1. Télécharger et ouvrir le paquet privé, puis lancer `start-private-preview.cmd` sous Windows.
2. Examiner ensemble `/private/`, `/private/portfolio.html` et `/private/series-blue.html`.
3. Examiner les captures publiques 390/768/1365 de l'artefact CI `browser-qa-artifacts` (expiration le 6 octobre 2026).
4. Consulter les changements et le rapport de la PR draft #44.
5. Recueillir une seule validation artistique groupée ; ne rien fusionner ni déployer avant décision de Théodore.

## Contrôles terminés

- `npm test` : succès ; Node 24/24, Python 207/207.
- Build public : 14/14 articles en profil `legacy-visible`.
- Registre de droits : 24/24 ressources publiques prêtes.
- Quality #90 : `quality`, `publication-filter`, `pages-profile`, `browser-qa` et `lighthouse` réussis.
- Playwright/axe et captures publiques : artefact `browser-qa-artifacts` de l'exécution `35718416185`.
- Lighthouse : artefact `lighthouse-reports` de la même exécution.

## Frontière privée

Les 12 JPEG extraits du Google Doc sont conservés uniquement dans `.private-media/` et documentés dans `research/d1-image-first-private-preview.md`. Le script `scripts/prepare-private-preview.mjs` ne s'exécute que lorsque `PRIVATE_PREVIEW=1`.

Ces fichiers sont des extractions du DOCX, non des originaux natifs. Leur provenance et leurs droits individuels restent à valider. Aucun octet de ces images n'est présent dans la branche, la PR ou les artefacts CI.
