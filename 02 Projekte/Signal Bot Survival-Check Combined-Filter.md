# Signal Bot — Survival-Check Combined-Filter (G5-Gate)

_Generiert: 2026-04-17T21:37:56.377015+00:00_

## User-Direktive 2026-04-17 (dreifach-emphatisch)
> „alle simulationen an einem unbekannten täglichen markt überleben müssen"

Dieser Check prüft, ob die In-Sample-Befunde aus `Signal Bot Combined-Filter-Sim.md` auf
**ungesehenen Tagen** und **fremden Tickern** generalisieren — oder ob sie nur Overfit waren.

## Methodik (3 Achsen pro Szenario)

1. **70/30 Zeit-Split:** früheste 70% Trades = Train, späteste 30% = Test. Strikt: train[-1] < test[0]
2. **Walk-Forward:** rolling 45d Train / 14d Test, Schritt 14d (relaxed wegen Korpus-Sparsität)
3. **Ticker-Disjoint:** 30% distinkt-Ticker als Holdout → nie im Training gesehen

**consistency_flag:** True wenn test_mean ≥ 0.5 × train_mean UND Vorzeichen-Match

## Szenario-Überblick

| Scenario | n | Survival-Score | consistency_flag |
|---|---|---|---|
| `S0_Baseline` | 83 | ❌ 2/7 | True |
| `S1_SkipPM` | 61 | ❌ 1/7 | False |
| `S2_SkipPM+AH` | 56 | ❌ 1/7 | False |
| `S3_S2+User_Ladder` | 56 | ❌ 1/7 | False |

## Detail pro Szenario

### S0_Baseline  — Ladder `H2_base`

**consistency_flag:** ✅ PASS  ·  **oos_positive_flag:** ❌ FAIL

| Achse | n_train | n_test | train_mean | test_mean | Δ | Notes |
|---|---|---|---|---|---|---|
| 70/30 Zeit  | 58 | 25 | -0.10% | -0.98% | -0.89pp | time_leak=False · tk_overlap=2 |
| Walk-Forward | — | Σ 0 | — | -0.35% | pos_folds=1/4 | fold_means=[-0.415, -2.12, 2.917, -1.768] |
| Ticker-Disjoint | 42 tkr | 18 tkr | -0.09% | -1.01% | -0.92pp | holdout=30% distinkt-Ticker |

### S1_SkipPM  — Ladder `H2_base`

**consistency_flag:** ❌ FAIL  ·  **oos_positive_flag:** ❌ FAIL

| Achse | n_train | n_test | train_mean | test_mean | Δ | Notes |
|---|---|---|---|---|---|---|
| 70/30 Zeit  | 42 | 19 | +0.18% | -0.49% | -0.67pp | time_leak=False · tk_overlap=1 |
| Walk-Forward | — | Σ 0 | — | -0.17% | pos_folds=1/4 | fold_means=[-0.346, -2.12, 2.917, -1.153] |
| Ticker-Disjoint | 33 tkr | 14 tkr | +0.27% | -0.65% | -0.92pp | holdout=30% distinkt-Ticker |

### S2_SkipPM+AH  — Ladder `H2_base`

**consistency_flag:** ❌ FAIL  ·  **oos_positive_flag:** ❌ FAIL

| Achse | n_train | n_test | train_mean | test_mean | Δ | Notes |
|---|---|---|---|---|---|---|
| 70/30 Zeit  | 39 | 17 | +0.26% | -0.19% | -0.46pp | time_leak=False · tk_overlap=0 |
| Walk-Forward | — | Σ 0 | — | -0.14% | pos_folds=1/4 | fold_means=[-0.219, -2.12, 2.917, -1.153] |
| Ticker-Disjoint | 31 tkr | 13 tkr | +0.44% | -0.49% | -0.93pp | holdout=30% distinkt-Ticker |

### S3_S2+User_Ladder  — Ladder `user_3_7_15`

**consistency_flag:** ❌ FAIL  ·  **oos_positive_flag:** ❌ FAIL

