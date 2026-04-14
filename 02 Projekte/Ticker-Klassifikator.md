---
tags: [projekt, signal-bot, klassifikator, testcenter]
status: draft
erstellt: 2026-04-14
parent: "[[Signal Bot Live-Roadmap]]"
---

# Ticker-Klassifikator (Controller)

## Kernidee

Ein **Live-Controller** der zur Signal-Zeit eingehende Ticker in **wenige, strukturell abgeleitete Kategorien** einordnet und pro Kategorie pre-kalibrierte SL/TP/Position-Regeln anwendet.

**Ziel:** Robustheit gegen Overfitting. Statt 30 Parameter über alle Trades zu optimieren → 3-5 Kategorien mit einfachen, stabilen Regeln.

## Grundprinzip (korrigiert 2026-04-14)

Kategorien werden **aus Ticker-Bewegungsmustern** abgeleitet, **nicht** aus Trade-Outcomes.
- Datenbasis: 49 Ticker × 65 Handelstage × 1min-Bars = ~1.2M Datenpunkte (strukturell)
- Statt: 61 Trade-Labels (zu wenig für Klassen-Kalibrierung)

Trade-Outcomes werden nur verwendet zur **Validierung**, nicht zur Kategorien-Definition.

## Architektur

```
Jack-Signal kommt rein
    ↓
FeatureExtractor (alles VOR Entry sichtbar)
    ↓
Classifier → Kategorie A/B/C/...
    ↓
Pre-kalibrierte Rules: { SL%, TP%, Position%, TSL%, Entry-Strategy }
    ↓
Order an IBKR
```

Inference zur Laufzeit: < 100ms. Modell wird offline trainiert, als Pickle gespeichert, Bot lädt beim Start.

## Feature-Katalog

### Kern-Features (Phase 1)

**Ticker-Struktur (aus Preis-Historie)**
- Median Day Range %
- Durchschnittliche ATR(5) / Close in %
- Halt-Häufigkeit (±30% in 5min Events)
- Volume-Profile: PM-Anteil / RTH-Open-30min-Anteil / AH-Anteil
- 1h-Autokorrelation (Trend-Persistenz vs Mean-Reversion)

**Ticker-Grundstoffe**
- Preisklasse (<$1, $1-5, $5-10, >$10)
- Sektor (Biotech / Tech / Industrial / SPAC / Crypto-adj)
- Market Cap Band (Nano / Micro / Small)

**Zeit**
- Wochentag (Mo-Fr)
- Uhrzeit-Bucket (PM / Open / Midday / Close / AH)

**Market Regime**
- SPY 1d Return + 20d Trend
- IWM 1d Return (wichtiger für Small-Caps)
- VIX Level + Change

### Sekundär-Features (Phase 2)

