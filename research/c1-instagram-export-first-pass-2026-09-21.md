# ANAD 2.0 — C1 : premier lot vérifié de l'export officiel Instagram

Date : 2026-09-21. Statut : **EN COURS — lot A chiffré VÉRIFIÉ, lot B échantillonné VÉRIFIÉ, lot C structure VÉRIFIÉE**. Ce document complète, sans remplacer, `research/c1-instagram-inventory-2026-09-21.md`.

## Périmètre et précautions

Source privée consultée en lecture seule : dossier Drive de l'export HTML décompressé du compte `@artnouveauetdeco`, `your_instagram_activity/media/posts.html`, `posts_1.html` et `your_instagram_activity/comments/post_comments_1.html`. Le dépôt ne reçoit **aucun HTML brut, aucune photographie, aucun commentaire brut, aucune archive**. Les légendes sont des déclarations du compte, non des sources patrimoniales indépendantes. Les liens Instagram confirmés antérieurement via Metricool restent dans le premier inventaire C1. L'export HTML examiné ici n'a pas fourni de permaliens Instagram exploitables dans `posts_1.html`.

Référence de gouvernance lue sur `main` avant le lot : `AGENTS.md`, `research/ANAD-PROJECT-STATE.md` (D12/D13), le premier inventaire C1 et `research/anad-2-execution-reset-2026-09-21.md`. **Aucun fichier D1/checkpoint, article, média runtime ou statut de publication modifié.**

## A — Comptage structurel et chevauchement

| Mesure | posts.html | posts_1.html |
| --- | ---: | ---: |
| Entrées individuelles datées | **1 431** | **1 162** |
| Entrées avec ≥ 1 chemin de média local dans le HTML | 1 163 | 1 162 |
| Entrées sans chemin local exploitable dans le HTML | 268 | 0 |
| Références de chemins de médias distincts par fichier | 1 201 | 1 190 |
| Publications avec plusieurs chemins associés dans le fichier simplifié | Non transposable directement : métadonnées imbriquées | **10** |

La version détaillée `posts.html` comprend 46 420 occurrences d'un conteneur HTML également utilisé pour les **sous-sections imbriquées** ; il est erroné de les compter comme posts. Chaque entrée de premier niveau a été délimitée par son repère final de date et l'association des médias a été calculée au sein de ce segment. `posts_1.html` possède 1 162 blocs de publication datés, avec une légende dans chaque bloc ; 1 152 comportent un média et 10 plusieurs médias (distribution : 3 × 2, 4 × 3, 1 × 4, 1 × 6, 1 × 10). Les 1 190 chemins du fichier simplifié sont tous présents dans `posts.html` ; **ne pas additionner les deux fichiers**. Le fichier détaillé référence 11 chemins supplémentaires. Les 268 entrées sans chemin `media/posts/...` possèdent des métadonnées textuelles, notamment date et légende : leur absence de chemin n'établit pas une absence de publication ni de photographie. Faute d'identifiant/permalien par ligne et de rapprochement systématique des 268 entrées, **1 431 est le nombre d'entrées datées du fichier principal, pas une certification d'unicité de 1 431 posts Instagram vivants**.

