# Gemeinschaftspraxis Günther – neue Website (Prototyp)

Stand: 23. November 2026 (Runde 4: Hero auf dem Handy, neues Praxisblau `#377EC3`) · Agentur: Grafitecture

## Inhalt des Pakets

| Pfad | Zweck |
|---|---|
| `dist/` | Fertige Website in drei Sprachen: Deutsch im Wurzelverzeichnis, Englisch unter `en/`, Türkisch unter `tr/` – je `index.html`, `faq.html`, `dr-evelyne-guenther.html`, `dr-andreas-guenther.html`; dazu `impressum.html` und `datenschutz.html` (nur Deutsch, aus allen Sprachen verlinkt), Assets, `robots.txt`, `sitemap.xml` (mit hreflang), `llms.txt` |
| `praesentation/praxis-guenther-praesentation.html` | Alle Seiten und alle drei Sprachen in **einer** Datei (Schriften und Bilder eingebettet) – zum Zeigen auf jedem Gerät, ohne Entwurfsbalken |
| `artefakt/` | Dieselbe Präsentation als Ordner mit getrennten Dateien – so als privater Link auf claude.ai veröffentlicht (mit einer kleinen Entwurfszeile ganz unten im Rot des Notfall-Bands) |
| `src/` | Seiteninhalte (`pages/*.html` Deutsch, `pages/en/`, `pages/tr/`), Notfall-Band (`partials/`), Rechtstexte (`legal/`), FAQ-Daten (`faq.json`, `faq.en.json`, `faq.tr.json`), strukturierte Daten (`jsonld/`) |
| `assets/` | CSS (Designsystem), JS, Schriften (Fira Sans, selbst gehostet), Logo-SVGs, Fotos |
| `tools/` | `build.py` (baut `dist/`, Präsentation, Artefakt), `i18n.py` (Texte von Kopf, Fuß, Team, Formularen, Metadaten in DE/EN/TR), `signet_paths.py` (Pfade des Original-Signets), `grade_photos.py` + `make_photos.py` (Farbangleichung der Praxisfotos), Screenshot-Helfer |
| `vercel.json` | Clean URLs (`/faq` statt `/faq.html`), Caching und Sicherheits-Header. `/assets` wird ein Jahr `immutable` gecacht – deshalb bindet `build.py` CSS und JS mit Prüfsumme ein (`site.css?v=…`, Funktion `versioned`), sonst sehen Besucher Änderungen nicht. Ein geändertes Bild oder eine geänderte Schrift unter neuem Dateinamen ablegen. |

Bauen: `python3 tools/build.py`
Fotos neu erzeugen (nur wenn sich Quellbilder ändern): `PRAXIS_SRC=…/WEBSEITE_DATEN/PRAXIS python3 tools/make_photos.py`.
Repository: `github.com/grafitecture/gemeinschaftspraxis_guenther` (Branch `main`). Deploy: GitHub → Vercel; `vercel.json` setzt `outputDirectory: dist`, Vercel liefert also direkt den fertigen Ordner `dist/` aus (kein Build-Schritt nötig – vor jedem Push `python3 tools/build.py` laufen lassen). **Vor dem Livegang** im `<head>` die Zeile `noindex, nofollow` entfernen (steht in `tools/build.py`, Funktion `head`).

Testen der Öffnungs-Logik: `index.html?jetzt=2026-11-23T09:30` (geöffnet) bzw. `?jetzt=2026-11-23T20:30` (geschlossen) simuliert eine Uhrzeit.

Sprachen: Live-Adressen `/`, `/en`, `/tr` (plus `/faq`, `/en/faq` usw.). Jede Seite verweist per `hreflang` auf ihre Geschwister, `x-default` ist Deutsch. In der Präsentation heißen die Routen `#start`, `#faq`, `#en`, `#en-faq`, `#tr-evelyne` usw.

## Designsystem

