---
tags: [signal-bot, parser-review, simulation, kalibrierung]
created: 2026-04-12
---

# Parser Review — Trade Simulationen

Jeder Trade aus dem Parser-Review wird hier vollständig simuliert. Am Ende leiten wir daraus optimale SL/TP-Regeln ab.

**Bot-Config für Simulationen:** Bankroll $10k, Position 20% = $2000, TSL 3%, TSL-Activation 1%, Auto-TP +3%/+6%

---

## Trade 1: RANI (ID 3517-3523) — Day Trade

**Signal:** Entry ~$1.18, SL $1.05, TP "around the opening" ($1.37)
**Typ:** Day Trade | **Datum:** 17. Okt 2025

| Zeitpunkt | Event | Bot-Aktion |
|---|---|---|
| Entry | $1.18 (Avg Jack: $1.21) | Entry $1.18, 1694 Shares, SL $1.05 |
| Kurs → $2.39 (High) | TSL aktiviert, Peak $2.39, TSL = $2.32 | — |
| Kurs fällt | TSL triggered | Exit ~$2.32 |

**Bot PnL: 1694 × ($2.32 - $1.18) = +$1,931** (Bestcase mit TSL)
**Jack PnL:** Avg $1.21, Exits bei $1.45-$1.48 → ~+20% auf Position

**Erkenntnis:** Bot mit TSL hätte hier DEUTLICH mehr verdient als Jack, weil TSL den Spike mitgenommen hätte. Jack hat konservativ bei +20% verkauft, Kurs lief bis +100%.

---

## Trade 2: IVF (ID 3524-3533) — Day Trade, Post-Spike

**Signal:** "Might risk and get some at 0.78, SL 0.70, Valid 15 min"
**Typ:** Day Trade | **Datum:** 17. Okt 2025
**Kontext:** IVF hatte am 16. Okt einen +180% Spike, Jack reitet die zweite Welle

### Signalverlauf

| ID | Zeit | Nachricht | Klassifikation |
|---|---|---|---|
| 3524 | 14:11 | Entry $0.78, SL $0.70, 15min | `b` — "might" + konkrete Params = Entry |
| 3526 | 14:22 | "Filled" (reply auf 3524) | `e` — Fill-Bestätigung |
| 3527 | 14:22 | "IVF order filled at 0.78" | `e` — Duplikat (standalone) |
| 3528 | 14:40 | "so far green, may take half out" | `n` — Status, kein Signal |
| 3529 | 14:42 | "Closed half at 0.825, leaving half to risk" | `s` — Partial Exit 50% |
| 3531 | 15:18 | "IVF moving up again" | `n` — Kommentar |
| 3533 | 15:35 | "Closed 25% at 0.865" | `s` — Partial Exit 25% |
| — | — | Keine weitere IVF-Nachricht | Rest verwaist |

### Simulation (2000 Shares @ $0.78 = $1560)

| Event | Shares | PnL kumuliert | SL |
|---|---|---|---|
| Entry $0.78 | 2000 | $0 | $0.70 |
| Partial Exit 50% @ $0.825 | 1000 | +$90 | → Orphan: $0.80 (midpoint) |
| Partial Exit 25% @ $0.865 (250 von 1000) | 750 | +$111.25 | → Orphan: $0.82 (midpoint) |
| Orphan TP1 $0.93 (50% von 750) | 375 | +$167.50 | $0.82 |
| Orphan TP2 $0.99 (rest) | 0 | +$246.25 | — |
| ODER: Kurs fällt → SL $0.82 | 0 | +$141.25 | — |

**Close am Signal-Tag:** ~$0.60 (split-bereinigt) → SL $0.82 wäre getriggert.

**Realistisches Bot-Ergebnis: +$141.25** (Partial Exits + Orphan SL auf Midpoint)
**Jack PnL:** 50% @ +5.8%, 25% @ +10.9%, 25% unbekannt

