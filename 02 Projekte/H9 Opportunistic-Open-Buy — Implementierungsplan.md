# H9 — Opportunistic-Open-Buy Implementierungsplan

**Erstellt:** 2026-04-17
**Trigger-Case:** NCPL 2025-12-09 — Jack-Limit $0.89–$0.96 nie getriggert, Post-Expiry Halt-Up auf $1.37, Jack Silent-Market-Buy @$1.05, Exit @$1.50 = +43%. Bot mit strikter Limit-Only: **Miss**.
**Memory-Eintrag:** `project_testcenter_r_hypotheses.md` → H9 (1 Case, 1 Ticker)
**Status:** Plan freigegeben 2026-04-17, Start-Gate: Wochenende (Phase 1)

---

## Ziel

Wenn Jacks angekündigte Limit-Range nie getroffen wird UND direkt danach ein Halt-Up am Open stattfindet, soll der Bot autonom nachkaufen — mit Size- und Cap-Limits, die Slippage und Chase-Risiko deckeln. Keine User-Approval-Loop (siehe `feedback_bot_full_autonomy.md`).

## Nicht-Ziele

- Kein generischer Volume-Spike-Trigger (Chase-Bucket-Sim 2026-04-17 hat gezeigt: nicht robust über K-Sensitivitäten)
- Kein Skip-Filter auf Volume allein (Sweet-Spot-Artefakt bei K=3)
- Keine Live-Aktivierung vor Walk-Forward-Validation

---

## 6 Phasen mit Gate-Logik

### Phase 1 — Parser-Range-Extraction (Blocker)

**Was:** Parser um drei neue Felder erweitern — `announced_range_low`, `announced_range_high`, `ttl_minutes`. Strukturiert in `results` persistieren.

**Jack-Jargon-Patterns (zu erkennen):**
- „between $X to $Y" / „between $X and $Y"
- „below $X to $Y" / „watching below $X"
- „price alert at $X to $Y" / „price alert 🔔 at $X"
- „drop to $X" / „if it drops to $X"
- „get some if it gets any fill between $X to $Y"
- „$X–$Y" (Dash-Notation)

**TTL-Patterns:**
- „valid for X minutes" / „in the next X min" / „X-min window"
- „in the coming two hours" → 120 min
- Default wenn nichts angegeben: 60 min (konservativ)

