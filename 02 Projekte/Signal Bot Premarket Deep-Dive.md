# Signal Bot — Premarket Deep-Dive

_Generiert: 2026-04-17T21:11:01.364714+00:00_

## Kontext — 22 Premarket-b-Verdicts mit 86% SL-Hit-Rate

Ursprungs-Finding: Time-of-Day-Analyse (`Signal Bot Time-of-Day.md`)
- Premarket (04:00-09:30 ET): 26.5% aller Buys
- Mean-PnL -1.31%, Winrate 14%, SL-Hit 19/22 = 86%

## Aggregat-Muster

**N Cases:** 22

### Ticker-Häufung

- `CETX`: 2
- `RANI`: 1
- `SCNX`: 1
- `BKYI`: 1
- `VSTM`: 1
- `BTBT`: 1
- `ELDN`: 1
- `AKBA`: 1
- `SOND`: 1
- `ENLV`: 1
- `AMBR`: 1
- `KTTA`: 1
- `DRCT`: 1
- `AHMA`: 1
- `BBAI`: 1
- `PLRZ`: 1
- `WHLR`: 1
- `TWG`: 1
- `BDRX`: 1
- `ALMS`: 1
- `LAES`: 1

### Stunden-Verteilung

- `04-06 (early_pm)`: 2
- `06-08 (mid_pm)`: 5
- `08-09:30 (late_pm)`: 15

### Premarket→RTH-Open Gap-Verhalten

- Avg Gap (Entry → RTH-Open): **-2.99%**
- Gap-Down (>-0.5%): 12/22
- Gap-Up (>+0.5%): 8/22
- Gap-Neutral: 2/22
- Daten fehlen: 0/22
- Avg RTH-First-30min Drawdown vs. Entry: **-12.69%**
- SL-Hit RTH-First-30min: **17/22 (77%)**

### Catalyst-Keywords im Msg-Text

Cases mit mind. 1 Catalyst-KW: 1/22 (5%)

- `news`: 1

## Einzel-Cases

