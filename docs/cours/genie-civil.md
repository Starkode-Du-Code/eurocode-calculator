# Cours — Génie Civil / Ingénierie Structure

> Concepts fondamentaux utilisés dans eurocode-calculator.

---

## 1. Résistance des Matériaux (RDM)

### Notions clés

| Notion | Symbole | Unité | Utilisé dans |
|--------|---------|-------|--------------|
| Contrainte normale | σ | MPa | Tous les calculs |
| Contrainte de cisaillement | τ | MPa | EC2 cisaillement |
| Moment fléchissant | M | kN·m | EC2 flexion |
| Effort normal | N | kN | EC3 compression |
| Effort tranchant | V | kN | EC2 cisaillement |
| Flèche | w | mm | EC2 SLS |
| Module d'Young | E | GPa | EC3 flambement |

### Relation contrainte-déformation

```
σ = E × ε     (loi de Hooke, domaine élastique)
```

### Flexion simple

```
σ = M × y / I

M_Rd = résistance de calcul de la section
M_Ed = moment de calcul (charges × portée)
Vérification : M_Ed ≤ M_Rd
```

---

## 2. Béton Armé (EC2)

### Classes de béton

| Classe | f_ck (MPa) | Usage typique |
|--------|------------|---------------|
| C20/25 | 20 | Fondations, remplissage |
| C25/30 | 25 | Éléments courants |
| C30/37 | 30 | Poutres, dalles |
| C40/50 | 40 | Précontrainte, haute résistance |

### Résistance de calcul

```
f_cd = α_cc × f_ck / γ_c

α_cc = 1.0 (EN 1992-1-1)
γ_c = 1.5 (valeur recommandée)
```

### Vérification flexion (simplifiée)

Pour une section rectangulaire en béton armé :
1. Définir la hauteur utile : `d = h - c - φ/2`
2. Calculer le moment résistant : dépend des armatures
3. Comparer : `M_Ed ≤ M_Rd`

**Dans notre API** : version simplifiée sans calcul d'armatures (conservateur).

### Diagramme contrainte-déformation du béton

```
σ
│    ┌───── f_cd
│   /
│  /  (palier)
│ /
│/____________ ε
0   ε_c2  ε_cu2
```

---

## 3. Structures Métalliques (EC3)

### Nuances d'acier

| Nuance | f_y (MPa) | Usage |
|--------|-----------|-------|
| S235 | 235 | Construction courante |
| S355 | 355 | Usage général (le plus courant) |
| S450 | 450 | Haute résistance |

### Flambement d'Euler

```
N_cr = π² × E × I / L²

Élancement : λ = L / i
Élancement réduit : λ̄ = (L/i) / π × √(f_y/E)
```

### Courbes de flambement

| Courbe | α | Pour |
|--------|---|------|
| a | 0.21 | Profilés laminés à chaud (forte imperfection) |
| b | 0.34 | Profilés laminés (HEA, IPE) |
| c | 0.49 | Tubes |
| d | 0.76 | Tôles |

### Facteur de réduction χ

```
φ = 0.5 × [1 + α(λ̄ - 0.2) + λ̄²]
χ = 1 / [φ + √(φ² - λ̄²)]
N_b,Rd = χ × A × f_y / γ_M1
```

---

## 4. Géotechnique (EC7)

### Types de sols et portance indicative

| Sol | q_ult (kPa) | φ (°) |
|-----|-------------|-------|
| Sable dense | 300 | 35-40 |
| Sable moyen | 200 | 30-35 |
| Argile raide | 150 | — |
| Argile molle | 30 | — |
| Roche | 3000+ | — |

### Vérification portance

```
σ_Ed = V_Ed / (B × L)     (contrainte appliquée)
σ_Rd = q_ult / γ_r         (résistance de calcul)
Vérification : σ_Ed ≤ σ_Rd
```

### Coefficients partiels EC7

| γ_r (résistance) | γ_G (poids propre) | γ_Q (charges) |
|-------------------|---------------------|------------------|
| 1.25 (DA1) | 1.35 | 1.5 |

---

## 5. Combinaisons de charges (EC0)

### États limites

| Type | Symbole | Exemple |
|------|---------|---------|
| Ultime (rupture) | ULS | Flexion, flambement |
| Service (fonctionnement) | SLS | Flèche, fissuration |
| Accidentel | ALS | Séisme, incendie |

### Combinaison ELU fondamentale (EC0 §6.4)

```
E_d = γ_G × G_k + γ_Q × Q_k,1 + γ_Q × ψ_0 × Q_k,2 + ...
```

---

## Ressources

- EN 1990 à EN 1998 (Eurocodes) — via votre bureau d'études
- [eurocodepy docs](https://pcachim.github.io/eurocodepy/) — implémentation Python
- Cours RDM/BA de votre formation d'ingénieur
- [Bael / EC2 comparatif](https://www.setra.fr) — guides SETRA gratuits
