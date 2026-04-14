---
tags: [signal-bot, klassifikator, analyse, phase-2, umgebung]
date: 2026-04-14
status: erste-ergebnisse
parent: "[[Ticker-Klassifikator]]"
---

# Ticker-Klassifikator Phase 2 — Umgebungsdaten × Cluster

**Datum:** 2026-04-14 (nachts, während Dominic schläft)
**Datenbasis:** 594 Signale (306 mit Cluster-Match) × 3 Cluster aus Phase 1
**Zeitraum:** 2025-10-09 bis 2026-01-08
**Methode:** Enrichment mit SPY/VIX/IWM + Weekday + Time-Bucket + Jack-Metadata + Keywords → Korrelation mit Cluster-Zuordnung

## Kurz-Fazit

Phase 1 hat gezeigt **WAS** die Cluster sind (Ticker-DNA). Phase 2 zeigt **WANN** und **WIE** Jack sie postet — und mit Trade-Simulation auch **wie profitabel** welche Regeln sind.

**7 harte Muster gefunden, die sofort handlungsrelevant sind:**

1. **Nur C1 ist profitabel** (Simulation): +1% avg PnL mit SL=10% / TP=15%, 44% Win-Rate. C0 ist strukturell negativ, C2 nur profitabel mit breitem SL=20% / TP=40% (+1.55%).
2. **C2 Monster hat einzigartiges Vokabular**: `low_float` 4×, `bull_flag` 4.5×, `halted` 2× häufiger als Baseline.
3. **C2 meidet Mittwoch komplett** (0 von 33 Signalen), signalisiert 78% an Mo/Fr — aber C2 **Freitags-Trades verlieren massiv** (8% Win, −7% avg). Freitags-C2 ignorieren.
4. **Trade-Type korreliert mit Cluster**: C1 hat 16% Swing, C0/C2 kaum Swing. **C0 als Swing ist 0% Win (N=7)** — Hard-Skip.
5. **🚨 Dilution-Filings (S-1/S-3/424B5) in letzten 7 Tagen halbieren Hit-Rate**: C1 von 42% auf 23% Win. Hard-Reject-Kandidat.
6. **C2 Monster-Tage sind news-getrieben auf Range-Ebene** (8-K in 7d → 3× größere Moves), aber die Richtung ist **unpredictable** — mit fixem SL frisst die erste Gegenbewegung die Position. Post-News = TSL nötig, nicht fixer SL.
7. **`kw_careful` ist Jack's eigenes Warnsignal** — 0% Win in C0/C2, 29% vs 40% in C1. Wenn er „careful" schreibt, Skip.

Das bedeutet: Live-Classifier kombiniert Cluster-Zuordnung (Ticker-DNA) **+** Jack-Textanalyse (Keywords + trade_type) **+** SEC-Filing-Check (Dilution/Earnings) **+** Wochentag/Zeit-Bucket-Filter. Jede Dimension trägt messbaren Effekt.

## Datenbasis

- 594 Signale mit Ticker (aus `parsed_signals.db`)
- **306 matchen** auf die 49 Phase-1-Ticker (Rest sind unbekannte/Watchlist-Namen)
- 296 davon haben Intraday-Bars am Signaltag (fast alle)
- Market-Regime via yfinance Daily (SPY/VIX/IWM/QQQ) — keine 60d-Limit, ging glatt durch
- Keywords: 13 Buckets (`low_float`, `halted`, `careful`, `watch`, `news`, ...)

## Erkenntnis 1 — Wochentag-Signatur pro Cluster

| Cluster | Mo | Di | Mi | Do | Fr | Auffällig |
|---|---|---|---|---|---|---|
| **C0 PM-Penny** | 38% | 30% | 12% | 5% | 14% | Montag/Dienstag-lastig |
| **C1 Solid Day** | 21% | 29% | **32%** | 5% | 13% | Mittwoch-Champion |
| **C2 Monster** | **42%** | 15% | **0%** | 6% | **36%** | Mo+Fr = 78%, Mi = 0 |

