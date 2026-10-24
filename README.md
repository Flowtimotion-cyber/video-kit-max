# Video-Kit — Schnitt, Social-Clips, Bilder und kleine Animationen mit Claude Code

Ein Werkzeugkasten für Leute, die viel echtes Material haben (Retreats, Referenz-Interviews, Location-Aufnahmen) und daraus regelmäßig Clips, Posts und Bilder in der eigenen Marke brauchen. Ohne KI-Avatar, ohne Schnittprogramm: Du sagst Claude Code, was du willst, die Skills sagen Claude, wie.

## Was drin ist

| Ordner | Skill | Wofür |
|---|---|---|
| `skills/social-clip/` | **Social-Clip** | Aus Rohmaterial fertige Clips: sichten, beste Momente, kürzen, Hochkant/Quadrat/Breit, Untertitel in Markenfarben, Intro/Outro, Export je Kanal |
| `skills/video-editing/` | **Video Editing** (MIT, Ian Perez, hier um den Stil `custom` erweitert) | Die Schnitt-Werkzeuge: Trimmen, Stille raus, Untertitel, Tempo, Text-Overlay |
| `skills/marken-animation/` | **Marken-Animation** | Intro-Karte, Bauchbinde, Zitat-Karte, Logo-Outro als kurze Animationen aus deiner Markendatei |
| `skills/bilder-higgsfield/` | **Bilder mit Higgsfield** | Stimmungsbilder, Location-Varianten, Hintergründe, kurze Foto-Animationen, mit Regeln für Kennzeichnung und echte Menschen |
| `brand/brand.json` | Deine Marke | Farben, Schriften, Logo, Untertitel-Stil, Tonalität, Formate, Freigabe-Regeln. Einmal ausfüllen, alle Skills lesen sie |
| `tools/bauen.py` | Vorlagen-Bauer | Macht aus einer Animations-Vorlage plus `brand.json` eine renderbare Komposition |

## Einrichten (einmal, etwa 20 Minuten)

1. **Claude Code** installieren: https://docs.anthropic.com/claude-code
2. Repo klonen, Skills bekannt machen:
   ```bash
   git clone https://github.com/Flowtimotion-cyber/video-kit-max.git
   cd video-kit-max
   mkdir -p ~/.claude/skills
   cp -r skills/* ~/.claude/skills/
   ```
   Windows: nach `C:\Users\<du>\.claude\skills\` kopieren. Die Skripte sind Bash, unter Windows laufen sie in Git Bash oder WSL.
3. **Werkzeuge**:
   - ffmpeg (macOS `brew install ffmpeg`, Windows `winget install Gyan.FFmpeg`, Linux `apt install ffmpeg`)
   - Python 3.10+, dann `pip install openai-whisper` (Untertitel) 
   - Node 18+, dann im Repo-Ordner `npm install hyperframes@0.8.183` (Animationen rendern)
   - Higgsfield nur, wenn du Bilder willst: `curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh`, dann `higgsfield auth login`
4. **Marke eintragen**: `brand/brand.json` öffnen, Name, Farben, Schriften, Website ausfüllen, Logo-Dateien nach `brand/logo/` legen. Der Untertitel-Stil braucht die Farben im ASS-Format, die Umrechnung steht als Hinweis in der Datei. Claude kann das für dich machen: „Trag meine Marke in brand.json ein: Primärfarbe #…, Logo liegt in …“.

## So nutzt du es

Claude Code im Repo-Ordner starten und sagen, was du willst:

- „Schneide aus `interview_anna.mp4` drei Reels mit je einer starken Aussage, Untertitel in unserer Marke, Zitat-Karte dazwischen.“
- „Mach aus den Retreat-Aufnahmen in `rohmaterial/` ein 45-Sekunden-Recap für Instagram, ruhig, mit Intro und Outro.“
- „Location-Clip für die Website aus `finca.mp4`, 16:9, ohne Untertitel, mit Musik aus `musik/`.“
- „Bauchbinde für Anna M., Teilnehmerin 2025, über den Clip ab Sekunde 2.“
- „Erzeuge drei Stimmungsbilder für die Ankündigung im Mai, Morgenlicht, keine Personen.“

Claude liefert die Dateien in `final/` plus einen kurzen Schnittbericht: welche Quelle, welcher Zeitbereich, Musikquelle, offene Freigaben.

## Grundregeln, die in den Skills stecken

- **Freigabe bleibt beim Menschen.** Claude schneidet und exportiert, veröffentlicht aber nichts.
- **Personen im Bild nur mit Einwilligung.** Teilnehmende und Referenzgeber müssen zugestimmt haben. Fehlt das, fliegt die Einstellung raus oder Claude fragt.
- **Keine KI-Menschen als echte Referenzen.** KI-Bilder werden gekennzeichnet, Location-Bilder zeigen den echten Ort.
- **Musik nur mit Lizenz.** Quelle steht im Bericht.
- **Marke nur aus `brand.json`.** Farben, Logo und Schrift werden nirgends sonst eingetragen.

## Stolperfallen

- Whisper lädt beim ersten Lauf ein Modell (ein paar hundert MB). Modell `small` ist ein guter Kompromiss für Deutsch.
- HyperFrames braucht ein Chromium. Findet es keins: `npx playwright install chromium` und `HYPERFRAMES_BROWSER_PATH` setzen.
- Die Animations-Vorlagen laden GSAP aus dem Netz. Offline: `gsap.min.js` neben die `index.html` legen.
- Handy-Videos haben oft eine Dreh-Markierung. Wenn ein Clip quer erscheint: `ffmpeg -i in.mp4 -vf "transpose=1" …` oder vorher `-noautorotate` prüfen.
- Bei 9:16 die Untertitel nicht ganz unten platzieren, dort liegt die App-Oberfläche. `MarginV` in `brand.json` hochsetzen.

## Mehr Animation?

Die vier Vorlagen hier sind die schnellen Marken-Bausteine. Für Montagen, Slideshows oder Effekt-Untertitel die offiziellen HyperFrames-Skills installieren: `npx skills add heygen-com/hyperframes --all`. Für Produktfotos, Werbespots oder ein komplettes Brandkit die offiziellen Higgsfield-Skills aus der CLI.

## Herkunft

Zusammengestellt von Timo Merz (Hermetikmarketing) mit Claude. Skill `video-editing` unter MIT-Lizenz (`skills/video-editing/LICENSE.txt`). Die übrigen Teile: Nutzung in Absprache mit Timo.
