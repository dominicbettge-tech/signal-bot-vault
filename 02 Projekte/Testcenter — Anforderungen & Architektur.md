---
tags: [signal-bot, testcenter, architektur, analyse]
date: 2026-04-13
status: draft
---

# Testcenter — Was braucht es für echte Verbesserungen?

## Zusammenfassung

Unsere aktuelle Simulation zeigt $18k/6Mo — aber basiert auf **Tageskerzen, perfekten Fills, keiner Slippage und 61 Trades**. Die Forschung zeigt: das reicht nicht. Hier ist was wir wirklich brauchen.

---

## 1. DATEN-LÜCKEN (Was fehlt)

### 1a. Intraday-Daten (1min/5min Bars) — KRITISCH

**Status:** FEHLT KOMPLETT. Gesamte Simulation auf Daily OHLC.

**Problem:** Jack postet um 10:34 "Valid 20 min". Die Tageskerze zeigt O=6.05, H=26.37, L=5.67. Aber:
- Kam das High um 10:50 (wir hätten es gefangen) oder um 15:30 (nach Expiry)?
- Kam erst das Low (SL getriggert) oder erst das High (Gewinn)?
- Wie lange blieb der Kurs am Peak (TSL-Window)?

**Ohne Intraday-Daten ist unsere gesamte Simulation Wunschdenken.**

**Lösung (priorisiert):**
| Quelle | Preis | Abdeckung | Empfehlung |
|---|---|---|---|
| **Polygon.io Starter** | $29/Mo | 1min, inkl. OTC+Delisted, 20+ Jahre | ⭐ Beste Option |
| **Alpaca** | Free | 1min, NASDAQ/NYSE, 5+ Jahre | Gut für Listed |
| **FirstRate Data** | ~$100-200 einmalig | 1min, 16k Ticker inkl. 7k Delisted | Survivorship-Bias-frei |
| IBKR reqHistoricalData | Free | 1min, nur ~6 Monate zurück | Zu kurz |
| Alpha Vantage | Free | 5min, 5 Calls/Min | Zu langsam |

**Empfehlung:** Polygon.io ($29/Mo) — deckt OTC und Delisted ab. Oder IBKR für die letzten 6 Monate als Startpunkt (kostenlos, aber begrenzt).

### 1b. Bid-Ask Spread Daten

**Status:** FEHLT. Simulation nimmt perfekte Fills an.

**Realität bei Penny Stocks:**
- $0.30 Stock mit Spread $0.02 = **6.7% Slippage roundtrip**
- $2.00 Stock mit Spread $0.05 = **2.5% roundtrip**
- $5.00 Stock mit Spread $0.03 = **0.6% roundtrip**

**Empirische Spread-Formel (aus Forschung):**
```
Spread% ≈ 2% × (Order_Quantity / Previous_Bar_Volume)
```
Plus Base-Spread basierend auf Preis:
- Sub-$1: 3-10% base spread
- $1-5: 1-3% base spread
- $5+: 0.3-1% base spread

### 1c. Trading Halt Daten

**Status:** FEHLT. 20/61 Trades hatten >50% Intraday-Move → wahrscheinlich Halts.

**LULD Halt-Trigger:**
- Stocks ≥$1: Halt bei **±30% in 5 Minuten**
- Stocks <$1: Halt bei **±50% in 5 Minuten**

**Resume-Gap Verteilung (aus Forschung):**
- 50% mild resume (±5%)
- 30% moderate gap (-20%)
- 20% catastrophic gap (-50%+)

