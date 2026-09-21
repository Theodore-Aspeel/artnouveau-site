# ANAD 2.0 — C1 : inventaire Instagram et rapprochement avec les articles existants

Date de collecte : 2026-09-21 (Europe/Brussels).
Statut : **EN COURS — premier relevé partiel VÉRIFIÉ**. La shortlist de trois dossiers multi-vues originaux reste **BLOQUÉE par la couverture des données et les fichiers natifs non vérifiés**.
Références lues sur `main` : `AGENTS.md`, `research/ANAD-PROJECT-STATE.md` (D12/D13), `research/anad-2-execution-reset-2026-09-21.md`, `src/data/articles.json`, `research/media-rights.json`.
**Périmètre : documentaire interne C1 seulement. Aucun fichier D1/checkpoint, article, média ou statut de publication modifié.**

## 1. Méthode, portée et limite d'accès

Compte connecté observé via Metricool : `@artnouveauetdeco`, marque `6978424` (timezone de la marque : Europe/Berlin). Extraction en lecture seule via connecteur `instagram / posts` : date (`IGPO01`), légende (`IGPO03`), identifiant (`IGPO04`), miniature (`IGPO05`), URL (`IGPO06`) et type (`IGPO07`). Une miniature de la réponse n'est pas un inventaire des médias, une preuve de carrousel complet, ni un fichier source HD.

Périodes interrogées pour les posts : 2024-01-01 au 2024-12-31 ; 2025-01-01 au 2025-06-30 ; 2025-07-01 au 2025-12-31 ; 2026-01-01 au 2026-04-30 ; 2026-05-01 au 2026-09-21. Les périodes 2024, 2025 et janvier-avril 2026 renvoient zéro ligne ; mai-septembre 2026 renvoie deux lignes. Reels interrogés sur 2025-01-01 au 2025-12-31 et 2026-01-01 au 2026-09-21 : zéro ligne. Les périodes sont des appels partiels au connecteur, pas une preuve d'exhaustivité de l'historique Instagram. Ne pas inférer qu'il n'existe pas d'autres publications ni Reels, surtout antérieurs à la connexion Metricool.

Périmètre confirmé : **2 publications, 2 sujets distincts, aucun dossier IG multi-vues prouvé**. Absence d'accès démontré aux enfants de carrousels, à la totalité du feed, à une archive Instagram officielle et à la photothèque native de Christophe.

## 2. Publications Instagram groupées par sujet

| Réf. | Sujet / lieu | Date / lien IG vérifié par Metricool | Type retourné / média accessible | Nombre total de vues du sujet | Originaux HD disponibles | Droits applicables aux photos IG | Couverture dans les 14 articles |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IG-001 | Monument au Maestro Serrano, Sueca (Espagne) | 2026-08-10 — https://www.instagram.com/p/Db3bdnXtBEh/ | `FEED_IMAGE` ; 1 miniature retournée | **Inconnu** ; au moins 1 représentation du sujet dans la réponse, sans preuve d'autres angles | **Inconnu** ; miniature ≠ natif | **À confirmer** pour ce fichier et ses réutilisations ; la légende/présence sur le compte ne suffit pas à identifier l'auteur ni l'accord précis | **Absent** de `src/data/articles.json` |
| IG-002 | Chiosco Ribaudo, Palerme (Italie) | 2026-07-28 — https://www.instagram.com/p/DbU3Cw2KOZc/ | `FEED_IMAGE` ; 1 miniature retournée | **Inconnu** ; au moins 1 représentation du sujet dans la réponse, sans preuve d'autres angles | **Inconnu** | **À confirmer** individuellement | **Absent** de `src/data/articles.json` |

Métadonnées descriptives provenant des légendes, **non contre-expertisées comme faits architecturaux** :
- IG-001 : monument Art Déco dédié au compositeur José Serrano ; légende évoquant le sculpteur Vicente Beltrán Grimal, structure pyramidale et figures allégoriques.
- IG-002 : kiosque de style Liberty ; légende mentionnant Ernesto Basile et 1916.

**Regroupement actuel** : une publication documentée par sujet ; aucune correspondance vérifiée à un deuxième post du même monument. Les URLs ci-dessus sont les liens retournés par Metricool, non la preuve d'une consultation exhaustive des médias Instagram.

