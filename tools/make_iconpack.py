#!/usr/bin/env python3
"""out/*.png (glass icons) -> Android icon pack resources + appfilter.xml"""
import csv, os, shutil
from PIL import Image
OUT = "out"; RES = "app/src/main/res"; ASSETS = "app/src/main/assets"
D = os.path.join(RES, "drawable-nodpi")
shutil.rmtree(D, ignore_errors=True)
os.makedirs(D); os.makedirs(os.path.join(RES, "xml"), exist_ok=True); os.makedirs(ASSETS, exist_ok=True)
items, n = [], 0
for r in csv.DictReader(open("mapping.csv", encoding="utf-8")):
    src = os.path.join(OUT, r["name"] + ".png")
    if not os.path.exists(src): continue
    Image.open(src).convert("RGBA").resize((512, 512), Image.LANCZOS).save(os.path.join(D, r["name"] + ".png"), optimize=True)
    n += 1
    if r["package"] and r["component"]:
        items.append(f'    <item component="ComponentInfo{{{r["package"]}/{r["component"]}}}" drawable="{r["name"]}" />')
if os.path.exists(os.path.join(D, "gallery.png")):
    shutil.copy(os.path.join(D, "gallery.png"), os.path.join(D, "ic_launcher.png"))
xml = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    ' + "\n".join(items) + "\n</resources>\n"
for p in (os.path.join(RES, "xml", "appfilter.xml"), os.path.join(ASSETS, "appfilter.xml")):
    open(p, "w", encoding="utf-8").write(xml)
print(f"{n} icons, {len(items)} mapped in appfilter.xml")
