# ANAD 2.0 — Registre central de l'état du projet

Dernière consolidation : 2026-09-20
Dépôt : `Theodore-Aspeel/artnouveau-site`
Référence du code public : `main`
Statut du présent registre : document de pilotage soumis à revue par PR ; les statuts ci-dessous ne valent pas approbation de publication.

## 1. Finalité et doctrine

ANAD 2.0 associe le travail photographique et éditorial de Christophe Aspel, un site patrimonial Art Nouveau / Art Déco en Europe et une audience Instagram existante (plus de 80 000 abonnés, chiffre communiqué par Théodore, à confirmer par les statistiques du compte). Théodore pilote les dimensions techniques, stratégiques et opérationnelles.

Objectif de long terme : un écosystème éditorial, communautaire et commercial cohérent, où Instagram crée la découverte, le site conserve la connaissance et les contenus peuvent susciter des relations avec des événements, institutions, partenaires et, ultérieurement, des revenus. La confiance, l'élégance et la fidélité patrimoniale priment sur la quantité de contenu et la monétisation agressive.

**Principe de séquence : prouver le cycle complet avant de multiplier les articles ou les Reels**. La stratégie commerciale et les instruments de mesure doivent être conçus dès maintenant ; les premières activations et dépenses sont conditionnées aux résultats et aux autorisations humaines, et non à un objectif de volume.

## 2. Gouvernance et statuts

- **GitHub** est la source de vérité pour le code, les décisions approuvées, les contrats, les ressources de production validées et les preuves d'implémentation. Une copie ajoutée aux sources du projet ChatGPT est une copie datée, non synchronisée automatiquement.
- **Discussion centrale en chat normal** : priorités, arbitrages et coordination interdomaines. Discussions spécialisées en chat normal : recherche, spécifications, audit et préparation des livrables. **Work/Codex** : interventions bornées nécessitant une exécution agentique ou du développement ; éviter d'y répéter les recherches déjà documentées.
- Christophe : auteur et photographe ; approbation artistique, éditoriale et documentaire des contenus le concernant. Théodore : arbitrage opérationnel, technique, budget et publication selon le processus convenu. Le niveau de contrôle humain est proportionné aux enjeux : ne pas demander une approbation à chaque micro-opération automatique ; exiger un contrôle avant diffusion publique, dépense, partenariat ou représentation patrimoniale incertaine.
- Aucune publication, dépense, prise de contact externe ou engagement commercial sans validation humaine explicite. Des brouillons, listes de prospects et prévisualisations peuvent être préparés sans envoi.
- Statuts uniques : **PROPOSÉ** (hypothèse), **VALIDÉ** (décision ou ressource approuvée), **EN COURS** (travail entrepris), **RÉALISÉ** (livrable existant et traçable), **VÉRIFIÉ** (contrôles appropriés effectués), **BLOQUÉ** (dépendance manquante). Ne pas déduire « réalisé » de « spécifié ».
- Pas de migration CMS/framework, base de données supplémentaire, abonnement, infrastructure cloud ou développement hors périmètre sans justification documentée et approbation.

## 3. État documenté par chantier