- **Hausfarben**: Blau `#377EC3` und Grau `#9BA2A7`. Seit 23. November 2026 auf Wunsch **ein** Blau auf der ganzen Seite: Überschriften, kleine Überschriften, Links, Buttons, blaue Flächen, Logo, Signet, Favicon, Haus im Fuß und Vorschaubild in `#377EC3` (vorher Praxisblau `#0080C9` plus Tiefblau `#006BA8`). Abgeleitet: Fläche `#E6F0F9`, leuchtendes G `#4592DE`, Hover der Haupt-Buttons `#306FAB`. Kontrast `#377EC3` auf Weiß 4,3 : 1 – für große Schrift ausreichend, für kleine Schrift (Links, Buttons, Text auf Blau) knapp unter AA (4,5 : 1); falls nötig, kleine Schrift in `#306FAB` (5,3 : 1) setzen. Alle Texte außer Überschriften in `#5A6268` (Praxisgrau, dunkler gestuft, 6,2 : 1) – wie der Einleitungstext. Dunkle Flächen `#2E3438`. Flächen `#F3F6F8` / `#E5F2FA` / `#EEF0F1`.
- **Linien und Ecken**: Alle Linien 1 px, hellgrau `#DDE1E3`; auf getönten Flächen (Sprechzeiten, Leistungen, Fragen, Haltung auf den Arztseiten) weiß. Bilder und Flächen (Fotos, Karten, Instagram-Kacheln, Kästen, Dialoge) mit leichter Rundung (8 px, `--r`); Buttons, Schaltflächen und kleine Schilder bleiben knapp (2 px, `--pill`); Punkte und runde Icons bleiben rund; Flächen über die ganze Breite ohne Rundung.
- **Überschriften** immer im kräftigen Schnitt (Fira Sans SemiBold 600).
- **Unterseiten** (Häufige Fragen, Impressum, Datenschutz) liegen auf hellgrauer Fläche `#EEF0F1` zwischen weißem Kopf und weißem Fuß (`.subpage`), damit man sie sofort als Unterseite erkennt; Linien darauf weiß, Themen-Schaltflächen und Hinweiskästen weiß.
- **Kopfzeile**: bleibt beim Scrollen oben stehen (sticky), ohne Linie darunter. Beim Öffnen der Seite ist der Schriftzug groß und skaliert auf den ersten 160 px Scrollweg stufenlos auf seine Endgröße (`--hs` in `site.js`). (Varianten mit Logo dicht über der Hero-Überschrift bzw. „erst Logo, dann Seite“ wurden ausprobiert und auf Wunsch zurückgenommen.) Nur Logo, Navigation und ein kleiner Sprachumschalter ohne Globus (DE/EN/TR); mobil öffnet ein Hamburger aus drei Linien im Praxisblau `#377EC3` das Menü (geöffnet wird daraus ein X, Beschriftung für Screenreader „Menü“/„Schließen“) – Telefon und „Termin anfragen“ sind aus dem Kopf entfernt (die Aktionsleiste unten auf dem Handy ist ebenfalls entfernt).
- **Schrift**: Fira Sans 300/400/500/600, selbst gehostet (keine Google-Fonts-Verbindung → DSGVO). Zeichensatz um Latin Extended-A erweitert, damit Türkisch (ğ, ş, İ) in Fira Sans erscheint.
- **Typoskala**: Perfect Fourth (1,333) auf dem Desktop, fließend per `clamp()` zwischen 360 und 1440 px; auf dem Smartphone 1,2, damit Komposita wie „Hausarztpraxis“ nicht unschön umbrechen.
- **Logo (Original aus `DATEN/`)**: `LOGO.pdf`, `LOGO_.VARIANTE.pdf` und `SIGNET.pdf` als SVG übernommen (`logo-zeile.svg`, `logo-block.svg`, `signet.svg`; Formen exakt, Blau seit 23.11.2026 `#377EC3` statt `#0080C9`). Einsatz:
  - Kopf: nur der Schriftzug „Gemeinschaftspraxis Günther“ ohne Signet, größer. Fuß: Signet + Schriftzug.
  - Hero-Überschrift immer zweizeilig („Ihre Hausarztpraxis / in Viernheim.“), die Größe passt sich der Spaltenbreite an. Sie steht mittig neben dem Foto. Einleitung darunter, emotional und ohne Leistungen: „Seit 1970 ist die Kreuzstraße 13 eine Adresse, der Viernheim vertraut. Heute sind hier Dr. Evelyne Günther, Dr. Andreas Günther und unser Team für Sie da – persönlich und mit Herz.“ (Die Praxis besteht seit 1970, damals mit anderen Ärzten – siehe Zeitstrahl.) Der Hinweis auf die Parkplätze steht dort nicht mehr (weiter in FAQ und Instagram).
  - **Hero auf dem Handy (bis 559 px)**: Reihenfolge Überschrift → Foto → Buttons. Das Foto geht über die volle Inhaltsbreite, das G sitzt im Foto (oben links). Einleitung und – auf Englisch/Türkisch – der Sprachhinweis entfallen. Statt „Anrufen“ und „Termin“ stehen dort zwei gleich breite Buttons nur mit Icon: Telefon und E-Mail (Beschriftung für Screenreader bleibt). Umsetzung rein per CSS (`.hero__text` wird `display: contents`), Markup gleich für alle Größen.
  - **Hero**: Das Signet groß über dem Abendfoto. Beim Laden fährt der graue Versatz hinter dem blauen G heraus – das Logo „baut sich“ wie die Profilbuchstaben an der Fassade. Während der Sprechzeiten leuchtet das G wie das hinterleuchtete G am Haus.
  - Favicon, Instagram-Avatar und Feed-Kacheln.
