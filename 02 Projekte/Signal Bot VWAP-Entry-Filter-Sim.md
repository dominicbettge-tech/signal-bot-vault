# Signal Bot — VWAP-Entry-Filter-Simulation

_Generiert: 2026-04-18T04:37:49.008581+00:00_

## P5 — VWAP als Entry-Gate

Idee: Statt VWAP als **Exit**-Signal zu verwenden (das war P4, G5-FAIL),
prüfen wir die Distanz **entry_price ↔ running-VWAP** als **Entry-Filter**.
Hypothese: Entries nahe an der VWAP (Mean-Reversion-Zone) vs. weit darüber
(Overextended-Chase) unterscheiden sich signifikant.

## Methodik
- Cumulative-VWAP ab Session-Start (04:00 ET) bis Entry-Bar
- distance_pct = (entry_open − VWAP) / VWAP × 100
- Gleicher Exit bei allen Configs: fixed-3%-TSL + Hard-SL −6% + TTL 240min
- Baseline = alle Buys ohne Filter

## Distanz-Verteilung

- n=83 · min=-27.46% · Q25=-2.15% · Median=+4.82% · Q75=+19.02% · max=+63.11%
- Anteil entry>VWAP: 63%
- Anteil |dist|<=1%: 10%

## Ergebnisse

| Config | n | Mean | Median | Winrate | Σ-PnL | Δ vs Baseline |
|---|---|---|---|---|---|---|
| `baseline` | 82 | -0.29% | -0.93% | 41% | -24.1% | — |
| `above_vwap_only` | 51 | -0.11% | -1.10% | 45% | -5.5% | +0.186pp |
| `below_vwap_only` | 31 | -0.60% | -0.53% | 35% | -18.6% | -0.307pp |
| `near_vwap_1pct` | 7 | +0.08% | -0.53% | 29% | +0.6% | +0.373pp |
| `extended_cap_3pct` | 37 | -0.52% | -0.91% | 35% | -19.3% | -0.229pp |

## G5-Gate (best candidate vs baseline)

| Config | consistency | oos_positive | time_70_30 train→test | walk-forward | ticker-disjoint |
|---|---|---|---|---|---|
| `above_vwap_only` | ❌ | ❌ | +0.27%→-0.94% | -0.54% (1/3) | +0.27%→-0.94% |
| `baseline` | ❌ | ❌ | +0.13%→-1.26% | -0.53% (1/4) | +0.14%→-1.35% |

## Interpretation

- Best-Candidate: `above_vwap_only` Mean -0.11% (Δ +0.186pp vs Baseline)
- Hinweis: G5-FAIL bei Indikator-Sims zuvor war 1-min-Noise-Artefakt. VWAP-Distanz
  als Entry-Filter operiert NICHT auf 1-min-Bewegung, sondern auf einem
  kumulativen Preis-Volumen-Durchschnitt → weniger noise-anfällig.
