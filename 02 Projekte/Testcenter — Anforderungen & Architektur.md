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
| **Order_Price_Offset_Pct** | 0 / +0.5 / +1 / +2 / +3 / +5% über Jacks Limit | Jack's Preis oft nicht mehr erreicht (RADX #3: Order 5.30, RTH-Low 5.60 → nie gefüllt). Offset nach oben = mehr Fills, aber schlechterer Entry |

### Aktualisierte Gesamtzahl Parameter: ~30

**Achtung:** 30 Parameter × multiple Werte = Milliarden Combos. Random Sampling (10k-50k) + Top 100 Walk-Forward bleibt der Ansatz. Alternativ: Bayesian Optimization statt Grid/Random.

---

## 7c. SIMULATION: Swing-Entries bedingt ausschließen

Aus LAES-Review msg 5409 (2026-04-14).

**Hypothese:** Swings sind strukturell ungünstig für den Bot:
- Besetzen einen der 5 Slots tagelang/wochenlang
- TSL 3% zu eng (Penny-Range bei Multi-Day-Holds)
- Jack's Edge ist Domain-Expertise die der Bot nicht hat
- Konkret: LAES 2026-03-16 Entry 3.30 → 2026-04-10 bei 2.10 = **-36% nach einem Monat**

**Varianten im Sweep:**
| Variante | Filter |
|---|---|
| A | Alle Swings traden (Baseline) |
| B | Keine Swings traden |
| C | Swings nur wenn Ticker-Cluster = C1 Stable (aus Klassifikator) |
| D | Swings nur bei Bankroll-Auslastung < 50% (Slot-Budget) |
| E | Swings nur mit Catalyst (Earnings/FDA) |
| F | Swings nur bei SPY > 20d MA (Regime-Filter) |

**Messung:** PnL / Sharpe / Max-DD / Win-Rate / Slot-Utilization-Effizienz (PnL pro Slot-Stunde)

**Entscheidungskriterium:** Wenn Variante X den Bot bei gleichem Risiko über mehrere Zeiträume besser macht → als Config-Flag `SWING_FILTER_MODE` einbauen.

---

## 7d. SIMULATION: Order-Price-Offset (Fill-Rate optimieren)

Aus RADX-Review msg 4145 (2026-04-14).

**Problem:** Jack sagt "order at 5.30" — RTH-Low des Tages war 5.60. Bot-Limit-Order @ 5.30 wurde nie gefüllt. Ähnlich oft bei anderen Signalen. Parser klassifiziert korrekt als `entry`, aber ohne Offset-Logik baut der Bot in vielen Fällen **keine Position auf** trotz "ausgeführtem Signal".

**Hypothese:** Jack's Preis ist eher ein Wunsch-Level als ein Marktpreis. Wenn wir **X% über** Jacks Limit ordern, erwischen wir mehr Trades — zum Preis von schlechterem Entry.

**Varianten im Sweep (Order_Price_Offset_Pct):**
| Variante | Limit-Preis | Effekt |
|---|---|---|
| A | Jacks Preis exakt (Baseline) | Niedrige Fill-Rate, beste Entry-Preise |
| B | Jacks Preis + 0.5% | Mehr Fills, minimal schlechterer Entry |
| C | Jacks Preis + 1% | Moderater Trade-off |
| D | Jacks Preis + 2% | Aggressiver |
| E | Jacks Preis + 3% | Sehr aggressiv |
| F | Jacks Preis + 5% | Market-Order-ähnlich |
| G | Market-Order bei Signal (IOC) | Maximal-Aggressiv, keine Limit-Kontrolle |
| H | Staggered: 50% bei Jack-Preis, 50% bei +1% | Hybrid |

**Messung:**
- Fill-Rate (% der Signale die eine Position auslösen)
- Avg Entry-Slippage vs. Jacks Preis (Basispunkte)
- PnL pro erfolgreichem Trade
- Gesamt-PnL (Fill-Rate × Durchschnitts-PnL)
- Win-Rate vs. Variante A

