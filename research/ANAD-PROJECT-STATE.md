# ANAD 2.0 — Registre central de l'état du projet

Dernière consolidation : 2026-09-20
Dépôt : `Theodore-Aspeel/artnouveau-site`
Référence du code public : `main`
Statut du présent registre : VALIDÉ et intégré à `main` (PR #23) ; les statuts ci-dessous ne valent pas approbation de publication.

## 0. Mise à jour opérationnelle du 20-09-2026 (soir)

Cette mise à jour prévaut sur les lignes plus anciennes du présent fichier lorsqu'elles décrivent le même chantier.

- **Maison Coilliot — VÉRIFIÉ** : PR #25 fusionnée ; vraies photographies de Christophe intégrées ; anciennes vues d'autres bâtiments retirées ; gate visuel humain clos ; article maintenu en `draft`, aucune publication.
- **Mesure — EN COURS** : PR #26 fusionnée ; protocole T0/J+1/J+7/J+30 documenté. Metricool connecté. Plausible supporté par le code mais inactif en production ; GA4 non connecté.
- **Search Console — EN COURS, état vérifié au 21-09-2026** : propriété URL-prefix `https://theodore-aspeel.github.io/artnouveau-site/` validée et rattachée à GSC Wizard. Le sitemap a été SOUMIS le 21-09-2026 ; son état Google est encore `isPending=true`, tandis que l'interface montre « Impossible de récupérer le sitemap » et 0 URL découverte. La lecture publique par GSC Wizard extrait 9 URL statiques, sans brouillon. Audit live de ces 9 pages : HTTP 200, indexables, canonicals cohérents. **BLOQUÉ pour conclure à la lecture Google** : vérifier le détail GSC et l'en-tête HTTP Content-Type du sitemap ; ne pas attribuer prématurément la cause au MIME, au XML ou au délai de traitement. Ne pas resoumettre sans diagnostic.
- **Transmission — RÉALISÉE** : `research/ANAD-HANDOFF-2026-09-20.md` intégré comme archive historique via PR #28 ; l'ancienne PR #24 a été fermée comme remplacée.
- **Priorité immédiate P0** : terminer Search Console/mesure et installer la première couche REUSE FIRST de QA (Playwright + axe-core + Lighthouse CI), puis effectuer le dry run du premier cycle Coilliot. Le gate SEO des drafts est désormais réalisé.

- **QA R1 — RÉALISÉ et VÉRIFIÉ** : PR #33 fusionnée, GitHub Pages déployé ; Playwright, axe-core et Lighthouse CI intégrés, aucune publication éditoriale. **REUSE FIRST — VÉRIFIÉ / EN COURS** : politique fusionnée via PR #30 ; benchmark transversal fusionné via PR #31. Architecture d'adoption jusqu'au 05-10 : Playwright + axe-core + Lighthouse CI en première vague ; Unlighthouse séparé car Node >=22.18 ; Pages CMS en spike sans migration ; Remotion réévalué via ses Agent Skills/templates/WebMCP lorsqu'un Reel redevient utile.

## 1. Finalité et doctrine

ANAD 2.0 associe le travail photographique et éditorial de Christophe Aspel, un site patrimonial Art Nouveau / Art Déco en Europe et une audience Instagram existante de **75 722 abonnés mesurés au 19-09-2026** via les données disponibles du compte connecté. Théodore pilote les dimensions techniques, stratégiques et opérationnelles.

Objectif de long terme : un écosystème éditorial, communautaire et commercial cohérent, où Instagram crée la découverte, le site conserve la connaissance et les contenus peuvent susciter des relations avec des événements, institutions, partenaires et, ultérieurement, des revenus. La confiance, l'élégance et la fidélité patrimoniale priment sur la quantité de contenu et la monétisation agressive.

**Principe de séquence : prouver le cycle complet avant de multiplier les productions**. La photographie originale de Christophe est le socle éditorial et artistique. Un article et un carrousel peuvent avancer sans Reel ; les Reels deviennent des contenus ponctuels lorsqu'ils apportent une lecture temporelle, spatiale ou architecturale distincte. La stratégie commerciale et les instruments de mesure doivent être conçus dès maintenant ; les premières activations et dépenses restent conditionnées aux résultats et aux autorisations humaines, et non à un objectif de volume.

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
| Reels illustrés | **EN COURS — préparation graphique**. Charte illustrée validée ; master ivoire V2 candidat, gros plan enseigne candidat. Contrôle du 20-09 : raccord **REFUSÉ** pour la paire réellement testée (master local V2 864 × 1536 et gros plan généré 1122 × 1402) : divergences d'oculus, moulures et ornements. La dernière façade générée sur ivoire est une ressource distincte ; ne pas lui attribuer les résultats du test local. Résolution Full HD du rapprochement demandé insuffisante avec le seul master local. Version à ciel bleu régénérée écartée comme master spatial. **PROPOSÉ** : spike Remotion 2,5D déterministe de cinq secondes, puis moteur standard (master unique) / enrichi (plaque raccordée). **NON RÉALISÉ** : moteur, Reel final publiable, distribution. | **Prochaine décision** : définir un test technique du mode standard avec le master local réellement livré et un zoom limité compatible avec sa résolution ; ne pas utiliser le gros plan refusé. Le raccord enrichi exige une ressource géométriquement corrigée et une validation séparée ; pas de promesse de vidéo finale Full HD avec les ressources présentes. Aucune vidéo IA payante obligatoire. Les précédents diaporamas n'ont pas été acceptés comme format cible. |
| SEO / connaissance | **RÉALISÉ** : fondations canoniques/hreflang/sitemap et JSON-LD Article/Place de base documenté. **À VÉRIFIER** : propriétés Search Console, indexation et mesures réelles ; liens internes, entités villes/architectes/mouvements et nouveaux formats de découverte restent à concevoir selon les données. | `research/anad-2-baseline-audit.md`, `research/anad-2-roadmap-90-days.md`. |
| Instagram et distribution | **VÉRIFIÉ partiellement** : compte `@artnouveauetdeco` connecté à Metricool ; **75 722 abonnés mesurés au 19-09-2026**. Historique détaillé incomplet et aucun Reel ANAD de référence. Aucun automatisme de diffusion approuvé. | Utiliser Metricool + données natives accessibles pour T0/J+1/J+7/J+30 ; conserver les originaux photographiques comme référence sur Instagram et le site. |
| Mesure / apprentissage | **VALIDÉ comme protocole de pilotage**, instrumentation site encore **À VÉRIFIER**. | Relevés T0, J+1, J+7 et J+30 : métriques sociales accessibles, trafic article si mesurable, temps humain et dépenses. Vérifier d'abord l'activation réelle de Plausible ; Search Console reste à connecter/vérifier. |
| Partenariats / revenus | **PROPOSÉ** : stratégie et modèle d'offres à étudier dès maintenant ; prospection externe, événements, produits et monétisation non activés sans accord. | Étudier événements Art Nouveau / Art Déco, invitations presse/créateur, collaborations patrimoniales, puis éventuellement guides urbains/parcours, partenariats transparents ou produits adaptés. |

## 4. Priorités et dépendances actuelles

**P0 — Immédiat : Maison Coilliot, corpus et intégrité éditoriale.** Rassembler les originaux réellement disponibles de Maison Coilliot, construire une planche-contact, sélectionner les photographies avec Christophe, remplacer ou retirer les deux images d'autres bâtiments lillois, préparer les deux corrections éditoriales identifiées et vérifier le rendu mobile. L'article reste en brouillon jusqu'au gate humain.

**P1 — Premier cycle social sans dépendance Reel.** Préparer le carrousel ou la publication photographique selon le corpus réel, une Story légère vers l'article et la convention de suivi. Le carrousel narratif photographique est le format de référence lorsque plusieurs images fortes existent. Un carrousel hybride illustration → photographie peut être testé ponctuellement, sans devenir une obligation.

**P2 — Mesure et présentation professionnelle.** Vérifier Plausible et le parcours Instagram → article ; appliquer le protocole T0/J+1/J+7/J+30. Renforcer progressivement la présentation de Christophe comme auteur-photographe et préparer un kit professionnel privé avant toute prospection.

**P3 — Audiovisuel.** Si les photographies et l'intention éditoriale justifient un Reel, produire d'abord un pilote déterministe dans DaVinci Resolve Free. Concepts prioritaires : exploration photographique narrative, photographie animée contrôlée, micro-lecture architecturale. Aucun achat nécessaire. Remotion sera réévalué seulement après 3–5 pilotes satisfaisants.

**P4 — Boucle complète, avant changement d'échelle.** Mesurer le premier cycle, documenter temps/coût/qualité, puis seulement décider de la répétition, de l'automatisation ou d'un test IA borné. L'IA vidéo n'est jamais requise ; un éventuel test payant doit faire l'objet d'une validation budgétaire séparée.

Les dates de la roadmap 90 jours restent des objectifs de planification, non des autorisations. Les nouvelles priorités ci-dessus doivent être réconciliées avec `research/anad-2-roadmap-90-days.md` et `research/anad-2-orchestration.md` dans un lot documentaire ciblé, sans supprimer leur historique.

## 5. Cycle de bout en bout à démontrer

`Photographies / sujet documenté → audit des faits et des droits → article ou page utile → sélection du ou des formats sociaux adaptés (photo / carrousel / Story / Reel ponctuel) → validation humaine → distribution → visite du site / réaction → mesure → apprentissage → prochain contenu ou proposition de partenariat`

Chaque campagne pilote doit préciser **avant** sa diffusion : audience cible et objectif, contenu, canal, appel à l'action, destination, métriques accessibles, coût en temps et budget, date de revue et conditions de poursuite/arrêt.

Métriques candidates à confirmer selon accès réels :
- Instagram : portée et vues, rétention lorsque disponible, durée moyenne, partages, sauvegardes, interactions utiles, visites du profil, nouveaux abonnés.
- Site : pages indexées, impressions/clics et requêtes Search Console, sessions ou visites par source lorsque mesurables, visites des articles depuis Instagram via liens traçables.
- Partenariats : contacts pertinents identifiés, messages approuvés et envoyés, réponses, invitations, collaborations réalisées.
- Économie : temps humain par article/Reel, coûts réels, éventuelles recettes et retombées non financières.

Les statistiques d'un Reel et les conversions vers le site ne sont pas entièrement attribuables entre elles sans données pertinentes ; noter les limites au lieu d'inventer une causalité. Ne définir des objectifs chiffrés qu'après un relevé de référence.

## 6. Décisions centrales à préserver

- **D01 VALIDÉ** — GitHub reste la source de vérité. Une seule discussion normale pilote les priorités globales ; Work/Codex exécutent des lots bornés.
- **D02 VALIDÉ — révisé le 20-09-2026** — Maison Coilliot poursuit son cycle indépendamment du Reel. Priorité immédiate : intégrité documentaire, corpus photographique, article, carrousel/photo, Story et mesure. Stratégie, mesure et modèle commercial restent à penser avant la multiplication des productions.
- **D03 VALIDÉ — révisé le 20-09-2026** — Photographie originale de Christophe = socle éditorial et artistique. Carrousels narratifs privilégiés quand le corpus le permet. Illustration = couche artistique secondaire ; un carrousel hybride illustration → photographie peut être expérimenté ponctuellement.
- **D04 VALIDÉ — révisé le 20-09-2026** — Pipeline audiovisuel initial : montage photographique déterministe dans DaVinci Resolve Free. Concepts prioritaires : exploration photographique narrative, photographie animée contrôlée, micro-lecture architecturale. Remotion différé jusqu'à 3–5 pilotes ; génération vidéo IA non standard.
- **D05 VALIDÉ — révisé le 20-09-2026** — Aucun nouvel abonnement ni test payant à ce stade. Toute dépense, publication ou prospection requiert un feu vert humain séparé.
- **D06 VALIDÉ** — Christophe et Théodore interviennent aux points de validation substantiels, pas sur chaque étape mécanique ; la qualité finale et l'autorisation de diffusion restent humaines.
- **D07 VALIDÉ** — Le pilotage courant reste dans le chat normal ; Work/Codex sont réservés aux lots bornés d'exécution. `research/anad-2-orchestration.md` et la roadmap restent à réconcilier documentairement sans réécrire leur historique.
- **D08 VALIDÉ — 20-09-2026** — Positionnement de travail : `ANAD — Art Nouveau et Art Déco en Europe · Publication photographique et patrimoniale de Christophe Aspel`. Identité visuelle photographie-first ; ivoire/encre/bronze comme cadre éditorial, sans filtre sur les photographies ; continuité typographique avec le site.
- **D09 VALIDÉ — 20-09-2026** — Reels ponctuels uniquement lorsqu'ils apportent une valeur distincte ; article/carrousel peuvent être publiés sans Reel. Aucun nombre artificiel de slides ; post simple préférable à un faux carrousel.
- **D10 VALIDÉ — 20-09-2026** — Fonds d'écran : piste expérimentale différée, mini-série limitée possible après validation artistique et droits ; aucune dépendance au premier cycle Coilliot.
- **D11 VALIDÉ — 20-09-2026** — Politique **REUSE FIRST** : avant tout nouvel outil, agent, workflow, template, pipeline ou développement significatif, effectuer un scan des capacités existantes et des dépôts GitHub matures, puis décider explicitement **REUSE / ADAPT / INSPIRE / BUILD**. Les stars/adoption, maintenance, tests, compatibilité, coût, sécurité et licence sont examinés de façon proportionnée. Référence : `research/anad-2-reuse-first-policy.md`.

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
- `research/anad-2-reuse-first-policy.md`
- `research/anad-2-reuse-landscape-2026-09-20.md`
- `research/anad-2-reuse-adoption-plan-2026-10-05.md`

Dernière revue : synthèse des documents GitHub accessibles au 2026-09-20 et décisions de pilotage confirmées par Théodore. Ce registre ne remplace pas un contrôle de la branche actuelle, du déploiement ni des données de compte externes.
