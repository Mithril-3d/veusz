import json
from collections import defaultdict

with open('docs/veusz_improvements/translations_dump.json', encoding='utf-8') as f:
    records = json.load(f)

unfin = [r for r in records if r['unfinished']]
print(f'Total unfinished: {len(unfin)}')

by_context = defaultdict(list)
for r in unfin:
    by_context[r['context']].append((r['source'], r['comment']))

for ctx, items in sorted(by_context.items(), key=lambda x: len(x[1]), reverse=True):
    print(f'=== Context: {ctx} ({len(items)} items) ===')
    for src, cm in items[:5]:
        cm_str = f' [{cm}]' if cm else ''
        print(f'  - {src}{cm_str}')
    if len(items) > 5:
        print(f'  ... and {len(items)-5} more')