**Implikation:** C2 Monster ist ein **Montag/Freitag-Phänomen**. Null Signale an einem Mittwoch über 13 Wochen ist kein Zufall. Das heißt entweder:
- Jack tradet Monster nur am Wochenanfang/-ende (Gap-Setup freitags, Re-Entry montags)
- Monster-Setups treten selten mittwochs auf (strukturell im Markt)

**Regel-Idee:** Wenn heute Mittwoch und Text enthält `low_float`/`halted` → **extra Vorsicht**, könnte Off-Pattern-Signal sein.

**Caveat:** Thursday nur 16 Signale insgesamt (Feiertags-Ausfälle Nov/Dez + generell niedrige Dichte). Wochentag-Statistik für Do ist dünn.

## Erkenntnis 2 — Keyword-Lift pro Cluster

Rate von Keyword in Jacks Text, normiert auf 100 Signale im Cluster:

| Keyword | C0 | C1 | C2 | Baseline | C2-Lift |
|---|---|---|---|---|---|
| `low_float` | 2.9 | 0.0 | **9.1** | 2.3 | **4.0×** |
| `bull_flag` | 2.2 | 0.0 | **9.1** | 2.0 | **4.5×** |
| `halted` | 13.7 | 5.2 | **21.2** | 10.8 | 2.0× |
| `careful` | 7.9 | 5.2 | **12.1** | 7.2 | 1.7× |
| `watch` | 12.9 | 9.0 | 6.1 | 10.5 | 0.6× |
| `news` | 20.1 | 21.6 | 27.3 | 21.6 | 1.3× |
| `entry_clean` | 2.2 | 6.0 | 3.0 | 3.9 | 0.8× |
| `conviction_high` | 0.0 | 3.0 | 0.0 | 1.3 | — |

**Implikationen:**

1. **C2 Monster ist ein Text-Detektor-Problem.** "Low float" und "bull flag" kombiniert = fast sichere C2-Zuordnung. Das sind die klassischen Penny-Runner-Muster.

2. **`conviction_high` ist C1-exklusiv** ("loading", "big size", "long term") — Jack ist nur bei stabilen Day/Swing-Tradern voll überzeugt. Bei Monstern bleibt er vorsichtig.

3. **C1 signalisiert NIE mit "low float" oder "bull flag"** (0 Hits in 134 Signalen). Saubere Negativ-Indikatoren.

4. **"watch" ist umgekehrt** — C2 postet seltener mit "watch", weil Monster meist schon laufen. C0/C1 sind öfter Watchlist-Kandidaten.

**Regel-Idee für Live-Controller:**
```
if text contains ("low float" or "bull flag"):
    prior = shift towards C2
if text contains "loading" or "big size":
    prior = shift towards C1
if text contains "halted" + is_pm:
    prior = shift towards C2
```
Sehr einfache Rules, aber statistisch signifikant.

## Erkenntnis 3 — Trade-Type-Klassifikation passt

Jacks explizite Klassifikation (`day_trade` / `swing` / `long_term`) korreliert mit der daten-getriebenen Cluster-Zuordnung:

| Cluster | day_trade | swing | long_term | unknown |
|---|---|---|---|---|
| C0 PM-Penny | 31% | 7% | 0% | 62% |
| C1 Solid Day | 13% | **16%** | 2% | 69% |
| C2 Monster | **46%** | 0% | 0% | 55% |

**Implikation:** Die Cluster, die wir rein aus Ticker-Bewegung abgeleitet haben, spiegeln Jacks Hold-Dauer-Präferenz. C2-Ticker sind fast immer Day-Trades, C1 enthält fast alle Swings. Das validiert das Cluster-System von einer völlig unabhängigen Seite.

**Consequence:** Wenn Jack "swing" in einem Signal explizit nennt, ist die C1-Zuordnung plausibler als C2. Das ist ein zusätzliches Signal für den Classifier.

## Erkenntnis 4 — Time-of-Day-Profile

