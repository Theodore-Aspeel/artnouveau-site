# ANAD 2.0 — C1 : audit initial de l'export propriétaire Instagram

Date : 2026-09-21. **EN COURS — accès à l'export et première extraction VÉRIFIÉS** ; audit bâtiment par bâtiment et rapprochement avec les originaux non achevés.

Cette note complète `research/c1-instagram-inventory-2026-09-21.md` (premier relevé limité au connecteur Metricool). **La limitation historique « seules deux publications accessibles » n'est plus d'actualité depuis la réception de l'export officiel**. Aucun résultat de ce relevé ne doit être confondu avec un décompte définitif d'articles, de bâtiments ou de vues originales.

## Accès vérifié, sans Work

L'export HTML du compte `artnouveauetdeco`, décompressé par le propriétaire dans un dossier Google Drive privé, est lisible via le connecteur Drive. Ne pas consigner l'URL privée du dossier ni des identifiants de fichiers dans le dépôt public. Organisation et fichiers effectivement observés :

- `your_instagram_activity/media/posts.html` (~10,4 Mo) et `posts_1.html` (~1,65 Mo) ;
- `your_instagram_activity/media/reels.html` (~103 Ko), `stories.html` (~1,25 Mo), `archived_posts.html` (~360 Ko) ;
- `your_instagram_activity/comments/post_comments_1.html` (~1,24 Mo), `hype.html` ;
- `logged_information/past_instagram_insights/posts.html`, `reels.html`, `stories.html` et autres historiques ;
- `media/posts/` (fichiers JPG/WEBP et dossiers mensuels dont les dates vont au moins de 2019 à 2025), `media/reels/`, `media/stories/`, `media/archived_posts/`.

L'export permet donc une **analyse historique** des publications, Reels, descriptions et médias exportés que les deux lignes Metricool ne permettaient pas. L'archive peut contenir des doublons et des publications archivées ; les fichiers HTML `posts.html` et `posts_1.html` ne doivent PAS être additionnés sans déduplication.

## Premières mesures techniques — ne pas présenter comme nombre de posts

Lecture des fichiers HTML via Drive, comptages exploratoires d'éléments HTML :
- `posts.html` : 1 431 marqueurs de date `_3-94 _a6-o` et 1 201 chemins distincts `media/posts/…` dans les attributs `src/href`. Ces deux chiffres ne sont **ni un nombre vérifié de publications**, ni un nombre de clichés originaux ; certains éléments peuvent être dupliqués ou appartenir à des sections imbriquées.
- `posts_1.html` : 1 162 marqueurs de date et 1 190 chemins de média distincts. Chevauchement à dédupliquer avec `posts.html`.
- `reels.html` : 69 marqueurs de date, 72 chemins médias distincts, à normaliser avant décompte final.
- `stories.html` : 695 marqueurs de date et 695 chemins distincts.
- `archived_posts.html` : 269 marqueurs de date et 270 chemins distincts.
- `post_comments_1.html` est accessible et contient des commentaires, mais la relation entre chaque commentaire et sa publication cible **n'est pas démontrée** par cette première inspection ; ne pas publier les noms d'utilisateurs et ne pas supposer que tous les commentaires tiers du compte sont présents.

L'extraction exploratoire de `posts.html` a trouvé **1 139 paires légende/média compatibles avec le motif HTML testé**, qui ne couvre pas tous les formats de publication. Des correspondances textuelles à un même bâtiment peuvent représenter de vraies vues différentes, des reposts du même cliché ou une confusion de nom ; revoir visuellement avant de valider des séries multi-vues.

## Premières pistes répétées dans les légendes exportées

Ces nombres sont des **paires légende/média retrouvées par recherche d'expressions** et NON des photos distinctes validées :

| Sujet apparent | Références légende/média retrouvées | Statut du corpus |
| --- | ---: | --- |
| Maison Coilliot, Lille | 9 | Dossier ANAD déjà traité, hors choix des prochains nouveaux sujets ; démonstration que Metricool sous-représentait l'historique. |
| Maison Saint-Cyr (Gustave Strauven), Bruxelles | 7 | Candidat de rapprochement des vues, des dates et des originaux ; les mentions d'architecte seul ne comptent pas. |
| Maison des Hiboux, Saint-Gilles | 6 | Dossier ANAD existant ; vérifier doublons/angles et correspondance aux 2 ressources du site. |
| Maison aux Tulipes, Bratislava | 2 | Dossier ANAD existant ; vérifier si plusieurs photos ou même photo rediffusée. |
| Palais de la Sécession, Vienne | 12 | Dossier ANAD existant ; réutilisations/attributions à autrui possibles selon la légende, droits à contrôler image par image. |
| Chiosco Ribaudo, Palerme | 1 | Dossier nouveau potentiel ; autres mentions éventuelles à rechercher sous variantes de nom. |
| Monument au Maestro Serrano, Sueca | 1 | Dossier nouveau potentiel ; rechercher autres angles et noms alternatifs. |

Les motifs s'appuient sur les légendes de `posts.html` et non sur une validation visuelle ou une recherche exhaustive. Les chiffres n'autorisent aucune nouvelle publication. L'export Instagram inclut des médias publiés, mais **ne démontre pas l'existence des originaux natifs HD** ni l'accord de réutilisation de contenus tiers.

## Prochain travail précis, dans une discussion normale et sans Work

1. Normaliser les pages HTML historiques en enregistrements `publication + légende + date + chemins média exporté + type + éventuelle URL/ID` et dédupliquer `posts.html`, `posts_1.html`, les archives et les Reels. Traiter les chemins médias comme des références privées à l'archive, pas comme des URL publiques. Vérifier sur échantillon les images d'un même post.
2. Regrouper les publications par bâtiment au moyen des légendes + ville + variantes de nom ; **ne pas fusionner des bâtiments voisins ni confondre auteur/architecte avec bâtiment**. Générer une présélection non Coilliot fondée sur médias distincts effectivement consultables.
3. Examiner le schéma des commentaires et déterminer si un identifiant ou une relation vers la publication est disponible. Si non, établir un corpus textuel séparé, **sans attribuer un commentaire à un bâtiment sur une simple supposition** ; ne pas publier de données personnelles.
4. Recouper les bâtiments présélectionnés avec les 14 slugs et le registre de droits, puis demander uniquement les originaux des 2–3 dossiers prometteurs.

**Effet sur le pilotage C1 :** l'absence d'historique IG complet via Metricool n'est plus un bloqueur. Le travail d'extraction et de normalisation est **EN COURS** ; la validation de plusieurs vues originales HD et des droits reste **BLOQUÉE jusqu'au rapprochement des originaux**. D1 et son checkpoint restent intacts. Aucune installation, publication, dépense ou modification du site.
