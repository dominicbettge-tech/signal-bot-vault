---
title: IBKR Paper Trading
type: tool
tags: [broker, paper-trading, execution]
created: 2026-04-20
updated: 2026-04-20
---

## Summary

Interactive Brokers Paper-Trading-Account = Ausführungs-Backend des [[Signal-Bot-MOC|Signal Bot]]. Simuliert echtes Trading gegen Live-Markt-Daten ohne echtes Geld. Verbindung via ib_insync + IB Gateway.

## Konfiguration (aus .env)

- `TRADING_MODE=paper` — nie auf live ohne explizite Anweisung
- `MAX_BANKROLL_USD=10000` — $10k Limit
- `MAX_OPEN_POSITIONS=5`
- `POSITION_SIZE_PERCENT=20` — 20% Bankroll pro Trade
- NetLiq aktuell: ~$1.25M (2026-04-20 Health Check)

## Code-Referenz

- `/root/signal_bot/ibkr_client.py` — Client-Wrapper
- Service: `systemctl status ibgateway`

## Regeln

- `.env` niemals committen oder ändern ohne Anweisung
- `TRADING_MODE=live` niemals setzen ohne explizite User-Anweisung
- Nach IBKR-Config-Änderungen: IB Gateway Reconnect nötig

## Related

- [[Signal-Bot-MOC]] — nutzt diesen Broker
- [[Jack-Sparo]] — dessen Signale hierher geroutet werden
