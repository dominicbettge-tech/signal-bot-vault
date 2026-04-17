# NCPL — Parser Review

**Status:** 🟡 94% done — 15/16 in-session reviewed + #4401 (07.01.26) noch offen
**Session-Window:** 2025-12-08 19:26 ET → 2025-12-09 11:14 ET (15 Messages)
**Out-of-Session:** #4401 @ 2026-01-07 14:28 ET (29 Tage später, eigene Session)
**Fill:** $1.05 opening (implizit via halt-up) @ 09:39 ET
**Exit:** $1.50 @ 09:45 ET (**+43%** auf 6 Min)

## Review-Tabelle (in-session, 15 Msgs)

| # | msg_id | ET | Jack-Text (DE-Kurz) | Verdict | Begründung |
|---|--------|-----|---------------------|---------|------------|
| 1 | 3998 | 08.12. 19:26 | Pre-Market-Watchlist: XCUR + NCPL, „didn't trade yet" | **w** | Watchlist, kein Order-Intent |
| 2 | 4002 | 09:10 | NCPL-Teil: Entry $0.96–$0.89, 20-Min-Fenster | **b** | Konkreter Order-Intent mit Range + TTL |
| 3 | 4004 | 09:38 | „NCPL Strong move ✅" | **n** | Reaktions-Kommentar, Fill erst #4005 |
| 4 | 4005 | 09:39 | „Halted up NCPL. Got A small order at the opening around 1.05 still holding" | **e** | Fill @ $1.05 — aber OPPORTUNISTISCH, außerhalb der 4002er Range; Parser: Jack tradet am Open anders als Alert-Range |
| 5 | 4006 | 09:39 | „NCPL Mentioned here since yesterday" | **n** | Rückblick-Hinweis |
| 6 | 4007 | 09:45 | „Took profit out at 1.50" | **x** | TP-Exit (Polygon-verified: NCPL H=$1.5199 um 09:43) |
| 7 | 4008 | 09:50 | Conditional: „if failed to break 1.54 → Entry 1.25–1.18 in 3–4 min" | **b** | Klassischer Conditional-Setup, Anker für Executor |
| 8 | 4009 | 09:54 | „Time out with no fill, lowest 1.27. Still watching" | **s** | Order expired (Low $1.27 > Trigger $1.25) |
| 9 | 4010 | 09:55 | „Only very tiny margin error team 1.27 to 1.25 0.02" | **n** | Kommentar zur Near-Miss |
| 10 | 4011 | 10:03 | „NCPL up and halted" | **n** | Marktkommentar |
| 11 | 4012 | 10:06 | „One more trade 1.42 Valid for 3 minutes" | **b** | Neuer Entry-Intent mit TTL |
| 12 | 4013 | 10:16 | „another halt up" | **n** | Status-Chatter |
| 13 | 4014 | 10:22 | „still a day trade but I believe the overbought will cause a sell off soon so be careful" | **s** | Trade-Type-Reconfirm + Caution → Distress-TSL 1.5% |
| 14 | 4015 | 10:28 | „halted down 3 minutes after my last text" | **n** | Post-hoc Validierung der Caution |
| 15 | 4018 | 11:10 | „Another volume push got a halt up" | **n** | Marktkommentar |
| 16 | 4019 | 11:14 | „NCPL new high .. What a day" | **n** | Day-End-Celebration |

## Out-of-Session

