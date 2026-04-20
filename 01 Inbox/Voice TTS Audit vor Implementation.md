---
tags: [inbox, hermes, voice, audit]
status: open
date: 2026-04-20
---

# Voice-TTS (edge-tts Katja) — Audit vor Implementation

## Status
**Deferred** — Implementation blockiert bis Hermes-Audit klärt ob Voice-Output-Pipeline überhaupt existiert/aktiv ist.

## Hard-Rule-Konflikt
SOUL.md: „NIEMALS Voice/Audio-Antworten zurückschicken" — gilt für Standard-Telegram-Replies.

Offen: gibt es eine separate **Night-Wakeup-Voice-Pipeline** (ausgehender Anruf an Dominic bei kritischen Events), die TTS wirklich braucht?

## Audit-Checkliste (vor Implementierung)

1. **Code-Audit Hermes-Container:**
   - [ ] `/opt/hermes/gateway/` — gibt es Voice/Call-Handler?
   - [ ] `/opt/hermes/hermes/` — tts_tools.py aktive Runtime oder nur Test-Stubs?
   - [ ] `config.yaml` — `tts:` Section vorhanden? provider/voiceId gesetzt?
   - [ ] `SOUL.md` — Ausnahme für Night-Wakeup dokumentiert?

2. **Infrastructure-Audit:**
   - [ ] Outbound-Voice via Telegram Bot API möglich? (sendVoice akzeptiert .ogg/.opus)
   - [ ] Call-Anbieter konfiguriert? (z.B. Twilio für echten Call statt Voice-Message)
   - [ ] Gibt es aktive Cron/Trigger die „Night-Wakeup" starten?

3. **User-Klärung nach Audit:**
   - Soll Voice nur bei `priority=critical` Events gefeuert werden?
   - Welche Events? (Bot-Crash, IBKR-Disconnect, Margin-Call, Trade-Loss > X%?)
   - Nachttstunden-Fenster? (z.B. 23:00-07:00 CET)

## Wenn Audit ergibt: Pipeline existiert nicht
→ Ticket schließen als **"Falsches Feature"** — keine Infra zum Upgraden vorhanden. Priorität niedrig (Stimme Dominics Alltag nicht wichtig genug um Pipeline neu zu bauen).

## Wenn Audit ergibt: Pipeline existiert
→ 3-Schritt-Plan:
1. `pip install edge-tts` im Hermes-Container
2. Config: `tts: provider: edge; voiceId: de-DE-KatjaNeural`
3. Test mit Sample-Text, Audit des Output-Formats (.mp3 vs .ogg, Bitrate, Delay)

## Aufwand-Schätzung (mit 7x-Multiplier)
- Audit: 20min → **realistisch 2-3h**
- Implementation bei positivem Audit: 15min → **realistisch 1-2h**
- Total: **3-5h realer Zeit**

**Nächster Trigger:** Beim nächsten Hermes-Feature-Build Audit inline durchführen (Regel „Hermes-Mitwachsen" #113).
