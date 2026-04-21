---
title: Miss-Case-Study GV 2026-04-02
type: analysis
tags: [signal-bot, miss-analysis, case-study, staggered-entry]
created: 2026-04-21
status: draft
related: [[Loop-Orchestrator]], [[Signal-Bot-MOC]]
---

## TL;DR

Am 4/2/2026 postete Jack 4× denselben GV-Entry (0.42-0.45 Range). Der Bot hat **2 Trades versucht**:

- **Trade #4** (11:44 ET) — gefüllt, +2.39% in 72s → **Erfolg**
- **Trade #5** (11:54 ET) — Limit-Order platziert bei $0.435 midpoint, **nie gefüllt** → nach 12min expired

Die beiden anderen Signale wurden korrekt per Dedup-Block gefiltert.

**Der Miss:** Bot legt nur **eine** Limit-Order am Midpoint. Wenn der Markt nach Jack's Post nicht zum Midpoint zurückfindet, verpasst der Bot den Entry komplett, obwohl der Preis durchaus in der oberen Hälfte der Range handelte.

## Chain — alle GV-Messages 4/2 (UTC→ET)

| # | UTC | ET | Typ | Jack-Text (gekürzt) |
|---|---|---|---|---|
| #43 | 15:43:20 | 11:43:20 | entry | "GV got up another upper resistance! Edited the order to: 0.42~0.45. Valid for 12 minutes." |
| #50 | 15:44:36 | 11:44:36 | entry | gleich (Telegram-Edit repost) |
| #56 | 15:54:03 | 11:54:03 | entry | gleich |
| #61 | 16:00:05 | 12:00:05 | entry | gleich |

Jack re-postete alle 10 Minuten denselben Text — typische Telegram-Edit-Repost-Mechanik.

## Bot-Aktionen und Order-Life

| Trade | opened ET | Sig | Limit@ | Filled | Exit | Status | PnL |
|---|---|---|---:|---|---|---|---:|
| #4 | 11:44:39 | #43 | 0.435 | ✅ (72s) | 0.4454 (trailing-SL) | closed | +$23.91 |
| #5 | 11:54:04 | #56 | 0.435 | ❌ | — | expired 12:01 | $0.00 |

