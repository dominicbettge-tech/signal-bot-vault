---
title: Auto-Research-Loop
type: moc
tags: [auto-research, karpathy-loop, exit-optimization, signal-bot, strategy-evolution]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**Auto-Research** ist Hauptprojekt #2 (User-Direktive 2026-04-21, neben [[Jack-Sparo|Jack-Bot]]) und implementiert Karpathys "auto-research"-Pattern für Exit-Strategie-Optimierung im [[Signal-Bot-MOC|Signal-Bot]]: LLM generiert Exit-Logik-Varianten → Backtest auf Jack-Korpus → Sharpe/PnL-Gate + Look-Ahead-Bias-Check → Champion behalten → Loop. Quelle: YouTube btG5YpvPkwE (Sharbel A.). Champion 2026-04-22: **R18r wide-rollover** (Mean +18.07, Sharpe 1.86, soft 4/4, fuzz 94%) — Series CLOSED bei Saturation. Strategie-File: `auto_research/strategies/cond_defer_rollover_regime_stall.py`.

## Aktueller Stand (2026-04-25)

- **Champion:** R18r — `cond_defer_rollover_regime_stall.py` mit bypass_tsl=0.05, stall_squeeze=5.0, stall_chop=10.0, rollover w=8 r=8 ceil=16
- **Status:** R18-Serie CLOSED (Strukturelle Saturation auf n=68 Korpus)
- **Production-Wiring:** Im Worktree, FLAG default OFF, **nicht deployed live**
- **Paper-Learning:** STAGGER + Swing + R18r aktiv, R16-verdict=n Override in `rule_engine_bridge`
- **Predecessors deployed:** Breakout-Entry (2026-04-21) + ALT-C Partial Live (2026-04-23)
- **Inflation-Bias:** Late-armed TSL erscheint in Sim besser als Realität → `realism_audit.py` Pflicht

## Pipeline

```
auto_research/
  prepare.py        → lädt Jack-Entries + bars_1min → Pickle
  strategies/*.py   → einzelne Exit-Strategien (LLM-editierbare Files)
  runner.py         → Loop: propose → backtest → gate → commit
  adversarial.py    → hard/soft Stress-Tests (RS-artifact, halt-down, fake-breakout, gap-down)
  adversarial_fuzz.py → fuzz-Familien mit Schwellen ≥85%
  bootstrap_ci.py   → Walk-Forward + OOS-Splits
  results.db        → jede Generation mit Code + Metriken + Verdict
```

**Fitness-Function:** Mean-PnL auf Jack-Signal-Korpus (141 Long-Entries gefillt, n=68 Walk-Forward) statt Sharpe alone. Kombiniert mit Drawdown-Cap und Min-PnL-Preservation.

**Guards:**
- 70/30 Train/Test OOS-Split (`feedback_generalization_first_always.md`)
- Cross-Ticker-Gate ≥3 Tickers / n≥30 pro Ticker
- Look-Ahead-Bias-Check (Reverse-Split-Artefakte können Mean +1412% Unsinn produzieren)
- TSL-Simulator-Inflation-Audit (`realism_audit.py`)
- Adversarial-Fuzz Schwelle ≥85%

## R-Series-Ledger

### Predecessor (R15-R17)

| Round | Champion | Mean | Sharpe | Notiz |
|---|---|---|---|---|
| R15b | byp=8.02/tsl=0.1 | +11.22 | n/a | 0 losses |
| R17c | regime-tight | +11.34 | 1.14 | sharpe-pass |

### R18-Series (Detail-Ledger)

| Round | Axis | Mean | Result |
|---|---|---|---|
| R18f | arm_defer_until_tier | +12.92 | shipped (baseline) |
| R18h | CA40 honest | +13.66 | shipped |
| R18j | tp=byp=14 | +16.66 | shipped |
| R18k | stall_arm | +16.88 | shipped |
| R18l | bypass_tsl=0.05 | +16.93 | shipped |
| R18m | weakCut(bar=25, peak=2) | +17.03 | shipped |
| R18n | sub-bypass rollover | +18.00 | shipped |
| R18o | widened rollover standalone | null | axis closed |
| R18p | volume vol-ratio | null | axis closed |
| R18q | regime-aware stall_tsl | +18.07 | shipped |
| **R18r** | **R18q + wide rollover** | **+18.07** | **CHAMPION (defensive uplift)** |
| R18s-prog | progressive bypass trail | null | axis closed |
| R18s-sustain | sustain-widening | null | unmöglich (kein Sustain pre-exit) |
| R18s-vwap | VWAP-cross-down | null | regression -5.4pp |
| R18s-scaleout | partial-at-parTSL + runner | null | dip_rally hits dip first |