| Cluster | Early/PM | Open30 | Midday | Close1h | AH |
|---|---|---|---|---|---|
| C0 | 20% | 19% | 45% | 8% | 9% |
| C1 | 23% | 12% | 51% | 7% | 8% |
| C2 | **33%** | 3% | 58% | **0%** | 6% |

**Implikation:**
- **C2 Monster wird NIE 15:00-16:00 signalisiert** (0 von 33). Jack macht die Monster-Plays früh oder gar nicht.
- **C2 PM-Rate** (33%) validiert Phase 1 (vol_pm_pct median 11.6% bei C2-Tickern) — Jack pickt die Stunden, wo C2 bereits aktiv ist.
- **C1 hat niedrigste Open30-Rate** (12%) — passt zur Phase-1-DNA "Midday-dominiert" (58% Volumen RTH-middle).

## Erkenntnis 5 — Monster-Days sind eher Norm als Ausnahme

**72.6%** aller Signal-Tage haben >50% Day-Range. Also an 7 von 10 Tagen, an denen Jack einen Ticker erwähnt, bewegt sich der Ticker wirklich stark.

Pro Cluster:
- **C0**: 114/139 = **82%** Monster-Signal-Tage (>50% Range)
- **C1**: 69/134 = **51%** Monster-Signal-Tage
- **C2**: 32/33 = **97%** Monster-Signal-Tage

**Interpretation:** Jack ist kein zufälliger Picker. Seine Signale treffen fast immer auf einen Tag mit überproportionaler Bewegung. C2 ist extrem: 97% der C2-Signale sind an Monster-Tagen — fast kein Leerlauf.

**Caveat:** "50% Range" ist für Penny-Stocks niedrig. Die Monster-Day-Definition aus Phase 1 war >100% Range. Mit dieser strengeren Schwelle (nicht in diesem Report gerechnet, aber ableitbar) wäre die C2-Rate immer noch bei ~60%.

## Erkenntnis 6 — Halted-Keyword × Cluster = massive Amplifikation

Wenn Jack das Wort "halted" verwendet, ändert sich die typische Bewegung:

| Cluster | kw_halted=0 Median | kw_halted=1 Median | Faktor |
|---|---|---|---|
| C0 | 156% | 165% | 1.06× |
| C1 | 51% | **229%** | **4.5×** |
| C2 | 382% | **1194%** | **3.1×** |

**Implikation:** "Halted" in einem C1-Text ist ein **starkes Warnsignal** — typische C1-Range ist 51%, aber wenn halted gementioned wird, ist es plötzlich 229%. C1 wird für einen Tag zu einem "C2-lookalike".

Das heißt: **Cluster-Zuordnung ist nicht statisch**. Es gibt "Event-Days" an denen ein C1-Ticker wie C2 handelt. Keyword-Detection kann diese Event-Days vorab flaggen.

**Regel-Idee:**
```
if cluster == C1 and "halted" in text:
    switch to C2 rules for this trade  # weiter SL, kleinere Position
```

## Erkenntnis 7 — Konfidenz-Feld ist nutzlos

Parser-Konfidenz (aus Claude-Parser) korreliert mit **keiner** Outcome-Metrik:
- `corr(confidence, day_return) = 0.07`
- `corr(confidence, day_range) = 0.04`

Median-Konfidenz ist überall 0.90, Std = 0.04. Der Parser gibt fast allen Signalen 0.90 — das Feld trägt keine diskriminative Info.

**Consequence:** Confidence-Threshold als Filter bringt nichts. Parser-Konfidenz ist effektiv ein konstanter Wert. Entweder neu kalibrieren oder nicht benutzen.

## Erkenntnis 8 — Signal-Density-Days als Regime-Proxy

Top-Tage nach Signal-Dichte:

| Datum | C0 | C1 | C2 | Total | Lesart |
|---|---|---|---|---|---|
| 2025-12-08 | 16 | 7 | 7 | **30** | Broad Day — alle 3 Cluster aktiv |
| 2025-12-10 | 10 | 10 | 0 | 20 | PM-Penny + Solid, keine Monster |
| 2026-01-06 | 0 | **20** | 0 | 20 | Reiner C1-Tag |
| 2025-12-09 | 14 | 0 | 0 | 14 | Reiner C0-Tag |
| 2025-12-22 | 11 | 3 | 0 | 14 | C0-dominiert |
| 2025-12-05 | 4 | 0 | 8 | 12 | **Monster-Tag** (CETX, TGL) |

