---
title: Parser V2
type: moc
tags: [parser, parser-v2, rule-based, signal-bot, pattern-db]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**Parser V2** ist der rule-based Pre-Filter vor dem Claude-LLM-Cascade des [[Signal-Bot-MOC|Signal-Bots]]. Drei-Layer-Architektur (Pattern-DB → Intent-Detect → Regex-Backstop) plus Hard-Fix-Layer (A/B/C/D/E/F) und Safety-Filter — fängt 67 Corpus-Idiome ohne API-Call. Ergänzt — nicht ersetzt — den klassischen [[Parser-MOC|Parser]]: V2 entscheidet `skip_llm | review | ignore`, der LLM bekommt nur die `review`-Bucket. Stand 2026-04-25: Accuracy 55.69% / recall_b 73% nach Splitter-Fix.

## Aktueller Stand (2026-04-25)

- **Pipeline:** Pattern-Match → Safety-Filter → Hard-Fix-Layer → Intent-Mapping
- **Pattern-DB:** `kairos_output/parser_patterns.json`, 67 Corpus-Idiome
- **Hard-Fix-Gruppen:** A (w→b Leak), B (Missed Entries/Adds), C (Missed Exits), D (Noise), E (Decisive Trade Templates, neu 2026-04-25), F (Recap/Alert-Precision-Guard, neu 2026-04-25)
- **Accuracy:** 55.69% (Pattern-only 33.33% → +Hardfix 37.33% → +Splitter+E/F 55.69%)
- **recall_b:** 73.15% (Baseline 37.04%, +36pp nach Splitter-Bug-Fix)
- **3-Schicht-Sicherheit:** Parser → Execution-Gate (conf≥0.80) → Kairos-Override (kc≥0.8 + Preis)
- **Setup-Path:** alert/watching/might-order → `trade_setups`-Tabelle, kein Sofort-Trade

## Komponenten

### Core-Module

- **`parser_v2/classifier_v2.py`** — Pattern-Match (`match_pattern`), Category→Intent-Mapping (46 Kategorien), Safety-Filter (`_apply_pattern_safety_filter`), `ClassificationV2`-Datenklasse
- **`parser_v2/hard_fix.py`** — 6 Regel-Gruppen A/B/C/D/E/F (post-Pattern, pre-Sub-Taxonomy)
- **`parser_v2/prefilter.py`** — `HARDFIX_WEAK_ENTRY_CAP=0.65`, force-review für starter/nibble-Marker
- **`parser_v2/extraction_v2.py`** — Ticker+Price-Regex-Backstop
- **`parser_v2/confidence.py`** — Confidence-Score-Aggregation
- **`parser_v2/message_splitter.py`** — Multi-Ticker-Split mit STOPWORD-Set (~30 Trading-Abkürzungen wie SL/TP/AH/ET/PM)

### Setup/Trigger-Engine (parallel-pfad)

- **`setup_detector.py`** (40 LOC) — `detect_setup(text)` keywords: alert, watching, if-it-hits, might+order
- **`setup_store.py`** (157 LOC) — async CRUD auf `trade_setups`-Tabelle
- **`trigger_engine.py`** (80 LOC) — `check_triggers(ticker, market_price, execute_cb)`, direction below/above
- **`signal_manager.py`-Hook** — vor `validate_for_execution`: setup→store, return (kein Gate)

### Learning-Loop

- **`parser_learning.py`** — `log_parser_mistake()` → `kairos_output/parser_mistakes.json`
- **`scripts/evaluate_parser.py`** — Eval mit Mistake-Logging
- **`scripts/analyze_mistakes.py`** — Top-N 2/3-grams, Rule-Suggestions → `parser_rule_suggestions.json` (Review-only, kein Auto-Apply)
- **`scripts/parser_v2_accuracy_audit.py`** — Audit gegen 1230 verdicted Jack-Messages aus `data/backtest_results.db`

