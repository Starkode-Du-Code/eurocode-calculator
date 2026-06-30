# Index de la documentation

> Carte complète de la documentation du projet eurocode-calculator.
> Commencer par le **Cours Master** si vous découvrez le projet.

## Navigation rapide

| # | Document | Pour qui | Contenu |
|---|----------|----------|---------|
| 01 | [Cours Master](01-COURS-MASTER.md) | Tout le monde | Guide complet : commandes, concepts, workflow projet |
| 02 | [Handoff IA](02-HANDOFF-IA.md) | IA + Humain | Relevé de session — état actuel du projet |
| 03 | [Workflow Humain vs IA](03-WORKFLOW-HUMAIN-VS-IA.md) | Apprenant | Comment faire chaque étape manuellement |
| 04 | [Démarrage Projet](04-DEMARRAGE-PROJET.md) | Débutant | Checklist jour 1 d'un nouveau projet |
| 05 | [Stratégie Madil4](05-STRATEGIE-MADIL4.md) | Portfolio | Constellation de repos, vision long terme |

## Cours par secteur

| Secteur | Document | Niveau |
|---------|----------|--------|
| Génie civil / Structure | [cours/genie-civil.md](cours/genie-civil.md) | Ingénieur |
| Eurocodes (EC0-EC8) | [cours/eurocodes.md](cours/eurocodes.md) | Ingénieur |
| Python | [cours/python.md](cours/python.md) | Débutant → Intermédiaire |
| Développement API (FastAPI) | [cours/fastapi-dev.md](cours/fastapi-dev.md) | Intermédiaire |
| DevOps (CI/CD, Docker) | [cours/devops.md](cours/devops.md) | Intermédiaire |

## Décisions techniques

| ADR | Sujet | Statut |
|-----|-------|--------|
| [ADR-001](decisions/ADR-001-stack-technique.md) | Choix de la stack technique | Accepté |

## Sessions de travail

| Session | Date | Sujet |
|---------|------|-------|
| [SESSION-001](sessions/SESSION-001-init.md) | 2026-06-30 | Initialisation du projet |
| [SESSION-002](sessions/SESSION-002-git-lancement.md) | 2026-06-30 | Git init + premier lancement API |
| [SESSION-003](sessions/SESSION-003-features-deploy.md) | 2026-06-30 | StructuralCodes, shear, deploy |

## Comment utiliser cette doc avec l'IA

1. **Nouvelle session IA** → donner le lien vers `02-HANDOFF-IA.md`
2. **Nouveau calcul Eurocode** → invoquer le skill `eurocode-calculations`
3. **Fin de session** → invoquer le skill `handoff-session`
4. **Apprendre un concept** → lire le cours du secteur concerné
5. **Faire sans IA** → suivre `03-WORKFLOW-HUMAIN-VS-IA.md`
