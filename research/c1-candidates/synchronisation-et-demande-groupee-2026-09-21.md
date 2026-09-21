# C1 — Traçabilité synchronisée et demande groupée pour trois dossiers candidats

Date de contrôle : 2026-09-21. **Statuts : RÉALISÉ/VÉRIFIÉ — fiches et indicateurs justifiés ; EN COURS — recherche ciblée des natifs et identification patrimoniale ; BLOQUÉ — preuve de droits individuels et approbation de publication.** Périmètre exclusivement documentaire, branche C1 et PR #40 ; aucune incidence D1, site, registre de droits, articles ni publications.

## 1. Source de vérité et version du catalogue privé

La **nouvelle version de référence des données privées pour les indicateurs d'inspection** est le ZIP **`ANAD-C1-catalogue-1431-prive-indicateurs-synchronises-2026-09-21.zip`** dans le dossier Drive privé « ANAD 2.0 — Catalogue Instagram C1 — privé ». Il contient le catalogue complet CSV/JSON, les index, la synthèse, un manifeste du delta d'inspection et les scripts originaux `extract.py`, `classify.py`, `finalize.py` **conservés à l'identique**. SHA-256 du ZIP : `cf59e0d306f3294c898fadd8ea89417cc00bfdf13029a1f3454d706843a93d69` ; ce hash permet de distinguer cette version de l'instantané initial. **Lecture de retour Drive et intégrité du ZIP vérifiées.**

Deux copies autonomes portant le suffixe `-indicateurs-synchronises-2026-09-21.csv` ont également été enregistrées dans le même dossier privé : le catalogue complet et l'index expurgé. **Les trois fichiers précédents restent en place comme instantanés historiques** ; ne pas les choisir pour lire les nouveaux drapeaux. La copie locale `ANAD-C1-livrable-final-1431-v2.zip` mentionnée dans le rapport de catalogue n'était **pas disponible parmi les fichiers du dossier Drive consulté** ; le ZIP synchronisé est dérivé de la sauvegarde complète initiale vérifiée et des preuves d'audit déjà disponibles, et ne présume pas d'autres corrections propres à une éventuelle v2 non consultée. Ne pas relancer l'extraction pour appliquer ces seules corrections.

