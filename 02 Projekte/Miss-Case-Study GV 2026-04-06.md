---
title: Miss-Case-Study GV 2026-04-06
type: analysis
tags: [signal-bot, miss-analysis, case-study, range-below-market]
created: 2026-04-21
status: draft
related: [[Loop-Orchestrator]], [[Signal-Bot-MOC]], [[Miss-Case-Study GV 2026-04-02]]
---

## TL;DR

Am 4/6 postete Jack **5× denselben Limit-Entry** für GV bei **0.255-0.27** "as long as no offering". Der Bot legte **1 Limit-Order** bei Midpoint 0.2625, die **nie füllte** — weil der Marktpreis den ganzen Tag in **0.31-0.40** handelte und die Range nie berührt wurde.

**Das ist eine andere Kategorie als GV 4/2:** Es ist kein Midpoint-Problem. Selbst `entry_high=0.27` lag **11% unter dem Intraday-Tief 0.3067**. Keine Staggered-Entry-Strategie hätte hier gefüllt.

**Root-Cause:** Jack's Range war bereits vor dem Post unter dem aktuellen Marktpreis. Der Bot hat das nicht erkannt und eine No-Fill-Order für 22h platziert.

## Chain — alle GV-Messages 4/6 (UTC→ET)

| # | UTC | ET | Typ | Jack-Text (gekürzt) |
|---|---|---|---|---|
| #69 | 13:16 | 09:16 | entry | "I placed me an order in GV 0.255~0.27 As long as no offering, valid 2h, day/swing" |
| #73 | 13:47 | 09:47 | entry | gleich (Repost) |
| #77 | 13:52 | 09:52 | entry | gleich |
| #82 | 14:39 | 10:39 | entry | gleich |
| #86 | 14:52 | 10:52 | entry | gleich |

Jack postete 5× denselben Text — typische Telegram-Edit-Repost-Mechanik, wie 4/2.

## Bot-Aktionen

| Trade | opened ET | Sig | Limit@ | Filled | Exit | Status | Shares | PnL |
|---|---|---|---:|---|---|---|---:|---:|
| #6 | 09:16:36 | #69 | 0.2625 (mid) | ❌ | None | "closed" 11:29 ET next day | 0 | None |

