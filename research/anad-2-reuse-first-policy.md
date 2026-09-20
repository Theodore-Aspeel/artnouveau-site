# ANAD 2.0 — Politique REUSE FIRST pour outils, agents et composants

Date : 2026-09-20  
Statut : **VALIDÉ** par Théodore.  
Portée : tous les chantiers ANAD 2.0 nécessitant un outil, une bibliothèque, un agent, un workflow, un composant, un template, un pipeline ou une infrastructure réutilisable.

## 1. Principe

ANAD 2.0 adopte une doctrine **REUSE FIRST** :

> Avant de construire ou d'acheter un outil, rechercher d'abord ce qui existe déjà, en particulier dans les dépôts GitHub publics et les écosystèmes d'agents/skills/plugins pertinents.

Le projet ne doit pas recréer inutilement une bibliothèque, un agent, un workflow ou une infrastructure déjà disponible et suffisamment mature.

Le développement spécifique ANAD est réservé en priorité à ce qui constitue réellement le contexte ou la valeur propre du projet : corpus de Christophe, règles éditoriales, droits, gouvernance, workflow humain, intégration des formats, expérience du site et décisions métier.

## 2. Scan obligatoire avant nouveau développement significatif

Pour tout nouveau besoin non trivial, le pilotage effectue d'abord un scan proportionné couvrant, selon le cas :

1. plugins/connecteurs déjà disponibles dans ChatGPT ou Codex ;
2. skills/agents déjà disponibles ;
3. dépôts GitHub publics pertinents ;
4. bibliothèques/packages standards de l'écosystème concerné ;
5. templates, starters, exemples maintenus ou projets de référence ;
6. outils gratuits ou déjà inclus dans la stack ANAD.

Les recherches GitHub doivent favoriser notamment :
- dépôts fortement étoilés ou largement utilisés ;
- projets actifs et récemment maintenus ;
- releases récentes ;
- plusieurs contributeurs ou communauté active ;
- CI/tests présents ;
- documentation exploitable ;
- compatibilité avec notre stack et Windows lorsque pertinent ;
- architecture réutilisable ou intégrable sans migration disproportionnée.

Les stars, forks et téléchargements sont des **signaux de découverte et de maturité**, pas des garanties absolues de qualité.

## 3. Décision standard : REUSE / ADAPT / INSPIRE / BUILD

Chaque scan doit déboucher sur une recommandation claire :

- **REUSE** : utiliser directement l'outil, skill, bibliothèque ou template.
- **ADAPT** : intégrer une solution existante avec une couche ANAD limitée.
- **INSPIRE** : reprendre l'architecture, les patterns ou les idées, sans copier le code.
- **BUILD** : développer spécifiquement parce qu'aucune solution existante n'est suffisamment adaptée.

La décision **BUILD** doit être justifiée par un écart concret : besoin métier spécifique, incompatibilité, maintenance insuffisante, coût, sécurité, licence, complexité d'intégration ou absence de solution mature.

## 4. Critères d'évaluation rapides

Le scan ne doit pas devenir une étude interminable. Pour les candidats sérieux, vérifier au minimum :

- adéquation fonctionnelle ;
- popularité / adoption ;
- activité récente ;
- issues et maintenance ;
- tests / CI ;
- licence si du code doit être copié ou intégré ;
- sécurité et gestion des secrets lorsque pertinent ;
- coût et dépendances externes ;
- facilité d'installation et de retrait ;
- compatibilité avec GitHub, ChatGPT/Codex et la stack ANAD ;
- risque de lock-in ;
- niveau de personnalisation requis.

Une ambiguïté de licence ou de sécurité n'interdit pas d'**étudier** ou de **s'inspirer** d'un projet. Elle devient pertinente avant copie, intégration ou redistribution de code.

## 5. Domaines concernés

La règle s'applique notamment à :

- SEO technique, Search Console, schema, CWV, GEO/AEO ;
- design du site, composants UI, galeries, accessibilité, responsive ;
- traitement d'images et optimisation média ;
- Reels, montage vidéo, templates Remotion/FFmpeg/Resolve, animation photo ;
- pipelines éditoriaux et CMS léger ;
- automatisation sociale et reporting ;
- analytics, tests, QA, monitoring et drift ;
- génération de rapports ;
- crawling, scraping, recherche documentaire ;
- outils développeur, CI/CD et déploiement ;
- futurs besoins commerciaux ou de newsletter.

## 6. Rapport attendu avant mise en œuvre

Pour un chantier significatif, le pilotage fournit une courte fiche :

| Élément | Attendu |
| --- | --- |
| Besoin | Ce qu'ANAD cherche à résoudre |
| Candidats | 3–10 solutions pertinentes lorsque le marché le permet |
| Maturité | stars/forks/adoption, activité, releases |
| Fit ANAD | ce qui correspond / manque |
| Coût | gratuit, open source, payant, API éventuelle |
| Intégration | difficulté et dépendances |
| Risques | licence, sécurité, lock-in, maintenance |
| Décision | REUSE / ADAPT / INSPIRE / BUILD |
| Pourquoi | justification concise |

Il n'est pas nécessaire de retenir systématiquement le projet le plus populaire. Le but est d'éviter le développement maison par défaut et de prendre une décision informée.

## 7. Conséquences pour le pilotage

- Ne plus lancer automatiquement Codex/Work pour construire un outil dès qu'un besoin apparaît.
- Le pilotage central réalise d'abord le scan de réutilisation.
- Si un dépôt ou outil mature couvre déjà 70–90 % du besoin, privilégier l'intégration ou l'adaptation plutôt qu'une réécriture.
- Les lots spécifiques ANAD doivent rester petits et se concentrer sur l'intégration, les contrats et les tests propres au projet.
- Éviter les nouveaux abonnements payants lorsqu'une solution gratuite/open source mature existe.
- Toute nouvelle dépendance importante reste soumise aux validations humaines ordinaires.

## 8. Premier cas de référence

Le dépôt `AgriciDaniel/claude-seo` a montré qu'un ensemble mature d'agents et de workflows SEO existait déjà, avec un port Codex séparé. Ce cas motive la formalisation de la présente règle.

Il ne constitue pas automatiquement une décision d'installation. Le traitement du SEO ANAD devra comparer l'existant du projet avec ces suites et d'autres candidats avant toute extension importante du tooling SEO.

## 9. Application immédiate

À partir de cette décision, tout nouveau chantier technique ou outillage majeur ANAD commence par :

`BESOIN → REUSE SCAN → REUSE / ADAPT / INSPIRE / BUILD → VALIDATION → EXÉCUTION`

Cette séquence devient la règle par défaut du projet.
