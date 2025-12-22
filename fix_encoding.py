# -*- coding: utf-8 -*-
import re

# Read the file
with open(r'c:\Users\emroa\Downloads\SND\app\src\main\assets\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix all encoding issues
fixes = [
    ('вЂ"', '—'),  # em dash
    ('вЂ'', '-'),  # hyphen
    ('вЂ', "'"),   # apostrophe  
    ('boвЂlimida', "bo'limida"),
    ('YoвЂq', "Yo'q"),
    ('boвЂyicha', "bo'yicha"),
]

for old, new in fixes:
    count = content.count(old)
    if count > 0:
        print(f"Replacing '{old}' → '{new}' ({count} occurrences)")
        content = content.replace(old, new)

# Write back
with open(r'c:\Users\emroa\Downloads\SND\app\src\main\assets\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nДone! All encoding errors fixed.")
