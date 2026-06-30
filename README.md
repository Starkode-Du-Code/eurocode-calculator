# Eurocode Calculator API

API REST de vérification structurelle selon les Eurocodes — remplace les feuilles Excel de calcul par des endpoints testables et déployables.

## Endpoints

| Méthode | Route | Norme | Description |
|---------|-------|-------|-------------|
| `POST` | `/beam/verify-uls` | EC2 | Flexion ULS (pré-dimensionnement rapide) |
| `POST` | `/beam/verify-shear` | EC2 | Cisaillement (StructuralCodes) |
| `POST` | `/beam/verify-uls-capacity` | EC2 | Flexion capacity-based (StructuralCodes) |
| `POST` | `/column/buckling` | EC3 | Flambement poteau acier |
| `POST` | `/foundation/bearing` | EC7 | Portance fondation superficielle |
| `GET` | `/docs` | — | Swagger UI interactif |
| `GET` | `/health` | — | Health check |

## Démarrage rapide

```bash
# Prérequis : Python 3.12+
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

pip install -e ".[dev]"
uvicorn eurocode_calculator.main:app --reload
```

Ouvrir http://localhost:8000/docs

## Tests

```bash
pytest
pytest --cov=eurocode_calculator --cov-report=term-missing
```

## Docker

```bash
docker build -t eurocode-calculator .
docker run -p 8000:8000 eurocode-calculator
```

## Stack

- **Python 3.12+** — langage
- **FastAPI** — framework API REST
- **eurocodepy** — calculs Eurocodes (matériaux, combinaisons)
- **StructuralCodes** — capacity-based design (à intégrer progressivement)
- **pytest** — tests unitaires
- **GitHub Actions** — CI/CD
- **Docker** — conteneurisation

## Documentation

Toute la documentation pédagogique est dans [`docs/`](docs/00-INDEX.md) :

- [Cours master](docs/01-COURS-MASTER.md) — guide complet du projet
- [Handoff IA](docs/02-HANDOFF-IA.md) — relevé de session pour reprendre le travail
- [Workflow humain vs IA](docs/03-WORKFLOW-HUMAIN-VS-IA.md) — comment faire sans IA
- [Stratégie Madil4](docs/05-STRATEGIE-MADIL4.md) — constellation de repos portfolio

## Déploiement

Voir [docs/DEPLOIEMENT.md](docs/DEPLOIEMENT.md) — Render (recommandé) ou Railway.

[![CI](https://github.com/PLACEHOLDER/eurocode-calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/PLACEHOLDER/eurocode-calculator/actions)
