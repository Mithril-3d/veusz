# -*- coding: utf-8 -*-
"""
local_translator.py
-------------------
Comprehensive, 100% offline translation engine for Veusz.
Incorporates:
1. EXACT_MAPPINGS
2. REMAINING_DICT
3. BULK_DICT
4. GEN_DICT
5. Grammar pattern matchers & domain vocabulary substitution
6. High-quality academic fallback
"""

import re
from translations_data import EXACT_MAPPINGS
from remaining_dict import REMAINING_DICT
from dict_bulk import BULK_DICT
from build_translations import GEN_DICT

# Combine dictionaries
ALL_DICTS = {}
ALL_DICTS.update(GEN_DICT)
ALL_DICTS.update(REMAINING_DICT)
ALL_DICTS.update(BULK_DICT)

# Common verbs & adjectives
VERB_ADJ_MAP = {
    'calculate': '計算する',
    'calculating': '計算中',
    'create': '作成する',
    'creating': '作成中',
    'apply': '適用する',
    'applying': '適用中',
    'select': '選択する',
    'selecting': '選択中',
    'choose': '選択する',
    'choosing': '選択中',
    'specify': '指定する',
    'specifying': '指定中',
    'enable': '有効にする',
    'disable': '無効にする',
    'hide': '非表示にする',
    'show': '表示する',
    'draw': '描画する',
    'drawing': '描画中',
    'plot': 'プロットする',
    'plotting': 'プロット中',
    'fit': 'フィットする',
    'fitting': 'フィッティング',
    'invert': '反転する',
    'scale': 'スケーリングする',
    'scaling': 'スケーリング',
    'normalize': '正規化する',
    'normalizing': '正規化',
    'smooth': '平滑化する',
    'smoothing': '平滑化',
    'filter': 'フィルタリングする',
    'filtering': 'フィルタリング',
    'interpolate': '補間する',
    'interpolating': '補間',
    'differentiate': '微分する',
    'differentiating': '微分',
    'integrate': '積分する',
    'integrating': '積分',
    'sort': 'ソートする',
    'sorting': 'ソート',
    'clip': 'クリップする',
    'clipping': 'クリッピング',
    'remove': '削除する',
    'removing': '削除中',
    'delete': '削除する',
    'deleting': '削除中',
    'edit': '編集する',
    'editing': '編集',
    'update': '更新する',
    'updating': '更新',
    'save': '保存する',
    'saving': '保存中',
    'load': '読み込む',
    'loading': '読み込み中',
    'import': 'インポートする',
    'importing': 'インポート中',
    'export': 'エクスポートする',
    'exporting': 'エクスポート中',
    'print': '印刷する',
    'printing': '印刷中',
    'copy': 'コピーする',
    'copying': 'コピー中',
    'cut': '切り取る',
    'paste': '貼り付ける',
    'pasting': '貼り付け中',
    'undo': '元に戻す',
    'redo': 'やり直す',
    'close': '閉じる',
    'open': '開く',
    'zoom': 'ズームする',
    'pan': 'パン (移動) する',
    'horizontal': '水平',
    'vertical': '垂直',
    'linear': '線形',
    'logarithmic': '対数',
    'log': '対数',
    'manual': '手動',
    'automatic': '自動',
    'auto': '自動',
    'relative': '相対',
    'absolute': '絶対',
    'positive': 'プラス側 (正)',
    'negative': 'マイナス側 (負)',
    'symmetric': '対称',
    'asymmetric': '非対称',
    'cumulative': '累積',
    'normalized': '正規化済み',
    'optional': '任意の',
    'default': '既定の',
    'custom': 'カスタム',
    'selected': '選択された',
    'active': 'アクティブな',
    'current': '現在の',
    'valid': '有効な',
    'invalid': '無効な',
    'empty': '空の',
    'unknown': '不明な',
    'maximum': '最大',
    'minimum': '最小',
    'first': '最初の',
    'last': '最後の',
    'next': '次の',
    'previous': '前の',
}

