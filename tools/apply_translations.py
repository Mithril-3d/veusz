#!/usr/bin/env python3
"""
apply_translations.py
---------------------
Applies the complete translation dictionaries to translation/veusz-strings_ja.ts,
removes 'unfinished' status, compiles translation/veusz_ja.qm, and produces
docs/veusz_improvements/translation_catalog.md.
"""

import os
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QCoreApplication, QTranslator

sys.path.append(os.path.dirname(__file__))
from final_mappings import FINAL_MAPPINGS
from local_translator import local_translate, ALL_DICTS
from compile_translations import ts_to_qm

# Merge all mappings
ALL_DICTS.update(FINAL_MAPPINGS)

def run():
    ts_file = 'translation/veusz-strings_ja.ts'
    tree = ET.parse(ts_file)
    root = tree.getroot()

    total_count = 0
    resolved_count = 0
    existing_count = 0

    catalog_records = []

    for ctx in root.findall('context'):
        cname = ctx.find('name').text or ''
        for msg in ctx.findall('message'):
            total_count += 1
            src_elem = msg.find('source')
            src = src_elem.text if src_elem is not None and src_elem.text else ''
            cm_elem = msg.find('comment')
            cm = cm_elem.text if cm_elem is not None and cm_elem.text else ''
            tr_elem = msg.find('translation')
            tr = tr_elem.text if tr_elem is not None and tr_elem.text else ''
            tr_type = tr_elem.get('type') if tr_elem is not None else ''

            is_unfinished = (tr_type == 'unfinished') or not (tr and tr.strip())

            if is_unfinished:
                new_tr = local_translate(cname, src, cm)
                if tr_elem is None:
                    tr_elem = ET.SubElement(msg, 'translation')
                tr_elem.text = new_tr
                if 'type' in tr_elem.attrib:
                    del tr_elem.attrib['type']
                resolved_count += 1
                status = "New (新規確定)"
                final_tr = new_tr
            else:
                existing_count += 1
                status = "Existing (既存確定)"
                final_tr = tr

            catalog_records.append({
                'context': cname,
                'source': src,
                'comment': cm,
                'translation': final_tr,
                'status': status
            })

    print(f"Total messages: {total_count}")
    print(f"Newly translated / resolved: {resolved_count}")
    print(f"Existing messages: {existing_count}")

    # Write updated TS
    print(f"Saving updated {ts_file}...")
    tree.write(ts_file, encoding='utf-8', xml_declaration=True)

    # Compile QM
    qm_file = 'translation/veusz_ja.qm'
    print(f"Compiling binary QM: {qm_file}...")
    compiled_count = ts_to_qm(ts_file, qm_file)
    print(f"Successfully compiled {compiled_count} messages into {qm_file}!")

    # Verify loading in QTranslator
    app = QCoreApplication([])
    translator = QTranslator()
    load_ok = translator.load(qm_file)
    print(f"QTranslator load verification: {'PASS' if load_ok else 'FAIL'}")
    assert load_ok, "Failed to load generated QM in QTranslator"

    # Write Full Catalog Markdown
    catalog_md = 'docs/veusz_improvements/translation_catalog.md'
    print(f"Generating full translation catalog: {catalog_md}...")
    with open(catalog_md, 'w', encoding='utf-8') as f:
        f.write("# Veusz 日本語翻訳対応カタログ (Translation Catalog)\n\n")
        f.write("Veusz の UI キー（英語原文）と日本語訳の完全対応カタログです。\n")
        f.write("無理な直訳を避け、アカデミック・グラフ描画ソフトで定着しているカタカナ表記・アルファベット表記を維持しています。\n\n")
        f.write(f"- 総メッセージ数: **{total_count} 件**\n")
        f.write(f"- 新規翻訳・補完: **{resolved_count} 件** (100% 翻訳完了)\n")
        f.write(f"- 既存翻訳: **{existing_count} 件**\n")
        f.write(f"- コンパイル済みバイナリ: [`translation/veusz_ja.qm`](file:///c:/Users/Vogler/Documents/3dprint/Antigravity/Veusz/translation/veusz_ja.qm)\n\n")
        f.write("| Context | Source (英語原文) | Translation (日本語訳) | 状態 |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for rec in catalog_records:
            ctx_esc = rec['context'].replace('|', '\\|')
            src_esc = rec['source'].replace('|', '\\|').replace('\n', '<br>')
            tr_esc = rec['translation'].replace('|', '\\|').replace('\n', '<br>')
            f.write(f"| `{ctx_esc}` | {src_esc} | {tr_esc} | {rec['status']} |\n")

    print("All tasks completed successfully!")

if __name__ == '__main__':
    run()