- **Haus im Fuß (`haus.pdf`)**: So eingesetzt wie auf der Visitenkarte im `PRINT`-Ordner – oben Logo, Ärzte mit Rollen, Sprechzeiten; darunter links Adresse, Telefon, Fax und E-Mail, rechts das Haus – auf dem Desktop mittig unter den Spalten „Sprechzeiten“ und „Praxis“, mit Abstand zum rechten Rand; auf dem Handy mittig – auf der hellgrauen Grundlinie (die Linien aus der Druckdatei sind entfernt); darunter nur noch das Copyright. Arztnamen und Spaltenüberschriften („Sprechzeiten“, „Praxis“) im Fuß einheitlich im Praxisblau `#377EC3`. Sprachwahl nur im Kopf. Neu für die Website: **Während der Sprechzeiten leuchten die Fenster.** Das Haus verlinkt auf die Routenplanung (Google Maps).
- **Fotos (`PRAXIS/`)**: Die echten Fotos bleiben in ihrem Stil, sie werden nur farblich angeglichen (`tools/grade_photos.py`): Weißabgleich, Blautöne bleiben und rücken Richtung Praxisblau, warme Töne werden zurückgenommen, Schatten leicht graublau, Lichter kühl-neutral, sanfte Kurve, leichte Vignette. Einsatz: Hero (Haus am Abend), Mosaik „Die Praxis“ mit dem **Empfang** groß, Außenreihe (G, Straße, Abend), Gartenreihe (vier Fotos, im Chat nachgeliefert: Überblick, Sessel unter dem Kugelahorn, zwei Sessel vor der Hecke, Rasen vor der Fassade), Arztseiten, Instagram. Quelle der Gartenfotos: `/home/claude/neu/GARTEN` → `foto-garten*.webp`. Alle Praxisfotos stehen auf Wunsch **ohne Bildunterschriften** (Beschreibung nur im `alt`-Text für Screenreader und Suchmaschinen).
- **Porträts – Demo-Serie (KI)**: Sieben erfundene Personen als einheitliche Serie, erzeugt mit Higgsfield (Nano Banana 2.1, 2K, quadratisch): ein Leitbild (Andreas), die übrigen sechs mit dem Leitbild als Vorlage für Hintergrund, Licht, Ausschnitt und Farbe. Heller Praxishintergrund, kühles Weiß/Hellgrau/gedecktes Blau; Ärzte im weißen Kittel, Team in schieferblauen Kasacks; Evelyne um 40. Nur für die Präsentation – nicht live verwenden. Übernahme aus Higgsfield über die Browser-Ansicht (800 × 800 px), Nachbearbeitung mit `tools/team_photos.py` (leichte Glättung, Farbangleichung an die Praxisfotos). Ohne Datei `assets/img/team-<name>.webp` zeigt die Seite eine graue Fläche (`.ph`).
  - Ärzte: Dr. Evelyne Günther, Dr. Andreas Günther.
  - Mitarbeiterinnen mit **fiktiven Namen und Texten**: Claudia Wendt (Empfang und Termine), Monika Berger (Praxisorganisation), Renate Hofmann (Labor und Blutabnahme), Lena Maurer (Impfungen und Vorsorge), Sophie Keller (Empfang und Rezepte).
