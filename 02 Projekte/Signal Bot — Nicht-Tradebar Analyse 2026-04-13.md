---
tags: [signal-bot, parser, analyse, bugs]
date: 2026-04-13
---

# 27 "Nicht tradebar" Entries — Analyse & Fixes

Aus der Simulation: 27 von 311 Entries hatten keinen extrahierten Preis → nicht tradebar. Ursachen:

## Kategorisierung

| Kategorie | Anzahl | Beispiel | Fix |
|---|---|---|---|
| **Fill-Bestätigungen fälschlich als Entry** | 16 | "Filled", "Filled at 2.52" | Parser-Bug: Haiku klassifiziert "Filled" als Entry statt Update |
| **Preis im Text, nicht extrahiert** | 4 | "BKYI 1.45 SL 1.36 Valid for 4 minutes" (ID 3623) | Parser-Bug: Haiku-Stage stecken geblieben, Sonnet nie aufgerufen |
| **Order-Reaktivierungen ohne Preis** | 3 | "Activated this order here", "Re activated my order" | Braucht Reply-Chain-Context (Preis im Parent) |
| **Leerer Text** | 2 | (kein Inhalt) | Nicht tradebar, korrekt |
| **Sonstige** | 2 | "Here we go ✅✅✅", "Overnight action for ACRV" | Kein actionable Signal |

## Fixes (priorisiert)

### Fix 1: "Filled" → Update (16 Treffer, Quick-Win)
Blocker-Regel in `parser_rules.py`:
- `"Filled"` / `"filled at X"` / `"Filled two orders"` → `update` (Fill-Confirmation)
- NICHT Entry. Jack bestätigt damit einen bereits platzierten Trade.

### Fix 2: Haiku→Sonnet Weiterleitung (4 Treffer)
IDs: 3623, 4278, 4426, 5191
- Haiku erkennt korrekt "Entry", extrahiert aber keinen Preis
- Muss an Sonnet weitergereicht werden für Price-Extraction
- Bug: `stage_reached=haiku` obwohl es ein Entry mit Preis im Text ist

### Fix 3: Reply-Chain Preis-Auflösung (3 Treffer)
- "Activated this order" → Parent-Message hat den Preis
- `parser_context.resolve_context()` muss Entry-Preis aus Parent ziehen
- Teilweise schon in Phase A identifiziert, noch nicht gefixt

## Beziehung zur Review

Die manuelle Review (Bulk ab 3937 + Phase B 47 Messages) fixt diese 27 NICHT direkt:
- Review prüft ob Nachrichten korrekt *klassifiziert* sind
- Diese 27 sind ein *Extraction*-Problem (richtig als Entry erkannt, aber Preis fehlt)
- **→ Nach der Review als separaten Parser-Bug-Batch fixen**

## Betroffene IDs

Fill-Confirmations: 526, 3526, 3837, 3849, 4369, 4436, 4637, 4687, 4909, 5055, 5176, 5192, 5252, 5300, 5472, 5602
Preis nicht extrahiert: 3623, 4278, 4426, 5191
Reaktivierungen: 523, 575, 670
Leer: 615, 5276
Sonstige: 4552 (ACRV), 943 (Exit korrekt erkannt)