### Bugs gefunden
- ~~Expiry schloss gefüllte Positionen~~ → GEFIXT (nur Pending)
- ~~`might`-Filter blockte echte Entries~~ → GEFIXT (might + Params = Entry)
- ~~Kein Partial-Exit-Handling~~ → GEFIXT (Orphan Protection)

---

## Trade 3: OMER (ID 3521-3760) — Swing, Post-Spike

**Signal:** Entry $8.40, SL $7.75, Swing, Valid till 12:00 ET
**Typ:** Swing | **Datum:** 17. Okt 2025
**Kontext:** OMER hatte am 15. Okt einen +154% Spike ($4.10 → $10.42), Jack steigt 2 Tage danach ein

### Signalverlauf

| ID | Datum | Nachricht | Klassifikation |
|---|---|---|---|
| 3521 | 17. Okt 14:03 | Entry $8.40, SL $7.75, Swing | `b` |
| 3530 | 17. Okt 14:44 | "Filled at 8.40, hold over weekend" | `e` |
| 3538 | 17. Okt 19:36 | "still holding OMER" | `n` |
| 3555 | 21. Okt 13:30 | "might average at 7.50, cut off below 6.85" | SL-Update → $6.85 |
| 3573 | 22. Okt 09:31 | "may cut if no support above 7.50" | `n` |
| 3575 | 22. Okt 13:50 | "hopefully finds weekly support" | `n` |
| 3610 | 24. Okt 12:04 | "still in my hold" | `n` |
| 3647 | 28. Okt 19:35 | "still holding patiently" | `n` |
| 3745 | 13. Nov 23:25 | "hopefully back above 8-9 in two weeks" | `n` |
| 3760 | 17. Nov 18:19 | "green for me team" | `n` |

### Kursverlauf

| Datum | O | H | L | C | Event |
|---|---|---|---|---|---|
| 17. Okt | $9.61 | $9.66 | $7.96 | $8.11 | Entry $8.40 |
| 20. Okt | $9.15 | $10.36 | $8.95 | $9.83 | **Spike! TSL aktiviert** |
| 21. Okt | $8.10 | $8.32 | $7.77 | $8.25 | Jack: SL → $6.85 |
| 22. Okt | $7.77 | $8.03 | $7.425 | $7.74 | Original SL $7.75 durchbrochen |
| 28. Okt | $7.73 | $8.05 | $7.44 | $7.96 | — |
| 31. Okt | $7.54 | $7.54 | $7.22 | $7.33 | — |
| 4. Nov | $7.06 | $7.24 | $6.71 | $6.73 | **Jack's SL $6.85 durchbrochen** |
| 14. Nov | $6.64 | $6.88 | $6.24 | $6.28 | Tiefpunkt |
| 17. Nov | $7.90 | $9.10 | $7.72 | $9.08 | **Spike! Jack sagt "green"** |

### Alle Szenarien (238 Shares = $2000)

| Szenario | Exit | PnL | Bewertung |
|---|---|---|---|
| **A: Bot mit TSL 3%** | **20. Okt @ ~$10.05** | **+$392.70** | ✅ BESTES ERGEBNIS |
| B: Bot TSL + SL-Update | 20. Okt @ ~$10.05 | +$392.70 | ✅ TSL greift vorher |
| C: Nur Original SL $7.75 | 22. Okt | -$154.70 | ❌ |
| D: Nur Jack's SL $6.85 | 4. Nov | -$368.90 | ❌❌ |
| E: Jack (avg down, mental SL) | hält → 17. Nov $9.10 | ~+$260 | ⚠️ nach -20% Drawdown |

### Erkenntnisse
1. **TSL 3% war BESSER als Jack** — Bot +$393 vs Jack ~+$260
2. **Jack's SL-Updates blind folgen = gefährlich** — $6.85 hätte -$369 gekostet
3. **TSL schützt vor Jack's Optimismus** — er hielt -20% Drawdown durch
4. **Post-Spike-Swings profitieren vom TSL** — fängt Gewinn auf dem Rückweg
5. **Jack's mentaler SL ≠ realer SL** — er postet Levels, hält sie nicht ein
6. **Average Down für Bot NICHT implementieren** — TSL-Exit war profitabler

