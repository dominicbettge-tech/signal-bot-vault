---
tags: [signal-bot, parser, backtest, review]
date: 2026-04-11
---

# Phase B — Manual Review Queue

**47 Messages** brauchen manuellen Check. DB: `backtest_results_2026-04-11.db` (Table `results`), CSV: `backtest_review_queue_2026-04-11.csv`

Für jede Zeile: `human_verdict` setzen = `entry` | `watch` | `cancel` | `commentary` | `unclear`

## opus_reject_after_sonnet_entry (27)

### msg 131 — SLS (2026-02-11)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Preis genannt – weder entry_low noch entry_high sind vorhanden. Ohne einen konkreten Orderpreis ist dies kein verwertbares Entry-Signal. Fällt unter die harte Reject-Regel: 'Kein Preis genannt'.
- **Text:** I opened an order valid till tomorrow pre market so far for SLS! Will cancel most likely if no fill in the pre market tomorrow!
- **Verdict:** _TBD_

### msg 401 — ? (2026-03-02)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker erkennbar, kein 'placed' Marker, kein TIF/Ablaufdatum. Dies ist eine allgemeine Beobachtung/Empfehlung für Swing-Trader, kein platzierter Order-Entry. Sonnet hat selbst nur 0.1 Confidence vergeben.
- **Text:** 4.36 ~4.60 very attractive entry for swing traders!
- **Verdict:** _TBD_

### msg 441 — OCGN (2026-03-05)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist kein Entry. 'my loading zone if it gets there today or tomorrow' ist konditional — Jack beschreibt eine Zone, in der er LADEN WÜRDE, falls der Preis dorthin kommt. Kein 'placed', kein TIF, kein Hinweis auf eine platzierte Order. Das ist eine Watch/Intent, kein placed order.
- **Text:** OCGN ⏎ 1.66~1.48 my loading zone if it gets there today or tomorrow
- **Verdict:** _TBD_

### msg 558 — ABOS (2026-03-18)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — "I am evaluating a plan" ist klar konditional/vorbereitend - kein placed order, kein TIF, kein Ablaufdatum. Dies ist eine Watch/Intent, kein Entry. Sonnet's eigene Reasoning erkennt sogar 'noch keine finale Entscheidung', klassifiziert es aber trotzdem als Entry. Harter Reject.
- **Text:** I am evaluating a plan for ABOS to add between  ⏎ 2.85~2.90
- **Verdict:** _TBD_

### msg 3698 — VSTM (2025-11-04)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — "Added more" ist kein neuer Entry, sondern ein Nachkauf zu einer bestehenden Position. Es gibt kein 'placed', kein TIF, kein Ablaufdatum. Dies ist ein Status-Update zu einem bereits laufenden Trade, kein eigenständiges Entry-Signal.
- **Text:** Added more VSTM 7.89
- **Verdict:** _TBD_

### msg 3708 — MTC (2025-11-06)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist ein Rückblick/Kommentar, kein Entry. 'The one mentioned here earlier' = Verweis auf einen früheren Trade. '700% mover almost' = Ergebnisbericht. '3 AH' ist ein nachträglicher Preis-/Status-Update, kein 'placed order'. Kein TIF, kein 'placed', keine Entry-Signalwörter. Klassischer Rückblick-Post.
- **Text:** MTC ⏎ 3 AH ⏎ The one mentioned here earlier and the only one for today ⏎ 700% mover almost
- **Verdict:** _TBD_

### msg 3714 — ELDN (2025-11-07)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — This is an ADD to an existing position, not a new entry. 'added little more at 1.57' means Jack is scaling into an already-open trade. There is no 'placed' marker, no TIF/expiry, and no indication of a new order being placed. This should be treated as commentary/position update, not a fresh entry signal.
- **Text:** ELDN ⏎ added little more at 1.57
- **Verdict:** _TBD_

### msg 3930 — GURE (2025-12-05)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Nur 'GURE at 11.60' ohne jeglichen Entry-Marker ('placed', 'order', TIF/Ablaufdauer etc.). Das ist eine reine Statusmeldung oder Watch – kein placed order. Kein Hinweis auf eine tatsächliche Order-Platzierung.
- **Text:** GURE at 11.60
- **Verdict:** _TBD_

### msg 4010 — ? (2025-12-09)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker, kein 'placed'-Marker, kein TIF. Dies ist ein Kommentar über eine Margin/Fehlertoleranz ('tiny margin error'), kein Entry. Sonnet hat selbst nur 0.15 Confidence. Klarer Reject.
- **Text:** Only very tiny margin error team ⏎ 1.27 to 1.25 ⏎ 0.02
- **Verdict:** _TBD_

