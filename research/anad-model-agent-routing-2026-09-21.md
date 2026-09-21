# ANAD 2.0 — Sélection des agents et modèles, discipline de coût

Date : 2026-09-21. **PROPOSÉ — politique à tester sur les PROCHAINES exécutions.** Ne pas modifier la session Work D1 déjà lancée, son commit de départ, ses variantes ni son checkpoint avant livraison. Ne pas interpréter cette note comme l'installation d'un routeur.

## Sources et distinctions vérifiées

- BMAD officiel fournit des agents nommés et des skills/workflows dans `docs/reference/skills-and-agents.md` : Sally (UX), Amelia (dev), Winston (architecture), Mary (analyse), John (produit), ainsi que `bmad-help` pour guider le choix des skills. **Un skill BMAD chargé dans Work/Codex n'impose pas par lui-même un modèle de calcul distinct.** Source : https://github.com/bmad-code-org/BMAD-METHOD/blob/main/docs/reference/skills-and-agents.md
- Dans Work, le modèle/l'effort sélectionné dans la discussion définit les valeurs du parent ; en l'absence de configuration explicite, un sous-agent peut hériter de ces valeurs. Codex permet, selon l'environnement et la version, de demander un modèle/effort précis pour un sous-agent ou de définir des agents personnalisés par fichiers `.codex/agents/*.toml` et paramètres de `config.toml`. **La possibilité d'imposer ces réglages aux sous-agents de la session Work doit être vérifiée dans le run ; une consigne textuelle ne prouve pas un changement de modèle.** Source : https://developers.openai.com/fr-FR/docs/agent-configuration/subagents
- La consommation de sous-agents/tâches séparées peut ne pas figurer dans le total affiché par la discussion principale ; consulter les limites d'utilisation et les relevés disponibles sans inventer de coût par agent. Source : https://help.openai.com/en/articles/20001478-reviewing-work-and-codex-usage-and-using-personal-analytics-in-chatgpt-desktop
- Captures fournies par Théodore le 21-09 : D1 lancé depuis Work en GPT-5.6 Sol, niveau Moyen ; environ 49 min d'exécution affichées, 4 sous-agents indiqués terminés, quota Work épuisé temporairement avec une heure de retour affichée. **Le screenshot ne démontre ni la configuration individuelle des sous-agents, ni la réussite QA, ni la livraison finale D1.**
- `research/anad-orchestration-state.yaml` est la source d'état D1 sur main, mais sa valeur initiale peut dater d'avant le run ; ne pas réécrire ce checkpoint depuis une autre discussion tant que le run D1 en cours ne l'a pas synchronisé. Ce document est indépendant du checkpoint D1.

## Briques GitHub examinées et adéquation à la consommation Work

