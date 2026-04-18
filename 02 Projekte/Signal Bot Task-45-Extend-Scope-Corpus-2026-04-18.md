# Task #45 — EXTEND-Scope Corpus-Analyse 2026-04-18

**Auftrag:** Corpus-Size für „EXTEND nach Expiry/Cancel" bestimmen (Hybrid-Design-Workflow n≥30-Gate).

## Current-Bot-Verhalten

`signal_manager.py:_handle_extend` (Zeile 184-211):
- Nur `status=pending` Trades (offene, nicht gefüllte Orders)
- Wenn Order bereits `expired` / `cancelled` / `filled`: **No-Op**

## Corpus-Scan (6 Monate: Oct 2025 – Apr 2026)

- **151 Messages** mit extend/cancel/expire-Keywords
- **22 reine EXTEND-Order-Messages** (saubere „Extended for another N minutes"-Muster)
- **93 Cancel-bezogene Messages** (separat — #48-Thema)

### EXTEND-Parent-Gap-Distribution

| Gap (min) | Count | Bot-Zustand |
|---|---|---|
| 0-15 | 12 | Pending — aktueller Code funktioniert ✅ |
| 15-30 | 5 | Grenzfall (Bot-Default ~30min TTL) |
| 30-60 | 3 | Wahrscheinlich expired ⚠️ |
| 60+ | 2 | Definitiv expired ⚠️ |
| Parent nicht gefunden | 5 | Orphan — unklar |

**→ Nur 4-5 Cases (~18-23%)** profitieren definitiv von der EXTEND-Scope-Expansion.

## Gate-Evaluation (User-Direktive „Generalization-First")

| Gate | Ist | Soll | Status |
|---|---|---|---|
| Corpus n≥30 | **4-5** | 30+ | ❌ FAIL |
| Cross-Ticker ≥3 | ✅ (10+) | 3 | ✅ |
| Out-of-Sample-Split | nicht gemacht | pflicht | ❌ |
| Impact pro Monat | ~0.8 | – | LOW |

**Einschätzung:** Unterhalb des Default-Change-Thresholds. CASE≠CORPUS-Regel greift (n=4-5).

## 5-Step Grounded-Decisions

1. **Features:** EXTEND-msg mit Minuten + Parent-Order mehr als 15min alt + Bot-Status „expired/cancelled"
2. **Prior-Context:** User hat Erweiterung im Gespräch grundsätzlich approved; Corpus-Check war offen.
3. **Precedents:** 
   - Adaptive-Stack-Case 2026-04-17 (n=3 Case → n=77 Corpus Rank 15/15) = Warnsignal gegen Small-N-Rollout
   - #46 Halt-Up-Skim (n=25, +15pp) = grenzwertig, aber strukturell homogen
4. **Alternativen:**
   - **A. Status-quo.** Verlust 0.8 Re-Entries/Monat. Null zusätzliche Fehler-Oberfläche.
   - **B. Hard-Expand (jede EXTEND re-submitted expired/cancelled).** n=5 gewonnen, ABER: Duplikat-Order-Risk, Cancel-by-User-Intent-Risk.
   - **C. Soft-Expand + Safety-Gates.** Nur bei: Parent=EXPIRED (nicht cancelled), Preis ±3% Jack-Entry, konkrete Minuten-Angabe. Config-Flag.
5. **Goal-Alignment:** Live-Readiness-Impact LOW (0.8/Monat × +1-5% pro Trade ≈ 0.02-0.05% Bankroll/Monat). Parallel: #42 Staggered (99 Fälle, +14pp) = Prio höher.

## Empfehlung

**Task #45 bleibt `pending` (NICHT autonom implementieren).**

- Corpus n=4-5 reicht nicht für Default-Change (Regel: n≥30)
- Low-Impact (~0.02-0.05% Bankroll/Monat)
- Fehler-Oberfläche (Duplikat-Order) potenziell höher als Gewinn
- Wenn implementiert: Option C mit strikten Safety-Gates (Config-Flag default OFF)

**Bessere Prio-Reihenfolge:**
1. #42 Staggered-Entry Bot-Code (Corpus n=99, +14pp, arch-choice pending)
2. #46 Halt-Up Bot-Code (n=25, +15pp)
3. (#45 EXTEND-Expiry — danach, wenn überhaupt)

## EXTEND-Corpus-Cases (Referenz)

Parent >15min alt (Expansion-Kandidaten):

| extend_mid | ticker | gap_min | ext_min | Notes |
|---|---|---|---|---|
| 3878 | AHMA | 17 | — | Bis-Uhrzeit, Grenzfall |
| 4636 | IVF | 66 | — | Klarer Expired-Fall |
| 4760 | NUWE | 20 | 15 | Grenzfall |
| 4797 | TIRX | 21 | 5 | Grenzfall + „no fill in time" |
| 5463 | ANNA | 34 | — | Expired |
| 5487 | PAVS | 37 | 10 | Expired |
| 5561 | AGPU | 22 | 3 | Compound-Extend (nach 5560) |

Orphan (kein Parent in 120min-Fenster, evtl. Parser-Gap):
- 4078 MIGI, 4253 MWG, 4483 AKBA, 5372 PRSO, 5531 SST

## Status

Analyse **DONE**, Task-Entscheidung: **bleibt pending** bis User-Approval auf Option C (Soft-Expand mit Safety-Gates, Config-Flag OFF default).
