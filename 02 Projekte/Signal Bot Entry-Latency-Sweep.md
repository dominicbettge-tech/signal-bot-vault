# Signal Bot — Entry-Latency-Sweep

_Generiert: 2026-04-17T21:06:16.653809+00:00_

## Setup
- **Korpus:** `human_verdict='b'` außer SLS
- **N simuliert:** 83 (skipped 0)
- **Latenzen:** [0, 60, 120, 300, 600] Sekunden (= 0/1/2/5/10 min delay)
- **Exit:** H2-Ladder [0.05, 0.1, 0.2] × [0.33, 0.33, 0.34], SL -3%, TTL 240min
- **Entry-Modell:** open der N-ten 1min-Bar nach Msg (N = latency/60)

## Latenz-Impact

| Latenz | Mean-PnL | Median | Winrate | SL-Hit | TP-Full | Mean-Entry-Drift vs. 0s |
|---|---|---|---|---|---|---|
| 0s (0min) | -0.401% | -3.00% | 22% | 57/83 | 8/83 | — |
| 60s (1min) | -0.978% | -3.00% | 18% | 63/82 | 3/82 | -0.269% |
| 120s (2min) | -1.309% | -3.00% | 17% | 65/81 | 2/81 | -0.073% |
| 300s (5min) | -0.199% | -3.00% | 25% | 58/81 | 8/81 | -1.090% |
| 600s (10min) | -0.444% | -3.00% | 22% | 60/81 | 5/81 | +0.166% |

## Edge-Decay pro +60s Latenz

Baseline (0s): Mean-PnL = -0.401%

| Latenz | Δ Mean-PnL vs. Baseline | pro 60s |
|---|---|---|
| 60s | -0.577pp | -0.577pp/min |
| 120s | -0.908pp | -0.454pp/min |
| 300s | +0.202pp | +0.040pp/min |
| 600s | -0.043pp | -0.004pp/min |

## Interpretation
- **Entry-Drift** > 0 bedeutet: Preis bewegt sich im Schnitt nach oben nach Msg → Bot kauft höher → Edge schrumpft
- **Entry-Drift** < 0 bedeutet: Preis fällt nach Msg (typisch für manche Setups) → Bot bekommt besseren Preis
- **Mean-PnL-Decay** = echter monetärer Kosten der Latenz auf diesem Korpus

### Non-monotoner Verlauf — „Pop-and-Drop"-Pattern

| Latenz | Mean-PnL | Entry-Drift |
|---|---|---|
| 0s | -0.40% | 0% (baseline) |
| 60s | **-0.98%** 🔴 | -0.27% (Preis schon bissl tiefer?) |
| 120s | **-1.31%** 🔴 | -0.07% |
| 300s | **-0.20%** 🟢 | -1.09% (Pullback!) |
| 600s | -0.44% | +0.17% |

**Hypothese:** Jacks Posts triggern initial einen Spike (Frontrunner / Scalper), der sich bei 60-120s als „Pop-Top" zeigt (Bot kauft aufs Hoch). Bei 300s sind Frontrunner raus, Pullback begonnen → Bot kriegt besseren Preis. Bei 600s trifft wieder Normalisierung.

**Live-Relevanz:** Der Signal-Bot mit ~6-10s Latenz liegt im **günstigen** Bereich (nahe 0s). **GEFÄHRLICH** ist der 60-120s-Korridor — wenn Parser hängt oder IBKR retries braucht, landet man im schlechtesten Fill-Fenster.

**Schutzmaßnahme-Idee:** Wenn Order-Placement > 30s nach Msg → Option A (skip) oder Option B (Limit statt Market + aggressiver Offset, z.B. -0.5% unter Current).

## Live-Bot-Implikation
- Aktuelle Signal-Bot-Latenz: Telegram-Read ≤1s + Parser ≤3s + IBKR-Order ≤2s ≈ **6-10s total**
- 60s-Szenario ist quasi Worst-Case-Reality (wenn Parser lange Chain-Lookup macht)
- 120s+ nur bei systemischen Problemen (Network, Restart, etc.)

## Generalisierungs-Vorbehalt (REGEL 4)
- In-Sample n=83 — Aussage über Latenz-Decay gilt für Jack-Style-Setups, nicht universell
- Kein Halt/Liquidity-Modell — Penny-Stocks können bei Msg-Post bereits weg-gelaufen sein

## Verbindungen memory
- `project_staggered_entry.md`: Staffel-Entry löst Latenz-Problem aus anderer Richtung
- `project_order_offset_simulation.md`: verwandter Testcenter-Parameter
