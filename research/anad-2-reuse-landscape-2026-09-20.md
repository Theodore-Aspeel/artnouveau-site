# ANAD 2.0 — Benchmark REUSE FIRST des outils et dépôts GitHub

Date : 2026-09-20  
Statut du benchmark : **RÉALISÉ — première cartographie transversale**.  
Statut des recommandations : **PROPOSÉ** sauf lorsqu'un outil est déjà utilisé et vérifié dans ANAD.  
Référence de gouvernance : `research/anad-2-reuse-first-policy.md`.

## 1. Objet

Identifier les briques matures déjà disponibles que ANAD peut **REUSE**, **ADAPT** ou utiliser comme **INSPIRE**, afin de réduire le développement maison.

Le benchmark couvre :
- SEO / Search Console / audit ;
- CMS / édition Git ;
- design et galeries ;
- image processing ;
- Reels / vidéo ;
- publication sociale / automatisation ;
- analytics ;
- QA / accessibilité / tests visuels ;
- crawling / recherche assistée.

Aucune installation, dépense ou migration n'est autorisée par ce document.

## 2. Grille de notation ANAD / 100

La note évalue le **fit ANAD aujourd'hui**, pas la qualité absolue du projet.

| Critère | Poids |
| --- | ---: |
| adéquation au besoin ANAD | 30 |
| intégration / réversibilité avec la stack actuelle | 20 |
| maturité / adoption (stars, forks, usage) | 15 |
| maintenance / activité récente | 15 |
| coût / infrastructure supplémentaire | 10 |
| licence / sécurité / clarté d'adoption | 10 |
| **Total** | **100** |

Les stars sont un signal important de découverte et de maturité, mais ne remplacent pas l'analyse de fit.

## 3. Résumé exécutif

### Candidats les plus intéressants

