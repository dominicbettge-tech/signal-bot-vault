# Loop-Orchestrator — Nacht-Seed 2026-04-20

**Stand:** Mo 2026-04-20 21:55 CET
**Service:** `signal-loop.service` läuft, Digest fällig 2026-04-21 08:00 CET
**Verarbeiteter Miss-Event-Backlog:** 1/1 (ENGINE_SKIP → deferred, korrekt)

---

## Was ich autonom gemacht habe

Da der `missed_trades`-Backlog heute Nacht leer ist (Alt-B ging heute erst live), habe ich **15 aus deinen Research-Memos abgeleitete Hypothesen** gegen das 272-Ticker-Polygon-Corpus durchsimuliert und durch das B-Standard Ship-Gate geschickt.

Skript: `scripts/loop_seed_research_hypotheses.py`

## Ergebnis in einem Satz

**15/15 Hypothesen scheitern — alle am gleichen Gate-Kriterium `trim_top3 does not hold`.** Das heißt: *jede* Verbesserung (TSL, TP, 2-Knob-Kombos) wird von 3 Outlier-Tickern getragen. Sobald du die Top-3-Gewinner aus dem Kandidaten entfernst, liegt er *unter* dem Baseline-Mean.

## Die 15 Tests (sortiert nach Test-Lift)

| # | Tag | Knobs | Train-Lift | Test-Lift | DD | Tickers↑ | Gate-Reason |
|---|-----|-------|-----------:|----------:|----:|---------:|------------|
| 13 | tp3_25pct | TP3=25% | +4.6% | **+234%** | −15% | 9 | train<5%, trim fails |
| 12 | tp2_15pct | TP2=15% | +4.4% | **+232%** | −15% | 12 | train<5%, trim fails |
| 9 | tp1_5pct | TP1=5% | +4.1% | **+231%** | −15% | 16 | train<5%, trim fails |
| 10 | tp1_8pct | TP1=8% | +3.3% | +231% | −15% | 14 | train<5%, trim fails |
| 11 | tp1_10pct | TP1=10% | +3.0% | +230% | −15% | 13 | train<5%, trim fails |
| 3 | tsl_4pct | TSL=4% | +39.4% | +28.6% | −15% | 22 | trim fails |
| 4 | tsl_5pct | TSL=5% | +40.7% | +27.4% | −15% | 22 | trim fails |
| 7 | tsl_act8_tsl5 | act=8%,tsl=5% | +41.9% | +27.4% | −15% | 21 | trim fails |
| 8 | tsl_act10_tsl4 | act=10%,tsl=4% | +41.3% | +27.5% | −15% | 19 | trim fails |
| 6 | tsl_act5_tsl3 | act=5%,tsl=3% | +41.1% | +17.9% | −15% | 21 | trim fails |
| 15 | tp10_tsl2 | TP1=10%,TSL=2% | +41.2% | +17.9% | −15% | 21 | trim fails |
| 5 | tsl_act3_tsl3 | act=3%,tsl=3% | +40.4% | +17.3% | −15% | 21 | trim fails |
| 14 | tp5_tsl3 | TP1=5%,TSL=3% | +39.8% | +16.8% | −15% | 21 | trim fails |
| 1 | tsl_2pct | TSL=2% | +39.8% | +16.8% | −15% | 21 | trim fails |
| 2 | tsl_3pct | TSL=3% | +39.8% | +16.8% | −15% | 21 | trim fails |

*(Test-Lift oben ist ggü. Train-Baseline, nicht Test-Baseline — in Ship-Gate so definiert.)*

## Die Anomalie

**Baseline (hard-SL@15%, keine TSL/TP):** Train-Mean = **+42.9%**

Das ist *unglaublich* hoch. Grund: Polygon-Corpus ist Penny-Stock-lastig; ein paar 10-Bagger wie die `OCGN`-Add-Events schleppen den Mean nach oben.

**Kandidaten mit TSL:** Train = +82–85% → Trim-Top-3 Mean ≈ **0%**.

Die 15 Hypothesen-Sweeps landen alle im gleichen Muster:
- Rohe Durchschnittswerte sehen *exzellent* aus
- Entferne die 3 besten Trades → Rest performt *schlechter* als Baseline

## Was das bedeutet

