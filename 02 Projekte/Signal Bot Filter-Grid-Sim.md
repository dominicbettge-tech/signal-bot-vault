# Signal Bot — Filter-Grid-Sim (Stage-3)

_Generiert: 2026-04-16T17:12:18+00:00_

## Setup
- **Trades cached:** 77
- **Slippage:** ja (Tier-basiert)
- **Subgroup-Counts:** {'swing': 19, 'day': 21, 'unspecified': 37}; ET-Hours: {5: 2, 6: 3, 7: 2, 8: 10, 9: 14, 10: 19, 11: 10, 12: 8, 13: 1, 14: 3, 15: 5}

## Basis-Strategien
- **B1_HardTP_10:** TP=10% / SL=0% / TrailAct=0% / TrailDist=3% / Split=single
- **B2_HardTP_25:** TP=25% / SL=0% / TrailAct=0% / TrailDist=3% / Split=single
- **B3_Scaled_50_50_TP10:** TP=10% / SL=0% / TrailAct=0% / TrailDist=3% / Split=50_50
- **B4_TP20_SL7:** TP=20% / SL=7% / TrailAct=0% / TrailDist=3% / Split=single
- **B5_TrailAfter10:** TP=999% / SL=0% / TrailAct=10% / TrailDist=5% / Split=single

## Beste Filter-Kombi je Basis-Strategie

| Strategie | Best Filter (tt / hour) | N | Mean % | Win % | Sharpe | TotRet % | MaxDD % | Δ Mean vs. no-filter |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| B1_HardTP_10 | only_day / lunch_window_12_13 | 2 | +9.50 | 100.0 | +67.175 | +1.91 | +0.00 | +8.26 |
| B2_HardTP_25 | only_day / lunch_window_12_13 | 2 | +24.50 | 100.0 | +173.241 | +4.96 | +0.00 | +19.88 |
| B3_Scaled_50_50_TP10 | only_day / lunch_window_12_13 | 2 | +7.00 | 100.0 | +49.497 | +1.40 | +0.00 | +6.09 |
| B4_TP20_SL7 | only_day / lunch_window_12_13 | 2 | +5.50 | 50.0 | +0.280 | +1.08 | -0.84 | +7.73 |
| B5_TrailAfter10 | only_day / lunch_window_12_13 | 2 | +7.00 | 100.0 | +1.203 | +1.40 | +0.00 | +7.28 |

## Baseline (no filter) je Strategie

| Strategie | N | Mean % | Win % | Sharpe | TotRet % | MaxDD % |
|---|---:|---:|---:|---:|---:|---:|
| B1_HardTP_10 | 77 | +1.24 | 62.3 | +0.107 | +9.47 | -5.59 |
| B2_HardTP_25 | 77 | +4.62 | 51.9 | +0.260 | +40.93 | -8.23 |
| B3_Scaled_50_50_TP10 | 77 | +0.91 | 63.6 | +0.100 | +6.92 | -3.95 |
| B4_TP20_SL7 | 77 | -2.23 | 26.0 | -0.237 | -16.09 | -17.02 |
| B5_TrailAfter10 | 77 | -0.28 | 54.5 | -0.023 | -2.69 | -7.63 |

## R16 Isolation (skip_swing, all hours)

| Strategie | N | Mean % | Win % | Δ Mean | Δ TotRet | Δ MaxDD |
|---|---:|---:|---:|---:|---:|---:|
| B1_HardTP_10 | 58 | +2.42 | 72.4 | +1.17 | +5.04 | +0.10 |
| B2_HardTP_25 | 58 | +6.63 | 58.6 | +2.00 | +4.17 | +0.00 |
| B3_Scaled_50_50_TP10 | 58 | +1.82 | 72.4 | +0.91 | +3.92 | -0.68 |
| B4_TP20_SL7 | 58 | -2.63 | 24.1 | -0.40 | +1.68 | +1.33 |
| B5_TrailAfter10 | 58 | +0.30 | 62.1 | +0.58 | +3.92 | +2.17 |

## R17 Isolation (all types, skip_after_15)

| Strategie | N | Mean % | Win % | Δ Mean | Δ TotRet | Δ MaxDD |
|---|---:|---:|---:|---:|---:|---:|
| B1_HardTP_10 | 72 | +1.61 | 65.3 | +0.37 | +2.27 | +0.00 |
| B2_HardTP_25 | 72 | +5.23 | 54.2 | +0.60 | +2.92 | -0.00 |
| B3_Scaled_50_50_TP10 | 72 | +1.26 | 66.7 | +0.35 | +2.22 | -0.00 |
| B4_TP20_SL7 | 72 | -2.20 | 26.4 | +0.03 | +1.12 | +1.14 |
| B5_TrailAfter10 | 72 | -0.02 | 56.9 | +0.26 | +2.02 | +0.00 |

## R16+R17 kombiniert (skip_swing + skip_after_15)

| Strategie | N | Mean % | Win % | Δ Mean | Δ TotRet | Δ MaxDD |
|---|---:|---:|---:|---:|---:|---:|
| B1_HardTP_10 | 56 | +2.81 | 75.0 | +1.57 | +7.02 | +0.10 |
| B2_HardTP_25 | 56 | +7.17 | 60.7 | +2.54 | +6.68 | -0.00 |
| B3_Scaled_50_50_TP10 | 56 | +2.19 | 75.0 | +1.28 | +5.84 | -0.68 |
| B4_TP20_SL7 | 56 | -2.55 | 25.0 | -0.32 | +2.53 | +1.44 |
| B5_TrailAfter10 | 56 | +0.61 | 64.3 | +0.89 | +5.67 | +2.17 |

## Interpretation

- **Δ Mean positiv** = Filter entfernt mehr Loser als Winner → R-Regel promoten zu Candidate+
- **Δ Mean ≈ 0 oder negativ** = Filter entfernt gute Trades mit → Hypothesis widerlegt
- **N sinkt** = weniger Trade-Gelegenheiten (Trade-Off gegen Auslastung)

## Caveats

- Subgruppen klein (Swing n=~19, After-15 n=~12) → Statistik instabil
- ET-Hour naiv computed (UTC-4, keine DST-Korrektur)
- Fairness: jede Zelle nutzt n = filter-passed Trades (nicht identisch mit Baseline-N)
