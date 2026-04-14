---
tags: [signal-bot, testcenter, architektur, variablen]
date: 2026-04-14
status: draft-v2
parent: "[[Signal Bot]]"
---

# Testcenter — Architektur v2

> v1 war eine Struktur-Liste. v2 fügt Experiment-**Disziplin** hinzu:
> Hypothesen statt Grid-Search-Blind, Sensitivity-Hierarchie, Interaktions-Matrix,
> Stop-Kriterien, Negative-Controls. Ohne diese Zusätze optimiert man Noise.

## 5-Schichten-Aufbau (aus v1, unverändert)

```
1. DATA-LAYER  → fixtures, intraday_bars, raw_messages, results
2. VARIABLE-REGISTRY (testcenter_params.yaml) → siehe A-G
3. PIPELINE  → features → regime → engine → safety → simulator → pnl
4. EXPERIMENT-FRAMEWORK  → single_run, grid_search, walk_forward, ablation
5. EVALUATION-LAYER  → win-rate × avg-pnl × max-DD × Sharpe × per-rule-attribution
```

## Variable-Registry A-G (aus v1, kondensiert)

**A. Position-Sizing** — base_pct, max_open, distress_mult×3, soft_score_reduction, multi_ticker_split
**B. Exit** — tsl_day/swing/distress, tp_ladder_split, hard_dd_cap, tp_cap_enabled
**C. Entry** — r1_offset, r1_ttl_extra, staggered_offsets, rth_only
**D. Gates** — falling_knife_db/ad, soft_score_skip, out_of_session_days, post_spike_window/pullback
**E. Circuit-Breakers** — daily_dd, aggregate_dd, loss_streak, api_errors, hit_rate_drift
**F. Regime-Gating** — active_regimes, vix_skip_below/above, vix_rising_bias
**G. Rule-Toggles** — r1_enabled…r9_enabled, active_statuses

(Detaillierte Defaults/Ranges stehen in Memory + Live-Roadmap, hier nur Struktur.)

---

## NEU §H — Sensitivity-Hierarchie

**Problem:** 30+ Variablen. Grid-Search über alle = 10^30 Kombinationen. Impossible.

**Lösung:** Variablen in 3 Tiers ordnen, Tier-1 zuerst, Tier-3 zuletzt (oder nie).

| Tier | Erwarteter Impact | Kriterium | Variablen |
|---|---|---|---|
| **T1 Critical** | ±5% PnL-Delta | direkt im Hot-Path jedes Trades | `tsl_day_pct`, `tp_ladder_split_a`, `base_position_pct`, `hard_dd_cap_pct`, `falling_knife_thresholds` |
| **T2 Material** | ±1-3% | moduliert viele Trades | `r1_offset_pct`, `soft_score_reduction_per_pt`, `distress_mult_×3`, `active_regimes` |
| **T3 Polish** | <1% | Einzelfälle oder selten | `loss_streak_max`, `vix_rising_bias`, `staggered_offsets`, `r1_ttl_extra_min` |

**Regel:** T1 erschöpfend sweepen, T2 nach T1 mit fixierten T1-Optima, T3 nur wenn T1+T2 keinen Gewinn mehr bringen oder als Robustness-Check.

## NEU §I — Interaktions-Matrix (Variablen-Kopplung)

**Problem:** TSL und Position-Size sind gekoppelt. 3% TSL × 20% Size ≠ 3% TSL × 10% Size + 20% Size × 1.5% TSL.

**Bekannte Kopplungen (aus Review-Memory):**

