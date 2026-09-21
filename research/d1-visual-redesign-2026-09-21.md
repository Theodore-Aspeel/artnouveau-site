# ANAD 2.0 - D1 refonte visuelle complète

Date : 2026-09-21  
Statut : **PRÊT POUR REVUE HUMAINE - implémentation et CI validées**  
Branche : `anad-2.0/d1-visual-redesign`  
PR draft : [#43](https://github.com/Theodore-Aspeel/artnouveau-site/pull/43)  
Base : `anad-2.0/d1-variant-b` au commit `e909e1e09ae4d77a8d47ba2b56b9dcab4dbd0b30`

## Décision appliquée

La variante B « Atelier photographique » reste la fondation technique. La nouvelle direction transforme cependant sa composition de façon substantielle : photographie plein cadre, contrastes encre/ivoire, grilles asymétriques, angles nets, titres à grande échelle et blocs documentaires plus distincts.

Une seule direction a été développée. BMAD n'a pas été relancé et aucune nouvelle recherche générale, dépendance, migration de framework ou modification du modèle éditorial n'a été introduite.

## État des livrables

- **RÉALISÉ** : branche dédiée créée depuis le HEAD exact de la variante B et PR draft #43 ouverte sans remplacer la PR #42.
- **RÉALISÉ** : accueil, auteur/portfolio, article, navigation, pied de page, mobile et tablette recomposés.
- **RÉALISÉ** : parcours auteur restauré dans les pages d'article par appel effectif du composant éditorial existant.
- **RÉALISÉ** : lanceur Windows `preview-windows.cmd`.
- **RÉALISÉ** : revue Playwright couvrant accueil, auteur et Maison Coilliot aux largeurs 390, 768 et desktop.
- **VALIDÉ** : workflow Quality #86 au commit `14573453a9841b028da3b91343ace150c9e4d05c`.
- **À VALIDER** : appréciation artistique et choix humain de fusion.
- **NON RÉALISÉ** : déploiement public, publication d'article ou fusion.

## Réutilisation ciblée

Décision **ADAPT** : les composants de la variante B, les helpers de routes et langues, le manifeste d'images responsives, les tests Playwright/axe-core/Lighthouse et les ressources photographiques autorisées existantes sont conservés. La refonte est une couche de composition CSS et quelques raccords HTML/JS, sans nouvelle bibliothèque.

## Fichiers modifiés

- `src/assets/styles/main.css` : direction visuelle globale et responsive.
- `src/assets/scripts/article-template.js` : activation du bloc auteur/portfolio/contact déjà construit.
- `src/pages/about.html` : classe de page dédiée.
- `src/pages/article-redirect.html` : classe de page dédiée.
- `src/pages/mentions.html` : classe de page dédiée.
- `scripts/build.mjs` : conservation correcte de `data-asset-base` après ajout de classe.
- `tests/web/d1-visual-review.spec.mjs` : matrice comparative 3 pages x 3 largeurs.
- `preview-windows.cmd` : prévisualisation locale Windows.

## Vérifications

[Workflow Quality #86](https://github.com/Theodore-Aspeel/artnouveau-site/actions/runs/35646626203) :

- `quality` : succès ;
- `pages-profile` : succès ;
- `publication-filter` : succès ;
- `lighthouse` : succès ;
- `browser-qa` : succès, parcours et contrôles axe-core inclus.

Les [captures comparatives et traces navigateur](https://github.com/Theodore-Aspeel/artnouveau-site/actions/runs/35646626203/artifacts/10660239325) couvrent les trois pages aux trois largeurs. Les [rapports Lighthouse](https://github.com/Theodore-Aspeel/artnouveau-site/actions/runs/35646626203/artifacts/10660720694) sont archivés séparément. Les artefacts expirent le 2026-10-05 selon la rétention GitHub actuelle.

## Prévisualisation Windows

1. Récupérer la branche.
2. Double-cliquer sur `preview-windows.cmd`.
3. Le script installe les dépendances verrouillées si nécessaire, ouvre `http://localhost:4173/fr/` et lance le serveur local.
4. Fermer la fenêtre du serveur pour arrêter la prévisualisation.

## Contrats préservés

- HTML/CSS/JS vanilla.
- Trois langues FR/EN/NL et fallbacks existants.
- Données des 14 articles inchangées.
- Statuts `draft`, règles `noindex`, droits et publication inchangés.
- Aucun média ajouté et aucune image IA.
- Aucun déploiement ni service externe supplémentaire.

## Limite connue

La baseline « avant » des captures est la version publique stable afin d'obtenir un comparatif reproductible dans la CI ; elle ne constitue pas une prévisualisation hébergée de la variante B. Si cette URL externe est temporairement indisponible lors d'une exécution future, le test joint un diagnostic texte, tandis que les captures et contrôles de la version « après » restent obligatoires.
