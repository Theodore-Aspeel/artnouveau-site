# ANAD 2.0 — C1 : livraison du catalogue structurel de l’export Instagram

> **CORRECTION DU PRÉREQUIS PHOTOGRAPHIQUE — VALIDÉE le 21-09-2026 :** Christophe ne conserve pas d'originaux photographiques historiques dans une photothèque distincte d'Instagram. Les anciennes demandes de fichiers RAW/JPEG natifs ou les formulations faisant de leur absence un blocage absolu sont **OBSOLÈTES** ; ne pas lancer de nouvelle extraction de l'archive ni rechercher une photothèque séparée. Les copies privées Instagram sont la source disponible ; une exploitation web de taille adaptée est **techniquement envisageable** selon la qualité de chaque copie, sous réserve de validation **individuelle de la provenance et des droits** puis d'une **autorisation humaine de publication distincte**. Pour les trois séries Villino Florio, Maison Bastin et rue Warocqué, le référentiel opérationnel à jour est constitué des fiches et de `research/c1-candidates/synchronisation-et-demande-groupee-2026-09-21.md` sur cette branche C1. Le présent rapport conserve ses observations et limites historiques indépendantes de cette correction.

Date de génération : 2026-09-21 (Europe/Brussels).
**Statut : RÉALISÉ / VÉRIFIÉ pour la couverture structurelle de l’export ; EN COURS pour l’identification du sujet des entrées ambiguës ; BLOQUÉ pour l’approbation des originaux et droits individuels.**

Sources de gouvernance lues sur `main` : `AGENTS.md`, `research/ANAD-PROJECT-STATE.md` (D12/D13), `research/c1-instagram-inventory-2026-09-21.md`, `research/anad-2-execution-reset-2026-09-21.md`, `package.json`. Ce livrable complète les trois rapports C1 déjà déposés dans la PR #40 ; aucun contrôle photographique approfondi n’a été relancé.

## 1. Périmètre et preuve de couverture

Lecture locale en une passe de deux fichiers HTML privés de l’export officiel Instagram déjà fourni dans Drive :
- `posts_1.html` : 1 162 publications non archivées dans cet export ;
- `archived_posts.html` : 269 publications archivées dans cet export ;
- **total 1 431 positions datées distinctes, numérotées `F0001`–`F1162` et `A0001`–`A0269` ; 1 460 chemins de médias associés** (1 190 et 270 respectivement).

Les scripts ont validé que chaque référence est unique, que les 1 431 entrées possèdent une date, une légende et au moins un chemin média dans les deux HTML, et que les statuts de toutes les entrées sont renseignés. Le catalogue est **complet en couverture des entrées historiques de ces deux fichiers**, pas une garantie d’accès exhaustif au compte Instagram actuel (stories, liens permanents, Reels, publications supprimées et statut en ligne non établis ici). Ne pas additionner `posts.html` aux deux fichiers : le rapprochement 1 162 + 269 = 1 431 est documenté dans le lot antérieur.

## 2. Résultat du classement conservateur

| Classe de sortie | Nombre | Signification |
| --- | ---: | --- |
| `BATIMENT_NOMME_AUTO` | **258** | Un nom propre de bâtiment, monument ou lieu architectural a été reconnu dans la légende par une règle explicite ; **cela ne prouve pas que la photo montre effectivement le lieu**. |
| `AUTRE_CONTENU` | **90** | Catégorie « autre contenu » attribuée automatiquement, donc susceptible d’erreurs sur des posts mixtes. |
| `AMBIGU_LIEU_OU_DESCRIPTION` | **862** | Ville, architecte, façade ou élément générique sans identification sûre du bâtiment. |
| `SUJET_INCONNU` | **201** | Pas d’information suffisante dans la légende pour identifier une identité de sujet. |
| `AMBIGU_IDENTITE` | **14** | Identité/nom générique ou variante à départager par source patrimoniale/adresse. |
| `AMBIGU_MULTISUJET` | **4** | La légende mentionne plusieurs bâtiments distincts, sans déduction fiable du sujet de la photo. |
| `AMBIGU_COMPARAISON` | **1** | Lieu cité comme comparaison et non comme sujet photographié (Maison Bergeret / librairie gantoise). |
| `AMBIGU_CONTEXTE` | **1** | Mention d’un bâtiment dans un concours/annonce, pas preuve du sujet représenté. |
| **Total** | **1 431** | **258 lieux nommés automatiquement, 90 contenus classés « autres » automatiquement, 1 083 sujets encore à examiner ou inconnus.** |

Les 258 entrées nommées sont associées à **96 identifiants normalisés de lieux architecturaux** (non 96 dossiers photographiques prouvés). **62 clusters de légendes répétées** recouvrent **162 entrées ambiguës** : un `C-...` signifie « texte proche répété », jamais « même bâtiment vérifié ».

## 3. Sauvegardes et reproductibilité — séparation stricte

