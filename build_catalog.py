#!/usr/bin/env python3
"""Build catalog.json from items/*/meta.json and assemble the Pages site in _site/."""
import json
import shutil
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / (sys.argv[1] if len(sys.argv) > 1 else "_site")

items = []
for meta in sorted((root / "items").glob("*/meta.json")):
    items.append(json.loads(meta.read_text(encoding="utf-8")))
items.sort(key=lambda m: (m.get("date", ""), m.get("title", "")), reverse=True)

if out.exists():
    shutil.rmtree(out)
out.mkdir()
(out / "catalog.json").write_text(json.dumps({"items": items}, indent=2) + "\n", encoding="utf-8")
for name in ("index.html", ".nojekyll"):
    if (root / name).exists():
        shutil.copy2(root / name, out / name)
if (root / "items").exists():
    shutil.copytree(root / "items", out / "items")
print(f"catalog: {len(items)} item(s) -> {out}")
