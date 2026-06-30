# Handoff IA — Relevé de session

> **Dernière mise à jour** : 2026-06-30 — Session 003 (features + deploy)
> **Statut projet** : V0.2 — 6 endpoints, StructuralCodes intégré, prêt push GitHub

---

## Fait ✅

- [x] 6 endpoints API (3 beam + column + foundation + health)
- [x] StructuralCodes : cisaillement + flexion capacity-based
- [x] 14 tests pytest — tous verts
- [x] Git repo dédié `eurocode-calculator/` branche `main`
- [x] `render.yaml`, `railway.toml`, `docs/DEPLOIEMENT.md`
- [x] Commit initial stagé (à confirmer/pousser)

## À faire ⏳

1. [ ] **Push GitHub** — `gh` non installé, action humaine requise
2. [ ] Déployer sur Render via Blueprint
3. [ ] Mettre à jour badge CI dans README (remplacer PLACEHOLDER)
4. [ ] `POST /beam/verify-punching`
5. [ ] `POST /loads/combinations` (EC0/EC1)

## Nouveaux endpoints

| Route | Lib | Usage |
|-------|-----|-------|
| `POST /beam/verify-shear` | StructuralCodes | Cisaillement EC2 |
| `POST /beam/verify-uls-capacity` | StructuralCodes | Flexion avec armatures |

## Commandes

```powershell
cd eurocode-calculator
.venv\Scripts\activate
pytest
uvicorn eurocode_calculator.main:app --reload
```

## Push GitHub

```powershell
gh auth login   # après winget install GitHub.cli
gh repo create eurocode-calculator --public --source=. --push
```
