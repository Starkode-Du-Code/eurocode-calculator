# ADR-001 — Choix de la stack technique

**Date** : 2026-06-30
**Statut** : Accepté
**Décideurs** : Hamed + Agent IA (session 001)

---

## Contexte

Nous devons choisir une stack pour eurocode-calculator, une API REST de vérification
structurelle Eurocodes. Le projet doit être :
- Déployable rapidement (2-4 semaines)
- Vitrine portfolio (Madil4 Model)
- Maintenable par un ingénieur + IA
- Testable automatiquement

## Décision

| Couche | Choix | Version |
|--------|-------|---------|
| Langage | Python | 3.12+ |
| Framework API | FastAPI | 0.115+ |
| Calculs Eurocode | eurocodepy | 2026.4+ |
| Capacity-based design | structuralcodes | 0.6+ |
| Validation données | Pydantic | v2 |
| Serveur ASGI | Uvicorn | 0.32+ |
| Tests | pytest + httpx | 8.3+ |
| Lint/format | Ruff | 0.8+ |
| CI/CD | GitHub Actions | — |
| Conteneur | Docker (python:3.12-slim) | — |
| Déploiement | Render ou Railway | gratuit |
| Couverture | Codecov | — |

## Alternatives considérées

### Langage

| Alternative | Pour | Contre | Verdict |
|-------------|------|--------|---------|
| **Python** | eurocodepy natif, écosystème data | Performance | ✅ Choisi |
| TypeScript/Node | Awatif (madil4) utilise TS | Pas de lib Eurocode mature | ❌ |
| C# / .NET | Robot Structural Analysis | Pas open source, lourd | ❌ |
| Julia | Calculs scientifiques | Écosystème petit, pas de lib EC | ❌ |

### Framework API

| Alternative | Pour | Contre | Verdict |
|-------------|------|--------|---------|
| **FastAPI** | Swagger auto, Pydantic, async, moderne | — | ✅ Choisi |
| Flask + flask-restx | Simple, connu | Pas de validation native, vieillissant | ❌ |
| Django REST | Batteries included | Trop lourd pour une API seule | ❌ |

### Librairie Eurocode

| Alternative | Pour | Contre | Verdict |
|-------------|------|--------|---------|
| **eurocodepy** | Active (2026), MIT, matériaux complets EC1-EC8 | Python 3.12+ requis | ✅ Principal |
| **structuralcodes** | Capacity-based, moment-curvature, fib | Plus complexe à intégrer | ✅ Complément |
| Calculs manuels | Contrôle total | Lent, erreurs, pas maintenable | ❌ |
| Excel + openpyxl | Familier pour ingénieurs | Pas une API, pas testable | ❌ |

## Conséquences

### Positives
- Swagger UI gratuit et automatique (vitrine portfolio)
- eurocodepy couvre EC1-EC8 avec matériaux typés
- pytest + CI = confiance dans les calculs
- Docker = déploiement reproductible

### Négatives
- Python 3.12+ obligatoire (exclut certains environnements d'entreprise)
- Calculs simplifiés au début (pas de vérification complète avec armatures)
- structuralcodes pas encore intégré (roadmap)

### Risques
- eurocodepy pourrait changer d'API entre versions → pinner la version
- Les calculs simplifiés ne remplacent pas un logiciel de BA certifié
- Pas d'authentification (OK pour portfolio, à ajouter en production)

## Architecture décidée

```
routers/ (HTTP mince) → services/ (logique Eurocode) → schemas/ (Pydantic)
```

Pas de base de données pour la V0.1 (calculs stateless).
