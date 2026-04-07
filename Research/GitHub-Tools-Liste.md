---
tags: [research, github, tools]
updated: 2026-04-07
---

# GitHub Tools — Wertigkeit für unsere Projekte

## Priorisiert nach Nutzen

### Tier 1 — Sofort relevant
1. **[freqtrade](https://github.com/freqtrade/freqtrade)** — Python Crypto Trading Bot mit Backtesting, 1000+ Exchanges via CCXT. Für Binance Bots.
2. **[jesse](https://github.com/jesse-ai/jesse)** — Backtesting-Framework für Crypto-Strategien, sehr saubere API
3. **[ib_async](https://github.com/ib-api-reloaded/ib_async)** — Moderner Fork von ib_insync (unser IBKR-Client), aktiv maintained
4. **[vectorbt](https://github.com/polakowo/vectorbt)** — Hochperformantes Backtesting mit NumPy/Pandas, sehr schnell
5. **[Systematic Debugging](https://github.com/microsoft/debugpy)** — Systematisches Debugging-Framework für Python, VSCode-Integration

### Tier 2 — Mittelfristig nützlich
6. **[ccxt](https://github.com/ccxt/ccxt)** — 100+ Exchange-APIs in einem Package (Binance, Bybit, etc.)
7. **[Lumibot](https://github.com/Lumibot/lumibot)** — Trading Bot Framework mit IBKR + Alpaca Support, sehr einfach
8. **[quantstats](https://github.com/ranaroussi/quantstats)** — Portfolio-Statistiken und Berichte (Sharpe, Drawdown, etc.)
9. **[backtrader](https://github.com/mementum/backtrader)** — Etabliertes Python Backtesting-Framework
10. **[pandas-ta](https://github.com/twopirllc/pandas-ta)** — 130+ technische Indikatoren für Pandas DataFrames

### Tier 3 — Langfristig interessant
11. **[OpenBB Terminal](https://github.com/OpenBB-finance/OpenBBTerminal)** — Open-Source Bloomberg-Alternative, Fundamental + Technical Data
12. **[Zipline-Reloaded](https://github.com/stefan-jansen/zipline-reloaded)** — Algorithmic Trading Library (Quantopian-Fork), aktiv maintained
13. **[nautilus_trader](https://github.com/nautechsystems/nautilus_trader)** — High-Performance Trading Framework in Python/Rust
14. **[AlphaVantage](https://github.com/RomelTorres/alpha_vantage)** — Gratis Marktdaten API Wrapper (Alterntive zu yfinance)
15. **[Gymnasium](https://github.com/Farama-Foundation/Gymnasium)** — RL-Environments für Trading-Strategien mit KI

## Systematic Debugging — Notizen
- Für Python-Bot-Debugging: `debugpy` + VSCode Remote Debugging direkt auf VPS
- Setzt Remote-Debug-Port auf VPS auf → Claude Code / VSCode kann live debuggen
- Nützlich wenn der Bot seltsame Fehler produziert (IBKR-Events, async-Race-Conditions)
- Installation: `pip install debugpy`
- Start: `python -m debugpy --listen 0.0.0.0:5678 --wait-for-client main.py`

## Nächste Schritte
- [ ] freqtrade installieren + erste Binance-Strategie backtesten
- [ ] vectorbt für schnelleres Backtesting integrieren
- [ ] ib_async als Ersatz für ib_insync evaluieren
