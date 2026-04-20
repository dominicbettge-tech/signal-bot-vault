---
tags: [inbox, projekt-idee, review-ui, telegram]
status: open
date: 2026-04-20
---

# Review-UI Inline-Telegram — Mini-Design-Skizze

## Status
**Skope-gated** — aktuelle CLI-UI läuft stabil, Rebuild nur bei klarem Pain-Point.

## Aktuelle CLI-UI (Ist-Zustand)
- Dominic öffnet Terminal → Review-Session startet
- Pro Message: Jack-Text + Context → ein Verdict-Code tippen
- `save_verdict.py` persistiert sofort
- Verdict-Codes: b/n/s/x/e/a/r/etc. (siehe `feedback_verdict_codes.md`)

## Idee Inline-Buttons in Telegram
- Telegram-Bot zeigt Jack-Text + Chain
- Unter jeder Message: Inline-Keyboard mit Verdict-Buttons [b] [n] [s] [x] [a] ...
- Klick → Verdict wird persistiert, nächste Message kommt automatisch

## Pro vs. Con

### Pro
- Mobil reviewen möglich (Bus, Toilette, Bed)
- Kein SSH + CLI nötig
- Low-Friction, mehr Reviews pro Woche möglich
- Telegram-Chat als Log (historische Referenz)

### Con
- Telegram-Inline-Keyboards haben Limit (max 8 Buttons pro Row, max ~15 wichtig)
- Verdict-Codes sind ~11-14 → braucht Paginierung oder Submenu
- Chain-Display komplexer (vs. CLI-Tabelle)
- Aktuelle CLI-UI ist eingespielt, Rebuild = 10-15h Arbeit
- Persistence-Race-Condition: schnelle User-Klicks könnten race mit backend
- Predict-Verdict-Output in Telegram-Format (vs Terminal-Tabelle)

## Scope-Fragen für Entscheidung
- [ ] Komplett-Replacement oder Parallel-Modus? (CLI + Telegram gleichzeitig)
- [ ] Self-Eval-Integration? (batch-grill-me)
- [ ] Wie werden Edge-Cases (NIGHT_QUEUE-Einträge) behandelt? (Skip-Button, Flag-Button)
- [ ] Multi-User? (nur Dominic oder auch später Team?)

## Meine Empfehlung (ungefragt)

**Nicht jetzt bauen.** Aktuelle CLI-UI funktioniert, Reviews laufen. Pain-Point müsste sein: „ich reviewe zu wenig wegen CLI-Friction". Falls das stimmt → rebuild lohnt.

**Falls doch:** Parallel-Modus (CLI bleibt, Telegram zusätzlich), MVP = nur b/n/s/x Buttons (4 meistgenutzte), Rest via Text-Reply.

## Aufwand-Schätzung (mit 7x-Multiplier)
- MVP (4 Buttons): 3h → **21-30h**
- Full (alle Verdict-Codes + Chain-Display + Edge-Case-UI): 15h → **100-150h**

**Trigger für Re-Eval:** Wenn Dominic sagt „Ich reviewe zu wenig weil CLI nervt" → dann lohnt es.
