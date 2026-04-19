# Signal Bot Deep-Dive Audit — 2026-04-19

**Kontext:** Autonome Generalüberprüfung (Task #84) während User-Pause. Ziel: Architektur-Health + Action-Liste für nächste Session.

---

## 1. Runtime / Services

| Service | PID | Status | Hinweis |
|---|---|---|---|
| `main.py` (Signal Bot) | 3566029 | läuft seit 2026-04-18 | 106MB RAM, 0:16 CPU-Zeit |
| `dashboard.py` | 2685766 | läuft seit 2026-04-10 | 26MB RAM |
| `review_ui.py` (Streamlit 8501) | 3526645 | läuft seit 2026-04-18 | 190MB RAM, 7:50 CPU |
| `check_api_and_resume.sh` | 3230814 | läuft seit 2026-04-15 | cronjob-resume |

systemd `is-active`-Probing blockiert in Sandbox; Prozess-Check via `ps` bestätigt Bot-Uptime.

---

## 2. Datenbanken (Disk-Inventar)

| DB | Pfad | Größe | Rows (Top-Tables) | Status |
|---|---|---:|---|---|
| trades.db | `/root/signal_bot/trades.db` | 892K | trades=27, signals=298, tp_targets=48, api_usage=6546, suggestions=17, trade_analyses=3 | HEALTHY |
| parsed_signals.db | `data/parsed_signals.db` | 1.5M | parsed_signals=2658 | HEALTHY |
| polygon_data.db | `data/polygon_data.db` | **1.8G** | bars (633k+) | Wachstumsbeobachtung ok |
| price_data_1min.db | `data/price_data_1min.db` | 330M | Legacy IBKR | Nur Legacy-Reads, neue Sims auf polygon_data |
| backtest_results.db | `data/backtest_results.db` | 4.9M | diverse Sim-Ergebnisse | HEALTHY |
| signal_chains.db | `data/signal_chains.db` | 60K | chains | HEALTHY |
| raw_messages.db | `data/raw_messages.db` | 1008K | telegram-raw | HEALTHY |
| **Leer/Stale (0 Byte):** `data/trades.db`, `data/feed_messages.db`, `data/monster_features.db`, `data/jack_messages.db`, `data/backtest_signals.db`, `data/signals.db`, `/root/signal_bot/polygon.db` | | | | ⚠️ Delete-Kandidaten |

**Action:** 7 leere DB-Dateien können gelöscht werden (nach User-Check). Nicht jetzt automatisch gelöscht wegen Blast-Radius-Risiko.

---

## 3. Feature-Flags (config.py-Inventar)

| Flag | Default | Letzter Status |
|---|---|---|
| TRAILING_SL_ENABLED | True | Live (TSL 2% seit 2026-04-18 Flip) |
| TRAILING_TP_ENABLED | True | Live |
| ORPHAN_TP_ENABLED | True | Live |
| ORPHAN_SL_MIDPOINT | True | Live |
| RULE_ENGINE_ENABLED | True | Live |
| OPUS_VALIDATE_ALL_ENTRIES | True | Live |
| STAGGER_ENABLED | **False** | Foundation DONE, Integration pending (Task #42) |
| HALT_SKIM_ENABLED | **False** | Foundation DONE, Integration pending (Task #46) |
| MODIFY_ORDER_SIZE_PARSING_ENABLED | False | Corpus n=2 → LOW-Prio |
| MODIFY_ORDER_SIZE_AUTO_ACTION | False | dito |
| PARSER_CHAIN_INHERIT_ENABLED | **False** | Parser-A2 Komp5 fertig, aber OFF |
| PARSER_CALIBRATION_ENABLED | **False** | Isotonic DONE, aber OFF |
| PARSER_STRUCTURED_OUTPUT_ENABLED | **False** | S3 DONE, aber OFF |
| PARSER_AGENTIC_EXTRACT_ENABLED | **False** | A2 DONE, aber OFF |
| PARSER_RAG_ENABLED | **False** | S1 DONE, aber OFF |
| MARKET_CONTEXT_GATE_ENABLED | **False** | NEU 2026-04-19, Default OFF |
| MARKET_CONTEXT_GATE_STRICT | **False** | Opt-In |
| PARSER_OPUS_FAIL_CLOSED | **False** | NEU, Fail-Open Default |

**9 Flags sind OFF**. Davon 5 Parser-A2-Komponenten fertig entwickelt aber nicht aktiviert — Regression-Run #66 zeigte keinen Edge auf 100 Golden-Messages. **Action:** Explizite OFF→ON-Entscheidung pro Flag nach Review-Komplettierung, dokumentiert im Flag-Inventory.

---

## 4. Code-Module (LoC-Hotspots)

| Modul | LoC | Hotspot? |
|---|---:|---|
| position_monitor.py | 853 | ⚠️ Main orchestrator — groß, aber kohärent. 5 Exception-Handler gehärtet 2026-04-19. |
| parser.py | 848 | ⚠️ Claude-Prompt + Flag-Cascade — erwartbar groß. Opus-Validate + Telegram-Alert-Flow dort. |
| main.py | 792 | OK — Reconciliation + Event-Loop. |
| analyzer.py | 759 | OK — Post-Mortem-Engine. |
| ibkr_client.py | 621 | OK — Connection + Order-Platzierung. `safe_call`-Wrapper (Task #68) integriert. |
| signal_manager.py | 602 | OK — Market-Gate (Task #78) + asyncio.Lock (Task #67) + partial-sell-alert (2026-04-19). |
| parser_rules.py | 569 | OK — Regel-Katalog + Few-Shot (29 Beispiele). |
| watchdog.py | 501 | OK — Heartbeat-Monitor. |
| db.py | 406 | OK |
| parser_agentic.py | 341 | OK (A2 Flag-OFF) |
| **test_simulation.py in /root/signal_bot/ (326 LoC)** | 326 | ⚠️ **Verdächtig — sollte in `tests/` liegen** |

**Action:** `test_simulation.py` → entweder nach `tests/` verschieben oder in `scripts/` wenn es ein Ad-hoc-Tool ist.

---

## 5. Test-Suite (13 Module, 70 Tests)

**Resultat:** 70/70 PASS (nachdem `test_parser_rules.test_few_shot_count_reasonable`-Bound von 20 auf 40 angehoben wurde — FEW_SHOT_EXAMPLES ist auf 29 gewachsen durch Self-Eval-Lessons).

| Test-Modul | Coverage |
|---|---|
| test_shadow_replay.py | simulate_trade + simulate_trade_ladder + **Slippage** (6 neue Tests 2026-04-19) |
| test_market_context.py | **6 Tests NEU 2026-04-19** (fail-open, high_vol-Block, strict-mode) |
| test_signal_manager.py | Core-Logik |
| test_signal_manager_lock.py | asyncio.Lock per Ticker (Task #67) |
| test_ibkr_safe_call.py | safe_call-Wrapper (Task #68) |
| test_stagger_tranches.py | Staggered-Entry (Task #42) |
| test_r15_ladder.py | R15-Ladder-Sim |
| test_parser_calibration.py | Isotonic-Regression |
| test_parser_rules.py | Regel-Konsistenz (bound fix) |
| test_parser_context.py | Chain-Inheritance |
| test_parser_regression.py | 100-Golden |
| test_rule_engine_bridge.py | Rule-Engine-Bridge |
| test_modify_order_size.py | MODIFY_ORDER_SIZE-Parser |

**Gap-Analysis:** Kein expliziter Test für:
- `position_monitor._loop` Happy-Path (wird implizit durch Smoke getestet)
- `analyzer.py` Post-Mortem (3 Trade-Analyses nur; wenig Fälle)
- Market-Gate-Integration in `signal_manager` (Unit-Test existiert, aber kein End-to-End)

**Action:** Nach Live-Rollout-Gate Integration-Test für `signal_manager + market_context` zusammen (Task #85 Kandidat).

---

## 6. Cron-Jobs (aktive Schedules)

| Cron | Zweck | Status |
|---|---|---|
| `*/30 * * * *` check_api_and_resume | API-Quota-Resume | Läuft seit 2026-04-15 |
| `30 21 * * 1-5` analyzer daily_digest | Post-Mortem Daily | OK |
| `0 17 * * 0` analyzer weekly_deep_dive | Weekly-Deep-Dive | OK |
| `15 23 * * *` testcenter run_daily | Nightly Testcenter | OK |
| `0 */2 * * *` codex_queue_loop | Codex-Quota-Retry | OK |
| `30 23 * * *` tsl_monitor_cron | TSL-2%-Premature-Exit-Check | NEU 2026-04-18 |
| `45 23 * * *` shadow_replay_cron | Nightly Shadow-Replay | NEU 2026-04-18 |
| `0 23 * * *` obsidian_github_sync | Vault→GitHub | OK |

**Kein Cron-Drift erkannt.** Alle Jobs schreiben in Logs, Quota-sicher.

---

## 7. Review-Status (Verdicts-Fortschritt)

- parsed_signals: **2658**
- verdicts persistiert in `parser_review_verdicts.csv`: **468**
- Verdict-Verteilung: n=224 (48%), w=78 (17%), b=77 (16%), e=43 (9%), s=27 (6%), u=13, x=5, sl_update=1
- **Ungereviewed:** ~2190 Messages (davon deutliches Has-Ticker-Subset)

**Action:** Task #82 Review-Batch-Curation priorisiert nach Signal-Type + Haiku-Vorschlag-Diskrepanz.

---

## 8. Inbox-Hygiene (Obsidian Vault)

**Vor:** 3 Files in `01 Inbox/` (2× autonome Reports, 1× Brain Dump leer).

**Nach:** 
- `AUTONOMOUS_REPORT_2026-04-17.md` + `AUTONOMOUS_BREAK_REPORT_2026-04-18.md` → `06 Archiv/Autonomous Reports/` verschoben
- `Brain Dump.md` bleibt (aktiver Eingang)

---

## 9. Memory-Index (MEMORY.md)

**Vor:** 40993 Byte, 208 Zeilen → System-Truncation bei Zeile 200 (Domänenwissen + infrastructure_problems wurden abgeschnitten).

**Nach:** 15164 Byte, 87 Zeilen → komplett im Context. Gruppiert in 8 Sektionen, redundante Zeilen zusammengefasst.

---

## 10. Offene Tech-Debt-Punkte

| Prio | Punkt | Next-Step |
|---|---|---|
| MED | `test_simulation.py` im Root statt `tests/` | Verschieben oder umbenennen |
| LOW | 7 leere DBs in `data/` | Nach User-Check löschen |
| MED | 5 Parser-A2-Flags auf OFF | OOS-Test auf 200-Korpus bevor OPS→ON |
| HIGH | Uncap-Hard-TP nur Mean-Edge, nicht Median-Edge | Paper-Gate-Test bevor UNCAP_TP_ENABLED=True in Live |
| MED | Tail-Robustness-Metriken: 2-Wochen-Live-Tracker fehlt | Hook in nightly-Shadow-Replay-Cron |
| LOW | Ticker-Alias-Map hardcoded in parser.py (IBO, IMG, SELLAS) | Konfig-File + DB-Migration bei Bedarf |
| LOW | Review-Queue-Cursor unklar (UI-Session ≠ CSV-Progress) | 1-File mit aktuellem Cursor, UI-persistent |

---

## Summary

**Health-Grade: A−.** Bot ist stabil, Tests grün, DB-Konsistenz gegeben, keine offenen Positionen. Haupt-Risk-Items:
1. **Tail-Dependency-Warnung** im Param-Sweep jetzt dokumentiert — Edge ist tail-driven, Median-Edge marginal
2. **5 Parser-A2-Flags auf OFF** — entwickelt, aber nicht aktiviert. Regression-Run zeigte keinen Edge
3. **`test_simulation.py` im Root** — kleiner Struktur-Defect

**Ready for:** Review-Batch-Preparation (Task #82), Daily-Note 2026-04-19 (#81), Abschlussbericht.
