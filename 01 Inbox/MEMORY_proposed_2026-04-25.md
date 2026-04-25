# Memory Index — VORSCHLAG (Phase C, 2026-04-25)

> ⚠️ Dies ist ein VORSCHLAG für die nächste MEMORY.md-Version.
> Die produktive Datei `/root/.claude/projects/-root-signal-bot/memory/MEMORY.md` bleibt UNANGETASTET.
> User entscheidet welche Cluster-Refs übernommen werden.

---

## REGELN -1 bis 9 (UNVERÄNDERT)

> ⚠️⚠️⚠️ **REGEL -1**: `grounded-decisions` 5-Step bei JEDER Empfehlung → `feedback_grounded_decisions_skill.md`
> ⚠️⚠️⚠️ **REGEL 0**: Skills SICHTBAR anwenden → `feedback_skill_visibility_enforcement.md`
> ⚠️⚠️⚠️ **REGEL 1**: Daily Journal `05 Daily Notes/YYYY-MM-DD.md` → `feedback_daily_journal_mandatory.md`
> ⚠️⚠️⚠️ **REGEL 2**: Tiefes Nachdenken (Prior+Precedents+Alt+Edge) → `feedback_deep_thinking_always.md`
> ⚠️⚠️⚠️ **REGEL 3 (Alt-B 2026-04-20)**: Durable Knowledge → `00 Wiki/` FIRST, Memory nur Runtime-Ops → `feedback_wiki_first_for_durable_knowledge.md`
> ⚠️⚠️⚠️ **REGEL 4 (Telegram-Style 2026-04-20)**: Status-Pings max 3 Sätze, einfaches Deutsch, kein Jargon → `feedback_telegram_status_simple_short.md`
> ⚠️⚠️⚠️ **REGEL 5 (Config-Refactor 2026-04-23)**: Nach config.py-Änderungen python3-Import-Check ALLER consumers vor Restart — sonst Silent-Parser-Fail → `feedback_config_refactor_verify_imports.md`
> ⚠️⚠️⚠️ **REGEL 6 (IBKR Min-Tick 2026-04-23)**: Preise ≥$1→round(,2), <$1→round(,4). `_tick_round()` nutzen. → `feedback_ibkr_tick_size_rule.md`
> ⚠️⚠️⚠️ **REGEL 7 (ChatGPT-Co-Design 2026-04-23 22:05)**: Code-Bauen NUR nach ChatGPT-Absprache. Memory/DB-Saves autonom OK. → `feedback_chatgpt_co_design_build_rule.md`
> ⚠️⚠️⚠️ **REGEL 8 (2026-04-23 22:37)**: ChatGPT-Deliveries/Files IMMER per Telegram senden, nie „Web-UI"-Hinweis → `feedback_chatgpt_always_via_telegram.md`
> ⚠️⚠️⚠️ **REGEL 9 (2026-04-24)**: KAIROS→ChatGPT-Exports IMMER als strukturiertes JSON → `feedback_kairos_chatgpt_export_json_schema.md`

---

## Wiki-MOC-Refs (ersetzen Cluster-Pins)

> ⚠️⚠️⚠️ **KAIROS** Entry-Strategy-Router, signal-kairos.service shadow-mode, Breakout-Champion 92-95% → `00 Wiki/Kairos-MOC.md`
> ⚠️⚠️⚠️ **KAIROS LATEST** Phase-2/3 Analytics, 115/115 Tests, .env-Flip pending → `project_kairos_phase23_analytics_2026_04_24.md`

> ⚠️⚠️⚠️ **PARSER_V2** 3-Layer (Pattern/Intent/Regex) + Hardfix A-F + Setup-Trigger-Engine, recall_b 73% → `00 Wiki/Parser-V2-MOC.md`
> ⚠️⚠️⚠️ **PARSER_V2 LATEST** Task 19 Splitter-Fix + Hardfix E/F, recall_b 37→73% → `project_parser_v2_task19_recall_uplift_2026_04_25.md`