Distribution des entrées datées de `posts.html` : 2019 : 349 ; 2020 : 474 ; 2021 : 230 ; 2022 : 122 ; 2023 : 46 ; 2024 : 85 ; 2025 : 105 ; 2026 (jusqu'au 10 août) : 20. Période visible : 5 avril 2019 au 10 août 2026. L'heure des deux variantes HTML d'une même entrée peut différer de quelques minutes ; la date et le chemin média sont des clés de rapprochement plus prudentes que la minute exacte.

**Portée de l'extraction qualitative à ce stade** : premier regroupement par légendes du **sous-ensemble de 1 162 publications `posts_1.html`**, non un catalogue nominatif exhaustif des 1 431 entrées. Les champs date, légende et chemins locaux ont été lus pour chacun des 1 162 blocs ; le classement architectural ci-dessous est un lot vérifiable ciblé. Les 268 entrées sans chemin, les 11 chemins supplémentaires, Reels, archives et Stories ne sont pas encore réconciliés par sujet.

## B — Regroupements ciblés et éligibilité des nouvelles pistes

Les chiffres ne dénombrent que les correspondances identifiées et classées dans `posts_1.html`. Une mention d'architecte seul, un hashtag thématique ou la comparaison avec un autre bâtiment ne prouve pas l'identité du sujet : les correspondances ambiguës sont exclues.

| Sujet nommé dans les légendes | Posts / médias associés | Repère(s) dans posts_1.html | Couverture dans les 14 articles existants | Observation |
| --- | ---: | --- | --- | --- |
| Maison Huot, Nancy | 6 / 6 | #9, #28, #60, #82, #85, #87 | absente | Façade, fenêtre principale et entrée sont explicitement évoquées. Deux images du dossier réellement examinées : façade entière et porte en gros plan, compositions distinctes. |
| Villino Florio, Palerme | 5 / 5 | #5, #13, #17, #18, #27 | absente | Plusieurs fichiers/posts ; angles non vérifiés. |
| Casina Cinese / Palazzina Cinese, Palerme | 3 / 5 | #12, #29, #31 | absente | Les trois médias de #29 sont présents dans le dossier Drive et ont été examinés : vue d'ensemble d'une pièce décorée, perspective sur une arcade, détail du décor peint sous l'arcade. **Trois compositions différentes VÉRIFIÉES, dans l'intérieur attribué par la légende à la Casina Cinese.** |
| Maison Spitzer, Budapest | 2 / 4 | #59, #150 | absente | Les trois médias de #150 sont présents et examinés : hall/perspective, détail de sculpture et relief décoratif. **Trois compositions différentes VÉRIFIÉES** ; quatrième fichier associé à #59 (entrée) non contrôlé visuellement. |
| Maison Saint-Cyr, Bruxelles | 6 explicites / 6 | #205, #217, #237, #489, #615, #707 ; #49 à réconcilier | absente | Plusieurs posts ; une légende crédite explicitement un tiers. Ne pas confondre avec d'autres œuvres de Strauven. |
| Maison Cauchie, Bruxelles | 9 mentions explicites / 9 | dont #238, #389, #480, #565, #598, #605, #676, #753 | absente | Les mentions de Paul Cauchie seul ne suffisent pas : il a décoré d'autres immeubles. Une légende remercie un tiers pour une photographie. |
| Pavillon aquarium, Nancy | 1 / 6 | #72 | absent comme article dédié | Six médias associés à un pavillon décrit dans la légende ; angles et identité exacte des vues non examinés. |
| Palais de la Sécession, Vienne | 12 / 12 | dont #313, #327, #705 | **article existant** | Au moins une légende indique façade latérale ; pas un nouveau sujet. |
| Maison Coilliot, Lille | 9 / 9 | dont #62, #215, #282 | **article existant** | Hors shortlist C1 ; ne pas reprendre le cycle. |
| Maison des Hiboux / Maison aux Tulipes | 1 / 1 chacune | #1120 / #1124 | **articles existants** | Correspondances de légendes, pas série d'originaux établie. |

### Mini-catalogue des trois pistes nouvelles examinées

Les références `#` désignent **la position ordinale dans `posts_1.html`**, non un ID Instagram ni un permalien.

- **C1-NEW-01 Casina Cinese, Palerme (Italie)** : #12, 2026-03-01, 1 média ; #29, 2025-11-03, 3 médias, fichiers export `17947122018054890.jpg`, `18044962397441732.jpg`, `18120954316519035.jpg` ; #31, 2025-10-30, 1 média. La légende présente la résidence sous les deux appellations « Casina Cinese » et « Palazzina Cinese ». Visuellement, trois cadrages distincts **de l'intérieur** ont été observés dans #29. Photos exportées sur Drive : **présence VÉRIFIÉE**, mais **originaux natifs/HD NON VÉRIFIÉS**, photographe et droits individuels **NON VÉRIFIÉS** (un filigrane de compte n'est pas une preuve de titularité).
- **C1-NEW-02 Maison Spitzer, Budapest (Hongrie)** : #59, 2025-07-13, 1 média de l'entrée ; #150, 2024-10-29, 3 médias, fichiers export `18048366310835856.jpg`, `18074540560584645.jpg`, `18317452015082828.jpg`. Le texte #150 indique Visegrádi utca 29 et attribue le bâtiment à József Klinger ; ces faits architecturaux demandent une vérification documentaire indépendante. Trois compositions distinctes de l'intérieur **VÉRIFIÉES** par inspection des trois JPEG. Fichiers export présents, originaux natifs/HD et droits individuels non vérifiés ; URL IG inconnue.
- **C1-NEW-03 Maison Huot, Nancy (France)** : #9 (2026-04-12), #28 (2025-11-16), #60 (2025-07-11), #82 (2025-05-24), #85 (2025-05-18), #87 (2025-05-15) ; six médias associés. Deux JPEG exportés visuellement comparés : `18051883769149816.jpg` (#60), façade entière, et `18299863966175518.jpg` (#87), gros plan de la porte et de son décor. **Deux compositions différentes VÉRIFIÉES** ; les quatre autres fichiers n'ont pas été comparés. Les légendes situent la maison à Nancy et évoquent l'architecte Émile André, faits à vérifier hors archive. Originaux natifs/HD, droits par fichier et liens IG non vérifiés.

Il s'agit d'une **présélection de repérage, non d'une validation éditoriale ou d'une autorisation de publication**. Une photographie téléchargée depuis Instagram peut avoir 1 440 px de largeur et n'est pas assimilable à un original natif/HD. Avant lancement de dossier, confirmer provenance, auteur et droits pour chaque nouveau fichier et rapprocher des originaux privés ; ne rien ajouter d'office à `research/media-rights.json`.

### Autres publications multi-médias à examiner

Parmi les **10** du sous-ensemble : #70 (Prusa 5 / Świętokrzyska 57, Wrocław, 4 médias, identité architecturale à vérifier), #71 (vitraux Jacques Grüber, Nancy, 3, attribution du lieu à préciser), #72 (pavillon aquarium, 6), #77 (librairie De Slegte, Gand, 2 ; la Maison Bergeret n'est mentionnée qu'à titre comparatif), #93 (jardins de l'École de Nancy, 10 ; ensemble paysager plutôt qu'immeuble unique), #152 (Palazzo della Gazzetta, Bari, 3 ; la légende parle de vestiges et remercie un tiers pour les informations), #618 (vide-poche, objet et non bâtiment, 2), #620 (Chalet des Bruyères, 2, identité/vues à contrôler). Les deux autres sont #29 et #150, examinés ci-dessus. **Dix publications multi-médias ne signifient ni dix bâtiments ni dix séries photo originales.**

## C — Commentaires : structure et limites vérifiées

`post_comments_1.html` contient **2 282 blocs datés**, dont **2 280 avec texte de commentaire extrait**. Les blocs donnent un commentaire, éventuellement un nom de compte et une date ; leurs balises `href` ne fournissent **aucun lien vers la publication source**, et aucun identifiant de post n'a été repéré. **Le rattachement déterministe commentaire → publication est BLOQUÉ par la structure de ce fichier seul.**

Un premier filtre textuel large a identifié 150 commentaires évoquant notamment un bâtiment, un architecte, une façade ou un vitrail ; **150 n'est pas le nombre de commentaires historiquement pertinents**. Exemples de pistes de vérification, reformulées sans recopier les commentaires : attribution d'une devanture de Bruxelles à Paul Hankar (commentaire daté du 15-02-2026) ; proposition d'identification d'un immeuble rue Hegedűs Gyula à Budapest (01-04-2025) ; discussion sur la Maison Cauchie (29-05-2025). Faute d'ancrage de post et de corroboration documentaire, ne pas introduire ces observations comme faits dans un article. Aucun commentaire brut/identifiant de commentateur n'est importé.

## Données encore manquantes et sortie du lot

1. Catalogue nominatif complet des 1 431 entrées : rapprocher les 268 entrées sans lien de média du fichier principal et les 11 chemins supplémentaires sans faux doublons, compléter la classification par bâtiment/sujet ; le catalogue ci-dessus n'est qu'un premier lot ciblé.
2. Lien Instagram/ID fiable pour les posts historiques : absent de `posts_1.html` ; conserver les deux permaliens fournis par Metricool dans le premier inventaire, sans en inventer de nouveaux.
3. Originaux natifs et HD des **trois** nouveaux sujets : export Instagram et images de rendu ne prouvent pas la disponibilité des fichiers source ; établir la correspondance avec la photothèque d'origine sans faire classer manuellement toute la collection.
4. Photographe, titularité et droits de réutilisation par image : à vérifier avant tout usage public, y compris pour les images filigranées ; certaines autres légendes du compte mentionnent des photographes tiers.
5. Source documentaire indépendante pour l'identification, l'histoire, les dates et auteurs des bâtiments ; les légendes et commentaires ne suffisent pas.
6. Vérification complémentaire des contenus `reels.html`, `archived_posts.html`, de l'index `media/posts/` et des éventuelles statistiques pertinentes, sans transformer C1 en audit de métriques.

**Aucune publication, dépense, installation, modification D1, modification du runtime, ni approbation de droits.** Lot exclusivement documentaire : les tests `npm run validate` / `npm run build` ne sont pas exécutés, car aucun code ni média du site n'a été modifié.
