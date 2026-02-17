import os
import json

# تنظیمات
THEMES_DIR = 'themes'
OUTPUT_FILE = 'manifest.json'
GITHUB_USER = 'synctech-projects'
GITHUB_REPO = 'my-dwin-themes'
BRANCH = 'main'

def get_file_size_kb(path):
    return int(os.path.getsize(path) / 1024)

def generate_manifest():
    manifest = {
        "version": "1.0.0",
        "themesRoot": THEMES_DIR,
        "themes": []
    }

    # بررسی پوشه themes
    if not os.path.exists(THEMES_DIR):
        print(f"Directory {THEMES_DIR} not found.")
        return

    # پیمایش پوشه های تم
    for theme_name in os.listdir(THEMES_DIR):
        theme_path = os.path.join(THEMES_DIR, theme_name)
        
        if not os.path.isdir(theme_path):
            continue

        # پیدا کردن فایل پریویو
        preview_path = None
        possible_previews = ['preview.png', 'preview.jpg', 'icon.png']
        for p in possible_previews:
            if os.path.exists(os.path.join(theme_path, p)):
                # مسیر باید با / باشد برای وب
                preview_path = f"{THEMES_DIR}/{theme_name}/{p}"
                break
        
        # لیست کردن فایل‌های داخل تم (مثلاً .icl, .tft, etc)
        theme_files = []
        total_size_kb = 0
        
        # فرض میکنیم فایل‌ها داخل پوشه Files هستند یا مستقیماً در ریشه تم
        # اینجا فرض میکنیم فایل های اصلی (مثل 32.icl) در یک زیرپوشه Files هستند
        # اگر ساختارت فرق دارد این قسمت را تغییر بده
        files_dir = os.path.join(theme_path, 'Files')
        search_dir = files_dir if os.path.exists(files_dir) else theme_path

        for root, dirs, files in os.walk(search_dir):
            for file in files:
                # نادیده گرفتن فایل‌های سیستمی و پریویو
                if file.startswith('.') or file in possible_previews:
                    continue
                
                # فقط فایل‌های DWIN را برداریم؟ یا همه؟ فعلاً همه.
                file_abs_path = os.path.join(root, file)
                size = get_file_size_kb(file_abs_path)
                total_size_kb += size
                
                # ساخت مسیر نسبی وب
                rel_path = os.path.relpath(file_abs_path, os.getcwd()).replace("\\", "/")
                
                theme_files.append({
                    "name": file,
                    "path": rel_path,
                    "sizeKb": size
                })

        if theme_files:
            manifest["themes"].append({
                "name": theme_name,
                "preview": preview_path,
                "files": theme_files,
                "totalSizeKb": total_size_kb
            })

    # ذخیره فایل JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Manifest generated with {len(manifest['themes'])} themes.")

if __name__ == "__main__":
    generate_manifest()
