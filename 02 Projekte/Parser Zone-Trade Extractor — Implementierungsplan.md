# Parser Zone-Trade Extractor — Implementierungsplan

**Erstellt:** 2026-04-17 während SLS-Chart-Review (43 Charts durchgescannt + 5-Session-Counterfactual-Sim)
**Trigger:** Chart-Durchscan zeigte **0 Jack-gezeichnete Zonen auf allen 43 SLS-Charts** — alle tradebaren Zonen kommen aus dem **Text**, nicht aus den Charts. Counterfactual-Sim mit `entry_style=hi+` ergab +5.58% Bankroll über 5 SLS-Sessions (3/5 Fills, Mean +9.14%/Fill).
**Status:** Plan freigegeben 2026-04-17, **Ausführung deferred bis Review-Komplettierung** (gleiche Regel wie Ticker-Miss-Fix-Plan).

> ⚠️⚠️⚠️ **GENERALISIERUNG-FIRST (Leit-Prinzip dieses Plans, User-Direktive 2026-04-17):**
> Jede Regel/Default (Range-Extractor, Timeframe, Conditional, Entry-Style `hi+`, Chain-Inheritance) muss auf **ZUKÜNFTIGEN, UNBEKANNTEN Charts/Messages profitabel** sein — nicht nur auf SLS-Korpus. Die +5.58% aus der SLS-Sim (n=5) sind **Hypothese, nicht Validierung**. Vor jeder Default-Setzung ist die Generalisierungs-Pipeline (siehe unten) Pflicht. User-Zitat dreifach: „das musst du immer im hinterkopf haben!!"

---

## Generalisierungs-Pipeline (Pflicht vor Default-Setzung)

Jede aus diesem Plan abgeleitete Regel oder jeder Default durchläuft:

1. **In-Sample-Sim** auf SLS-Korpus (bereits gemacht für `hi+`)
2. **Cross-Ticker-Sim** auf ≥3 anderen Tickern (IBRX, OCGN, ACRV, RCKT) — Gate: ≥3 Ticker positiv, Mean ≥ +1pp gegen Baseline
3. **Out-of-Sample-Split** 70/30: Trainings-Korpus bis Datum D, Held-Out ab D+14 Tage — Gate: Out-of-Sample ≥ In-Sample × 0.7 (keine Overfit-Degradation)
4. **Walk-Forward** mit rolling train/test-Windows (z.B. 60/14 Tage) — Gate: Mean über alle Windows positiv, Sharpe > 0
5. **Regime-Split**: bull/bear/flat einzeln messen (SPY-Regime als Filter) — Gate: in keinem Regime negativ
6. **Adversarial-Check**: neue Jack-Message-Varianten (Watchlist-Multi-Ticker, Caution-Keywords, Out-of-Session-Mentions) — darf Regel nicht ad absurdum führen
7. **Corpus-Scale-Gate**: ≥30 Zone-Trades gesamt — sonst bleibt Hypothese (NIE Default)

**Nur wenn alle 7 Gates grün:** Regel wird Live-Default.
**Sonst:** Bleibt ticker-spezifisch (Config-Override) oder wird verworfen.

---

## Problem-Analyse

