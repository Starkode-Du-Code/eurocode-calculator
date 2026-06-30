# Cours — Python pour l'ingénierie

> Python est le langage utilisé dans eurocode-calculator.
> Ce cours couvre ce dont vous avez besoin, pas tout Python.

---

## 1. Installation et environnement

### Installer Python 3.12+

```bash
# Vérifier la version
python --version   # → Python 3.12.x minimum

# Windows : télécharger sur https://python.org
# Ou via winget :
winget install Python.Python.3.12
```

### Environnement virtuel (obligatoire)

```bash
python -m venv .venv          # Créer
.venv\Scripts\activate        # Activer (Windows)
source .venv/bin/activate     # Activer (Linux/macOS)
deactivate                    # Désactiver
```

**Pourquoi ?** Isole les dépendances du projet. Sans venv, `pip install` pollue Python global.

### Installer des packages

```bash
pip install fastapi           # Un package
pip install -e ".[dev]"       # Projet en mode éditable + extras
pip freeze > requirements.txt # Exporter les versions
```

---

## 2. Syntaxe essentielle

### Variables et types

```python
# Types de base
name: str = "C30/37"
fck: float = 30.0
width_mm: int = 300
is_verified: bool = True

# Listes et dictionnaires
grades = ["C25/30", "C30/37", "C40/50"]
soil_capacity = {"dense_sand": 300, "soft_clay": 30}
```

### Fonctions

```python
def calculate_moment_resistant(fcd: float, b: float, d: float) -> float:
    """Calcule M_Rd pour une section rectangulaire."""
    return 0.15 * fcd * b * d**2

# Appel
m_rd = calculate_moment_resistant(fcd=20.0, b=0.3, d=0.46)
```

### Classes

```python
class BeamSection:
    def __init__(self, width_mm: float, height_mm: float):
        self.width_mm = width_mm
        self.height_mm = height_mm

    @property
    def area_mm2(self) -> float:
        return self.width_mm * self.height_mm

section = BeamSection(300, 500)
print(section.area_mm2)  # 150000
```

---

## 3. Modules et imports

```python
# Import standard
import math
result = math.sqrt(144)  # 12.0

# Import avec alias
import eurocodepy as ec
concrete = ec.Concrete("C30/37")

# Import sélectif
from eurocodepy.ec1 import Load, LoadType

# Import local (notre projet)
from eurocode_calculator.services.beam_service import verify_beam_uls
```

---

## 4. Pydantic — Validation de données

Utilisé pour les schemas request/response de l'API.

```python
from pydantic import BaseModel, Field

class BeamRequest(BaseModel):
    width_mm: float = Field(gt=0, description="Largeur [mm]")
    height_mm: float = Field(gt=0, description="Hauteur [mm]")
    moment_knm: float

# Validation automatique
req = BeamRequest(width_mm=300, height_mm=500, moment_knm=50)  # OK
req = BeamRequest(width_mm=-100, height_mm=500, moment_knm=50)   # Erreur !
```

**Pourquoi ?** FastAPI utilise Pydantic pour valider les entrées HTTP automatiquement.

---

## 5. Tests avec pytest

```python
# tests/test_example.py

def test_moment_positive():
    result = calculate_moment_resistant(20, 0.3, 0.46)
    assert result > 0

def test_moment_zero_height():
    result = calculate_moment_resistant(20, 0.3, 0)
    assert result == 0

# Lancer : pytest tests/test_example.py -v
```

### Fixtures (données de test réutilisables)

```python
import pytest

@pytest.fixture
def standard_beam():
    return BeamSection(width_mm=300, height_mm=500)

def test_area(standard_beam):
    assert standard_beam.area_mm2 == 150000
```

---

## 6. Gestion des erreurs

```python
# Erreur basique
try:
    concrete = ec.Concrete("INVALID")
except (KeyError, ValueError) as e:
    print(f"Classe de béton inconnue : {e}")

# Dans l'API, Pydantic gère les erreurs de validation (HTTP 422)
# FastAPI gère les exceptions non catchées (HTTP 500)
```

---

## 7. Commandes du quotidien

| Commande | Quand l'utiliser |
|----------|------------------|
| `python -m venv .venv` | Début de chaque projet |
| `pip install -e ".[dev]"` | Après clone ou changement de deps |
| `python -c "import eurocodepy; print(eurocodepy.__version__)"` | Vérifier une lib |
| `pytest -x` | Debug un test qui échoue |
| `python -m pdb script.py` | Debugger pas à pas |
| `ruff check --fix src/` | Corriger le style auto |

---

## Ressources

- [Python officiel](https://docs.python.org/3/tutorial/) — tutoriel
- [Real Python](https://realpython.com/) — articles pratiques
- [Pydantic docs](https://docs.pydantic.dev/) — validation
- [pytest docs](https://docs.pytest.org/) — tests
