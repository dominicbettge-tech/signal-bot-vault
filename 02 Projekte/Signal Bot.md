---
tags: [projekt]
status: aktiv
erstellt: 2026-04-09
---

# Signal Bot v3

## Ziel

Vollautomatischer US-Aktienhandel über IBKR. Liest Signale aus Jack Sparo's Telegram-Kanälen, parsed sie mit Claude, führt Orders über Interactive Brokers aus. Aktuell Paper Trading — nach 2+ Wochen stabiler Performance → Live mit 5k€.

## Stack

- Python, SQLite, asyncio, ib_insync, Telethon
- VPS: Hostinger MK2 (187.124.166.210)
- Services: signal-bot, signal-watchdog, ibgateway

## Status

Paper Trading aktiv. Alle P0-P3 Bugs behoben (Stand 2026-04-09).

## Nächste Schritte

- [ ] 2+ Wochen fehlerfreies Paper Trading
- [ ] Performance auswerten
- [ ] Live-Start vorbereiten

## Bekannte offene Punkte

- GV Ghost-Short: BUY 500 Cover-Order PreSubmitted (füllt bei Marktöffnung)
- Replay-Bug: alte Telegram-Nachrichten bekommen Expiry ab "jetzt" nach Restart
- Separaten Anthropic API-Key für Bot erstellen

## Notizen

Backtest-Ergebnisse: [[Backtest 2026-04-07]]
Fehler-Historie: siehe [[Signal Bot Fehler-Log]]
