# Signal Bot — Indikator-Sim Masterübersicht (2026-04-17 Abend 5)

_Generiert automatisch nach User-Direktive „autonom bis morgen früh"._

## Ausgangsfrage (User, 2026-04-17)
> *„mit was für indikatoren arbeitet jack wohl und miit welchem von ihnen könnte man den bot unterstützen nachher rim live trading um seine profitabilität zu steigern"*

→ Fünf Exit-Layer-Indikatoren auf dem 82-Buy-Corpus (b-Verdicts, 1-min-Polygon-Bars, 240-min-TTL, Hard-SL -6%) simuliert und durch G5-Gate (70/30-Time + Walk-Forward + Ticker-Disjoint + neuer `oos_positive_flag`) geprüft.

## Ergebnis-Matrix

| Indikator | Best-Variante | Trigger | n | Mean | Δ Baseline | Winrate | G5-consistency | G5-oos_positive | Train→Test 70/30 | WF mean (pos/total) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Baseline** | 3%-TSL (reference) | fixed TSL | 82 | -0.29% | 0 | 41% | — | — | — | — |
| P1 ATR | K=1.5 | 1.5× ATR-14 (1-min) | 80 | -1.08% | -0.72pp | 29% | ❌ | ❌ | — | — |
| P2 RSI-1min | `rsi_only` | RSI≥70 + Decline | 82 | **+1.62%** (!) | +1.92pp | 32% | ❌ | ❌ | -0.63% → +6.77% | -1.57% (1/4) |
| H12c RSI-5min | `rsi5_tsl3` | 5-min-RSI + 3%-TSL | 82 | -0.20% | +0.09pp | 44% | ❌ | ❌ | +0.16% → -1.02% | -0.23% (1/4) |
| P3 Volume-Climax | `vc_k3_tsl3` | Vol≥3×MA + Bearish + TSL | 82 | -0.34% | -0.05pp | 41% | ❌ | ❌ | — | — |
| P4 VWAP-Break | `vwap_tsl3` | Close<cum-VWAP + Bearish + TSL | 82 | -0.29% | 0.00pp | 44% | ❌ | ❌ | +0.08% → -1.14% | -0.47% (1/4) |

**Zentrale Beobachtung:** Keine einzige Indikator-Variante besteht das G5-Gate auf diesem Korpus.

## Kritisches Meta-Finding

**Die scheinbar riesige In-Sample-Edge der RSI-1-min-Variante (+1.92pp) verschwindet fast komplett in der 5-min-Denoising-Variante (+0.09pp).**

Das ist ein **klassisches Noise-Overfit-Signal**:
- 1-min-Auflösung + Penny-Stock-Volatilität = True-Noise-Regime
- "Edge" entsteht durch zufällige RSI-Kreuzungen, die korreliert sind mit den letzten ~25 Trades des Korpus
- Walk-Forward zeigt erwartungsgemäß 1/4 positive Folds → der Gewinn kommt aus genau EINEM zeitlichen Abschnitt
- Ticker-Disjoint Train vs. Test (-0.71% vs +7.27%) bestätigt: test-Ticker sind zufällig die „glücklichen"

## Warum Baseline 3% TSL gewinnt

1. **Niedrige Varianz:** Fixed TSL zieht bei jedem Trade gleich, keine Indicator-False-Positives
2. **Gegenseitige Abdeckung mit Hard-SL:** 3% TSL hält Gewinne, Hard-SL deckt Risiko
3. **Indikator-Trigger ohne TSL (Hard-SL only)** ist KATASTROPHAL (Mean -1.88% bis -2.74%), weil ohne TSL kein Profit-Schutz existiert
4. **Indikator-Trigger MIT TSL** ersetzt nur einige TSL-Hits durch Indikator-Hits → kein PnL-Delta (Wasser-Statt-Wasser)

## Tool-Upgrade dieses Abends

- **`oos_positive_flag`** neu in `testcenter/walk_forward.py` `survival_check()`
- **Grund:** Alter `consistency_flag` gab False zurück wenn Train<0 aber Test>0 (OOS-Improvement). Semantisch falsch.
- **Neu:** `oos_positive_flag = test_mean>0 ∧ walk_forward_mean>0 ∧ ticker_disjoint_test>0`
- **Tests:** 24/24 grün im Walk-Forward-Suite, 347/347 gesamt im Testcenter

## Konsequenz (Default-Entscheidungen)

1. **fixed-3%-TSL bleibt der Default.** Keine Änderung bei TSL-Logik.
2. **Alle fünf Indikator-Hypothesen (H12/H12c/H13/H14/H15)** markiert als Hypothese-only, keine Library-Promotion.
3. **Indikator-Retest braucht:** n≥150 + 5-min-Aufl. (min) + Cross-Regime (Bull/Flat/Bear ≥30 pro Regime) + Parser-verbesserte Messages.
4. **Echter Hebel für Live-Profitabilität: Parser-Quality-Maximization** — mehr Bot-ready-Messages → mehr Trade-Samples → erst dann robuste Default-Änderungen möglich.

## Artefakte

- `scripts/atr_tsl_sim.py`
- `scripts/rsi_peak_exit_sim.py`
- `scripts/rsi_5min_exit_sim.py`
- `scripts/volume_climax_exit_sim.py`
- `scripts/vwap_break_exit_sim.py`
- `scripts/survival_check_combined.py` (erweitert um `oos_positive_flag`-Check, 7 Checks gesamt)
- `testcenter/walk_forward.py` + Tests
- Einzelreports je Sim unter `02 Projekte/Signal Bot *-Sim.md`

## Anti-Pattern-Log (damit wir das nicht wieder machen)

- **1-min-Indikatoren auf n<100 Penny-Stock-Korpus** → produziert immer scheinbare Edges, immer Noise. Nie wieder als Default-Kandidat ohne 5-min-Denoising-Cross-Check.
- **`consistency_flag` allein** ist ein Zu-Streng-Gate. `oos_positive_flag` fängt OOS-Improvements → jetzt beide Flags Pflicht-Rendering.
- **In-Sample-Delta >1pp ohne G5-Check** ist keine Empfehlung, sondern eine Hypothese. Verankert in `feedback_generalization_first_always.md`.

*Masterübersicht geschrieben 2026-04-17/18 autonom, kein User-Approval nötig für Dokumentations-Files.*
