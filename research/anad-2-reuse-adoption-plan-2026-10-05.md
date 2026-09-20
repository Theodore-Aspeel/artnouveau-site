# ANAD 2.0 — Plan d'adoption REUSE FIRST jusqu'au 5 octobre 2026

Date : 2026-09-20  
Statut : **VALIDÉ pour la doctrine, PROPOSÉ pour les lots techniques tant qu'ils ne sont pas exécutés.**  
Références :
- `research/ANAD-PROJECT-STATE.md`
- `research/ANAD-HANDOFF-2026-09-20.md`
- `research/anad-2-reuse-first-policy.md`
- `research/anad-2-reuse-landscape-2026-09-20.md`

## 1. Objectif

Changer la manière de construire ANAD :

- réutiliser d'abord des briques, agents, skills et outils éprouvés ;
- limiter le code spécifique aux règles métier ANAD ;
- respecter le calendrier du premier cycle Maison Coilliot ;
- ne pas ouvrir simultanément tous les chantiers ;
- ne pas ajouter de coût ou d'infrastructure permanente sans besoin mesuré.

Échéance de préparation : **autour du 5 octobre 2026**, sans transformer cette date en obligation de publication.

## 2. Ordre opérationnel

### Vague 1 — 20–23 septembre : socle QA / SEO réutilisable

**But :** renforcer immédiatement tout le reste du projet avec des outils standards.

#### A. Playwright — REUSE
- navigateur Chromium/Firefox/WebKit ;
- tests mobile 390 / 768 ;
- captures et régressions visuelles ;
- navigation FR/EN/NL ;
- menus, article, galerie, footer.

Compatibilité vérifiée : Node >=20, donc cohérent avec ANAD.

#### B. axe-core — REUSE
- moteur accessibilité standard ;
- utiliser dans les tests navigateur plutôt qu'un moteur a11y maison.

#### C. Lighthouse CI — REUSE
- assertions performance / SEO / best practices ;
- ajouter des seuils prudents, non arbitraires ;
- éviter de bloquer le projet sur des scores parfaits au premier passage.

#### D. Unlighthouse — REUSE HORS CI PRINCIPALE
- audit site-wide Lighthouse ;
- Node >=22.18.0 requis ;
- ne pas migrer le runtime ANAD de Node 20 vers Node 22 uniquement pour cet outil ;
- utiliser séparément pour les audits périodiques.

#### E. claude-seo — REUSE / INSPIRE
- utiliser comme framework/checklist/skills SEO ;
- ne pas recréer ses agents généralistes dans ANAD ;
- GSC Wizard reste la source des données Search Console réelles.

**Critère de sortie :**
ANAD possède une couche QA standard réutilisable avant les prochains changements de site.

### Vague 2 — 21–24 septembre : Search Console et mesure

État déjà réalisé :
- propriété Search Console validée ;
- GSC Wizard connecté ;
- gate SEO des drafts fusionné ;
- sitemap public réduit à 9 URL statiques ;
- Coilliot reste `draft` et `noindex,follow`.

À terminer :
- soumettre manuellement `sitemap.xml` à Google Search Console ;
- suivre uniquement les 9 URL indexables ;
- garder les drafts hors de l'index ;
- établir T0 avant diffusion Coilliot ;
- ne pas installer un analytics complet tant que la mesure manquante n'est pas démontrée.

Candidates analytics si besoin futur :
1. GoatCounter pour simplicité ;
2. Umami pour analytics plus riche / MCP ;
3. Plausible seulement après comparaison coût/besoin.

### Vague 3 — 22–26 septembre : CMS / édition

#### Pages CMS — ADAPT / SPIKE

Pourquoi :
- GitHub-first ;
- MIT ;
- support explicite de JSON ;
- gestion médias ;
- ~4k stars, projet actif.

Mais :
- self-host complet = Next.js + PostgreSQL + GitHub App ;
- disproportionné à adopter sans preuve ;
- ne pas remplacer l'Editorial Manager maintenant.

Spike borné :
- vérifier si `src/data/articles.json` peut être représenté proprement ;
- vérifier objets imbriqués, listes, FR/EN/NL, médias ;
- vérifier si le workflow peut rester PR/GitHub-first ;
- aucun déploiement CMS et aucune DB durant le spike.

