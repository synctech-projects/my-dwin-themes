import os
import json

# تنظیمات
THEMES_DIR = 'themes'
OUTPUT_FILE = 'manifest.json'
# لیست فرمت‌هایی که می‌خواهیم لیست شوند (برای جلوگیری از لیست شدن فایل‌های سیستمی)
VALID_EXTENSIONS = ['.icl', '.fnt', '.bin', '.hzqk', '.txt', '.jpg', '.png', '.bmp']

def get_theme_data():
    themes = []
    
    if not os.path.exists(THEMES_DIR):
        print(f"Error: Directory '{THEMES_DIR}' not found.")
        return []

    # لیست کردن پوشه‌های داخل themes
    for theme_name in os.listdir(THEMES_DIR):
        theme_path = os.path.join(THEMES_DIR, theme_name)
        
        if os.path.isdir(theme_path):
            theme_files = []
            total_size_bytes = 0
            preview_path = None
            
            # پیمایش تمام فایل‌های داخل پوشه تم
            for root, _, files in os.walk(theme_path):
                for file in files:
                    # نادیده گرفتن فایل‌های سیستمی و مخفی
                    if file.startswith('.'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    # مسیر نسبی برای URL (تبدیل \ به / برای ویندوز)
                    relative_path = os.path.relpath(file_path, start='.').replace('\\', '/')
                    
                    # اگر عکس پیش‌نمایش باشد
                    if file.lower() == 'preview.png':
                        preview_path = relative_path
                    
                    # اضافه کردن به لیست فایل‌های قابل دانلود
                    # (چک کردن پسوند اختیاری است، اما برای تمیزی خوبه)
                    ext = os.path.splitext(file)[1].lower()
                    if ext in VALID_EXTENSIONS or True: # فعلا همه را قبول میکنیم
                        size = os.path.getsize(file_path)
                        total_size_bytes += size
                        
                        theme_files.append({
                            "name": file,
                            "path": relative_path,
                            "sizeKb": round(size / 1024, 2)
                        })

            # ساخت آبجکت تم
            if theme_files:
                themes.append({
                    "id": theme_name, # استفاده از نام پوشه به عنوان ID
                    "name": theme_name,
                    "preview": preview_path, # مسیر نسبی
                    "totalSizeKb": int(total_size_bytes / 1024),
                    "files": theme_files
                })
                print(f"Processed: {theme_name} | Files: {len(theme_files)} | Size: {int(total_size_bytes/1024)}KB")

    return themes

if __name__ == "__main__":
    data = get_theme_data()
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nSUCCESS: '{OUTPUT_FILE}' generated with {len(data)} themes.")
