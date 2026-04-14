---
tags: [signal-bot, klassifikator, simulation, head-to-head]
date: 2026-04-14
status: fertig
parent: "[[Ticker-Klassifikator]]"
---

# Head-to-Head: aktueller Bot vs. Cluster-Regeln

**Datum:** 2026-04-14 (Nachmittag)
**Datenbasis:** 45 Jack-Entry-Signale mit vollen 1min-Daten (von 121 insgesamt, 76 Signale nicht abgedeckt)
**Position-Size:** $2.000 pro Trade ($10k Bankroll × 20%)

## Drei Strategien im Vergleich

### A — BASELINE (aktueller Bot)

Regeln wie in `config.py`:
- SL: Jack's SL wenn vorhanden, sonst initial 3% unter Entry
- 3% TSL, aktiviert nach +1%
- Auto-TP: 50% bei +3%, 50% bei +6%
- EOD-Exit (day_trade) / max 5d (swing)

### B — CLUSTER (Phase 2 Regel-Katalog)

- C0 default-reject
- C1: SL=10% / TP=15% (fix, voll Position)
- C2: SL=20% / TP=40% (fix, halbe Position)
- P0.3 kw_careful skip C0/C2, halve C1
- P1.1 C2 Friday skip / P1.2 C0 swing skip / P1.3 C2 only PM
- Dilution-Filter

### C — HYBRID

Baseline-Exit-Logic (TSL + Auto-TP), aber **Cluster-Reject-Filter** vorgeschaltet.

## Ergebnisse

| Strategie | Trades | Win-Rate | Avg PnL | Total USD |
|---|---|---|---|---|
| **A Baseline** | 45 | 44.4% | +0.15% | **+$135** |
| **B Cluster (fix)** | 16 (29 rejected) | 43.8% | −1.97% | **−$232** |
| **C Hybrid** | 16 (29 rejected) | 43.8% | **+0.33%** | **+$100** |

## Kritische Erkenntnisse

### 1. Cluster mit fixen SL/TP verliert gegen Baseline

Auf den **gleichen 16 Trades** (die Cluster nicht abgelehnt hat):
- Baseline: +0.33% avg
- Cluster: −1.97% avg
- **Delta: −2.30%**

Die festen 10%/20% Stop-Losses schneiden Positionen zu schnell, bevor die Baseline's TSL den Recovery-Sweep mitnimmt.

### 2. Cluster-Reject-Filter ist marginal negativ

Die 29 rejecteten Trades hätten in Baseline +$29 gemacht. Nicht viel, aber **auch nicht negativ**. Die "Opportunity Cost" der Reject-Regeln ist klein.

**Hybrid (Baseline-Exit + Cluster-Reject) liefert:**
- Mehr PnL pro Trade (+0.33% vs +0.15%)
- Aber weniger Trades (16 vs 45)
- Netto −$35 vs Baseline

### 3. Cluster-weise Breakdown

| Cluster | N | Baseline | Cluster | Delta |
|---|---|---|---|---|
| C0 | 23 (alle reject) | −0.29% WR 39% | — | — |
| **C1** | 13 | +0.36% WR 46% | **+0.64% WR 54%** | **+0.28%** |
| C2 | 9 (3 traded) | +0.97% WR 56% | **−13.27% WR 0%** | **−14.24%** |

**C1 ist der einzige Ort wo Cluster-Regeln gewinnen.** C2 ist ein Disaster — der 20% SL triggert in allen 3 Trades.

### 4. Einzelfälle

