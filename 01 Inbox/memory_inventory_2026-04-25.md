---
title: Memory Inventory & Wiki-Migrations-Vorschlag
type: inventory
tags: [memory, wiki, migration, housekeeping]
created: 2026-04-25
updated: 2026-04-25
---

# Memory Inventory 2026-04-25

**Quelle:** `/root/.claude/projects/-root-signal-bot/memory/` — 346 .md-Files (ohne `MEMORY.md` selbst).

**MEMORY.md:** 184 Zeilen, ~110 Pin-Einträge im Index, Limit 200.

## Cluster-Übersicht

| Cluster | Files | Hat-Wiki-MOC? | Empfehlung | Beispiel-Files |
|---|---:|---|---|---|
| **Kairos** | 20 | ❌ nein | **MOC schreiben** | `project_kairos_v1_deployed_2026_04_23.md`, `project_kairos_phase32_router_wired_2026_04_24.md`, `project_kairos_codex_prio15_fixes_2026_04_24.md` |
| **Parser_V2** | 5 | ❌ nein (Parser-MOC=Vorgänger) | **MOC schreiben** | `project_parser_v2_pattern_integration_2026_04_24.md`, `project_parser_v2_top5_rules_2026_04_24.md`, `project_parser_v2_task19_recall_uplift_2026_04_25.md` |
| **Auto-Research** | 15 | ❌ nein | **MOC schreiben** | `project_auto_research_round18r_wide_rollover_winner.md`, `project_hauptprojekt_2_auto_research_loop.md` |
| **KAPPI** | 28 | ❌ nein | **MOC schreiben** | `project_kappi_p4_0d_expanded_corpus_holdout_2026_04_22.md`, `project_kappi_p4_6_conditional_tp_winner_2026_04_22.md`, `project_kappi_p7_entry_filter_watch_2026_04_22.md` |
| **Watchdog** | 3 | ❌ nein | **MOC schreiben** | `project_watchdog_blueprint_alignment_2026_04_24.md`, `project_watchdog_restart_storm_2026_04_25.md`, `project_watchdog_hardening_2026_04_17.md` |
| **Review-Workflow** | 38 | ❌ nein | **MOC schreiben** | `feedback_complete_review_workflow.md`, `feedback_review_method_v3.md`, `project_review_bootstrap.md` |
| **Testcenter** | 13 | ❌ nein | **MOC schreiben** | `project_testcenter.md`, `project_testcenter_phase1_complete.md`, `project_testcenter_4phase_plan.md` |
| Jack-Sparo | 12 | ✅ `Jack-Sparo.md` | Bleibt (skip) | `feedback_jack_main_project_priority.md`, `project_jack_miss_analysis_04_21_22.md` |
| Halt-Up | 3 | ✅ `Halt-Up-Pattern.md` | Bleibt (skip) | `project_halt_up_autoskim_peak_tsl.md` |
| Hermes | 7 | ✅ `Hermes-Gateway.md` | Bleibt (skip) | `project_hermes_bridge_architecture.md`, `feedback_hermes_grows_with_us.md` |
| Parser (Vorgänger) | 13 | ✅ `Parser-MOC.md` | Bleibt (skip) | `project_parser_baseline_2026_04_18.md`, `project_parser_max_route_deployed_2026_04_22.md` |
| Karpathy/LLM-Wiki | ~3 | ✅ `Karpathy-LLM-Wiki.md` | Bleibt (skip) | `project_karpathy_4q_research_2026_04_23.md` |
| Ticker-Klassifikator | ~2 | ✅ `Ticker-Klassifikator-MOC.md` | Bleibt (skip) | `project_ticker_classifier.md` |
| Loop-Orchestrator | ~2 | ✅ `Loop-Orchestrator.md` | Bleibt (skip) | `project_alt_b_missed_trades_loop_2026_04_20.md` |
| User-Profile/Style/Briefing | ~43 | n/a | **Bleibt im Memory** (Runtime-Ops) | `feedback_style.md`, `feedback_telegram_status_simple_short.md`, `user_profile.md` |
| Project-Strategien (Staggered/TSL/TP/Conditional) | ~19 | (teils Halt-Up, teils Parser-MOC) | **Bleibt im Memory** (Strategie-Specs, später cross-link) | `project_staggered_entry.md`, `project_tsl_2pct_default_candidate.md` |
| Misc (Roadmap/Bugs/Sessions/Plans) | ~50+ | n/a | **Bleibt im Memory** | `project_session_wrap_*`, `project_bugs_fixed.md`, `project_next_session_plan_*` |

## Zusammenfassung

- **MOC-Kandidaten heute:** 7 (Kairos, Parser_V2, Auto-Research, KAPPI, Watchdog, Review-Workflow, Testcenter)
- **Bereits abgedeckt:** 7 (Jack-Sparo, Halt-Up, Hermes, Parser, Karpathy, Ticker-Klassifikator, Loop-Orchestrator)
- **Bleibt Runtime-Memory:** ~120 Files (User-Profile, Style-Feedback, Strategie-Specs, Session-Wraps)
- **Archivierung:** keine — alle Files unangetastet, additiv-only.

## Nach Phase B

In `00 Wiki/` wird existieren:
- `Kairos-MOC.md` (neu)
- `Parser-V2-MOC.md` (neu, ergänzt Parser-MOC)
- `Auto-Research-MOC.md` (neu)
- `KAPPI-MOC.md` (neu)
- `Watchdog-MOC.md` (neu)
- `Review-Workflow-MOC.md` (neu)
- `Testcenter-MOC.md` (neu)

In MEMORY.md (vorgeschlagen, separate Datei): Cluster-Pins werden auf 1-2 Zeilen pro Konzept reduziert mit Wiki-Verweis.
