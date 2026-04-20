---
title: Jack Sparo
type: person
tags: [signal-source, trading]
created: 2026-04-20
updated: 2026-04-20
---

## Summary

Jack Sparo = der Signal-Geber, dessen Telegram-Kanal-Nachrichten der [[Signal-Bot-MOC|Signal Bot]] parsed und ausführt. Zentrale externe Entität für das gesamte Signal-Bot-System.

## Charakteristika (empirisch 2026-04-18 / 2026-04-19 audits)

- **Self-adjustierende Alerts** — Jack ändert Entry-Levels bei Bewegung, nicht starre Orders.
- **Jargon-Muster** — „Price Alert" = effektive Buy-Order (siehe Feedback-Memory).
- **Messaging-Stil** — kurze, implizite Referenzen; Pronoun-Auflösung braucht Chain-Kontext.
- **Keine Telegram-Replies** — Chains sind linear, keine Reply-Threads.

## Edge-Audits

- [[02 Projekte/Signal Bot Jack-Edge-Audit|Jack-Edge-Audit]]
- [[02 Projekte/Signal Bot Jack-Exit-Matrix|Jack-Exit-Matrix]]
- [[02 Projekte/Signal Bot Jack-Slippage-Matrix|Jack-Slippage-Matrix]]

## Related

- [[Signal-Bot-MOC]] — konsumiert Jacks Signale
- [[Parser-MOC]] — interpretiert Jacks Sprache
- [[Halt-Up-Pattern]] — Pattern das Jack häufig callt
- [[04 Ressourcen/Trading Gruppen/Trading Gruppen|Trading Gruppen]] — Quellen-Doku

## Externe Referenzen

- Memory: `feedback_jack_narrative_vs_price_reality.md` — Jack erzählt Narrativ, Preis macht anderes
- Memory: `feedback_conditional_trigger_is_buy.md` — „Conditional Trigger" = Buy-Order
- Memory: `feedback_jack_self_adjusts_alerts.md` — Alerts werden nachjustiert
- Memory: `reference_jack_staggered_entry_method.md` — Staggered-Entry-Methode
