# Stratégie Madil4 — Constellation de repos portfolio

> Modèle inspiré de Mohamed Adil (madil4) — ingénieur structure néerlandais
> qui a construit une double identité ingénieur + développeur via des repos open source.

---

## Le modèle en bref

Mohamed Adil ne vend pas ses diplômes. Il vend sa capacité à **automatiser le travail
répétitif des bureaux d'études**. Son repo [Awatif](https://github.com/madil4/awatif)
(161 stars, TypeScript/WebGL) est devenu sa carte de visite.

**Ta cible** : Créer une constellation de 4-6 repos qui prouvent que tu peux :
1. **Calculer** — Eurocodes, FEM, béton armé
2. **Automatiser** — BIM, Excel, métrés
3. **Déployer** — API, web app, CI/CD, Docker
4. **Visualiser** — 3D web, rapports interactifs

---

## La constellation (roadmap)

### Vague 1 — Impact immédiat (2-4 semaines chacun)

| # | Repo | Statut | Prouve |
|---|------|--------|--------|
| 1 | **eurocode-calculator** | 🟢 En cours | Calculer + Déployer |
| 2 | excel-to-bim | ⏳ Planifié | Automatiser |
| 3 | structural-report-gen | ⏳ Planifié | Visualiser |

### Vague 2 — Profondeur (1-2 mois chacun)

| # | Repo | Prouve |
|---|------|--------|
| 4 | fem-web-viewer | Calculer + Visualiser |
| 5 | quantity-takeoff-api | Automatiser |
| 6 | portfolio-site | Déployer + Personal branding |

---

## eurocode-calculator — Vague 1, Repo 1

### Positionnement

> "J'ai remplacé les feuilles Excel de calcul structurel par une API REST
> testée, documentée et déployée. 3 Eurocodes, 9 tests, CI/CD, Docker."

### Stack vitrine

| Techno | Pourquoi c'est visible |
|--------|----------------------|
| Python | Langage #1 en data/ingénierie |
| FastAPI | Framework moderne, Swagger auto |
| eurocodepy | Lib active, montre veille technique |
| pytest + CI | Montre rigueur ingénieur |
| Docker | Montre compétence DevOps |
| GitHub Actions | Montre automatisation |

### Ce qui impressionne un recruteur / client

1. **Swagger UI live** — il peut tester l'API dans son navigateur
2. **Tests verts** — badge CI sur le README
3. **Code propre** — architecture routers/services/schemas
4. **Documentation** — cours, pas juste un README vide
5. **Calculs corrects** — vérifiés contre la norme

### Phrases pour LinkedIn / CV

- "API REST de vérification Eurocodes (EC2, EC3, EC7) — Python, FastAPI, eurocodepy"
- "Remplace les feuilles Excel de calcul structurel par des endpoints testés et déployés"
- "9 tests automatisés, CI/CD GitHub Actions, déploiement Docker"

---

## Comment enchaîner les vagues

```
Vague 1 (semaines 1-12)
├── eurocode-calculator ─── API calculs ────────┐
├── excel-to-bim ────────── Automatisation Excel ┤
└── structural-report-gen ── Rapports PDF/HTML ──┤
                                                  │
Vague 2 (mois 4-8)                               ▼
├── fem-web-viewer ──────── 3D WebGL ◄─── synergies
├── quantity-takeoff-api ── Métrés BIM
└── portfolio-site ──────── Vitrine de tout
```

### Règles d'enchaînement

1. **Finir avant de commencer** — chaque repo doit être déployable
2. **Réutiliser** — eurocode-calculator sera une dépendance des autres repos
3. **Documenter** — chaque repo a son handoff IA et ses cours
4. **Publier** — repo public GitHub dès la V0.1

---

## Métriques de succès

| Métrique | Objectif Vague 1 | Objectif Vague 2 |
|----------|-------------------|-------------------|
| Repos publics | 3 | 6 |
| Stars GitHub total | 50+ | 200+ |
| Endpoints API | 10+ | 30+ |
| Tests automatisés | 30+ | 100+ |
| Déploiements live | 2+ | 4+ |
| Posts LinkedIn | 3 | 10+ |

---

## Ressources

- [Awatif (madil4)](https://github.com/madil4/awatif) — référence du modèle
- [eurocodepy](https://github.com/pcachim/eurocodepy) — lib de calcul
- [StructuralCodes](https://github.com/fib-international/structuralcodes) — capacity-based design
- [FastAPI](https://fastapi.tiangolo.com/) — framework API
