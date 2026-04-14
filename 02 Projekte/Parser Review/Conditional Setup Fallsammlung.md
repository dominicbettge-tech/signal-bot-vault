---
tags: [parser, review, conditional-setup, fallsammlung]
erstellt: 2026-04-14
ziel: 80%+ Erkennungsrate ableiten bevor Parser-Regel in Regeln.md eingebaut wird
---

# Conditional Setup — Fallsammlung

Alle Fälle sammeln, in denen Jack **ein Setup mit Bedingung + Preis ankündigt** und der Trade dann nachweislich funktioniert hätte (oder nicht). Ziel: aus allen Fällen zusammen eine Parser-Regel ableiten die bei **>80% der Fälle** korrekt triggert und <20% False-Positives hat.

Verwandt:
- [[../Conditional Watchlist Auto-Entry]] — Feature-Spec
- [[Regeln]] — finale Regel wird hier eingebaut sobald Fälle ausreichen

---

## Fall 1 — LAES (2026-02-12 → 2026-03-16)

**Setup-Ankündigung (msg 5113, 2026-02-12 19:11 ET):**
> "I am paying attention to LAES. Current chart if it gets below 3.58 and stays above 3.36 it might represent double bottoms. And it may push a move by 8% to 12% from around these levels!"

**Was Jack selbst gemacht hat:** 4 Wochen später (msg 5409, 2026-03-16) eingestiegen bei 3.29-3.31.

**Würde der Bot das können?** Teilweise — Level 3.36-3.58 war breit, Expiry unklar. Drawdown danach −36%.

**Phrasen in dieser Nachricht:**
- "if it gets below X" (breaks_below als Setup-Entry, aber eigentlich Long-Bias)
- "stays above Y" (stays_above als Invalidation)
- "it might represent double bottoms" (Pattern)
- "may push a move by X% to Y%" (Target-Range)

---

## Fall 2 — RADX (2025-12-15 09:15 ET)

**Setup-Ankündigung (msg 4109):**
> "Another one moved big pre market today is RADX. It may get another bull flag if it stays above 13.00 in the coming 10 minutes"

**Was Jack selbst gemacht hat:** 25 Minuten später (msg 4114) rein bei 13, halb raus bei 16 — +23% Easy Trade.

**Würde der Bot das können?** Ja, klar definierte Bedingung + enger Zeitrahmen. Bot hätte bei T+10min geprüft ob Close > 13 und dann Limit-Buy.

**Phrasen in dieser Nachricht:**
- "if it stays above X" (stays_above)
- "in the coming 10 minutes" (expiry T+10min)
- "bull flag" (Pattern)
- "may get another" (Pattern wiederholt vorher)

---

## Fall 3 — NCPL (2025-12-09 14:50 ET, msg 4008)

**Setup-Ankündigung:**
> "NCPL If it failed to break 1.54 resistance it may drop below 1.25 to 1.18 there I may enter for quick day trade in the coming 3 to 4 minutes max."

**Was Jack selbst gemacht hat:** Nichts — seine Order füllte nicht (msg 4009: "Time out with no fill the lowest it got 1.27. Still watching").

**Was die Realität machte:** Low war **1.27** → Jacks Range 1.25-1.18 wurde **knapp nicht erreicht**. Nachfolgender Run auf Peak 1.94.

**Würde der Bot das können?** Ja — mit **Offset +2%**: Bot-Range wäre [1.275, 1.204], Low 1.27 hätte gefüllt. Ride auf 1.94 = **+53%**. Ohne Offset: wie Jack kein Fill.

**Phrasen in dieser Nachricht:**
- "If it failed to break X resistance" (fail-condition)
- "it may drop below X to Y" (entry_range, with hedge "may drop")
- "there I may enter" (soft entry, hedge "may enter")
- "for quick day trade" (trade_type=day)
- "in the coming 3 to 4 minutes max" (tight TTL)

**Kern-Lernerfahrung:** Jacks Ranges sind oft **genau verfehlt**. Offset-Entry (+2-3%) ist der Hebel, um bei knappen Miss trotzdem reinzukommen. NCPL ist Proof-Case für Memory `project_conditional_setup_executor.md`.

---

## *(weitere Fälle beim Review einfügen)*

---

# Conditional **Orders** (Sub-Sammlung)

Verwandtes, aber separates Pattern: Jack kündigt eine **Limit-Order mit weicher/bedingter Sprache** an ("I may buy if filled at X"). Unterschied zu Conditional-Setup oben:
- **Setup**: Trigger-Bedingung an Kursverlauf ("if it breaks X / stays above Y") → daraus folgt ein Trade
- **Order**: passive Limit-Order mit Soft-Language ("I may average if it gets me filled at X") → der Trade IST schon definiert (Preis, Ticker, Side), nur das "ob" ist weich

