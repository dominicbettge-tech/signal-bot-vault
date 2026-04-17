# Signal Bot — Time-of-Day-Analyse

_Generiert: 2026-04-17T21:08:13.512465+00:00_

## Setup
- **Korpus:** `human_verdict='b'` außer SLS (83 trades, skipped 0)
- **Exit:** H2-Ladder [0.05, 0.1, 0.2] × [0.33, 0.33, 0.34], SL -3%, TTL 240min
- **Entry:** next-bar-open nach Msg
- **Buckets ET:** premarket 04:00-09:30 · open 09:30-10:30 · mid_morning 10:30-12:00 · lunch 12:00-14:00 · afternoon 14:00-15:30 · close 15:30-16:00 · after_hours 16:00-20:00

## PnL je Bucket

| Bucket | n | Mean-PnL | Median | Winrate | SL-Hit | TP-Full |
|---|---|---|---|---|---|---|
| premarket | 22 | -1.305% | -3.00% | 14% | 19/22 | 1/22 |
| open | 20 | -0.490% | -3.00% | 20% | 17/20 | 2/20 |
| mid_morning | 18 | -0.409% | -2.66% | 17% | 11/18 | 1/18 |
| lunch | 9 | +0.839% | -1.95% | 44% | 4/9 | 1/9 |
| afternoon | 9 | +1.849% | -0.29% | 33% | 3/9 | 2/9 |
| close | 0 | — | — | — | — | — |
| after_hours | 5 | -1.747% | -3.00% | 20% | 3/5 | 0/5 |
| overnight | 0 | — | — | — | — | — |

## Best / Worst-Bucket (n≥5)
- **Best:** `afternoon` Mean=+1.85% (n=9)
- **Worst:** `after_hours` Mean=-1.75% (n=5)
- **Spread:** 3.60pp

## Verteilung Buy-Signale je Tageszeit

- `premarket   `  22 (26.5%) █████████████
- `open        `  20 (24.1%) ████████████
- `mid_morning `  18 (21.7%) ██████████
- `lunch       `   9 (10.8%) █████
- `afternoon   `   9 (10.8%) █████
- `close       `   0 ( 0.0%) 
- `after_hours `   5 ( 6.0%) ███
- `overnight   `   0 ( 0.0%) 

## Interpretation
- **Dünn besetzte Buckets (n<5)** nicht aussagekräftig → brauchen mehr Corpus
- **Premarket / AH** meist dünne Liquidität → vorsichtig interpretieren
- Spread Best-Worst gibt Hinweis, ob Time-of-Day-Filter Edge bringen könnte

### 🚨 Kritischer Befund: Premarket = Bot-Killer

- **Premarket: SL-Hit-Rate 86% (19/22)**. Mean -1.31%, WR 14%
- 26.5% aller Jack-Buy-Signale kommen premarket → größter einzelner Bucket
- Pattern: Jack postet vor Open, Premarket-Rip, Bot kauft aufs Hoch, RTH-Open fällt → SL

### 🟢 Grüne Zone: Lunch + Afternoon

- **Lunch** (12:00-14:00): Mean +0.84%, WR 44% (n=9)
- **Afternoon** (14:00-15:30): Mean **+1.85%**, WR 33% (n=9)
- Pattern-Hypothese: Nachmittags-Setups haben klareren Trend/Volumen, weniger „News-Pop-Drop"

### Hypothese-Kandidat (R-Library)

**R-Hypo-TOD1:** Premarket-Size-Halvierung oder Wait-for-RTH-Open
- Evidenz: 19/22 SL-Hit-Rate im Premarket
- Alternative: Order als Limit an Premarket-VWAP setzen statt Market
- Gate: n≥30 Premarket nötig für Default-Change

**R-Hypo-TOD2:** Lunch+Afternoon-Boost
- Evidenz: Spread +3.6pp vs. Premarket
- Alternative: Position-Size +10% in diesen Fenstern
- Gate: n≥20 je Bucket nötig

## Actionable Ideas (wenn Spread > 2pp)
- **Time-of-Day-Gate:** Worst-Bucket Size-Reduktion 50% oder Skip
- **Best-Bucket-Bonus:** Position-Size +10% im Best-Fenster
- Testen im Phase-C Parameter-Sweep mit Walk-Forward

## Generalisierungs-Vorbehalt (REGEL 4)
- In-Sample n=83 — einzelne Buckets haben teils n<10
- Jack-Posting-Pattern saisonal (Earnings, News-Events) → kein stabiles Zeit-Regime
- Penny-Stock-Liquidität verändert sich regelbasiert mit Catalysts

## Verbindungen memory
- `project_testcenter_intraday.md`: Premarket/AH-Daten MUSS für Jack
- `feedback_adaptive_stack_validated.md`: H2 Ladder als Standardexit