**Sur GitHub**, `research/c1-instagram-catalog-index-expurge-2026-09-21.csv` a été actualisé sur la **branche C1 seulement** ; il reste expurgé (sans légendes brutes, chemins de médias ni photos). Les **10 lignes modifiées** sont uniquement `F0005, F0013, F0017, F0018, F0027, F0729, F0740, F0746, F0751, F1020`, où `visual_file_inspected` passe de `False` à `True`. Toutes ont **un seul média** et sont documentées dans [l'audit existant Losseau/Bastin/Villino Florio](../c1-instagram-series-and-limitations-2026-09-21.md). Les drapeaux déjà vrais des six entrées Warocqué et de deux entrées Bastin restent inchangés.

## 2. Résultat des contrôles de non-régression

| Contrôle | Avant / source complète initiale | Après / catalogue privé synchronisé et index GitHub |
| --- | ---: | ---: |
| Positions historiques F0001–F1162 / A0001–A0269 | 1 431 | **1 431 — inchangé** |
| Références de médias de l'export | 1 460 | **1 460 — inchangé** |
| `BATIMENT_NOMME_AUTO` | 258 | **258 — inchangé** |
| `AUTRE_CONTENU` | 90 | **90 — inchangé** |
| Entrées ambiguës ou inconnues | 1 083 | **1 083 — inchangé** |
| Identifiants normalisés | 96 | **96 — aucune classification modifiée** |
| Publications marquées avec au moins un média inspecté | 26 | **36 — exactement +10 justifiées** |
| Originaux natifs / droits de réutilisation de ces 18 copies | Inconnus / non vérifiés | **Inconnus / non vérifiés — aucun changement** |

Vérification comparative des 1 431 lignes du ZIP : **seule** la valeur `visual_inspected` des dix références ci-dessus est modifiée par rapport à l'archive initiale ; les champs de classification, statut des droits, sujet, références, chemins et légendes restent identiques. Les agrégats de signalement visuel de la synthèse interne et les deux index dérivés reflètent ces dix modifications, sans changement de catégorie ni de cluster. Les trois scripts préexistants sont préservés octet pour octet. **Attention :** relancer les scripts sur les seuls HTML peut reconstruire un ancien état des drapeaux ; le ZIP porte un manifeste JSON des dix corrections à préserver/réappliquer lors d'une future génération.

### Sémantique des preuves : ne jamais confondre les niveaux

1. **Publication inspectée (`True`)** : au moins **un** média de cette publication a fait l'objet d'un contrôle visuel documenté ; ce drapeau ne veut pas dire « tous les médias du carrousel ».
2. **Fichiers réellement inspectés** : décompte directement tiré des audits fichier par fichier : **18/18 pour les trois sujets de ce lot** (5 Villino + 7 Bastin + 6 Warocqué). Les **36 drapeaux de publications** du catalogue ne sont **pas** un décompte global de fichiers médias inspectés.
3. **Compositions distinctes** : **5 pour Villino Florio, 5 familles pour Maison Bastin, au moins 5 familles pour Warocqué**, toutes à lire avec leur description et les reprises possibles dans les fiches.
4. **Prises de vue natives indépendantes : INCONNUES.** Un recadrage et un retraitement peuvent générer plusieurs JPEG ; différences de hash et nombre de familles visuelles ne tranchent pas.
5. **Droit de nouvelle réutilisation vérifié : AUCUN** pour les 18 médias du lot, faute de sources natives, d'auteur individuel et d'autorisation documentée. Ne rien changer à `research/media-rights.json` par présomption.

## 3. Trois fiches candidates terminées

- [Villino Florio, Palerme — 5 médias, 5 compositions](villino-florio-2026-09-21.md).
- [Maison Bastin / Maison des Médecins — 7 médias, 5 familles](maison-bastin-2026-09-21.md).
- [Maison de la rue Warocqué — 6 médias, au moins 5 familles](maison-warocque-2026-09-21.md).

Dans les 14 articles de `src/data/articles.json` sur `main`, **aucun article n'a l'une de ces trois identités** ; ce contrôle d'identité ne certifie pas que des photos ressemblantes n'apparaissent dans aucun contenu générique. La recherche ciblée de fichiers image par **nom de sujet** dans le Drive accessible n'a pas identifié d'original natif correspondant : seul un fichier numérique de l'export a été retrouvé sous « Florio ». **Ce résultat limité de recherche par nom n'exclut pas des archives personnelles numérotées, classées autrement ou non accessibles au connecteur.**

## 4. Demande groupée minimale à transmettre à Théodore / Christophe — PROPOSÉE

**Une seule recherche groupée, sans téléversement de toute la photothèque.** Si des originaux ou leurs répertoires sont déjà accessibles à Christophe, fournir **trois liens vers les dossiers source existants**, ou **une sélection ciblée des fichiers originaux** correspondant aux cinq familles visuelles de chacun des trois sujets, soit **jusqu'à quinze familles recherchées** (pas quinze fichiers natifs supposés disponibles).

| Dossier | Références à rapprocher et preuve demandée |
| --- | --- |
| **Villino Florio** | `F0005, F0013, F0017, F0018, F0027` : cinq éléments déjà distincts visuellement ; retrouver le fichier natif correspondant à chacun si disponible. |
| **Maison Bastin** | Famille A : `F0394/F1020` (commencer par **un** original pour vérifier la reprise) ; B : `F0717` ; C : `F0729/F0740` (commencer par **un** original pour vérifier le recadrage) ; D : `F0746` ; E : `F0751`. |
| **Maison rue Warocqué** | Famille A : `F0267/F0586` (commencer par **un** original) ; B : `F0728` ; C : `F0736` ; D : `F0742` ; E : `F0745` (façade entière). |

**Pour les seuls fichiers trouvés et envisagés :** indiquer leur **emplacement source** (lien vers dossier, pas nécessairement copie), le **nom de fichier natif réel**, l'**auteur/ayant droit** de chaque photographie et, s'ils sont disponibles, dimensions/EXIF/date de prise de vue. Préciser si certaines copies Instagram sont issues **du même original**, notamment les paires A/C Bastin et A Warocqué. Indiquer les **usages autorisés** pour le site, le portfolio, un carrousel ou Reel éventuel et toute restriction connue (photographe tiers, intérieur, conditions d'accès ou demande des propriétaires). Une confirmation d'auteur et de droits devra être conservée séparément du catalogue et **validée humainement** avant approbation de médias.

Si des originaux sont introuvables, relever explicitement `NON RETROUVÉ` **par famille**, sans inventer de correspondance ou refaire tout l'export. **Aucune publication, transmission publique ou ajout au registre des droits ne résulte de cette demande.**

## 5. Limites d'accès et état réel de clôture de ce lot

- **Accessible et effectivement consulté :** gouvernance GitHub sur `main` ; quatre rapports C1 et index sur la branche ; ancien ZIP complet, CSV privés et dossier Drive ; 14 articles et registre de droits ; recherche ciblée de noms de fichiers dans Drive. **Nouvelle sauvegarde ZIP/CSV synchronisée déposée et relue dans le même dossier Drive.**
- **Non accessible / non établi pour le présent lot :** copie locale antérieure `ANAD-C1-livrable-final-1431-v2.zip` non présente dans ce dossier Drive ; répertoires natifs HD identifiés de Christophe ; fichier source individuel, auteur, titularité et permission de réutilisation pour chacun des 18 médias ; preuve patrimoniale indépendante des identités/adresses/attributions ; éventuelles restrictions contractuelles de prises de vue intérieures ou chez les propriétaires ; statut Instagram en temps réel et permaliens individuels.
- **Non entrepris volontairement :** nouvelle extraction des 1 431 entrées ; revue des 1 083 entrées incertaines ; vérification des 1 460 fichiers médias ; nouvelles analyses des photos déjà auditées ; modification des scripts ou du site ; fusion, publication, achat, sous-agent et action D1. La sauvegarde privée a été dérivée de la version initiale et des preuves déjà documentées ; **pas d'affirmation d'accès à une v2 absente**.

**Bilan : trois fiches candidates RÉALISÉES, traçabilité des 18/18 médias VÉRIFIÉE, dix marqueurs synchronisés dans GitHub et le Drive privé ; rapprochement des originaux EN COURS et approbation photographique BLOQUÉE.**