**Jack-Metadaten**
- Bild dabei ja/nein
- Nachricht-Länge
- Keywords („low float", „bull flag", „halted up", „careful", „watch")
- Sentiment-Tag (Conviction / Vorsichtig / Warnung)
- Trade-Typ (Day / Swing / Watchlist)
- Reply-Tiefe
- Jack's Tages-Sentiment-Aggregat (NLP über alle Nachrichten des Tages)
- Signal-Dichte des Tages (wie viele Trades insgesamt)

**Ticker-Fundamentals**
- Float-Size
- Short Interest %
- Letzte Earnings-Distanz
- Company-Description-Keywords („clinical trial", „merger", „SPAC")
- 52w-Range + aktuelle Position
- Eigenkapital / Cash / Debt

**Zeit-Verfeinerung**
- Tag im Monat
- Distanz zu Feiertagen
- Earnings-Season Phase

## Kategorien-Hypothese (zu validieren)

| Kategorie | DNA | Regel-Idee |
|---|---|---|
| **High-Vol Monster** | ATR 40%+, PM-heavy, Halts | Wide SL 20%, No TP-Cap, PM-Entry ok, kleine Position |
| **Clean Day Trade** | ATR 10-20%, Open-30min-spike | Tight SL 5%, TP 15%, RTH-only |
| **Low-Liquidity Penny** | Spread >3%, sporadisches Volume | Skip oder minimale Position |
| **Solid Swing** | ATR <15%, evenly spread volume | Wide SL 8%, Multi-day hold |

Anzahl Kategorien wird durch **Cluster-Analyse** bestimmt, nicht vorgegeben. Start mit **2 Kategorien** (Monster vs Normal), dann verfeinern.

## Regel-Ableitung

**Daten-getrieben, nicht Trade-outcome-basiert:**
- SL = 1.5 × typische Intraday-ATR der Kategorie
- TSL = 2.5 × ATR
- Position-Size = C / Volatility (volatilere Kategorie → kleinere Position)
- Entry-Window = typischer Peak-Time-Korridor der Kategorie

Nur die **Skalar-Faktoren** (1.5, 2.5 etc.) werden gegen Trade-Outcomes validiert — deutlich kleineres Sample-Problem als 20-Parameter-Optimierung.

## Methodik

**Phase 1 — Offline Analyse**
1. Feature-Extraktion für alle 49 Ticker aus `price_data_1min.db`
2. Market-Kontext (SPY/VIX/IWM) via yfinance Daily
3. Unsupervised Clustering (k-means + PCA-Reduktion)
4. Cluster-Profile anschauen — machen sie Sinn? Namen finden.
5. Pro Cluster: typische Struktur-Werte → Regel-Skalare

**Phase 2 — Regel-Validierung**
1. Für jede Kategorie: simulierte Performance der Regeln auf den Backtest-Trades
2. Walk-Forward: Train Okt-Nov, Validate Dez-Jan
3. Skalar-Kalibrierung (ATR-Multiplikator 1.5 vs 2.0 vs 2.5)

**Phase 3 — Integration in Bot**
1. `classifier.py` — Feature-Extraktion + Cluster-Assignment
2. `rules.py` — Kategorie → Regel-Map
3. Integration in `signal_manager.py` als Pre-Trade-Hook
4. Fallback: bei unklarer Zuordnung → konservative Default-Regeln

## Abhängigkeiten

- **Testcenter mit 1min-Daten** — Voraussetzung für Regel-Validierung
- **CMBM/LVRO:** nur Daily — werden in der Analyse als Daily-Only markiert oder später via Polygon nachgezogen
- **Parser Review** fortlaufend — generiert saubere Signal-Labels für Phase 2

## Risiken / Caveats

- **Curse of Dimensionality**: 25+ Features × 49 Ticker → Cluster zerfallen. Feature-Reduktion via PCA oder manuelles Grouping nötig.
- **Regime-Drift**: Kategorien aus Okt 2025–Jan 2026 gelten evtl. nicht für Mai 2026 wenn Bull-Momentum stirbt. → Monitoring + periodisches Re-Training.
- **Survivorship Bias**: CMBM/LVRO sind delisted — der Bot sieht in der Historie nur „überlebende" Ticker. Delistete Verlierer fehlen.
- **Kategorien-Overlap**: Ticker kann in mehrere fallen. Priorisierung oder Soft-Assignment nötig.
- **Skip-Kategorie ist der wichtigste Output**: „nicht handeln" wertvoller als feinere SL/TP-Abstufung.

## Nächste Schritte

- [ ] Phase-1-Analyse starten — Feature-Extraktion + erstes Clustering ([[Ticker-Klassifikator Phase 1 Ergebnisse]])
- [ ] Ergebnisse ansehen, Feature-Set ggf. reduzieren
- [ ] Falls Clustering sinnvoll wirkt → Phase 2 Regel-Validierung
- [ ] Falls nicht → Feature-Set überarbeiten oder Ansatz verwerfen

## Bezug zu anderen Projekten

- [[Testcenter — Anforderungen & Architektur]] — Section 6 (Adaptive Strategie-Wahl / Monster-Score) ist dieselbe Idee, hier allgemeiner gefasst
- [[Signal Bot Live-Roadmap]] — Phase 2 (Paper-Profitabilität messen)
- [[Signal Bot Fehler-Log]] — aktuelle Parser-Bugs beeinflussen Label-Qualität
