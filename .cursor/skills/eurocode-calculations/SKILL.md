---
name: eurocode-calculations
description: Guide pour ajouter un nouveau calcul Eurocode à l'API. Utiliser quand l'utilisateur demande un nouvel endpoint de vérification structurelle, un nouveau calcul EC2/EC3/EC7, ou l'intégration de StructuralCodes.
---

# Ajouter un calcul Eurocode

## Checklist

```
- [ ] 1. Identifier la norme et la clause (ex: EC2 §6.2 cisaillement)
- [ ] 2. Créer le schema request/response dans schemas/
- [ ] 3. Implémenter la logique dans services/
- [ ] 4. Créer le router dans routers/
- [ ] 5. Enregistrer le router dans main.py
- [ ] 6. Écrire les tests (OK, FAIL, 422)
- [ ] 7. Mettre à jour AGENTS.md roadmap
- [ ] 8. Lancer pytest
```

## Structure d'un nouveau endpoint

### 1. Schema (`schemas/<domain>.py`)

```python
class ShearVerifyRequest(BaseModel):
    concrete_grade: str = "C30/37"
    width_mm: float = Field(gt=0)
    shear_force_kn: float

class ShearVerifyResponse(BaseModel):
    verified: bool
    utilization_ratio: float
    message: str
```

### 2. Service (`services/<domain>_service.py`)

```python
def verify_shear(request: ShearVerifyRequest) -> ShearVerifyResponse:
    """Vérification cisaillement — EN 1992-1-1 §6.2."""
    concrete = ec.Concrete(request.concrete_grade)
    # ... calcul ...
    return ShearVerifyResponse(...)
```

### 3. Router (`routers/<domain>.py`)

```python
@router.post("/verify-shear", response_model=ShearVerifyResponse)
def post_verify_shear(request: ShearVerifyRequest) -> ShearVerifyResponse:
    return verify_shear(request)
```

### 4. Tests (`tests/test_<domain>.py`)

Toujours 3 cas minimum : succès, échec, validation erreur (422).

## Librairies

| Besoin | Lib | Import |
|--------|-----|--------|
| Matériaux béton/acier | eurocodepy | `import eurocodepy as ec` |
| Profilés acier | eurocodepy | `ec.SteelProfile("HEA200")` |
| Combinaisons charges | eurocodepy | `from eurocodepy.ec1 import LoadCombinations` |
| Capacity-based design | structuralcodes | `from structuralcodes import ...` |
| Sols EC7 | eurocodepy ec7 | `from eurocodepy.ec7 import ...` |

## Références

- eurocodepy docs : https://pcachim.github.io/eurocodepy/
- StructuralCodes docs : https://fib-international.github.io/structuralcodes/
- Cours détaillé : `docs/cours/eurocodes.md`
