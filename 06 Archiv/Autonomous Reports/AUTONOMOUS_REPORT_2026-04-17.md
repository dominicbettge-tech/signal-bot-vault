---
tags: [inbox, autonomous-report, priority]
date: 2026-04-17
read_at_next_session: true
---

# 📋 Autonomous Session Report — 2026-04-17 Abend

> **USER-AUFGABE:** Beim nächsten Session-Start unaufgefordert lesen. Zusammenfassung was in meiner Abwesenheit autonom gearbeitet wurde.

## Kontext

User ist beim Freundin-Abend, hat autonome Ausführung der 11-Task-Prio-Liste freigegeben. Codex war Plan-Partner, aber **Codex-Quota-Exceeded** → me-alone sequential. Session-Budget zu 50% vor Start genutzt, "zwischen allen Aufgaben stets speichern".

## Abgearbeitete Tasks (Status)

### ✅ P0 #1 Daily-Journal 2026-04-17
- 2 neue Sektionen in Daily Note angehängt: „Abend — SLS-Review-Abschluss + Chart-Pattern-Learner-Setup" und „Abend 2 — Autonomous Block"
- ALWAYS-ON REGEL 4 (Generalisierungs-First) als 4. Triple-Warning in MEMORY.md

### ✅ P1 #2 Testcenter-Backlog 7 Engine-Bugs — **VERIFIZIERT BEREITS DONE**
- Bug #7 (R2 „placed at") ✅ DONE 2026-04-16 — im Backlog als done markiert
- Bug #6 (R8 <14d) ✅ DONE 2026-04-16 — im Backlog als done markiert
- **Bug #8 (R2 „filled" Status-Updates, 13× im Fixture-Set) ✅ DONE** — features.py Zeile 560-595: vollständige B+C-Hybrid-Implementierung aktiv:
  - `is_fill_announcement` requires: `has_fill_announcement AND NOT is_hypothetical_fill AND NOT has_exit_announcement AND NOT is_example_fill AND NOT is_negated_fill AND NOT is_chain_status_update`
  - `_HYPOTHETICAL_RE` erweitert um `if|can|see if|gets me`
  - `_EXAMPLE_FILL_RE` + `_NEGATED_FILL_RE` neu
  - `is_chain_status_update` mit Re-Cap-Pattern-Detection + 30min-Chain-Lookback
- **Verifikation:** Vollsuite `python3 -m unittest discover` → **323 Tests grün** (2 skipped/live-Polygon)

### ✅ P1 #4 R15 Plumbing Schritt A — **VERIFIZIERT BEREITS DONE**
- `runner.py:run_batch(polygon_cur=...)`, `fast_review._review_one(polygon_cur=...)`, `run_daily.py` — alle reichen Polygon-Cursor durch bis `extract_all(market_snapshot=...)`
- `PolygonCurWiringTests` 3/3 grün (no-cur / pass-through / failing-cur graceful)
- **Memory-Backlog-Eintrag ist veraltet, wird am Ende gepatcht**

### ✅ P1 #3 Chart-Pattern-Learner Projekt-Skelett — DONE
- Neues Verzeichnis `/root/chart_pattern_learner/` mit Struktur `data/ schema/ models/ scripts/ notebooks/ tests/`
- `README.md` mit 3 Architektur-Alternativen (Alt-A Vision-LLM, Alt-B XGBoost, Alt-C Hybrid) + 7-Gate-Pipeline
- `schema/feature_spec.md` mit Label-Tabelle + Chart-Image-Features (Candle/Indikator/ZigZag/Volume) + Output-Vektor-Spec + Versionierung v0-v2
- `scripts/sls_data_loader.py` read-only Signal-Bot-DB-Loader
  - **Smoke-Test erfolgreich:** 120 SLS-Verdicts geladen (93n/24w/2s/1e), 43/120 Charts resolved, DB-Schema-Fixes während Dev (results-Tabelle statt verdicts, raw_messages.message_id statt id, media_path relativ zu SIGNAL_BOT_ROOT)
- `.gitignore` (data/, models/, *.parquet)
- **Nicht im signal_bot-Core** — klar getrennt per feedback_sls_excluded_from_tz.md

### 🔴 P1 #4 Codex-Evaluation — BLOCKED: Quota exceeded
- `codex exec "Antworte nur mit PING"` → „ERROR: Quota exceeded. Check your plan and billing details."
- Queue-Skript `codex_review_next.sh` wartet auf Reset (existiert schon)

### ✅ P2 #5 Jack-Edge-Audit Re-Run — DONE
- 83 Buy-Verdicts korpusweit, 77 simulierbar (SLS raus).
- **Jack-Edge naiv:** Mean +1.00% (30m), alle längeren Windows negativ → 🔴 NO-GO Heuristik. 66% Trades ≥5% up in 4h → Upper-Bound bestätigt: Ceiling vorhanden, Timing entscheidet.
- **Hybrid-Exit-Sim Top-5 (korpus-konsistent 2026-04-17):**
  1. **H2_Ladder_33_33_34** — Mean +1.77%, Win 58%, MaxDD −4.69%, TotRet +14.08% ← Default-Strategie bestätigt
  2. H1_Ladder_25_50_25 — +1.63% / 61% / −4.89% / +12.81%
  3. B0_HardTP_10 (Fallback) — +1.24% / 62% / −5.59% / +9.47%
  4. H12_Jack_TP_Preplace — identisch zu B0
  5. B1_Scaled_50_50 — +0.91% / 64% / −3.95% / +6.92%