Beide haben "if"-Sprache, aber andere Bot-Aktion: Setup → bedingten Trigger anlegen; Order → passive Limit direkt rein.

## Order-Fall 1 — MIST (2025-12-22 09:42 ET, msg 4200)

**Original (Multi-Signal mit RADX-Status):**
> "MIST another brutal sell pressure. **I may average little more if it gets me something around 1.80 filled** but honestly not gonna risk more in it now as I have another open one RADX but RADX so far not too bad."

**Was Jack vermutlich gemacht hat:** Limit-Order MIST @ ~1.80 platziert (Averaging-Down zu bestehender Position).

**Würde der Bot das heute können?** Nein, doppelt nicht:
1. Multi-Signal — Parser sieht nur einen Ticker pro Message
2. Soft-Language ("may", "if it gets me filled") — selbst wenn er MIST sehen würde, wird das vermutlich nicht als Entry geparst

**Phrasen für die Matrix:**
- "I may average little more"
- "if it gets me [filled] at X" / "if I get something around X filled"
- "not gonna risk more" (Inverse-Signal: Position-Cap)

**Bot-Idealverhalten:** Limit-Buy MIST @ 1.80 als **add-to-position** (kein neuer Trade-Eintrag, sondern Average-Down auf bestehender), mit Position-Cap "not more than X".

---

## Order-Phrasen-Matrix

| Phrase | Fälle | Bedeutung |
|---|---|---|
| "I may average if [it gets me] filled at X" | MIST#4200 | passive Limit-Buy, Averaging-Down |
| "may add some at X" | (TBD) | passive Limit-Buy, Add-to-Position |
| "not gonna risk more" | MIST#4200 | Position-Cap, kein weiterer Add |

---

# Order-after-Fill Pattern (Sub-Sammlung)

**Pattern:** Jack postet eine Order-Ankündigung **NACHDEM** er den Trade bereits gemacht hat. Die "Order"-Nachricht ist effektiv eine späte Bestätigung seines eigenen Fills, oft mit Limit-Werten, die im genannten Fenster nicht mehr erreicht werden.

**Bot-Implikation:** Wir können seinen Order-Ankündigungen **nicht trauen** als Trigger — der eigentliche Move ist schon vorbei. Zwei mögliche Bot-Antworten:
1. **Ignorieren** — Order-Ankündigungen verwerfen, nur "got filled at X" als Trigger nutzen
2. **Order-Price-Offset (Testcenter)** — Bot ordert Jacks Preis +1-3% (wenn Historie zeigt, dass Trade profitabel wird) → hängt mit `project_order_offset_simulation.md` zusammen

## Order-after-Fill Fall 1 — RADX (2025-12-17 09:44 ET, msg 4160)

**Original:** "Activated this order again got small filled at 5.35. Left the others open"
**Latenz:** Jacks Nachricht **9 min nach** echtem Fill (09:35 vs. 09:44).
**Bot-Reaktion heute:** würde versuchen bei 5.35 zu kaufen — Bar @09:44 zeigt ~5.50, Slippage +3%.

## Order-after-Fill Fall 2 — MIST (2025-12-15 13:18 ET, msg 4126)

**Original:** "MIST got some at 2.28 but will hold for now. For swing to long"
**Vorgeschichte:** Order-Ankündigung um 09:51 mit Limit 2.20-2.23.
**Polygon-Realität:**
- 2.28 wurde **nur 09:36-09:48** gehandelt (Open-Auction-Crash, vor der Order-Ankündigung!)
- Im Order-Fenster 09:51-13:18: tiefster Kurs **2.25** → Order **niemals** im Range
- Bar @13:18 (Fill-Bericht): 2.36-2.38 — kein 2.28 zu finden
**Latenz:** Echter Fill ~09:36-09:48, Bericht 13:18 = **3.5-4 Stunden später**.
**Doppelter Fail für den Bot:**
1. Original-Order 2.20-2.23 hätte nicht gefüllt
2. Bei "got at 2.28" Reaktion → Markt ist 4h weiter, Slippage +4% (2.28 → 2.37)

## Order-after-Fill Pattern-Matrix

| Phrase | Fälle | Echte Latenz | Bot-Slippage |
|---|---|---|---|
| "got [small/some] filled at X" | RADX#4160 | 9 min | +3% |
| "got some at X" | MIST#4126 | 3-4 h | +4% |
| "I averaged at X" | (TBD) | (TBD) | (TBD) |
| "took half/some out at X" | RADX#4114 (vermutlich) | (TBD) | (TBD) |

