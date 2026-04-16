# Signal Bot — Jack Exit-Strategy-Matrix mit Slippage

_Generiert: 2026-04-16T09:43:44+00:00_

## Setup

- **Trades:** 77
- **Slippage-Modell:** Tier-basiert (Bid-Ask-Spread per Side + SL-Halt-Boost)

| Tier (avg-close) | Spread/Side | SL-Halt-Boost |
|---|---:|---:|
| <$2 | 0.60% | +1.5% |
| $2-5 | 0.40% | +1.0% |
| $5-10 | 0.30% | +0.5% |
| $10-20 | 0.20% | +0.3% |
| >$20 | 0.15% | +0.2% |

Round-trip-Cost = 2×Spread + ggf. SL-Boost. Auf Penny-Stocks (<$5): typisch -0.8 bis -1.2pp pro Trade.

## Strategie-Ranking mit Slippage (sortiert nach Mean per-trade)

| Strategie | Mean % | Win % | Sharpe-like | Std % | Avg Win % | Avg Loss % | Min % | Max % | Eq Final | Total Ret % | Max-DD % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| S2_HardTP_10 | +1.24 | 62.3 | +0.107 | 11.58 | +8.31 | -10.45 | -32.9 | +9.8 | 1.0947 | +9.47 | -5.59 |
| S5_Scaled_TP_50_50 | +0.91 | 63.6 | +0.100 | 9.15 | +6.16 | -8.28 | -32.9 | +7.3 | 1.0692 | +6.92 | -3.95 |
| S1_HardTP_5 | +0.58 | 71.4 | +0.072 | 8.06 | +4.28 | -8.67 | -32.9 | +4.8 | 1.0430 | +4.30 | -4.19 |
| S8_TrailOnly_3 | -1.57 | 26.0 | -0.515 | 3.05 | +2.58 | -3.03 | -5.1 | +7.0 | 0.8857 | -11.43 | -11.65 |
| S6_QuickLock_Trail3 | -1.57 | 27.3 | -0.537 | 2.93 | +2.43 | -3.08 | -5.1 | +5.8 | 0.8854 | -11.46 | -11.57 |
| S4_TP10_SL3 | -2.26 | 15.6 | -0.539 | 4.19 | +6.33 | -3.85 | -5.1 | +9.8 | 0.8394 | -16.06 | -16.54 |
| S9_TrailOnly_5 | -2.32 | 23.4 | -0.566 | 4.10 | +3.13 | -3.99 | -7.1 | +16.7 | 0.8356 | -16.44 | -16.44 |
| S3_TP10_SL5 | -2.66 | 22.1 | -0.469 | 5.68 | +6.75 | -5.33 | -7.1 | +9.8 | 0.8133 | -18.67 | -18.94 |
| S0_NaiveHold_EOD | -3.34 | 33.8 | -0.147 | 22.68 | +15.71 | -13.06 | -75.6 | +114.0 | 0.7580 | -24.20 | -31.22 |
| S7_ScaledJack_TSL_R15v3 | -3.76 | 24.7 | -0.329 | 11.43 | +11.33 | -8.71 | -12.1 | +49.1 | 0.7443 | -25.57 | -25.57 |

## Verdict (mit Slippage-Realität)

- **Beste Strategie:** `S2_HardTP_10` mit Mean +1.24%/trade, Sharpe-like +0.107, MaxDD -5.59%
- **Naive-Baseline:** -3.34% — Delta: **+4.59pp**

**Gesamt-Verdict:** 🟢 GO — Bot bleibt profitabel auch unter realistischer Slippage.

## Caveats

- Slippage-Tiers sind heuristisch (kein NBBO im Polygon-DB) — 2026 könnten reale Spreads enger sein dank Tick-Reform
- Hi-Lo-Range im Korpus ist ~0.4% intra-bar (proxy für Spread untere Schranke)
- SL-Halt-Boost basiert auf Biotech-Crash-Beobachtung; non-Biotech-Tickers haben weniger Halt-Risk
- Limit-Order-Non-Fill-Risk (HIGH touched limit aber nicht filled) NICHT modelliert — würde HardTP weiter abwerten
- Reale IBKR-Smart-Routing kann besser sein als Tier-Spread (typically gets mid+spread/4)
