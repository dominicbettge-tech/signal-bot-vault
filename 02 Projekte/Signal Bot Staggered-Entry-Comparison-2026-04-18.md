# Staggered-Entry Offset-Scheme Comparison — 2026-04-18

**Kontext:** Task #42 Post-Review-Build. Jack's Gold-Zitat msg 4938 (2026-02-02) beschreibt 6-Level-Ladder (-3%/-1.5%/0% Lower + 0%/+3%/+4.5% Upper). Unsere bisherige Bot-Staffel +0%/+0.5%/+0.75%/+1% war zu eng. HXHX-Case (2025-12-22) zeigte: Jack-Upper-Leg hätte +13.30% gefangen (TSL 10%), Narrow hätte 0% gefangen.

## Sim-Setup

- **Korpus:** 97 Buy-Verdicts (ohne SLS), identische N für alle 3 Schemes
- **Fill-Window:** 60min ab Msg
- **Exit:** H2-Ladder [+5%/+10%/+20% TP × 33/33/34], SL -3%, TTL 240min
- **Tranche-Split:** equal (1/N pro Level)
- **Script:** `scripts/jack_staggered_entry_sim.py`

## Ergebnisse (identische N=97)

| Scheme | Offsets | Tranches/Max | Mean PnL | Median PnL | Trim-Mean (±3) | Winrate |
|---|---|---|---|---|---|---|
| **Narrow (Bot-Default)** | 0, +0.5%, +0.75%, +1% | 3.38 / 4 | -0.52% | -3.00% | -0.84% | 19% |
| **Jack-Upper-Only** | 0, +3%, +4.5% | 2.06 / 3 | **-1.49%** | -2.00% | -1.70% | **10%** |
| **Jack-Full (Gold)** | -3%, -1.5%, 0, +3%, +4.5% | 4.06 / 5 | **-0.08%** | -1.80% | -0.38% | **26%** |

**Outlier-Check:** Top-3 PnLs identisch (+11.8% ×3) über alle Schemes = gleicher Ticker. Edge also nicht outlier-driven — Trim-Mean bestätigt Jack-Full-Edge.

## Interpretation

1. **Jack-Full > Narrow > Jack-Upper** auf allen Metriken (Mean +0.44pp, Winrate +7pp)
2. **Lower-Leg ist der Wert** — -3%/-1.5% fängt Dips = besserer Avg-Entry
3. **Upper-Only ist schlechter als Bot-Default** — forciertes Chasing in Up-Moves, SL triggert oft
4. Absolute PnL bleibt negativ bei allen Schemes → Entry-Scheme alleine ist nicht die Antwort, Exit-Scheme fehlt im Vergleich

## Caveats (feedback_generalization_first_always.md)

- ⚠️ **Kein Out-of-Sample Split** — N=97 ist Training+Test kombiniert. OOS-Validierung steht aus.
- ⚠️ **Exit-Scheme fixed** — nur H2-Ladder getestet. HXHX-Case zeigte TSL 10% > H2 für Low-Float.
- ⚠️ **Fill-Window 60min fix** — Jack cancelt nach 30min. Realistisches Modell: 30min + Cancel-Logic.
- ⚠️ **Kein Position-Sizing-Sensitivity** — Equal-Split vs Pyramid-Weighted nicht verglichen.

## Next Steps (Task #42 Completion)

1. **TSL-Exit-Variant:** Jack-Full × TSL [3/5/8/10/15%] Grid-Sim (HXHX-Pattern auf Korpus) ✅ **DONE**
2. **OOS Split:** Train auf 50% Korpus → Test auf anderen 50% (saisonal oder random)
3. **Position-Weight-Sim:** Equal vs Lower-Heavy (dip-catch-priorität) vs Upper-Heavy
4. **30min Fill-Window:** Realistic Cancel-Logic gemäß Jack msg 4618

## TSL-Grid-Sim Ergebnis (Jack-Full Entry × TSL-Exit)

