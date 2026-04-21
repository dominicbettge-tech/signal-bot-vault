# Signal Bot — Staggered Range-Entry Sim

_Generiert: 2026-04-21T04:06:30.903062Z_

## Setup
- **Korpus:** alle `signals.signal_type='entry'` mit entry_low != entry_high (n=29)
- **Expiry:** 60min — Limit aktiv nach Signal
- **Hold:** 120min — Exit = Close des letzten Bars
- **Fill-Rule:** bar.low <= limit → fill; wenn bar.open < limit auch → fill @ open
- **PnL weighted on full-position** (nicht-gefüllte Tranchen → 0-Anteil)

## Varianten
- **Baseline:** 1 Limit @ midpoint (aktueller Bot)
- **CAND-B (Konservativ):** 3 Tranchen — 50% @ entry_high / 30% @ midpoint / 20% @ entry_low
- **CAND-C (Aggressiv):** 100% @ entry_high

## Ergebnis
```
BASELINE (mid only)  fill_rate=20.0% mean_fill_frac=0.20 mean_pnl=+1.51% winrate=25%
CAND-B (50/30/20)    fill_rate=65.0% mean_fill_frac=0.42 mean_pnl=-1.51% winrate=23%
CAND-C (100 @ high)  fill_rate=65.0% mean_fill_frac=0.65 mean_pnl=-3.65% winrate=23%
```

## Per-Signal Details

| Ticker | ET | Range | Base-Fill | Base-PnL | B-Fill | B-PnL | C-Fill | C-PnL |
|---|---|---|---:|---:|---:|---:|---:|---:|
| BFRG | 2026-03-30T09:47 | [1.02,1.06] | 1.00 | 19.23 | 1.00 | 18.55 | 1.00 | 16.98 |
| AGPU | 2026-04-01T11:39 | [3.17,3.22] | 0.00 | — | 0.50 | 4.04 | 1.00 | 8.07 |
| GV | 2026-04-02T11:43 | [0.42,0.45] | 0.00 | — | 0.50 | -8.87 | 1.00 | -17.73 |
| GV | 2026-04-02T11:44 | [0.42,0.45] | 0.00 | — | 0.50 | -8.37 | 1.00 | -16.73 |
| GV | 2026-04-02T11:54 | [0.42,0.45] | 0.00 | — | 0.50 | -4.67 | 1.00 | -9.33 |
| GV | 2026-04-02T12:00 | [0.42,0.45] | 0.00 | — | 0.50 | -6.48 | 1.00 | -12.96 |
| GV | 2026-04-06T09:16 | [0.255,0.27] | 0.00 | — | 0.00 | — | 0.00 | — |
| GV | 2026-04-06T09:47 | [0.255,0.27] | 0.00 | — | 0.00 | — | 0.00 | — |
| GV | 2026-04-06T09:52 | [0.255,0.27] | 0.00 | — | 0.00 | — | 0.00 | — |
| GV | 2026-04-06T10:39 | [0.255,0.27] | 0.00 | — | 0.00 | — | 0.00 | — |
| GV | 2026-04-06T10:52 | [0.255,0.27] | 0.00 | — | 0.00 | — | 0.00 | — |
| ADVB | 2026-04-07T07:30 | [6.82,7.1] | 0.00 | — | 0.50 | 1.41 | 1.00 | 2.82 |
| ADVB | 2026-04-07T07:36 | [6.82,7.1] | 0.00 | — | 0.50 | -0.45 | 1.00 | -0.89 |
| ADVB | 2026-04-07T07:40 | [6.82,7.1] | 0.00 | — | 0.50 | -0.35 | 1.00 | -0.7 |
| ADVB | 2026-04-07T07:44 | [6.82,7.1] | 0.00 | — | 0.50 | -0.21 | 1.00 | -0.42 |
| ADVB | 2026-04-07T08:51 | [6.82,7.1] | 1.00 | -3.07 | 1.00 | -3.65 | 1.00 | -4.98 |
| OMEX | 2026-04-08T09:48 | [1.62,1.67] | 1.00 | -6.38 | 1.00 | -6.81 | 1.00 | -7.78 |
| OMEX | 2026-04-08T11:32 | [1.62,1.67] | 1.00 | -3.74 | 1.00 | -3.74 | 1.00 | -3.74 |
| OCGN | 2026-04-13T09:05 | [1.64,1.68] | 0.00 | — | 0.00 | — | 0.00 | — |
| LAES | 2026-04-16T11:57 | [2.45,2.49] | 0.00 | — | 0.00 | — | 0.00 | — |