> ⚠️⚠️⚠️ **AUTO-RESEARCH** Karpathy-Loop für Exit-Optimierung, R18r Champion +18.07/Sh 1.86, Series CLOSED bei Saturation → `00 Wiki/Auto-Research-MOC.md`
> ⚠️⚠️⚠️ **AUTO-RESEARCH LATEST** R18r wide-rollover shipped, Saturation auf n=68, R19+ braucht n>100 → `project_auto_research_round18s_saturation_report.md`

> ⚠️⚠️⚠️ **KAPPI** 10-Wochen Karpathy-Loop für TP-Discovery, Champion TP_HARD_THEN_HOLD(20) shipped → `00 Wiki/KAPPI-MOC.md`
> ⚠️⚠️⚠️ **KAPPI LATEST** P6 ROUND CLOSED (alle NULL), P7 Entry-Filter PAUSED auf Live-Corpus n=2 → `project_kappi_p6_round_closed_2026_04_22.md`

> ⚠️⚠️⚠️ **WATCHDOG** Observability-Triade (Bot+Position+Kairos-Heartbeat), read-only, Restart-Storm-RCA pending fixes → `00 Wiki/Watchdog-MOC.md`
> ⚠️⚠️⚠️ **WATCHDOG LATEST** Restart-Storm 2026-04-25 06:39, 3 Bugs (timeout/lock/restart_all.sh) → `project_watchdog_restart_storm_2026_04_25.md`

> ⚠️⚠️⚠️ **REVIEW-WORKFLOW** 7-Phasen End-to-End (Bootstrap→Verdict→Edge→Sim→Rule→Commit→Report), 6 Verdict-Codes b/e/x/s/w/n → `00 Wiki/Review-Workflow-MOC.md`
> ⚠️⚠️⚠️ **REVIEW-WORKFLOW LATEST** Bootstrap-Pflicht-Ablauf, save_verdict.py SOFORT, Self-Eval ≥50 → `project_review_bootstrap.md`

> ⚠️⚠️⚠️ **TESTCENTER** Phase-1 komplett (7 Module/132 Tests), Phase-A Runner+Fast-Pass-UI im Build, 21 R-Hypothesen → `00 Wiki/Testcenter-MOC.md`
> ⚠️⚠️⚠️ **TESTCENTER LATEST** Phase-A Clean-Baseline gesetzt, Phase-B Reviews-Vorrang aktiv → `project_testcenter_phase_a_clean_baseline.md`

---

## Bestehende Wiki-MOCs (Pointer-Refs, kein Bloat)

> ⚠️⚠️ **JACK = HAUPTPROJEKT** alles andere sekundär → `00 Wiki/Jack-Sparo.md` + `feedback_jack_main_project_priority.md`
> ⚠️⚠️ **HALT-UP** Grid-Winner Mean +39.38% Win 94.3% → `00 Wiki/Halt-Up-Pattern.md` + `project_halt_up_autoskim_peak_tsl.md`
> ⚠️⚠️ **HERMES** Telegram-Bridge → `00 Wiki/Hermes-Gateway.md` + `feedback_auto_fix_hermes_communication.md`
> ⚠️⚠️ **PARSER (V1)** Claude-LLM-Cascade → `00 Wiki/Parser-MOC.md`
> ⚠️⚠️ **KARPATHY-WIKI** Pattern-Quelle → `00 Wiki/Karpathy-LLM-Wiki.md`
> ⚠️⚠️ **TICKER-KLASSIFIKATOR** → `00 Wiki/Ticker-Klassifikator-MOC.md`
> ⚠️⚠️ **LOOP-ORCHESTRATOR** → `00 Wiki/Loop-Orchestrator.md`
> ⚠️⚠️ **SIGNAL-BOT** Container-MOC → `00 Wiki/Signal-Bot-MOC.md`
> ⚠️⚠️ **IBKR-PAPER-TRADING** → `00 Wiki/IBKR-Paper-Trading.md`

---

## Runtime-Ops & Behavior-Pins (BLEIBT — kein MOC)

