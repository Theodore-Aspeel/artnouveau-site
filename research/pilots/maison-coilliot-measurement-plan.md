# Maison Coilliot - protocole de mesure du premier cycle

## Mise à jour opérationnelle du 21 septembre 2026

Le statut ci-dessous remplace les passages datés du 20 septembre relatifs à Search Console et au lien Coilliot ; conserver le reste comme baseline historique.

- **Search Console — VÉRIFIÉ pour l'accès, EN COURS pour le sitemap** : propriété URL-prefix validée et rattachée à GSC Wizard. Sitemap soumis le 21 septembre, mais GSC indique encore `isPending=true` / « Impossible de récupérer le sitemap » ; 0 URL découverte dans l'interface. Le lecteur public GSC Wizard récupère 9 URL statiques, 0 article `draft`. Cause non déterminée : attendre le détail du rapport et vérifier le Content-Type HTTP avant toute correction technique ou nouvelle soumission.
- **Coilliot — VÉRIFIÉ côté liens publics, sans publication** : slug `maison-coilliot-lille-hector-guimard`, statut `draft`, page `noindex,follow`. Liens UTM Story et profil testés en HTTP 200, canonical sans paramètres UTM. Les UTM n'impliquent **aucune mesure effective de sessions** tant qu'aucun analytics site n'est activé.
- **R1 QA — VÉRIFIÉ** : PR #33 fusionnée et déployée ; Playwright, axe-core, Lighthouse CI disponibles. L'article n'a pas été publié.

Liens exacts pour le dry run (ne pas diffuser avant approbation) :

- Story : `https://theodore-aspeel.github.io/artnouveau-site/fr/articles/maison-coilliot-lille-hector-guimard/?utm_source=instagram&utm_medium=organic_social&utm_campaign=anad_maison_coilliot&utm_content=story_link`
- Profil : `https://theodore-aspeel.github.io/artnouveau-site/fr/articles/maison-coilliot-lille-hector-guimard/?utm_source=instagram&utm_medium=organic_social&utm_campaign=anad_maison_coilliot&utm_content=profile_link`


Date : 2026-09-20  
Statut : **EN COURS** pour le chantier mesure. Les constats techniques ci-dessous sont **VÉRIFIÉS** lorsqu'une preuve est indiquée. Les choix d'instrumentation non encore approuvés restent **PROPOSÉS**.

## 1. Objet

Préparer la mesure du premier cycle Maison Coilliot sans ajouter de publication, dépense ou automatisation de diffusion.

Le protocole doit permettre de distinguer :
- performance du contenu Instagram ;
- passage d'Instagram vers l'article lorsque cette mesure est réellement accessible ;
- visibilité organique Google ;
- temps humain et coût du cycle.

Aucune causalité entre performance Instagram et trafic site ne doit être affirmée sans donnée d'attribution correspondante.

## 2. État vérifié au 20 septembre 2026

### Article Coilliot

**RÉALISÉ et VÉRIFIÉ :**
- PR #25 fusionnée dans `main` ;
- commit de merge : `3d7d45c53f50e6c22730638d1e2d36d6b07da214` ;
- l'article reste en statut `draft`.

Le déploiement GitHub Pages déclenché par ce merge était encore en cours au dernier contrôle de cette note.

### Plausible

**VÉRIFIÉ : support présent dans le dépôt, mesure production inactive.**

Le build sait injecter Plausible lorsque `PLAUSIBLE_DOMAIN` est renseigné. Le workflow GitHub Pages lit cette variable depuis les variables du dépôt.

Dans les logs du dernier déploiement production contrôlé avant le merge Coilliot, `PLAUSIBLE_DOMAIN` est vide. Le script Plausible n'est donc pas activé par ce build.

Conséquence : aucune session ou visite UTM ne doit être attribuée à Plausible tant que cette activation n'a pas été vérifiée.

### Google Search Console / GSC Wizard

**VÉRIFIÉ : compte Google connecté, propriété ANAD absente.**

Le compte Google connecté à GSC Wizard dispose du scope Search Console. En revanche :
- aucune propriété n'est actuellement enregistrée dans GSC Wizard ;
- la tentative d'ajouter `https://theodore-aspeel.github.io/artnouveau-site/` échoue car cette propriété n'existe pas dans le compte Google Search Console.

**BLOQUÉ :** la propriété URL-prefix doit d'abord être créée et vérifiée dans Google Search Console. Après cela, elle pourra être enregistrée dans GSC Wizard et auditée.

### Google Analytics 4

**VÉRIFIÉ : non connecté à GSC Wizard.**

