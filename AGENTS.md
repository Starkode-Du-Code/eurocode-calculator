# AGENTS.md — Instructions pour l'agent IA

> Ce fichier est lu par les agents IA (Cursor, Kimi, etc.) pour comprendre le contexte, les conventions et le workflow du projet.
> Il doit rester synchronisé avec l'état réel du code. Mettre à jour ce fichier quand la stack, l'architecture ou les processus changent.

---

## 1. Vue d'ensemble du projet

- **Nom** : `eurocode-calculator`
- **Version** : `0.1.0`
- **Objectif** : API REST Python de vérification structurelle selon les Eurocodes (EC2 béton, EC3 acier, EC7 sols). Elle remplace des feuilles Excel de calcul par des endpoints testables, documentés et déployables.
- **Stratégie** : Vague 1 du "Madil4 Model" — prouver calcul + automatisation + déploiement.
- **Public cible** : Ingénieurs structure, bureaux d'études, portfolio technique.
- **Langue du code** : anglais (variables, fonctions, classes).
- **Langue de la documentation utilisateur et des docstrings** : français.
- **État actuel** : 6 endpoints implémentés, 14 tests pytest verts, prêt pour déploiement Render/Railway/Docker.

---

## 2. Stack technique

| Couche | Technologie | Version / Détails |
|--------|-------------|-------------------|
| Langage | Python | `>=3.12` (développé et testé sur 3.13) |
| Framework API | FastAPI | `>=0.115.0` |
| Serveur ASGI | Uvicorn | `[standard]>=0.32.0` |
| Validation données | Pydantic v2 | `>=2.10.0` |
| Configuration | pydantic-settings | `>=2.6.0` |
| Calculs Eurocode (interne) | `src/eurocode_calculator/core` | EC2 béton, EC3 acier/profilés, matériaux |
| Calculs capacity-based | structuralcodes | `>=0.6.0` (EC2 cisaillement, flexion avec armatures) |
| Tests | pytest + httpx + pytest-cov | `>=8.3.0` |
| Lint / format | Ruff | `>=0.8.0`, line-length 120, cible py312 |
| CI/CD | GitHub Actions | `.github/workflows/ci.yml` |
| Couverture | Codecov | upload depuis la CI sur Python 3.12 |
| Conteneur | Docker | `python:3.12-slim-bookworm` |
| Déploiement | Render (recommandé), Railway, Docker | fichiers `render.yaml`, `railway.toml`, `Dockerfile` |

**Remarque sur les dépendances** : `eurocodepy` a été retiré des dépendances core pour éviter les frictions de build au déploiement. Il reste disponible en extra optionnel (`pip install -e ".[eurocode]"`) pour tests ou référence. Les calculs Eurocodes de base (matériaux, flexion simplifiée EC2, flambement EC3) sont implémentés dans le module interne `src/eurocode_calculator/core`.

---

## 3. Architecture et organisation du code

Le code source se trouve dans `src/eurocode_calculator/`.

```
src/eurocode_calculator/
├── __init__.py              # version 0.1.0
├── main.py                  # Point d'entrée FastAPI (create_app, run)
├── config.py                # Settings pydantic-settings (env vars)
├── routers/                 # Endpoints HTTP (couche mince)
│   ├── beam.py
│   ├── column.py
│   └── foundation.py
├── services/                # Logique métier Eurocode
│   ├── beam_service.py              # POST /beam/verify-uls (core EC2, simplifié)
│   ├── beam_shear_service.py        # POST /beam/verify-shear (structuralcodes)
│   ├── beam_capacity_service.py     # POST /beam/verify-uls-capacity (structuralcodes)
│   ├── column_service.py            # POST /column/buckling (core EC3 + formule analytique)
│   ├── foundation_service.py        # POST /foundation/bearing (données typiques EC7)
│   └── structuralcodes_setup.py     # Helpers EC2 capacity-based
├── core/                    # Calculs Eurocodes internes (sans eurocodepy)
│   ├── materials.py
│   ├── ec2_concrete.py
│   └── ec3_steel.py
└── schemas/                 # Modèles Pydantic request/response
    ├── beam.py
    ├── column.py
    └── foundation.py
```

### Règles d'architecture

