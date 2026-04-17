# Signal Bot — RSI-5min-Exit-Simulation (H12c)

_Generiert: 2026-04-17T21:41:48.249899+00:00_

## Nachfolge zu P2 (1-min-RSI war OOS-Fail)

H12c aus `project_testcenter_r_hypotheses.md`: 1-min-RSI zeigte WF-Fail (1/4 pos folds). Hypothese: 5-min-Aggregation reduziert Noise.

## Methodik
- 1min-Bars zu 5min aggregiert (OHLC)
- RSI-14 auf 5min-Close, Warmup 120min pre-entry
- Trigger: Pos >= +1.0% UND RSI >= 70 UND RSI(t) < RSI(t-2) (10-min Lag)
- Hard-SL -6%, TTL 240min

## Ergebnisse

| Rank | Config | n | Mean | Winrate | Σ-PnL | Exit-Reasons |
|---|---|---|---|---|---|---|
| 1 | `rsi5_tsl3` | 82 | -0.20% | 44% | -16.4% | tsl:56 · hard_sl:11 · ttl:10 · rsi_peak_5m:5 |
| 2 | `baseline_3pct` | 82 | -0.29% | 41% | -24.1% | tsl:61 · hard_sl:11 · ttl:10 |
| 3 | `rsi5_only` | 82 | -2.11% | 29% | -173.4% | hard_sl:48 · ttl:22 · rsi_peak_5m:12 |

## Delta vs. baseline_3pct

| Config | Δ Mean | Δ Winrate | Δ Σ-PnL |
|---|---|---|---|
| `rsi5_tsl3` | +0.093pp | +2.4% | +7.6pp |
| `rsi5_only` | -1.821pp | -12.2% | -149.3pp |

## G5-Gate

| Config | consistency | oos_positive | time_70_30 train→test | walk-forward | ticker-disjoint |
|---|---|---|---|---|---|
| `rsi5_tsl3` | ❌ | ❌ | +0.16%→-1.02% | -0.23% (1/4) | +0.18%→-1.11% |
| `baseline_3pct` | ❌ | ❌ | +0.13%→-1.26% | -0.53% (1/4) | +0.14%→-1.35% |

## Interpretation

- Best-Config: `rsi5_tsl3` Mean -0.20%
- Delta vs. Baseline: +0.093pp
