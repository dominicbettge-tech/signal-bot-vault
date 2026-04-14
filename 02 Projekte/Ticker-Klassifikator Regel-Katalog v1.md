---
tags: [signal-bot, klassifikator, regeln, phase-3-draft]
date: 2026-04-14
status: entwurf
parent: "[[Ticker-Klassifikator]]"
---

# Regel-Katalog v1 — Draft für Live-Classifier

**Entstanden nachts am 2026-04-14 aus Phase 2 Analyse.** Sortiert nach Evidenz-Stärke. Alle Regeln sind gegen Simulation von 1.480 Trades (296 Signale × 5 Szenarien) getestet, NICHT gegen echte Trades (die liegen alle nach dem Signal-Window).

## Priorisierung (vor Morgen-Gespräch)

| Prio | Regel | Evidenz | Effekt |
|---|---|---|---|
| **P0** | SL/TP pro Cluster | Simulation | C1 +1%/Trade vs −3% default |
| **P0** | Dilution-Filter (S-1/S-3 in 7d) | SEC-Filings + Simulation | C1 Win 42→23% wenn nicht gefiltert |
| **P0** | `kw_careful` = Skip | Simulation | 0% Win in C0/C2 |
| **P1** | C2-Freitags-Skip | Simulation | 8% Win −7% PnL |
| **P1** | C0-Swing = Skip | Simulation | 0% Win (N=7) |
| **P1** | C2 nur in PM-Bucket | Simulation | Midday: 11% Win −7%, PM: 36% Win +2.7% |
| **P2** | Earnings am Tag/Vortag = Skip | SEC-Filings | C1 Win 57% → 17% |
| **P2** | `low_float` + `bull_flag` = wahrscheinlich C2 | Keyword-Lift | 4-4.5× häufiger in C2 |
| **P3** | 8-K in 7d → TSL statt fixer SL | Range-Amp + Win-Rate-Drop | sinnvoll aber nicht simuliert |
| **P3** | Market-Regime | zu wenig Samples | N<30 bull_quiet, 0 bear |

## P0 — Must-Have (hohe Evidenz, einfache Implementierung)

### P0.1 — Cluster-spezifische SL/TP

```
if cluster == C0:
    # PM-Penny — strukturell nicht profitabel mit fixen Regeln
    REJECT_DEFAULT = True  # Skip wenn kein explizites Override
    # Falls trotzdem handeln:
    SL = 10%, TP = 25%  # bestes Szenario, aber avg PnL −2.4%
elif cluster == C1:
    # Solid Mid-Cap Day Trade — profitable Basis-Regel
    SL = 10%
    TP = 15%
    POSITION_SIZE = full  # 20% bankroll normal
elif cluster == C2:
    # Monster — breit oder nicht
    SL = 20%
    TP = 40%
    POSITION_SIZE = half  # halbe Position wegen Vol
```

**Quelle:** `simulation_report.txt` Section A+H.

### P0.2 — Dilution-Filter

```python
def has_recent_dilution(ticker: str, date: datetime) -> bool:
    """Check SEC EDGAR for S-1/S-3/424B5 in last 7 days."""
    filings = fetch_edgar(ticker, forms=['S-1', 'S-3', '424B5'],
                          start=date - timedelta(days=7), end=date)
    return len(filings) > 0

# In signal handler:
if has_recent_dilution(ticker, now):
    reject_signal("Dilution filing within 7 days")
```

**Latency:** EDGAR ~300ms pro Ticker. Cache all-filings täglich, nur inkrementell ab dann.

**Quelle:** `news_correlation_report.txt` Section E; `simulation_report.txt` Section C.

### P0.3 — `kw_careful` Skip

```python
CAREFUL_PATTERNS = ['careful', 'caution', 'watch out', 'risky', 'risk']

if any(p in signal_text.lower() for p in CAREFUL_PATTERNS):
    if cluster in ('C0', 'C2'):
        reject_signal("Careful keyword in C0/C2 context")
    elif cluster == 'C1':
        # Halbe Position + engerer SL
        POSITION_SIZE *= 0.5
        SL *= 0.7
```

**Quelle:** `simulation_report.txt` Section G.

## P1 — High Priority

### P1.1 — C2-Freitags-Skip

```python
if cluster == 'C2' and signal_date.weekday() == 4:  # Friday
    reject_signal("C2 Friday signals lose 8% win rate avg -7%")
```

**Quelle:** `simulation_report.txt` Section E.

### P1.2 — C0-Swing = Skip

```python
if cluster == 'C0' and trade_type == 'swing':
    reject_signal("C0 swing trades 0% win rate (N=7)")
```

