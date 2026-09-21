# ANAD 2.0 — C1 : rapprochement archives et extension du catalogue par sujet

> **CORRECTION DU PRÉREQUIS PHOTOGRAPHIQUE — VALIDÉE le 21-09-2026 :** Christophe ne conserve pas d'originaux photographiques historiques dans une photothèque distincte d'Instagram. Les anciennes demandes de fichiers RAW/JPEG natifs ou les formulations faisant de leur absence un blocage absolu sont **OBSOLÈTES** ; ne pas lancer de nouvelle extraction de l'archive ni rechercher une photothèque séparée. Les copies privées Instagram sont la source disponible ; une exploitation web de taille adaptée est **techniquement envisageable** selon la qualité de chaque copie, sous réserve de validation **individuelle de la provenance et des droits** puis d'une **autorisation humaine de publication distincte**. Pour les trois séries Villino Florio, Maison Bastin et rue Warocqué, le référentiel opérationnel à jour est constitué des fiches et de `research/c1-candidates/synchronisation-et-demande-groupee-2026-09-21.md` sur cette branche C1. Le présent rapport conserve ses observations et limites historiques indépendantes de cette correction.

Date : 2026-09-21. Statut : **RÉALISÉ — extraction ciblée et rapprochement des HTML ; VÉRIFIÉ pour les décomptes et correspondances indiqués ; EN COURS pour le catalogue nominatif exhaustif et les droits**.

**État cumulatif actualisé :** après l'examen cumulatif des **18 images** des séries Maison Losseau, Maison Bastin et Villino Florio (dont quatre déjà contrôlées dans le premier lot), **dix nouveaux sujets** ont plusieurs compositions visuellement vérifiées dans les copies exportées. Le dixième est **Villino Florio** ; les six médias Losseau et sept Bastin ont maintenant été examinés dans leur intégralité et leurs cadrages proches explicités. Lire `research/c1-instagram-series-and-limitations-2026-09-21.md`, dont la section **« Limites de l'analyse » doit accompagner tout transfert au pilotage**. Le rapport intermédiaire `research/c1-instagram-multiview-series-audit-2026-09-21.md` documente l'étape précédente à neuf sujets et 16 fichiers examinés. **Aucun dossier source natif ni droit de publication supplémentaire validé.**

