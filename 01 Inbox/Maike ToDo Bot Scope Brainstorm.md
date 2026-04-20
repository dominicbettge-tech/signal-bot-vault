---
tags: [inbox, projekt-idee, maike, telegram-bot]
status: open
date: 2026-04-20
---

# Maike-ToDo-Bot — Scope-Brainstorm

## Status
**Skope-gated** — Implementation wartet auf Dominics Scope-Definition.

## Offene Scope-Fragen

### 1. Kern-Funktionalität
- [ ] Nur Text-ToDos? (Eingabe via Telegram, Liste abrufbar, Haken setzen)
- [ ] Auch Reminder? (Zeit/Datum-basiert, Bot pingt zurück)
- [ ] Auch Voice-Input? (Whisper → Text → ToDo)
- [ ] Auch Foto-Input? (OCR / Bild-Attachment)
- [ ] Shopping-Liste-Modus? (Kategorien, Quantity)

### 2. Intelligenz-Level
- [ ] Dumme Liste (nur CRUD)
- [ ] Mittel (Reminder, Kategorisierung, Suche)
- [ ] Smart (LLM verstehst Intent: „morgen Brot kaufen" → Reminder + Shopping-List)

### 3. Integration
- [ ] Isoliert (eigener Bot, eigene DB)
- [ ] Teil von Hermes (shared Infra, aber eigene User-Section)
- [ ] Shared zwischen Maike + Dominic (Paar-ToDos)

### 4. Privacy / DSGVO
- ⚠️ **Fremde Person** — braucht:
  - Expliziter Opt-in (Maike muss wissen und zustimmen, dass KI involviert)
  - Datenverschlüsselung at-rest
  - Lösch-Möglichkeit (alle Daten)
  - Kein Training auf ihren Messages
- DSGVO-Checklist: Data-Minimisation + Zweckbindung + Transparenz

### 5. Tech-Stack
- [ ] Eigener Telegram-Bot mit python-telegram-bot
- [ ] Shared Hermes-Infra (Bridge + Outbox)
- [ ] SQLite-DB oder Notion-Integration?

## Meine Empfehlung (ungefragt)

**MVP:** Eigener Bot, SQLite, nur Text-ToDos + Reminder. Kein LLM. Opt-in-Dialog beim ersten Start.

**Grund:** DSGVO minimal-invasiv, keine KI-Entscheidungen über fremde Person, Maike versteht was sie zustimmt.

**Expansion nach 2 Wochen:** Wenn sie es nutzt → Voice-Input (Whisper-API), LLM für „Intent-Parsing".

## Aufwand-Schätzung (mit 7x-Multiplier)
- MVP: 3h Design + 6h Implementation → **realistisch 30-60h**
- Deployment: 1h → **7-10h**

**Nicht ohne Dominics Go starten.**
