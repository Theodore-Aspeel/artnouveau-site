# ANAD 2.0 — Mission d'orchestration D1 : pilote non publiable

Date : 2026-09-21. **VALIDÉ pour préparation du pilote**, mais **NON DÉMARRÉ** pour l'exécution Work/Codex. Source de vérité : GitHub main, registre central D12. L'architecture native-first avec adaptation ciblée de BMAD est validée par Théodore ; aucune installation BMAD complète.

## But et limites

Démontrer que Work peut coordonner, dans les limites réelles de ses outils, un dossier D1 de bout en bout avec le minimum de transferts humains ; Codex ne sera mandaté que pour des modifications isolées nécessaires. Ne pas prétendre que Work et Codex sont déjà automatiquement intégrés ; si une frontière exige un transfert, en faire la preuve et le comptabiliser.

**D1 seulement** : deux variantes visuellement distinctes et navigables de la présentation de Christophe Aspel auteur-photographe et du chemin bâtiment → photographies → article → auteur/contact. Conserver HTML/CSS/JS vanilla, FR/EN/NL, identité éditoriale et photos originales. Coilliot reste draft/noindex, uniquement exemple technique si nécessaire. Ne pas lancer C1, Reel, nouveau CMS, Search Console ou analytics dans ce pilote.

## Initialisation à l'exécution

1. Lire sur **main** AGENTS.md, research/ANAD-PROJECT-STATE.md, research/anad-2-execution-reset-2026-09-21.md, research/anad-2-reuse-first-policy.md ; lire research/anad-orchestration-state.yaml seulement **après intégration sur main**, sinon lire l'exemplaire de branche et le signaler.
2. Capturer HEAD(main) au moment de commencer comme source_commit effectif du pilote, sans confondre ce nouveau commit avec le snapshot de préparation. Les deux variantes doivent partir du même source_commit effectif.
3. Vérifier quelles tâches Work/Codex et connexions sont effectivement disponibles ; ne pas inventer d'agent persistant ni d'accès à des cookies/identifiants Instagram. Si deux environnements Codex indépendants ne sont pas disponibles, proposer une exécution isolée alternative sans demander à Théodore de copier manuellement les mêmes fichiers.
4. Réutiliser les patterns BMAD de discovery/UX/spec/review **comme méthode**, sans installer tout BMAD ni ajouter de dépendances.

## Livrables

- Captures de la baseline à 390 px, 768 px et desktop.
- Variante A et B **navigables en privé**, issues du même commit de départ et clairement séparées ; captures aux mêmes trois largeurs.
- Matrice A/B de 1 page maximum, parcours photo/auteur/contact, écarts et limites.
- Faits et actifs à confirmer par Christophe : ne pas inventer de biographie, portfolio, référence, moyen de contact professionnel ou droits.
- Tests existants : npm run validate, npm run build, npm run qa:web, npm run rights:check quand un asset est modifié ; noter résultats et erreurs exacts. Comparer la performance de l'accueil sans transformer un score Lighthouse arbitraire en blocage de livraison.
- Inventaire des fichiers touchés, URL de previews *uniquement si privées/non indexables et autorisées*, sinon artefacts locaux ; SHA/branches des variantes si disponibles.
- Journal : transferts manuels, relances sur contexte déjà écrit, décisions humaines légitimes, temps humain actif, temps écoulé, consommation Work/Codex si visible.
- Reprise : si le système le permet, créer un checkpoint contenant les **références vérifiables** aux deux variantes et aux sorties ; vérifier qu'un nouveau contexte peut retrouver les livrables depuis GitHub/checkpoint sans reconstitution manuelle.

## Interdictions et gate

Pas de modification de main, fusion, publication Instagram/site, changement des statuts d'articles, création d'assets publics hors validation, dépense, contact externe, nouvelle connexion ou installation complète BMAD. **Ne pas créer de PR de choix visuel avant la revue groupée**. Une unique revue humaine A / B / aucune et des corrections groupées est attendue ; décision de publication éventuelle entièrement séparée.

Le checkpoint de préparation n'est pas un résultat d'exécution. Mettre D1 en EN COURS uniquement si le run a effectivement démarré, RÉALISÉ uniquement quand ses artefacts existent, VÉRIFIÉ uniquement après tests et revue appropriés.
