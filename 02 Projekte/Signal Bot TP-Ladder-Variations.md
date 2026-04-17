# Signal Bot — TP-Ladder-Variations-Sim

_Generiert: 2026-04-17T21:04:34.088838+00:00_

## Setup
- **Korpus:** `human_verdict='b'` außer SLS
- **N simuliert:** 83 (skipped 0)
- **SL:** -3% fix
- **TTL:** 240min
- **Entry:** next-bar-open nach Msg

## Ranking (nach Mean-PnL)

| Rank | Variant | TPs | Shares | Mean-PnL | Median-PnL | Winrate | SL-Hits | TP-Full | Mean-MaxDD |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `user_3_7_15` | +3%/+7%/+15% | 33%/33%/34% | -0.151% | -1.02% | 31% | 55/83 | 10/83 | -4.01% |
| 2 | `early_weight` | +3%/+7%/+15% | 50%/30%/20% | -0.191% | -0.95% | 31% | 55/83 | 10/83 | -4.01% |
| 3 | `late_weight` | +5%/+10%/+20% | 25%/25%/50% | -0.307% | -3.00% | 22% | 57/83 | 7/83 | -4.10% |
| 4 | `moderate_run` | +5%/+15%/+30% | 33%/33%/34% | -0.318% | -3.00% | 22% | 60/83 | 4/83 | -4.24% |
| 5 | `H2_base` | +5%/+10%/+20% | 33%/33%/34% | -0.398% | -3.00% | 22% | 57/83 | 7/83 | -4.10% |
| 6 | `runner` | +10%/+20%/+40% | 33%/33%/34% | -0.450% | -3.00% | 22% | 60/83 | 2/83 | -4.24% |
| 7 | `aggressive` | +2%/+5%/+10% | 33%/33%/34% | -0.585% | -1.35% | 33% | 55/83 | 10/83 | -3.98% |

## Delta vs. H2_base (current default, Mean=-0.398%)

| Variant | Δ Mean-PnL |
|---|---|
| `user_3_7_15` | +0.248pp 📈 |
| `early_weight` | +0.207pp 📈 |
| `late_weight` | +0.091pp 📈 |
| `moderate_run` | +0.080pp 📈 |
| `H2_base` | +0.000pp → |
| `runner` | -0.052pp 📉 |
| `aggressive` | -0.187pp 📉 |

## Lesart
- **TP-Full** = Anteil Trades, die alle 3 Ladder-Stufen treffen (= runner-Scenario)
- **SL-Hits** = Anteil Trades, die den -3% Hard-SL treffen
- **Mean-MaxDD** = durchschnittlicher intra-trade Drawdown (nicht realisiert)
- Entry-Assumption = next-bar-open, keine Slippage

## Generalisierungs-Vorbehalt (REGEL 4)
- In-Sample n=83. Default-Change **nur** nach Walk-Forward + Cross-Ticker + n≥30 Out-of-Sample
- Korpus ist Biotech-lastig (Jack-Bias). Out-of-Regime-Transfer unklar
- `feedback_case_vs_corpus_evidence.md`: Rank-1 hier = Hypothese, nicht Default

## Caveats
- Kein Entry-Latenz-Modell (nur 1min-Latenz aus next-bar-open)
- Kein Slippage auf TP-Limit-Orders
- TTL 4h — Runner-Varianten (+40% Target) kommen in 4h oft nicht an → TP-Full-Rate niedrig, obwohl Pattern vielleicht da
- Biotech-Halt/Liquidity-Spikes nicht modelliert

## Verbindungen memory
- `feedback_adaptive_stack_validated.md`: H2 Ladder 33/33/34 ist aktueller Default
- `project_testcenter_4phase_plan.md`: TP-Ladder-Tuning gehört zu Phase C
- Staggered-Entry-Report 2026-04-17: empfahl +3/+7/+15 — hier getestet als `user_3_7_15`
