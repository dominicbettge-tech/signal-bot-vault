---
title: Loop-Orchestrator
type: architecture
tags: [signal-bot, architecture, loop, hermes, learning-loop]
created: 2026-04-20
updated: 2026-04-20
status: shipped
---

## Summary

Der **Loop-Orchestrator** ist das autonome Lern-System des [[Signal-Bot-MOC|Signal-Bot v3]]. Es nimmt missed-trade-Events (und perspektivisch closed-trade-Events), schlägt per Opus 4.7 einen Knob-Fix aus einer 12-Key-Whitelist vor, validiert diesen gegen das 272-Ticker-Polygon-Corpus mit dem B-Standard-Ship-Gate, und queued bestandene Vorschläge als PENDING-Proposals für User-Review im morgendlichen Telegram-Digest.

**Zero-Auto-Deploy**: Jeder Knob-Change braucht explizite User-Genehmigung per `/loop approve` + `/loop apply`.

## Kern-Prinzip (Hermes-Lessons)

LLM proposes → **deterministic gate decides**. Das Ship-Gate ist der Regel-basierte Entscheider; Opus darf nur Hypothesen generieren, niemals selbst evaluieren (siehe [[Hermes-Gateway]] für die selbst-evaluations-Falle, die wir damit umgehen).

Drei Hermes-Integrationen aktiv:
- **Hermes-A** — `loop_rejected_hypotheses`-Tabelle + dialektischer Prior-Context: Opus sieht beim nächsten Versuch, welche Knobs bereits abgelehnt wurden, und darf diese NICHT erneut vorschlagen.
- **Hermes-B** — Reflect-Mode: Opus synthesiert im Daily-Digest eine 3-5-Satz-Pattern-Zusammenfassung über den PENDING-Stack. Läuft NACH dem Ship-Gate → kann Acceptance nicht beeinflussen.
- **Hermes-C** — Recovery-Hints auf dem Classifier: `needs_gate_sim` / `defer_to_human` / `auto_retry_later` routen je nach Abort-Reason, ob der Corpus-Sim überhaupt aussagekräftig wäre.

**Applied-Knob-Lock**: Hypothesen-Prompt listet aktuell live-gesetzte Knobs als "NICHT zurücksetzen" — verhindert silent-rollback von User-approved Änderungen.

## Pipeline (pro Event)

```
missed_trade-Event
  ↓
1. replayer.replay_message()     — parser + gate-chain dry-run
  ↓  reached_stage, abort_reason
2. classifier.classify_replay()  — root_cause + candidate_knobs + hints
  ↓  (defer_to_human? → skipped)
3. hypothesis.generate()         — Opus-4.7 schlägt 1-2 Knobs vor
  ↓  (dialectic prior + applied-locks im Prompt)
4. simulator.simulate_corpus()   — 272-Ticker Polygon train/test
  ↓  SimResult (baseline_mean, candidate_train, candidate_test, max_dd, trim_top3_holds, ...)
5. ship_gate.evaluate()          — B-Standard-Thresholds
  ↓  (passed? → ship-gate-ok-PENDING; failed? → failed-PENDING + persist rejected)
6. queue_db.insert_proposal()    — status=PENDING
```

## Ship-Gate Thresholds (User-confirmed 2026-04-20)

- Train-Lift ≥ **+5%** (immer)
- Test-Lift ≥ **+3%** bei 1-Knob, **+5%** bei 2-Knob
- Tickers-Improved ≥ **3** bei 1-Knob, **4** bei 2-Knob
- Max-DD-Tolerance: Kandidat darf Baseline-DD nicht um mehr als 10% absolut verschlechtern
- `trim_top3_holds` muss True sein — schützt vor outlier-driven Ergebnissen
- `n_trades ≥ 30`

⚠️ **Bekannte Methodik-Frage** (2026-04-20): `trim_top3_holds` vergleicht *trimmed candidate vs full-mean baseline*, nicht symmetrisch. Das 272-Ticker-Corpus ist penny-stock-lastig (baseline_mean +42.9%, 3 Mega-Winner tragen alles), was alle Knob-Sweeps gegen diese Asymmetrie verlieren lässt. Siehe Findings-Doc.

## Whitelist (12 Keys, 8 Groups)

Aus `loop/models.py:WHITELIST_KEYS`:
- **Parser**: `MIN_CONFIDENCE`
- **Gate**: `OVERSOLD_SKIP_BUFFER`, `MAX_OPEN_POSITIONS`
- **TSL**: `TRAILING_SL_PERCENT`, `TRAILING_SL_ACTIVATION_PERCENT`
- **TP**: `TAKE_PROFIT_PERCENT_1/2/3`
- **Timing**: `EXPIRY_MINUTES`
- **Staggered-Entry**: `STAGGERED_ENTRY_LEVELS/OFFSETS/SIZES`