NOUN_MAP = {
    'dataset': 'データセット',
    'datasets': 'データセット',
    'widget': 'ウィジェット',
    'widgets': 'ウィジェット',
    'plot': 'プロット',
    'plots': 'プロット',
    'graph': 'グラフ',
    'graphs': 'グラフ',
    'page': 'ページ',
    'pages': 'ページ',
    'axis': '軸',
    'axes': '軸',
    'grid': 'グリッド',
    'major tick': '主目盛り',
    'major ticks': '主目盛り',
    'minor tick': '補助目盛り',
    'minor ticks': '補助目盛り',
    'tick': '目盛り',
    'ticks': '目盛り',
    'tick label': '目盛りラベル',
    'tick labels': '目盛りラベル',
    'tick position': '目盛り位置',
    'tick positions': '目盛り位置',
    'label': 'ラベル',
    'labels': 'ラベル',
    'key': '凡例',
    'legend': '凡例',
    'color': '色',
    'colour': '色',
    'colors': '色',
    'colours': '色',
    'colormap': 'カラーマップ',
    'colormaps': 'カラーマップ',
    'colorbar': 'カラーバー',
    'colorbars': 'カラーバー',
    'line': '線',
    'lines': '線',
    'line style': '線種',
    'line width': '線幅',
    'width': '幅',
    'height': '高さ',
    'size': 'サイズ',
    'sizes': 'サイズ',
    'point': '点',
    'points': '点',
    'marker': 'マーカー',
    'markers': 'マーカー',
    'symbol': 'シンボル',
    'symbols': 'シンボル',
    'fill': '塗りつぶし',
    'hatch': 'ハッチング',
    'pattern': 'パターン',
    'transparency': '透明度',
    'opacity': '不透明度',
    'font': 'フォント',
    'font size': 'フォントサイズ',
    'alignment': '配置',
    'position': '位置',
    'positions': '位置',
    'anchor': 'アンカー',
    'margin': '余白',
    'margins': '余白',
    'padding': 'パディング',
    'spacing': '間隔',
    'angle': '角度',
    'rotation': '回転',
    'scale': 'スケール',
    'range': '範囲',
    'limit': '限界',
    'limits': '限界値',
    'minimum': '最小値',
    'maximum': '最大値',
    'min': '最小',
    'max': '最大',
    'mean': '平均',
    'median': '中央値',
    'standard deviation': '標準偏差',
    'variance': '分散',
    'error bar': 'エラーバー',
    'error bars': 'エラーバー',
    'error': 'エラー',
    'whisker': 'ひげ',
    'whiskers': 'ひげ',
    'outlier': '外れ値',
    'outliers': '外れ値',
    'box': '箱',
    'boxes': '箱',
    'border': '枠線',
    'fraction': '比率',
    'value': '値',
    'values': '値',
    'expression': '数式',
    'expressions': '数式',
    'function': '関数',
    'functions': '関数',
    'variable': '変数',
    'variables': '変数',
    'parameter': 'パラメータ',
    'parameters': 'パラメータ',
    'contour': '等高線',
    'contours': '等高線',
    'surface': '曲面',
    'vector field': 'ベクトル場',
    'histogram': 'ヒストグラム',
    'histograms': 'ヒストグラム',
    'bin': 'ビン',
    'bins': 'ビン',
    'binning': 'ビン分割',
    'bin width': 'ビン幅',
    'document': 'ドキュメント',
    'file': 'ファイル',
    'files': 'ファイル',
    'folder': 'フォルダ',
    'directory': 'ディレクトリ',
    'window': 'ウィンドウ',
    'dialog': 'ダイアログ',
    'toolbar': 'ツールバー',
    'console': 'コンソール',
    'command': 'コマンド',
    'commands': 'コマンド',
    'settings': '設定',
    'setting': '設定',
    'preferences': '環境設定',
    'options': 'オプション',
    'properties': 'プロパティ',
    'text': 'テキスト',
    'number': '数値',
    'column': '列',
    'columns': '列',
    'row': '行',
    'rows': '行',
    'header': 'ヘッダー',
    'footer': 'フッター',
    'step': 'ステップ',
    'steps': 'ステップ',
    'delimiter': '区切り文字',
    'separator': 'セパレータ',
    'preview': 'プレビュー',
    'factor': '係数・倍率',
    'constant': '定数',
    'ratio': '比率',
    'degree': '度',
    'degrees': '度',
    'radian': 'ラジアン',
    'radians': 'ラジアン',
    'algorithm': 'アルゴリズム',
    'method': '手法',
    'mode': 'モード',
    'type': '種類',
    'name': '名前',
    'title': 'タイトル',
    'item': '項目',
    'items': '項目',
    'level': 'レベル',
    'levels': 'レベル',
    'curve': '曲線',
    'curves': '曲線',
    'bar': 'バー',
    'bars': 'バー',
    'cap': 'キャップ',
    'caps': 'キャップ',
    'arrow': '矢印',
    'arrows': '矢印',
    'break': 'ブレーク',
    'breaks': 'ブレーク',
    'gap': 'ギャップ',
    'gaps': 'ギャップ',
    'shape': '形状',
    'image': '画像',
    'images': '画像',
    'bitmap': 'ビットマップ',
    'vector': 'ベクター',
    'distance': '距離',
    'order': '次数・順序',
    'interval': '間隔',
    'intervals': '間隔',
    'weight': '重み',
    'weights': '重み',
    'count': 'カウント数',
    'counts': 'カウント数',
    'sum': '合計',
    'difference': '差分',
    'quotient': '商',
    'product': '積',
    'residual': '残差',
    'residuals': '残差',
    'covariance': '共分散',
}

def translate_phrase(text: str) -> str:
    """Translate single word or short phrase."""
    t_clean = text.strip()
    t_low = t_clean.lower()
    if t_clean in ALL_DICTS:
        return ALL_DICTS[t_clean]
    if t_low in NOUN_MAP:
        return NOUN_MAP[t_low]
    if t_low in VERB_ADJ_MAP:
        return VERB_ADJ_MAP[t_low]
    return text

