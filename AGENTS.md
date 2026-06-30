# AGENTS.md — Instructions pour l'agent IA

> Ce fichier est lu automatiquement par Cursor et les agents IA.
> Il définit le contexte, les règles et le workflow du projet.

## Identité du projet

- **Nom** : eurocode-calculator
- **Objectif** : API REST Python remplaçant les feuilles Excel de calcul structurel Eurocodes
- **Stratégie** : Vague 1 du "Madil4 Model" — prouver calcul + automatisation + déploiement
- **Public** : Ingénieurs structure, bureaux d'études, portfolio technique

## Stack technique

| Couche | Technologie | Version min |
|--------|-------------|-------------|
| Langage | Python | 3.12+ |
| API | FastAPI + Uvicorn | 0.115+ |
| Calculs | eurocodepy, structuralcodes | latest |
| Validation | Pydantic v2 | 2.10+ |
| Tests | pytest + httpx | 8.3+ |
| CI/CD | GitHub Actions | — |
| Conteneur | Docker | — |

## Architecture

```
src/eurocode_calculator/
├── main.py          # Point d'entrée FastAPI
├── config.py        # Settings (pydantic-settings)
├── routers/         # Endpoints HTTP (minces)
├── services/        # Logique métier Eurocodes
└── schemas/         # Modèles Pydantic request/response
```

**Règle d'or** : les routers ne contiennent PAS de logique de calcul.
Toute la logique Eurocode va dans `services/`.

## Conventions de code

- Langue du code : **anglais** (noms de variables, fonctions, classes)
- Langue de la doc utilisateur : **français**
- Type hints obligatoires sur toutes les fonctions publiques
- Docstrings Google style sur les services
- Un endpoint = un router + un service + un schema request + un schema response
- Tests dans `tests/test_<module>.py`, un fichier par domaine

## Commandes essentielles

```bash
# Installer
pip install -e ".[dev]"

# Lancer l'API en dev
uvicorn eurocode_calculator.main:app --reload

# Tests
pytest
pytest --cov=eurocode_calculator

# Lint
ruff check src tests
ruff format src tests

# Docker
docker build -t eurocode-calculator .
docker run -p 8000:8000 eurocode-calculator
```

## Workflow agent IA

### Avant de coder

1. Lire `docs/02-HANDOFF-IA.md` pour le contexte de la dernière session
2. Lire les ADR dans `docs/decisions/` pour les choix techniques verrouillés
3. Vérifier les issues/TODOs dans `docs/sessions/`

### Pendant le développement

1. Modifier le service d'abord, puis le schema, puis le router
2. Écrire/mettre à jour les tests correspondants
3. Lancer `pytest` avant de terminer
4. Ne pas toucher aux fichiers hors scope de la tâche

### Après chaque session

1. Mettre à jour `docs/02-HANDOFF-IA.md` avec :
   - Ce qui a été fait
   - Ce qui reste à faire
   - Décisions prises
   - Commandes exécutées
   - Fichiers modifiés
2. **Ajouter une entrée dans le journal** `docs/03-WORKFLOW-HUMAIN-VS-IA.md` :
   - Demande utilisateur (verbatim ou résumé)
   - Ce que l'IA a fait
   - Ce que l'humain a fait (si applicable)
   - Comment refaire sans IA (commandes pas à pas)
3. Créer un fichier `docs/sessions/SESSION-XXX-<sujet>.md` si session significative

## Endpoints planifiés (roadmap)

- [x] `POST /beam/verify-uls` — EC2 flexion simple (eurocodepy)
- [x] `POST /beam/verify-shear` — EC2 cisaillement (StructuralCodes)
- [x] `POST /beam/verify-uls-capacity` — EC2 flexion capacity-based (StructuralCodes)
- [x] `POST /column/buckling` — EC3 flambement
- [x] `POST /foundation/bearing` — EC7 portance
- [ ] `POST /beam/verify-punching` — EC2 poinçonnement
- [ ] `POST /column/biaxial` — EC3 flexion biaxiale (StructuralCodes)
- [ ] `POST /loads/combinations` — EC0/EC1 combinaisons de charges
- [ ] `GET /materials/concrete` — catalogue matériaux
- [ ] `GET /materials/steel` — catalogue aciers

## Skills projet

Les skills dans `.cursor/skills/` fournissent des workflows spécialisés :

- `handoff-session` — générer un relevé de fin de session
- `eurocode-calculations` — guide pour ajouter un nouveau calcul Eurocode

## Documentation de référence

| Document | Contenu |
|----------|---------|
| `docs/01-COURS-MASTER.md` | Cours complet : commandes, concepts, workflow |
| `docs/02-HANDOFF-IA.md` | Relevé de session (TOUJOURS mettre à jour) |
| `docs/03-WORKFLOW-HUMAIN-VS-IA.md` | Parcours manuel sans IA |
| `docs/cours/` | Cours par secteur (génie civil, python, devops…) |
| `docs/decisions/` | Architecture Decision Records (ADR) |

## Ce qu'il ne faut PAS faire

- Ne pas commit sans demande explicite de l'utilisateur
- Ne pas ajouter de dépendances sans ADR
- Ne pas mettre de secrets dans le code (.env est gitignored)
- Ne pas simplifier les calculs sans documenter les hypothèses
- Ne pas créer de fichiers markdown non demandés (sauf handoff/sessions)