| MsgID | Ticker | ET | Entry | PM-High | RTH-Open | Gap-% | RTH-1st-30m-Low | DD% | SL? | Catalysts | Snippet |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 3517 | RANI | 2025-10-17 08:50 | 1.31 | 1.55 | 1.37 | +4.58% | 1.20 | -8.40% | 🔴 | — | RANI I am going to take the risk and open a position around 1.18 With 1.05 SL And I will sell  most likely around the op |
| 3608 | SCNX | 2025-10-24 08:02 | 2.06 | 2.06 | 1.93 | -6.30% | 1.58 | -23.29% | 🔴 | — | SCNX  I am risking and adding some for possible intra day move at current price around 1.75 may add more if it drops to  |
| 3623 | BKYI | 2025-10-27 06:48 | 1.78 | 2.14 | 1.90 | +6.74% | 1.58 | -11.24% | 🔴 | — | BKYI 1.45 SL 1.36 Valid for 4 minutes |
| 3696 | VSTM | 2025-11-04 08:31 | 8.99 | 9.39 | 9.11 | +1.33% | 7.55 | -16.02% | 🔴 | — | Added some VSTM at 8.10  Placed another order at 8.40 if you are interested. Swing to long .  They got earning this morn |
| 3697 | BTBT | 2025-11-04 08:32 | 3.27 | 3.30 | 3.25 | -0.59% | 3.15 | -3.65% | 🔴 | — | Placed order at 2.93 for BTBT |
| 3712 | ELDN | 2025-11-07 09:03 | 1.96 | 2.13 | 2.00 | +2.06% | 1.86 | -5.08% | 🔴 | — | I placed an order at  ELDN  1.65 Might start a position around current price ( around 1.75 to 1.90) and add to it if it  |
| 3723 | AKBA | 2025-11-11 08:43 | 1.68 | 1.69 | 1.68 | +0.00% | 1.67 | -0.60% | — | — | AKBA I started an order at 1.62 1.55 1.49 SL 1.39 Valid till 12:00 PM US ET |
| 3772 | SOND | 2025-11-20 08:21 | 0.19 | 0.20 | 0.18 | -5.48% | 0.17 | -13.22% | 🔴 | — | SOND is moving with so far a good volume. I will go on and place an order at 0.1780 SL 0.1690 Valid for 10 minutes  To d |
| 3779 | ENLV | 2025-11-24 08:57 | 1.73 | 1.74 | 1.59 | -7.80% | 1.38 | -20.23% | 🔴 | — | ENLV is moving pre market  But I saw it got some warrants regardless . I may day trade it. Placed an order at  1.48 SL 1 |
| 3813 | AMBR | 2025-11-26 08:32 | 2.36 | 2.75 | 2.70 | +14.38% | 2.50 | +5.91% | — | — | AMBR got a good earning pre market  I placed an order at 2.18 valid for 4 minutes for a possible trade. |
| 3830 | KTTA | 2025-11-28 09:25 | 1.51 | 2.06 | 1.43 | -5.63% | 1.37 | -9.27% | 🔴 | — | KTTA Got multiple levels of volatility. Placed an order at 1.14 valid for 4 minutes will cancel automatically before the |
| 3841 | DRCT | 2025-12-01 07:10 | 10.25 | 10.63 | 9.87 | -3.70% | 8.16 | -20.34% | 🔴 | — | Moving my attention to DRCT Not the best volume yet but the stock is seeing some volatility pre market . Placed an order |
| 3845 | AHMA | 2025-12-01 09:07 | 11.93 | 12.86 | 10.55 | -11.57% | 9.49 | -20.45% | 🔴 | — | Placed an order at AHMA at  9.88 Will keep it open for 12 minutes. |
| 3846 | BBAI | 2025-12-01 09:18 | 6.12 | 6.20 | 6.14 | +0.33% | 6.00 | -1.96% | — | — | Placed an order at  5.77 for BBAI valid for one hour . For swing . |
| 3871 | PLRZ | 2025-12-02 09:12 | 6.76 | 7.35 | 6.97 | +3.11% | 6.23 | -7.84% | 🔴 | — | PLRZ placed an order at  5.93 Valid for 5 minutes only. |
| 3922 | WHLR | 2025-12-05 08:56 | 19.77 | 20.55 | 16.98 | -14.11% | 16.23 | -17.91% | 🔴 | — | Placed an order at 5.92  for WHLR Valid for 6 minutes only . |
| 3954 | CETX | 2025-12-08 05:36 | 7.15 | 20.56 | 8.13 | +13.71% | 7.11 | -0.56% | — | news | CETX Another mover pre market no news . Super low float. Might be a good one for day trade. I placed an order pre market |
| 3959 | CETX | 2025-12-08 05:51 | 11.09 | 20.56 | 8.13 | -26.69% | 7.11 | -35.89% | 🔴 | — | CETX placed an order at  9.66 Valid for 8 minutes |
| 3963 | TWG | 2025-12-08 06:36 | 10.94 | 11.15 | 9.51 | -13.07% | 8.62 | -21.21% | 🔴 | — | TWG placed me an order at 9.93 Valid for 9 minutes. For day trade.  CETX  I will be careful here waiting till it settles |
| 3964 | BDRX | 2025-12-08 06:57 | 65.90 | 65.95 | 36.25 | -44.99% | 35.00 | -46.89% | 🔴 | — | BDRX Another low float mover pre market today. I honestly will be careful with those type of moves but if you trade them |
| 4365 | ALMS | 2026-01-06 07:50 | 17.02 | 19.16 | 22.20 | +30.43% | 18.51 | +8.75% | — | — | ALMS got new pre market . The price moved to almost 18 plus . I placed me an order at 15.75 for any quick trade pre mark |
| 5409 | LAES | 2026-03-16 08:35 | 3.64 | 3.77 | 3.55 | -2.47% | 3.28 | -9.89% | 🔴 | — | LAES is dropping pre market  I might add some for intra day trade and over night swing if it gets my order at 3.18~3.32  |

## Pattern-Interpretation

**Gap-Down dominiert** — Premarket-Hoch wird nach RTH-Open abverkauft. Pop-Top-Pattern.

**Avg Drawdown RTH-First-30min:** -12.69% — d.h. im Schnitt fällt der Kurs nach Entry um diesen Betrag bevor er sich erholt.

### Treiber-Hypothesen
- **Dominanz SL-Hits in RTH-First-30min:** Pattern ist entry-zu-high, RTH-Drop, SL-getriggert. H10a (Hard-Skip) würde das vollständig adressieren.
- **Gap-Down-Häufung:** H10c (Wait-for-RTH) wäre ideal — Bot würde beim RTH-Open-Gap-Down niedriger einsteigen.

## Empfehlung für Phase-C-Testcenter-Sweep

1. **H10a (Hard-Skip) als Default-Kandidat** — Evidenz stark, False-Skip-Rate niedrig (nur 3/22 Winners)
2. **H10c (Wait-for-RTH)** als Alternative wenn Gap-Down-Rate dominiert
3. **H10d (Premarket-VWAP-Limit)** wenn RTH-Gap-Risiko gemindert werden soll
4. **Frühe Premarket (04-06 ET)** braucht separates Handling wegen dünner Bars
5. **Biotech-Filter kombiniert:** wenn Ticker Biotech-Cluster UND Premarket → immer Skip

## Generalisierungs-Vorbehalt
- n=22, nur In-Sample
- Walk-Forward-Split (2025-Q4 Train / 2026-Q1 Test) PFLICHT vor Default-Change
- Biotech-Bias: Jack ist Biotech-lastig → Out-of-Market-Transfer unklar
