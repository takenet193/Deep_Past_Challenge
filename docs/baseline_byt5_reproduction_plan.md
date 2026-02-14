# ByT5 + Optuna + Chunked Beam Search 再現計画

## 目的

harukiharada 氏の Kaggle ノートブックをローカル環境で再現し、ベースラインの方針決定に活用する。

- **参考ノートブック**: https://www.kaggle.com/code/harukiharada/byt5-optuna-tuning-chunked-beam-search
- **スコア**: 35.1（Bronze）
- **リファレンス**: `knowledge/zettelkasten/references/harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000.md`

---

## フェーズ 1: 環境セットアップ

### 1.1 依存パッケージの追加

`requirements.txt` に以下を追加:

```
# 深層学習（ByT5 用）
torch>=2.0.0
transformers>=4.30.0
tokenizers>=0.13.0
accelerate>=0.20.0

# ハイパーパラメータチューニング
optuna>=3.0.0

# 評価
sacrebleu>=2.3.0

# 既存
sentencepiece>=0.1.99  # ByT5 の一部バージョンで使用
```

### 1.2 Kaggle CLI のセットアップ（推奨）

ノートブック・データセット取得のため:

```bash
pip install kaggle
# ~/.kaggle/kaggle.json に API キーを配置
```

### 1.3 ノートブック取得

```bash
# ノートブックを pull
kaggle kernels pull harukiharada/byt5-optuna-tuning-chunked-beam-search -p scripts/kaggle_notebooks/

# または .ipynb を手動でダウンロードし、scripts/kaggle_notebooks/ に配置
```

---

## フェーズ 2: データ・モデル取得

### 2.1 コンペデータ

- 既に `data/raw/` に配置済みを想定
- 未取得の場合: `kaggle competitions download -c deep-past-initiative-machine-translation`

### 2.2 ByT5 モデル

**オプション A**: Kaggle データセット（推奨）

```bash
kaggle datasets download -d pascalledesma/deep-past-byt5-models -p data/models/
```

**オプション B**: HuggingFace からベースモデル

- `google/byt5-base` を transformers で `from_pretrained` により自動ダウンロード

---

## フェーズ 3: 前処理の統一

既存の前処理ガイド（`deep_past_preprocessing_20260211130000`）に従う:

1. **必須**: Ḫ/ḫ → H/h
2. **必須**: 書記記号除去（!, ?, /, : 等）
3. **必須**: train の文単位分割（`Sentences_Oare_FirstWord_LinNum.csv` 利用）
4. **推奨**: determinatives の統一、下付き数字 ASCII 化

harukiharada ノートブック内の前処理と差分があれば、Eval で比較検証する。

---

## フェーズ 4: 再現実行

### 4.1 軽量版（ローカル検証）

- データをサブセット（例: 100 件）に絞り、推論パイプラインのみ実行
- Optuna はトライアル数最小（例: 2）で動作確認

### 4.2 フル再現

- 全データ・フル Optuna で Kaggle 環境と同等の条件で実行
- ローカル GPU がなければ Colab / Kaggle Notebook を利用

---

## フェーズ 5: 方針の決定

再現結果を踏まえ、以下を検討:

1. **前処理**: harukiharada の前処理 vs 既存ガイドの差分と効果
2. **Chunked Beam Search**: チャンクサイズ・オーバーラップの最適値
3. **Optuna で探索するパラメータ**: beam_size, length_penalty, max_length 等
4. **アンサンブル**: 単一モデル vs 複数モデル（AnthonyTherrien 由来のアンサンブル活用可否）

---

## フォルダ構成（案）

```
scripts/
  kaggle_notebooks/     # 取得した Kaggle ノートブック
  byt5_reproduction/    # 再現用スクリプト（変換後）
data/
  raw/                  # コンペデータ
  processed/            # 前処理済み（文単位分割等）
  models/               # ByT5 モデル（Kaggle Dataset から）
```

---

## 次のアクション

- [ ] `requirements.txt` に ByT5 / Optuna / sacrebleu を追加
- [ ] Kaggle CLI でノートブックを取得
- [ ] ノートブックを .py に変換し、ローカル実行可能な形に整理
- [ ] 軽量版で推論パイプラインの動作確認
- [ ] リファレンスノートに具体的なパラメータ・実装メモを追記
