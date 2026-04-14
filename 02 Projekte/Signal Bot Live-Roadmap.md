---
tags: [projekt, signal-bot, roadmap, live-trading]
status: aktiv
started: 2026-04-11
target: Mini-Live-Pilot mit 500-1000€ auf IBKR-Live-Account
---

# Signal Bot — Roadmap zum Live-Trading

**Ziel:** Den Bot so weit bringen dass er mit kleinem Echtgeld-Betrag (500-1000€) auf einem IBKR-Live-Account läuft, ohne unkontrolliertes Risiko und mit nachgewiesener Edge.

**Nicht das Ziel:** Schnell live gehen. Jede Phase hat **Exit-Kriterien**. Die nächste Phase startet erst wenn die aktuelle nachweislich abgeschlossen ist — nicht nach Zeitplan, nach Kriterium.

Arbeitsmodus: **täglich bearbeiten**. Bei jedem Briefing wird der Status der aktuellen Phase geprüft und die nächste konkrete Aktion hervorgehoben.

---

## Phase 1 — Parser-Zuverlässigkeit

**Warum kritisch:** Falsch-Interpretation von Signalen ist der größte Einzelrisiko-Faktor. Bei Paper ärgerlich, bei Live = direkter Geldverlust. Bekannte Fehlinterpretationen: INHD-Edit, OMEX-Catchup.

### Aufgaben
- [ ] 100 Nachrichten aus `data/raw_messages.db` (2658 gesamt: 2134 Premium + 524 Biotech) ziehen, beide Kanäle
- [ ] Mit Opus als Tabelle aufbereiten
- [ ] Gemeinsam durchgehen — für jede Nachricht: was meint Jack wirklich, wie soll der Bot reagieren?
- [ ] Parser-Regeln präzise ableiten
- [ ] `parser.py` anpassen (mit Brainstorming-Skill — Design first)
- [ ] Regression-Test gegen die 100 Nachrichten (alle müssen korrekt geparst werden)
- [ ] Stichprobe über zusätzliche 200 Nachrichten ziehen — Genauigkeit messen

### Exit-Kriterium
**≥95% korrekte Parser-Interpretation** auf einem Sample von ≥300 Nachrichten aus beiden Kanälen, inklusive der bisher problematischen Edge-Cases (Edits, Catchups, mehrdeutige Signale, AH/PM-Zeiträume).

---

## Phase 2 — Paper-Profitabilität messen

**Warum kritisch:** Ohne nachgewiesene Edge ist Live-Trading Glücksspiel. Wir brauchen Zahlen, nicht Bauchgefühl.

### Aufgaben
- [ ] Metriken definieren die wir tracken: **Erwartungswert pro Trade** (positiv erforderlich), **Hit-Rate**, **durchschnittlicher Gewinn vs. Verlust**, **Sharpe**, **max Drawdown**, **Sample-Size**
- [ ] Analyzer-Reports so erweitern dass diese Metriken täglich/wöchentlich im Digest auftauchen
- [ ] Saubere Tracking-Infrastruktur: alle Trades müssen mit vollständigen Daten in DB landen (Entry, Exit, Fees, Slippage, PnL, Trade-Dauer, Tageszeit, Kanal)
- [ ] 4-8 Wochen stabiler Paper-Betrieb mit dem verbesserten Parser aus Phase 1

### Exit-Kriterium
- **Mindestens 4 Wochen** Paper-Betrieb nach Parser-Fix
- **Mindestens 30 tatsächlich gefüllte Trades** (nicht expired/cancelled) als Sample
- **Positiver Erwartungswert** nach Gebühren
- **Max Drawdown < 15%** des Paper-Startkapitals
- **Keine strukturellen Bugs** in den 4 Wochen

---

## Phase 3 — Track B Feld-Bestätigung

**Warum:** Die AH/PM-Order-Logik (`StopLimitOrder`, marketable `LimitOrder`) wurde am 2026-04-10 deployed, Dry-Test 2026-04-11 bestätigt. Im Live-Markt aber noch nicht beobachtet.

### Aufgaben
- [ ] Erste 5 echte Exits beobachten — im Log muss `LIMIT EXIT:` auftauchen (nicht `MARKET EXIT (fallback):`)
- [ ] Fill-Rate messen — welcher Prozentsatz der LimitOrder-Exits wird tatsächlich gefüllt?
- [ ] AH/PM-Fills explizit beobachten (wenn Jack in AH signalisiert und Bot exit triggered)
- [ ] Wenn Fill-Rate < 90% → Slippage dynamisch machen (größerer Band in AH/PM)

### Exit-Kriterium
- **≥5 LimitOrder-Exits erfolgreich gefüllt**
- **Mindestens 1 AH- oder PM-Exit erfolgreich gefüllt**
- **Keine hängenden Exits** (Limit nicht gefüllt, Position blieb stehen) — wenn doch, Slippage anpassen und nochmal

---

