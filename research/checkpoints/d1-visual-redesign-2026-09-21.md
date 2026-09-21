# Checkpoint D1 - refonte visuelle complète

Date : 2026-09-21  
Statut : **EN COURS**  
Branche : `anad-2.0/d1-visual-redesign`  
Base immuable : variante B, commit `e909e1e09ae4d77a8d47ba2b56b9dcab4dbd0b30`

## Reprise rapide

La décision humaine remplace le périmètre visuel initial de D1, sans modifier les autres décisions ANAD. La refonte « revue photographique » est implémentée et enregistrée. Ne pas relancer BMAD, ne pas créer d'autres variantes et ne pas reprendre l'audit général des outils.

Prochaine action déterministe :

1. lire le résultat du workflow Quality du dernier commit de la branche ;
2. corriger uniquement les erreurs réelles de build, Playwright, axe ou Lighthouse ;
3. récupérer l'artefact `browser-qa-artifacts` qui contient les captures 390/768/desktop ;
4. présenter une seule revue humaine groupée ;
5. ne fusionner ni cette PR ni la PR #42 avant validation de Théodore.

## Points techniques

- Le défaut de la PR #42 provenait notamment du fait que `appendEditorialBlock()` était défini mais jamais appelé.
- La refonte ne change pas `src/data/articles.json`.
- Le preview Windows est `preview-windows.cmd`.
- Le rapport est `research/d1-visual-redesign-2026-09-21.md`.
- Le checkpoint historique du premier pilote D1 n'a pas été modifié.