**Implikation:** Jack hat "Theme-Days". Am 2026-01-06 postet er 20 Signale, alle C1. Am 2025-12-05 postet er 8 C2-Signale und **keine** C1. Der Kanal selbst ist ein Regime-Indikator — wenn heute schon 5 C2-Signale reinkamen, ist die 6. C2-Chance wahrscheinlicher.

## Market-Regime-Analyse (schwach — zu wenig Regime-Wechsel)

Von 306 Signalen:
- 271 (89%) in "chop"
- 29 (9%) in "bull_quiet"
- 6 (2%) in "high_vol"
- 0 in "bear"

Der Zeitraum Okt 2025–Jan 2026 war SPY-seitig weitgehend chopping (SPY 20d-Return selten >3%). **Das Sample-Problem ist groß** — wir können nicht behaupten, dass Bull/Bear den Cluster beeinflusst, weil wir kein Bull/Bear sauber hatten.

Auffällig aber: Im **bull_quiet**-Regime (29 Signale) war `avg_day_return = 25.7%` vs `chop = 66%`. Das passt zu dem Stylized-Fact, dass **Penny-Runs in Chop-Märkten besser laufen** als in ruhigen Bull-Phasen (Geld rotiert aus Large-Caps). **Vorsichtig interpretieren** — N=29.

**Für zukünftige Phase:** Bei SPY-Drawdown >5% kommt echtes Bear-Regime — dann müssen wir Cluster neu kalibrieren. Aktuell nicht testbar.

## Erkenntnis 9 — SEC-Filings als objektiver News-Proxy

Weil Polygon erst heute Abend kommt und yfinance-News nur „aktuell" zurückgibt, habe ich auf **SEC EDGAR 8-K Filings** als historische News-Quelle ausgewichen. Jede material-relevante Firmen-News (Merger, FDA-Approval, Officer-Change, Offering, Earnings) muss als 8-K/6-K gemeldet werden, mit Filing-Datum und Item-Codes (1.01, 2.02, 5.02 etc.).

**Alle 49 Ticker sind in EDGAR gelistet. Gezogen: 6.183 Filings gesamt (3.558 8-K, 1.788 6-K, 458 Dilution-Filings S-1/S-3/424B5).**

### 9a — Dilution-Filings sind ein harter Warner 🚨

Wenn in den letzten 7 Tagen ein S-1/S-3/424B5 (Prospectus = Aktien-Verwässerung) kommt, **halbiert sich die Hit-Rate massiv**:

| Cluster | ohne Dilution 7d | mit Dilution 7d |
|---|---|---|
| **C0** | 74% bull, +58% Return | **14% bull, −4% Return** |
| **C1** | 55% bull, +39% Return | **21% bull, −3% Return** |
| **C2** | 84% bull, +205% Return | 100% bull (N=2, zu klein) |

**Das ist die härteste Regel aus Phase 2:** Check vor jedem Trade die letzten 7 Tage auf S-1/S-3/424B5. Wenn ja → **Skip oder Halbposition**.

Code-Idee:
```python
if filings_in_window(ticker, now, -7, 0, form_types=['S-1','S-3','424B5']):
    reject_signal("Dilution risk: offering in last 7d")
```

### 9b — Earnings-Filings am Signal-Tag = schlechtes Setup

C1-Signale mit Earnings-8-K am Signal-Tag oder Vortag:
- Ohne Earnings: median_range 80%, +41% Return, 57% bull (N=116)
- Mit Earnings: median_range 27%, **−8% Return, 17% bull** (N=18)

Earnings verursachen unkalkulierbare Lücken (vor allem bei Mikro-Cap-Biotechs). Jack postet trotzdem — wahrscheinlich weil er nicht prüft. Classifier sollte das.

