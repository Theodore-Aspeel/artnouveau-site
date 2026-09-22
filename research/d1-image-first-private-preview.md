# D1 image-first - prévisualisation photographique privée

Date : 2026-09-22  
Statut : **RÉALISÉ localement - médias non publiables**

## Frontière de confidentialité

Les douze JPEG utilisés par cette maquette proviennent exclusivement de l'export DOCX du Google Doc privé `ANAD D1 - Planche photographique privée - maquette uniquement`.

- Le dossier Drive ne contient aucun JPEG autonome, uniquement le document Google Docs.
- L'export DOCX pèse environ 3,4 Mo et contient 12 JPEG incorporés.
- Les dimensions extraites vont de 1063 x 1536 à 1536 x 1493. Il s'agit de versions incorporées et potentiellement recompressées, pas d'originaux natifs.
- Aucun de ces JPEG ne doit être ajouté à GitHub, à `src/`, au registre de droits, à un artefact CI ou à un déploiement.
- Le répertoire local `.private-media/` est ignoré par Git. Le build public standard ne crée jamais `dist/private/`.

## Noms attendus

| Fichier local | Libellé vérifié dans la planche |
| --- | --- |
| `blue-01-overview-19126.jpg` | Série bleue, vue d'ensemble, 19126.jpg |
| `blue-02-turret-19123.jpg` | Série bleue, tourelle et partie haute, 19123.jpg |
| `blue-03-door-19122.jpg` | Série bleue, porte et encadrement, 19122.jpg |
| `blue-04-oriel-19119.jpg` | Série bleue, oriel, balcon et ferronnerie, 19119.jpg |
| `blue-05-detail-19118.jpg` | Série bleue, gros plan sur décor bleu, 19118.jpg |
| `interior-a-19136.jpg` | Intérieur A, identité non vérifiée, 19136.jpg |
| `interior-b-19134.jpg` | Intérieur B, rapprochement non vérifié, 19134.jpg |
| `interior-c-19144.jpg` | Intérieur C, identité non vérifiée, 19144.jpg |
| `hall-01-interior-19157.jpg` | Halle, vue intérieure générale, 19157.jpg |
| `hall-02-facade-19152.jpg` | Halle, façade monumentale, 19152.jpg |
| `hall-03-detail-19148.jpg` | Halle, détail de marquise et décor, 19148.jpg |
| `other-facade-19114.jpg` | Autre façade aux briques claires, 19114.jpg |

## Lancement Windows

1. Placer les 12 JPEG renommés dans `.private-media/` à la racine du dépôt.
2. Double-cliquer sur `preview-private-windows.cmd`.
3. Le script vérifie Node et les médias, construit d'abord le site public, crée ensuite `dist/private/` localement, démarre le serveur et ouvre le navigateur seulement lorsque le serveur écoute.
4. Parcourir `/private/`, `/private/portfolio.html` et `/private/series-blue.html`.
5. Fermer la fenêtre du serveur pour arrêter la prévisualisation. Un prochain build public efface `dist/private/`.

## Parcours démontré

La série bleue est présentée sans identification architecturale inventée : vue générale, partie haute, seuil, oriel/ferronnerie, détail décoratif, puis rappel du futur verrou documentaire.

