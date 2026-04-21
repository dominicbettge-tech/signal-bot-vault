---
title: Miss-Case-Study SPY 2026-04-09
type: analysis
tags: [signal-bot, miss-analysis, case-study, parser-anomaly]
created: 2026-04-21
status: draft
related: [[Miss-Case-Study GV 2026-04-06]], [[Loop-Orchestrator]]
---

## TL;DR

Am 4/9 postete Jack 2× **"SPY Entry: 500.0 Stop: 490.0 Target: 512.0 Day Trade"**. Der echte SPY handelte zu dieser Zeit bei **$674-$681** — also **26% über** Jack's Entry-Price. Bot legte korrekt keine Position an (price never touches 500).

**Dies ist kein Entry-Strategie-Problem, sondern ein Parser-/Validation-Problem.** Die Jack-Zahlen passen nicht zur SPY-ETF-Realität. Fix-Vorschlag wie bei GV 4/6: **Range-Gap-Filter** als neuer Gate-Check.

## Chain — SPY 4/9 Messages

| # | UTC | ET | Typ | Jack-Text |
|---|---|---|---|---|
| #190 | 06:37 | 02:37 | entry | "I placed me an order in SPY Entry: 500.0 Stop: 490.0 Target: 512.0 Day Trade" |
| #191 | 06:39 | 02:39 | entry | gleich (2min-Repost) |

Beide overnight pre-market (NYSE öffnet 09:30 ET). Extrem runde Zahlen (500/490/512) — **untypisch** für Jack's übliche Decimal-Precision.

## SPY-Kurs am 4/9 (Polygon daily)

- Open: **$674.84**
- High: **$681.16**
- Low: **$673.77**
- Close: **$679.91**
- Volume: 57.1M

Jack's Entry bei **$500** lag **−25.9%** unter dem intraday Low von $673.77. Kein Pullback auch nur ansatzweise möglich.

## Bot-Aktionen

**Keine Trades in `trades` für SPY 4/9.** `missed_trades` hat 2 Einträge aus dem Retro-Bootstrap dieses Morgens (`RETRO_NO_TRADE`). Kein echter Live-Trade-Attempt.

## Hypothesen zu den 500-Zahlen

1. **Witz / Educational Example** — Jack nimmt runde $500 für ein schematisches Setup-Beispiel
2. **Parser-Fehler** — Jack schrieb z.B. "SPXS" oder "SPYD" (kleinere Ticker die bei $500 handeln könnten), Parser normalisierte auf "SPY"
3. **Copy-Paste aus altem Post** — 2022 als SPY tatsächlich nahe $500 stand
4. **Testmessage / Missverständnis** — Jack ruft Setup für ein anderes Asset namens "SPY" aus (z.B. ein SPY-Leveraged-ETF)

Keine dieser Hypothesen ist per-Case-Study verifizierbar ohne Jack direkt zu fragen. **Für Bot-Logik irrelevant:** In ALLEN Fällen ist der Fix derselbe — erkennen dass Jack's Entry-Range weit vom Marktpreis liegt und SKIP oder USER-DECISION triggern.

## Fix-Vorschlag: Reuse "Range-Gap-Filter" aus GV 4/6

Siehe [[Miss-Case-Study GV 2026-04-06#Fix-Vorschlag]]. Beide Cases (GV 4/6 und SPY 4/9) lassen sich durch denselben Filter abfangen:

```python
RANGE_GAP_MAX_PCT = 0.03  # entry_high max 3% unter last_price
```

- GV 4/6: entry_high 0.27 vs last_price 0.34 → Gap 20.6% → SKIP
- SPY 4/9: entry 500 vs last_price ~680 → Gap 26.5% → SKIP

**Beide korrekt abgefangen mit einem einzigen Gate-Check.**

## Abgeleiteter Pattern: "Range-Below-Market" ist ein wiederkehrendes Miss-Pattern

| Case | Jack-Range | Markt-Preis | Gap | Fill |
|---|---|---|---:|---|
| GV 4/2 | 0.42-0.45 | 0.47 (Post-Zeit) | -4.2% (nah) | ✓ Trade #4 filled |
| GV 4/6 | 0.255-0.27 | 0.34 | -20.6% | ✗ kein Fill |
| SPY 4/9 | 500 | 680 | -26.5% | ✗ kein Fill |

**Threshold-Hypothese:** ~5-10% Gap ist die Kipplinie zwischen "realistic Pullback" und "No-Fill-Sicherheit". Kalibrierung nötig aus grösserem Sample.

## Was noch offen ist

- SPY-Parser-Anomalie separat verifizieren (eventuell Fuzzy-Match zwischen "SPY" und Near-Ticker)
- Range-Gap-Filter threshold (3%, 5%, 10%?) — brauche mehr Samples für Kalibrierung
- Gate-Level-Knob → nicht corpus-sim-validierbar → manuelle User-Review via `/loop` NEEDS_MANUAL