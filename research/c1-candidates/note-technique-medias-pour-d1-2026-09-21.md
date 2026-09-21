# ANAD 2.0 — C1 → D1 : contraintes des photographies Instagram pour la refonte visuelle

Date : 2026-09-21. **RÉALISÉ — note technique préparée ; PROPOSÉ — usages d'affichage ; EN COURS — confirmation auteur et droits ; PUBLICATION NON AUTORISÉE.** Document C1 destiné à consultation par D1, **sans modification ni demande d'arrêt de son chantier**.

## Constat vérifié sur les trois séries C1

L'audit existant de **18/18 copies Instagram** a sélectionné **14 copies candidates** pour un affichage web modéré. **L'export officiel Instagram est la source photographique historique disponible** ; ne pas demander de RAW ou JPEG natif distinct. La qualité réelle a été contrôlée sur ces copies, **pas sur une exportation haute définition supposée ni dans la version responsive finale du site**.

| Série | Principale candidate (ordinal privé) | Dimensions source et limites | Vues secondaires retenues et usage envisagé |
| --- | --- | --- | --- |
| Villino Florio | **F0027**, façade | **1 440 × 1 440 px**, ~264 Ko ; façade lisible, perspective montante et ciel clair ; **≤ 700 px CSS de large** en affichage principal encadré, sans grand recadrage. | F0005 escalier 1 440 × 1 920, F0013 cheminée 1 440 × 1 920, F0018 vitrail 1 440 × 1 116 : détails/galerie ≤ 650 px CSS. F0017 terrasse 1 440 × 1 535 : secondaire facultative ≤ 500 px CSS. |
| Maison Bastin | **F0394**, façade | **1 440 × 1 440 px**, ~337 Ko ; façade assez complète avec ombres soutenues ; **≤ 700 px CSS**, sans plein écran. | F0717 oriel 756 × 756 : vignette ≤ 350 px ; F0729 vitrail 1 029 × 1 029 : détail ≤ 450 px, contre-jour ; F0746 intérieur 1 080 × 1 135 : galerie ≤ 450 px ; F0751 portes 1 073 × 1 073 : vignette ≤ 400 px. |
| Maison de la rue Warocqué | **F0745**, façade | **1 080 × 1 167 px**, ~222 Ko ; façade cadrée, ombres et ciel clair ; **≤ 500 px CSS**, pas de hero plein écran. | F0586 panneau à la grue 1 440 × 1 440 : détail ≤ 650 px ; F0742 paon 1 080 × 1 350 : détail vertical ≤ 500 px ; F0736 baie 1 080 × 1 080 : petite vignette ≤ 350 px, rendu doux. |

**Exclusions techniques / reprises :** F1020 (façade Bastin trop proche de F0394) ; F0740 (même vitrail que F0729, très sombre et 806 px) ; F0267 (panneau de grue quasi identique à F0586) ; F0728 (vitrage Warocqué aux hautes lumières fortement écrêtées). **F0017** est une cinquième candidate facultative pour Villino, et non une obligation de remplir artificiellement une galerie. L'examen conclut à cinq compositions Villino, cinq familles Bastin et au moins cinq familles Warocqué **dans l'archive**, mais seuls quatre médias Warocqué sont sélectionnés : « familles » n'équivaut ni à « prises de vues originales indépendantes » ni à « droits approuvés ».

## Recommandations d'intégration visuelle (PROPOSÉES, à adapter par D1)

- Employer des **cadres éditoriaux de largeur limitée**, des grilles asymétriques de taille contrôlée ou des mises en page texte/photo ; prévoir une réserve typographique ou un fond uni pour les sections larges. **Ne pas forcer une photographie source de 1 080–1 440 px dans un grand hero bord à bord**, particulièrement sur écran Retina/haute densité.
- Garder les compositions complètes lorsque la façade ou la perspective a peu de marge ; éviter les recadrages `cover` agressifs sur les images principales. Prévoir `object-fit: contain` ou un cadre à ratio compatible selon le contexte, sans imposer de recadrage destructeur.
- Une **vignette de détail** peut être techniquement utile malgré une faible résolution (ex. F0717, 756 px de large) ; ne pas l'ouvrir par défaut en lightbox plein écran ou la présenter comme un agrandissement riche en détails. Éviter la récupération artificielle de lumières déjà brûlées et l'upscale inventant des éléments architecturaux.
- Les largeurs CSS sont des **bornes indicatives conservatrices** fondées sur les copies mesurées et la consultation visuelle, **pas des résultats de QA responsive**. Contrôler ultérieurement la lisibilité au ratio et à la densité d'écran réels avant tout choix définitif d'affichage.
- **D1 continue dès maintenant avec les images déjà approuvées** et une maquette adaptable à la qualité variable des futurs médias. Cette note n'autorise **ni l'ajout immédiat des 14 fichiers C1 au site ni l'attente de la fin de C1**. Elle ne modifie pas son dépôt de travail, sa PR ni son checkpoint.

## Provenance, droits et décision humaine — statuts distincts

1. **COPIE DISPONIBLE : VÉRIFIÉE** pour 18/18.
2. **QUALITÉ WEB : VÉRIFIÉE dans les limites des fiches**, avec 14 usages candidats et quatre copies non sélectionnées ; rendu final responsive non testé.
3. **PROVENANCE ET DROITS : EN COURS** pour chaque copie candidate ; sa présence sur Instagram, l'absence de crédit à un tiers et un filigrane ne prouvent pas la titularité.
4. **PUBLICATION : NON AUTORISÉE** sans validation humaine distincte après confirmation des droits et du choix éditorial.

**Unique demande groupée déjà préparée, non envoyée :** consulter `research/c1-candidates/synchronisation-et-demande-groupee-2026-09-21.md`. Ne pas envoyer de demandes fragmentées ni chercher une photothèque native distincte. Si une copie est attribuée à un tiers ou reste incertaine, l'isoler ; aucune entrée automatique dans `research/media-rights.json`.

## Limites connues à préserver dans le transfert

L'audit ne démontre pas l'existence de versions HD, l'identité du photographe pour chaque fichier, une autorisation de reproduction, l'identité patrimoniale indépendante des bâtiments, ni la qualité à pleine largeur/plein écran. Les 1 460 références médiatiques globales n'ont **pas** fait l'objet d'un audit de qualité ; ce lot porte uniquement sur les **18 images définies**. La planche-contact privée évoquée dans la synthèse C1 n'est **pas prouvée présente dans le dossier Drive des livrables synchronisés consulté pour cette note** : son existence et son emplacement doivent être confirmés avant de prétendre l'avoir transmise. Le dossier Drive contient le catalogue et l'index synchronisés, pas de planche photo repérée dans sa liste de six éléments. Ne partager ni image privée ni légende brute dans GitHub ou la discussion D1.