## 3. Corpus éditorial existant dans GitHub (indépendant de l'inventaire IG)

Lecture directe de `src/data/articles.json` sur `main` : **14 articles, tous `draft`**. Les chiffres ci-dessous sont des *références de fichiers d'images de rendu* dans les articles, non le nombre de photographies natives, ni un lien vérifié vers Instagram.

| Zone | Article / identifiant stable | Fichiers image référencés dans l'article | Contrôle du sujet des images |
| --- | --- | ---: | --- |
| Lille | `maison-coilliot-lille-hector-guimard` | 3 | 3 vues du sujet dans les champs média ; dossier déjà traité, **hors shortlist C1** |
| Lille | `lhuitriere-lille-art-deco` | 3 | 1 vue de L'Huîtrière ; les 2 supports décrivent **d'autres bâtiments** (Maison Coilliot, loge Lumière du Nord) : ne pas compter comme 3 vues de L'Huîtrière |
| Bruxelles | `maison-fernand-lefever-bruxelles` | 1 | 1 référence de rendu |
| Saint-Gilles | `maison-des-hiboux-saint-gilles` | 2 | Façade + gros plan du sgraffite « Les Hiboux » ; **2 fichiers du même bâtiment selon les métadonnées de l'article** |
| Anvers | `maison-lotus-anvers` | 1 | 1 référence de rendu |
| Bratislava | `maison-aux-tulipes-bratislava-jeno-schiller` | 2 | Façade + entrée décrite dans le même article ; identité de l'entrée à confirmer sur originaux |
| Tournai | `maison-strauven-avenue-van-cutsem-2729-tournai-1904` | 2 | Détail de porte + façade à oriel dans le même article ; correspondance de l'adresse à confirmer sur originaux |
| Vienne | `palais-de-la-secession-vienne-18971898` | 1 | 1 référence de rendu |
| Vienne | `maison-aux-majoliques-vienne` | 1 | 1 référence de rendu |
| Milan | `casa-campanini-milan-1904` | 1 | 1 référence de rendu |
| Anvers | `den-tijd-le-temps-anvers` | 2 | Le support décrit « Den Dag » ; **ne pas compter automatiquement comme second angle de Den Tijd** |
| Milan | `aquarium-de-milan-1906` | 1 | 1 référence de rendu |
| Ixelles | `maison-ernest-delune-maitre-verrier` | 1 | 1 référence de rendu |
| Charleroi | `facade-art-deco-charleroi` | 1 | 1 référence de rendu |

Le registre `research/media-rights.json` classe explicitement des **chemins de médias runtime** existants dans une collection « original_photography » avec Christophe Aspel comme auteur/titulaire, statut `cleared`, sur la base d'une déclaration du propriétaire enregistrée le 2026-09-15. Cela confirme la déclaration de droits **pour les chemins listés**, sans démontrer la présence d'originaux natifs/HD, sans relier ces fichiers aux deux posts IG et sans autoriser par extrapolation de nouveaux fichiers non répertoriés. Les crédits publics n'étant pas remplis sur toutes les entrées d'article, préférer le registre explicite pour ce contrôle interne ; conserver le gate de droits avant toute nouvelle publication.

## 4. Cartes candidats et pré-shortlist de vérification (non sélection éditoriale)

**C-IG-001 — Monument au Maestro Serrano, Sueca**
- Source Instagram : IG-001, URL connue ; une ligne Metricool et une miniature.
- Plusieurs publications du même sujet : non démontrées ; plusieurs prises de vue distinctes : inconnues.
- Source native/HD, identité de l'auteur, autorisation de réutilisation et correspondance avec les images publiées : inconnues.
- Couverture article : aucune dans les 14 articles.
- **PROPOSÉ** : rapprocher ce post du dossier d'originaux tenu par Christophe puis inspecter les angles réels, sans présumer d'un carrousel.

**C-IG-002 — Chiosco Ribaudo, Palerme**
- Source Instagram : IG-002, URL connue ; une ligne Metricool et une miniature.
- Plusieurs publications/angles : non démontrés ; sources HD, provenance et droits précis : inconnus.
- Couverture article : aucune dans les 14 articles.
- **PROPOSÉ** : même vérification d'origine, série photo et droits que C-IG-001.