> ⚠️⚠️⚠️ **MONITOR-ERRORS NIE IGNORIEREN** jeder Loop-Error ist kritisch → `feedback_never_dismiss_monitor_errors.md`
> ⚠️⚠️ **REVIEW-BOOTSTRAP** vor erstem Verdict → `project_review_bootstrap.md`
> ⚠️⚠️ **USER-CURATES-FIRST** → `feedback_user_curates_messages_first.md`
> ⚠️⚠️ **HYBRID-DESIGN** 6-Schritt → `feedback_hybrid_design_workflow.md`
> ⚠️⚠️ **UI-FIRST ≥50 Tasks** → `feedback_ui_first_efficiency_trigger.md`
> ⚠️⚠️ **CASE ≠ CORPUS** (n≤3 Hyp, n≥30 Default) → `feedback_case_vs_corpus_evidence.md`
> ⚠️⚠️⚠️ **ZAHLEN NUR AUS QUELLE** → `feedback_post_compaction_db_reread.md`
> ⚠️⚠️⚠️ **GENERALISIERUNG-FIRST** (OOS + Cross-Ticker ≥3 + n≥30) → `feedback_generalization_first_always.md`
> ⚠️ **AUTONOMER REPORT** 2-3 Sätze Value → `feedback_autonomous_work_report_format.md`
> ⚠️⚠️⚠️ **REVIEW-TABELLE + PREIS-ZUR-UHRZEIT** → `feedback_review_table_with_price_at_time.md`
> ⚠️⚠️ **CONDITIONAL-TRIGGER = b** → `feedback_conditional_trigger_is_buy.md`
> ⚠️⚠️ **JACK-NARRATIVE ≠ REALITY** → `feedback_jack_narrative_vs_price_reality.md`
> ⚠️⚠️⚠️ **ALLES TABELLE** → `feedback_always_table_format.md`
> ⚠️⚠️ **USER SETZT TEMPO** → `feedback_user_paces_review.md`
> ⚠️⚠️⚠️ **SIMULIEREN STATT FRAGEN** → `feedback_simulate_before_asking.md`
> ⚠️⚠️⚠️ **AUTO-QUEUE JEDER TICKER** → `feedback_auto_queue_every_pasted_ticker.md`
> ⚠️⚠️⚠️ **NIGHT-SIM = VOLLE DB-HISTORIE** → `feedback_sim_uses_full_db_history.md`
> ⚠️⚠️⚠️ **PRICE-RANGE-TICKER-DISAMBIG** → `feedback_price_range_ticker_disambiguation.md`
> ⚠️⚠️⚠️ **ZEIT × 7-10** → `feedback_time_estimates_7x_multiplier.md`
> ⚠️⚠️⚠️ **FEATURE IN EINEM SHOT** → `feedback_feature_completeness_first_pass.md`
> ⚠️⚠️⚠️ **NIGHT_QUEUE SEQUENZIELL** → `feedback_night_queue_sequential_execution.md`
> ⚠️⚠️ **MAX-ACCOUNT, NIE API-KOSTEN** → `feedback_max_account_no_api_billing.md`
> ⚠️⚠️⚠️ **NIE WIEDER NACH API FRAGEN** → `feedback_never_ask_about_api.md`
> ⚠️⚠️⚠️ **PARSER-MAX-ROUTE LIVE 2026-04-22** `claude -p` subprocess, OAuth → `project_parser_max_route_deployed_2026_04_22.md`
> ⚠️⚠️⚠️ **2-MIN-IDLE → AUTO-CONTINUE** → `feedback_autonomous_continue_after_2min.md`
> ⚠️⚠️ **VERDICT-GLOSSAR VOR METRIKEN** → `feedback_verdict_glossary_before_metrics.md`
> ⚠️⚠️⚠️ **TRIM-TOP-3 PFLICHT** → `feedback_trim_top3_mandatory_in_sims.md`
> ⚠️⚠️⚠️ **SIM-DB-ROUTING** (polygon 272 Tickers primary) → `feedback_sim_script_db_routing_audit.md`
> ⚠️⚠️ **DELEGATE-TO-HERMES** → `feedback_delegate_to_hermes.md`
> ⚠️⚠️ **HERMES-MITWACHSEN** (8-Punkt-Check) → `feedback_hermes_grows_with_us.md`
> ⚠️⚠️⚠️ **HERMES-LESSONS** LLM proposes / gate decides → `feedback_hermes_lessons_self_eval_trap.md`
> ⚠️⚠️⚠️ **PARSED_SIGNALS = BATCH** (stale 2026-04-06) → `feedback_parsed_signals_is_batch_snapshot.md`
> ⚠️⚠️⚠️ **DB-PATH: data/ vs flat** → `reference_db_path_map_2026-04-20.md`
> ⚠️⚠️⚠️ **COUNT-CLAIMS BRAUCHEN ZEITRAUM** → `feedback_count_claims_need_scope.md`
> ⚠️ **YT-TRANSKRIPT: notegpt.io** → `feedback_youtube_transcript_prefer_scrapers.md`
> ⚠️⚠️⚠️ **UNIVERSAL RULES, NICHT EINZELFALL** → `feedback_universal_rules_not_per_trade.md`
> ⚠️⚠️⚠️ **PROFIT-LOCKS JACK-UNABHÄNGIG** (3% Trailing-SL) → `feedback_profit_locks_jack_independent.md`
> ⚠️⚠️⚠️ **HERMES SELBST-FIXEN** → `feedback_auto_fix_hermes_communication.md`
> ⚠️⚠️⚠️ **IST-ZUSTAND PRÜFEN VOR ÄNDERUNG** → `feedback_check_state_before_proposing.md`
> ⚠️⚠️⚠️ **PIPELINE-IMPACT-TRACE vor Layer-Änderung** → `feedback_trace_full_pipeline_before_layer_change.md`
> ⚠️⚠️⚠️ **TSL-SIMULATOR-INFLATION-BIAS** → `feedback_tsl_simulator_inflation_bias.md`
> ⚠️⚠️⚠️ **ALT-C PRIMARY OBJECTIVE = PROFIT MAX ALL-TICKER** → `project_alt_c_primary_objective_profit_max.md`

