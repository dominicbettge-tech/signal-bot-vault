---
tags: [bereich]
---

# Trading

## Beschreibung

Automatisierter US-Aktienhandel über Interactive Brokers. Signalquelle: Jack Sparo's Telegram-Kanäle. Aktuell Paper Trading — Ziel: Live-Start nach 2+ Wochen stabiler Performance.

## Strategie (aus Backtest 2026-04-07)

- **Nur Day Trades** — Swing Trades verlieren Geld
- **SL:** 2% vom Entry
- **TP1:** +5%, **TP2:** +10%
- **Win Rate:** 62% | **Profit Factor:** 3.92 | **Expectancy:** ~$80/Trade
- **Position Size:** 20% des Bankrolls pro Trade

## Aktuelle Kanäle

- JACK SPARO PREMIUM TRADING GROUP (`-1002677824966`)
- JACK SPARO BIOTECH STOCKS – THE SPECIAL TRADES (`-1003775983137`)

## Laufende Parameter (.env)

| Parameter | Wert |
|---|---|
| MAX_BANKROLL_USD | $10.000 |
| MAX_OPEN_POSITIONS | 5 |
| POSITION_SIZE_PERCENT | 20% |
| TRAILING_SL_PERCENT | 3.0% |
| TRADING_MODE | paper |

## Referenzen

- [[Signal Bot v3]]
- [[Backtest 2026-04-06 Jack-Sparo-Backtest]]