**Quelle:** SEC MIDAS System (https://www.sec.gov/marketstructure/midas) — kostenlos aber mühsam zu parsen.

### 1d. Crowding/Follower-Effekt

**Status:** NICHT MODELLIERT.

**Forschung (ScienceDirect 2022, Journal of Finance 2025):**
- Followers erzielen im Schnitt **negative Returns** auf kopierte Signale
- Alpha Decay: erste Mover fangen den Großteil, Nachzügler finden keinen Edge
- Crowding = komprimierte Upside, Fat-Tail Downside
- Bei 500+ Followern auf dünnem Orderbuch: **+0.5-2% adverse Fill** über Jack's Preis

**Modell für Testcenter:**
```
Realistic_Entry = Jack_Entry × (1 + crowding_penalty)
crowding_penalty = 0.005 + 0.015 × (1 - min(daily_volume, 5M) / 5M)
```
→ Hochvolumig: +0.5%, Niedrigvolumig: +2%

---

## 2. SLIPPAGE-MODELL (Forschungsbasiert)

Die Forschung (IBKR Quant, Trade2Win, QuantConnect) empfiehlt:

| Szenario | Slippage | Quelle |
|---|---|---|
| Entry (Limit Order, liquid) | 0.5-1% | IBKR Quant |
| Entry (Limit Order, illiquid penny) | 1.5-2% | Trade2Win |
| Exit (TSL trigger, liquid) | 1-1.5% | QuantConnect |
| Exit (TSL trigger, illiquid penny) | 2.5-4% | Trade2Win |
| Exit (nach Halt resume) | 15-40% Gap-Down | SEC MIDAS |
| Crowding Penalty | 0.5-2% | ScienceDirect |

**Roundtrip-Slippage für Penny Stock:**
- Best Case (liquid, no halt): 2-3%
- Normal Case: 4-6%
- Worst Case (illiquid + halt): 20-50%

**→ Bei einem 3% TSL ist die Slippage GRÖSSER als der Trailing-Abstand!**
Das erklärt warum 3% TSL bei Penny Stocks zu eng ist. Die Forschung empfiehlt **8-15% für Day Trades, 15-25% für Swings** bei Micro-Caps.

---

## 3. STATISTISCHE ANALYSE

### Sample Size Problem

| Metrik | Unser Wert | Minimum laut Forschung |
|---|---|---|
| Trades | 61 | **200** (Bailey & López de Prado) |
| Zeitraum | 4 Monate (Okt-Jan) | 12+ Monate, multiple Regime |
| Parameter optimiert | 3 (TSL%, TP%, Max-Hold) | Max 1 pro 20 Trades |
| Marktregime abgedeckt | 1 (Bull/Momentum) | ≥3 (Bull, Bear, Choppy) |

**Mit 61 Trades und 3 Parametern können wir Skill NICHT von Glück unterscheiden.**

### Konfidenzintervalle

- **Aktuelle WR 45.6%**: 95% CI = [33.7%, 58.0%] — enthält 50%!
- **Optimierte WR 91.8%**: 95% CI = [82.2%, 96.4%]
- Für Signifikanz über 50% bei WR=60% braucht es **92 Trades**
- Für Signifikanz über 50% bei WR=55% braucht es **380 Trades**

### Bootstrap (10.000 Resamples)

Monatlicher Ertrag (optimiert, mit Slippage-Discounts):
- **5. Perzentil: $2.481/Mo**
- **Median: $2.986/Mo**
- **95. Perzentil: $3.566/Mo**
- P(Gesamtverlust): 0.0%

### Stress-Szenarien

| Szenario | Median/Monat | P(Verlust) |
|---|---|---|
| Baseline | $2.987 | 0% |
| -20% Win-Size | $2.386 | 0% |
| -30% Win-Rate | $2.008 | 0% |
| Beides (-30% WR, -20% Size) | $1.591 | 0% |
| **Worst Case** (-50% WR, -40% Size) | **$763** | **0%** |
| Nur kleine Trades (keine Monster) | $879 | 0% |

**→ Selbst im Worst Case bleibt das System profitabel** — aber die Marge wird dünn.

---

## 4. TESTCENTER ARCHITEKTUR

### Was es können muss:

```
┌──────────────────────────────────────────────┐
│                 DATA LAYER                    │
├──────────────────────────────────────────────┤
│ raw_messages.db          (Jack's Nachrichten)│
│ parsed_signals.db        (Parser-Output)     │
│ price_data_1min.db  ←NEW (Intraday Bars)     │
│ price_data_daily.db      (Tageskerzen)       │
│ halt_data.db         ←NEW (LULD Halts)       │
│ spread_model.json    ←NEW (Bid-Ask Modell)   │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│              SIMULATION ENGINE               │
├──────────────────────────────────────────────┤
│ 1. Signal empfangen (Timestamp + Preis)      │
│ 2. Fill-Simulation:                          │
│    - Crowding Penalty berechnen              │
│    - Spread/Slippage addieren                │
│    - Fill ja/nein (Preis vs. Intraday-Range) │
│ 3. Position-Management:                      │
│    - TSL Tick-by-Tick (1min Bars)            │
│    - Halt-Detection + Resume-Gap             │
│    - Partial Exits (Jack's Signale)          │
│ 4. Exit-Simulation:                          │
│    - TSL-Trigger + Exit-Slippage             │
│    - Max-Hold-Expiry                         │
│    - Jack-Exit-Signal                        │
│ 5. Fee-Berechnung (IBKR Tiered exakt)       │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│            PARAMETER SWEEP                   │
├──────────────────────────────────────────────┤
│ TSL_Day: [2, 3, 5, 8, 10, 15%]             │
│ TSL_Swing: [5, 8, 10, 15, 20, 25%]         │
│ TSL_Activation: [0.5, 1, 2, 3%]            │
│ TSL_Accel_Threshold: [5, 10, 15, 20%] ←NEW │
│ TSL_Accel_Factor: [2x, 3x, 4x]        ←NEW│
│ Breakeven_Lock: [10, 15, 20, 25%]     ←NEW │
│ TSL_Delayed_Start: [50, 75, 100, 150%] ←NEW│
│ TSL_Delayed_Pct: [10, 15, 20%]        ←NEW │
│ Monster_Score_Threshold: [2, 3, 4]     ←NEW │
│ Signal_Latency: [5, 15, 30, 60, 120s] ←NEW │
│ ATR_Pos_Size_N: [1.0, 1.5, 2.0, 2.5]  ←NEW│
│ Entry_Time_Filter: [PM/open30/all]     ←NEW │
│ Catalyst_Tier: [1, 2, 3]              ←NEW │
│ Regime_Filter: [SPY>20dMA, VIX<X]     ←NEW │
│ Hard_Stop_Max: [10, 15, 20%]          ←NEW │
│ Cool_Down_Min: [0, 30, 60, 120]       ←NEW │
│ Halt_Grace: [0, 60, 120, 300s]        ←NEW │
│ AH_Trading: [on, off]                 ←NEW │
│ Max_Hold_Day: [1, 2, 3, 5 Tage]            │
│ Max_Hold_Swing: [5, 10, 15, 20 Tage]       │
│ Entry_Slippage: [0.5, 1, 1.5, 2%]          │
│ Crowding: [0, 0.5, 1, 2%]                  │
│ Volume_Filter: [0, 500k, 1M, 2M]           │
│ Position_Size: [5, 10, 15, 20%]            │
│ → Sampling: 10.000-50.000 Random Combos    │
│ → Top 100 → Full Walk-Forward               │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│            VALIDATION                        │
├──────────────────────────────────────────────┤
│ 1. Walk-Forward:                             │
│    Train: Okt-Dez 2025                       │
│    Validate: Jan-Apr 2026                    │
│ 2. Monte Carlo (2000+ Runs)                  │
│ 3. Parameter Sensitivity (±2% jede Variable) │
│ 4. Stress Test (WR-30%, Size-20%)           │
│ 5. Sharpe > 2.0 erforderlich                │
└──────────────────────────────────────────────┘
```

### Priorisierte Schritte

| # | Schritt | Aufwand | Abhängigkeit | Impact |
|---|---|---|---|---|
| 1 | **Parser Review fertig** (ab ID 3937) | 2-3 Sessions | — | Mehr Trades für Validation |
| 2 | **Intraday-Daten beschaffen** (Polygon oder IBKR) | 1 Session | — | Fundament für alles |
| 3 | **Slippage-Modell bauen** | 1 Session | #2 | Realistische Fills |
| 4 | **1min-TSL-Simulation** | 2 Sessions | #2, #3 | Echte TSL-Ergebnisse |
| 5 | **Parameter-Sweep** | 1 Session (automatisiert) | #4 | Optimale Werte |
| 6 | **Walk-Forward Validation** | 1 Session | #1, #5 | Overfitting-Check |
| 7 | **Halt-Modell** | 1 Session | #2 | Risiko-Realismus |
| 8 | **Crowding-Modell** | 1 Session | #2 | Entry-Realismus |

---

## 5. WAS SOFORT GEÄNDERT WERDEN KANN (ohne Testcenter)

Diese Änderungen sind **unabhängig von Parametern robust**:

1. **TP-Cap entfernen** — In JEDEM Szenario besser. Kein einziger TP2-Trade wäre mit TSL schlechter gewesen.
2. **TSL nach Trade-Typ** — 3% Day, 8% Swing. Evidenz aus OMER, LAES, ELBM eindeutig.
3. **Swing-Trades optional machen** — Config-Toggle. Für den Anfang nur Day Trades.
4. **Exakte Fee-Berechnung** — einfach zu implementieren, macht Simulation ehrlicher.

---

## 6. ADAPTIVE STRATEGIE-WAHL (Monster-Score)

**Kern-Idee:** Nicht eine fixe Strategie für alle Trades, sondern vor jedem Trade die Vortags-Indikatoren berechnen und automatisch die passende Exit-Strategie wählen.

### Monster-Score (0-5 Punkte, berechnet vor Entry)

| Kriterium | Bedingung | Quelle |
|---|---|---|
| RSI(14) daily | > 70 | Tageskerze Vortag |
| ATR(5)/Close | > 30% | Tageskerzen letzte 5 Tage |
| Volume | > 10× 20-Tage-Avg | Tageskerze Vortag |
| Range Expansion | 2+ Tage steigende Daily Range | Tageskerzen |
| Jack-Keywords | "low float", "bull flag", "halted up" | Signal-Text |

### Strategie pro Score-Band

| Score | Kategorie | Exit-Strategie | Entry |
|---|---|---|---|
| 0-1 | Normal | TSL 3% act@10% | Jack's Limit Order |
| 2-3 | Hot | TSL 5% act@20% + Partial 50% bei +30% | Limit mit +0.5% Offset |
| 4-5 | Monster | Strategie D (BE@+20%, TSL 15%@+100%) | **Sofortkauf** |

### Evidenz (aus Ticker-Review mit 1min-Daten)

**CETX 08.12.2025** — Score 5/5 (RSI=82, ATR/Close=98%, Vol=32×, Range↑, "super low float")
- Jack: $0 (kein Fill, beide Limits zu tief)
- TSL 3% act@10%: +$1.031 (+51.7%) — nur erste Welle
- **Strategie D: +$2.003 (+100.4%)** — beide Wellen mitgenommen
- RSI-basierter Exit: +$1.344 (+67.4%) — zu früh raus
- ATR-basierter TSL: +$689 (+34.5%) — zu eng

**Erkenntnis:** RSI/ATR/Vol als Exit-Tool bringt bei Monstern nichts (Moves zu schnell, Indikatoren hinken nach). Aber als Entry-Filter sind sie extrem wertvoll.

### Im Testcenter zu validieren
- Score-Gewichte: sind alle Kriterien gleich wichtig oder gewichtet?
- Schwellenwerte: ist >70 RSI richtig oder >60 oder >80?
- Strategie-Mapping: stimmen die Bänder oder braucht es feinere Abstufung?
- **Über ALLE Ticker validieren — nicht auf CETX optimieren!**

---

## 7. FEHLENDE PARAMETER (identifiziert 2026-04-13)

Aus Online-Research (QuantConnect, QuantifiedStrategies, LuxAlgo, Bookmap) und eigener CETX-Analyse:

### Im Parameter Sweep ergänzen

| Parameter | Range | Warum fehlt es |
|---|---|---|
| **Signal_Latency_Sec** | 5 / 15 / 30 / 60 / 120 | Copy-Trading verliert Alpha pro Sekunde. Slippage-Modell hat keine Zeitdimension — Kurs bewegt sich WÄHREND wir die Order platzieren |
| **ATR_Position_Sizing** | risk$ / (N × ATR), N=1.0-2.5 | Fix 20% ignoriert Volatilität. TSL 3% bei 15%-ATR Stock = sofortiger Trigger. Dollar-Risk pro Trade normalisieren |
| **Entry_Time_Filter** | PM-only / 09:30-10:15 / 09:30-11:00 / all-day / no-last-30min | 24% der Tageshochs in ersten 30min RTH. Spätere Entries haben schlechtere Fill-Rate |
| **Catalyst_Tier** | news=1 / earnings=2 / no-catalyst=3 | Catalyst-driven Momentum ist der Edge bei Penny Stocks. "No catalyst" Trades separat messen |
| **Regime_Filter** | SPY > 20d MA / VIX < X | Penny Momentum stirbt in Risk-Off/Choppy. Macro-Gate reduziert Drawdown massiv |
| **Hard_Stop_Max_Loss** | 10 / 15 / 20% vom Entry | GAP-PROTECTION: unabhängig vom TSL, absolute Verlustgrenze pro Trade. Wenn Halt + Gap-Down |
| **Cool_Down_Minutes** | 0 / 30 / 60 / 120 nach Loss auf selben Ticker | Zweiter Trade nach Stop-Out auf demselben Ticker = kompoundierende Verluste |

### Aktualisierte Gesamtzahl Parameter: ~30

**Achtung:** 30 Parameter × multiple Werte = Milliarden Combos. Random Sampling (10k-50k) + Top 100 Walk-Forward bleibt der Ansatz. Alternativ: Bayesian Optimization statt Grid/Random.

---

## 8. OFFENE FORSCHUNGSFRAGEN

1. **ATR-basierter TSL vs. fixer Prozent-TSL** — Die Forschung empfiehlt 2-3× ATR(14) statt fixem %. Braucht Intraday-Daten zum Berechnen.
2. **Optimale Reaktionszeit auf Jack's Signal** — Wie viel Alpha verlieren wir pro Minute Verzögerung? Braucht Intraday-Daten. → Jetzt als `Signal_Latency_Sec` im Sweep.
3. **Wochentag-/Uhrzeiteffekte** — Sind PM-Trades besser als RTH? Montags vs. Freitags? → Jetzt als `Entry_Time_Filter` im Sweep.
4. **Kanal-Unterschied** — Premium vs. Biotech: anderer Edge?
5. **Survivorship Bias** — Unsere Price-Daten enthalten nur existierende Ticker. Delisted/bankrotte Penny Stocks fehlen → überschätzt Returns.
6. **Bayesian vs. Random Sampling** — Bei 30 Parametern ist Bayesian Optimization (Optuna/SMAC) effizienter als Random. Evaluieren.
