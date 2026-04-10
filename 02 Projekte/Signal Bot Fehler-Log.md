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

---

## Tradeprobleme / Verpasste Trades

### AH-Exit fehlt — After-Hours Trading unvollständig
- **Problem:** Bot kann AH kaufen (`LimitOrder` + `outsideRth=True` ✅), aber **nicht AH verkaufen** — Exit läuft über `MarketOrder` ohne `outsideRth=True` → wird erst bei Marktöffnung ausgeführt
- **Konkrete Auswirkung:** ISPC 09.04.2026 — Jack Signal AH bei $0.13, Kurs lief auf $0.20 (+54%). Bot hätte kaufen können, aber SL/TP wären nicht AH ausführbar gewesen → unkontrolliertes Overnight-Risiko
- **Fix:** Exit-Orders ebenfalls mit `outsideRth=True` als `LimitOrder` platzieren
- **Risiko beachten:** AH-Liquidität ist dünn — Slippage bei SL-Ausführung möglich
- **Priorität:** Medium — Wochenendprojekt 2026-04-12/13
- **Datei:** `ibkr_client.py` ~Zeile 370 (MarketOrder Exit)

### Verpasster Trade: ISPC 09.04.2026
- **Signal:** Jack Sparo AH — *"I am watching ISPC move AH. If it gets my order at 0.16–0.1625 filled..."*
- **Kurs bei Signal:** $0.13 → AH-Hoch $0.20 (+54%)
- **Warum kein Trade:** Safety-Block auf Keyword `"watching"` (inzwischen entfernt ✅)
- **Nachträgliche Bewertung:** Signal war mehrdeutig (Jackselbst unsicher, kein TP genannt, warnte vor Unberechenbarkeit) — Safety-Block war möglicherweise trotzdem korrekt
- **Potenzieller Gewinn:** ~$1.077 bei $2k Position ($0.13 → $0.20, 15.384 Shares)
- **Lehre:** Parser-Confidence allein reicht nicht — Signalqualität und AH-Ausführbarkeit separat prüfen
