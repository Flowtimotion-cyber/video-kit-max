---
name: social-clip
description: Aus vorhandenem Videomaterial (Retreat-Aufnahmen, Referenz-Interviews, Location-Videos) fertige Clips schneiden — Sichten, beste Momente finden, kürzen, Hochkant/Quadrat/Breit, Untertitel in Markenfarben, Intro/Outro, Export für Instagram, TikTok, LinkedIn, YouTube. Nutzen bei „mach aus dem Interview drei Reels“, „schneide das Retreat-Video auf 60 Sekunden“, „Location-Clip für die Website“.
---

# Social-Clip aus vorhandenem Material

Du bekommst Rohmaterial und einen Wunsch („drei Reels aus dem Interview mit Anna“, „Recap vom Retreat, 45 Sekunden, mit Musik“). Ergebnis: fertige Dateien im richtigen Format plus ein kurzer Schnittbericht, was woher kommt.

Werkzeuge: ffmpeg und ffprobe, Whisper (Transkript), die Skripte aus `skills/video-editing/scripts/`, die Vorlagen aus `skills/marken-animation/`. Marke aus `brand/brand.json`.

## 0. Bevor du schneidest
- `brand/brand.json` lesen: Farben, Untertitel-Stil, Tonalität, Formate.
- Fragen, wenn unklar: Zielkanal (Reels/TikTok 9:16, LinkedIn 1:1 oder 16:9, YouTube 16:9), Länge, mit oder ohne Untertitel, mit oder ohne Musik. Eine Rückfrage, nicht fünf.
- Personen im Bild: Nur weiterverarbeiten, wenn die Einwilligung vorliegt (steht in `brand.json` unter `freigabe`). Im Zweifel fragen und im Bericht vermerken.

## 1. Sichten
```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate,codec_name -of default=nw=1 rohmaterial.mp4
# Kontaktbogen: alle 10 Sekunden ein Bild, 6 Spalten
ffmpeg -v error -y -i rohmaterial.mp4 -vf "fps=1/10,scale=320:-1,tile=6x8" sichtung.jpg
# Szenenwechsel finden (Schwelle 0.3)
ffmpeg -v error -i rohmaterial.mp4 -vf "select='gt(scene,0.3)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | head -50
```
Kontaktbogen ansehen. Bei Interviews zusätzlich transkribieren:
```bash
bash skills/video-editing/scripts/transcribe.sh rohmaterial.mp4 --model small --language de
```
Das SRT ist dein Suchindex: Zitate, starke Sätze, Lacher, Pausen.

## 2. Momente auswählen
- Für Referenzen (Testimonials): den Satz suchen, der ein konkretes Vorher/Nachher nennt. Kein „es war toll“, sondern „ich schlafe wieder durch“. Ein Clip, eine Aussage.
- Für Retreat-Recaps: Rhythmus aus weit (Ort, Gruppe), nah (Hände, Gesichter mit Einwilligung, Details) und Stimmung (Licht, Natur). 2–4 Sekunden pro Einstellung, keine Einstellung zweimal.
- Für Location-Videos: ein Weg durch den Ort (Ankommen, Räume, Außen, Abend). Langsam, ruhige Schnitte, 4–6 Sekunden pro Einstellung.
- Liste schreiben: `Quelle | von | bis | warum`. Die kommt am Ende in den Schnittbericht.

## 3. Schneiden
```bash
# Einzelner Ausschnitt, bildgenau (neu kodiert)
bash skills/video-editing/scripts/trim.sh rohmaterial.mp4 --start 00:04:12 --end 00:04:31 --output teile/01.mp4
# Interview: Pausen und Füllwörter raus
bash skills/video-editing/scripts/jumpcut.sh teile/01.mp4 --threshold -32 --duration 0.4 --padding 0.12
# Teile aneinander (gleiche Auflösung und Framerate vorausgesetzt)
printf "file '01.mp4'\nfile '02.mp4'\nfile '03.mp4'\n" > teile/liste.txt
ffmpeg -y -f concat -safe 0 -i teile/liste.txt -c copy roh_schnitt.mp4
```
Unterschiedliche Quellen (Handy + Kamera) erst auf ein Format bringen (Schritt 4), dann zusammensetzen.