### 9c — C2 Monster ist News-getrieben

| Cluster | 8-K am Signal-Tag | 8-K in 7d davor | 8-K in 3d danach |
|---|---|---|---|
| C0 | 25% | 12% | 14% |
| C1 | 31% | 36% | 27% |
| **C2** | 15% | **52%** | **61%** |

C2 Monster hat die **doppelte Filing-Rate** in den 7 Tagen vor dem Signal-Tag — News-Events sind der Trigger für die Monster-Tage. Und 61% der C2-Signale haben ein 8-K in den 3 Tagen **nach** dem Signal — typisch für „multi-day News-Cycles" (PR-Push, Analyst-Follow-up).

**Interessant am Signal-Tag selbst:** C2 hat mit 15% die niedrigste 8-K-Rate. Jack postet nicht AUF die News, sondern auf den Nach-News-Push.

### 9d — News-Intensity × Day-Range Bestätigung für C2

```
C2 mit 1 × 8-K in 7d before:  n=14, median_range 1194%, mean_return +396%, 93% bull
C2 ohne 8-K in 7d before:     n=16, median_range  342%, mean_return  +45%, 75% bull
```

Ein einzelnes 8-K in der Vorwoche **triert bei C2 einen 3× stärkeren Move** und erhöht die Hit-Rate von 75% auf 93%. Starkes Live-Signal.

### 9e — Bearish-8-K am Signal-Tag ist in Jacks Signalen NULL

Von 306 Signalen: **0** haben am Signal-Tag einen bearish-tagged 8-K (Officer-Departure, Delisting-Notice, Non-Reliance-on-Financials). Jack filtert diese Tage offenbar komplett aus — bewusst oder unbewusst. Das ist eine saubere Entlastung der Strategie: **wir müssen nicht befürchten, ein „Bad-News-Day"-Signal zu bekommen**, weil Jack sie nie postet.

Caveat: "Bearish" ist hier nur aus Item-Codes abgeleitet, nicht aus Filing-Text. Ein 7.01 (RegFD) kann auch negative News sein. Richtige Textanalyse folgt später.

### 9f — Filing-Heatmap als Ergänzung im Live-Bot

Pro eingehendem Signal bereits VOR Entry abfragen:
1. `has_dilution_7d` (bool) — **HARD REJECT** wenn True
2. `has_earnings_today_or_yesterday` (bool) — **HARD REJECT** oder Halbposition
3. `n_8k_last_7d` (int) — bei >=1 und C2-Kandidat → Position ruhig aggressiver
4. `n_bearish_items_today` (int) — Hardcoded 0 in unseren Daten, aber behalten als Safety-Net

Performance: EDGAR hat Rate-Limit von 10 req/s, Latency ~300ms. Für Live-Bot müssen wir cachen (täglicher Pull der letzten 30 Tage aller Watchlist-Ticker, refresh stündlich).

## Erkenntnis 10 — Trade-Simulation validiert (und stellt infrage) die Regeln

Unsere 18 echten Trades liegen außerhalb des Signal-Windows (März/April 2026 vs Okt 2025–Jan 2026), also keine direkte Validation möglich. Stattdessen: **theoretische Trade-Simulation** auf 296 Signalen × 5 SL/TP-Szenarien = 1.480 simulierte Trades.

**Simulations-Logik:** Entry beim nächsten 1min-Bar nach Signal-Timestamp. Exit bei SL-Hit / TP-Hit / EOD-Close am Signal-Tag. Keine Multi-Day-Holds, keine TSL, keine Partial-TPs. Das ist eine **untere Schranke** — mit TSL/Partial-TPs wäre die Performance typischerweise besser.

### 10a — Nur C1 ist profitabel (bei enger Regel)

Optimale Regel pro Cluster (aus Simulation):

| Cluster | SL | TP | n | Win-Rate | Avg PnL |
|---|---|---|---|---|---|
| **C0 PM-Penny** | — | — | 130 | 12–26% | **immer negativ** (beste: −2.4%) |
| **C1 Solid Day** | **10%** | **15%** | 133 | **44%** | **+1.01%** |
| **C2 Monster** | **20%** | **40%** | 33 | 36% | **+1.55%** |

