---
tags: [signal-bot, parser, analyse, phase-1]
date: 2026-04-11
status: completed-draft
---

# Parser-Analyse — 100 Nachrichten Sample

Gezogen aus `raw_messages.db` am 2026-04-11. Stratifiziert über den gesamten Zeitraum — 80 Premium (Okt 2025 → Apr 2026) + 20 Biotech (Feb → Mär 2026).

Analyse von Claude/Opus durchgeführt am 2026-04-11. Klassifikation + Bot-Reaktion + abgeleitete Parser-Regel pro Nachricht.

## Typ-Verteilung

- **STATUS_UPDATE**: 39
- **NO_SIGNAL**: 21
- **MARKET_COMMENT**: 5
- **CANCEL**: 4
- **WATCH_ALERT**: 3
- **ENTRY_ORDER_NO_SL**: 3
- **WATCHLIST**: 3
- **AMBIGUOUS_CONTEXT**: 3
- **EXIT_PARTIAL**: 3
- **ENTRY_ORDER**: 2
- **EXIT_SELL**: 2
- **CONDITIONAL_WATCH**: 2
- **WATCHLIST_INTENT**: 2
- **ENTRY_ORDER_AH_NO_SL**: 1
- **AMBIGUOUS_ADD**: 1
- **COMPLEX_ENTRY**: 1
- **AMBIGUOUS_RESUBMIT**: 1
- **EXIT_PROFIT**: 1
- **EXPIRED_CANCEL**: 1
- **ENTRY_ORDER_RANGE**: 1
- **ENTRY_ORDER_RANGE_NO_SL**: 1

## Kern-Erkenntnisse

Von 100 Nachrichten sind nur **~8-10 klassische Entry-Signale** (ENTRY_ORDER mit vollständiger Struktur). Der Rest verteilt sich auf Status-Updates (~50%), Noise/Chat (~20%), Watchlists/Alerts (~10%), Exits (~5%) und Edge-Cases.