## 4. Format
Hochkant 9:16 aus 16:9, Mitte beschnitten:
```bash
ffmpeg -y -i roh_schnitt.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920:flags=lanczos" -r 30 -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 160k hoch.mp4
```
Wenn die Person nicht in der Mitte steht: `crop=ih*9/16:ih:x=<Pixel von links>:0`. Bei bewegtem Motiv lieber unscharfer Hintergrund statt Beschnitt:
```bash
ffmpeg -y -i roh_schnitt.mp4 -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:10[bg];[0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" -c:v libx264 -crf 20 -c:a aac hoch_blur.mp4
```
Quadrat: `crop=ih:ih,scale=1080:1080`. Breit bleibt, nur auf 1920×1080 skalieren.

## 5. Untertitel in der Marke
```bash
bash skills/video-editing/scripts/transcribe.sh hoch.mp4 --model small --language de   # falls noch kein SRT
export CAPTION_FORCE_STYLE="$(python3 -c "import json;print(json.load(open('brand/brand.json'))['untertitel']['force_style'])")"
bash skills/video-editing/scripts/caption.sh hoch.mp4 hoch.srt --style custom --output hoch_ut.mp4
```
SRT vorher lesen und Namen, Orte, Fachwörter korrigieren. Bei 9:16 die Untertitel nicht in die unteren 20 % legen (dort liegt die App-Oberfläche): `MarginV` in `brand.json` auf etwa 300 stellen oder `Alignment=5` (Mitte) nutzen.

## 6. Intro, Outro, Zitat-Karte
Mit dem Skill `marken-animation` bauen und rendern, dann vor- und nachschalten:
```bash
# alle Teile müssen gleiche Auflösung, Framerate und Tonspur haben; Karten ohne Ton bekommen Stille
ffmpeg -y -i renders/intro.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -shortest -c:v copy -c:a aac intro_a.mp4
printf "file 'intro_a.mp4'\nfile 'hoch_ut.mp4'\nfile 'outro_a.mp4'\n" > liste.txt
ffmpeg -y -f concat -safe 0 -i liste.txt -c copy fertig_roh.mp4
```
Bei Framerate-Unterschieden nicht `-c copy`, sondern neu kodieren (`-c:v libx264 -crf 20 -r 30 -c:a aac`).

## 7. Musik und Ton
- Nur Musik mit Lizenz (eigene Lizenz, Plattform-Bibliothek oder frei lizenziert). Quelle im Bericht nennen.
- Stimme vorn, Musik hinten: Musik auf etwa −22 dB unter der Stimme, Ausblenden am Ende.
  ```bash
  ffmpeg -y -i fertig_roh.mp4 -i musik.mp3 -filter_complex "[1:a]volume=0.12,afade=t=out:st=<Ende-3>:d=3[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k fertig_musik.mp4
  ```
- Lautheit am Ende normieren: `-af loudnorm=I=-14:TP=-1:LRA=11`.

## 8. Export
| Kanal | Format | Einstellungen |
|---|---|---|
| Instagram Reels, TikTok | 1080×1920, 30 fps | H.264, CRF 20, AAC 160k, max. 90 s |
| Instagram Feed | 1080×1080 oder 1080×1350 | wie oben |
| LinkedIn | 1080×1080 oder 1920×1080 | wie oben, Untertitel Pflicht (läuft stumm) |
| YouTube, Website | 1920×1080, 25 oder 30 fps | H.264, CRF 18–20 |

```bash
ffmpeg -y -i fertig_musik.mp4 -af loudnorm=I=-14:TP=-1:LRA=11 -c:v libx264 -crf 20 -preset slow -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 160k final/anna_reel_01.mp4
ffmpeg -y -ss 1 -i final/anna_reel_01.mp4 -frames:v 1 -q:v 3 final/anna_reel_01.jpg
```
Dateiname: `<thema>_<kanal>_<nr>.mp4`.

## 9. Prüfen und berichten
- Einmal komplett ansehen. Anfang und Ende ohne schwarze Frames, Untertitel lesbar, Ton ohne Knackser, Musik nicht lauter als die Stimme.
- 3 Standbilder (Anfang, Mitte, Ende) ansehen.
- Schnittbericht als kurze Liste: Quelle und Zeitbereich je Teil, Musikquelle, Einwilligungen, offene Punkte. Keine Veröffentlichung durch dich: Freigabe macht ein Mensch.

## Was du nicht tust
- Keine Gesichter von Teilnehmenden ohne Freigabe in Clips lassen. Wenn unsicher: Einstellung ersetzen oder fragen.
- Keine Zitate kürzen, bis sich der Sinn ändert. Auslassungen nur zwischen vollständigen Sätzen.
- Keine KI-Bilder als echte Aufnahmen ausgeben (siehe Skill `bilder-higgsfield`).
