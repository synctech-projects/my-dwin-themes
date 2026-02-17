import os
import json

# تنظیمات
THEMES_DIR = 'themes'
OUTPUT_FILE = 'manifest.json'
# دامنه پایه برای دسترسی فایل‌ها از طریق jsDelivr (یا گیت‌هاب خام)
# نکته: اگر در Flutter آدرس پایه را هندل می‌کنی، اینجا مسیر نسبی کافی است.
# من اینجا مسیر نسبی (Relative Path) می‌سازم تا در Flutter انعطاف‌پذیر باشی.

def generate_manifest():
    themes = []
    
    # بررسی وجود پوشه themes
    if not os.path.exists(THEMES_DIR):
        print(f"Error: Directory '{THEMES_DIR}' not found.")
        return

    # اسکن پوشه‌ها
    # ساختار مورد انتظار: themes/theme_name/preview.jpg
    entries = sorted(os.listdir(THEMES_DIR))
    
    for entry in entries:
        theme_path = os.path.join(THEMES_DIR, entry)
        
        # فقط پوشه‌ها را پردازش کن
        if os.path.isdir(theme_path):
            theme_id = entry
            
            # پیدا کردن فایل پریویو (jpg یا png)
            preview_image = None
            for ext in ['.jpg', '.jpeg', '.png']:
                if os.path.exists(os.path.join(theme_path, f"preview{ext}")):
                    preview_image = f"{THEMES_DIR}/{theme_id}/preview{ext}"
                    break
            
            # اگر عکس نبود، یک عکس پیش‌فرض یا null بگذار (اینجا رد می‌کنیم)
            if not preview_image:
                print(f"Warning: No preview image found for '{theme_id}'. Skipping.")
                continue

            # ساخت آبجکت تم
            theme_data = {
                "id": theme_id,
                "name": theme_id.replace('_', ' ').title(), # تبدیل theme_01 به Theme 01
                "previewUrl": preview_image,
                "downloadUrl": f"{THEMES_DIR}/{theme_id}", # آدرس پوشه برای دانلود فایل‌ها
                "size": "Unknown" # می‌توان بعداً حجم فایل‌های داخل پوشه را محاسبه کرد
            }
            
            themes.append(theme_data)

    # ذخیره فایل manifest.json
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(themes, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Success! Generated manifest.json with {len(themes)} themes.")

if __name__ == "__main__":
    generate_manifest()
