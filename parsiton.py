# -*- coding: utf-8 -*-

import sys
import re
from bidi.algorithm import get_display
from arabic_reshaper import reshape

def reshaper(text):
    if isinstance(text, str):  
        return get_display(reshape(text))
    return text  

keyword_map = {
    "تعریف": "def",
    "اگر": "if",
    "وگرنه": "else",
    "در غیر این صورت": "elif",
    "بازگردان": "return",
    "برای": "for",
    "در": "in",
    "چاپ": "print",
    "درحالی‌که": "while",
    "درست": "True",
    "نادرست": "False",
    "هیچ": "None",
    "و": "and",
    "یا": "or", 
    "نه": "not",
}

def parsi_to_python(code: str) -> str:
    # جایگزینی کلمات کلیدی فقط برای کلمات کامل
    for fa, en in keyword_map.items():
        pattern = r'\b' + re.escape(fa) + r'\b'
        code = re.sub(pattern, en, code)
    return code


original_print = print
def custom_print(*args, **kwargs):
    reshaped_args = [reshaper(arg) for arg in args]
    original_print(*reshaped_args, **kwargs)

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print(("لطفاً مسیر فایل .parsi را وارد کنید. مثال: parsi_python.py code.parsi"))
        sys.exit(1)
    
    parsi_file = sys.argv[1]
    if not parsi_file.endswith(".parsi"):
        print(("فایل ورودی باید پسوند .parsi داشته باشد!"))
        sys.exit(1)
    
    try:
        with open(parsi_file, "r", encoding="utf-8") as f:
            fa_code = f.read()
    except FileNotFoundError:
        print(reshaper(f"فایل {parsi_file} پیدا نشد!"))
        sys.exit(1)
    
    py_code = parsi_to_python(fa_code)
    
   
    import builtins
    builtins.print = custom_print
    
    print("✅ کد تبدیل شد! اجرای برنامه...")
    try:
        exec(py_code)
    except Exception as e:
        print(reshaper(f"خطا در اجرای کد: {str(e)}"))
    finally:
        
        builtins.print = original_print