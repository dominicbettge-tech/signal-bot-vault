---
tags: [parser, regeln]
zuletzt: 2026-04-10
---

# Parser-Regeln — aus Jack-Review abgeleitet

Diese Regeln werden direkt in den Parser übersetzt sobald die Review abgeschlossen ist.

---

## Signal-Typen

### entry

#### Grundregeln
- Ticker + Preis + SL = klares Entry-Signal
- "Valid for X minutes" = Expiry in Minuten ab Nachrichtenzeit
- "day trade" = trade_type=daytrade, Expiry Ende des Handelstages falls kein explizites Expiry
- "swing" = trade_type=swing, kein Expiry
- Fehlender SL → Bot setzt Default-SL
- **"might" + konkreter Preis = Entry** (Evidenz: ID 3564 OMEX, ID 5621 FUSE)
- **"might" OHNE Preis = Watchlist** (z.B. "might share a trade soon")

#### Entry-Phrasen (vollständige Liste aus Review 2026-04-12)

**Kategorie 1: "Placed an order" — Order bereits platziert**
- "Placed an order at X" (häufigste Form, 37+ Treffer)
- "Placed me an order at X" (3535)
- "Placed an order at X for TICKER" (3697)
- "I placed an order at X" (3663, 3712, 3728, 3763)
- "I placed a risky order at X" (3663 CMBM)
- "I placed three orders: X / X / X" (3763 DRMA)
- "Placed another order at X" (3696)
- "TICKER last order for today placed around X" (3588 LAES)
- "New order at X" (3889)
- "Update the order … X" = Order-Ersatz (3891)
- "Will cancel and edit the order to X" = neues Entry nach Halt (3781 INHD, 3875, 3933)

**Kategorie 2: "Will place" — Ankündigung**
- "I will place an order at X" (3536 PSTV)
- "I will go on and place an order at X" (3772 SOND)

**Kategorie 3: "Might" + konkreter Preis = Entry**
- "Might place an order at X" (3824)
- "Might risk and get some if my order at X" (3524 IVF)
- "Small position might be opened at X for swing" (3564 OMEX)
- "Might add if it fills my order at X" (3677)

**Kategorie 4: "Starting / Opening a position"**
- "I am going to take the risk and open a position around X" (3517 RANI)
- "I may start a position X up to Y" (3546 CATX)
- "I am starting a small position in TICKER if it stays above X" (3638 WGRX)
- "Started small at X" (3586 LAES)
- "I started an order at X" (3723 AKBA)
- "I am risking and adding some … at current price" (3608)

**Kategorie 5: Price Alert + Order Combo**
- "Price alert at X … I may place an order around that" (3962 GNS)
- "I placed a price alert at X and an order to start at Y" (3887)

**Kategorie 6: Zone-basiert**
- "below X and above Y a loading zone … valid till further notice" (3881 GNS)
- "X to Y might adding zone for swing" (3701 LAES)
- "below X is my incoming adding zone" (3659 VSTM)

**Kategorie 7: Implizit — Ticker + Preis + SL + Expiry ohne Trigger-Phrase**
Format: `TICKER / Day trade / PREIS / SL / SL_PREIS / Valid for X minutes`
Erkennung: Ticker + Preisnummer + "SL" + "Valid for" = Entry auch ohne Verb (3488, 3510, 3560, 3577, 3623, 3626, 3644, 3705, 3727, 3738)

#### Averaging/Nachkauf-Phrasen (eigener Signal-Typ `averaging`)

Nur wenn Bot bereits in Position ist. Sonst = neues Entry.

- "Added some TICKER at X" (3696, 3863, 3934)
- "Added more TICKER X" (3698 VSTM)
- "Added little more TICKER at X" (3574 OMEX, 3714 ELDN)
- "I am adding some TICKER" (3863, 3934)
- "I am adding little more TICKER at X to average my spot" (3796)
- "Averaged little on TICKER at X" (3910)
- "added some at X but small" (3715 SLS)
- "I might add more around X" (3700, 3805)
- "might start adding" (3892)
- "might average at X" (3555 OMER)

#### Fill-Bestätigungen (Signal-Typ `update`, KEIN neues Entry)