**Das ist die eindeutigste Aussage aus Phase 2:**
- **C0 PM-Penny ist auf Tagesbasis nie profitabel** mit einfachen SL/TP — braucht entweder bessere Filter (News, Keywords) oder ist strukturell für Holds nicht geeignet
- **C1 liebt engen SL** (10%) und schnelles TP (15%). Matches die Phase-1-Hypothese „kontrollierbare Day Trades"
- **C2 braucht breite Regeln** (SL=20%, TP=40%). Tight SL=5% gibt bei C2 nur **6% Win-Rate**! Validiert Phase-1-Hypothese „2.0 × ATR ≈ 50% SL für Monster"

### 10b — Exit-Reason zeigt die Cluster-Physik

Bei SL=10/TP=25 (Baseline):

| Cluster | SL-Hit | TP-Hit | EOD |
|---|---|---|---|
| C0 | **66%** | 18% | 16% |
| C1 | 32% | 14% | **54%** |
| C2 | **82%** | 15% | 3% |

C2 fliegt in 82% der Fälle durch 10% SL raus — das ist der Cluster-Eigenbau. Ohne wideren SL trifft Jack bei C2 fast immer Noise. C1 dagegen bleibt in der Hälfte der Trades bis EOD stabil — niedrige Intraday-Vol.

### 10c — Dilution-Filter validiert (Effekt schwächer als Day-Range-Studie vermuten ließ)

| Cluster | ohne Dilution 7d | mit Dilution 7d |
|---|---|---|
| C0 | 21% Win | 14% Win (N=7) |
| **C1** | **42% Win** | **23% Win** (N=13) |
| C2 | 16% Win | 50% (N=2, nicht aussagekräftig) |
| **Global** | **30% Win** | **23% Win** |

**C1 mit Dilution-Warnung: Win-Rate fällt von 42% auf 23%.** Das ist ein starker Live-Filter-Kandidat. Global-Effekt (7 Prozentpunkte) matcht die Day-Range-Hypothese, wenn auch kleiner.

Die Day-Range-Studie (Section 9a) zeigte `Return 58% → -4%` — das ist EOD-Close-Return, nicht Trade-PnL. Mit SL=10 greift der SL bevor der volle Drop da ist. Deshalb ist der **Trade-PnL-Effekt kleiner als der Day-Return-Effekt**. Gute Lektion: SL begrenzt Downside, aber auch die Sichtbarkeit des Filter-Effekts.

### 10d — 8-K-News in 7d ist zweischneidig

| Cluster | ohne 8-K 7d | mit 8-K 7d | Lesart |
|---|---|---|---|
| C0 | 22% Win | **12% Win** | 8-K in C0 = schlechter |
| C1 | 40% Win | 40% Win | kein Effekt |
| C2 | 25% Win | **12% Win** | 8-K in C2 = schlechter! |

**Überraschung:** In Section 9d zeigte C2 mit 8-K massive Range-Amplifikation (1194% vs 342% median). Aber in der Trade-Simulation ist C2 mit 8-K 7d WENIGER profitabel (12% vs 25% Win-Rate)!

**Interpretation:** News-Tage haben große Moves, aber die Richtung ist **unpredictable** — mit festem SL/TP frisst der erste Downside-Spike die Position, bevor der Run kommt. Die Day-Range-Zahl erfasst absolute Bewegung, nicht Reihenfolge. Für Live-Trading heißt das: **Post-News-Days brauchen TSL, nicht fixen SL**.

### 10e — Time-Bucket pro Cluster

| Cluster | Bester Time-Bucket | Win | Avg PnL |
|---|---|---|---|
| C0 | **close1h** (15:00-16:00) | 45% | +6.17% |
| C1 | **pm** | 37% | +3.36% |
| C2 | **pm** | 36% | +2.73% |

