# Parser-Accuracy Deep-Dive — 2026-04-18 (6-Path-Solution)

**Auftrag:** „Wie der Parser die best möglichen und genauesten Ergebnisse liefern würde. Tief nachdenken. Verschiedene Wege."

**Current Baseline:** 3-Tier-Cascade Haiku→Sonnet→Opus, Hit-Rate Self-Eval ~66.7% (unter 70%-Gate), bekannte Lücken:
- Chain-Inheritance-Fails (XAIR/ATON 8 Cases)
- Multi-Ticker-Messages (Row-Cloning deferred #38)
- Pronoun-References ohne Ticker-Auflösung
- Haiku unterrepräsentiert e/x (1.4%/2.2% vs erwartet ~5-8%)

---

## Phase 1 — 3 naheliegende Pfade (Same-Stack: Claude-API-NLP)

### A1 Baseline — Prompt-Engineering-Iteration
- Bessere Few-Shots aus 1733 human-labeled Korpus extrahieren
- Chain-Inheritance als Post-Parse-Pass
- Bestehenden Cascade-Flow beibehalten, nur Prompts verbessern
- Known-Pattern-Regression-Test vor Deployment

### A2 Konservativ — Cascade + Confidence-Gates + Schema-Validation
- A1 PLUS:
  - Claude-Parser liefert Confidence-Score (0-1)
  - Gate ≥0.9 direct, 0.7-0.9 Sonnet-Verify, <0.7 Opus+Human-Flag
  - Pydantic-Schema-Validator vor DB-Schreib (blockt fehlformatte Outputs)
  - Dry-Run-Mode: Parser schreibt erst in `review_meta` JSON, Human confirmiert

### A3 Aggressiv — Ensemble + Self-Consistency
- A1 PLUS:
  - Parallel Haiku+Sonnet, Majority-Vote bei Divergenz
  - Self-Consistency: 3× identische Prompts, Mehrheitsantwort
  - Verdict-Predictor-Cross-Check (`predict_verdict.py`)

---

## Phase 2 — 3 laterale Pfade + Divergenz-Gate

### B1 [Tech-Stack] — Deterministisches Regelsystem (Python, kein LLM in Hot-Path)
- YAML-Rule-Engine (knüpft an `project_rule_engine_architecture.md`)
- Regex-Patterns + spaCy-NER für Ticker
- LLM nur als Fallback für unbekannte Patterns (Hybrid)
- Divergenz: **Tech** (Claude → Regex+YAML) + **Philo** (Generativ → Deterministisch)

### B2 [Architektur] — Fine-tuned Small Model (Lokal-Inferenz, Training aus unserer DB)
- Fine-Tune Llama 3B / Mistral 7B auf 1733 labeled Messages
- Quantize (4-bit) → lokale Inferenz auf VPS
- Shadow-Mode: Parallel zu Claude-Parser, Divergenz-Log
- Progressive Cutover nach 2 Wochen Shadow
- Divergenz: **Tech** (API → Local-Model) + **Architektur** (Prompt → Fine-Tune)

### B3 [Philosophie] — Human-in-the-Loop mit Active Learning
- Parser schlägt vor → Human confirmiert ALLES (zero-trust)
- Review-Queue priorisiert by Uncertainty (höchste Entropie zuerst)
- Jedes Human-Verdict wird als Training-Signal für Prompt-Adjust verwendet
- Ziel: 95%+ Accuracy durch Human-Feedback-Loop
- Divergenz: **Philo** (Auto → Human-Curated) + **Verantwortungsgrenze** (Im-Prozess → Human-Bottleneck)

---

## Phase 2.5a — GitHub/Skill-Discovery

Bereits bekannt:
- `signal-parser-review` Skill installed (`/root/.claude/skills/`)
- `claude-trading-skills/` Repo mit 52 Skills geklont
- `backtest-expert + trader-memory-core` aus tradermonty als Blueprint referenziert

Keine direkt adaptierbaren neuen Skills gefunden. A-Pfade sind mit bestehenden Skills angereichert.

---

## Phase 2.5b — Web-Research (skipped: internal signal-bot domain, kein knowledge-cutoff-gap)

Signal-Parser ist domain-spezifisch — best-practices aus generischer LLM-Classification übertragen sich nur teilweise. Fokus auf eigenem Korpus + interner Evidenz.

---

## Phase 3+4 — Blind-Scoring (Q → R → G → Aggregat)

### Q (Qualität: Korrektheit/Wartbarkeit/Testbarkeit)

| | Q | Begründung |
|---|---|---|
| A1 | 5 | inkrementell, kein grundlegender Hit-Rate-Lift |
| A2 | 7 | Confidence-Gates sind state-of-the-art, testbar |
| A3 | 7 | Self-Consistency empirisch validiert, komplexer aber korrekt |
| B1 | 7 | reproducible, debugging easy, aber Coverage an Patterns gebunden |
| B2 | 9 | Fine-Tune ist best-in-class bei ausreichend Data — deterministisch |
| B3 | 7 | Active Learning konvergiert zu 95%+ wenn Zyklen durchgehalten |

### R (Risiko: hoch=safe)

| | R | Begründung |
|---|---|---|
| A1 | 7 | inkrementelle Prompt-Änderung, isoliert |
| A2 | 7 | additive Validation, opt-in via Config-Flags |
| A3 | 5 | parallele API-Calls verdoppeln Kosten, 3× Output kann divergieren |
| B1 | 5 | Rebuild-Risk, Coverage-Lücken bei neuen Jack-Mustern |
| B2 | 3 | Training-Pipeline neu, Deployment-Footprint, Eval-Gap-Risiko |
| B3 | 7 | additive, User-Feedback ist sicherste Quelle |

### G (Goal-Alignment: Live-Bot-Phase-Progress)

| | G | Begründung |
|---|---|---|
| A1 | 5 | inkrementell, kein Phase-B-Unlock |
| A2 | 7 | Confidence-Gates sind Live-kritisch (Gate „kein Bot-Trade bei low-conf") |
| A3 | 5 | Ensemble kostet mehr, marginaler Accuracy-Lift |
| B1 | 5 | Coverage-Risiko bei neuen Jack-Mustern → Live-Regression |
| B2 | 7 | Lokal-Inferenz = Live-Speed + 0-API-Cost, aber Training blockiert Phase |
| B3 | 5 | Active Learning = langsame Konvergenz, kein schneller Live-Unlock |

### Aggregat (0.5·Q + 0.25·R + 0.25·G)

| | Score |
|---|---|
| A1 | 5.50 |
| **A2** | **7.00** ⭐ |
| A3 | 6.00 |
| B1 | 6.00 |
| **B2** | **7.00** ⭐ (initial Tie) |
| B3 | 6.50 |

**Tie A2 ↔ B2 @ 7.00 → Simulation.**

---

## Phase 4.5 — Simulation der Top-2

### A2 Simulation: Cascade + Confidence-Gates + Schema-Validation

**Walkthrough:**
1. Telegram-Msg → Parser.py → Haiku-call mit `return confidence`-Prompt
2. Output: `ParsedSignal(ticker=X, verdict=b, confidence=0.92)`
3. Confidence ≥0.9: direkt an DB + Bot
4. Confidence 0.7-0.9: Sonnet-Verify-Call, Consensus-Check, weiter
5. Confidence <0.7: Opus-Fallback + Telegram-Alert „Manual-Review needed"
6. Pydantic-Validator prüft Schema (Ticker-Format, Preis-Range, Signal-Type-Enum) — blockt Writes wenn fail

**Edge-Cases:**
- ⚠️ Confidence-Score selbst unzuverlässig (LLM-Self-Assessment ≠ actual accuracy)
  - Mitigation: Calibration-Plot auf Hold-out-50 Messages, Gates iterativ anpassen
- Schema-Break bei neuen Jack-Formaten (z.B. neue Price-Notation „$X per ADS")
  - Mitigation: Telegram-Alert + Human-Fallback-Pfad
- Sonnet-Verify 30% der Fälle = +50% API-Cost
  - Mitigation: Haiku-Confidence Gate bei 0.85 nach Calibration (niedriger = weniger Escalation)

**Failure-Modes:**
- Confidence-Gate zu strikt → Bot-Miss-Rate steigt (false-negatives)
- Schema-Validator zu streng → Live-Blocker bei edge-cases

**Rescore:** Q=7 (bleibt), R=7 (bleibt), G=7 (bleibt) → **A2 = 7.00**

### B2 Simulation: Fine-tuned Small Model

**Walkthrough:**
1. Collect Training-Data: 1733 labeled + backfill Haiku-verdicts → ~1900 samples
2. ⚠️ Label-Noise-Check: Haiku ist 66% accurate → ~34% Training-Samples sind wrong
3. Hold-out 20% → N_test=380
4. Fine-Tune Llama 3B via RunPod/Colab ($20-50 one-time)
5. Quantize 4-bit → Model 1.5GB, läuft auf VPS (16GB RAM, kein GPU)
6. Shadow-Mode 2 Wochen parallel zu Claude-Parser
7. Divergenz-Log manuell auswerten
8. Progressive Cutover

**Edge-Cases:**
- ⚠⚠️ **Training-Data zu klein**: Industry-Standard ist 5-10k+ Samples, wir haben 1733 mit Noise
  - Generalization-Fail auf new Jack-Patterns wahrscheinlich
  - LoRA reduziert Data-Requirement, aber hebt es nicht auf
- ⚠⚠️ **Label-Noise ≈34%**: Self-Eval zeigt 66.7% Haiku-Accuracy → Trainings-Signal ist verrauscht
  - Model lernt Noise mit, extrapoliert nicht besser als Haiku selbst
- Dependency-Risk: HF/RunPod-Outage blockiert Training-Pipeline
- Eval-Gap: Kein echter OOS-Test möglich (Review-Backlog siehe V2-Sim-Report)

**Failure-Modes:**
- Silent regressions bei neuen Message-Mustern (z.B. Jack wechselt zu neuem Format 2026-Q2)
- Model-Drift nicht sichtbar ohne laufende Shadow-Metrics

**Rescore nach Sim:**
- Q: 9 → **5** (Training-Data-Volume unter Minimum, Label-Noise 34% vergiftet Signal, Generalization-Fail wahrscheinlich)
- R: 3 → **3** (bleibt)
- G: 7 → **5** (monatelanger Pre-Req: Review-Backlog-Aufholen, Shadow-Cycle)

→ B2 neu = 0.5·5 + 0.25·3 + 0.25·5 = 2.5 + 0.75 + 1.25 = **4.50**

---

## Phase 5 — Winner

**A2 Konservativ (7.00, klar nach Simulation)**

vs B2-neu 4.50. Delta 2.50 → klarer Winner.

B2 Fine-Tune scheitert in der Simulation an zu kleiner & noisy Training-Data. Industry-Standard 5-10k Samples, wir haben 1733 mit 34% Label-Noise. Pre-Req „Review-Backlog aufholen" kostet Wochen und liefert dann nur Ersatz für etwas, das A2 direkt auf Claude-API erreicht.

---

## Konkrete A2-Umsetzung (implementation-ready)

### Komponenten

1. **Confidence-Score-Prompt-Extension** (`parser.py`)
   - Prompt-Postfix: „Rate your confidence 0-1 based on: (a) message clarity, (b) ticker-extractability, (c) signal-type-unambiguity"
   - Parse `confidence` Feld im JSON-Output

2. **Cascade-Gates** (`parser.py` / neue `parser_router.py`)
   ```
   Haiku → confidence
     ≥ 0.9: commit
     0.7 ≤ c < 0.9: Sonnet-Verify, if agree commit
     c < 0.7: Opus + Telegram-Alert + human-review queue
   ```

3. **Schema-Validator** (neue Datei `parser_schema.py`)
   - Pydantic `ParsedSignal(BaseModel)` — Ticker-Regex, Price-Bounds, Enum
   - `validate_parsed_signal()` vor jedem DB-Schreib
   - Fehler-Queue in `parse_failures.db`

4. **Dry-Run-Review-Mode** (extension in `review_ui.py`)
   - Neuer Filter `parser_uncertain` (confidence < 0.7)
   - Review-UI zeigt Parser-Vorschlag + Claude-Reasoning-Snippet

5. **Chain-Inheritance-Post-Pass** (neue Datei `parser_chain_resolver.py`)
   - 30-Min-Fenster gleicher Kanal: Exit/Status ohne Ticker → inherit vom vorherigen Order-Msg
   - Adressiert XAIR/ATON-Fail (Task #47)

6. **Known-Pattern-Test-Suite** (`tests/test_parser_regression.py`)
   - 100 kuratierte Messages mit expected Output
   - Läuft in CI + vor jedem Prompt-Change
   - Regression-Gate: Hit-Rate ≥ letzter Baseline

### Implementation-Reihenfolge

| # | Komponente | Dauer | Priority |
|---|---|---|---|
| 1 | Test-Suite (100 Golden-Messages) | 2h | MUST-FIRST (Safety) |
| 2 | Schema-Validator | 1h | HIGH (prevents DB-corruption) |
| 3 | Confidence-Score Prompt-Extension | 30min | HIGH |
| 4 | Cascade-Router | 2h | HIGH |
| 5 | Chain-Inheritance-Post-Pass | 2h | HIGH (fixes #47) |
| 6 | Dry-Run-Mode in Review-UI | 1h | MEDIUM |

Total ≈ 8.5h → 2-3 Sessions, ein Weekend-Task.

### Success-Metrics

- Parser-Hit-Rate auf Golden-Set ≥ 85% (current ~66.7%)
- Confidence-Calibration: bei reported conf=0.9 tatsächliche Acc ≥ 0.85
- Human-Fallback-Rate < 15% der Messages
- DB-Schema-Errors = 0
- Chain-Inheritance XAIR/ATON-Subset: 8/8 korrekt

### Explizit NICHT geplant

- Fine-Tune Small-Model (B2) — Training-Data-Volume/Quality-Gap, Re-evaluate bei 10k+ clean labels
- Ensemble-Approach (A3) — Cost-Overhead ohne klaren Edge
- Pure-Regex (B1) — Coverage-Risk bei neuen Jack-Mustern
- Active-Learning (B3) — zu langsam für Phase-B-Timeline

---

## 6-Path Kompakt-Ergebnis

```
6-Path-Analyse: Parser-Accuracy-Maximierung   [>10 min | Sim aktiv]

RUNDE 1 (naheliegend)
  A1 Prompt-Iteration                      Q=5 R=7 G=5  →  5.50
  A2 Cascade+Confidence+Schema             Q=7 R=7 G=7  →  7.00 ⭐
  A3 Ensemble + Self-Consistency           Q=7 R=5 G=5  →  6.00

RUNDE 2 (lateral)
  B1 Regex+YAML-Rule-Engine [Tech]         Q=7 R=5 G=5  →  6.00
  B2 Fine-Tune Small-Model [Arch]          Q=9 R=3 G=7  →  7.00 ⭐ (initial)
  B3 Active Learning Human-Loop [Philo]    Q=7 R=7 G=5  →  6.50

Simulation (Top-2):
  A2: Walkthrough ok, Edge-Case „Conf unreliable" → Calibration-Mitigation
      → bleibt 7.00
  B2: Edge-Case „1733 Samples + 34% Noise" → Q 9→5, G 7→5
      → sinkt auf 4.50

→ A2 WINNER (7.00, Δ2.50 klar). Start-Roadmap: Test-Suite → Schema → Confidence → Router → Chain-Inherit.
```

## Status

**Design DONE.** 
- Score-ranked, blind-scored, simulated, winner klar.
- Implementation-Plan vorhanden (6 Komponenten, 8.5h Gesamt).
- User-Approval für Implementation pending.