Gate-level Knobs (`MIN_CONFIDENCE`, `MAX_OPEN_POSITIONS`, `OVERSOLD_SKIP_BUFFER`, `EXPIRY_MINUTES`, `STAGGERED_ENTRY_*`) sind nicht via Corpus-Sim validierbar → Classifier setzt `needs_gate_sim=True` → Queue landet als NEEDS_MANUAL.

## Files

- `loop/orchestrator.py` — Daemon, run_tick, run_forever, process_event
- `loop/extractor.py` — miss/trade-Events aus `trades.db` (cursor-basiert)
- `loop/replayer.py` — dry-run durch parser + gate-chain
- `loop/classifier.py` — abort_reason → (root_cause, candidate_knobs, hints)
- `loop/hypothesis.py` — Opus-CLI Wrapper (Max-Account, nicht API), dialectic prior
- `loop/simulator.py` — sim_engine-Wrapper gegen pairs_train/test.json
- `loop/ship_gate.py` — B-Standard Thresholds
- `loop/queue_db.py` — CRUD für loop_proposals + loop_rejected_hypotheses + loop_state
- `loop/reporter.py` — Daily-Digest (Vault-Markdown + Telegram + Reflect-Mode)
- `loop/models.py` — Dataclasses (Hypothesis, SimResult, ReplayResult, Proposal) + Whitelist

## Telegram-Commands (`/loop`)

- `/loop status` — Service-State, Cursor, PENDING/APPROVED/APPLIED/REJECTED-Counter
- `/loop proposals` — Top 10 PENDING (gate-ok ✅ / failed ⚠️)
- `/loop approve <id>` — PENDING → APPROVED
- `/loop reject <id>` — PENDING → REJECTED + persist in `loop_rejected_hypotheses` (dialektischer Prior)
- `/loop apply <id>` — APPROVED/PENDING → APPLIED (live übernommen, Applied-Lock aktiv)
- `/loop digest` — Force-Run Daily-Digest
- `/loop start` / `/loop stop` — systemctl für `signal-loop.service`

## Service

- **systemd-Unit**: `/etc/systemd/system/signal-loop.service`
- **Launcher**: `python3 -m loop.orchestrator`
- **Logs**: `/root/signal_bot/logs/loop_orchestrator.log`
- **Poll**: 300s (5 min)
- **Digest-Time**: 08:00 Europe/Berlin
- **Restart**: on-failure, RestartSec=30
- **KillSignal**: SIGTERM, TimeoutStopSec=120 (Opus-CLI darf sauber zu Ende)

## DB-Tabellen

- `loop_proposals` — Haupt-Queue, status PENDING/APPROVED/REJECTED/APPLIED
- `loop_rejected_hypotheses` — dialektischer Prior für Opus (Hermes-A)
- `loop_state` — key-value store (cursor unter key `last_cursor`)

## Bootstrap

`scripts/loop_bootstrap.py [--limit N] [--no-set-cursor]` — processed alle historischen `missed_trades`-Rows newest→oldest, setzt cursor auf NOW wenn fertig. Einmal vor erstem Service-Start.

## Tests

`tests/test_loop_*.py` (59 Tests, alle grün):
- `test_loop_models.py` — Whitelist, Hypothesis-Validation
- `test_loop_queue_db.py` — CRUD + Rejected-Tabelle (Hermes-A)
- `test_loop_classifier.py` — abort_reason-Mapping + Recovery-Hints (Hermes-C)
- `test_loop_replayer.py` — parser + gate-chain dry-run
- `test_loop_hypothesis.py` — Prior-Context + Applied-Locks im Prompt
- `test_loop_extractor.py` — cursor-based event extraction
- `test_loop_simulator.py` — gate-level-knob NotImplementedError
- `test_loop_ship_gate.py` — B-Standard-Thresholds
- `test_loop_reporter.py` — Digest + Reflect-Mode (Hermes-B)
- `test_loop_orchestrator.py` — end-to-end pipeline + ATOS-Exit-Regression

## Docs

- [[02 Projekte/Loop-Orchestrator Nacht-Seed 2026-04-20|Nacht-Seed 2026-04-20]] — 15-Hypothesen-Sweep + Corpus-Anomalie-Finding
- [[05 Daily Notes/2026-04-21|2026-04-21 Morning-Briefing]]

## Verwandte Konzepte

- [[Hermes-Gateway]] — Self-Evaluations-Falle die wir mit "LLM proposes / gate decides" umgehen
- [[Jack-Sparo]] — Signal-Quelle, deren Misses gelernt werden
- [[Halt-Up-Pattern]] — erfolgreich gelerntes Profit-Lock-Pattern (bereits live, Validierungs-Referenz)
- [[IBKR-Paper-Trading]] — Execution-Layer