**Dossier privé Google Drive créé pour ce livrable :** « ANAD 2.0 — Catalogue Instagram C1 — privé » (dans l’espace privé du compte, distinct du dépôt public). Le fichier de référence pour reprise est `ANAD-C1-catalogue-1431-prive-avec-scripts.zip` : il contient le catalogue complet CSV/JSON, le résumé, un index expurgé, `extract.py`, `classify.py`, `finalize.py` et les notes de méthode. **Ce ZIP est une version complète du catalogue à 1 431 entrées.** La copie locale consolidée `ANAD-C1-livrable-final-1431-v2.zip` actualise en outre les indicateurs de contrôle visuel des 18 images documentées dans le lot Losseau/Bastin/Villino Florio (SHA-256 : `36235fc0cc71fe90b363977e35837c00735a3c8013eebed9e71cc5ba0c2ee4cc`). Le ZIP Drive initial contient les mêmes 1 431 références, statuts et clusters mais ses drapeaux `visually_inspected` ne recensent pas encore intégralement ce lot complémentaire ; pour ce champ, le rapport des 18 images fait foi tant que la copie Drive n'a pas été actualisée. Les deux HTML sources et toutes les photographies restent dans leur dossier Drive source d’origine, sans copie dans ce ZIP.

Le dossier Drive contient aussi un CSV autonome du catalogue de base et un index autonome, utiles pour consultation rapide ; **le ZIP est à privilégier pour la version finale consolidée avec clusters et scripts**, car le CSV autonome correspond à un instantané légèrement antérieur du même classement des 1 431 positions.

**Dans GitHub, uniquement** `research/c1-instagram-catalog-index-expurge-2026-09-21.csv` (1 431 lignes de référence ordinale, catégorie, slug et drapeaux ; aucune légende brute, nom de compte, chemin ni photographie privée) et ce rapport de synthèse, à côté des trois rapports C1 déjà présents. Les données brutes de l’export (HTML, légendes, fichiers médias, commentaires, métadonnées privées) **ne sont pas commitées**. La branche C1 et la PR #40 sont laissées ouvertes et non fusionnées. Le registre sur `main` et le checkpoint D1 ne sont pas modifiés.

La reproduction locale utilise **Python et BeautifulSoup déjà disponibles**, sans nouvelle installation ni sous-agent. Le script `extract.py` attend des copies locales privées des deux HTML à leurs chemins indiqués dans le README et émet l’extraction complète ; `classify.py` applique les alias conservateurs et les statuts ; `finalize.py` construit les clusters et fichiers dérivés. Ces fichiers sont dans le ZIP privé et non dans les dépendances de production du site.

## 4. Degré réel de vérification des séries et droits

Les rapports photographiques précédents vérifient directement plusieurs compositions exportées pour **dix nouveaux sujets explicitement documentés** : Casina Cinese, Maison Spitzer, Maison Huot, Maison Losseau, Maison Bastin, Maison Piot, maison de la rue Warocqué, église Sainte-Thérèse de Wattrelos, Maison Paon de Gand et **Villino Florio, Palerme**. Le rapport complémentaire `research/c1-instagram-series-and-limitations-2026-09-21.md`, présent sur cette branche, documente l'ouverture et l'examen des **18/18 images** des séries Losseau, Bastin et Villino Florio, dont **cinq compositions distinctes pour Villino Florio**. Ce dernier est le dixième dossier **visuellement vérifié dans les copies exportées**, non un corpus natif/HD ou juridique validé.

Les indicateurs `visually_inspected` du catalogue concernent certaines publications mentionnées dans les rapports antérieurs, **pas toutes les images de la publication**, notamment les carrousels ; le nombre de fichiers effectivement examinés doit être lu dans les audits de photos, pas déduit du seul drapeau de publication.

**Limites majeures :** aucune comparaison systématique de toutes les 1 460 copies de médias, aucun dédoublonnage image exhaustif, aucune preuve automatique de correspondance des images exportées aux natifs HD de Christophe, aucune approbation individuelle des droits, aucune identification indépendante de tous les bâtiments par adresse/registre patrimonial. Le filigrane du compte, l’absence de crédit tiers ou le fait d’apparaître dans un export ne prouvent ni l’auteur ni les droits. Les crédits de photographes tiers relevés dans les rapports précédents restent à traiter média par média. Le statut courant d’Instagram, les identifiants/liens de chaque post et le rattachement commentaires→post restent partiels ou inconnus. L’exactitude de la classification automatique est **non mesurée par un échantillon aléatoire indépendant** : les nombres sont des résultats des règles, pas une mesure de précision du modèle.

**Bilan de clôture de ce lot :** couverture des 1 431 entrées **VÉRIFIÉE** ; résolution des 1 083 entrées ambiguës/inconnues **NON RÉALISÉE**, explicitement conservées dans le catalogue pour une revue ciblée ; approbation photographique **BLOQUÉE** jusqu’aux natifs et droits. Aucun nouvel examen visuel exhaustif demandé/entrepris, aucun changement site, aucun statut de publication modifié, aucune dépense ni installation payante.
