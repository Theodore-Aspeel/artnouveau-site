# ANAD 2.0 — C1 : synthèse synchronisée, qualité web et validation humaine groupée

Date : 2026-09-21. **RÉALISÉ / VÉRIFIÉ : audit technique de 18/18 copies privées, sélection candidate de 14 copies et traçabilité historique ; EN COURS : attribution de l'auteur et droits de réutilisation ; PUBLICATION : NON AUTORISÉE.** Branch C1 / PR #40 documentaire uniquement, aucune modification du site, du registre des droits, de `main` ni du checkpoint D1.

## 0. Correction du prérequis photographique — VALIDÉE par Théodore

**Christophe ne possède pas de photothèque historique distincte de son compte Instagram.** Pour les trois dossiers ici examinés, **les copies privées de l'export Instagram sont les meilleures sources disponibles connues**. La recherche de RAW/JPEG natifs, de noms de fichiers d'origine ou d'EXIF source, et toute nouvelle extraction de l'archive ne sont **plus demandées**. Les passages antérieurs des audits, fiches et rapports qui faisaient de ces natifs une condition sine qua non d'exploitation web sont **OBSOLÈTES pour l'exécution présente**, y compris lorsqu'ils restent conservés comme historique. L'absence de fichiers natifs limite la définition et le potentiel de recadrage ; elle ne bloque **pas** une utilisation web adaptée de la copie Instagram lorsque **qualité, auteur, droits et autorisation de publication** sont établis.

**Quatre états indépendants, sans raccourci :** (1) `COPIE_INSTAGRAM_DISPONIBLE` : **VÉRIFIÉ** pour 18/18 ; (2) `QUALITÉ_WEB` : **VÉRIFIÉE pour usages précis, LIMITÉE ou ÉCARTÉE** selon chaque fiche, sans examen du futur rendu responsive ; (3) `PROVENANCE_ET_DROITS` : **À CONFIRMER** sur les 14 copies retenues auprès de Christophe ; (4) `PUBLICATION_AUTORISÉE` : **NON**, en attente d'une validation humaine ultérieure explicite du contenu et de sa diffusion. Même un « oui, je suis auteur et j'accepte la réutilisation » ne constitue pas une instruction de publier maintenant.

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
5. **Droit de nouvelle réutilisation vérifié : AUCUN** pour les 18 médias du lot : l'auteur individuel et les permissions applicables restent à confirmer auprès de Christophe. L'absence de fichiers natifs distincts n'est pas un motif de blocage pour un usage web adapté des copies. Ne rien changer à `research/media-rights.json` par présomption.


## 3. Trois sélections web candidates — 18 copies expertisées, 14 retenues (PROPOSÉ)

Les trois fiches ci-dessous remplacent leurs versions exigeant des « originaux » et réutilisent les audits des compositions déjà effectués ; **aucune nouvelle extraction de l'archive**. Dimensions, volumes, observations de lisibilité et tailles CSS adaptées sont indiqués **par fichier** dans chaque fiche. Pour éviter les doublons, un thème architectural répété ne devient pas une photographie indépendante du seul fait que son export possède un autre chemin ou un autre hash.

| Dossier / fiche | Copies ouvertes | Sélection candidate pour maquette web | Alternatives privées non retenues | Limite principale |
| --- | ---: | --- | --- | --- |
| [Villino Florio](villino-florio-2026-09-21.md) | **5/5** | **F0027** (façade, principale cadrée), **F0005** (escalier), **F0013** (cheminée), **F0018** (vitrail), **F0017** (terrasse, vignette facultative). **5 compositions**. | Aucune exclue par qualité ; F0017 seulement secondaire. | Les 1 440 px de large limitent une bannière panoramique/plein écran ; F0017 renseigne peu l'identité du bâtiment. |
| [Maison Bastin](maison-bastin-2026-09-21.md) | **7/7** | **F0394** (façade), **F0717** (oriel, vignette), **F0729** (vitrail), **F0746** (intérieur), **F0751** (portes, vignette). **5 familles**. | **F1020** (quasi-même façade que F0394), **F0740** (même vitrail que F0729, copie 806 px très sombre). | F0717 : 756 px ; F0729 : fort contre-jour ; F0746 et F0751 : profondeur/hautes lumières et douceur. |
| [Maison rue Warocqué](maison-warocque-2026-09-21.md) | **6/6** | **F0745** (façade, principale encadrée), **F0586** (grue), **F0742** (paon), **F0736** (baie, vignette). **4 familles**. | **F0267** (quasi-même panneau de grue que F0586), **F0728** (verrière distincte mais hautes lumières sévèrement écrêtées). | Image générale 1 080 px de large : pas de grand hero ni fort zoom ; F0736 relativement douce. |
| **Total** | **18/18** | **14 copies, dans des usages web adaptés** | **4 copies non sélectionnées** | Ni vingt vues indépendantes, ni quatorze auteurs et droits confirmés. |