**Warum das wichtig ist:**
- 282 Entry-Signale mit konkretem Preis im Korpus
- Bei vielen dieser Signale haben wir aktuell vermutlich **keinen Fill** → zählt in der Simulation fälschlich als "ausgeführter Trade mit PnL=0"
- Mit Polygon-Intraday-Daten (1-min OHLC) können wir **pro Signal prüfen:** "Bei Offset X% wäre die Order gefüllt worden, bei Offset Y% nicht"
- Finden welcher Offset die beste Risiko-adjustierte Rendite bringt

**Entscheidung:** Offset-Range im Sweep ergänzen, Gewinner als `ORDER_OFFSET_PCT` in der Live-Config verankern.

**Verbunden mit:**
- [[02 Projekte/Signal Bot|Signal Bot]] — staggered_entry Memo (Bot soll mehrere Orders leicht über Jack-Preis platzieren)
- Slippage-Modell (Section 2) — Offset + Spread zusammen modellieren

---

## 7e. SAFETY-GATES für Conditional-Setup-Executor (NCPL #7 → Projekt)

Aus NCPL-Review 2026-04-14 (msg 4008) abgeleitet. User-Direktive: *"muss für zukünftige Trades passend und möglichst sicher sein"*. Quell-Memo: `project_conditional_setup_executor.md`.

**Kontext:** Jack postet "If X failed to break Y ... drop to Z1-Z2 ... enter for quick day trade in T minutes"-Setups. Bot soll das automatisch triggern — aber nur mit belastbaren Safety-Gates, damit die Regel auch auf unbekannten zukünftigen Signalen sicher bleibt.

**Edge (bewiesen NCPL):** Entry-Range +2% Offset füllt wo Jack knapp verfehlt → +53% auf NCPL-Peak verfügbar. Aber ein einziger Fall = noch kein Beweis für Robustheit.

### 8 Hard Safety-Gates (als Testcenter-Sweep-Variablen)

| # | Gate | Default | Sweep-Range | Zweck |
|---|---|---|---|---|
| 1 | `Cond_Max_Position_Size` | 10% Bankroll | {5%, 10%, 15%, 20%} | Conditional ist spekulativer als Hard-Order → halbierte Size |
| 2 | `Cond_Max_DD_Cap` | -10% | {-8%, -10%, -12%, -15%} | Enger Stop bei Hedge-Sprache |
| 3 | `Cond_SoftScore_Veto` | ≥ 5 | {3, 5, 7, off} | Falling-Knife blockieren |
| 4 | `Cond_Resistance_Reject_Required` | true | {true, false} | Phantom-Trigger vermeiden |
| 5 | `Cond_Offset_Cap` | +3% max | {1%, 2%, 3%, 5%} | Risk-Reward bewahren |
| 6 | `Cond_TTL_Buffer` | +1 min | {0, 1, 2, 3 min} | Stale Setups killen |
| 7 | `Cond_Market_Regime_Gate` | VIX>25 OR SPY<-1% → halbieren | {on, off, halbieren, skippen} | Risk-Off-Filter |
| 8 | `Cond_Time_of_Day` | 09:30-15:30 ET | {RTH, RTH+PM, nur 09:30-14:00, ...} | Liquidität + Spread |

### Re-Validierungs-Regel (Drift-Schutz)
- Alle **50 getriggerte Setups** → Hit-Rate automatisch neu berechnen
- Wenn Hit-Rate < 50% → Regel **pausieren**, Re-Analyse
- Wenn Hit-Rate > 65% über 3 Quartale → Offset-Kalibrierung

