# Memory Index

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
> ⚠️⚠️⚠️ **REGEL 9 (2026-04-24)**: KAIROS→ChatGPT-Exports IMMER als strukturiertes JSON (signals/trades/events/anomalies + optional Quick-Metrics), nicht Free-Text → `feedback_kairos_chatgpt_export_json_schema.md`
> ⚠️⚠️⚠️ **ENTRY-COMPARE PHASE-2 2026-04-23** SQL-Schema + Regime + Proposal-Engine + Decision-Layer (flag-gated) + Dashboard. 18/18 Tests. → `project_kairos_entry_compare_phase2_2026_04_23.md`
> ⚠️⚠️⚠️ **PHASE-2 QUALITY-ENGINE 2026-04-23 23:40** entry_quality.py (ChatGPT-Spec), both_viable → winner. Phase-1 n=18: Breakout 89%, Stagger-Delay 22.2min = Edge-Killer. 26/26 Tests. → `project_kairos_phase2_quality_engine_2026_04_23.md`
> ⚠️⚠️⚠️ **PHASE-2.1 SCORE-BASED 2026-04-24 00:15** determine_best_entry jetzt score-based statt max_upside. Breakout 86% (n=22), avg Score 5× höher, price_advantage 9.6%. 29/29 Tests. → `project_kairos_phase21_score_based_2026_04_23.md`
> ⚠️⚠️⚠️ **PHASE-3.2 FULL-CORPUS+SHADOW 2026-04-23** autonom A-E: n=54 (polygon) bestätigt Breakout 92.6%. entry_router.py=breakout (nicht in main.py). Shadow-dict+KAIROS_SHADOW_MODE flag. 46/46 Tests. → `project_kairos_phase32_full_corpus_shadow_2026_04_23.md`
> ⚠️⚠️⚠️ **PHASE-3.2 ROUTER-WIRED 2026-04-24** main.py HARD-SWITCH: choose_entry_strategy() vor STAGGER_ENABLED. shadow→shadow_compare. 85/85 Tests. Bot-Restart pending (`.env`-Handoff: KAIROS_LIVE_ENABLED+KAIROS_SHADOW_MODE=true). → `project_kairos_phase32_router_wired_2026_04_24.md`
> ⚠️⚠️⚠️ **CODEX PRIO 1-5 FIXES 2026-04-24** CRITICAL Fill-Match/SL-Dup/Cancel-Race/Router-Gate/Shadow-Integrity. models+db+signal_mgr+main+pos_mon+live_shadow. 85/85 Tests + 3 Smoke grün. Pending: .env-Flip+Restart. → `project_kairos_codex_prio15_fixes_2026_04_24.md`
> ⚠️⚠️⚠️ **PHASE-2/3 ANALYTICS 2026-04-24** Shadow-only: report_builder + router_features + auto_router + build_daily_report + kairos_daily_report overlay. 115/115 Tests, zero live-impact. → `project_kairos_phase23_analytics_2026_04_24.md`
> ⚠️⚠️⚠️ **PARSER_V2 PATTERN-LAYER + SAFETY-FILTER 2026-04-24** 3-Layer (Pattern 67/Intent/Regex) + w→b-Filter + 3-Schicht-Sicherheit Parser→Gate(0.80)→Override(kc0.8+price). Accuracy 10.67→33.33%. → `project_parser_v2_pattern_integration_2026_04_24.md`
> ⚠️⚠️ **PAPER-REPORT SHADOW+LEARNING 2026-04-24 (Tasks 14+15)** 📉 SHADOW PERFORMANCE + 🧠 LEARNING INSIGHTS im Daily-Report: Shadow simuliert +10%/-5%/EOD, Learning gruppiert Missed-Winners (pnl≥10%) nach range/support/action-Features + canned Suggestions. Reuse replay_full_jack_baseline, zero DB-Change. → `project_paper_report_shadow_section_2026_04_24.md`
> ⚠️⚠️⚠️ **RANGE+SUPPORT UNLOCK 2026-04-24 (Task 16)** `_is_range_support()` + Setup-Marker `source_override="range_support_override"` + Trigger-Rescue bypasst range_filter. Nur Setups (trig required), keine Parser/Filter-Änderung. Mirror in paper_trader + replay, 100/100 Parity. Smoke ✓ (NVDA 800-820 support bounce). → `project_range_support_unlock_2026_04_24.md`
> ⚠️⚠️⚠️ **WATCHDOG RESTART-STORM 2026-04-25 06:39-06:41** User-Restart-Race vs Watchdog-Auto-Restart. 3 Bugs: 30s-timeout zu kurz (Bot-Stop braucht 90s), kein Restart-Lock, restart_all.sh fehlt signal-kairos. Sekundär: Ghost-Snapshot 14h stale ignoriert. → `project_watchdog_restart_storm_2026_04_25.md`
> ⚠️⚠️⚠️ **PARSER_V2 TOP-5 RULES 2026-04-24** decisive-action-Guard (placed/filled/bought), short-no-ticker-noise (<4), ticker-required für took_position/entered, Confidence-Cap 0.65 + nie skip_llm für starter/nibble. → `project_parser_v2_top5_rules_2026_04_24.md`
> ⚠️⚠️⚠️ **PARSER_V2 TASK 19 RECALL-UPLIFT 2026-04-25** Splitter-Bug (SL/TP/ET als Ticker zerschnitt Templates) + neue hard_fix Gruppen E (DayTrade/Placed/Filled) + F (PriceAlert/Missed/Recap). recall_b 37→73%. → `project_parser_v2_task19_recall_uplift_2026_04_25.md`
> ⚠️⚠️⚠️ **SETUP/TRIGGER-ENGINE 2026-04-24** detect_setup→store_setup→trigger_engine. Alert/watching/might-order-Msgs landen in `trade_setups`-Tabelle (status=active), kein Sofort-Trade. `check_triggers(ticker,price)` feuert bei Markt-Level. Pending: Wire an position_monitor Price-Poll. → `project_parser_v2_setup_trigger_integration_2026_04_24.md`
> ⚠️⚠️⚠️ **WATCHDOG BLUEPRINT-ALIGNMENT 2026-04-24** +Kairos-Service/Heartbeat/Ghost-Alert (read-only snapshot). Kairos-Daemon schreibt .kairos_heartbeat atomic. Observability-Triade vollständig. → `project_watchdog_blueprint_alignment_2026_04_24.md`
> ⚠️⚠️⚠️ **MONITOR-ERRORS NIE IGNORIEREN** 2026-04-24: `pos.unrealizedPNL` crashte Heartbeat 7h42m, SL/TP effektiv tot bis Watchdog-Alert. Jeder Loop-Error ist kritisch. → `feedback_never_dismiss_monitor_errors.md`
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
> ⚠️⚠️ **HALT-UP-GRID-WINNER** (n=53/37 Mean +39.38% Win 94.3%) → `project_halt_up_autoskim_peak_tsl.md`
> ⚠️⚠️⚠️ **ALLES TABELLE** → `feedback_always_table_format.md`
> ⚠️⚠️ **USER SETZT TEMPO** → `feedback_user_paces_review.md`
> ⚠️⚠️⚠️ **SIMULIEREN STATT FRAGEN** → `feedback_simulate_before_asking.md`
> ⚠️⚠️⚠️ **KOMPLETTER REVIEW-WORKFLOW** 7 Phasen → `feedback_complete_review_workflow.md`
> ⚠️⚠️⚠️ **REVIEW = NUR PARSER** → `feedback_review_parser_only_phase.md`
> ⚠️⚠️⚠️ **AUTO-QUEUE JEDER TICKER** → `feedback_auto_queue_every_pasted_ticker.md`
> ⚠️⚠️⚠️ **NIGHT-SIM = VOLLE DB-HISTORIE** → `feedback_sim_uses_full_db_history.md`
> ⚠️⚠️⚠️ **PRICE-RANGE-TICKER-DISAMBIG** → `feedback_price_range_ticker_disambiguation.md`
> ⚠️⚠️⚠️ **REVIEW-HAUPTLINIE** → `feedback_review_mainline_workflow.md`
> ⚠️⚠️⚠️ **ZEIT × 7-10** → `feedback_time_estimates_7x_multiplier.md`
> ⚠️⚠️⚠️ **FEATURE IN EINEM SHOT** → `feedback_feature_completeness_first_pass.md`
> ⚠️⚠️⚠️ **NIGHT_QUEUE SEQUENZIELL** → `feedback_night_queue_sequential_execution.md`
> ⚠️⚠️ **MAX-ACCOUNT, NIE API-KOSTEN** → `feedback_max_account_no_api_billing.md`
> ⚠️⚠️⚠️ **NIE WIEDER NACH API FRAGEN** (2026-04-22 21:26) → `feedback_never_ask_about_api.md`
> ⚠️⚠️⚠️ **PARSER-MAX-ROUTE LIVE 2026-04-22 19:21** (`claude -p` subprocess, OAuth, ENV-strip, 4s/call, Fallback→API, commit b728b2e) → `project_parser_max_route_deployed_2026_04_22.md`
> ⚠️⚠️⚠️ **FULL 6W-REPLAY 2026-04-22** 635 Jack-Msgs, R18R_WIDE +$1044 vs TIGHT −$233. → `project_full_replay_6w_findings_2026_04_22.md`
> ⚠️⚠️⚠️ **KARPATHY 4Q-RESEARCH 2026-04-23** Q1 cond_break 7 hits, Q2 Σ+508% (inflation), Q3 r18r bestätigt, Q4 skip_sub_1_penny +15.27pp. → `project_karpathy_4q_research_2026_04_23.md`
> ⚠️⚠️⚠️ **ALT-C PARTIAL LIVE 2026-04-23** POS=50%/$5k, Stagger bi-dir ±6%, PRE_GAP_FILTER. → `project_alt_c_deployed_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS REVIEW-IMPL 2026-04-23** 7 items, 18/18 tests — Realistic-Exit/Regime-Tagger/Dynamic-Slip/Quality-Score. → `project_kairos_review_implementation_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS RL-STACK SHADOW-SHIP 2026-04-23 20:43** commit ec40080, 7 Module + 2 Tabellen, 10 Flags OFF, 20/20 Tests. → `project_kairos_rl_stack_deployed_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS P2.5+P2.6 SHADOW-SHIP 2026-04-23 21:00** commit 6eba401, Pattern-Discovery (Lane1+2) + Karpathy-Loop, 36/36 Tests, 7 Flags OFF, pandas_ta dropped. → `project_kairos_p25_p26_shipped_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS P2.6 GUARDS 2026-04-23 21:30** commit 45f60f6, DebugLog+Overfit+TimeSplit+Regime, 64/64 Tests, 9 Flags OFF, `scripts/kairos_morning_run.py` für ChatGPT-Review. → `project_kairos_p26_guards_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS HARDENING 2026-04-23 22:30** Ref-Time-Dedup + Orphan-Gate + Dispatcher + Breakout-Fallback, 26/26 Tests, 5 Flags OFF. → `project_kairos_hardening_2026_04_23.md`
> ⚠️⚠️⚠️ **ENTRY-COMPARISON PIPELINE 2026-04-23 23:xx** ChatGPT-Spec, 6 Module + 8 Tests, läuft auf Phase-1-Delivery. Erste Zahlen: both_viable 18/22, Ø max↑ 22-65%. → `project_entry_comparison_pipeline_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS PHASE-3 PULLBACK 2026-04-23** ChatGPT-Hypothese widerlegt: Breakout dominiert Pullback MEHR als Momentum (B-Score 0.45 vs 0.19, 2.4×). n=22. → `project_kairos_phase3_pullback_analysis_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS PHASE-2.2 PRICE-ADV-FIX 2026-04-23** Score += -0.5*price_advantage_ratio + Stagger.first_price. Breakout 19→21/22 (95.5%). Edge real, nicht Peak-Bias. 39/39 Tests. → `project_kairos_phase22_price_adv_fixes_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS PHASE-3.1 SWEEP 2026-04-23** Thresholds 3/5/7/10/15%. KEIN Flip-Punkt — Stagger gewinnt in keinem Regime (max 9% bei 3%-Bucket). Breakout 94-100% global. → `project_kairos_phase31_threshold_sweep_2026_04_23.md`
> ⚠️⚠️⚠️ **DEDUP EMPTY-TICKER FIX 2026-04-22** (MIRA-Miss RCA: `(None, COMMENTARY)`-Collision killed raw_message. Fix in safety.py) → `project_dedup_empty_ticker_fix_2026_04_22.md`
> ⚠️⚠️ **CHAIN-INHERIT LIVE-DB 2026-04-22** (rewrite zu trades.db:signals, default=True. "Sold half at 1.52" → ONFO) → `project_chain_inherit_live_signals_2026_04_22.md`
> ⚠️⚠️ **JACK-MISS-ANALYSIS 04-21/22** LOBO/BTBT/AGPU. AGPU echter Miss via API-Blackout. Fix=Breakout+MAX-Route. → `project_jack_miss_analysis_04_21_22.md`
> ⚠️⚠️ **TELEGRAM=CLAUDE-HOME** → `project_claude_home_inbox_architecture.md`
> ⚠️⚠️ **DELEGATE-TO-HERMES** → `feedback_delegate_to_hermes.md`
> ⚠️⚠️ **HERMES-MITWACHSEN** (8-Punkt-Check) → `feedback_hermes_grows_with_us.md`
> ⚠️⚠️⚠️ **2-MIN-IDLE → AUTO-CONTINUE** → `feedback_autonomous_continue_after_2min.md`
> ⚠️⚠️ **VERDICT-GLOSSAR VOR METRIKEN** → `feedback_verdict_glossary_before_metrics.md`
> ⚠️⚠️⚠️ **TRIM-TOP-3 PFLICHT** → `feedback_trim_top3_mandatory_in_sims.md`
> ⚠️⚠️⚠️ **SIM-DB-ROUTING** (polygon 272 Tickers primary) → `feedback_sim_script_db_routing_audit.md`
> ⚠️⚠️ **OVERSOLD-LADDER 21.5% NO-FILL** → `project_aggressive_limit_oversold_pattern.md`
> ⚠️⚠️ **USER-GATE-TRIO shipped 2026-04-20** → `project_user_gate_trio_specs_2026_04_20.md`
> ⚠️⚠️ **ALT-B MISSED-TRADES-LOOP shipped 2026-04-20** (14 Miss-Cats, Forward-Sim, /misses+/reconcile) → `project_alt_b_missed_trades_loop_2026_04_20.md`
> ⚠️⚠️⚠️ **HERMES-LESSONS** LLM proposes / gate decides, Applied-Knob-Lock, Human-in-loop → `feedback_hermes_lessons_self_eval_trap.md`
> ⚠️⚠️⚠️ **PARSED_SIGNALS = BATCH** (stale 2026-04-06) → `feedback_parsed_signals_is_batch_snapshot.md`
> ⚠️⚠️⚠️ **DB-PATH: data/ vs flat** → `reference_db_path_map_2026-04-20.md`
> ⚠️⚠️⚠️ **COUNT-CLAIMS BRAUCHEN ZEITRAUM** → `feedback_count_claims_need_scope.md`
> ⚠️ **YT-TRANSKRIPT: notegpt.io** → `feedback_youtube_transcript_prefer_scrapers.md`
> ⚠️ **BATCH-SIM 2026-04-20** (n=71 Total, Gate PASSED) → `project_batch_ticker_sim_2026_04_20.md`
> ⚠️⚠️ **CLONE-CANONICAL-GAP + FIX-20** (12 rows pending --apply) → `project_clone_canonical_gap_2026_04_20.md`
> ⚠️⚠️ **SESSION-WRAP 2026-04-20 T9-17** (Parser-Phase-2-Stack, alle FIX-Skripte 2-33% Coverage-Gap) → `project_session_wrap_2026_04_20_turns_9_17.md`
> ⚠️⚠️⚠️ **PARSER-PHASE-2 READY-STACK 2026-04-20** (4 drafts + 2 plans + 182 real-data-samples, ~19h integration) → `project_parser_phase2_ready_stack_2026_04_20.md`
> ⚠️⚠️⚠️ **UNIVERSAL RULES, NICHT EINZELFALL** → `feedback_universal_rules_not_per_trade.md`
> ⚠️⚠️⚠️ **PROFIT-LOCKS JACK-UNABHÄNGIG** (3% Trailing-SL ONFO-validated) → `feedback_profit_locks_jack_independent.md`
> ⚠️⚠️ **DARK-CORPUS 2 683 Jack-Msgs pre-03-30** (Okt 2025 – Mar 2026, >99% unparsed) → `project_historical_raw_corpus_pre_march30.md`
> ⚠️⚠️⚠️ **ALT-C PRIMARY OBJECTIVE = PROFIT MAX ALL-TICKER** (invent→sim→cross→memorize→propose) → `project_alt_c_primary_objective_profit_max.md`
> ⚠️⚠️⚠️ **HERMES SELBST-FIXEN** (wenn kaputt, sofort Gateway-Restart — sonst silent-inaktiv) → `feedback_auto_fix_hermes_communication.md`
> ⚠️⚠️⚠️ **JACK = HAUPTPROJEKT** (alles andere sekundär, 2026-04-21) → `feedback_jack_main_project_priority.md`
> ⚠️⚠️⚠️ **IST-ZUSTAND PRÜFEN VOR ÄNDERUNG** (nie aus config-Default raten, immer .env/Code lesen) → `feedback_check_state_before_proposing.md`
> ⚠️ **End-to-End Layer-Diagnose (Parser×Entry×Exit)** Idee geparkt 2026-04-21 → `project_end_to_end_layer_diagnosis_idea.md`
> ⚠️⚠️⚠️ **KAIROS-BOT PLAN 2026-04-23** 11 Phasen P0-P5.5 inkl P2.5+P2.6, 92h raw → `project_kairos_implementation_plan_2026_04_23.md`
> ⚠️⚠️⚠️ **KAIROS v1 DEPLOYED 2026-04-23 09:52 CEST** signal-kairos.service active shadow-mode, Hooks in sig_mgr+pos_mon, **Bot-Restart pending** → `project_kairos_v1_deployed_2026_04_23.md`
> ⚠️⚠️⚠️ **PIPELINE-IMPACT-TRACE vor Layer-Änderung** (grep alle Consumer + Order-Preis-Risiko) → `feedback_trace_full_pipeline_before_layer_change.md`
> ⚠️⚠️⚠️ **BREAKOUT-ENTRY DEPLOYED 2026-04-21 16:00 CET** (ENTRY_MODE=breakout, AUTO_TP_LEVELS=leer, Paper läuft) → `project_breakout_entry_deployed_2026_04_21.md`
> ⚠️⚠️⚠️ **HAUPTPROJEKT 2: Auto-Research-Loop (Karpathy-Style)** Exit-Optimierung via LLM-Generate→Backtest→Gate→Loop → `project_hauptprojekt_2_auto_research_loop.md`
> ⚠️⚠️⚠️ **AUTO-RESEARCH R15b byp=8.02/tsl=0.1** Mean +11.22%, 0 losses. (predecessor) → `project_auto_research_day1_winner.md`
> ⚠️⚠️⚠️ **AUTO-RESEARCH R17c REGIME-TIGHT** Mean +11.34, Sh 1.14. (predecessor) → `project_auto_research_round17c_regime_tight.md`
> ⚠️⚠️⚠️ **R18r Wide-Rollover CHAMPION 2026-04-22** Mean +18.07, Sh 1.86, soft 4/4, fuzz 94%. → `project_auto_research_round18r_wide_rollover_winner.md`
> ⚠️⚠️⚠️ **TSL-SIMULATOR-INFLATION-BIAS** Late-armed TSL appears better in sim than reality. Run `realism_audit.py`. → `feedback_tsl_simulator_inflation_bias.md`
> ⚠️⚠️ **R18s SATURATION 2026-04-22** R18-series CLOSED (3 axes all NULL). Next: n>100 or re-entry framework. → `project_auto_research_round18s_saturation_report.md`
> ⚠️⚠️ **R18r PROD-WIRING 2026-04-22** Engine+hook+config im Worktree, FLAG default OFF, nicht deployed. → `project_r18r_production_wiring_2026_04_22.md`
> ⚠️⚠️ **PAPER-LEARNING-MODE 2026-04-22 07:35** STAGGER+Swing+R18r aktiv, R16-verdict=n Override in rule_engine_bridge → `project_paper_learning_mode_flags_2026_04_22.md`
> ⚠️⚠️ **CHART-VISION-SCANNER v1 shipped 2026-04-21** (LAES 04-14 +14.9% TP1, random n=10 zero FP) → `project_chart_vision_scanner_2026_04_21.md`
> ⚠️⚠️⚠️ **KAPPI Champion 2026-04-22** static tp_hard_then_hold(20) shipped — Train +12.84/Hold +12.48/WR 85%, 59/269 corpus-survivors. → `project_kappi_p4_0d_expanded_corpus_holdout_2026_04_22.md`
> ⚠️⚠️⚠️ **KAPPI P4.6 LEAKAGE-LESSON** cond(f5≥12)+15.76% war leaky (9/84 tp30-fires im 0-5min). Ship static, skip conditional. → `project_kappi_p4_6_conditional_tp_winner_2026_04_22.md`
> ⚠️⚠️ **KAPPI P4.4 REALISM-AUDIT** shadow_fires DB + BLOCK>+2pp/WATCH Policy für Pre-Promote. → `project_kappi_p4_4_realism_audit_framework_2026_04_22.md`
> ⚠️⚠️⚠️ **KAPPI P7 ENTRY-FILTER WATCH** Per-Trade-Δ ≠ Total-Profit-Δ lesson (Gate cost −27.8pp total). → `project_kappi_p7_entry_filter_watch_2026_04_22.md`
> ⚠️⚠️ **KAPPI P6 ROUND CLOSED** 7 Tests: ATR/VWAP/VolDecay/TimeDecay/DDCap all NULL. TP_HARD_20 robust. → `project_kappi_p6_round_closed_2026_04_22.md`