### msg 4160 — RADX (2025-12-17)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist ein Status-Update zu einer bereits bestehenden Order aus dem Parent, nicht ein neuer Entry. 'Activated this order again got small filled at 5.35' beschreibt eine Teilfüllung einer zuvor platzierten Order. Der eigentliche Entry war im Parent. 'Left the others open' ist reiner Status. Kein neuer placed-Marker, kein TIF, kein neuer Preis-Intent → Commentary/Update, nicht ein eigenständiges Entry-Signal.
- **Text:** Activated this order again got small filled at 5.35 ⏎ Left the others open
- **Verdict:** _TBD_

### msg 4292 — ? (2025-12-29)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker, kein 'placed' Marker, kein TIF. Die Nachricht beschreibt eine Preisbewegung mit Checkmarks (Rückblick/Erfolgsmeldung), nicht einen neuen Entry. Sonnet hat selbst nur 0.1 Confidence. Klarer Reject.
- **Text:** 0.455 to 0.488 ⏎ Then to 0.52  ⏎ ✅✅!
- **Verdict:** _TBD_

### msg 4408 — IMRX (2026-01-07)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Nachricht ist nur 'IMRX 7.50' - kein 'placed', kein TIF, kein Zeitlimit, keine Action-Marker. Das ist eher eine Watch/Callout/Price-Level-Nennung als ein tatsächlich platzierter Order-Entry. Kein expliziter Hinweis auf eine gesetzte Order.
- **Text:** IMRX 7.50
- **Verdict:** _TBD_

### msg 4452 — ACRV (2026-01-09)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist kein neuer Entry-Alert, sondern ein Update zu einer bestehenden Position. 'Added another order' bedeutet, er stockt eine bereits laufende Position auf. 'Holding strong' bestätigt, dass er bereits drin ist. Es gibt keinen TIF/Ablaufzeit-Marker, keinen 'placed' für einen neuen Trade. Dies ist ein Positions-Update/Commentary, kein actionable Entry-Signal.
- **Text:** ACRV for full transparency  ⏎ Added another order at 1.84  ⏎ Holding strong …
- **Verdict:** _TBD_

### msg 4464 — ACRV (2026-01-12)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist kein neuer Entry mit Order-Placement. 'Added little more ACRV at 1.62' ist ein Rückblick/Status-Update über eine bereits getätigte Nachkauf-Aktion bei einem bestehenden Swing-Trade. Es gibt kein TIF, kein 'placed an order', keine Gültigkeitsdauer. Der Rest des Textes spricht über zukünftige Pläne ('I will focus on day trades'). Dies ist Commentary/Status, kein actionable Entry-Signal.
- **Text:** Added little more ACRV at 1.62 but honestly no more budget for it . I will focus on some day trades to create profit cushion to use in any next swing or to average.
- **Verdict:** _TBD_

### msg 4509 — XAIR (2026-01-13)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist kein Entry. Es gibt kein 'placed', kein TIF, kein Ablaufdatum. 'if you added pay attention to that' ist ein Hinweis an Leute, die bereits eine Position haben – es ist eine Watch/Status-Nachricht, keine neue Order. Kein Marker für einen platzierten Trade.
- **Text:** XAIR  ⏎ around 2.08 to 2.13 if you added pay attention to that.
- **Verdict:** _TBD_

### msg 4552 — ACRV (2026-01-15)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Entry: Kein Preis genannt, kein 'placed' Marker, kein TIF. 'Overnight action for ACRV' ist eine vage Ankündigung/Watch/Hinweis, kein platzierter Trade. Sonnet's eigene niedrige Confidence (0.45) bestätigt dies ebenfalls.
- **Text:** Overnight action for ACRV .  ⏎ Enjoy team
- **Verdict:** _TBD_

### msg 4616 — ? (2026-01-16)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker identifizierbar – weder im Text noch im Kontext. Ohne Ticker ist das Signal nicht verwertbar. Sonnet hat bereits korrekt confidence=0.2 gesetzt und ticker=null. Dies sollte als COMMENTARY behandelt werden.
- **Text:** I placed another one at 1.22
- **Verdict:** _TBD_

