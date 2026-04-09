---
tags: [ressource]
zuletzt-aktualisiert: 2026-04-09
---

# Claude Skills

Dokumentation aller installierten Claude Code Skills auf dem VPS.

## Installierte Skills (`/root/.claude/skills/`)

### brainstorming
Vor jeder Implementierung — klärt Requirements, Design und Intent bevor Code geschrieben wird. Verhindert dass wir in die falsche Richtung bauen.

### systematic-debugging
Strukturierter Debugging-Prozess. Wird bei hartnäckigen Bugs eingesetzt statt blindem Rumprobieren.

### writing-plans
Implementierungsplan schreiben bevor Code angefasst wird. Gut für größere Features.

### executing-plans
Einen fertigen Plan aus einer separaten Session abarbeiten — mit Review-Checkpoints.

### verification-before-completion
Vor "fertig" wirklich verifizieren dass alles funktioniert. Kein voreiliges "erledigt".

### test-driven-development
Tests zuerst schreiben, dann Implementierung. Für kritische Komponenten.

### dispatching-parallel-agents
Mehrere unabhängige Aufgaben gleichzeitig an Subagenten delegieren. Spart Zeit bei parallelen Tasks.

### subagent-driven-development
Implementierung mit Subagenten — für größere unabhängige Aufgabenblöcke.

### using-git-worktrees
Isolierte Git-Worktrees für Feature-Arbeit. Trennt Entwicklung vom laufenden System.

### finishing-a-development-branch
Branch-Abschluss strukturiert durchführen: Merge, PR oder Cleanup.

### requesting-code-review
Code Review anfordern bevor Merge — stellt sicher dass Arbeit die Requirements erfüllt.

### receiving-code-review
Code Review richtig verarbeiten — nicht blind umsetzen, sondern technisch prüfen.

### writing-skills
Neue Skills erstellen, testen und deployen.

### using-superpowers
Meta-Skill — erklärt wie man Skills findet und richtig einsetzt.

---

## Workflow: Wann welcher Skill?

| Situation | Skill |
|---|---|
| Neues Feature planen | `brainstorming` → `writing-plans` |
| Feature bauen | `executing-plans` |
| Bug fixen | `systematic-debugging` |
| Fertig? | `verification-before-completion` |
| Mehrere unabhängige Tasks | `dispatching-parallel-agents` |
| Branch abschließen | `finishing-a-development-branch` |

## Referenzen

- [[Claude Code Tools]]
