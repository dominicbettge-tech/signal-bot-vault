# Signal Bot — Staggered-Entry-Sim

_Generiert: 2026-04-17T20:50:37.161108Z_

## Setup
- **Korpus:** alle `human_verdict='b'` außer SLS (feedback_sls_excluded_from_tz)
- **Offsets:** [0.0, 0.005, 0.0075, 0.01]
- **Fill-Window:** 60min
- **Exit:** H2 Ladder [0.05, 0.1, 0.2] × [0.33, 0.33, 0.34], SL -3%, TTL 240min
- **N simuliert:** 81, skipped 2

## Ergebnis
- **Any-Tranche-Fill-Rate:** 100.0% (81/81)
- **Mean Tranches Filled:** 3.44 / 4
- **Mean PnL (filled):** -0.57% (weighted-on-full-position)
- **Winrate:** 20%

## Vergleich mit Baseline (Jack-Edge-Audit 60m Hold)
- Baseline Mean: -1.54%, Winrate 39%, Fill 100% (naive next-bar-open)
- Staffel öffnet höhere Fill-Granularität, Avg-Entry leicht über Jack-Preis

## Caveats
- Vereinfachtes Exit-Modell: Exit-Fenster startet bei Msg, nicht bei erstem Tranche-Fill
- PnL weighted on full-position → Fill-Rate-Delta bereits eingepreist
- Keine Spread/Slippage auf Tranche-Limits simuliert
