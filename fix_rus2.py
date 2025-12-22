# coding: utf-8
import codecs
import re

# Read
with codecs.open('c:\\Users\\emroa\\Downloads\\SND\\app\\src\\main\\assets\\index.html', 'r', 'utf-8') as f:
    content = f.read()

# Replace pattern: Р[А-Я] with Cyrillic
# This broken encoding uses Latin P (Р) followed by Cyrillic
content = re.sub(r'Р([А-ЯЁа-яё]+)', lambda m: chr(1056 + ord(m.group(1)[0]) - ord('А')) + m.group(1)[1:], content)

# Write
with codecs.open('c:\\Users\\emroa\\Downloads\\SND\\app\\src\\main\\assets\\index.html', 'w', 'utf-8') as f:
    f.write(content)

print("Done!")
