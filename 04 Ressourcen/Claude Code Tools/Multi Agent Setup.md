---
tags: [ressource, claude-code, testing]
erstellt: 2026-04-09
---

# Multi Agent Setup — Zwei Claude Code Instanzen

## Konzept

Zwei separate Claude Code Instanzen auf dem VPS mit verschiedenen Accounts laufen lassen.

```bash
# Instanz 1 (Standard / Pro)
~/.claude/

# Instanz 2 (zweiter Account)
CLAUDE_CONFIG_DIR=~/.claude_account2 claude
```

Jede Instanz hat eigene Login-Session, Settings und Memory.

## Vorteile für Bot-Stresstests

**Instanz 1 — Angreifer/Tester**
- Sendet simulierte Signale im Schnelldurchlauf
- Feuert Edge Cases (gleichzeitige Signale, ungültige Daten, Duplikate)
- Hammert API mit Requests

**Instanz 2 — Beobachter/Analyst**
- Überwacht Logs live während Instanz 1 stresst
- Prüft DB-Konsistenz in Echtzeit
- Erkennt Race Conditions und Memory Leaks

## Anwendungsfälle

### Signal Bot
- Instanz 1: 20 Signale gleichzeitig → testet Deduplication + Position Limits
- Instanz 2: prüft ob alle korrekt verarbeitet, nichts doppelt getradet

### Binance Bot (später)
- Instanz 1: simuliert Volumenspikes + Taranis-News gleichzeitig
- Instanz 2: bewertet ob Signal-Logik korrekt priorisiert

## Referenzen

- [[Claude Code Tools]]
- [[Signal Bot v3]]
- [[Binance Volume Trading Bot]]