- **Notfall-Band „Außerhalb der Sprechzeiten“**: kompakt ganz unten auf jeder Seite, nach dem Fuß (Text in `src/partials/sos.de.html`, `.en`, `.tr`). Farbe Signalrot `#C8102E` (Notfall); Weiß darauf 5,9 : 1. Inhalt: 112, 116 117 und unter „In der Nähe“ die Notaufnahme St. Josef-Krankenhaus mit der Nummer 06204 703-0 in der ersten Zeile (die Bereitschaftsdienstzentrale Bergstraße ist auf Wunsch entfernt).
- **Blaue Sektionen über die ganze Breite** (Praxisblau `#377EC3`, invertiert):
  - **Aktuell**: Überschrift und Meldungen weiß, Linien halbtransparent weiß; der Impf-Check steht als weiße Karte auf dem Blau. Die Schließung „zwischen den Jahren“ bekommt ein weißes Schild mit roter Schrift (Datum), Überschrift und Text weiß.
  - **Wir bilden aus.**: als Balken direkt über dem Fuß; weiße Überschrift und Schrift, weißer Button mit blauer Schrift.
- **Rot** nur für Notfall und Schließzeiten: Notfall-Band in Signalrot `#C8102E`; Datum der Meldung „Praxis zwischen den Jahren geschlossen“ unter Aktuell als weißes Schild mit roter Schrift `#B3261E` (6,6 : 1 auf Weiß).
- **Farbcode der Ärzte**: Blau für Dr. Evelyne Günther, Grau für Dr. Andreas Günther.
- **Impressum und Datenschutz**: neu geschrieben für den Betrieb auf Vercel (Stand November 2026): § 5 DDG statt § 5 TMG, Landesärztekammer Hessen (Hanauer Landstraße 152) und KV Hessen (Europa-Allee 90) mit aktuellen Anschriften, kein Link mehr zur EU-Streitschlichtungsplattform (seit 20. Juli 2025 abgeschaltet), Vercel als Auftragsverarbeiter mit DPF-Zertifizierung, keine Cookies, kein Tracking, Gesundheitsdaten nach Art. 9 DSGVO, Aufsichtsbehörde HBDI. Auf beiden Seiten das Grafitecture-Feld im Agentur-Standard wie auf raumrent.de (lindgrüne Fläche `#DAFD55`, Text `#435960`, Grafitecture-Logo, „Marken mit KI.“, Link zu grafitecture.de; Logo in `tools/gt_logo.svg`); in der Datenschutzerklärung zusätzlich Grafitecture als technischer Dienstleister (Auftragsverarbeiter).
- **Vorschaubild** für Messenger/soziale Netzwerke (`og-bild.png`): Original-Logo, Claim, Hausfoto.

## Was die Seite „state of the art“ macht