Le consentement Google Analytics n'est pas actuellement accordé à GSC Wizard et aucune propriété GA4 n'est accessible par ce canal.

Aucune implémentation GA4 n'est décidée par le présent document.

### Metricool / Instagram

**VÉRIFIÉ :**
- marque Metricool : `artnouveauetdeco` ;
- compte Instagram : `@artnouveauetdeco` ;
- 75 722 abonnés mesurés le 19-09-2026 ;
- la connexion Metricool est récente et le relevé demandé sur les publications du 24-08 au 20-09 ne renvoie pas de lignes exploitables.

Conséquence : ne pas fabriquer de "médiane récente du compte" à partir de données absentes. Le premier cycle doit constituer sa propre baseline.

Metricool expose à partir de maintenant les métriques utiles suivantes : portée, vues, interactions, likes, commentaires, sauvegardes, partages, abonnements issus des publications, données de Stories et taps sur les liens de profil lorsque disponibles.

## 3. Baseline et points de mesure

### T0 - avant diffusion

Enregistrer :
- date et heure de diffusion prévues ;
- URL finale de l'article ;
- statut de l'article ;
- nombre d'abonnés Instagram ;
- taps de liens de profil disponibles sur la période T0 ;
- contenu exact diffusé et format ;
- temps humain déjà consacré au cycle ;
- dépenses réelles, attendues à 0 EUR pour ce premier cycle sauf validation séparée.

### J+1, J+7 et J+30

Instagram / Metricool :
- portée et vues ;
- interactions ;
- likes et commentaires ;
- sauvegardes ;
- partages ;
- nouveaux abonnements attribués au contenu lorsque disponibles ;
- données Story : portée, impressions, sorties, réponses, taps avant/arrière ;
- taps sur les liens du profil lorsque disponibles.

Instagram natif :
- relever manuellement les taps du sticker de lien de la Story si cette métrique est disponible et non exposée par Metricool.

Site :
- trafic de l'article et attribution UTM uniquement si un outil de mesure site est effectivement activé ;
- sinon marquer la métrique **NON MESURABLE** au lieu de l'estimer.

Search Console :
- impressions, clics, requêtes, position et indexation sont des métriques SEO séparées ;
- elles ne servent pas à attribuer du trafic Instagram.

Économie du cycle :
- temps humain ;
- dépenses ;
- incidents ou reprises ;
- décision de poursuivre, simplifier ou arrêter certains formats.

## 4. Convention UTM du premier cycle

Convention **PROPOSÉE** pour tous les liens Instagram traçables vers Maison Coilliot :

| Champ | Valeur |
| --- | --- |
| `utm_source` | `instagram` |
| `utm_medium` | `organic_social` |
| `utm_campaign` | `anad_maison_coilliot` |
| `utm_content` | `story_link` ou `profile_link` selon le point d'entrée |

Ne pas utiliser `anad_reel_...` pour ce cycle sauf s'il s'agit réellement d'un Reel. Le contrat Reel historique reste spécifique à son format.

Exemple de destination FR :

`https://theodore-aspeel.github.io/artnouveau-site/fr/articles/maison-coilliot-lille-hector-guimard/?utm_source=instagram&utm_medium=organic_social&utm_campaign=anad_maison_coilliot&utm_content=story_link`

Le lien exact doit être testé après le déploiement et avant toute diffusion.

## 5. Décisions et limites

**VALIDÉ antérieurement :**
- relevés T0, J+1, J+7 et J+30 ;
- pas de dashboard payant requis ;
- aucune dépense ou publication automatique ;
- mesure des limites plutôt qu'invention de données.

**PROPOSÉ pour ce cycle :**
- ne pas bloquer le pilote sur l'absence actuelle d'une analytics site complète ;
- utiliser Metricool et les Insights Instagram comme baseline sociale ;
- créer et vérifier Search Console avant le cycle si possible ;
- conserver la convention UTM dès le premier cycle, même si la mesure des sessions site reste temporairement indisponible.

**NON DÉCIDÉ :**
- activation de Plausible ;
- ajout de GA4 ;
- ajout d'un autre outil de mesure.

Tout changement de stack de mesure doit être validé avant implémentation.

## 6. Prochaine action unique

Créer et vérifier dans Google Search Console la propriété URL-prefix :

`https://theodore-aspeel.github.io/artnouveau-site/`

Si Google exige une preuve HTML ou une balise de vérification, préparer un lot GitHub dédié sur branche avec test et preview, puis refaire `add_site` dans GSC Wizard.

Aucune publication Coilliot n'est autorisée par ce document.
