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

### Parser: Multi-Signal-Nachrichten werden nicht erkannt
- **Problem:** Eine Nachricht enthält mehrere Signale, Parser vergibt nur ein Verdict
- **Beispiel:** ALMS #4375 — "4 orders all filled buy" (Status) + "Sold one order at 15.82" (Partial Exit 25%)
- **Risiko:** Exit-Signal wird verschluckt, Position bleibt zu groß
- **Fix-Idee:** Parser muss Nachrichten splitten oder mehrere Signale pro Nachricht zurückgeben
- **Priorität:** P2 — betrifft vor allem Zusammenfassungs-Nachrichten
- **Gefunden:** Review 2026-04-13 (ALMS #4375)

### Parser: "will cut if no support" ist KEIN SL-Update
- **Nachricht:** "ALMS looks weak will most likely cut it if no support above 14.25"
- **Parser sagt:** STATUS_UPDATE → **korrekt!**
- **Begründung:** Jack überlegt laut, setzt keinen harten SL. 1 Minute später (#4372) sieht er den Rebound und hält. "Most likely cut it if..." = Beobachtung, keine Order.
- **Regel:** Konditionale SL-Aussagen ("if no support", "might cut", "will most likely") sind Status, kein STOP_LOSS_UPDATE. Nur explizite SL-Setzungen ("SL at X", "stop at X") sind echte Updates.
- **Gefunden:** Review 2026-04-13 (ALMS #4371)

### Parser: Fill-Bestätigung wird als neuer Entry erkannt
- **Problem:** "Filled" / "ALMs filled" nach einem Entry wird als neuer Entry klassifiziert statt als Status-Update
- **Zwei Fälle:**
  1. **Mit Reply:** Nachricht ist Reply auf Entry → Stage 0 hat Parent-Context, aber Classifier ignoriert ihn (z.B. ALMS #4369 → Reply auf #4365)
  2. **Ohne Reply:** Nachricht hat kein `reply_to_msg_id`, nur zeitliche Nähe + gleicher Ticker (z.B. ALMS #4368, 12 Min nach Entry, 2 andere Nachrichten dazwischen)
- **Risiko:** Bot öffnet zweite Position oder verdoppelt Shares — bei Live = echtes Geld
- **Fix-Idee:** Wenn Nachricht nur "filled" + Ticker enthält UND offene/pending Position für Ticker existiert → STATUS_UPDATE, kein Entry
- **Priorität:** P1 — vor Live-Gang fixen
- **Gefunden:** Review 2026-04-13 (ALMS)

### Replay-Bug nach Restart
- **Problem:** Alte Telegram-Nachrichten erhalten nach Bot-Restart Expiry ab "jetzt" statt original Timestamp
- **Auswirkung:** Können als neue Signale re-processed werden
- **Priorität:** Medium

### Separate API-Keys
- **To-do:** Separaten Anthropic API-Key für den Bot erstellen (aktuell shared)

---

### ⚠️ Strategie-Anpassungen aus RCT-Analyse (13.04.)
1. ~~**IBKR-DB Reconciliation**~~ ✅ `position_monitor.py` — `_reconcile_ibkr_positions()` jede Runde
2. ~~**Range-Orders: Mid statt Upper**~~ ✅ `signal_manager.py` — `entry_mid` statt `entry_high`
3. ~~**Halt-Awareness / Order-Change**~~ ✅ `signal_manager.py` — PENDING Orders werden cancelled + re-entered
4. ~~**Exit-Signal → immer IBKR prüfen**~~ ✅ `signal_manager.py` — Ghost-Position-Exit in `_handle_exit`
5. ~~**Averaging nach Halt**~~ ✅ `safety.py` — DEDUP Preis-Check >5% = Nachkauf erlaubt

### ~~P0: DB-IBKR Desync~~ ✅ Behoben (13.04.)
- **Problem:** RCT Trade #20 in DB als `closed`, aber IBKR zeigt 1.639 Shares
- **Fix 1:** Exit-Handler prüft IBKR direkt bei Ghost-Position → `signal_manager.py`
- **Fix 2:** Reconciliation in Position Monitor → `position_monitor.py`
- **Fix 3:** RCT Ghost-Position manuell geschlossen @$1.01 (realized PnL: -$360.93)

### ~~P1: Averaging-Signal als Duplikat geblockt~~ ✅ Behoben (13.04.)
- **Fix:** DEDUP vergleicht Preis — >5% Differenz = Nachkauf, nicht Duplikat → `safety.py`

### ~~P1: Order-Change "switched order to X" ignoriert~~ ✅ Behoben (13.04.)
- **Fix 1:** `ENTRY_UPDATE` Taxonomie + Mapping → `parser_rules.py`
- **Fix 2:** Entry-Handler cancelled PENDING Orders + re-enters → `signal_manager.py`
- **Fix 3:** Entry-Trigger-Pattern um "switched order" + "will try order" erweitert → `parser_rules.py`
- **Fix 4:** Opus-Validate-Prompt um ORDER-CHANGE-Erkennung erweitert → `parser.py`

### ~~P2: "will try one order" mit Preis rejected~~ ✅ Behoben (13.04.)
- **Fix 1:** "will try one order" / "will try an order" als ENTRY_KEYWORD → `safety.py`
- **Fix 2:** "will try order" als Entry-Trigger (übertrumpft Soft-Blocker) → `parser_rules.py`
- **Fix 3:** Opus-Prompt erkennt "will try one order at X" als Entry → `parser.py`

---

## Intraday-Download (2026-04-13 abgeschlossen)

- **49/51 Ticker** mit 1min-Bars erfolgreich via IBKR, 2.617.610 Bars, `data/price_data_1min.db`
- **CMBM + LVRO bei IBKR nicht verfügbar** (beide vermutlich delisted)
- **Notlösung 2026-04-14:** Daily-Bars via yfinance gezogen, Tabelle `bars_daily` in selber DB
  - CMBM 65 Bars, LVRO 65 Bars (jeweils 2025-10-14 bis 2026-01-15)
  - Entdeckung: beide Ticker waren an Jack-Tagen Monster-Moves (CMBM 29.10.: +165% Range, LVRO 02.01.: +184% Range)
- **TODO:** 1min-Bars für CMBM/LVRO inkl. PM/AH nachziehen — Quellen:
  - Polygon.io Starter ($29/Mo, hat delisted + OTC + PM/AH) ⭐
  - Alpaca Free (unsicher bei delisted, nur IEX)
- **Einschränkung Daily-Only:** TSL-Simulation für diese Ticker nur grob möglich (keine Intraday-Pfade)

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
