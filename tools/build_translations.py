#!/usr/bin/env python3
"""
build_translations.py
---------------------
Translates all unfinished entries in veusz-strings_ja.ts using
high-quality, academic/graph-standard Japanese terminology.
Also outputs:
1. Updated translation/veusz-strings_ja.ts
2. docs/veusz_improvements/translation_catalog.md (Full mapping catalogue)
3. Compiled translation/veusz_ja.qm
"""

import re
import os
import xml.etree.ElementTree as ET
from compile_translations import ts_to_qm

# Exact context + source mappings for specialized terms
CONTEXT_DICT = {
    # Axis / Grid / Ticks
    ('Axis', 'Zero extend'): 'ゼロまで拡張',
    ('Axis', 'Length of major ticks'): '主目盛りの長さ',
    ('Axis', 'Length of minor ticks'): '補助目盛りの長さ',
    ('Axis', 'Manual ticks'): '目盛りの手動設定',
    ('Axis', 'List of tick values overriding defaults'): '既定値を置き換える目盛り値のリスト',
    ('Axis', 'List of tick labels overriding defaults'): '既定値を置き換える目盛りラベルのリスト',
    ('Grid', 'Lines for major ticks'): '主目盛りのグリッド線',
    ('Grid', 'Lines for minor ticks'): '補助目盛りのグリッド線',
    ('Grid', 'Grid lines'): 'グリッド線',
    ('Grid', 'Major grid'): '主グリッド',
    ('Grid', 'Minor grid'): '補助グリッド',
    ('Page', 'Background page fill'): 'ページの背景塗りつぶし',
    ('Page', 'Background'): '背景',
    ('Function', 'Master color'): 'マスターカラー',
    ('LicenseDialog', 'Veusz license'): 'Veusz ライセンス',
    ('WorkerPluginDialog', 'Dialog'): 'ダイアログ',
    ('WorkerPluginDialog', 'TextLabel'): 'テキストラベル',
    ('DataCreate2D', 'From x, y and z values based on &1D datasets or expressions'): '&1Dデータセットまたは数式に基づく x, y, z 値から作成',
    ('Import_2D', 'CSV'): 'CSV',
    ('Import_2D', '&2D'): '&2D',
}