**Vorgehen:**
1. Parser-Pattern-Liste im Prompt ergänzen (few-shot mit NCPL #4002, ORKT #4000, #4002)
2. JSON-Schema um 3 Felder erweitern, `NULL` wenn nicht extrahiert
3. Retroaktiv auf 2'824 Rows in `backtest_results.db` laufen
4. Coverage-Report: Wie viele b-Verdicts haben jetzt Range + TTL?

**Gate Phase 1 → 2:** ≥60% Range-Coverage auf b-Verdicts. Sonst Jargon-Patterns nachziehen oder H9 als unmachbar einstufen.

**Abbruch-Kriterium:** Coverage <40% auch nach Pattern-Iteration → Hypothese closen, in Memory markieren.

**Aufwand:** 4–6h. Parallelisierbar mit `project_parser_quality_maximization.md` (G3-Gate).

---

### Phase 2 — Korpus-Screen: H9-eligible Cases identifizieren

**Was:** Script `scripts/h9_candidate_screen.py` — findet alle b-Trades, bei denen die announced Range im TTL-Fenster NIE getroffen wurde, gefolgt von Halt-Up am Open.

**Logik pro b-Trade:**
1. Lade announced Range + TTL (aus Phase 1)
2. Fetch Polygon-Bars von `msg_et` bis `msg_et + ttl_minutes`
3. Wenn `min(low) <= range_high` → `filled_in_range` (kein H9-Case)
4. Sonst → `expired_no_fill`
5. Für expired: Fetch Bars 09:30–09:35 ET des gleichen Tages
6. Halt-Up-Check: `vol_entry_bar >= 3 × median(vol_pre_30min)` UND `close > open × 1.03`
7. Chase-Cap-Check: `current_price <= range_high × 1.15`
8. Alle Checks erfüllt → `h9_eligible = True`

**Output:** CSV mit n_eligible und Feature-Detail pro Case.

**Gate Phase 2 → 3:** `n_eligible >= 30`. Unter 30 Cases ist Sim nicht aussagekräftig (Memory: `feedback_case_vs_corpus_evidence.md`).

**Fallback bei n<30:** H9 bleibt als Hypothese, weiter Cases sammeln bei zukünftigen Ticker-Reviews. Phase 3–6 werden pausiert bis Threshold erreicht.

**Aufwand:** 1–2h.

---

### Phase 3 — H9-Varianten simulieren

**Was:** Script `scripts/h9_variant_sim.py` — Template `jack_hybrid_exit_sim.py`.

**Drei Varianten:**
- **H9a (Status-quo):** kein Reentry, Baseline. Erwartung: Miss auf allen eligible Cases → 0% PnL-Contribution.
- **H9b (Market-Buy mit Cap):** Market-Buy bei Trigger, Position-Size × 0.5, Cap-Limit +3% über Open-Preis.
- **H9c (Adaptive-Limit-Reentry):** Neue Limit-Order +8–10% über ursprünglicher Range-High, TTL 10 Min, Size × 0.7.

**Exit-Strategie für alle Varianten:** H2-Ladder 33/33/34 (+5/+10/+20) — Corpus-Sieger per 2026-04-17.

**Slippage:** Tier-basiert (Preis-abhängig, 0.15–0.60% Spread + 0.2–1.5% SL-Halt-Boost).

**Ranking-Metrik:** Composite-Score = `Mean × WinRate/100 × (1 − |MaxDD|/20)`.

**Aufwand:** 2–3h.

---

### Phase 4 — Walk-Forward & Sensitivität

**Was:** Validierung, dass H9 nicht overfit ist.

**Out-of-Sample-Split:**
- In-Sample: älteste 80% der eligible Cases
- Out-of-Sample: neueste 20%
- Sieger aus In-Sample muss auch Out-of-Sample positiv sein

**Sensitivitäts-Sweep:**
- Offset-% bei H9c: {5, 7, 9, 11, 13, 15}
- Volume-Threshold beim Halt-Up-Filter: {2.0×, 2.5×, 3.0×, 4.0×, 5.0×}
- TTL-Window-Interpretation: ±5 Min
- Cap-%-Toleranz bei H9b: {1%, 3%, 5%}

**Gate Phase 4 → 5:** Positive Edge (>0 Composite-Score vs Baseline) bei ≥70% der Parameter-Kombinationen. Sonst overfit-Risiko.

**Abbruch-Kriterium:** Edge nur in schmalem Sweet-Spot → Skip-K=3-Falle. Nicht deployen. In Memory als „H9 nicht robust auf n=X" dokumentieren.

**Aufwand:** 2–3h.

---

### Phase 5 — Integration in `position_monitor.py`

**Was:** H9-State-Machine einbauen, wenn Phase 4 grünes Licht gab.

**Neue Module/Methoden:**
- `h9_tracker.py` — verfolgt für jeden aktiven Ticker: Range, TTL, Expiry-Zeitpunkt
- `position_monitor._check_h9_trigger(ticker, current_bar)` — prüft Halt-Up-Bedingung post-Expiry
- `position_monitor._execute_h9_reentry(ticker, variant)` — löst Market-Buy oder Re-Limit aus

**Safety-Gates (alle müssen grün sein):**
- H4-Regel: wenn Distress-Keyword in letzter 30-Min-Chain → blocken
- „too risky" im Jack-Text → blocken
- Max 1 Reentry pro Ticker pro Tag
- Gesamt-Position-Size nach Reentry ≤ normaler 10%-Cap
- Safety-Hard-SL bleibt wie in R15 definiert

**Tests:**
- Unit-Tests für jeden Safety-Gate
- Integration-Test auf NCPL-Fixture (muss H9b/c fire, H9a nicht)
- Negativ-Test: bei Distress-Keyword muss Trigger blocken

**Aufwand:** 2–3h.

---

### Phase 6 — Paper-Live-Smoke

**Was:** H9 aktiv im Paper-Trading, nach Phase B der Profit-Pipeline.

**Observability:**
- Daily-Journal-Metrik: H9-Fires/Tag
- Per-Fire: Ticker, Eingangspreis, Range-Announced, Trigger-Verzögerung, Fill-Preis, Exit-PnL
- Wöchentliche Aggregation: Cumulative H9-Contribution zum Bankroll

**Deaktivierungs-Trigger:**
- Drift-Check: 2 Wochen negative H9-Contribution → auto-off
- Safety-Gate-Verletzungen: >0 blockierte Fires, die manuell als falsch gekennzeichnet werden

**Aufwand:** laufend, 30 Min/Tag Monitoring.

---

## Abhängigkeiten zu anderen Projekten

| Projekt | Beziehung |
|---|---|
| `project_parser_quality_maximization.md` | Phase 1 = G3-Gate dort |
| `jack_hybrid_exit_sim.py` | Template für Phase 3 |
| `feedback_bot_full_autonomy.md` | H9 muss autonom sein, keine User-Approval |
| `feedback_message_chain_awareness.md` | announced Range = echte Order (Jack-Jargon-Regel) |
| `project_staggered_entry.md` | H9 ist Post-Expiry-Reentry-Layer |
| `project_testcenter_r_hypotheses.md` | Hauptablage der H-Patterns |
| `project_reusable_rule_library.md` | Ziel-Ablage (R10-Kandidat) nach Promotion |

---

## Aufwands-Summary

| Phase | Aufwand | Voraussetzung |
|---|---:|---|
| 1. Parser-Range-Extraction | 4–6h | — |
| 2. Korpus-Screen | 1–2h | Phase 1 Gate grün |
| 3. H9-Variant-Sim | 2–3h | Phase 2 n≥30 |
| 4. Walk-Forward | 2–3h | Phase 3 läuft |
| 5. Integration | 2–3h | Phase 4 Gate grün |
| 6. Paper-Smoke | laufend | Phase 5 deployed + Profit-Pipeline Phase B abgeschlossen |

**Gesamt Phase 1–5:** ca. 13–17h. Realistisch Wochenende 2026-04-18/19 für Phase 1, dann Phase 2–4 über 2 Abende.

---

## Offene Fragen

- Interaktion H9 × H4 (Re-Entry-Block): wenn beide aktiv, welcher gewinnt? Default: H4 > H9 (Distress-Block hat Priorität).
- Optimaler Offset-%: NCPL-Case zeigt +8.33% Sweet-Spot. Braucht Corpus-Bestätigung (Phase 4-Sensitivitäts-Sweep).
- Halt-Up-Definition: 3× Volume vs. 5× Volume? Phase 4-Sweep beantwortet das.

## Verbunden

- `/root/.claude/projects/-root-signal-bot/memory/project_testcenter_r_hypotheses.md` (H9-Hypothese-Eintrag)
- `/root/.claude/projects/-root-signal-bot/memory/project_parser_quality_maximization.md` (Phase 1 als G3-Gate)
- `/root/obsidian_vault/02 Projekte/Parser Review/Ticker/NCPL.md` (Trigger-Case)
- `/root/signal_bot/scripts/jack_hybrid_exit_sim.py` (Template Phase 3)
- `/root/signal_bot/scripts/chase_bucket_sim.py` (Negativ-Evidenz, Volume-only reicht nicht)
