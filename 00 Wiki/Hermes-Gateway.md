---
title: Hermes Gateway
type: tool
tags: [telegram, bridge, automation]
created: 2026-04-20
updated: 2026-04-20
sources: [[01 Inbox/Hermes Setup Woche|Hermes Setup Woche]], [[01 Inbox/Hermes Freundin-Zugang Design|Hermes Freundin-Zugang Design]], [[01 Inbox/Voice TTS Audit vor Implementation|Voice-TTS Audit 2026-04-20]]
---

## Summary

Telegram-Front-End für die persistente `claude-home`-Session auf der VPS. Routet eingehende Telegram-Nachrichten (Text + Voice) an Claude Code, liefert Antworten zurück. Delegiert Nicht-Dev-Tasks (Kalender, Reminder, Voice-Output, Scheduled-Tasks) aus `claude-home` heraus an eigene lokale Tools.

## Details

### Architektur-Pfad

```
Dominic (Telegram)
   ↓
Hermes Gateway (Container)
   ↓ POST /v1/chat/completions
Bridge :8765 (Host)
   ↓ /tmp/claude_inbox/msg_*.json  (chat_id=0 internal)
tmux claude-home (UserPromptSubmit-Hook)
   ↓ /tmp/claude_outbox/reply_msg_*.txt
Hermes → Telegram
```

Zusätzlich: direkter `/inbox`-Push mit `chat_id=781400898` für autonome Wakeups (Cron, Daemons) — skippt Hermes, Outbox-Poller liefert.

### Aktuelle Fähigkeiten

- Text-In / Text-Out (Deutsch, terse)
- Voice-In (Whisper-Transkription lokal) → Text-Out (Hard-Rule: **niemals** Voice zurück)
- Slash-Commands `/start`, `/help`, `/sethome` lokal ohne LLM-Call
- Short-Acks („ok", „danke") lokal

### Delegations-Handler (Phase-1 done 2026-04-20)

Claude-home soll Nicht-Dev-Requests NICHT selbst ausführen, sondern an Hermes delegieren:

- `cron` — Scheduled Tasks
- `reminder` — Telegram-Pings
- `note` — Vault-Writes via Hermes-Obsidian-Skill
- `contact` (stub)
- `media` (stub)

Phase-2: Tests + Outbox-Poller-Integration (User-Go pending).

### Mitwachs-Regel

8-Punkt-Pattern aus `feedback_hermes_grows_with_us.md`: bei jeder Signal-Bot-Feature-„done"-Meldung inline die Hermes-Checkliste durchgehen (SOUL.md / MEMORY.md / Skills / Tools aktualisieren).

### Bekannte Grenzen

- Bridge-Timeout selten → Antwort „Bridge-Timeout, bitte nochmal"
- „Session already in use"-Fehler wenn `claude` parallel als eigene Instanz läuft → Remote-Control-Mode statt neuer Session
- Niemals Voice zurück (User-Feedback 2026-04-19)

### Pending Features & Audits

- **Voice-TTS (edge-tts Katja)** — [[01 Inbox/Voice TTS Audit vor Implementation|Audit-Plan 2026-04-20]]. **Deferred** bis Audit klärt ob Night-Wakeup-Voice-Pipeline existiert. SOUL.md-Hard-Rule „niemals Voice" gilt für Standard-Replies; Ausnahme nur bei `priority=critical` Night-Wakeup denkbar. Aufwand 3-5h (mit 7×-Multiplier). Trigger: beim nächsten Hermes-Feature-Build inline via Regel „Hermes-Mitwachsen" (#113).

  **Stimmen-Lösungsraum** (aus [[01 Inbox/TODO|TODO.md]] 2026-04-19): (a) edge-tts `de-DE-KatjaNeural`/`ConradNeural` — kostenlos, MS-cloud, offline nein; (b) Piper-TTS lokal `de-thorsten-*`/`de-kerstin-*` — offline, mittelgute Quali; (c) ElevenLabs DE — sehr gut, kostet, API-Key; (d) Coqui-XTTS v2 — Voice-Cloning, lokal, RAM-hungrig. Default-Empfehlung: edge-tts KatjaNeural (null-effort, gut).

- **Delegation claude-home → Hermes Phase-2** — [[01 Inbox/TODO|TODO.md]]. Phase-1 shipped 2026-04-20 (Plan + Skelett: `signal_bot/scripts/hermes_delegation_handler.py`). Phase-2 = Integration in outbox-poller + Tests + 3 full-Handler. Aufwand 14-20h. **User-Go pending.**

- **Remote-Control PC über Telegram** — [[01 Inbox/TODO|TODO.md]]. Dominic will VPS-PC von unterwegs steuern (exec, logs, service-restart). Default-Design: (b) Slash-Commands (`/exec`, `/restart`, `/log`, `/edit`) + Whitelist + Audit-Log in Daily-Notes. Unterscheidet sich von Delegation (echte Host-Actions vs. Task-Routing).

- **Review-UI mobile** — [[01 Inbox/TODO|TODO.md]]. Parser-Review nicht nur auf Server. Optionen: (a) eigene App, (b) Telegram-Inline-Keyboard pro Verdict, (c) PWA. Default: Telegram-Inline (Infra steht). Mini-Design-Skizze in [[01 Inbox/Review UI Inline Telegram Skizze|Review UI Inline Telegram Skizze]]. Ship sobald Parser-Features stabil.

## Related

- [[Signal-Bot-MOC]] — konsumiert Hermes für Telegram-Output-Delegation
- [[Karpathy-LLM-Wiki]] — Hermes kann später `ingest` via Telegram anstossen

## History / Log

- Setup-Woche (Inbox-Note): Architektur-Design und erste Implementation
- 2026-04-19: Hard-Rule „niemals Voice-Antworten" gesetzt
- 2026-04-20: Delegation-Handler-Skelett gebaut (Phase-1 done)
