# ANAD 2.0 — Mission d'orchestration D1 : pilote non publiable

Date : 2026-09-21. **VALIDÉ pour préparation du pilote**, mais **NON DÉMARRÉ** pour l'exécution Work/Codex. Source de vérité : GitHub main, registre central D12. L'architecture GitHub + Work/Codex est validée ; **tester effectivement BMAD officiel** dans un environnement D1 isolé, sans présumer que les procédures ANAD maison sont supérieures. Les permissions techniques ont été élargies à la demande de Théodore ; aucune diffusion éditoriale ni dépense n'est incluse.

## But et limites

Démontrer que Work peut coordonner, dans les limites réelles de ses outils, un dossier D1 de bout en bout avec le minimum de transferts humains ; Codex ne sera mandaté que pour des modifications isolées nécessaires. Ne pas prétendre que Work et Codex sont déjà automatiquement intégrés ; si une frontière exige un transfert, en faire la preuve et le comptabiliser.

**D1 seulement** : deux variantes visuellement distinctes et navigables de la présentation de Christophe Aspel auteur-photographe et du chemin bâtiment → photographies → article → auteur/contact. Conserver HTML/CSS/JS vanilla, FR/EN/NL, identité éditoriale et photos originales. Coilliot reste draft/noindex, uniquement exemple technique si nécessaire. Ne pas lancer C1, Reel, nouveau CMS, Search Console ou analytics dans ce pilote.

## Initialisation à l'exécution

1. Lire sur **main** AGENTS.md, research/ANAD-PROJECT-STATE.md, research/anad-2-execution-reset-2026-09-21.md, research/anad-2-reuse-first-policy.md ; lire research/anad-orchestration-state.yaml seulement **après intégration sur main**, sinon lire l'exemplaire de branche et le signaler.
2. Capturer HEAD(main) au moment de commencer comme source_commit effectif du pilote, sans confondre ce nouveau commit avec le snapshot de préparation. Les deux variantes doivent partir du même source_commit effectif.
3. Vérifier quelles tâches Work/Codex et connexions sont effectivement disponibles ; ne pas inventer d'agent persistant ni d'accès à des cookies/identifiants Instagram. Si deux environnements Codex indépendants ne sont pas disponibles, proposer une exécution isolée alternative sans demander à Théodore de copier manuellement les mêmes fichiers.
4. Vérifier la documentation officielle actuelle BMAD-METHOD et les prérequis, puis **installer/exécuter ses skills/workflows officiels UX / build / review dans un environnement isolé de pilote**, si l'outil d'exécution le permet. Employer sa procédure d'intégration d'un projet existant ; lire nos décisions validées sans générer de constitution/roadmap concurrentes. Une installation ciblée dans ce sandbox est autorisée ; ne pas installer globalement, ajouter de dépendance au site ou activer des modules payants. Si Work/Codex ne permet pas d'appeler BMAD directement, décrire la limitation vérifiée et donner le chemin le plus court, sans prétendre que des agents ont réellement tourné.
5. Comparer la démarche BMAD réellement exécutée et la démarche native sur les mêmes critères (reprises de contexte, transferts humains, vérifications, livrables, qualité visuelle, temps actif). **Ne pas doubler mécaniquement toute la production A/B** : BMAD peut coordonner les deux variantes et les outils QA natifs vérifier les résultats. Le succès de BMAD ne se déduit pas du nombre d'étoiles, et la supériorité des composants ANAD maison n'est pas supposée.

## Livrables

- Captures de la baseline à 390 px, 768 px et desktop.
- Variante A et B **navigables**, issues du même commit de départ et clairement séparées ; captures aux mêmes trois largeurs. Utiliser des prévisualisations non indexables avec des médias déjà autorisés, ou des artefacts locaux si une PR déclenche une preview accessible au public contenant des contenus non approuvés.
- Matrice A/B de 1 page maximum, parcours photo/auteur/contact, écarts et limites.
- Faits et actifs à confirmer par Christophe : ne pas inventer de biographie, portfolio, référence, moyen de contact professionnel ou droits.
- Tests existants : npm run validate, npm run build, npm run qa:web, npm run rights:check quand un asset est modifié ; noter résultats et erreurs exacts. Comparer la performance de l'accueil sans transformer un score Lighthouse arbitraire en blocage de livraison.
- Inventaire des fichiers touchés, liens de branches / PR draft et URL de previews de test si leur exposition est compatible avec les droits et le statut du contenu ; sinon artefacts locaux ; SHA des variantes et preuve d'exécution de BMAD (skill/workflow/version, sorties et limites).
- Journal : transferts manuels, relances sur contexte déjà écrit, décisions humaines légitimes, temps humain actif, temps écoulé, consommation Work/Codex si visible.
- Reprise : si le système le permet, créer un checkpoint contenant les **références vérifiables** aux deux variantes et aux sorties ; vérifier qu'un nouveau contexte peut retrouver les livrables depuis GitHub/checkpoint sans reconstitution manuelle.

## Interdictions et gate

**Autorisé sans micro-validation** : créer des branches, y pousser des commits, lancer la CI et ouvrir des PR draft pour les deux variantes ; fusionner une PR purement documentaire ou de QA non éditoriale, bornée et verte, après revue technique, avec traçabilité dans le registre. Une PR peut déclencher une URL de preview publiquement accessible : vérifier son périmètre avant push et ne pas y mettre de nouveaux contenus/images non approuvés. **Interdit** : push direct sur main, fusion d'une variante D1 modifiant la présentation publique avant le choix groupé de Théodore, publication Instagram, passage d'article à published, dépense, contact externe, nouvelle connexion ou installation BMAD globale/dans le runtime du site. Les changements techniques mineurs déjà dans la portée validée peuvent être fusionnés après CI et revue s'ils ne modifient pas la direction artistique, les données publiques ni les droits. Une unique revue humaine A / B / aucune est attendue pour choisir la direction visuelle ; la diffusion éditoriale requiert une décision distincte.

Le checkpoint de préparation n'est pas un résultat d'exécution. Mettre D1 en EN COURS uniquement si le run a effectivement démarré, RÉALISÉ uniquement quand ses artefacts existent, VÉRIFIÉ uniquement après tests et revue appropriés.
