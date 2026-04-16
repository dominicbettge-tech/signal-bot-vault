# Signal Bot — Jack-Edge-Audit

_Generiert: 2026-04-16T09:25:21+00:00_

## Setup

- **Quelle:** alle `human_verdict='b'` aus backtest_results.db
- **Zeitraum:** 2025-10-10 → 2026-03-27
- **Total Buy-Verdicts mit Ticker:** 83
- **Simulierbare Trades (Polygon-Coverage):** 83
- **Slippage-Modell:** 1min-Latenz (entry = open des nächsten Bars nach msg)
- **Position-Sizing für Equity-Curve:** 10% Bankroll, sequenziell, log-additiv

## Per-Trade-Statistik (Signal-Qualität)

| Window | n | Mean % | Win % | Avg Win % | Avg Loss % | Expectancy % | Sharpe-like | Min % | Max % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 30m | 77 | +1.00 | 44.2 | +11.12 | -7.01 | +1.00 | +0.048 | -19.6 | +156.4 |
| 60m | 77 | -1.54 | 39.0 | +8.45 | -7.91 | -1.54 | -0.128 | -36.1 | +42.8 |
| 120m | 77 | -2.03 | 37.7 | +11.29 | -10.08 | -2.03 | -0.128 | -34.4 | +77.4 |
| 240m | 77 | -2.57 | 40.3 | +13.84 | -13.64 | -2.57 | -0.113 | -75.4 | +115.9 |
| EOD | 77 | -0.10 | 39.0 | +22.46 | -14.50 | -0.10 | -0.003 | -79.4 | +174.4 |

## Equity-Curve (10% Position-Size, sequenziell)

| Window | n | Final Eq | Total Return % | Max-DD % |
|---|---:|---:|---:|---:|
| 30m | 77 | 1.0637 | +6.37 | -12.87 |
| 60m | 77 | 0.8834 | -11.66 | -13.24 |
| 120m | 77 | 0.8471 | -15.29 | -19.68 |
| 240m | 77 | 0.8042 | -19.58 | -28.71 |
| EOD | 77 | 0.9579 | -4.21 | -28.12 |

## Upper-Bound-Diagnostik (4h Intra-Window)

Ceiling: was perfektes Exit-Timing maximal einbringen würde.
Floor: maximal beobachteter Drawdown wenn nicht exited.

- **Avg max_high_4h:** +21.76% (Median trade hatte max +12.35%)
- **Avg min_low_4h:** -16.75% (Median trade hatte min -13.09%)
- **% Trades mit max_high_4h ≥ 5%:** 66.2%
- **% Trades mit max_high_4h ≥ 10%:** 53.2%
- **% Trades mit min_low_4h ≤ -5%:** 71.4%
- **% Trades mit min_low_4h ≤ -10%:** 57.1%

## GO/NO-GO Verdict

**Heuristik (per-trade Mean & Sharpe-like):**
- Mean ≥ +1% UND Sharpe-like ≥ 0.15 → 🟢 GO (Signal hat Edge)
- Mean ≥ 0 UND Win-Rate ≥ 50% → 🟡 MAYBE (Edge vorhanden aber dünn)
- Sonst → 🔴 NO-GO (Bot kann das nicht retten)

| Window | Mean % | Sharpe-like | Win % | Verdict |
|---|---:|---:|---:|---|
| 30m | +1.00 | +0.048 | 44.2 | 🔴 NO-GO |
| 60m | -1.54 | -0.128 | 39.0 | 🔴 NO-GO |
| 120m | -2.03 | -0.128 | 37.7 | 🔴 NO-GO |
| 240m | -2.57 | -0.113 | 40.3 | 🔴 NO-GO |
| EOD | -0.10 | -0.003 | 39.0 | 🔴 NO-GO |

## Caveats

- **Slippage:** nur 1min-Latenz, kein Spread-Modell (Penny-Stocks haben echte Spreads). Echte Zahlen sind 1-3% schlechter pro Trade.
- **Survivorship:** nur Messages die Jack POSTET (nicht: failed setups die er nicht erwähnt).
- **Sample-Size:** ~83 Trades sind zu wenig für robuste Sharpe-Schätzung. Stand-Alone-Indikator, nicht Final-Antwort.
- **Reviewer-Bias:** b-Verdicts wurden manuell vergeben — möglicherweise Cherry-Picking der klaren Buy-Setups.
- **No Concurrency:** Equity-Curve sequenziell — Real-Bot hätte 5 parallele Slots, Trades überlappen.