# Signal Bot — Hybrid-Exit-Simulation

_Generiert: 2026-04-17T20:48:15+00:00_

## Zweck

Empirische Validierung von 10 Hybrid-Exit-Varianten (H1-H10) gegen
die Static-Baseline B0=S2_HardTP_10 / B1=S5_Scaled_50_50, bevor wir
die R15-Action im Live-Bot konfigurieren.

## Setup

- **Trades:** 77 b-Verdicts mit Polygon-Coverage
- **Window:** 4h post-entry ODER 15:55 ET, whichever first
- **Slippage:** Tier-basiert (0.15-0.60% Spread + 0.2-1.5% SL-Halt-Boost)
- **Entry:** next-bar open, effective = open × (1 + Spread)
- **ATR:** rolling 14-Bar True-Range (h-l Proxy)
- **VWAP:** aus polygon-bars_1min.vwap Spalte (official VWAP)

## Ranking — Composite-Score (Mean × WinRate × (1-|MaxDD|/20))

| # | Strategie | Score | Mean % | Win % | Sharpe | MaxDD % | TotRet % | Final Eq |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | H2_Ladder_33_33_34 | +0.792 | +1.77 | 58.4 | +0.163 | -4.69 | +14.08 | 1.1408 |
| 2 | H1_Ladder_25_50_25 | +0.750 | +1.63 | 61.0 | +0.149 | -4.89 | +12.81 | 1.1281 |
| 3 | B0_HardTP_10 | +0.558 | +1.24 | 62.3 | +0.107 | -5.59 | +9.47 | 1.0947 |
| 4 | H12_Jack_TP_Preplace | +0.558 | +1.24 | 62.3 | +0.107 | -5.59 | +9.47 | 1.0947 |
| 5 | B1_Scaled_50_50 | +0.465 | +0.91 | 63.6 | +0.100 | -3.95 | +6.92 | 1.0692 |
| 6 | H5_Scaled_VWAPRunner | +0.392 | +0.97 | 59.7 | +0.082 | -6.51 | +7.20 | 1.0720 |
| 7 | H8_Scaled_BE_Stop | +0.190 | +0.35 | 71.4 | +0.041 | -4.86 | +2.45 | 1.0245 |
| 8 | H9_Super_Hybrid | +0.159 | +0.36 | 62.3 | +0.037 | -5.85 | +2.44 | 1.0244 |
| 9 | H4_Scaled_ATRTrail | +0.086 | +0.23 | 61.0 | +0.020 | -7.74 | +1.29 | 1.0129 |
| 10 | H6_Chandelier_25ATR | -0.004 | -2.41 | 15.6 | -0.239 | -19.79 | -17.26 | 0.8274 |
| 11 | H13_Regime_Switch_FastRamp | -0.027 | -2.70 | 22.1 | -0.482 | -19.09 | -18.90 | 0.8110 |
| 12 | H10_ATR_Adaptive_TP | -0.032 | -2.66 | 22.1 | -0.468 | -18.92 | -18.66 | 0.8134 |
| 13 | H7_TimeDecay_SL | -0.050 | -2.48 | 18.2 | -0.447 | -17.78 | -17.50 | 0.8250 |
| 14 | H3_TripleBarrier_10_4_120 | -0.088 | -2.20 | 20.8 | -0.430 | -16.16 | -15.65 | 0.8435 |
| 15 | H11_RSI_Adaptive_Stack | -0.116 | -2.26 | 26.0 | -0.581 | -16.07 | -16.07 | 0.8393 |

## Detail-Stats aller Strategien

| Strategie | n | Mean % | Std % | Win % | Avg Win | Avg Loss | Min % | Max % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| H2_Ladder_33_33_34 | 77 | +1.77 | 10.85 | 58.4 | +8.88 | -8.23 | -32.9 | +11.6 |
| H1_Ladder_25_50_25 | 77 | +1.63 | 10.88 | 61.0 | +8.36 | -8.92 | -32.9 | +11.1 |
| B0_HardTP_10 | 77 | +1.24 | 11.58 | 62.3 | +8.31 | -10.45 | -32.9 | +9.8 |
| H12_Jack_TP_Preplace | 77 | +1.24 | 11.58 | 62.3 | +8.31 | -10.45 | -32.9 | +9.8 |
| B1_Scaled_50_50 | 77 | +0.91 | 9.15 | 63.6 | +6.16 | -8.28 | -32.9 | +7.3 |
| H5_Scaled_VWAPRunner | 77 | +0.97 | 11.89 | 59.7 | +8.45 | -10.12 | -32.9 | +18.7 |
| H8_Scaled_BE_Stop | 77 | +0.35 | 8.59 | 71.4 | +3.96 | -8.67 | -32.9 | +9.8 |
| H9_Super_Hybrid | 77 | +0.36 | 9.85 | 62.3 | +6.15 | -9.22 | -32.9 | +13.7 |
| H4_Scaled_ATRTrail | 77 | +0.23 | 11.19 | 61.0 | +6.83 | -10.11 | -32.9 | +20.4 |
| H6_Chandelier_25ATR | 77 | -2.41 | 10.08 | 15.6 | +12.43 | -5.15 | -18.9 | +47.7 |
| H13_Regime_Switch_FastRamp | 77 | -2.70 | 5.60 | 22.1 | +6.58 | -5.33 | -7.1 | +10.1 |
| H10_ATR_Adaptive_TP | 77 | -2.66 | 5.69 | 22.1 | +6.76 | -5.33 | -7.1 | +10.0 |
| H7_TimeDecay_SL | 77 | -2.48 | 5.55 | 18.2 | +8.11 | -4.83 | -7.1 | +9.8 |
| H3_TripleBarrier_10_4_120 | 77 | -2.20 | 5.10 | 20.8 | +6.59 | -4.50 | -6.1 | +9.8 |
| H11_RSI_Adaptive_Stack | 77 | -2.26 | 3.90 | 26.0 | +2.76 | -4.03 | -7.1 | +8.8 |

## Verdict

**🏆 Sieger:** `H2_Ladder_33_33_34` — Score +0.792, Mean +1.77%, Win 58.4%, MaxDD -4.69%

- **Delta vs B0 (HardTP+10):** +0.53pp Mean, MaxDD -4.69% vs -5.59%
- **Delta vs B1 (Scaled 50/50):** +0.86pp Mean, MaxDD -4.69% vs -3.95%

## Integration-Empfehlung

- **H2_Ladder_33_33_34 als neue R15-Action** → Integration in `position_monitor.py`:
  - Siehe Spezifikation unten

## Caveats

- Sample n=77 — Walk-Forward-Validation auf zukünftige Smoke-Daten essentiell vor Live
- VWAP-Exits (H5) sind model-optimistisch, weil echte Live-Exits mind. 1min Latenz hätten
- Chandelier-ATR (H6/H9) basiert auf h-l Range, nicht echtem True-Range (keine Gaps)
- Time-Decay (H7) und Triple-Barrier (H3) hängen stark von Window-Länge ab — 4h-Cap könnte
  positiv oder negativ biasen je nach Ticker-Typ
- Limit-TP-Annahme: Bot setzt Limit zum Entry-Zeitpunkt (sonst Hi-Touch=Limit-Fill-Problem)
