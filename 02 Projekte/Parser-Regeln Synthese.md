---
tags: [signal-bot, parser, rules, phase-1]
date: 2026-04-11
status: draft
---

# Parser-Regeln Synthese — aus 100-Nachrichten-Sample

Ableitung aus `Parser-Analyse 100 Nachrichten.md`. Diese Datei ist die Grundlage für die `parser.py`-Überarbeitung in Phase 1.

## Message-Typen (Taxonomie)

Jede Nachricht wird in einen dieser Typen klassifiziert:

| Typ | Beschreibung | Bot-Action |
|---|---|---|
| `ENTRY_ORDER` | Klassischer Entry mit Ticker + Preis + SL + TIF | LIMIT BUY platzieren |
| `ENTRY_ORDER_NO_SL` | Entry ohne expliziten SL | **Policy-Entscheidung nötig** (siehe unten) |
| `ENTRY_ORDER_RANGE` | Entry mit Preis-Range "X~Y" oder "X to Y" | LIMIT @ oberem Range-Ende |
| `ENTRY_ORDER_AH_NO_SL` | AH/PM Entry ohne SL | `outsideRth=True` + SL-Policy |
| `EXIT_SELL` | Expliziter Full-Exit | Komplett schließen |
| `EXIT_PARTIAL` | Partial-Exit mit Prozentsatz | Teil schließen (% von Original) |
| `EXIT_PROFIT` | "Secure profit" ohne Menge | Default = 100% Exit |
| `CANCEL` | Order-Cancel-Bestätigung | Pending Orders für Ticker canceln |
| `STATUS_UPDATE` | PnL, Hold, Halt, Kurs-Update | **Nichts tun** |
| `WATCH_ALERT` | Preis-Alert, KEINE Order | **Nichts tun** |
| `WATCHLIST` | "Watching", "keep an eye" | **Nichts tun** |
| `WATCHLIST_INTENT` | "Will add", "going to trade" | **Nichts tun** (Zukunft) |
| `CONDITIONAL_WATCH` | "If X then I may" | **Nichts tun** |
| `MARKET_COMMENT` | Makro/Philosophie | **Nichts tun** |
| `NO_SIGNAL` | Gruß, Chat, Legal, Marketing | **Nichts tun** |
| `AMBIGUOUS_*` | Kontext-abhängig / unvollständig | **Skip + Alert** |

## Harte Blocker (Ticker aber KEIN Entry)

Wenn eine Nachricht einen Ticker enthält, ist das **nicht** automatisch ein Entry. Diese Keywords blocken Entry-Interpretation **hart**:

### Alert-Block
- `price alert`
- `placed a price alert`
- `not an order`, `only alert`, `only an alert`
- 🔔 **in Verbindung mit** "watch from there", "in my brokerage"

→ Typ: `WATCH_ALERT`

### Status-Block (Rückblick/Hold/Halt)
- `still holding`, `strong hold`, `in the hold zone`
- `green for me`, `red for me`
- `halted up`, `halted down`, `halt`
- `up again`, `down again`, `rebound`
- `beautiful swing`, `nice ✅`, `leg up`, `omg`, `insane`
- `X from entry around Y`, `X% from entry`
- `got to X`, `moved from X to Y`
- `broke up resistance`, `broke through`
- `fully closed` (Past-Tense Fill)
- `traded it from X to Y`
- Emoji-Spam (`✅✅✅`, `ℹ️`, `❤️`) **ohne** Order-Struktur

→ Typ: `STATUS_UPDATE`

### Watchlist/Intent-Block
- `watching`, `will watch`, `keep an eye`, `keep a close eye`
- `possible`, `might share`, `planning to`, `will add`
- `going to add`, `may get some`, `might get some`
- `interested move`, `might adjust`
- `for Monday`, `for tomorrow`, `tonight pre market`

→ Typ: `WATCHLIST` oder `WATCHLIST_INTENT`

### Konditional-Block
- Sätze mit `if ... then I may / might / will`
- `if it gets to X and stays above Y`

→ Typ: `CONDITIONAL_WATCH`

### Negation-Block
- `not to be trusted`, `weak volume`
- `too high`, `high price tag`, `too expensive`
- `I don't`, `I am not`, `no fill no trade`
- `not fair for team`, `I can personally but`

→ Typ: `NO_SIGNAL` / `MARKET_COMMENT`

### Meta/Service/Legal-Block
- `forward-looking`, `at your own risk`, `hold provider harmless`
- `VIP member`, `quarterly fees`, `special deal`, `Email me`
- `this is how I`, `my style`, `my strategy`, `never hesitate`
- **Mehrere Ticker in Fließtext** ohne Preis-Struktur (Marketing-Liste)

→ Typ: `NO_SIGNAL`

## Entry-Erkennung (Positiv-Muster)

Ein Entry **darf** nur feuern wenn ALLE drei Bedingungen erfüllt sind:

1. **Ticker** klar erkennbar (meist erste Zeile, max 5 Zeichen, Uppercase)
2. **Aktive Order-Phrase**: 
   - `placed an order at` / `placed me an order` / `placed order`
   - `day trade: PRICE` (Header-Variante)
   - `day trade alert 🔔 for TICKER` + Preis-Struktur
3. **Preis + TIF** explizit vorhanden:
   - Preis als Zahl (mit optionalem Range "X~Y")
   - TIF: `Valid for N minutes` / `for next N minutes` / `till market closed` / `after hours` / `pre market`

**SL** ist **optional** (Policy siehe unten).