*(Signal #73/77/82/86 → Dedup-Block, korrekt)*

**Datenmodell-Flags:**
- `fill_price=None`, `shares=0`, `ibkr_order_id=None` — Order wurde registriert aber nie gefüllt/ge-IBKR-submitted
- `stop_loss=0.36` ist **über entry_price 0.2625** — parser-Artefakt (Jack gab keinen expliziten SL, möglicher Auto-Fill-Bug)
- `closed_at` = 22h später → de-facto Expiry, nicht SL/TP-Trigger

## Preis-Verlauf GV 4/6 (Polygon 1-min ET)

```
09:00  0.3416 (pre-market)
09:16  0.3436 ← Jack Signal #69  — Midpoint-Limit 0.2625 aktiviert
09:30  0.3449 (Markt-Open)
---    intraday 0.3067 - 0.4012 — NIE unter 0.3067
15:59  0.3499 (Close)

Jack-Range 0.255-0.27:
  entry_low  0.255  → 17% unter Intraday-Tief
  midpoint   0.2625 → 14% unter Intraday-Tief
  entry_high 0.27   → 11.5% unter Intraday-Tief

Bars mit low ≤ 0.27: 0/391 (regular session + pre-market)
```

**Entscheidender Punkt:** Selbst der aggressivste Tranche-Preis (entry_high 0.27) lag 11.5% **unter** dem gesamten Trading-Range. Keine Staggered-Tranche hätte gefüllt.

## Warum hat's nicht geklappt?

| Faktor | Reality | Bot-Verhalten |
|---|---|---|
| Price-at-Post | ~0.34 | Ignoriert, Limit @ 0.2625 |
| Jack-Range | 0.255-0.27 (11-17% unter Markt) | akzeptiert als Entry-Range |
| Pullback-Wait | Würde 11% Mean-Revert brauchen | 22h gewartet → Expiry |
| Pre-Market-Context | Post um 09:16 ET (pre-market) | Kein Pre-Market-Flag |

**Root-Cause:** Jack's Range war zum Post-Zeitpunkt bereits **unter dem aktuellen Marktpreis**. Der Bot behandelt jede Range identisch, unabhängig davon, wie weit sie vom Marktpreis entfernt ist.

## Fix-Vorschlag (grounded-decisions, 5-Step)

**Features:** 
- Jack-Range posted at P_current ≈ 0.34, range [0.255, 0.27] = 15% unter Mid-Range
- Midpoint-Strategie naiv angewendet → 0% Fill-Chance
- 5 Reposts über 1.5h → Jack selbst signalisiert Skepsis ("as long as no offering")

**Prior-Context:**
- GV 4/2 Case-Study zeigte: Staggered-Entry hilft bei Ranges *nah* am Preis, nicht bei Ranges weit weg
- Loop-Orchestrator Whitelist hat keinen Knob für "range_vs_market_price_gap"
- `project_oversold_ladder.md`: 21.5% No-Fill-Rate auf aggressiver Limit-Strategie
- Jack-Range 0.255-0.27 = -25% OFF Peak-High 0.40 — das ist Extreme-Pullback-Hope, nicht Setup-Trigger

**Precedents:**
- GV 4/2: Range war ±3% von Mid-Price → Pullback realistisch
- GV 4/6: Range war -15% von Mid-Price → Pullback unrealistisch
- Pattern: **Range-to-Market Gap** als Filter-Kriterium

**3 Alternativen:**

| Variante | Mechanik | Pro | Contra |
|---|---|---|---|
| A Baseline | Limit @ Midpoint egal wo Markt steht | einfach | No-Fill bei grossem Gap (siehe 4/6) |
| **B Range-Gap-Filter** | **SKIP wenn `entry_high` < `last_price * 0.97`** (= >3% unter Markt) | verhindert No-Fill-Leaks; belässt nahe Ranges | kann valide Pullback-Setups verwerfen |
| C Chase-Fallback | Wenn Range unter Markt: ersetze Limit durch Market-Order @ entry_high | filled garantiert | hohe Slippage, widerspricht Jack's Intent |

**Goal-Alignment:**
- B schützt vor No-Fill-Leaks und erzwingt User-Decision bei "weit entfernten Ranges"
- Beste Alternative: **B Range-Gap-Filter** als neuer Gate-Check in `safety.py` oder `signal_manager.py`
- Nicht via Corpus-Sim validierbar (Gate-Level-Knob) → würde als NEEDS_MANUAL in Loop-Queue landen

**→ Empfehlung: B (Range-Gap-Filter).** Kein Knob-Tuning, sondern neuer Gate-Check.

## Vorgeschlagene Implementation

```python
# In signal_manager.py oder safety.py
RANGE_GAP_MAX_PCT = 0.03  # entry_high max 3% unter last_price

def check_range_reachable(signal, last_price):
    if not signal.entry_high or not last_price:
        return True  # kein Check möglich
    gap = (last_price - signal.entry_high) / last_price
    if gap > RANGE_GAP_MAX_PCT:
        # Range liegt >3% unter Markt → User-Decision nötig
        return False
    return True
```

**Notifier-Path:** Bei Fail → Post-Miss `miss_category='RANGE_BELOW_MARKET'` + Telegram-Alert "⚠️ Jack-Range X weit unter aktuellem Markt Y — skippe, bitte manuell prüfen".

## Was noch offen ist

- Gate-Level-Knob → kein Corpus-Sim → manuelle Validierung nötig
- Prüfen: hat der historische Bot Trade #6 jemals zu IBKR submitted? `ibkr_order_id=None` deutet auf Error-Pfad hin
- Parser-Auto-SL-Bug: stop_loss=0.36 > entry_price 0.2625 → nicht sinnvoll für LONG, separat prüfen
- `total_shares=2000` aber `shares=0` → Dead-Record-State zu prüfen