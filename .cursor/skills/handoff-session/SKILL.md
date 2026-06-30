---
name: handoff-session
description: Génère un relevé de fin de session pour handoff entre IA ou entre humain et IA. Utiliser en fin de session de travail, quand l'utilisateur demande un relevé, ou avant de changer d'agent IA.
---

# Handoff Session — Relevé de passation

## Quand utiliser

- Fin de chaque session de travail significative
- Avant de changer d'agent IA (Cursor, Claude, ChatGPT…)
- Quand l'utilisateur dit "fais un relevé" ou "handoff"

## Procédure

1. Lire l'état actuel du projet (`git status`, fichiers modifiés)
2. Mettre à jour `docs/02-HANDOFF-IA.md` avec le template ci-dessous
3. Si session importante, créer `docs/sessions/SESSION-XXX-<sujet>.md`

## Template handoff

```markdown
# Handoff — Session [NUMÉRO] — [DATE]

## Contexte
[1-2 phrases : objectif de la session]

## Fait ✅
- [ ] Item 1
- [ ] Item 2

## En cours 🔄
- [ ] Item avec état partiel

## À faire ⏳
- [ ] Prochaine tâche prioritaire
- [ ] Tâche secondaire

## Décisions prises
| Décision | Raison | Alternative écartée |
|----------|--------|---------------------|
| ... | ... | ... |

## Fichiers modifiés
- `path/to/file.py` — description du changement

## Commandes exécutées
\`\`\`bash
pip install -e ".[dev]"
pytest
\`\`\`

## Problèmes / blocages
- [Description et solution tentée]

## Pour reprendre
1. Lire ce fichier
2. [Instruction spécifique]
3. Lancer `pytest` pour vérifier l'état
```

## Règles

- Être factuel, pas de spéculation
- Lister TOUS les fichiers modifiés
- Indiquer les commandes exactes exécutées
- Numéroter les sessions séquentiellement (SESSION-001, 002…)