## Top-5 Rules + 5 Core-Gesetze (2026-04-24)

| # | Rule | Implementation |
|---|---|---|
| 1 | uncertainty + NOT placed/filled/bought → update | hard_fix A-Soft, _DECISIVE_ACTION_RE |
| 2 | zone/area/around + NOT placed → update | hard_fix A-Soft (live) |
| 3 | starter/nibble/entered/took position + ticker → entry | hard_fix B + ticker-required Guard |
| 4 | no ticker + not reply-context → update OR noise | hard_fix D |
| 5 | word_count<4 + no ticker → noise | hard_fix D-Sub |
| Safety | starter/nibble entry → conf cap 0.65, never skip_llm | prefilter `HARDFIX_WEAK_ENTRY_CAP` |

**Core-Gesetze:** Intent>Wörter • Action>Sprache (placed/filled/bought schlägt Uncertainty) • Uncertainty kills Execution • Structure Required (ticker+action) • System>Parser (Gate+Override fängt was Parser durchlässt)

## Phasen-Historie

| Datum | Phase | Inhalt |
|---|---|---|
| 2026-04-24 | PATTERN-LAYER | 3-Layer-Architektur, 67 Idiome, w→b-Safety-Filter, Accuracy 10.67→33.33% |
| 2026-04-24 | HARD-FIX A/B/C/D | 4 Regel-Gruppen post-Pattern, 33.33→37.33% |
| 2026-04-24 | TOP-5 RULES | ChatGPT-Spec, decisive-action-Guard, ticker-required, conf-cap 0.65 |
| 2026-04-24 | LEARNING-LOOP | mistake-log + analyze_mistakes.py + 20 Suggestions aus n=94 |
| 2026-04-24 | SETUP/TRIGGER | detect_setup→store_setup→trigger_engine, parallel-pfad zu Gate |
| 2026-04-25 | TASK 19 RECALL-UPLIFT | Splitter-STOPWORDS + Hardfix E (Decisive Templates) + F (Precision-Guard), recall_b 37→73%, Accuracy 53.5→55.69% |

## Was bleibt offen

- **e-Klasse Recall stagniert (28%)** — "Filled at X" strukturell ambig (buy-fill vs sell-fill) → braucht Chain-Inheritance
- **ENTRY_AVERAGING-FPs** — Pattern-DB matcht zu früh auf "watching"/"adding zone"
- **u-Klasse 220 FPs** — AMBIGUOUS-Bucket bleibt Restmüll-Lager
- **trigger_engine.check_triggers()** noch nicht an `position_monitor` Price-Poll-Loop gewired
- **/setups Telegram-Command** für aktive Setup-Liste fehlt

## Memory-Detail-Files

- `/root/.claude/projects/-root-signal-bot/memory/project_parser_v2_pattern_integration_2026_04_24.md` — 3-Layer + Safety-Filter
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_v2_hardfix_and_learning_loop_2026_04_24.md` — Hard-Fix A/B/C/D + Learning-Loop
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_v2_top5_rules_2026_04_24.md` — Top-5 Rules + 5 Core-Gesetze
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_v2_setup_trigger_integration_2026_04_24.md` — Setup-Detect + Trigger-Engine
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_v2_task19_recall_uplift_2026_04_25.md` — Splitter-Bug-Fix + Hardfix E/F

## Related

- [[Signal-Bot-MOC]] — Container-Bot
- [[Parser-MOC]] — Vorgänger (Claude-LLM-Cascade), Parser_V2 schaltet vor
- [[Kairos-MOC]] — Override kommt nach Gate
- [[Jack-Sparo]] — Signal-Quelle, deren Idiome die Pattern-DB füllen
- [[Karpathy-LLM-Wiki]] — Inspirations-Pattern für Learning-Loop
- [[Ticker-Klassifikator-MOC]] — nachgelagerter Klassifikator