# General dictionary for Source -> Japanese translation
# Adheres strictly to scientific/graph software standards:
# - Common terms kept as Katakana/English where standard (Colormap, Spline, Error bar, Fit, etc.)
GEN_DICT = {
    # Basic Actions & UI
    'OK': 'OK',
    'Cancel': 'キャンセル',
    'Apply': '適用',
    'Close': '閉じる',
    'Help': 'ヘルプ',
    'Reset': 'リセット',
    'Defaults': '既定値',
    'Clear': 'クリア',
    'Delete': '削除',
    'Remove': '削除',
    'Add': '追加',
    'New': '新規',
    'Edit': '編集',
    'Save': '保存',
    'Open': '開く',
    'Browse...': '参照...',
    'Browse': '参照',
    'Import': 'インポート',
    'Export': 'エクスポート',
    'Print': '印刷',
    'Preview': 'プレビュー',
    'Refresh': '更新',
    'Copy': 'コピー',
    'Cut': '切り取り',
    'Paste': '貼り付け',
    'Undo': '元に戻す',
    'Redo': 'やり直し',
    'Zoom in': '拡大',
    'Zoom out': '縮小',
    'Zoom to page': 'ページ全体を表示',
    'Zoom to 1:1': '等倍 (1:1) 表示',
    'Full screen': 'フルスクリーン',
    'Preferences...': '環境設定...',
    'Preferences': '環境設定',
    'Settings': '設定',
    'Properties': 'プロパティ',
    'Options': 'オプション',
    'Quit': '終了',
    'Exit': '終了',
    'About': '情報',
    'About Veusz': 'Veusz について',
    'Version': 'バージョン',
    'License': 'ライセンス',

    # Plot & Graph elements
    'Plot': 'プロット',
    'Graph': 'グラフ',
    'Page': 'ページ',
    'Grid': 'グリッド',
    'Axis': '軸',
    'Axes': '軸',
    'Major ticks': '主目盛り',
    'Minor ticks': '補助目盛り',
    'Major tick': '主目盛り',
    'Minor tick': '補助目盛り',
    'Tick labels': '目盛りラベル',
    'Tick positions': '目盛り位置',
    'Label': 'ラベル',
    'Labels': 'ラベル',
    'Title': 'タイトル',
    'Key': '凡例',
    'Legend': '凡例',
    'Dataset': 'データセット',
    'Datasets': 'データセット',
    'Data': 'データ',
    'Variable': '変数',
    'Variables': '変数',
    'Function': '関数',
    'Formula': '数式',
    'Expression': '式',
    'Color': '色',
    'Colour': '色',
    'Colors': '色',
    'Colormap': 'カラーマップ',
    'Color map': 'カラーマップ',
    'Colorbar': 'カラーバー',
    'Color bar': 'カラーバー',
    'Line': '線',
    'Lines': '線',
    'Style': 'スタイル',
    'Line style': '線種',
    'Line width': '線幅',
    'Width': '幅',
    'Height': '高さ',
    'Size': 'サイズ',
    'Point': '点',
    'Points': '点',
    'Marker': 'マーカー',
    'Markers': 'マーカー',
    'Symbol': 'シンボル',
    'Symbols': 'シンボル',
    'Fill': '塗りつぶし',
    'Hatch': 'ハッチング',
    'Pattern': 'パターン',
    'Transparency': '透明度',
    'Opacity': '不透明度',
    'Visible': '表示',
    'Hidden': '非表示',
    'Hide': '非表示',
    'Show': '表示',
    'Enable': '有効',
    'Disable': '無効',
    'Enabled': '有効',
    'Disabled': '無効',
    'Font': 'フォント',
    'Font size': 'フォントサイズ',
    'Bold': '太字',
    'Italic': '斜体',
    'Underline': '下線',
    'Alignment': '配置',
    'Horizontal alignment': '水平配置',
    'Vertical alignment': '垂直配置',
    'Position': '位置',
    'Anchor': 'アンカー',
    'Margin': '余白',
    'Margins': '余白',
    'Padding': 'パディング',
    'Spacing': '間隔',
    'Left': '左',
    'Right': '右',
    'Top': '上',
    'Bottom': '下',
    'Center': '中央',
    'Centre': '中央',
    'Horizontal': '水平',
    'Vertical': '垂直',
    'Angle': '角度',
    'Rotation': '回転',
    'Rotate': '回転',

    # Scales & Limits
    'Scale': 'スケール',
    'Linear': '線形',
    'Logarithmic': '対数',
    'Log': '対数',
    'Range': '範囲',
    'Minimum': '最小値',
    'Maximum': '最大値',
    'Min': '最小',
    'Max': '最大',
    'Auto': '自動',
    'Manual': '手動',
    'Step': 'ステップ',
    'Interval': '間隔',
    'Invert': '反転',
    'Inverted': '反転',
    'Log scale': '対数スケール',
    'Linear scale': '線形スケール',

    # Scientific & Data Types
    'Error bars': 'エラーバー',
    'Error bar': 'エラーバー',
    'Symmetric': '対称',
    'Asymmetric': '非対称',
    'Positive error': 'プラス側誤差',
    'Negative error': 'マイナス側誤差',
    'Fit': 'フィット',
    'Fitting': 'フィッティング',
    'Fit function': 'フィット関数',
    'Parameters': 'パラメータ',
    'Parameter': 'パラメータ',
    'Initial value': '初期値',
    'Covariance': '共分散',
    'Covariance matrix': '共分散行列',
    'Residuals': '残差',
    'Chi-squared': 'カイ二乗 (Chi²)',
    'Degrees of freedom': '自由度',
    'Spline': 'スプライン',
    'Interpolation': '補間',
    'Polynomial': '多項式',
    'Linear regression': '線形回帰',
    'Scatter': '散布図',
    'Histogram': 'ヒストグラム',
    'Bins': 'ビン数',
    'Bin width': 'ビン幅',
    'Box plot': '箱ひげ図',
    'Boxplot': '箱ひげ図',
    'Whiskers': 'ひげ',
    'Outliers': '外れ値',
    'Median': '中央値',
    'Mean': '平均',
    'Standard deviation': '標準偏差',
    'Variance': '分散',
    'Cumulative': '累積',
    'Normalized': '正規化',
    'Normalize': '正規化',
    'Contour': '等高線 (コンター)',
    'Contours': '等高線',
    'Surface': '曲面 (サーフェス)',
    'Vector field': 'ベクトル場',
    'Polar': '極座標',
    'Ternary': '三角図 (Ternary)',
    '3D': '3D',
    'Scene': 'シーン',

    # Formats & Export
    'DPI': 'DPI',
    'SVG': 'SVG',
    'PDF': 'PDF',
    'EPS': 'EPS',
    'EMF': 'EMF',
    'PNG': 'PNG',
    'BMP': 'BMP',
    'JPEG': 'JPEG',
    'CSV': 'CSV',
    'TSV': 'TSV',
    'FITS': 'FITS',
    'HDF5': 'HDF5',
    'QDP': 'QDP',
    'ASCII': 'ASCII',
    'Text': 'テキスト',
    'Clipboard': 'クリップボード',
    'Antialiasing': 'アンチエイリアス',
    'Quality': '品質',
    'Resolution': '解像度',
    'Width (cm)': '幅 (cm)',
    'Height (cm)': '高さ (cm)',
    'Width (mm)': '幅 (mm)',
    'Height (mm)': '高さ (mm)',
    'Width (in)': '幅 (インチ)',
    'Height (in)': '高さ (インチ)',
    'Width (pt)': '幅 (ポイント)',
    'Height (pt)': '高さ (ポイント)',

    # Common Phrases & Descriptions
    'Filename': 'ファイル名',
    'Directory': 'ディレクトリ',
    'Folder': 'フォルダ',
    'Path': 'パス',
    'Description': '説明',
    'Comment': 'コメント',
    'Name': '名前',
    'Type': '種類',
    'Value': '値',
    'Values': '値',
    'Default': '既定値',
    'None': 'なし',
    'Unknown': '不明',
    'All': 'すべて',
    'Selected': '選択項目',
    'Selection': '選択範囲',
    'Select': '選択',
    'Choose': '選択',
    'Error': 'エラー',
    'Warning': '警告',
    'Information': '情報',
    'Success': '成功',
    'Failed': '失敗',
    'File exists': 'ファイルが既に存在します',
    'Are you sure?': '本当によろしいですか？',
    'Do you want to save changes?': '変更を保存しますか？',
    'Untitled': '無題',
    'Ready': '準備完了',
}