**C-GH-001 — Maison des Hiboux, Saint-Gilles**
- Source : article `maison-des-hiboux-saint-gilles` sur GitHub, **pas de lien Instagram vérifié**.
- Deux références de rendu distinctes sur le même bâtiment selon l'article : `assets/images/articles/maison-des-hiboux-saint-gilles.png` (façade) et `assets/images/articles/gros-plan-sur-le-sgraffito-de-la-maison-des-hiboux-bruxelles.png` (détail).
- Chemins listés au registre des droits ; **fichiers natifs HD, série multi-angle plus large et posts IG correspondants inconnus**.
- Couverture : article déjà existant, statut draft ; dossier possible pour tester la découverte de plusieurs vues *sur GitHub*, **pas un nouveau sujet non couvert**.
- **PROPOSÉ** : localiser les deux originaux, confirmer qu'ils décrivent bien le même bâtiment et chercher les posts Instagram associés. Ne pas en faire un nouvel article en doublon.

**Autres candidats GitHub à recouper** : `maison-strauven-avenue-van-cutsem-2729-tournai-1904` et `maison-aux-tulipes-bratislava-jeno-schiller` référencent chacun deux images dans un même article, mais leur identité spatiale doit être confirmée sur les originaux. Aucune URL IG correspondante vérifiée. Ne pas utiliser `lhuitriere-lille-art-deco` ou `den-tijd-le-temps-anvers` comme preuves de multi-vues à partir du simple nombre de supports.

**Décision de sortie C1** : trois cartes de *repérage* sont présentées ; **zéro sujet démontré à ce stade comme dossier source IG + multi-vues originales HD + droits individuels vérifiés**. La shortlist de trois dossiers *éligibles au prochain cycle* est donc **BLOQUÉE**, sans bloquer le travail d'inventaire.

## 5. Manques précis et voie minimale de résolution

1. **Historique Instagram** : obtenir un export officiel de publications depuis le compte propriétaire ou un accès autorisé permettant de parcourir les posts et enfants des carrousels ; récupérer au minimum URL/post ID, date, légende, type, liste des médias et lien sujet. Ne pas inférer des absences à partir des réponses vides de Metricool ; ne pas scraper ni demander d'identifiants.
2. **Réconciliation bâtiment** : regrouper les posts par identité de bâtiment (nom + ville + adresse si établie), sans fusionner des bâtiments voisins ni compter deux fois un même média.
3. **Originaux** : pour chaque candidat, obtenir un index du dossier natif avec noms de fichiers, dimensions, 2–3 vignettes/planche-contact et correspondance post ↔ original. Une miniature IG et un asset optimisé du site ne prouvent pas l'existence du natif HD.
4. **Provenance/droits** : identifier le photographe, détenteur des droits et accord de réutilisation par *nouveau fichier* ; confirmer les éventuels tiers présents et enregistrer les futurs assets retenus explicitement dans le registre avant toute exploitation publique.
5. **Chevauchement éditorial** : rapprocher les sujets extraits de la liste des 14 identifiants `draft`; privilégier pour un futur nouveau dossier un sujet non couvert, mais ne rien sélectionner définitivement sans corpus et sources.

**Une action humaine minimale proposée** : faire fournir par Christophe **un export officiel du compte Instagram (métadonnées de publications si disponibles) OU un index de sa photothèque organisé par bâtiment**, avec l'emplacement des originaux des deux sujets IG identifiés ; demander les fichiers natifs eux-mêmes uniquement pour les 2–3 dossiers qui survivront au tri. L'index seul peut débloquer la recherche de multi-vues ; si ni export ni index ne peut être partagé, C1 reste partiel.

## 6. Exécution et contrôles

- Collecte en lecture seule via Metricool et GitHub ; vérification des 14 slugs/statuts/médias et du registre de droits.
- Aucune publication, dépense, installation, extraction d'images pour rediffusion, mutation du runtime ou du checkpoint D1.
- Les commandes `npm run validate` / `npm run build` ne sont pas exécutées : lot purement documentaire, sans changement du code/site ni environnement de build requis.
