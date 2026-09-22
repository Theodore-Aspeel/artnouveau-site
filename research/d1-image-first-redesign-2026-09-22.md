# ANAD 2.0 - D1 direction image-first

Date : 2026-09-22  
Statut : **EN COURS - implémentation locale réalisée, validation navigateur/CI et revue humaine attendues**  
Branche : `anad-2.0/d1-image-first`  
Base technique : PR #43, commit `9f725dc97099503f8d46df82648f104ec6667b81`

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
- Export Drive : 12 images incorporées récupérables et mappées aux douze libellés.
- Frontière de confidentialité : `.private-media/` ignoré ; `dist/private/` produit uniquement avec `PRIVATE_PREVIEW=1`.

## BLOQUÉ / RÉSERVES

- Les images privées sont des extractions DOCX, donc potentiellement recompressées.
- Leur provenance et leurs droits individuels ne sont pas validés pour publication.
- Le navigateur Chromium local n'a pas pu être téléchargé dans l'environnement Work ; les captures publiques et les contrôles navigateur doivent donc être produits par la CI GitHub. Les captures privées restent à produire dans le paquet local, hors CI.

## VALIDATION HUMAINE

La réussite technique ne vaut pas validation artistique. Théodore doit examiner ensemble l'accueil, le portfolio, un article public et le parcours privé de la série bleue avant toute fusion.