def local_translate(context: str, source: str, comment: str = '') -> str:
    """Comprehensive translation for any Veusz string."""
    # 1. Exact Context + Source
    if (context, source) in EXACT_MAPPINGS:
        return EXACT_MAPPINGS[(context, source)]

    # 2. Exact in ALL_DICTS
    if source in ALL_DICTS:
        return ALL_DICTS[source]
    s_strip = source.strip()
    if s_strip in ALL_DICTS:
        return ALL_DICTS[s_strip]

    # Accelerator key
    if '&' in source:
        clean = source.replace('&', '')
        if clean in ALL_DICTS:
            base = ALL_DICTS[clean]
            m = re.search(r'&([A-Za-z0-9])', source)
            if m:
                return f"{base}(&{m.group(1)})"
            return base

    # 3. Common grammatical templates
    # "Whether to [verb] [something]"
    m = re.match(r'^Whether to (.*)$', source, re.IGNORECASE)
    if m:
        sub = m.group(1)
        return f'{translate_phrase(sub)}するかどうか'

    # "Dataset of [something]" / "Dataset with [something]"
    m = re.match(r'^Dataset (?:of|with) (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}を含むデータセット'

    # "Dataset to [action]"
    m = re.match(r'^Dataset to (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}するデータセット'

    # "Fraction of [something]"
    m = re.match(r'^Fraction of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の割合'

    # "Number of [something]"
    m = re.match(r'^Number of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の数'

    # "Range of [something]"
    m = re.match(r'^Range of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の範囲'

    # "Positions along [something]"
    m = re.match(r'^Positions along (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}に沿った位置'

    # "Lines for [something]"
    m = re.match(r'^Lines for (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の線'

    # "Color of [something]" / "Colour of [something]"
    m = re.match(r'^(?:Color|Colour) of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の色'

    # "Color for [something]" / "Colour for [something]"
    m = re.match(r'^(?:Color|Colour) for (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の色'

    # "Width of [something]"
    m = re.match(r'^Width of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の幅'

    # "Size of [something]"
    m = re.match(r'^Size of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のサイズ'

    # "Style of [something]"
    m = re.match(r'^Style of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のスタイル'

    # "Font for [something]" / "Font of [something]"
    m = re.match(r'^Font (?:for|of) (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のフォント'

    # "Transparency of [something]"
    m = re.match(r'^Transparency (?:of|for) (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の透明度'

    # "Fill fraction of [something]"
    m = re.match(r'^Fill fraction of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の塗りつぶし比率'

    # "Marker for [something]"
    m = re.match(r'^Marker for (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のマーカー'

    # "Line around [something]"
    m = re.match(r'^Line around (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の外枠線'

    # "List of [something]"
    m = re.match(r'^List of (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のリスト'

    # "Add [something]"
    m = re.match(r'^Add (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}を追加'

    # "Delete [something]" / "Remove [something]"
    m = re.match(r'^(?:Delete|Remove) (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}を削除'

    # "Edit [something]"
    m = re.match(r'^Edit (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}を編集'

    # "Show [something]"
    m = re.match(r'^Show (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}を表示'

    # "Hide [something]"
    m = re.match(r'^Hide (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}を非表示'

    # "Scale [something]"
    m = re.match(r'^Scale (.*)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のスケーリング'

    # "[Something] color" / "[Something] colour"
    m = re.match(r'^(.*) (?:color|colour)$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の色'

    # "[Something] style"
    m = re.match(r'^(.*) style$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のスタイル'

    # "[Something] width"
    m = re.match(r'^(.*) width$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の幅'

    # "[Something] line"
    m = re.match(r'^(.*) line$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}線'

    # "[Something] border"
    m = re.match(r'^(.*) border$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の境界線'

    # "[Something] fill"
    m = re.match(r'^(.*) fill$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}の塗りつぶし'

    # "[Something] size"
    m = re.match(r'^(.*) size$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}のサイズ'

    # "[Something] mode"
    m = re.match(r'^(.*) mode$', source, re.IGNORECASE)
    if m:
        item = translate_phrase(m.group(1))
        return f'{item}モード'

    # Word-by-word fallback for short titles
    words = source.split()
    if len(words) <= 3:
        tr_words = [translate_phrase(w) for w in words]
        if any(tw != w for tw, w in zip(tr_words, words)):
            return ''.join(tr_words) if all('\u3000' <= ch <= '\u9fff' for tw in tr_words for ch in tw) else ' '.join(tr_words)

    # Contextual fallbacks for complex sentences
    # Replace key terms in place
    translated_text = source
    for en_term, ja_term in sorted(NOUN_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = re.compile(rf'\b{re.escape(en_term)}\b', re.IGNORECASE)
        translated_text = pattern.sub(ja_term, translated_text)
    for en_term, ja_term in sorted(VERB_ADJ_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = re.compile(rf'\b{re.escape(en_term)}\b', re.IGNORECASE)
        translated_text = pattern.sub(ja_term, translated_text)

    if translated_text != source:
        return translated_text

    # Default fallback
    return source

print("local_translator v3 ready")
