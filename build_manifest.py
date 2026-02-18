import os
import json
import hashlib

THEMES_DIR = 'themes'
OUTPUT_FILE = 'manifest.json'

VALID_EXTENSIONS = ['.icl', '.fnt', '.bin', '.hzqk', '.txt', '.jpg', '.png', '.bmp']


def slugify(name: str) -> str:
    return name.strip().lower().replace(' ', '_')


def calculate_hash(data) -> str:
    encoded = json.dumps(data, sort_keys=True, ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def load_existing_manifest():
    if not os.path.exists(OUTPUT_FILE):
        return 0, None

    with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
        try:
            manifest = json.load(f)
            return manifest.get('version', 0), manifest.get('themes')
        except Exception:
            return 0, None


def get_theme_data():
    themes = []

    if not os.path.exists(THEMES_DIR):
        print(f"Error: Directory '{THEMES_DIR}' not found.")
        return []

    for theme_name in sorted(os.listdir(THEMES_DIR)):
        theme_path = os.path.join(THEMES_DIR, theme_name)

        if not os.path.isdir(theme_path):
            continue

        theme_files = []
        total_size_bytes = 0
        preview_path = None

        for root, _, files in os.walk(theme_path):
            for file in files:
                if file.startswith('.'):
                    continue

                ext = os.path.splitext(file)[1].lower()
                if ext not in VALID_EXTENSIONS:
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, start='.').replace('\\', '/')

                if file.lower() == 'preview.png':
                    preview_path = relative_path

                size = os.path.getsize(file_path)
                total_size_bytes += size

                theme_files.append({
                    "name": file,
                    "path": relative_path,
                    "sizeKb": round(size / 1024, 2)
                })

        if theme_files:
            themes.append({
                "id": slugify(theme_name),
                "name": theme_name,
                "preview": preview_path,
                "totalSizeKb": int(total_size_bytes / 1024),
                "files": theme_files
            })

            print(f"Processed: {theme_name} | Files: {len(theme_files)}")

    return themes


if __name__ == "__main__":
    old_version, old_themes = load_existing_manifest()
    new_themes = get_theme_data()

    old_hash = calculate_hash(old_themes) if old_themes else None
    new_hash = calculate_hash(new_themes)

    version = old_version
    if old_hash != new_hash:
        version += 1
        print(f"📦 Manifest changed → version bumped to {version}")
    else:
        print(f"✅ No changes detected → version stays {version}")

    manifest = {
        "version": version,
        "themes": new_themes
    }

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nSUCCESS: '{OUTPUT_FILE}' generated | Themes: {len(new_themes)} | Version: {version}")