---

## Aktuelle Tactical-Pins (kurzlebig, möglicherweise nach 2-4 Wochen entfernen)

> ⚠️⚠️⚠️ **RANGE+SUPPORT UNLOCK 2026-04-24** Setup-Marker `range_support_override`, Trigger-Rescue, Mirror in paper_trader → `project_range_support_unlock_2026_04_24.md`
> ⚠️⚠️ **PAPER-REPORT SHADOW+LEARNING 2026-04-24** Shadow-Performance + Learning-Insights im Daily-Report → `project_paper_report_shadow_section_2026_04_24.md`
> ⚠️⚠️⚠️ **DEDUP EMPTY-TICKER FIX 2026-04-22** MIRA-Miss RCA in safety.py → `project_dedup_empty_ticker_fix_2026_04_22.md`
> ⚠️⚠️ **CHAIN-INHERIT LIVE-DB 2026-04-22** rewrite zu trades.db:signals → `project_chain_inherit_live_signals_2026_04_22.md`
> ⚠️⚠️ **JACK-MISS-ANALYSIS 04-21/22** LOBO/BTBT/AGPU → `project_jack_miss_analysis_04_21_22.md`
> ⚠️⚠️ **TELEGRAM=CLAUDE-HOME** → `project_claude_home_inbox_architecture.md`
> ⚠️⚠️ **OVERSOLD-LADDER 21.5% NO-FILL** → `project_aggressive_limit_oversold_pattern.md`
> ⚠️⚠️ **USER-GATE-TRIO shipped 2026-04-20** → `project_user_gate_trio_specs_2026_04_20.md`
> ⚠️⚠️ **ALT-B MISSED-TRADES-LOOP shipped 2026-04-20** → `project_alt_b_missed_trades_loop_2026_04_20.md`
> ⚠️ **BATCH-SIM 2026-04-20** (n=71 Total, Gate PASSED) → `project_batch_ticker_sim_2026_04_20.md`
> ⚠️⚠️ **CLONE-CANONICAL-GAP + FIX-20** → `project_clone_canonical_gap_2026_04_20.md`
> ⚠️⚠️ **SESSION-WRAP 2026-04-20 T9-17** → `project_session_wrap_2026_04_20_turns_9_17.md`
> ⚠️⚠️⚠️ **PARSER-PHASE-2 READY-STACK 2026-04-20** → `project_parser_phase2_ready_stack_2026_04_20.md`
> ⚠️⚠️ **DARK-CORPUS 2 683 Jack-Msgs pre-03-30** → `project_historical_raw_corpus_pre_march30.md`
> ⚠️ **End-to-End Layer-Diagnose** Idee geparkt → `project_end_to_end_layer_diagnosis_idea.md`
> ⚠️⚠️⚠️ **BREAKOUT-ENTRY DEPLOYED 2026-04-21** ENTRY_MODE=breakout, Paper läuft → `project_breakout_entry_deployed_2026_04_21.md`
> ⚠️⚠️⚠️ **ALT-C PARTIAL LIVE 2026-04-23** POS=50%/$5k, Stagger bi-dir ±6%, PRE_GAP_FILTER → `project_alt_c_deployed_2026_04_23.md`
> ⚠️⚠️⚠️ **FULL 6W-REPLAY 2026-04-22** 635 Jack-Msgs, R18R_WIDE +$1044 vs TIGHT −$233 → `project_full_replay_6w_findings_2026_04_22.md`
> ⚠️⚠️⚠️ **KARPATHY 4Q-RESEARCH 2026-04-23** → `project_karpathy_4q_research_2026_04_23.md`
> ⚠️⚠️ **R18r PROD-WIRING 2026-04-22** Engine im Worktree, FLAG OFF, nicht deployed → `project_r18r_production_wiring_2026_04_22.md`
> ⚠️⚠️ **PAPER-LEARNING-MODE 2026-04-22** STAGGER+Swing+R18r aktiv → `project_paper_learning_mode_flags_2026_04_22.md`
> ⚠️⚠️ **CHART-VISION-SCANNER v1 shipped 2026-04-21** → `project_chart_vision_scanner_2026_04_21.md`