- **Keine Adaptive-Variante im Top-5** → `feedback_adaptive_stack_validated.md` DATA-REFUTED bleibt korrekt.
- Reports: `Signal Bot Jack-Edge-Audit.md` + `Signal Bot Hybrid-Exit-Sim.md` im Vault

### ✅ P2 #6 Parser-Quality-Maximization Fixture-Prep — DONE
- `testcenter/gates_check.py` angelegt
- G1/G2 lauffähig (callback zu `scripts/self_eval_verdicts.py`)
- G3/G4/G5 als TODO-Stubs — Samstag Block 1/2/7 zieht sie grün
- Exit-Code-Spec: 0 (all pass), 1 (any fail), 2 (any stub) → Cron-/CI-tauglich
- Wochenende kann **mit `gates_check.py --only G1,G2` sofort starten**, baseline 0.633

### 🟡 P2 #7 TSL-by-Trade-Type Sweep — SKIPPED (benötigt Codex, quota blocked)

### ✅ P2 #8 Staggered-Entry-Sim — DONE (⚠️ negatives Signal)
- `scripts/jack_staggered_entry_sim.py` neu, 81 Trades, Offsets [0, +0.5%, +0.75%, +1%]
- **Any-Tranche-Fill-Rate 100%**, Mean 3.44/4 Tranchen gefüllt
- **ABER: Mean-PnL -0.57% @ 20% Winrate** gegen H2-Naive +1.77% @ 58%
- **Trade-Off-Befund:** Höhere Fill-Rate über höheren Avg-Entry führt dazu, dass +5%-TP öfter verpasst wird → Kurs-Edge geht verloren
- Report: `Signal Bot Staggered-Entry-Sim.md`
- **Empfehlung für User:** Staffel-Offsets NUR in Kombination mit niedrigerer TP-Schwelle (z.B. +3%/+7%/+15%) testen, ODER nur bei explizitem SOPA-Typ Low-Fill-Case aktivieren, nicht global. Ursprünglicher Slippage-Fix war overdenken wert.
### ✅ P3 #10 Obsidian-Skills evaluiert — DONE
- Repo kepano/obsidian-skills (24.8k ⭐, MIT) — 5 Skills: obsidian-markdown, obsidian-bases, json-canvas, obsidian-cli, defuddle
- **HIGH-Relevanz:** `obsidian-markdown` (Wikilinks/Callouts/Properties) + `defuddle` (Web→Markdown Token-Saver, passt zu `feedback_token_efficiency.md`)
- **LOW-Relevanz:** obsidian-bases, json-canvas, obsidian-cli (nicht genutzt)
- **NICHT installiert** — User-Entscheidung. Installations-Pfad in Memory dokumentiert (`reference_obsidian_skills_evaluated.md`)
- Empfehlung: manueller Drop in `/root/obsidian_vault/.claude/skills/` statt Global-Marketplace-Install

### 🟡 P2 #7 TSL-by-Trade-Type / P3 #9 Multi-Ticker-Cloning / P3 #11 CC-Extensions — NICHT GEMACHT
- **P2 #7 TSL:** Braucht Codex (quota blocked) oder 1-2h me-alone — Kontext-Budget gegen Ende
- **P3 #9 Multi-Ticker-Cloning:** „Mittel"-Risiko DB-Schema-Änderung, braucht User-Review vor Implementation
- **P3 #11 CC-Extensions:** Cursor zu weit, nicht Session-kritisch

## Offene / Blocker
- **Codex-Quota:** reset unbekannt — blockt P1 #4, P2 #7 Parallel-Benchmark
- **IBRX-Review:** user curatet ZUERST (feedback_user_curates_messages_first.md)
- **Backlog #8 bug:** verifiziert DONE heute, ABER Precision-FAIL in invariants könnte noch andere Ursachen haben → nächstes Smoke-Run zeigt Effekt

## Wichtige Befunde (TL;DR für User)

1. **H2 Ladder 33/33/34 ist unverändert Sieger** auf 77-Trade-Korpus (Mean +1.77%, TotRet +14.08%). **Keine Adaptive-Variante im Top-5** → `feedback_adaptive_stack_validated.md` DATA-REFUTED bestätigt.
2. **Staggered-Entry ist NICHT universal gut** — 100% Fill aber nur 20% Winrate auf H2-Ladder → Kurs-Edge fällt weg. Nur für Low-Fill-Cases (SOPA-Typ) selektiv einsetzen.
3. **Engine-Code-Stand ist überraschend aktuell** — R15 Plumbing + Bug #6/#7/#8 alle bereits implementiert, 323 Tests grün. Backlog-Memory war veraltet (jetzt gepatcht).
4. **Generalisierung-First ist neue ALWAYS-ON-Regel** (4. Triple-Warning in MEMORY.md) — jede Default-Änderung muss Out-of-Sample überleben.
5. **Chart-Pattern-Learner ist als Extra-Projekt aufgesetzt** (`/root/chart_pattern_learner/`) — separiert von Signal-Bot-Core, nutzt SLS-Daten, 7-Gate-Pipeline definiert.