## User Profile
- user_profile.md, feedback_style.md, feedback_invoking.md, feedback_model_routing.md, feedback_token_efficiency.md
- feedback_briefing_shortcut.md, feedback_image_sharing.md
- feedback_end_to_end_autonomy.md, feedback_autonomous_session_loop.md, feedback_session_freeze_save_everything.md, feedback_session_keepalive_services_check.md, feedback_bot_full_autonomy.md
- feedback_claude_root_launch.md, feedback_mirror_enumeration.md, feedback_decision_format.md, feedback_consistency_critical.md, feedback_no_parallel_work.md
- feedback_no_polygon_key_nag.md, feedback_no_openai_key_nag.md, feedback_stopping_bot.md
- feedback_save_means_save.md, feedback_verify_changes.md
- feedback_proactive_bot_improvements.md, feedback_nag_about_review.md, feedback_auto_save_tz.md
- feedback_alternatives_must_span_layers.md, feedback_alternatives_include_hybrid.md
- feedback_obsidian_vault.md, feedback_solve_autonomously_before_asking_for_help.md, feedback_dual_claude_coordination.md

## Review-Workflow
- feedback_review_format.md, feedback_review_format_v2.md, feedback_review_format_v3.md, feedback_review_long_message_layout.md, feedback_review_table_default_layout.md, feedback_review_method_v3.md
- feedback_review_klicks_format.md, feedback_review_output_compact.md, feedback_review_batch_approval.md, feedback_review_translate_jack_text.md
- feedback_persist_review.md, feedback_verdict_codes.md, feedback_verdict_words_not_letters.md, feedback_verdict_noise_bias.md, feedback_verdict_learning_loop.md
- feedback_self_eval_cadence.md, feedback_self_eval_seed418_lessons.md, feedback_self_eval_consolidated_2026_04_18.md, feedback_session_health_check_mandatory.md
- feedback_fill_vs_entry.md, feedback_buy_without_price_equals_n.md, feedback_trade_type_clarification.md, feedback_message_chain_awareness.md, feedback_out_of_session_mention.md, feedback_pronoun_reference_needs_prices.md, feedback_noise_one_click.md, feedback_soft_score_position_sizing.md
- feedback_ticker_by_ticker_discussion_file.md, feedback_read_charts_during_review.md, feedback_chain_display_validated.md, feedback_sls_excluded_from_tz.md
- feedback_adaptive_stack_validated.md, feedback_distress_tsl_validated.md, feedback_jack_self_adjusts_alerts.md