| Achse | n_train | n_test | train_mean | test_mean | Δ | Notes |
|---|---|---|---|---|---|---|
| 70/30 Zeit  | 39 | 17 | +0.50% | -0.41% | -0.91pp | time_leak=False · tk_overlap=0 |
| Walk-Forward | — | Σ 0 | — | -0.25% | pos_folds=1/4 | fold_means=[-0.399, -1.24, 1.8, -1.153] |
| Ticker-Disjoint | 31 tkr | 13 tkr | +0.69% | -0.68% | -1.37pp | holdout=30% distinkt-Ticker |

## Checks-Matrix

| Scenario | consistency | test_70_30>0 | wf_mean>0 | wf_majority | ticker_disjoint>0 | no_time_leak |
|---|---|---|---|---|---|---|
| `S0_Baseline` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `S1_SkipPM` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `S2_SkipPM+AH` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `S3_S2+User_Ladder` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

## 🚨 Hauptbefund

**KEIN Szenario überlebt das G5-Gate.** S3 (heutiger "Sieger" aus Combined-Filter-Sim mit
+0.22% Mean in-sample) erreicht auf OOS-Test nur 1/6 Checks.

- **Train-vs-Test 70/30:** Alle Filter-Szenarien zeigen **Vorzeichen-Flip**
  (S1-S3 Train positiv → Test negativ). Der Filter entfernt In-Sample-Noise, nicht generalisierbaren Edge.
- **Walk-Forward:** Pattern `fold_means=[fN, fD, fJ, fF]` zeigt **eine einzige positive Fold-Periode**
  (Dez->Jan), alle anderen verlieren. Die +0.22% sind ein Regime-Artefakt.
- **Ticker-Disjoint:** Holdout-Ticker verlieren durchgaengig -0.5 bis -1.4pp vs. Train.
  -> Der Korpus-Edge kommt aus **wiederholten Tickern**, nicht aus der Strategie-Logik.

## Interpretation

- **Zero-Tolerance-Gate:** Default-Change nur bei 6/6 ✅ — heute trifft NIEMAND zu
- **Regime-Artefakt-Erkennung:** pos_folds=1/4 bei Walk-Forward = ein glücklicher Monat, nicht Edge
- **Ticker-Overfit-Erkennung:** Holdout-Ticker-Delta < −0.5pp bei allen Filter-Szenarien
- **Positive Nachricht:** Das G5-Gate hat seine Arbeit getan — Overfit wurde **VOR** Default-Change erkannt

## Nächste Schritte

1. **KEIN Default-Change für Skip-PM, Skip-AH oder user_3_7_15** — zurück zu H2_base-Default
2. H10/H11 in `project_testcenter_r_hypotheses.md` als **OOS-FAIL** markieren
3. Korpus-Ausbau Priorität #1: n=83 ist zu klein, Biotech-Bias zu stark
4. Nächste Hebel: Ticker-Liquidity-Filter, Regime-bedingte Sizing, Catalyst-Presence-Check
5. Re-Test bei n≥150 Trades + Cross-Regime-Corpus

## Ticker-Diversitaet-Diagnostik (2026-04-17 abends)

- **Total Trades:** 83
- **Unique Ticker:** 60 (sehr hohe Diversitaet)
- **Singleton-Ticker (n=1):** 40/60 = 67%
- **Wiederholende Ticker (n>=3):** 3/60 = 5% (AKBA/LAES/AQST je 3x)
- **Top-3-Ticker-Share:** 10.8% · Top-10-Share: 27.7%

**Interpretation:** Korpus ist diversifiziert, KEIN Concentration-Bias. Ticker-Disjoint-Fail
kommt NICHT aus Edge-auf-Wenigen-Tickern. Stattdessen: der `Edge' ist regime-spezifisch
(eine Fold-Periode positiv). Strategy-level Features wie Time-of-Day sind auf In-Sample zwar
statistisch signifikant, verlieren aber im OOS, weil das echte Signal schwach ist und
Regime-Shifts dominieren.

## Verbindungen
- `Signal Bot Combined-Filter-Sim.md` — In-Sample-Basis
- `testcenter/walk_forward.py` — Helper-Library (22 Unit-Tests grün)
- `testcenter/test_walk_forward.py` — Gate-Logik abgesichert
- Memory `feedback_generalization_first_always.md`, `feedback_case_vs_corpus_evidence.md`

