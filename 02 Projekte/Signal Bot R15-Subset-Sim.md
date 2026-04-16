# Signal Bot — R15 Subset-Sim: HardTP vs Scaled-Jack-TSL

_Generiert: 2026-04-16T09:40:00+00:00_

## Setup

- **Quelle:** alle `human_verdict='b'` aus backtest_results.db (83 total)
- **Filter:** R15-eligible = `monster_score ≥ 0.4` UND `msg_et ∈ [09:30, 14:00)`
- **Subset-Größe:** 27 Trades
- **Skipped:** score<floor=25, out_of_RTH=22, no_features=9, no_bar=0
- **Window:** 4h post-entry oder EOD (15:55 ET)

## Action-Layer-Vergleich auf R15-eligible Subset

| Action-Layer | n | Mean % | Win % | Sharpe-like | Std % | Min % | Max % | Eq Final | Total Ret % | Max-DD % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HardTP_10 (NEU R15-Action) | 27 | +1.88 | 77.8 | +0.122 | 15.39 | -31.9 | +10.0 | 1.0486 | +4.86 | -4.29 |
| NaiveHold_EOD (Baseline) | 27 | -1.42 | 44.4 | -0.043 | 32.98 | -75.4 | +115.9 | 0.9491 | -5.09 | -14.52 |
| ScaledJack_TSL (ALT R15-v3) | 27 | -2.85 | 29.6 | -0.247 | 11.54 | -10.0 | +24.8 | 0.9242 | -7.58 | -8.92 |

## Verdict

🟢 **HardTP+10 schlägt Scaled-Jack-TSL auf R15-eligible Subset:**
  - HardTP_10: Mean **+1.88%/trade** (Rang 1)
  - ScaledJack_TSL: Mean **-2.85%/trade** (Rang 3)
  - Delta: **+4.73pp** zugunsten HardTP

→ R15-Action-Umstellung von Trail auf Hard-TP+10 ist auf der Ziel-Population validiert.

## Per-Trade-Detail

| # | Ticker | Msg-ID | Score | msg_et | Entry $ | HardTP_10 % | Scaled-Jack % | Naive-EOD % |
|---|---|---:|---:|---|---:|---:|---:|---:|
| 1 | GNPX | 3488 | 1.00 | 09:54 | 34.73 | +10.00 | -10.00 | +8.95 |
| 2 | IVF | 3524 | 0.45 | 10:11 | 32.76 | +10.00 | -0.44 | -0.44 |
| 3 | VSEE | 3560 | 0.90 | 10:28 | 0.90 | +10.00 | -10.00 | -7.06 |
| 4 | BENF | 3577 | 0.90 | 10:09 | 9.92 | -6.47 | -10.00 | -6.47 |
| 5 | SCNX | 3600 | 0.90 | 10:23 | 1.32 | +10.00 | -10.00 | -4.15 |
| 6 | CODX | 3626 | 0.90 | 09:49 | 24.61 | +10.00 | -10.00 | +31.02 |
| 7 | XHLD | 3644 | 0.90 | 09:44 | 10.13 | +10.00 | +18.62 | -28.93 |
| 8 | MTC | 3705 | 0.55 | 11:33 | 0.72 | +10.00 | -10.00 | +115.88 |
| 9 | MSPR | 3727 | 0.70 | 09:52 | 0.73 | -24.99 | -10.00 | -24.99 |
| 10 | SLRX | 3728 | 0.70 | 10:22 | 0.99 | +1.60 | +1.60 | +1.60 |
| 11 | LPTX | 3732 | 0.90 | 12:33 | 1.64 | +10.00 | -10.00 | +23.78 |
| 12 | CYPH | 3748 | 0.70 | 10:18 | 2.79 | +10.00 | +3.23 | +3.23 |
| 13 | CYPH | 3749 | 0.70 | 10:30 | 3.04 | +10.00 | -10.00 | -5.75 |
| 14 | AMIX | 3754 | 0.90 | 09:37 | 1.45 | -27.58 | -10.00 | -27.58 |
| 15 | INHD | 3780 | 1.00 | 11:21 | 57.60 | +10.00 | +24.77 | -75.41 |
| 16 | CETY | 3797 | 0.90 | 09:54 | 2.12 | +10.00 | -10.00 | +25.37 |
| 17 | QTTB | 3848 | 0.90 | 09:38 | 4.93 | +10.00 | -10.00 | -13.39 |
| 18 | IRBT | 3861 | 0.55 | 11:02 | 2.38 | -30.82 | -10.00 | -30.82 |
| 19 | PLRZ | 3874 | 0.75 | 10:04 | 6.65 | +10.00 | -10.00 | +12.63 |
| 20 | ADCT | 3889 | 0.45 | 11:55 | 3.10 | +10.00 | +21.74 | +21.74 |
| 21 | KALA | 3907 | 0.90 | 10:12 | 1.63 | -31.92 | -10.00 | -31.92 |
| 22 | EKSO | 3913 | 0.45 | 11:08 | 3.63 | +10.00 | +11.57 | +11.57 |
| 23 | GURE | 3925 | 0.50 | 10:00 | 9.83 | +10.00 | -10.00 | -8.62 |
| 24 | WVE | 3975 | 0.90 | 10:41 | 16.65 | +10.00 | +16.40 | +16.40 |
| 25 | IMMP | 3977 | 0.90 | 10:52 | 3.29 | -29.18 | -10.00 | -29.18 |
| 26 | WVE | 3980 | 0.90 | 11:15 | 17.63 | +10.00 | +5.56 | +5.56 |
| 27 | NCPL | 4012 | 0.90 | 10:06 | 1.64 | +10.00 | -10.00 | -21.41 |

## Caveats

- Subset klein (n=27) → größere Confidence erst mit mehr R15-Coverage
- Kein Spread-/Slippage-Modell — P2-Block
- HardTP setzt voraus dass Bot Limit @+10% direkt nach Fill platziert (1-2s Latenz akzeptabel)
- Trail-Action assumes Trail-Activation NACH 1. TP (sonst -15% Trail >= -10% SL)
