# Vault Context

Dieses Vault ist das Zweite Gehirn von Dominic Bettge.

## Über mich

Dominic Bettge, Physiotherapeut aus Deutschland. Baut automatisierte Trading-Systeme — aktuell den Signal Bot v3 der Telegram-Signale von Jack Sparo parsed und über IBKR Paper Trading ausführt. Ziel: finanzielle Unabhängigkeit durch automatisierten Handel. Ausführliches Profil in 00 Kontext/Über mich.md.

## Vault-Struktur

- **00 Kontext/**: Persönliches Kontext-Profil (Über mich.md, ICP.md, Angebot.md, Schreibstil.md, Branding.md). Zentrale Referenz für alle inhaltlichen Aufgaben.
- **01 Inbox/**: Schnelle Gedanken, Brain Dumps, unverarbeitete Notizen. Alles was noch keinen festen Platz hat landet hier.
- **02 Projekte/**: Aktive Projekte. Signal Bot.md (Hauptprojekt), Trading.md (Strategie), Signal Bot Fehler-Log.md (alle Bugs).
- **03 Bereiche/**: Trading/ (Strategie, Parameter, Kanäle), Finanzen/ (IBKR Account, Ziele).
- **04 Ressourcen/**: Claude Skills/, Claude Code Tools/, KI Allgemein/, Trading Gruppen/ (Jack Sparo Kanäle).
- **05 Daily Notes/**: Tägliches Logbuch. Format: YYYY-MM-DD.md
- **06 Archiv/**: Abgeschlossene Projekte und inaktive Bereiche.
- **07 Anhänge/**: Bilder, PDFs, Medien.

## Was Claude hier speichert

- Bugfixes → `02 Projekte/Signal Bot Fehler-Log.md`
- Projektfortschritt → `02 Projekte/Signal Bot.md`
- Trading-Erkenntnisse → `03 Bereiche/Trading/Trading.md`
- Neue Skills/Tools → `04 Ressourcen/Claude Skills/`
- Session-Ende → Daily Note in `05 Daily Notes/YYYY-MM-DD.md` anbieten

## Regeln für dieses Vault

- Nutze [[Wikilinks]] für Verknüpfungen zwischen Notizen
- Neue Notizen ohne klaren Platz kommen in 01 Inbox/
- Daily Notes im Format: YYYY-MM-DD.md
- YAML Frontmatter nutzen: tags, status, date
- Dateinamen in normaler Schreibweise mit Leerzeichen und Großbuchstaben
- Neue Projekte als einzelne .md Datei direkt unter 02 Projekte/
- Bereiche und Ressourcen sind immer Ordner
- Abgeschlossene Projekte nach 06 Archiv/ verschieben — nur auf Anweisung
- Bevor Dateien gelöscht oder überschrieben werden, nachfragen
- Wenn Dominic sagt "merk dir das" → in die passende Kontext-Datei speichern

## Session-Routinen

### Bei Session-Start
1. Prüfe 01 Inbox/ auf neue Notizen, zeige was drin liegt, biete an einzusortieren

### Kontext bei Bedarf
Wenn Dominic fragt "Was ist gerade aktuell?" oder "Wo war ich stehen geblieben?": Lies die letzten 2-3 Daily Notes und die aktiven Projekt-Dateien für ein kurzes Briefing.

### Bei Session-Ende
Anbieten:
1. Daily Note in 05 Daily Notes/ erstellen mit Zusammenfassung
2. Neue Erkenntnisse als Notizen speichern
3. Inbox aufräumen falls nötig
