---
title: KAPPI
type: moc
tags: [kappi, karpathy-loop, tp-optimization, signal-bot, autonomous-research]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**KAPPI** (Kappi-Test) ist der 10-Wochen-autonome Karpathy-Loop für TP-Strategie-Discovery im [[Signal-Bot-MOC|Signal-Bot]] — Schwester-Projekt zu [[Auto-Research-MOC]] (Exit-Optimierung), aber TP-Ladder + Entry-Filter + Meta-Layer im Fokus. Worktree-isoliert in `auto-research-max/`, Namespace `kappi_test/`, Max-Account-only (claude -p CLI, keine API-Kosten). Champion 2026-04-22: **TP_HARD_THEN_HOLD(20)** — Train +12.84% / Hold +12.48% / WR 85% / 59 von 269 Combo-Survivors. Phasen P1-P8 zum großen Teil abgeschlossen.

## Aktueller Stand (2026-04-25)

- **Status:** P6 Round CLOSED, P7 Entry-Filter PAUSED, P8 BB-Exhaustion + Session-TP NULL
- **Champion:** `tp_hard_then_hold(tp_pct=20.0)` — shadow-shipped, statisch
- **Realism-Audit:** P4.4 framework live (`shadow_fires` DB + BLOCK>+2pp/WATCH Policy)
- **P4.6 Lesson:** `cond(f5≥12)+15.76%` war leaky (9/84 tp30-fires im 0-5min) → static gewählt, conditional skipped
- **P7 Entry-Filter:** range<2% feature passes per-trade-Δ (+6.60pp) ABER kostet Total-Profit (-27.8pp) → WATCH
- **Korpus:** n=84 expanded (2 live + 66 sim + 16 parsed_signal touch-validated), 269 Combos getestet

## Invarianten

1. Paper-only. `TRADING_MODE=live` tabu.
2. Production-Bot auf main-Branch unangetastet. Merge nur via User-Gate.
3. Freeze-Resume: alles SQLite-persistent, Checkpoint pro Generation.
4. **4-Gate-Pflicht** vor Promotion (Adv + WF + OOS + Cross-Ticker ≥3/n≥30).
5. Rule-Semantik-Tabu: R16/R17 (Skip-Rules) dürfen LLM nie wegoptimieren.
6. Top-3-Trim: jede Metrik mit/ohne Top-3-Winner berichtet.
7. Nach jedem Task: Memory + Telegram-Ping. Keine Ausnahme.

## Phasen-Struktur

### Phase 1 — Fill-Rate & Exit-Hardening (Woche 1-2)

| Task | Inhalt |
|---|---|
| P1.1 | Jack-Dip-Ladder (descending LIMITs) |
| P1.2 | R6 TP-Ladder Default 50/30/20 @+5/+10/+20% (Evidence: 2.64× ABOS) |
| P1.3 | R1 Conditional-Offset +2% Range-Offset (6 Cases) |
| P1.4 | R3 Distress-TSL + Caution-Feature-Tagger |
| P1.5 | R15 Monster-Detector (score≥0.40 + RTH + Size×2 + TP-Ladder) |
| P1.6 | P0.2 Dilution-Hard-Reject scharf |

### Phase 2 — Karpathy-Full-Build (Woche 2-3)

| Task | Inhalt |
|---|---|
| P2.1 | LLM-Proposer-Agent (`claude -p` Max-Account, JSON→strategy-files) |
| P2.2 | program.md mit R1-R17 Seed + Jack-Bias-Facts |
| P2.3 | Auto-Promote-Trigger (fitness > best×1.02 ∧ 4/4 Gates ∧ Holdout) |
| P2.4 | Temporal-Holdout (letzte 14 Tage versiegelt) |
| P2.5 | Daemon `kappi-research.service` + Checkpoint + Memory-Append |

### Phase 3 — Discovery (Woche 3-5)

E1-E5 Entry-Family, N1-N3 Multi-Timeframe-Confirm + VWAP-Anchor + SPY-Correlation, Multi-Agent 5-Agent-Fanout + Genetic-Crossover.

### Phase 4 — Meta-Layer (Woche 5-8)

P4.0d Expanded-Corpus-Holdout, P4.1 Regime-Layer, P4.2 Kelly-Sizing, P4.3 Ensemble-Paper, **P4.4 Realism-Audit** (Sim-Inflation-Schutz), P4.5 Dark-Corpus 2683 Jack-Msgs.

### Phase 5-8 — Validation, Pareto, Round-Closes

P5 Final-Stack-Audit, P6 ATR/VWAP/VolDecay/TimeDecay/DDCap (alle NULL), P7 Entry-Filter (PAUSED on live-corpus n=2), P8 BB-Exhaustion + Session-TP (NULL).

## Champion-Ladder (P4.0d Expanded n=84)

| # | Family | Params | Train | Hold | HoldWR |
|---|---|---|---|---|---|
| 1 | tp_hard_then_hold | tp_pct=30.0 | +14.23% | +15.37% | 76% |
| 2 | tp_hard_then_hold | tp_pct=25.0 | +13.86% | +14.85% | 82% |
| **3** | **tp_hard_then_hold** | **tp_pct=20.0** | **+13.44%** | **+13.40%** | **88% (CHAMPION)** |
| 4 | tp_hard_then_hold | tp_pct=15.0 | +12.23% | +10.05% | 88% |
| 5 | time_stop | max_bars_no_peak=20 | +9.12% | +8.04% | 88% |

