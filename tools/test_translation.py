import xml.etree.ElementTree as ET
from PyQt5.QtCore import QCoreApplication, QTranslator

# 1. Verify TS has 0 unfinished
tree = ET.parse('translation/veusz-strings_ja.ts')
root = tree.getroot()
unfinished = 0
total = 0
for msg in root.iter('message'):
    total += 1
    tr = msg.find('translation')
    if tr is not None:
        if tr.get('type') == 'unfinished' or not (tr.text and tr.text.strip()):
            unfinished += 1
    else:
        unfinished += 1

print(f"TS Verification: Total {total}, Unfinished: {unfinished}")
assert unfinished == 0, f"Expected 0 unfinished, got {unfinished}"

# 2. Verify QM load & translation
app = QCoreApplication([])
trans = QTranslator()
ok = trans.load('translation/veusz_ja.qm')
assert ok, "QM file failed to load"
app.installTranslator(trans)

test_cases = [
    ('AboutDialog', 'About Veusz', 'Veuszについて'),
    ('Axis', 'Zero extend', 'ゼロまで拡張'),
    ('BoxPlot', 'Whisker mode', 'ひげの計算モード'),
    ('Histo', 'Histogram of a dataset', 'データセットのヒストグラム'),
    ('PrefsDialog', 'Page background color', 'ページの背景色'),
    ('MainWindow', '&File', 'ファイル(&F)'),
]

for ctx, src, expected in test_cases:
    actual = app.translate(ctx, src)
    print(f"[{ctx}] '{src}' -> '{actual}'")
    assert actual == expected, f"Expected '{expected}', got '{actual}'"

print("ALL TESTS PASSED SUCCESSFULLY!")
