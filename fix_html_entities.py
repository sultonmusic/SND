# coding: utf-8
import html
import codecs

# Read the file
with codecs.open('c:\\Users\\emroa\\Downloads\\SND\\app\\src\\main\\assets\\index.html', 'r', 'utf-8') as f:
    content = f.read()

# Find and decode HTML entities in Russian text sections
# This will convert Р—Р°РіСЂСѓР·РєРё back to normal Cyrillic
import re

# Decode HTML entities
content = html.unescape(content)

# Write back
with codecs.open('c:\\Users\\emroa\\Downloads\\SND\\app\\src\\main\\assets\\index.html', 'w', 'utf-8') as f:
    f.write(content)

print("Done! HTML entities decoded.")