## Phase 4 — Kill-Switches und Risk Controls

**Warum kritisch:** Im Live-Betrieb darf ein Bug oder eine Pechsträhne niemals ungebremst weiterfeuern. Das System muss sich selbst abschalten können.

### Aufgaben
- [ ] Audit von `safety.py` — was existiert bereits an Risk Controls?
- [ ] **`max_daily_loss`** implementieren: absoluter Euro-Betrag, bei Erreichen → alle offenen Positionen schließen, keine neuen Entries, Telegram-Alert
- [ ] **`max_weekly_loss`**: analog, aber weekly
- [ ] **`max_consecutive_losses`**: nach N verlorenen Trades in Folge → Cool-Down, manueller Reset nötig
- [ ] **`max_positions_simultaneous`**: bereits vorhanden (5), für Live auf 3 senken
- [ ] **Position-Size anpassen** für Live: 10% statt 20% (bei Live ist Cash-Puffer wichtiger)
- [ ] **"Halt and notify"** State-Machine — Bot kann in einen Zustand wo er nur Positionen verwaltet aber keine neuen Entries annimmt

### Exit-Kriterium
- Alle oben genannten Kill-Switches implementiert, konfigurierbar via `.env`
- **Unit-Test oder manueller Test** dass jeder Switch einmal getriggert und korrekt gehandelt hat
- **Dokumentation** im `/root/signal_bot/CLAUDE.md` welche Switches existieren und wie sie zu konfigurieren sind

---

## Phase 5 — Error-Recovery-Edge-Cases

**Warum:** Crashes und Disconnects passieren. Die Frage ist ob das System sauber wiederanläuft oder Positionen in undefiniertem Zustand hinterlässt.

### Aufgaben
- [ ] **IBKR-Reconnect bei offenen Positionen** — State wird korrekt aus IBKR neu geholt, keine Duplikate, keine verlorenen Positionen
- [ ] **Orphaned Orders** — Orders die bei IBKR liegen aber nicht in unserer DB (oder umgekehrt) werden beim Start erkannt und geloggt
- [ ] **Stuck pending orders** — Watchdog erkennt das schon, aber: gibt es automatische Aktion oder nur Alert?
- [ ] **Duplicate Signal Race** — Jack spammt 3 Nachrichten in 2 Sekunden → Deduplication greift
- [ ] **Channel Edit nach Order** — wenn Jack seinen Post editiert nachdem die Order schon raus ist

### Exit-Kriterium
- Für jeden Edge-Case: **dokumentiertes Verhalten** (was passiert, ist es korrekt) und wenn nötig Fix implementiert
- **Chaos-Test**: systemctl restart während offener Position — Bot erkennt Position nach Start korrekt

---

## Phase 6 — Live-Pilot-Vorbereitung

**Warum:** Die organisatorischen und operativen Dinge die vor dem Live-Gang zwingend erledigt sein müssen.

### Aufgaben
- [ ] **Steuer-Report-Export** — Skript das alle Trades eines Zeitraums im für die deutsche Einkommensteuer geeigneten Format ausgibt (Datum, Ticker, Kauf-Preis, Verkaufs-Preis, Stückzahl, Gewinn/Verlust, Gebühren)
- [ ] **IBKR Live-Account einrichten** (separat zum Paper-Account DU7690936)
- [ ] **Start-Kapital 500-1000€** auf den Live-Account transferieren
- [ ] **`.env` für Live-Modus** vorbereiten (neuer Account-ID, reduzierte Position-Size, aktivierte Kill-Switches)
- [ ] **Rollback-Plan**: exakte Schritte um sofort zurück auf Paper zu wechseln wenn was passiert
- [ ] **Monitoring-Erhöhung**: Telegram-Alerts für jede Aktion im Live-Modus, nicht nur kritische

### Exit-Kriterium
- Steuer-Export funktioniert, wurde einmal händisch verifiziert
- Live-Account ist funktionsfähig, per `ib_insync` verbunden, wird aber noch nicht gehandelt
- Rollback-Plan im Vault dokumentiert

---

## Phase 6.5 — Channel-Skalierung (Diversifikation statt größere Trades)

**Strategie:** Wenn der Bot mit Jack als Single-Source profitabel läuft, **nicht** die Position-Size hochfahren — stattdessen mehr Signalquellen parallel dazuschalten und Position-Size pro Trade **reduzieren**. Diversifikation schlägt Konzentration.

**Kalibrierungspunkt:** Jack kostet $400/Jahr = $33/Monat → Sweet Spot für echte Solo-Trader ist $10–$80/Monat. Alles darüber ist meist Kurs-Vermarktung mit Signal-Beiwerk.

