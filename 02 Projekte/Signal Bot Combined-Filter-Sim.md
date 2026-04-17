# Signal Bot — Combined-Filter-Sim

_Generiert: 2026-04-17T21:13:22.075332+00:00_

## Setup
- **Korpus:** 83 b-Verdicts (ex SLS)
- **Size:** 20% pro Trade (Config-Default)
- **SL:** -3% fix, **TTL:** 240min, Entry next-bar-open

## Szenarien

| # | Name | Ladder | Skip-PM | Skip-AH |
|---|---|---|---|---|
| — | `S0_Baseline` | `H2_base` | — | — |
| — | `S1_SkipPM` | `H2_base` | ✓ | — |
| — | `S2_SkipPM+AH` | `H2_base` | ✓ | ✓ |
| — | `S3_S2+User_Ladder` | `user_3_7_15` | ✓ | ✓ |

## Ergebnisse

| Scenario | N | Skipped | Mean-PnL | Winrate | SL-Rate | TP-Full | Σ-PnL | Bankroll Δ/Trade @20% |
|---|---|---|---|---|---|---|---|---|
| `S0_Baseline` | 83 | 0 | -0.37% | 22% | 69% | 8% | -30.4% | -0.073% |
| `S1_SkipPM` | 61 | 22 | -0.03% | 25% | 62% | 10% | -1.7% | -0.006% |
| `S2_SkipPM+AH` | 56 | 27 | +0.13% | 25% | 62% | 11% | +7.0% | +0.025% |
| `S3_S2+User_Ladder` | 56 | 27 | +0.22% | 32% | 59% | 16% | +12.4% | +0.044% |

## Delta vs. Baseline

| Scenario | Δ Mean-PnL | Δ Winrate | Δ Σ-PnL | Extrapolation: bei 200 Trades/Jahr, 20% Size, 10k Bankroll |
|---|---|---|---|---|
| `S0_Baseline` | +0.000pp | +0.0% | +0.0pp | ~200 trades → -0.15% bankroll/yr ≈ $-1,466 |
| `S1_SkipPM` | +0.338pp | +2.9% | +28.7pp | ~147 trades → -0.01% bankroll/yr ≈ $-82 |
| `S2_SkipPM+AH` | +0.492pp | +3.3% | +37.4pp | ~135 trades → +0.03% bankroll/yr ≈ $+339 |
| `S3_S2+User_Ladder` | +0.587pp | +10.5% | +42.8pp | ~135 trades → +0.06% bankroll/yr ≈ $+596 |

## Interpretation

- **Baseline (H2, kein Filter):** Mean -0.37%, Sum -30.4pp — weder profitabel noch katastrophal, aber -0.4% Mean zeigt klar fehlenden Edge
- **S1 Skip-PM alleine:** Entfernt 22 schlechteste Trades (Premarket) → Mean und Winrate sollten stark springen
- **S2 +Skip-AH:** Entfernt zusätzliche 5 schwache Trades
- **S3 +User-Ladder:** Kombiniert mit engerer TP-Ladder (+3/+7/+15) — engere TPs werden öfter voll gefüllt

## Generalisierungs-Vorbehalt (REGEL 4)
- In-Sample n=83, einzelne Buckets kleiner
- Kein Walk-Forward-Split
- Cross-Ticker unklar (Biotech-Bias)
- Default-Change nur nach G5-Gate

## Priorisierung für Phase-C-Sweep
1. **H10a (Skip-Premarket)** — stärkster Einzel-Hebel, braucht Walk-Forward-Validation + OOS-Test
2. **user_3_7_15 Ladder** — +0.25pp Corpus-Aggregat, wenig Downside-Risk, leicht zu testen
3. **Skip-AH (H7a)** — mager unterstützt (n=5), würde bei mehr Daten gewinnen

## Verbindungen memory
- `project_testcenter_r_hypotheses.md` H10, H11
- `Signal Bot Time-of-Day.md` — Quelle
- `Signal Bot Premarket Deep-Dive.md` — 22 Cases
- `Signal Bot TP-Ladder-Variations.md` — Ladder-Ranking