---

## User Profile (BLEIBT)
- user_profile.md, feedback_style.md, feedback_invoking.md, feedback_model_routing.md, feedback_token_efficiency.md
- feedback_briefing_shortcut.md, feedback_image_sharing.md
- feedback_end_to_end_autonomy.md, feedback_autonomous_session_loop.md, feedback_session_freeze_save_everything.md, feedback_session_keepalive_services_check.md, feedback_bot_full_autonomy.md
- feedback_claude_root_launch.md, feedback_mirror_enumeration.md, feedback_decision_format.md, feedback_consistency_critical.md, feedback_no_parallel_work.md
- feedback_no_polygon_key_nag.md, feedback_no_openai_key_nag.md, feedback_stopping_bot.md
- feedback_save_means_save.md, feedback_verify_changes.md
- feedback_proactive_bot_improvements.md, feedback_nag_about_review.md, feedback_auto_save_tz.md
- feedback_alternatives_must_span_layers.md, feedback_alternatives_include_hybrid.md
- feedback_obsidian_vault.md, feedback_solve_autonomously_before_asking_for_help.md, feedback_dual_claude_coordination.md

## Skills & Tools (BLEIBT)
- reference_verdict_tools.md, reference_claude_code_install_2026_04_16.md, reference_claude_trading_skills_repo.md
- reference_obsidian_skills.md, reference_obsidian_skills_evaluated.md, reference_github_search_templates.md, reference_telegram_bots.md
- feedback_wrap_up_skill.md, feedback_scope_framework_skill.md, feedback_six_path_solution.md, feedback_doe_folder_structure.md, feedback_ralph_wiggum_loop.md, feedback_grill_me_skill.md, feedback_skill_check_enforcement.md

## Strategie-Specs (BLEIBT — MOC-Querverweise via [[Halt-Up-Pattern]] etc.)
- project_conditional_setup_collection.md, project_conditional_setup_executor.md, project_conditional_watchlist.md, project_watchlist_immediate_entry_sim.md
- project_multi_ticker_strategy_proof_ncpl.md, project_caution_signals.md, project_soft_keyword_filter.md, project_defensive_hebel.md
- project_staggered_entry.md, project_order_offset_simulation.md, project_averaging_strategy.md, project_swing_exclusion.md
- project_tsl_by_trade_type.md, project_tp_calibration.md, project_tsl_2pct_default_candidate.md, project_adaptive_exit_indicators.md, project_classifier_phase2.md
- project_reusable_rule_library.md, project_rule_derivation_pipeline.md

