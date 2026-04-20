---
title: Parser MOC
type: moc
tags: [parser, signal-bot, map-of-content]
created: 2026-04-20
updated: 2026-04-20
---

## Summary

Map of Content für alle Parser-bezogenen Notizen. Parser = Claude-basierter Signal-Extractor der [[Jack-Sparo]]-Telegram-Nachrichten in strukturierte Orders übersetzt. Code: `/root/signal_bot/parser.py` + `parser_rules.py`.

## Review-Queues

- [[02 Projekte/Parser Rebuild — Phase B Review Queue|Phase B Review Queue]]
- [[02 Projekte/Parser Rebuild — Phase B Review Queue v2|Phase B Review Queue v2]]
- [[02 Projekte/Parser Rebuild — Stress Test Phase A|Stress Test Phase A]]
- [[02 Projekte/Parser Review Trade Simulationen|Parser Review Trade Simulationen]]

## Analyses

- [[02 Projekte/Parser-Analyse 100 Nachrichten|Parser-Analyse 100 Nachrichten]]
- [[02 Projekte/Parser-Regeln Synthese|Parser-Regeln Synthese]]
- [[02 Projekte/Signal Bot Parser-Accuracy-6Path-2026-04-18|Parser-Accuracy 6-Path 2026-04-18]]

## Implementation Plans

- [[02 Projekte/Parser Ticker-Miss-Fix — Implementierungsplan|Ticker-Miss-Fix Plan]]
- [[02 Projekte/Parser Zone-Trade Extractor — Implementierungsplan|Zone-Trade Extractor Plan]]
- [[02 Projekte/Parser Review/Signal Thread Architektur|Signal Thread Architektur Plan]]

## Review-Batches (Parser Review/)

- [[02 Projekte/Parser Review/Batch_Review_2026-04-18|Batch-Review 2026-04-18]]
- [[02 Projekte/Parser Review/Review-Batch-2026-04-19 — README|Review-Batch 2026-04-19 (252 Messages)]]
- [[02 Projekte/Parser Review/Ticker Queue|Ticker Queue]]

## Per-Ticker Reviews

- [[02 Projekte/Parser Review/Ticker/NCPL|NCPL]] (+ [[02 Projekte/Parser Review/Ticker/NCPL_full_dump_3998-4401|NCPL Full-Dump #3998-#4401]])
- [[02 Projekte/Parser Review/Ticker/ORKT|ORKT]]
- [[02 Projekte/Parser Review/Ticker/SLS|SLS]]

## Related Concepts

- [[Signal-Bot-MOC]] — Parent-MOC
- [[Ticker-Klassifikator-MOC]] — nachgelagerter Klassifikator
- [[Karpathy-LLM-Wiki]] — Pattern das wir fürs Wiki nutzen

## Milestones (Parser-History)

- **2026-04-20** — Phase-1 Bundle shipped (ENTRY_CONDITIONAL-Taxonomy + Watchlist-Strictness + Averaging-Phrases). 7/7 Tests grün.
- **2026-04-18** — Baseline gemessen (6-Path-Accuracy).
