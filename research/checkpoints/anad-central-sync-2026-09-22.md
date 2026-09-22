# ANAD 2.0 — Checkpoint central de synchronisation (22-09-2026)

**Statut : PROPOSÉ pour revue et intégration dans `main`.** Ce document décrit des éléments vérifiés sur les références indiquées et des orientations encore proposées ; il n'approuve aucune fusion D1 ni publication éditoriale. Base de la branche de préparation : `f29ff1035da4f6616b77e1fb0368f47ef2610eda`.

## Hiérarchie des sources et décisions conservées

- `AGENTS.md` et `research/ANAD-PROJECT-STATE.md` sur `main` restent la référence de gouvernance. Le registre central porte une dernière consolidation datée du 20 septembre : **ses états D1/C1 du pilote initial sont historiques** au regard des PR décrites ci-dessous. Le présent checkpoint ne réécrit pas rétroactivement leur statut.
- D12 et `research/anad-2-execution-reset-2026-09-21.md` : priorité à la chaîne réutilisable photographie / identité du bâtiment / corpus sourcé / article / site / validation humaine, sans pression de publication Coilliot.
- Deux responsabilités productives séparées : **pôle éditorial/C1** (identification, provenance, photos, sources, charte rédactionnelle, articles, dossiers privés) ; **D1/Work** (UX/UI, développement, intégration, prévisualisation et QA). La discussion centrale pilote les interfaces entre domaines. La mission du pôle éditorial a été formulée en chat ; **son exécution et la validation de la charte restent non vérifiées**.
- Statuts obligatoires : PROPOSÉ, VALIDÉ, EN COURS, RÉALISÉ, VÉRIFIÉ, BLOQUÉ. Préparer un article ou un dessin n'en autorise ni l'intégration publique ni la publication.

## D1 — état des branches au 22-09-2026

