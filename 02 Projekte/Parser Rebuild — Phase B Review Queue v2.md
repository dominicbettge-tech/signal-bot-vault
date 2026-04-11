---
tags: [signal-bot, parser, review-queue, v2]
date: 2026-04-11
---

# Parser Rebuild — Phase B Review Queue (v2, Vision-fähig)

**49 Messages** zur manuellen Review, gruppiert nach Grund. v1 hatte 47 Flags, v2 hat 49. Die Vision-Verbesserungen haben einige Fälle gelöst (msg 131 SLS) aber neue aufgeworfen.

Pro Eintrag: msg-id · channel · v2-Klassifikation · Raw-Text · Opus-Reasoning. Annotiere in der nächsten Spalte deine Meinung beim Durchgehen.

## Reasons nach Häufigkeit

- **opus_reject_after_sonnet_entry**: 31
- **haiku_ambiguous**: 11
- **disagree_old=entry_new=watchlist**: 2
- **disagree_old=entry_new=exit**: 1
- **disagree_old=update_new=entry**: 1
- **disagree_old=watchlist_new=entry**: 1
- **low_conf_entry=0.20**: 1
- **low_conf_entry=0.35**: 1

---

## opus_reject_after_sonnet_entry (31)

### #1 — msg 3574 · JACK SPARO PREMIUM · 2025-10-22

- **v2 classification:** commentary ticker=OMEX entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist kein neuer Entry, sondern ein Add-on zu einer bestehenden Position ('Added little more', 'yesterday I opened only a small position. Increased little more today holding still'). Es gibt keinen 'placed' Marker, kein TIF, keine Ablaufzeit. Es ist ein Status-Update über eine bereits laufende Po
- **Raw text:**

```
Added little more OMEX at 2.49 
Might wait to see where it could settle again yesterday I opened only a small position. Increased little more today holding still
```

- **Dein Verdict:** _____________________________________

### #2 — msg 3701 · JACK SPARO PREMIUM · 2025-11-04

- **v2 classification:** commentary ticker=LAES entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist kein Entry. 'might adding zone' ist konditional/prospektiv – er beschreibt eine potenzielle Zone, kein platziertes Order. Kein 'placed', kein TIF, kein Ablaufdatum. 'Will keep posted' bestätigt, dass dies eine Watch/Intent ist, keine ausgeführte Order.
- **Raw text:**

```
LAES 
5.50 to 5.25 might adding zone for swing . Will keep posted
```

- **Dein Verdict:** _____________________________________

### #3 — msg 3714 · JACK SPARO PREMIUM · 2025-11-07

- **v2 classification:** commentary ticker=ELDN entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** "added little more at 1.57" ist ein Add-on zu einer bestehenden Position, kein neuer Entry. Es gibt keinen 'placed'-Marker, kein TIF, kein Ablaufdatum. Dies ist ein Status-Update zu einem bereits laufenden Trade, kein eigenständiges Entry-Signal.
- **Raw text:**

```
ELDN
added little more at 1.57
```

- **Dein Verdict:** _____________________________________

### #4 — msg 3930 · JACK SPARO PREMIUM · 2025-12-05

- **v2 classification:** commentary ticker=GURE entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Nur 'GURE at 11.60' — kein 'placed', kein TIF, kein Ablaufdatum, kein Indikator für eine tatsächlich platzierte Order. Das ist bestenfalls eine Beobachtung/Watch, kein Entry.
- **Raw text:**

```
GURE at 11.60
```

- **Dein Verdict:** _____________________________________

### #5 — msg 4234 · JACK SPARO PREMIUM · 2025-12-23

- **v2 classification:** commentary ticker=PCLA entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_AH
- **Opus verdict:** REJECT
- **Opus reason:** This is conditional/speculative, not a placed order. 'I may put an order' is genuine uncertainty here — unlike 'I might place' + 'valid for N minutes' which signals an actual entry. There is no TIF, no 'placed' confirmation, no validity window. The language 'Counting a possible 27% drop... possible 
- **Raw text:**

