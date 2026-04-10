# Researcher / Testzentrum — Smart Trader

> Autonomes Strategie-Testsystem für den Binance/Crypto-Bot. Ziel: stündlich neue Strategien generieren, backtesten, validieren — mit Ollama (lokal) + Kimi K2.5 (fast kostenlos).

## Status: AUF EIS (2026-04-10)

Service gestoppt und deaktiviert (`systemctl disable researcher`).

**Grund:** Trainingsdaten stammen aus dem Bärenmarkt 2022–2023. Backtest-Performance überträgt sich kaum auf Live-Trading. Energie wird stattdessen in den Binance Bot (Jack-Signale) investiert — echte Signale > generierte Strategien.

**Wiedereinstieg macht Sinn wenn:**
- Trainingsdaten regelmäßig aktualisiert werden
- Neue Strategien erst 2–4 Wochen live auf Testnet laufen bevor sie als "gut" gelten
- Ein echter Paper-Trading-Validierungsschritt vor dem Behalten existiert

### Bugs gefunden & behoben (2026-04-10, Opus-Analyse)

**Root Causes warum der alte Researcher in der Praxis versagt hat:**

1. **Orphaned Metrics (Hauptproblem):** `best_metrics_momentum.json` zeigte Sharpe 4.502, aber die zugehörige Strategie war manuell überschrieben worden und hatte tatsächlich Sharpe 0.052. Alle neuen Strategien wurden seitdem verworfen (0 kept in hunderten Generationen).

2. **Falsche Sharpe-Formel:** `sqrt(n / 10_symbole)` statt `sqrt(n / 2_jahre)` — mehr Trades = künstlich höherer Sharpe, Strategien nicht vergleichbar.

3. **Kein Integrity-Check:** Manuelles Überschreiben einer Strategie-Datei invalidierte die Metriken-Datei nicht.

**Fixes eingebaut:**
- `evaluate.py`: Sharpe-Formel korrigiert auf `sqrt(trades_per_year)`
- `researcher.py`: Integrity-Check beim Start (Drift > 0.5 → Reset)
- `researcher.py`: mtime-Check (Strategie neuer als Metriken → Re-Evaluation)
- `researcher.py`: Canonical `best_metrics.json` wird bei neuer Bestmarke mitsynchronisiert
- Alle Metriken-Dateien auf echte Werte zurückgesetzt

**Reale Baseline nach Reset:**
| Familie | Train Sharpe | Test Sharpe | Trades (Train) |
|---|---|---|---|
| breakout | +2.68 | +1.49 | 4086 |
| grid | +1.03 | +3.20 | 111 |
| momentum | +0.26 | +2.06 | 6403 |
| mean_reversion | +6.15 | +7.91 | 1106 (suspekt, wird re-evaluiert) |
| scalping | −5.20 | −4.33 | 6956 (negativ, Neusuche) |

---

## Pfad

```
/data/.openclaw/workspace/trading-bot/
├── TRADING_STATUS.md              ← Auto-aktualisiert alle 5 Min
├── bots/
│   ├── llm_trader/                ← Einfacher LLM-Trader (wenig genutzt)
│   │   ├── trader.py
│   │   └── requirements.txt
│   └── smart_trader/              ← Haupt-Bot
│       ├── bot.py                 ← Bot-Einstiegspunkt (Port 8766 paper, 8776 testnet)
│       ├── strategy.py            ← Trading-Strategie
│       ├── strategy_controller.py
│       ├── backtest.py
│       └── research/              ← Das Testzentrum
│           ├── researcher.py      ← Autonomer Researcher (Kimi K2.5)
│           ├── arena.py           ← Strategie-Arena
│           ├── evaluate.py        ← Backtest-Evaluation
│           ├── evaluate_vbt.py    ← VectorBT-Evaluation
│           ├── controller_researcher.py
│           ├── controller_decide.py
│           ├── daily_reviewer.py
│           ├── hyperopt.py        ← Hyperparameter-Optimierung
│           ├── prepare.py         ← Daten vorbereiten
│           ├── decay_detector.py
│           ├── regime_memory.py
│           ├── risk_manager.py
│           ├── post_mortem_analyzer.py
│           ├── reporter.py
│           └── data/              ← OHLCV CSVs (echte Daten!)
│               └── [SYMBOL]_train/test.[1h/15m/4h].csv
│                   BTC, ETH, SOL, BNB, ADA, AVAX, DOT, DOGE, LINK, XRP
└── results/
```