## Parser & Classifier — Vorgänger-Stack (BLEIBT)
- project_ticker_classifier.md, project_parser_multi_ticker_cloning.md, project_parser_ticker_miss_fix.md, project_parser_ticker_aliases.md, project_parser_chain_inheritance_exits_gap.md
- project_parser_a2_implementation.md, project_parser_quality_maximization.md, project_parser_zone_trade_extractor.md, project_jack_no_telegram_replies.md, project_ticker_price_mismatch_reverse_split.md
- project_parser_baseline_2026_04_18.md, project_parser_quality_sprint_2026_04_18.md, project_plan_c_lite_opus_skip.md

## Projekt-Kontext & Roadmap (BLEIBT)
- project_context.md, project_live_roadmap.md, project_billing.md
- project_weekend_task.md, project_weekend_master_list_2026_04_18.md, project_email_source_roadmap.md
- project_capitol_trades_stream.md, project_wheel_options_strategy.md, project_voice_telegram_agent.md, project_pm_mover_bot_backlog.md
- project_mem0_install_done.md, project_paperclip_eval_2026_04_17.md, project_cc_extensions_backlog.md, project_claude_code_power_features_2026_04_17.md, project_power_features_retrofit_2026_04_17.md
- project_skill_optimization_plan.md, project_skill_adapt_queue_2026_04_16.md, project_six_path_trial_review.md, project_codex_review_cadence_2026_04_17.md
- project_next_session_plan_2026_04_17.md, project_parabolic_late_entry_strategy_2026_04_17.md
- project_bugs_fixed.md, project_telegram_session_cleanup.md
- project_hermes_bridge_architecture.md, project_hermes_telegram_plan.md, project_hermes_install_after_night_queue.md
- project_bot_architecture_entry_primary.md, project_jack_subgroup_filter_analysis.md

## Verdict-Domänen-Specials (BLEIBT — verlinkt aus Review-Workflow-MOC)
- feedback_conditional_buy_with_price.md, feedback_jack_jargon_price_alert_equals_order.md
- feedback_verdict_blindspots_2026_04_18.md, feedback_no_feierabend_suggestions.md
- feedback_collaborative_design_patterns.md, feedback_claude_only_signal_bot.md, feedback_max_third_party_blocked.md
- reference_claude_code_features_2026_04_16.md

## Domänenwissen & Externe Referenzen (BLEIBT)
- reference_lopez_de_prado_ssrn_papers.md, reference_murphy_rsi_oscillator_rules.md, reference_elder_triple_screen.md, reference_reddit_afml_framefar_case.md
- reference_jack_staggered_entry_method.md, research_biotech_premarket_sources.md
- infrastructure_problems.md, reference_yt_transcript_vps_ban_bypass.md, project_karpathy_llm_wiki_pattern_obsidian.md

---

## Migrations-Notiz

**Vorher:** ~110 Cluster-Pins, 184 Zeilen, 7 große Cluster (Kairos 18, Review-Workflow 24, Auto-Research 8, KAPPI 5, Parser_V2 4, Watchdog 3, Testcenter 2) als detaillierte Pins.

**Nachher:** Cluster-Pins reduziert auf 2 Refs pro MOC (1× Wiki-MOC + 1× LATEST), restliche Detail-Files erreichbar über die MOCs. Geschätzt ~140 Zeilen, mehr Headroom unter dem 200-Zeilen-Limit.

**Was NICHT migriert wurde:**
- Runtime-Behavior-Pins (Tabelle, Tempo, Zahlen-aus-Quelle etc.) — bleiben als individuelle Pins
- Kurzlebige Tactical-Pins (Range-Support-Unlock, Dedup-Fix etc.) — bleiben für 2-4 Wochen, dann entfernen
- User-Profile, Skills, Strategie-Specs, Domänenwissen — keine Cluster-Bloat-Quelle

**User-Entscheidung:**
- Ja: produktive MEMORY.md mit diesem Vorschlag überschreiben
- Nein: nichts ändern, MEMORY.md bleibt im Original-Stand
- Teilweise: einzelne Cluster-Refs übernehmen, andere lassen
