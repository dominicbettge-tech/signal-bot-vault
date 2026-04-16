# Signal Bot — Jack Exit-Strategy-Matrix

_Generiert: 2026-04-16T09:31:14+00:00_

- **Trades:** 77 (alle b-Verdicts mit Polygon-Coverage)
- **Zeitraum:** 2025-10-10 → 2026-03-27
- **Window:** 4h post-entry ODER EOD (15:55 ET), whichever first
- **Slippage:** 1min-Latenz (entry = next-bar open) — kein Spread-Modell

## Strategie-Ranking (sortiert nach Mean per-trade)

| Strategie | Mean % | Win % | Sharpe-like | Std % | Avg Win % | Avg Loss % | Min % | Max % | Eq Final | Total Ret % | Max-DD % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S2_HardTP_10 | +2.04 | 68.8 | +0.179 | 11.38 | +8.12 | -11.39 | -31.9 | +10.0 | 1.1638 | +16.38 | -5.25 |
| S5_Scaled_TP_50_50 | +1.68 | 71.4 | +0.189 | 8.88 | +6.03 | -9.18 | -31.9 | +7.5 | 1.1347 | +13.47 | -3.19 |
| S1_HardTP_5 | +1.33 | 77.9 | +0.171 | 7.77 | +4.40 | -9.53 | -31.9 | +5.0 | 1.1051 | +10.51 | -3.19 |
| S6_QuickLock_Trail3 | +0.02 | 39.0 | +0.008 | 3.02 | +3.24 | -2.03 | -3.0 | +7.3 | 1.0014 | +0.14 | -2.10 |
| S8_TrailOnly_3 | -0.02 | 39.0 | -0.006 | 3.13 | +3.13 | -2.03 | -3.0 | +9.7 | 0.9981 | -0.19 | -1.97 |
| S9_TrailOnly_5 | -0.87 | 35.1 | -0.214 | 4.09 | +3.04 | -2.99 | -5.0 | +19.5 | 0.9343 | -6.57 | -6.61 |
| S4_TP10_SL3 | -1.00 | 20.8 | -0.246 | 4.09 | +5.81 | -2.79 | -3.0 | +10.0 | 0.9249 | -7.51 | -8.66 |
| S3_TP10_SL5 | -1.25 | 29.9 | -0.222 | 5.62 | +6.27 | -4.45 | -5.0 | +10.0 | 0.9073 | -9.27 | -10.58 |
| S0_NaiveHold_EOD | -2.57 | 40.3 | -0.113 | 22.79 | +13.84 | -13.64 | -75.4 | +115.9 | 0.8042 | -19.58 | -28.71 |
| S7_ScaledJack_TSL_R15v3 | -2.66 | 29.9 | -0.237 | 11.23 | +10.08 | -8.08 | -10.0 | +49.7 | 0.8108 | -18.92 | -20.13 |

## Verdict

- **Beste Strategie:** `S2_HardTP_10` mit Mean +2.04%/trade, Sharpe-like +0.179, MaxDD -5.25%
- **Naive-Baseline (S0):** Mean -2.57%/trade — Differenz: **+4.61pp**
- **Schlechteste:** `S7_ScaledJack_TSL_R15v3` mit Mean -2.66%/trade

**Gesamt-Verdict:** 🟢 GO — Mindestens eine Strategie zeigt belastbares Edge.

## Caveats

- Limit-TPs gehen davon aus dass Bot LIMIT-Order setzt vor Entry — bei Penny-Stock-Spreads bekommt man oft schlechtere Fills
- Trail/Stop davon aus dass Bot innerhalb 1min auf Bar-Low reagieren kann — IBKR-Rundtrip ist real
- Keine Slippage auf SL-Hits modelliert — bei Halt/Gap-Down -3% SL kann real -10%+ sein
- 77 Trades = noch immer kleine Sample fuer Strategy-Selection — Walk-Forward nach P1 Slippage
- Scaled-Jack-TSL hat empirische Trail-Activation NACH 1. TP (sonst -15% Trail >= -10% SL)