### Deployment-Gates (Pflicht vor Live)
1. ≥ 5 Template-Matches im Review-Korpus (Stand 2026-04-14: 1 — NCPL #7)
2. Walk-Forward-Test: Train Q3/Q4 2025, Test Q1 2026 → Hit-Rate-Degradation ≤ 5pp
3. Offset-Variante ≥ 10% PnL-Delta über Jack-Baseline (Fill-Rate × Win-Rate × Avg-PnL)
4. **Dry-Run 30 Paper-Trades** in Live-Market-Daten: Hit-Rate paper ≈ Hit-Rate backtest
5. Initial Live-Size = 5% (statt default 10%), Ramp-up auf 10% erst nach 50 realen Trades

### Wachstumspfad für die Regel
Die Regel soll mit jedem neuen Template-Match nach-kalibriert werden:
- **Jede neue Session** → weitere Fälle in `Conditional Setup Fallsammlung.md` einfügen
- **Phrasen-Matrix** erweitert sich organisch
- **Ab 5 Fälle** → erste statistische Validierung (Binomial-CI)
- **Ab 10 Fälle** → Safety-Gate-Defaults empirisch neu setzen
- **Ab 20 Fälle** → Live-Deploy-Gate 3 erreicht, Offset final kalibriert
- **Laufend:** Drift-Check nach je 50 Live-Trigger (Re-Validierungs-Regel oben)

**Verbunden mit:**
- `project_conditional_setup_executor.md` — Detail-Memo, Template, Safety-Gates
- `[[Conditional Setup Fallsammlung]]` — laufende Case-Sammlung
- Section 7d oben (Order-Price-Offset) — selbe Offset-Mechanik, andere Auslöser

---

## 7b. SIMULATION: Conditional Watchlist Auto-Entry

Aus LAES-Review 2026-04-14 identifiziert — siehe [[Conditional Watchlist Auto-Entry]].

**Hypothese:** Jack kündigt Setups mit Preis-Levels vorab an (z.B. "if gets below 3.58 and stays above 3.36 → double bottom, 8-12% move"). Ein Bot der diese Bedingungen überwacht und bei Erfüllung autonom einsteigt würde zusätzliche Trades fangen.

**Testcenter muss simulieren können:**
- Extraktion aller historischen Conditional-Setups aus geparstem Signal-Korpus
- Für jedes Setup: wurde Bedingung innerhalb Expiry erfüllt (Intraday-Check)?
- Hit-Rate: % der Setups die triggern
- Jack-Miss-Rate: % der triggered Setups wo Jack selbst NICHT einsteigt (False-Positive-Marker)
- Simulierter PnL mit eigener SL/TP-Regel (z.B. SL 3% unter Support-Zone, TP bei Target-Range-Mitte)
- Vergleich: Baseline (nur explizite Entries) vs. Baseline + Conditional Watchlist

**Entscheidung:** Nur implementieren wenn positiver EV nach Gebühren + Slippage.

---

## 8. OFFENE FORSCHUNGSFRAGEN

1. **ATR-basierter TSL vs. fixer Prozent-TSL** — Die Forschung empfiehlt 2-3× ATR(14) statt fixem %. Braucht Intraday-Daten zum Berechnen.
2. **Optimale Reaktionszeit auf Jack's Signal** — Wie viel Alpha verlieren wir pro Minute Verzögerung? Braucht Intraday-Daten. → Jetzt als `Signal_Latency_Sec` im Sweep.
3. **Wochentag-/Uhrzeiteffekte** — Sind PM-Trades besser als RTH? Montags vs. Freitags? → Jetzt als `Entry_Time_Filter` im Sweep.
4. **Kanal-Unterschied** — Premium vs. Biotech: anderer Edge?
5. **Survivorship Bias** — Unsere Price-Daten enthalten nur existierende Ticker. Delisted/bankrotte Penny Stocks fehlen → überschätzt Returns.
6. **Bayesian vs. Random Sampling** — Bei 30 Parametern ist Bayesian Optimization (Optuna/SMAC) effizienter als Random. Evaluieren.
