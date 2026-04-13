---
tags: [signal-bot, analyse, testcenter, tsl, halt-trading]
date: 2026-04-13
---

# TGL Deep Dive — Warum der Bot Monster-Trades verpasst & Lösungen

## Der Fall TGL (2025-12-05)

**Timeline:**
- Jack postet Entry-Hinweis bei ~17.25 (vor ID 3937)
- TGL haltet sofort nach oben, öffnet bei 20+
- Jack: Entry 18.88 → Exit ~22, dann Entry 17.25 → halted up → Sold 26.60
- AH geht TGL auf **40** (+132% ab 17.25)

**Was der Bot gemacht hätte:**
| Szenario | Entry | Exit | Profit | vs. Potenzial |
|---|---|---|---|---|
| TP-Cap 4.5% | 17.25 | 18.03 | +$45 | 2% vom Potenzial |
| TSL 3% flat | 17.25 | ~17.70 | +$26 | 1% vom Potenzial |
| TSL 8% | 17.25 | irgendwo 22-30 | +$300-750 | 15-35% |
| TSL dynamisch (10-15%) | 17.25 | irgendwo 25-35 | +$500-1000 | 25-50% |
| Nicht gefüllt (Halt) | — | — | $0 | 0% |

## Drei fundamentale Probleme

### 1. Jack postet Recaps, keine Pre-Alerts (bei Monster-Trades)
Bot-Pipeline ist ~15 Sekunden (Listener <1s → Haiku 2s → Sonnet 3s → Opus 5s → IBKR 2s). Das ist schnell genug.
**Das Problem ist nicht Bot-Latenz, sondern Jack's Posting-Verhalten:** Bei Monster-Trades postet er oft NACH dem Fill als Recap ("did a small trade from 18.88 to 22"). Bei normalen Trades postet er Pre-Alerts ("placed an order at X, valid for 15 minutes") — dort ist der Bot konkurrenzfähig.

### 2. TSL 3% ist zu eng für Momentum-Trades
- Bei Halt-Stocks mit 5-10% Swings zwischen Halts ist 3% Rauschen
- Bot wird bei jedem Pullback rausgeschüttelt
- Stock hat noch 100%+ vor sich

### 3. Halts machen TSL blind
- Während Trading-Halt kann TSL nicht triggern
- Stock haltet bei 20, TSL steht bei 19.40
- Halt löst sich auf, Stock öffnet bei 15 → TSL triggert bei 15, nicht 19.40
- Gap-Risiko ist real und unberechenbar

## Lösungsansätze

### A. Akzeptieren was wir nicht können
Bot wird NIEMALS Jack's Halt-Trades in Echtzeit replizieren. Jack ist schneller als sein eigener Kanal. **Aber:** wir müssen die Trades die wir fangen MAXIMAL ausreiten.

### B. Acceleration-basierter TSL (GRÖSSTER HEBEL — Testcenter-Variable)

| Situation | TSL | Begründung |
|---|---|---|
| Normal Day-Trade | 3% | Standard, bewährt |
| Stock >10% in <30min | 8-10% | Momentum nicht abwürgen |
| Stock haltet nach oben | 12-15% oder zeitbasiert | Gap-Schutz |
| Swing-Trade | 8% | Bereits identifiziert (OMER/LAES Evidenz) |

**Implementierung:** Volatilität der letzten 30min messen (z.B. ATR auf 1min-Bars), TSL dynamisch skalieren.

### C. Halt-Awareness im Position Monitor
- IBKR meldet Halts über Market Data Events
- Wenn Halt erkannt: TSL-Evaluation pausieren
- Nach Halt-Resume: 2-Minuten Grace Period bevor TSL wieder aktiv wird
- Verhindert Gap-Through-Exits
- **Kein Testcenter nötig — reiner Code-Change**

### D. Post-Halt Re-Entry
Wenn Bot initialen Halt-Trade verpasst, aber Jack danach nochmal ein Level postet → Bot steigt nach Halt auf höherem Level ein. Riskanter (Entry bei 20+ statt 17.25), aber profitabel wenn Stock auf 40 geht.

### E. AH-Extension
TGL ging von 26.60 (Jack's Exit) auf 40 AH. Position nicht bei Market Close schließen — TSL auch in Extended Hours aktiv lassen.
**Kein Testcenter nötig — Config-Change in position_monitor.py**

## Testcenter-Variablen (aus dieser Analyse)

Neue Parameter für den Sweep:
```
TSL_Acceleration_Threshold: [5, 10, 15, 20%]  # Ab welchem Move in 30min
TSL_Acceleration_Factor: [2x, 3x, 4x]         # Um wie viel TSL weiten
Halt_Grace_Period: [0, 60, 120, 300s]          # Sekunden nach Halt-Resume
AH_Trading: [on, off]                          # Extended Hours TSL
```

## Evidenz aus Simulation

Von 61 Trades hatten **20 Trades >50% Intraday-Move** — fast alle mit Halts. Diese 20 Trades machen **~90% des Gesamtprofits**. Der Bot verpasst sie systematisch wegen:
- TP-Cap (schneidet bei +4.5% ab)
- TSL 3% (rausgeschüttelt)
- Halt-Blindheit (Gap-Through)
- Latenz (Recap statt Pre-Alert)
