---
title: Review-Workflow
type: moc
tags: [review, parser-review, verdict, signal-bot, learning-loop]
created: 2026-04-25
updated: 2026-04-25
---

## Summary

**Review-Workflow** ist der menschliche Verdict-Loop des [[Signal-Bot-MOC|Signal-Bots]] — Jack-Sparo-Telegram-Messages werden vom User in 6 Codes (b/e/x/s/w/n) klassifiziert, sofort persistiert, und füttern Parser- und Strategie-Lernschleifen. Seit 2026-04-19 End-to-End: **Bootstrap → Verdict → Edge → Sim → Rule → Commit → Report** in 7 Phasen, nicht mehr nur Verdict-Vergabe. Reviews enden mit adoptierten Rules, nicht mit Tabellen. Ticker-basiert (nicht chronologisch), Verdicts SOFORT via `save_verdict.py`, Self-Eval alle ≥50 Verdicts, Hit-Rate <70% = STOPP+Debug.

## Aktueller Stand (2026-04-25)

- **Methode:** Ticker-basiert (v3, ab 2026-04-13), nicht chronologische 10er-Blöcke
- **Verdict-Codes:** b/e/x/s/w/n + u (unklar) — niemals neue erfinden
- **Output-Format:** NUR Tabelle, Jack-Text 1:1 vollständig oben, Prosa max 2-3 Sätze
- **Persistenz:** `save_verdict.py` SOFORT, kein Batching (140 Verdicts am 12.04. verloren)
- **Self-Eval-Kadenz:** ≥50 neue Verdicts → kalibrieren VOR neuen Reviews
- **Verdict-Bias:** bei Zweifel `n`, nicht `s/w/x` (`feedback_verdict_noise_bias.md`)

## Verdict-Codes

| Code | Bedeutung | Beispiel |
|---|---|---|
| **b** | Buy/Entry | "placed order at 15.75" |
| **e** | Averaging/Nachkauf | "averaged more at 15.05" |
| **x** | Exit/Sell (auch partial) | "sold at 17.15", "closed 15%" |
| **s** | Status-Update | "back green", "at 16.55", "rebound above support" |
| **w** | Watchlist | "watching", "bull flag", "will share a trade" |
| **n** | Noise (kein Signal) | "enjoy team", "wow", "team" |
| **u** | Unklar (Fallback) | bei Zweifel zwischen Codes |

**Bias-Regel:** Bei Zweifel `n`, nicht `s/w/x` — Conservative-Default schützt Parser-Train-Set vor False-Positive-Drift.

## End-to-End-Workflow (7 Phasen, 2026-04-19+)

### Phase 1 — Bootstrap (vor erstem Verdict)

1. 6 Feedback-Files lesen: `noise_bias`, `verdict_codes`, `trade_type`, `soft_score`, `message_chain`, `output_compact`
2. `predict_verdict.py <msg_id>` pro Message (automatisiert 5-Step grounded-decisions)
3. Review-Status + nächster Ticker aus `project_review_pending_tickers.md`
4. Self-Eval-Kadenz-Check: ≥50 neue Verdicts seit letztem Run → Self-Eval vorher
5. Jack-Text IMMER 1:1 vollständig zeigen, NUR Tabelle ausgeben
6. Bar-Coverage-Check (`feedback_session_health_check_mandatory.md`)

### Phase 2 — Verdict-Assignment (pro Ticker)

1. Review-Tabelle: msg | UTC→ET | Type | Preis-zur-Uhrzeit | Text | Verdict
2. Verdicts SOFORT via `save_verdict.py` persistieren (kein Batching)
3. Chain-Display validieren
4. User setzt Tempo — NIE "nächster Ticker?" fragen

### Phase 3 — Edge-Detection (während/nach Ticker-Review)

Trigger-Signale:
- Jack's Exit war schlecht (Median-Verlust, Holding too long, Panic-Sell)
- Jack-Narrative ≠ Preis-Realität
- Wiederholendes Pattern (Halt-Up, Parabolic, Distress)
- User stellt Performance-Frage ("was wäre besser gewesen")