Ce document **complète** `research/c1-instagram-inventory-2026-09-21.md` (baseline Metricool sur `main`) et `research/c1-instagram-export-first-pass-2026-09-21.md` (premier lot de l'export sur cette branche). Il précise une limite désormais résolue dans le premier lot : les entrées sans chemin `media/posts/` sont des publications archivées avec des médias rangés sous `media/archived_posts/`, et non nécessairement des images manquantes. Les nombres par bâtiment ci-dessous sont des **repérages qualifiés**, pas des statistiques exhaustives du feed ou des droits prouvés.

## 1. Réconciliation de l'export officiel : trois vues d'un même historique

- `your_instagram_activity/media/posts.html` : **1 431 entrées de premier niveau datées** (et non les 46 420 conteneurs imbriqués). C'est la vue de l'historique principal incluant les archives.
- `your_instagram_activity/media/posts_1.html` : **1 162 entrées datées**, avec **1 190 chemins de médias distincts** `media/posts/` (1 152 entrées avec un chemin, dix entrées avec plusieurs).
- `your_instagram_activity/media/archived_posts.html` : **269 entrées datées**, avec **270 chemins de médias distincts** `media/archived_posts/` (268 entrées avec un média, une avec deux).
- **VÉRIFIÉ : chacune des 269 entrées du fichier d'archives correspond à une et une seule des 269 entrées supplémentaires dans `posts.html`**, en rapprochant date civile et début de légende normalisé ; aucune des 269 n'est orpheline ou ambiguë avec cette clé. La distribution des entrées archivées est : 2019 : 249 ; 2020 : 11 ; 2021 : 6 ; 2022 : 2 ; 2024 : 1.
- Ainsi, **1 162 + 269 = 1 431 entrées historiques datées**, classées comme non archivées ou archivées dans **l'export à cette date**. Ce ne sont pas 1 431 publications actuellement visibles dans la grille Instagram ; leur statut en ligne n'a pas fait l'objet d'un contrôle Instagram temps réel.
- Dans `posts.html`, **1 190 chemins de médias de `posts_1.html` sont déjà présents**, auxquels s'ajoutent 11 chemins `media/posts/` ; un des onze est associé à une entrée archivée du 24-06-2019 (légende « Hairdresser »). **Ne pas additionner les 1 201 chemins du fichier détaillé aux 1 190 du fichier simplifié**, et ne pas présumer que les dix autres fichiers supplémentaires constituent dix publications supplémentaires. L'archive a son répertoire de médias distinct, ce qui rend les anciennes mentions « 268 posts sans médias » **obsolètes** en tant que diagnostic de fichiers absents.
- `reels.html` : **69 repères datés** et **72 chemins de médias distincts** ont été observés. Les 93 occurrences du conteneur HTML ne sont **pas** 93 Reels individuels : certaines sont imbriquées. Un contrôle de liaison Reel → post photo et du contenu audiovisuel reste à effectuer ; ne pas additionner ces 69 à la population des 1 431 sans analyse de chevauchement.

Clé d'audit interne : `feed #N` désigne le N-ième bloc de publication daté dans `posts_1.html` ; `archive #N` désigne le N-ième bloc daté dans `archived_posts.html`. **Aucun de ces ordinaux ne doit être présenté comme un ID ou permalink Instagram.** Les liens Metricool déjà consignés dans l'inventaire initial restent les seuls permaliens individuellement établis dans les premiers lots.

## 2. Extension vérifiable du catalogue par identité de bâtiment

Méthode : regroupements explicites par appellation et variantes déjà trouvées dans les légendes ; exclusion des simples mentions d'un architecte pouvant désigner plusieurs bâtiments. Les comptes et références concernent les **occurrences identifiées**, donc des minima d'inventaire qui peuvent évoluer avec la résolution des légendes génériques. `Médias` = nombre de chemins associés aux occurrences du groupe, **ni nombre d'angles distincts ni nombre d'originaux natifs**.

| Bâtiment ou ensemble identifié par légende | Non archivées | Archivées | Médias associés | Repères vérifiables et état |
| --- | ---: | ---: | ---: | --- |
| Maison Piot / Maison des Francs-Maçons | 9 | 1 | 10 | feed #338, #522 ; archive #17. Nouveau sujet, images et droits à examiner. |
| Maison Bastin / Maison des Médecins | 7 | 0 | 7 | feed #394, #717. Nouveau sujet ; lieux/angles à confirmer sur fichiers. |
| Maison Losseau, Mons | 6 | 0 | 6 | feed #483, #499 ; légende de #499 explicitement consacrée à l'entrée. Nouveau sujet. |
| Maison De Poore | 4 | 1 | 5 | feed #153, #551 ; archive #106. Identité de lieu et fichiers à vérifier avant sélection. |
| Maison Bacot / Maison Pirnay / Maison Gentry | 4 | 1 | 5 | feed #400, #569 ; archive #14. Variantes dénommées conjointement dans la légende ; lieu et corpus à contrôler. |
| Casa Galimberti, Milan | 4 | 0 | 4 | feed #781, #786. Nouveau sujet, vues non contrôlées. |
| Casa Campani, Milan | 3 | 0 | 3 | feed #457, #626. Ne pas confondre avec Casa Campanini, qui est un autre sujet du corpus GitHub. |
| Anciens magasins Waucquez / Centre de la bande dessinée, Bruxelles | 4 | 0 | 4 | feed #670, #693. Nouveau sujet, quatre occurrences identifiées. |
| Jardin d'hiver des Ursulines, Malines | 4 | 0 | 4 | feed #280, #350. #280 mentionne explicitement des « vues » précédemment partagées ; les images distinctes restent à vérifier. |
| Maison personnelle d'Édouard Frankinet | 2 | 0 | 2 | feed #512, #543. Identification et lieu exact à corroborer. |
| Villa Olga, Blankenberge | 2 | 0 | 2 | feed #595, #663. Nouveau sujet ; doublon potentiel à examiner. |
| Immeuble Les Chardons, Paris | 2 | 0 | 2 | feed #371, #602. Les deux légendes remercient un tiers : **droits à examiner en priorité, pas une ressource réputée appartenir à Christophe**. |
| Palau de la Música Catalana / Palais de la Musique Catalane, Barcelone | 4 | 0 | 4 | feed #110, #128. Nouveau sujet ; vue intérieure et lieu à confirmer pour chaque image. |
| Teatro / Théâtre Kursaal Santalucia, Bari | 3 | 0 | 3 | feed #123, #127. Nouveau sujet ; variantes d'appellation rapprochées. |
| Palazzo della Gazzetta, Bari | 1 | 0 | 3 | feed #152. Trois médias du même post, mais la légende parle de vestiges et crédite un tiers pour des informations ; vérifier les photos et l'identification de chacune. |
| Maison Huot, Nancy | 6 | 0 | 6 | feed #9, #28, #60, #82, #85, #87. **Deux compositions distinctes réellement vérifiées au lot précédent**, 4 autres images à comparer ; nouveau sujet. |
| Casina Cinese / Palazzina Cinese, Palerme | 3 | 0 | 5 | feed #12, #29, #31. **Trois compositions intérieures distinctes vérifiées** au lot précédent ; nouveau sujet. |
| Maison Spitzer, Budapest | 2 | 0 | 4 | feed #59, #150. **Trois compositions distinctes vérifiées** au lot précédent ; nouveau sujet. |
| Villino Florio, Palerme | 5 | 0 | 5 | feed #5, #13, #17, #18, #27. Nouveau sujet ; distinctivité des cinq images non vérifiée. |
| Maison Saint-Cyr, Bruxelles | 7 | 0 | 7 | feed #49, #205, #217, #237, #489, #615, #707. Nouvelle piste ; au moins une légende attribue explicitement une photo à un tiers. |
| Maison Cauchie, Bruxelles | 9 | 0 | 9 | Plusieurs occurrences `Maison Cauchie` ; exclure les légendes sur **d'autres œuvres de Paul Cauchie**. Nouveau sujet, droits hétérogènes possibles. |
| Maison Coilliot, Lille | 9 | 2 | 11 | feed #62, #215 ; archive #7, #70. **Article existant et hors nouvelle shortlist C1.** |
| Maison Delune | 15 | 2 | 17 | feed #10, #251 ; archive #2, #27. **Attention : « Château Feys / Château Solbosch » et maison de l'architecte Ernest Delune pour un maître verrier ne sont pas nécessairement le même bâtiment.** Le chiffre est un ensemble de mentions Delune à **scinder par adresse/identité** avant toute utilisation comme série photographique. Sujet(s) déjà couverts en partie par l'article existant, ne pas assimiler les dix-sept fichiers à un seul bâtiment. |
| Palais de la Sécession, Vienne | 12 | 1 | 13 | feed #313, #327 ; archive #45. Article existant. |
| Maison des Hiboux, Saint-Gilles | **3** | 0 | **3** | feed #271, #393, #1120. Le premier lot ne comptait que la mention française exacte #1120 ; deux légendes en anglais « Les Hiboux house » ont été rapprochées. **Article existant**, pas nouveau sujet. |
| Maison aux Tulipes, Bratislava | 1 confirmée | 1 candidate à réconcilier | 1 + 1 candidate | feed #1124 ; archive #262 « Tulip house » : le nom générique seul ne permet pas de certifier le même bâtiment. Article existant. |
| Ancienne chemiserie / magasin Niguet, Bruxelles | 5 | 1 | 6 | feed #216, #341 ; archive #9. La légende archivée crédite explicitement une source tierce pour sa photo ; nouveau sujet, droits non présumés. |
| Chalet des Bruyères | 1 | 0 | 2 | feed #620 : publication multi-médias ; nouveau sujet à vérifier visuellement. |
| Pavillon aquarium de l'École de Nancy | 1 | 0 | 6 | feed #72 : publication multi-médias, six images associées, angles et sources non inspectés ; nouveau sujet. |

**Corrections et avertissements par rapport aux recherches approximatives :** les trois mentions de « Maison des Hiboux » incluent deux intitulés en anglais ; une même référence à « Paul Cauchie » ne prouve pas qu'il s'agit de la Maison Cauchie ; une légende qui compare la librairie de Gand à la Maison Bergeret ne constitue pas un post photographique de la Maison Bergeret. Le regroupement « Delune » doit être **scindé**, car plusieurs bâtiments peuvent partager ce nom d'architecte et des appellations proches. La Maison Strauven à Tournai doit être distinguée de la Maison Saint-Cyr à Bruxelles et, à Tournai, l'adresse Van Cutsem 19 de l'adresse 27/29. Aucun compte global d'occurrences issu d'une requête libre sur « Strauven » n'est validé par bâtiment.

## 3. Choix de prochains contrôles C1 (PROPOSÉ, aucun usage autorisé)

**Nouvelles pistes additionnelles à inspecter visuellement par sous-ensemble** : Maison Losseau (porte d'entrée + vues), Maison Piot (10 chemins), Maison Bastin (7), Maison Bacot/Pirnay/Gentry (5), Jardin d'hiver des Ursulines (4), Villa Olga (2) et Chalet des Bruyères (2). Ce sont des **candidats de preuve**, non un classement éditorial ni une confirmation d'angles ou de droits. Les trois premiers dossiers visuellement contrôlés du premier lot (Casina Cinese, Spitzer, Huot) restent les seuls de cet inventaire pour lesquels plusieurs cadrages photographiques ont réellement été examinés.

**Contrôles à effectuer dans le cadre C1 :** pour chaque sujet, vérifier un à un les fichiers d'export et leur identité spatiale, repérer les images identiques réutilisées, puis rechercher la correspondance avec les vrais fichiers natifs et les autorisations individuelles. La présence d'un JPEG dans l'export officiel établit la présence d'une **copie exportée**, non l'original HD, l'auteur, la titularité ni un feu vert de publication. Les légendes contenant des crédits de photographes tiers imposent une vérification spécifique. Un nom d'architecte, une année de construction, une attribution et une adresse tirés des légendes restent **à confirmer par recherche documentaire indépendante** avant rédaction.


## 3 bis. Contrôle visuel additionnel de quatre JPEG de l'export — VÉRIFIÉ

Deux nouveaux sujets du catalogue possèdent désormais **au moins deux compositions distinctes effectivement examinées**, en plus des trois sujets déjà vérifiés dans le premier lot :

| Sujet | Publications et fichiers de l'export comparés | Observation visuelle directement contrôlée | Portée de la preuve |
| --- | --- | --- | --- |
| **Maison Losseau, Mons** | feed #483 (06-04-2021, `media/posts/17937998227486818.jpg`) et feed #499 (19-03-2021, `media/posts/202103/17905530085745430.jpg`) | #483 montre un gros plan d'une verrière colorée ornée de motifs floraux ; #499 montre le décor floral doré d'une porte/grille vitrée. Ce sont **deux compositions clairement distinctes**, associées au même sujet par leurs légendes. | **Deux vues distinctes de détails** vérifiées dans les copies exportées. Aucune vue d'ensemble ni preuve de natifs HD, d'auteur ou de droits issue de ce seul contrôle. |
| **Maison Bastin / Maison des Médecins** | feed #394 (14-11-2021, `media/posts/17925798670840061.jpg`) et feed #717 (15-09-2020, `media/posts/18161997109033317.jpg`) | #394 montre la façade entière et son oriel ; #717 un gros plan de ce même élément en saillie et de son balcon. **Deux cadrages différents, avec recoupement architectural visible**. | **Deux vues distinctes**, dont une façade entière et un détail vérifiés sur des copies Instagram ; originaux HD, auteur et droits non vérifiés. |

Ces contrôles reposent sur l'ouverture des quatre JPEG présents dans `media/posts/` sur le dossier Drive de l'export, sans les copier dans GitHub. Les filigranes du compte et la présence de ces images dans l'export ne prouvent pas, à eux seuls, que Christophe est l'auteur ou dispose des autorisations nécessaires. Les autres images attribuées à ces bâtiments (respectivement six et sept au total) **n'ont pas encore été examinées visuellement**.

**Bilan photographique C1 après ce contrôle : cinq dossiers de nouveaux sujets comportent plusieurs compositions visuellement vérifiées dans les fichiers exportés : Casina Cinese, Maison Spitzer, Maison Huot, Maison Losseau et Maison Bastin.** Aucun n'est encore un dossier source approuvé pour publication faute de lien aux originaux et de contrôle individuel des droits.


## 3 ter. Nouveau contrôle de vues et triage de provenance — VÉRIFIÉ pour les JPEG et déclarations des légendes

**Maison Piot / Maison des Francs-Maçons : sixième dossier source multi-compositions vérifié dans l'export.** Deux fichiers de deux publications ont été réellement ouverts et comparés : `feed #338`, 30-03-2022, `media/posts/17943669562790454.webp` (copie exportée fournie en aperçu JPEG), montre l'entrée complète et les deux reliefs latéraux ; `feed #522`, 01-03-2021, `media/posts/202103/17888731474991559.jpg`, cadre un vitrail géométrique au-dessus d'une ouverture, sans montrer l'ensemble de l'entrée précédente. **Les deux compositions sont distinctes**, associées à la Maison Piot par leurs légendes. L'appartenance de chaque détail au bâtiment est attestée par la légende de son post, non par une expertise architecturale indépendante. Sur les **9 posts non archivés et 1 post archivé (10 médias)** du groupe, seuls ces deux fichiers ont été examinés visuellement. Ni natifs HD ni titularité des droits individuels ne sont vérifiés. Le filigrane du compte ne vaut pas preuve de photographie originale.

**Casa Galimberti, Milan : deux fichiers distincts examinés, mais plusieurs angles NON VÉRIFIÉS.** `feed #781` (08-07-2020, `media/posts/17870526259826346.jpg`) et `feed #786` (04-07-2020, `media/posts/17860487815991427.jpg`) présentent des éléments décoratifs différents autour d'une fenêtre et d'un balcon, mais avec une perspective et un cadrage très similaires. Ce sont deux médias **et deux décors différents**, pas une démonstration d'angles photographiques différents. Deux fichiers contrôlés sur les quatre publications du sujet ; vue de façade entière et originaux natifs inconnus.

### Nouvelles notices de sujets repérés, non encore éligibles

Les `F#` désignent les positions dans `posts_1.html` ; `A#` celles dans `archived_posts.html`. Le nom de ville provient de la légende/hashtags, non d'une vérification patrimoniale indépendante.

| Sujet / catégorie | Posts F / A et chemins associés | Références de vérification | Limite et prochaine preuve |
| --- | ---: | --- | --- |
| Maison Paon, Gand | 2 / 0 ; 2 médias | F749 (19-08-2020), F810 (05-06-2020) | Même appellation dans les deux légendes, angles/doublons, auteur et identité spatiale à vérifier. |
| Façade Art Déco, Mouscron | 3 / 0 ; 3 médias | F636 (29-11-2020), F655 et F656 (14-11-2020) | Légendes très génériques et quasi identiques : **ne pas certifier un bâtiment unique** sans inspection des photographies et adresse. |
| Façade Art Déco, Tournai | 3 / 0 ; 3 médias | F723 (10-09-2020), F755 (14-08-2020), F761 (06-08-2020) | Regroupement lexical seulement ; ne pas fusionner avec un dossier Strauven ni certifier même façade. |
| Façade associée à Georges De Porre, Tournai | 2 / 0 ; 2 médias | F426 (07-08-2021), F1128 (17-11-2019) | Une légende indique place Victor-Carbonnelle et l'autre le n° 5 : hypothèse de rapprochement **PROPOSÉE**, adresse et vues à vérifier sur photographies/sources. |
| Musée La Piscine, Roubaix | 6 / 0 ; 6 médias | F392, F523, F685, F715, F732, F739 | Six occurrences mentionnant le musée, mais aucune série d'angles ni droits prouvés ; distinguer édifice, exposition et œuvres photographiées. |
| Musée Horta, Bruxelles | **3** occurrences nominatives directes non archivées et **1** archivée ; au moins 4 médias | F360, F644, F734, A6 | Ne **pas** compter F488 (annonce sur l'Hôtel/Musée Hannon où le Musée Horta n'est cité que comme partenaire). F644 crédite explicitement une photographie à un tiers. Cette correction supplante le regroupement automatisé de 5 mentions plus haut. |
| Hôtel Ciamberlani, Bruxelles | 1 / 0 ; 1 média | F811 (04-06-2020) | Sujet nominal autonome, multi-vues non démontré. |

### Risques de droits identifiés dans les légendes, à ne pas noyer dans le volume

| Sujet | Mentions explicites à isoler | Conséquence pour C1 |
| --- | --- | --- |
| Jardin d'hiver des Ursulines, Malines | **4/4 occurrences** F280, F350, F747, F754 comportent des crédits photographiques ou institutionnels à des tiers dans leurs légendes. | **BLOQUÉ pour présélection comme corpus photographique original de Christophe** : ne pas traiter les quatre médias comme librement réutilisables ; rechercher indépendamment les éventuels originaux de Christophe, s'ils existent. |
| Immeuble Les Chardons, Paris | **2/2 occurrences** F371 et F602 créditent des tiers. | Photographies publiées ≠ photographies de Christophe ; ne pas intégrer comme corpus d'origine sans autorisation vérifiée. |
| Ancienne chemiserie / magasin Niguet, Bruxelles | **3 occurrences sur 6** (F396, F432 et A9) mentionnent explicitement une photographie fournie par un tiers ; F216, F341, F365 restent sans provenance individuelle prouvée. | Scinder les images par auteur/autorisation ; ne pas extrapoler les droits du compte à l'ensemble du groupe. |
| Maison Saint-Cyr, Bruxelles | F489 et F615 signalent un crédit/une réutilisation de photographie d'autrui dans leurs légendes ; sept médias avaient été regroupés. | Vérifier les droits média par média, même si plusieurs fichiers montrent la même façade. |
| Maison Horta / Musée Horta | F644 crédite la photographie d'un tiers ; F488 ne photographie pas nécessairement le Musée Horta. | Corriger la catégorie avant toute présélection et ne pas attribuer un cliché crédité à Christophe. |

Les mentions de crédit constituent des **indices explicites de provenance tierce**, et non une décision juridique sur la portée d'éventuelles licences ou autorisations. L'absence de crédit n'établit **jamais** l'auteur ni les droits d'un autre fichier. Les six dossiers ayant des compositions distinctes confirmées à ce stade sont : **Casina Cinese, Maison Spitzer, Maison Huot, Maison Losseau, Maison Bastin et Maison Piot**. **Zéro dossier source validé pour publication** : la correspondance avec des photographies natives/HD et les droits par fichier restent ouverts.

## 4. Confidentialité, domaine D1 et tests

Cet enrichissement GitHub ne contient **aucun HTML brut, fichier photo/vidéo, commentaire brut, métrique privée ou export complet des légendes**. Il ne crée aucun fichier dans le runtime du site, ne modifie ni le premier inventaire intégré à `main` ni les documents/checkpoints D1, ne fusionne ni ne publie quoi que ce soit. Les tests de build et validation npm ne sont pas requis pour ce lot **strictement documentaire** ; seule la lecture de retour du nouveau document sur la branche est prévue.
