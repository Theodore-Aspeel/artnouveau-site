# ANAD 2.0 - D1 direction image-first

Date : 2026-09-22  
Statut : **PRÊT POUR REVUE HUMAINE - implémentation et contrôles techniques terminés**
Branche : `anad-2.0/d1-image-first`
Base technique : PR #43, commit `9f725dc97099503f8d46df82648f104ec6667b81`
PR draft : #44
HEAD vérifié : `523c23dbad6b1656f18078c4f84122fc3e287029`

## PROPOSÉ

Une seule direction : ANAD comme portfolio photographique d'auteur. Une photographie ouvre chaque parcours ; le texte vient ensuite. Les sélections sont des séquences verticales, jamais une mosaïque décorative.

## RÉALISÉ

- Accueil sans paragraphes superposés à l'image : photographie autonome et invitation courte dans un rail adjacent.
- Sélection d'ouverture transformée en succession de grandes photographies respectant leurs proportions.
- Portfolio auteur transformé en séries espacées, avec portrait en couleur et méthode longue repliable.
- Articles réordonnés : image principale, identité du bâtiment, galerie, puis texte et données documentaires.
- Palette ivoire, encre et bleu architectural ; suppression des grands voiles sombres sur les photographies.
- Lanceur Windows public corrigé pour ouvrir le navigateur après le démarrage effectif du serveur.
- Lanceur privé et générateur local ajoutés, sans média privé dans Git.
- Maquette privée de la série bleue et index séparé des autres sujets.

## ACQUIS TECHNIQUES RÉUTILISÉS

Décision **ADAPT** : HTML/CSS/JS vanilla, routes localisées, helpers article, images responsives, droits, publication, brouillons, `noindex`, bloc auteur/portfolio/contact, Playwright, axe-core, Lighthouse et preview Node de la PR #43.

## IMAGES RÉELLEMENT UTILISÉES

- Code GitHub et CI : uniquement les médias déjà présents et autorisés dans le dépôt.
- Maquette locale privée : 12 JPEG extraits du DOCX de la planche Drive ; aucune prétention d'original natif.
- Série pilote : cinq vues du bâtiment bleu, présentées sous libellés descriptifs uniquement.

## VÉRIFIÉ

- Validation de contenu : succès local.
- Contrôle du registre de droits public : 24/24 ressources prêtes, aucune anomalie.
- Build public : succès, 14/14 articles en mode `legacy-visible`.
- Tests Node : 24/24 réussis ; tests Python : 207/207 réussis.
- Export Drive : 12 images incorporées récupérables et mappées aux douze libellés.
- Frontière de confidentialité : `.private-media/` ignoré ; `dist/private/` produit uniquement avec `PRIVATE_PREVIEW=1`.
- Workflow Quality #90 : succès complet sur le HEAD vérifié (`quality`, `publication-filter`, `pages-profile`, `browser-qa` et `lighthouse`).
- Playwright/axe : succès en CI après correction ciblée des contrastes ; captures comparatives accueil, auteur et article aux largeurs 390, 768 et 1365 px dans l'artefact `browser-qa-artifacts`.
- Lighthouse CI : succès ; rapports conservés dans l'artefact `lighthouse-reports`.

## BLOQUÉ / RÉSERVES

- Les images privées sont des extractions DOCX, donc potentiellement recompressées.
- Leur provenance et leurs droits individuels ne sont pas validés pour publication.
- Le téléchargement de Chromium a été bloqué dans l'environnement Work. Les contrôles navigateur et captures publiques ont donc été exécutés par la CI GitHub, avec succès.
- Aucune capture contenant les photographies privées n'a été envoyée dans GitHub ou ses artefacts. La démonstration de ces images reste interactive et locale dans le paquet de revue Windows.

## VALIDATION HUMAINE

La réussite technique ne vaut pas validation artistique. Théodore doit examiner ensemble l'accueil, le portfolio, un article public et le parcours privé de la série bleue avant toute fusion.
