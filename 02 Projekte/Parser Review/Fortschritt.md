---
tags: [parser, review, in-progress]
zuletzt: 2026-04-10
nächste_message_id: 3488
---

# Parser Review — Fortschritt

Ziel: Alle 129 Entry-Signale (+ exits/updates) durchgehen, Korrekturen dokumentieren, Parser neu schreiben.

**Vorgehen pro Session:**
1. Diese Datei lesen → wissen wo wir aufgehört haben
2. Ab `nächste_message_id` weitermachen
3. Erkenntnisse in `Regeln.md` eintragen
4. `nächste_message_id` aktualisieren

---

## Status

- [ ] Entry-Signale (129 total) — **bei ID 3488 (11/129)**
- [ ] Exit-Signale (35)
- [ ] Updates (108)
- [ ] Watchlist (166)
- [ ] Parser neu schreiben

---

## AH/PM-Sampling (2026-04-10, Opus)

Stichprobe: nächste 20 Entries ab ID 3488. Markiert wenn Entry in PM/AH oder Follow-ups in AH/PM mit Exit-Sprache.

**Ergebnis: 6/20 = 30% AH/PM-abhängig** (konservativ gerechnet)

| ID | Ticker | Entry-Phase | AH/PM-Follow-ups | Kommentar |
|---|---|---|---|---|
| 3517 | RANI | **PM** | — | Entry in Pre-Market, Bot kann nicht spielen |
| 3586 | LAES | RTH | 2 (14:41 PM, 22:24 AH) | AH-Management |
| 3588 | LAES | RTH | 2 (14:41 PM, 22:24 AH) | Zweiter LAES-Entry, gleiche Follow-ups |
| 3600 | SCNX | RTH | 1 (12:36 PM) | PM-Follow-up |
| 3608 | SCNX | **PM** | 1 (12:36 PM) | Entry in Pre-Market |
| 3623 | BKYI | **PM** | — | Entry in Pre-Market |

**Plus ELBM (ID 3469) aus vorheriger Review** → realistische Quote eher **35-40%**.

## ⚠️ Nebenbefund: Preisdaten unbrauchbar

`data/price_data.db` enthält **Post-Split-Preise** für Ticker mit Reverse Split (z.B. GNPX, IVF, CODX, XHLD, CMBM, BENF zeigen $20-$55 wo Jack bei $0.50-$1.50 gehandelt hat).

**Konsequenz:** Backtests auf dieser DB sind **wertlos**. Muss durch split-adjustierte Daten ersetzt werden (Polygon/yfinance mit `auto_adjust=False`, oder Event-basiert korrigieren).

## Strategische Konsequenz

Die drei Probleme hängen zusammen:
1. **Parser versteht Kontext nicht** → ELBM/LAES werden falsch klassifiziert
2. **Kein AH/PM-Support** → 35-40% der Signale strukturell nicht spielbar
3. **Split-unadjusted Preisdaten** → keine echte Validierung möglich

**Priorisierung neu überdacht** — nicht "erst Review, dann Architektur", sondern parallel:
- **Track A:** Parser Review fortsetzen (wie gehabt) — für die 60-65% RTH-Signale
- **Track B:** AH-Exit implementieren (Wochenendprojekt) — öffnet die anderen 35-40%
- **Track C:** Preisdaten fixen (Split-Adjustment) — ohne das keine echten Backtests

---

## Bereits reviewed (IDs)

| ID | Datum | Text (kurz) | Korrekt? | Korrektur |
|---|---|---|---|---|
| 3449 | 2025-10-10 | GWH @ 3.65, SL 3.30, 7min | ✅ | — |
| 3458 | 2025-10-13 | ELBM day trade 3.49, SL 3.25, 4min | ✅ | — |
| 3459 | 2025-10-13 | ELBM new order 4.45, SL 4.15, 4min | ✅ | — |
| 3469 | 2025-10-14 | ELBM 4.65 filled, add below 4.50, swing | ✅ Entry | Neues Swing-Entry — Day Trades vom Vortag abgelaufen, neuer Kontext |
| 3470 | 2025-10-14 | "Just to clear something the ticker name ELBM" | ⏭️ | Ticker-Klarstellung, ignorieren |
| 3471 | 2025-10-14 | "So far I am up in ELBM not bad but still holding" | ⏭️ | Update/Commentary — kein neues Entry |
| 3479 | 2025-10-14 | "took some profit out around 5 but left 70% overnight" | ⏭️ | Partial Exit — Update |
| 3483 | 2025-10-15 | "still slightly up, watching to exit" | ⏭️ | Update/Commentary |
| 3487 | 2025-10-15 | "ELBM closed at minor no loss no profit at 4.50" | ⏭️ | Exit-Meldung |
| 3488 | 2025-10-15 | GNPX 0.58, SL 0.52, 4min | ✅ | — |
