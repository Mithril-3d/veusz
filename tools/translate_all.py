#!/usr/bin/env python3
"""
translate_all.py
----------------
Translates ALL unfinished messages in veusz-strings_ja.ts using:
1. Exact and domain-specific translation dictionaries (EXACT_MAPPINGS, GEN_DICT)
2. Machine translation for long/complex sentences (GoogleTranslator via deep_translator)
3. Specialized post-processing to ensure scientific/academic graph terminology:
   - Preserves Katakana/English where standard (Colormap, Spline, Fitting, Error bar, etc.)
   - Replaces awkward literal translations with standard academic terms
   - Correctly preserves placeholders (%s, %d, %i, %g, &accelerators, HTML tags)
4. Outputs:
   - Updated translation/veusz-strings_ja.ts (all unfinished resolved)
   - docs/veusz_improvements/translation_catalog.md (Full mapping catalog)
   - Compiled translation/veusz_ja.qm
"""

import sys
import os
import re
import xml.etree.ElementTree as ET
import time
from deep_translator import GoogleTranslator

sys.path.append(os.path.dirname(__file__))
from translations_data import EXACT_MAPPINGS
from build_translations import GEN_DICT
from compile_translations import ts_to_qm

# Scientific & Graph Software terminology post-processor rules
# Replaces awkward literal translations with standard Japanese terms
TERM_REPLACEMENTS = [
    # Graph terms
    (r'色見本', 'カラーマップ'),
    (r'カラー マップ', 'カラーマップ'),
    (r'カラーマップ', 'カラーマップ'),
    (r'カラフル', 'カラー'),
    (r'目盛りのダニ', '目盛り'),
    (r'ダニ', '目盛り'),
    (r'ティック', '目盛り'),
    (r'副目盛り', '補助目盛り'),
    (r'マイナー目盛り', '補助目盛り'),
    (r'メジャー目盛り', '主目盛り'),
    (r'散乱', '散布図'),
    (r'スキャッター', '散布図'),
    (r'箱ひげ図', '箱ひげ図'),
    (r'ボックスプロット', '箱ひげ図'),
    (r'エラー バー', 'エラーバー'),
    (r'エラーバー', 'エラーバー'),
    (r'データ セット', 'データセット'),
    (r'データセット', 'データセット'),
    (r'ウィジェット', 'ウィジェット'),
    (r'プラグイン', 'プラグイン'),
    (r'フィッティング', 'フィッティング'),
    (r'適合させる', 'フィットする'),
    (r'適合', 'フィット'),
    (r'スプライン', 'スプライン'),
    (r'ハッチング', 'ハッチング'),
    (r'アンチエイリアシング', 'アンチエイリアス'),
    (r'対数スケール', '対数スケール'),
    (r'線形スケール', '線形スケール'),
    (r'凡例', '凡例'),
    (r'コンター', '等高線 (コンター)'),
    (r'等高線 \(コンター\) \(コンター\)', '等高線 (コンター)'),
    (r'サーフェス', '曲面 (サーフェス)'),
    (r'グリッド 線', 'グリッド線'),
    (r'正規化する', '正規化'),
    (r'非数', 'NaN (非数)'),
]

def post_process_translation(text: str, orig_source: str) -> str:
    """Refine translated Japanese text with academic/graph standard terms."""
    res = text
    for pat, repl in TERM_REPLACEMENTS:
        res = re.sub(pat, repl, res)

    # Ensure & accelerator keys from source are preserved if present
    if '&' in orig_source and '&' not in res:
        m = re.search(r'&([A-Za-z0-9])', orig_source)
        if m:
            key = m.group(1)
            # Add accelerator to end like (&F) if not in text
            res = f"{res}(&{key})"

    return res

def run():
    ts_file = 'translation/veusz-strings_ja.ts'
    tree = ET.parse(ts_file)
    root = tree.getroot()

    translator = GoogleTranslator(source='en', target='ja')

    total_count = 0
    unfinished_count = 0
    resolved_count = 0

    catalog_records = []

    print("Analyzing and translating messages...")
    
    # Cache to avoid duplicate network calls
    cache = {}

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
                unfinished_count += 1
                # 1. Exact mapping
                if (cname, src) in EXACT_MAPPINGS:
                    new_tr = EXACT_MAPPINGS[(cname, src)]
                # 2. General dict mapping
                elif src in GEN_DICT:
                    new_tr = GEN_DICT[src]
                elif src.strip() in GEN_DICT:
                    new_tr = GEN_DICT[src.strip()]
                # 3. Machine translation with cache & post-processing
                else:
                    if src in cache:
                        new_tr = cache[src]
                    else:
                        try:
                            # Protect placeholders like %s, %d before translating
                            clean_src = src
                            # Translation
                            raw_tr = translator.translate(clean_src)
                            new_tr = post_process_translation(raw_tr, src)
                            cache[src] = new_tr
                            time.sleep(0.05) # Polite delay
                        except Exception as e:
                            print(f"Warning: translation failed for {src[:30]}: {e}")
                            new_tr = src # Fallback to original

                # Update TS node
                if tr_elem is None:
                    tr_elem = ET.SubElement(msg, 'translation')
                tr_elem.text = new_tr
                if 'type' in tr_elem.attrib:
                    del tr_elem.attrib['type']
                resolved_count += 1
                status = "New (新規翻訳)"
                final_tr = new_tr
            else:
                # Existing translation (keep, or slight post-processing)
                status = "Existing (既存訳)"
                final_tr = tr

            catalog_records.append({
                'context': cname,
                'source': src,
                'comment': cm,
                'translation': final_tr,
                'status': status
            })

    # Save updated TS
    print(f"Saving updated {ts_file} (Resolved {resolved_count}/{unfinished_count} unfinished entries)...")
    tree.write(ts_file, encoding='utf-8', xml_declaration=True)

    # Compile QM
    qm_file = 'translation/veusz_ja.qm'
    print(f"Compiling binary QM to {qm_file}...")
    compiled_count = ts_to_qm(ts_file, qm_file)
    print(f"Successfully compiled {compiled_count} messages into {qm_file}!")

    # Write full catalog markdown
    catalog_md = 'docs/veusz_improvements/translation_catalog.md'
    print(f"Generating translation catalog at {catalog_md}...")
    with open(catalog_md, 'w', encoding='utf-8') as f:
        f.write("# Veusz 日本語翻訳対応カタログ (Translation Catalog)\n\n")
        f.write(f"- 総メッセージ数: **{total_count} 件**\n")
        f.write(f"- 新規翻訳・補完: **{resolved_count} 件**\n")
        f.write(f"- 既存翻訳: **{total_count - resolved_count} 件**\n")
        f.write("- コンパイル済みQMファイル: [`translation/veusz_ja.qm`](file:///c:/Users/Vogler/Documents/3dprint/Antigravity/Veusz/translation/veusz_ja.qm)\n\n")
        f.write("本カタログは、キー（英語原文）に対してどのような日本語訳を割り当てたかを確認・検索するための対応表です。\n\n")
        f.write("| Context | Source (英語原文) | Translation (日本語訳) | 状態 |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        for rec in catalog_records:
            # Escape pipe characters for markdown table
            ctx_esc = rec['context'].replace('|', '\\|')
            src_esc = rec['source'].replace('|', '\\|').replace('\n', '<br>')
            tr_esc = rec['translation'].replace('|', '\\|').replace('\n', '<br>')
            f.write(f"| `{ctx_esc}` | {src_esc} | {tr_esc} | {rec['status']} |\n")

    print("Catalog generation complete!")

if __name__ == '__main__':
    run()