### msg 4624 — AUID (2026-01-16)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein 'placed' Marker, kein TIF/Ablaufdatum. Die Checkmarks ✅✅✅ deuten auf einen RÜCKBLICK hin – Jack feiert einen bereits erfolgreichen Trade ('nice gift to you all' = Ergebnis, nicht neuer Entry). 1.58 ist hier der erreichte Kurs oder Take-Profit, nicht ein neuer Entry-Preis. Dies ist Commentary/Rückblick, kein Entry-Signal.
- **Text:** Here you go team! ⏎ My Friday nice gift to you all ⏎ AUID 1.58 ✅✅✅
- **Verdict:** _TBD_

### msg 4695 — SXTP (2026-01-22)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Entry-Signal. Kein 'placed', kein TIF/Ablaufdauer, kein klarer Action-Marker. 'SXTP 5:70' ist zu vage – könnte ein Preis-Update, Watch, oder Hinweis sein, aber kein bestätigter Entry. Ohne 'placed an order', 'valid for X minutes' oder ähnliche Formulierung ist das kein qualifizierter Trade-Entry.
- **Text:** Team ⏎ SXTP 5:70
- **Verdict:** _TBD_

### msg 4730 — ? (2026-01-26)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker genannt und kein Kontext verfügbar, um den Ticker zuzuordnen. Ohne Ticker ist dies kein verwertbares Signal. Sonnet hat dies korrekt erkannt (confidence 0.2), aber trotzdem als Entry extrahiert statt zu rejecten.
- **Text:** Placed me another order at 4.75 will see if anything will fill in the next 15 minutes. Remember you always can adjust your entry or exit . I only share ideas here not a copy paste trades.
- **Verdict:** _TBD_

### msg 4766 — HIND (2026-01-27)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist kein neuer Entry, sondern ein STATUS-UPDATE zum bereits platzierten Parent-Trade (Entry war bei 5.85). 'Filled half at 5.55' bedeutet, dass die Hälfte der Position bei 5.55 gefüllt wurde - aber das ist der Fill-Preis eines BESTEHENDEN Orders, nicht ein neuer Entry. Der Original-Entry war bei 5.85 (Parent). Außerdem: 5.55 < 5.85 bedeutet der Kurs ist GEFALLEN seit dem Entry - 'filled half' bei einem niedrigeren Preis als der Entry ergibt keinen Sinn als neuer Long-Entry. Dies ist ein Trade-Management-Update (partial fill + conditional stop), kein neuer platzierter Order.
- **Text:** Filled half at 5.55 . ⏎ If no support above 5 will cut it .
- **Verdict:** _TBD_

### msg 4909 — DKI (2026-02-02)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Die Roh-Nachricht 'Here we go ✅✅✅' ist lediglich ein Status-Update/Bestätigung, dass sich der Trade entwickelt oder dass er eingestiegen ist - aber es ist KEIN eigenständiger Entry-Call. Der Parent-Text sagt 'I am going to risk and get some around 0.62~0.65' - das ist ein Intent/Ankündigung ('going to'), kein 'placed' mit TIF. Die Kombination aus einem vagen Intent im Parent und einem Emoji-Reply ohne Preis/TIF ergibt keinen validen Entry. Kein expliziter 'placed' Marker, kein TIF, keine konkreten Order-Details in der eigentlichen Nachricht.
- **Text:** Here we go ✅✅✅
- **Verdict:** _TBD_

### msg 5096 — ? (2026-02-11)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker in der Nachricht genannt und kein Kontext verfügbar, um den Ticker zu ermitteln. Ohne Ticker ist kein valides Trade-Signal extrahierbar. Sonnet hat dies korrekt erkannt (confidence 0.15), aber dennoch als Entry klassifiziert statt es abzulehnen.
- **Text:** I placed me an order at  ⏎ 2.15 see if any will be filled in the next 20 minutes.
- **Verdict:** _TBD_

### msg 5202 — XWEL (2026-02-24)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Entry: Kein Preis, kein 'placed', kein TIF. 'hot one AH so far' ist eine reine Beobachtung/Rückblick auf After-Hours-Bewegung. Fällt klar unter 'Kein Preis genannt' und 'Rückblick'. Sonnet hat richtigerweise niedrige Confidence, aber es hätte gar nicht als Entry klassifiziert werden sollen.
- **Text:** XWEL hot one AH so far
- **Verdict:** _TBD_

### msg 5268 — ? (2026-02-27)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Kein Ticker angegeben, kein Kontext verfügbar. Zudem beschreibt die Nachricht einen bereits abgeschlossenen Trade (Entry + Exits in Vergangenheitsform), nicht eine neue Order. Dies ist ein Rückblick/Recap, kein Entry-Signal.
- **Text:** Entry around 0.62 ⏎ Two exits around 0.66 ⏎ Final exit 0.71
- **Verdict:** _TBD_