| Chantier | État au 20-09-2026 | Référence / prochain verrou |
| --- | --- | --- |
| Site et fondations | **RÉALISÉ** : site statique multilingue, construction déterministe, GitHub Pages, validations/CI et prévisualisations PR Netlify documentés. Qualité mobile réelle : contrôle humain à maintenir. | `research/anad-2-recovery-state.md`, `research/anad-2-preview-decision.md`, `research/anad-2-mobile-editorial-pilot.md`. Le présent registre n'atteste pas d'un nouveau test de rendu ou de déploiement. |
| Corpus éditorial | **RÉALISÉ** : 14 articles v2 et contrats de contrôle éditorial/documentaire dans la baseline documentée. **BLOQUÉ pour généralisation** : validation humaine article par article, exception Charleroi, transition prudente des statuts. Les articles `draft` conservent temporairement la visibilité historique ; le mode strict `published-only` ne doit pas être activé globalement sans préparation. | `research/anad-2-publication-readiness.md`, `research/publication-gate-flow.md`. |
| Maison Coilliot — article | **EN COURS** : contrôles éditoriaux, FR/EN/NL et droits rapportés comme prêts par le pipeline, mais décision de publication non acquise. Deux images complémentaires montrent d'autres bâtiments lillois : éviter de les laisser passer pour des vues de Coilliot ; trancher leur présentation ou remplacement. | `research/pipeline-status-contract.md`, `research/pilots/maison-coilliot-fact-review.md`. Contrôle final de Christophe, cadrage, date, dry run et autorisation avant publication. |
| Outil éditorial et automatisation | **RÉALISÉ** : gestionnaire éditorial et contrats de transmission `artnouveau.social_package@1`, `artnouveau.reel_pilot@1`, `artnouveau.pipeline_status@1` ; suivi du parcours éditorial documenté et PR récentes fusionnées. **NON RÉALISÉ** : rendu Reel, publication Instagram automatique, boucle intégrée de performances. | `research/social-automation-handoff.md`, `research/reel-pilot-contract.md`, `research/pipeline-status-contract.md`. |
| Reels illustrés | **EN COURS — préparation graphique**. Charte illustrée validée ; master ivoire V2 candidat, gros plan enseigne candidat. Raccord géométrique, inscriptions et résolution encore à contrôler. Version à ciel bleu régénérée écartée comme master spatial. **PROPOSÉ** : spike Remotion 2,5D déterministe de cinq secondes, puis moteur standard (master unique) / enrichi (plaque raccordée). **NON RÉALISÉ** : moteur, Reel final publiable, distribution. | Finir contrôle et validation du package Coilliot ; ensuite seulement spike Codex borné. Aucune vidéo IA payante obligatoire. Les précédents diaporamas n'ont pas été acceptés comme format cible. |
| SEO / connaissance | **RÉALISÉ** : fondations canoniques/hreflang/sitemap et JSON-LD Article/Place de base documenté. **À VÉRIFIER** : propriétés Search Console, indexation et mesures réelles ; liens internes, entités villes/architectes/mouvements et nouveaux formats de découverte restent à concevoir selon les données. | `research/anad-2-baseline-audit.md`, `research/anad-2-roadmap-90-days.md`. |
| Instagram et distribution | Audience existante déclarée, mais autorisations du compte, capacité de publication, outil de statistiques et métriques historiques **À VÉRIFIER**. Aucun automatisme de diffusion approuvé. | Mesurer la base actuelle avant le premier contenu expérimental ; conserver les originaux photographiques dans le carrousel et sur le site. |
| Mesure / apprentissage | **PROPOSÉ**, pas encore une boucle opérationnelle vérifiée. | Établir le relevé initial, le suivi des publications et une revue des résultats au lieu d'écrire cinq Reels ou quinze articles sans retour mesuré. |
| Partenariats / revenus | **PROPOSÉ** : stratégie et modèle d'offres à étudier dès maintenant ; prospection externe, événements, produits et monétisation non activés sans accord. | Étudier événements Art Nouveau / Art Déco, invitations presse/créateur, collaborations patrimoniales, puis éventuellement guides urbains/parcours, partenariats transparents ou produits adaptés. |

## 4. Priorités et dépendances actuelles

**P0 — Immédiat (prochains jours) :** clôturer l'audit du raccord master V2 / enseigne Coilliot, puis produire un **unique** spike Remotion de 5 s si le package graphique est approuvé. Seul le résultat visuel et documentaire autorisera le lot de développement suivant. La préparation de ce prototype ne vaut pas autorisation de publication de l'article ou du Reel.

**P1 — En parallèle, hors Work si possible :** concevoir le **cycle de mesure minimal avant diffusion** : état initial du compte Instagram et du site, accès autorisés aux données existantes, définition de quelques indicateurs, liens traçables, modèle de relevé et règle de bilan après chaque publication. Ne pas construire une plateforme d'analytics avant d'avoir exploité les outils déjà disponibles.

**P2 — Dès le prototype audiovisuel évalué :** concevoir et documenter un **hub stratégique commercial/marketing/SEO**, en commençant par une recherche externe ciblée et datée (créateurs patrimoniaux, médias culturels, institutions, offices de tourisme, festivals et événements, propositions de valeur, pratiques de partenariats, attentes des publics, modèles de guides). Distinguer faits sourcés, hypothèses et opportunités à tester. Un hub désigne d'abord des processus et documents raccordés aux données existantes, pas un nouveau logiciel payant. Préparer une courte liste de partenaires potentiels, des scénarios d'approche et une première proposition de valeur ; aucun message envoyé sans validation.

**P3 — Ensuite :** corriger les points prioritaires du site, finaliser le pilote éditorial Maison Coilliot et organiser une première publication/article-carrousel-Reel approuvée **avec suivi**. Les corrections bloquant la lisibilité, l'identité du bâtiment, la conformité ou la mesure passent avant les corrections purement cosmétiques. Les décisions de publication restent distinctes du prototype technique.

**P4 — Boucle complète, avant changement d'échelle :** analyser une première campagne et ses enseignements, puis tester la reproductibilité du moteur sur un deuxième bâtiment. Améliorer uniquement ce que les observations justifient. Envisager ultérieurement des revenus, des offres payantes ou une hausse d'abonnement selon les résultats, les coûts et la charge de travail.