**Contrôle de qualité :** 18 fichiers ouverts localement et mesurés ; formats visuellement lisibles en galerie de taille raisonnable ; métrique comparative de netteté utilisée seulement en soutien à la revue humaine des images. Les pixels source sont comptés ; **la netteté perçue dépend aussi du contenu photographié, des zones uniformes, du JPEG et de la taille de restitution**. Pas de garantie de rendu final avant maquette responsive, ni de restauration réelle des blancs brûlés ou des noirs bouchés. La copie F0267, dont le chemin export comporte un suffixe `.webp`, a été mesurée sur la version JPEG matérialisée par l'accès Drive ; ces mesures ne certifient pas le format binaire de l'objet WEBP d'origine. Aucun média privé ou planche-contact ne figure dans la PR.

## 4. Une seule demande privée groupée à adresser à Christophe — PRÉPARÉE, NON ENVOYÉE

La planche de sélection **privée** des 14 copies, préparée séparément **hors GitHub public**, porte les références ci-dessus et montre les vignettes. À transmettre à Christophe uniquement par un canal privé lors d'une **unique revue des trois séries**. Si cette planche n'est pas disponible dans un futur contexte, utiliser les dates, ordres et descriptions des trois fiches pour récupérer les images dans le Drive privé **sans relancer l'extraction HTML**. Ne pas déposer cette planche ni les copies sur GitHub.

> Christophe, nous avons préparé trois séries de photos à partir des copies Instagram disponibles, pour éventuellement présenter ton travail sur le site Art Nouveau et Déco. Peux-tu regarder **une seule fois la planche privée des 14 images** et nous confirmer, **pour chaque image proposée**, si tu as personnellement pris la photographie, si elle provient d'un autre photographe ou si tu n'es plus certain de sa provenance ?
>
> **Villino Florio :** F0027, F0005, F0013, F0018 et F0017 (facultative). **Maison Bastin :** F0394, F0717, F0729, F0746 et F0751. **Rue Warocqué :** F0745, F0586, F0742 et F0736.
>
> Pour les photos dont tu es bien l'auteur ou pour lesquelles tu disposes d'une autorisation applicable, nous confirmes-tu la possibilité de les **réutiliser sur le site ANAD (article et portfolio)**, en te créditant comme photographe lorsque c'est exact ? Peux-tu préciser séparément si une reprise en **carrousel Instagram** et dans un **Reel** serait permise, ou si certains usages doivent rester exclus ? Y a-t-il des restrictions connues liées aux intérieurs de Villino Florio / Maison Bastin ou à l'accès et aux propriétaires de la maison rue Warocqué ?
>
> Si une photographie vient d'un tiers, merci de nous indiquer, si tu le sais, **qui en est l'auteur** et si tu disposes d'une permission explicite couvrant l'usage envisagé. En cas de doute, indique simplement « auteur ou droits incertains » : nous ne retiendrons pas cette image pour publication. **Nous ne te demandons aucun RAW, JPEG d'origine ou dossier photographique supplémentaire ; les copies Instagram suffisent au contrôle technique actuel. Il n'y aura aucune publication automatique après ton retour.**

**Crédits tiers explicites dans ces 18 légendes :** aucun signalé par les audits des trois sous-ensembles ; **cela n'établit ni paternité ni autorisation**. D'autres dossiers C1 (Jardin d'hiver des Ursulines, Les Chardons, magasin Niguet, etc.) contiennent des crédits tiers explicites et **ne sont pas mêlés à cette demande groupée**. Si Christophe identifie un crédit ou une provenance tierce concernant une des 14 copies, l'isoler dans la fiche, retirer la photo de la présélection et conserver séparément la preuve d'une éventuelle autorisation **avant tout changement du registre des droits**.

## 5. Limites opérationnelles et état du lot

- **Couverture :** 18/18 copies des **trois dossiers désignés**, pas 18/1 460 images évaluées au hasard ; le catalogue structurel couvre **1 431 entrées**, dont 1 083 restent ambiguës/inconnues au classement de l'index. Les dix dossiers multi-compositions documentés par les audits ne sont ni dix sites validés juridiquement ni un inventaire photo exhaustif.
- **Prises originales et comparaison :** la source originale de prise de vue n'existe pas sous la forme d'un fichier séparé accessible ; il est donc parfois impossible de distinguer une reprise/crop d'une prise indépendante. Nous retenons **un représentant par famille visuelle**, plutôt que d'affirmer un nombre invérifiable de déclenchements photographiques. Une copie de faible définition ne peut être agrandie sans perte réelle de détails.
- **Identités et autorisations :** les légendes Instagram ne certifient pas seules l'identité patrimoniale ni les auteurs des photos. Aucune réponse de Christophe, aucun droit photographique individuel, aucune autorisation de publication, aucun droit relatif aux intérieurs ou à la propriété privée n'a été vérifié dans ce lot. Le consentement de Christophe en tant que photographe ne constitue pas à lui seul une vérification de toutes les éventuelles restrictions contractuelles connues.
- **Diffusion :** la planche privée et les 18 copies restent **hors du dépôt public** ; `research/media-rights.json`, les articles, les états de publication, D1 et `main` ne sont pas modifiés. La PR #40 reste en brouillon. Aucun envoi à Christophe ni publication, dépense, installation, fusion ou nouvelle recherche générale sur les outils n'a été effectué.

**Sortie concrète : trois fiches corrigées, qualité web individualisée pour 18 copies, présélection de 14 compositions et une seule demande de revue groupée prête à être transmise en privé.** La validation humaine de provenance/droits reste **EN ATTENTE** ; toute décision ultérieure de publication reste à obtenir explicitement.