| # | msg_id | ET | Status |
|---|--------|-----|--------|
| — | 4401 | 2026-01-07 14:28 | 🟡 Out-of-Session (29 Tage), gehört zu 2026-01-07 Session („Also news AH and 37% move") — eigene Review-Runde nötig |

## Verdict-Verteilung (in-session)

- **b** (entry-intent): 3 (#4002, #4008, #4012)
- **e** (fill): 1 (#4005)
- **x** (exit): 1 (#4007, **+43%**)
- **s** (status/caution): 3 (#4009, #4014, —)
- **w** (watchlist): 1 (#3998)
- **n** (noise): 7

## Diskussion (2026-04-17)

**Opportunistic-Fill-Problem (#4005):** Jack füllte um 09:39 @ $1.05 — das liegt AUSSERHALB der in #4002 angekündigten Range $0.96–$0.89. Parser-Implikation: Jack folgt seinen Alert-Orders nicht strikt. Der Bot kann Jacks Alert-Order NICHT als Leitorder behandeln, weil er oft opportunistisch am Open einsteigt (halt-up = Markt-Volatilität + schnelle Entscheidung). → Bestätigt `feedback_bot_full_autonomy.md` zusätzlich.

**TP-Nachweis via Polygon:** User fragte gezielt ob $1.50 wirklich erreicht wurde. Polygon-Check: NCPL H=$1.5199 um 09:43 (2 Min vor #4007) — bestätigt. Analoger Check für ORKT widerlegte dort $1.50-Zuordnung.

**Distress-TSL-Validation (#4014):** „still a day trade but be careful" = Trade-Type-Reconfirm UND Caution → Engere TSL (1.5%), nicht Hard-Exit. Entspricht `feedback_distress_tsl_validated.md`.

**Halt-Pattern:** NCPL hatte 3 Halt-Ups an diesem Tag (#4011, #4013, #4018). Parser sollte Halt-Status als Feature tracken (Halt-Count pro Session = Distress- oder Momentum-Indikator).

## Bot-Relevanz / Parser-Regeln

- **Multi-Ticker-Row-Cloning:** #3998 (XCUR+NCPL) und #4002 (XCUR+NCPL+ORKT) wieder Multi-Ticker — Row-Cloning bestätigt als Pflicht-Feature.
- **Opportunistic-Fill-Parsing:** #4005 Fill-Preis $1.05 außerhalb der angekündigten Range → Parser muss `fill_price` unabhängig von Alert-Range akzeptieren und als separate Evidenz speichern (nicht als Alert-Rangefehler flaggen).
- **Conditional-Setup mit TTL:** #4008 ist Template für den Conditional-Setup-Executor (`project_conditional_setup_executor.md`): Condition „fail 1.54", Action „Entry 1.25–1.18", TTL „3–4 min".
- **Re-Entry-Pattern:** #4012 „One more trade" = expliziter Re-Entry-Trigger, Parser-Keyword.
- **Halt-Count als Feature:** 3 Halt-Ups in 1.5h → Feature-Engineering für Soft-Score / Volatility-Regime.

## Price-Action (Polygon, 2025-12-09)

- 09:38 Fill ~$1.05 (opening halt-up)
- 09:43 Peak #1 $1.5199 (TP-Trigger #4007 @ $1.50 → **+43%** in 5 Min)
- 09:50–09:54 Dip auf $1.27–$1.25 (Conditional #4008 knapp verfehlt, Low $1.27 > Trigger $1.25)
- ~10:22 Overbought-Warnung (#4014) → tatsächlich Halt-Down 3 Min später (#4015 bestätigt)

## Opportunistic-Open-Buy-Analyse (User-Diskussion 2026-04-17)

**Ausgangsfrage:** Warum filled Jack bei $1.05 wenn announced Range $0.89–$0.96 war?

**Erkenntnis (Polygon-basiert):**
- Pre-Market VOR #4002 (04:00–09:00 ET): Low **$0.82** — Range wäre gefillt worden, aber die Order existierte da noch nicht
- #4002-Announce-Fenster (09:10–09:30 ET): Low $1.01 — Range nie erreicht, Order **expired ohne Fill**
- Open 09:30: $1.04, Halt-Up bis $1.37 in 9 Min
- Jack-Fill @$1.05 um 09:39 = **Silent-Market-Buy ohne Channel-Announcement**
- Bot-Problem: strikte Limit-Only-Logic hätte NCPL komplett verpasst (+43% Miss)

**Offset-Sim auf NCPL 09:10–09:45 ET:**

| Offset über $0.96 | Limit | Fill-Preis | Zeit | PnL bis $1.50 |
|-------------------|-------|------------|------|---------------|
| 0% (pure Mirror) | $0.960 | expired → Reentry $1.10 | 09:31 | +36.0% |
| +5% | $1.008 | expired → Reentry $1.10 | 09:31 | +36.0% |
| **+8.33%** | **$1.040** | **$1.04 (exakter Open-Hit)** | **09:23** | **+44.2%** |
| +9.38% (Jack-real) | $1.050 | $1.05 | 09:18 | +42.9% |
| +10% | $1.056 | $1.056 | 09:18 | +42.0% |
| +12% | $1.075 | $1.075 | 09:10 | +39.5% |
| +15% / +20% | $1.10 / $1.15 | $1.08 (Cap-Open) | 09:10 | +38.8% |

**Sweet-Spot: +8–10% Offset** → Fill ~$1.05, PnL ~+42–44%.

**Corpus-Validierung blockiert:** Parser extrahiert Preis-Ranges nicht strukturiert (0% Coverage). Bevor Offset-Default aus n=1 abgeleitet werden kann, muss Parser-Range-Extraction stehen.

→ Als **Hypothese H9** in `project_testcenter_r_hypotheses.md` (Opportunistic-Open-Buy nach Limit-Expiry) gespeichert, 3 Sub-Varianten (H9a/b/c) für späteren Sweep.

## Offene Punkte

- **#4401 (2026-01-07):** out-of-session-Verdict noch offen, gehört zur 2026-01-07-Session (neue Watchlist: AMOD + NCPL news AH 37%). Bei AMOD-Review mitbehandeln.
- **H9 (Opportunistic-Open-Buy):** 1 Case (dieser), Corpus-Sim blockiert bis Parser-Range-Extraction.
- **Halt-Count-Feature:** als Soft-Score-Input noch nicht im Bot.
- **Parser-Range-Extraction:** Vorbedingung für H9-Sim. Als Task in `project_parser_quality_maximization.md` für Wochenende.