→ Trigger für Phase 4. Nicht User fragen welche Variante — autonom sim'en.

### Phase 4 — Sim-Validierung (autonom, 30-60min)

1. Pattern-Definition (z.B. "Halt-Up auf offener Position in Profit")
2. DB-Scan: n≥30 Fälle aus Korpus
3. Cross-Ticker ≥3 verschiedene Tickers Pflicht
4. Grid-Search: 5-10 Parameter-Kombinationen
5. Slippage-Stress: 0/25/50/100/200 bps
6. Robust-Metrik: Trim-Top-3 als Haupt-Score
7. Goal-Alignment-Score: gegen alte Default + Jack-Baseline
8. "Zahlen nur aus Quelle": frischer Sim-Run, keine Memory-Zitate

### Phase 5 — Commit (wenn Winner klar besser)

1. `config.py` Default ändern + Comment-Block mit n-basierten Numbers
2. Modul-Docstring updaten
3. Tests grün (`pytest tests/test_X.py`)
4. Memory-Update: `project_*.md` + MEMORY.md-Pin
5. Flag OFF bleibt Default — nur Parameter-Defaults, nicht Aktivierung

### Phase 6 — Paper-Gate (User-Entscheidung)

- Criteria definieren: Mean ≥ X% über Y+ Events
- Scripts reproduzierbar in `/root/signal_bot/scripts/`
- JSON-Artifacts für Audit-Trail

### Phase 7 — Report (an User, als Tabelle)

1. TL;DR-Tabelle: Alt vs Neu vs Jack-Baseline (Mean/Median/Win/MaxLoss/Δ)
2. Slippage-Tabelle für Robustheit
3. Top-5-Grid für Transparenz
4. Change-List: was committed (config/docstring/tests/memory)
5. Nächste Schritte: Paper-Gate-Criterium + User-Flag-Entscheidung
6. Prosa max 2-3 Sätze pro Tabelle

## Tools

| Tool | Zweck |
|---|---|
| `scripts/predict_verdict.py <msg_id>` | 5-Step grounded-decisions automatisiert (Heuristik+Precedent) |
| `scripts/verdict_precedent.py` | ähnliche Cases aus History |
| `scripts/save_verdict.py` | SOFORT-persist (DB `data/backtest_results.db.results.human_verdict`) |
| `scripts/self_eval_verdicts.py` | Hit-Rate-Kalibrierung (Seed-basiert, alle ≥50) |
| `scripts/parser_v2_accuracy_audit.py` | 1230 verdicted Messages → Accuracy-Audit |
| Bash-Bootstrap-One-Liner | Status + nächster Ticker + Self-Eval-Age |

## Anti-Patterns (NICHT tun)

- ❌ Verdict ohne `predict_verdict.py` — Bias kehrt zurück
- ❌ Jack-Text zusammenfassen — User muss Original sehen
- ❌ Review-Analyse-Output vor Tabelle schreiben — User-Regel: NUR Tabelle
- ❌ Verdict ohne sofortigen `save_verdict.py` Call (140 verloren am 12.04.)
- ❌ 50+ Verdicts ohne zwischen-Kalibrierung
- ❌ Den User fragen "welche Variante" — Sim klärt
- ❌ Nach jedem Ticker fragen "weiter?" — User setzt Tempo
- ❌ Memory-Zahlen als Sim-Evidenz — immer frisch ausführen
- ❌ Flag ON ohne Paper-Gate
- ❌ < n=30 / <3 Tickers "Winner" deklarieren — Hypothese, nicht Default
- ❌ Ohne Tests-grün committen

## Critical Rules (Memory-Pins)

- `feedback_verdict_codes.md` — 6 Kürzel + u
- `feedback_verdict_noise_bias.md` — Zweifel → n
- `feedback_review_output_compact.md` — NUR Tabelle, Jack-Text 1:1
- `feedback_persist_review.md` — save_verdict.py SOFORT
- `feedback_user_paces_review.md` — User setzt Tempo
- `feedback_review_table_with_price_at_time.md` — Preis-zur-Uhrzeit Pflicht
- `feedback_simulate_before_asking.md` — autonom statt fragen
- `feedback_review_translate_jack_text.md` — Jack-Englisch übersetzen wenn Tabelle
- `feedback_review_klicks_format.md` — Klick-Format