- **Routers minces** : ils ne contiennent PAS de logique de calcul. Ils reçoivent le schema, appellent le service et retournent le schema.
- **Services** : tout le calcul Eurocode, les hypothèses et les messages utilisateur y sont centralisés.
- **Schemas** : un endpoint = un schema `Request` + un schema `Response`.
- **Stateless** : pas de base de données en V0.1. Chaque requête est indépendante.

### Endpoints implémentés

| Méthode | Route | Norme | Service | Description |
|---------|-------|-------|---------|-------------|
| `POST` | `/beam/verify-uls` | EC2 | `beam_service.py` | Flexion ULS simplifiée (section rectangulaire, sans armatures détaillées) |
| `POST` | `/beam/verify-shear` | EC2 §6.2 | `beam_shear_service.py` | Cisaillement avec `VRdc`, `VRds`, `VRdmax` via StructuralCodes |
| `POST` | `/beam/verify-uls-capacity` | EC2 | `beam_capacity_service.py` | Flexion capacity-based avec armatures via `BeamSection` |
| `POST` | `/column/buckling` | EC3-1-1 §6.3 | `column_service.py` | Flambement poteau acier (formule de Perry-Robertson simplifiée) |
| `POST` | `/foundation/bearing` | EC7-1 §6.5 | `foundation_service.py` | Portance semelle superficielle (valeurs indicatives de sol) |
| `GET` | `/health` | — | `main.py` | Health check |
| `GET` | `/` | — | `main.py` | Liste des endpoints |
| `GET` | `/docs` | — | FastAPI | Swagger UI interactive |
| `GET` | `/redoc` | — | FastAPI | ReDoc |

---

## 4. Configuration

Les paramètres sont gérés par `pydantic-settings` dans `src/eurocode_calculator/config.py`.

Variables d'environnement (voir `.env.example`) :

| Variable | Défaut | Description |
|----------|--------|-------------|
| `DEBUG` | `false` | Active le rechargement automatique d'uvicorn |
| `HOST` | `0.0.0.0` | Interface d'écoute |
| `PORT` | `8000` | Port d'écoute |
| `APP_NAME` | `"Eurocode Calculator API"` | Nom affiché dans la doc OpenAPI |
| `DEFAULT_GAMMA_C` | `1.5` | Coefficient partiel béton par défaut |
| `DEFAULT_GAMMA_S` | `1.0` | Coefficient partiel acier par défaut |
| `DEFAULT_GAMMA_M` | `1.15` | Coefficient partiel matériaux métalliques par défaut |

Le fichier `.env` est gitignoré. Copier `.env.example` vers `.env` pour le développement local.

---

## 5. Commandes essentielles

### Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate        # Windows

pip install -e ".[dev]"
# ou, si eurocodepy est nécessaire pour comparaison/référence :
pip install -e ".[dev,eurocode]"
```

### Lancer l'API en développement

```bash
uvicorn eurocode_calculator.main:app --reload
# ou
python -m eurocode_calculator.main
```

La documentation interactive est disponible sur `http://localhost:8000/docs`.

### Tests

```bash
pytest                                    # 14 tests
pytest --cov=eurocode_calculator         # avec couverture
pytest --cov=eurocode_calculator --cov-report=term-missing
```

La couverture minimale est configurée à 70 % dans `pyproject.toml` (`fail_under = 70`).

### Lint et formatage

```bash
ruff check src tests
ruff format src tests
```

Ruff utilise :
- `line-length = 120`
- `target-version = "py312"`
- règles `E`, `F`, `I`, `W`

### Docker

```bash
docker build -t eurocode-calculator .
docker run -p 8000:8000 eurocode-calculator
```

---

## 6. Conventions de code

### Style

- **Imports** : stdlib → third-party → local. Ruff trie automatiquement les imports.
- **Type hints** obligatoires sur toutes les fonctions publiques.
- **Docstrings** style Google sur les fonctions de service ; décrire les hypothèses et référencer la clause Eurocode (ex: EN 1992-1-1 §6.2).
- **Nommage** : respecter la notation Eurocode dans les champs API (`fck`, `fcd`, `gamma_c`, `moment_ed_knm`, `utilization_ratio`).
- **Langue** : code en anglais, docstrings et messages en français.

### Structure d'un nouvel endpoint