État GitHub vérifié : [PR #42](https://github.com/Theodore-Aspeel/artnouveau-site/pull/42), [#43](https://github.com/Theodore-Aspeel/artnouveau-site/pull/43), [#44](https://github.com/Theodore-Aspeel/artnouveau-site/pull/44), [#45](https://github.com/Theodore-Aspeel/artnouveau-site/pull/45) et [#46](https://github.com/Theodore-Aspeel/artnouveau-site/pull/46) sont toutes **ouvertes, draft et non fusionnées**. #43 cible la branche #42 ; #44 cible #43 ; #45 et #46 ciblent `main`. Il ne faut donc ni les fusionner en bloc ni interpréter les cinq directions comme une seule implémentation commune.

- **RÉALISÉ techniquement, VÉRIFIÉ en CI pour la PR #46** : branche `anad-2.0/d1-preproduction-premium`, HEAD `f720854b4fef75247170f096e2dbf6052f8b352f` ; [Quality #97](https://github.com/Theodore-Aspeel/artnouveau-site/actions/runs/35772474163) : `completed / success` sur ce même SHA. Accueil photographique et prévisualisation locale des médias privés décrits dans [son rapport](../d1-preproduction-premium-2026-09-22.md) **sur sa propre branche**, non dans `main`.
- **À VALIDER HUMAINEMENT** : rendu esthétique réel de la maquette privée #46 (accueil, mobile, hiérarchie, photos). La revue critique précédente portait sur des itérations antérieures : ne pas conclure que #46 est acceptée ou rejetée sans inspection de cette version.
- Villino Florio et Maison Bastin : les nouveaux articles ne sont pas créés par #46. Préserver les statuts `draft/noindex`, les contrats trilingues et le contrôle des droits. N'exposer aucun JPEG privé dans Git, CI, captures publiques ou déploiement.

## C1 — état documentaire actualisé

- [PR #40](https://github.com/Theodore-Aspeel/artnouveau-site/pull/40), branche `anad-2.0/c1-instagram-export-2026-09-21` : **ouverte/draft, non fusionnée** ; contient rapports d'inventaire, fiches de séries et index expurgé (aucune photographie ou archive privée).
- **RÉALISÉ / VÉRIFIÉ sur la portée des deux HTML de l'export officiel** : 1 431 positions historiques (1 162 non archivées + 269 archivées), 1 460 chemins médias ; 258 entrées automatiquement nommées, sans preuve d'identité photographique ; 1 083 ambiguës ou inconnues. Référence : `research/c1-instagram-catalogue-structurel-1431-2026-09-21.md` **sur la branche #40**, ainsi que `research/c1-candidates/synchronisation-et-demande-groupee-2026-09-21.md`.
- **Correction VALIDÉE dans le chantier C1** : pas de photothèque historique distincte à rechercher. Les copies Instagram sont les meilleures copies historiques connues ; ne pas relancer une extraction complète ni exiger des RAW/JPEG natifs supplémentaires comme condition absolue. La qualité web et les droits/publication se vérifient séparément, média par média. Les anciens passages du rapport C1 sur `main` qui posaient l'absence de natifs comme blocage général sont dépassés sur ce point précis.
- **RÉALISÉ en Drive privé** : corpus des quatre pilotes : 3 vues existantes Coilliot, 2 vues existantes Hiboux ; 5 copies JPEG autonomes Villino et 5 Bastin. Les 10 copies C1 sont autorisées pour **maquette locale privée seulement** selon le manifeste associé. Ne pas publier, ajouter au registre public des droits par extrapolation, attribuer une pièce intérieure sans preuve ni employer le numéro ordinal de l'export comme identifiant Instagram.
- La charte éditoriale et les nouveaux articles demeurent **PROPOSÉS / NON LIVRÉS dans les sources consultées** ; ne pas confondre les quatre dossiers pilotes déjà préparés avec des articles publiés.

## Nouveaux sujets du pôle éditorial

**EN COURS de préparation en conversation, livraison non vérifiée :** Habitations Marconi (Forest), Maison Piot (Liège) et Palais Chinois/Palazzina Cinese (Palerme). Des photographies et planches illustrées ont été transmises en conversation, mais il n'existe pas de preuve ici de dossiers finalisés, de charte rédactionnelle approuvée, d'identités historiques totalement contre-vérifiées ni d'autorisation de diffusion publique. Les planches dérivées ne sont pas les photographies originales ni des sources historiques autonomes ; le Palais Chinois relève d'une autre période architecturale et doit être catégorisé sans fausse attribution Art nouveau.

**PROPOSÉ** : une discussion éditoriale spécialisée assure le tri réel, les manifestes de vues, les sources patrimoniales et les articles EN/FR/NL dans des dossiers privés ; Work ne reprend que les paquets livrés, sous contrôle du pilotage. Ne pas enregistrer des fichiers JPEG ou des liens Drive privés dans le présent checkpoint public.

## Identification des bâtiments à partir des photographies

Rapport de recherche approfondie fourni au pilotage le 22 septembre : **RÉALISÉ pour l'étude documentaire**, **NON VÉRIFIÉ empiriquement sur les cas difficiles ANAD**. Proposition : recherche visuelle par moteurs grand public avec dérivées autorisées, liste de candidats limitée à la ville, références Commons/Wikidata/OSM et patrimoines locaux, comparaison positive/négative, puis validation humaine. Sorties : `IDENTIFICATION CONFIRMÉE`, `CANDIDAT PROBABLE`, `NON IDENTIFIÉ` ; ne jamais transformer automatiquement « probable » en légende ou article définitif.

**NON VALIDÉ / NON DÉVELOPPÉ** : aucune API/MCP officielle de recherche inversée Lens/Yandex/Bing n'a été attestée dans la discussion ; pas de nouveau logiciel, Cloud billing, scraper de moteurs visuels ou index Street View. Réaliser un pilote sur de vraies séries difficiles avant toute architecture supplémentaire. L'identification du bâtiment ne prouve ni la provenance du fichier photographique ni les droits de diffusion.

## Gates et prochaine synchronisation

1. Faire une revue artistique **de la maquette #46 elle-même** ; conserver les autres PR draft en attendant le choix humain explicite d'une base.
2. Obtenir du pôle éditorial une charte au statut explicitement validé ou proposé, puis au moins un dossier réel : JPEG autonomes, manifeste de vues, faits sourcés, légendes, article EN/FR/NL, droits et réserves. Le pôle ne développe pas le site.
3. Préparer seulement ensuite une mission Work bornée, dont la branche de base réelle et la frontière entre médias privés, médias publics et publication sont explicites.
4. **Nouveau checkpoint obligatoire** avant le prochain Work ou dès qu'un premier article prêt et la charte sont livrés/validés, selon le premier événement ; la discussion centrale signale ce seuil, vérifie les liens/preuves et demande validation des éventuels changements de priorité, d'architecture ou de périmètre.

**Aucune fusion ni déploiement ni changement de statut éditorial par ce checkpoint.**

## Addendum au checkpoint : premier dossier éditorial livré (22-09-2026)

**JALON ATTEINT — RÉALISÉ / VÉRIFIÉ dans le périmètre privé consulté.** La charte éditoriale v1.1 a été **VALIDÉE pour la préproduction**. Le pôle éditorial a livré un premier dossier consacré au **n° 32 des Habitations Marconi, Forest** : quatre copies JPEG autonomes, documentation patrimoniale, manifeste des vues et droits, article EN/FR/NL, légendes et textes alternatifs individualisés. Le dossier privé et ses deux documents spécialisés ont été consultés par le pilotage ; les quatre copies sont présentes individuellement dans leur dossier photographique privé. Les contrôles de dimensions et empreintes SHA-256 sont documentés sur les fichiers **avant** dépôt Drive, tandis que le contrôle post-dépôt porte sur les tailles et les métadonnées du dossier, non sur un nouveau hash distant.

**Correction documentaire :** les quatre photographies du lot concernent le seul immeuble n° 32, attribué à Léon Govaerts par la notice régionale Urban 29216. Les immeubles d'Émile Hellemans et d'Henri Jacobs appartiennent au contexte de l'ensemble mais ne sont pas photographiés dans cette série. Les textes ont été recentrés sur ce périmètre ; la distinction entre la correspondance visuelle et la source patrimoniale est documentée dans le livrable privé.

**PROPOSÉ pour relecture humaine :** article dans les trois langues, choix d'une vue générale en ouverture puis entrée et détail, quatrième photographie d'entrée conservée comme variante de réserve. **NON VALIDÉS :** publication de chacune des quatre photos, crédits définitifs, choix visuel final, validation éditoriale de diffusion, intégration technique et publication. Cette livraison ne change pas le statut des quatorze articles actuellement existants dans le site.

**Effet sur le gate précédent :** la dépendance « charte + premier dossier prêt pour relecture privée » est désormais satisfaite. Les dépendances encore ouvertes sont la revue artistique réelle de la maquette D1 PR #46, le choix d'une branche D1 de référence pour toute correction et la validation spécifique des droits avant toute exposition publique. Le pôle éditorial peut continuer les autres dossiers en parallèle sans déléguer son travail à Work. Le prochain Work ne doit pas recommencer la recherche historique ou le tri photographique Marconi.

Le checkpoint **ne fusionne pas la PR documentaire en cours**, n'ajoute aucun lien Drive privé, photographie, métadonnée privée d'image ou texte d'article au dépôt public et ne vaut aucune approbation de mise en ligne.

## Addendum : Maison Piot — deuxième dossier éditorial privé livré (22-09-2026)

**RÉALISÉ / VÉRIFIÉ dans le périmètre Drive consulté :** le pôle éditorial a livré Maison Piot (Liège), six fichiers JPEG photographiques autonomes, plus une planche illustrative séparée, ainsi qu'un manifeste, une fiche historique, un article EN/FR/NL, six légendes et six textes alternatifs par langue. Aucun de ces fichiers privés n'est déposé dans cette PR.

**Documentation :** maison du 17 rue de Sélys datée de 1904, architecte Victor Rogister selon les références réunies par le pôle ; deux reliefs féminins distincts, l'un au coq, l'autre à la chouette. L'interprétation symbolique jour/nuit est attribuée à une source spécialisée, non déduite du surnom « Maison des Francs-Maçons ». L'attribution sculpturale à Oscar Berchmans est mentionnée avec ses sources, sans prétendre à une signature visible sur les photographies. Tout fait historique et tout choix éditorial restent soumis à la relecture préalable à diffusion.

**Sélection PROPOSÉE, non artistiquement validée :** photographie générale en ouverture, puis porte, inscription/date, baie supérieure et les deux reliefs distincts. Le manifeste garde les six originaux inchangés et exclut la planche dérivée de la galerie documentaire. La planche présente une extension `.png` alors que son format binaire réel est JPEG ; ne pas la traiter comme un PNG valide ni l'utiliser publiquement sans clarification des droits.

**NON VALIDÉS :** droits individuels de publication, crédit définitif, utilisation publique de la planche, ordre de galerie et texte définitifs. Le pôle éditorial n'a modifié ni le code ni le registre public des droits.

**Adaptation du gate humain à la demande de Théodore :** les Docs sont les pièces de contrôle éditorial, **pas l'interface de validation artistique**. Ne pas exiger de validation du rythme des articles à la seule lecture des documents. Après revue de la maquette #46 et choix d'une seule base D1, préparer une **prévisualisation privée navigable** des vraies pages d'articles Marconi/Piot, sans images privées dans Git, CI ou preview publique. La visualisation privée n'est ni la permission d'une intégration publique ni une autorisation de publier. Le pôle éditorial peut préparer d'autres dossiers indépendamment de Work.

**Checkpoint suivant** : avant la prochaine mission Work, ou à toute modification substantielle du périmètre, de la base D1 ou des droits.