### msg 5331 — MOBX (2026-03-05)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — Dies ist kein neuer Entry/Order. 'I reduced my entry to 0.54~0.61' beschreibt eine Anpassung einer bestehenden Position (er hat bereits Shares bei 0.40 avg laut Parent). Es gibt keinen 'placed'-Marker, kein TIF/Ablaufdatum. 'again not a big order yet' und 'bearish sentiment... might stay low for sometime' deuten auf eine Positionsverwaltung/Kommentar hin, nicht auf ein klares Entry-Signal. Kein actionable Entry für Follower.
- **Text:** I reduced my entry to 0.54~0.61 again not a big order yet . Bearish sentiment into it and it might stay low for sometime.
- **Verdict:** _TBD_

### msg 5409 — LAES (2026-03-16)
- **Stage:** opus → `commentary` (conf 0.3)
- **Opus:** REJECT — This is conditional/intent, NOT a placed order. 'I might add some... if it gets my order at 3.18~3.32 filled' — 'I might' + 'if it gets filled' is clearly conditional. There is no 'placed' marker, no TIF/validity window ('Valid for N minutes'), and no confirmation of execution. The Jack-linguistik rule about 'I might place' requiring a validity timeframe to count as an entry is not met here. This is a watch/intent, not an actionable entry signal.
- **Text:** LAES is dropping pre market  ⏎ I might add some for intra day trade and over night swing if it gets my order at ⏎ 3.18~3.32 filled ⏎ Below 3.00 will be a bearish zone.
- **Verdict:** _TBD_

## haiku_ambiguous (12)

### msg 3462 — OCGN (2025-10-13)
- **Stage:** haiku → `commentary` (conf 0.85)
- **Text:** OCGN
- **Verdict:** _TBD_

### msg 3900 — ADCT (2025-12-03)
- **Stage:** haiku → `commentary` (conf 0.85)
- **Text:** ADCT ⏎ 3.53
- **Verdict:** _TBD_

### msg 4385 — ALMS (2026-01-06)
- **Stage:** haiku → `commentary` (conf 0.75)
- **Text:** ALMS 18
- **Verdict:** _TBD_

### msg 4432 — ? (2026-01-08)
- **Stage:** haiku → `commentary` (conf 0.75)
- **Text:** Two orders at 1.93 and 1.89 no fill yet
- **Verdict:** _TBD_

### msg 4692 — ? (2026-01-22)
- **Stage:** haiku → `commentary` (conf 0.85)
- **Text:** 5.45
- **Verdict:** _TBD_

### msg 4807 — ? (2026-01-28)
- **Stage:** haiku → `commentary` (conf 0.75)
- **Text:** FEED  ⏎ edit my order to  ⏎ 2.19 ⏎ For 3 minutes
- **Verdict:** _TBD_

### msg 4889 — ? (2026-01-30)
- **Stage:** haiku → `commentary` (conf 0.75)
- **Text:** Edit the order to ⏎ 0.74 risky one so far but small amount to risk
- **Verdict:** _TBD_

### msg 4949 — ATOS (2026-02-03)
- **Stage:** haiku → `commentary` (conf 0.65)
- **Text:** Added two orders below 5 ⏎ Shared the plan yesterday!
- **Verdict:** _TBD_

### msg 5087 — RENX (2026-02-11)
- **Stage:** haiku → `commentary` (conf 0.7)
- **Text:** RENX
- **Verdict:** _TBD_

### msg 5247 — ? (2026-02-27)
- **Stage:** haiku → `commentary` (conf 0.7)
- **Text:** Team pay attention to  ⏎ WTI ⏎ BATL
- **Verdict:** _TBD_

### msg 5355 — ASNS (2026-03-09)
- **Stage:** haiku → `commentary` (conf 0.85)
- **Text:** ASNS 0.44
- **Verdict:** _TBD_

### msg 5418 — WNW (2026-03-16)
- **Stage:** sonnet → `commentary` (conf 0.2)
- **Text:** WNW ⏎ 12
- **Verdict:** _TBD_

## disagree_old=entry_new=watchlist (2)

### msg 717 — OCGN (2026-04-10)
- **Stage:** haiku → `watchlist` (conf 0.85)
- **Old Parser:** `entry` / OCGN
- **Text:** OCGN ⏎ below 1.70 will accumulate again. Order valid till  ⏎ End of trading season tonight at  ⏎ 08:00 PM ET US
- **Verdict:** _TBD_

