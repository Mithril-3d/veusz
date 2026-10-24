#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix translation issues:
1. WidgetTree context: Name -> 名前, Type -> 種類
2. ToolsPlugin context: Colors, General, Widgets, Replace text, etc.
3. Tutorial context: Window title, buttons (Next, Close), and natural Japanese text for all 38 steps.
"""

import os
import sys
import xml.etree.ElementTree as ET

TUTORIAL_TRANSLATIONS = {
    # Step 1: Welcome
    "<h1>Welcome to Veusz!</h1>": """<h1>Veusz へようこそ！</h1>

<p>このチュートリアルでは、Veusz の基本的な使い方を素早く学べます。</p>

<p>このチュートリアルは、パネル右上の閉じるボタンからいつでも終了できます。また、ヘルプメニューからいつでも再開できます。</p>

<p class="usercmd">「次へ」ボタンを押して進んでください。</p>""",

    # Step 2: Widgets
    "<h1>Widgets</h1>": """<h1>ウィジェット</h1>

<p>Veusz のプロットは「<b>ウィジェット</b>」を組み合わせて作成されます。プロットの各要素を作るために、様々な種類のウィジェットが用意されています。例えば、座標軸、グラフ、データプロット、関数プロットなどのウィジェットがあります。</p>

<p>また、特別なウィジェットもあります。例えばグリッドウィジェットは、複数のグラフを格子状（グリッド）に整列して配置できます。</p>""",

    # Step 3: Hierarchy
    "<p>Widgets can often be placed inside each other.": """<p>ウィジェットは入れ子（階層構造）にして配置できます。例えば、グラフウィジェットはページウィジェットやグリッドウィジェットの中に配置され、プロット用のウィジェットはグラフウィジェットの中に配置されます。</p>

<p>異なる種類のウィジェットを複数配置することも可能です。例えば、1ページ内に複数のグラフを並べたり、1つのグラフ内に複数のプロットウィジェットや軸ウィジェットを配置できます。</p>""",

    # Step 4: Widget editing
    "<h1>Widget editing</h1>": """<h1>ウィジェットの編集</h1>

<p>点滅しているウィンドウが「編集」ウィンドウです。現在プロットに含まれるウィジェットが階層ツリーで表示されています。各ウィジェットには名前（左列）と種類（右列）があります。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 5: Expand widget
    "<p>The graph widget is the currently selected widget.</p>": """<p>現在、グラフウィジェットが選択されています。</p>

<p class="usercmd">編集ウィンドウでグラフウィジェットを展開し（左側の矢印または＋をクリック）、x 軸ウィジェットを選択してください。</p>""",

    # Step 6: Widget properties
    "<h1>Widget properties</h1>": """<h1>ウィジェットのプロパティ</h1>

<p>このウィンドウには、現在選択されているウィジェット（グラフの x 軸）のプロパティが表示されます。</p>

<p class="usercmd">「ラベル」の右側にあるテキスト入力欄をクリックし、適当な文字を入力して Enter キーを押してください。</p>""",

    # Step 7: Label updated
    "<p>Notice that the x axis label of your plot has now been updated.": """<p>プロットの x 軸ラベルが更新されたことを確認してください。プロパティウィンドウで設定を変更すると、プロットに即座に反映されます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 8: Adding widgets
    "<h1>Adding widgets</h1>": """<h1>ウィジェットの追加</h1>

<p>点滅している「ウィジェットの追加」ツールバーを使うと、新しいウィジェットをプロットに追加できます。現在選択されているウィジェットの子要素として追加されます。</p>

<p>ツールバーには、ページ、グラフ、グリッド、軸、関数、データプロット、ラベル、画像、図形などのウィジェットを追加するボタンが並んでいます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 9: Add a function
    "<h1>Add a function</h1>": """<h1>関数の追加</h1>

<p>グラフに関数プロットウィジェットを追加してみましょう。</p>

<p class="usercmd">「関数の挿入」ボタン（点滅中）をクリックするか、メニューの「挿入 → 関数」を選択してください。</p>""",

    # Step 10: Function added
    "<p>You have now added a function widget to the graph widget.": """<p>グラフに関数ウィジェットが追加されました。既定では関数 y = x がプロットされます。</p>

<p class="usercmd">プロパティウィンドウで「関数」設定を <code>sin(x)</code> に変更し、Enter キーを押してください。</p>""",

    # Step 11: Formatting
    "<h1>Formatting</h1>": """<h1>書式設定</h1>

<p>ウィジェットには、見た目を調整するための様々な書式設定プロパティがあります。書式設定は、プロパティウィンドウの下部にある「書式設定」タブに表示されます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 12: Formatting tabs
    "<p>Different types of formatting properties are grouped under tabs": """<p>書式設定プロパティはタブごとにグループ化されています。現在の関数ウィジェットには「メイン」タブ（線種、太さ、色など）と「塗りつぶし」タブがあります。</p>

