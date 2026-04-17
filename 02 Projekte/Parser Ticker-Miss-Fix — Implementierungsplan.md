# Parser Ticker-Miss-Fix — Implementierungsplan

**Erstellt:** 2026-04-17 während SLS-Review
**Trigger:** 52 SLS-bezogene Messages im Korpus mit `ticker=NULL` entdeckt (1.92% Corpus-Rate, SLS-spezifisch >30% Miss). Parser versiebt ~30% des tatsächlichen SLS-Materials.
**Status:** Plan freigegeben 2026-04-17, **Ausführung deferred bis Review-Komplettierung** (User-Direktive 2026-04-17: „am ende, aber plan speichern").

---

## Problem-Analyse

### Drei Ursachen (Parser-Code gelesen 2026-04-17)

**U1: Regex zu eng — `_TICKER_RE = \b[A-Z]{2,5}\b`**
- Datei: `parser_rules.py:252` und `parser_context.py:62`
- Effekt: Company-Namen wie `SELLAS` (6 Zeichen) werden nicht gematcht
- Keine Alias-Map (SELLAS → SLS, CABA → CABA, etc.)
- Beispiele: SLS #54 „SELLAS IN THE BIOTECH GROUP", #108 „SELLAS Life Sciences (NASDAQ: SLS)"

**U2: Multi-Ticker-Marketing-Block (absolut)**
- Datei: `parser_rules.py:323-330`
- Logik: wenn >2 unterschiedliche Ticker UND kein Entry-Trigger → `NO_SIGNAL`-Blocker (ticker=NULL)
- Effekt: Watchlist/Multi-Ticker-Analysen werden komplett ignoriert
- Beispiele: #113 „watching: SLS IBRX CMPX ALT", #240 „taking notes for: SLS IBRX OCGN CABA ACRV GUTS MIST ALT ABOS VSTM", #117 „Options flow for: IBRX SLS is getting bearish"
- Missed Content: Level-Analysen („SLS IBRX getting bearish sentiment") + Cross-Ticker-Relevanz

**U3: Chain-Inheritance nur via Telegram-Reply**
- Datei: `parser_context.py:151-198` (`resolve_context`)
- Logik: Stage 0 prüft `reply_to_msg_id`, sonst `active_trades`, sonst `none`
- Effekt: Conversational-Chain-Inheritance (Jack postet Folgemessage zum gleichen Ticker ohne Ticker-Token im Text) fehlt komplett
- Beispiele: SLS #232 „weekly support above 3.44~3.54 still intact" (5 Sek nach #228 SLS-Chart), #58 „30 days still intact above 3.35 to 3.45" (nach SLS-Chart-Dump)

### Impact-Schätzung
- Korpus-weit: 52 SLS-Missed / 2'714 Text-Rows = **1.92% Miss-Rate**
- SLS-spezifisch: 52 missed / (120 + 52) = **30.2% Under-Capture**
- Andere Ticker vermutlich ähnlich (IBRX, OCGN, CABA werden oft in Watchlist-Multi-Ticker-Messages genannt)

---

## 2-stufiger Lösungsansatz

### Schritt 1 — DB-Backfill (sicher, keine Live-Bot-Touch)

**Ziel:** Review-Queue vervollständigen, ohne Live-Parser-Code zu ändern.

**Script:** `/root/signal_bot/scripts/backfill_ticker_assignment.py`

**Logik (in Reihenfolge):**
1. Backup: `cp data/backtest_results.db data/backtest_results.db.bak_YYYYMMDD`
2. Scan alle `SELECT * FROM results WHERE new_ticker IS NULL AND old_ticker IS NULL AND raw_text IS NOT NULL AND LENGTH(raw_text) > 0`
3. Pro Row:
   - **(a) Alias-Map anwenden** — Company-Namen auf Ticker mappen:
     ```python
     COMPANY_TO_TICKER = {
         "SELLAS": "SLS", "sellas": "SLS",
         "OCUGEN": "OCGN",
         "IMMUNOGEN": "IMGN",  # etc. — pflegen aus Korpus
         # TODO: aus allen haiku_type=STATUS_UPDATE-Texten eine Liste generieren
     }
     ```
   - **(b) Multi-Ticker-Extraktion** (relaxed):
     - Finde ALLE Ticker-Kandidaten (Regex + Alias-Map + Blacklist)
     - Wenn genau 1 → assign
     - Wenn >1:
       - Primary-Detection: Ticker in erster Zeile (Zeile 1–2) + Ticker in ALL-CAPS + Ticker am Wortanfang = Primary
       - Wenn Primary eindeutig → assign Primary, Rest als `mentioned_tickers` in human_note-Feld
       - Wenn nicht eindeutig → skip (behalte NULL, flag für manual review)
   - **(c) Chain-Inheritance (Fallback)**:
     - Wenn nach (a)+(b) immer noch NULL:
     - Query: prior 30 Min same `channel_id`, same `raw_messages.date`-Window
     - Finde die nächstgelegene Message mit eindeutigem `new_ticker` oder `old_ticker` IS NOT NULL
     - Wenn diese <30 Min alt UND kein Kontextwechsel (kein anderer Ticker im Chain-Window): erbe
     - Sonst NULL belassen
4. `UPDATE results SET new_ticker = ?, human_note = human_note || ' [backfilled: reason=X]' WHERE message_id = ?`
5. Verify-Report:
   - Vorher/Nachher-Count pro Ticker (für Top-10-Review-Queue)
   - Recovery-Rate: wie viele der 52 SLS-Misses recovered
   - Flag-List: welche Messages bleiben NULL nach Backfill (für manual triage)

**Gate:** Recovery-Rate ≥60% auf SLS-Misses. Sonst Logik iterieren (mehr Aliases, breiteres Chain-Window).

**Risiko:** nur `backtest_results.db` (Review-Daten), Live-Trading-Bot unbetroffen. Backup + Rollback-Plan.

**Aufwand:** 30–45 Min (Script + Unit-Tests auf 5 bekannten SLS-Fälle + Backfill + Verify).

### Schritt 2 — Live-Parser-Code-Fix (nach Review-Komplettierung)

**Ziel:** Zukünftige Messages sauber parsen, Root-Cause fixen.

**Dateien:**
- `parser_rules.py` — Regex + Multi-Ticker-Block anpassen
- `parser_context.py` — Chain-Inheritance-Logik ergänzen
- Neue Datei: `parser_aliases.py` — Company-Name-to-Ticker-Map
- Unit-Tests: `tests/test_parser_ticker_extraction.py`

**Code-Änderungen:**

**2a. SELLAS-Alias (+ weitere Biotech-Namen)**
```python
# parser_aliases.py
COMPANY_TO_TICKER = {
    "SELLAS": "SLS",
    "OCUGEN": "OCGN",
    # ... kuratiert aus Korpus
}

def resolve_company_alias(text: str) -> Optional[str]:
    text_upper = text.upper()
    for name, ticker in COMPANY_TO_TICKER.items():
        if name in text_upper:
            return ticker
    return None
```
- Integration in `parser_rules._extract_tickers()` + `parser_context._extract_first_ticker()`

**2b. Multi-Ticker-Cloning statt -Block**
- Anstatt `NO_SIGNAL`-Blocker bei >2 Tickern: jeden Ticker als eigene Row mit `parent_msg_id`
- Siehe `project_parser_multi_ticker_cloning.md` (Option A, bereits beschlossen 2026-04-14)
- Trigger-Case: #240 „taking notes for: SLS IBRX OCGN CABA…" → 10 Rows, alle mit parent_msg_id=240

**2c. Chain-Inheritance (30-Min-Fallback)**
- In `resolve_context()` nach Reply-Check und vor Active-Trades:
```python
# Pfad 1.5: Conversational-Chain (30 Min same channel)
if message_id and channel_id and current_text_has_no_ticker():
    async with aiosqlite.connect(RAW_DB_PATH) as con:
        cur = await con.execute(
            "SELECT text FROM raw_messages "
            "WHERE channel_id = ? AND date BETWEEN datetime(?, '-30 minutes') AND ? "
            "AND LENGTH(text) > 0 "
            "ORDER BY date DESC LIMIT 5",
            (channel_id, current_date, current_date)
        )
        # Extrahiere eindeutigen Ticker aus den 5 prior Messages
        # Wenn 1 Ticker dominiert (≥3 Mal) und kein Kontextwechsel: inherit
```

**2d. Unit-Tests (pflicht, nicht optional)**
- Test-Fixtures aus den 52 SLS-Misses + 10 bekannten Multi-Ticker-Cases
- Expected-Output-Dict pro Fixture
- CI-Gate: keine Regression auf bekannten b-Verdicts

**Aufwand:** 3–5h (Code + Tests + Review + Deploy).

**Gate Schritt 2 → Deploy:**
- Backfill-Logik aus Schritt 1 muss identische Ergebnisse liefern
- 100% Tests grün
- Smoke-Test auf Live-Listener 24h ohne Fehlklassifikationen

---

## Reihenfolge & Timing

**Aktuelle Ausführung:** **Deferred** — erst nach SLS-Review-Abschluss.
- Rationale: `project_priority_review_before_testcenter.md` priorisiert Review komplett fertig bevor Parser/Strategie-Änderungen. Parser-Fix ist substanzielle Logik-Änderung und fällt unter Bot-Verbesserung.
- User-Direktive 2026-04-17: „nein, am ende, aber plan speichern"

**Trigger für Ausführung:**
1. Aktuelle SLS-Review beendet (alle 120 getaggten Messages)
2. Alle Top-N-Ticker-Reviews abgeschlossen (IBRX, OCGN, ACRV, RCKT etc.)
3. Dann: Schritt 1 ausführen → SLS-Review-Nachlauf mit 52 recovered Messages
4. Schritt 2 ausführen → Live-Parser-Code-Fix + Redeploy

---

## Dokumentation & Learnings

- Diese Misses sind ein Beweis, dass Reviews Parser-Gaps identifizieren. Jede Ticker-Review-Session soll zukünftig einen „Parser-Miss-Scan" am Ende enthalten:
  ```sql
  SELECT COUNT(*) FROM results WHERE raw_text LIKE '%<TICKER>%' AND new_ticker IS NULL AND old_ticker IS NULL;
  ```
- Pflege der `COMPANY_TO_TICKER`-Map iterativ aus den Reviews:
  - SLS ↔ SELLAS (gefunden 2026-04-17)
  - TODO: Durchscan aller ticker=NULL Rows nach Firmennamen → Kandidaten-Liste

---

## Verbunden

- `/root/.claude/projects/-root-signal-bot/memory/project_parser_multi_ticker_cloning.md` — Schritt 2b bereits beschlossen
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_quality_maximization.md` — Wochenend-Task, hier andocken
- `/root/.claude/projects/-root-signal-bot/memory/project_priority_review_before_testcenter.md` — Rationale für Deferral
- `/root/.claude/projects/-root-signal-bot/memory/feedback_proactive_bot_improvements.md` — Review-Findings sofort dokumentieren
- `/root/obsidian_vault/02 Projekte/Parser Review/Ticker/SLS.md` — Trigger-Case