**Cluster-Wins (C1 mit TP 15%):**
- BBAI 2025-12-01: Baseline −1.0% vs Cluster **+15.0%** (Baseline's TSL schnitt bei +1% Gewinn ab)
- ALMS 2026-01-06: Baseline +1.8% vs Cluster **+15.0%**
- MIST 2025-12-15: Baseline +4.5% vs Cluster **+15.0%**
- ELDN 2025-11-07: Baseline +4.5% vs Cluster **+15.0%**

**Cluster-Verluste:**
- CETX 2025-12-08 (C2): Baseline −0.4% vs Cluster **−20.0%** (voller SL-Hit)
- MIMI 2025-12-19 (C2): Baseline +2.8% vs Cluster **−12.1%**
- TMDE 2026-01-05 (C1): Baseline +2.2% vs Cluster **−10.0%** (SL-Hit auf Flash-Dip)
- AQST 2026-01-08 (C1): Baseline +1.6% vs Cluster **−10.0%**

## Interpretation

### Baseline-TSL ist mächtig

Die Baseline dominiert in Exit-Reasons mit 28/45 TSL-Hits (62%) und 9/45 Auto-TP-Hits (20%). Das TSL rettet vor Flash-Dips und sichert Teilgewinne. Fester SL macht das nicht.

### Feste TP bei C1 ist Gold wert

Für C1 **war** die feste TP=15% besser als Auto-TP 3/6%, weil Baseline's Auto-TP die Gewinne zu früh abschneidet. BBAI, ALMS, MIST, ELDN hätten alle +15% statt +0-5% gehabt.

**Schlussfolgerung:** Das ideale System:
- **Entry + Reject-Filter:** Cluster-Regeln (P0-P1)
- **Exit C1:** fester TP 15% aber TSL 5% als Safety-Net
- **Exit C2:** Baseline's TSL (3-5%) + Auto-TP — fester SL ist tödlich hier
- **C0:** Default-reject (beide Strategien sind auf C0 negativ/neutral)

### Die "296 vs 45" Diskrepanz

Phase 2d sagte: C1 mit 10/15 → +1% avg, WR 44%. Hier sagen wir: +0.64% avg, WR 54%. Unterschied:
- Phase 2d: 296 Signale, ALLE Ticker inkl. nicht-geclusterte
- Hier: nur 45 Trades mit vollen 1min-Daten

**Phase 2d rechnete mit daily OHLC** (SL/TP-Hit-Heuristik), hier mit echten 1min-Bars (präziser, weil intraday-order flow). Die tatsächliche Performance ist aus 45 Trades gemessen realistischer aber kleiner Stichprobe.

## Was unternehmen?

### Sofort (noch heute, kein Code-Review nötig)

1. **Cluster-Regeln NICHT live deployen** in der aktuellen Form
2. **Memorieren:** Phase-2d-Simulations-Regeln sind überoptimistisch, weil daily-Bar-Approximation

### Nach Polygon-Daten

3. **Hybrid-Variante bauen:** Cluster-Classifier+Reject-Regeln als Pre-Trade-Hook, aber Exit weiterhin Baseline-Mechanik
4. **C1-Experiment:** Feste TP 15% als neue Auto-TP-Level (statt 3%/6%) testen auf N>100
5. **C2-Experiment:** Noch engerer TSL (2%?) statt 20% fester SL

### Mittelfristig

6. **Re-Run** nach Ticker-Set-Erweiterung (39 non-clustered Ticker mit Polygon)
7. **1min-Daten-Backfill** für die 76 Signale die hier fehlten (BBAI/PLRZ/TMDE haben Daten, aber andere tickers müssen ergänzt werden)

## Caveats

- **N=45** ist klein. Mehrere Einzeltrades verzerren Durchschnitte. Zum Beispiel macht BBAI's +15% Cluster-Gewinn 1% des 45-Trade-Durchschnitts aus.
- **Keine Slippage** modelliert (Entry immer zum Limit gefüllt). Real würde Baseline eher unter Entry gefüllt, Cluster gleich.
- **Keine Orders in PM/AH** für Baseline simuliert — aber Jack postet viele in PM. Bot muss diese AH-Signale erkennen können.
- **Aktueller Bot hat mehr:** 2-stufige Auto-TP, Trailing-TP, Orphan-TP — ich habe nur vereinfachte Version simuliert. Echt ist vermutlich etwas besser.

## Output-Files

- `/root/signal_bot/scripts/compare_baseline_vs_cluster.py`
- `/root/signal_bot/reports/ticker_classifier/comparison_baseline_cluster.txt`
- `/root/signal_bot/reports/ticker_classifier/comparison_baseline_cluster.csv`
