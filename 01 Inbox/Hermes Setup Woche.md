# Hermes Ausbau — Wochenliste

Erstellt 2026-04-19. Abarbeitung nacheinander.

| # | Task | Aufwand | Voraussetzung |
|---|---|---|---|
| 1 | Google-OAuth-Setup (Calendar + Contacts) | 15 min | Google-Account Zustimmung |
| 2 | Google Calendar anbinden — Termine lesen/anlegen, Geburtstage | 30 min | #1 |
| 3 | Yahoo Mail anbinden via IMAP/SMTP (himalaya) — lesen, Entwürfe, Schreibstil-Analyse | 45 min | Yahoo-App-Passwort |
| 4 | Google Contacts — Geburtstags-Sync in Kalender | 15 min | #1 |
| 5 | Obsidian-Vault-Zugriff (Notizen lesen/schreiben, Daily Notes) | 10 min | läuft schon |
| 6 | Listen-System — Einkauf, ToDo privat, Geschenkideen, Haushalt, Ideen | 30 min | Speicherort wählen (Keep vs Obsidian) |
| 7 | Freundin-Zugang — Telegram-Whitelist erweitern, Absender-Unterscheidung | 20 min | ihre Chat-ID |
| 8 | Morgen-Briefing Cronjob — Kalender + Mails + Wetter + Signal-Bot-Status | 20 min | #2, #3 |
| 9 | Abend-Rückblick Cronjob — Tagesüberblick, offene ToDos | 15 min | #6 |
| 10 | Reminder-System — ad-hoc "erinnere mich morgen 14 Uhr an X" | 15 min | läuft schon |
| 11 | Signal-Bot-Monitoring — Ping bei Problemen, Status-Pull | 20 min | Bridge läuft |
| 12 | Philips Hue (optional) — Lichtsteuerung per Sprach/Text | 20 min | Hue-Bridge-Credentials |
| 13 | Linear/Notion (optional) — Tasks anlegen falls genutzt | 15 min | API-Token |

**Summe Kern (1-11):** ca. 4 h verteilt über Woche.
**Reihenfolge-Empfehlung:** #1 zuerst (blockiert #2-#4), dann #6+#7 parallel, dann Cronjobs #8+#9, dann Signal-Bot #11.

**Nächster Schritt:** Google-OAuth anstoßen (#1). Dafür brauch ich dein OK und du machst einmalig Auth-Flow im Browser durch.
