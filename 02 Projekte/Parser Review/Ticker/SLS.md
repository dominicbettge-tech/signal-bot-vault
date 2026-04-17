# SLS — Parser Review

**Status:** ✅ Review abgeschlossen 2026-04-17 · 120/120 (100%) · 777 Verdicts in DB (gesamt Review-Korpus 27.5%)
**⚠️ Scope-Ausschluss 2026-04-17:** SLS komplett RAUS aus Testcenter/Signal-Bot-Hauptlinie. Daten bleiben ausschließlich für **separates Chart-Pattern-Learner-Extra-Projekt** verfügbar. Siehe `feedback_sls_excluded_from_tz.md`.
**⚠️ Parser-Miss entdeckt:** +52 SLS-Messages mit ticker=NULL (siehe `project_parser_ticker_miss_fix.md`) — Backfill nach Review-Abschluss, dann 172 total
**Span:** 2025-10-14 → 2026-04-09 (≈6 Monate, 53 Sessions)
**Pre-Review (vor 2026-04-17):** 10 Messages Okt–Dez 2025 bereits verdict-getagged (nicht in dieser Runde)

## Review-Tabellen

### Session 2025-12-22 bis 2026-01-09 (7 Messages)

| # | msg_id | ET | Jack-Text (EN) | Verdict | Begründung |
|---|---|---|---|---|---|
| 1 | 4214 | 22.12.25 11:35 | SLS. If you remember adding zone shared here few weeks ago was 1.45 and below we got that. 85% profit since then. It is up to you where you want to secure profit in those biotech. I always calculate my risk before any reward regardless! Enjoy. | **n** | Rückblick-Brag, keine neue Order |
| 2 | 4327 | 31.12.25 12:29 | *siehe [A]* | **w** | Analyse + Hold-Empfehlung + Resistance $3.99, kein Entry-Trigger |
| 3 | 4363 | 05.01.26 21:49 | My great team here my post here about SLS when it was still below 4 !!! Got to 5 plus just only from this one …. And remember I started covering it here when it was below 1.45 ✅✅! Enjoy ✅ | **n** | Post-hoc-Jubel |
| 4 | 4427 | 08.01.26 12:42 | *siehe [B]* | **w** | Multi-Level-Analyse + bedingter Trigger "close above 4" + Catalyst-Erwähnung |
| 5 | 4441 | 09.01.26 09:25 | Pre market action broke 3.73 support. The volume lower than yesterday average so far by 6%. | **n** | Reines Price-Update |
| 6 | 4444 | 09.01.26 09:59 | We are at that 3.35 lines I talked about yesterday… | **n** | Status-Confirm |
| 7 | 4446 | 09.01.26 11:18 | I wish everyone here to read it again!!! | **n** | Chatter |

### Session 2026-01-12 (2 Messages)

| # | msg_id | ET | Jack-Text (EN) | Verdict | Begründung |
|---|---|---|---|---|---|
| 8 | 4474 | 12.01.26 16:13 | Did you see those levels mentioned here team | **n** | Rückfrage/Chatter, kein Trigger |
| 9 | 4475 | 12.01.26 16:14 | SLS last week tested the 30 days support around 3.30 to 3.20 as mentioned previously and today it is trying to reverse | **n** | Status-Confirm auf alte Analyse, keine neue Order |

### Session 2026-02-08 bis 2026-02-13 (15 Messages) — mit Chain-Markern

