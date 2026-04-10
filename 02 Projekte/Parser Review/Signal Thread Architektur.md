---
tags: [parser, architektur, plan]
erstellt: 2026-04-10
status: geplant
---

# Signal Thread Architektur — Plan

Erkenntnis: Jack nutzt Telegram-Replies intensiv. Nachrichten ohne Ticker-Wiederholung gehen dem Parser verloren. Lösung: Signal Threads.

## Kernidee

Ein Entry öffnet einen **Signal Thread**. Alle Follow-ups (Replies, Ticker-Updates, SL-Changes, Exits) werden diesem Thread zugeordnet. Der Parser bekommt immer den vollen Thread-Kontext.

## Zuordnungslogik (3 Stufen)

1. **reply_to_msg_id** — Telegram-Reply direkt auf Thread-Nachricht → sicher
2. **Ticker + aktiver Thread** — Ticker bekannt + offener Thread → zuordnen
3. **Claude-Inferenz** — kein Ticker, kein Reply → Claude entscheidet anhand aktiver Threads

## Neue DB-Tabellen (in trades.db)

```sql
CREATE TABLE signal_threads (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker      TEXT NOT NULL,
    channel     TEXT NOT NULL,
    trade_type  TEXT,            -- day_trade / swing
    status      TEXT DEFAULT 'active',  -- active / closed / expired
    opened_at   TEXT NOT NULL,
    closed_at   TEXT,
    trade_id    INTEGER          -- FK zu trades(id)
);

CREATE TABLE signal_thread_messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id       INTEGER NOT NULL,
    telegram_msg_id INTEGER,
    reply_to_msg_id INTEGER,
    timestamp       TEXT NOT NULL,
    signal_type     TEXT,        -- entry / sl_update / tp / exit / update / commentary
    raw_text        TEXT,
    parsed_data     TEXT         -- JSON
);
```

## Umsetzungsplan (6 Schritte)

- [ ] **1. DB-Migration** — `reply_to_msg_id` zu `raw_messages` hinzufügen, neue Thread-Tabellen anlegen
- [ ] **2. download_history.py** — `reply_to_msg_id` erfassen, neu laufen lassen
- [ ] **3. listener.py** — `msg_id` + `reply_to_msg_id` aus Events extrahieren, Callback-Signatur erweitern
- [ ] **4. db.py** — Thread-CRUD: `create_thread`, `get_thread_by_message`, `get_active_thread`, `add_message_to_thread`
- [ ] **5. signal_manager.py** — Thread-Zuordnung vor Parser-Aufruf
- [ ] **6. parser.py** — Kontext-Parameter + System-Prompt erweitern

## Parser-Prompt Erweiterung

```
CONTEXT HANDLING:
When previous messages from the same trade thread are provided:
1. Identify ticker if not in current message
2. Determine if this is an update to existing position
3. "New order" + Reply → replacement entry (cancel old, new entry)
4. Track SL changes across messages
```

## Aufwand

~2 Tage. Kern (Schritte 1-6) ca. 1 Tag.

**Abhängigkeit:** Erst Parser-Review abschließen → dann Architektur umsetzen.  
Grund: Wir brauchen vollständige Parser-Regeln bevor wir den Prompt neu schreiben.

## Referenz

- Analyse von Claude Opus (2026-04-10)
- [[Fortschritt]] — Parser-Review läuft parallel
- [[Regeln]] — werden hier einfließen