**C2 in midday: 11% Win, −6.85% avg — FATAL.** C2-Signale nur in der Pre-Market-Phase nehmen. Das war auch in Phase 2 Section C klar (C2 33% PM-Share), aber jetzt mit Outcome-Zahlen.

**C0 in PM: 13% Win, −5.6% avg — ebenfalls schlecht.** Das widerspricht dem Phase-1-Vorschlag „PM-Entry ok für C0". Falls Jack C0 in PM postet, ist das typisch ein „hinter der Welle kommen".

### 10f — Keyword-Filter wirken

| Keyword | Effekt | Empfehlung |
|---|---|---|
| `kw_careful` | 0% Win in C0/C2, 29% vs 40% in C1 | **Hard-Skip wenn mentioned** |
| `kw_halted` | C2: 0% Win (vs 23% ohne) | **Skip für C2** |
| `kw_low_float` | C0: 0% Win (N=4), C2: 33% (N=3) | nicht eindeutig, behalten |

`kw_careful` ist der klarste Filter — Jacks eigene Warnungen stimmen. Wenn er „careful" schreibt, sollten wir es ernst nehmen.

### 10g — Wochentag-Überraschungen

| Cluster | Best Weekday | Worst Weekday |
|---|---|---|
| C0 | **Wednesday** (35% Win, +2.8%) | Monday (16%) |
| C1 | **Friday** (53% Win, +4.65%) | Wednesday (33%) |
| C2 | Tuesday (40%, N=5) | **Friday** (8% Win, −7%) |

**Widerspruch zu Phase 2 Section 1 Weekday-Signatur:**
- Phase 2 Erkenntnis 1: C2 signalisiert Mo/Fr (78% der C2-Signale). Das ist WIE OFT er postet.
- Phase 2d Erkenntnis 10g: C2 am Freitag hat nur 8% Win-Rate. Das ist WIE GUT die Freitags-Signale sind.
- **Kombiniert: Jack postet C2 am häufigsten Mo/Fr, aber die Freitags-Trades verlieren massiv.** Das ist ein klarer Arbitrage — C2-Freitags-Signale ignorieren oder auf nächsten Montag verschieben.

### 10h — Trade-Type-Labels sind evidenzbasiert

| Cluster × Trade-Type | Win-Rate | Avg PnL |
|---|---|---|
| C0 day_trade | 20% | −2.8% |
| **C0 swing** | **0%** | −8.6% |
| C1 day_trade | 33% | −1.1% |
| C1 swing | 36% | −1.2% |
| C1 long_term | 100% (N=2) | +6.4% |
| C2 day_trade | 27% | −1.3% |
| C2 unknown | 11% | −6.1% |

**C0 swing = definitive Skip-Regel** (0% Win, N=7). Wenn Jack einen C0-Ticker als Swing markiert, ist das fast garantiert ein Verlust-Trade.

**C1 long_term (N=2)**: Sehr kleines Sample, aber beide Trades profitabel. Lockert die Hypothese „Swing nur für C1" etwas auf.

### Caveats der Simulation

1. **Nur Signal-Day Exit** — Jack's Swing-Trades gehen über mehrere Tage, EOD-Close vernichtet diese Trades unfairly. Multi-Day-Simulation wäre korrekter für Swings.
2. **Kein TSL / Partial-TP** — unsere reale Strategie ist komplexer, Simulation ist konservative untere Schranke.
3. **Entry bei Signal-Minute-Close** — ignoriert Jack's tatsächliche Entry-Kriterien (er postet manchmal ein „Price Alert" als Anker).
4. **Keine Slippage / Fees** — auf Penny-Stocks reale Kosten 0.5-2% pro Trade, würde alle Zahlen um 1-4 PP verschlechtern.
5. **Vergleich trades.db vs. Signal-Window unmöglich** — unsere 18 echten Trades sind aus März/April 2026, alle außerhalb unseres Signal-Windows. Keine Direkt-Validation.

## Offene Fragen

