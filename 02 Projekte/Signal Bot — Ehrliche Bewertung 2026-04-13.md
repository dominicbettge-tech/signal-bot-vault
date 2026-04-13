---
tags: [signal-bot, analyse, bewertung]
date: 2026-04-13
---

# Signal Bot — Ehrliche Bewertung (2026-04-13)

Basierend auf 6 Monaten Daten (2025-10-09 bis 2026-04-10), 2.824 Nachrichten, 122 Backtest-Signale, 68 gefüllte Trades.

## Die harten Zahlen

| Metrik | Wert | Bewertung |
|---|---|---|
| Nachrichten gesamt | 2.824 (6 Monate) | |
| Davon echte Entry-Signale | ~129 (4,9%) | 95% Rauschen |
| Signal-zu-Noise | 1:20 | Parser muss extrem präzise sein |
| Backtest: gefüllte Trades | 68 von 122 (56%) | Fast die Hälfte läuft ins Leere |
| Win Rate | 45,6% | Unter 50% |
| Total PnL (Backtest) | +$341 auf 68 Trades | ~$5 pro Trade — marginal |
| Avg Gewinn-Trade | +$45 (4,5%) | Gedeckelt durch TP2 |
| Avg Verlust-Trade | -$47 (-4,7%) | Symmetrisch — kein Edge im R:R |
| Swing Trades | -$174 gesamt, 11% WR | Klar negativ |
| Day Trades | +$440, 51% WR | Einzige profitable Kategorie |

## PnL-Verteilung

- `>+10%`: 0 Trades — kein einziger großer Gewinner
- `+5-10%`: 0 Trades
- `+0-5%`: 31 Trades — alle Gewinne hier (max 4,5%)
- `=0%`: 15 Trades (Expiry)
- `-0-5%`: 16 Trades
- `-5-10%`: 4 Trades
- `<-10%`: 2 Trades (bis -14%)

Gewinne bei 4,5% gedeckelt (TP2), Verluste gehen bis -14%. Asymmetrie in die falsche Richtung.

## Positiv

1. **Day Trades haben leichten Edge** — 51% WR bei +0,8% avg
2. **71% der Entries same-day erreichbar**, 69% gehen in die richtige Richtung
3. **Bot schneller als Mensch** — bei 10-20min Validity ein Vorteil
4. **Verpasste Live-Trades (SILO +$694, ADVB +$256)** zeigen echte Opportunity
5. **Trailing-SL funktioniert** — avg +$10 statt -$47 bei hartem SL
6. **Same-Day Performance genuinely positiv**: 71% WR bei Reachable Entries (Subagent-Analyse über Preisdaten)

## Negativ

1. **$341 auf 68 Trades über 6 Monate ist quasi Null** — nach Kosten breakeven
2. **Kein Trade über +5%** — TP2 schneidet Gewinner ab (manche Ticker liefen +40-120% same-day)
3. **Swing = Verlust** — -$174 bei 9 Trades, Penny Stocks overnight ist toxisch
4. **56% Fill-Rate** — fast die Hälfte der Signale verfällt
5. **Jack postet keine Exits** — nur 13% haben Exit-Post, Bot muss eigenständig managen
6. **SL fehlt in 72% der Signale** — Bot braucht eigene Defaults
7. **Split-Daten-Problem** — 17 Ticker mit falschen Preisdaten (Reverse Splits) verzerren Backtest
8. **Overnight-Halten zerstört Edge** — 3-Tage WR sinkt auf 39%, 5-Tage auf 35%

## Szenarien

### Mit Optimierungen (realistisch)
- Nur Day Trades (53/6Mo ≈ 9/Monat)
- Trailing-SL statt fester TP → avg Gewinn ~$15-25 statt $5
- Minus Kommissionen (~$3/Trade)
- **Erwartungswert: $100-200/Monat bei $10k = 1-2% monatlich**

### Ohne Optimierungen (Status Quo)
- $341/6Mo = $57/Monat vor Kosten
- Minus: Jack Abo ($33), VPS (~$10), Kommissionen (~$25)
- **Netto: ~$0 oder leicht negativ**

## Fazit

Das System ist aktuell breakeven bis marginal profitabel. Es hat einen realen, aber dünnen Edge bei Day Trades. Der Haupthebel liegt in **besserer Exit-Strategie** — TP2 bei 4,5% killt die großen Gewinner. Trailing-SL zeigt bereits bessere Ergebnisse. Nach Parser-Rebuild + TP-Kalibrierung im Testcenter: $100-300/Monat möglich. Aber: schmale Edge, kein Goldesel. Ein einzelner Bug-Tag kann den Monatsgewinn ausmachen oder zerstören.

## Haupthebel für Verbesserung (priorisiert)

1. **TP-Deckelung aufheben** — Trailing-SL statt fester TP2, Gewinne laufen lassen
2. **Swing Trades abschalten** — nur Day Trades
3. **Parser-Präzision** — bei 4,9% echten Signalen darf kein einziges falsch geparsed werden
4. **SL-Defaults kalibrieren** — eigene Defaults für die 72% ohne Jack-SL
5. **Fill-Rate verbessern** — aggressivere Limit-Preise oder Market-bei-Confirm
6. **Channel-Diversifikation** (Phase 6.5) — mehr Signalquellen statt größere Trades