## Testcenter-Simulation (Vermerk)

**Idee:** Statt Jack-Preis stur zu nehmen, **Order-Price-Offset** sweepen — z.B. Jack-Preis × 1.01 (+1%). Hypothese: wenn die Historie zeigt, dass der Trade danach profitabel wird, lohnt sich +1% Slippage in Kauf nehmen, um überhaupt gefüllt zu werden.

**Sweep-Range im Testcenter:** {0%, +0.5%, +1%, +2%, +3%, +5%} × {Limit, Market-IOC, Stop-Limit}

Konkret für die beiden Fälle:
- **RADX #4160:** Jacks Preis 5.35, +1% = 5.40, +2% = 5.46. Polygon @09:44: ~5.50. → +3-4% nötig für realen Fill.
- **MIST #4126:** Jacks Preis 2.28, +1% = 2.30, +5% = 2.39. Polygon @13:18: 2.37. → +4% nötig.

**Daraus:** Tendenz für Penny-Stocks mit Fill-Latency-Pattern eher **+3-5% Offset**. Genauer Wert via Sweep über alle 282 Entry-Signale.

Connected to:
- Memory `project_order_offset_simulation.md` (Testcenter-Parameter)
- Vault `Testcenter — Anforderungen & Architektur.md` Section 7d

---

# Soft-Keyword Risk-Score (Sub-Sammlung) ⚠️ Anti-Pattern

**Idee (User-Vorgabe 2026-04-14, MIST-Review):** Akkumulation von Soft-/Hedge-Sprache in Jacks Messages = Bot-Risk-Indikator. Viele weiche Worte → unsicherer Trade → Bot **skippt** oder reduziert Position.

**Konkreter Auslöser:** MIST-Review zeigt 64 Soft-Keywords in 17 Messages = **ø 3.8 pro Message**. Trade war "zu lang, zu gefährlich, zu unprofitabel — Falling-Knife-Pattern". Final Result: Avg 1.89 → 1.70 = -10% Buchverlust nach 2 Monaten.

## Soft-Keyword-Kategorien (mit MIST-Hits)

| Kategorie | Beispiel-Phrasen | MIST-Hits | Bot-Bedeutung |
|---|---|---|---|
| **modal_uncertain** | might, may, could, would, should, maybe | 10 | Unsicherheit → kein klarer Trade |
| **hedges** | for now, so far, honestly, personally, some | 13 | Aufweichung eigener Aussage |
| **conditional** | if, in case, as long as, whenever | 7 | Bedingung → kein klarer Trigger |
| **time_vague** | soon, tomorrow, this week, later | 9 | Zeit unklar → Expiry undefiniert |
| **defensive_bearish** | still red, brutal sell, downtrend, **bearish**, bearish zone, **risk gauge too high** | 7 | **MARKT-WARNUNG** — Bot vorsichtig |
| **hold_passiv** | still holding, will hold, **holding for long**, see how it goes, take it easy | 11 | **passiv-statt-aktiv** → Bot keinen neuen Entry |
| **avg_down_falling_knife** | average more, averaged more, add more if, **adding again and again**, final average, small/medium block | 7 | **FALLING-KNIFE** — Bot blocken |
| **swing_long_hold** ⚠️ neu | **swing** (im Trade-Kontext, nicht Day), swing-list, swing to long, holding for long, for swing | (TBD) | Höheres Risiko als Day-Trades — Bot Position halbieren |

## MIST-Top-Risk-Messages (höchster Soft-Score, mit erweiterten Keywords)

| # | Msg | Score | Was sticht raus |
|---|---|---|---|
| **16** | 235 | **11** ⚠️ | "**bearish** zone" + "**swing**" 2× + "**oversold**" + "**downtrend**" — höchster Score, klassisches Falling-Knife-Setup |
| 12 | 4187 | 9 | "honestly tried to take it easy", "might be a good sign", 3× hold_passiv |
| 15 | 4200 | 7 | "may average little more if filled", "honestly not gonna risk", "brutal sell pressure" |
| 10 | 4161 | 7 | "averaged more", "final average", "see how it goes" — Falling-Knife-Cluster |
| 11 | 4180 | 6 | "**swing** list", "risk gauge too high", "still holding" — Markt-Warnung |