## Memory-Detail-Files

### Bootstrap & Workflow
- `/root/.claude/projects/-root-signal-bot/memory/project_review_bootstrap.md` — Pflicht-Bootstrap
- `/root/.claude/projects/-root-signal-bot/memory/feedback_complete_review_workflow.md` — 7-Phasen-End-to-End
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_mainline_workflow.md` — Hauptlinie
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_parser_only_phase.md` — Review = nur Parser
- `/root/.claude/projects/-root-signal-bot/memory/project_review_pending_tickers.md` — Queue

### Verdict-Codes & Bias
- `/root/.claude/projects/-root-signal-bot/memory/feedback_verdict_codes.md` — Kürzel-Liste
- `/root/.claude/projects/-root-signal-bot/memory/feedback_verdict_noise_bias.md` — n-Bias
- `/root/.claude/projects/-root-signal-bot/memory/feedback_verdict_words_not_letters.md` — Worte statt Buchstaben
- `/root/.claude/projects/-root-signal-bot/memory/feedback_verdict_glossary_before_metrics.md` — Glossar zuerst
- `/root/.claude/projects/-root-signal-bot/memory/feedback_verdict_learning_loop.md` — Loop-Pattern
- `/root/.claude/projects/-root-signal-bot/memory/feedback_verdict_blindspots_2026_04_18.md` — Blindspots-Audit

### Output-Format
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_format.md` / `_v2.md` / `_v3.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_method_v3.md` — Ticker-basiert
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_long_message_layout.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_table_default_layout.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_table_with_price_at_time.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_klicks_format.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_output_compact.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_translate_jack_text.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_review_batch_approval.md`

### Self-Eval & Kadenz
- `/root/.claude/projects/-root-signal-bot/memory/feedback_self_eval_cadence.md` — ≥50 trigger
- `/root/.claude/projects/-root-signal-bot/memory/feedback_self_eval_seed418_lessons.md` — Seed-Lessons
- `/root/.claude/projects/-root-signal-bot/memory/feedback_self_eval_consolidated_2026_04_18.md` — konsolidiert
- `/root/.claude/projects/-root-signal-bot/memory/feedback_session_health_check_mandatory.md`

### Tools
- `/root/.claude/projects/-root-signal-bot/memory/reference_verdict_tools.md` — Toolchain-Übersicht

### Domänen-Spezial-Verdict-Regeln
- `/root/.claude/projects/-root-signal-bot/memory/feedback_fill_vs_entry.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_buy_without_price_equals_n.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_trade_type_clarification.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_message_chain_awareness.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_out_of_session_mention.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_pronoun_reference_needs_prices.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_noise_one_click.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_soft_score_position_sizing.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_ticker_by_ticker_discussion_file.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_read_charts_during_review.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_chain_display_validated.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_sls_excluded_from_tz.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_jack_self_adjusts_alerts.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_adaptive_stack_validated.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_distress_tsl_validated.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_conditional_trigger_is_buy.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_conditional_buy_with_price.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_jack_jargon_price_alert_equals_order.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_jack_narrative_vs_price_reality.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_no_feierabend_suggestions.md`
- `/root/.claude/projects/-root-signal-bot/memory/feedback_user_curates_messages_first.md`

## Related

- [[Signal-Bot-MOC]] — Container-Bot
- [[Parser-MOC]] — Parser-Loop wird durch Reviews trainiert
- [[Parser-V2-MOC]] — V2 nutzt 1230 verdicted Messages für Audit
- [[Jack-Sparo]] — Signal-Quelle, Verdicts klassifizieren ihre Messages
- [[Karpathy-LLM-Wiki]] — verwandtes Pattern (Eval+Self-Eval-Loop)