1. Créer le schema `Request` / `Response` dans `schemas/<domain>.py`.
2. Implémenter la logique dans `services/<domain>_service.py`.
3. Créer la route dans `routers/<domain>.py`.
4. Enregistrer le router dans `main.py`.
5. Ajouter les tests dans `tests/test_<domain>.py` (minimum : cas OK, cas FAIL, cas 422).
6. Mettre à jour la roadmap dans `AGENTS.md`.
7. Lancer `pytest` avant de terminer.

### Calculs structurels

- Documenter les hypothèses simplificatrices dans la docstring.
- Retourner systématiquement un `utilization_ratio` (`M_Ed/M_Rd`, `N_Ed/N_Rd`, `σ_Ed/σ_Rd`).
- Utiliser le module interne `core` pour les matériaux, catalogues et calculs analytiques EC2/EC3.
- Utiliser `structuralcodes` pour les vérifications capacity-based avancées.
- Chaque calcul doit être vérifiable contre une solution analytique manuelle ; ajouter le cas de référence dans les tests avec les valeurs attendues.

---

## 7. Tests

- **Framework** : pytest avec `fastapi.testclient.TestClient`.
- **Fixture** : `client` définie dans `tests/conftest.py`.
- **Fichiers** : un fichier par domaine (`test_beam.py`, `test_column.py`, `test_foundation.py`, `test_health.py`).
- **Nombre actuel** : 14 tests, tous passants.
- **Scénarios obligatoires** pour chaque endpoint :
  - Cas passant (`ok`) : vérifier que `verified` est `True` et que les valeurs retournées sont cohérentes.
  - Cas non passant (`fail`) : vérifier que `verified` est `False` et `utilization_ratio > 1.0`.
  - Cas de validation 422 : envoyer des dimensions négatives ou des champs manquants.

Configuration pytest (dans `pyproject.toml`) :
- `testpaths = ["tests"]`
- `pythonpath = ["src"]`
- `addopts = "-v --tb=short"`

---

## 8. CI/CD et déploiement

### GitHub Actions

Fichier `.github/workflows/ci.yml` :

- Déclenché sur `push` vers `main`/`develop` et sur `pull_request` vers `main`.
- Matrice Python : `3.12` et `3.13`.
- Étapes :
  1. Checkout du code.
  2. Setup Python.
  3. Installation : `pip install -e ".[dev]"`.
  4. Lint : `ruff check src tests`.
  5. Tests avec couverture : `pytest --cov=eurocode_calculator --cov-report=xml --cov-report=term-missing`.
  6. Upload couverture vers Codecov (uniquement sur Python 3.12).

### Render (recommandé)

- Fichier `render.yaml` (Blueprint).
- Runtime Python, plan gratuit.
- `buildCommand` : `pip install -e .`
- `startCommand` : `uvicorn eurocode_calculator.main:app --host 0.0.0.0 --port $PORT`
- Health check sur `/health`.
- Variables d'environnement définies : `PYTHON_VERSION=3.13.0`, `DEBUG=false`.

### Railway (alternative)

- Fichier `railway.toml` : builder Dockerfile, healthcheck `/health`, restart `ON_FAILURE`.
- Railway peut aussi utiliser directement le `Dockerfile` présent à la racine.

### Docker

- Multi-stage build : `python:3.12-slim-bookworm` (builder + runtime).
- Utilise `uv` comme résolveur/installateur de dépendances.
- Installe uniquement les dépendances core (pas `dev`, pas `eurocode`).
- Image finale plus légère en copiant les site-packages du builder.
- Expose le port `8000`.
- Commande par défaut : `uvicorn eurocode_calculator.main:app --host 0.0.0.0 --port 8000`.

### Vérification post-déploiement

```bash
curl https://<votre-url>/health
curl https://<votre-url>/docs
```

---

## 9. Organisation de la documentation

Toute la documentation pédagogique et de suivi est dans `docs/`.

| Document | Contenu |
|----------|---------|
| `docs/00-INDEX.md` | Carte de navigation de la documentation |
| `docs/01-COURS-MASTER.md` | Cours complet : commandes, concepts, workflow |
| `docs/02-HANDOFF-IA.md` | Relevé de session — état courant du projet |
| `docs/03-WORKFLOW-HUMAIN-VS-IA.md` | Parcours manuel sans IA |
| `docs/04-DEMARRAGE-PROJET.md` | Checklist jour 1 d'un nouveau projet |
| `docs/05-STRATEGIE-MADIL4.md` | Vision long terme, constellation de repos portfolio |
| `docs/DEPLOIEMENT.md` | Instructions détaillées Render / Railway / Docker |
| `docs/cours/` | Cours par secteur (génie civil, python, FastAPI, DevOps, Eurocodes) |
| `docs/decisions/` | Architecture Decision Records (ADR) |
| `docs/sessions/` | Comptes-rendus de sessions de travail |

