# Cours — Eurocodes (EC0 à EC8)

> Référence rapide des normes utilisées et planifiées dans eurocode-calculator.

---

## Vue d'ensemble

| Code | Norme | Sujet | Statut dans l'API |
|------|-------|-------|-------------------|
| EC0 | EN 1990 | Bases de calcul | ⏳ Planifié (combinaisons) |
| EC1 | EN 1991 | Actions sur structures | ⏳ Planifié (charges) |
| EC2 | EN 1992 | Béton armé | ✅ Flexion ULS |
| EC3 | EN 1993 | Structures métalliques | ✅ Flambement |
| EC5 | EN 1995 | Structures bois | ⏳ Futur |
| EC7 | EN 1997 | Géotechnique | ✅ Portance |
| EC8 | EN 1998 | Séisme | ⏳ Futur |

---

## EC2 — Béton armé (EN 1992-1-1)

### Parties utilisées

| Section | Sujet | Endpoint |
|---------|-------|----------|
| §3 | Matériaux | `ec.Concrete("C30/37")` |
| §6.1 | Résistance longitudinale (flexion) | `POST /beam/verify-uls` |
| §6.2 | Cisaillement | ⏳ `/beam/verify-shear` |
| §6.4 | Appuis d'about | ⏳ Futur |
| §6.5 | Effort localisé | ⏳ Futur |
| §6.4.5 | Poinçonnement | ⏳ `/beam/verify-punching` |
| §7.2 | Fissuration SLS | ⏳ Futur |

### Avec eurocodepy

```python
import eurocodepy as ec

# Matériau
concrete = ec.Concrete("C30/37")
concrete.fck   # 30 MPa
concrete.fcd   # 20 MPa (γc=1.5)

# Acier d'armature
steel = ec.ReinforcementSteel("B500B")
steel.fyk  # 500 MPa
```

### Avec StructuralCodes (capacity-based)

```python
from structuralcodes import codes
from structuralcodes.materials.concrete import create_concrete
from structuralcodes.sections import GenericSection

# Section avec calcul moment-courbure complet
concrete = create_concrete("C30/37")
# ... configuration section + armatures ...
# ... calcul M-Rd précis ...
```

---

## EC3 — Structures métalliques (EN 1993-1-1)

### Parties utilisées

| Section | Sujet | Endpoint |
|---------|-------|----------|
| §3 | Matériaux | `ec.Steel("S355")` |
| §6.2 | Résistance section | ⏳ Futur |
| §6.3 | Flambement | `POST /column/buckling` |
| §6.3.3 | Flexion déviée | ⏳ `/column/biaxial` |

### Avec eurocodepy

```python
import eurocodepy as ec

steel = ec.Steel("S355")
steel.fy   # 355 MPa
steel.fu   # 510 MPa

# Profilé (si disponible dans le catalogue)
profile = ec.SteelProfile("HEA200")
profile.A   # mm²
profile.iy  # mm (rayon de giration)
```

---

## EC7 — Géotechnique (EN 1997-1)

### Parties utilisées

| Section | Sujet | Endpoint |
|---------|-------|----------|
| §6.5 | Portance fondations superficielles | `POST /foundation/bearing` |
| §9 | Poussees des terres | ⏳ Futur |

### Avec eurocodepy

```python
from eurocodepy.ec7 import Soil, bearing_resistance

soil = Soil("dense_sand")
# Résistance de portance selon Annex D
```

---

## EC0/EC1 — Combinaisons de charges

### Planifié : POST /loads/combinations

```python
from eurocodepy.ec1 import Load, LoadType, LoadCombinations, CombinationType

loads = [
    Load("G1", LoadType.PERMANENT, 10.0),    # kN/m
    Load("Q1", LoadType.LIVE, 5.0),
    Load("W1", LoadType.WIND, 3.0),
]
combos = LoadCombinations(loads)
uls = combos.get(CombinationType.ULS)
# → {"G1": 13.5, "Q1": 7.5, "W1": 4.5}
```

---

## Annexes nationales

| Pays | Annexe | Impact |
|------|--------|--------|
| France (NF) | NF EN 1992-1-1/NA | γ_c, ψ_0, classes d'exposition |
| Belgique (NBN) | NBN EN 1992-1-1/NA | Coefficients spécifiques |
| Suisse (SIA) | SIA 262 | Remplace partiellement EC2 |

**Dans notre API** : valeurs recommandées CEN par défaut.
Les annexes nationales seront un paramètre `national_annex` dans une version future.

---

## Références

- [eurocodepy documentation](https://pcachim.github.io/eurocodepy/)
- [StructuralCodes documentation](https://fib-international.github.io/structuralcodes/)
- [Eurocodes en ligne](https://eurocodes.jrc.ec.europa.eu/) — textes officiels