---

## Daten vorhanden

10 Symbole × 3 Timeframes (1h, 15m, 4h) × train/test Split:
- Train: 2022–2023
- Test: 2024–heute
- Funding Rates ebenfalls vorhanden

**Das ist gut** — echte Daten sind da. Das Problem war nicht die Datenbasis sondern der Researcher-Code der sie falsch/gar nicht genutzt hat.

---

## Strategie-Familien

| Familie | Best Strategy File | Metrics File |
|---|---|---|
| momentum | `best_strategy_momentum.py` | `best_metrics_momentum.json` |
| mean_reversion | `best_strategy_mean_reversion.py` | `best_metrics_mean_reversion.json` |
| breakout | `best_strategy_breakout.py` | `best_metrics_breakout.json` |
| scalping | `best_strategy_scalping.py` | `best_metrics_scalping.json` |
| grid | `best_strategy_grid.py` | `best_metrics_grid.json` |
| support_resistance | `best_strategy_support_resistance.py` | — |

Aktuelle beste Metriken (verdächtig hoch — wahrscheinlich Look-Ahead):
- Train Sharpe: 4.861 | Test Sharpe: 3.42 | Test Return: 54% | Gen: 64.778

---

## Wie researcher.py funktioniert (Konzept)

1. Lädt beste aktuelle Strategie + Metriken
2. Fragt Kimi K2.5 nach verbesserter Strategie
3. Bewertet auf TRAIN-Daten (2022–2023)
4. Prüft auf Look-Ahead-Betrug
5. Walk-Forward-Stabilitätstest
6. Validiert auf TEST-Daten (2024–heute)
7. Wenn besser → neue Bestmarke speichern
8. Plateau-Erkennung: nach 20 Gens ohne Fortschritt → Temperatur/Typ wechseln
9. HTTP `/progress` Endpoint auf Port 8767

---

## Das Problem (warum es scheiterte)

Der Researcher hat entweder:
- **Look-Ahead-Bias**: Zukünftige Daten in den Backtest durchsickern lassen
- **Halluzinierte Ergebnisse**: Das LLM hat Metriken erfunden statt wirklich zu rechnen
- **Falscher Daten-Split**: Testdaten während Training gesehen

Sharpe 4.86 auf Train + 3.42 auf Test ist bei 64.778 Generationen ein starkes Zeichen für Überanpassung oder Betrug.

---

## Ports

| Service | Port |
|---|---|
| Paper Bot | 8766 |
| Testnet Bot | 8776 |
| Researcher Progress | 8767 |

---

## Ziel: Sauberes Testzentrum (Phase 2)

**Vision:** Stündlicher Cycle:
1. LLM (Kimi K2.5 oder Ollama lokal) generiert neue Strategie
2. Echter Backtest auf CSV-Daten (kein Cheating)
3. Out-of-Sample Validierung auf separatem Test-Set
4. Nur wenn besser: Speichern + Telegram-Benachrichtigung
5. Wöchentliche Zusammenfassung

**Anti-Cheat-Anforderungen:**
- Strikte Train/Test-Trennung im Code
- Kein Zugriff auf Test-Daten während Generierung
- Ergebnisse reproduzierbar (seed fixieren)
- Metriken realistisch plausibilisieren (Sharpe > 3 = red flag)

---

## Nächste Schritte

- [ ] `researcher.py` auf Look-Ahead-Bug untersuchen
- [ ] Saubere Evaluation-Pipeline bauen (evaluate.py als Basis)
- [ ] Kimi K2.5 API-Key prüfen (in `.env`)
- [ ] Ollama-Modelle prüfen welche lokal verfügbar
- [ ] Researcher als systemd-Service mit stündlichem Trigger
