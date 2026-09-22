# Checkpoint D1 - direction image-first

Date : 2026-09-22  
Statut : **EN COURS**  
Branche : `anad-2.0/d1-image-first`  
Base : PR #43 au commit `9f725dc97099503f8d46df82648f104ec6667b81`

## Reprise déterministe

La PR #43 est rejetée artistiquement mais conservée comme base technique. La nouvelle direction image-first est implémentée localement. Ne pas relancer BMAD, ne pas créer de variante concurrente et ne pas modifier C1.

1. Exécuter les tests Node et navigateur.
2. Corriger uniquement les régressions réelles.
3. Pousser la branche et ouvrir une PR draft basée sur `anad-2.0/d1-visual-redesign` afin de préserver #42 et #43.
4. Récupérer les captures publiques 390/768/desktop de la CI sans y inclure les médias privés.
5. Produire les captures privées depuis `.private-media/` hors GitHub.
6. Présenter une seule revue humaine groupée ; ne rien fusionner ni déployer.

## Frontière privée

Les 12 JPEG extraits du Google Doc sont conservés uniquement dans `.private-media/` et documentés dans `research/d1-image-first-private-preview.md`. Le script `scripts/prepare-private-preview.mjs` ne s'exécute que lorsque `PRIVATE_PREVIEW=1`.