### Saturation-Signal

Per-round Mean-Uplift abnehmend: R18j +3.00pp → R18n +0.97pp → R18q +0.07pp → R18r 0.00pp (defensiv only) → R18s* 0.00pp.

**Strukturelle Saturation auf n=68 Korpus.** Post-Exit-Upside +2681pp ist unreichbar unter Single-Exit-Semantik (28/51 parTSL-Exits sind dip_rally — Trail-Widening trifft Dip vor Rally).

## Was R19+ braucht

1. **Korpus-Expansion (n>100)** — mehr Trade-Shape-Variety
2. **Re-Entry-Semantik** — State-Machine post-exit, Bodendetektion, zweiter Exit (10× Komplexität, Framework-Redesign)
3. **Entry-Side-Optimierung** — Fills selber tunen (aktuell fixed input)
4. **Kelly-Position-Sizing** für Monster-Shape-Entries (orthogonal zur Exit-Axis)

## Komponenten

- **`auto_research/strategies/`** — pluggable Strategy-Files (cond_defer_rollover_regime_stall.py = Champion)
- **`auto_research/agents/`** — LLM-Agents-Wrapper
- **`peak_lock_exit_engine.py`** — root-Module, in Bot integriert
- **`r18r_exit_engine.py`** — root-Module, R18r-Inference-Engine
- **`scripts/full_replay_6w_max.py`** — 635 Jack-Msgs Replay (R18r_WIDE +$1044 vs TIGHT −$233)

## Verwandte Erkenntnisse

- **Karpathy 4Q-Research 2026-04-23:** Q1 cond_break 7 hits, Q2 Σ+508% (inflation), Q3 r18r bestätigt, Q4 skip_sub_1_penny +15.27pp
- **ALT-C Primary Objective:** Profit Max All-Ticker (invent→sim→cross→memorize→propose)
- **TSL-Simulator-Inflation-Bias:** Late-armed TSL appears better in sim than reality

## Memory-Detail-Files

- `/root/.claude/projects/-root-signal-bot/memory/project_hauptprojekt_2_auto_research_loop.md` — Konzept + Architektur-Skizze
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_day1_winner.md` — R15b
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round17c_regime_tight.md` — R17c
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18_cond_safety.md` — R18 Safety
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18f_cond_defer.md` — R18f
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18h_ca40_honest.md` — R18h
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18i_caw_winner.md` — R18i
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18j_caw14_winner.md` — R18j
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18k_stall_winner.md` — R18k
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18l_tight_byp.md` — R18l
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18m_weakcut_winner.md` — R18m
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18n_rollover_winner.md` — R18n
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18q_regime_stall_winner.md` — R18q
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18r_wide_rollover_winner.md` — **R18r CHAMPION**
- `/root/.claude/projects/-root-signal-bot/memory/project_auto_research_round18s_saturation_report.md` — Saturation
- `/root/.claude/projects/-root-signal-bot/memory/project_r18r_production_wiring_2026_04_22.md` — Prod-Wiring (FLAG OFF)
- `/root/.claude/projects/-root-signal-bot/memory/project_paper_learning_mode_flags_2026_04_22.md` — Paper-Learning
- `/root/.claude/projects/-root-signal-bot/memory/project_breakout_entry_deployed_2026_04_21.md` — Predecessor Breakout-Entry
- `/root/.claude/projects/-root-signal-bot/memory/project_alt_c_deployed_2026_04_23.md` — ALT-C Partial Live
- `/root/.claude/projects/-root-signal-bot/memory/project_full_replay_6w_findings_2026_04_22.md` — 6W-Replay
- `/root/.claude/projects/-root-signal-bot/memory/project_karpathy_4q_research_2026_04_23.md` — 4Q-Research
- `/root/.claude/projects/-root-signal-bot/memory/feedback_tsl_simulator_inflation_bias.md` — Sim-Inflation-Lesson

## Related

- [[Signal-Bot-MOC]] — Container-Bot
- [[Jack-Sparo]] — Signal-Quelle
- [[Kairos-MOC]] — Schwester-Pipeline für Entry-Optimierung
- [[Karpathy-LLM-Wiki]] — Pattern-Quelle
- [[Halt-Up-Pattern]] — eines der Exit-Pattern
- [[KAPPI-MOC]] — Schwester-Loop (TP-Optimierung)

## Externe Referenzen

- YouTube btG5YpvPkwE — Sharbel A. Auto-Research-Tutorial (2026-04-21, 18:55 min)
- Karpathy auto-research repo — referenced in video description