- **Live-Status als Licht** (Zeitzone Berlin, inkl. Feiertage und Praxisurlaub): Während der Sprechzeiten leuchtet das G im Hero und die Fenster im Fuß leuchten. Die Textanzeige „Jetzt geöffnet …“ / „Gerade geschlossen …“ ist auf Wunsch entfernt, ebenso der Schließhinweis unter den Sprechzeiten (die Schließung steht in Rot unter „Aktuell“).
- **Schluss-Abschnitt** „Wir sind für Sie da.“ (Anrufen, Termin, Route) über dem Fuß ist auf Wunsch entfernt; die Seite endet mit „Wir bilden aus.“, dann Fuß und Notfall-Band.
- **Kontextabhängige Haupt-Aktion**: Praxis offen → „Anrufen“ ist der Hauptbutton; geschlossen → „Termin online anfragen“ rückt nach vorn (auf dem Handy wird dann E-Mail zum Hauptbutton). „Anrufen“ und „Termin“ sind immer gleich breit; reicht die Textspalte nicht für beide nebeneinander (Tablet schmal, Desktop um 1024–1200 px), stehen sie gleich breit untereinander.
- **Termin anfragen** und **Folgerezept bestellen** als Dialoge (Prototyp – senden nichts). Im Hero stehen nur noch „Termin online anfragen“ und „Anrufen“; die Zeile „Folgerezept bestellen – für Medikamente, die wir Ihnen bereits verordnet haben.“ ist dort auf Wunsch entfernt (das Folgerezept bleibt unter „Was können wir für Sie tun?“ erreichbar).
- **„Was können wir für Sie tun?“** kompakt und dezent: sechs Anliegen (Termin, Akute Beschwerden, Folgerezept, Blutabnahme, Impfung, Hausbesuch) in drei Spalten (Tablet zwei, Handy eine), kleines Linien-Icon ohne Kreis, Überschrift klein im Praxisblau, Text klein, Textlinks statt Buttons.
- **Impf-Check** nach STIKO 2026 (Alter + Vorerkrankung → passende Impfungen).
- **Sprechzeiten** als schlichte Tabelle (Tag · Vormittag · Nachmittag, Wochenende in einer Zeile), der heutige Tag in Blau hervorgehoben, Blutabnahme als Zeile darunter.
- **Anfahrt**: Der Abschnitt „So finden Sie uns“ ist auf Wunsch entfernt (Lageplan, Wegbeschreibung, Bildfolge Eingang → Empfang). Route: Haus im Fuß (Google Maps); Adresse und Parken stehen im Fuß, im Hero und in den FAQ.
- **FAQ-Seite** mit 36 Fragen (Englisch und Türkisch 37, zusätzlich „In welcher Sprache?“), Themen-Sprungmarken, Direktlinks. Suchfeld und Seitenkasten „Ihre Frage war nicht dabei?“ sind auf Wunsch entfernt; die Fragen stehen in einer Spalte. Der Abschnitt „Häufige Fragen“ auf der Startseite ist ebenfalls entfernt – die FAQ-Seite erreicht man über die Navigation und den Fuß.
- **Dreisprachig**: Deutsch, Englisch, Türkisch – inklusive Team, Fuß, Live-Status, Impf-Check, Formulare.
- **KI- und Suchmaschinen-Lesbarkeit**: JSON-LD (`MedicalClinic`, `Person`, `FAQPage`, `BreadcrumbList`), `llms.txt`, `sitemap.xml`, antwortorientierte Texte. Google zeigt seit dem 7. Mai 2026 keine FAQ-Rich-Results mehr – das Markup bleibt sinnvoll, weil Suchmaschinen und KI-Systeme es lesen.
- **Barrierefreiheit**: Kontraste ≥ 4,5 : 1 (Ausnahme: Blau `#377EC3` auf Weiß 4,3 : 1, siehe Hausfarben), Tastaturbedienung, sichtbarer Fokus, Skip-Link, `prefers-reduced-motion` (dann keine Logo-Animation), Touch-Ziele ≥ 44 px.
- **Instagram**: Beispiel-Feed (Entwurf). Die Beiträge stehen auch auf der englischen und türkischen Seite auf Deutsch (`lang="de"`), so wie sie auf Instagram erscheinen; Überschrift und Button folgen der Seitensprache. Live sollte der echte Feed erst nach Klick geladen werden (2-Klick-Lösung).

## Offene Punkte – mit der Praxis klären