**MIST-Gesamt: 70 Soft-Marker in 17 Messages** = ø 4.1 pro Message. Final Result: Avg 1.89 → 1.70 (-10% Buchverlust nach 2 Mon.). **Bot-Hypothese:** Bei Soft-Score-Schwelle ≥ 6 hätte der Bot vermutlich 5 von 17 Messages geblockt → kein Avg-Down-Trade → vermutlich neutral statt -10%.

## Bot-Logik-Vorschlag

1. **Pro Message:** Soft-Score berechnen (Summe Hits über alle Kategorien)
2. **Pro Trade-Sequence:** akkumulierter Soft-Score über alle Messages für 1 Ticker im aktiven Fenster
3. **Schwellwerte (vorläufig, im Testcenter zu kalibrieren):**
   - Single-Message > 5 → Warnung, Position halbieren
   - Sequence-Total > 20 → Position **schließen**
   - **Falling-Knife-Veto:** wenn `defensive_bearish ≥ 2 UND avg_down ≥ 1` in derselben Message → **Trade skippen** (kein neuer Entry, keine Add)
4. **Komplement zu Sentiment-Sammlung:** Soft-Keywords sind Jacks-eigener Score, Sentiment-Aussagen sind Markt-Score → beide kombinieren

## Sweep-Kandidat fürs Testcenter

- **`Soft_Score_Threshold`**: {3, 5, 8, 10, 15} → Position-Size halbieren ab Schwellwert
- **`Falling_Knife_Veto`**: {on, off}
- **`Defensive_Bearish_Multiplier`**: defensive_bearish-Hits zählen 2×, 3×, 5× — sind sie wichtiger als modale Unsicherheit?

Connected to:
- Memory `project_caution_signals.md` (Jack-Warnungen als SL-Input — selbe Familie)
- Memory `project_averaging_strategy.md` (Nachkäufe-Strategie — wann lohnt es sich, wann ist es Falling-Knife)
- Sentiment-Sammlung oben (Markt-Score)

---

# Market-Sentiment Aussagen (Sub-Sammlung)

**Primärer Bot-Hebel: Regime-Filter** — bei "Pressure", "Careful", "Sell-Off-Zone" → kleinere Positions, engere TSL, evtl. neue Entries pausieren.

Sekundär (später):
- Pre-Signal-Alert ("will share soon") — Listener priorisieren
- Cross-Check mit Polygon SPY/VIX/IWM — Trefferquote messen

Verbindet sich mit:
- Memory `project_classifier_phase2.md` (VIX/SPY-Klassifikation, Phase 2f)
- Memory `project_caution_signals.md` ("careful" / "sell off zone" als SL-Input)
- Testcenter Section 7 Parameter `Regime_Filter` — Jack-Sentiment als **zweite Datenquelle** zusätzlich zu SPY/VIX

## Sentiment-Fall 1 — Markt-Pressure (2025-12-22 14:15 ET, msg 4216)

**Original (Block B aus RADX-Exit-Message):**
> "The market in some pressure sell and I am looking into some opportunities will share soon whenever they get to my trading zone."

**Bot-Idealverhalten:** `market_regime = pressure_sell` für nächste 2-4h → bestehende Positions TSL um 1-2pp enger, neue Entries Position-Size halbieren.

**Cross-Check Polygon + yfinance (durchgeführt 2026-04-14):**

| Index | 22.12. Close | vs. 19.12. | Signal |
|---|---|---|---|
| **VIX** | 14.08 | -5.6% | **VIX FÄLLT** = Risk-On |
| **SPY** | 684.83 | +0.62% | Up-Day |
| **IWM** (Russell 2000, Penny-Proxy) | 253.58 | +1.11% | **stark up** |

**Befund Fall 1:** Markt war risk-ON, Russell sogar +1.1% — Jacks "pressure sell" war **idiosynkratisch** (auf seine RADX/MIST-Holdings bezogen, nicht Marktlage).

**Methodisch wichtig:** Sentiment-Aussagen IMMER gegen alle 3 Indizes (VIX, SPY, IWM) cross-checken. Wenn Jack systematisch falsch liegt → Sentiment als Bot-Input **deaktivieren**. Wenn richtig (besonders in Penny/IWM) → wertvoller Regime-Hebel.

**Phrasen für die Matrix:**
- "market in some pressure sell" / "market under pressure"
- "looking into some opportunities will share soon"
- "in my trading zone"

---

## Sentiment-Phrasen-Matrix

| Phrase | Fälle | Bot-Hebel | SPY-Realität |
|---|---|---|---|
| "market in pressure sell" / "market under pressure" | RADX#4216 | Regime: kleinere Positions, engere TSL | Fall 1: SPY flat (+0.04%) |
| "will share soon whenever in my trading zone" | RADX#4216 | (sekundär) Listener-Priorität | n/a |
| "careful" / "sell off zone" | (TBD aus caution-Memory) | SL nachziehen | (TBD) |

