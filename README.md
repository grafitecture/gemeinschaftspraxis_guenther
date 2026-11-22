# Gemeinschaftspraxis Günther – Website

Neue Website für die Gemeinschaftspraxis Günther, Kreuzstraße 13, Viernheim (gemeinschaftspraxis-guenther.de). Statische Seite in Deutsch, Englisch und Türkisch. Entwurf und technische Betreuung: Grafitecture GmbH.

- `dist/` – fertige Website, wird von Vercel ausgeliefert (`vercel.json` → `outputDirectory: dist`)
- `src/`, `assets/`, `tools/` – Quellen; neu bauen mit `python3 tools/build.py`
- `praesentation/` – alle Seiten in einer HTML-Datei zum Zeigen
- `UEBERGABE.md` – Designsystem, Funktionen, offene Punkte

Stand: Prototyp. Die Seite trägt `noindex, nofollow`; vor dem Livegang in `tools/build.py` (Funktion `head`) entfernen. Die Teamporträts sind KI-Demobilder mit erfundenen Namen und werden vor dem Livegang durch echte Fotos ersetzt.
