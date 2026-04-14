---
tags: [signal-bot, klassifikator, phase-2, vix, spy, market-regime]
date: 2026-04-14
status: fertig
parent: "[[Ticker-Klassifikator]]"
---

# Phase 2f — VIX/SPY × Win-Rate (Market-Regime-Korrelation)

**Frage:** Korreliert das Markt-Umfeld (SPY-Return, VIX-Level) mit Jack-Signal-Performance?

**Kurze Antwort:** **Ja, teilweise stark.** Neue harte Regel-Kandidaten identifiziert.

## Datenbasis

- 296 Signale × 10%/15% SL/TP Szenario (aus `signals_simulated.csv`)
- Alle 296 mit kompletten VIX/SPY-Daten gematcht
- SPY/VIX via yfinance (Phase 2 Enrichment)

## Key Findings

### 1. SPY rote Tage = C1 profitiert massiv

| SPY 1d Return | N | Win-Rate | Avg PnL |
|---|---|---|---|
| rot (<−1%) | 13 | **54%** | −0.01% |
| slightly rot | 58 | 33% | −2.09% |
| flat | 92 | 27% | −2.56% |
| slightly green | 124 | 38% | −0.14% |
| green (>+1%) | 9 | 11% | **−4.33%** |

**C1 isoliert:** SPY rot (<−1%) → 58% Win (N=12). SPY green (>+1%) → 0% Win (N=2).

**Intuition:** Panik-Selling im Index → SPY-Futures-Reversals → Small-Caps ziehen mit. Jacks Setups feiern Reversals, nicht Trends.

**Caveat:** Green-Extrem hat nur N=2 Samples. Rot-Extrem N=13 ist stabil.

### 2. VIX-Level: Mittlere Bereiche bevorzugt

| VIX | N | Win-Rate | Avg PnL |
|---|---|---|---|
| low (<14) | 12 | 17% | −3.36% |
| normal (14-18) | 224 | 34% | −1.32% |
| elevated (18-22) | 54 | 35% | −1.03% |
| high (>22) | 6 | 33% | −3.42% |

**C0 krasst:** In VIX low (<14) und high (>22) **0% Win** (N=10 kombiniert). → Schlechte Volatilitäts-Extreme für PM-Penny.

**C1 unabhängig:** 40-67% Win in allen VIX-Buckets → C1 ist regime-robust.

**C2 nur im normalen VIX-Fenster:** N=31, 19% Win, −5.2% avg. Bei VIX elevated N=2 (50% Win, aber zu klein).

### 3. VIX Änderung (Volatility-of-Volatility)

| VIX 1d Δ | N | Win-Rate | Avg PnL |
|---|---|---|---|
| falling (>−3%) | 110 | 32% | −1.47% |
| slight down | 69 | 30% | −1.99% |
| **slight up (0-3%)** | **27** | **41%** | **+2.17%** |
| spiking (>+3%) | 90 | 36% | −1.92% |

**Beste Markt-Bedingung:** VIX steigt moderat (0-3%). Nur **diese Kategorie hat positives Avg-PnL**. Klassischer "Angst im Aufbau, aber kein Panik" — Setups greifen am effektivsten.

### 4. Market-Regime (Phase 2-Definition)

| Regime | N | Win-Rate | Avg PnL |
|---|---|---|---|
| bull_quiet (SPY positiv, VIX <14) | 29 | 28% | −3.42% |
| chop (Rest) | 261 | 34% | −1.12% |
| high_vol (VIX >20) | 6 | 33% | −3.42% |

**Erwartung war "bull_quiet = good", Realität ist "chop = best".** Jack's Strategy funktioniert in volatilen, unsteten Märkten — nicht in ruhigen Trend-Phasen.

⚠️ Nur 6 `high_vol`-Samples — Aussage nicht robust.

## Neue Regel-Kandidaten

### P1.4 — SPY-Extreme-Filter für C1 (NEU)

```python
# C1 ist stabil außer bei extremem SPY green
if label == 'C1' and spy_return_1d > 1.0:
    position_size *= 0.5  # halbe Position (N=2 Sample small)
    rules_fired.append('P1.4_c1_spy_green_weak')
```

**Evidenz:** 2/9 SPY>1% Win-Rate (11%), aber Sample klein. Als Warnung, nicht Skip.

### P1.5 — VIX-Extreme-Skip für C0 (NEU)

```python
# C0 ist in VIX-Extremen 0% Win
if label == 'C0' and (vix_close < 14 or vix_close > 22):
    reject(reason='C0 + VIX-Extrem 0% Win-Rate')
```

**Evidenz:** 10 Trades bei VIX<14 oder >22, alle Loss.

**Aber:** C0 ist schon default-reject in P0.1 — diese Regel wäre redundant für Live. Wichtig als Info-Layer für "falls wir C0 mal freischalten".

### P2.3 — VIX rising als positive Bias (NEU)

```python
# VIX steigt moderat (0-3%) = beste Performance
if 0 < vix_return_1d < 3.0:
    position_size *= 1.2  # nur wenn auch kein reject
    rules_fired.append('P2.3_vix_rising_bias')
```

**Evidenz:** 27 Trades, 41% Win-Rate, +2.17% avg. Einzige positive Kategorie im Gesamtschnitt.

**Caveat:** N=27 ist borderline. Will man 1.2× Bias-Modifier auf diesem Sample riskieren? Erst nach Sample-Vergrößerung (nach Polygon).

## Was zu klein für Regel ist

- SPY green>+1%: N=9 → zu klein
- VIX high>22: N=6 → zu klein  
- C2 in VIX elevated: N=2 → zu klein

Merken für Re-Run nach Polygon + 6 Monate mehr Historie.

## Updates für rules.py (vorgeschlagen, nicht gemacht)

```python
# Zusätzlicher Parameter: market_flags
def apply_rules(..., market_flags: dict = None):
    market_flags = market_flags or {}
    vix = market_flags.get('vix_close')
    spy_1d = market_flags.get('spy_return_1d')
    vix_1d = market_flags.get('vix_return_1d')
    
    # P1.4 SPY extreme
    if label == 'C1' and spy_1d is not None and spy_1d > 1.0:
        d.position_size_mult *= 0.5
        d.rules_fired.append('P1.4_c1_spy_green_weak')
    
    # P1.5 VIX extreme (informational, C0 redundant)
    if label == 'C0' and vix is not None and (vix < 14 or vix > 22):
        # nur loggen, weil P0.1 schon rejected
        d.rules_fired.append('P1.5_c0_vix_extreme_info')
    
    # P2.3 VIX rising bias (experimental, nicht aktivieren bis N>50)
    # if vix_1d is not None and 0 < vix_1d < 3.0 and not d.reject:
    #     d.position_size_mult *= 1.2
    #     d.rules_fired.append('P2.3_vix_rising_bias')
```

**Empfehlung:** P1.5 nur als Info-Rule einbauen (C0 ist schon reject). P1.4 + P2.3 erst nach Polygon-Datenerweiterung live testen.

## Nächste Schritte

- [ ] Nach Polygon + Ticker-Gap-Schließung: Re-Run mit N~600 Signalen, Regel-Schwellen validieren
- [ ] `signal_enriched.csv` in live-Bot einbinden: täglich SPY/VIX holen und als Feature an Classifier geben
- [ ] Optional: Correlate win-rate nicht nur pro Cluster sondern pro (cluster × weekday × vix_bucket)

## Output-Files

- `/root/signal_bot/reports/ticker_classifier/vix_spy_correlation.txt`
