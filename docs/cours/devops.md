# Cours — DevOps (CI/CD, Docker, Déploiement)

> Automatiser la qualité et le déploiement de eurocode-calculator.

---

## 1. Git — Contrôle de version

### Workflow quotidien

```bash
git status                    # Voir les changements
git add src/ tests/           # Stager des fichiers
git commit -m "feat: add shear verification endpoint"
git push origin main          # Pousser sur GitHub
```

### Convention de commits

| Préfixe | Usage | Exemple |
|---------|-------|---------|
| `feat:` | Nouvelle fonctionnalité | `feat: add EC2 shear endpoint` |
| `fix:` | Correction de bug | `fix: correct buckling chi factor` |
| `test:` | Ajout/modif tests | `test: add foundation edge cases` |
| `docs:` | Documentation | `docs: update handoff session 002` |
| `ci:` | CI/CD | `ci: add Python 3.13 to matrix` |
| `refactor:` | Refactoring | `refactor: extract material lookup` |

---

## 2. GitHub Actions — CI/CD

### Qu'est-ce que la CI ?

**Continuous Integration** : à chaque `git push`, un robot :
1. Installe Python
2. Installe les dépendances
3. Vérifie le style (ruff)
4. Lance les tests (pytest)
5. Mesure la couverture (codecov)

Si un test échoue → le push est marqué rouge sur GitHub.

### Notre workflow (.github/workflows/ci.yml)

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -e ".[dev]"
      - run: ruff check src tests
      - run: pytest --cov=eurocode_calculator
```

### Badge CI sur le README

```markdown
![CI](https://github.com/<user>/eurocode-calculator/actions/workflows/ci.yml/badge.svg)
```

---

## 3. Docker — Conteneurisation

### Pourquoi Docker ?

- "Ça marche sur ma machine" → ça marche partout
- Déploiement identique en local, staging, production
- Isolation complète (Python, deps, config)

### Notre Dockerfile

```dockerfile
FROM python:3.12-slim     # Image de base légère
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src/ src/
RUN pip install --no-cache-dir -e .
EXPOSE 8000
CMD ["uvicorn", "eurocode_calculator.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Commandes Docker

| Commande | Action |
|----------|--------|
| `docker build -t eurocode-calculator .` | Construire l'image |
| `docker run -p 8000:8000 eurocode-calculator` | Lancer |
| `docker ps` | Conteneurs actifs |
| `docker logs <id>` | Voir les logs |
| `docker stop <id>` | Arrêter |
| `docker rmi eurocode-calculator` | Supprimer l'image |

### Docker Compose (optionnel, multi-services)

```yaml
# docker-compose.yml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
```

```bash
docker compose up -d    # Lancer en background
docker compose down     # Arrêter
```

---

## 4. Déploiement — Render (gratuit)

### Étapes

1. Pousser le code sur GitHub
2. Créer un compte sur https://render.com
3. New → Web Service → Connecter le repo GitHub
4. Configuration :
   - **Build Command** : `pip install -e .`
   - **Start Command** : `uvicorn eurocode_calculator.main:app --host 0.0.0.0 --port $PORT`
   - **Environment** : Python 3
5. Deploy → URL live en 2-3 minutes

### Alternative : Railway

1. https://railway.app → New Project → Deploy from GitHub
2. Railway détecte le Dockerfile automatiquement
3. URL live instantanée

---

## 5. Qualité de code — Ruff

```bash
ruff check src tests          # Vérifier
ruff check --fix src tests    # Corriger automatiquement
ruff format src tests         # Formater
```

Ruff remplace flake8 + isort + black en un seul outil, 10-100x plus rapide.

---

## 6. Couverture de tests — Codecov

```bash
pytest --cov=eurocode_calculator --cov-report=xml
```

Codecov lit le fichier `coverage.xml` et affiche un rapport sur GitHub.
Objectif : > 80% de couverture.

---

## 7. Pipeline complet visualisé

```
Développeur                    GitHub                     Production
─────────                    ──────                     ──────────
                                                            
Code + git push ──────────▶ Actions CI                    
                            ├── ruff ✓                    
                            ├── pytest ✓ ──▶ Codecov      
                            └── badge vert                
                                                        
                            Render/Railway ◀── Dockerfile 
                                    │                     
                                    ▼                     
                            https://xxx.onrender.com/docs 
```

---

## Checklist déploiement

- [ ] Repo GitHub public
- [ ] CI verte (badge)
- [ ] Dockerfile fonctionnel
- [ ] Compte Render ou Railway
- [ ] Service déployé
- [ ] URL dans le README
- [ ] Swagger accessible publiquement

---

## Ressources

- [GitHub Actions docs](https://docs.github.com/en/actions)
- [Docker getting started](https://docs.docker.com/get-started/)
- [Render docs](https://render.com/docs)
- [Ruff](https://docs.astral.sh/ruff/)
