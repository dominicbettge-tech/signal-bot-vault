# Signal Bot — Walk-Forward Validierung

_Generiert: 2026-04-16T09:54:14+00:00_

## Setup

- **Split:** 70% / 30%  (split-date: `2025-12-04`)
- **Train n:** 53  **Test n:** 24
- **Grid:** COARSE (1200 combos)
- **Slippage:** ja
- **Top-K Train re-validiert auf Test:** 20

## Ergebnisse (sortiert nach Test-Mean — true out-of-sample)

| Rang | Params | Train Mean | Test Mean | Δ Train→Test | Train Sharpe | Test Sharpe | Test Win % | Test DD % |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | TP=25 SL=0 TrA=0 TrD=3 Split=single | +5.72 | +2.19 | -3.53 | +0.326 | +0.119 | 45.8 | -7.12 |
| 2 | TP=20 SL=0 TrA=0 TrD=3 Split=single | +4.12 | +1.94 | -2.18 | +0.264 | +0.115 | 50.0 | -7.12 |
| 3 | TP=25 SL=0 TrA=0 TrD=3 Split=50_50 | +4.14 | +1.93 | -2.21 | +0.292 | +0.128 | 54.2 | -4.55 |
| 4 | TP=15 SL=0 TrA=0 TrD=3 Split=single | +3.23 | +1.76 | -1.46 | +0.245 | +0.121 | 54.2 | -4.06 |
| 5 | TP=25 SL=0 TrA=0 TrD=3 Split=33_33_34 | +3.41 | +1.42 | -1.99 | +0.256 | +0.099 | 54.2 | -4.62 |
| 6 | TP=12 SL=0 TrA=0 TrD=3 Split=single | +2.55 | +1.42 | -1.13 | +0.215 | +0.105 | 58.3 | -3.52 |
| 7 | TP=20 SL=0 TrA=0 TrD=3 Split=50_50 | +2.82 | +1.28 | -1.55 | +0.221 | +0.090 | 50.0 | -4.92 |
| 8 | TP=25 SL=0 TrA=15 TrD=8 Split=single | +3.71 | +0.99 | -2.72 | +0.249 | +0.063 | 45.8 | -4.80 |
| 9 | TP=20 SL=0 TrA=0 TrD=3 Split=33_33_34 | +2.51 | +0.92 | -1.59 | +0.209 | +0.068 | 54.2 | -4.50 |
| 10 | TP=25 SL=0 TrA=15 TrD=5 Split=single | +3.06 | +0.84 | -2.22 | +0.215 | +0.056 | 54.2 | -4.48 |
| 11 | TP=25 SL=0 TrA=15 TrD=8 Split=50_50 | +3.02 | +0.70 | -2.32 | +0.233 | +0.050 | 50.0 | -3.54 |
| 12 | TP=20 SL=0 TrA=15 TrD=8 Split=single | +3.10 | +0.58 | -2.52 | +0.224 | +0.039 | 45.8 | -4.80 |
| 13 | TP=30 SL=0 TrA=15 TrD=8 Split=50_50 | +2.67 | +0.55 | -2.12 | +0.204 | +0.037 | 45.8 | -4.80 |
| 14 | TP=12 SL=0 TrA=15 TrD=8 Split=single | +2.55 | +0.30 | -2.25 | +0.215 | +0.023 | 50.0 | -3.52 |
| 15 | TP=15 SL=0 TrA=0 TrD=3 Split=33_33_34 | +2.07 | +0.29 | -1.78 | +0.221 | +0.023 | 58.3 | -3.84 |
| 16 | TP=15 SL=0 TrA=15 TrD=8 Split=single | +3.00 | -0.13 | -3.13 | +0.229 | -0.009 | 45.8 | -5.23 |
| 17 | TP=15 SL=0 TrA=15 TrD=8 Split=33_33_34 | +1.99 | -0.71 | -2.70 | +0.214 | -0.060 | 58.3 | -3.86 |
| 18 | TP=5 SL=0 TrA=0 TrD=3 Split=single | +1.51 | -1.47 | -2.98 | +0.238 | -0.136 | 62.5 | -4.19 |
| 19 | TP=5 SL=0 TrA=15 TrD=8 Split=single | +1.51 | -1.47 | -2.98 | +0.238 | -0.136 | 62.5 | -4.19 |
| 20 | TP=5 SL=0 TrA=15 TrD=3 Split=single | +1.33 | -1.47 | -2.80 | +0.208 | -0.136 | 62.5 | -4.19 |

## Robust-Filter

Combos mit `test_mean > 0` UND `Δ > -2pp` (kein Overfitting-Crash):

1. **TP=15 SL=0 TrA=0 TrD=3 Split=single** — Train +3.23% → Test +1.76% (Δ -1.46pp)
2. **TP=25 SL=0 TrA=0 TrD=3 Split=33_33_34** — Train +3.41% → Test +1.42% (Δ -1.99pp)
3. **TP=12 SL=0 TrA=0 TrD=3 Split=single** — Train +2.55% → Test +1.42% (Δ -1.13pp)
4. **TP=20 SL=0 TrA=0 TrD=3 Split=50_50** — Train +2.82% → Test +1.28% (Δ -1.55pp)
5. **TP=20 SL=0 TrA=0 TrD=3 Split=33_33_34** — Train +2.51% → Test +0.92% (Δ -1.59pp)
6. **TP=15 SL=0 TrA=0 TrD=3 Split=33_33_34** — Train +2.07% → Test +0.29% (Δ -1.78pp)

## Empfehlung

**Deploy-Kandidat:** TP=15% / SL=0% / TrailAct=0% / TrailDist=3% / Split=single

- Test-Mean: **+1.76%**
- Test-Sharpe: **+0.121**
- Train→Test-Drift: **-1.46pp**

✅ **Stabil:** Drift gering — Deployment-würdig.

## Caveats

- Test-Sample: nur 24 Trades — statistische Power begrenzt.
- Walk-Forward statisch (single split) — Rolling-WF wäre robuster.
- Slippage Tier-Modell heuristisch.
- Concurrency-Annahme: alle Trades sequenziell.
