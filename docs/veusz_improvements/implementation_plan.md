# 実装計画: Veusz 機能改善と日本語ローカライズ

## 概要
本プロジェクトでは以下の3つの改善を段階的に実施します。
各機能はGitの独立したブランチで開発し、個別のプルリクエスト（PR）として提出可能な構成とします。

1. **日本語ローカライズ拡充とQM生成** (`feature/japanese-translation`)
2. **グラフの拡張メタファイル (EMF) クリップボードコピー** (`feature/clipboard-emf-copy`)
3. **ラベル文字修飾UIの強化 (LabPlot風)** (`feature/label-formatting-toolbar`)

---

## 1. 日本語ローカライズ拡充 (Phase 1)

### 背景・現状
- `translation/veusz-strings_ja.ts` は全2,323件中、720件のみ翻訳済み、1,603件が未翻訳 (`type="unfinished"`)。
- 既存の訳文にも不自然な機械翻訳調が散見される。
- 環境に `lrelease` がなくても動作するコンパイル手段が必要。

### 方針・用語ルール
- **アカデミック・科学技術標準の用語選定**:
  - 無理な日本語直訳は避け、専門分野で定着しているカタカナ語や英語表記を採用。
  - 例:
    - Colormap -> カラーマップ (色見本 ではなく)
    - Spline -> スプライン
    - Fit -> フィッティング
    - Plugin -> プラグイン
    - Scatter -> 散布図 / スキャッター
    - Error bar -> エラーバー
    - DPI, SVG, PDF, CSV, ASCII -> そのまま英字
    - Major/Minor ticks -> 主目盛り / 補助目盛り

### 実装手順
1. **未翻訳テキスト抽出**:
   - Pythonスクリプトを用いて `veusz-strings_ja.ts` から未翻訳メッセージおよび文脈（context, source text）を抽出。
2. **翻訳辞書の構築と適用**:
   - 科学グラフソフトの文脈に沿った高品質な対訳を作成し、`.ts` ファイルを更新。
3. **QMバイナリコンパイラ (`compile_translations.py`) 作成**:
   - Python標準またはPyQtを活用し、`.ts` XMLから Qt の `.qm` バイナリを直接出力する軽量スクリプトを作成。
4. **検証**:
   - `QTranslator` で生成された `.qm` をロードし、キーと翻訳文字列が正しく展開されるかを自動テスト。

---

## 2. クリップボードへのEMFコピー (Phase 2)

### 実装手順
1. **ブランチ作成**: `master` から `feature/clipboard-emf-copy` を分岐。
2. **EMF出力連携**:
   - 既存の `document.exportEMF()` または `pyemf3` 出力をバッファ（メモリ）上で生成。
3. **WindowsクリップボードAPI連携**:
   - `ctypes` または `win32clipboard` を利用して `CF_ENHMETAFILE` 形式でクリップボードに格納する関数を作成。
4. **UI導線の追加**:
   - グラフプレビュー領域のコンテキストメニューに「クリップボードに保存 (EMF)」を追加。
   - ショートカットキー `Ctrl+C`（または `Ctrl+Shift+C`）にアクションを割り当て。
5. **検証**:
   - PowerPoint / Word / Excel に直接ペーストし、ベクター形式の高品質な図として挿入できることを確認。

---

## 3. ラベル文字修飾UI強化 (Phase 3)

### 実装手順
1. **ブランチ作成**: `master` から `feature/label-formatting-toolbar` を分岐。
2. **UIウィジェット設計**:
   - LabPlotのテキスト編集UIを参考に、プロパティパネルのラベル入力欄上部にミニボタン（Bold, Italic, Sup, Sub, Symbol）を配置。
3. **テキスト挿入ロジック**:
   - 選択されたテキストを Veusz の記法（`\textbf{...}`, `\italic{...}`, `^{...}`, `_{...}`）でラップ。
4. **検証**:
   - グラフ上のテキストレンダラーで正しく装飾が反映されることを確認。
