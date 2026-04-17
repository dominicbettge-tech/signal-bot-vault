# Signal Bot — TSL-Sweep nach Trade-Typ

_Generiert: 2026-04-17T21:00:26.846336Z_

## Setup
- **Korpus:** alle `human_verdict='b'` außer SLS
- **N simuliert:** 83 (skipped 0)
- **TSL-Werte:** ['2%', '3%', '4%', '5%', '6%', '8%', '10%', '12%', '15%']
- **Hard-SL:** -6% fix (Catastrophic-Guard)
- **TTL:** 240min
- **Entry:** next-bar-open nach Msg

## Mean-PnL je TSL × Kohorte

| TSL | all | day_kw | swing_kw | parser_day | parser_unknown |
|---|---|---|---|---|---|
| 2% | +0.04% (42%, n=83) | +0.98% (55%, n=22) | -0.22% (32%, n=19) | +0.58% (48%, n=23) | -0.07% (44%, n=48) |
| 3% | -0.26% (39%, n=83) | +0.62% (50%, n=22) | -0.40% (37%, n=19) | +0.24% (43%, n=23) | -0.28% (40%, n=48) |
| 4% | -0.57% (40%, n=83) | -0.12% (41%, n=22) | -0.59% (37%, n=19) | -0.47% (39%, n=23) | -0.60% (42%, n=48) |
| 5% | -1.06% (31%, n=83) | -1.28% (32%, n=22) | -0.94% (26%, n=19) | -1.67% (30%, n=23) | -0.99% (33%, n=48) |
| 6% | -0.85% (34%, n=83) | -1.27% (32%, n=22) | +0.96% (37%, n=19) | -1.62% (30%, n=23) | -0.81% (35%, n=48) |
| 8% | -1.13% (31%, n=83) | -1.00% (36%, n=22) | +0.24% (32%, n=19) | -1.28% (35%, n=23) | -1.37% (29%, n=48) |
| 10% | -1.37% (27%, n=83) | +0.09% (27%, n=22) | -0.18% (32%, n=19) | -0.17% (26%, n=23) | -2.27% (25%, n=48) |
| 12% | -1.45% (28%, n=83) | +0.29% (32%, n=22) | -0.43% (32%, n=19) | +0.02% (30%, n=23) | -2.44% (25%, n=48) |
| 15% | -0.04% (31%, n=83) | +2.15% (36%, n=22) | +0.22% (37%, n=19) | +1.80% (35%, n=23) | -0.77% (29%, n=48) |

## Best-TSL pro Kohorte

| Kohorte | Best-TSL | Mean-PnL | Winrate | n |
|---|---|---|---|---|
| all | 2% | +0.04% | 42% | 83 |
| day_kw | 15% | +2.15% | 36% | 22 |
| swing_kw | 6% | +0.96% | 37% | 19 |
| parser_day | 15% | +1.80% | 35% | 23 |
| parser_unknown | 2% | -0.07% | 44% | 48 |

## TSL-Exit-Anteile (wie oft wird TSL getroffen?)

| TSL | all | day_kw | swing_kw | parser_day | parser_unknown |
|---|---|---|---|---|---|
| 2% | 67/83 (81%) | 17/22 (77%) | 19/19 (100%) | 17/23 (74%) | 40/48 (83%) |
| 3% | 61/83 (73%) | 17/22 (77%) | 14/19 (74%) | 17/23 (74%) | 37/48 (77%) |
| 4% | 56/83 (67%) | 17/22 (77%) | 12/19 (63%) | 17/23 (74%) | 33/48 (69%) |
| 5% | 44/83 (53%) | 12/22 (55%) | 9/19 (47%) | 11/23 (48%) | 30/48 (62%) |
| 6% | 36/83 (43%) | 12/22 (55%) | 6/19 (32%) | 11/23 (48%) | 23/48 (48%) |
| 8% | 30/83 (36%) | 11/22 (50%) | 4/19 (21%) | 10/23 (43%) | 19/48 (40%) |
| 10% | 23/83 (28%) | 10/22 (45%) | 2/19 (11%) | 10/23 (43%) | 12/48 (25%) |
| 12% | 17/83 (20%) | 7/22 (32%) | 2/19 (11%) | 7/23 (30%) | 9/48 (19%) |
| 15% | 12/83 (14%) | 7/22 (32%) | 0/19 (0%) | 7/23 (30%) | 4/48 (8%) |

## Lesart
- **Mean-PnL** = Durchschnittsrendite über alle Trades der Kohorte bei dem TSL-Wert
- **Winrate** = Anteil Trades mit PnL > 0
- **Hard-SL -6%** liegt über allen TSL-Werten; greift nur bei Gap-Down oder Volatilitäts-Spike
- Entry = next-bar-open nach Msg (1min Latenz)

## Caveats
- Swing/Day-Zuordnung per Keyword-Regex → grobes Proxy
- Parser-Trade-Type 48/71 = 'unknown', nur 23 = 'day_trade', 0 = 'swing' → Label-Qualität mager
- Kein Slippage-Modell auf TSL-Fill
- TTL=4h für alle — Swing-Kohorte müsste eigentlich 1-3d laufen (nicht modelliert)

## Validierungs-Quellen memory
- `project_tsl_by_trade_type.md`: OMER/LAES/VSTM-Cases (Day=3%, Swing=8-10%, Long=15-20%)
- `project_testcenter_4phase_plan.md`: TSL-Optimierung gehört zu Phase C