| Priorité | Projet | Domaine | Snapshot GitHub | Score ANAD | Décision proposée |
| --- | --- | --- | --- | ---: | --- |
| A | [microsoft/playwright](https://github.com/microsoft/playwright) | QA / mobile / visuel | ~96.4k stars, Apache-2.0, très actif | **96** | **REUSE** |
| A | [lovell/sharp](https://github.com/lovell/sharp) | image processing | ~32.7k stars, Apache-2.0, très actif | **96** | **REUSE — déjà réalisé** |
| A | [harlan-zw/unlighthouse](https://github.com/harlan-zw/unlighthouse) | audit site-wide Lighthouse | ~4.9k stars, MIT, actif | **93** | **REUSE** |
| A | [GoogleChrome/lighthouse-ci](https://github.com/GoogleChrome/lighthouse-ci) | QA SEO/performance CI | ~7.1k stars, Apache-2.0 | **92** | **REUSE** |
| A | [dimsemenov/PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe) | galerie / lightbox | ~25.3k stars, MIT, framework-independent | **91** | **REUSE** |
| A/B | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | agents / SEO | ~17.3k stars, MIT, 25 skills + 18 agents | **90** | **REUSE / INSPIRE** |
| B | [hunvreus/pagescms](https://github.com/hunvreus/pagescms) | CMS Git | ~4.0k stars, MIT, GitHub-first, JSON + médias | **90** | **ADAPT / pilote** |
| B | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | vidéo déterministe | ~59.9k stars, très actif, Agent Skills/templates/WebMCP | **92** | **REUSE plus tard** |
| B | [dequelabs/axe-core](https://github.com/dequelabs/axe-core) | accessibilité | ~7.5k stars, MPL-2.0, actif | **87** | **REUSE avec Playwright** |
| B | [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | crawl / recherche | ~84.0k stars, Apache-2.0, actif | **86** | **ADAPT si besoin de crawl massif** |
| B | [gitroomhq/postiz-app](https://github.com/gitroomhq/postiz-app) | social scheduling | ~36.1k stars, AGPL-3.0, API + agent | **84** | **WATCH / ADAPT après pilote Metricool** |
| B | [umami-software/umami](https://github.com/umami-software/umami) | analytics | ~38.9k stars, MIT, actif, MCP disponible | **82** | **WATCH / REUSE si analytics site nécessaire** |

## 3 bis. Bibliothèques générales d'agents / skills

Ce scan change la méthode de découverte elle-même : avant de chercher un agent spécialisé isolé, ANAD peut interroger des catalogues déjà massifs et maintenus.

| Projet | Snapshot GitHub | Intérêt ANAD | Score | Décision |
| --- | --- | --- | ---: | --- |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | ~97.6k stars, MIT, très actif | skills d'ingénierie production-grade pour agents | **96** | **REUSE comme catalogue/référentiel** |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | ~51.0k stars, MIT | CRO, SEO, analytics, copywriting, growth | **94** | **REUSE / INSPIRE pour marketing** |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | ~34.6k stars, MIT, 1000+ skills | catalogue multi-agent compatible Codex/Claude/Gemini/Cursor | **94** | **REUSE comme index de découverte** |
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | ~26.2k stars, MIT, 380+ skills | engineering, marketing, product, research, business | **91** | **REUSE comme catalogue** |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | ~54.4k stars, très actif | sélection de skills, agents, plugins et tooling | **86** | **INSPIRE / découverte** |

### Conséquence de méthode

Avant tout futur développement, le REUSE SCAN doit désormais consulter **deux niveaux** :

1. **catalogues de skills/agents** (Agent Skills, VoltAgent, Marketing Skills, Claude Skills, etc.) ;
2. **dépôts métier spécialisés** (SEO, vidéo, CMS, QA, analytics, etc.).

Cette approche est plus efficace qu'une recherche GitHub brute seule : les catalogues font déjà une partie du travail de curation.

### Ordre de découverte proposé

`besoin ANAD → skills déjà connectés → catalogues agents/skills → repos métier GitHub → librairies standard → BUILD seulement si écart réel`

## 4. SEO / Search Console / audit

### AgriciDaniel/claude-seo — 90/100 — REUSE / INSPIRE

Snapshot :
- ~17.3k stars ;
- ~2.5k forks ;
- MIT ;
- activité récente ;
- 25 sous-skills et 18 agents ;
- technical SEO, E-E-A-T, schema, GEO/AEO, hreflang, backlinks, Google APIs, reports.

**Fit ANAD : très élevé.**

Ce projet peut servir de référence pour les checklists, l'orchestration des audits, les agents spécialisés et les rapports. Il couvre une grande partie des fonctions SEO que ANAD aurait sinon tendance à reconstruire.

Limite : cible principale Claude Code. Ne pas recréer ses 25 skills à la main dans ANAD.

### AgriciDaniel/codex-seo — 80/100 — CANDIDAT À CLARIFIER

Snapshot :
- ~738 stars ;
- 26 workflows / 24 agents TOML ;
- port Codex natif ;
- très bon fit fonctionnel.

Le README le présente comme MIT, mais le fichier `LICENSE` contrôlé dans le dépôt est actuellement propriétaire / membership-based. Ce point **n'empêche pas l'étude**, mais doit être clarifié avant copie/intégration de code.

Décision : **INSPIRE immédiatement ; REUSE seulement après clarification de la licence applicable.**

### Unlighthouse — 93/100 — REUSE

Snapshot :
- ~4.9k stars ;
- MIT ;
- actif ;
- Node ;
- lance Lighthouse sur un site entier avec sampling et UI ;
- peut générer un agent skill via `skilld`.

Très bon fit avec le site statique ANAD. Peut compléter Search Console avec une mesure technique multi-page, sans construire notre propre crawler Lighthouse.

### Google Lighthouse / Lighthouse CI — 90–92/100 — REUSE

- Lighthouse : ~30.8k stars, Apache-2.0, très actif.
- Lighthouse CI : ~7.1k stars, Apache-2.0.

Lighthouse CI permet des assertions automatisées sur les commits et peut bloquer les régressions. ANAD devrait utiliser l'outil officiel plutôt que développer ses propres scores de performance/SEO.

### Architecture proposée SEO

**PROPOSÉ :**
- GSC Wizard = données Search Console réelles ;
- Unlighthouse = audit site-wide ;
- Lighthouse CI = garde-fou CI ;
- claude-seo = framework d'analyse / agents / checklists ;
- règles ANAD = publication, droits, provenance et gouvernance spécifiques.

Éviter de développer un « moteur SEO ANAD » généraliste.

## 5. CMS / outil éditorial

### Pages CMS — 90/100 — ADAPT / pilote

Snapshot :
- ~4.0k stars ;
- MIT ;
- GitHub-first ;
- conçu pour sites statiques ;
- gestion de contenu et médias directement dans le repository ;
- schéma de configuration vérifié : formats `json`, `yaml`, `toml`, frontmatter, datagrid, code et raw pris en charge.

Le code confirme une architecture par collections, champs et médias. Le projet gère des formats structurés/frontmatter ; il mérite un spike spécifique pour vérifier la compatibilité exacte avec la structure imbriquée de `src/data/articles.json`.

**Valeur potentielle : élevée.**  
Il pourrait éviter de faire évoluer indéfiniment notre Editorial Manager Python.

### Decap CMS — 82/100 — ADAPT

Snapshot :
- ~19.4k stars ;
- MIT ;
- très mature ;
- Git-based CMS pour générateurs statiques.

Plus mature que Pages CMS, mais historiquement plus lourd à configurer (authentification, modèles de contenu, workflow).

### TinaCMS — 65/100 — WATCH

~13.8k stars, Apache-2.0, très mature mais plus intrusif pour notre stack vanilla.

### Keystatic — 72/100 — WATCH

~2.4k stars, MIT, TypeScript, Markdown/YAML/JSON, sans DB. Intéressant mais plus naturellement intégré aux stacks JS/frameworks modernes.

### Décision proposée CMS

Ne pas migrer maintenant.  
**Prochain spike utile : Pages CMS vs Editorial Manager actuel**, centré uniquement sur :
- édition de `articles.json` ;
- médias ;
- FR/EN/NL ;
- droits/gates ;
- workflow PR.

## 6. Design / galerie / UI

### PhotoSwipe — 91/100 — REUSE

Snapshot :
- ~25.3k stars ;
- MIT ;
- framework-independent ;
- galerie image mobile/desktop.

Très bon candidat si ANAD ajoute un vrai mode d'exploration photographique / lightbox. Ne pas construire une lightbox maison.

### Pico CSS — 76/100 — INSPIRE

~16.9k stars, MIT, CSS minimal pour HTML sémantique.

ANAD possède déjà une identité visuelle forte. Pico n'est pas recommandé comme remplacement global, mais ses patterns sémantiques, formulaires et règles d'accessibilité peuvent inspirer les composants utilitaires.

### Open Props / Primer CSS — INSPIRE

- Open Props : ~5.5k stars, MIT, design tokens CSS.
- Primer CSS : ~13.0k stars, MIT.

À utiliser comme références pour tokens/composants, pas comme redesign complet.

### Sharp — 96/100 — REUSE DÉJÀ RÉALISÉ

Snapshot :
- ~32.7k stars ;
- Apache-2.0 ;
- très actif.

ANAD utilise déjà `sharp` dans ses devDependencies. C'est un exemple réussi de la doctrine REUSE FIRST : ne pas réinventer la génération de formats/redimensionnement.

### imgproxy — 55/100 — NE PAS AJOUTER MAINTENANT

~11.1k stars, très solide, mais nécessite un serveur d'images dédié ; disproportionné pour GitHub Pages.

## 7. Reels / vidéo

### Remotion — 92/100 — REUSE PLUS TARD

Snapshot :
- ~59.9k stars ;
- très actif ;
- vidéo programmatique React ;
- templates, composants, captions, transitions ;
- documentation dédiée aux **Agent Skills**, prompts et templates ;
- **WebMCP** documenté pour contrôler Remotion Studio avec un agent ;
- création de projet scriptable pensée explicitement pour les coding agents.

Conclusion importante : notre ancien prototype Remotion insatisfaisant ne signifie pas que l'écosystème Remotion est mauvais. Nous avons utilisé une approche maison trop étroite.

Lorsque le Reel Lab sera rouvert, commencer par :
- skills agents officiels Remotion ;
- templates officiels ;
- composants existants ;
- exemples communautaires ;
avant tout moteur ANAD spécifique.

La décision antérieure de tester d'abord quelques pilotes déterministes reste valide.

### FFmpeg — 85/100 — REUSE comme moteur bas niveau

~64.4k stars. Standard mature. Utiliser pour encodage/transformation, pas reconstruire un moteur média.

### MoviePy — 74/100 — ADAPT si Python disponible

~14.9k stars, MIT. Bon pour pan/zoom/compositing simple, mais l'environnement Windows actuel rend Node/Remotion plus naturel pour ANAD.

### MoneyPrinterTurbo — 57/100 — INSPIRE

Snapshot :
- ~124.8k stars ;
- MIT ;
- très actif ;
- génération automatisée de shorts depuis thème/keywords.

Projet extrêmement populaire et intéressant architecturalement. En revanche son pipeline orienté génération massive/script + médias + musique est mal aligné avec l'identité photographie-first et documentaire de Christophe.

À étudier pour :
- orchestration vidéo ;
- sous-titres ;
- assemblage ;
- configuration ;
- batch processing.

Ne pas adopter sa direction créative par défaut.

## 8. Social / scheduling

### Postiz — 84/100 — WATCH / ADAPT

Snapshot :
- ~36.1k stars ;
- AGPL-3.0 ;
- Instagram et nombreuses plateformes ;
- scheduling, analytics, API ;
- agent CLI ;
- intégrations n8n/Make.

Très intéressant à moyen terme pour réduire la dépendance à un SaaS de scheduling.

**Mais :** Metricool est déjà connecté et répond au premier cycle. Ne pas migrer avant d'avoir mesuré le besoin réel.

### Mixpost — 72/100 — WATCH

~3.7k stars, MIT, self-hosted, scheduling/analytics. Plus simple juridiquement mais stack Laravel/PHP supplémentaire.

### n8n — 76/100 — WATCH

~205k stars. Très puissant pour automatisation. Mais il peut devenir une seconde couche d'orchestration et une infrastructure permanente. À adopter uniquement si les workflows ANAD deviennent suffisamment nombreux et stables.

### Activepieces — 74/100 — WATCH

~24.6k stars. Même logique que n8n : utile si le besoin multi-app devient réel.

## 9. Analytics

### Umami — 82/100 — WATCH / REUSE

Snapshot :
- ~38.9k stars ;
- MIT ;
- privacy-first ;
- campagnes, conversions ;
- self-host/cloud ;
- endpoint MCP disponible.

Très bon candidat si ANAD veut mesurer les sessions UTM sans Plausible payant.

Coût caché : self-hosting nécessite Node + PostgreSQL ou un service cloud.

### Plausible — 78/100 — WATCH

~29.2k stars, AGPL-3.0. ANAD sait déjà l'injecter mais `PLAUSIBLE_DOMAIN` est inactif. À comparer à Umami/GoatCounter avant toute activation payante.

### GoatCounter — 80/100 — À ÉTUDIER

~6.0k stars. Très léger, sans suivi de données personnelles. Potentiellement plus proportionné qu'un stack analytics complet.

### Matomo — 58/100 — NE PAS AJOUTER

~21.9k stars mais architecture PHP/DB lourde pour notre besoin actuel.

## 10. QA / accessibilité / visual regression

### Playwright — 96/100 — REUSE

Snapshot :
- ~96.4k stars ;
- Apache-2.0 ;
- très actif ;
- Chromium/Firefox/WebKit ;
- screenshots et comparaisons visuelles natives.

Très fort candidat pour :
- 390 px / 768 px ;
- menus ouverts/fermés ;
- captures desktop/mobile ;
- contrôle des pages FR/EN/NL ;
- régressions visuelles ;
- tests navigation/publication.

ANAD ne doit pas développer un moteur maison de capture navigateur.

### Lighthouse CI — 92/100 — REUSE

Voir section SEO. Complément naturel de Playwright.

### axe-core — 87/100 — REUSE AVEC PLAYWRIGHT

~7.5k stars, MPL-2.0, moteur d'accessibilité largement utilisé.

### Pa11y — 82/100 — ALTERNATIVE

~4.5k stars, LGPL-3.0. Très bon outil CLI d'accessibilité, mais axe-core intégré aux tests Playwright paraît plus cohérent avec notre stack.

### BackstopJS — 62/100 — NE PAS PRIVILÉGIER

~7.2k stars, MIT et puissant, mais le README indique que le projet cherche actuellement un nouveau maintainer/owner. Playwright couvre déjà la majorité du besoin avec moins de duplication.

## 11. Crawl / recherche / extraction

### Crawl4AI — 86/100 — ADAPT SI LE BESOIN ARRIVE

Snapshot :
- ~84.0k stars ;
- Apache-2.0 ;
- local, sans clé obligatoire ;
- sortie Markdown LLM-ready ;
- deep crawl / sessions / proxies / Playwright.

Excellent candidat si ANAD commence à automatiser des recherches patrimoniales répétitives sur des dizaines/centaines de pages.

Ne pas l'introduire tant que les outils de recherche existants suffisent.

### Firecrawl — 81/100 — WATCH

Snapshot :
- ~182.6k stars ;
- AGPL-3.0 ;
- API/MCP ;
- search/scrape/crawl/map/interact ;
- très mature et agent-ready.

Très puissant mais l'offre hébergée utilise des clés/API et le self-host est une infrastructure supplémentaire. À privilégier seulement si le gain par rapport à Crawl4AI ou aux outils ChatGPT est démontré.

### Browser-use — 68/100 — DUPLICATION ACTUELLE

~115.5k stars, MIT. Très impressionnant, mais ChatGPT Work possède déjà une capacité de navigateur/Computer Use pour les workflows où elle est nécessaire.

### Scrapy — 75/100 — REUSE SI CRAWLER DÉTERMINISTE

~64.4k stars, BSD-3-Clause. Excellent framework généraliste, mais plus bas niveau que Crawl4AI pour un pipeline orienté agents.

## 12. Ce qu'ANAD ne doit probablement plus développer lui-même

Sous réserve des spikes ciblés :

- crawler Lighthouse multi-page ;
- moteur de screenshots navigateur ;
- moteur d'accessibilité généraliste ;
- lightbox photo ;
- transformations d'images de base ;
- moteur bas niveau vidéo/encodage ;
- CMS Git complet ;
- scheduler social complet ;
- analytics web complet ;
- crawler web généraliste ;
- framework SEO générique.

Le développement ANAD doit se concentrer sur :
- contrats éditoriaux propres au projet ;
- fact-checking patrimonial ;
- droits des photographies ;
- règles FR/EN/NL ;
- publication gates ;
- sélection artistique ;
- intégration des briques ;
- mesures et décisions métier.

## 13. Shortlist d'expérimentations proposées

Aucune n'est lancée automatiquement.

### Spike R1 — QA
**Playwright + axe-core + Lighthouse CI / Unlighthouse**

Objectif : remplacer les contrôles manuels répétitifs par des outils standards.

### Spike R2 — SEO
**claude-seo comme framework + GSC Wizard + Unlighthouse**

Objectif : déterminer quelles briques SEO ANAD peut supprimer/ne plus développer.

### Spike R3 — Editorial
**Pages CMS**

Objectif : vérifier si Christophe peut éditer le corpus Git sans dépendre de l'éditeur Python maison.

### Spike R4 — Galerie
**PhotoSwipe**

Objectif : prototype lightbox photo sur une page article, sans redesign général.

### Spike R5 — Reel Lab futur
**Remotion skills/templates officiels**

Objectif : reprendre le Reel Lab depuis l'écosystème existant plutôt qu'un moteur maison.

### Spike R6 — Social futur
**Postiz**

Objectif : comparer uniquement lorsque Metricool devient limitant.

## 14. Décision de pilotage proposée

**PROPOSÉ :** appliquer le benchmark en deux vagues.

**Vague 1 — maintenant / avant premier cycle complet**
- Playwright ;
- axe-core ;
- Lighthouse CI ou Unlighthouse ;
- claude-seo comme référentiel d'audit ;
- conserver Sharp ;
- tester Pages CMS seulement en lecture/spike.

**Vague 2 — après le premier cycle mesuré**
- PhotoSwipe si besoin galerie ;
- Remotion officiel pour Reel Lab ;
- Postiz si besoin de scheduling/automation ;
- Umami/GoatCounter si analytics site devient nécessaire ;
- Crawl4AI si la recherche patrimoniale devient industrialisée.

## 15. Conclusion

Le scan confirme l'hypothèse de Théodore : il existe déjà de nombreuses briques matures que ANAD peut réutiliser.

La correction stratégique n'est pas de remplacer tout ANAD par des projets externes ; elle est de déplacer notre effort :

**moins de frameworks maison, plus d'intégration de briques éprouvées, et développement spécifique uniquement là où ANAD possède une vraie logique métier propre.**
