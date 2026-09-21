# ANAD 2.0 — Exécution recentrée : système répétable et expérience du site

Date : 2026-09-21. Statut : **VALIDÉ — réorientation de priorité par Théodore** ; les travaux proposés ci-dessous ne sont ni implémentés ni autorisés à être publiés.

## Décision de pilotage qui remplace l'ancien chemin critique

Ne plus faire de la publication immédiate de Maison Coilliot ni du 5 octobre une dépendance bloquante. La priorité est un **système éditorial réutilisable** partant des photographies et publications Instagram existantes, produisant un dossier documentaire et une expérience de site soignée, puis des formats sociaux reproductibles. Coilliot est un article techniquement finalisé et conservé en `draft/noindex` ; il pourra servir de jeu de test non publiable, sans rouvrir son contenu en boucle. Aucun Reel Coilliot obligatoire.

L'échéance du 5 octobre reste un **repère de préparation, non un quota d'heures quotidiennes ni une date de diffusion**. Ne pas supposer que Théodore peut consacrer 12 h/jour à l'exécution ou aux validations. Réduire son intervention à des revues groupées de livrables visuels/décisions, pas des micro-gates.

## État réel et interfaces disponibles

- **VÉRIFIÉ** : QA Playwright + axe-core + Lighthouse CI installée (PR #33) ; Sharp déjà utilisé. Résultat QA R1 : couverture échantillonnée verte, performance Lighthouse de l'accueil FR 58 au dernier relevé, page About FR 92 ; plusieurs problèmes non critiques et alertes transitives restent ouverts. QA n'équivaut pas à une refonte UX terminée.
- **VÉRIFIÉ** : page actuelle `src/pages/about.html` : présentation éditoriale longue à la première personne, portrait dans `src/assets/images/site/author/author-portrait-2026.jpg`, Instagram comme contact principal ; identité professionnelle, rôle d'auteur-photographe, portfolio/collaborations/contact professionnel restent à concevoir avec Christophe, sans inventer sa biographie, ses références ni valider implicitement son portrait.
- **VÉRIFIÉ** : Metricool connecté à `@artnouveauetdeco`, marque 6978424. L'API `Instagram Posts` peut fournir dates, légendes, miniatures, liens, type, portée et enregistrements pour les publications renvoyées ; elle ne prouve pas à elle seule le nombre de photos originales d'un bâtiment et ne donne pas automatiquement le corpus HD. Sur la période 2026-05-01–2026-09-21, seulement deux posts sont renvoyés : monument au Maestro Serrano, Sueca (10-08-2026, image seule dans la réponse, https://www.instagram.com/p/Db3bdnXtBEh/) et Chiosco Ribaudo, Palerme (28-07-2026, image seule, https://www.instagram.com/p/DbU3Cw2KOZc/). **CANDIDATS de repérage, pas dossiers multi-vues validés.** Les périodes 2025-10–2026-04 interrogées n'ont pas renvoyé de lignes ; cela ne prouve pas l'absence de publications Instagram.
- **VÉRIFIÉ** : la recherche Canva « Art Nouveau » n'a renvoyé aucun design préexistant dans le compte connecté. Ne pas dire que des modèles Canva ANAD existent déjà.
- **VÉRIFIÉ** : aucune connexion disponible ne démontre ici l'accès à toute la photothèque Instagram, à tous les médias d'un carrousel ou aux originaux de Christophe. Il faut préciser le périmètre d'accès avant de bâtir un importeur ; ne pas scraper/connecter/dépenser par défaut.
- **VÉRIFIÉ** : Search Console validé, sitemap soumis et HTTP 200 / `application/xml` ; traitement Google en attente au dernier contrôle. Ce suivi reste non bloquant et ne justifie aucun nouveau lot SEO immédiat.

## Ligne de production cible — logique métier ANAD uniquement

`inventaire de publications existantes → regroupement par bâtiment et disponibilité des vues originales → choix de 2–3 dossiers source documentés → validation de la provenance et des droits → fiche article réutilisable FR/EN/NL → sélection photo/site → déclinaisons visuelles (post/carrousel ; Reel seulement si le corpus s'y prête) → tests navigateur/accessibilité/SEO → validation humaine groupée → éventuelle diffusion distinctement autorisée → mesure`.

Réutiliser les contrats existants `artnouveau.social_package@1`, `artnouveau.reel_pilot@1`, `artnouveau.pipeline_status@1`, l'Editorial Manager existant et GitHub comme source de vérité ; ne pas remplacer ces briques sans comparaison concrète.

## Lots d'exécution, dans cet ordre de valeur (deux pistes actives maximum)

### D1 — Site : identité Christophe + parcours photo (priorité immédiate, travail en parallèle de C1)

**PROPOSÉ :** audit du site actuel et des 3 langues sur prévisualisations Playwright, puis **deux variantes visuelles concrètes** de la page auteur/portfolio et de la navigation « découvrir un bâtiment → images → article → auteur/contact ». Présentation explicite de Christophe Aspel comme auteur-photographe ; origine de ses photos, crédits, contact professionnel et références uniquement après preuve/validation. Conserver la photographie originale, le cadre ivoire/encre/bronze, la hiérarchie éditoriale et la stack vanilla. Reprendre des patterns et composants éprouvés ; ne pas installer un framework entier pour faire une page.

Briques candidates **à tester**, non adoptées : PhotoSwipe (galerie/lightbox responsive), medium-zoom (simple zoom photo), Open Props (tokens ciblés) ; ne pas cumuler PhotoSwipe et medium-zoom pour la même fonction. Faire un diagnostic de fit sur le site actuel avant toute dépendance. Le repo Shoelace historique est archivé ; ne pas l'adopter sur la seule base du benchmark 20-09. Les bibliothèques de design sont des moyens, pas la direction artistique.

**Livrables :** captures 390/768/desktop de l'état initial + deux variantes visuelles navigables en preview non publiées ; matrice de différence à 1 page ; liste des informations/visuels exacts restant à valider par Christophe ; une seule proposition de PR d'implémentation après choix visuel. Ne pas toucher aux 14 statuts.

### C1 — Inventaire Instagram et choix des dossiers source (en parallèle de D1)

**PROPOSÉ :** utiliser d'abord les métadonnées/légendes/liens déjà disponibles via Metricool et les données GitHub ; produire un tableau de publications groupées par bâtiment, URLs de post, nombre de vues **confirmées / inconnu**, présence d'originaux HD **confirmée / inconnue**, sujets déjà couverts par les 14 articles et autres candidats. Construire la première shortlist de 3 sujets **si les preuves le permettent**, sinon expliciter le manque sans inventer.

Pour accéder à tout le feed et aux carrousels, vérifier si le compte Instagram peut être parcouru dans Work connecté avec session autorisée ou par export officiel fourni par le propriétaire ; demander une seule action d'accès si nécessaire. Ne pas confondre `post IG`, `miniature IG`, `carrousel complet` et `photographies natives réutilisables`. Pas de scraping avec identifiants ni d'import forcé.

**Livrable :** 3 dossiers-candidats documentés ou blocage précis d'accès ; une carte « sources / droits / photos natives / disponibilité multi-angle » par sujet. Aucun article ni photo inventés.

### M1 — Ateliers de formats réutilisables, une fois D1/C1 amorcés

**PROPOSÉ :** choisir un dossier photo vérifié et préparer **une maquette de carrousel reproductible** + **un test privé de Reel court** (9:16, photographie-first) à partir de sources autorisées. Explorer d'abord les Agent Skills/templates officiels de Remotion et FFmpeg/DaVinci existants, sans refaire de moteur ni générer de façade architecturale fantaisiste. Vérifier les conditions exactes de licence et de rendu avant d'intégrer Remotion. Aucun Reel n'est une condition pour générer un article ; les formats sont des modules interchangeables.

**Livrable :** template paramétré ou prototype reproductible avec sources, durée, sous-titres si utiles, remplacements d'images sans coder un second film ; fichier local téléchargeable/artefact CI, non posté sur Instagram.

### P1 — Relier les modules pour un dossier nouveau, AVANT toute publication

**PROPOSÉ :** comparer l'éditeur existant à Pages CMS pour l'édition réelle de JSON multilingue/médias et l'enchaînement PR ; n'introduire ni Next/PostgreSQL ni migration tant que l'avantage n'est pas démontré. Comparer Metricool actuellement connecté et Postiz uniquement sur fonctions réellement manquantes ; n'installer aucun second scheduler pour l'apparence. Faire passer **un nouveau dossier source** par la chaîne interne `sources → article draft → médias → formats sociaux → preview → QA`. Le statut `draft` reste inchangé jusqu'à autorisation explicite.

**Livrable :** démonstration interne reproductible sur un sujet source authentique et checklist simple « entrée = originaux/sources, sortie = site + carrousel + Reel facultatif », temps humain mesuré ; pas de diffusion obligatoire.

## Discipline de vitesse

- Deux pistes actives maximum, **D1 et C1 maintenant** ; M1 à l'issue de leur première sortie, P1 après preuve des modules. Pas de nouvelle recherche générale sur tous les outils.
- Réutiliser le benchmark `research/anad-2-reuse-landscape-2026-09-20.md` comme **index de candidats**, pas comme liste d'installations autorisées.
- Les agents spécialisés disposent d'une mission bornée et produisent preview/PR/rapport d'écart ; pas une nouvelle roadmap autonome. Remonter architecture, périmètre et coût au pilotage central.
- **Budget d'attention humain :** une revue groupée par lot, avec liens et captures, 2–3 choix explicites maximum, durée visée 15–30 min par revue. Les 5 octobre et 90 jours restent des jalons de planification, pas une injonction à travailler tous les jours.
- Ne pas revenir au cycle Coilliot, au sitemap ou à l'analytics comme « prochain blocage » tant qu'une nouvelle anomalie avérée n'empêche pas D1/C1.
- Aucune publication, prospection, dépense, changement global d'architecture ni exposition publique de nouveaux médias sans feu vert humain spécifique.

## Prochain geste exécutif

**Commencer immédiatement D1 et C1 en parallèle**, avec livrables tangibles : previews comparables du site/auteur et shortlist source Instagram. Leur résultat déclenche M1 ; Coilliot peut rester un exemple déjà prêt, pas le sujet imposé de la chaîne répétable.