| # | msg_id | ET | Jack-Text | Verdict | Chain | Begründung |
|---|---|---|---|---|---|---|
| 10 | 28 | 08.02. 21:55 | SELLAS will get an update every day ! | **n** | — | Meta-Ankündigung |
| 11 | 36 | 09.02. 01:42 | *[Yahoo 1D, $3.73 Close, $3.86 Overnight]* | **n** | — | Sonntag-Preis-Ping, isoliert, no-overlay |
| 12 | 55 | 09.02. 17:47 | *[StockMaster 1M, Close $3.705]* | **n** | **C1-start** | Chart-Dump 1/3, no-overlay |
| 13 | 56 | 09.02. 17:48 | *[StockMaster 3M, ATH $5.18 → $3.70]* | **n** | → #55 | Chart-Dump 2/3 |
| 14 | 57 | 09.02. 17:48 | *[StockMaster 6M, +131.88%]* | **n** | → #55 | Chart-Dump 3/3 |
| 15 | 70 | 09.02. 21:10 | SLIGHT Bullish end of the day close so far in SLS | **n** | → #55-57 | EOD-Status zum Chart-Set |
| 16 | 75 | 10.02. 02:54 | Let us see what tomorrow will bring in SLS . I am working on the new chart prediction for it! | **n** | **C2-start** | Teaser → liefert in #85 |
| 17 | 85 | 10.02. 15:18 | Most recent SLS chart update. Weekly resistance at 4.20 Weekly support at 3.62~3.66 All mentioned in the chart! | **w** | → #75 | Angekündigte Level-Analyse geliefert |
| 18 | 107 | 11.02. 01:48 | Open interest options for SLS is still too high compared to similar market cap and industry rivals! | **n** | — | Eigenständige Seitenbemerkung |
| 19 | 116 | 11.02. 15:21 | Touched below the weekly support then barely back above it! No add still for me | **n** | → #85 | Support-Retest + expliziter No-Add |
| 20 | 124 | 11.02. 19:22 | Last chart updat Support levels still as mentioned in my previous message! So far we tested the weekly support and bounce little of it! | **n** | → #85, #116 | Level-Confirm |
| 21 | 131 | 11.02. 22:27 | I opened an order valid till tomorrow pre market so far for SLS! Will cancel most likely if no fill in the pre market tomorrow! | **n** | **C4-start** | Buy-Announcement OHNE Preis → per Regel `feedback_buy_without_price_equals_n.md` = n. Retro-Resolve via #157 @$3.45, no-fill |
| 22 | 156 | 12.02. 22:50 | *[StockMaster 1M, Close $3.55, Low $3.46]* | **n** | **C5-start** | Chart-Paar zu #157, no-overlay |
| 23 | 157 | 12.02. 22:52 | *siehe [C]* | **w** | → #131, #156 | Retro-Preis-Disclosure $3.45 + neues Weekly-Support $3.41–3.47 |
| 24 | 165 | 13.02. 14:49 | SLS needs to close above 3.60 otherwise it may head into testing below 3.40 support lines . | **w** | → #157 | Conditional-Level (close>3.60 else test<3.40) |

**[C] #157 (12.02.26 22:52 ET):**
> SLS today we saw the low was 3.46 my last night order at 3.45 went with no fill ( so unlucky but also too accurate close to that low)
> The new support stands now around 3.41~3.47 for the weekly but we will know more tomorrow!
> Overall today market put a big pressure in multiple stocks!
> But honestly a lot of BIOTECH stocks did fine!

**Chain-Cluster-Summary Session 2:**
- **C1** #55/56/57 → #70: Multi-Timeframe-Chart-Dump gefolgt von EOD-Status
- **C2** #75 → #85: Teaser-to-Delivery (angekündigter Level-Report)
- **C3** #85 → #116 → #124: Support-Retest-Verlauf über 28h
- **C4** #131 → #157: Order-ohne-Preis → Retro-Preis-Disclosure $3.45, no-fill
- **C5** #156 → #157: Chart-Text-Paar binnen 2 Min
- **C6** #157 → #165: Support-Levels ins Next-Day-Conditional übernommen

**Counterfactual-Sim #131 (Entry @ Last Close $3.67, H2-Ladder +5/+10/+20, SL −3%):**
- Feb 12 RTH: High $3.6884 (kein TP), Low $3.46 → **SL getroffen, PnL −3.00%**
- Ergebnis: Last-Close-Heuristik für Buy-ohne-Preis = unprofitabel (konfirmiert auf 2 sauber vergleichbaren Cases: Mean −1.66%)

### Session 2026-02-13 bis 2026-02-24 (20 Messages) — mit Chain-Markern

