---
tags: [parser, review, ticker-basiert]
zuletzt: 2026-04-14
parent: "[[Parser Review/Fortschritt]]"
---

# Parser Review — Ticker Queue

**Ab 2026-04-13 Ticker-basierter Workflow.** Nach 12.04.-Datenverlust.

## Erledigt

| # | Ticker | Datum | Msgs | Notes |
|---|---|---|---|---|
| 1 | CETX | 2025-12-08 | 8 | massive PM-Spike, 3% TSL killt sofort, CAUTION_WARNING-Kategorie vorgemerkt |
| 2 | ALMS | 2026-01-06 | 22 | 4-staffel-Entries, SL vs TSL Kollision, Flash-Dip-Problem, SL-1%-Regel |

## Nächste priorisierte Kandidaten

Sortiert nach **Messages × Strukturiertheit × Cluster-Coverage**:

| # | Ticker | Msgs | Entries | Updates | Exits | TP | Cluster | Zeitraum | Warum priorisieren |
|---|---|---|---|---|---|---|---|---|---|
| 3 | **LAES** | 23 | 2 | 3 | 0 | 1 | C1 | Okt–Jan | Längster Multi-Session-Swing, Jack erwähnt mehrfach (280% Gewinn), Cluster-Referenz |
| 4 | **TWG** | 13 | 1 | 2 | **2** | 0 | C1 | Dez 5-8 | Seltener Fall mit 2 expliziten Exits = komplette Trade-Story |
| 5 | **OMER** | 18 | 1 | 4 | 0 | 0 | C1 | Okt–Dez | Langer Swing mit Updates, Jack averaged |
| 6 | **RADX** | 15 | 1 | 4 | 0 | 1 | C1 | Dez 15-26 | Saubere Struktur mit TP, Multi-Day |
| 7 | **NCPL** | 13 | 1 | 2 | 0 | 1 | C1 | Dez 9 | 1-Tag-Swing mit TP, kompakt |
| 8 | **GURE** | 11 | 3 | 4 | 0 | 0 | C1 | Dez 5-10 | 3 Entries = wahrscheinlich Averaging-Story |
| 9 | **POM** | 10 | 1 | 4 | 0 | 1 | C0 | Dez 10 | C0-Penny mit TP, Kontrast zu C1-Beispielen |
| 10 | **SLS** | 20 | 0 | 1 | 1 | 1 | — | Okt–Jan | Non-clustered, 0 Entries aber TP+Exit = Watchlist-only Case |

## Begründung der Reihenfolge

**Warum LAES als #3:** Jack nennt LAES als eines seiner Top-Signale (280% in 3 Monaten). 23 Messages über ~3 Monate decken Swing-Management-Fälle ab, die bei CETX/ALMS fehlten (Multi-Day-Hold, Averaging, Partial Exits).

**Warum TWG als #4:** 2 Exit-Messages sind selten. Wir können den kompletten Lifecycle beobachten und den Parser am Exit-Handling-Verhalten testen.

**Warum OMER #5:** Zweiter Swing-Case, kürzer als LAES, hilft Pattern-Stabilität zu prüfen.

**SLS als #10 (Sonderkategorie):** Jack nennt SLS 20× aber **nie als Entry**. Das ist entweder ein Watchlist-Only-Ticker oder ein Parser-Fehler (Entry wird als Commentary klassifiziert). Lohnt sich zu prüfen.

## Non-clustered Ticker mit Entries (für Phase-3 Erweiterung)

Diese 39 Ticker haben Entries aber sind nicht in Phase-1-Cluster. Nach Polygon-Daten-Integration müssen sie re-clustered werden:

OCG(4), CMBM(2), AKBA(2), GNPX(2), IVF(2), DRMA(2), NDRA(2), PSTV(2), PCLA(2), NVVE(2), INHD(2), BENF(1), AMBR(1), BTBT(1), FLYX(1), HSPO(1), EKSO(1), DTCK(1), CODX(1), CNEY(1), LVRO(1), LPTX(1), KTTA(1), IRBT(1), GNS(1), MWG(1), MASK(1), SLRX(1), WHLR(1), ASBP(1), SRXH(1), AEHL(1), DRCT(1), HTOO(1), NDRA(1), LTRN(1), VRME(1), OMEX(1), SRZN(1)

**CMBM und LVRO sind delisted** → nur daily data möglich, nicht clustered.

## Review-Workflow (aus REVIEW_RULES.md)

1. Ticker wählen (von oben)
2. Alle Messages chronologisch lesen
3. Intraday-Chart parallel (1min Daten aus `data/price_data_1min.db`)
4. Pro Message: Verdict (b/e/x/s/w/n) + Korrektur
5. **SOFORT in DB speichern** (scripts/save_verdict.py)
6. Erkenntnisse ins `Regeln.md`
7. Am Ende Ticker-Summary in dieses Doc

## Context für nächste Session

- Phase 2/2e/2f Classifier-Analyse ist abgeschlossen (Vault-Docs + rules.py)
- Polygon-Daten kommen heute Abend → danach kann Cluster-Set erweitert werden
- Review-Datenspeicherung: unbedingt `save_verdict.py` nutzen, nicht nur im Chat merken