```
PCLA 
more than 700 M volume
Team I may put an order after hours at 
0.2875
Counting a possible 27% drop AH then a possible 16% to 18% reverse
But if they announce any offering auto cancel.
```

- **Dein Verdict:** _____________________________________

### #6 — msg 4267 · JACK SPARO PREMIUM · 2025-12-24

- **v2 classification:** commentary ticker=AQST entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** This is NOT a placed order. The language is forward-looking and conditional: 'A stock to focus on this coming Friday for a possible January price movement', 'I will start adding between 5.40 up to 5.70', 'Possible exit I am aiming for a possible 30%'. There is no 'placed' marker, no TIF, no indicati
- **Raw text:**

```
A stock to focus on this coming Friday for a possible January price movement.
AQST!
I will start adding between 
5.40 up to 5.70
Possible exit I am aiming for a possible 30% prior to the PDUFA  date ( Jan 31st so far expected not confirmed).
```

- **Dein Verdict:** _____________________________________

### #7 — msg 4283 · JACK SPARO PREMIUM · 2025-12-26

- **v2 classification:** commentary ticker=SOPA entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** The phrase 'possible entry' indicates conditionality/uncertainty — this is NOT the same as 'I placed an order at X'. Jack's typical entry phrasing is 'I placed' or 'I might place' + TIF. Here 'possible entry' reads more like a watch/plan rather than a confirmed placed order. The word 'possible' is a
- **Raw text:**

```
New plan
1.85 possible entry 
Valid for 5 minutes only so far
```

- **Dein Verdict:** _____________________________________

### #8 — msg 4346 · JACK SPARO PREMIUM · 2026-01-05

- **v2 classification:** commentary ticker=ACHV entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** This is a watchlist/analysis, NOT a placed order. Key phrases: 'I am going to pay attention more to ACHV', 'There is a potential good swing in it', 'I am expecting'. No 'placed' marker, no TIF, no order confirmation. The entry range and SL are presented as potential/conditional levels for future con
- **Raw text:**

```
Good evening my great team here.
I hope you all enjoyed your weekend.
I am going to pay attention more to ACHV
The stock entered a bullish zone for both 30 / 90 days chart.
There is a potential good swing in it.
The entry between:
4.10 up to 4.60
With a possible 3.80 as SL for 90 days .
I am expecting 
5.50 up to 6.00 in the short term ( 10 to 14 days )
It has also  a potential bigger move within the next 90 days.
```

- **Dein Verdict:** _____________________________________

### #9 — msg 4392 · JACK SPARO PREMIUM · 2026-01-06

- **v2 classification:** commentary ticker=ALMS entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Kein 'placed' Marker, kein TIF, keine Expiry. 'ALMS 21.35 team 😁' ist eher eine Statusmeldung/Celebration (z.B. Kurs hat 21.35 erreicht) oder ein casual Hinweis, aber kein klarer Entry. Kein Verb das eine Order-Platzierung signalisiert. Harte Reject-Regel: kein 'placed' und kein TIF.
- **Raw text:**

```
ALMS 21.35 team 😁
```

- **Dein Verdict:** _____________________________________

### #10 — msg 4408 · JACK SPARO PREMIUM · 2026-01-07

- **v2 classification:** commentary ticker=IMRX entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Nur 'IMRX 7.50' ohne jeglichen Entry-Marker (kein 'placed', kein TIF, kein 'valid for', kein Alert-Emoji). Das ist eine Watch/Notiz/Preisniveau-Nennung, kein platzierter Order. Sonnet's eigene niedrige Confidence (0.72) bestätigt die Unsicherheit. Harter Reject: kein 'placed' Marker, kein TIF.
- **Raw text:**

```
IMRX 7.50
```

- **Dein Verdict:** _____________________________________

### #11 — msg 4410 · JACK SPARO PREMIUM · 2026-01-07