### Option 1 — das Corpus ist zu spitz
Der Train-Split hat 48 Paare; wenn 3 davon pnl_pct > 100% haben, repräsentieren sie 6% der Paare aber >50% des Mean-Beitrags. Kein Knob kann *diese spezifischen* Winner reproduzieren; der Rest ist Rauschen.

**→ Abhilfe:** Stratifiziertes Subsampling des Corpus — z.B. Median-Volume-Bucket, damit Penny-Stock-Raketen nicht alle Knob-Metriken dominieren. Alternativ: Outlier-Cap bei pnl_pct ≤ 100%.

### Option 2 — das Ship-Gate vergleicht asymmetrisch
Aktuell: `trim_top3(cand) >= mean(base)`. Fairer wäre `trim_top3(cand) >= trim_top3(base)` (Apples-to-Apples). Falls der Baseline selbst auch top-3-lastig ist (sehr wahrscheinlich bei penny-stock-lastigem Corpus), würde die symmetrische Variante den Gate bestehen lassen.

**→ Fix:** 1 Zeile in `loop/ship_gate.py` — auch Baseline trimmen. Siehe `loop/simulator.py:160-164` wo nur Candidate getrimmt wird.

### Option 3 — TSL/TP bringen WIRKLICH nichts in diesem Marktregime
Denkbar, aber unwahrscheinlich — TSL-Literatur (Murphy) und deine eigenen Backtest-Sessions (`project_halt_up_autoskim_peak_tsl.md`) zeigen konsistent +20–30% Uplift.

## Meine Empfehlung (grounded-decisions, 5-Step)

- **Features:** 15/15 Fail auf *ein* Gate-Kriterium; alle anderen Metriken (Train-Lift, DD, Tickers↑) passen; Test-Lift-Zahlen bei TP-Knobs extrem hoch (+231%) weil TP-Exit früh greift bei 10-Baggern.
- **Prior-Context:** Ship-Gate wurde von dir als "B-Standard" spezifiziert am 2026-04-20 morgens; `trim_top3` kam aus der `full-edge-rule-extraction`-Skill-Empfehlung.
- **Precedents:** `project_averaging_sim_2026_04_20` hat ähnliche Ergebnisse — Corpus-Performance ist extrem schief-verteilt. In `project_halt_up_autoskim_peak_tsl` wurde *nicht* gegen dieses Corpus getestet sondern nur gegen die HALT-UP-Subsample (n=53).
- **3 Alternativen:**
  - *Baseline:* Gate unverändert lassen, warten auf echte Miss-Events, nur vom Loop lernen (eng aber robust)
  - *Konservativ:* Gate-Änderung `trim_top3(cand) vs trim_top3(base)` (Option 2 oben), + Corpus-Outlier-Cap bei pnl_pct ≤ 100% (Option 1)
  - *Aggressiv:* Gate weichen lassen (z.B. trim_top3 nur *Warnung* statt Fail), Hypothesen trotzdem shippen
- **Goal-Alignment-Score:** *Konservativ* bringt uns am nächsten zum Ziel "robuste Knob-Entscheidungen aus echtem Edge ableiten" ohne Shipping-Disziplin zu verlieren. Aggressiv öffnet den Outlier-Fall, der uns bei NCPL/FARMR etc. schon gebissen hat.

**→ Empfehlung: Konservativ.** Morgen früh 10 Minuten Fix in `ship_gate.py` + `simulator.py`, dann Re-Run der 15 Hypothesen.

## Saubere 06:00-Stats

- `/loop status` → Service active, cursor at 2026-04-20 21:48 CET
- `/loop proposals` → 0 PENDING (seeded 15 sind REJECTED, markiert als "auto-rejected in overnight seed sweep 2026-04-20")
- `loop_rejected_hypotheses` → 15 Einträge mit rejection_reason — Opus wird diese in zukünftigen Hypothesen-Zyklen als "nicht nochmal vorschlagen" sehen (dialectic prior, Hermes-A Integration)
- Vault-Digest 2026-04-21 erscheint um 08:00 CET — wird leer sein (keine PENDING), aber Telegram-Ping kommt

---

*Rechnen: 15 Sims × 1.0s = 15s Wall-Time. Rest der Nacht = idle Service-Monitoring.*