| Brique | Fonction vérifiée | Adéquation immédiate |
|---|---|---|
| BMAD `bmad-help` et agents/skills officiels | Aide au choix du rôle/workflow selon la tâche, à partir des artéfacts du projet. | **REUSE** pour la sélection métier ; ne choisit pas automatiquement un modèle moins coûteux pour chaque exécution Work. |
| Codex sous-agents natifs + config agent | Paramètres de modèle et d'effort par agent personnalisé selon environnement/version. | **REUSE / pilote ciblé** : mesurer quelles options sont réellement appliquées dans Work/Codex. Aucune config globale sur la machine de Théodore sans demande. |
| [RouteLLM](https://github.com/lm-sys/RouteLLM) | Route de simples requêtes d'API vers un modèle moins coûteux suivant un routeur et un seuil. Exemples README historiquement GPT-4/Mixtral. | **WATCH** pour un futur pipeline API ; ne route pas directement le sélecteur de modèle de Work/les quotas de l'abonnement. |
| [LiteLLM](https://github.com/BerriAI/litellm) | Passerelle multi-fournisseurs, suivi, load balancing, budgets/routage selon configuration. | **WATCH** : service et appels API distincts, potentiellement facturés ; ne pas installer pour « économiser » le quota Work. |
| [Semantic Router](https://github.com/aurelio-labs/semantic-router), [vLLM Semantic Router](https://github.com/vllm-project/semantic-router) | Routage sémantique/mixture-of-models des requêtes dans une infrastructure de modèles. | **WATCH** si ANAD possède un véritable runtime/API multi-modèles ; hors besoin immédiat. |
| [Claude Code Router](https://github.com/musistudio/claude-code-router) | Passerelle locale vers fournisseurs/modèles, annonce une compatibilité avec Codex CLI et d'autres clients API. | **WATCH** : ne présumer ni compatibilité avec Work cloud ni conservation des droits de l'abonnement ChatGPT ; ne pas lui remettre des secrets en pilote. |

**Conclusion :** une *politique de sélection légère* + les contrôles natifs Codex est le premier pas réversible. Il n'existe pas dans les solutions contrôlées de brique vérifiée qui branche gratuitement un « meilleur modèle par tâche » sur le sélecteur Work tout en utilisant les quotas du plan ChatGPT. Évaluer un routeur API seulement en présence d'un besoin API démontré et avec autorisation de coût distincte.

## Politique de lancement à appliquer à la prochaine mission, non à D1 en cours

Avant de lancer Work, consigner brièvement le rôle du **coordinateur parent**, le modèle et l'effort réellement offerts dans l'interface ; demander explicitement aux agents de ne pas déléguer des tâches triviales. **Valeur de départ proposée** : modèle rapide de type Terra si visible et disponible dans Work, effort Moyen ; sinon sélectionner un modèle accessible et noter le choix. Ne pas présumer que Luna/Terra/Sol/Astra sont tous disponibles sur tous les écrans ou que les coûts par crédit Business décrivent le quota personnel de Théodore.

| Nature de la tâche | Agent / skill approprié | Niveau de calcul à essayer d'abord | Contrôle |
|---|---|---|---|
| Lecture ciblée, inventaire, listes et extraction déterministe | Explorateur natif / script / Mary seulement si analyse nécessaire | Commande ou script déterministe d'abord ; modèle rapide/faible effort si utile | Liens et comptage exact ; aucune deuxième lecture exhaustive. |
| Conception UX, direction photographique D1 | Sally et skill UX BMAD | Modèle de milieu/haut de gamme, effort Moyen, ajuster si qualité insuffisante | Deux variantes visuelles réellement navigables et comparables. |
| Architecture et choix techniques engageants | Winston/architecture BMAD | Modèle fort, effort Moyen ; élevé seulement sur problème démontré | Décision documentée et vérifiable ; pas de nouvelle roadmap. |
| Implémentation claire et locale | Amelia / `bmad-build` et Codex | Modèle rapide à intermédiaire, effort Moyen | Tests ciblés et diff ; escalade seulement en cas d'échec réel. |
| Lancer la QA, récupérer les sorties, comparer captures | Commandes Playwright/axe/Lighthouse existantes puis agent de synthèse si besoin | Automatisation non-LLM en premier ; petit modèle pour synthèse | Logs et fichiers de preuve, jamais « QA verte » sans exécution. |
| Revue indépendante ambiguë, sécurité/droits | `bmad-review`, agent spécialisé si réellement indépendant | Modèle plus fort, effort Moyen | Preuves et décisions ; droits/photo restent sous contrôle humain. |

## Règles de routage sobres

1. **Rôle ≠ modèle ≠ sous-agent.** Sélectionner le skill officiel selon la tâche, puis le modèle/effort seulement si la plateforme expose et applique cette capacité.
2. **Réduire le volume avant de réduire le modèle** : lectures GitHub par chemins/sections, contexte source_commit, sorties compactes, commandes déterministes, images optimisées et prompts avec critères de sortie.
3. **Paralléliser uniquement l'indépendant** : deux variantes D1 isolées oui ; cinq agents lisant tout le dépôt en double non. Définir au maximum deux pistes de produit, délégation selon nécessité réelle.
4. Budget indicatif par mission : résultat minimal vérifiable d'abord, une boucle de correction ciblée, une QA pertinente, une revue groupée ; escalader en modèle/effort sur échec concret plutôt que lancer plusieurs recherches profondes concurrentes.
5. Journal après chaque exécution : modèle/effort **observé** du parent ; modèle/effort du sous-agent uniquement si vérifié, sinon `non observable` ; nombre de sous-agents, transferts manuels, résultat réel, éventuelle consommation observable. Ne pas attribuer des coûts calculés sur la seule durée affichée.
6. **Aucune commutation de modèle ou reprise automatique d'une exécution Work épuisée supposée** : attendre la restauration de la limite ; consulter les sorties/checkpoints existants avant de relancer ou de demander un nouveau run. Si D1 a fini, récupérer ses artefacts avant de lancer autre chose.

## Test restreint après D1

Piloter sur une petite tâche ANAD comparable deux modalités réellement disponibles : parent Work au modèle/effort de départ vs même mission avec sous-agent bas coût explicitement paramétré si l'environnement le permet. Mesurer temps humain, qualité, nombre de nouvelles tentatives et consommation observable ; **pas de second D1 complet coûteux**. Si réglage des sous-agents impossible dans Work, préférer un lancement de mission bornée séparée via l'interface ou des agents personnalisés Codex dans environnement isolé. Tout paramètre `.codex/agents` dans le dépôt doit être testé et validé sur branche avant adoption.
