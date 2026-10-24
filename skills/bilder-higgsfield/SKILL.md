---
name: bilder-higgsfield
description: Bilder und kurze Bewegtbilder mit Higgsfield erzeugen, passend zur eigenen Marke — Stimmungsbilder für Retreats, Varianten von Location-Fotos, Hintergründe für Zitat-Karten und Posts, kurze Animationen aus einem Foto (Image-to-Video). Nutzen bei „mach mir ein Bild für …“, „animier das Location-Foto“, „Hintergrund für den Post“.
---

# Bilder und kurze Animationen mit Higgsfield

Higgsfield läuft über die Kommandozeile `higgsfield`. Du brauchst ein eigenes Higgsfield-Konto, die Kosten laufen über dessen Guthaben.

## Einrichten (einmal)
```bash
curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
higgsfield auth login        # interaktiv, macht der Mensch
higgsfield account status
```
Die ausführlichen Higgsfield-Skills (Modelle, Produktfotos, Brandkit) kommen mit der CLI bzw. über `higgsfield skills`. Dieser Skill hier legt nur fest, wie wir sie **für unsere Marke** nutzen.

## Vorher aus `brand/brand.json` holen
- Farben (Primär, Sekundär, Hintergrund) als Wörter in den Prompt übersetzen („warmes Grün, sandfarbener Hintergrund, goldene Akzente“), nicht als Hex.
- `tonalitaet.stimmung` wird zur Bildstimmung („ruhig, warm, nahbar, natürliches Licht“).
- Was die Marke vermeidet („Druck, Superlative“) heißt im Bild: keine gestellten Jubelposen, keine Stockfoto-Optik.

## Standardaufruf
```bash
higgsfield generate create --model gpt_image_2 --aspect_ratio 4:5 --wait \
  --prompt "Morgenlicht in einem Retreat-Raum auf Mallorca, Yogamatten auf Holzboden, offene Fenster zum Garten, warmes Grün und Sandtöne, ruhig, natürlich, kein Text, keine Personen"
```
- Seitenverhältnisse: Posts `4:5` oder `1:1`, Reels-Hintergrund `9:16`, Website `16:9`.
- Mehrere Varianten? `--num_images 3` wenn das Modell es kann, sonst drei Aufrufe mit kleinen Prompt-Änderungen.
- Prompt immer mit „kein Text“ beenden. Text kommt später aus den Marken-Vorlagen, nicht aus dem Bildmodell.

## Vier Einsatzfälle
1. **Stimmungsbild für Retreat-Ankündigung.** Ort, Licht, Jahreszeit, zwei Markenfarben, keine Personen. Ergebnis als Hintergrund für die Zitat-Karte oder den Post.
2. **Location-Foto veredeln.** Echtes Foto als Referenz mitgeben (`--image pfad.jpg`) und nur Licht/Stimmung ändern lassen („gleicher Raum, Abendlicht, Kerzen“). Architektur und Ausstattung bleiben echt. Keine Räume erfinden, die es dort nicht gibt.
3. **Kurze Animation aus einem Foto** (3–6 Sekunden, für Reels-Anfang oder Website):
   ```bash
   higgsfield generate create --model seedance_2 --image location.jpg --duration 5 --wait \
     --prompt "langsame Kamerafahrt nach vorn, Vorhänge bewegen sich leicht im Wind, Licht flackert sanft, sonst alles unverändert"
   ```
   Modellnamen vorher mit `higgsfield model list` prüfen, sie ändern sich.
4. **Hintergrundfläche für Text-Posts.** Abstrakt, ruhig, in Markenfarben, viel freie Fläche in der Mitte („weiche Farbverläufe, Sand und Grün, leichte Papierstruktur, kein Motiv, kein Text“).

## Regeln
- **Keine erfundenen Menschen als Teilnehmende oder Referenzgeber.** Keine KI-Gesichter in Testimonials. Menschen nur, wenn ausdrücklich gewünscht und erkennbar illustrativ.
- **Kennzeichnen.** Wenn `brand.json` → `freigabe.ki_bilder_kennzeichnen` wahr ist: im Schnittbericht und in der Bildunterschrift vermerken („Bild: KI-generiert“). Bei Location-Bildern, die den echten Ort zeigen sollen, lieber das echte Foto nehmen.
- **Guthaben nennen**, bevor du mehr als fünf Bilder oder ein Video erzeugst (`higgsfield account status`).
- Ergebnisse herunterladen nach `bilder/JJJJ-MM-TT_<thema>/`, Prompt daneben in `prompts.md` speichern, damit Varianten reproduzierbar sind.
- Das Bild danach kurz ansehen: Hände, Schrift, Spiegelungen, doppelte Gegenstände. Ein verunglücktes Bild lieber neu erzeugen als retuschieren.

## Zusammenspiel
- Bild → `marken-animation` (Zitat-Karte mit Bildhintergrund: eigene Vorlage anlegen, `background-image` auf das Bild)
- Animation → `social-clip` als Eröffnungseinstellung
- Für komplette Werbevideos und Produktbilder die offiziellen Higgsfield-Skills (Marketing Studio, Brandkit) nutzen, nicht diesen.
