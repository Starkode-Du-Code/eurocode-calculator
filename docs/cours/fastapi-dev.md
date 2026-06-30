# Cours — Développement API avec FastAPI

> FastAPI est le framework qui expose nos calculs Eurocodes en endpoints HTTP.

---

## 1. Qu'est-ce qu'une API REST ?

Une API REST expose des **ressources** via des **URLs** et des **verbes HTTP** :

| Verbe | Action | Exemple |
|-------|--------|---------|
| GET | Lire | `GET /health` → statut |
| POST | Créer / Calculer | `POST /beam/verify-uls` → résultat |
| PUT | Modifier | `PUT /materials/C30/37` |
| DELETE | Supprimer | `DELETE /cache` |

Notre API est principalement **POST** car chaque appel **calcule** un résultat.

---

## 2. FastAPI en 5 minutes

### Installation

```bash
pip install fastapi uvicorn[standard]
```

### App minimale

```python
from fastapi import FastAPI

app = FastAPI(title="Mon API")

@app.get("/health")
def health():
    return {"status": "ok"}
```

### Lancer

```bash
uvicorn main:app --reload
# → http://localhost:8000/docs (Swagger UI automatique)
```

---

## 3. Architecture de notre API

### Point d'entrée (main.py)

```python
def create_app() -> FastAPI:
    app = FastAPI(title="Eurocode Calculator API")
    app.include_router(beam_router)      # /beam/*
    app.include_router(column_router)    # /column/*
    app.include_router(foundation_router)  # /foundation/*
    return app
```

### Router (routers/beam.py) — couche HTTP

```python
router = APIRouter(prefix="/beam", tags=["Poutre — EC2"])

@router.post("/verify-uls", response_model=BeamVerifyULSResponse)
def post_verify_uls(request: BeamVerifyULSRequest):
    return verify_beam_uls(request)  # Délègue au service
```

**Règle** : le router ne fait QUE recevoir la requête et appeler le service.

### Service (services/beam_service.py) — couche métier

```python
def verify_beam_uls(request: BeamVerifyULSRequest) -> BeamVerifyULSResponse:
    concrete = ec.Concrete(request.concrete_grade)
    # ... calculs Eurocode ...
    return BeamVerifyULSResponse(verified=True, ...)
```

### Schema (schemas/beam.py) — couche validation

```python
class BeamVerifyULSRequest(BaseModel):
    concrete_grade: str = "C30/37"
    width_mm: float = Field(gt=0)
    moment_knm: float
```

---

## 4. Swagger UI — Tester sans code

1. Lancer l'API : `uvicorn eurocode_calculator.main:app --reload`
2. Ouvrir http://localhost:8000/docs
3. Cliquer sur un endpoint → "Try it out"
4. Remplir les paramètres → "Execute"
5. Voir la réponse JSON

C'est la **vitrine** du projet — un recruteur peut tester l'API en 30 secondes.

---

## 5. Tester l'API programmatiquement

### Avec TestClient (pytest)

```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.post("/beam/verify-uls", json={
    "concrete_grade": "C30/37",
    "width_mm": 300, "height_mm": 500,
    "moment_knm": 50
})
assert response.status_code == 200
assert response.json()["verified"] is True
```

### Avec curl (terminal)

```bash
curl -X POST http://localhost:8000/beam/verify-uls \
  -H "Content-Type: application/json" \
  -d '{"concrete_grade":"C30/37","width_mm":300,"height_mm":500,"moment_knm":50}'
```

### Avec httpx (Python async)

```python
import httpx

async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
    response = await client.post("/beam/verify-uls", json={...})
```

---

## 6. Ajouter un nouvel endpoint — pas à pas

1. **Schema** : définir request/response dans `schemas/`
2. **Service** : implémenter le calcul dans `services/`
3. **Router** : créer l'endpoint dans `routers/`
4. **Main** : `app.include_router(new_router)`
5. **Test** : 3 cas minimum dans `tests/`
6. **Vérifier** : `pytest` + Swagger UI

Voir le skill `.cursor/skills/eurocode-calculations/SKILL.md` pour la checklist complète.

---

## 7. Configuration

### Variables d'environnement (.env)

```env
DEBUG=true
PORT=8000
DEFAULT_GAMMA_C=1.5
```

### Settings (config.py)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    port: int = 8000
```

---

## Ressources

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) — officiel, excellent
- [Pydantic v2](https://docs.pydantic.dev/) — validation de données
- [Uvicorn](https://www.uvicorn.org/) — serveur ASGI