### Befund aus SLS-Chart-Review (43 Images)
- **Alle 43 Charts = StockMaster Auto-Charts** (ZigZag 5%, SMA 10/50, MACD, RSI) oder Broker-Screenshots
- **ZERO Jack-Overlay-Zeichnungen** — Labels wie `4.84 31.17%` / `3.49 -16.90%` sind StockMaster-Auto-Pivots, keine Handels-Zonen
- **Alle tradebaren Zonen kommen aus dem Text** (z.B. „3.35~3.45", „support above 3.44~3.54", „daily range 3.40 to 3.60")
- Konsequenz: **Chart-OCR für Zone-Extraktion ist redundant** — Parser muss Text-Zonen sauber erfassen

### Counterfactual-Sim-Befund (5 SLS-Sessions)
- Standard-Limit-Entries (`lo`/`mid`/`hi`) füllen selten (1/5 Fills), weil Jacks Support-Zonen echt halten
- **`entry_style=hi+` (zone_hi × 1.005)** fängt Momentum-Breakouts ab → **3/5 Fills, +9.14% Mean, +5.58% Bankroll**
- Market-Entry (`close`) scheitert mit 4 SL-Hits (−0.08% Bankroll)
- **Harte Design-Entscheidung: `hi+` wird Default-Entry-Style für Zone-Trades**

### Die 5 Parser-Lücken (priorisiert)

| # | Lücke | Priorität | Frequenz im SLS-Korpus |
|---|---|---|---|
| **L1** | Range-Extractor-Regex (`3.35~3.45`, `3.40 to 3.60`) | P1 | ~30 Messages |
| **L2** | Timeframe-Tag (`daily`, `weekly`, `monthly`, `90d`, `15d`) | P1 | ~25 Messages |
| **L3** | Konditional-Parser (`if fail X, enter Y`) | P1 | ~8 Messages |
| **L4** | Watchlist-Staging (Zone ohne Entry-Trigger persistieren) | P2 | ~15 Messages |
| **L5** | Chain-Range-Inheritance (30-Min-Window, erbt vorige Zone) | P2 | ~10 Messages |

### Sim-getriebene Zusatz-HYPOTHESE: Entry-Style `hi+`
- **E1 (HYPOTHESE, nicht Default!)** — `entry_style=hi+` (zone_hi×1.005) als Kandidat für Zone-Trades
- In-Sample-Befund SLS n=5: 3/5 Fills, Mean +9.14%, Bankroll +5.58%
- **STATUS: n=5 / 1 Ticker — NICHT genug für Default**, muss alle 7 Gates der Generalisierungs-Pipeline durchlaufen
- Nächster Schritt: Cross-Ticker-Sim auf IBRX/OCGN/ACRV/RCKT nach jeweiliger Review-Komplettierung
- Grund für Hypothese: Stagger 0.5% über Zone-Obergrenze triggert Breakout, während Jack-Support hält und `lo`-Limits selten füllen — aber: könnte SLS-spezifisches Artefakt sein (Biotech-Volatilität, Range-breite, Session-Länge)

---

## 3-stufiger Lösungsansatz

### Schritt 1 — DB-Schema-Erweiterung + Backfill

**Ziel:** Zonen-Struktur in Results-DB kodieren, ohne Live-Parser zu ändern.

**Script:** `/root/signal_bot/scripts/backfill_zone_extraction.py`

**DB-Migration (`backtest_results.db`):**
```sql
ALTER TABLE results ADD COLUMN zone_lo REAL;
ALTER TABLE results ADD COLUMN zone_hi REAL;
ALTER TABLE results ADD COLUMN zone_timeframe TEXT;  -- day/week/month/Nd
ALTER TABLE results ADD COLUMN zone_type TEXT;       -- support/resistance/range/conditional
ALTER TABLE results ADD COLUMN zone_conditional_on TEXT;  -- free-text trigger ("if fail 3.30")
ALTER TABLE results ADD COLUMN zone_source_msg_id INTEGER;  -- für Chain-Inheritance
```

**Backfill-Logik:**
1. Backup: `cp data/backtest_results.db data/backtest_results.db.bak_20260417_zones`
2. Scan alle `SELECT * FROM results WHERE new_ticker IS NOT NULL AND raw_text LIKE '%~%' OR raw_text LIKE '%to%'`
3. Range-Extractor:
   ```python
   RANGE_RE = re.compile(r'(?:\$)?(\d+\.\d{2,4})\s*[~–—\-]\s*(?:\$)?(\d+\.\d{2,4})')
   RANGE_TO_RE = re.compile(r'(?:\$)?(\d+\.\d{2,4})\s+to\s+(?:\$)?(\d+\.\d{2,4})')
   ```
4. Timeframe-Tag:
   ```python
   TF_RE = re.compile(r'\b(daily|weekly|monthly|intraday|(\d+)\s*(day|week|month|hr|hour))\b', re.I)
   ```
5. Zone-Type-Classifier: Kontextwörter (`support`/`resistance`/`range`/`entry zone`/`if`)
6. Update pro Row + Verify-Report

**Gate:** Recovery-Rate ≥70% auf SLS-Range-Messages. Sonst Logik iterieren.

**Aufwand:** 45–60 Min.

### Schritt 2 — Live-Parser-Code-Fix

**Ziel:** Neue Messages sauber zerlegen, Root-Cause fixen.

**Dateien:**
- `parser_rules.py` — Range-Regex + Timeframe-Tag + Conditional-Logik
- `parser_context.py` — Chain-Range-Inheritance (30-Min-Window)
- Neue Datei: `parser_zones.py` — Zone-Extractor mit Unit-Tests
- `db.py` + `models.py` — Schema-Erweiterung Live-DB (analog backtest)
- `tests/test_parser_zones.py` — Fixture-basiert

**Code-Änderungen:**

**2a. Range-Extractor (L1)**
```python
# parser_zones.py
import re
from typing import NamedTuple, Optional

class Zone(NamedTuple):
    lo: float
    hi: float
    timeframe: Optional[str]
    type: str
    conditional_on: Optional[str]

RANGE_PATTERNS = [
    re.compile(r'(?:\$)?(\d+\.\d{2,4})\s*[~–—]\s*(?:\$)?(\d+\.\d{2,4})'),
    re.compile(r'(?:\$)?(\d+\.\d{2,4})\s+to\s+(?:\$)?(\d+\.\d{2,4})'),
    re.compile(r'between\s+(?:\$)?(\d+\.\d{2,4})\s+and\s+(?:\$)?(\d+\.\d{2,4})', re.I),
]

def extract_zones(text: str) -> list[Zone]:
    zones = []
    for pat in RANGE_PATTERNS:
        for m in pat.finditer(text):
            lo, hi = sorted([float(m.group(1)), float(m.group(2))])
            if 0.1 <= lo <= 10000 and hi/lo < 3:  # Sanity
                zones.append(Zone(lo, hi, _extract_tf(text, m),
                                  _classify_zone(text, m), None))
    return zones
```

**2b. Timeframe-Tag (L2)**
- Fenster ±50 Zeichen um Zone-Match scannen
- Keywords `daily/weekly/monthly/Nd/Nw` → `zone_timeframe`
- Default: `unknown` (nicht NULL, damit Analytics filtern kann)

**2c. Konditional-Parser (L3)**
```python
CONDITIONAL_PATTERNS = [
    re.compile(r'if\s+(?:it\s+)?fail(?:s)?\s+(?:\$)?(\d+\.\d{2,4})', re.I),
    re.compile(r'if\s+(?:it\s+)?drop(?:s)?\s+(?:below\s+)?(?:\$)?(\d+\.\d{2,4})', re.I),
    re.compile(r'if\s+(?:it\s+)?(?:breaks?|clears?)\s+(?:\$)?(\d+\.\d{2,4})', re.I),
]
# → zone_conditional_on = "fail 3.30" (free text)
# → verdict bleibt c (conditional), NICHT sofort b
```

**2d. Watchlist-Staging (L4)**
- Neue `WATCHLIST` / `CONDITIONAL_WATCH` Taxonomie soll Zonen **persistieren** (nicht blockieren)
- `parser_rules.py:245` — aus `SOFT_BLOCKERS` raus: `watchlist`, `conditional`
- Stattdessen: `STAGED`-Flag setzen, Bot-Engine prüft später Entry-Trigger

**2e. Chain-Range-Inheritance (L5)**
- In `parser_context.resolve_context()` nach Ticker-Chain-Check:
```python
# Wenn current_message keine eigene Zone hat → prüfe prior 30 Min
if not extracted_zones and channel_id and message_id:
    prior = await get_prior_messages(channel_id, message_id, minutes=30)
    for pm in prior:
        if pm.new_ticker == current_ticker and pm.zone_lo:
            zone_source_msg_id = pm.message_id
            inherit zone_lo/hi/tf/type
            break
```

**2f. Entry-Style-Default `hi+` (E1)**
- `signal_manager.py` — Entry-Order-Builder:
```python
DEFAULT_ENTRY_STYLE = "hi+"  # 2026-04-17: Sim-validiert auf 5 SLS-Sessions

def build_entry_order(zone: Zone, style: str = DEFAULT_ENTRY_STYLE):
    if style == "hi+":
        limit_price = round(zone.hi * 1.005, 2)
    elif style == "hi":
        limit_price = zone.hi
    elif style == "mid":
        limit_price = round((zone.lo + zone.hi) / 2, 2)
    # ...
```
- Config-Override möglich via `.env`: `ZONE_ENTRY_STYLE=hi+` (Default)

**2g. Unit-Tests (pflicht)**
- Fixtures aus allen 43 SLS-Chart-Messages + 10 Range-Messages ohne Chart
- Expected-Output-Dict pro Fixture
- Test-Matrix: Zone-Extraction × Timeframe × Conditional × Chain-Inheritance

**Aufwand:** 4–6h (Code + Tests + DB-Migration + Review + Deploy).

**Gate Schritt 2 → Deploy:**
- Backfill-Logik aus Schritt 1 muss identische Ergebnisse liefern
- 100% Tests grün
- Smoke-Test auf Live-Listener 24h ohne Fehlklassifikationen
- Corpus-Walk auf 77-Trade-Baseline: neue Zonen-Features dürfen Hit-Rate nicht senken

### Schritt 3 — Cross-Ticker-Validierung (vor Scaling)

**Ziel:** Entry-Style `hi+` + Zone-Extractor auf anderen Tickern verifizieren (SLS n=5 zu klein für Default).

**Pipeline:**
1. Nach SLS-Review: IBRX, OCGN, ACRV, RCKT Sessions in gleicher Sim laufen
2. Bankroll-Delta pro Ticker tracken
3. **Gate**: `hi+` muss auf ≥3 Tickern positiv sein UND Corpus-Mean ≥ +1pp gegen `mid`-Baseline
4. Wenn Gate nicht: Entry-Style-Config bleibt ticker-spezifisch, nicht global

**Aufwand:** 2h nach jedem Ticker-Review.

---

## Reihenfolge & Timing

**Aktuelle Ausführung:** **Deferred** — gleiche Regel wie Ticker-Miss-Fix-Plan.

**Trigger für Ausführung (streng sequentiell, Gates-gebunden):**
1. SLS-Review fertig (120/120)
2. IBRX, OCGN, ACRV, RCKT Reviews abgeschlossen (für Cross-Ticker-Datenbasis)
3. **Schritt 1** (DB-Backfill Zone-Extractor L1-L5) ausführen → Backtest-DB erweitert
4. **Schritt 3** (Generalisierungs-Pipeline) — alle 7 Gates auf `hi+`-Hypothese fahren:
   - Wenn alle grün: `hi+` wird Default
   - Wenn teilweise: `hi+` bleibt Config-Override pro Ticker-Regime
   - Wenn rot: `hi+` wird verworfen, neue Entry-Style-Suche
5. **Schritt 2** (Live-Parser-Code-Fix L1-L5 + E1) — nur wenn Schritt 3 Gates grün
6. **24h-Smoke-Test** auf Live-Listener ohne neue Trades (Parser-only)
7. **48h-Paper-Trade-Test** auf Live-Listener mit neuen Zone-Defaults
8. Deploy nach Smoke + Paper grün
9. **Drift-Monitoring** nach Deploy: rolling 14-Tage-Hit-Rate, Alert wenn < 70% der In-Sample-Performance

**Abhängigkeiten:**
- `project_parser_ticker_miss_fix.md` — muss VOR diesem Plan laufen (sonst Backfill doppelt)
- `project_parser_multi_ticker_cloning.md` — kann parallel zu 2b laufen (gleiche Code-Dateien)
- `project_parser_quality_maximization.md` — Wochenend-Task, hier andocken

---

## Dokumentation & Learnings

- **Meta-Learning 1 (2026-04-17 REVIDIERT):** Jack's Zonen kommen aus dem **Text** — aber Charts sind NICHT wertlos. StockMaster-Auto-Features (ZigZag-Pivot-Labels, SMA10/50, RSI, MACD, Volume) sind **eigenständig tradebar**, auch ohne Jack-Overlay. Bei Tickern mit dünnen Text-Entries (SLS: ~10% w-Rate) ist Chart-OCR der primäre Wert-Hebel, nicht nur Soft-Score-Enhancer. `project_chart_ocr_range_validator.md` Scope bleibt korrekt (UC1-UC5), Priorität steigt.
- **Meta-Learning 2**: Entry-Style-Simulation auf Historie **bevor** Parser-Default gesetzt wird — aber In-Sample allein reicht NICHT. Out-of-Sample + Cross-Ticker + Walk-Forward sind Pflicht.
- **Meta-Learning 3**: Der „Jack macht Support-Analysen, die echt halten"-Befund validiert R15 (Staggered-Entry oberhalb Zone) als Generalisierungs-**Kandidat** über Tickers hinweg — aber nur wenn Gates 1-7 grün.
- **Meta-Learning 4 (Leit-Prinzip, fett):** Der Bot muss auf **morgen** profitabel sein, nicht nur auf **gestern**. Jede Regel, die nur auf Trainings-Korpus funktioniert, bricht auf Live-Flow ein (Adaptive-Stack Rank 15/15 ist das Mahnmal).

**Parser-Miss-Scan am Review-Ende (analog Ticker-Miss-Fix):**
```sql
-- Messages mit Range im Text, aber zone_lo IS NULL
SELECT COUNT(*) FROM results
WHERE raw_text REGEXP '[0-9]+\.[0-9]{2}[~–—to ]+[0-9]+\.[0-9]{2}'
  AND zone_lo IS NULL;
```

---

## Verbunden

- `/root/.claude/projects/-root-signal-bot/memory/project_parser_ticker_miss_fix.md` — Schritt 0, Prerequisite
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_multi_ticker_cloning.md` — parallel 2b
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_quality_maximization.md` — Wochenend-Task, hier andocken
- `/root/.claude/projects/-root-signal-bot/memory/project_chart_ocr_range_validator.md` — **neu zu revidieren**: OCR nicht für Zonen, nur für Features
- `/root/.claude/projects/-root-signal-bot/memory/project_priority_review_before_testcenter.md` — Rationale für Deferral
- `/root/.claude/projects/-root-signal-bot/memory/feedback_adaptive_stack_validated.md` — H2-Ladder (Sim-Setup)
- `/root/.claude/projects/-root-signal-bot/memory/project_jack_edge_audit_2026_04_16.md` — Volatility-Edge-These
- `/root/obsidian_vault/02 Projekte/Parser Review/Ticker/SLS.md` — Trigger-Case, Chart-Befund
