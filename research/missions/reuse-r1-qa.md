# ANAD 2.0 — Mission R1 : QA standardisée par réutilisation

Statut : **PROPOSÉ — prêt pour exécution Codex après validation du pilotage.**

## Objectif

Ajouter une première couche QA standard fondée sur des briques éprouvées, sans modifier l'architecture du site :

- Playwright pour navigateur / responsive / captures ;
- axe-core via Playwright pour accessibilité ;
- Lighthouse CI pour performance / SEO / best practices.

Ne pas intégrer Unlighthouse dans la CI principale : la version actuelle exige Node >=22.18.0 alors qu'ANAD est volontairement sur Node 20.

## Avant modification

Lire :
- `AGENTS.md`
- `research/ANAD-PROJECT-STATE.md`
- `research/anad-2-reuse-first-policy.md`
- `research/anad-2-reuse-landscape-2026-09-20.md`
- `research/anad-2-reuse-adoption-plan-2026-10-05.md`
- `research/anad-2-baseline-audit.md`

Travailler sur une branche dédiée :
`anad-2.0/reuse-r1-qa`

Ne jamais travailler directement sur `main`.

## Briques à réutiliser

Candidats validés par le benchmark :
- `@playwright/test`
- `@axe-core/playwright`
- `@lhci/cli`

Ne pas écrire de moteur de screenshot, d'audit accessibilité ou de score Lighthouse maison.

## Contraintes

- conserver Node 20 ;
- conserver vanilla HTML/CSS/JS ;
- pas de migration framework ;
- pas de changement éditorial ou graphique opportuniste ;
- aucun statut d'article modifié ;
- Maison Coilliot reste `draft` et `noindex,follow` ;
- pas de publication ;
- pas de service payant ;
- ne pas toucher à Plausible/GA4 ;
- préserver les workflows CI existants.

## Serveur de test existant

Réutiliser `npm run preview` / `scripts/preview.mjs`.

Ce serveur :
- construit `dist/` ;
- sert l'artefact sur le port 4173 par défaut ;
- sait servir les routes de répertoire avec `index.html`.

Ne pas ajouter un second serveur local sauf impossibilité démontrée.

## Couverture Playwright minimale

Créer une suite courte mais utile.

Viewports :
- mobile : 390 px ;
- tablette : 768 px ;
- desktop : environ 1365 px.

Pages minimales :
- accueil FR ;
- accueil EN ou NL pour vérifier le multilingue ;
- Maison Coilliot FR ;
- about FR.

Vérifier au minimum :
- HTTP/rendu correct ;
- absence de débordement horizontal ;
- navigation principale visible/utilisable ;
- menu mobile si applicable ;
- H1 visible après rendu client ;
- hero/image principale présente sur Coilliot ;
- canonical cohérent ;
- Coilliot conserve `noindex,follow` ;
- page statique publique conserve `index,follow`.

Ne pas créer des centaines d'assertions fragiles.

## Accessibilité axe-core

Sur un petit échantillon représentatif :
- accueil FR ;
- Maison Coilliot ;
- about.

Exécuter axe après rendu.

Gate initial :
- aucune violation `critical` ou `serious`.

Les violations modérées peuvent être rapportées sans forcément bloquer le premier lot si elles sont documentées.

Ne pas remplacer la revue humaine du design par axe.

## Régression visuelle

Utiliser les primitives Playwright `toHaveScreenshot` uniquement sur quelques vues stables si les snapshots sont suffisamment déterministes dans GitHub Actions.

Minimum candidat :
- accueil 390 ;
- accueil desktop ;
- Coilliot 390 ;
- Coilliot desktop.

Si les polices externes ou le rendu GitHub Actions rendent les snapshots instables :
- le documenter ;
- privilégier les screenshots comme artefacts/revue plutôt qu'un gate pixel-perfect fragile.

Ne pas ajouter BackstopJS en parallèle.

## Lighthouse CI

Ajouter une configuration simple contre le preview local.

Auditer au minimum :
- homepage FR ;
- page about FR.

Ne pas auditer Coilliot comme page SEO indexable tant qu'elle reste `draft/noindex`.

Seuils initiaux :
- utiliser les recommandations Lighthouse pour erreurs évidentes ;
- définir des seuils prudents pour éviter les régressions ;
- ne pas inventer une exigence arbitraire de 100/100.

Le premier lot doit surtout capturer une baseline reproductible.

## CI

Ajouter des jobs ou étapes clairement séparés des tests métier existants.

La CI existante doit continuer de vérifier :
- qualité ;
- profil GitHub Pages ;
- filtre publication.

Le nouveau navigateur/QA peut être séparé pour que les échecs soient lisibles.

Installer Chromium Playwright dans la CI selon la méthode officielle.

## Scripts package.json

Ajouter des commandes explicites, par exemple :
- `test:e2e`
- `test:a11y` si séparé ;
- `test:lighthouse`
- éventuellement `qa:web`

Éviter de transformer `npm run quality` en une commande très lente avant d'avoir mesuré le coût CI.

## Livrable

Fournir :
- branche ;
- commit(s) ;
- PR brouillon ;
- fichiers modifiés ;
- dépendances ajoutées et versions ;
- temps approximatif des nouveaux jobs ;
- résultats de :
  - `npm run validate`
  - `npm run rights:check`
  - `npm run build`
  - tests Node
  - tests Python
  - Playwright
  - axe
  - Lighthouse CI
- captures utiles si produites ;
- anomalies découvertes, séparées des corrections réellement faites.

## Important

Ce lot est un **lot d'intégration de briques existantes**, pas une refonte QA.

Si une brique impose une complexité disproportionnée :
- ne pas réimplémenter soi-même ;
- documenter le problème ;
- revenir au pilotage avec une alternative REUSE FIRST.

Ne pas merger sans retour au pilotage central.
