import os
import json

# تنظیمات مسیرها
THEMES_DIR = 'themes'
OUTPUT_FILE = 'manifest.json'

# فرمت‌های مجاز فایل‌های DWIN (می‌تونی کم و زیاد کنی)
VALID_EXTENSIONS = {'.icl', '.jpg', '.bmp', '.fnt', '.bin', '.zk', '.cz', '.txt'}

def get_files_recursively(folder_path):
    file_list = []
    total_size = 0
    
    # پیمایش تمام زیرپوشه‌ها و فایل‌ها
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # بررسی فرمت فایل (اختیاری: اگر همه فایل‌ها رو میخوای شرط رو بردار)
            ext = os.path.splitext(file)[1].lower()
            if ext in VALID_EXTENSIONS or file == 'preview.png':
                full_path = os.path.join(root, file)
                # مسیر نسبی برای ذخیره در جیسون (سازگار با لینوکس و ویندوز)
                relative_path = full_path.replace('\\', '/')
                
                size = os.path.getsize(full_path)
                total_size += size
                
                file_info = {
                    'name': file,
                    'path': relative_path,  # مسیر کامل نسبی برای دانلود
                    'sizeKb': int(size / 1024) if size > 0 else 1
                }
                file_list.append(file_info)
                
    return file_list, total_size

def build_manifest():
    themes = []
    
    if not os.path.exists(THEMES_DIR):
        print(f"Directory {THEMES_DIR} not found.")
        return

    # پیمایش پوشه‌های اصلی داخل themes
    for item in os.listdir(THEMES_DIR):
        item_path = os.path.join(THEMES_DIR, item)
        
        if os.path.isdir(item_path):
            print(f"Processing theme: {item}")
            
            # استخراج فایل‌ها و حجم کل
            files, total_size_bytes = get_files_recursively(item_path)
            
            # پیدا کردن آدرس پیش‌نمایش (اگر فایل preview.png داشته باشه)
            preview_path = None
            for f in files:
                if f['name'].lower() == 'preview.png':
                    preview_path = f['path']
                    break
            
            theme_obj = {
                "name": item,
                "totalSizeKb": int(total_size_bytes / 1024),
                "preview": preview_path, # کلید مورد انتظار فلاتر
                "files": files           # کلید حیاتی که قبلاً نبود
            }
            
            themes.append(theme_obj)

    # ذخیره جیسون نهایی
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(themes, f, indent=2, ensure_ascii=False)
    
    print(f"Manifest generated with {len(themes)} themes.")

if __name__ == '__main__':
    build_manifest()
