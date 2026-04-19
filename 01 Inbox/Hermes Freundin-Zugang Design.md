# Hermes — Freundin-Zugang für gemeinsame Listen (Design)

Erstellt 2026-04-19. Ausarbeitung vor Implementierung (nächste Woche).

## Ziel
Freundin (Vanessa?) kann über denselben Telegram-Bot Einträge auf gemeinsame Listen setzen, damit Dominic nicht vergisst was sie ihm aufträgt.

## Rollenmodell
| Rolle | Chat-ID | Rechte |
|---|---|---|
| Owner | 781400898 (Dominic) | Alles: Listen, Kalender, Signal-Bot, System, Reminder, Config |
| Contributor | (Freundin, tbd) | Listen schreiben/lesen, Reminder für Owner setzen, Kalender-Einträge vorschlagen |
| — | alle anderen | abgewiesen |

Keine extra Passwörter — Telegram-Chat-ID ist Auth. Whitelist in `/opt/data/config.yaml`.

## User Flows

### Flow A: Freundin trägt auf Liste ein
1. Vanessa → "pack Milch auf Einkauf"
2. Hermes erkennt Absender-ID → Rolle Contributor → Ziel-Owner 781400898
3. Eintrag in `04 Listen/Einkauf.md` mit Marker `- [ ] Milch (Vanessa, 2026-04-19 16:15)`
4. Ack an Vanessa: "Hab ich Dominic auf Einkauf gesetzt"
5. Ping an Dominic (konfigurierbar): "Vanessa: Milch auf Einkauf"

### Flow B: Dominic fragt Liste ab
1. Dominic → "Einkaufsliste"
2. Hermes rendert `04 Listen/Einkauf.md` als Tabelle mit Absender + Zeit

### Flow C: Freundin setzt Reminder
1. Vanessa → "erinnere Dominic morgen 18 Uhr an Elternbesuch"
2. Hermes legt Cronjob an, Target = Owner-Chat
3. Ack an Vanessa + Ping morgen an Dominic

### Flow D: Abarbeiten
1. Dominic → "Milch erledigt" oder Tippen auf Checkbox in Obsidian
2. Eintrag wird abgehakt, bleibt sichtbar bis Wochenende → dann Archiv

## Listen-Katalog
| Liste | Pfad | Schreiber | Leser |
|---|---|---|---|
| Einkauf | 04 Listen/Einkauf.md | beide | beide |
| Haushalt/Reparaturen | 04 Listen/Haushalt.md | beide | beide |
| Geschenke (Vanessa zu Geburtstag etc.) | 04 Listen/Geschenke.md | nur Dominic | nur Dominic |
| Geschenke (Dominic zu Geburtstag) | 04 Listen/Geschenke-Dominic.md | nur Vanessa | nur Vanessa |
| ToDo Paar | 04 Listen/ToDo-Paar.md | beide | beide |
| Ideen-Dump | 04 Listen/Ideen.md | beide | beide |

Geschenk-Listen sind rollenspezifisch getrennt damit Überraschungen nicht geleakt werden.

## Notification-Regeln (konfigurierbar)
| Event | Default | Alternativen |
|---|---|---|
| Vanessa trägt auf Einkauf ein | sofort Ping | gebündelt 18 Uhr / aus |
| Vanessa setzt Reminder | sofort Ack beide Seiten | — |
| Reminder feuert | Push an Owner | Push an beide (optional) |
| Liste wird leer | Ping "Einkauf fertig" | aus |

## Edge-Cases
1. Beide schreiben gleichzeitig denselben Eintrag → Dedup via Normalisierung (lowercase, ersten 20 Zeichen matchen) → zweiter Eintrag wird ignoriert mit Ack "hast du schon"
2. Vanessa schickt systemnahen Befehl (z.B. "stopp Signal-Bot") → abweisen mit "Dafür fehlen dir Rechte, frag Dominic"
3. Vanessa will eigene private Liste (z.B. "meine ToDos") → separate Datei, nur für sie sichtbar — muss separat entschieden werden
4. Chat-ID-Leak → Auth über Chat-ID allein reicht für Paar-Szenario, aber nicht bei erweitertem Kreis — dann Second-Factor nötig

## Offene Fragen an Dominic
1. Wie heißt die Freundin im System (Display-Name)?
2. Soll sie eine eigene private Liste kriegen (getrennt von Paar-Listen)?
3. Notification-Default: sofort-Ping oder abendliche Bündelung?
4. Geschenk-Listen getrennt: OK so?

## Nächste Schritte (nächste Woche)
1. Chat-ID-Whitelist-Struktur in Config-File anlegen (Rollenmodell)
2. Listen-Verzeichnis `04 Listen/` in Vault anlegen mit 6 Start-Dateien
3. Parser erweitern: "pack X auf Liste Y" / "erinnere Z an W"
4. Notifier erweitern: Cross-User-Pings
5. Test mit zwei Chat-IDs (erst dein Zweit-Telegram, dann Freundin)
