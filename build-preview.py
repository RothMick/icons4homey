#!/usr/bin/env python3
"""Baeckt alle SVGs dieses Ordners fest in index.html ein.

Warum ueberhaupt: Farbe laesst sich nur an einem SVG aendern, das inline im
Dokument steht. Ein per <img src> geladenes SVG ist ein eigenes Dokument, in das
kein CSS von aussen hineinreicht. Frueher holte die Seite die Dateien zur
Laufzeit per fetch -- das scheitert beim Oeffnen ueber file:// an CORS und fiel
dann auf <img> zurueck, wo das Umfaerben nicht mehr griff. Eingebacken
funktioniert die Vorschau ueberall, auch offline und ohne Server.

Aufruf:  python3 build-preview.py
Quelle:  preview-template.html + alle *.svg im selben Ordner
Ziel:    index.html  (generiert -- nicht von Hand bearbeiten)
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = 'http://www.w3.org/2000/svg'
XLINK_NS = 'http://www.w3.org/1999/xlink'
ET.register_namespace('', SVG_NS)
ET.register_namespace('xlink', XLINK_NS)

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / 'preview-template.html'
TARGET = HERE / 'index.html'
INDENT = ' ' * 12


def sort_key(path: Path):
    """Alphabetisch, aber Basismodell vor + und ++.

    Reines ASCII wuerde 'c+' vor 'c.svg' einsortieren, weil '+' (43) kleiner
    ist als '.' (46). Fuer den Leser gehoert das Grundmodell nach vorn.
    """
    stem = path.stem
    base = stem.rstrip('+')
    return (base, len(stem) - len(base))


def namespace_ids(svg: ET.Element, prefix: str) -> None:
    """IDs praefixen, damit sie im gemeinsamen Dokument eindeutig bleiben.

    Inline liegen alle Icons in EINEM ID-Namensraum. Figma vergibt Muster wie
    'path-3-inside-1_158_95'; zwei Exporte aus derselben Datei kollidieren, und
    url(#...) greift dann auf das zuerst eingebundene Icon.
    """
    mapping = {}
    for el in svg.iter():
        old = el.get('id')
        if old:
            new = f'{prefix}-{old}'
            mapping[old] = new
            el.set('id', new)
    if not mapping:
        return
    for el in svg.iter():
        for attr, value in list(el.attrib.items()):
            if '#' not in value:
                continue
            new_value = value
            for old, new in mapping.items():
                new_value = new_value.replace(f'url(#{old})', f'url(#{new})')
                if new_value == f'#{old}':
                    new_value = f'#{new}'
            if new_value != value:
                el.set(attr, new_value)


def strip_internal_style(svg: ET.Element) -> int:
    """Interne <style>-Bloecke entfernen.

    Beim Inlining wirken sie dokumentweit statt nur im eigenen SVG -- acht
    Marstek-Icons ergaeben acht identische .i4h-accent-Regeln. Die Regel steht
    stattdessen einmal in preview-template.html. Die class-Attribute bleiben,
    nur der Regeltraeger wandert.
    """
    removed = 0
    for parent in svg.iter():
        for child in list(parent):
            if child.tag == f'{{{SVG_NS}}}style':
                parent.remove(child)
                removed += 1
    return removed


def prepare(path: Path, index: int) -> str:
    svg = ET.fromstring(path.read_text())
    if svg.tag != f'{{{SVG_NS}}}svg':
        raise SystemExit(f'{path.name}: Wurzelelement ist kein <svg>')
    if not svg.get('viewBox'):
        raise SystemExit(f'{path.name}: keine viewBox, skaliert sonst nicht')

    # Feste Groesse raus, die Kachel bestimmt die Groesse ueber CSS
    svg.attrib.pop('width', None)
    svg.attrib.pop('height', None)
    svg.set('role', 'img')
    svg.set('aria-label', path.name)
    namespace_ids(svg, f'i{index}')
    strip_internal_style(svg)

    markup = ET.tostring(svg, encoding='unicode')
    # ElementTree schreibt den Default-Namespace als ns0, wenn schon registriert
    markup = markup.replace(f' xmlns:ns0="{SVG_NS}"', '').replace('ns0:', '')
    return INDENT + markup.strip()


def main() -> int:
    if not TEMPLATE.exists():
        raise SystemExit(f'Vorlage fehlt: {TEMPLATE.name}')

    files = sorted((p for p in HERE.glob('*.svg')), key=sort_key)
    if not files:
        raise SystemExit('Keine SVGs gefunden')

    cards = []
    styles_removed = 0
    for i, path in enumerate(files):
        before = path.read_text().count('<style')
        markup = prepare(path, i)
        styles_removed += before
        cards.append(
            f'{" " * 12}<div class="icon-card">\n'
            f'{" " * 16}<div class="icon-preview">\n'
            f'{markup}\n'
            f'{" " * 16}</div>\n'
            f'{" " * 16}<div class="icon-name">{path.name}</div>\n'
            f'{" " * 16}<div class="icon-size">SVG</div>\n'
            f'{" " * 12}</div>'
        )

    html = TEMPLATE.read_text()
    for marker in ('<!--ICONS-->', '<!--COUNT-->'):
        if marker not in html:
            raise SystemExit(f'Marker {marker} fehlt in {TEMPLATE.name}')

    banner = ('<!-- GENERIERT von build-preview.py aus preview-template.html '
              '+ den *.svg dieses Ordners.\n     Nicht von Hand bearbeiten - '
              'Aenderungen gehoeren in die Vorlage. -->\n')
    html = html.replace('<!--ICONS-->', '\n\n'.join(cards))
    html = html.replace('<!--COUNT-->', str(len(files)))
    html = html.replace('<!DOCTYPE html>\n', '<!DOCTYPE html>\n' + banner, 1)

    TARGET.write_text(html)
    print(f'index.html geschrieben: {len(files)} Icons eingebacken, '
          f'{styles_removed} interne <style>-Bloecke zusammengefasst, '
          f'{len(html) // 1024} KB')
    return 0


if __name__ == '__main__':
    sys.exit(main())
