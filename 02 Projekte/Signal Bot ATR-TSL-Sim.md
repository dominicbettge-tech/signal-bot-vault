# Signal Bot — ATR-TSL-Simulation

_Generiert: 2026-04-17T21:32:01.549762+00:00_

## User-Input 2026-04-17
> *"mit was für indikatoren arbeitet jack wohl und mit welchem von ihnen könnte man den bot unterstützen"*

**P1 aus Überlegung:** ATR-basiertes TSL als erster Indikator-Layer simulieren.

## Methodik
- ATR-14 aus 1min-Bars der letzten 60min vor Entry
- TSL-Distance = K × ATR%, K ∈ [1.0, 1.5, 2.0, 2.5, 3.0]
- Hard-SL -6%, TTL 240min, Entry next-bar-open
- Baseline: fixed 3% TSL

## Coverage
- Total Buy-Verdicts: 83
- ATR-berechenbar (≥14+1 pre-bars): **80** (96%)

## Ergebnisse

| Rank | Config | n | Mean-PnL | Winrate | Median | TSL-Hit | Hard-SL | TTL | Σ-PnL |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `baseline_3pct` | 80 | -0.36% | 41% | -1.03% | 76% | 14% | 10% | -28.8% |
| 2 | `K1.5` | 80 | -1.08% | 29% | -0.81% | 71% | 29% | 0% | -86.1% |
| 3 | `K2.5` | 80 | -1.11% | 31% | -1.16% | 57% | 42% | 0% | -88.7% |
| 4 | `K1.0` | 80 | -1.11% | 30% | -0.45% | 76% | 24% | 0% | -88.9% |
| 5 | `K2.0` | 80 | -1.29% | 31% | -0.89% | 59% | 41% | 0% | -103.2% |
| 6 | `K3.0` | 80 | -1.64% | 25% | -2.48% | 52% | 46% | 1% | -131.1% |

## Delta vs. baseline_3pct

| Config | Δ Mean | Δ Winrate | Δ Σ-PnL |
|---|---|---|---|
| `K1.5` | -0.716pp | -12.5% | -57.3pp |
| `K2.5` | -0.748pp | -10.0% | -59.9pp |
| `K1.0` | -0.751pp | -11.2% | -60.1pp |
| `K2.0` | -0.930pp | -10.0% | -74.4pp |
| `K3.0` | -1.279pp | -16.2% | -102.3pp |

## ATR-Verteilung (pro Trade, in % vom Entry)

- Min: 0.13% · Max: 17.66% · Median: 3.49% · Mean: 3.73%

| ATR-Bucket | n Trades | % |
|---|---|---|
| <0.5% | 17 | 21.2% |
| 0.5-1% | 5 | 6.2% |
| 1-2% | 7 | 8.8% |
| 2-5% | 26 | 32.5% |
| >5% | 25 | 31.2% |

## G5-Gate Survival-Check

| Config | consistency | time_70_30 train→test | walk-forward mean | ticker-disjoint |
|---|---|---|---|---|
| `baseline_3pct` | ✅ | -0.00% → -1.19% | -0.53% (1/4 pos) | +0.06% → -1.33% |
| `baseline_3pct` | ✅ | -0.00% → -1.19% | -0.53% (1/4 pos) | +0.06% → -1.33% |

## Interpretation

- **Best-Config:** `baseline_3pct` mit Mean -0.36% (Δ +0.000pp vs. baseline_3pct)
- **ATR-Coverage:** 96% der Trades haben genug pre-bars für ATR-14
- **Achtung:** wenn Best-Config nur marginal besser als Baseline (<+0.3pp), ist ATR-TSL Regime-sensitiv
- **G5-Gate-Pflicht:** Default-Change nur wenn survival_check.consistency_flag=True UND ≥4/6 Checks

## Nächste Schritte
1. Wenn G5-Gate ✅ → ATR-TSL als H12-Kandidat in `project_testcenter_r_hypotheses.md` eintragen
2. Wenn G5-Gate ❌ → ATR-TSL als In-Sample-Artefakt markieren, Parser/Corpus-Ausbau hat Vorrang
3. Nächste Indikator-Sim: RSI-Peak-Exit (P2)

## Vorbehalte
- 1min-ATR kapturiert nicht die tägliche Range — Alternative: ATR-14 auf 5min oder daily
- Kein Slippage-Modell auf TSL-Fill
- Hard-SL -6% fest = kann gerade bei high-ATR-Tickern zu eng sein
- Keine Stratifizierung nach Ticker-Liquidity