Kleines Sample, aber 0/7 ist eindeutig negativ — no evidence of any C0 swing working.

**Quelle:** `simulation_report.txt` Section I.

### P1.3 — C2 nur PM-Entry

```python
if cluster == 'C2':
    et_hour = now_et.hour
    et_minute = now_et.minute
    is_pm = (4*60 <= et_hour*60 + et_minute < 9*60 + 30)  # PM session
    if not is_pm:
        reject_signal("C2 only in PM bucket (midday 11% win, PM 36% win)")
```

**Quelle:** `simulation_report.txt` Section F.

## P2 — Nice-to-Have

### P2.1 — Earnings-Nähe = Skip/Halb

```python
def is_earnings_near(ticker: str, date: datetime) -> bool:
    filings_8k = fetch_edgar(ticker, forms=['8-K'],
                             start=date - timedelta(days=1), end=date)
    return any(parse_items(f['items']).contains('2.02') for f in filings_8k)

if is_earnings_near(ticker, now):
    if cluster == 'C1':
        POSITION_SIZE *= 0.5  # halbe Position
    else:
        reject_signal("Earnings filing yesterday/today, too volatile")
```

**Effekt:** C1 Win-Rate fällt 57% → 17% bei Earnings-Nähe.

### P2.2 — Keyword-basierte Cluster-Boost

```python
# Wenn Cluster-Zuordnung unsicher (neuer Ticker), text-based Heuristik:
text_low = signal_text.lower()
if ('low float' in text_low or 'bull flag' in text_low):
    likely_cluster = 'C2'  # 4-4.5× Keyword-Rate in C2
elif 'halted' in text_low:
    likely_cluster = 'C2'  # 2× Lift
elif 'loading' in text_low or 'big size' in text_low:
    likely_cluster = 'C1'  # conviction_high nur in C1
```

Nur nutzen wenn Cluster nicht bekannt. Cluster-Features > Keywords.

**Quelle:** `phase2_correlations.txt` Section E.

## P3 — Speculative / Needs More Data

### P3.1 — Post-News TSL

Hypothese: 8-K in 7d → große Moves, aber unpredictable Richtung. Fixer SL wird ausgestoppt bevor echter Run kommt. TSL würde Position durch erste Gegenbewegung halten.

```python
has_news = has_8k_within(ticker, now, days=7)
if has_news:
    USE_TSL = True
    TSL_PERCENT = 5  # locker
    INITIAL_SL = cluster_default * 1.5  # weiter gesetzt
else:
    USE_TSL = False  # normaler SL
```

Nicht simuliert. Would need multi-bar-state simulation.

### P3.2 — Signal-Dichte-Regime

Tage mit 20+ Signalen und alle in einem Cluster = "Jack's Theme-Day". Cluster-spezifische Aggression:
- 20+ Signale alle C1 → Q1-Regeln anwenden
- 8+ Signale alle C2 → C2-Regeln, aber kleinere Position (Monster-Regime wahrscheinlicher Outcome)

Nicht getestet.

## Architektur-Skizze

```
Jack-Signal kommt rein
    ↓
1. Parser (bereits existiert) → ticker, text, trade_type
    ↓
2. Classifier.classify(ticker) → cluster (C0/C1/C2/UNKNOWN)
    ↓
3. RuleEngine.apply(cluster, text, ticker, now):
    a) P0.2 Dilution-Check → REJECT if flagged
    b) P2.1 Earnings-Check → REJECT/HALF if flagged
    c) P0.3 kw_careful → apply modifier
    d) P1.1 Friday-C2 → REJECT
    e) P1.2 Swing-C0 → REJECT
    f) P1.3 Time-Bucket C2 → REJECT if not PM
    g) P0.1 Cluster-SL/TP → set params
    ↓
4. signal_manager → create order with final params
```

Inference-Latency-Budget: <500ms (EDGAR ~300ms = biggest chunk).

## Nächste Schritte

- [ ] Morgen mit Dominic: welche P0-Regeln live?
- [ ] `classifier.py`-Skelett mit Cluster-Zuordnung pro Ticker (PKL-File laden)
- [ ] `rules.py`-Skelett mit P0-Regeln hardcoded
- [ ] Integration in `signal_manager.py` als Pre-Trade-Hook
- [ ] EDGAR-Cache-Layer (täglich 6:00 alle 49 Ticker refresh)
- [ ] Monitoring: pro Live-Trade loggen welche Rules gefired haben
- [ ] Nach ~20 Live-Trades: Regeln gegen Realität checken, Shifter vs. Simulation bewerten
