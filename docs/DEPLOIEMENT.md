# Déploiement

## Render (recommandé — gratuit, Blueprint)

1. Pousser le code sur GitHub (`main`)
2. [render.com](https://render.com) → **New** → **Blueprint**
3. Connecter le repo `eurocode-calculator`
4. Render lit `render.yaml` automatiquement
5. Deploy → URL live : `https://eurocode-calculator.onrender.com`

### Variables d'environnement Render

| Variable | Valeur |
|----------|--------|
| `PYTHON_VERSION` | `3.13.0` |
| `DEBUG` | `false` |

## Railway (alternative)

1. [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
2. Railway détecte le `Dockerfile` ou `railway.toml`
3. Port exposé automatiquement via `$PORT`

```bash
# CLI Railway (optionnel)
npm i -g @railway/cli
railway login
railway init
railway up
```

## Docker (local ou tout hébergeur)

```bash
docker build -t eurocode-calculator .
docker run -p 8000:8000 eurocode-calculator
```

## Vérification post-déploiement

```bash
curl https://<votre-url>/health
curl https://<votre-url>/docs
```

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) lance pytest + ruff à chaque push.
Branch protection recommandée : exiger CI verte avant merge.