| # | msg_id | ET | Jack-Text | Verdict | Chain | Begründung |
|---|---|---|---|---|---|---|
| 25 | 166 | 13.02. 15:00 | *siehe [D]* | **w** | → #165 | Multi-Level-Analyse: Support 3.24-3.39, Reversal-Window 3.60-3.66, Volumen-Warnung |
| 26 | 177 | 13.02. 19:12 | Let us see that reverse above 3.64 so far is happening | **n** | → #166 | Status-Confirm gegen Reversal-Zone |
| 27 | 181 | 14.02. 03:21 | *siehe [E]* | **w** | → #166 | Conditional: 3.34-3.46 hold / 3.80 break → 4.10-4.12 / REGAL 2-Wochen |
| 28 | 200 | 17.02. 16:32 | *[StockMaster 1M Feb 17, Close $3.715, −9.49%]* | **n** | — | No-overlay Kontext |
| 29 | 220 | 18.02. 16:31 | *[StockMaster 1M Feb 18, Close $3.795, +9.68%]* | **n** | **C10** | No-overlay |
| 30 | 222 | 18.02. 16:32 | *[identisch zu #220]* | **n** | → #220 | Duplikat 36 Sek später |
| 31 | 228 | 18.02. 21:49 | *[StockMaster 1M Feb 18 spät, Close $3.79]* | **n** | → #220 | Abend-Update |
| 32 | 230 | 18.02. 21:49 | Check the chart here | **n** | → #228 | Pointer-Chatter auf #228 |
| 33 | 231 | 18.02. 21:49 | And here ✅✅ | **n** | → #230 | Chatter-Echo |
| 34 | 241 | 19.02. 15:56 | SLS Crossing the board again above 4 ✅✅! | **n** | → #181 | Brag („above 4" aus #181 getriggert) |
| 35 | 246 | 19.02. 22:35 | *[StockMaster 1M Feb 19, Close $4.04, H $4.23, +22.25%]* | **n** | **C13** | No-overlay Breakout |
| 36 | 247 | 19.02. 22:35 | *[StockMaster 3M Feb 19, +158.97%]* | **n** | → #246 | 3M-Kontext 6 Sek später |
| 37 | 256 | 20.02. 15:50 | *[StockMaster 1M Feb 20, Close $4.25]* | **n** | **C14** | No-overlay Continuation |
| 38 | 257 | 20.02. 15:50 | SLS chart 📊 all came in real time as prescribed and predicted so far ✅✅ | **n** | → #256 | Self-Brag |
| 39 | 269 | 23.02. 03:31 | Good evening my incredible team here! Some overnight price actions . Let's us see what next week will bring! | **n** | — | Greeting |
| 40 | 276 | 23.02. 16:04 | SLS strong momentum ✅ | **n** | — | Status-Update |
| 41 | 285 | 23.02. 19:20 | *[StockMaster 1M Feb 23, Close $4.635, H $4.80, +39.31%]* | **n** | **C15** | Stärkste Bewegung seit Tief |
| 42 | 288 | 24.02. 00:49 | 90 days is telling some more about SELLAS move . | **n** | — | Teaser vor Analyse |
| 43 | 292 | 24.02. 02:44 | *[Yahoo 1D Feb 23, Close $4.44, Overnight $4.50 +8.43%]* | **n** | → #288 | Overnight bullish |
| 44 | 294 | 24.02. 02:45 | *siehe [F]* | **w** | → #288, #292 | Dual-Ticker (SLS+IBRX) + Open-Interest/Short-Interest-Watch |

**[D] #166 (13.02.26 15:00 ET):**
> SELLAS most updated chart
> 3.24~3.39 critical support line for both 30/60 days.
> If no reversal above 3.60~3.66 today we still have a chance next week on Tuesday but the volume is getting lower than last two weeks average!

**[E] #181 (14.02.26 03:21 ET):**
> SLS got a tricky chart 📊 status as of now .
> Next week especially Thursday will decide a lot of it .
> 3.34~3.46 needs to stay strong otherwise I can see a possible down trend towards 3 level. If it can break above 3.80 next week then 4.10 to 4.12 can be next . So far no update or any news about REGAL but we might hear something in two weeks!

**[F] #294 (24.02.26 02:45 ET):**
> Overnight action for both SLS and IBRX!
> I will pay attention to SLS price action this week team .
> From looking at the open interest for options and the short interest this week we might get more price action in it

**Chain-Cluster-Summary Session 3:** C7 #166→#177→#241 (Reversal-Prediction → Confirm → above-4-Break), C10 #220→#222→#228 (Same-Day-Updates), C12 #228→#230→#231 (Chart+Pointer-Chatter), C13 #246→#247, C14 #256→#257, C15 #285→#288→#292→#294.

**⚠️ Parser-Miss entdeckt während Session 3:** 52 weitere SLS-bezogene Messages mit ticker=NULL im Korpus. Davon identifiziert:
- **#154** (12.02. 17:09) „3.45 SLS order It got to 3.46 are you kidding me!!" — **frühere Retro-Disclosure zu #131** (18h40 nach Order, vor #157!)
- **#229** (18.02. 21:49) „SLS same as my previous chart no change. Hold zone" — Chain-Status nach #228
- **#232** (18.02. 21:51) „weekly support above 3.44~3.54 still intact" — Chain-implicit
- **#248** (19.02. 22:37) „30/90 days in SLS got better today. Support 3.47~3.62. closes above 4.20 bullish" — Major Level-Analyse
- **#286** (23.02. 19:22) „broke few resistances. Major resistances 4.80~4.95" — Level-Analyse
- Weitere 47 Messages inkl. #48, #54, #58, #95, #104, #108, #113, #117, #221, #240, #274, #3471, #3472, #3477, #3482, #3495, #3672, #3679, #3767, #3950, #4069, #4076, #4151, #4271, #4367, #4403 u.a.
- Backfill-Plan: `/root/obsidian_vault/02 Projekte/Parser Ticker-Miss-Fix — Implementierungsplan.md` (deferred bis Review-Komplettierung)

**[A] #4327 (31.12.25 12:29 ET):**
> SLS and only here. I want to share my most recent view! Only my personal opinion so far and as anything I share nothing to be considered as a financial advice (already shared full pinned disclaimer here you can read it in the pin message)! But SLS got a good monthly chart so far! RSI keeps putting pressure into the price basis. As long as no brutal offer or dilution I think it still a good hold. The 52 high at 3.99 so far is the resistance. Closing above 3.50 today will be a fine end for this great year 2025 in it. Remember I shared SLS here too many times and last official buy it was below 1.45 and in my emails. Enjoy my incredible team and I am seeing more great trades ahead in 2026 for us!

**[B] #4427 (08.01.26 12:42 ET):**
> An update about SLS since a lot in this group still looking it or maybe hold some: So far the RSI is cooling down but we can tell from the volume trend it may still under pressure sell for the rest of this week. The 30 days support around 3.25 to 3.35 is a major important line. If it breaks below that it may be a bearish sign for the short term. 3.73 to 3.78 a support line for the 10 days but it is not too strong it may visit that again and reverse above 3.90. If it closes above 4 today it could trigger a short run. If the company announces any more info about REGAL Phase 3 it also may be the near term catalyst but no one knows when. I will start share my regular updates in the private special group for biotech stocks that I will create next week. I don't want also to mix stuff this group is mainly for day and swing trades.

## Diskussion (2026-04-17)

Keine strukturierten Entries bisher — Session startet mit pure Analysis/Rückblick-Messages. Noch keine b/e/x-Verdicts in dieser Serie.

## Bot-Relevanz / Parser-Regeln

- **Catalyst-Erwähnung #4427:** „REGAL Phase 3 catalyst" — Jack gibt FDA-Katalysator als Nebenbemerkung bekannt. Parser sollte Keyword-Flag `pending_catalyst` setzen, wenn Phase-2/3/FDA-Muster im Text — Input für Biotech-Blackout-Regel.
- **Multi-Level-Support #4427:** Jack gibt 4 Levels (3.25-3.35, 3.73-3.78, 3.90, 4.00). Parser-Range-Extraction (H9 Phase 1) muss Multi-Level erfassen, nicht nur Single-Range.
- **Bedingter Entry-Trigger #4427:** „If it closes above 4 today it could trigger a short run" → Conditional-Setup (gleiches Muster wie NCPL #4008). Als Chain-Marker für Folgemessages.
- **Buy-ohne-Preis #131 (R-Regel-Kandidat „Chain-Price-Resolver"):** Jack postet „I opened an order" ohne $-Wert. Parser-Lücke: Preis erst 26h später via #157 retro disclosed. Counterfactual-Sim (Entry @ Last Close + H2-Ladder) zeigt −3.00% SL-Hit für SLS (und Mean −1.66% auf 2 cleanly-simulable Cases im Korpus) → Last-Close-Heuristik unprofitabel. Sauberer Pfad: **30-Min-Chain-Resolver** auf Parent-Message, sonst **n**. Siehe `feedback_buy_without_price_equals_n.md`.
- **Chart-Chain-Anchoring:** Jack postet Multi-Timeframe-Charts (1M/3M/6M) vor textlichen Level-Analysen (C1: #55-57 → #70/#85, C5: #156 → #157). Parser sollte `chart_preceded_by_N_minutes` setzen und Text-Soft-Score leicht erhöhen, wenn binnen ≤180 Min ein Chart-Paket kam.
- **No-Overlay-Chart-Priorisierung:** 5/5 Charts in Session 2 sind reine Broker-Screenshots (Yahoo, StockMaster), keine Jack-Zeichnungen. OCR-Budget sollte auf Charts mit Jack-Overlay fokussieren, nicht auf reine Broker-Dumps.

## Offene Punkte

- **Post-Review-TODO:** 52 ticker=NULL SLS-Messages reviewen nach Backfill (Plan: `Parser Ticker-Miss-Fix — Implementierungsplan.md`)

---

## ⭐ Final-Analyse (2026-04-17 Review-Abschluss)

### Verdict-Verteilung (120 Messages)
| Verdict | Count | % | Bedeutung |
|---|---|---|---|
| **n** (Noise) | 93 | 77.5% | Status/Self-Praise/Post-hoc/Celebration |
| **w** (Watch/Zone-Setup) | 24 | 20.0% | Chart-Zonen, Conditional, Watchlist |
| **s** (Status-Adjust) | 2 | 1.7% | Trade-Parameter-Änderung |
| **e** (Exit-Signal) | 1 | 0.8% | Exit-Indikator |
| **b** (Buy) | **0** | **0%** | **KEINE direkten Buy-Signale im Text** |

### Kern-Erkenntnis (User-Direktive 2026-04-17)
> *„SLS nicht wirklich tradebar außer die charts"*

SLS mit **Text-Only-Parser ist nicht profitabel** — 0 Text-basierte Buy-Signale auf 120 Messages. **Wert entsteht nur via:**
1. **Chart-Pattern-Learner** (siehe `project_chart_pattern_learner.md`) — 24 w-Verdicts sind Zone/Chart-Setups
2. **Zone-Trade-Extractor** (siehe `project_parser_zone_trade_extractor.md`) — Range+Timeframe+Conditional aus Text extrahieren
3. **Counterfactual-Sim (5 Sessions, H2+hi+)** = +5.58% Bankroll → Hypothese, n=5 zu klein für Default

### Parser-Lücken-Highlights aus SLS
- **L1 (Range-Extractor):** 8+ klare Range-Cases (#429 `4.71~4.8`, #548 `5.01~5.05`, #600 `5.60~5.80`+`4.79~4.90`, #693 `4.01~4.03`+`4.60~4.85`, #685 `3.90~3.95`)
- **L2 (Timeframe-Tag):** explizite TF-Labels in allen Prime-Cases (weekly, monthly, 15 days, 30 days, 90 days)
- **L3 (Conditional):** #466 „if breaks up / retreats below 5.50", #665 „below 4 might trigger SL", #713 „if closes above 5.10"
- **L4 (Watchlist-Staging):** fast alle w-Verdicts sind WATCHLIST_INTENT ohne sofortigen Entry → Zone persistieren, Trigger später
- **L5 (Chain-Range-Inheritance):** #545 „This one so far still valid" — Chain-Ref ohne Preis, braucht 30-Min-Window-Inheritance

### Chart-Pattern-Learner-Trainingsdaten aus SLS
- **43 Chart-Images** (alle StockMaster-Auto, keine Jack-Overlays) — rohe Trainingsdaten
- **24 w-Verdicts** mit Zone-Kontext — Labels für Pattern→Trade-Mapping
- **Polygon bars_daily** (197 bars, 2025-07-01 → 2026-04-13) — Outcome-Labels (MFE/MAE/Fill)

### Nächste Ticker für Cross-Ticker-Generalisierung
IBRX → OCGN → ACRV → RCKT (Biotech-Peers mit vergleichbarer Volatilität, nötig für Gate 2 der 7-Gate-Pipeline)