*(Signal #50 und #61 → Dedup-Block, korrekt)*

## Preis-Verlauf GV 4/2 (Polygon 1-min ET)

```
11:41  0.490  open
11:43  0.485  ← Jack Signal #43 ─┐
11:44  0.495  ← TRADE #4 gefüllt ├─ GV pumpt kurz auf 0.519
11:45  0.519  ← +1min Hoch       │
11:45  0.4454 ← TRADE #4 closed  │  ← exit hier (Trailing-SL)
11:49  0.464  ← −14min Tief      │
11:54  0.485  ← Jack Signal #56 ─┘
11:54  Limit@0.435 platziert (Trade #5)
11:55-12:06 Preis oszilliert 0.44-0.50, Low: 0.438 @ 11:45 nach Peak
12:06  0.455  ← Expiry-Fenster zu
12:07  0.447  ← local Low — kam NIE unter 0.438!
```

**Entscheidender Punkt:** Zwischen 11:54 (Order platziert) und 12:06 (Expiry) war das Preis-Minimum **0.447**. Die Limit-Order bei **0.435** hätte einen Drop von weiteren −2.7% gebraucht, der nie kam.

Hätte der Bot stattdessen bei **entry_high 0.45** gekauft, wäre die Order in dieser 12-Minuten-Phase **ständig fillbar** gewesen (Preis touchte 0.45 in 10 von 12 Minuten).

## Warum hat's nicht geklappt?

| Faktor | Baseline-Logik | Real-Verhalten |
|---|---|---|
| Entry-Preis-Wahl | Midpoint der Jack-Range (mean) | 0.435 — unterster Tick des Tages war 0.438 |
| Order-Tranchen | 1 Tranche für 100% Position | Alles auf eine Karte |
| Aggressivität | Konservativ (tiefer Limit hoffen auf Pullback) | Der Pullback kam nicht tief genug |
| Expiry | 12min (Jack-Vorgabe übernommen) | Zu knapp um auf Midpoint zu warten |

**Root-Cause:** Limit-Order-Strategie ist "warten bis Preis zum besten Mittel kommt". Wenn der Markt stattdessen in der oberen Range-Hälfte bleibt (was bei +Impuls häufig ist), kein Fill.

## Fix-Vorschlag (grounded-decisions, 5-Step)

**Features:** Jack-Range 0.42-0.45 (7% breit), Bot-Midpoint-Strategie, Trade #4 erfolgreich bei gleicher Logik (weil Markt kurz abdropte) — Trade #5 scheitert weil Markt 10min später in oberer Hälfte blieb. Expiry 12min knapp.

**Prior-Context:**
- Vault-Note [[02 Projekte/Signal Bot Staggered-Entry-Sim]] existiert — Infrastruktur für 3-Tranchen-Entries da
- `loop/models.py` whitelist: `STAGGERED_ENTRY_LEVELS`, `STAGGERED_ENTRY_OFFSETS`, `STAGGERED_ENTRY_SIZES`
- Memory `project_staggered_entry.md`: Jack selbst empfiehlt staggered entries
- `feedback_fill_vs_entry.md`: fill-Wahrscheinlichkeit ist ein erster-Klasse Konzept

**Precedents:**
- Trade #4 als positiver Referenzpunkt (gleiche Range, Midpoint-Fill erfolgreich → Strategie funktioniert BEI kurzem Dip)
- `project_aggressive_limit_oversold_pattern.md`: 21.5% No-Fill-Rate auf aggressiver Limit-Strategie → empirisch belegtes Fill-Problem

**3 Alternativen:**

| Variante | Mechanik | Pro | Contra |
|---|---|---|---|
| A Baseline | 1 Limit @ Midpoint (aktuell) | einfach, lowest slippage | hohe No-Fill-Rate bei seitlichen Märkten |
| **B Konservativ** | **3 Tranchen: 50% @ entry_high, 30% @ midpoint, 20% @ entry_low** | höchste Fill-Rate, partial-Fills schon gut | etwas höhere Avg-Entry |
| C Aggressiv | Market-Order @ entry_high mit Stop @ entry_low | garantierter Fill | max Slippage; Stop sofort aktiv |

**Goal-Alignment:**
- B bringt uns am nächsten zu "Bot trifft mehr Jack-Entries": erhöht Fill-Rate ohne Slippage explodieren zu lassen
- Und passt zu Jack's eigener Staggered-Philosophie
- Backtestbar gegen 272-Ticker-Corpus über STAGGERED_ENTRY-Knobs

**→ Empfehlung: B Konservativ.**

## Vorgeschlagene Knob-Werte

```python
STAGGERED_ENTRY_LEVELS = 3
STAGGERED_ENTRY_OFFSETS = [1.0, 0.5, 0.0]   # [entry_high, midpoint, entry_low] als Fraction of range
STAGGERED_ENTRY_SIZES = [0.5, 0.3, 0.2]     # 50% / 30% / 20% split
EXPIRY_MINUTES = 15                          # +3 min Puffer (ggü Jack's 12min Standard)
```

## Backtest-Plan

1. **Simulator:** `scripts/jack_staggered_entry_sim.py` existiert — gegen 272-Ticker Polygon-Corpus laufen lassen
2. **Vergleich Baseline vs B** → Train/Test-Split, Ship-Gate-Thresholds (Train≥5%, Test≥3%, Tickers↑≥3, Trim-Top-3 hält)
3. **Erfolgs-Definition:**
   - Fill-Rate steigt von ~65% (28/43 aktuell) auf ≥80%
   - Kein DD-Blowup (max-DD nicht mehr als +10% ggü Baseline)
   - Trim-Top-3 hält (Ship-Gate-Kriterium)

## Simulations-Ergebnis (2026-04-21, n=20 Range-Signale)

Sim-Skript: `scripts/sim_staggered_range_entry.py` — testet gegen alle Signale mit echtem entry_low/entry_high aus trades.db (29 total, 20 mit Polygon-Bar-Daten).

**Setup:** expiry=60min, hold=60min, Exit=Close des letzten Bars.

| Variante | Fill-Rate | Mean-Fill-Frac | Mean-PnL | Winrate |
|---|---:|---:|---:|---:|
| Baseline (mid only) | 20% | 0.20 | +1.51% | 25% |
| **CAND-B (50/30/20)** | **65%** | 0.42 | -1.51% | 23% |
| CAND-C (100 @ high) | 65% | 0.65 | -3.65% | 23% |

**Kernfinding:** Staggered-Entry verdreifacht Fill-Rate (20% → 65%), aber Mean-PnL wird schlechter weil wir am oberen Range-Ende einsteigen wenn kein Mean-Revert kommt.

**Wichtig einzuordnen:**
1. `entry_orders`-Tabelle ist **leer** (0 rows total) → aktueller Bot nutzt Staggered-Infra nicht; Sim testet Zukunfts-Verhalten.
2. Trade #4 GV 4/2: bars zeigen low=0.4835 bei 11:44 → strikter Buy-Limit @ 0.435 hätte NICHT gefüllt. Trotzdem öffnete Trade #4 mit +2.39% Exit. Deutet auf IBKR-spezifisches Fill-Verhalten hin (Market-Order? Negotiated Fill?), das die Sim nicht modelliert.
3. Exit-Modell ist naiv (60min-Hold). Mit echten TSL/TP-Ladders könnte CAND-B besser aussehen.
4. Per-Signal Detail: CAND-B/C verdoppeln Fill-Rate primär bei ADVB (07:30-07:44) und AGPU (11:39), wo Preis im oberen Drittel der Range bleibt.

## Empfehlung nach Sim

**NICHT unilateral shippen.** Fill-Rate-Gewinn ist klar (20% → 65%), aber ohne realistisches Exit-Modell kann Netto-Edge nicht bewertet werden.

**Nächster Schritt:** Sim-Erweiterung um H2-Ladder-Exit (+5/+10/+20 TP, SL -3%, TTL 4h). Dann Re-Run und Vergleich gegen Baseline. Wenn auch mit realistischem Exit CAND-B Net-Positiv → Shippen als Knob-Vorschlag via Loop-Orchestrator.

## Was noch offen ist

- Sim-Erweiterung mit H2-Ladder-Exit (s.o.)
- Die anderen Misses (GV 4/6, SPY 4/9) sind separate Case-Study
- Trade #4 hatte `fill_price=NULL` trotz +$23.91 Profit — Datenmodell-Inkonsistenz separat prüfen (TODO)
- `entry_orders` wurde nie live befüllt → Staggered-Entry ist Spec, nicht Code-Reality. Activation-Pfad muss geklärt werden.

---

## Entscheidung angefordert

User-OK nötig bevor:
1. Corpus-Simulation Variante B läuft (~5 min Wall-Time)
2. Bei OK der Simulation: Implementierung als PENDING-Proposal in Loop-Queue
3. Dort dann dein normaler `/loop approve` + `/loop apply`-Flow

Wenn OK signalisiert: Ich starte die Sim und pinge Ergebnis per Telegram.
