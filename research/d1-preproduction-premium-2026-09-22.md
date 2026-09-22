# D1 — reprise visuelle depuis la préproduction privée

Date : 2026-09-22  
Branche : `anad-2.0/d1-preproduction-premium`  
Statut : **RÉALISÉ techniquement, À VALIDER artistiquement**

## VALIDÉ

- GitHub reste la source de vérité ; aucune fusion ni publication n'est autorisée par ce lot.
- Les quatre sujets pilotes sont Maison Coilliot, Maison des Hiboux, Villino Florio et Maison des Médecins / Bastin.
- L'anglais reste la langue affichée par défaut ; FR, EN et NL sont conservés.
- Les dix JPEG C1 ne peuvent être utilisés que dans une revue locale privée.

## RÉALISÉ

- Recomposition de l'accueil en journal photographique sobre : hero carré respectant le cadrage du Villino Florio, hiérarchie bâtiment / ville / lecture, séquences asymétriques et espaces plus généreux.
- Suppression des formulations « Four Buildings », du grand crédit photographique redondant et du bloc technique de statut en fin de page.
- Présentation des corpus selon leur volume réel : 3 vues Coilliot, 2 vues Hiboux, 4 vues Villino utilisées sur l'accueil, 5 vues Bastin.
- Les dossiers non finalisés restent signalés comme « en préparation » et ne reçoivent aucun faux lien d'article.
- Réutilisation du mécanisme local de prévisualisation D1 : `.private-media/` est ignoré par Git ; `npm run preview:private` injecte les JPEG uniquement après le build public local.
- Aucun framework, service, média externe ou dépendance de production ajouté.

## VÉRIFIÉ

- Les fichiers privés ne sont ni suivis par Git, ni copiés par le build public, ni référencés par un attribut `src` public.
- Les dimensions et formats des dix copies Drive correspondent au manifeste de préproduction.
- `npm run validate`, build public, tests Node, tests Python et profil `published-only` exécutés localement.
- Le contrôle des droits publics reste à 23/23 ; un avertissement historique non bloquant subsiste pour un média enregistré mais inutilisé.

## BLOQUÉ / LIMITES

- Le navigateur Playwright local n'a pas pu être téléchargé dans l'environnement Work ; les captures et contrôles axe/Lighthouse doivent donc être confirmés par la CI GitHub déjà en place.
- Les copies Instagram limitent la taille d'affichage. Aucun hero panoramique plein écran n'est simulé et aucun agrandissement génératif n'est appliqué.
- Le lot ne crée pas les articles Villino Florio ou Maison Bastin et ne modifie aucun statut éditorial.

## À VALIDER HUMAINEMENT

- Qualité artistique de l'accueil sur desktop, tablette et mobile.
- Pertinence du Villino Florio comme ouverture et du rythme alternant façades et détails.
- Autorisation éventuelle d'étendre ultérieurement cette direction aux pages article et auteur.

Le succès de la CI ne constitue pas une validation artistique.
