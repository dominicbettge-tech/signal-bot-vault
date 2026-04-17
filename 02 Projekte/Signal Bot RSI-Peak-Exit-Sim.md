# Signal Bot — RSI-Peak-Exit-Simulation

_Generiert: 2026-04-17T21:37:39.789629+00:00_

## P2 aus Indikator-Überlegung 2026-04-17

RSI-Peak-Exit als Zusatzlayer: wenn Position im Plus + RSI>=70 + RSI-Decline → Force-Exit.

## Methodik
- RSI-14 auf 1min-Close, Warmup 30min pre-entry
- Trigger: Pos >= +1.0% UND RSI >= 70 UND RSI(t) < RSI(t-3)
- Hard-SL -6%, TTL 240min
- 3 Varianten: `rsi_only` / `rsi_tsl3` / `rsi_tsl5` vs. baseline_3pct

## Ergebnisse

| Rank | Config | n | Mean | Winrate | Σ-PnL | Exit-Reasons |
|---|---|---|---|---|---|---|
| 1 | `rsi_only` | 82 | +1.62% | 32% | +133.1% | hard_sl:47 · rsi_peak:20 · ttl:15 |
| 2 | `rsi_tsl3` | 82 | -0.25% | 43% | -20.6% | tsl:58 · hard_sl:11 · ttl:9 · rsi_peak:4 |
| 3 | `baseline_3pct` | 82 | -0.29% | 41% | -24.1% | tsl:61 · hard_sl:11 · ttl:10 |
| 4 | `rsi_tsl5` | 82 | -1.25% | 32% | -102.6% | tsl:42 · hard_sl:21 · ttl:14 · rsi_peak:5 |

## Delta vs. baseline_3pct

| Config | Δ Mean | Δ Winrate | Δ Σ-PnL |
|---|---|---|---|
| `rsi_only` | +1.917pp | -9.8% | +157.2pp |
| `rsi_tsl3` | +0.043pp | +1.2% | +3.5pp |
| `rsi_tsl5` | -0.957pp | -9.8% | -78.5pp |

## G5-Gate

| Config | consistency | oos_positive | time_70_30 train→test | walk-forward | ticker-disjoint |
|---|---|---|---|---|---|
| `rsi_only` | ❌ | ❌ | -0.63%→+6.77% | -1.57% (1/4) | -0.71%→+7.27% |
| `baseline_3pct` | ❌ | ❌ | +0.13%→-1.26% | -0.53% (1/4) | +0.14%→-1.35% |

**Legende:** consistency = strikt (sign-match + magnitude ≥50%). oos_positive = lockerer (test>0 UND walk-forward mean>0 UND ticker-disjoint test>0 — fängt OOS-Verbesserung ein).


## Interpretation

- **Best-Config:** `rsi_only` Mean +1.62%
- **Delta vs. Baseline:** +1.917pp
- RSI-Trigger-Häufigkeit:
  - `rsi_only`: 24% der Trades durch RSI-Peak beendet
  - `rsi_tsl3`: 5% der Trades durch RSI-Peak beendet
  - `rsi_tsl5`: 6% der Trades durch RSI-Peak beendet

## Vorbehalte
- RSI auf 1min extrem noisy; 5min wäre stabiler
- Entry-Moment zählt nicht für RSI (Jack postet oft nach Pre-Entry-Move → RSI schon hoch)
- Keine Cross-Validation gegen VWAP/MA-Trend

