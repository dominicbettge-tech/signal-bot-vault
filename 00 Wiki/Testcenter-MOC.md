---
title: Testcenter
type: moc
tags: [testcenter, parameter-optimizer, signal-bot, simulation, rule-engine]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**Testcenter** ist die Backtest- + Rule-Validation-Infrastruktur des [[Signal-Bot-MOC|Signal-Bots]] — pure-function-Engine mit YAML-Rules, 610 Fixtures (152 core, 458 noise), `decisions_db` für Observability + 132 Tests grün. Dient zwei Zwecken: (1) Phase-1-Evaluation der R1-R9-Rules vor Live-Deployment, (2) langfristig evolutionärer Parameter-Optimizer für SL/TP/TSL/Entry-Offsets/Sizing über alle historischen Trades. Stand 2026-04-15: Phase-1 komplett (7 Module, 132 Tests), Phase-A Runner+Fast-Pass-UI in Build, Reviews + Sweeps Phase-B/C pending. Pfad: `/root/signal_bot/testcenter/`.

## Aktueller Stand (2026-04-25)

- **Phase-1:** komplett (7 Module, 132 Tests grün, 2026-04-14)
- **Phase-A:** Clean-Baseline gesetzt, Runner-Script + Fast-Pass-UI im Build
- **Engine-Status:** R1, R2, R3, R4, R6, R7, R8 live, R5/R9 deferred (brauchen chart-OCR + Timestamp-Logic)
- **Korpus:** 610 Fixtures (152 core, 458 noise) aus reviewed Messages
- **Backend-Plan:** Architektur Opus, Ausführung Kimi 2.5 / Ollama (kostenlos)
- **Voraussetzung:** Parser-Review fertig — DB sauber, Reverse-Splits bereinigt

## 7 Module (Phase-1)

| # | File | Tests | Funktion |
|---|------|---:|----------|
| 1 | `build_rules.py` | 9 | Memory-MD → `rules.yaml` (9 Rules, Drift-Detection) |
| 2 | `build_fixtures.py` + `fixtures.py` | 12 | DB → 610 YAML-Fixtures |
| 3 | `features.py` | 37 | Feature-Bundle §7, 7 Soft-Keyword-Kategorien, MIST-Veto |
| 4 | `regime.py` | 33 | VIX/SPY-Buckets, Phase-2f-Thresholds |
| 5 | `engine.py` | 15 | Rule-Match + Priority-Ladder + Falling-Knife-Veto |
| 6 | `safety.py` | 22 | 7 Circuit-Breakers (pure fns, state-dict) |
| 7 | `decisions_db.py` | 4 | SQLite-Observability pro evaluate()-Call |

**Pfad:** `/root/signal_bot/testcenter/`. Tests: `python3 -m unittest test_*`.

## Architektur-Entscheidungen (sakrosankt)

- **Pure-Function-Pattern** durchgängig — keine Klassen, alle Module testbar ohne Mocks
- **Feature-Bundle §7** composable: text/chart/context/regime/precedent_features Top-Level
- **rules.yaml** = Metadaten (status/action/evidence), Matching-Logik in `engine._MATCHERS`
- **Priority-Ladder:** R8(100) > R9(90) > R3(80) > R1(60) > R5(55) > R2(50) > R6(40) > R4(30) > R7(20)
- **Falling-Knife-Veto** = globaler Kill-Switch, überstimmt Priority-Ladder
- **Active-Status-Filter** = `{Validated, Candidate+}` default, Candidate logged but not fired
- **State-Dict** für safety.py statt Controller-Objekt — Replay-kompatibel
- **Fixture-Immutability** sakrosankt nach Commit (`--force` bricht bewusst)

## Integration-Sweep (610 Fixtures)

- **b-Verdicts (n=88):** 97.7% Fire-Rate, R2 dominiert → Adaptive-Stack greift
- **n-Verdicts (n=286):** 20.6% Fire-Rate → Engine diskriminiert Noise korrekt
- **R3 Distress-TSL:** genau 1× getriggert (NCPL-4014) — exakt wie Memory vorhersagt
- **Falling-Knife-Veto:** 1× (MIST-235) — kanonischer Case bestätigt
- **Soft-Score avg:** b=0.68, e=0.67, n=0.66, s=0.61, **w=1.45** (Warnsignal-Funktion bestätigt)

## 4-Phasen-Plan (User-Direktive 2026-04-14)

### Phase A — Build (~1.5h fokussiert)

1. Runner-Script (`testcenter/run_daily.py`) TDD
2. Invariant-Checker: Coverage / Precision / Per-Rule-Ratio
3. Outcome-Attacher: joined `decisions_db` mit `polygon_data.db` (9.685.426 1m-Bars) → PnL pro Match
4. Report-Writer: Markdown nach `testcenter/reports/YYYY-MM-DD.md`
5. **Fast-Pass-UI** (`testcenter/fast_review.py`) — y/n/Korrektur, Ziel 120 Verdicts/h statt 12/h
6. Cron: `0 23 * * * cd /root/signal_bot/testcenter && python3 run_daily.py >> logs/runner.log 2>&1`

### Phase B — Reviews + Hintergrund (Tag 2-7)

- User: Reviews wie gewohnt
- Hintergrund: Runner läuft 23:00 autonom, neue Verdicts → Fixtures via `build_fixtures.py`
- Morgens 5min Report-Check
- VERBOTEN: TZ-Code während Review-Session, Parameter-Sweeps (Phase C), neue Engine-Features

