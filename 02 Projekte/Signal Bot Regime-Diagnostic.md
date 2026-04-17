# Signal Bot — Regime-Diagnostic (Walk-Forward vs. SPY)

_Generiert: 2026-04-17T21:26:11.537720_

**Frage:** Ist die eine positive Walk-Forward-Fold (Survival-Check Combined-Filter) ein Bull-Regime-Artefakt?

**Methodik:** Für jede Fold-Test-Window SPY-Close-to-Close-Return berechnen.
Regime-Klassifikation: BULL (>+2%), FLAT (-2% bis +2%), BEAR (<-2%)

## S0_Baseline — Ladder `H2_base` (n=83)

| Fold | Test-Window | n_test | Fold-Mean-PnL | SPY-Return | Regime |
|---|---|---|---|---|---|
| 0 | 2025-11-24 → 2025-12-08 | 33 | -0.42% | SPY +2.23% | **BULL** |
| 1 | 2025-12-08 → 2025-12-22 | 3 | -2.12% | SPY +0.18% | **FLAT** |
| 2 | 2025-12-22 → 2026-01-05 | 3 | +2.92% | SPY +0.42% | **FLAT** |
| 3 | 2026-01-05 → 2026-01-19 | 3 | -1.77% | SPY +0.57% | **FLAT** |

## S3_S2+User_Ladder — Ladder `user_3_7_15` (n=56)

| Fold | Test-Window | n_test | Fold-Mean-PnL | SPY-Return | Regime |
|---|---|---|---|---|---|
| 0 | 2025-11-24 → 2025-12-08 | 21 | -0.40% | SPY +2.23% | **BULL** |
| 1 | 2025-12-08 → 2025-12-22 | 3 | -1.24% | SPY +0.18% | **FLAT** |
| 2 | 2025-12-22 → 2026-01-05 | 3 | +1.80% | SPY +0.42% | **FLAT** |
| 3 | 2026-01-05 → 2026-01-19 | 2 | -1.15% | SPY +0.57% | **FLAT** |

## Korpus-Regime-Verteilung (pro Trade)

Jeder Trade wird mit SPY-20-Tage-Return bis zum Message-Datum klassifiziert.

| Regime | n Trades | Mean-PnL (H2_base) |
|---|---|---|
| BULL | 24 | -1.05% |
| FLAT | 53 | +0.10% |
| BEAR | 6 | -1.77% |
| n/a | 0 | +0.00% |

## Interpretation (auto-generiert)

- **BULL** Mean: -1.05% (n=24)
- **FLAT** Mean: +0.10% (n=53)
- **BEAR** Mean: -1.77% (n=6)

**Befund:** FLAT ist das beste Regime — Jacks Low-Cap-Setups
generalisieren NICHT auf Broad-Market-Richtung. Vermutliche Ursache:
Jacks Edge haengt an idiosynkratischen Catalysts/News, die in Bull/Bear-Phasen
von Broad-Market-Flow ueberschattet werden (Bull: Mega-Cap-Rotation, Bear: Flight-to-Quality).

**Walk-Forward-Folds:** Nur eine Fold positiv (+2.92%), aber sie lag in FLAT-Regime
genauso wie zwei andere negative Folds (-2.12%, -1.77%). → Kein regime-lineares Signal,
sondern Noise innerhalb FLAT. Die positive Fold war statistischer Zufall, nicht Strategie-Edge.

**Konsequenz:** Kein Bull/Bear-Filter als Default-Kandidat.
Regime-Gate würde FLAT-Trades (n=53, +0.10%) nicht gegenüber BULL (n=24, -1.05%) filtern
ohne deutlich kleineren Korpus zu haben. Erst bei n>=30 pro Regime re-testen.

## Vorbehalt
- SPY-20d-Return ist grobe Proxy, ignoriert Volatility-Regime (VIX) + Sektor-Rotation
- Nur 4 Fold-Test-Windows → unter der Replikations-Schwelle n≥10
- Regime-Klassifikation mit ±2% Threshold willkürlich, keine Empirie hinter Zahl