## Skills & Tools
- reference_verdict_tools.md, reference_claude_code_install_2026_04_16.md, reference_claude_trading_skills_repo.md
- reference_obsidian_skills.md, reference_obsidian_skills_evaluated.md, reference_github_search_templates.md, reference_telegram_bots.md
- feedback_wrap_up_skill.md, feedback_scope_framework_skill.md, feedback_six_path_solution.md, feedback_doe_folder_structure.md, feedback_ralph_wiggum_loop.md, feedback_grill_me_skill.md, feedback_skill_check_enforcement.md

## Review-Queue & Rules
- project_review_pending_tickers.md, project_review_bootstrap.md, project_reusable_rule_library.md, project_rule_derivation_pipeline.md, project_priority_review_before_testcenter.md
- project_conditional_setup_collection.md, project_conditional_setup_executor.md, project_conditional_watchlist.md, project_watchlist_immediate_entry_sim.md
- project_multi_ticker_strategy_proof_ncpl.md, project_caution_signals.md, project_soft_keyword_filter.md, project_defensive_hebel.md
- project_staggered_entry.md, project_order_offset_simulation.md, project_averaging_strategy.md, project_swing_exclusion.md
- project_tsl_by_trade_type.md, project_tp_calibration.md, project_tsl_2pct_default_candidate.md, project_adaptive_exit_indicators.md, project_classifier_phase2.md