---

## Regel-Ableitungen (laufend aktualisiert)

### SL-Regeln (Stand: Trade 1-3)
- ✅ **Trailing SL 3% bei ALLEN Trade-Typen behalten** — auch Swings
- ✅ **TSL-Activation bei 1% über Entry** — früh genug um Spikes zu fangen
- ⚠️ **Jack's SL-Updates parsen aber vorsichtig nutzen** — nur als Untergrenze, nie TSL überschreiben
- ❌ **Kein Average Down** — erhöht Risiko, TSL-Exit ist profitabler

### TP-Regeln (Stand: Trade 1-3)
- ✅ **Partial Exits folgen** — "closed half", "closed 25%" parsen und ausführen
- ✅ **Orphan Protection nach Partial Exit** — gestaffelte TPs für Restposition
- ⚠️ **Orphan TP-Werte vorläufig** (+7%/+15%) — nach Review kalibrieren

### Parser-Regeln (Stand: Trade 1-3)
- ✅ **"might" + konkrete Params = Entry** (nicht REJECT)
- ✅ **"cut it off below X" = SL-Update**
- ✅ **"closed half/25%/rest" = Partial/Full Exit**
- ✅ **"around X" = Range ±3-4%** um den Preis

---

## Trade 4: RANI #2 (ID 3535) — Day Trade, Re-Entry

**Signal:** Entry $1.49, SL $1.34, Valid 3 min, Day Trade
**Typ:** Day Trade | **Datum:** 17. Okt 2025 16:15 UTC
**Kontext:** Re-Entry nach erstem RANI-Trade (closed bei $1.45-1.48)

Keine Fill-Bestätigung danach. Nächste RANI-Nachrichten sind nur watching/Kommentare.
Valid 3 min = extrem kurzes Fenster → vermutlich nicht gefüllt.

**Ergebnis: Vermutlich expired. PnL = $0.**

Falls gefüllt: TSL Peak $2.39, Exit ~$2.32 → +$1,113 (aber unwahrscheinlich)

---

## Trade 5: PSTV (ID 3536) — AH-Order, nicht gefüllt

**Signal:** "I will place an order at 0.55 to 0.57, Valid till 6:00 PM ET"
**Typ:** AH-Trade | **Datum:** 17. Okt 2025 15:18 ET
**Kontext:** Kein SL genannt → Default SL 7.2% = $0.52

**Kursdaten (unsplit, ÷25):** O $0.60, H $0.64, L $0.596, C $0.62
Daily Low $0.596 > Entry High $0.57 → **Limit nie erreicht.**

**Ergebnis: Nicht gefüllt. PnL = $0.**

**Parser-Erkenntnis:** "will place an order at X" + Preis + Expiry = Entry (Testfall hinzugefügt).
**Reverse Split:** PSTV 1:25 am 2. April 2026 — Kurse ÷25 für historische Vergleiche.

---

## Ergebnis-Übersicht

| # | Trade | Ticker | Typ | PnL Bot | PnL Jack (est.) | Bot besser? |
|---|---|---|---|---|---|---|
| 1 | RANI #1 | RANI | Day | +$1,931 | ~+$400 | ✅ TSL fing Spike |
| 2 | IVF | IVF | Day (Post-Spike) | +$141 | ~+$100 | ✅ Orphan Protection |
| 3 | OMER | OMER | Swing (Post-Spike) | +$393 | ~+$260 | ✅ TSL > Jack's Geduld |
| 4 | RANI #2 | RANI | Day (Re-Entry) | $0 (expired) | $0 (expired) | — |
| 5 | PSTV | PSTV | AH | $0 (not filled) | $0 (not filled) | — |
| **Gesamt** | | | | **+$2,465** | **~+$760** | **Bot 3.2× besser** |

## Noch zu simulieren
_(wird bei jedem neuen Trade im Review ergänzt)_

| ID | Ticker | Typ | Status |
|---|---|---|---|
| 3546 | CATX | Swing | ausstehend — nächste Session |
| ... | ... | ... | ... |