**Walk-Forward Aggregat (3 Folds):** tp=25 mean_test +15.58% (best), tp=30 schmalste Range (consistent).

**LOO Ticker-Robustness:** TP_HARD_20 65/65 LOO-survivors, worst Δhold -0.41% — generalisiert.

## Family-Pass-Rate (n=84)

| Family | Survivors |
|---|---|
| tsl_after_profit_plus_tp | 25 |
| tp_ladder | 12 |
| tsl_plus_tp | 10 |
| tp_hard_then_hold | 7 |
| time_stop | 2 |
| tsl_after_profit | 2 |
| momentum_fade | 1 |

## Critical Lessons

- **Per-Trade-Δ ≠ Total-Profit-Δ** (P7-Lesson) — Filter kann per-trade quality verbessern und Total-$ kaputt machen
- **Leakage hides in conditional logic** (P4.6) — `cond(f5≥12)` fired 9/84 im 0-5min-Fenster → fake +15.76%
- **Live-Corpus-Thinness blockiert Entry-Filter** — n_live=2, Filter "lernt" essentiell "skip live"
- **Touch-Check rettet Baseline** — 52/141 parsed_signals never-touched → ohne Touch-Check +1200% inflation
- **TSL-Familien sind nicht tot** — n=84 zeigt 25 tsl_after_profit_plus_tp Combos (war 0 bei n=71)

## Namespace-Layout

```
kappi_test/
├── strategies/        # kappi_<rule>_<variant>.py
├── agents/            # llm_proposer.py, orchestrator.py
├── filters/           # kappi_p02_dilution.py
├── sizer/             # kappi_kelly.py
├── holdout/           # temporal_holdout.json (14d sealed)
├── memory/            # pX_Y_<topic>_2026-MM-DD.md
├── logs/              # runner-loop-N.log
├── checkpoints/       # progress.json
└── results/           # kappi_generations DB
```

## Memory-Detail-Files

- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_test_masterplan_2026_04_22.md` — 10-Wochen-Plan
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p1_1_jack_dip_ladder_2026_04_22.md` — P1.1
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p1_2_r6_tp_ladder_2026_04_22.md` — P1.2
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p1_3_r1_conditional_offset_2026_04_22.md` — P1.3
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p1_4_r3_distress_tsl_2026_04_22.md` — P1.4
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p1_5_r15_monster_detector_2026_04_22.md` — P1.5
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p1_6_p0_2_dilution_sharp_2026_04_22.md` — P1.6
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p2_1_llm_proposer_2026_04_22.md` — P2.1
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p2_2_program_md_expansion_2026_04_22.md` — P2.2
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p2_3_auto_promote_2026_04_22.md` — P2.3
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p2_4_temporal_holdout_2026_04_22.md` — P2.4
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p2_5_daemon_real_eval_2026_04_22.md` — P2.5
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p3_2_n1_mtf_confirm_2026_04_22.md` — P3.2
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p3_3_3_4_n2_n3_2026_04_22.md` — P3.3-3.4
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p4_0a_n1_shadow_ship_2026_04_22.md` — P4.0a
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p4_0b_champion_holdout_audit_2026_04_22.md` — P4.0b
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p4_0d_expanded_corpus_holdout_2026_04_22.md` — **P4.0d Champion-Audit n=84**
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p4_4_realism_audit_framework_2026_04_22.md` — Realism-Audit Framework
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p4_6_conditional_tp_winner_2026_04_22.md` — P4.6 Leakage-Lesson
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p4_6_tp_hard_30_shadow_wire_2026_04_22.md` — TP_HARD_30 Shadow
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p5_1_final_stack_audit_2026_04_22.md` — P5.1
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p5_validation_burst_2026_04_22.md` — P5 Validation
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p6_3_scale_out_watch_2026_04_22.md` — P6.3
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p6_atr_null_result_2026_04_22.md` — P6 ATR
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p6_round_closed_2026_04_22.md` — P6 CLOSED
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p7_entry_filter_watch_2026_04_22.md` — P7 Entry-Filter (WATCH)
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p8_2_bb_exhaustion_null_2026_04_22.md` — P8.2 BB-NULL
- `/root/.claude/projects/-root-signal-bot/memory/project_kappi_p8_session_tp_null_2026_04_22.md` — P8 Session-NULL

## Related

- [[Signal-Bot-MOC]] — Container-Bot
- [[Auto-Research-MOC]] — Schwester-Loop (Exit-Optimierung)
- [[Karpathy-LLM-Wiki]] — Pattern-Quelle (auto-research)
- [[Jack-Sparo]] — Korpus-Quelle (n=84 Fills)
- [[Kairos-MOC]] — Schwester-Pipeline (Entry-Strategy)

## Externe Referenzen

- YouTube btG5YpvPkwE — Sharbel A. Auto-Research-Tutorial
- Karpathy auto-research repo (referenced in video)
