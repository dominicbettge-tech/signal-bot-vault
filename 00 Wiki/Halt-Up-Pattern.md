---
title: Halt-Up-Pattern
type: pattern
tags: [trading, halt-up, validated-edge]
created: 2026-04-20
updated: 2026-04-20
---

## Summary

**Halt-Up** = Trading-Pattern bei dem ein Ticker nach Trading-Halt mit Aufwärts-Gap wieder eröffnet. Bei [[Jack-Sparo]] häufig gecallt, vom [[Signal-Bot-MOC|Signal Bot]] mit **Autoskim + Peak-TSL**-Strategie adressiert. **Aktuell stärkste validierte Edge** im System (Stand 2026-04-20).

## Validierte Metriken

| Corpus | n | Mean P&L | Win-Rate |
|:-|:-:|:-:|:-:|
| Original (Halt-Up-Sim 2026-04-18) | 53 | +39.38% | 94.3% |
| Extended (Batch-Ticker-Sim 2026-04-20) | 37 Halt-Up Winner | +4.29% | — |
| Jack-Hold Baseline (Vergleich) | 37 | −9.76% | — |
| **Edge** | — | **+14.05pp** | **+47pp vs Jack-Hold** |

Cross-Corpus Gate PASSED auf allen 3 Kriterien (Mean-Δ, Win-Δ, MaxLoss).

## Strategie-Details

- **Autoskim** — partial profits ab bestimmter Peak-Distanz
- **Peak-TSL** — Trailing-Stop folgt Peak, nicht Entry
- **Position-Size** — 20% Bankroll default
- **Live-Status (2026-04-20)** — als Paper-Gate aktiviert, 23:40 CEST Monitor läuft

## Related

- [[02 Projekte/Signal Bot Halted-Up-Sim-2026-04-18|Halted-Up-Sim Details]]
- [[Signal-Bot-MOC]]
- [[Ticker-Klassifikator-MOC]] — Klassifikator erkennt Halt-Up-Ticker
- [[Jack-Sparo]] — häufigster Caller dieses Patterns

## Externe Referenzen

- Memory: `project_halt_up_autoskim_peak_tsl.md`
- Memory: `project_batch_ticker_sim_2026_04_20.md`
- Report: `signal_bot/reports/night_20260420_batch_tickers_perf.md`
