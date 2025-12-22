# coding: utf-8
import codecs

# Read the file
with codecs.open('c:\\Users\\emroa\\Downloads\\SND\\app\\src\\main\\assets\\index.html', 'r', 'utf-8') as f:
    content = f.read()

# Fix all encoding issues - using unicode escapes
content = content.replace('\u0432\u0402\u201c', '—')  # em dash
content = content.replace('\u0432\u0402\u2018', '-')  # hyphen
content = content.replace('\u0432\u0402', "'")  # apostrophe

# Write back
with codecs.open('c:\\Users\\emroa\\Downloads\\SND\\app\\src\\main\\assets\\index.html', 'w', 'utf-8') as f:
    f.write(content)

print("Done! All encoding errors fixed.")
