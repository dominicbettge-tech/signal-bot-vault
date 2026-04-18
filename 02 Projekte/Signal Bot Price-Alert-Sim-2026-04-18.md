# Price-Alert-as-Entry Sim — 2026-04-18

**Kontext:** Task #43. Corpus n=73 Alert-Messages. Hypothese: Jack's "price alert" als Pre-Entry-Trigger nutzen, vor expliziter Order.

## Setup

- **Korpus:** 73 Alert-Messages (`LOWER(text) LIKE '%price alert%' OR text LIKE '%🔔%'` + ticker)
- **Exit:** TSL 3% + Hard-SL -5% + TTL 240min (Sieger Task #42 TSL-Grid)
- **Fill-Logic:** Buy-Limit (fill wenn `low ≤ limit_price`)
- **Bug-Fix:** Exit-Bars starten bei `first_fill_ts`, nicht bei `msg_ts` (verhindert Lookahead)

## Strategien

| Strategy | Logic |
|---|---|
| A — Eager | Single Limit @ alert_price |
| B — Dip | Single Limit @ alert_price × 0.95 (-5%) |
| C — Laddered | 3 Tranchen @ [0%, -3%, -5%] × alert_price |

## Ergebnisse

### 2h Fill-Window

| Strategy | N | Fill-Rate | Mean PnL | Median | Winrate | SL-Hits |
|---|---|---|---|---|---|---|
| A Eager | 69 | 31.9% | -3.20% | -5.00% | 18% | 15 |
| B Dip | 69 | 26.1% | -3.85% | -5.00% | 11% | 14 |
| **C Laddered** | 69 | 31.9% | **-2.73%** | -5.00% | 23% | 15 |

### 24h Fill-Window

| Strategy | N | Fill-Rate | Mean PnL | Median | Winrate | SL-Hits |
|---|---|---|---|---|---|---|
| A Eager | 70 | 47.1% | -1.71% | -2.46% | 33% | 15 |
| B Dip | 70 | 40.0% | -2.28% | -4.00% | 29% | 14 |
| **C Laddered** | 70 | 47.1% | **-0.79%** | -0.02% | **48%** | 15 |

## Decision-Gate Check

Projekt-Gate: "Strategie B oder C >+20% Avg-P&L vs Baseline bei Hit-Rate ≥40% → Integration"

**Strategy C @24h:**
- Hit-Rate 48% ✓ (> 40%)
- Mean PnL -0.79% ✗ (< Baseline 0%, Gate erwartet +20%)

**Entscheidung: FAIL Gate.** Aktuelle Bot-Verhalten (Alerts ignorieren) bleibt richtig.

## Subthreshold-Findings

1. **C Laddered konsistent beste Strategie** über beide Fill-Windows (höchste Winrate, mildeste Mean-PnL)
2. **24h-Fill-Window signifikant besser als 2h** — Alerts sind *Pre-Trigger*, Konversion Braucht Zeit (deckt sich mit Corpus-Observation 28%±12h)
3. **TSL 3% + Hard-SL -5% zu eng für Alert-Volatilität** — 15 SL-Hits bei Strategy C (21% der 70 alerts). Penny-Stock-Alerts haben oft wide spreads.

## Next Steps (Subthreshold-Exploration)

Falls User später reaktiviert:
- **TSL 5-8% Test** (Penny-Stock-Volatilität)
- **Position-Size-Cap** (halber Alpha-Allocation pro Alert)
- **Alert-Filter** nach Sentiment/Ticker-Type (Biotech vs Non-Biotech)
- **Strategy D — Priority-Watch:** bei nachfolgender Jack-Order Position-Size ×1.5

## Files

- Sim-Script: `/tmp/price_alert_sim.py`
- Results: stdout-Output oben

## Status

**Task #43: DONE (Decision: No-Integration).** Current Bot-Verhalten bleibt (Alert = reine Watch-Signal, keine Auto-Order).
