---
tags: [signal-bot, simulation, analyse]
date: 2026-04-13
---

# Signal Bot — Simulation: Vorher vs. Nach allen Fixes

Basierend auf 61 split-bereinigte Trades aus 6 Monaten (Okt 2025 – Jan 2026).
Bankroll $10k, Position $1k pro Trade.

## Die eine Änderung die alles ändert: TP-Cap entfernen

Das aktuelle System deckelt JEDEN Gewinn bei +4,5% (TP2). Das sind maximal $45 pro Trade.
Gleichzeitig laufen Verluste bis -14% ($140). **Das R:R-Verhältnis ist invertiert.**

Jack handelt Penny Stocks die regelmäßig +50% bis +200% intraday laufen. Von den 61 Trades:
- 20 Trades liefen >50% über Entry am selben Tag
- 36 Trades liefen 10-50% über Entry
- Nur 5 Trades liefen <10%

**Der Bot hat bei jedem dieser Monster-Moves bei +4,5% verkauft.**

## Ergebnisse

| Szenario | Total PnL | Pro Trade | Pro Monat |
|---|---|---|---|
| **AKTUELL** (TP2 4.5%, TSL 3% flat) | $503 | $8 | $84 |
| **OPTIMIERT** (TSL only, kein TP-Cap) | $27.414 | $449 | $4.569 |
| **REALISTISCH** (mit Slippage/Halts/Gaps) | $18.038 | $296 | $3.006 |

### Nur Day Trades (sicherste Variante)

| Szenario | Total PnL | Pro Trade | Pro Monat |
|---|---|---|---|
| AKTUELL | $601 | $13 | $100 |
| REALISTISCH | $16.847 | $366 | $2.808 |

### Monatliche Verteilung

| Monat | Realistisch |
|---|---|
| 2025-10 | $4.126 |
| 2025-11 | $2.745 |
| 2025-12 | $9.910 |
| 2026-01 | $1.257 |

## Welche Fixes treiben den Unterschied?

### 1. TP-Cap entfernen (~90% des Deltas)
- 27 von 68 Trades exiteten bei TP2 (+4.5% = $45)
- Davon liefen 27/27 danach DEUTLICH höher
- Top-Beispiel: MTC — TP2 bei $45, TSL hätte $3.007 gebracht (+6.600% mehr)
- **Allein diese Änderung verwandelt das System von breakeven zu profitabel**

### 2. TSL nach Trade-Typ (Day 3%, Swing 8%)
- Swing-Trades mit TSL 3% wurden systematisch rausgeschüttelt
- ELBM: mit 3% TSL = -$140 Verlust, mit 8% TSL = +$250 Gewinn
- Dreht Swings von -$174 auf ~+$1.000

### 3. Alle Parser-Bugfixes (18 Bugs behoben)
- Bessere Signal-Erkennung: +28 echte Entries (v2 vs v1)
- Weniger False Positives: halluzinierte Preise (VRAX), falsche Entry-Erkennung (GURE)
- Partial Exits korrekt verarbeitet
- Reply-Chain-Ticker korrekt aufgelöst

### 4. Slippage-Mitigation (noch nicht implementiert, geschätzt)
- Volume-Filter: ~20-30% der Signale fallen raus, Rest besser handelbar
- Mid-Price Limit: spart ~1-2% pro Trade
- Position-Size-Cap: kein Market Impact bei illiquiden Stocks

## Ehrliche Risiken & Caveats

### Was diese Simulation NICHT berücksichtigt:

1. **Survivorship Bias** — wir simulieren nur Trades die Jack gepostet hat. Er postet seine Verlierer seltener (nur 13% der Trades haben Exit-Posts).

2. **Halt-Risiko** — 20 der 61 Trades hatten >50% Intraday-Moves. Viele davon mit Trading-Halts. Während eines Halts kann der TSL NICHT triggern. Der Kurs kann nach dem Halt 30%+ unter dem TSL-Level eröffnen.

3. **Penny Stock Liquidität** — bei $0.30-Stocks mit Spread $0.01-0.02 ist das schon 3-7% Slippage. Die "realistischen" Discount-Faktoren (50-95%) sind geschätzt, nicht gemessen.

4. **Klumpenrisiko** — Dezember 2025 allein brachte $9.910 (55% des Gesamtertrags). Ein schlechter Monat und der Jahresgewinn halbiert sich.

5. **Pattern Decay** — Penny Stock Momentum-Trading kann aufhören zu funktionieren wenn: (a) Jack's Signale schlechter werden, (b) zu viele Follower die gleichen Trades machen (Crowding), (c) Marktregime wechselt.

6. **Sample Size** — 61 Trades in 4 Monaten (Jan-Daten enden). Statistisch nicht signifikant. Die Konfidenz-Intervalle sind riesig.

7. **Keine Kommissions-Slippage auf Penny Stocks** — IBKR berechnet Minimum $1 pro Trade. Bei $0.30-Stocks mit 3000+ Shares können SEC/FINRA-Fees relevant werden.

### Discount-Faktoren in der "realistischen" Simulation:
- Monster-Trades (>100% Move): 50% des TSL-Profits (Halts, Gaps)
- Große Trades (50-100%): 70%
- Normale Trades (10-50%): 85%
- Kleine Trades (<10%): 95%
- Verluste: 100% (kein Discount — Verluste sind real)

## Netto-Rechnung (pro Monat, realistisch)

| Posten | Betrag |
|---|---|
| Brutto-Ertrag | $3.006 |
| - Kommissionen | -$25 |
| - Jack Abo | -$33 |
| - VPS | -$10 |
| - Claude API | -$15 |
| **Netto** | **$2.923** |

**ROI auf $10k Bankroll: ~350% p.a.** — ABER mit hoher Varianz und den oben genannten Risiken.

## Empfohlene Änderungen (priorisiert)

| Priorität | Änderung | Geschätzter Impact |
|---|---|---|
| **P0** | TP-Cap entfernen, nur TSL | +$17.000/6Mo (90% des Deltas) |
| **P1** | TSL nach Trade-Typ (Day 3%, Swing 8%) | +$1.200/6Mo |
| **P2** | Parser-Bugs alle fixen (v2 fertig) | +28 Entries, weniger False Positives |
| **P3** | Volume-Filter | Weniger Trades, bessere Fill-Rate |
| **P4** | Averaging-Support | Geschätzt +20% auf Swing-Trades |

## Fazit

> **Das System hat echtes Profit-Potenzial — aber der TP-Cap bei 4,5% zerstört es komplett.** Eine einzige Config-Änderung (TP2 entfernen, nur TSL) verwandelt ein breakeven-System in ein hochprofitables. Die Zahlen sind mit Vorsicht zu genießen (kleines Sample, Penny-Stock-Risiken), aber der Kern-Befund ist robust: Jack pickt Stocks die explodieren, und der Bot schneidet die Gewinne bei +4,5% ab. Das ist wie einen Rennwagen im ersten Gang fahren.
