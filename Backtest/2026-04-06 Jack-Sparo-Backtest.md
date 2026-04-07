---
tags: [backtest, analysis, jack-sparo]
date: 2026-04-06
total_trades: 68
win_rate: 45.6
total_pnl: 341.50
---

# Backtest — Jack Sparo Signal-Analyse
*Erstellt: 2026-04-06 19:38*

## Zusammenfassung
| Metrik | Wert |
|--------|------|
| Trades gefüllt | 68 |
| Win-Rate | 45.6% |
| Gesamt-PnL | $341.50 |
| Ø PnL/Trade | $5.02 |
| Max Drawdown | $0.00 |

## Charts
![[backtest_equity.png]]
![[backtest_pnl_dist.png]]
![[backtest_exit_reasons.png]]
![[backtest_tickers.png]]
![[backtest_confidence.png]]

## Key Insights
- **Day Trades** performieren deutlich besser als Swing Trades
- **TP2-Exits** (+6%) erzielen den gesamten Gewinn ($1213)
- **Swing Trades** verlieren Geld — nur Day Trades handeln
- **Confidence** hat kaum Einfluss (fast alle Signale ≥ 0.8)
- Fill-Rate: nur 56% → viele Signale werden nicht ausgelöst

## Empfehlungen
1. Nur Day Trades ausführen (WR 51%, PnL $440)
2. Swing Trades deaktivieren (WR 11%, PnL -$174)
3. Größere Position bei hoher Confidence möglich
4. Trailing SL beibehalten (6 Trades, 67% WR)
