import json
import os
from datetime import datetime

ROOT = "themes"
OUT_FILE = "manifest.json"
VALID_EXTS = (".icl", ".bin")

themes = []

for theme_name in sorted(os.listdir(ROOT)):
    theme_dir = os.path.join(ROOT, theme_name)
    if not os.path.isdir(theme_dir):
        continue

    files_dir = os.path.join(theme_dir, "Files")
    if not os.path.isdir(files_dir):
        continue

    files = []
    total_kb = 0

    for fname in sorted(os.listdir(files_dir)):
        if not fname.lower().endswith(VALID_EXTS):
            continue

        fpath = os.path.join(files_dir, fname)
        size_kb = os.path.getsize(fpath) // 1024
        total_kb += size_kb

        files.append({
            "name": fname,
            "path": f"{ROOT}/{theme_name}/Files/{fname}",
            "sizeKb": size_kb
        })

    if not files:
        continue

    preview = f"{ROOT}/{theme_name}/preview.png"
    if not os.path.exists(preview):
        preview = None

    themes.append({
        "name": theme_name,
        "preview": preview,
        "files": files,
        "totalSizeKb": total_kb
    })

manifest = {
    "version": datetime.utcnow().isoformat() + "Z",
    "themesRoot": ROOT,
    "themes": themes
}

with open(OUT_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"✔ manifest.json generated ({len(themes)} themes)")
