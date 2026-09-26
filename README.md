# icons4homey

Custom SVG Icons Collection

## Preview

[**View Icon Preview →**](https://htmlpreview.github.io/?https://github.com/RothMick/icons4homey/blob/main/index.html)

Klick den Link um alle Icons in einer interaktiven Vorschau zu sehen.

## Icons

- Sun-Moon variations
- Garbage collection
- Awtrix
- NAS devices
- Gardena devices
- Marstek B2500
- Marstek Jupiter C / C+ / C++
- Marstek Venus D / D+ / D++
- Marstek Venus E

## Farben

Die Icons sind einfarbig ueber `currentColor` aufgebaut und uebernehmen damit die
Textfarbe ihrer Umgebung:

```html
<span style="color: #fff">
  <!-- SVG hier inline einbinden, nicht per <img> -->
</span>
```

Wichtig: Das funktioniert nur bei **inline eingebundenem** SVG. Ein per `<img src>`
geladenes SVG ist ein eigenes Dokument, in das kein CSS von aussen hineinreicht --
dort bleibt das Icon schwarz. Genau deshalb steht der SVG-Code in `index.html`
fest im Dokument und wird nicht zur Laufzeit nachgeladen.

Die Marstek-Icons haben zusaetzlich einen gruenen Akzent (Fuellstands- bzw.
Statusstrich). Der laesst sich ueber eine CSS-Variable umfaerben:

```css
.mein-icon { --icon-accent: #ff9800; }
```

Ohne gesetzte Variable bleibt es bei `#1FC855`. Standalone geoeffnet rendern alle
Icons unveraendert schwarz mit gruenem Akzent.

## Preview bauen

`index.html` ist **generiert** und wird nicht von Hand bearbeitet. Die SVGs stehen
fest im Dokument, damit sich ihre Farbe dort ueberhaupt aendern laesst -- und damit
die Seite ohne Server, offline und per Doppelklick ueber `file://` funktioniert.

Nach jedem neuen oder geaenderten Icon:

```bash
python3 build-preview.py
```

| Datei                   | Rolle                                              |
|-------------------------|----------------------------------------------------|
| `preview-template.html` | Layout, CSS, Theme-Umschalter -- hier wird editiert |
| `build-preview.py`      | baeckt alle `*.svg` in die Vorlage ein              |
| `index.html`            | Ergebnis, nicht von Hand anfassen                   |

Das Skript sortiert die Icons alphabetisch (Basismodell vor `+` und `++`), macht
die IDs pro Icon eindeutig und fasst die internen `<style>`-Bloecke der Icons zu
einer Regel in der Vorlage zusammen.

## GitHub Pages

Um GitHub Pages zu aktivieren und die Preview unter einer eigenen Domain zu hosten:

1. Gehe zu **Repository Settings**
2. Scroll zu **Pages**
3. Wähle "Deploy from a branch"
4. Branch: `main`, Folder: `/ (root)`
5. Die Preview wird dann unter `https://rothmick.github.io/icons4homey/` verfügbar