## Parser & Classifier
- project_ticker_classifier.md, project_parser_multi_ticker_cloning.md, project_parser_ticker_miss_fix.md, project_parser_ticker_aliases.md, project_parser_chain_inheritance_exits_gap.md
- project_parser_a2_implementation.md, project_parser_quality_maximization.md, project_parser_zone_trade_extractor.md, project_jack_no_telegram_replies.md, project_ticker_price_mismatch_reverse_split.md
- project_parser_baseline_2026_04_18.md, project_parser_quality_sprint_2026_04_18.md, project_plan_c_lite_opus_skip.md

## Testcenter & Simulation
- project_testcenter.md, project_testcenter_intraday.md, project_testcenter_architecture.md, project_testcenter_phase1_complete.md, project_testcenter_4phase_plan.md, project_testcenter_phase_a_complete.md, project_testcenter_phase_a_clean_baseline.md, project_testcenter_backlog_2026_04_15.md, project_testcenter_2026_04_15_evening_handover.md, project_testcenter_r_hypotheses.md
- project_testcenter_halted_up_autosell.md, project_testcenter_price_alert_as_entry.md, project_simulation_results.md, project_slippage_mitigation_options.md
- project_rule_engine_architecture.md, project_bot_knowledge_integration.md, project_jack_edge_audit_2026_04_16.md, project_module_hybrid_review_2026_04_17.md, project_profit_pipeline_2026_04_16.md
- project_round2_autonomous_2026_04_18.md, project_param_sweep_uncap_tp_2026_04_18.md, project_rule_hypotheses.md
- project_post_backfill_sims_2026_04_18.md, project_polygon_backfill_tickers_24.md
- project_42_46_implementation_design.md, project_42_staggered_entry_foundation.md, project_46_halt_up_hybrid_foundation.md, project_45_extend_scope_closed.md
- project_post_review_build_queue.md, project_chart_ocr_range_validator.md, project_chart_pattern_learner.md, project_batch_ticker_sim_2026_04_20.md