| Paar | Warum gekoppelt | Experiment-Konsequenz |
|---|---|---|
| `tsl_day × base_position` | enger TSL @ hoher Size = Overtrading durch häufige Stop-Outs | nur gemeinsam sweepen |
| `tp_ladder_split × hard_dd_cap` | 50/50 Split braucht engeren DD-Cap als 80/20 | paarweise, nicht isoliert |
| `falling_knife_db × ad` | beide Thresholds definieren Veto-Präzision zusammen | 2D-Grid statt 2x1D |
| `r1_offset × soft_score_skip` | höherer Offset + lockerer Skip = mehr schlechte Fills | paarweise |
| `distress_mult × hard_dd_cap` | große Multiplier verstoßen gegen DD-Cap wenn zu eng | gemeinsam kalibrieren |
| `active_regimes × regime-gated rules` | Rule-Toggle-Effekt abhängig vom Regime-Mix im Val-Fenster | Regime-stratifizierte Evaluation |

**Regel:** Kopplungen als 2D/3D-Slices sweepen, nicht als 1D-Marginalien. Das ist der Unterschied zwischen "Grid-Search" (naiv) und "Sparse-Design" (kompetent).

## NEU §J — Experiment-Protokoll (Hypothesis-Driven)

**Anti-Pattern:** "Lass uns mal TSL zwischen 1% und 5% durchprobieren und schauen was passiert."

**Korrektes Protokoll pro Experiment:**

```
1. HYPOTHESE (vorab schriftlich)
   "TSL 3% → 2% verbessert PnL für Day-Trades in chop-Regime um ≥1%
    (N≥80 Trades), ohne max-DD >15% zu vergrößern."

2. PRÄDIKATE (was muss wahr sein = Erfolg)
   - primary: avg_pnl Δ ≥ +1.0 pp
   - guard: max_dd Δ ≤ +3 pp
   - guard: win_rate Δ ≥ -5 pp (kein Win-Rate-Kollaps)

3. DESIGN
   - Welche Variable(n)? [tsl_day_pct]
   - Range: {1.5, 2, 2.5, 3, 3.5, 4}
   - Alle anderen Variablen: fixiert auf Baseline
   - Split: walk-forward 2025-Q4→2026-Q1 (Train/Val)
   - N pro Zelle: min 80

4. DURCHFÜHRUNG
   - Seed-Log für Reproduzierbarkeit
   - Runner-Version-Tag einfrieren
   - Report automatisch generiert (keine manuelle Interpretation)

5. KONKLUSION
   - Prädikate erfüllt? JA/NEIN/TEILWEISE
   - Next Action: commit to Default | reject | follow-up experiment
   - Ergebnis ARCHIVIEREN (siehe §L Meta-Learning)

6. PRE-REGISTRATION
   - Hypothese + Prädikate vor Run speichern, nicht nachträglich
   - verhindert p-hacking und hindsight-bias
```

**Ohne dieses Protokoll:** Man findet Muster, aber oft sind es Overfits auf das Val-Set.

## NEU §K — Negative-Controls (Leak-Detektoren)

**Idee:** Variablen, die **kein** Signal enthalten dürften. Wenn sie PnL beeinflussen → Data-Leak oder Bug.

| Negative-Control | Warum erwartet = 0 Effekt | Wenn doch Effekt → |
|---|---|---|
| `msg_id_modulo_7` | Random Partitions | Leak: Reihenfolge-abhängige Features |
| `random_shuffled_regime_labels` | zerstörtes Regime-Signal | Engine nutzt Regime indirekt über Leck |
| `fixture_generated_at_timestamp` | Metadaten nicht Trading-relevant | Versehentlich als Feature extrahiert |
| `random_soft_score_noise_±2` | zufälliges Rauschen | Engine zu sensitiv an Threshold |

**Regel:** Vor jeder Optimierungs-Kampagne einmal Negative-Controls durchlaufen lassen. Falls sie Effekt zeigen → Stop, Pipeline reparieren bevor optimiert wird.

## NEU §L — Meta-Learning (Experiment-Archiv)

**Problem:** Ohne Archiv wiederholen wir Experimente, die schon gelaufen sind.

**Lösung:** `experiments.db` mit einem Row pro Run:

```sql
CREATE TABLE experiments (
  exp_id TEXT PRIMARY KEY,        -- UUID
  run_at TEXT,                    -- ISO-Timestamp
  hypothesis TEXT,                -- Freitext, pre-registered
  predicates_json TEXT,           -- primary/guard Metriken + Thresholds
  param_config_json TEXT,         -- exakter Param-Snapshot
  fixture_set TEXT,               -- Hash der verwendeten Fixtures
  runner_version TEXT,            -- Git-SHA oder Tag
  result_metrics_json TEXT,       -- alle Metriken post-hoc
  conclusion TEXT,                -- "accepted" | "rejected" | "inconclusive"
  followup_exp_id TEXT            -- Chain für Experiment-Serien
);
```

**Nutzen:**
- Duplikate werden verhindert (Param-Hash-Check)
- Experiment-Chains sichtbar ("wir haben TSL 5× getestet")
- Drift-Analyse ("im Juni war Default X, heute ist es Y, warum?")
- Reproduzierbarkeit: `exp_id` → alle Inputs rekonstruierbar

## NEU §M — Stop-Kriterien

**Anti-Pattern:** Optimierung läuft bis Burnout, aber wann genug?

**Harte Stop-Kriterien:**

1. **Convergence** — letzte 3 Experimente haben Δ avg_pnl < 0.3pp → Plateau erreicht
2. **Overfit-Signal** — Train-PnL steigt weiter, Val-PnL fällt → Stop und rollback
3. **Confidence-Interval-Breite** — CI_95 überlappt mit Baseline → nicht signifikant, Variable nicht weiter tunen
4. **Complexity-Budget** — >10 Variablen aktiv getuned → einfrieren, vor mehr Tuning Ergebnisse verifizieren
5. **Real-World-Divergenz** — Live-Performance driftet >20% von Simulation → Simulation reparieren, nicht weiter optimieren

**Soft Stop-Kriterien:** Tests grün, Code-Review bestanden, Negative-Controls clean, Meta-Archiv up-to-date.

## NEU §N — Metrics-Hierarchie (nicht alle Metriken gleich)

| Tier | Metrik | Rolle |
|---|---|---|
| **Primary** | Sharpe-Ratio (risk-adjusted) | Einzige Entscheidungs-Metrik |
| **Guard-Rails** | max_drawdown, loss_streak_max, volatility | müssen NICHT schlechter werden |
| **Diagnostisch** | per-rule hit-rate, trade-count, avg-hold-time | Interpretations-Layer, keine Optimierung |
| **Deskriptiv** | gross-pnl, trade-count-by-ticker | nur Reporting |

**Regel:** Primary-Metric optimieren, Guard-Rails als Constraints. Diagnostics schauen, aber nicht danach optimieren (sonst Goodhart's Law).

---

## Minimal-MVP-Reihenfolge (überarbeitet)

```
A. Runner-Script + Invariant-Checker        ← Phase 2a (deterministisch, kostenlos)
B. Intraday-Outcome-Attacher                 ← braucht Bars-DB
C. Metrics-Writer (Primary + Guards)         ← §N
D. Negative-Control-Suite                    ← §K, Pflicht-Gate vor Optimierung
E. Meta-Archiv-DB + Pre-Registration-UI      ← §J + §L
F. Tier-1-Sweeps (hypothesis-driven)         ← §H + §J, 5-8 Variablen
G. Walk-Forward-Harness                      ← §J
H. Tier-2-Sweeps mit Kopplungen              ← §I
I. Chart-OCR (optional)                      ← ganz am Ende
```

**Kernidee v2:** Phase 1 (Pipeline) ist fertig. Phase 2 ist nicht "Param-Sweep-Fabrik" sondern **"Disziplinierte Experiment-Fabrik"** — Hypothesen, Pre-Registration, Negative-Controls, Meta-Archiv, Stop-Kriterien. Ohne diese Disziplin optimiert man 6 Monate lang Noise und findet hinterher Live keinen Effekt.

Kimi/LLM weiterhin nirgends nötig. Pipeline bleibt deterministisch.
