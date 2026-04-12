---
tags: [signal-bot, parser-review, kalibrierung]
created: 2026-04-12
---

# Orphan Protection — Kalibrierung nach Review

## Status: VORLÄUFIG — Werte erst nach komplettem Parser-Review finalisieren!

## Was ist Orphan Protection?
Nach einem Partial Exit von Jack verwaist die Restposition. Der Bot setzt automatisch gestaffelte TPs + angepassten SL.

## Aktuelle Werte (basierend auf IVF-Trade ID 3524-3533)

| Parameter | Wert | Begründung | Config-Key |
|---|---|---|---|
| TP Stufe 1 | +7% vom Exit-Preis | Jack's erster Exit war +5.8%, zweiter +10.9% | `ORPHAN_TP_STEP_PERCENT` |
| TP Stufe 2 | +15% vom Exit-Preis | Konservativ über Jack's zweitem Exit | `ORPHAN_TP_STEP2_PERCENT` |
| SL | Midpoint Entry↔Exit | Nicht pure BE (zu eng bei Penny Stocks) | `ORPHAN_SL_MIDPOINT` |
| TP1 Sell% | 50% der Restposition | Gestaffelt raus | hardcoded |
| TP2 Sell% | 100% Rest | Alles raus | hardcoded |

## Offene Fragen für Kalibrierung
- [ ] Sind +7% / +15% bei allen Trade-Typen sinnvoll oder nur bei Penny Stocks?
- [ ] Sollte der Midpoint-SL bei Swings anders sein als bei Day Trades?
- [ ] Wie oft lässt Jack Restpositionen "verwaisen"? (Häufigkeit im Review zählen)
- [ ] Bei welchen Trades wäre der Midpoint-SL zu eng / zu weit gewesen?
- [ ] Sollten TP-Sell-Prozente (50%/100%) auch konfigurierbar sein?
- [ ] Sollte Orphan Protection erst nach X Minuten ohne neues Signal aktivieren statt sofort?

## Datensammlung aus Parser-Review

| Trade ID | Ticker | Partial Exits | Restposition? | Was wäre mit Orphan Protection passiert? |
|---|---|---|---|---|
| 3524-3533 | IVF | 50% @ 0.825, 25% @ 0.865 | 25% (kein Exit-Signal) | TP1 $0.93, TP2 $0.99, SL $0.82 — vermutlich SL getriggert (Kurs fiel auf Close $0.60 split-adj) |

**WICHTIG:** Diese Tabelle bei jedem Partial-Exit-Trade im Review ergänzen!

## Swing-Trade-Problem: OMER (ID 3521-3760)

Jack's OMER-Trade zeigt ein grundsätzliches Problem mit Swing-Trades:

| Datum | Event | Jack | Bot |
|---|---|---|---|
| 17. Okt | Entry $8.40, SL $7.75 | ✅ | ✅ |
| 21. Okt | Kurs fällt auf $7.77 | Senkt SL mental auf $6.85 (ID 3555) | SL $7.75 hält noch |
| 22. Okt | Low $7.425 | Hält weiter | **SL getriggert → -$154.70** |
| 28. Okt | Kurs $7.96 | "still holding patiently" | Position geschlossen |
| 17. Nov | Kurs grün | "green for me team" | Nicht mehr investiert |

### Vollständige Simulation (alle Szenarien)

| Szenario | Exit-Datum | Exit-Preis | PnL (238 Shares) | Bewertung |
|---|---|---|---|---|
| **A: Bot Original SL + Trailing SL 3%** | **20. Okt (TSL)** | **~$10.05** | **+$392.70** | ✅ BESTES ERGEBNIS |
| B: Bot mit Jack's SL-Update $6.85 + TSL | 20. Okt (TSL) | ~$10.05 | +$392.70 | ✅ TSL schlägt vorher zu |
| C: Nur Original SL $7.75 (kein TSL) | 22. Okt | $7.75 | -$154.70 | ❌ |
| D: Nur Jack's SL $6.85 (kein TSL) | 4. Nov | $6.85 | -$368.90 | ❌❌ |
| E: Jack real (avg down, mental SL) | hält bis 17. Nov+ | ~$9.10 | ~+$260 (geschätzt) | ⚠️ mit -20% Drawdown |

**Kurs-Spike am 17. Nov:** OMER sprang von $7.90 auf $9.10 — daher Jack's "green for me".
Aber: Sein SL $6.85 wurde am 4. Nov (Low $6.71) und 14. Nov (Low $6.24) durchbrochen.
Jack hat entweder keinen echten SL gesetzt oder ihn still entfernt → mentaler SL ≠ realer SL.

### Erkenntnisse

1. **Trailing SL 3% war hier BESSER als Jack** — Bot +$393 vs Jack ~+$260 (mit 4 Wochen Stress)
2. **Jack's SL-Updates blind zu folgen ist gefährlich** — sein Update auf $6.85 hätte -$369 gekostet
3. **Trailing SL schützt vor Jack's Optimismus** — er hielt durch -20% Drawdown, unser Bot sicherte Gewinne
4. **Vorherige Annahme "TSL zu eng für Swings" war FALSCH** — zumindest für Post-Spike-Swings ist TSL optimal
5. **Jack's Nachkauf-Strategie (avg down) ist für den Bot nicht sinnvoll** — erhöht Risiko, unser TSL-Exit war profitabler
6. **Jack's mentaler vs realer SL divergieren** — er postet SL-Levels aber hält sie nicht ein

### Regel-Ableitung
- ✅ Trailing SL bei Swing-Trades BEHALTEN (nicht deaktivieren)
- ⚠️ Jack's SL-Updates parsen, ABER: nur als Untergrenze nutzen (SL nur SENKEN, nie unter TSL)
- ❌ Nachkauf/Average Down NICHT implementieren — zu riskant, TSL-Exit ist profitabler
- ✅ Post-Spike-Entries sind OK wenn TSL aktiv ist — TSL fängt den Gewinn auf dem Rückweg

### Parser-Rules TODO
- [x] "cut it off if it drops below X" → `STOP_LOSS_UPDATE` mit neuem SL (Testfall hinzugefügt)
- [ ] "might average at X" → `n` (ignorieren, kein Nachkauf für Bot)

## Verwandt
- [[Signal Bot Live-Roadmap]] Phase D
- [[Signal Bot]] Hauptseite