## Projekt-Kontext & Roadmap
- project_context.md, project_live_roadmap.md, project_billing.md
- project_weekend_task.md, project_weekend_master_list_2026_04_18.md, project_email_source_roadmap.md
- project_capitol_trades_stream.md, project_wheel_options_strategy.md, project_voice_telegram_agent.md, project_pm_mover_bot_backlog.md
- project_mem0_install_done.md, project_paperclip_eval_2026_04_17.md, project_cc_extensions_backlog.md, project_claude_code_power_features_2026_04_17.md, project_power_features_retrofit_2026_04_17.md
- project_skill_optimization_plan.md, project_skill_adapt_queue_2026_04_16.md, project_six_path_trial_review.md, project_codex_review_cadence_2026_04_17.md
- project_next_session_plan_2026_04_17.md, project_watchdog_hardening_2026_04_17.md, project_parabolic_late_entry_strategy_2026_04_17.md
- project_bugs_fixed.md, project_telegram_session_cleanup.md
- project_hermes_bridge_architecture.md, project_hermes_telegram_plan.md, project_hermes_install_after_night_queue.md
- project_bot_architecture_entry_primary.md, project_jack_subgroup_filter_analysis.md

## Verdict & Review (specialized)
- feedback_conditional_buy_with_price.md, feedback_jack_jargon_price_alert_equals_order.md
- feedback_verdict_blindspots_2026_04_18.md, feedback_no_feierabend_suggestions.md
- feedback_collaborative_design_patterns.md, feedback_claude_only_signal_bot.md, feedback_max_third_party_blocked.md
- reference_claude_code_features_2026_04_16.md

## Domänenwissen & Referenzen
- reference_lopez_de_prado_ssrn_papers.md, reference_murphy_rsi_oscillator_rules.md, reference_elder_triple_screen.md, reference_reddit_afml_framefar_case.md
- reference_jack_staggered_entry_method.md, research_biotech_premarket_sources.md
- infrastructure_problems.md, reference_yt_transcript_vps_ban_bypass.md, project_karpathy_llm_wiki_pattern_obsidian.md
