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

## Changelog

Was sich wann geändert hat, steht in [CHANGELOG.md](CHANGELOG.md).

## Farben

Die Icons sind einfarbig über `currentColor` aufgebaut und übernehmen damit die
Textfarbe ihrer Umgebung:

```html
<span style="color: #fff">
  <!-- SVG hier inline einbinden, nicht per <img> -->
</span>
```

Wichtig: Das funktioniert nur bei **inline eingebundenem** SVG. Ein per `<img src>`
geladenes SVG ist ein eigenes Dokument, in das kein CSS von außen hineinreicht --
dort bleibt das Icon schwarz. Genau deshalb steht der SVG-Code in `index.html`
fest im Dokument und wird nicht zur Laufzeit nachgeladen.

Die Marstek-Icons haben zusätzlich einen grünen Akzent (Füllstands- bzw.
Statusstrich). Der lässt sich über eine CSS-Variable umfärben:

```css
.mein-icon { --icon-accent: #ff9800; }
```

Ohne gesetzte Variable bleibt es bei `#1FC855`. Standalone geöffnet rendern alle
Icons unverändert schwarz mit grünem Akzent.

## Preview bauen

`index.html` ist **generiert** und wird nicht von Hand bearbeitet. Die SVGs stehen
fest im Dokument, damit sich ihre Farbe dort überhaupt ändern lässt -- und damit
die Seite ohne Server, offline und per Doppelklick über `file://` funktioniert.

Nach jedem neuen oder geänderten Icon:

```bash
python3 build-preview.py
```

| Datei                   | Rolle                                              |
|-------------------------|----------------------------------------------------|
| `preview-template.html` | Layout, CSS, Theme-Umschalter -- hier wird editiert |
| `build-preview.py`      | bäckt alle `*.svg` in die Vorlage ein              |
| `index.html`            | Ergebnis, nicht von Hand anfassen                   |

Das Skript sortiert die Icons alphabetisch (Basismodell vor `+` und `++`), macht
die IDs pro Icon eindeutig und fasst die internen `<style>`-Blöcke der Icons zu
einer Regel in der Vorlage zusammen.

## GitHub Pages

Um GitHub Pages zu aktivieren und die Preview unter einer eigenen Domain zu hosten:

1. Gehe zu **Repository Settings**
2. Scroll zu **Pages**
3. Wähle "Deploy from a branch"
4. Branch: `main`, Folder: `/ (root)`
5. Die Preview wird dann unter `https://rothmick.github.io/icons4homey/` verfügbar
