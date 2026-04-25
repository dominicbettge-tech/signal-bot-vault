---
title: Kairos
type: moc
tags: [kairos, entry-strategy, shadow-mode, signal-bot]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**Kairos** ist der Entry-Strategy-Router des [[Signal-Bot-MOC|Signal-Bots]]. Vergleicht für jedes Jack-Signal mehrere Entry-Strategien (Stagger, Breakout, Pullback) gegen reale Preisverläufe und wählt per Score-Engine die beste. Ziel: max Upside bei min Drawdown — Breakout-Strategie hat sich als Champion (92-95% Win-Rate gegen Stagger) etabliert. Läuft seit 2026-04-23 als systemd-Service `signal-kairos` im Shadow-Mode parallel zum Bot, ohne Order-Impact (Live-Switch flag-gated).

## Aktueller Stand (2026-04-25)

- **Service:** `signal-kairos.service` ACTIVE (Shadow-Mode, since 2026-04-23 09:52 CEST)
- **Bot-Wiring:** `main.py` HARD-SWITCH `choose_entry_strategy()` vor STAGGER_ENABLED
- **Flags:** `KAIROS_LIVE_ENABLED=true`, `KAIROS_SHADOW_MODE=true` — Shadow-Flag dominiert, Heartbeat-Mode bleibt "shadow"; Live-Schalter erst nach Phase-4-OOS-Validation aktiv
- **Tests:** 115/115 grün (Phase-2/3-Analytics-Stand)
- **Decision:** Breakout dominiert Pullback (B-Score 0.45 vs 0.19, 2.4×) UND Stagger (94-100% global)
- **Pending:** Bot-Restart nach .env-Flip auf Live, dann Shadow-Compare-Telemetry-Auswertung

## Komponenten

- **`entry_router.py`** — Default-Strategy=breakout, dispatched Calls von `signal_manager.py`
- **`entry_quality.py`** — Score-Engine: `score = upside − 0.5 × price_advantage_ratio − stagger_delay_penalty`
- **`choose_entry_strategy()`** in `main.py` — schaltet Strategie pro Signal um
- **Shadow-Dict** + `live_shadow.py` — paralleler Vergleich ohne Order-Impact, in `kairos_decision_snapshots`-Tabelle persistiert
- **Pattern-Discovery (P2.5+2.6)** — Lane-1+2-Karpathy-Loop, Pattern-Triggers in `kairos_pattern_triggers`
- **RL-Stack (P2.x)** — 7 Module + 2 Tabellen, 10 Flags OFF (shadow-only)
- **Hardening:** Ref-Time-Dedup, Orphan-Gate, Dispatcher, Breakout-Fallback

## Phasen-Historie

