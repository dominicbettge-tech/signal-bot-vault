---
tags: [signal-bot, klassifikator, analyse, phase-1]
date: 2026-04-14
status: erste-ergebnisse
parent: "[[Ticker-Klassifikator]]"
---

# Ticker-Klassifikator Phase 1 — Erste Ergebnisse

**Datum:** 2026-04-14 (nachts)
**Datenbasis:** 49 Ticker × ~65 Handelstage × 1min-Bars (2.617.610 Bars)
**Zeitraum:** 2025-10-15 bis 2026-01-15
**Methode:** 17 strukturelle Features → StandardScaler → PCA → k-means

## Kurz-Fazit

**Muster sind erkennbar, aber nicht scharf.** Silhouette-Score ≈ 0.28 für k=3-6 — moderate bis schwache Cluster-Struktur. **k=3 ist der praktikabelste Kompromiss** aus Interpretierbarkeit und Erklärungskraft.

PCA erklärt nur 37% Varianz in der ersten Komponente, 68% in den ersten 5 — deutet auf viele schwach korrelierte Features hin, keine einzelne dominante Struktur-Achse.

## Die 3 Cluster

### C0 — PM-Heavy Penny (24 Ticker, 49%)
- **Preis:** $1.23 median — klassische Penny-Zone
- **PM-Volume-Anteil:** **18%** (hoch!)
- **Day Range:** 11% median, 32% p90
- **Monster-Tage:** 1.6%
- **Mitglieder:** VRAX, ENLV, AMIX, BKYI, MNDR, HIHO, RANI, NCPL, QTTB, SOBR, PLRZ, RADX, KALA, ELBM, GWH, HXHX, SCNX, SIDU, SOPA, WGRX, BBGI, GURE, CETY, TWG
- **Signale:** 139 gesamt, **5.8 pro Ticker**

**Charakter:** Niedrigpreis-Ticker mit starker Pre-Market-Aktivität. Jack handelt diese moderat häufig, Moves sind kontrolliert aber erkennbar.

### C1 — Solid Mid-Cap Day Trade (16 Ticker, 33%)
- **Preis:** $4.39 median
- **PM-Volume:** 4.6% (niedrig)
- **Day Range:** 8.4% median, 17.5% p90 (tightest!)
- **Midday-dominiert:** 58% Volumen zwischen 10:00-15:00
- **Mitglieder:** ADCT, ALMS, AQST, BBAI, ELDN, IKT, IMMP, LAES, MIST, MTC, OMER, PCSA, POM, TMDE, VSTM, WVE
- **Signale:** 134 gesamt, **8.4 pro Ticker** ← meist-getradet

**Charakter:** Stabile, RTH-konzentrierte Tickers mit niedriger Volatilität. Jack's bevorzugtes Jagdrevier — höchste Signal-Dichte pro Ticker.

### C2 — High-Vol Monster-Kandidat (9 Ticker, 18%)
- **Preis:** $3.22 median
- **PM-Volume:** 11.6%
- **Day Range:** 16.6% median, **56% p90**
- **Monster-Tage:** **4.7%**
- **Gap-Häufigkeit:** 3.1% (höchste)
- **Mitglieder:** AHMA, AMCI, CETX, CYPH, MIGI, MIMI, MSPR, TGL, VSEE
- **Signale:** 33 gesamt, **3.7 pro Ticker** ← seltenste

**Charakter:** Explosive Ticker mit häufigen Gap-Moves und seltener Signal-Dichte. Jack fasst die weniger an, aber wenn, dann können's die großen Gewinner sein (CETX 08.12. +229%, AMCI, MSPR im p90 >97%).

## Erkannte Muster

1. **Volatilität entkoppelt sich vom Preis**: C1 (höchster Preis) hat niedrigste Vol, C2 (mittlerer Preis) hat höchste. Nicht klassisch.

2. **Jack-Präferenz ist klar**: C1 (stabil) = 8.4 Signale/Ticker, C2 (Monster) = 3.7. Er bevorzugt kontrollierbare Day Trades. Das ist einerseits vernünftig, andererseits erklärt's warum Monster-Chancen (wie CETX) teils nicht stärker ausgenutzt werden.

3. **PM-Aktivität clustert mit Penny-Level**: Die 8 PM-heavy-Ticker sind fast alle <$1 (VRAX $0.45, AMIX $0.84, BKYI $0.73, ENLV $0.96). After-Hours-Volumen ist bei allen Cluster sehr niedrig (<5%, Ausnahme TWG 27%).