### Entry-Phrase-Varianten (aus Sample gesehen)
```
# Variante 1 — explizit
TICKER
placed an order at PRICE
SL
SL_PRICE
Valid for N minutes
Day trade

# Variante 2 — Header
TICKER
Day trade:
PRICE
SL
SL_PRICE
Valid for N minutes

# Variante 3 — Alert-Entry (nicht Alert-Watch!)
Day trade alert 🔔 for
TICKER
Placed an order at PRICE for N minutes

# Variante 4 — AH/PM
TICKER
After hours
I placed an order at
PRICE
Valid for
N minutes

# Variante 5 — Range
TICKER
I placed me a day trade order at X~Y
For the next N minutes

# Variante 6 — EOD TIF
I placed an order at X~Y valid till today market closed for TICKER
```

## SL-Policy (offene Entscheidung)

Im Sample: **~50% der Entries haben KEINEN expliziten SL.** Das ist der wichtigste offene Punkt für Live.

**Optionen:**

**A) Skip + Alert** (sicherste Option)
- Entry wird nicht platziert, User bekommt Telegram-Alert mit Parse-Ergebnis
- Pro: kein undefiniertes Risiko
- Con: ~50% der Trades werden verpasst

**B) Default-SL aus `config.py`**
- Nutze `TRAILING_SL_PERCENT` (3%) oder neuen `DEFAULT_INITIAL_SL_PCT`
- Pro: kein Verpassen
- Con: Default kann falsch sein für Micro-Caps / volatile Stocks

**C) Halbe Position bei SL-loser Entries**
- Entry trotzdem, aber mit `POSITION_SIZE_PERCENT / 2`
- Plus Default-SL
- Pro: reduziert Risiko bei Unsicherheit
- Con: Komplexität, halbe Upside

**Empfehlung für Brainstorming:** Option **C** für Paper, Option **A** für Live-Pilot-Phase (7). Deckt Risiko besser ab und lässt uns Daten sammeln.

## Range-Policy

Preise wie `2.68~2.73` oder `0.73~0.77`:

**Empfehlung:** LIMIT BUY am **oberen Ende** (2.73 bzw. 0.77).
- Grund: Jack will meistens aggressiv gefüllt werden, oberes Ende erhöht Fill-Wahrscheinlichkeit.
- Alternativ: Range-Mitte (konservativer).

## TIF-Mapping

| Text | TIF-Implementation |
|---|---|
| `Valid for N minutes` / `for N minutes` | GTD (Good-Till-Date) = `now() + N min` |
| `for the next N minutes` | gleich |
| `till today market closed` / `end of day` | DAY |
| `after hours` / `AH` | `outsideRth=True` + DAY |
| `pre market` / `PM` | `outsideRth=True` + DAY |
| *nicht angegeben* | Default: 5 Minuten GTD |

## Multi-Ticker in einer Nachricht

**Regel:** Nur Ticker mit **direkter Action-Zuordnung** wird getradet.

- `Closed the rest of XAIR at 2.23 and turned my attention to ATON` → Exit XAIR, **nichts** auf ATON
- `I am going to add some WTI BATL tonight` → FUTURE_INTENT, kein Entry für beide
- `ATOS\nMoved some today still holding.\nSLS\nIBRX\nRCKT` → STATUS alle, **keine** Action

**Nie:** zwei Tickers → zwei Orders aus einer Nachricht.

## Fehlender Ticker → AMBIGUOUS

Nachrichten wie:
- `Extended the time for another 3 minutes`
- `This is still valid`
- `I filled some. Placed another order at 2.83 and 2.79`
- `The 25% I left sold at 7.80`
- `Exit another 20% at 3.75 filled`
- `Cancelled my order as it passed the time`

→ **NIE** Ticker aus vorheriger Nachricht inferieren. Policy: skippen + Telegram-Alert an User.

Der Bot sollte für solche Fälle **manuelle Telegram-Commands** bieten (`sell TICKER`, `cancel TICKER`, `extend TICKER N`) — und die bestehende `commands.py`-Infrastruktur nutzen.

## Edit-/Race-Fälle (Roadmap-Referenzen)

### INHD-Edit-Case (#14)
```
INHD omg 😳.. Leg up ✅✅
```
→ STATUS_UPDATE. Parser **darf nicht** als Entry feuern (INHD existiert als Ticker, aber keine Order-Struktur).

### OMEX-Catchup / OCGN-Retrospektive (#3)
```
OCGN
around 1.70 also a successful one
ℹ️✅ℹ️
```
→ STATUS_UPDATE. `around X + also a successful` = Rückblick, kein Entry.

**Regel:** `around X` allein **ist kein Entry-Trigger**. Braucht zusätzlich `placed` / `placed an order`.

## Priorität für parser.py-Umbau

1. **Blocker-Layer** zuerst: harte Keyword-Blacklist, bevor LLM-Parsing startet (spart Tokens UND verhindert False-Positives)
2. **Positiv-Pattern-Match** als Pre-Filter (Entry muss 3 Bedingungen erfüllen)
3. **LLM-Parse** nur noch auf verbleibenden Kandidaten
4. **SL-Policy-Flag** in config
5. **Range-Handling** explizit in der Struct

## Nächste Schritte (aus Phase 1 Roadmap)

- [ ] **Brainstorming-Session** für parser.py-Umbau — Design first, 2-3 Architektur-Alternativen
  - Option A: Regex/Keyword-Layer + Claude nur für Edge-Cases
  - Option B: Claude komplett aber mit striktem System-Prompt aus diesen Regeln
  - Option C: Hybrid — Blocker als Regex, Rest via Claude mit Rules-Injection
- [ ] parser.py anpassen
- [ ] Regression-Test: Diese 100 Nachrichten + erwarteter Typ als `tests/test_parser_regression.py`
- [ ] Stichprobe 200 weitere Nachrichten → Genauigkeit messen (Ziel ≥95%)
