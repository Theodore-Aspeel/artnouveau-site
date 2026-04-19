# NL-13 - Comportement des articles non disponibles en neerlandais

## Decision

En preview NL, conserver tous les articles visibles, mais signaler clairement les articles qui ne sont pas encore disponibles en neerlandais.

Libelle recommande pour les surfaces compactes :

```text
Alleen in het Frans
```

Libelle recommande pour une page article ouverte en NL quand son contenu NL manque :

```text
Dit artikel is voorlopig alleen in het Frans beschikbaar.
```

Cette strategie evite un fallback FR silencieux, preserve la continuite du corpus, et ne masque pas artificiellement la moitie du site pendant la migration progressive.

## Comportement actuel observe

- `nl` est une locale de preview, pas une locale publique.
- Les liens de preview publics visibles dans la navigation restent limites a FR et EN.
- Les textes statiques peuvent deja se rendre en neerlandais quand `?previewLocale=nl` est present.
- Les helpers article selectionnent `content.nl` quand il existe, puis retombent automatiquement sur les fallbacks configures, aujourd'hui `fr` puis `en`.
- Les 14 articles restent visibles en home, galerie, cartes, liens autour, et precedent / suivant.
- Les 7 articles sans `content.nl` affichent donc du contenu francais dans une interface neerlandaise, sans indicateur visible.

Articles actuellement disponibles en NL :

- `maison-fernand-lefever-bruxelles`
- `maison-des-hiboux-saint-gilles`
- `maison-lotus-anvers`
- `casa-campanini-milan-1904`
- `den-tijd-le-temps-anvers`
- `aquarium-de-milan-1906`
- `maison-ernest-delune-maitre-verrier`

Articles non encore disponibles en NL :

- `maison-coilliot-lille-hector-guimard`
- `lhuitriere-lille-art-deco`
- `maison-aux-tulipes-bratislava-jeno-schiller`
- `maison-strauven-avenue-van-cutsem-2729-tournai-1904`
- `palais-de-la-secession-vienne-18971898`
- `maison-aux-majoliques-vienne`
- `facade-art-deco-charleroi`

## Options comparees

### Fallback FR silencieux

Avantages :

- Aucun changement de rendu.
- Tous les liens continuent de fonctionner.
- Le corpus reste complet.

Limites :

- Experience confuse : interface NL, article FR, sans explication.
- Risque de donner l'impression d'une traduction incomplete ou cassee.
- Peu robuste si la preview NL devient plus visible.

Conclusion : acceptable comme fallback technique interne, insuffisant comme comportement produit.

### Masquer les articles non prets

Avantages :

- Experience NL purement neerlandaise.
- Pas de melange visible entre interface NL et texte FR.

Limites :

- La home et la galerie changent fortement de corpus selon la locale.
- Les clusters editorialement utiles deviennent incomplets.
- Les liens `around`, precedent et suivant peuvent disparaitre ou sauter des articles, ce qui modifie la lecture du site.
- Strategie fragile tant que seulement une partie du corpus est disponible en NL.

Conclusion : trop radical pour une migration progressive et trop couteux en coherence editoriale.

### Afficher avec indicateur clair

Avantages :

- Le corpus reste complet.
- L'utilisateur comprend pourquoi un texte francais apparait en mode NL.
- Les parcours editoriaux et liens internes restent stables.
- La strategie accompagne naturellement la progression article par article.

Limites :

- Necessite un petit ajout de disponibilite locale dans le runtime.
- Demande un libelle court et coherent sur plusieurs surfaces.

Conclusion : meilleure strategie pour le stade actuel.

## Application par zone

### Home

La home NL doit garder les memes sections et continuer a alimenter la selection, les parcours par ville et les rythmes avec le corpus complet.

Pour chaque lien ou carte pointant vers un article non disponible en NL, afficher un indicateur discret `Alleen in het Frans`.

Ne pas reduire les compteurs aux seuls articles NL-ready tant que le corpus complet reste visible.

### Listes / galerie

La galerie NL doit lister les 14 articles.

Les filtres par tags doivent continuer a fonctionner sur tout le corpus. Quand un filtre renvoie des articles non disponibles en NL, les cartes doivent les afficher avec le meme indicateur.

Ne pas introduire de filtre implicite "NL seulement" dans ce lot.

### Cartes d'articles

Chaque carte doit pouvoir connaitre la disponibilite effective de l'article pour la locale courante.

En mode NL :

- article avec `content.nl` exploitable : rendu normal ;
- article sans contenu NL exploitable : rendu fallback FR, avec badge `Alleen in het Frans`.

Le badge doit etre visible dans le corps de carte ou pres du meta, pas seulement dans un attribut technique.

### Liens around

Les liens `around` doivent rester visibles meme si la cible n'est pas disponible en NL.

Si la cible est non disponible en NL, ajouter un indicateur a cote du lien ou sous le titre :

```text
Alleen in het Frans
```

Ne pas supprimer le lien, car la relation editoriale reste valide.

### Article precedent / suivant

La sequence precedent / suivant doit rester basee sur l'ordre editorial complet.

En mode NL, si la carte precedent ou suivant pointe vers un article non disponible en NL, afficher le meme indicateur.

Ne pas recalculer la sequence sur les seuls articles NL-ready, sinon l'ordre de lecture change selon la langue et devient difficile a expliquer.

## Ordre de mise en oeuvre conseille

1. Ajouter dans `article-access.js` un helper de disponibilite locale, par exemple `getArticleLocaleAvailability(article, locale)`.
2. Definir une regle stricte de disponibilite NL : `content.nl.title`, `content.nl.dek` et au moins une section NL non vide suffisent pour considerer l'article disponible en NL.
3. Ajouter les messages i18n pour le badge compact et l'avertissement article.
4. Afficher le badge sur les cartes home / galerie.
5. Afficher le badge sur les liens `around` et precedent / suivant.
6. Ajouter un avertissement court en haut de page article quand la page NL rend un fallback FR.
7. Valider avec `npm run validate` et `npm run build`.

## Hors perimetre NL-13

- Pas de switch public NL.
- Pas de nouveau contenu NL.
- Pas de masquage d'articles.
- Pas de changement SEO ou de routes localisees.
- Pas de modification de `src/data/articles.json`.
- Pas de refonte visuelle.