- **v2 classification:** commentary ticker=IMRX entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist kein Entry. Es gibt keinen 'placed'-Marker, kein TIF/Ablaufdatum, und keine Order-Indikation. 'IMRX 7.89 ✅✅!' ist eine Bestätigung/Status-Update (z.B. Kursziel erreicht, TP getroffen) - die Checkmarks deuten auf Erfolg/Bestätigung hin, nicht auf eine neue Order-Platzierung. Kein Entry-Signa
- **Raw text:**

```
IMRX 
7.89 ✅✅!
```

- **Dein Verdict:** _____________________________________

### #12 — msg 4431 · JACK SPARO PREMIUM · 2026-01-08

- **v2 classification:** commentary ticker=ACRV entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist ein Status-Update ('holding still'), kein neuer Entry. Jack berichtet, dass er bereits eine Position bei 1.98 hat und sie noch hält. Es gibt keinen 'placed'-Marker, kein TIF, und keine Aufforderung zum Einstieg. Der eigentliche Entry war die Parent-Nachricht ('I might start a small position
- **Raw text:**

```
Got one order at 1.98 holding still
```

- **Dein Verdict:** _____________________________________

### #13 — msg 4452 · JACK SPARO PREMIUM · 2026-01-09

- **v2 classification:** commentary ticker=ACRV entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist kein neuer Entry-Alert, sondern ein Update zu einer bestehenden Position ('Added another order' = Nachkauf/Averaging, 'Holding strong' = Status-Update). Es fehlt jeglicher TIF/Expiry-Marker und kein 'placed'-Indikator für einen neuen Trade. 'For full transparency' deutet auf einen informati
- **Raw text:**

```
ACRV for full transparency 
Added another order at 1.84 
Holding strong …
```

- **Dein Verdict:** _____________________________________

### #14 — msg 4509 · JACK SPARO PREMIUM · 2026-01-13

- **v2 classification:** commentary ticker=XAIR entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** Kein Entry. 'if you added pay attention to that' ist eine Statusmeldung/Hinweis für Leute, die bereits eine Position haben. Kein 'placed', kein TIF, kein Ablaufdatum. Es ist weder ein neuer Order noch ein klarer Entry-Aufruf, sondern ein Kommentar zu einem bestehenden Trade. Konditional ('if you add
- **Raw text:**

```
XAIR 
around 2.08 to 2.13 if you added pay attention to that.
```

- **Dein Verdict:** _____________________________________

### #15 — msg 4647 · JACK SPARO PREMIUM · 2026-01-20

- **v2 classification:** commentary ticker=IVF entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Das ✅ nach einem Ticker + Preis ist typisch für eine Bestätigung/Status-Update (z.B. 'Target erreicht' oder 'Trade geschlossen'), nicht für einen neuen Entry. Es fehlen jegliche Entry-Marker: kein 'placed', kein TIF, kein 'valid for X minutes', kein 'order'. Dies ist kein placed order, sondern ein R
- **Raw text:**

```
IVF 3.55 ✅
```

- **Dein Verdict:** _____________________________________

### #16 — msg 4682 · JACK SPARO PREMIUM · 2026-01-22

- **v2 classification:** commentary ticker=None entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Multi-Ticker-Nachricht mit zwei separaten Entries (IOTR @ 6.95 und SXTP @ 4.26). Beide sind echte Entries mit 'placed me an order' und TIF, aber das System kann nur einen Ticker pro Signal verarbeiten. Ohne Kontext zur Priorisierung eines einzelnen Tickers muss dies rejected werden. Sonnet hat korre
- **Raw text:**

```
Pre market Day trades:
IOTR
placed me an order :
6.95
Valid for 15 minutes only!
SXTP
4.26
Valid for 10 minutes
```

- **Dein Verdict:** _____________________________________

### #17 — msg 4695 · JACK SPARO PREMIUM · 2026-01-22

- **v2 classification:** commentary ticker=SXTP entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Kein 'placed' Marker, kein TIF, kein Ablaufdatum. 'Team SXTP 5:70' ist extrem knapp und enthält keinen klaren Entry-Indikator. Könnte ein Watch, ein Status-Update oder sogar eine Shorthand-Notiz sein. Ohne expliziten Hinweis auf eine platzierte Order (placed, order, valid for, day trade alert etc.) 
- **Raw text:**

```
Team
SXTP 5:70
```

- **Dein Verdict:** _____________________________________

### #18 — msg 4730 · JACK SPARO PREMIUM · 2026-01-26

- **v2 classification:** commentary ticker=None entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Kein Ticker identifizierbar – weder im Text noch im Kontext (NO_CONTEXT). Ohne Ticker ist kein valides Signal möglich. Sonnet hat dies korrekt erkannt (confidence 0.2), aber trotzdem als Entry extrahiert statt abzulehnen. REJECT → COMMENTARY.
- **Raw text:**

```
Placed me another order at 4.75 will see if anything will fill in the next 15 minutes. Remember you always can adjust your entry or exit . I only share ideas here not a copy paste trades.
```

- **Dein Verdict:** _____________________________________

### #19 — msg 4907 · JACK SPARO PREMIUM · 2026-02-02

- **v2 classification:** commentary ticker=DKI entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist kein platzierter Order-Entry. 'I am going to risk and get some around 0.62~0.65' ist eine Absichtserklärung/Intent ('going to'), kein 'placed'-Marker. Es fehlt jeglicher TIF/Validity-Marker ('Valid for N minutes') und kein 'placed' oder äquivalenter Ausdruck. 'Going to' + 'to risk them for 
- **Raw text:**

```
DKI
another point of interest in the pre market season 
I am going to risk and get some around 0.62~0.65
To risk them for a possible 20% in the coming  hour or so
```

- **Dein Verdict:** _____________________________________

### #20 — msg 4949 · JACK SPARO PREMIUM · 2026-02-03

- **v2 classification:** commentary ticker=ATOS entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Kein klarer Entry mit spezifischem Preis. 'Added two orders below 5' ist vage - kein konkreter Limit-Preis, kein TIF, kein 'Valid for N minutes'. 'Below 5' ist eine ungefähre Zone, keine präzise Entry-Angabe. Zudem fehlt jegliche Zeitangabe/Expiry. 'Shared the plan yesterday' verweist auf einen früh
- **Raw text:**

```
Added two orders below 5
Shared the plan yesterday!
```

- **Dein Verdict:** _____________________________________

### #21 — msg 4982 · JACK SPARO PREMIUM · 2026-02-05

- **v2 classification:** commentary ticker=GUTS entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** This is conditional, not a placed order. 'if it gets there' makes the entire entry contingent on price reaching 0.385 — it's a limit order announcement with conditions ('if it gets there', 'as soon as it stays above 0.35 and no Reverse split news'). There's no 'placed' marker, no TIF/expiry, and the
- **Raw text:**

```
GUTS
One more order at 0.385 if it gets there then it will be in the hold as soon as it stays above 
0.35 and no Reverse split news!
```

- **Dein Verdict:** _____________________________________

### #22 — msg 5096 · JACK SPARO PREMIUM · 2026-02-11

- **v2 classification:** commentary ticker=None entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_NO_SL
- **Opus verdict:** REJECT
- **Opus reason:** Kein Ticker identifizierbar – weder im Text noch über Kontext. Ohne Ticker ist das Signal nicht actionable. Sonnet hat korrekt ticker=null gesetzt mit confidence 0.2, was bereits ein Reject-Indikator ist. Entry ohne Ticker → REJECT.
- **Raw text:**

```
I placed me an order at 
2.15 see if any will be filled in the next 20 minutes.
```

- **Dein Verdict:** _____________________________________

### #23 — msg 5275 · JACK SPARO PREMIUM · 2026-03-02

- **v2 classification:** commentary ticker=TPET entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist eine Fill-Bestätigung ('Filled at... average cost 0.76'), kein neuer Entry. Der eigentliche Entry war die Parent-Nachricht mit 'Placed an order at 0.71~0.75'. Diese Nachricht ist ein Status-Update/Kommentar zum bereits platzierten Trade, nicht ein eigenständiger Entry.
- **Raw text:**

```
Filled at exact time 6:43 AM US ET average cost 0.76
```

- **Dein Verdict:** _____________________________________

### #24 — msg 401 · JACK SPARO BIOTECH · 2026-03-02

- **v2 classification:** commentary ticker=None entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** Kein Ticker genannt, kein 'placed' Marker, kein TIF. Dies ist eine Beobachtung/Empfehlung für Swing Trader ('very attractive entry'), kein platzierter Order. Ohne Ticker und ohne Action-Marker ist dies Commentary.
- **Raw text:**

```
4.36 ~4.60 very attractive entry for swing traders!
```

- **Dein Verdict:** _____________________________________

### #25 — msg 5331 · JACK SPARO PREMIUM · 2026-03-05

- **v2 classification:** commentary ticker=MOBX entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist kein neuer Entry/placed order. 'I reduced my entry to 0.54~0.61' beschreibt eine Anpassung seiner bestehenden Position (er hat bereits Shares bei 0.40 avg laut Parent). 'again not a big order yet' und 'Bearish sentiment... it might stay low for sometime' zeigen Unsicherheit/Abwarten. Kein '
- **Raw text:**

```
I reduced my entry to 0.54~0.61 again not a big order yet . Bearish sentiment into it and it might stay low for sometime.
```

- **Dein Verdict:** _____________________________________

### #26 — msg 5332 · JACK SPARO PREMIUM · 2026-03-05

- **v2 classification:** commentary ticker=None entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Kein Ticker genannt – weder in der aktuellen Nachricht noch im Parent-Context. Ohne Ticker ist das Signal nicht actionable. Außerdem ist dies eher ein Status-Update ('order filled', 'orders still open') zu einem bereits zuvor platzierten Entry, kein neuer Entry selbst. Sonnet hat das mit 0.35 Confid
- **Raw text:**

```
One order filled at 0.615 even 2 other orders still open
```

- **Dein Verdict:** _____________________________________

### #27 — msg 441 · JACK SPARO BIOTECH · 2026-03-05

- **v2 classification:** commentary ticker=OCGN entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** Dies ist eine Watch/Intent, kein Entry. 'my loading zone if it gets there' ist konditional — er hat keinen Order platziert, sondern beschreibt eine Zone, die er kaufen WÜRDE, falls der Preis dorthin fällt. Kein 'placed', kein TIF, kein Ablaufdatum. 'if it gets there' ist ein klarer Konditional-Marke
- **Raw text:**

```
OCGN
1.66~1.48 my loading zone if it gets there today or tomorrow
```

- **Dein Verdict:** _____________________________________

### #28 — msg 5409 · JACK SPARO PREMIUM · 2026-03-16

- **v2 classification:** commentary ticker=LAES entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** This is conditional/intent, NOT a placed order. 'I might add some... if it gets my order filled' is explicitly conditional — he's saying he MIGHT do something IF the price reaches his level. There's no 'placed', no TIF, no 'valid for N minutes'. The phrase 'I might' here is genuinely conditional (pa
- **Raw text:**

```
LAES is dropping pre market 
I might add some for intra day trade and over night swing if it gets my order at
3.18~3.32 filled
Below 3.00 will be a bearish zone.
```

- **Dein Verdict:** _____________________________________

### #29 — msg 558 · JACK SPARO BIOTECH · 2026-03-18

- **v2 classification:** commentary ticker=ABOS entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** REJECT
- **Opus reason:** "I am evaluating a plan" ist klar konditional/intentional — kein placed order, kein TIF, kein "placed" Marker. Dies ist eine Watch/Planung, kein Entry. Harte Reject-Regel: Konditional ohne Action-Marker.
- **Raw text:**

```
I am evaluating a plan for ABOS to add between 
2.85~2.90
```

- **Dein Verdict:** _____________________________________

### #30 — msg 626 · JACK SPARO BIOTECH · 2026-03-25

- **v2 classification:** commentary ticker=OCGN entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** Nur Ticker + Preis ohne jeglichen Action-Marker ('placed', 'order', 'day trade alert', TIF, etc.). Kein 'Valid for N minutes', kein 'placed', kein Screenshot. Das ist eher eine Watch/Notiz als ein bestätigter Entry. Fällt unter 'Kein placed Marker'.
- **Raw text:**

```
OCGN
2.10
```

- **Dein Verdict:** _____________________________________

### #31 — msg 656 · JACK SPARO BIOTECH · 2026-03-27

- **v2 classification:** commentary ticker=RCKT entry=None-None conf=0.3
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** REJECT
- **Opus reason:** This is conditional/uncertain - 'will place at 3.50 if it fills good if not will wait to see what to do next week.' He says he WILL place (future intent), not that he HAS placed. There's no 'placed' marker, no TIF/expiry, and the conditional 'if it fills good if not will wait' shows uncertainty. Thi
- **Raw text:**

```
RCKT 
One last order for today will place at 3.50 if it fills good if not will wait to see what to do next week.
Again this is a big lesson why we must take profit prior to any catalysts .
Same profit you make you can risk !
```

- **Dein Verdict:** _____________________________________

## haiku_ambiguous (11)

### #32 — msg 3462 · JACK SPARO PREMIUM · 2025-10-13

- **v2 classification:** commentary ticker=OCGN entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
OCGN
```

- **Dein Verdict:** _____________________________________

### #33 — msg 3936 · JACK SPARO PREMIUM · 2025-12-05

- **v2 classification:** commentary ticker=None entry=None-None conf=0.7
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
I got few at 18.88
```

- **Dein Verdict:** _____________________________________

### #34 — msg 4385 · JACK SPARO PREMIUM · 2026-01-06

- **v2 classification:** commentary ticker=ALMS entry=None-None conf=0.75
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
ALMS 18
```

- **Dein Verdict:** _____________________________________

### #35 — msg 4421 · JACK SPARO PREMIUM · 2026-01-08

- **v2 classification:** commentary ticker=None entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
IMG
The ticker name
```

- **Dein Verdict:** _____________________________________

### #36 — msg 4616 · JACK SPARO PREMIUM · 2026-01-16

- **v2 classification:** commentary ticker=None entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
I placed another one at 1.22
```

- **Dein Verdict:** _____________________________________

### #37 — msg 4692 · JACK SPARO PREMIUM · 2026-01-22

- **v2 classification:** commentary ticker=None entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
5.45
```

- **Dein Verdict:** _____________________________________

### #38 — msg 4852 · JACK SPARO PREMIUM · 2026-01-29

- **v2 classification:** commentary ticker=None entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
I placed small order to risk at
1.18 if fills in the next 7 minutes will trade it then if not will pass . The stock doesn’t have much info about the volume to risk
```

- **Dein Verdict:** _____________________________________

### #39 — msg 4889 · JACK SPARO PREMIUM · 2026-01-30

- **v2 classification:** commentary ticker=None entry=None-None conf=0.75
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
Edit the order to
0.74 risky one so far but small amount to risk
```

- **Dein Verdict:** _____________________________________

### #40 — msg 5087 · JACK SPARO PREMIUM · 2026-02-11

- **v2 classification:** commentary ticker=None entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
RENX
```

- **Dein Verdict:** _____________________________________

### #41 — msg 5268 · JACK SPARO PREMIUM · 2026-02-27

- **v2 classification:** commentary ticker=None entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
Entry around 0.62
Two exits around 0.66
Final exit 0.71
```

- **Dein Verdict:** _____________________________________

### #42 — msg 5418 · JACK SPARO PREMIUM · 2026-03-16

- **v2 classification:** commentary ticker=WNW entry=None-None conf=0.85
- **Haiku type:** AMBIGUOUS
- **Opus verdict:** None
- **Raw text:**

```
WNW
12
```

- **Dein Verdict:** _____________________________________

## disagree_old=entry_new=watchlist (2)

### #43 — msg 5592 · JACK SPARO PREMIUM · 2026-04-07

- **v2 classification:** watchlist ticker=None entry=None-None conf=0.95
- **Haiku type:** None
- **Opus verdict:** None
- **Raw text:**

```
Good early morning my incredible team here.
I am taking risk :
Opening small positions for day trades in :
ADVB if it gets any order fill for me : 
Below 7.10
And above
6.82
In coming 45 minutes to 50 minutes. 
SILO :
0.48~0.51
Also valid for 45 minutes .
If nothing filled in this time mentioned. I will wait till after 
07:00 AM US ET to check further for new trades and will share by then!
```

- **Dein Verdict:** _____________________________________

### #44 — msg 717 · JACK SPARO BIOTECH · 2026-04-10

- **v2 classification:** watchlist ticker=OCGN entry=None-None conf=0.92
- **Haiku type:** CONDITIONAL_WATCH
- **Opus verdict:** None
- **Raw text:**

```
OCGN
below 1.70 will accumulate again. Order valid till 
End of trading season tonight at 
08:00 PM ET US
```

- **Dein Verdict:** _____________________________________

## disagree_old=entry_new=exit (1)

### #45 — msg 5546 · JACK SPARO PREMIUM · 2026-03-30

- **v2 classification:** exit ticker=LAES entry=2.25-2.25 conf=0.55
- **Haiku type:** EXIT_SELL
- **Opus verdict:** None
- **Raw text:**

```
LAES 2.25 filled for Me.
Full transparency here!
```

- **Dein Verdict:** _____________________________________

## disagree_old=update_new=entry (1)

### #46 — msg 5602 · JACK SPARO PREMIUM · 2026-04-07

- **v2 classification:** entry ticker=GEVO entry=None-None conf=0.95
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** None
- **Raw text:**

```
I got one order bought for GEVO at
1.97 filled
```

- **Dein Verdict:** _____________________________________

## disagree_old=watchlist_new=entry (1)

### #47 — msg 5621 · JACK SPARO PREMIUM · 2026-04-10

- **v2 classification:** entry ticker=FUSE entry=1.62-1.67 conf=0.92
- **Haiku type:** ENTRY_ORDER_RANGE
- **Opus verdict:** APPROVE
- **Opus reason:** Klassisches Jack-Pattern: 'I might place' + konkreter Preis-Range + 'Valid for N minutes' = Entry. Ticker FUSE korrekt, Range 1.62~1.67 korrekt als entry_low/high, trade_type day_trade korrekt, expiry 10 minutes korrekt, kein SL im Text → null korrekt. Alles sauber.
- **Raw text:**

```
I might place a small day trade order in FUSE
1.62~1.67
Valid for the next 10 minutes only!
```

- **Dein Verdict:** _____________________________________

## low_conf_entry=0.20 (1)

### #48 — msg 4711 · JACK SPARO PREMIUM · 2026-01-23

- **v2 classification:** entry ticker=None entry=15.7-15.7 conf=0.2
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** APPROVE
- **Opus reason:** opus error: Expecting value: line 1 column 1 (char 0)
- **Raw text:**

```
MOVE 
placed an order at 
15.70
For the next 7 minutes 
Again I am not in hurry. I don’t want to ruin my week fomo trading any stock.
If you want to take any risk you always can but try to secure profit.
```

- **Dein Verdict:** _____________________________________

## low_conf_entry=0.35 (1)

### #49 — msg 5494 · JACK SPARO PREMIUM · 2026-03-24

- **v2 classification:** entry ticker=None entry=0.52-0.52 conf=0.35
- **Haiku type:** ENTRY_ORDER
- **Opus verdict:** APPROVE
- **Opus reason:** Extraktion ist korrekt: Fills bei 0.52 bestätigt (Entry), SL bei 0.43 explizit genannt. Ticker fehlt tatsächlich weder in dieser Nachricht noch im Parent-Text — ticker=null ist korrekt. Confidence von 0.35 ist angemessen niedrig wegen fehlendem Ticker. Das Signal wird vermutlich ohnehin verworfen we
- **Raw text:**

```
Two small orders filled at 
0.52 
Placed a SL
at 0.43 will hold if it stays above 0.46
```

- **Dein Verdict:** _____________________________________