### Aufgaben
- [ ] **`scripts/evaluate_channel.py` bauen** — nimmt Channel-ID, läuft Resync → Parser → Backtest → 1-Seiten-Report (PnL, DD, Win-Rate, avg Hold, AH/PM-Anteil, Slippage-Empfindlichkeit). Wiederverwendbar für jede Kandidat-Gruppe.
- [ ] **Kandidaten-Pool sammeln** aus Reddit (r/pennystocks, r/Daytrading), X-Threads, Jacks eigenem Umfeld. Filter: $10–$80/Monat, Live-Entries mit Zeitstempel, Verluste offen gepostet, kein Copy-Trading/PAMM.
- [ ] **Jede Kandidat-Gruppe beitreten** (Free-Tier/Trial), History via Telethon ziehen, durch `evaluate_channel.py` jagen, objektiv bewerten
- [ ] **Multi-Channel im Bot aktivieren** — `listener.py` Channel-Liste erweitern, Channel-Quelle pro Trade in DB tracken (für späteres Per-Channel-PnL)
- [ ] **Position-Size reduzieren** proportional zur Channel-Anzahl: 2 Channels → 10% statt 20%, 4 Channels → 5%, usw.
- [ ] **Pro Channel Kill-Switch** — wenn ein Channel über N Trades negativen EV zeigt, wird er automatisch deaktiviert

### Exit-Kriterium
- Mindestens **2, maximal 4 Channels** aktiv im Paper-Betrieb
- Jeder aktive Channel hat eigenen Backtest-Report im Vault mit positiver Baseline
- Gesamt-Portfolio-Drawdown **besser** als Jack-Single-Source-Baseline (Diversifikations-Vorteil nachgewiesen)

---

## Phase 7 — Live-Pilot

**Endlich.** Kleiner Betrag, strikte Kontrolle, sehr enges Monitoring.

### Aufgaben
- [ ] **Go-Live** mit 500-1000€, reduzierten Position-Sizes, aktivierten Kill-Switches
- [ ] **Täglich manuelles Monitoring** — nicht nur der Digest, auch Direct-Checks der DB und Logs
- [ ] **Wöchentlich Review**: PnL, Fills vs. Paper-Erwartung, Probleme, Kill-Switch-Trigger
- [ ] **Nach 3-4 Wochen Go/No-Go-Entscheidung**: Skalierung auf größere Beträge, oder zurück in eine Phase zwecks weiterer Verbesserung

### Exit-Kriterium (für Skalierung)
- **Positiver Erwartungswert** im Live-Betrieb, kein signifikanter Unterschied zu Paper
- **Kein einziger "Bot-Fehler" der Geld gekostet hat** (Bug, Race, Missverständnis)
- **Alle Kill-Switches haben sich bewährt** (oder wurden nie nötig, was auch OK ist)

---

## Parallele Sub-Projekte

- [[Claude Daily Reports]] — automatisierte Opus-Reports (Morning/Evening/Weekly) über @Jacksanalyse_bot. **Abhängigkeit:** wird erst nach Parser Rebuild Phase B gebaut. Geplanter `analyzer.py` Daily Digest 23:30 wird dadurch ersetzt.
- [[Parser Rebuild — Stress Test Phase A]] — aktueller Fokus von Phase 1
- [[Parser Rebuild — Phase B Review Queue]] — manuelle Review nach Backtest-Abschluss

## TODO-After-Liste (nach Phase 1 + Testcenter)

- [ ] [[Conditional Watchlist Auto-Entry]] — Setup-Ankündigungen (Levels/Pattern) automatisch überwachen, bei Trigger Alert/Entry. **Vorher im Testcenter simulieren** ob positiver EV. Motivierender Case: LAES 5113 → 5409.
- [ ] **Multi-Signal-Parser (Sub-Task Phase 1)** — Parser-Output von `Signal` → `List[Signal]` umstellen (Schema-Change, Empfehlung "Option B"). Claude entscheidet selbst wieviele Tickers in einer Nachricht stecken; signal_manager loopt über Liste. Motivierender Case: RADX #9 (msg 4200) — MIST-Nachkauf @1.80 + RADX-Status in 1 Nachricht, aktueller Parser verliert MIST. Aufwand ~1 Tag. Abhängigkeit: nach Parser-Review komplett, vor Testcenter-Bau.

## Aktueller Stand (2026-04-11)

- **Aktive Phase:** Phase 1 (Parser-Zuverlässigkeit)
- **Gerade in Arbeit:** P3 Wochenendprojekt — 100 Nachrichten analysieren
- **Abgeschlossen aus Phase 3 bereits:** Track B Code-Review + Dry-Test (2026-04-11)
- **Nicht angefangen:** Phase 2-7

## Daily Workflow
1. **Briefing** am Session-Start (Shortcut) — pulled Status-Check, Daily Note, aktuelle Phase aus dieser Roadmap
2. **Arbeit an den offenen Aufgaben der aktuellen Phase**
3. **Check-off** erledigter Aufgaben in dieser Datei
4. **Daily Note** mit Zusammenfassung am Session-Ende

Roadmap-Änderungen werden hier direkt eingepflegt — nicht in neue Dateien, nicht in die Memory.
