---
tags: [parser, regeln]
zuletzt: 2026-04-10
---

# Parser-Regeln — aus Jack-Review abgeleitet

Diese Regeln werden direkt in den Parser übersetzt sobald die Review abgeschlossen ist.

---

## Signal-Typen

### entry
- Ticker + Preis + SL = klares Entry-Signal
- "Valid for X minutes" = Expiry in Minuten ab Nachrichtenzeit
- "day trade" = trade_type=daytrade, Expiry Ende des Handelstages falls kein explizites Expiry
- "swing" = trade_type=swing, kein Expiry
- "Placed an order at X" = Limit-Order bei X

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
