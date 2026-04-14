---
tags: [briefing, morgen, schlaf-output]
date: 2026-04-14
status: fertig-zum-lesen
---

# Morning-Briefing 2026-04-14

**Für Dominic — was ich nachts gemacht habe während du geschlafen hast.**

## TL;DR (30 Sekunden)

Phase 2 des Ticker-Klassifikators ist **komplett durchgelaufen**. Ich habe:

1. **594 Signale mit Umgebungsdaten angereichert** (SPY/VIX/IWM, Weekday, Time-Bucket, Jack-Keywords)
2. **6.183 SEC-Filings** für unsere 49 Ticker gezogen (8-K, 6-K, S-1/S-3 = Verwässerungs-Warnungen)
3. **1.480 Trades simuliert** (296 Signale × 5 SL/TP-Szenarien)
4. **7 harte Regeln identifiziert**, davon 3× P0 (live-reif)
5. **Phase 3 Skelett geschrieben** (`classifier.py` + `rules.py`) — läuft im Dry-Run-Mode
6. **Regel-Katalog v1** als Vault-Note mit Code-Snippets

Alle Ergebnisse im Vault + scripts-Ordner gespeichert, nichts zu bestätigen.

## Die 3 wichtigsten Befunde

### 1. Nur C1 ist profitabel (Simulation)

| Cluster | Beste Regel | Win-Rate | Avg PnL/Trade |
|---|---|---|---|
| C0 PM-Penny | SL=10%/TP=25% | 21% | **−2.4%** |
| **C1 Solid Day** | **SL=10%/TP=15%** | **44%** | **+1.0%** |
| C2 Monster | SL=20%/TP=40% | 36% | **+1.5%** |

C0 ist strukturell ein Verlust-Cluster in der Simulation — braucht entweder Skip oder komplett andere Regeln. C1 liebt enge Regeln. C2 braucht breite Regeln (20% SL, 40% TP) — Tight SL=5% gibt nur 6% Win-Rate bei C2.

### 2. Dilution-Filings sind ein harter Warner

Wenn ein Ticker in den letzten 7 Tagen ein S-1/S-3/424B5 gefiled hat (Offering/Verwässerung):

| Cluster | ohne Dilution | mit Dilution |
|---|---|---|
| C1 Win-Rate | **42%** | **23%** |
| Global Win-Rate | 30% | 23% |

**Hard-Reject-Kandidat.** Check via SEC EDGAR, kostet 300ms Latency, cacheable.

### 3. C2 Monster am Freitag = Totalausfall

Phase-2-Paradox:
- Jack postet **36% aller C2-Signale am Freitag** (häufigster Tag)
- **C2-Freitags-Trades haben 8% Win-Rate und −7% avg PnL**

Einer der klarsten Mismatches zwischen „wie oft gepostet" und „wie profitabel". Freitags-C2 ignorieren oder auf Montag verschieben.

## Weitere Befunde (Details im Phase-2-Vault-Doc)

- **`kw_careful`** (Jacks eigene Warnung): 0% Win in C0/C2 → Skip. In C1: halbe Position.
- **C2 nur in PM-Bucket** (04:00-09:30 ET): Midday 11% Win, PM 36% Win.
- **C0-Swing-Trades**: 0% Win-Rate (N=7) — Hard-Skip.
- **Earnings am Signal-Tag**: C1 Win-Rate fällt von 57% auf 17%.
- **`low_float` + `bull_flag` Keywords**: 4–4.5× häufiger in C2. Nutzbar für Cluster-Boost bei unbekannten Tickern.
- **Market-Regime-Analyse**: zu wenig Samples. 89% der Signale waren in „chop"-Phase, 0 in „bear". Regime-Filter brauchen längere Historie.

## News-Tage — warum Range ≠ Gewinn

Interessante Paradoxie, die ich gefunden habe:
- 8-K in 7d vor C2-Signal → **3× größere Day-Range** (1194% vs 342%)
- 8-K in 7d vor C2-Signal → **WENIGER profitable Trades** (12% Win vs 25%)

