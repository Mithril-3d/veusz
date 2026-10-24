import xml.etree.ElementTree as ET
import csv

tree = ET.parse('translation/veusz-strings_ja.ts')
root = tree.getroot()

with open('docs/veusz_improvements/unfinished_strings.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Context', 'Source', 'Comment'])
    for ctx in root.findall('context'):
        cname = ctx.find('name').text or ''
        for msg in ctx.findall('message'):
            tr_elem = msg.find('translation')
            tr = tr_elem.text if tr_elem is not None and tr_elem.text else ''
            tr_type = tr_elem.get('type') if tr_elem is not None else ''
            if tr_type == 'unfinished' or not tr.strip():
                src = msg.find('source').text or ''
                cm = (msg.find('comment').text or '') if msg.find('comment') is not None else ''
                writer.writerow([cname, src, cm])

print("Saved unfinished_strings.csv")