<p class="usercmd">「メイン」タブで線の色を別の色に変更してみてください。</p>""",

    # Step 13: Line style
    "<p>Veusz lets you choose a line style, thickness and color": """<p>Veusz では、線のスタイル、太さ、色を自由に変更できます。また、透過度（透明度）の設定も可能です。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 14: Datasets
    "<h1>Datasets</h1>": """<h1>データセット</h1>

<p>Veusz の多くのウィジェットは「データセット」をプロットします。データセットは、ファイルからのインポート、新しいデータの入力、または既存データセットからの計算によって作成できます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 15: Importing data
    "<h1>Importing data</h1>": """<h1>データのインポート</h1>

<p>まず、データをインポートしてみましょう。</p>

<p class="usercmd">「データのインポート」ボタン（点滅中）をクリックするか、メニューの「データ → インポート」を選択してください。</p>""",

    # Step 16: Import dialog
    "<p>This is the data import dialog.": """<p>これがデータインポートダイアログです。このチュートリアルでは、あらかじめサンプルデータファイルが自動的に選択されています。</p>

<p class="usercmd">「インポート」ボタンをクリックしてデータを読み込んでください。</p>""",

    # Step 17: Guess datatype
    "<p>Veusz will try to guess the datatype": """<p>Veusz はデータの形式（数値、テキスト、日時など）を自動判別します。2D データや多次元データのインポートにも対応しています。</p>

<p class="usercmd">インポートダイアログの「閉じる」ボタンをクリックしてください。</p>""",

    # Step 18: Datasets loaded
    "<p>Notice how Veusz has loaded the three different datasets": """<p>3つの異なるデータセットが読み込まれたことを確認してください。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 19: Data viewing window
    "<p>The Data viewing window (flashing)": """<p>点滅している「データ」ウィンドウには、現在読み込まれているデータセットが表示されます。データセットのプレビューや編集がここから行えます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 20: Plotting data
    "<h1>Plotting data</h1>": """<h1>データのプロット</h1>

<p>ポイントプロットウィジェットを使うと、x-y データをプロットできます。</p>

<p class="usercmd">「点の挿入」ボタン（点滅中）をクリックして、ポイントプロットウィジェットを追加してください。</p>""",

    # Step 21: Setting datasets
    "<p>The datasets to be plotted are in the widget's properties": """<p>プロットするデータセットは、プロパティウィンドウで指定します。</p>

<p class="usercmd">「Xデータ」設定を <code>x</code> に変更してください。</p>""",

    # Step 22: Y data
    '<p class="usercmd">Change the "Y data" setting to be the': """<p class="usercmd">次に、「Yデータ」設定を <code>y</code> に変更してください。</p>""",

    # Step 23: Data plotted
    "<p>Veusz has now plotted the data on the graph.": """<p>グラフ上にデータがプロットされました。ポイントの形やサイズ、エラーバー、色などを自由に変更できます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 24: Change point color
    "<p>Now we will change the point color.</p>": """<p>ポイントの色を変更してみましょう。</p>

<p class="usercmd">書式設定の「メイン」タブで、マーカーの塗りつぶし色を別の色に変更してください。</p>""",

    # Step 25: Adding a second dataset
    "<h1>Adding a second dataset</h1>": """<h1>2つ目のデータセットを追加</h1>

<p>もう1つのポイントプロットウィジェットを追加して、別のデータをプロットしてみましょう。</p>

<p class="usercmd">「点の挿入」ボタン（点滅中）をクリックしてください。</p>""",

    # Step 26: Second X data
    '<p class="usercmd">Change the "X data" setting to be the <code>x</code>': """<p class="usercmd">2つ目のウィジェットの「Xデータ」を <code>x</code> に設定してください。</p>""",

    # Step 27: Second Y data
    '<p class="usercmd">Next, change the "Y data" setting to be the <code>y2</code>': """<p class="usercmd">次に、「Yデータ」を <code>y2</code> に設定してください。</p>""",

    # Step 28: Fill below
    "<p>We can fill regions under plots": """<p>プロットの下部を塗りつぶすこともできます。書式設定の「塗りつぶし」タブで設定可能です。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 29: Saving
    "<h1>Saving</h1>": """<h1>保存</h1>