Les dates de la roadmap 90 jours restent des objectifs de planification, non des autorisations. Les nouvelles priorités ci-dessus doivent être réconciliées avec `research/anad-2-roadmap-90-days.md` et `research/anad-2-orchestration.md` dans un lot documentaire ciblé, sans supprimer leur historique.

## 5. Cycle de bout en bout à démontrer

`Photographies / sujet documenté → audit des faits et des droits → article ou page utile → création visuelle approuvée → Reel illustré + carrousel photographique → validation humaine → distribution → visite du site / réaction → mesure → apprentissage → prochain contenu ou proposition de partenariat`

Chaque campagne pilote doit préciser **avant** sa diffusion : audience cible et objectif, contenu, canal, appel à l'action, destination, métriques accessibles, coût en temps et budget, date de revue et conditions de poursuite/arrêt.

Métriques candidates à confirmer selon accès réels :
- Instagram : portée et vues, rétention lorsque disponible, durée moyenne, partages, sauvegardes, interactions utiles, visites du profil, nouveaux abonnés.
- Site : pages indexées, impressions/clics et requêtes Search Console, sessions ou visites par source lorsque mesurables, visites des articles depuis Instagram via liens traçables.
- Partenariats : contacts pertinents identifiés, messages approuvés et envoyés, réponses, invitations, collaborations réalisées.
- Économie : temps humain par article/Reel, coûts réels, éventuelles recettes et retombées non financières.

Les statistiques d'un Reel et les conversions vers le site ne sont pas entièrement attribuables entre elles sans données pertinentes ; noter les limites au lieu d'inventer une causalité. Ne définir des objectifs chiffrés qu'après un relevé de référence.

## 6. Décisions centrales à préserver

- **D01 VALIDÉ** — GitHub reste la source de vérité. Une seule discussion normale pilote les priorités globales ; Work/Codex exécutent des lots bornés.
- **D02 VALIDÉ** — Priorité immédiate au prototype Reel Coilliot ; corrections non bloquantes du site ensuite. Stratégie, mesure et modèle commercial doivent être pensés **avant** la multiplication des productions ; revenus progressifs plutôt qu'une monétisation agressive immédiate.
- **D03 VALIDÉ** — Illustrations animées pour le Reel pilote ; photographies originales pour carrousel et site ; fidélité architecturale et approbation artistique indispensables.
- **D04 VALIDÉ COMME HYPOTHÈSE TECHNIQUE** — Remotion 2,5D déterministe, modes standard/enrichi, pas de générateur IA vidéo payant requis ; prototype de 5 s avant moteur complet.
- **D05 VALIDÉ** — Budget additionnel nul pour le prototype ; aucune dépense, publication ou prospection envoyée sans feu vert humain.
- **D06 VALIDÉ** — Christophe et Théodore interviennent aux points de validation substantiels, pas sur chaque étape mécanique ; la qualité finale et l'autorisation de diffusion restent humaines.
- **D07 À METTRE À JOUR** — L'ancien document d'orchestration désigne Work comme chef d'orchestre ; pour limiter le quota, le pilotage courant est transféré au chat normal et au présent registre. L'ancienne roadmap décrit un Reel photographique ; le premier pilote utilise désormais des illustrations. Ces deux documents doivent être mis en cohérence sans réécrire l'historique.

## 7. Organisation des discussions et transmission

Ouvrir une discussion spécialisée uniquement lorsqu'un chantier devient actif : site/développement, outil éditorial, visuels/Reels, SEO et données, partenariats/marketing, etc. Ne pas multiplier les « cerveaux centraux ». Le registre suffit pour transmettre l'état partagé ; une discussion doit vérifier les fichiers courants lorsqu'elle réalise une tâche importante.

Compte rendu de fin de lot : domaine et date ; statut exact ; fait / non fait ; fichiers et liens ; vérifications ; décisions à valider ; blocage ; **une prochaine action**. Pour le code : branche, PR et tests. Pour les ressources graphiques : fichiers exacts et état de validation.

Ne pas recopier des spécifications volumineuses ici : conserver leurs documents spécialisés, avec leurs liens. Ne mettre à jour ce fichier que lorsqu'un jalon, un blocage, une priorité ou une décision transversale change.

## 8. Références de départ

- `AGENTS.md`
- `research/anad-2-recovery-state.md`
- `research/anad-2-orchestration.md`
- `research/anad-2-roadmap-90-days.md`
- `research/anad-2-publication-readiness.md`
- `research/anad-2-preview-decision.md`
- `research/pipeline-status-contract.md`
- `research/publication-gate-flow.md`
- `research/reel-pilot-contract.md`
- `research/social-automation-handoff.md`

Dernière revue : synthèse des documents GitHub accessibles au 2026-09-20 et décisions de pilotage confirmées par Théodore. Ce registre ne remplace pas un contrôle de la branche actuelle, du déploiement ni des données de compte externes.
