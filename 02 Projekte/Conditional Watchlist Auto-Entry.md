---
tags: [signal-bot, feature, backlog, parser]
status: idee
erstellt: 2026-04-14
priorität: nach Phase 1 + Testcenter
---

# Conditional Watchlist → Auto-Entry

Jack kommuniziert Setups oft **vorab**: er beschreibt Pattern + Preis-Levels, und trifft den Entry selbst erst wenn die Bedingung eintritt. Aktuell erkennt der Bot nur explizite "place order"-Signale und verpasst das Setup-Handwerk.

## Motivierender Case: LAES 2026-02-12 → 2026-03-16

**Setup-Ankündigung (msg 5113, 2026-02-12 19:11 ET):**
> "I am paying attention to LAES. Current chart if it gets below 3.58 and stays above 3.36 it might represent double bottoms. And it may push a move by 8% to 12% from around these levels! If you are interested place price alerts 🔔 around those levels!"

**Tatsächlicher Entry von Jack (msg 5409, 2026-03-16 08:35 ET, ~4 Wochen später):**
> "LAES is dropping pre market. I might add some for intra day trade and over night swing if it gets my order at 3.18~3.32 filled. Below 3.00 will be a bearish zone."

**Fill (msg 5411, 09:41 ET):**
> "Got two orders filled at 3.29 3.31. Left only one at 3.18 opens."

→ Jack hat uns das Muster erklärt, dann selbst mitgespielt. Ein autonomer Bot hätte den Setup früh erkennen und selbst ausführen können.

## Quellen für Conditional Watchlist Einträge

Zwei Input-Kanäle für die gleiche `watchlist_conditions`-Tabelle:

### Quelle A: Jack's Text (Parser-extrahiert)
- "if below 3.58 and stays above 3.36" (msg 5113)
- "RSI oversold below 1.95 OR break 2.35" (msg 5617)

### Quelle B: Technische Indikatoren (Bot-generiert)
**Washout-Re-Entry Trigger** — automatisch generiert wenn:
1. Ticker war in letzten 90 Tagen im Universe (Jack erwähnt oder getradet)
2. Current Drawdown vom 20d-Hoch > 25%
3. RSI(14) in letzten 5 Tagen <= 30
4. Current RSI > yesterday RSI (Trend-Umkehr)
5. Today Low > Yesterday Low (Higher Low)
6. Volume today < 0.7 × 20d avg (Capitulation vorbei)
7. SPY Regime-Filter ok

**LAES Fallbeispiel 2026-04-09:**
- Drawdown: −36% vom 3.30 Hoch ✅
- RSI deep oversold (Chart) ✅
- Volume 28M @ Crash → 8M aktuell ✅
- Higher Low: 2.02 → 2.05 → 2.13 ✅
- Hätte Entry @ 2.10 getriggert, SL 1.98, TP1 2.27 (+8%), TP2 2.42 (+15%)
- Heute bei 2.21 = +5.2% unrealized

## Konzept

### 1. Parser erweitern
Neuer Signal-Typ `conditional_setup` mit Feldern:
- `trigger_zone` (oben/unten)
- `support_zone`
- `pattern` (double_bottom, breakout, etc.)
- `direction` (long/short)
- `target_pct_min`, `target_pct_max`
- `expiry` (default 7-14 Tage)

### 2. Monitor-State
Neue Tabelle `watchlist_conditions`:
```sql
id, ticker, condition_json, created_at, expires_at, status (active/triggered/expired/cancelled)
```

### 3. Intraday-Engine
Separater Task der Live-Preise gegen aktive Conditions matcht. Bei Match:
- Logge Trigger-Event
- Sende Telegram-Alert (Modus 1) ODER
- Platziere Limit-Order (Modus 2, erst nach Evidenz)

### 4. Modi — schrittweise aktivieren
- **Phase A:** Alert-Only — Bot sagt "Jacks Setup LAES aktiv" ohne zu traden
- **Phase B:** Auto-Entry mit sehr kleiner Size (10% der normalen)
- **Phase C:** Volle Size wenn EV nachgewiesen

## Risiken

- **Parser-Mehrdeutigkeit:** "may", "might", "if" sind nicht automatisch Intent. Jack meint manchmal nur "price alert zur Beobachtung"
- **Kein SL-Signal:** Bei Setup-Ankündigungen gibt Jack selten konkreten SL — Bot muss eigenen setzen
- **Scope-Creep:** Lenkt von aktueller Phase (Review → Testcenter → Live) ab
- **Falsche Trigger:** Bedingung wird erfüllt, aber Jack steigt aus anderen Gründen nicht ein

## Abhängigkeiten

1. **Parser-Review fertig** — ohne saubere Klassifikation gibt's keine Watchlist-Extraktion
2. **Testcenter gebaut** — muss simulieren können: bei welchem % der Jack-Setups triggert die Bedingung? Mit welchem PnL?
3. **Intraday-Daten für alle Ticker** — Simulation nur möglich wenn 1-min-Bars vorhanden

## Backtest-Frage für Testcenter

**Simulation:** Für jedes historische Setup-Signal (letzte 6-12 Monate):
- Extrahiere Condition aus Text
- Prüfe Intraday-Daten: wurde Condition innerhalb Expiry erfüllt?
- Bei Erfüllung: simuliere Entry bei Support-Level, eigener SL 3% unter Zone, TP bei Target-Range-Mitte
- Messe: Win-Rate, avg PnL, Hit-Rate (wie oft trifft Jack's Prognose), False-Positives

Wenn **positiver EV nach Gebühren** → Feature implementieren. Wenn nicht → Idee verwerfen.

## Status

- **2026-04-14:** Idee niedergeschrieben aus LAES-Review-Block 2. Kein Code.
- Erinnerung setzen: nach Parser-Review abschließen → Testcenter-Simulation vor Implementierung.

## Verwandte Notizen

- [[Signal Bot Live-Roadmap]] — einzuordnen nach Phase 2
- [[Testcenter — Anforderungen & Architektur]] — Simulation als Test-Case
- [[Signal Bot]] — "Near-Miss & Watching-Simulation" im Ideen-Backlog (ähnliches Konzept, 2026-04-11)
