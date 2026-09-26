# Changelog

Alle nennenswerten Änderungen an diesem Projekt. Format angelehnt an
[Keep a Changelog](https://keepachangelog.com/de/1.1.0/).

Das Projekt ist nicht versioniert — die Einträge sind nach Datum gruppiert.

## 2026-09-26

### Hinzugefügt

- Hell/Dunkel-Umschalter in der Vorschau. Die Wahl landet in `localStorage`;
  ohne gespeicherte Wahl folgt die Seite `prefers-color-scheme`.
- `build-preview.py` und `preview-template.html`. `index.html` wird daraus
  erzeugt und nicht mehr von Hand bearbeitet.
- Abschnitt „Farben" im README, der den Farbvertrag der Icons beschreibt.

### Geändert

- Alle 18 Icons tragen ihre Geometrie als `currentColor` und übernehmen damit
  die Textfarbe ihrer Umgebung. Zehn Dateien waren noch auf `#000`/`black`
  festgenagelt, acht nutzten `currentColor` bereits.
- Der grüne Akzent der Marstek-Icons hängt an `var(--icon-accent, #1FC855)`.
  Das Literal bleibt als Präsentationsattribut daneben stehen, damit auch
  Renderer ohne CSS-Unterstützung Grün zeigen.
- Der SVG-Code steht fest in `index.html`, statt zur Laufzeit per `fetch`
  geholt zu werden. Farbe lässt sich nur an einem inline eingebundenen SVG
  ändern; über `file://` scheiterte der `fetch` an CORS und fiel auf `<img>`
  zurück, wo genau das nicht mehr ging. Die Seite lädt jetzt keine externe
  Ressource mehr und funktioniert per Doppelklick ohne Server.

### Entfernt

- Der graue Kasten hinter den Icons. Die Icons stehen direkt auf der Karte,
  die Kacheln bleiben. Die Variable `--tile-bg` wird damit nicht mehr gebraucht.
- `fetch`, `DOMParser`, das Umfärben per JavaScript und der `<img>`-Fallback in
  der Vorschau. Die Aufgaben erledigt jetzt das Build-Skript.

### Behoben

- Die Statistik-Box am Seitenende hatte weiße Schrift auf hellem Grund und war
  dadurch unlesbar.

### Anmerkung

`@media (prefers-color-scheme: dark)` liegt bewusst **nicht** in den
SVG-Dateien. Es meldet die Einstellung des Betriebssystems, nicht den
Hintergrund der Seite — ein Icon auf heller Oberfläche bei dunklem System wäre
sonst weiß auf weiß. Über hell/dunkel entscheidet die Umgebung. Der Preis: als
`<img>` eingebunden bleibt ein Icon schwarz, dort reicht kein CSS hinein.

## 2026-09-20

### Hinzugefügt

- Sieben Marstek-Icons: Jupiter C, C+ und C++, Venus D, D+ und D++, Venus E.

### Geändert

- `marstek_b2500.svg` durch den aktuellen Export ersetzt.

### Behoben

- Den Exporten fehlte die `viewBox`. In der Vorschau landen die Icons in einer
  120×120-Kachel — ohne `viewBox` schrumpft nur das Viewport-Rechteck, der
  Inhalt bleibt auf 960 px und wird beschnitten statt skaliert.
- Die Dateinamen der `+`- und `++`-Varianten enthalten ein `+`, das über
  mehrere URL-Rewrites als Leerzeichen gelesen werden kann. Die Vorschau
  kodierte den Pfad daher mit `encodeURIComponent` (inzwischen hinfällig, weil
  die SVGs fest im Dokument stehen).

## 2026-07-05

### Hinzugefügt

- Erste Fassung der Icon-Sammlung mit Vorschau-Seite.
- README mit Link auf die Vorschau und Anleitung für GitHub Pages.

### Behoben

- Icons wurden doppelt gerendert; das Grid wird vor dem Aufbau geleert und
  gegen einen zweiten Durchlauf abgesichert.

### Geändert

- Icons alphabetisch sortiert.