Grund: News-Tage sind volatil, aber die Richtung ist unpredictable. Ein fixer 10% SL wird vom ersten Gegen-Spike ausgestoppt, bevor der eigentliche Move kommt. **Post-News = TSL nötig, nicht fixer SL.** (P3-Regel, noch nicht simuliert.)

## Code-Status

### Neu geschriebene Scripts (lauffähig, getestet)

```
/root/signal_bot/scripts/
  enrich_signals.py              # Signal + Umgebung
  correlate_signals_clusters.py  # Cluster × Umgebung
  fetch_news_sec.py              # SEC EDGAR Filings
  correlate_news_signals.py      # Cluster × News
  correlate_trades_clusters.py   # echte Trades (limitiert)
  simulate_signal_trades.py      # 1480-Trade-Simulation

/root/signal_bot/
  classifier.py                  # Phase-3 Live-Classifier
  rules.py                       # Phase-3 Rule Engine (dry-run)
```

### Test-Lauf des Rule-Engines

```
LAES (C1)  → SL=10% | TP=15% | Pos×1.0 (clean, no reject)
CETX (C2)  → WÜRDE REJECT: kw_careful in C2 + Friday
OMER (C1)  → SL=10% | TP=15% | Pos×1.0 (clean)
VRAX (C0)  → WÜRDE REJECT: C0 PM-Penny default reject
```

Das heißt: von 4 Test-Cases würden 2 geskipped, 2 sauber gehandelt. Das sieht vernünftig aus.

## Ungemachtes / Für heute

1. **Integration in `signal_manager.py`** — classifier + rules als Pre-Trade-Hook einbauen. **Noch nicht getan**, braucht Code-Review gemeinsam mit dir.
2. **EDGAR-Cache-Layer** — tägliche Background-Refresh für alle Watchlist-Ticker. Nur Skeleton skizziert.
3. **Polygon.io** — wolltest du heute Abend einrichten. Dann kann ich PR-News + Sentiment als zusätzliche Layer integrieren.
4. **1min-Daten für CMBM/LVRO** — kommt erst mit Polygon, haben aktuell nur Daily.
5. **Swing-Multi-Day-Simulation** — aktuelle Simulation nur EOD-Exit, Swings werden ungerecht bewertet.
6. **Reale-Trade-Validation** — unsere 18 echten Trades liegen außerhalb Signal-Window, Cross-Validation ist nicht möglich. Sobald neue Jack-Signale geparst sind, kann die Simulation gegen echte Outcomes laufen.

## Die 4 Vault-Docs zum Nachlesen

1. **[[Ticker-Klassifikator Phase 2 Umgebungsdaten]]** — volle Analyse (10 Erkenntnisse)
2. **[[Ticker-Klassifikator Regel-Katalog v1]]** — 7 P0/P1/P2/P3 Regeln mit Code-Snippets
3. **[[Ticker-Klassifikator Phase 1 Ergebnisse]]** — Cluster-Grundlage (von gestern)
4. **[[Ticker-Klassifikator]]** — Master-Plan

## Meine Empfehlung für den Tag

1. Vault-Docs scannen (20 Min)
2. Entscheidung: welche P0-Regeln integrieren wir heute in `signal_manager.py`?
3. EDGAR-Cache-Layer bauen (30 Min Arbeit)
4. Integration + Dry-Run-Mode für 1 Tag laufen lassen bevor scharf geschalten
5. Polygon heute Abend — dann Phase 2e (Pressemitteilungen + Sentiment)

**Caveat:** Simulation ist konservative untere Schranke. TSL + Partial-TPs würden alle Zahlen verbessern. Die Regeln sind Richtungs-richtig, die konkreten Schwellen (10% SL, 15% TP) sollten gegen echte Trades kalibriert werden, nicht blind übernommen.

Guten Morgen.
