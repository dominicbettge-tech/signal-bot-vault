# Review-Batch 2026-04-19 — 252 kuratierte Messages

**Zweck:** 200-300 priorisierte Messages für die nächste Review-Session (User-Auftrag 2026-04-19).

## Inhalt

- **252 high-value messages** (Signal-Type ∈ {entry, take_profit, exit, cancel, stop_loss_update, extend, watchlist, update})
- **Datumsbereich:** 2025-10-09 → 2026-01-08
- **78 distinct Tickers** (plus 50 ohne Ticker = Pronoun-/Chain-Messages)
- Commentary-Only Messages (1940 Stück) sind **ausgeschlossen** — dort ist Verdict meist `n` und Review liefert wenig Signal

## Top-Tickers (Review-Chains)

| Ticker | Msgs | Bemerkung |
|---|---:|---|
| (ohne Ticker) | 50 | Pronoun/Chain-Inheritance, brauchen Context ±5 |
| RADX | 13 | Review-Queue-Spitze per `project_review_pending_tickers.md` |
| OCG | 9 | |
| PCLA | 9 | |
| ALMS | 9 | |
| BBGI | 8 | |
| IMRX | 8 | |
| ELBM | 7 | |
| NCPL | 7 | Multi-Ticker-Strategy-Proof-Case |
| POM | 7 | |
| MIST | 6 | Multi-Signal aus #9 per Memory |
| OCGN, TWG, SLS, GNPX, OMER, SIDU, TMDE, PSTV, PCSA | 3-5 | |

## Reihenfolge

**Empfehlung:** nach User-Direktive `feedback_ticker_by_ticker_discussion_file.md` — Ticker-basiert, nicht chronologisch. 
Reihenfolge aus `project_review_pending_tickers.md`: **RADX → MIST → AQST → GURE → SOPA → NCPL → ABOS** zuerst.

Danach sortiert nach Message-Count descending, dann chronologisch.

## Datei-Output

`Review-Batch-2026-04-19.csv` (| als Delimiter)

**Spalten:** `message_id | date | signal_type | ticker | side | entry_low | entry_high | stop_loss | confidence | trade_type | text` (Text auf 500 Chars gekürzt, Newlines zu Spaces)

## Streamlit-UI Einbindung

Die CSV kann von `scripts/review_ui.py` gelesen werden (bisher nutzt die UI `parsed_signals`-Table direkt). Optional:

```python
# In review_ui.py, um auf Batch zu filtern:
import pandas as pd
batch = pd.read_csv('/root/obsidian_vault/02 Projekte/Parser Review/Review-Batch-2026-04-19.csv', sep='|')
filter_ids = set(batch['message_id'])
# Only show messages in filter_ids
```

## Batch-Modus vorschlag

Per `feedback_review_batch_approval.md` — Tabelle mit vorausgefüllten Verdicts aus Haiku-Vorschlag; User sagt „ja" / „nein #N" / Spot-Fix.

**Problem:** Haiku-Suggestions-DB enthält aktuell **Parser-Reclassifications** (results-Table in backtest_results.db), nicht Verdict-Vorschläge. Würde einen zweiten Haiku-Batch brauchen für Verdict-Vorschlag — ODER User reviewt ohne Vorschlag via Streamlit-UI.

## Verdict-Bias-Hinweise (aus Self-Eval)

- **Self-Eval 2026-04-18 (seed418):** 66.7% Hit-Rate, 5 Blindspots (`feedback_self_eval_seed418_lessons.md`):
  - filled nach Avg = e
  - OoS-Holds = n
  - „might get" = n/w
  - Teaser mit % = w
  - Single-Price + monthly + conditional = w
- **Cross-Seed Consolidated (R6-R11):** Retro-Fill=s, Heading-close=s, Sold-Nth-order=x, Halt-Resume=e, Watchlist-Trigger=w, Multi-Status=w

Beim Review diese Regeln als mentale Checkliste.

## Next Steps

1. User öffnet Streamlit-UI (Port 8501) oder durchgeht CSV-Zeilen
2. Optional: Haiku-Verdict-Batch-Run vorher (Skript wäre `batch_classify_haiku.py` mit angepasstem Prompt → Verdict-Vorschlag statt Reclassify)
3. Verdicts → `parser_review_verdicts.csv` (sofort persistieren per `feedback_persist_review.md`)
4. Nach 50 Verdicts: Self-Eval-Run (per `feedback_self_eval_cadence.md`)