## Persistierungs-Quittung

**Vault-Artefakte:**
- Daily Note 2026-04-17: ergänzt um Abend-Sektion + Abend-2-Sektion
- `Parser Zone-Trade Extractor — Implementierungsplan.md`
- `Signal Bot Jack-Edge-Audit.md` (re-run)
- `Signal Bot Hybrid-Exit-Sim.md` (re-run)
- `Signal Bot Staggered-Entry-Sim.md` (neu)
- `01 Inbox/AUTONOMOUS_REPORT_2026-04-17.md` (dieses File)

**Memory-System (/root/.claude/projects/-root-signal-bot/memory/):**
- `MEMORY.md`: 4. Triple-Warning (Generalisierung-First) + 5 neue Index-Einträge
- Neu: `feedback_generalization_first_always.md`, `project_chart_pattern_learner.md`, `feedback_sls_excluded_from_tz.md`, `project_parser_zone_trade_extractor.md`, `reference_obsidian_skills_evaluated.md`
- Edit: `project_chart_ocr_range_validator.md` (Scope-Clarification), `project_testcenter_backlog_2026_04_15.md` (Bug #8 + R15 Schritt A auf DONE)

**Code-Artefakte:**
- `/root/chart_pattern_learner/` neu (README + schema + loader + .gitignore)
- `/root/signal_bot/testcenter/gates_check.py` neu
- `/root/signal_bot/scripts/jack_staggered_entry_sim.py` neu
- KEINE Änderungen in parser.py / engine.py / runner.py / fast_review.py (bereits on-target)

**Tests-Status:** 323 grün (2 skipped Live-Polygon) bei jedem Full-Suite-Run heute

## Empfehlung für dein „zurück"-Session

1. **Erst:** Diesen Bericht lesen, dann entscheiden
2. **Kurz:** IBRX-Review starten (User-curated Messages erwartet)
3. **Wochenende:** Parser-Quality-Maximization Block 0-4 mit `gates_check.py --only G1,G2` starten — funktioniert schon
4. **Staggered-Entry:** Wenn überhaupt, mit angepasster TP-Ladder (+3%/+7%/+15%) neu simulieren, nicht mit H2-Standard
5. **Chart-Pattern-Learner:** `/root/chart_pattern_learner/scripts/sls_data_loader.py --output ../data/sls_training.parquet` als erster Schritt wenn bereit

---

## 🔄 Nachtrag 2026-04-17 ~21:00 — User schob „weiter autonom suchen" nach

User hat explizit nachgelegt: *„du solltest dir doch autonom aufgabensuchen.ws ist los?"* — 11er-Liste war nicht die Obergrenze. Weiter autonom bis Token-Ende, nach jedem Schritt speichern, Simulationen erlaubt.

### ✅ P2 #7 TSL-by-Trade-Type Sweep — DONE (solo, Codex bleibt quota-blocked)

**Script:** `/root/signal_bot/scripts/tsl_by_trade_type_sweep.py` neu
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot TSL-Sweep.md`
**CSV:** `/root/signal_bot/data/tsl_by_trade_type_sweep.csv` (747 Rows = 83 Trades × 9 TSL)

**Design:** next-bar-open Entry, TSL trailt Peak-Hi, Hard-SL -6% fix, TTL 4h. TSL-Werte 2/3/4/5/6/8/10/12/15 %. Kohorten: `all`, `day_kw`, `swing_kw`, `parser_day`, `parser_unknown`.

**Befunde:**

| Kohorte | Best-TSL | Mean-PnL | Winrate | n |
|---|---|---|---|---|
| all | **2%** | +0.04% | 42% | 83 |
| day_kw (raw_text swing/daytrade match) | **15%** | +2.15% | 36% | 22 |
| swing_kw | **6%** | +0.96% | 37% | 19 |
| parser_day (sonnet.trade_type=day_trade) | **15%** | +1.80% | 35% | 23 |
| parser_unknown | **2%** | -0.07% | 44% | 48 |

**Interpretation (kritisch lesen):**
- Arbeitshypothese aus `project_tsl_by_trade_type.md` (Day=3%, Swing=8-10%) wird **nur teilweise bestätigt**:
  - Swing-Kohorte: 6% ist tatsächlich besser als 3% (+0.96% vs. -0.40%), grob im Hypothesenbereich
  - Day-Kohorte: **überraschend** — 15% deutlich besser als 2-3%. Vermutlich weil 4h TTL hart droppt und enge TSL früh rausschmeißen, bevor Volatilität sich fängt
- **All-Korpus: Best ist 2% TSL** — aber Mean nur +0.04%, das ist kein Edge. Winrate 42% bestätigt den Jack-Edge-Audit-Befund
- TSL-Trefferquote fällt steil: 2% trifft in 81% der Trades, 15% nur in 14% — d.h. 15% funktioniert primär weil es NICHT greift (TTL-Exit dominiert)

**Action:** Noch KEIN Default-Change. Das ist ein Einzel-Korpus-Befund mit bekannten Caveats:
- Keyword-Labeling grobes Proxy (19 swing_kw aus 83)
- Parser-Trade-Type 0 swing, 48 unknown → Label-Qualität mager
- TTL=4h unfair für Swing — müsste 1-3d laufen, nicht modelliert
- Kein Slippage auf TSL-Fill
- Hard-SL -6% dämpft Downside künstlich

**Generalisierung-Check (REGEL 4):** Walk-Forward-Split + Cross-Ticker ≥3 + n≥30 je Kohorte noch offen. TSL-Default bleibt 3% bis G5-Gate grün ist.

### ✅ Chart-Pattern-Learner: Idee „Trading-Bücher als RAG-Corpus" aufgenommen

User-Idee 2026-04-17: *„theoretisch, wenn der chart reader funktioniert, könnte man die wahrscheinlichkeit eines autonomen traderbot erhöhen der nach chartpadderntradet, wenn man ihn mit ein paar tradingbücher über chartpaddern füttert xd"*

**Umsetzung:** `/root/chart_pattern_learner/README.md` + neuer Abschnitt `docs/book_rag_integration.md` (Design-Skizze):
- RAG-Corpus aus public-domain / user-owned Trading-Books (z.B. Bulkowski „Encyclopedia of Chart Patterns", Edwards & Magee „Technical Analysis of Stock Trends", Murphy „Technical Analysis of Financial Markets")
- 3 Alternativen:
  - **Alt-R1 (RAG-Retrieval):** Chart-Features → Similar-Pattern-Chunks aus Büchern → Vision-LLM-Prompt-Augmentation
  - **Alt-R2 (Fine-Tune):** Chart-Snippet + Pattern-Label-Paare aus Büchern für Supervised-Fine-Tune des Hybrid-Models
  - **Alt-R3 (Rule-Extraction):** Bücher → strukturierte Pattern-Rules (breakout, H&S, cup&handle, flag) → deterministisch matchen, Chart-Learner nur als Ergänzung
- Lizenz-Check PFLICHT vor Ingest (Copyright!), lokaler Vector-Store (chromadb oder faiss)
- Generalisierung-Gates G1-G5 gelten auch hier — Buch-Wissen OK, aber Out-of-Sample-Pattern-Detection muss trotzdem n≥30 + cross-ticker bestehen

### ✅ TP-Ladder-Variations-Sim — DONE (neuer Einzel-Edge bestätigt, aber Korpus-schwach)

**Script:** `/root/signal_bot/scripts/tp_ladder_variations_sim.py` neu
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot TP-Ladder-Variations.md`
**CSV:** `/root/signal_bot/data/tp_ladder_variations_sim.csv` (581 Rows = 83 × 7 Varianten)

**7 Varianten getestet** (alle mit SL=-3%, TTL=240min, next-bar-open):

| Rank | Variant | Mean-PnL | Δ vs. H2_base | TP-Full |
|---|---|---|---|---|
| 1 | **user_3_7_15** (+3/+7/+15 × 33/33/34) | -0.151% | **+0.248pp** 📈 | 10/83 |
| 2 | early_weight (+3/+7/+15 × 50/30/20) | -0.191% | +0.207pp 📈 | 10/83 |
| 3 | late_weight (+5/+10/+20 × 25/25/50) | -0.307% | +0.091pp 📈 | 7/83 |
| 4 | moderate_run (+5/+15/+30) | -0.318% | +0.080pp 📈 | 4/83 |
| 5 | **H2_base** (aktuell default) | -0.398% | — | 7/83 |
| 6 | runner (+10/+20/+40) | -0.450% | -0.052pp 📉 | 2/83 |
| 7 | aggressive (+2/+5/+10) | -0.585% | -0.187pp 📉 | 10/83 |

**Meta-Befund (wichtig):** Alle 7 Varianten sind **negativ**. Der Engpass ist nicht die Ladder, sondern der Buy-Korpus selbst (Mean ≈ -0.4% im Schnitt, 22-33% Winrate). Jack-Edge-Audit-Rerun bestätigte das bereits (Mean -1.54% @ 60min naive).

**User-Vorschlag validiert (schwach):** +3/+7/+15 schlägt +5/+10/+20 um +0.25pp. Haupttreiber: engere TPs werden öfter voll gefüllt (10 vs. 7 TP-Full), dadurch mehr realisierter Gewinn auf Runner-Trades.

**Action:** KEIN Default-Change ohne G1-G5 Out-of-Sample-Gates. +0.25pp ist im Noise-Bereich und n=83 ist zu klein. Aber user_3_7_15 ist **Prio-Kandidat** für Phase-C-Sweep mit Walk-Forward + Cross-Ticker.

**Generalisierungs-Check (REGEL 4):** Case ≠ Corpus gilt — der Corpus hat bereits gesprochen, die Richtung stimmt, aber Default-Change braucht separaten Out-of-Sample-Split.

### ✅ Entry-Latenz-Sweep — DONE (non-monotoner Pop-and-Drop-Befund)

**Script:** `/root/signal_bot/scripts/entry_latency_sweep.py`
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot Entry-Latency-Sweep.md`

**Ergebnis:** Non-monoton, 0s/300s günstig, 60-120s Worst-Case

| Latenz | Mean-PnL |
|---|---|
| 0s | -0.40% (baseline) |
| 60s | **-0.98%** 🔴 |
| 120s | **-1.31%** 🔴 |
| 300s | **-0.20%** 🟢 (Pullback-Fenster) |
| 600s | -0.44% |

**Hypothese Pop-and-Drop:** Jacks Posts triggern initial Spike durch Frontrunner. Bei 60-120s kauft Bot aufs Hoch. Bei 300s sind Frontrunner raus, Pullback begonnen → bessere Preise. Bei 600s Normalisierung.

**Live-Relevanz:** Signal-Bot ~6-10s Latenz → **im günstigen Bereich**. **Gefährlich** wäre 60-120s (Parser-Hänger / IBKR-Retry).

**Schutzmaßnahme-Idee (Backlog):** Wenn Order-Placement > 30s nach Msg → (a) skip oder (b) Limit mit aggressivem Offset unter Current-Price.

### ✅ Time-of-Day-Analyse — DONE (🚨 Premarket = Bot-Killer)

**Script:** `/root/signal_bot/scripts/time_of_day_analysis.py`
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot Time-of-Day.md`

**PnL je Bucket (H2-Ladder Exit, SL -3%, TTL 4h):**

| Bucket | n | Mean-PnL | Winrate | SL-Hit-Rate |
|---|---|---|---|---|
| **premarket** (04:00-09:30) | 22 | **-1.31%** 🔴 | 14% | **86%** (19/22) |
| open (09:30-10:30) | 20 | -0.49% | 20% | 85% |
| mid_morning (10:30-12:00) | 18 | -0.41% | 17% | 61% |
| **lunch** (12:00-14:00) | 9 | +0.84% 🟢 | 44% | 44% |
| **afternoon** (14:00-15:30) | 9 | **+1.85%** 🟢 | 33% | 33% |
| after_hours (16:00-20:00) | 5 | -1.75% | 20% | 60% |

**Kritische Befunde:**
1. **Premarket ist Bot-Killer:** 26.5% aller Jack-Buys, 86% SL-Hit-Rate. Wahrscheinlich Pre-Open-Rip-Post dann RTH-Fall Pattern.
2. **Afternoon = Best Zone:** Mean +1.85%, aber nur 10.8% der Signale
3. **Spread Best-Worst: 3.60pp** — signifikanter Edge wenn validierbar

**Neue Hypothesen in R-Hypothesen-Library** (`project_testcenter_r_hypotheses.md`):
- **H10 (R19-Kandidat):** Premarket-Caution — 4 Sub-Varianten (Skip, Half-Size, Wait-for-RTH, VWAP-Limit)
- **H11 (R20-Kandidat):** Entry-Latency-Guard — 3 Sub-Varianten aus 60-120s-Danger-Fenster

**Action:** KEIN Default-Change — Walk-Forward + Cross-Ticker-Validation in Phase C nötig.

### ✅ Combined-Filter-Sim — **VORZEICHEN-WECHSEL** (Baseline → S3 dreht Korpus positiv)

**Script:** `/root/signal_bot/scripts/combined_filter_sim.py`
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot Combined-Filter-Sim.md`

**4 Szenarien auf n=83 b-Verdicts:**

| Scenario | N | Mean-PnL | Winrate | Σ-PnL | Bankroll Δ @200 Trades/Jahr, 20% Size |
|---|---|---|---|---|---|
| `S0_Baseline` (H2, kein Filter) | 83 | -0.37% | 22% | -30.4pp | ≈ **-$1,466/yr** |
| `S1_SkipPM` | 61 | -0.03% | 25% | -1.7pp | ≈ -$82/yr |
| `S2_SkipPM+AH` | 56 | +0.13% | 25% | +7.0pp | ≈ +$339/yr |
| **`S3_S2+User_Ladder`** | **56** | **+0.22%** | **32%** | **+12.4pp** | **≈ +$596/yr** |

**Delta S3 vs. Baseline:** Mean +0.59pp, Winrate +10.5pp, **Σ-PnL +42.8pp**. Das ist auf dem In-Sample-Korpus ein **Vorzeichen-Wechsel** — Bot dreht von leichtem Loss zu leichtem Gain.

**Kombination:** H10a (Skip-Premarket) + H7a-Variante (Skip-AH) + user_3_7_15 (engere TP-Ladder).

**In-Sample-Vorbehalt:** Das ist optimistisches Bias-In-Sample. Walk-Forward + Out-of-Sample-Split + Cross-Ticker-Check PFLICHT vor Default-Change. Aber: Delta ist groß genug (~+60bp Mean-PnL-Verschiebung), dass das Signal nicht nur Noise sein kann.

**Phase-C-Testcenter-Priorität neu:**
1. **Skip-Premarket (H10a)** = 60% des Deltas (-0.37% → -0.03%)
2. **user_3_7_15 Ladder** = 17% des Deltas (+0.13% → +0.22%)
3. **Skip-AH (H7a-PM-Variante)** = 23% des Deltas (-0.03% → +0.13%)

### ✅ Premarket Deep-Dive — DONE (77% SL in 30min, -12.69% Avg-DD, 5% Catalyst)

**Script:** `/root/signal_bot/scripts/premarket_deep_dive.py`
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot Premarket Deep-Dive.md`

**Fakten aus 22 Einzel-Cases:**
- **Avg Gap Entry→RTH-Open: -2.99%** — Bot ist schon am RTH-Open im Schnitt fast -3% (≈SL-Threshold!)
- **Avg Drawdown RTH-First-30min: -12.69%** — massive Intraday-Drops
- **SL-Hit in ersten 30min RTH: 77% (17/22)** — Trades killen sich in der ersten halben RTH-Stunde
- **Catalyst-KW nur 1/22 (5%)** — Premarket-Picks sind NICHT news-getrieben, sondern Jacks spekulative Setups
- **Keine Ticker-Häufung** (CETX 2×, Rest 1×)
- **Stunden-Bias: 68% in 08:00-09:30 ET** (späte Premarket, kurz vor Open)

**Interpretation:** Die Premarket-Verdict-Klasse ist nicht durch Catalysts oder spezifische Biotech-Pumps erklärbar, sondern durch Jacks Posting-Pattern „last-chance-Setups" kurz vor Open. Die Community-Dynamik treibt Preise zu Premarket-High, RTH-Open gap-downed oder gap-uped und dann wird zum SL verkauft.

**H10-Update:** Deep-Dive-Befunde in R-Hypothesen-Memory eingetragen (n=22 Evidence-Base, H10a = klarer Kandidat).

### Artefakte-Nachtrag

**Neu:**
- `scripts/tsl_by_trade_type_sweep.py` + `data/tsl_by_trade_type_sweep.csv` + `02 Projekte/Signal Bot TSL-Sweep.md`
- `scripts/tp_ladder_variations_sim.py` + `data/tp_ladder_variations_sim.csv` + `02 Projekte/Signal Bot TP-Ladder-Variations.md`
- `scripts/entry_latency_sweep.py` + `data/entry_latency_sweep.csv` + `02 Projekte/Signal Bot Entry-Latency-Sweep.md`
- `scripts/time_of_day_analysis.py` + `data/time_of_day_analysis.csv` + `02 Projekte/Signal Bot Time-of-Day.md`
- `scripts/premarket_deep_dive.py` + `02 Projekte/Signal Bot Premarket Deep-Dive.md`
- `scripts/combined_filter_sim.py` + `02 Projekte/Signal Bot Combined-Filter-Sim.md`
- `chart_pattern_learner/docs/book_rag_integration.md` + README-Ergänzung
- `project_testcenter_r_hypotheses.md` — 2 neue Hypothesen H10+H11

**Tests-Status:** Noch nicht neu gelaufen seit letztem 323-Grün; Sweep-Script ist pure Analytics, kein Core-Test-Impact

---

## 🚨 Abend 3 — User-Direktive Generalisierung-First + G5-Gate-Anwendung

User-Direktive 2026-04-17 abends: *"denk bei deiner arbeit daran das alle simulationen an einem unbekannten täglichen markt überleben müssen, beziehe das mit in deine arbeit ein!"*

### ✅ Walk-Forward-Helper (`testcenter/walk_forward.py`) — DONE

Neue Helper-Library für strikte OOS-Validation:
- `time_split(trades, train_fraction=0.7)` — strikt chronologisch, Leakage-Assertion
- `ticker_disjoint_split(trades, holdout_fraction=0.3)` — Ticker-Overlap-Gate
- `walk_forward_splits(train_days=45, test_days=14, step_days=14)` — rolling windows
- `check_leakage(train, test)` — temporal + ticker overlap detection
- `survival_check(trades, strategy_fn)` — voller G5-Gate-Orchestrator → `consistency_flag`

### 🚨 Survival-Check Combined-Filter — KRITISCHER BEFUND

**Script:** `/root/signal_bot/scripts/survival_check_combined.py`
**Report:** `/root/obsidian_vault/02 Projekte/Signal Bot Survival-Check Combined-Filter.md`

Anwendung des G5-Gates auf die 4 heutigen Combined-Filter-Szenarien:

| Scenario | In-Sample Mean | Survival-Score | Verdict |
|---|---|---|---|
| S0_Baseline (H2, kein Filter) | -0.37% | **2/6** ❌ | Negativ aber konsistent |
| S1_SkipPM | -0.03% | **1/6** ❌ | Vorzeichen-Flip Train→Test |
| S2_SkipPM+AH | +0.13% | **1/6** ❌ | Vorzeichen-Flip Train→Test |
| **S3_S2+User_Ladder** (heutiger "Sieger") | **+0.22%** | **1/6** ❌ | Vorzeichen-Flip Train→Test |

**Kern-Befund:** S3 (+0.22% In-Sample Mean, +10.5pp Winrate) erreicht auf OOS nur **1/6 Checks**. Alle Filter-Szenarien zeigen Vorzeichen-Flip (Train positiv → Test negativ). Walk-Forward-Fold-Means zeigen **eine einzige positive Periode** (Dez→Jan), alle anderen Folds verlieren → die In-Sample-Gains sind Regime-Artefakt.

**Ticker-Disjoint-Delta** durchgängig -0.5 bis -1.4pp: der Edge kommt aus wiederholten Tickern, nicht aus der Strategie-Logik.

### Konsequenzen

1. **KEIN Default-Change** für Skip-PM, Skip-AH oder user_3_7_15 Ladder
2. **H10/H11 zurückgestuft** auf „Hypothese mit In-Sample-Evidenz, OOS-FAIL" (memory aktualisiert)
3. **Positives Zeichen:** Das G5-Gate hat funktioniert — Overfit wurde VOR Default-Change erkannt
4. **Nächste Priorität:** Korpus-Ausbau (n≥150, weniger Biotech-Bias), dann Re-Test

### Artefakte-Nachtrag 2

**Neu:**
- `testcenter/walk_forward.py` (G5-Gate-Helper, ~200 LOC)
- `scripts/survival_check_combined.py` (Driver für 4 Szenarien)
- `02 Projekte/Signal Bot Survival-Check Combined-Filter.md` (Report)

**Memory-Updates:**
- `project_testcenter_r_hypotheses.md` — H10 als G5-GATE-FAIL markiert, H11 mit Caveat versehen

**Regel-Stärkung:** `feedback_generalization_first_always.md` wurde heute konkret validiert — der Reflex „sieht im Korpus gut aus → in Memory schreiben" hätte heute 3 falsche Defaults produziert, G5-Gate hat sie gefangen.

---

*Bericht-Ende 2026-04-17 Abend 3. Walk-Forward-Helper + Survival-Check = direkte Antwort auf User-Generalisierung-Direktive. S3-Hypothese tot, Korpus-Grenzen als echtes nächstes Ziel identifiziert.*

---

## 🧪 Abend 4 Nachtrag — Regime + Ticker-Diagnose, Tests

### ✅ Walk-Forward Unit Tests (22/22 grün)
- `testcenter/test_walk_forward.py` neu — 5 Test-Klassen über `time_split` / `ticker_disjoint_split` / `walk_forward_splits` / `check_leakage` / `survival_check`
- Test-Suite-Total: 345 Tests grün (+22)
- Sichert G5-Gate gegen Regressionen — der Helper entscheidet ab jetzt alle Default-Vorschläge

### ✅ Regime-Diagnostic (SPY-basiert)
- `scripts/regime_diagnostic.py` + `02 Projekte/Signal Bot Regime-Diagnostic.md`
- Klassifikation per SPY-20d-Return: BULL (>+2%), FLAT (±2%), BEAR (<-2%)
- **Per-Trade-Verteilung:** BULL -1.05% (n=24) · **FLAT +0.10% (n=53)** · BEAR -1.77% (n=6)
- **Gegen Intuition:** BULL-Regime ist SCHLECHTESTES — Jacks Low-Cap-Setups verlieren gegen Mega-Cap-Rotation
- Walk-Forward: 1/4 positive Fold lag in FLAT-Regime wie 2 andere negative → kein Regime-Edge, Noise-innerhalb-FLAT
- **Kein Regime-Gate als Default-Kandidat** — pro Regime zu wenig n

### ✅ Ticker-Concentration
- 60 unique Tickers / 83 Trades, 67% Singletons (!), Top-3 nur 10.8%
- Korpus ist sehr diversifiziert → Ticker-Disjoint-Fail KEINE Ticker-Concentration
- Stärkt Corpus-Too-Small-Diagnose

### Gesamt-Artefakte Abend 3+4
**Neue Files:**
- `testcenter/walk_forward.py` (Helper, 284 LOC)
- `testcenter/test_walk_forward.py` (22 Unit Tests)
- `scripts/survival_check_combined.py` (G5-Gate-Driver)
- `scripts/regime_diagnostic.py` (SPY-Regime)
- `02 Projekte/Signal Bot Survival-Check Combined-Filter.md`
- `02 Projekte/Signal Bot Regime-Diagnostic.md`

**Memory Updates:**
- `project_testcenter_r_hypotheses.md` — H10 G5-GATE-FAIL, H11 Caveat

### Hauptbefund des Tages (in einem Satz)
**n=83 ist strukturell zu klein für Default-Entscheidungen — die scheinbaren Edges zerfallen im OOS-/Regime-/Walk-Forward-Test. Korpus-Ausbau hat jetzt höhere Prio als weitere In-Sample-Sweeps.**

*Bericht-Ende 2026-04-17 Abend 4. G5-Gate-Workflow operativ, künftig Pflicht vor Default-Vorschlägen.*

## Abend 5 — Indikator-Marathon (autonom ab 22:30 CET)

User-Direktive: *„du sollst autonom abreiten und mich nicht fragen, nach jeder operation oder ende eines test speciehr und dann weiter bis morgen früh"* + *„mit was für indikatoren arbeitet jack wohl und mit welchem könnte man den bot unterstützen"*

### Ausgangsfrage
Welche Indikatoren (RSI, ATR, Volume, MACD, VWAP) würden Jacks Exits unterstützen?
→ 4 Sim-Scripts im Korpus (82 Buys × 1-min-Polygon-Bars × 240-min-TTL × Hard-SL-6%) gebaut und gegen G5-Gate geprüft.

### P1: ATR-TSL — `scripts/atr_tsl_sim.py`
- ATR-14 aus 60-min-pre-entry 1-min-Bars, K ∈ {1, 1.5, 2, 2.5, 3}
- Baseline 3% schlägt **alle** ATR-Varianten (Gewinner -0.36%, bester ATR K1.5 -1.08%)
- ATR-Median 3.49%, 21% der Trades haben ATR <0.5% → premature Exits
- **Verdikt: ❌ Negativ-Finding**, H13 dokumentiert

### P2: RSI-Peak-Exit 1-min — `scripts/rsi_peak_exit_sim.py`
- RSI-14 auf 1-min-Close, Trigger Pos≥+1%+RSI≥70+RSI(t)<RSI(t-3)
- **In-Sample-Peak: `rsi_only` Mean +1.62% vs. Baseline -0.29%** (Δ +1.92pp, +133%-Σ)
- G5-Gate: `consistency_flag=False` (Sign-Flip train<0→test>0) UND `oos_positive_flag=False` (WF -1.57%, 1/4 pos Folds)
- Test-Sieg kommt aus den letzten ~25 Trades — klassisches Regime-Artefakt
- **Verdikt: ❌ G5-Fail**, H12 dokumentiert

### Tool-Upgrade: neuer `oos_positive_flag`
- `consistency_flag` allein war zu streng (verwirft OOS-Improvements)
- Neu: `oos_positive_flag = test_mean>0 ∧ walk_forward mean>0 ∧ ticker_disjoint_test>0`
- Unit Tests: 24/24 grün (+2 für die beiden Flag-Zustände)
- Integration in `rsi_peak_exit_sim.py`, `volume_climax_exit_sim.py`, `rsi_5min_exit_sim.py`, `survival_check_combined.py`

### P3: Volume-Climax-Exit — `scripts/volume_climax_exit_sim.py`
- Volume ≥ K × 20-bar-MA + Bearish-Close + Pos≥+1% → Force-Exit
- K=3 ohne TSL: Mean -1.88% (52 Hard-SL-Hits — TSL-Schutz weg!)
- K=3 + TSL3%: Mean -0.34% (VC triggert nur 1×, de facto = Baseline)
- K=5 ohne TSL: Mean -2.74%
- **Verdikt: ❌ Negativ-Finding**, H14 dokumentiert

### H12c: RSI-5min-Variante — `scripts/rsi_5min_exit_sim.py`
- 1-min-Bars zu 5-min-OHLC aggregiert, RSI-14 auf 5-min-Close, Lag 10min
- `rsi5_tsl3`: Mean -0.20% (Δ **+0.09pp** vs. Baseline)
- `rsi5_only`: Mean -2.11%
- G5-Gate auch hier Fail (train +0.16% → test -1.02%)
- **Kritisches Meta-Finding:** 1-min-Edge +1.92pp, 5-min-Edge +0.09pp → **+1.92pp war pures Noise**

### Gesamt-Artefakte Abend 5
**Neue Files:**
- `scripts/atr_tsl_sim.py`
- `scripts/rsi_peak_exit_sim.py`
- `scripts/volume_climax_exit_sim.py`
- `scripts/rsi_5min_exit_sim.py`
- `02 Projekte/Signal Bot ATR-TSL-Sim.md`
- `02 Projekte/Signal Bot RSI-Peak-Exit-Sim.md`
- `02 Projekte/Signal Bot Volume-Climax-Exit-Sim.md`
- `02 Projekte/Signal Bot RSI-5min-Exit-Sim.md`

**Testcenter-Upgrade:** `oos_positive_flag` in `testcenter/walk_forward.py`, +2 Tests grün

**Memory:** `project_testcenter_r_hypotheses.md` + H12/H12c/H13/H14 + Meta-Lesson-Section

### Hauptbefund Abend 5 (in einem Satz)
**Kein Indikator (ATR, RSI-1min, RSI-5min, Volume-Climax) schlägt fixed-3%-TSL auf n=82 nach G5-Gate — 1-min-Auflösung + kleiner Korpus produzieren systematisch Overfit-Edges, die im 5-min-Denoising zerfallen.**

### Konsequenz für morgen
- Indikator-Erweiterungen **vor** Default-Upgrade brauchen **n≥150 + Cross-Regime + ≥5-min-Auflösung + OOS-Gate**
- Prio bleibt: Parser-Quality-Maximization (mehr Bot-ready-Messages → mehr Trade-Samples)
- fixed-3%-TSL bleibt der einzige OOS-belastbare Default auf diesem Korpus

*Bericht-Ende Abend 5 2026-04-17/18. Alle Findings persistiert, Memory aktualisiert.*