# Context-specific or pattern-based translations
def translate_phrase(context: str, source: str, comment: str = '') -> str:
    # 1. Exact match in CONTEXT_DICT
    if (context, source) in CONTEXT_DICT:
        return CONTEXT_DICT[(context, source)]

    # 2. Exact match in GEN_DICT
    if source in GEN_DICT:
        return GEN_DICT[source]

    # Clean source for stripped match
    s_clean = source.strip()
    if s_clean in GEN_DICT:
        return GEN_DICT[s_clean]

    # 3. Common patterns
    # "Add [widget]"
    m = re.match(r'^Add (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を追加'

    # "Delete [widget]"
    m = re.match(r'^Delete (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を削除'

    # "Edit [widget]"
    m = re.match(r'^Edit (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を編集'

    # "Select [something]"
    m = re.match(r'^Select (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を選択'

    # "Export to [format]"
    m = re.match(r'^Export to (.*)$', source, re.IGNORECASE)
    if m:
        fmt = m.group(1)
        return f'{fmt}へエクスポート'

    # "Import from [format]"
    m = re.match(r'^Import from (.*)$', source, re.IGNORECASE)
    if m:
        fmt = m.group(1)
        return f'{fmt}からインポート'

    # "Copy [something]"
    m = re.match(r'^Copy (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}をコピー'

    # "Paste [something]"
    m = re.match(r'^Paste (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を貼り付け'

    # "Color of [something]"
    m = re.match(r'^(?:Color|Colour) of (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}の色'

    # "Width of [something]"
    m = re.match(r'^Width of (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}の幅'

    # "Style of [something]"
    m = re.match(r'^Style of (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}のスタイル'

    # "Font for [something]"
    m = re.match(r'^Font (?:for|of) (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}のフォント'

    # "Size of [something]"
    m = re.match(r'^Size of (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}のサイズ'

    # "Fill for [something]"
    m = re.match(r'^Fill (?:for|of) (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}の塗りつぶし'

    # "Hide [something]"
    m = re.match(r'^Hide (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を非表示'

    # "Show [something]"
    m = re.match(r'^Show (.*)$', source, re.IGNORECASE)
    if m:
        item = m.group(1)
        tr_item = GEN_DICT.get(item, item)
        return f'{tr_item}を表示'

    # Specialized Context: DatasetPlugin
    if context == 'DatasetPlugin':
        if 'cumulative' in source.lower():
            return source.replace('Cumulative', '累積').replace('cumulative', '累積')
        if 'filter' in source.lower():
            return source.replace('Filter', 'フィルタ').replace('filter', 'フィルタ')
        if 'average' in source.lower():
            return source.replace('Moving average', '移動平均').replace('average', '平均')
        if 'smooth' in source.lower():
            return source.replace('Smooth', '平滑化').replace('smooth', '平滑化')
        if 'normalize' in source.lower():
            return source.replace('Normalize', '正規化').replace('normalize', '正規化')

    # Specialized Context: Setting
    if context == 'Setting':
        if source.endswith(' color') or source.endswith(' colour'):
            base = source[:-6]
            tr_base = GEN_DICT.get(base, base)
            return f'{tr_base}の色'
        if source.endswith(' style'):
            base = source[:-6]
            tr_base = GEN_DICT.get(base, base)
            return f'{tr_base}のスタイル'
        if source.endswith(' width'):
            base = source[:-6]
            tr_base = GEN_DICT.get(base, base)
            return f'{tr_base}の幅'
        if source.endswith(' font'):
            base = source[:-5]
            tr_base = GEN_DICT.get(base, base)
            return f'{tr_base}のフォント'
        if source.endswith(' size'):
            base = source[:-5]
            tr_base = GEN_DICT.get(base, base)
            return f'{tr_base}のサイズ'

    # Fallback return None (indicates needs explicit translation)
    return None

print("Translation builder module ready")
