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

## Min-Tick-Size-Rule (US-Aktien)

IBKR lehnt Orders ab, deren Limit/Stop-Preis die Mindest-Tickgröße verletzt: **Warning 110 "The price does not conform to the minimum price variation for this contract."**

| Preis-Range | Min-Tick | Rundung im Code |
|---|---|---|
| ≥ $1.00 | $0.01 (Cent) | `round(price, 2)` |
| < $1.00 | $0.0001 | `round(price, 4)` |

**Konsequenz bei Verletzung:** Order hängt endlos in `PendingSubmit`, wird nie routed. DB-Status kann "working" zeigen obwohl IBKR die Order gar nicht angenommen hat.

**Helfer im Code:**
- `signal_manager._tick_round(price)` — für Entry-Ladder, Default-SL
- `ibkr_client._tick_round(price)` — defensiv in place_stop_limit_buy/sell + place_market_exit

**Nie** `round(order_price, 4)` ohne Preis-Level-Check auf Order-Preise anwenden. Nur für Display/Log, nicht für `lmtPrice`/`stopPrice`/`auxPrice`.

**Historischer Incident:** 2026-04-23 LAES Trade #37 — 4/5 Stagger-Legs abgelehnt (4284 $2.444 / 4285 $2.522 / 4287 $2.8119 / 4288 $2.8938), nur Center-Leg 4286 $2.60 Submitted. Fix shipped in 7 Call-Sites (signal_manager, main, ibkr_client).

## Related

- [[Signal-Bot-MOC]] — nutzt diesen Broker
- [[Jack-Sparo]] — dessen Signale hierher geroutet werden
