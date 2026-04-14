---
tags: [signal-bot, klassifikator, phase-2, sentiment]
date: 2026-04-14
status: fertig
parent: "[[Ticker-Klassifikator]]"
---

# Phase 2e — Macro/Market-Keyword-Scan

**Frage:** Kommentiert Jack den Markt so regelmäßig, dass wir seinen Sentiment als Filter nutzen können?

**Kurze Antwort:** **Nein.** Als eigenständiger Filter zu schwach. SPY/VIX direkt verwenden.

## Datenbasis

- 2.658 Messages gescannt (commentary + update + alle anderen)
- 165 Trading-Tage
- 16 Keyword-Kategorien (macro, sentiment, events)

## Ergebnisse

### Keyword-Frequenz (wie oft pro Tag)

| Kategorie | Hits | Anteil Tage |
|---|---|---|
| `scanning` (Begrüßung) | 147 | 64.6% |
| `halted_mention` | 85 | 29.2% |
| `congrats/green team` | 33 | 17.4% |
| `volatile` | 12 | 6.9% |
| `watch_mode / sidelines` | 7 | 4.9% |
| `good_day_outcome` (post-hoc) | 8 | 5.6% |
| `no_trade_today` | 5 | 3.5% |
| `fed/fomc/cpi` | 6 | 3.5% |
| `red_market` | 4 | 2.8% |
| `big_run` | 4 | 2.8% |
| `nothing_worth` | 4 | 2.1% |
| `strong_day` | 3 | 2.1% |

Rest <1% oder = 0.

### Kernerkenntnis

Jack schreibt **kaum** über Markt-Regime. Seine Commentary-Messages sind:
- Begrüßungen ("good morning my team")
- Ticker-Statusberichte ("LAES gained 280%")
- Congrats-Messages nach erfolgreichen Trades
- Gelegentlich Allgemeinplätze wie "scanning activities"

**Er filtert nicht öffentlich nach Markt-Umfeld.** Er sucht Setups an allen Tagen, auch an volatilen/roten.

## Signal-Outcome × Stimmungs-Tag

| Jack-Mood | N Tage | N Trades | Win-Rate | Avg PnL |
|---|---|---|---|---|
| cautious (Jack warnt 2+x/Tag) | 4 | 44 | **38.6%** | **−0.1%** |
| neutral | 139 | 251 | 32.5% | **−1.6%** |
| bearish (net macro −2+) | 1 | — | — | — |

**Überraschung:** Wenn Jack explizit "careful" schreibt, performen die Trades an dem Tag **besser** (+1.5% Delta im avg PnL). Wenige Samples (N=44), aber konsistent mit: Jack's Warnung = echter Vol-Tag, Trader sind selektiver.

⚠️ Ein N=1 bearish Tag ist zu wenig. Muss gesammelt werden über längere Historie.

## Top "Unusual" Tage

### Fed/Macro-Event-Mentions (5 Tage)
- 2025-12-10, 2026-01-28, 2026-02-11, 2026-03-01, 2026-03-17

### Red/Choppy-Tage (14 Tage)
- 2026-04-02, 2026-02-08, 2026-01-12, 2026-01-14 etc.

### Nothing-Found-Tage (8 Tage)
- 2026-02-04, 2025-10-16, 2025-12-22, 2025-10-17, 2026-01-30, 2026-02-06, 2026-03-05, 2026-03-09

Diese 8 Tage wären Kandidaten für "Skip-Day" Regel, aber zu wenige Samples für statistische Aussage.

## Ableitungen für Signal-Bot

### Was NICHT funktioniert
- **Keyword-Only Macro-Filter** → zu wenige Signale. 91% der Tage haben 0 Mood-Marker.
- **"Jack-Warnung" als Hard-Skip** → kontra-produktiv, weil Trades an Caution-Tagen sogar besser performen.

### Was funktionieren könnte
1. **SPY/VIX direkt** als Market-Regime-Filter (bereits in Phase 2 Enrichment: `signals_enriched.csv` hat SPY-Change, VIX-Level)
2. **"Nothing worth risk"-Tage** als schwacher Signal-Quality-Boost: wenn Jack an einem Tag nur 1-2 Signale postet und beide haben caution-Hinweise → Position halbieren
3. **Fed-Event-Tage** als separater Tag für Post-Mortem, nicht als Live-Filter (zu selten N=5)

## Regel-Update v1.1

Füge zu `rules.py` hinzu **als Informations-Layer, nicht als Reject**:

```python
def extract_daily_mood(date_et) -> dict:
    """Scans all messages on this day for macro keywords."""
    return {
        'jack_n_messages': ...,
        'jack_n_caution': ...,
        'jack_n_nothing_worth': ...,
        'spy_change_pct': ...,  # aus enriched signals
        'vix_level': ...,
    }

# Nur als Logging, nicht als Reject-Criterion
```

## Nächste Schritte

- [ ] Phase 2f: Welche VIX/SPY-Kombinationen korrelieren mit Win-Rate-Drop? (Daten liegen schon in signals_enriched.csv)
- [ ] Nach Polygon-Integration: News-Headlines + Sentiment als dritte Layer

## Output-Files

- `/root/signal_bot/reports/ticker_classifier/market_keywords_report.txt`
- `/root/signal_bot/reports/ticker_classifier/daily_mood.csv`
- `/root/signal_bot/reports/ticker_classifier/daily_keywords_v2.csv`
- `/root/signal_bot/scripts/scan_market_keywords.py`
