---
title: Signal Bot MOC
type: moc
tags: [signal-bot, map-of-content]
created: 2026-04-20
updated: 2026-04-20
---

## Summary

Map of Content für alle Signal-Bot-bezogenen Notizen im Vault. Ein zentraler Einstiegspunkt statt 50+ Orphan-Notes. Signal Bot v3 = automatisierter US-Aktienhandel auf Basis von [[Jack-Sparo]]-Telegram-Signalen über [[IBKR-Paper-Trading]].

## Core Docs

- [[02 Projekte/Signal Bot|Signal Bot]] — Hauptprojekt-Doku
- [[02 Projekte/Signal Bot Fehler-Log|Signal Bot Fehler-Log]] — alle Bugs
- [[02 Projekte/Signal Bot Live-Roadmap|Signal Bot Live-Roadmap]]
- [[02 Projekte/Signal Bot — Ehrliche Bewertung 2026-04-13|Ehrliche Bewertung]]
- [[02 Projekte/Signal Bot Deep-Dive Audit 2026-04-19|Deep-Dive Audit]]
- [[02 Projekte/Signal Bot External Critique 2026-04-19|External Critique]]

## Simulations

- [[02 Projekte/Signal Bot ATR-TSL-Sim|ATR-TSL-Sim]]
- [[02 Projekte/Signal Bot Combined-Filter-Sim|Combined-Filter-Sim]]
- [[02 Projekte/Signal Bot Entry-Latency-Sweep|Entry-Latency-Sweep]]
- [[02 Projekte/Signal Bot Filter-Grid-Sim|Filter-Grid-Sim]]
- [[02 Projekte/Signal Bot Full-Corpus-Sim-2026-04-18|Full-Corpus-Sim 2026-04-18]]
- [[02 Projekte/Signal Bot Halted-Up-Sim-2026-04-18|Halted-Up-Sim]] → siehe [[Halt-Up-Pattern]]
- [[02 Projekte/Signal Bot Hybrid-Exit-Sim|Hybrid-Exit-Sim]]
- [[02 Projekte/Signal Bot Price-Alert-Sim-2026-04-18|Price-Alert-Sim]]
- [[02 Projekte/Signal Bot R15-Subset-Sim|R15-Subset-Sim]]
- [[02 Projekte/Signal Bot RSI-5min-Exit-Sim|RSI-5min-Exit-Sim]]
- [[02 Projekte/Signal Bot RSI-Peak-Exit-Sim|RSI-Peak-Exit-Sim]]
- [[02 Projekte/Signal Bot Staggered-Entry-Sim|Staggered-Entry-Sim]] + [[02 Projekte/Signal Bot Staggered-Entry-Comparison-2026-04-18|Comparison 2026-04-18]]
- [[02 Projekte/Signal Bot TP-Ladder-Variations|TP-Ladder-Variations]]
- [[02 Projekte/Signal Bot TSL-Grid-Sim-2026-04-18|TSL-Grid-Sim]] + [[02 Projekte/Signal Bot TSL-Sweep|TSL-Sweep]]
- [[02 Projekte/Signal Bot VWAP-Break-Exit-Sim|VWAP-Break-Exit-Sim]] + [[02 Projekte/Signal Bot VWAP-Entry-Filter-Sim|VWAP-Entry-Filter-Sim]]
- [[02 Projekte/Signal Bot Volume-Climax-Exit-Sim|Volume-Climax-Exit-Sim]]
- [[02 Projekte/Signal Bot Walk-Forward|Walk-Forward]]
- [[02 Projekte/Signal Bot Indikator-Sim Masterübersicht 2026-04-17|Indikator-Sim Masterübersicht]]
- [[02 Projekte/Signal Bot Grid-Optimizer|Grid-Optimizer (Massiv-Sim)]]
- [[02 Projekte/Signal Bot Task-45-Extend-Scope-Corpus-2026-04-18|Task-45 EXTEND-Scope Corpus]]

## Implementation Plans & Architektur

- [[Loop-Orchestrator]] — autonomes Lern-System (Miss-Event → Opus-Hypothese → Corpus-Sim → Ship-Gate → PENDING)
- [[02 Projekte/H9 Opportunistic-Open-Buy — Implementierungsplan|H9 Opportunistic-Open-Buy Plan]]
- [[02 Projekte/Testcenter — Architektur v2|Testcenter Architektur v2]]
- [[02 Projekte/Orphan Protection Kalibrierung|Orphan-Protection Kalibrierung]]

## Edge-Audits

- [[02 Projekte/Signal Bot Jack-Edge-Audit|Jack-Edge-Audit]]
- [[02 Projekte/Signal Bot Jack-Exit-Matrix|Jack-Exit-Matrix]]
- [[02 Projekte/Signal Bot Jack-Slippage-Matrix|Jack-Slippage-Matrix]]
- [[02 Projekte/Signal Bot Premarket Deep-Dive|Premarket Deep-Dive]]
- [[02 Projekte/Signal Bot Regime-Diagnostic|Regime-Diagnostic]]
- [[02 Projekte/Signal Bot Time-of-Day|Time-of-Day]]
- [[02 Projekte/Signal Bot Survival-Check Combined-Filter|Survival-Check]]
- [[02 Projekte/Signal Bot — TGL Deep Dive & Acceleration-TSL|TGL Deep Dive]]
- [[02 Projekte/Signal Bot — Nicht-Tradebar Analyse 2026-04-13|Nicht-Tradebar Analyse]]
- [[02 Projekte/Signal Bot — Simulation nach Fixes 2026-04-13|Simulation nach Fixes]]

## Related Concepts

- [[Parser-MOC]] — alles rund um Signal-Parser
- [[Ticker-Klassifikator-MOC]] — Phase-1/2 Klassifikator
- [[IBKR-Paper-Trading]] — Ausführungs-Backend
- [[Jack-Sparo]] — Signal-Quelle
- [[Halt-Up-Pattern]] — validiertes Strategie-Pattern
- [[Hermes-Gateway]] — Telegram-Front-End (Delegation-Target)
- [[GPT-Code-Review-Findings]] — 8-Runden GPT-Kritik an `signal_manager.py`

## Code-Referenz

`/root/signal_bot/` — siehe `/root/signal_bot/CLAUDE.md` für Architektur.

## Research & Tooling

- [[Research/GitHub-50-Tools|GitHub — 50 beste Tools für unsere Projekte]] — Tier-1/2/3 Ranking
- [[04 Ressourcen/Claude Code Tools/Multi Agent Setup|Multi-Agent Setup]] — Zwei Claude-Code-Instanzen parallel
