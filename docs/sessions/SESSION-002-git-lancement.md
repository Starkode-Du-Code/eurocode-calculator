# SESSION-002 — Git init + premier lancement API

**Date** : 2026-06-30
**Acteur principal** : Hamed (humain)
**Documentation** : Agent IA (Cursor)

---

## Demande

Documenter systématiquement chaque action (demande, réponse IA, équivalent humain)
dans `docs/03-WORKFLOW-HUMAIN-VS-IA.md`.

## Actions humaines

1. `git init` dans `Projet_1/` (repo parent, branche `master`)
2. `cd eurocode-calculator`
3. `.venv\Scripts\activate`
4. `uvicorn eurocode_calculator.main:app --reload`
5. Test navigateur : `/` et `/docs` → 200 OK

## État git

```
Repo root : C:/Users/hamed/OneDrive/Bureau/Projet_1/.git/
Branche   : master
Commits   : aucun encore
Untracked : eurocode-calculator/
```

## État API

- Serveur Uvicorn actif avec `--reload`
- Swagger accessible sur http://localhost:8000/docs
- 9 tests pytest passent (validés session précédente)

## À faire session suivante

- [ ] Premier `git commit`
- [ ] Créer repo GitHub `eurocode-calculator`
- [ ] `git push`
- [ ] Décider : garder git à `Projet_1/` ou déplacer vers `eurocode-calculator/` seul

## Référence

Journal détaillé humain vs IA : `docs/03-WORKFLOW-HUMAIN-VS-IA.md` → SESSION-002