- "Filled" (standalone reply, 3526, 3578, 3798, 3849)
- "Filled at X" (3821, 3837)
- "TICKER order filled at X" (3527, 3580)
- "Got my orders at X then Y filled" (3773 SOND)
- "Got two orders filled X / Y" (3790)
- "I got few at X" (3936 TGL)
- "TICKER X filled for me" (5546)

### update / kein neues Entry
- "X filled for me" = Jack ist bereits drin → kein neues Entry für Bot, sondern `update`
- *(weitere Regeln folgen)*

---

### Nicht traden: "filled for me" + Jack managed im AH/PM → Bot kann nicht folgen

- **Regel:** Wenn Jack sagt "X filled for me" → **nicht einsteigen**, wenn der Bot keine AH/PM-Exits unterstützt. Jacks Gewinne kommen oft aus After-Hours/Pre-Market Management, das der Bot in Regular Session nicht replizieren kann.

- **Beispiel ID 3469 (ELBM, 2025-10-14 → 15):**
  - Jack Entry: $4.65 (14.10, 14:06 UTC / 10:06 ET Regular Session)
  - Jack sagt: 30% Teilverkauf "around 5", 70% overnight gehalten, Rest bei $4.50 geschlossen → P&L exakt $0 (breakeven)

- **Zeitliche Rekonstruktion (UTC → ET, US Eastern):**
  | UTC | ET | Phase | Event |
  |---|---|---|---|
  | 14.10 14:06 | 10:06 | RTH | Entry @ $4.65 |
  | 14.10 21:27 | **17:27** | **After-Hours** | "took profit around 5" (30%) |
  | 15.10 13:18 | **9:18** | **Pre-Market** | "closed at 4.50" (70%) |

- **Kursdaten (Daily OHLC):**
  | Datum | Open | High | Low | Close |
  |---|---|---|---|---|
  | 14.10 | $6.22 | $6.32 | $4.21 | $4.71 |
  | 15.10 | $4.27 | $4.28 | $2.17 | $2.31 |

- **Warum Bot das nicht kann:**
  - 30% @ $5 existierte nicht in Regular Session (RTH-High nach Entry ~$4.71) → After-Hours Exit
  - 70% @ $4.50 existierte nicht am 15.10 (Open schon $4.27) → Pre-Market Exit
  - Bot mit SL $4.00 hätte Tag 1 überlebt (Low $4.21), Tag 2 beim Crash auf $2.17 SL getriggert
  - **Bot-Verlust: ~-14%** vs. **Jack: breakeven**

- **P&L-Mathematik (bestätigt Jacks Aussage):**
  - Teil 1: `(5.00 - 4.65) × 0.30 = +$0.105/share`
  - Teil 2: `(4.50 - 4.65) × 0.70 = -$0.105/share`
  - Gesamt: `$0.000/share` ✅ breakeven

- **Fazit:** Jacks Edge ist AH/PM-Trading. Solange der Bot keine `LimitOrder` mit `outsideRth=True` spielt, sind solche Trades ein Verlustgeschäft.

- **Verknüpfung:** [[../../05 Daily Notes/2026-04-10]] — AH-Exit ist das Wochenendprojekt

### Bedingte Orders müssen als "unfilled" erkannt werden

- **Regel:** Signale mit Preislimit (`"at X"`, `"if it gets to X"`, `"placed an order at X"`) dürfen nur als Trade gezählt werden, wenn der Tages-Low (Long) bzw. Tages-High (Short) den Limit-Preis tatsächlich erreicht hat.
- **Beispiel PSTV (ID 3513, 2026-10-16):** "if it gets to 0.56 AH I am adding some" — RTH-Low am Tag war $0.60 → Order nie gefüllt.
- **Beispiel PSTV (ID 3536, 2026-10-17):** "I will place an order at 0.55 to 0.57" — RTH-Low $0.60 → nie gefüllt.
- **Parser muss:** Bei Limit-Orders den tatsächlichen Kursverlauf (Tages-OHLC oder Intraday) prüfen, bevor der Trade als "ausgeführt" markiert wird.
- **Konsequenz:** Backtest-Statistiken werden verfälscht wenn nicht-gefüllte Orders wie gefüllte behandelt werden.

## Offene Fragen

*Keine offenen Fragen.*
