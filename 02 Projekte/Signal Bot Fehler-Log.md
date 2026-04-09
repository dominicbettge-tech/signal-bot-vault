---
tags: [projekt, bugs]
status: aktiv
erstellt: 2026-04-09
---

# Signal Bot Fehler-Log

Dokumentation aller behobenen und offenen Bugs im [[Signal Bot v3]].

---

## Behobene Bugs

### P0: fill_price wurde nicht gesetzt
- **Problem:** Nach Order-Fill blieb `fill_price` NULL in der DB
- **Fix:** IBKR-Callback ausgewertet und `fill_price` beim Fill-Event gesetzt
- **Datum:** 2026-04-06

### P0: IBKR-Check beim Start
- **Problem:** Bot crashte wenn IBGateway nicht erreichbar war, ohne saubere Fehlermeldung
- **Fix:** Verbindungscheck mit Retry-Loop beim Start eingebaut
- **Datum:** 2026-04-06

### P1: PENDING-Status blieb hängen
- **Problem:** Orders blieben auf `pending` wenn IBKR sie ablehnte
- **Fix:** Status-Update auf `cancelled` bei IBKR-Reject
- **Datum:** 2026-04-07

### P1: Analyzer exit_price N/A
- **Problem:** Bei Exit-Signalen wurde kein `exit_price` gesetzt — Analyzer zeigte N/A
- **Ursache:** Exit-Price kommt vom IBKR-Fill, nicht aus dem Signal
- **Status:** Bekannt, Phase 2

---

## Offene Bugs / bekannte Probleme

### ~~GV Ghost-Short~~ ✅ Behoben
- **Problem:** Position -500 GV in IBKR, obwohl Trade in DB als `closed`
- **Fix:** BUY 500 Cover-Order ausgeführt — Position = 0, realized PNL = -$8.92
- **Datum:** 2026-04-09

### Replay-Bug nach Restart
- **Problem:** Alte Telegram-Nachrichten erhalten nach Bot-Restart Expiry ab "jetzt" statt original Timestamp
- **Auswirkung:** Können als neue Signale re-processed werden
- **Priorität:** Medium

### Separate API-Keys
- **To-do:** Separaten Anthropic API-Key für den Bot erstellen (aktuell shared)