<p>作成したドキュメントは「ファイル → 保存」から保存できます。Veusz のドキュメント形式（.vsz）はテキストファイルであり、Python スクリプトとして直接読み書きすることも可能です。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 30: Exporting
    "<h1>Exporting</h1>": """<h1>画像・ベクターのエクスポート</h1>

<p>ドキュメントは、SVG、PDF、EPS などのベクター形式や、PNG、JPG、BMP、EMF などの形式で高画質にエクスポートできます。クリップボードへの EMF コピーにも対応しています。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 31: Cut and paste
    "<h1>Cut and paste</h1>": """<h1>切り取りと貼り付け</h1>

<p>ウィジェットは切り取り、コピー、貼り付けが可能です。別のドキュメントや別のページへの複製も簡単に行えます。</p>

<p class="usercmd">グラフウィジェットを選択した状態で、「次へ」を押してください。</p>""",

    # Step 32: Click cut
    '<p class="usercmd">Now click the Cut icon (flashing)': """<p class="usercmd">「切り取り」アイコン（点滅中）をクリックするか、Ctrl+X を押してグラフを切り取ってください。</p>""",

    # Step 33: Adding a grid
    "<h1>Adding a grid</h1>": """<h1>グリッド（格子）の追加</h1>

<p>複数のグラフを並べるために、グリッドウィジェットを追加しましょう。</p>

<p class="usercmd">「グリッドの挿入」ボタン（点滅中）をクリックしてください。</p>""",

    # Step 34: Click paste 1
    '<p class="usercmd">Now click the Paste icon (flashing)': """<p class="usercmd">「貼り付け」アイコン（点滅中）をクリックするか、Ctrl+V を押してください。</p>""",

    # Step 35: Click paste 2
    '<p class="usercmd">For a second time, click the Paste icon': """<p class="usercmd">もう一度「貼り付け」をクリックして、2つ目のグラフを配置してください。</p>""",

    # Step 36: Grid arrangement
    "<p>Having the graphs side-by-side": """<p>2つのグラフがグリッド内に整列して配置されました。グリッドウィジェットのプロパティで行数や列数を変更できます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 37: Margins
    "<p>We could now adjust the margins": """<p>グラフやグリッドの余白（マージン）を調整することで、学会誌やプレゼンテーションに最適な美しいレイアウトを作成できます。</p>

<p class="usercmd">「次へ」を押して進んでください。</p>""",

    # Step 38: The End
    "<h1>The End</h1>": """<h1>チュートリアル完了！</h1>

<p>Veusz チュートリアルを完了しました！Veusz には他にも、3D プロット、極座標プロット、三元プロット、データフィッティングなど多彩な機能が備わっています。</p>

<p>詳しくは、ヘルプメニューの「ドキュメント」や各種サンプルファイル（例）をご覧ください。</p>

<p class="usercmd">「閉じる」をクリックしてチュートリアルを終了してください。</p>""",
}

