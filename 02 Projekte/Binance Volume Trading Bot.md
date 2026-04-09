---
tags: [projekt]
status: aktiv
erstellt: 2026-04-09
phase: Planung
rhythmus: Schrittweise — wird mit freien Token aus dem Pro-Abo bearbeitet
signalquelle: offen — Überlegung externe Signale (Telegram/Copy Trading) statt eigener Generierung
---

# Binance Volume Trading Bot

## Ziel

Automatisierter Krypto-Handelsbot auf Binance der auf Basis von Volumen-Analyse und News-Sentiment handelt.

## Offene Grundsatzentscheidung: Signalquelle

| Option | Aufwand | Vorteil |
|---|---|---|
| Telegram-Kanäle (wie Jack) | niedrig — Parser vom Signal Bot wiederverwendbar | flexibel, günstig |
| Binance Copy Trading | sehr niedrig — direkt auf Plattform | einfachste Integration |
| 3Commas / Cornix | mittel | großer Marktplatz |
| TradingView Webhooks | mittel | viele Trader, professionell |
| Eigene Signale (Volumen+News) | hoch | unabhängig |

## Konzept

- **Volumentrading:** Trades basieren auf ungewöhnlichen Volumenspitzen
- **News-Layer:** Taranis AI liest News aus → Bot reagiert auf relevante Ereignisse
- **Wissensbasis:** Bot wird mit Trading-Büchern gefüttert → kontextuelles Marktverständnis

## Checkliste — Was wir brauchen

### Infrastruktur
- [ ] 1. Binance Account + API-Key (mit Trading-Rechten)
- [ ] 2. Taranis AI installiert & konfiguriert (Docker)
- [ ] 3. VPS-Ressourcen prüfen (~2-4GB RAM für Taranis)

### Daten & Wissen
- [x] 4. Trading-Bücher als Wissensbasis (10 PDFs in `/root/books/`)
- [ ] 5. Coin-/Pair-Liste definieren
- [ ] 6. Volumen-Schwellenwerte definieren

### Bot-Komponenten (Code)
- [x] 7. Binance API Client (Marktdaten + Order-Execution) ← Smart Trader Basis
- [ ] 8. Volumen-Analyse Modul (Spike-Erkennung)
- [ ] 9. Taranis API Client (News + Sentiment)
- [ ] 10. Signal-Logik (Volumen + News → Trade)
- [ ] 11. Order-Management (Entry, SL, TP)
- [ ] 12. Risiko-Management (Position Sizing, Max Daily Loss)
- [ ] 13. Datenbank (SQLite — Trades, Signale, Performance)
- [ ] 14. Telegram-Notifier

### Testing
- [ ] 15. Paper Trading (Binance Testnet)
- [ ] 16. Backtest-Framework

### Offene Entscheidungen
- [ ] 17. Spot oder Futures?
- [ ] 18. Welche Coins? (Top 20, nur BTC/ETH, breiter?)
- [ ] 19. Timeframe? (1m, 5m, 15m)

## Wissensbasis — Trading-Bücher (`/root/books/`)

- Jack D. Schwager — Market Wizards
- Jack D. Schwager — The New Market Wizards
- Jack D. Schwager — Hedge Fund Market Wizards
- Alexander Elder — Come Into My Trading Room
- Alexander Elder — Study Guide for the New
- John J. Murphy — Technical Analysis of the Financial Markets
- Mark Douglas — Trading in the Zone
- Edwin Lefèvre — Reminiscences of a Stock Operator
- Michael W. Covel — The Little Book of Trading
- Sandra Kalde — Mein 1. Jahr als Trader

## Vorgänger: Smart Trader (Backup: `/root/smart_trader_backup_20260325_1933.tar.gz`)

Bereits fertiger Binance Bot — kann als Basis genutzt werden:
- Binance API via httpx/aiohttp (kein Key für Marktdaten nötig)
- Symbole: BTCUSDT, ETHUSDT, SOLUSDT — 1h Timeframe
- LLM: Ollama/Kimi K2.5 bereits integriert
- Paper Trading Modus vorhanden
- Risiko: ATR-basiert, 10% Position Size, max. 3 Positionen
- Telegram-Notifier vorhanden
- HTTP-API auf Port 8766

→ Checkliste Punkt 7 (Binance API Client) ist damit bereits erledigt.

## Taranis AI (News-Layer)

- **GitHub:** https://github.com/taranis-ai/taranis-ai
- **Was es ist:** Open-Source OSINT-Plattform — sammelt und analysiert News aus Websites, RSS, Social Media, Email
- **Stack:** 82% Python, PostgreSQL/SQLite, RabbitMQ, Celery
- **Integration:** Bot fragt Taranis REST API nach aufbereiteten News-Signalen
- **Flow:** News-Ereignis → Taranis → Bot prüft Volumen → Trade-Entscheidung

## Referenzen

- [[Trading]]
- [[Claude Skills]]
