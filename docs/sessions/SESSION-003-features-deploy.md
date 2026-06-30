# SESSION-003 — Features senior + git + déploiement

**Date** : 2026-06-30
**Agent** : Cursor

## Demande utilisateur

> Faire selon bonnes pratiques senior : git init + push GitHub, verify-shear,
> StructuralCodes capacity-based, déploiement Render/Railway.

## Livré

### Code
- `POST /beam/verify-shear` — StructuralCodes `VRdc`, `VRds`, `VRdmax`
- `POST /beam/verify-uls-capacity` — StructuralCodes `BeamSection.calculate_bending_strength()`
- `services/structuralcodes_setup.py` — adapter partagé EC2
- 14 tests pytest (5 nouveaux)

### DevOps
- Git repo dédié dans `eurocode-calculator/` (branche `main`)
- `render.yaml` — Blueprint Render
- `railway.toml` + `Dockerfile` — Railway
- `docs/DEPLOIEMENT.md`
- `.env.example`

### Git
- Suppression `.git` parent `Projet_1/` (anti-pattern monorepo accidentel)
- `git init -b main` dans `eurocode-calculator/`
- Premier commit à faire / push GitHub (gh CLI non installé)

## Référence

Journal détaillé : `docs/03-WORKFLOW-HUMAIN-VS-IA.md` → SESSION-003
