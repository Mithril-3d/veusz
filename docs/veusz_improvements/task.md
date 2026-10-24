# Veusz 改善タスクリスト

## 1. 日本語ローカライズ拡充 (ブランチ: feature/japanese-translation) - 【完了】
- [x] translation/veusz-strings_ja.ts の未翻訳項目 (1,603件) の抽出
- [x] 科学・グラフソフトウェアとして適切な用語（無理な直訳を避け、定着したカタカナ・英語表記を採用）による翻訳・校正
  - [x] 既存の不自然な日本語訳の見直し・用語統一
  - [x] 未翻訳項目（1,603件）の全件翻訳・解決（未翻訳 0件達成）
- [x] キーと日本語訳の対応カタログ (`docs/veusz_improvements/translation_catalog.md`) の作成
- [x] TSからQMバイナリを直接生成するビルドスクリプト (`tools/compile_translations.py`) の作成
- [x] QMファイル (`translation/veusz_ja.qm`) の生成と動作検証（QTranslator によるロードテスト成功）
- [x] 言語設定および日本語環境での自動検出・ロード実装 (`veusz/veusz_main.py`)

## 2. クリップボードへの拡張メタファイル(EMF)コピー (ブランチ: feature/clipboard-emf-copy) - 【完了】
- [x] WindowsクリップボードへのEMF形式 (CF_ENHMETAFILE) 格納モジュール (`veusz/utils/windows_clipboard.py`) の実装 (64bit API対応)
- [x] グラフプレビュー画面での右クリックメニュー「画像としてコピー」項目の追加 (`veusz/windows/plotwindow.py`)
- [x] ショートカットキー `Ctrl+Shift+C` の割り当てと競合回避 (`veusz/windows/treeeditwindow.py`)
- [x] ハイブリッドクリップボード対応 (EMF + PNG/SVG を同時に格納し、Office ではベクター画像、ペイント等ではビットマップ画像として貼り付け可能)
- [x] 単体テストおよび統合検証スクリプト (`tools/test_clipboard_emf.py`) による全件PASS確認

## 3. ラベルの文字修飾UI強化 (ブランチ: feature/label-formatting-toolbar) - 【完了】
- [x] LabPlot風テキスト修飾UIの調査・設計（ミニツールバー＋グリッド文字パレット）
- [x] SettingEdit / テキスト入力欄向け修飾ミニツールバー (`TextFormatToolbar`) の実装 (`veusz/setting/controls.py`)
  - 太字 (B: `\bold{}`), 斜体 (I: `\italic{}`), 下線 (U: `\underline{}`), 上付き (x²: `^{}`), 下付き (x₂: `_{}`), 分数 (a/b: `\frac{}{}`)
  - ギリシャ文字パレット (α▾: `GridPaletteMenu`) によるワンクリック挿入
  - 科学・数学記号パレット (±▾: `GridPaletteMenu`) によるワンクリック挿入
- [x] ポップアップ編集ダイアログ (`_EditBox`) のツールバー統合・Esc/Enterショートカット対応
- [x] インライン入力欄 (`String.edit`) での `Ctrl+B`, `Ctrl+I`, `Ctrl+U` 直接タグ囲みショートカット対応
- [x] 単体テストおよび統合検証スクリプト (`tools/test_formatting_toolbar.py`) による全件PASS確認
