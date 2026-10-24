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

## 2. クリップボードへの拡張メタファイル(EMF)コピー (ブランチ: feature/clipboard-emf-copy)
- [ ] WindowsクリップボードへのEMF形式 (CF_ENHMETAFILE) 格納モジュールの実装
- [ ] グラフプレビュー画面での右クリックメニュー「クリップボードに保存」項目の追加
- [ ] ショートカットキー (Ctrl+C / Ctrl+Shift+C) の割り当てと競合チェック
- [ ] Word / PowerPoint / Excel 等への貼り付けテスト

## 3. ラベルの文字修飾UI強化 (ブランチ: feature/label-formatting-toolbar)
- [ ] LabPlot等のテキスト修飾UIの調査・設計
- [ ] SettingEdit / テキスト入力欄向け修飾ミニツールバーの実装
  - 太字 (B: \textbf{}), 斜体 (I: \italic{}), 上付き (x²: ^{}), 下付き (x₂: _{}), ギリシャ文字パレット
- [ ] 選択テキストの一括タグ囲み・挿入アシスト動作の検証