EXTRA_TRANSLATIONS = {
    'WidgetTree': {
        'Name': '名前',
        'Type': '種類',
    },
    'Tutorial': {
        'Tutorial - Veusz': 'チュートリアル - Veusz',
        'Next': '次へ',
        'Close': '閉じる',
    },
    'ToolsPlugin': {
        'Colors': '色',
        'General': '一般',
        'Widgets': 'ウィジェット',
        'Replace text': 'テキストの置換',
        'Replace text…': 'テキストの置換…',
        'Replace text...': 'テキストの置換…',
        'Increase font sizes': 'フォントサイズを拡大',
        'Increase font sizes…': 'フォントサイズを拡大…',
        'Increase font sizes...': 'フォントサイズを拡大…',
        'Decrease font sizes': 'フォントサイズを縮小',
        'Decrease font sizes…': 'フォントサイズを縮小…',
        'Decrease font sizes...': 'フォントサイズを縮小…',
        'Search and replace text in settings': '設定内のテキストを検索・置換',
        'Searches for text in a setting and replaces it': '設定内のテキストを検索し、別のテキストに置換します',
        'Invert colormap': 'カラーマップを反転',
        'Randomize order': '順序をランダム化',
        'Colormap Sequence': 'カラーマップシーケンス',
        'Colormap': 'カラーマップ',
        'Sequence': 'シーケンス',
        'Swap': '入れ替え',
        'Swap two colors': '2つの色を入れ替え',
        'Change references and defaults': '参照と既定値を変更',
        'Delete hidden': '非表示の項目を削除',
        'Mass rename': '一括名前変更',
        'Mass rename widgets': 'ウィジェットの一括名前変更',
    },
    'TreeEditDock': {
        '&Copy as Image': '画像としてコピー (EMF)(&C)',
        'Copy the current page as svg image': '現在のページを画像（EMF）としてクリップボードにコピー',
        'Copy current page to clipboard as image (EMF on Windows)': '現在のページを画像（EMF）としてクリップボードにコピー',
    },
    'TreeEditWindow': {
        '&Copy as Image': '画像としてコピー (EMF)(&C)',
        'Copy the current page as svg image': '現在のページを画像（EMF）としてクリップボードにコピー',
        'Copy current page to clipboard as image (EMF on Windows)': '現在のページを画像（EMF）としてクリップボードにコピー',
    },
    'PlotWindow': {
        '&Previous page': '前のページ(&P)',
        '&Next page': '次のページ(&N)',
        'Move to the previous page': '前のページへ移動',
        'Move to the next page': '次のページへ移動',
        'Force update': '強制再描画',
        'Close full screen': '全画面表示を終了',
        'Updates': '自動更新設定',
        'Antialias': 'アンチエイリアス',
        'reset axes': '軸をリセット',
        'Full screen toolbar': '全画面ツールバー',
    },
}

def main():
    ts_file = 'translation/veusz-strings_ja.ts'
    tree = ET.parse(ts_file)
    root = tree.getroot()

    contexts_by_name = {}
    for ctx in root.findall('context'):
        name_elem = ctx.find('name')
        if name_elem is not None and name_elem.text:
            contexts_by_name[name_elem.text] = ctx

    # 1. Update Tutorial translations
    tut_ctx = contexts_by_name.get('Tutorial')
    if tut_ctx is not None:
        for msg in tut_ctx.findall('message'):
            src_elem = msg.find('source')
            tr_elem = msg.find('translation')
            if src_elem is not None and src_elem.text and tr_elem is not None:
                src_text = src_elem.text.strip()
                # Check for match in TUTORIAL_TRANSLATIONS
                for key, val in TUTORIAL_TRANSLATIONS.items():
                    if key in src_text:
                        tr_elem.text = val
                        if 'type' in tr_elem.attrib:
                            del tr_elem.attrib['type']
                        break

    # 2. Add extra translations to contexts
    for ctx_name, kv in EXTRA_TRANSLATIONS.items():
        ctx = contexts_by_name.get(ctx_name)
        if ctx is None:
            ctx = ET.SubElement(root, 'context')
            name_elem = ET.SubElement(ctx, 'name')
            name_elem.text = ctx_name
            contexts_by_name[ctx_name] = ctx

        # Check existing messages
        existing_srcs = set()
        for msg in ctx.findall('message'):
            src = msg.find('source')
            if src is not None and src.text:
                existing_srcs.add(src.text.strip())
                if src.text.strip() in kv:
                    tr = msg.find('translation')
                    if tr is not None:
                        tr.text = kv[src.text.strip()]
                        if 'type' in tr.attrib:
                            del tr.attrib['type']

        for src, tr in kv.items():
            if src not in existing_srcs:
                msg_elem = ET.SubElement(ctx, 'message')
                s_elem = ET.SubElement(msg_elem, 'source')
                s_elem.text = src
                t_elem = ET.SubElement(msg_elem, 'translation')
                t_elem.text = tr

    # Write out ts file
    tree.write(ts_file, encoding='utf-8', xml_declaration=True)
    print("Updated TS file written.")

    # Compile QM
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    from compile_translations import ts_to_qm
    count = ts_to_qm(ts_file, 'translation/veusz_ja.qm')
    print(f"Compiled {count} translations into translation/veusz_ja.qm")

if __name__ == '__main__':
    main()
