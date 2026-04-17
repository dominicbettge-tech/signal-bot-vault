# ORKT — Parser Review

**Status:** ✅ done (2026-04-17)
**Session-Window:** 2025-12-09 07:14 ET → 09:33 ET (3 Messages)
**Prev-Day-Close:** ~$0.90 (150% move gestern ohne News)
**Fill:** $1.20/$1.21 @ 09:33 ET
**Jack-Post-Fill-Silence:** 0 Follow-up-Messages (komplettes Schweigen)

## Review-Tabelle

| # | msg_id | ET | Jack-Text (EN) | DE-Kurz | Verdict | Begründung |
|---|--------|-----|----------------|---------|---------|------------|
| 1 | 4000 | 07:14 | siehe [A] | Alert bei $1.13–$1.15 platziert (pre-market, 2h-Fenster) | **b** | Klarer Order-Intent mit Range + Zeit-Trigger, Soft-Score +1 („too risky, might") |
| 2 | 4002 | 09:10 | siehe [B] | Order-Replace: Alert auf $1.19–$1.22 verschoben | **b** | Multi-Ticker (XCUR/NCPL/ORKT), Order-Modify (nicht Cancel+New), Chain-Inheritance zu #4000 |
| 3 | 4003 | 09:33 | „ORKT got me filled at 1.20 and 1.21" | Fill-Bestätigung | **s** | Status (kein neuer Entry); Ladder-Exit-Default aktiviert |

## Volltexte

**[A] #4000 (2025-12-09 07:14 ET / 12:14 UTC):**
> So far after almost 2 hours trying to scan the market activities across the board. There are few movers but the price tag is too high to risk. ATMC already up 650%… The other movers are facing pressure sell. XCUR might risk and get some if it drops below 8.00 and stays above 6.85… ORKT — moved up yesterday by 150% low float no material news caused the move so too risky but I might place price alert 🔔 at 1.13 to 1.15 and see if it will go there in the coming two hours.

**[B] #4002 (2025-12-09 09:10 ET / 14:10 UTC):**
> So far my top watch list and possibly day trade spots: XCUR may risk and add some if it can get me any order fill between 8.20 to 7.50… NCPL Got some volume, watching below 0.96 to 0.89… ORKT — I am keeping my monitor on for it. Adjust my price alert to 1.19 up to 1.22. Will keep an eye for sure.

**[C] #4003 (2025-12-09 09:33 ET / 14:33 UTC):**
> ORKT got me filled at 1.20 and 1.21

## Diskussion (2026-04-17)

**Initial-Fehler:** Claude hat Preise halluziniert ($10.80/$10.95 statt $1.13–$1.22), weil nach Compaction aus Chat-Gedächtnis statt DB gerechnet wurde. User-Korrektur führte zur neuen Meta-Regel `feedback_post_compaction_db_reread.md` (Preise IMMER frisch aus `raw_messages.db`).

**Exit-Signal-Prüfung:** User fragte gezielt nach Exit. Claude prüfte alle 20 Messages nach Fill → kein ORKT-Bezug, nicht einmal impliziert. Kandidat war #4007 „Took profit out at 1.50" — Polygon-Check widerlegte: NCPL erreichte $1.5199 um 09:43, ORKT nur $1.49 (1 Cent zu wenig). Der $1.50-TP gehört eindeutig zu NCPL.

**Regie-Befund:** ORKT ist ein Silent-Post-Fill-Case → Bot muss autonom exiten. Daraus resultiert `feedback_bot_full_autonomy.md` (ORKT als Evidenz für Pure-Mirror-Verbot).

## Bot-Relevanz / Parser-Regeln

- **Multi-Ticker-Row-Cloning (R-Kandidat):** #4000 und #4002 enthalten jeweils 3 Ticker parallel — Parser muss pro Ticker eine Zeile in `parsed_signals` erzeugen (`parent_msg_id` + `ticker_index`). Aktuell unterdokumentiert.
- **Chain-Inheritance:** Soft-Score (+1) aus #4000 → #4002, weil „still monitoring" keine neuen Keywords einführt.
- **Price-Alert-Semantik:** Jack-Jargon „price alert 🔔" = vorgeplatzter Limit-Buy (nicht bloße Notification). Parser sollte `order_type=LIMIT` setzen.
- **Pre-Market-Staging:** #4000 um 07:14 ET erzeugt Order, die bis ~09:14 ET laufen soll; #4002 um 09:10 ET verlängert/verschiebt Alert-Range. Parser muss TTL respektieren.

## Price-Action-Analyse (Polygon, 2025-12-09 nach Fill 09:33 ET)

| Zeit | Event | Preis | vs Fill |
|------|-------|-------|---------|
| 09:33 | Fill | $1.205 | 0% |
| 09:34 | Intraday-High #1 | $1.49 | +23.7% |
| 09:43 | Post-Peak Low | $1.23 | +2.1% |
| 11:48 | Peak | $1.647 | +36.7% |
| 15:59 | EoD Close | $1.306 | +8.4% |
| — | Hard-SL −5% ($1.145) | nicht erreicht | — |

**Exit-Vergleich (hypothetisch):**

| Strategie | Exit | PnL % |
|-----------|------|-------|
| HardTP +10% ($1.326) | 09:33 Bar High $1.43 | **+10.0%** |
| Ladder 33/33/34 (+5/+10/+20) | 09:33–09:34 | **+11.55%** |
| Hold EoD | $1.306 | +8.4% |
| H11 RSI-Adaptive (Case) | Peak-Trail | +34.6% (Case-optimal) |
| Pure Mirror | — | unmöglich (Jack schweigt) |

## Offene Punkte

- Multi-Ticker-Row-Cloning ist nicht live implementiert — Parser erzeugt aktuell eine Zeile pro Message. Blocker für Testcenter Ticker-Einzel-Simulation. (→ `project_parser_multi_ticker_cloning.md`)
- Pre-Market-Order-TTL-Handling beim Bot noch nicht geprüft — ob Alert-Orders vor 09:30 aktiv sind oder erst bei Open.