| Datum | Phase | Inhalt |
|---|---|---|
| 2026-04-23 | KAIROS-BOT PLAN | 11 Phasen P0-P5.5, ~92h raw, External-Review |
| 2026-04-23 09:52 | v1 DEPLOYED | `signal-kairos.service`, Hooks in `signal_manager.py`+`position_monitor.py`, Shadow-Mode |
| 2026-04-23 | REVIEW-IMPL | 7 items, 18/18 Tests — Realistic-Exit/Regime-Tagger/Dynamic-Slip/Quality-Score |
| 2026-04-23 20:43 | RL-STACK | 7 Module + 2 Tabellen, 20/20 Tests, 10 Flags OFF |
| 2026-04-23 21:00 | P2.5+P2.6 | Pattern-Discovery + Karpathy-Loop, 36/36 Tests |
| 2026-04-23 21:30 | P2.6 GUARDS | DebugLog+Overfit+TimeSplit+Regime, 64/64 Tests |
| 2026-04-23 22:30 | HARDENING | Ref-Time-Dedup + Orphan-Gate + Dispatcher + Breakout-Fallback, 26/26 Tests |
| 2026-04-23 | ENTRY-COMPARE PHASE-2 | SQL + Regime + Proposal-Engine + Decision-Layer + Dashboard, 18/18 Tests |
| 2026-04-23 23:40 | PHASE-2 QUALITY | `entry_quality.py` ChatGPT-Spec, n=18 Breakout 89%, Stagger-Delay 22.2min = Edge-Killer |
| 2026-04-24 00:15 | PHASE-2.1 SCORE | `determine_best_entry` jetzt score-based, Breakout 86% (n=22), avg Score 5× höher |
| 2026-04-23 | PHASE-2.2 PRICE-ADV | Score += −0.5×price_advantage_ratio, Breakout 19→21/22 (95.5%) |
| 2026-04-23 | PHASE-3.1 SWEEP | Thresholds 3/5/7/10/15% — KEIN Flip-Punkt, Stagger gewinnt nirgends |
| 2026-04-23 | PHASE-3 PULLBACK | Breakout dominiert Pullback (B 0.45 vs 0.19, 2.4×) |
| 2026-04-23 | PHASE-3.2 FULL-CORPUS | n=54 polygon Breakout 92.6%, `entry_router.py` shipped (nicht in main.py), Shadow-dict, 46/46 Tests |
| 2026-04-24 | PHASE-3.2 ROUTER-WIRED | `main.py` HARD-SWITCH, `choose_entry_strategy()`, shadow_compare, 85/85 Tests |
| 2026-04-24 | CODEX PRIO 1-5 FIXES | Fill-Match/SL-Dup/Cancel-Race/Router-Gate/Shadow-Integrity, 85/85 Tests + 3 Smoke |
| 2026-04-24 | PHASE-2/3 ANALYTICS | `report_builder` + `router_features` + `auto_router` + `build_daily_report`, 115/115 Tests, zero live-impact |

## Memory-Detail-Files

- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_implementation_plan_2026_04_23.md` — 11-Phasen-Masterplan P0-P5.5
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_v1_deployed_2026_04_23.md` — v1 Service-Deploy
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_external_review_2026_04_23.md` — External Review
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_review_implementation_2026_04_23.md` — 7 items aus Review umgesetzt
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_rl_stack_deployed_2026_04_23.md` — RL-Stack
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_p25_p26_shipped_2026_04_23.md` — Pattern-Discovery
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_p26_guards_2026_04_23.md` — Guard-Layer
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_hardening_2026_04_23.md` — Hardening-Wave
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_entry_compare_phase2_2026_04_23.md` — Phase-2 Compare
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase2_quality_engine_2026_04_23.md` — Quality-Engine
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase21_score_based_2026_04_23.md` — Score-based Engine
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase22_price_adv_fixes_2026_04_23.md` — Price-Advantage-Fix
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase31_threshold_sweep_2026_04_23.md` — Threshold-Sweep
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase3_pullback_analysis_2026_04_23.md` — Pullback-Analyse
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase32_full_corpus_shadow_2026_04_23.md` — Full-Corpus n=54
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase32_router_wired_2026_04_24.md` — main.py-Wiring
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_codex_prio15_fixes_2026_04_24.md` — Codex-Reviews
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_phase23_analytics_2026_04_24.md` — Analytics-Layer
- `/root/.claude/projects/-root-signal-bot/memory/project_kairos_paper_shadow_codex_handoff_2026_04_24.md` — Codex-Handoff
- `/root/.claude/projects/-root-signal-bot/memory/feedback_kairos_chatgpt_export_json_schema.md` — Export-Schema (REGEL 9)

## Related

- [[Signal-Bot-MOC]] — Container-Bot
- [[Jack-Sparo]] — Signal-Quelle
- [[Parser-MOC]] / [[Parser-V2-MOC]] — liefert Signale an Kairos
- [[Halt-Up-Pattern]] — eines der getesteten Patterns
- [[Auto-Research-MOC]] — Schwester-Pipeline für Exit-Optimierung
- [[Watchdog-MOC]] — überwacht `signal-kairos.service`