1. **Fotos**: Echte Porträts der Ärzte und des Teams (Fotoshooting, quadratisch, möglichst gleicher Hintergrund und gleiches Licht) – sie ersetzen die grauen Flächen. Für alle Abgebildeten eine schriftliche Einwilligung zur Veröffentlichung einholen.
2. **Rechtstexte bestätigen**: Rechtsform der Gemeinschaftspraxis (GbR oder Partnerschaft – bei Partnerschaft Registerangaben ergänzen), Facharzt­bezeichnungen, ob ein Datenschutzbeauftragter benannt ist (Pflicht ab 20 Personen, die ständig mit Daten arbeiten), ob die Patienteninformation zum Datenschutz an der Anmeldung ausliegt, Auftragsverarbeitungsvertrag zwischen Praxis und Grafitecture für die technische Betreuung. Vercel-Konto mit Pro-Tarif nutzen (Hobby ist nur für nicht-kommerzielle Projekte) und den Auftragsverarbeitungsvertrag (DPA) dokumentieren. Sobald Online-Termine oder Rezeptbestellung angebunden sind, Datenschutzerklärung um den Anbieter ergänzen. Abschließende Prüfung durch eine Rechtsberatung empfohlen.
3. **Team**: Echte Namen, Aufgaben und Kurztexte der Mitarbeiterinnen – die jetzigen sind erfunden. Wer möchte namentlich auf der Seite stehen?
4. **Online-Terminsystem** auswählen (z. B. Doctolib, samedi o. ä.) und **verschlüsselten Dienst für Rezeptbestellungen** festlegen; Datenschutzerklärung anpassen.
5. **Neue Patienten**: Aufnahme ja/nein? FAQ-Antwort ist bewusst offen formuliert.
6. **Privatpatienten/Selbstzahler**: laut Arztverzeichnis ja – bitte bestätigen.
7. **Palliativmedizin**: Zusatzbezeichnung vorhanden – als Leistung nennen?
8. **Lungenkrebs-Früherkennung**: Bietet die Praxis Beratung/Teilnahmeprüfung an?
9. **Akupunktur**: Darf die Praxis bei LWS-/Kniearthrose-Schmerzen über die Kasse abrechnen?
10. **Barrierefreiheit der Räume** (Stufen, Aufzug, Rollstuhl) – dann in den FAQ ergänzen.
11. **Schließzeiten** pflegen in `assets/js/site.js` (`CLOSED`, `HOLIDAYS`) und in `src/jsonld/start.json`. Heiligabend (24.12.) offen?
12. **Korrektur gegenüber der alten Seite**: Check-up ab 35 alle **drei** Jahre (Hautkrebs-Screening alle zwei Jahre). Alte Bereitschaftsdienst-Zeiten durch 116 117 ersetzt.
13. **Haltungssätze** auf den Arztseiten sind Textvorschläge → freigeben lassen. Persönliche Angaben (Geburtsjahr, Familie) weiter gewünscht?
14. **Ausbildung**: Jahrgang 2027 bestätigen.
15. **Zeitstrahl prüfen**: Die Jahreszahlen (u. a. Umbau 2019 und 2023) wurden aus den Fotos abgeleitet.
16. **Sprachen in der Sprechstunde**: Welche Sprachen spricht das Team?
17. **Übersetzungen** von Muttersprachlern gegenlesen lassen, besonders Türkisch.

## Quellen für die aktuellen Inhalte

- STIKO-Empfehlungen 2026 (Grippe, Pneumokokken, Gürtelrose ab 60; RSV einmalig ab 75 bzw. ab 60 mit Grunderkrankung; Corona jährlich ab 75 seit Juli 2026)
- G-BA / KBV: Lungenkrebs-Früherkennung seit 1. April 2026 für starke Raucher 50–75
- ePA-Nutzungspflicht für Praxen seit 1. Oktober 2025
- Bundesgesundheitsministerium: Check-up und Krebsfrüherkennung; E-Rezept-Einlösewege
- Verbraucherzentrale: Akupunktur als Kassenleistung
- Primärversorgungssystem: Referentenentwurf angekündigt, Start frühestens 2028
- Google Search Central: Ende der FAQ-Rich-Results am 7. Mai 2026
- Landesärztekammer Hessen, Merkblatt zu Pflichtangaben: Kammer Hanauer Landstraße 152, KV Hessen Europa-Allee 90
- IHK / Händlerbund: Abschaltung der EU-OS-Plattform zum 20. Juli 2025, Hinweis im Impressum entfernen
- Vercel: Zertifizierung nach dem EU-US Data Privacy Framework, Privacy Notice (Stand 1. Juni 2026), Data Processing Addendum
- HBDI: Anschrift Gustav-Stresemann-Ring 1, 65189 Wiesbaden
