# Checkpoint D1 - refonte visuelle complète

Date : 2026-09-21  
Statut : **PRÊT POUR REVUE HUMAINE**  
Branche : `anad-2.0/d1-visual-redesign`  
PR draft : [#43](https://github.com/Theodore-Aspeel/artnouveau-site/pull/43)  
Base immuable : variante B, commit `e909e1e09ae4d77a8d47ba2b56b9dcab4dbd0b30`

## Reprise rapide

La décision humaine remplace le périmètre visuel initial de D1, sans modifier les autres décisions ANAD. La refonte « revue photographique » est implémentée et enregistrée. Ne pas relancer BMAD, ne pas créer d'autres variantes et ne pas reprendre l'audit général des outils.

Le code validé est le commit `14573453a9841b028da3b91343ace150c9e4d05c`. Le [workflow Quality #86](https://github.com/Theodore-Aspeel/artnouveau-site/actions/runs/35646626203) est entièrement vert : quality, pages-profile, publication-filter, Lighthouse et browser-qa.

Les [captures comparatives](https://github.com/Theodore-Aspeel/artnouveau-site/actions/runs/35646626203/artifacts/10660239325) couvrent accueil, auteur et article à 390, 768 et desktop. La baseline avant est le site public stable ; la version après provient de la branche locale construite en CI. L'artefact expire le 2026-10-05 selon la rétention GitHub actuelle.

## Prochaine décision humaine

1. examiner la PR draft #43 et son rapport ;
2. parcourir localement la branche avec `preview-windows.cmd` ;
3. rendre une seule revue artistique groupée ;
4. ne fusionner ni cette PR ni la PR #42 avant validation de Théodore.

## Points techniques

- Le défaut de la PR #42 provenait notamment du fait que `appendEditorialBlock()` était défini mais jamais appelé ; l'appel est restauré.
- La refonte ne change pas `src/data/articles.json`.
- Les brouillons, `noindex`, droits, langues et pipeline de publication sont préservés.
- Le rapport est `research/d1-visual-redesign-2026-09-21.md`.
- Le checkpoint historique du premier pilote D1 n'a pas été modifié.
- Aucun déploiement, publication d'article, service payant ni fusion n'a été effectué.