### Phase C — Sweeps (~2-3 Tage nach Review-Ende)

1. `build_rules.py` neu (inkl. neuer R10+)
2. **Negative-Controls (§K)** — Leak-Detektoren, müssen clean sein BEVOR optimiert
3. Walk-Forward-Harness (Train/Val chronologisch getrennt)
4. **Tier-1 Parameter-Sweeps:** `tsl_day_pct`, `tp_ladder_split_a`, `base_position_pct`, `hard_dd_cap_pct`, `falling_knife_thresholds`
5. Hypothesis-driven (§J), nicht blind
6. Meta-Archiv-DB (`experiments.db`) für Reproduzierbarkeit

### Phase D — Live-Integration (~2 Tage)

1. Signal-Bot-Code gegen TZ-Optima updaten
2. Shadow-Mode 1 Woche: alt entscheidet, neu vergleicht, **nicht ausführen**
3. Metrik-Vergleich + explizite User-Freigabe
4. Live-Schaltung mit kleinem Budget zuerst

## Geplante Features (21 R-Hypothesen)

Aus `project_testcenter.md` (vor-Review-Stand):

1. **Staggered Entry Backtest** (Entry +0.5%/+1%/+1.25%)
2. **Parameter-Optimizer** (evolutionär, 100+ Generationen)
3. **Volatilitäts-basierter TSL** (X × ATR)
4. **Averaging-Strategie** (Reserve-Budget, SL-Anpassung)
5. **"Secure Profit" Regel** (X% Market Sell + TSL auf Rest)
6. **"Around X" Entry-Offset**
7. **Dynamische Positionsgröße** (Trade-Type-spezifisch + Kelly)
8. **"Halted up" als Trigger** (CMBM +85%/+201% Evidenz)
9. **Validity ignorieren / Sofortkauf** (CYPH +41%, AKBA +8.9%, VSTM +26%, SLRX +180%, WHLR +105%)
10. **Sentiment-Modifier** (bearish/risky-Keywords)
10b. **Mid-Trade Risk Warnings** (KALA, KTTA Evidenz)
11. **Red-Flag-Ankündigungen**
12. **RSI als Exit-Indikator** (>70-80)
13. **Watchlist-Entry Filter** (Low Float + Penny Stocks)
14. **Watchlist-Mention als Entry** (VSEE +266%)
15. **Jack's "private Trades"** (FRGT +14.6%)
16. **Monster-Ticker Profil** (INHD +296%, MTC +700%, CMBM +450%)
17. **TSL schlägt Jack's manuelle SL** (GNS +56%, AMIX +47%)
18. **Slot-Opportunitätskosten / Max-Haltezeit**
19. **"Valid till further notice" / GTC-Orders** (GNS +26%)
20. **Breakeven-Lock + Delayed TSL** (Strategie D — CETX +100.4%)
21. **Monster-Score als Entry-Filter + Strategie-Wähler** (5-Punkte-System, RSI/ATR/Vol/Range/Keywords)

## Unveränderliche Regeln

- **Reviews haben Vorrang** — TZ-Arbeit darf Review-Qualität NIE beeinträchtigen
- **Runner muss deterministisch bleiben** — kein LLM in der Schleife, kein Kimi, kein Ollama in Runner
- **Phase-A erst KOMPLETT** vor Phase-B-Start
- **Negative-Controls clean** vor Sweeps
- **API-Key 2026-04-14 exponiert** → muss regeneriert werden vor Cron-Aktivierung

## Nächste Schritte (Build-Manifest §3+)

1. Runner-Script (610 Fixtures Batch)
2. Outcome-Tracker (decisions.id ↔ simulated_trades.id)
3. Drift-Monitor (rolling window vs Baseline)
4. Validation-Pipeline §H (Walk-Forward Train/Val)
5. Chart-Features (Vision-OCR für StockMaster-Charts) — Backlog `project_chart_ocr_range_validator.md`
6. R5/R9 Matcher (nach Chart + Timestamp-Helper)
7. Live-Integration: parser.py + signal_manager.py gegen TZ-Module

## Memory-Detail-Files

- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter.md` — Vor-Review-Plan + 21 R-Hypothesen
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_architecture.md` — Architektur v2
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_4phase_plan.md` — 4-Phasen verbindlich
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_phase1_complete.md` — Phase-1 (7 Module / 132 Tests)
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_phase_a_complete.md` — Phase-A
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_phase_a_clean_baseline.md` — Clean-Baseline
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_intraday.md` — Intraday-Layer
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_backlog_2026_04_15.md` — Backlog
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_2026_04_15_evening_handover.md` — Handover
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_r_hypotheses.md` — R-Hypothesen
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_halted_up_autosell.md` — Halt-Up-Strategy
- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_price_alert_as_entry.md` — Price-Alert-Entry
- `/root/.claude/projects/-root-signal-bot/memory/project_priority_review_before_testcenter.md` — Reviews-vor-TC

## Related

- [[Signal-Bot-MOC]] — Container-Bot
- [[Parser-MOC]] / [[Parser-V2-MOC]] — Verdicts → Fixtures-Pipeline
- [[Review-Workflow-MOC]] — Verdict-Source für Fixtures
- [[Auto-Research-MOC]] — Strategy-Evolution-Pendant (Karpathy-Loop)
- [[KAPPI-MOC]] — TP-Optimization-Pendant
- [[Halt-Up-Pattern]] — eines der Test-Patterns
- [[Jack-Sparo]] — Korpus-Quelle
