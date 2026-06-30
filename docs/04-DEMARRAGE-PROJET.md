# Démarrage d'un nouveau projet — Checklist

> Réutilisable pour chaque nouveau repo de la constellation Madil4.

---

## Phase 0 — Cadrage (30 min)

- [ ] **Problème en 1 phrase** : "Je résous ___ pour ___"
- [ ] **Utilisateur cible** : ingénieur structure / développeur / les deux
- [ ] **Livrable** : API / web app / CLI / package pip / notebook
- [ ] **Critère de succès** : "Ça marche quand ___"
- [ ] **Stack** : choisir et documenter dans un ADR

## Phase 1 — Squelette (2-4h)

```bash
mkdir <nom-projet> && cd <nom-projet>
python -m venv .venv && .venv\Scripts\activate
git init
```

- [ ] `pyproject.toml` avec dépendances
- [ ] `.gitignore` (Python, .env, .venv)
- [ ] Structure `src/<package>/`
- [ ] `main.py` avec 1 endpoint `/health` qui retourne `{"status": "ok"}`
- [ ] 1 test qui passe
- [ ] `README.md` avec commandes install + run
- [ ] `AGENTS.md` avec contexte pour l'IA

## Phase 2 — Fondations (1 journée)

- [ ] Architecture en couches (routers/services/schemas ou équivalent)
- [ ] 2-3 features métier fonctionnelles
- [ ] Tests pour chaque feature (OK + FAIL + validation)
- [ ] CI/CD GitHub Actions (lint + test)
- [ ] Dockerfile

## Phase 3 — Documentation (1/2 journée)

- [ ] `docs/00-INDEX.md` — table des matières
- [ ] `docs/01-COURS-MASTER.md` — guide complet
- [ ] `docs/02-HANDOFF-IA.md` — relevé de session
- [ ] `docs/03-WORKFLOW-HUMAIN-VS-IA.md` — parcours manuel
- [ ] `docs/cours/` — cours par secteur utilisé
- [ ] `.cursor/rules/` — règles pour l'agent IA
- [ ] `.cursor/skills/` — workflows spécialisés

## Phase 4 — Vitrine (1 journée)

- [ ] Repo public sur GitHub
- [ ] README avec badges (CI, coverage, version)
- [ ] Déploiement (Render, Railway, ou Vercel)
- [ ] Lien Swagger / démo live dans le README
- [ ] Post LinkedIn / portfolio

## Prompt IA pour démarrer un nouveau projet

```
Crée la base du projet <nom> en suivant la checklist de docs/04-DEMARRAGE-PROJET.md.
Stack : <stack>. Feature principale : <description>.
Inclure AGENTS.md, rules, skills, et documentation complète.
```

## Variantes par type de projet

### API backend (comme eurocode-calculator)
- Focus : endpoints + tests + Swagger + Docker
- Déploiement : Render / Railway

### Web app (vague 2+)
- Ajouter : frontend React/Next.js dans `frontend/`
- Monorepo ou repos séparés
- Déploiement : Vercel (front) + Render (back)

### Package pip
- Focus : `pip install <nom>` + docs API
- PyPI publish via GitHub Actions
- Pas besoin de Docker

### Outil CLI
- Remplacer FastAPI par Typer
- `pip install` + commande console
- Tests via `subprocess` ou `CliRunner`

### Notebook d'ingénierie
- Jupyter + eurocodepy directement
- Export en PDF/HTML pour le bureau d'études
- Pas de CI/CD nécessaire au début