Décision ensuite :
- REUSE hosted / ADAPT ;
- ou conserver l'éditeur ANAD si le mapping est trop artificiel.

### Vague 4 — 23–29 septembre : premier cycle Coilliot

Les photographies réelles et le gate visuel sont déjà validés.

À faire :
- contrôle automatique mobile/desktop avec la nouvelle couche QA ;
- URL finale et UTM ;
- Story légère / lien ;
- T0 Metricool + Search Console ;
- dry run de publication ;
- décision humaine de date/statut séparée.

Le carrousel reste une production simple, non un chantier technique.

### Vague 5 — 27 septembre–5 octobre : présentation / expérience et briques optionnelles

#### PhotoSwipe — REUSE si besoin galerie
- ne pas construire une lightbox maison ;
- prototype seulement si l'expérience photo justifie le changement.

#### Présentation Christophe / crédibilité
- améliorer auteur / photographe / contact / portfolio si validé ;
- rechercher d'abord les composants/patterns existants avant développement.

#### Reel
Ne pas forcer un Reel dans le premier cycle.

Si le Reel Lab est rouvert :
- commencer par **Remotion Agent Skills + prompts + templates + WebMCP** ;
- utiliser FFmpeg comme moteur bas niveau si nécessaire ;
- ne pas reconstruire un moteur ANAD complet ;
- DaVinci Resolve Free reste valide pour un montage manuel pilote.

## 3. Ce qui est explicitement repoussé

Jusqu'à preuve de besoin :

- Postiz / Mixpost : Metricool répond au cycle initial ;
- n8n / Activepieces : pas de nouvelle couche d'orchestration permanente ;
- Umami / Plausible / GoatCounter : décision après clarification du trou de mesure ;
- Crawl4AI / Firecrawl : seulement si la recherche patrimoniale doit être industrialisée ;
- migration de framework ou CMS lourd ;
- moteur vidéo maison ;
- nouvel abonnement.

## 4. Architecture cible à court terme

```text
GitHub = source de vérité
        |
        +-- données éditoriales / droits / décisions ANAD
        |
        +-- CI métier ANAD
        |     +-- validation contenu
        |     +-- droits
        |     +-- publication gate
        |
        +-- briques standards réutilisées
              +-- Sharp : images
              +-- Playwright : navigateur / visuel
              +-- axe-core : accessibilité
              +-- Lighthouse CI : performance / SEO
              +-- claude-seo : skills / audit SEO
              +-- GSC Wizard : données Google
              +-- Metricool : données sociales
              +-- PhotoSwipe : galerie si besoin
              +-- Remotion ecosystem : vidéo si besoin
```

ANAD conserve uniquement les règles spécifiques :
- patrimoine / faits ;
- corpus Christophe ;
- droits ;
- localisation ;
- statuts et gates ;
- style éditorial ;
- décisions de publication ;
- contrats entre les étapes.

## 5. Règle de construction

Pour chaque nouveau besoin :

`besoin → agents/skills existants → repos GitHub matures → librairies standard → benchmark → REUSE/ADAPT/INSPIRE/BUILD`

Le développement spécifique n'est lancé que pour la partie qui reste réellement propre à ANAD.

## 6. Premier lot d'exécution

**Lot R1 — QA standardisée : Playwright + axe-core + Lighthouse CI**

Statut : **PROPOSÉ, prêt à lancer dans Codex.**

Objectif :
- installer uniquement les dépendances nécessaires ;
- ajouter quelques tests représentatifs, pas une usine à tests ;
- couvrir 390, 768 et desktop ;
- tester FR/EN/NL et Coilliot draft ;
- ajouter accessibilité automatique ;
- ajouter Lighthouse CI avec seuils de régression prudents ;
- préserver la CI existante et Node 20.

Unlighthouse reste externe au lot à cause de son exigence Node 22.18.

## 7. Critère de réussite avant le 5 octobre

Le projet est prêt lorsque :

- le premier cycle Coilliot peut être revu et mesuré de bout en bout ;
- la QA mobile/desktop/a11y/performance repose sur des briques standard ;
- Search Console dispose d'une baseline propre ;
- l'outil éditorial futur a été comparé à Pages CMS plutôt que développé par inertie ;
- aucun Reel ou automatisme lourd n'est devenu une dépendance artificielle ;
- les prochaines extensions partent du benchmark REUSE FIRST.
