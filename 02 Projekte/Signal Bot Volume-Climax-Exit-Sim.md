# Signal Bot — Volume-Climax-Exit-Simulation

_Generiert: 2026-04-17T21:40:02.889196+00:00_

## P3 aus Indikator-Überlegung 2026-04-17

Volume-Climax-Exit als Zusatzlayer: wenn Position im Plus + Volume >= K x 20-bar-mean + Bearish-Close → Force-Exit.

## Methodik
- Rolling 20-bar Volume-Mean auf 1min-Bars, Warmup 30min
- Trigger: Pos >= +1.0% UND Volume >= K × MA UND Close < Open
- Hard-SL -6%, TTL 240min
- 4 Varianten: `vc_k3_only` / `vc_k5_only` / `vc_k3_tsl3` vs. baseline_3pct

## Ergebnisse

| Rank | Config | n | Mean | Winrate | Σ-PnL | Exit-Reasons |
|---|---|---|---|---|---|---|
| 1 | `baseline_3pct` | 82 | -0.29% | 41% | -24.1% | tsl:61 · hard_sl:11 · ttl:10 |
| 2 | `vc_k3_tsl3` | 82 | -0.34% | 41% | -27.6% | tsl:61 · hard_sl:11 · ttl:9 · vol_climax:1 |
| 3 | `vc_k3_only` | 82 | -1.88% | 24% | -154.5% | hard_sl:52 · ttl:17 · vol_climax:13 |
| 4 | `vc_k5_only` | 82 | -2.74% | 23% | -224.3% | hard_sl:53 · ttl:20 · vol_climax:9 |

## Delta vs. baseline_3pct

| Config | Δ Mean | Δ Winrate | Δ Σ-PnL |
|---|---|---|---|
| `vc_k3_tsl3` | -0.043pp | +0.0% | -3.6pp |
| `vc_k3_only` | -1.591pp | -17.1% | -130.5pp |
| `vc_k5_only` | -2.442pp | -18.3% | -200.3pp |

## G5-Gate

| Config | consistency | oos_positive | time_70_30 train→test | walk-forward | ticker-disjoint |
|---|---|---|---|---|---|
| `baseline_3pct` | ❌ | ❌ | +0.13%→-1.26% | -0.53% (1/4) | +0.14%→-1.35% |
| `baseline_3pct` | ❌ | ❌ | +0.13%→-1.26% | -0.53% (1/4) | +0.14%→-1.35% |

## Interpretation

- **Best-Config:** `baseline_3pct` Mean -0.29%
- **Delta vs. Baseline:** +0.000pp

- Volume-Climax-Trigger-Häufigkeit:
  - `vc_k3_only`: 16% der Trades durch Vol-Climax beendet
  - `vc_k5_only`: 11% der Trades durch Vol-Climax beendet
  - `vc_k3_tsl3`: 1% der Trades durch Vol-Climax beendet

## Vorbehalte
- Volume-Spike-Definition hängt stark von K ab (noise bei Low-Volume-Bars)
- Pre-Market hat abweichende Volume-Baseline (RTH-MA unpassend)
- Keine Cross-Validation gegen RSI/ATR-Stack