**Wichtigste Parser-Gefahren:**
1. **Status-Updates als Entries missverstehen** (OMEX-Catchup, INHD-Edit — Tickers ohne Order-Struktur)
2. **Kontext-Inferenz aus Vor-Nachrichten** (Ticker aus msg N-1 für msg N nutzen — Race-Risiko)
3. **Alert-Keywords als Entries** (#2 ELBM, #33 MREO — 'price alert' ist KEINE Order)
4. **Konditionale Sätze als Entries** ('if X then I may' = kein Entry)
5. **Marketing-/Service-Ankündigungen mit Ticker-Listen** (#37 Biotech-Group)
6. **Negations** ('not a fill', 'too expensive', 'not to be trusted')
7. **Chart/Bild-Verweise** ohne Text-Substanz

---

## Details pro Nachricht

### #1 — PREM · 2025-10-09T00:21:28+00:00 · msg_id=3439

```
Good evening my great team 
I will be up early tomorrow to scan the market activities for any trades.
Have a wonderful evening!
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Abendgruß, keine Trade-Info.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Nachrichten ohne Ticker und ohne Preis-/SL-Felder → NO_SIGNAL. Greeting-Keywords (Good morning/evening, team, have a, enjoy) als schwaches NO_SIGNAL-Signal.

---

### #2 — PREM · 2025-10-14T10:47:12+00:00 · msg_id=3465

```
ELBM
I placed a price alert at 5.30
Not an order only alert 🚨.
I will keep you posted
```

**Typ:** `WATCH_ALERT` · **Ticker:** ELBM

**Jack meint:** Preis-Alert bei 5.30 gesetzt, explizit KEINE Order.

**Bot-Reaktion:** Nichts tun. Nur loggen.

**Parser-Regel:** KRITISCH: Wenn 'alert' + 'not an order' / 'only alert' / '🚨' → NIEMALS Order platzieren. Parser muss Alert-Keywords hart blockieren, auch wenn Ticker + Preis im Text stehen.

---

### #3 — PREM · 2025-10-15T14:29:42+00:00 · msg_id=3492

```
OCGN
around 1.70 also a successful one 
ℹ️✅ℹ️
```

**Typ:** `STATUS_UPDATE` · **Ticker:** OCGN

**Jack meint:** Rückblickender Erfolgsbericht: 'around 1.70 also a successful one'. Keine neue Entry.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** KRITISCH (OMEX-Catchup-Case): 'around X' + Erfolgs-/Rückblick-Keywords (successful, worked, nice, green, also a, leg up) → STATUS_UPDATE, keine Order. Besonders wenn Emoji-Reihen (✅ℹ️) ohne weitere Struktur.

---

### #4 — PREM · 2025-10-17T13:09:44+00:00 · msg_id=3519

```
Around 1.18 in trading terms can be
From 1.14 up to 1.23 that’s why I said around 1.18 those all suggested and you must edit any numbers based on your budget. 
I said that in multiple comments before here .
Enjoy
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Meta-Erklärung was 'around' bedeutet. Kein konkreter Trade.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Kein Ticker im Text → kein Trade. Meta/Edukations-Texte über Trading-Begriffe erkennen ('in trading terms', 'I said that in', 'you must edit').

---

### #5 — PREM · 2025-10-20T16:10:58+00:00 · msg_id=3545

```
Again team
I am still seeing that the AWS issue is only 60% solved 
As soon as it gets solved will be back fully active here
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Infrastruktur-Update (AWS-Problem).

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Kein Ticker → kein Trade. Keywords 'AWS', 'issue', 'will be back' → META.

---

### #6 — PREM · 2025-10-22T09:26:08+00:00 · msg_id=3572

```
It is being pushed by what so called Meme stocks traders and honestly at this point it is like a lottery ticket. No technical or fundamentals to support the current move other than short squeeze plus major interest in the Retail sector. Most likely it will be a day trade all day long today if I find any levels that might fall under any technical levels will share here but again I may traded it without sharing as in my opinion it is too much volatility and it needs fast action.
```

**Typ:** `MARKET_COMMENT` · **Ticker:** —

**Jack meint:** Allgemeine Meme-Stock-Einordnung, kein Ticker.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Langer Fließtext ohne Ticker → MARKET_COMMENT. Wichtig: Parser darf NICHT Kontext aus vorheriger Nachricht einmischen (Ticker aus msg N-1 nicht auf msg N übertragen).

---

### #7 — PREM · 2025-10-23T14:23:55+00:00 · msg_id=3600

```
SCNX
placed an order at 1.11
SL
1.03 
Valid for 5 minutes 
Day trade
```

**Typ:** `ENTRY_ORDER` · **Ticker:** SCNX

**Jack meint:** BUY SCNX @ 1.11, SL 1.03, gültig 5 Min, Day Trade.

**Bot-Reaktion:** LIMIT BUY SCNX @ 1.11, SL 1.03, TIF 5 Min, Day-Trade-Flag.

**Parser-Regel:** CANONICAL ENTRY: Ticker auf eigener Zeile + 'placed an order at PRICE' + 'SL PRICE' + 'Valid for N minutes' → ENTRY. 'Day trade' = Day-Trade-Flag setzen (schnellere TP, Force-Close vor Close).

---

### #8 — PREM · 2025-10-27T13:49:47+00:00 · msg_id=3626

```
CODX
Day trade:
0.72
SL
0.64
Valid for 5 minutes.
```

**Typ:** `ENTRY_ORDER` · **Ticker:** CODX

**Jack meint:** BUY CODX @ 0.72, SL 0.64, 5 Min, Day Trade.

**Bot-Reaktion:** LIMIT BUY CODX @ 0.72, SL 0.64, TIF 5 Min, Day-Trade-Flag.

**Parser-Regel:** Variante: 'Day trade:' als Header statt Inline. Parser muss beide Varianten erkennen. 'Day trade:' + Preis direkt darunter = Entry-Preis.

---

### #9 — PREM · 2025-10-29T13:35:55+00:00 · msg_id=3653

```
CMBM halted up
Then halted down
```

**Typ:** `STATUS_UPDATE` · **Ticker:** CMBM

**Jack meint:** Halt-Info (up dann down).

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'halted up/down' ohne Preis/Order-Struktur → STATUS_UPDATE. Halt-Keyword blockt Entry-Interpretation.

---

### #10 — PREM · 2025-10-31T16:14:45+00:00 · msg_id=3680

```
Bearish sentiment in the market we have to be careful.
I usually don’t risk much on Fridays
```

**Typ:** `MARKET_COMMENT` · **Ticker:** —

**Jack meint:** Vorsichts-Hinweis für Freitag.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Kein Ticker. Stimmungs-Keywords ('bearish', 'careful', 'don't risk much') → MARKET_COMMENT.

---

### #11 — PREM · 2025-11-05T18:55:15+00:00 · msg_id=3706

```
MTC nice ✅ℹ️✅
```

**Typ:** `STATUS_UPDATE` · **Ticker:** MTC

**Jack meint:** Erfolgsmeldung zu bestehender Position.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Ticker + 'nice' + Emoji-Reihe OHNE Preise/SL → STATUS_UPDATE. Nie als Entry interpretieren.

---

### #12 — PREM · 2025-11-12T17:52:52+00:00 · msg_id=3733

```
LPTX halted up again
```

**Typ:** `STATUS_UPDATE` · **Ticker:** LPTX

**Jack meint:** Halt-Info.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Wie #9. 'halted' = Status, nie Entry.

---

### #13 — PREM · 2025-11-17T18:19:56+00:00 · msg_id=3760

```
OMER green for me team.
```

**Typ:** `STATUS_UPDATE` · **Ticker:** OMER

**Jack meint:** PnL-Meldung ('green for me').

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Ticker + 'green' / 'red' / 'up' / 'down' + 'for me' → STATUS_UPDATE.

---

### #14 — PREM · 2025-11-24T17:14:22+00:00 · msg_id=3786

```
INHD omg 😳.. Leg up ✅✅
```

**Typ:** `STATUS_UPDATE` · **Ticker:** INHD

**Jack meint:** Celebration/Status zu bestehender Position ('Leg up').

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** KRITISCH (INHD-Edit-Case aus Roadmap): Ticker + 'omg' / '😳' / 'leg up' / Emoji-Spam → STATUS_UPDATE. 'Leg up' = die Aktie läuft weiter, NICHT neuer Entry.

---

### #15 — PREM · 2025-11-26T13:32:39+00:00 · msg_id=3813

```
AMBR got a good earning pre market 
I placed an order at 2.18 valid for 4 minutes for a possible trade.
```

**Typ:** `ENTRY_ORDER_NO_SL` · **Ticker:** AMBR

**Jack meint:** BUY AMBR @ 2.18, 4 Min, kein expliziter SL. Earning-Kontext.

**Bot-Reaktion:** Vorschlag: Entry platzieren MIT Default-SL (z.B. TRAILING_SL_PERCENT aus config) oder skippen + Telegram-Alert für manuellen Entscheid.

**Parser-Regel:** WICHTIG: Entry-Signal ohne SL ist häufig. Policy-Entscheidung nötig: (A) Default-SL auto-setzen (z.B. -5%), (B) skippen + alerten, (C) kleinere Position. Empfehlung: Alert + skip bis manuell entschieden — SL-lose Entries sind Live-Risiko.

---

### #16 — PREM · 2025-12-01T12:05:48+00:00 · msg_id=3840

```
CNEY traded it from 2.09 to 2.13 and fully closed
I mentioned the major risk and it dropped below the 2 minutes support so it is a bearish zone . 
100% accurate predictions in it so far.
```

**Typ:** `STATUS_UPDATE` · **Ticker:** CNEY

**Jack meint:** Rückblick: 'traded it from 2.09 to 2.13 and fully closed'.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'traded it from X to Y', 'fully closed' → STATUS_UPDATE. Past tense + Erfolgsbewertung = rückblickend.

---

### #17 — PREM · 2025-12-01T22:19:05+00:00 · msg_id=3866

```
TAOP
After hours 
I placed an order at 
3.35
Valid for 
6 minutes
```

**Typ:** `ENTRY_ORDER_AH_NO_SL` · **Ticker:** TAOP

**Jack meint:** BUY TAOP @ 3.35 After Hours, 6 Min, kein SL genannt.

**Bot-Reaktion:** LIMIT BUY TAOP @ 3.35 mit outsideRth=True (Track B), 6 Min TIF. SL-Problem wie #15.

**Parser-Regel:** KRITISCH: 'After hours' / 'Pre market' / 'AH' / 'PM' → outsideRth=True Flag setzen (Track B). Plus SL-lose-Entry-Policy wie #15.

---

### #18 — PREM · 2025-12-03T17:20:23+00:00 · msg_id=3893

```
I filled some 
Placed another order at 2.83 and 2.79
No more for today .
Might add more this week 
Planning to hold for 25% to 30% profit .
```

**Typ:** `AMBIGUOUS_ADD` · **Ticker:** —

**Jack meint:** Fügt zur bestehenden Position nach: weitere Orders @ 2.83 und 2.79. Ticker nur aus Kontext.

**Bot-Reaktion:** Skip + Alert. Multi-Preis-Adds und Kontext-Abhängigkeit sind zu fragil für Auto-Execution.

**Parser-Regel:** KRITISCH: Nachrichten ohne eigenen Ticker ('I filled some', 'Placed another', 'this is still valid') → AMBIGUOUS. NIEMALS Ticker aus vorheriger Nachricht inferieren — Race-Condition-Risiko. Policy: skippen + loggen.

---

### #19 — PREM · 2025-12-05T13:12:55+00:00 · msg_id=3921

```
I saw that big move in SMX . The same stock I mentioned here last week and Monday but the issue:
The price tag for it is too high I can personally trade it and few others but it will not be fair for my team members who don’t have much liquidity.
That’s why I focus in what I share here on stocks that’s fit most of everyone time and budget.
```

**Typ:** `NO_SIGNAL` · **Ticker:** SMX

**Jack meint:** Erwähnt SMX aber sagt explizit: zu teuer, nicht handelbar für Team.

**Bot-Reaktion:** Nichts tun — explizit kein Entry.

**Parser-Regel:** KRITISCH: 'too high', 'not fair for team', 'I can personally but' → expliziter Non-Trade. Parser muss 'Ticker erwähnt ≠ Entry' verstehen. Negations-Keywords blocken Entry.

---

### #20 — PREM · 2025-12-05T23:56:11+00:00 · msg_id=3947

```
My great team
TWG as a low float and it moved big tonight AH.
I am planning to keep it in my top watch list for Monday pre market. 
I know I keep bugging you but I am sharing here everything I think 🤔 might be beneficial for us.
```

**Typ:** `WATCHLIST` · **Ticker:** TWG

**Jack meint:** Watchlist-Eintrag für Montag, kein aktuelles Order.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Keywords 'watch list', 'planning to keep', 'might', 'for Monday/tomorrow' → WATCHLIST. Kein Entry. Keine Zukunfts-Orders.

---

### #21 — PREM · 2025-12-08T15:36:29+00:00 · msg_id=3974

```
This is still valid
```

**Typ:** `AMBIGUOUS_CONTEXT` · **Ticker:** —

**Jack meint:** 'This is still valid' — Referenz auf eine frühere Nachricht.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Nachrichten ohne Ticker und ohne Struktur → AMBIGUOUS. Bot darf sich nicht auf Kontext stützen.

---

### #22 — PREM · 2025-12-09T13:16:58+00:00 · msg_id=4001

```
XCUR got to 8.11 lowest after my alert 🔔 here then rebound to 9.50
```

**Typ:** `STATUS_UPDATE` · **Ticker:** XCUR

**Jack meint:** Rückblick auf Kursbewegung nach Alert.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'got to X after my alert' → STATUS_UPDATE (retrospektiv).

---

### #23 — PREM · 2025-12-09T21:33:25+00:00 · msg_id=4027

```
Another mover with high price tag 
IPW
so far it is above 21 AH .
```

**Typ:** `MARKET_COMMENT` · **Ticker:** IPW

**Jack meint:** Mover-Hinweis, 'high price tag' = nicht handelbar.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'another mover', 'so far it is above X AH' ohne 'placed an order' → MARKET_COMMENT. 'High price tag' als zusätzlicher Block.

---

### #24 — PREM · 2025-12-10T16:30:16+00:00 · msg_id=4054

```
POM no support needed to cut it all . I need my day trade money so I am not interested to hold . It may recover later who knows but in my criteria and my budget I need to keep special budget for each trade.
An example:
I have 1 k to use in it
Max pain 500 
If it gets below 500 loss I cut 
If it stays above the max pain I keep .
I don’t use more than my budget no matter what .
Each trade with budget 
My personal preference only you must find your strategy
```

**Typ:** `EXIT_SELL` · **Ticker:** POM

**Jack meint:** 'no support needed to cut it all' — schließt POM komplett.

**Bot-Reaktion:** SELL POM (falls Position offen), ganze Position.

**Parser-Regel:** KRITISCH: 'cut it all', 'cut all', 'fully out', 'closed it', 'cutting' → EXIT_SELL. Unterscheidung 'cut' (Exit) vs 'cut losses' (gleicher Exit, anderes Framing).

---

### #25 — PREM · 2025-12-11T23:43:55+00:00 · msg_id=4081

```
Good evening my team.
I honestly don’t see anything worth the risk AH tonight.
Most likely will keep my buy power for tomorrow.
TLRY is moving but volume is weak AH and not to be trusted.
I will keep you posted ✅✅ℹ️✅✅!
```

**Typ:** `NO_SIGNAL` · **Ticker:** TLRY

**Jack meint:** Erwähnt TLRY aber sagt explizit: 'volume weak, not to be trusted'.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'not to be trusted', 'weak volume', 'I honestly don't see' → Non-Trade. Negations vor Ticker/nach Ticker beachten.

---

### #26 — PREM · 2025-12-15T10:19:47+00:00 · msg_id=4107

```
Good morning my great team here.
I am currently scanning the pre market activities for any major opportunities.
I will keep you posted!
The best of luck for this week ✅✅ℹ️✅✅!
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Morgens-Gruß, noch am Scannen, keine konkrete Opportunity.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'scanning for opportunities', 'will keep you posted', 'best of luck' → NO_SIGNAL Boilerplate.

---

### #27 — PREM · 2025-12-16T13:43:17+00:00 · msg_id=4135

```
Extended the time for another 3 minutes
```

**Typ:** `AMBIGUOUS_CONTEXT` · **Ticker:** —

**Jack meint:** TIF-Verlängerung um 3 Min — bezieht sich auf vorherige Order.

**Bot-Reaktion:** Skippen + Alert. TIF-Extends ohne Ticker sind zu kontextabhängig.

**Parser-Regel:** KRITISCH: 'Extended the time', 'for another N minutes', 'still valid' ohne Ticker → AMBIGUOUS. Bot implementiert besser einen separaten 'extend' Telegram-Command manuell statt aus Chat zu parsen.

---

### #28 — PREM · 2025-12-17T15:03:38+00:00 · msg_id=4162

```
PCSA
Entered at 6.53 might exit after the halt.
Placed another order at
5.50 will see if it will fill in the next 5 minutes
```

**Typ:** `COMPLEX_ENTRY` · **Ticker:** PCSA

**Jack meint:** Bereits in Position @ 6.53. Zusätzliche Limit-Order @ 5.50 für 5 Min. 'might exit after halt' ist konditional, keine Aktion.

**Bot-Reaktion:** Wenn PCSA-Position noch nicht offen: skippen (entry war retrospektiv). Wenn neue Limit-Order-Struktur erkennbar: LIMIT BUY @ 5.50 für 5 Min zusätzlich.

**Parser-Regel:** KRITISCH (Mix-Case): 'Entered at X' = past-tense Fill-Report (KEINE neue Order). 'Placed another order at Y' = neue Order. Parser muss beide Segmente getrennt behandeln. Ohne SL → SL-Policy anwenden.

---

### #29 — PREM · 2025-12-19T13:18:27+00:00 · msg_id=4188

```
Good morning my great team .
So far PRPH pre market mover with a small price tags.
I am watching it more for my possible price levels trade plan.
```

**Typ:** `WATCHLIST` · **Ticker:** PRPH

**Jack meint:** Pre-Market-Mover-Beobachtung, 'possible trade plan'.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'watching it more', 'possible', 'trade plan', 'might' → WATCHLIST. Konjunktive Formulierung = kein Entry.

---

### #30 — PREM · 2025-12-22T17:13:14+00:00 · msg_id=4215

```
Good afternoon again my great team.
I am scanning again some market activities to find any opportunities!
Enjoy ✅
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Nachmittags-Gruß, noch am Scannen.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #26.

---

### #31 — PREM · 2025-12-23T22:55:43+00:00 · msg_id=4242

```
PCLA my team
I am securing half out at 0.307 filled
```

**Typ:** `EXIT_PARTIAL` · **Ticker:** PCLA

**Jack meint:** 'securing half out at 0.307 filled' → 50% der Position @ 0.307 verkauft.

**Bot-Reaktion:** SELL 50% PCLA-Position @ market (Fill ist bereits erfolgt — Bot soll eigene Position synchronisieren).

**Parser-Regel:** KRITISCH: 'half out', 'securing half', 'sold half', 'cut half' → EXIT_PARTIAL 50%. 'filled' = bestätigter Fill, nicht neue Order. Bot sollte sofort 50% der offenen Position schließen (marktnah Limit).

---

### #32 — PREM · 2025-12-24T21:31:03+00:00 · msg_id=4269

```
I wish you all a wonderful Christmas Eve and a peaceful holiday’s season!

I wish we could put up some of the Christmas spirit in jars and open a jar of it every month.”
— Harlan Miller-
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Weihnachts-Gruß mit Zitat.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Seasonal/Gruß-Texte → NO_SIGNAL.

---

### #33 — PREM · 2025-12-29T16:17:07+00:00 · msg_id=4296

```
MREO dropped 91% with data.
I usually look at those for any possible dead cat bounces when they reach certain levels.
I placed a price alert 🔔 in my brokerage at 0.18 will watch from there
```

**Typ:** `WATCH_ALERT` · **Ticker:** MREO

**Jack meint:** Price-Alert @ 0.18 in Brokerage, 'will watch'. KEINE Order.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'price alert 🔔', 'in my brokerage', 'will watch from there' → WATCH_ALERT. Wie #2 — Alert ≠ Order.

---

### #34 — PREM · 2025-12-31T16:01:48+00:00 · msg_id=4323

```
For anyone used this info pay attention 
ANGH up good from the suggested level in case you hold it
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ANGH

**Jack meint:** Rückblickende Bestätigung einer früheren Empfehlung.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'pay attention', 'from the suggested level', 'in case you hold it' → STATUS_UPDATE retrospektiv. Keywords 'suggested level' = frühere Nachricht, nicht neue Order.

---

### #35 — PREM · 2026-01-05T13:01:17+00:00 · msg_id=4349

```
IMRX 
I am still holding 60% of what I got last week . I am hoping to get some profit today or tomorrow at most will see!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** IMRX

**Jack meint:** Hält 60% der Position aus letzter Woche, hofft auf Profit.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'still holding X% of what I got', 'hoping' → STATUS_UPDATE. Position existiert bereits.

---

### #36 — PREM · 2026-01-06T13:25:51+00:00 · msg_id=4376

```
This is how I day trade ..
No panic no rush no blah blah fake hype!
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Philosophie, kein Trade.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Meta-Kommentare zur eigenen Trading-Philosophie → NO_SIGNAL.

---

### #37 — PREM · 2026-01-07T12:58:50+00:00 · msg_id=4403

```
Good morning team again:
Please read this:
I will be soon creating a special group only for some important biotech stocks.
If you are already a VIP member in my email group you will be automatically included at no charge.
If you are not the group will be in quarterly based fees ( 3 months fee ) the first 100 to join will get a 70% discount ( special deal very special) 
I will share in the group regular daily and hourly updates ( all possible chart indicators, news , trading plans , volume analysis and more ) about the most publicly traded biotech stocks : 
SLS SELLAS 
ALT
AKBA
ATOS
AQST
and others!
It will be a unique opportunity and only for limited time!
If you are interested and please only serious traders to contact me to my emails:
Jsparo7396@gmail.com
Jsparo7397@gmail.com
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Marketing für neue Biotech-Gruppe, enthält Ticker-Liste aber keine Orders.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** KRITISCH: Ticker-Aufzählungen in Marketing-/Service-Ankündigungen dürfen NIEMALS als Signale interpretiert werden. Keywords 'VIP member', 'quarterly fees', 'email me', 'special deal' → Service-Ankündigung. Parser-Schutz: mehrere Ticker in einer Nachricht + kein Preis → NO_SIGNAL.

---

### #38 — PREM · 2026-01-08T18:02:55+00:00 · msg_id=4429

```
IMRX
If we open the best book that been written by the best traders around they could not play it the way we did team.
I shared a full plan about it last week when it was around 6.50 to 6.35
It went up yesterday to 8.40
I told you here clearly what I am doing and why it is too important to secure profit.
Please check back the messages here about it!
Today IMRX in a big sell off I might share a new plan about it but I am not in rush !
```

**Typ:** `STATUS_UPDATE` · **Ticker:** IMRX

**Jack meint:** Narrative über IMRX-Verlauf, deutet 'new plan' an aber platziert keine Order.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'might share a new plan', 'not in rush', narrative past-tense → STATUS_UPDATE. Kein Entry bis explizite Order-Struktur erscheint.

---

### #39 — PREM · 2026-01-11T23:20:29+00:00 · msg_id=4457

```
Good evening my wonderful team.
Next week I am expecting a lot of volatility in the market. Which means more opportunities ✅✅!
I will keep you posted ✅!
Always love and respect to all of you . Please never hesitate to reach out with any inquiries!
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Abendgruß + Ausblick.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #1.

---

### #40 — PREM · 2026-01-12T19:24:47+00:00 · msg_id=4484

```
EVTV halted up again ℹ️
```

**Typ:** `STATUS_UPDATE` · **Ticker:** EVTV

**Jack meint:** Halt-Info.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Wie #9.

---

### #41 — PREM · 2026-01-13T20:13:31+00:00 · msg_id=4511

```
Closed the rest of XAIR at 2.23 and turned my attention to ATON.
```

**Typ:** `EXIT_SELL` · **Ticker:** XAIR

**Jack meint:** 'Closed the rest of XAIR at 2.23' → Restposition verkauft. ATON nur als Hinweis, kein Entry.

**Bot-Reaktion:** SELL alle verbleibenden XAIR-Shares. ATON: nichts tun.

**Parser-Regel:** KRITISCH: 'Closed the rest of', 'closed remaining', 'sold remaining' → EXIT_SELL der ganzen Restposition. Mehrere Ticker in einer Nachricht: nur der explizit mit Action verbundene Ticker wird getradet ('turned attention to' = Watchlist, kein Entry).

---

### #42 — PREM · 2026-01-14T16:21:28+00:00 · msg_id=4539

```
It was unbelievable how it got filled and up in 3 seconds that’s insane team
```

**Typ:** `STATUS_UPDATE` · **Ticker:** —

**Jack meint:** Ausruf über schnellen Fill der vorherigen Order.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Kein Ticker + emotional ('insane', 'unbelievable') → STATUS_UPDATE.

---

### #43 — PREM · 2026-01-15T15:23:24+00:00 · msg_id=4566

```
AUID got to 2.31
Sold 15% out from the 25% left at 2.22
Keeping that last 10%
```

**Typ:** `EXIT_PARTIAL` · **Ticker:** AUID

**Jack meint:** Verkauft 15% @ 2.22 (aus den 25% die noch offen waren). 10% bleiben.

**Bot-Reaktion:** SELL 15% der AUID-Position @ ~2.22. Prozentsatz bezieht sich auf ursprüngliche Position, nicht aktuelle.

**Parser-Regel:** KRITISCH: Prozentsätze in Exit-Nachrichten sind relativ zur URSPRÜNGLICHEN Position, nicht zur aktuell verbleibenden. 'Sold X% out from the Y% left' → X% der Original-Position abbauen. Das ist fragil — Bot sollte Original-Shares-Count in DB tracken (ist bereits `shares` vs `remaining_shares`).

---

### #44 — PREM · 2026-01-16T13:02:42+00:00 · msg_id=4593

```
VERO 
Pay attention I brought back my previous order:
This one valid for 5 minutes
```

**Typ:** `AMBIGUOUS_RESUBMIT` · **Ticker:** VERO

**Jack meint:** 'brought back my previous order... valid for 5 minutes' — reichen vorigen Order wieder ein, kein expliziter Preis/SL.

**Bot-Reaktion:** Skippen + Alert. Preis fehlt — zu fragil.

**Parser-Regel:** 'brought back', 'previous order', 'resubmitted' ohne explizite Preise → AMBIGUOUS. Preis-Inferenz aus früherer Nachricht = Race-Risiko.

---

### #45 — PREM · 2026-01-16T18:09:04+00:00 · msg_id=4619

```
AUID
1.28
1.22 all filled 
Let’s us see by next week what it does!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** AUID

**Jack meint:** Fill-Report: @ 1.28 und 1.22 beide gefüllt (multi-entry fill rückblickend).

**Bot-Reaktion:** Nichts tun (Fills sind historisch).

**Parser-Regel:** 'all filled' + multiple Preise ohne 'placed an order at' → STATUS_UPDATE retrospektiv. Past-tense Fill-Report.

---

### #46 — PREM · 2026-01-20T14:21:12+00:00 · msg_id=4646

```
Anyone used my alert about IVF as a day trades  made good money 💰 ..
I will keep scanning the market for any opportunities but again my style in trading is about:
Entry
Exit 
And real trades.
Some group front load their members and they claim fake wins over them. I never and don’t need this type of unprofessional behavior!
```

**Typ:** `NO_SIGNAL` · **Ticker:** IVF

**Jack meint:** IVF rückblickend erwähnt, Rest ist Philosophie/Rant.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'Anyone used my alert about X' → retrospektive Frage, kein Entry. Rant-Keywords ('fake hype', 'front load') → NO_SIGNAL.

---

### #47 — PREM · 2026-01-21T16:13:50+00:00 · msg_id=4673

```
ACRV beautiful swing team.
Remember when I shared it was around or close to great entry levels. Those trades are real money makers!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ACRV

**Jack meint:** 'beautiful swing' + 'remember when I shared' — retrospektive Erfolgsmeldung.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'beautiful swing', 'real money makers', 'remember when' → STATUS_UPDATE retrospektiv.

---

### #48 — PREM · 2026-01-22T14:31:58+00:00 · msg_id=4699

```
The 25% I left sold at 7.80 ✅✅✅
```

**Typ:** `AMBIGUOUS_CONTEXT` · **Ticker:** —

**Jack meint:** 'The 25% I left sold at 7.80' — kontextabhängiger Exit der letzten Tranche, kein Ticker.

**Bot-Reaktion:** Skippen + Alert (kein Ticker). ODER: manuell via 'sell TICKER'-Command schließen.

**Parser-Regel:** Exit-Reports ohne Ticker → AMBIGUOUS. Policy: Bot trackt eigenen State und schließt bei 'sell TICKER' Telegram-Command (bereits implementiert).

---

### #49 — PREM · 2026-01-26T11:40:38+00:00 · msg_id=4726

```
BATL broke up another resistance
```

**Typ:** `STATUS_UPDATE` · **Ticker:** BATL

**Jack meint:** Resistance-Break-Info.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'broke up', 'broke through', 'broke resistance' → STATUS_UPDATE. Technische Beobachtung, kein Entry.

---

### #50 — PREM · 2026-01-26T21:53:25+00:00 · msg_id=4753

```
PHGE
Low float moving AH.
If it gets below 7.20 and stays above 6.88 in the coming 15 minutes I may get some .
```

**Typ:** `CONDITIONAL_WATCH` · **Ticker:** PHGE

**Jack meint:** Konditionale Beobachtung: 'If it gets below 7.20 AND stays above 6.88 in the next 15 min I may get some' — keine Order platziert.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** KRITISCH: Konditionale Sätze ('If X then I may', 'If it goes to Y') → kein Entry. 'may get some', 'might add' = Unsicherheit. Nur reaktive Orders platzieren wenn Jack explizit 'placed an order at X' sagt, nicht konditional.

---

### #51 — PREM · 2026-01-27T22:37:10+00:00 · msg_id=4779

```
WTI
Still holding it.
I am expecting it to give me more soon . Oil prices will soar up in my personal opinion in the coming few weeks. If you want to secure profit not bad remember I shared my idea about it when it was below 1.80
```

**Typ:** `STATUS_UPDATE` · **Ticker:** WTI

**Jack meint:** Hält WTI, Hold-Kommentar, Öl-Makro-These, retrospektiver Entry-Hinweis.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'Still holding', 'expecting it to give me more', 'remember I shared' → STATUS_UPDATE. Makro-Kommentar + Retrospektive.

---

### #52 — PREM · 2026-01-28T16:00:32+00:00 · msg_id=4806

```
Day trade alert 🔔 for
FEED
Placed an order at 1.78 for 7 minutes
```

**Typ:** `ENTRY_ORDER_NO_SL` · **Ticker:** FEED

**Jack meint:** Day-Trade-Alert FEED: BUY @ 1.78 für 7 Min. Kein SL.

**Bot-Reaktion:** LIMIT BUY FEED @ 1.78, TIF 7 Min, Day-Trade-Flag, SL-Policy (Default oder Skip).

**Parser-Regel:** 'Day trade alert 🔔 for TICKER\nPlaced an order at X for Y minutes' = Entry-Variante. 🔔 hier IST Teil des Entries (nicht Alert-only wie #2) — Unterscheidung: 'alert for + Order-Struktur' vs 'price alert... not an order'.

---

### #53 — PREM · 2026-01-29T14:53:57+00:00 · msg_id=4833

```
Moved from 3.66 time of sharing the post to 4.55
```

**Typ:** `STATUS_UPDATE` · **Ticker:** —

**Jack meint:** Retrospektive Kursbewegung 3.66 → 4.55.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'Moved from X to Y', 'time of sharing' → STATUS_UPDATE retrospektiv, ohne Ticker auch kein Kontext.

---

### #54 — PREM · 2026-01-29T21:50:28+00:00 · msg_id=4859

```
Team again
Entry levels always you can adjust 
Like
1.18
Then 
1.22 will be fine
Below or above by little Margin
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Meta-Erklärung über 'Entry levels kann man anpassen'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Edukation/Meta ohne Ticker → NO_SIGNAL. 'Entry levels always you can adjust' = Regel-Erklärung.

---

### #55 — PREM · 2026-01-30T20:28:58+00:00 · msg_id=4886

```
ELPW!!!
2500% mover!!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ELPW

**Jack meint:** Begeisterte Erwähnung eines 2500% Movers, keine Order.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Ticker + Bewunderungs-Ausrufe ('!!!', 'X% mover') ohne Preis/Order-Struktur → STATUS_UPDATE / kein Entry.

---

### #56 — PREM · 2026-02-02T11:56:47+00:00 · msg_id=4913

```
DKI
0.87 from entry around 0.66 ✅✅
```

**Typ:** `STATUS_UPDATE` · **Ticker:** DKI

**Jack meint:** PnL-Report: DKI @ 0.87 vom Entry around 0.66.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'X from entry around Y' + ✅ → retrospektiver PnL-Report. Past-tense Struktur.

---

### #57 — PREM · 2026-02-02T23:21:51+00:00 · msg_id=4939

```
No entry being reached even with flexing the possibility.
I will place a price alert 🔔 at 3.10 valid for the next 30 minutes and watch from there
```

**Typ:** `WATCH_ALERT` · **Ticker:** —

**Jack meint:** Kein Fill erreicht → Price-Alert bei 3.10 für 30 Min statt Order.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'No entry being reached', 'will place a price alert 🔔' → WATCH_ALERT. Unterscheidung: 'price alert' = Beobachtung, 'alert for + order' = Entry.

---

### #58 — PREM · 2026-02-04T15:03:13+00:00 · msg_id=4966

```
MAMO 
My SL there around 1 
So far still holding. Might add little more if I do any other profitable day trade!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** MAMO

**Jack meint:** Hält MAMO, SL 'around 1', 'might add more' konditional.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'still holding', 'my SL there around X', 'might add' → STATUS_UPDATE + konditionaler Add. 'around' beim SL = unpräziser Richtwert, Bot sollte bestehenden SL nicht ändern aus so einer Nachricht.

---

### #59 — PREM · 2026-02-06T15:46:52+00:00 · msg_id=4993

```
No fill no trade . 
I am looking into SMX halted up so far .
```

**Typ:** `NO_SIGNAL` · **Ticker:** SMX

**Jack meint:** 'No fill no trade' + SMX-Beobachtung.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'No fill no trade' = expliziter Nicht-Trade. 'Looking into X halted' = Beobachtung.

---

### #60 — PREM · 2026-02-09T14:41:06+00:00 · msg_id=5019

```
UOKA got another halt up
```

**Typ:** `STATUS_UPDATE` · **Ticker:** UOKA

**Jack meint:** Halt-Info.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #9.

---

### #61 — PREM · 2026-02-09T20:59:19+00:00 · msg_id=5046

```
BRLS team let us secure that nice profit
```

**Typ:** `EXIT_PROFIT` · **Ticker:** BRLS

**Jack meint:** 'let us secure that nice profit' — möchte Profit sichern.

**Bot-Reaktion:** Vorschlag: Position schließen (komplett oder teilweise). Wenn nicht quantifiziert → Komplett-Exit.

**Parser-Regel:** KRITISCH: 'let us secure', 'securing profit', 'take profit' → EXIT_PROFIT. Wenn keine Prozent-Angabe: Default = 100% Exit. Bei 'securing half/part' = partial.

---

### #62 — PREM · 2026-02-10T17:46:35+00:00 · msg_id=5073

```
QNCX the one mentioned here when it was around 0.28 now 0.42
```

**Typ:** `STATUS_UPDATE` · **Ticker:** QNCX

**Jack meint:** Retrospektive Erfolgsmeldung 0.28 → 0.42.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'the one mentioned here when it was around X now Y' → STATUS_UPDATE retrospektiv.

---

### #63 — PREM · 2026-02-11T20:53:31+00:00 · msg_id=5099

```
Time out for NCI! No open orders!
```

**Typ:** `EXPIRED_CANCEL` · **Ticker:** NCI

**Jack meint:** 'Time out for NCI! No open orders!' → TIF abgelaufen, keine offenen Orders mehr.

**Bot-Reaktion:** Order cancellieren (bzw. ist schon expired via TIF). Keine Aktion nötig wenn TIF korrekt gesetzt war.

**Parser-Regel:** 'Time out', 'no open orders' → ORDER_EXPIRED-Bestätigung. Bot sollte seinerseits bestehende pending Orders des Tickers canceln (Sicherheitsnetz).

---

### #64 — PREM · 2026-02-17T13:39:29+00:00 · msg_id=5126

```
OLB
Placed me an order at
0.74 
For next 10 minutes
```

**Typ:** `ENTRY_ORDER_NO_SL` · **Ticker:** OLB

**Jack meint:** BUY OLB @ 0.74 für 10 Min. Kein SL.

**Bot-Reaktion:** LIMIT BUY OLB @ 0.74, TIF 10 Min. SL-Policy.

**Parser-Regel:** Variante: 'Placed me an order at X\nFor next N minutes'. Typo 'placed me' (Jack-Eigenart) — Parser darf sich nicht an 'I placed' klammern, 'placed' als Keyword reicht.

---

### #65 — PREM · 2026-02-19T15:15:36+00:00 · msg_id=5153

```
KNRX 
I placed me a day trade order at 2.68~2.73
For the next 10 minutes
```

**Typ:** `ENTRY_ORDER_RANGE` · **Ticker:** KNRX

**Jack meint:** BUY KNRX @ 2.68~2.73 (Range) für 10 Min, Day Trade.

**Bot-Reaktion:** LIMIT BUY KNRX bei Range-Mitte (2.705) ODER zwei separate Limit-Orders. Vorschlag: eine Limit @ oberem Ende 2.73 (aggressiv fill).

**Parser-Regel:** KRITISCH: Preis-Ranges 'X~Y' oder 'X to Y' → Policy-Entscheidung. Empfehlung: Limit Order @ oberem Ende (aggressiver Fill, da Jack meistens bullish Entry will). Alternative: Range-Mitte. 'Day trade' Keyword auch hier möglich.

---

### #66 — PREM · 2026-02-23T14:59:57+00:00 · msg_id=5181

```
TIRX:
Entry around 0.0975 all reached you saw it
It got to above 0.11
Easy trade a stock that everyone can afford to trade!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** TIRX

**Jack meint:** Retrospektiver Entry-Report: 'entry around 0.0975 all reached' + Erfolgsmeldung.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'Entry around X all reached' + 'it got to above Y' + 'easy trade' → STATUS_UPDATE retrospektiv. Past-tense Fill-Bestätigung.

---

### #67 — PREM · 2026-02-24T22:36:30+00:00 · msg_id=5208

```
Team risky move but it might be worth it!
I am going to add some
WTI 
BATL
tonight.
There are rumors of a possible attack this week on Iran or by this coming weekend it might push the Oil price higher!
Risky move so will use some not going to use much capital!
```

**Typ:** `WATCHLIST_INTENT` · **Ticker:** WTI,BATL

**Jack meint:** 'I am going to add some WTI BATL tonight' — Absicht, noch keine Order platziert.

**Bot-Reaktion:** Nichts tun. Vielleicht logging.

**Parser-Regel:** KRITISCH: 'I am going to', 'planning to add', 'will add' → FUTURE_INTENT, noch kein Entry. Nur wenn später explizite 'Placed an order at X' Nachricht kommt. Auch: mehrere Ticker in einer Nachricht → Mehrdeutigkeit.

---

### #68 — PREM · 2026-02-26T15:47:43+00:00 · msg_id=5236

```
Cancelled my order as it passed the time vs volume that I need to trade
```

**Typ:** `CANCEL` · **Ticker:** —

**Jack meint:** Hat Order gecancelt (Timing/Volume passte nicht).

**Bot-Reaktion:** Nichts tun (wenn TIF korrekt war, ist Order schon abgelaufen).

**Parser-Regel:** 'Cancelled my order', 'passed the time' → CANCEL_CONFIRM. Bot sollte eigene pending Orders canceln wenn Ticker-Kontext klar ist — ohne Ticker: skip.

---

### #69 — PREM · 2026-02-27T13:45:45+00:00 · msg_id=5262

```
Don’t ever look back at a trade after you sell unless you want to recover with a plan not a fomo
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Trading-Philosophie über FOMO.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #36.

---

### #70 — PREM · 2026-03-02T14:10:10+00:00 · msg_id=5290

```
TPET again new high pre market team ✅
```

**Typ:** `STATUS_UPDATE` · **Ticker:** TPET

**Jack meint:** 'new high pre market' + ✅.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'new high', 'again' + ✅ ohne Preise → STATUS_UPDATE.

---

### #71 — PREM · 2026-03-03T17:04:54+00:00 · msg_id=5318

```
MOBX 0.72 got there now 0.70 what a day!
I will appreciate your support in Stocktwits it helps me bring more serious traders to our great group!
God bless you all 🙏
```

**Typ:** `STATUS_UPDATE` · **Ticker:** MOBX

**Jack meint:** PnL + Stocktwits-Werbung.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'X got there now Y' + 'what a day' + Social-Media-Bitte → STATUS_UPDATE + Rauschen.

---

### #72 — PREM · 2026-03-06T14:46:04+00:00 · msg_id=5344

```
PRSO order already canceled pre market. I will evaluate if I am interested to open a new order I will keep you posted
```

**Typ:** `CANCEL` · **Ticker:** PRSO

**Jack meint:** PRSO Order gecancelt. 'Might share new order'.

**Bot-Reaktion:** Eigene PRSO-Pending-Orders canceln.

**Parser-Regel:** 'order already canceled' + Ticker → CANCEL_CONFIRM mit Ticker. Bot sollte eigene pending Orders für diesen Ticker canceln.

---

### #73 — PREM · 2026-03-10T14:22:18+00:00 · msg_id=5371

```
LGVN interested move
Might share a trade soon .
```

**Typ:** `WATCHLIST_INTENT` · **Ticker:** LGVN

**Jack meint:** 'Might share a trade soon' = Absicht.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'interested move', 'might share soon' → FUTURE_INTENT, kein Entry.

---

### #74 — PREM · 2026-03-12T15:39:22+00:00 · msg_id=5398

```
Cancelled but still evaluating any further order . No more open orders in it so far
```

**Typ:** `CANCEL` · **Ticker:** —

**Jack meint:** Cancel-Bestätigung, ohne Ticker.

**Bot-Reaktion:** Nichts tun (Ticker fehlt).

**Parser-Regel:** Cancel ohne Ticker → skippen. Bot kann nicht wissen welcher Trade gemeint ist.

---

### #75 — PREM · 2026-03-17T12:16:13+00:00 · msg_id=5424

```
LNAI moved big might adjust the order soon
```

**Typ:** `STATUS_UPDATE` · **Ticker:** LNAI

**Jack meint:** 'might adjust the order soon' → Absicht ohne konkrete Werte.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** 'might adjust', 'moved big' → STATUS_UPDATE + FUTURE_INTENT. Bot wartet auf explizite neue Order-Struktur.

---

### #76 — PREM · 2026-03-19T13:25:09+00:00 · msg_id=5451

```
SER 
broke up another resistance.
The order cancelled but I most likely will share a new one .
```

**Typ:** `STATUS_UPDATE` · **Ticker:** SER

**Jack meint:** Resistance-Break + Cancel-Info + 'will share new' Absicht.

**Bot-Reaktion:** Eigene SER-Pending-Orders canceln.

**Parser-Regel:** Kombi: 'broke up resistance' (Status) + 'order cancelled' (Cancel) + 'might share new' (Intent). Parser-Priorität: CANCEL als harter Trigger, dann Wartestellung.

---

### #77 — PREM · 2026-03-23T14:13:34+00:00 · msg_id=5478

```
Exit another 20% at 3.75 filled
```

**Typ:** `EXIT_PARTIAL` · **Ticker:** —

**Jack meint:** Exit weitere 20% @ 3.75. Kein Ticker.

**Bot-Reaktion:** Skippen (kein Ticker). Manuell via 'sell TICKER' Command.

**Parser-Regel:** 'Exit another N% at X filled' ohne Ticker → AMBIGUOUS. Policy wie #48.

---

### #78 — PREM · 2026-03-24T20:36:59+00:00 · msg_id=5505

```
I  am scanning all after market activities for any possible trade.
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Scannt After-Market.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #26.

---

### #79 — PREM · 2026-03-27T17:47:00+00:00 · msg_id=5532

```
Cancelled for now!
If you keep any of it open ( I might risk one order ) you must be able to take profit quick.
Good luck 🍀!
```

**Typ:** `CANCEL` · **Ticker:** —

**Jack meint:** Cancel ohne Ticker + Risiko-Warnung.

**Bot-Reaktion:** Skippen.

**Parser-Regel:** Wie #68/#74.

---

### #80 — PREM · 2026-04-01T15:39:59+00:00 · msg_id=5559

```
If you don’t know how to trade and understand the risk better to avoid.
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Risk-Disclaimer-Sentenz.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #36.

---

### #81 — BIO · 2026-02-08T15:35:50+00:00 · msg_id=9

```
Forward-Looking Statements: Any forward-looking statements, such as expected stock moves, earnings outcomes, or price targets, are speculative and subject to risks and uncertainties. Actual results may differ materially from those projected.
Use at Your Own Risk: By accessing or using this Information, you acknowledge that you do so at your own risk and agree to hold the provider harmless for any outcomes resulting from your investment decisions.
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Kanal-Disclaimer (Forward-Looking Statements / Use at Own Risk). Legal-Boilerplate.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** KRITISCH: Disclaimer/Legal-Boilerplate-Keywords ('forward-looking', 'at your own risk', 'hold provider harmless') → NO_SIGNAL mit hoher Priorität. Kommt typisch zu Channel-Start.

---

### #82 — BIO · 2026-02-09T19:55:34+00:00 · msg_id=62

```
We are almost close to the predicted weekly resistance team!
Mentioned too early today
```

**Typ:** `MARKET_COMMENT` · **Ticker:** —

**Jack meint:** Kein Ticker, nur 'weekly resistance'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #6.

---

### #83 — BIO · 2026-02-11T01:55:30+00:00 · msg_id=109

```
Again that’s what I found when I do any research about REGAL . I am trying to share everything that’s might important but in this group I am also focused on profitability ( swing to long and day to swing) making money is the reason everyone of you joined I guess!
```

**Typ:** `MARKET_COMMENT` · **Ticker:** REGAL

**Jack meint:** REGAL-Research-Kommentar + Fokus-Statement.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'what I found when I do research about X' + Philosophie → MARKET_COMMENT ohne Action.

---

### #84 — BIO · 2026-02-12T03:03:43+00:00 · msg_id=137

```
Over night action for ACRV . I will keep a close eye on it tomorrow and Friday!
```

**Typ:** `WATCHLIST` · **Ticker:** ACRV

**Jack meint:** 'Over night action... keep close eye' → Watch.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'keep a close eye', 'overnight action' → WATCH.

---

### #85 — BIO · 2026-02-13T16:25:31+00:00 · msg_id=171

```
ABOS 
11% from my yesterday entry levels
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ABOS

**Jack meint:** PnL: '11% from my yesterday entry levels'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'X% from my entry', 'from yesterday levels' → STATUS_UPDATE.

---

### #86 — BIO · 2026-02-17T17:37:05+00:00 · msg_id=204

```
I placed an order at 0.73~0.77 valid till today market closed for IMUX. I got a nice history trading this . Especially if some of you were in my special list  that I shared about this one last year!
```

**Typ:** `ENTRY_ORDER_RANGE_NO_SL` · **Ticker:** IMUX

**Jack meint:** BUY IMUX @ 0.73~0.77, gültig bis Market Close, kein SL.

**Bot-Reaktion:** LIMIT BUY IMUX @ 0.77 (oberes Range-Ende), TIF bis Market Close (EOD). SL-Policy.

**Parser-Regel:** KRITISCH: 'valid till today market closed' → TIF = EOD (bis Close), nicht Minuten. Parser muss 'minutes', 'market closed', 'end of day', 'pre market', 'after hours' als unterschiedliche TIF-Flavors erkennen. Range wie #65.

---

### #87 — BIO · 2026-02-19T17:29:14+00:00 · msg_id=243

```
IBRX
Strong hold .
Buyers got the early dip . 
I will share my new chart module around the end of the day.
```

**Typ:** `STATUS_UPDATE` · **Ticker:** IBRX

**Jack meint:** 'Strong hold', 'buyers got early dip'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'strong hold', 'buyers got the dip' → STATUS_UPDATE. Hold-Empfehlung ist kein Entry.

---

### #88 — BIO · 2026-02-23T22:29:12+00:00 · msg_id=287

```
My Great team.
Pay attention to TARA
Among the strong biotech stocks got a drop AH tonight but I think 🤔 personally I will place a price alert around 5.12~5.30 if it gets there again tonight might get some. If I couldn’t fill any order tonight will watch it tomorrow pre market and update my order!
```

**Typ:** `CONDITIONAL_WATCH` · **Ticker:** TARA

**Jack meint:** 'I will place a price alert around 5.12~5.30 if it gets there again' → konditionaler Alert-Plan.

**Bot-Reaktion:** Nichts tun.

**Parser-Regel:** Konditionale Alerts + 'might get some' + 'if' → nie Entry. Wie #50.

---

### #89 — BIO · 2026-02-24T22:17:04+00:00 · msg_id=321

```
Explain the number
The green one
The expectation for the week
1.70 1.74 all came in real time chart .
Check all other levels
Remember red numbers the support and green ones the resistances.
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Erklärung über Zahlen/Chart-Module.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Meta/Edukation über eigene Chart-Notation → NO_SIGNAL.

---

### #90 — BIO · 2026-02-26T13:59:11+00:00 · msg_id=352

```
IBRX
some rebound pre market from yesterday sell off
```

**Typ:** `STATUS_UPDATE` · **Ticker:** IBRX

**Jack meint:** 'some rebound pre market'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'rebound', 'pre market from yesterday' → STATUS.

---

### #91 — BIO · 2026-02-27T23:46:24+00:00 · msg_id=380

```
Team IBRX is moving ✅✅
```

**Typ:** `STATUS_UPDATE` · **Ticker:** IBRX

**Jack meint:** 'IBRX is moving ✅✅'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'X is moving' + ✅ → STATUS.

---

### #92 — BIO · 2026-03-04T15:43:29+00:00 · msg_id=419

```
ATOS in the move .
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ATOS

**Jack meint:** 'ATOS in the move'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #91.

---

### #93 — BIO · 2026-03-06T17:36:36+00:00 · msg_id=449

```
I am planning to hold till around March 20th to March 22th
```

**Typ:** `NO_SIGNAL` · **Ticker:** —

**Jack meint:** Hold-Absicht ohne Ticker.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'Planning to hold till date X' ohne Ticker → kein Action.

---

### #94 — BIO · 2026-03-10T22:34:36+00:00 · msg_id=479

```
We are in a good strong position here team!
AKBA ❤️
```

**Typ:** `STATUS_UPDATE` · **Ticker:** AKBA

**Jack meint:** 'in a good strong position here team! AKBA ❤️'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'strong position', ❤️ → STATUS. Emoji-Heavy ohne Struktur.

---

### #95 — BIO · 2026-03-12T19:23:29+00:00 · msg_id=512

```
ATOS is doing good today team. Hopefully it will do more! Will see! Still holding.
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ATOS

**Jack meint:** 'doing good today, still holding'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Wie #35.

---

### #96 — BIO · 2026-03-17T12:02:59+00:00 · msg_id=543

```
IBRX up again pre market
```

**Typ:** `STATUS_UPDATE` · **Ticker:** IBRX

**Jack meint:** 'up again pre market'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** 'up again', 'down again' → STATUS.

---

### #97 — BIO · 2026-03-20T14:13:19+00:00 · msg_id=574

```
ATOS
Moved some today still holding.
SLS
IBRX
OCGN
RCKT
I will share more updates still also in the hold zone✅✅
```

**Typ:** `STATUS_UPDATE` · **Ticker:** ATOS,SLS,IBRX,OCGN,RCKT

**Jack meint:** Multi-Ticker-Hold-Report: 'Moved some today still holding' + weitere Ticker 'in hold zone'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** KRITISCH: Mehrere Ticker als Liste untereinander + 'still holding' / 'hold zone' → STATUS_UPDATE multi. 'Moved some' ist ambig (partial exit?) aber ohne Prozent/Preis zu vage für Action. Policy: logging + Alert an User.

---

### #98 — BIO · 2026-03-24T01:31:17+00:00 · msg_id=602

```
SLS
Most recent update chart with all the needed numbers
```

**Typ:** `NO_SIGNAL` · **Ticker:** SLS

**Jack meint:** 'Most recent update chart with the needed numbers' — bezieht sich auf ein Bild/Chart.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** KRITISCH: Nachrichten die auf Chart/Bild verweisen ('chart', 'module', 'image', 'see attached') → keine Parse-Basis. Ohne OCR/Vision ist das out-of-scope.

---

### #99 — BIO · 2026-03-25T18:31:17+00:00 · msg_id=634

```
RCKT
I wish you are enjoying it team
```

**Typ:** `STATUS_UPDATE` · **Ticker:** RCKT

**Jack meint:** 'I wish you are enjoying it team'.

**Bot-Reaktion:** Ignorieren.

**Parser-Regel:** Feedback-Phrase → STATUS.

---

### #100 — BIO · 2026-03-30T14:55:52+00:00 · msg_id=665

```
SLS
below 4 might trigger some SL  rides just be aware of that.
It’s shorts tactics to bring down the price . I am not going to panic about it yet!
```

**Typ:** `STATUS_UPDATE` · **Ticker:** SLS

**Jack meint:** 'below 4 might trigger SL rides, not panicking' → Warnung vor möglicher SL-Kaskade.

**Bot-Reaktion:** Ignorieren. Aber: wenn SLS-Position mit SL @ ~4 offen ist → User alerten (könnte beabsichtigt sein, Jack hält durch).

**Parser-Regel:** Meta-Warnung über SL-Hunting ist kein Entry/Exit-Signal. 'not panicking yet' → Hold-Intention.

---