### msg 5592 — ? (2026-04-07)
- **Stage:** blocker → `watchlist` (conf 0.95)
- **Old Parser:** `entry` / ADVB
- **Text:** Good early morning my incredible team here. ⏎ I am taking risk : ⏎ Opening small positions for day trades in : ⏎ ADVB if it gets any order fill for me :  ⏎ Below 7.10 ⏎ And above ⏎ 6.82 ⏎ In coming 45 minutes to 50 minutes.  ⏎ SILO : ⏎ 0.48~0.51 ⏎ Also valid for 45 minutes . ⏎ If nothing filled in this time mentioned. I will wait till after  ⏎ 07:00 AM US ET to check further for new trades and will share by then!
- **Verdict:** _TBD_

## disagree_old=entry_new=exit (1)

### msg 5546 — LAES (2026-03-30)
- **Stage:** haiku → `exit` (conf 0.85)
- **Old Parser:** `entry` / LAES
- **Text:** LAES 2.25 filled for Me. ⏎ Full transparency here!
- **Verdict:** _TBD_

## disagree_old=update_new=entry (1)

### msg 5602 — GEVO (2026-04-07)
- **Stage:** opus → `entry` (conf 0.85)
- **Old Parser:** `update` / GEVO
- **Opus:** APPROVE — Klarer Entry: 'got one order bought for GEVO at 1.97 filled' = bestätigter Kauf (filled) bei 1.97. Ticker, Preis und Action stimmen. Kein SL/TP im Text, korrekt als null. Trade-Type unknown ist akzeptabel da nicht spezifiziert.
- **Text:** I got one order bought for GEVO at ⏎ 1.97 filled
- **Verdict:** _TBD_

## disagree_old=watchlist_new=entry (1)

### msg 5621 — FUSE (2026-04-10)
- **Stage:** opus → `entry` (conf 0.95)
- **Old Parser:** `watchlist` / FUSE
- **Opus:** APPROVE — Classic Jack pattern: 'I might place' + 'Valid for the next 10 minutes only!' = confirmed Entry per Jack-Linguistik rules. Ticker FUSE correct, entry range 1.62~1.67 correctly parsed, trade_type day_trade correct, expiry 10 minutes correct, no SL/TP mentioned so nulls are appropriate.
- **Text:** I might place a small day trade order in FUSE ⏎ 1.62~1.67 ⏎ Valid for the next 10 minutes only!
- **Verdict:** _TBD_

## low_conf_entry=0.20 (1)

### msg 4682 — ? (2026-01-22)
- **Stage:** opus → `entry` (conf 0.2)
- **Opus:** APPROVE — opus error: Expecting value: line 1 column 1 (char 0)
- **Text:** Pre market Day trades: ⏎ IOTR ⏎ placed me an order : ⏎ 6.95 ⏎ Valid for 15 minutes only! ⏎ SXTP ⏎ 4.26 ⏎ Valid for 10 minutes
- **Verdict:** _TBD_

## low_conf_entry=0.30 (1)

### msg 5494 — ? (2026-03-24)
- **Stage:** opus → `entry` (conf 0.3)
- **Opus:** APPROVE — Extraktion ist korrekt. Es ist ein echtes Entry (filled at 0.52) mit explizitem SL bei 0.43. Ticker ist weder in dieser Nachricht noch im Parent-Text genannt, daher null korrekt. Confidence 0.3 ist angemessen wegen fehlendem Ticker – ohne Ticker kann das Signal nicht sinnvoll verwendet werden.
- **Text:** Two small orders filled at  ⏎ 0.52  ⏎ Placed a SL ⏎ at 0.43 will hold if it stays above 0.46
- **Verdict:** _TBD_

## low_conf_entry=0.65 (1)

### msg 4162 — PCSA (2025-12-17)
- **Stage:** opus → `entry` (conf 0.65)
- **Opus:** CORRECT — 6.53 is already filled ('Entered at 6.53') - this is a past action, not a pending order. The actionable entry for followers is the new order at 5.50 with 5-minute expiry. Treating 5.50-6.53 as a range would be incorrect since 6.53 is already executed, not a limit to fill at.
- **Text:** PCSA ⏎ Entered at 6.53 might exit after the halt. ⏎ Placed another order at ⏎ 5.50 will see if it will fill in the next 5 minutes
- **Verdict:** _TBD_