### Règles de documentation

- **Avant chaque session** : lire `docs/02-HANDOFF-IA.md`.
- **Après chaque session** : mettre à jour `docs/02-HANDOFF-IA.md` avec ce qui a été fait, ce qui reste, les décisions prises, les commandes exécutées et les fichiers modifiés.
- **Session significative** : créer un fichier `docs/sessions/SESSION-XXX-<sujet>.md`.
- **Nouvelle ADR** : si un choix technique important est verrouillé, l'ajouter dans `docs/decisions/`.

---

## 10. Skills et règles Cursor

Le répertoire `.cursor/` contient des règles et skills utilisés par Cursor (et lisibles par les autres agents) :

- `.cursor/rules/project-core.mdc` : standards fondamentaux, architecture, tests obligatoires.
- `.cursor/rules/python-standards.mdc` : style Python, type hints, docstrings, patterns.
- `.cursor/rules/structural-engineering.mdc` : principes de calcul Eurocode, notation, validation.
- `.cursor/skills/eurocode-calculations/SKILL.md` : checklist pour ajouter un nouveau calcul Eurocode.
- `.cursor/skills/handoff-session/SKILL.md` : template de relevé de fin de session.

---

## 11. Roadmap des endpoints

| Route | Norme | Statut | Implémentation |
|-------|-------|--------|----------------|
| `POST /beam/verify-uls` | EC2 | ✅ | `beam_service.py` (core EC2, simplifié) |
| `POST /beam/verify-shear` | EC2 §6.2 | ✅ | `beam_shear_service.py` (structuralcodes) |
| `POST /beam/verify-uls-capacity` | EC2 | ✅ | `beam_capacity_service.py` (structuralcodes) |
| `POST /column/buckling` | EC3-1-1 §6.3 | ✅ | `column_service.py` |
| `POST /foundation/bearing` | EC7-1 §6.5 | ✅ | `foundation_service.py` |
| `GET /health` | — | ✅ | `main.py` |
| `POST /beam/verify-punching` | EC2 | ⬜ | Roadmap |
| `POST /column/biaxial` | EC3 | ⬜ | Roadmap (structuralcodes) |
| `POST /loads/combinations` | EC0/EC1 | ⬜ | Roadmap |
| `GET /materials/concrete` | — | ⬜ | Roadmap |
| `GET /materials/steel` | — | ⬜ | Roadmap |

---

## 12. Considérations de sécurité

- **Pas d'authentification** en V0.1. C'est acceptable pour un portfolio / POC, mais doit être ajoutée avant toute mise en production réelle.
- **Pas de secrets dans le code** : les variables sensibles vont dans `.env` (gitignoré). Utiliser `.env.example` comme modèle.
- **Calculs à usage informatif** : les vérifications actuelles sont simplifiées et ne remplacent pas un logiciel de calcul structurel certifié. Toute simplification doit être documentée dans la docstring du service concerné.
- **Dépendances** : `structuralcodes` évolue rapidement ; penser à pinner la version si un comportement de calcul capacity-based devient critique. Le module interne `core` est maîtrisé et ne dépend pas d'une lib externe.

---

## 13. Ce qu'il ne faut PAS faire

- Ne pas commit sans demande explicite de l'utilisateur.
- Ne pas ajouter de dépendances sans documenter la raison (idéalement via une ADR).
- Ne pas mettre de secrets dans le code source.
- Ne pas simplifier les calculs sans documenter les hypothèses.
- Ne pas créer de fichiers markdown non demandés, sauf handoff/sessions/ADR.
- Ne pas placer de logique métier dans les routers.

---

## 14. Références rapides

- eurocodepy : https://pcachim.github.io/eurocodepy/
- StructuralCodes : https://fib-international.github.io/structuralcodes/
- FastAPI : https://fastapi.tiangolo.com/
- Pydantic : https://docs.pydantic.dev/
