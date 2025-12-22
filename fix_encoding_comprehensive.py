# coding: utf-8
"""
Comprehensive encoding fix for Soundora index.html
Fixes Windows-1251/UTF-8 mojibake issues in Russian text
"""

import re
import os

# Path to the file
file_path = r'c:\Users\emroa\Downloads\SND\app\src\main\assets\index.html'

print("Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"File size: {len(content)} characters")

# Define replacement mappings for garbled Russian text
# These are Windows-1251 bytes interpreted as UTF-8 (mojibake)
replacements = {
    # Downloads section
    'Р—Р°РіСЂСѓР·РєРё': 'Загрузки',
    'РќРµС‚ Р·Р°РіСЂСѓР¶РµРЅРЅС‹С… С„РёР»СЊРјРѕРІ': 'Нет загруженных фильмов',
    'Р¤РёР»СЊРј РґРѕР±Р°РІР»РµРЅ РІ Р·Р°РіСЂСѓР·РєРё': 'Фильм добавлен в загрузки',
    'РќР°С‡Р°Р»Р°СЃСЊ Р·Р°РіСЂСѓР·РєР°. Р¤РёР»СЊРј РїРѕСЏРІРёС‚СЃСЏ РІ СЂР°Р·РґРµР»Рµ Р·Р°РіСЂСѓР·РѕРє': 'Началась загрузка. Фильм появится в разделе загрузок',
    'Р—Р°РіСЂСѓР¶РµРЅРѕ': 'Загружено',
    'РЎРєР°С‡Р°С‚СЊ': 'Скачать',
    
    # Online/Offline status
    'Р'С‹ РѕС„Р»Р°Р№РЅ': 'Вы офлайн',
    'Р'С‹ РѕРЅР»Р°Р№РЅ': 'Вы онлайн',
    
    # Resume playback
    'Р'С‹ РѕСЃС‚Р°РЅРѕРІРёР»РёСЃСЊ СЂР°РЅРµРµ. РџСЂРѕРґРѕР»Р¶РёС‚СЊ РїСЂРѕСЃРјРѕС‚СЂ СЃ СЌС‚РѕРіРѕ РјРµСЃС‚Р°?': 'Вы остановились ранее. Продолжить просмотр с этого места?',
    'РџРѕРєР°Р·С‹РІР°С‚СЊ Р·Р°РїСЂРѕСЃ РїСЂРѕРґРѕР»Р¶РµРЅРёСЏ': 'Показывать запрос продолжения',
    'РџСЂРё РІРѕР·РІСЂР°С‚Рµ Рє С„РёР»СЊРјСѓ СЃРїСЂР°С€РёРІР°С‚СЊ, С…РѕС‚РёС‚Рµ Р»Рё РїСЂРѕРґРѕР»Р¶РёС‚СЊ СЃ СЃРѕС…СЂР°РЅС'РЅРЅРѕРіРѕ РјРµСЃС‚Р°': 'При возврате к фильму спрашивать, хотите ли продолжить с сохранённого места',
    'Р"Р°': 'Да',
    'РќРµС‚': 'Нет',
    
    # Subscription info
    'Р"РµР№СЃС‚РІРёС‚РµР»СЊРЅРѕ РґРѕ': 'Действительно до',
    'РґРЅРµР№ РѕСЃС‚Р°Р»РѕСЃСЊ': 'дней осталось',
    'РѕС†РµРЅРѕРє': 'оценок',
    
    # Profile management
    'Р"РѕР±Р°РІРёС‚СЊ РїСЂРѕС„РёР»СЊ': 'Добавить профиль',
    'Р"РѕР±Р°РІРёС‚СЊ РґРµС‚СЃРєРёР№': 'Добавить детский',
    'РЎРјРµРЅРёС‚СЊ Р°РєРєР°СѓРЅС‚': 'Сменить аккаунт',
    
    # Promo codes
    'РџСЂРѕРјРѕРєРѕРґ': 'Промокод',
    'Р'РІРµРґРёС‚Рµ РїСЂРѕРјРѕРєРѕРґ': 'Введите промокод',
    'РђРєС‚РёРІРёСЂРѕРІР°С‚СЊ': 'Активировать',
    'Р'Р°С€Рё РїСЂРѕРјРѕРєРѕРґС‹': 'Ваши промокоды',
    'РђРєС‚РёРІРёСЂРѕРІР°РЅ': 'Активирован',
    'РќРµ РёСЃРїРѕР»СЊР·РѕРІР°РЅ': 'Не использован',
    'РљРѕРїРёСЂРѕРІР°С‚СЊ': 'Копировать',
    'РЎРѕР·РґР°С‚СЊ РєРѕРґ': 'Создать код',
    'РџСЂРѕРјРѕРєРѕРґРѕРІ РЅРµС‚': 'Промокодов нет',
    'РџСЂРѕРјРѕРєРѕРґ СЃРєРѕРїРёСЂРѕРІР°РЅ': 'Промокод скопирован',
    
    # Support chat
    'Р§Р°С‚ РїРѕРґРґРµСЂР¶РєРё': 'Чат поддержки',
    'РџРѕР¶Р°Р»СѓР№СЃС‚Р°, РґРѕР¶РґРёС‚РµСЃСЊ РїРѕРґРєР»СЋС‡РµРЅРёСЏ РѕРїРµСЂР°С‚РѕСЂР°': 'Пожалуйста, дождитесь подключения оператора',
    'Р'Р°С€Р° РїРѕР·РёС†РёСЏ РІ РѕС‡РµСЂРµРґРё': 'Ваша позиция в очереди',
    'Р'РІРµРґРёС‚Рµ СЃРѕРѕР±С‰РµРЅРёРµ': 'Введите сообщение',
    'РћС‚РїСЂР°РІРёС‚СЊ': 'Отправить',
}

# Apply replacements
total_replacements = 0
for garbled, correct in replacements.items():
    count = content.count(garbled)
    if count > 0:
        print(f"Fixing: {garbled[:30]}... → {correct[:30]}... ({count} occurrences)")
        content = content.replace(garbled, correct)
        total_replacements += count

print(f"\nTotal replacements made: {total_replacements}")

# Create backup
backup_path = file_path + '.backup'
if not os.path.exists(backup_path):
    print(f"Creating backup at: {backup_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        with open(backup_path, 'w', encoding='utf-8') as bf:
            bf.write(f.read())

# Write fixed content
print("Writing fixed content...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ Done! All encoding errors fixed.")
print(f"Backup saved to: {backup_path}")
