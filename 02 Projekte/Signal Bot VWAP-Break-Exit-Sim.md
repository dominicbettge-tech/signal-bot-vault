# Signal Bot — VWAP-Break-Down-Exit-Simulation

_Generiert: 2026-04-17T21:45:30.441658+00:00_

## P4 aus Indikator-Überlegung 2026-04-17

VWAP-Break-Down-Exit: wenn Position im Plus + Close unter Session-VWAP + Bearish-Bar → Force-Exit.

## Methodik
- Cumulative-VWAP vom Session-Start (04:00 ET) bis aktuelle Bar
- Trigger: Pos >= +1.0% UND Close < cum-VWAP UND Close < Open
- Hard-SL -6%, TTL 240min

## Ergebnisse

| Rank | Config | n | Mean | Winrate | Σ-PnL | Exit-Reasons |
|---|---|---|---|---|---|---|
| 1 | `vwap_tsl3` | 82 | -0.29% | 44% | -24.1% | tsl:53 · hard_sl:11 · ttl:10 · vwap_break:8 |
| 2 | `baseline_3pct` | 82 | -0.29% | 41% | -24.1% | tsl:61 · hard_sl:11 · ttl:10 |
| 3 | `vwap_only` | 82 | -2.23% | 33% | -183.2% | hard_sl:46 · vwap_break:19 · ttl:17 |

## Delta vs. baseline_3pct

| Config | Δ Mean | Δ Winrate | Δ Σ-PnL |
|---|---|---|---|
| `vwap_tsl3` | +0.000pp | +2.4% | +0.0pp |
| `vwap_only` | -1.941pp | -8.5% | -159.2pp |

## G5-Gate

| Config | consistency | oos_positive | time_70_30 train→test | walk-forward | ticker-disjoint |
|---|---|---|---|---|---|
| `vwap_tsl3` | ❌ | ❌ | +0.08%→-1.14% | -0.47% (1/4) | +0.09%→-1.23% |
| `baseline_3pct` | ❌ | ❌ | +0.13%→-1.26% | -0.53% (1/4) | +0.14%→-1.35% |

## Interpretation

- Best-Config: `vwap_tsl3` Mean -0.29%
- Delta vs. Baseline: +0.000pp
