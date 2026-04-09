---
tags: [ressource]
---

# Claude Code Tools

Übersicht der genutzten Claude Code Features und Tools auf dem VPS.

## Setup

- **Modell:** claude-sonnet-4-6 (Standard), claude-opus-4-6 (Weekly Analyzer)
- **VPS:** Hostinger MK2, `/root/signal_bot/`
- **Obsidian Vault:** `/root/obsidian_vault/`
- **Memory:** `/root/.claude/projects/-root-signal-bot/memory/`

## Wichtige Slash-Commands

| Command | Funktion |
|---|---|
| `/cost` | API-Kosten der Session anzeigen |
| `/clear` | Kontext leeren |
| `/compact` | Kontext komprimieren |

## CLAUDE.md Dateien

| Pfad | Zweck |
|---|---|
| `/root/CLAUDE.md` | OpenClaw-Sicherheitsanleitung |
| `/root/signal_bot/CLAUDE.md` | Signal Bot Projektanleitung |
| `/root/obsidian_vault/CLAUDE.md` | Vault-Kontext und Routinen |

## Memory-System

Persistentes Gedächtnis unter `/root/.claude/projects/-root-signal-bot/memory/`:
- `user_profile.md` — Wer Dominic ist
- `project_context.md` — Signal Bot Kontext
- `feedback_style.md` — Wie Claude hier arbeiten soll
- `infrastructure_problems.md` — IBKR/systemd Probleme & Fixes
- `feedback_obsidian_vault.md` — Vault als Second Brain nutzen

## Obsidian als Second Brain

Ab 2026-04-09: Claude nutzt `/root/obsidian_vault/` als persistentes Gedächtnis.
Alles Wichtige aus unserer Arbeit wird dort gespeichert:
- Bugs, Fixes, Erkenntnisse
- Projektfortschritt
- Getroffene Entscheidungen
