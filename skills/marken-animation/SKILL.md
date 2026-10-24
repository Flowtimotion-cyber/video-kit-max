---
name: marken-animation
description: Kleine animierte Bausteine in der eigenen Marke bauen — Intro-Karte, Bauchbinde (Name + Rolle), Zitat-Karte für Referenzen, Logo-Outro — als HyperFrames-Komposition aus brand.json, in 16:9, 9:16 oder 1:1. Nutzen bei „Intro für das Retreat-Video“, „Bauchbinde für Anna“, „Zitat-Karte aus der Referenz“, „Outro mit Logo“.
---

# Marken-Animation

Vier Vorlagen, eine Markendatei. Du füllst Text ein, das Skript baut eine HTML-Komposition, HyperFrames rendert daraus ein Video.

| Vorlage | Was sie zeigt | Standard-Dauer |
|---|---|---|
| `intro` | Farbbalken wischt, dann Logo, Titel, Linie, Untertitel | 5 s |
| `bauchbinde` | Name und Rolle unten links, schiebt rein und raus | 5 s |
| `zitat` | Referenz-Zitat wortweise, Autor, Logo | 7 s |
| `outro` | Logo, Markenname, Claim, Website-Pille auf Primärfarbe | 5 s |

Alle Farben, Schriften und das Logo kommen aus `brand/brand.json`. Nichts davon in die Vorlagen schreiben.

## Voraussetzungen
- Node 18+, einmalig im Repo-Ordner: `npm install hyperframes@0.8.183` (oder `npx hyperframes` nutzen).
- Python 3.10+ für `tools/bauen.py`.
- Für das Rendern braucht HyperFrames ein Chromium. Wenn es keins findet: `npx playwright install chromium` und `HYPERFRAMES_BROWSER_PATH` auf die ausführbare Datei setzen.
- Die Vorlagen laden GSAP von cdnjs. Offline: `gsap.min.js` neben die `index.html` legen und den `<script src>` anpassen.

## Ablauf
1. Prüfen, ob `brand/brand.json` ausgefüllt ist (Name, Farben, Logo-Datei vorhanden). Wenn nicht, erst danach fragen. Ohne Logo bauen die Vorlagen trotzdem, nur ohne Logo.
2. Vorlage bauen:
   ```bash
   python3 tools/bauen.py intro --out out/intro --format breit --set TITEL="Retreat Mallorca 2026" --set UNTERTITEL="Fünf Tage, die bleiben"
   python3 tools/bauen.py zitat --out out/zitat-anna --format reels --set ZITAT="Ich bin als andere Frau zurückgekommen." --set AUTOR="Anna M., Teilnehmerin 2025"
   python3 tools/bauen.py outro --out out/outro --format reels
   ```
   Formate: `breit` (1920×1080), `reels` (1080×1920), `quadrat` (1080×1080) oder `BREITExHOEHE`. Dauer mit `--dauer 6`.
3. Standbild prüfen, bevor du renderst: `out/intro/index.html` im Browser öffnen, in der Konsole `window.__timelines["<ID>"].seek(2.5)` (die ID steht in der Ausgabe von `bauen.py`). Langer Text? Dann kürzen oder `--dauer` erhöhen, nicht die Schriftgröße in der Vorlage verkleinern.
4. Rendern:
   ```bash
   npx hyperframes render out/intro -o renders/intro.mp4 -f 25 --quiet
   ```
5. In den Schnitt einbauen (siehe Skill `social-clip`): Intro und Outro als eigene Clips vor und hinter das Material, Zitat-Karte als Zwischenschnitt.

## Bauchbinde über ein laufendes Video legen
Zwei Wege, je nachdem, was HyperFrames bei dir kann:
- **Mit Alpha:** `npx hyperframes render --help` ansehen. Gibt es eine Option für transparente Ausgabe (WebM/MOV mit Alpha), diese nutzen und mit ffmpeg überlagern:
  ```bash
  ffmpeg -i clip.mp4 -i renders/bb-anna.webm -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,2,7)'" -c:a copy clip_bb.mp4
  ```
- **Greenscreen (geht immer):** mit `--set HINTERGRUND=#00FF00` bauen, rendern, dann keyen:
  ```bash
  ffmpeg -i clip.mp4 -i renders/bb-anna.mp4 -filter_complex "[1:v]chromakey=0x00FF00:0.12:0.1[bb];[0:v][bb]overlay=0:0:enable='between(t,2,7)'" -c:a copy clip_bb.mp4
  ```
  `between(t,2,7)`: Bauchbinde läuft von Sekunde 2 bis 7. Die Bauchbinde selbst dauert 5 s, also passend wählen.

## Eigene Vorlagen
Eine Vorlage ist eine HTML-Datei mit `#root` (Attribute `data-composition-id`, `data-width`, `data-height`, `data-duration`) und einer pausierten GSAP-Timeline, die unter `window.__timelines[ID]` hängt. Platzhalter in `{{GROSSBUCHSTABEN}}`. Kopiere `intro.html`, ändere Layout und Timeline, lege sie unter `templates/` ab und rufe sie mit `bauen.py <name>` auf. Schriftgrößen immer relativ zu `--u` (ein Prozent der Breite), dann passt die Vorlage in allen drei Formaten.

Für aufwendigere Animationen (Montagen, Slideshows, Captions mit Effekten) die offiziellen HyperFrames-Skills installieren: `npx skills add heygen-com/hyperframes --all`. Die Vorlagen hier bleiben die schnellen Marken-Bausteine.

## Regeln
- Markenfarben und Logo nur aus `brand.json`. Keine Schriftgröße „mal eben“ in der Vorlage hartcodieren.
- Vor dem Rendern ein Standbild ansehen, nach dem Rendern das Video einmal abspielen.
- Dateien: Kompositionen nach `out/`, fertige Videos nach `renders/`. Beides ist in `.gitignore`.
