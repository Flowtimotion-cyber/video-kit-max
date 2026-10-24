#!/usr/bin/env python3
"""Baut aus einer Vorlage (skills/marken-animation/templates/*.html) eine HyperFrames-Komposition.

Liest brand/brand.json, ersetzt {{PLATZHALTER}} und legt out/<name>/index.html plus assets/ an.

Beispiele:
  python3 tools/bauen.py intro --out out/intro --format breit --set TITEL="Retreat Mallorca 2026" --set UNTERTITEL="Fünf Tage, die bleiben"
  python3 tools/bauen.py bauchbinde --out out/bb-anna --format reels --set NAME="Anna M." --set ROLLE="Teilnehmerin 2025"
  python3 tools/bauen.py zitat --out out/zitat-1 --format quadrat --set ZITAT="Ich bin als andere Frau zurückgekommen." --set AUTOR="Anna M."
  python3 tools/bauen.py outro --out out/outro --format reels

Danach rendern: npx hyperframes render out/intro -o renders/intro.mp4 -f 25
"""
import argparse, json, pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "skills" / "marken-animation" / "templates"
BRAND = json.loads((ROOT / "brand" / "brand.json").read_text(encoding="utf-8"))

DEFAULT_DAUER = {"intro": 5, "bauchbinde": 5, "zitat": 7, "outro": 5}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vorlage", help="intro | bauchbinde | zitat | outro (oder Pfad zu einer eigenen .html)")
    ap.add_argument("--out", required=True, help="Zielordner, z. B. out/intro")
    ap.add_argument("--format", default="breit", help="reels | quadrat | breit (aus brand.json) oder BREITExHOEHE")
    ap.add_argument("--dauer", type=float, help="Sekunden (Standard je Vorlage)")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=WERT", help="Platzhalter füllen, mehrfach möglich")
    a = ap.parse_args()

    src = pathlib.Path(a.vorlage)
    if not src.exists():
        src = TPL / f"{a.vorlage}.html"
    if not src.exists():
        sys.exit(f"Vorlage nicht gefunden: {a.vorlage} (vorhanden: {', '.join(p.stem for p in TPL.glob('*.html'))})")

    if "x" in a.format and a.format.replace("x", "").isdigit():
        w, h = (int(x) for x in a.format.split("x"))
    else:
        f = BRAND["formate"].get(a.format)
        if not f:
            sys.exit(f"Unbekanntes Format: {a.format}")
        w, h = f["breite"], f["hoehe"]

    name = src.stem
    dauer = a.dauer or DEFAULT_DAUER.get(name, 5)
    out = pathlib.Path(a.out)
    (out / "assets").mkdir(parents=True, exist_ok=True)

    # Logo: dunkles Logo auf hellem Hintergrund, helles Logo auf dunklem
    logo_rel = ""
    for key in ("dunkel", "hell"):
        p = ROOT / BRAND["logo"].get(key, "")
        if p.is_file():
            shutil.copy(p, out / "assets" / p.name)
            logo_rel = logo_rel or f"assets/{p.name}"
    if not logo_rel:
        print("Hinweis: kein Logo in brand/logo/ gefunden, Platzhalter bleibt leer.")

    werte = {
        "ID": f"{name}-{w}x{h}",
        "BREITE": str(w), "HOEHE": str(h), "DAUER": f"{dauer:g}",
        "MARKE": BRAND["name"], "CLAIM": BRAND.get("claim", ""), "WEBSITE": BRAND.get("website", ""),
        "FARBE_PRIMAER": BRAND["farben"]["primaer"], "FARBE_SEKUNDAER": BRAND["farben"]["sekundaer"],
        "FARBE_HINTERGRUND": BRAND["farben"]["hintergrund"], "FARBE_TEXT": BRAND["farben"]["text"],
        "FARBE_HELL": BRAND["farben"].get("hell", "#FFFFFF"),
        "SCHRIFT_UEBERSCHRIFT": BRAND["schrift"]["ueberschrift"], "SCHRIFT_FLIESSTEXT": BRAND["schrift"]["fliesstext"],
        "LOGO": logo_rel, "LOGO_ANZEIGE": "block" if logo_rel else "none",
        "HINTERGRUND": "transparent",
        "TITEL": "", "UNTERTITEL": "", "NAME": "", "ROLLE": "", "ZITAT": "", "AUTOR": "",
    }
    for kv in a.set:
        if "=" not in kv:
            sys.exit(f"--set braucht KEY=WERT, bekommen: {kv}")
        k, v = kv.split("=", 1)
        werte[k.strip().upper()] = v

    html = src.read_text(encoding="utf-8")
    fehlend = set()

    def ersetze(m):
        k = m.group(1)
        if k in werte:
            return werte[k]
        fehlend.add(k)
        return ""

    html = re.sub(r"\{\{([A-Z_]+)\}\}", ersetze, html)
    (out / "index.html").write_text(html, encoding="utf-8")
    if fehlend:
        print("Warnung, Platzhalter ohne Wert:", ", ".join(sorted(fehlend)))
    print(f"OK {out / 'index.html'}  {w}x{h}  {dauer:g}s  Komposition-ID {werte['ID']}")
    print(f"Rendern: npx hyperframes render {out} -o renders/{out.name}.mp4 -f 25")


if __name__ == "__main__":
    main()
