# -*- coding: utf-8 -*-
"""
Comprehensive fix for Soundora encoding issues
This handles Windows-1251 mojibake that appears in Russian translations
"""

import re
import os

file_path = r'c:\Users\emroa\Downloads\SND\app\src\main\assets\index.html'

print("=" * 60)
print("Soundora Encoding Fix Script")
print("=" * 60)

# Read the file
print("\n[1/4] Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    original_content = f.read()

print(f"      File size: {len(original_content):,} characters")

# Create comprehensive mapping
# This is based on analyzing the mojibake patterns
# Each garbled sequence maps to its correct Cyrillic equivalent

print("\n[2/4] Creating encoding fix mappings...")

# Build character-level mappings for common Cyrillic letters that got mangled
# These mappings were derived by analyzing the actual hex values in the file

char_fixes = {
    # Common two-char sequences (Cyrillic letter -> mojibake)
    '\u0420\u2019': 'В',  # В (capital V)
    '\u0421\u2039': 'ы',  # ы (lowercase y)
    '\u0420\u0455': 'о',  # о (lowercase o) 
    '\u0421\u201e': 'ф',  # ф (lowercase f)
    '\u0420\u00bb': 'л',  # л (lowercase l)
    '\u0420\u00b0': 'а',  # а (lowercase a)
    '\u0420\u2116': 'й',  # й (lowercase i with breve)
    '\u0420\u0405': 'н',  # н (lowercase n)
    '\u0420\u2014': 'З',  # З (capital Z)
    '\u0421\u0402': 'р',  # р (lowercase r)
    '\u0421\u0453': 'у',  # у (lowercase u)
    '\u0420\u0456': 'г',  # г (lowercase g)
    '\u0420\u0454': 'к',  # к (lowercase k)
    '\u0420\u0451': 'и',  # и (lowercase i)
    '\u0420\u00b5': 'е',  # е (lowercase e)
    '\u0421\u201a': 'т',  # т (lowercase t)
    '\u0420\u00a4': 'Ф',  # Ф (capital F)
    '\u0420\u0458': 'м',  # м (lowercase m)
    '\u0420\u0491': 'д',  # д (lowercase d)
    '\u0420\u00b1': 'б',  # б (lowercase b)
    '\u0420\u00b2': 'в',  # в (lowercase v)
    '\u0421\u2030': 'щ',  # щ (lowercase shch)
    '\u0420\u045c': 'Н',  # Н (capital N)
    '\u0421\u2021': 'ч',  # ч (lowercase ch)
    '\u0421\u0403': 'с',  # с (lowercase s)
    '\u0420\u00b6': 'ж',  # ж (lowercase zh)
    '\u0421\u2020': 'х',  # х (lowercase kh)
    '\u0420\u045b': 'О',  # О (capital O)
    '\u0420\u00a0': 'Р',  # Р (capital R)
    '\u0421\u201a': 'т',  # т (lowercase t)
    '\u0421\u040a': 'ь',  # ь (soft sign)
    '\u0420\u040e': 'С',  # С (capital S)
    '\u0421\u040b': 'ю',  # ю (lowercase yu)
    '\u0420\u0452': 'А',  # А (capital A)
    '\u0421\u2018': 'ё',  # ё (lowercase yo)
    '\u0420\u0406': 'в',  # в (lowercase v) - alternate
    '\u0421\u040f': 'я',  # я (lowercase ya)
    '\u0420\u201d': 'Д',  # Д (capital D)
    '\u0420\u045e': 'Т',  # Т (capital T)
}

# Apply character-level fixes
content = original_content
for garbled, correct in char_fixes.items():
    content = content.replace(garbled, correct)

print(f"      Created {len(char_fixes)} character mappings")

# Count how many changes were made
changes_made = sum(1 for i, (a, b) in enumerate(zip(original_content, content)) if a != b)
print(f"      Applied {changes_made:,} character fixes")

print("\n[3/4] Creating backup...")
backup_path = file_path + '.backup_encoding'
if not os.path.exists(backup_path):
    with open(backup_path, 'w', encoding='utf-8') as bf:
        bf.write(original_content)
    print(f"      Backup saved: {backup_path}")
else:
    print(f"      Backup already exists: {backup_path}")

print("\n[4/4] Writing fixed content...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"      Fixed file saved")

print("\n" + "=" * 60)
print("✓ ENCODING FIX COMPLETE!")
print("=" * 60)
print(f"Total changes: {changes_made:,} characters fixed")
print(f"Backup: {backup_path}")
print("=" * 60)
