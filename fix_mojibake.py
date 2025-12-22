# coding: utf-8
"""
Fix encoding issues by detecting and fixing mojibake patterns
"""

import re

file_path = r'c:\Users\emroa\Downloads\SND\app\src\main\assets\index.html'

print("Reading file...")
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original file size: {len(content)} characters")

# Create a comprehensive regex pattern to find mojibake sequences
# These are sequences that contain the specific mojibake characters
mojibake_patterns = [
    # Pattern: Sequences starting with Р and containing mojibake characters
    r'Р[А-ЯЁа-яёРЎСЊ\u0080-\u00FF\u2018-\u203A]+',
]

# Find all potential mojibake sequences
potential_mojibake = set()
for pattern in mojibake_patterns:
    matches = re.findall(pattern, content)
    for match in matches:
        # Check if it contains suspicious characters (non-Cyrillic in expected Cyrillic context)
        if any(c in match for c in 'ЃІЅЇ'):
            potential_mojibake.add(match)

print(f"\nFound {len(potential_mojibake)} potential mojibake sequences")

# Manual approach: encode the file correctly
# The issue is Windows-1251 text was incorrectly interpreted as UTF-8

# Strategy: Re-encode problematic sections
def fix_mojibake_line_by_line(text):
    """
    Attempt to fix mojibake by re-encoding problematic parts
    """
    lines = text.split('\n')
    fixed_lines = []
    fixes_made = 0
    
    for line in lines:
        # Check if line contains mojibake markers
        if 'Р' in line and any(char in line for char in 'ЃІЅЇ'):
            # This line likely has mojibake
            try:
                # Try to fix by encoding as latin1 then decoding as windows-1251
                # This reverses the double-encoding
                fixed_line = line.encode('latin1').decode('windows-1251')
                fixed_lines.append(fixed_line)
                if fixed_line != line:
                    fixes_made += 1
            except (UnicodeEncodeError, UnicodeDecodeError):
                # If that doesn't work, keep original
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    print(f"Fixed {fixes_made} lines with mojibake")
    return '\n'.join(fixed_lines)

# Apply the fix
print("\nAttempting to fix mojibake...")
fixed_content = fix_mojibake_line_by_line(content)

# Backup original
import os
backup_path = file_path + '.backup_before_fix'
if not os.path.exists(backup_path):
    print(f"Creating backup: {backup_path}")
    with open(backup_path, 'w', encoding='utf-8') as bf:
        bf.write(content)

# Write fixed content
print("Writing fixed content...")
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("\n✓ Encoding fix complete!")
print(f"Backup saved to: {backup_path}")
