---
title: GPT Code-Review Findings
type: concept
tags: [code-review, external-llm, signal-bot]
created: 2026-04-20
updated: 2026-04-20
sources: [[02 Projekte/GPT Code-Review Vorschläge 2026-04-18|GPT Code-Review Vorschläge 2026-04-18]]
---

## Summary

8 Runden GPT-Kritik an `signal_manager.py` und der [[Signal-Bot-MOC|Signal-Bot]]-Gesamt-Architektur. Resultat: **6 ACCEPT-Items (A-F)**, 3 **LATER** (erst Sim im Testcenter), **6 REJECT** (Missverständnisse: LOC als God-Class, SQLite→Postgres, In-Memory-active_trades, Hardcoded-Shares-Irrtum).

## Details

### ACCEPT (Priorität)

| # | Item | Warum | Effort |
|:-:|:-|:-|:-:|
| A | Unit-Tests für `signal_manager.py` | P/R-Regression ohne Live-Bot | 2-3h |
| B | Concurrency/Dedup Integration-Test | Simuliert parallele Signals | 30min |
| C | IBKR `safe_call` Wrapper (Retry+Timeout) | Konsolidiert existierende Error-201-Retry-Logik | 30min |
| D | Isotonic-Regression Calibration | ECE 0.38 → <0.10 Ziel | 1h |
| E | Parser-Flags-Regression Smoke-Test | Script existiert, Run pending (~$2 API) | 1h |
| F | `asyncio.Lock` per Ticker | 20 LOC gegen gleichzeitige Signals | 20min |

### REJECT — und warum GPT sich irrte

| REJECT | Grund |
|:-|:-|
| Core-Rebuild bot/core/ | Dispatcher-Pattern ist sauber, 422 LOC ist kein God-Class |
| SQLite → PostgreSQL | SQLite passt für Single-VPS, Crash-Recovery-Vorteil |
| In-Memory `active_trades` dict | DB als Source-of-Truth ist Feature, nicht Bug |
| Hardcoded `shares = int(1000/price)` | ignoriert `POSITION_SIZE_PERCENT` + `MAX_BANKROLL_USD` config |
| `len(self.trades) < 3` hardcoded | ignoriert `MAX_OPEN_POSITIONS` config |

### Meta-Learnings

- Externes LLM sieht Code ohne Config-Kontext — projiziert „smells" die Configs längst regeln.
- GPT-Runden 1-4 liefern den Grossteil des Value, Runden 5-8 wiederholen + halluzinieren Architektur-Änderungen.
- **Regel:** Code-Review-Findings ins Vault, aber jedes Item gegen `.env` + Dispatcher-Flow gegenprüfen BEVOR man ACCEPT setzt.

## Related

- [[Signal-Bot-MOC]] — Ziel des Reviews
- [[Parser-MOC]] — separater Review-Scope
- [[Chase-AI-Insights]], [[Matt-Pocock-Principles]] — YT-basierte Reviews als Gegenpol

## History / Log

- 2026-04-18: 8 GPT-Runden durchgearbeitet, Verdicts final
- 2026-04-20: Ingest ins Wiki