4. **Monster-Kandidaten sind RAR**: Nur 2 Ticker (MSPR, AMCI) haben >100% p90 Range. Selbst in C2 sind die meisten im 50-60% p90 Bereich. Die Monster-Tage sind **Ausnahmen, nicht Regel**.

5. **Autokorrelation überall ≈ 0**: Keine Trend-Persistenz über 1h-Intervalle. Klassisches Random-Walk-Verhalten auf stündlicher Basis. Bedeutet: Momentum-Edge liegt in Sekunden-bis-Minuten, nicht Stunden.

6. **Bullish-Bias variiert**: C1 zeigt 45% bullish-Tage, C0/C2 nur 36%. C1-Ticker haben strukturell weniger Abstürze (auch weil gewählt für Stabilität).

## Regel-Hypothesen (roh, nicht validiert)

| Cluster | SL-Idee | TSL-Idee | Position | Entry-Strategie |
|---|---|---|---|---|
| **C0 PM-Penny** | 1.5 × ATR ≈ **25%** | 2.0 × ATR ≈ **33%** | Halbe (hohe Vol) | PM-Entry ok, Skip bei Spread >5% |
| **C1 Solid Day** | 1.5 × ATR ≈ **15%** | 2.5 × ATR ≈ **25%** | Normale | RTH-only, Open-30min priorisieren |
| **C2 Monster** | 2.0 × ATR ≈ **50%** | No hard TSL, BE-Lock @+20% | Kleine (Risk) | Sofort-Entry auch ohne Limit |

Diese Zahlen sind direkt aus den typischen Intraday-Schwingungen abgeleitet (mean_atr_pct × Multiplikator). **Müssen gegen Trade-Outcomes validiert werden — kommt in Phase 2.**

## Einschränkungen

1. **Silhouette 0.28** — Cluster sind nicht scharf. k=6 war optimal nach Silhouette, aber k=3 ist praktikabler. Es gibt keinen natürlichen "richtigen" Wert.

2. **49 Ticker ist grenzwertig** für 17-dim Clustering. Bessere Klarheit würde mit 100+ Tickern kommen. CMBM/LVRO fehlen im Cluster-Set (nur Daily-Daten).

3. **Kein Zeit-Aspekt integriert** — Features sind Ticker-Aggregate über 65 Tage. Ob der selbe Ticker in Bull- vs Bear-Phase andere DNA zeigt, nicht untersucht.

4. **Keine Jack-Metadaten dabei** — noch keine Sentiment-/Bild-/Keyword-Features integriert. Kommt in Phase 2 als zusätzliche Features oder separater Layer.

5. **Survivorship Bias** — nur "überlebende" Ticker im Set. Delistete/bankrotte Momentum-Namen fehlen.

## Nächste Schritte

1. **Visualisierung** — PCA-Scatter-Plot mit Cluster-Farben, Ticker-Labels. 2D-Plot erzeugen.
2. **Sanity-Check** — Konkrete Trades von gestern (CETX, ALMS) in Cluster-Kontext setzen. Passt die Zuordnung zum beobachteten Verhalten?
3. **Jack-Metadaten** als Zweit-Layer: Innerhalb eines Clusters zusätzlich nach Jack-Signal-Tags clustern (Keyword-Presence, Bild ja/nein, Message-Länge).
4. **Market-Regime** dazunehmen: SPY/VIX/IWM des Signaltages als Feature (nicht des Tickers, sondern des Zeitpunkts).
5. **Regel-Validierung** (Phase 2) — Testcenter mit 1min-Daten nötig; Regel-Skalare (1.5×, 2.0× etc.) gegen Backtest-Performance kalibrieren.

## Dateien

- **Features:** `/root/signal_bot/reports/ticker_classifier/features.csv` (49 × 22)
- **Cluster-Zuordnung:** `features_with_clusters.csv` (inkl. cluster_k3, cluster_k4, cluster_k5)
- **Profile:** `cluster_profiles.csv`
- **Mitglieder:** `cluster_members.json`
- **Scripts:** `/root/signal_bot/scripts/cluster_tickers.py`, `cluster_analyze.py`

## Offene Fragen für nächste Session

- Ergibt es mehr Sinn, hierarchisch zu clustern (statt k-means)?
- Sind die 17 Features das richtige Set, oder überwiegen Volumen-Features das Vol-Profil?
- Macht Soft-Clustering (Gaussian Mixture) mehr Sinn als harte Zuordnung?
- Wie würde ein Tree-Classifier (Decision Tree auf Monster-Tag als Label) aussehen?
