
# Audit: tables and figure captions across all section files vs reference
# Usage: python scripts/temp/audit_styles.py

files = {
    'intro_ref': r'c:/Users/elgin/Documents/GitHub/IS431/pages/introduction.html',
    'sec1_intro': r'c:/Users/elgin/Documents/GitHub/IS431/sections/introduction.html',
    'sec2_prob': r'c:/Users/elgin/Documents/GitHub/IS431/sections/problem-clarification.html',
    'sec3_concept': r'c:/Users/elgin/Documents/GitHub/IS431/sections/design-methodology.html',
    'sec4_system': r'c:/Users/elgin/Documents/GitHub/IS431/sections/final-design.html',
}

for name, path in files.items():
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print('=== ' + name + ' ===')
    for i, l in enumerate(lines, 1):
        s = l.strip()
        if '<table' in s:
            uses_class = 'report-table' in s
            marker = 'OK ' if uses_class else 'BAD'
            print('  [' + marker + '] TABLE  L' + str(i) + ': ' + s[:100])
        if 'fig-caption' in s or ('figure' in s.lower() and '<sub' in s.lower()):
            marker = 'OK ' if 'fig-caption' in s else 'BAD'
            print('  [' + marker + '] FIG    L' + str(i) + ': ' + s[:100])
        if 'sub style=' in s and 'figure' in s.lower():
            print('  [BAD] FIG-INLINE L' + str(i) + ': ' + s[:100])
        if 'arrow-left' in s or 'arrow-right' in s or 'Back to Report' in s or 'Footer nav' in s.lower():
            print('  [NAV] ARROW L' + str(i) + ': ' + s[:100])
    print()
