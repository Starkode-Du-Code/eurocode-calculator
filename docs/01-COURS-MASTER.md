# Cours Master — eurocode-calculator

> Guide complet : tout ce qui est fait dans ce projet, les commandes, les concepts,
> et comment être efficace avec l'IA pour le développer.

---

## Table des matières

1. [Vision du projet](#1-vision-du-projet)
2. [Quand on commence un projet — la checklist](#2-quand-on-commence-un-projet)
3. [Être efficace avec l'IA](#3-être-efficace-avec-lia)
4. [Commandes essentielles](#4-commandes-essentielles)
5. [Architecture expliquée](#5-architecture-expliquée)
6. [Les 3 endpoints en détail](#6-les-3-endpoints-en-détail)
7. [Le pipeline complet](#7-le-pipeline-complet)
8. [Prochaines étapes](#8-prochaines-étapes)

---

## 1. Vision du projet

### Le problème

Dans un bureau d'études structure, les calculs Eurocodes se font encore majoritairement dans Excel :
- Formules copiées-collées, erreurs fréquentes
- Pas de traçabilité ni de tests
- Impossible à intégrer dans un workflow BIM/automatisé
- Chaque ingénieur refait les mêmes calculs

### La solution

Une **API REST** qui expose les vérifications Eurocodes comme des endpoints HTTP :
- `POST /beam/verify-uls` → remplace la feuille Excel "Vérif poutre béton"
- Chaque calcul est **testé automatiquement** (pytest)
- **Swagger UI** auto-généré pour tester visuellement
- **Déployable** en un clic (Docker, Render, Railway)

### Le modèle Madil4

Mohamed Adil (ingénieur structure néerlandais) a prouvé qu'on peut construire une carrière
à l'intersection **génie civil + développement**. Son repo [Awatif](https://github.com/madil4/awatif)
(161 stars, TypeScript/WebGL) est sa carte de visite.

Ce projet est la **Vague 1** d'une constellation de 4-6 repos portfolio :
- **Calculer** (Eurocodes, FEM, béton armé) ← ce projet
- Automatiser (BIM, Excel, métrés)
- Déployer (API, web app, CI/CD, Docker) ← ce projet aussi
- Visualiser (3D web, rapports interactifs)

---

## 2. Quand on commence un projet

### Checklist jour 1 (ce qui a été fait ici)

```
Phase 0 — Cadrage (30 min)
├── [x] Définir le problème en 1 phrase
├── [x] Choisir la stack (voir ADR-001)
├── [x] Créer le repo avec structure de base
└── [x] Écrire AGENTS.md (instructions pour l'IA)

Phase 1 — Squelette (2-4h)
├── [x] pyproject.toml + dépendances
├── [x] Point d'entrée (main.py)
├── [x] 1 endpoint minimal qui fonctionne
├── [x] 1 test qui passe
└── [x] README avec commandes de démarrage

Phase 2 — Fondations (1 journée)
├── [x] Architecture routers/services/schemas
├── [x] 3 endpoints métier
├── [x] Tests pour chaque endpoint
├── [x] CI/CD GitHub Actions
└── [x] Dockerfile

Phase 3 — Documentation (1/2 journée)
├── [x] Cours master (ce fichier)
├── [x] Handoff IA
├── [x] Workflow humain vs IA
├── [x] Cours par secteur
└── [x] Configuration agent (rules + skills)
```

### Variantes selon le type de projet

| Type de projet | Adapter |
|----------------|---------|
| API seule (comme ici) | Focus endpoints + tests + Swagger |
| Web app | Ajouter frontend (React/Next.js) en vague 2 |
| CLI | Remplacer FastAPI par Typer/Click |
| Notebook | Jupyter + eurocodepy directement |
| Package pip | Focus sur `pip install` + docs API |

---

## 3. Être efficace avec l'IA

### Les 5 règles d'or

#### Règle 1 : Donner le contexte AVANT la tâche

```
❌ "Ajoute un endpoint pour le cisaillement"
✅ "Lis docs/02-HANDOFF-IA.md et AGENTS.md. Ensuite ajoute POST /beam/verify-shear
    en suivant le pattern existant dans services/beam_service.py"
```

#### Règle 2 : Une tâche = un scope précis

```
❌ "Améliore le projet"
✅ "Ajoute les tests pour le cas où concrete_grade est invalide dans test_beam.py"
```

#### Règle 3 : Toujours demander un handoff en fin de session

```
"Fais un relevé de session et mets à jour docs/02-HANDOFF-IA.md"
```

#### Règle 4 : Vérifier le travail de l'IA

```bash
pytest                    # Les tests passent ?
ruff check src tests      # Pas d'erreurs de lint ?
uvicorn ... --reload      # L'API démarre ?
# Tester manuellement sur http://localhost:8000/docs
```

#### Règle 5 : Utiliser les skills et rules du projet

Les fichiers dans `.cursor/skills/` et `.cursor/rules/` guident l'IA automatiquement.
Ne pas réinventer les instructions à chaque session.

### Prompts types efficaces

| Objectif | Prompt |
|----------|--------|
| Nouveau calcul | "Suis le skill eurocode-calculations pour ajouter POST /beam/verify-shear" |
| Debug | "pytest échoue sur test_beam_verify_uls_ok, voici l'erreur : [coller]" |
| Refactoring | "Extrais la logique de flambement dans column_service.py sans changer l'API" |
| Documentation | "Mets à jour le handoff et crée SESSION-002" |
| Déploiement | "Configure le déploiement Render avec le Dockerfile existant" |
| Revue | "Relis services/beam_service.py et vérifie les hypothèses EC2" |

### Ce que l'IA fait bien

- Générer le boilerplate (schemas, routers, tests)
- Traduire une formule Excel en code Python
- Écrire la CI/CD et le Dockerfile
- Créer la documentation
- Refactorer en respectant les patterns existants

### Ce que l'IA fait mal (vérifier manuellement)

- Les calculs Eurocodes complexes (vérifier contre la norme)
- Les coefficients partiels et annexes nationales
- Les choix d'architecture (lire les ADR)
- Les décisions de sécurité (secrets, auth)

---

## 4. Commandes essentielles

### Python & environnement virtuel

| Commande | À quoi ça sert | Variantes |
|----------|----------------|-----------|
| `python -m venv .venv` | Créer un environnement virtuel isolé | `python3` sur Linux/macOS |
| `.venv\Scripts\activate` | Activer le venv (Windows) | `source .venv/bin/activate` (Linux/macOS) |
| `deactivate` | Désactiver le venv | — |
| `pip install -e ".[dev]"` | Installer le projet en mode éditable + deps dev | `pip install -r requirements.txt` (sans dev) |
| `pip list` | Voir les packages installés | `pip show eurocodepy` (détail d'un package) |

### Lancer l'API

| Commande | À quoi ça sert | Variantes |
|----------|----------------|-----------|
| `uvicorn eurocode_calculator.main:app --reload` | Lancer l'API en dev avec hot-reload | `--port 3000` pour changer le port |
| `python -m eurocode_calculator.main` | Lancer via le point d'entrée Python | — |
| `eurocode-api` | Lancer via le script console (après install) | — |

### Tests

| Commande | À quoi ça sert | Variantes |
|----------|----------------|-----------|
| `pytest` | Lancer tous les tests | `pytest -x` (stop au 1er échec) |
| `pytest tests/test_beam.py` | Tester un seul fichier | `pytest -k "beam"` (filtre par nom) |
| `pytest --cov=eurocode_calculator` | Tests + couverture de code | `--cov-report=html` (rapport HTML) |
| `pytest -v` | Mode verbeux (détail de chaque test) | `--tb=long` (traceback complet) |

### Qualité de code

| Commande | À quoi ça sert | Variantes |
|----------|----------------|-----------|
| `ruff check src tests` | Vérifier le style et les erreurs | `ruff check --fix` (corriger auto) |
| `ruff format src tests` | Formater le code | — |

### Docker

| Commande | À quoi ça sert | Variantes |
|----------|----------------|-----------|
| `docker build -t eurocode-calculator .` | Construire l'image | `--no-cache` (forcer rebuild) |
| `docker run -p 8000:8000 eurocode-calculator` | Lancer le conteneur | `-d` (background) |
| `docker ps` | Voir les conteneurs actifs | `docker logs <id>` (voir les logs) |

### Git

| Commande | À quoi ça sert | Variantes |
|----------|----------------|-----------|
| `git init` | Initialiser le repo | — |
| `git add .` | Stager tous les fichiers | `git add src/` (un dossier) |
| `git commit -m "message"` | Commiter | — |
| `git push -u origin main` | Pousser sur GitHub | — |

### Tester l'API manuellement

```bash
# Health check
curl http://localhost:8000/health

# Vérification poutre
curl -X POST http://localhost:8000/beam/verify-uls \
  -H "Content-Type: application/json" \
  -d '{"concrete_grade":"C30/37","width_mm":300,"height_mm":500,"moment_knm":50}'

# Ou ouvrir http://localhost:8000/docs dans le navigateur (Swagger UI)
```

---

## 5. Architecture expliquée

```
Requête HTTP                    Réponse JSON
     │                               ▲
     ▼                               │
┌─────────┐    ┌──────────┐    ┌──────────┐
│ Router  │───▶│ Service  │───▶│ Schema   │
│ (mince) │    │ (calcul) │    │ Response │
└─────────┘    └──────────┘    └──────────┘
     │              │
     │         ┌────┴────┐
     │         │eurocodepy│
     │         │structural│
     │         │  codes   │
     │         └─────────┘
     ▼
┌─────────┐
│ Schema  │
│ Request │
└─────────┘
```

### Pourquoi cette séparation ?

| Couche | Responsabilité | Testable ? |
|--------|---------------|------------|
| **Router** | Recevoir HTTP, appeler le service | Via TestClient (intégration) |
| **Service** | Logique Eurocode, calculs | Directement (unitaire) |
| **Schema** | Validation des données entrée/sortie | Via Pydantic (automatique) |
| **Config** | Variables d'environnement | Via Settings |

---

## 6. Les 3 endpoints en détail

### POST /beam/verify-uls (EC2)

**Remplace** : Feuille Excel "Vérif flexion poutre béton"

**Entrée** : classe béton, dimensions section, moment de calcul
**Sortie** : vérifié oui/non, M_Rd, taux d'utilisation
**Norme** : EN 1992-1-1, flexion simple
**Hypothèse actuelle** : section rectangulaire sans calcul d'armatures (conservateur)

### POST /column/buckling (EC3)

**Remplace** : Feuille Excel "Vérif flambement poteau"

**Entrée** : nuance acier, profilé, longueur, effort normal
**Sortie** : vérifié oui/non, N_b,Rd, élancement λ̄
**Norme** : EN 1993-1-1 §6.3
**Hypothèse actuelle** : flambement autour de l'axe faible, courbe b

### POST /foundation/bearing (EC7)

**Remplace** : Feuille Excel "Vérif portance semelle"

**Entrée** : type de sol, dimensions semelle, charge verticale
**Sortie** : vérifié oui/non, σ_Rd, contrainte appliquée
**Norme** : EN 1997-1 §6.5
**Hypothèse actuelle** : portance simplifiée (pas de pente de rupture)

---

## 7. Le pipeline complet

```
Développement local          CI/CD                    Production
───────────────          ─────────              ──────────────
Code Python              git push               Docker container
    │                        │                       │
    ▼                        ▼                       ▼
pytest (local)           GitHub Actions           Render / Railway
ruff check               ├── ruff check           (gratuit)
uvicorn --reload         ├── pytest               │
    │                    ├── coverage              ▼
    ▼                    └── codecov           https://eurocode-calc.onrender.com
localhost:8000/docs                              │
                                                 ▼
                                            /docs (Swagger)
```

---

## 8. Prochaines étapes

Voir la liste priorisée dans [02-HANDOFF-IA.md](02-HANDOFF-IA.md).

Pour approfondir un secteur :
- Génie civil → [cours/genie-civil.md](cours/genie-civil.md)
- Eurocodes → [cours/eurocodes.md](cours/eurocodes.md)
- Python → [cours/python.md](cours/python.md)
- FastAPI → [cours/fastapi-dev.md](cours/fastapi-dev.md)
- DevOps → [cours/devops.md](cours/devops.md)

Pour comprendre le cheminement IA → humain :
- [03-WORKFLOW-HUMAIN-VS-IA.md](03-WORKFLOW-HUMAIN-VS-IA.md)

Pour la vision portfolio :
- [05-STRATEGIE-MADIL4.md](05-STRATEGIE-MADIL4.md)