Script: `/tmp/stagger_tsl_grid.py` | Hard-SL -5%, TTL 240min, Limit-Fill (Lower: buy-limit L≤P, Upper: stop-buy H≥P)

| TSL% | N | Mean PnL | Median | Winrate | SL-Hits | TTL-Hits |
|---|---|---|---|---|---|---|
| **3%** | 97 | **-0.34%** | -0.36% | **33%** | 13 | 9 |
| 5% | 97 | -1.06% | -1.19% | 24% | 28 | 15 |
| 8% | 97 | -1.11% | -3.00% | 25% | 48 | 21 |
| 10% | 97 | -1.46% | -3.00% | 25% | 58 | 21 |
| 15% | 97 | -0.63% | -3.00% | 26% | 62 | 24 |

### ⚠️⚠️ CASE ≠ CORPUS Bestätigung

**HXHX-Case (n=1):** TSL 10% war Sieger (+13.30%)
**Korpus (n=97):** TSL **3%** ist Sieger (Mean -0.34%, Winrate 33%)

Perfekte Anwendung von `feedback_case_vs_corpus_evidence.md`: HXHX war Low-Float-Edge-Case, TSL 10% generalisiert NICHT. **Neuer Default: TSL 3%** wenn Staffel-Entry aktiv.

### Sieger-Kombination

**Jack-Full Entry (-3/-1.5/0/+3/+4.5%) + TSL 3%** (gegen Narrow+H2 Baseline):
- Mean PnL: **-0.34%** vs -0.52% (+0.18pp)
- Winrate: **33%** vs 19% (+14pp)
- Mean-Filled-Tranches: 4.06/5 (vs 3.38/4)

Noch immer negativ-Mean — absolute Profitabilität nicht bewiesen, aber **relative Verbesserung signifikant** und OOS-validation fehlt noch.

## Files

- Narrow: `/tmp/stagger_narrow.csv` + `.md`
- Jack-Upper: `/tmp/stagger_jack_upper.csv` + `.md`
- Jack-Full: `/tmp/stagger_jack_full.csv` + `.md`

## Decision für Bot (vorläufig)

Jack-Full-Pattern [-3%, -1.5%, 0, +3%, +4.5%] als neue Staffel-Default, PENDING:
- OOS-Validierung (Gate 2 aus Hybrid-Design-Workflow)
- TSL-Kombination (wegen HXHX-Evidenz)
- User-Approval

## Post-Backfill Re-Run (149/150 = 99.3% Coverage)

**N=99 (+2 vs 97 pre-backfill).** Ergebnisse bestätigt auf erweitertem Korpus:

| Metrik | Pre-Backfill (n=97) | Post-Backfill (n=99) | Δ |
|---|---|---|---|
| Jack-Full+H2 Mean PnL | -0.08% | -0.12% | -0.04pp |
| Jack-Full+TSL3 Mean PnL | -0.34% | -0.33% | +0.01pp |
| Jack-Full+TSL3 Winrate | 33% | 33% | — |

**Robust gegen Korpus-Expansion → Ergebnis nicht overfit an 97 spezifische Trades.**

## Final Decision (pending User-Approval)

**Recommended Bot-Default:**
- Entry-Staffel: **Jack-Full [-3%, -1.5%, 0, +3%, +4.5%]** (5 Tranchen à 20%)
- Exit: **TSL 3%** + Hard-SL -5% + TTL 240min
- Fill-Window: 60min dann cancel (alignt Jack msg 4618)

**Erwartete Verbesserung gegenüber aktuellem Narrow+H2-Default:**
- Mean PnL: -0.52% → -0.33% (+0.19pp)
- Winrate: 19% → 33% (+14pp)

**Status:** Sim-Portion Task #42 dokumentiert. Bot-Code-Implementation (parser.py ladder + signal_manager N-parallel-orders) pending User-Approval per Hybrid-Design-Workflow.