**Methodisch:** Ab Sentiment-Fall 5 zusätzlich **IWM (Russell 2000)** in den Cross-Check (Penny-näher als SPY). VIX entweder Starter-Upgrade oder via IBKR-API holen.

---

## Phrasen-Matrix Conditional-Setup (wird gefüllt während Review läuft)

| Phrase | Fälle | Richtung | Trigger-Typ |
|---|---|---|---|
| "if it stays above X" | RADX#4109 | long | stays_above |
| "if it gets below X" | LAES#5113 | long* | breaks_below |
| "stays above Y" (Invalidation) | LAES#5113 | — | invalidation_level |
| "may push a move by X% to Y%" | LAES#5113 | — | target_range |
| "in the coming X minutes" | RADX#4109, NCPL#4008 | — | expiry_window |
| "if it failed to break X resistance" | NCPL#4008 | long (rejection play) | breaks_below_after_fail |
| "it may drop below X to Y" | NCPL#4008 | long (buy-the-dip) | entry_range |
| "there I may enter for quick day trade" | NCPL#4008 | long | soft_entry_intent |

*Bei LAES "below X and above Y" → Double-Bottom = Long-Bias obwohl "below" in der Phrase.

---

## Offene Fragen für die Regel-Ableitung

1. **Wie unterscheiden von pure Watchlist?** → Vermutlich: konkreter Preis + Konditional-Phrase zwingend
2. **Wie Richtung erkennen wenn kein Pattern-Wort?** → Context aus vorheriger Nachricht? Market-Sentiment?
3. **Default-Expiry wenn keiner angegeben?** → LAES hatte keinen, RADX 10min. Fallback 24h?
4. **Was tun bei kombinierten Bedingungen ("below X and above Y")?** → Zone-Entry statt Trigger?
5. **Wie oft triggert Jack seinen eigenen Setup ohne Ankündigung?** → Hit-Rate-Frage für Testcenter

## Status

- **2026-04-14:** Sammlung gestartet, 2 Conditional-Setup-Fälle (LAES + RADX) + 1 Conditional-Order-Fall (MIST). Mindestens 10-15 Fälle pro Sub-Sammlung nötig bevor Regel belastbar ist.
- **Nächster Schritt:** Weitere Fälle beim Review einfügen, dann Regel-Entwurf — getrennt für Setup vs. Order.


---

## Sub-Sammlung: Emoji-Celebration als Exit-Hint (Stand 2026-04-14)

Rare aber wiederkehrend: Jack postet eine Message fast ohne Text, nur Emojis (😁🎉✅🙌💯) nach einem Kursziel-Touch. Menschlich = Ausstieg gefeiert. Bot-blind.

| Fall | Ticker | msg_id | Kontext (Preis + Zeit) | Was der Bot aktuell tut |
|---|---|---|---|---|
| 1 | GURE | #4064 | 12-10 13:44 ET, 2min nach Spike-Top 6.32 (Peak des Trades) | nichts — Parser ignoriert emoji-only |

### Warum relevant für TZ
- Bei GURE: Wenn **B (Jack-SL-Floor)** + **C (Jack-TP-Limit 6.00)** aus #9 schon aktiv wären → Bot wäre über TP-Limit bei 6.00 raus, Emoji-Message irrelevant (Position schon zu).
- Wenn Bot aber NICHT schon draußen wäre (z.B. weil Jacks #9-Level verspätet geparsed): Emoji-Celebration kurz nach Spike = **sekundärer Exit-Hint**.
- **TZ-Parameter-Kandidat:** `Emoji_Celebration_Exit_Backup` {off, active_only_if_position_open_AND_price_within_5pct_of_max}

### Detection-Heuristik
- Emoji-Dichte ≥ 2 im Message-Text
- Text-Wörter-Count ≤ 3 (nach Ticker-Entfernung)
- Ticker-Open-Position existiert
- Preis in letzten 15 min hat max_since_entry × 0.95 erreicht oder höher
- Trade aktuell im Profit (PnL > 0)

### Offene Frage
- **False-Positive-Rate:** Wie oft feiert Jack ohne selbst rauszugehen? Brauchen mehr Fälle aus SOPA/NCPL/ABOS zum Abgleich.

### Status
- **2026-04-14:** 1 Fall (GURE). Sekundäre Überlegung, nicht primäres Exit-Signal. TZ soll entscheiden ob es marginalen Alpha-Beitrag gibt.
