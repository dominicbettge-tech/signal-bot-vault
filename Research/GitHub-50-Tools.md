---
tags: [research, github, tools, priority]
updated: 2026-04-07
---

# GitHub — 50 Beste Tools für unsere Projekte
*Sortiert nach Priorität & Nutzen für Signal Bot, Backtesting, Crypto Bots*

---

## 🔴 TIER 1 — Sofort einsetzbar (direkt relevant)

| # | Tool | Stars | Nutzen für uns |
|---|------|-------|----------------|
| 1 | **[freqtrade](https://github.com/freqtrade/freqtrade)** | 48k | Binance Bots — Backtesting, Live Trading, Telegram-Control, 100+ Exchanges |
| 2 | **[ccxt](https://github.com/ccxt/ccxt)** | 42k | Binance + 100 weitere Exchanges in einer API — Basis für alle Crypto Bots |
| 3 | **[jesse](https://github.com/jesse-ai/jesse)** | 7.6k | Crypto Backtesting + Live Trading, saubere Python API, Paper Trading |
| 4 | **[ib_async](https://github.com/ib-api-reloaded/ib_async)** | 1.2k | Modernerer Fork von ib_insync — unser IBKR-Client, aktiv maintained |
| 5 | **[backtesting.py](https://github.com/kernc/backtesting.py)** | 6k | Schnelles Backtesting, interaktive Charts, sehr leicht zu bedienen |
| 6 | **[quantstats](https://github.com/ranaroussi/quantstats)** | 5k | Portfolio-Statistiken: Sharpe, Sortino, Drawdown, HTML-Reports |
| 7 | **[pandas-ta](https://github.com/twopirllc/pandas-ta)** | 5k | 130+ technische Indikatoren (RSI, MACD, BB) direkt in Pandas |
| 8 | **[vectorbt](https://github.com/polakowo/vectorbt)** | 4k | Ultra-schnelles Backtesting via NumPy, ideal für Grid-Search Optimierung |
| 9 | **[yfinance](https://github.com/ranaroussi/yfinance)** | 15k | Yahoo Finance Daten — bereits genutzt, gratis Tages + Intraday Kurse |
| 10 | **[telethon](https://github.com/LonamiWebs/Telethon)** | 10k | Telegram MTProto Client — bereits genutzt für Signal-Download |

---

## 🟠 TIER 2 — Kurzfristig (innerhalb 1 Monat einbauen)

| # | Tool | Stars | Nutzen für uns |
|---|------|-------|----------------|
| 11 | **[nautilus_trader](https://github.com/nautechsystems/nautilus_trader)** | 3k | High-Performance Event-Driven Trading Framework (Python + Rust), IBKR-Support |
| 12 | **[hftbacktest](https://github.com/nkaz001/hftbacktest)** | 2k | Tick-by-Tick Backtesting mit vollständigem Order Book — für präzisere Simulation |
| 13 | **[lumibot](https://github.com/Lumibot/lumibot)** | 2k | Einfaches Trading Framework mit IBKR + Alpaca, weniger Code als unser aktueller Bot |
| 14 | **[pyfolio-reloaded](https://github.com/stefan-jansen/pyfolio-reloaded)** | 800 | Portfolio Tear Sheets — automatische Visualisierung aller Trade-Metriken |
| 15 | **[EazeBot](https://github.com/MarcelBeining/EazeBot)** | 800 | Telegram Bot für Crypto Trading auf Exchanges — Referenz-Implementierung |
| 16 | **[finagg](https://github.com/theOGognf/finagg)** | 1k | Finanzdata-Aggregator: SEC, Fed, Yahoo Finance → SQLite/Pandas |
| 17 | **[akshare](https://github.com/akfamily/akshare)** | 10k | Gratis Finanzdata: Aktien, Crypto, Makro — Alternative zu yfinance |
| 18 | **[openbb](https://github.com/OpenBB-finance/OpenBBTerminal)** | 35k | Open-Source Bloomberg: Fundamentaldaten, News, Insider Trading |
| 19 | **[ta-lib](https://github.com/mrjbq7/ta-lib)** | 10k | C-basierte TA Library, 150+ Indikatoren, sehr schnell (schneller als pandas-ta) |
| 20 | **[python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)** | 27k | Stabilere Alternative zu aiogram für unseren Notification Bot |

---

## 🟡 TIER 3 — Mittelfristig (1-3 Monate)

| # | Tool | Stars | Nutzen für uns |
|---|------|-------|----------------|
| 21 | **[zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded)** | 1k | Quantopian-Fork, Event-Driven Backtesting, Fundamentaldaten-Integration |
| 22 | **[PyBroker](https://github.com/edtechre/pybroker)** | 2k | ML-fähiges Backtesting Framework mit Walk-Forward Optimization |
| 23 | **[FinRL](https://github.com/AI4Finance-Foundation/FinRL)** | 11k | Deep Reinforcement Learning für Trading — KI-Strategien entwickeln |
| 24 | **[Gymnasium](https://github.com/Farama-Foundation/Gymnasium)** | 8k | RL-Environments — Basis für KI-Trading-Strategien (mit FinRL) |
| 25 | **[stable-baselines3](https://github.com/DLR-RM/stable-baselines3)** | 10k | RL-Algorithmen für Trading-KI (PPO, A2C, SAC) |
| 26 | **[hummingbot](https://github.com/hummingbot/hummingbot)** | 18k | Market Making + HFT Bot, 50+ Exchanges, Binance direkt |
| 27 | **[pycryptobot](https://github.com/whittlem/pycryptobot)** | 2k | Simpler Crypto Bot mit Telegram-Alerts und Binance-Integration |
| 28 | **[qf-lib](https://github.com/quarkfin/qf-lib)** | 500 | Modulares Backtesting + Live Trading mit IBKR und Crypto-Support |
| 29 | **[qtpylib](https://github.com/ranaroussi/qtpylib)** | 2k | Event-Driven Algo Trading mit IBKR Paper/Live Support |
| 30 | **[alpaca-trade-api](https://github.com/alpacahq/alpaca-py)** | 1k | Alpaca als IBKR-Alternative für US-Aktien (Commission-Free) |

---

## 🟢 TIER 4 — Langfristig / Forschung

| # | Tool | Stars | Nutzen für uns |
|---|------|-------|----------------|
| 31 | **[awesome-systematic-trading](https://github.com/wangzhe3224/awesome-systematic-trading)** | 5k | Kuratierte Liste aller Quant-Tools — regelmäßig checken |
| 32 | **[best-of-algorithmic-trading](https://github.com/merovinh/best-of-algorithmic-trading)** | 2k | Wöchentlich aktualisierte Rangliste aller Trading-Tools |
| 33 | **[awesome-quant](https://github.com/wilsonfreitas/awesome-quant)** | 16k | Riesige Liste aller Quant-Finance-Ressourcen |
| 34 | **[riskfolio-lib](https://github.com/dcajasn/Riskfolio-Lib)** | 3k | Portfolio-Optimierung: Markowitz, Black-Litterman, Risk Parity |
| 35 | **[bt](https://github.com/pmorissette/bt)** | 2k | Flexibles Backtesting Framework, einfache Strategie-Komposition |
| 36 | **[lean](https://github.com/QuantConnect/Lean)** | 10k | QuantConnect Backtesting Engine (C#/Python), Institutionen-Grade |
| 37 | **[optuna](https://github.com/optuna/optuna)** | 12k | Hyperparameter-Optimierung — für Strategy Parameter Tuning |
| 38 | **[mlflow](https://github.com/mlflow/mlflow)** | 20k | Experiment-Tracking für Trading-Strategien und ML-Modelle |
| 39 | **[evidently](https://github.com/evidentlyai/evidently)** | 6k | ML/Modell-Monitoring — überwacht ob Claude-Parser noch akkurat ist |
| 40 | **[plotly](https://github.com/plotly/plotly.py)** | 17k | Interaktive Charts — bessere Backtest-Visualisierung als matplotlib |

---

## ⚙️ TIER 5 — Dev-Tools & Infrastruktur

| # | Tool | Stars | Nutzen für uns |
|---|------|-------|----------------|
| 41 | **[Systematic Debugging (debugpy)](https://github.com/microsoft/debugpy)** | 2k | Remote-Debugging des Bots direkt auf VPS via VSCode |
| 42 | **[loguru](https://github.com/Delgan/loguru)** | 22k | Besseres Logging als stdlib logging — farbe, rotation, structured |
| 43 | **[tenacity](https://github.com/jd/tenacity)** | 6k | Retry-Logic für API-Calls (IBKR, Anthropic, yfinance) |
| 44 | **[schedule](https://github.com/dbader/schedule)** | 12k | Einfacher Python Job Scheduler — Alterntive zu Cron für interne Tasks |
| 45 | **[pydantic](https://github.com/pydantic/pydantic)** | 23k | Data Validation für Trade-Models — bereits teilweise genutzt |
| 46 | **[rich](https://github.com/Textualize/rich)** | 50k | Schöne Terminal-Ausgabe für Backtest-Reports und Debug-Output |
| 47 | **[httpx](https://github.com/encode/httpx)** | 14k | Moderner async HTTP Client — Alternative zu requests für API-Calls |
| 48 | **[prometheus_client](https://github.com/prometheus/client_python)** | 4k | Metriken-Export für Bot-Monitoring (Grafana Dashboard) |
| 49 | **[SQLModel](https://github.com/fastapi/sqlmodel)** | 15k | SQLite ORM (Pydantic + SQLAlchemy) — cleaner als raw sqlite3 |
| 50 | **[typer](https://github.com/fastapi/typer)** | 17k | CLI-Tool-Builder — für unsere backtest scripts mit schönen Argumenten |

---

## 📋 Nächste Schritte

- [ ] **freqtrade** installieren + erste Binance Day-Trade-Strategie
- [ ] **vectorbt** für schnelleres Parameter-Grid-Search (ersetzt unser optimize.py)
- [ ] **quantstats** HTML-Report aus Backtest-Ergebnissen generieren
- [ ] **ib_async** evaluieren als ib_insync-Ersatz
- [ ] **debugpy** für Remote-VPS-Debugging einrichten
- [ ] **plotly** für interaktive Backtest-Charts (statt matplotlib)
- [ ] **optuna** für automatische Strategy-Optimierung

---

## Verwandt

- [[Research/GitHub-Tools-Liste|GitHub Tools — Wertigkeits-Matrix]] — Kurzliste mit Ranking-Details
- [[Signal-Bot-MOC]] — Haupt-Konsument der Tier-1-Tools