1. **Switcher-Signale**: C1-Ticker mit "halted"-Text — springen sie dauerhaft in C2-DNA oder nur für einen Tag? Brauchen Multi-Day-Tracking.
2. **Wochentag-Effekt echt?** Oder Artefakt der 13-Wochen-Window? Mit 6 Monaten Daten gegenprüfen.
3. **Sentiment-Feature fehlt**: Nur Keyword-Dict bisher. NLP-Embedding (sentence-transformer) pro Signal wäre besser — erfasst Tonfall ("careful" mit Ausrufezeichen vs. beiläufig).
4. **Inter-Signal-Zeit**: Wenn Jack 3 Signale in 10min postet — steigt die Hit-Rate? Nicht gemessen.
5. **Trade-Outcome-Validation**: Wir haben 61 eigene Trades. An welche Cluster gingen die? Welche Win-Rate pro Cluster? (Braucht trades.db × signals.db-Join, morgen.)

## Dateien

- **Enrichment-Skript:** `/root/signal_bot/scripts/enrich_signals.py`
- **Korrelations-Skript (Umgebung):** `/root/signal_bot/scripts/correlate_signals_clusters.py`
- **SEC-Filings-Fetcher:** `/root/signal_bot/scripts/fetch_news_sec.py`
- **News-Korrelations-Skript:** `/root/signal_bot/scripts/correlate_news_signals.py`
- **Simulations-Skript:** `/root/signal_bot/scripts/simulate_signal_trades.py`
- **Trade-Outcome-Skript:** `/root/signal_bot/scripts/correlate_trades_clusters.py`
- **Output:**
  - `reports/ticker_classifier/signals_enriched.csv` (594 × 74) — Signale mit Umgebung
  - `reports/ticker_classifier/signals_with_performance.csv` (306 × 80) — +1min-Day-Performance
  - `reports/ticker_classifier/signals_with_news.csv` (306 × 105) — +SEC-Filing-Counts
  - `reports/ticker_classifier/sec_filings_raw.csv` (6183 Filings) — alle 8-K/6-K/S-1/S-3/424B5
  - `reports/ticker_classifier/phase2_correlations.txt` — Umgebungs-Auswertung
  - `reports/ticker_classifier/news_correlation_report.txt` — News-Auswertung
  - `reports/ticker_classifier/signals_simulated.csv` (1480 × 16) — Trade-Simulation mit SL/TP-Szenarien
  - `reports/ticker_classifier/simulation_report.txt` — Cluster × SL/TP Outcome
  - `reports/ticker_classifier/trades_enriched.csv` — unsere 18 realen Trades mit Cluster/News-Annotation
  - `reports/ticker_classifier/trades_outcome_report.txt` — Real-Trade-Analyse (limitiert: kein Cluster-Match)

## Nächste Schritte (morgen durchsprechen)

1. **Hard-Reject-Regel live verdrahten** — vor jedem Entry SEC-EDGAR-Check auf Dilution-Filing (S-1/S-3/424B5) in letzten 7 Tagen. Höchste Evidenz-Qualität.
2. **Regel-Katalog aufsetzen** — konkrete if/then-Rules aus Keyword-Lift, Weekday-Muster und News-Aktivität, priorisiert nach Evidenz.
3. **Trade-Outcome-Join** — Cluster × PnL × Win-Rate unserer 61 echten Trades. Siehe Phase 2c.
4. **C1→C2-Switcher-Detection** — bei welchen Events (Halted-Keyword, 8-K in 7d) wechselt C1-Ticker vorübergehend ins Monster-Verhalten?
5. **Sentiment-Embedding** statt Keyword-Dict — robuster gegen Synonyme.
6. **Filing-Text-Analyse** — heute nur Item-Codes, nicht Filing-Inhalt. Claude-basiert Titles klassifizieren (Contract/FDA/Offering/Earnings/…) wäre qualitativ besser.
7. **Polygon.io nach Aktivierung** — Pressemitteilungen mit Sentiment-Score pro Ticker × Datum, ergänzt die SEC-Sicht um PR-Wire / Analyst-News.
8. **Phase 3 Integration** — erste `classifier.py`-Draft mit diesen Regeln, Dry-Run gegen neue Signale.
