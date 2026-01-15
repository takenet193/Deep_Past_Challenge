---
type: task
id: task-20260114141258
title: "Disaster Tweets: BERTモデルの実験（ディスカッションから取得）"
author: takeikumi
status: active
priority: high
project: kaggle_disaster_tweets_baseline_improvement
mode: experiment
context:
  - project_kaggle_disaster_tweets_baseline_improvement
  - project_kaggle_disaster_tweets
dependencies:
  - exp20260106030720_report
related_notes:
  - project_kaggle_disaster_tweets_baseline_improvement
created: 2026-01-14
updated: 2026-01-14
tags: [kaggle, kaggle_disaster_tweets, improvement, bert, deep-learning, experiment, discussion]
---

# タスク: Disaster Tweets - BERTモデルの実験（ディスカッションから取得）

#kaggle_disaster_tweets

## 目的

Kaggleディスカッションから取得した`bert.ipynb`ノートブックを分析し、このプロジェクトのexperiments形式に変換して実験を実施する。

**期待効果**: 深層学習モデル（BERT）による性能向上を期待。CV F1 0.80-0.85程度、Public LB 0.85-0.87程度を目標。

## 背景・根拠

### 取得経緯
- Kaggleディスカッションから取得したノートブック（`bert.ipynb`）
- ベースライン改善プロジェクトの一環として、深層学習モデルの実装を検討

### ベースライン結果（参考）
- **ベースライン（exp20260106030720）**: CV F1=0.7425、Public LB=0.80079（TF-IDF + LogisticRegression）
- **改善実験1（exp20260112174906）**: CV F1=0.7416、Public LB=0.77965（keyword特徴量追加）
- **改善実験2（exp20260112201310）**: CV F1=0.7469、Public LB=0.80202（C値チューニング）

### 深層学習モデルの位置づけ
- プロジェクトの改善案（中期〜長期目標）として位置づけられている
- 期待効果: CV F1 0.85-0.90程度、Public LB 0.88-0.92程度

## bert.ipynb 分析レポート

### 実装概要

#### 1. モデルアーキテクチャ
- **ベースモデル**: BERT（bert-base-uncased）
- **分類ヘッド**: Linear(768 → 2) + Dropout(0.5)
- **実装**: PyTorch + transformersライブラリ

#### 2. データ処理
- **データセットクラス**: `MyDataset`
  - train/testデータの読み込み
  - AutoTokenizer（bert-base-uncased）を使用
  - トークナイズ: max_length=128, padding='max_length', truncation=True
  - 出力: (input_ids, attention_mask, token_type_ids), label

#### 3. ハイパーパラメータ
```python
batch_size = 256
shuffle = True
num_workers = 0
lr = 2e-5
weight_decay = 1e-2
epochs = 25
max_length = 128
dropout = 0.5
```

#### 4. 学習設定
- **オプティマイザ**: AdamW（lr=2e-5, weight_decay=1e-2）
- **損失関数**: CrossEntropyLoss
- **デバイス**: CUDA（利用可能な場合）、DataParallel対応
- **学習ループ**: 25エポック、tqdmで進捗表示

#### 5. 学習結果（ノートブック実行結果より）
- 25エポック完了
- 最終エポックのloss: 0.0036（エポック25）
- 学習中のloss推移:
  - エポック1: 0.353
  - エポック5: 0.192
  - エポック10: 0.045
  - エポック15: 0.011
  - エポック20: 0.010
  - エポック25: 0.004

#### 6. 推論・提出ファイル作成
- testデータセットの作成
- モデルを評価モードに設定
- バッチ推論を実行
- submission.csvの作成（id, target列）

### コードの特徴

#### 良い点
- ✅ 標準的なBERT分類タスクの実装
- ✅ DataParallelによるマルチGPU対応
- ✅ 適切なドロップアウト（0.5）の使用
- ✅ AdamWオプティマイザの使用（重み減衰あり）

#### 改善が必要な点
- ⚠️ CV評価が実装されていない（trainデータ全体で学習のみ）
- ⚠️ バリデーションセットでの性能評価がない
- ⚠️ 学習済みモデルの保存処理が明確でない
- ⚠️ データパスがハードコードされている（`/data/koushurui/Data/kaggle/disaster-tweets`）
- ⚠️ モデルパスがハードコードされている（`/data/koushurui/Code/LLMS/google-bert/bert-base-uncased`）
- ⚠️ 提出ファイルの保存パスがハードコードされている（`/home/koushurui/Documents/Code/Kaggle/disaster-tweets/submission.csv`）
- ⚠️ `__getitem__`メソッドの戻り値に問題（test時：`(input_ids, attention_mask, token_type_ids), ` - 空のタプルが返される）

### 実装の本質的な処理の流れ

1. **データ準備**
   - train.csv, test.csvの読み込み
   - BERTトークナイザーの初期化
   - データセットクラスの作成

2. **モデル定義**
   - BERTモデルの読み込み（bert-base-uncased）
   - 分類ヘッドの定義（Linear + Dropout）
   - デバイスへの移動

3. **学習**
   - DataLoaderの作成（batch_size=256）
   - 25エポックの学習ループ
   - AdamWオプティマイザで最適化
   - CrossEntropyLossで損失計算

4. **推論**
   - testデータセットの作成
   - モデルを評価モードに設定
   - バッチ推論を実行
   - 予測結果をsubmission.csvに保存

## 成果物（このタスクの完了条件）

- `bert.ipynb`の分析レポートがこのタスクノートに記録されている ✅
- プロジェクト形式（experiments/）に変換した実験コードが作成されている
  - `experiments/exp[timestamp]_bert/exp[timestamp]_config.yaml`
  - `experiments/exp[timestamp]_bert/exp[timestamp]_train.py`
  - `experiments/exp[timestamp]_bert/exp[timestamp]_predict.py`
- CV評価が実装され、ベースラインとの比較が可能になっている
- `submission.csv`をKaggleに提出し、Public LBの結果を取得している
- 実験結果（CVスコア、Public LB）と学びを実験レポートに記録している
- プロジェクトノート（`project_kaggle_disaster_tweets_baseline_improvement.md`）に実験ログを追加している

## プロジェクト形式への変換計画

### 基本方針

**本質的な処理の流れを変えず、精度も変えず、このプロジェクトの形式に直す**

- BERTモデル、分類ヘッド、学習設定はそのまま維持
- データ処理の流れは維持（トークナイズ、バッチ処理など）
- ハイパーパラメータは基本的に維持（必要に応じてconfig.yamlで調整可能にする）

### 1. ディレクトリ構造

```
experiments/exp[timestamp]_bert/
├── exp[timestamp]_config.yaml       # 設定ファイル
├── exp[timestamp]_train.py          # 学習スクリプト
└── exp[timestamp]_predict.py        # 推論スクリプト

results/exp[timestamp]_bert/
├── exp[timestamp]_report.md         # 実験レポート
├── exp[timestamp]_metrics.json      # 評価指標
├── exp[timestamp]_cv_results.json   # CV結果
├── exp[timestamp]_submission.csv    # 提出ファイル
└── exp[timestamp]_model.pth         # モデルファイル（PyTorch形式）
```

### 2. config.yamlの設計

#### 実験メタデータ
- `experiment.id`: 実験ID（タイムスタンプ）
- `experiment.name`: "bert"
- `experiment.description`: "BERT (bert-base-uncased) + Linear + Dropout"
- `experiment.parent_experiment`: `exp20260106030720`（ベースライン）

#### データ設定
- `data.train_path`: `data/raw/train.csv`
- `data.test_path`: `data/raw/test.csv`
- `data.model_path`: `bert-base-uncased`（Hugging Faceモデル名、またはローカルパス）

#### 前処理設定
- `preprocessing.max_length`: 128
- `preprocessing.padding`: "max_length"
- `preprocessing.truncation`: true

#### モデル設定
- `model.type`: "BERT"
- `model.base_model`: "bert-base-uncased"
- `model.dropout`: 0.5
- `model.num_classes`: 2

#### 学習設定
- `training.batch_size`: 256
- `training.epochs`: 25
- `training.learning_rate`: 2e-5
- `training.weight_decay`: 1e-2
- `training.optimizer`: "AdamW"
- `training.loss`: "CrossEntropyLoss"
- `training.shuffle`: true
- `training.num_workers`: 0

#### 検証設定
- `validation.method`: "stratified_kfold"
- `validation.n_folds`: 5
- `validation.shuffle`: true
- `validation.random_state`: 42

#### 出力設定
- `output.results_dir`: "./results/"
- `output.save_model`: true
- `output.save_predictions`: true

#### シード設定
- `seed`: 42

### 3. train.pyの実装方針

#### 3.1 コード構造
```python
# 1. インポート
# 2. パス設定（REPO_ROOT基準）
# 3. config.yaml読み込み
# 4. 乱数シード設定
# 5. デバイス設定
# 6. データ読み込み
# 7. データセット・DataLoader作成
# 8. モデル定義
# 9. 損失関数・オプティマイザ定義
# 10. CV評価（StratifiedKFold）
# 11. 全データで学習（最終モデル）
# 12. 結果保存（metrics.json, cv_results.json, model.pth）
```

#### 3.2 変更点

**維持する要素（本質的な処理）:**
- ✅ BERTモデルのアーキテクチャ（BertModel + Linear + Dropout）
- ✅ トークナイズ処理（max_length=128, padding, truncation）
- ✅ 学習ループの構造（エポック、バッチ処理）
- ✅ AdamWオプティマイザ（lr=2e-5, weight_decay=1e-2）
- ✅ CrossEntropyLoss
- ✅ DataParallel対応
- ✅ バッチサイズ（256）、エポック数（25）

**変更・追加する要素:**
- 🔄 データパス: ハードコード → config.yamlから読み込み（REPO_ROOT基準）
- ➕ CV評価の実装: StratifiedKFold（5 folds）でCV評価を追加
- ➕ モデル保存: PyTorch形式（.pth）で保存
- ➕ メトリクス保存: metrics.json, cv_results.jsonに保存
- 🔄 データセットクラス: `__getitem__`の戻り値を修正（test時も適切に処理）
- ➕ ログ出力: 進捗表示を改善（tqdm使用）

#### 3.3 CV評価の実装

```python
# StratifiedKFoldでCV評価
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train_texts, y_train)):
    # フォールドごとのデータ分割
    train_dataset = MyDataset(...)
    val_dataset = MyDataset(...)
    
    # モデル初期化
    model = BertClassifer(...)
    
    # 学習（trainデータのみ）
    train_epochs(...)
    
    # 評価（valデータ）
    val_score = evaluate(...)
    cv_scores.append(val_score)

# CV結果を保存
cv_mean = np.mean(cv_scores)
cv_std = np.std(cv_scores)
```

**注意点:**
- CV評価では、各フォールドでモデルを再初期化する必要がある
- BERTモデルの学習は時間がかかるため、CV評価は計算コストが高い
- 必要に応じて、CV評価をスキップするオプションも検討

#### 3.4 モデル保存

```python
# モデル、トークナイザー、設定を保存
torch.save({
    'model_state_dict': model.state_dict(),
    'model_config': {
        'base_model': config['model']['base_model'],
        'dropout': config['model']['dropout'],
        'num_classes': config['model']['num_classes']
    },
    'tokenizer': tokenizer,  # またはトークナイザーの設定
    'config': config
}, model_path)
```

### 4. predict.pyの実装方針

#### 4.1 コード構造
```python
# 1. インポート
# 2. パス設定
# 3. config.yaml読み込み
# 4. デバイス設定
# 5. モデル読み込み
# 6. testデータ読み込み
# 7. データセット・DataLoader作成
# 8. 推論実行
# 9. submission.csv作成・保存
```

#### 4.2 変更点

**維持する要素:**
- ✅ 推論の流れ（データ読み込み → トークナイズ → バッチ推論 → 予測）
- ✅ 評価モード（`model.eval()`）
- ✅ `torch.no_grad()`コンテキスト

**変更・追加する要素:**
- 🔄 モデル読み込み: 保存したモデルから読み込み
- 🔄 データパス: config.yamlから読み込み
- 🔄 出力パス: results/ディレクトリに保存
- ➕ 予測結果の検証: 予測値の範囲確認（0 or 1）

### 5. 実装時の注意点

#### 5.1 データパスの処理
- ハードコードされたパスを`REPO_ROOT`基準の相対パスに変更
- config.yamlから読み込む

#### 5.2 モデルパスの処理
- `bert-base-uncased`はHugging Faceモデル名として指定
- ローカルパスが必要な場合は、環境変数またはconfig.yamlで指定

#### 5.3 CV評価の計算コスト
- BERTモデルの学習は時間がかかる（25エポック × 5 folds = 125エポック分の学習）
- 必要に応じて、CV評価をスキップするオプションを追加
- または、CV評価を簡略化（3 folds、エポック数削減など）

#### 5.4 メモリ使用量
- バッチサイズ256は大きい可能性がある
- GPUメモリが不足する場合は、バッチサイズを調整（128, 64など）

#### 5.5 再現性
- 乱数シードを統一（PyTorch、NumPy、Python標準ライブラリ）
- DataLoaderの`worker_init_fn`でシードを設定

#### 5.6 データセットクラスの修正
- `__getitem__`メソッドの戻り値を修正（test時も適切に処理）
- train時: `(input_ids, attention_mask, token_type_ids), label`
- test時: `(input_ids, attention_mask, token_type_ids), -1`（またはダミーラベル）

### 6. 実装チェックリスト

#### 6.1 実験準備
- [ ] 実験IDをタイムスタンプ形式で生成
- [ ] `experiments/exp[timestamp]_bert/`ディレクトリを作成
- [ ] `results/exp[timestamp]_bert/`ディレクトリを作成

#### 6.2 config.yaml作成
- [ ] 実験メタデータを設定
- [ ] データパスを設定
- [ ] モデル設定を記述
- [ ] 学習設定を記述
- [ ] 検証設定を記述

#### 6.3 train.py実装
- [ ] データ読み込み（config.yamlからパス取得）
- [ ] データセットクラス実装（`__getitem__`修正）
- [ ] モデル定義（BertClassifer）
- [ ] CV評価実装（StratifiedKFold）
- [ ] 全データで学習
- [ ] 結果保存（metrics.json, cv_results.json, model.pth）

#### 6.4 predict.py実装
- [ ] モデル読み込み
- [ ] testデータ読み込み
- [ ] 推論実行
- [ ] submission.csv作成・保存

#### 6.5 テスト・検証
- [ ] train.pyが正常に実行できることを確認
- [ ] CV評価が正常に動作することを確認
- [ ] predict.pyが正常に実行できることを確認
- [ ] 予測結果が適切な形式であることを確認

#### 6.6 提出・記録
- [ ] Kaggleにsubmission.csvを提出
- [ ] Public LBスコアを取得
- [ ] 実験レポート作成
- [ ] プロジェクトノートに実験ログを追加

## 期待される結果

### ベースラインとの比較
- **ベースライン**: CV F1=0.7425、Public LB=0.80079（TF-IDF + LogisticRegression）
- **期待値**: CV F1 0.80-0.85程度、Public LB 0.85-0.87程度
- **目標**: 深層学習モデルによる性能向上

### 成功の判断基準
- CV F1がベースライン（0.7425）より大幅に向上している
- Public LBがベースライン（0.80079）より向上している
- 過学習が適切にコントロールされている（Dropout使用）

## 実行環境・方法の決定

### 実行環境
- **環境**: Google Colab（GPU: T4）
- **理由**: ローカルMacBook ProにはGPUがなく、CPUのみでの実行は非現実的

### データ読み込み方法
- **方法**: Google Driveから読み込む
- **データパス**: `/content/drive/MyDrive/kaggle_disaster_tweet/`
- **データファイル**: `train.csv`, `test.csv`
- **フォルダ名**: `kaggle_disaster_tweet`（実際のアップロード先）

### 実行方針（第1段階）
- **CV評価**: 最初は**スキップ**（動作確認・学習時間短縮のため）
- **実行時間の目安**: 約1-2時間（25エポック）
- **次のステップ**: 動作確認後、必要に応じてCV評価を追加

### 注意点
- Colabの無料版制限: セッション最大12時間、90分アイドル後にタイムアウト
- モデル・結果の保存: Google Driveに保存することを推奨

## 参考資料

- プロジェクトノート: [[project_kaggle_disaster_tweets_baseline_improvement|project: kaggle_disaster_tweets_baseline_improvement]]
- ベースライン実験レポート: [[exp20260106030720_report|exp20260106030720_report]]
- 親プロジェクト: [[project_kaggle_disaster_tweets|project: kaggle_disaster_tweets]]
- bert.ipynb: `bert.ipynb`（プロジェクトルート）

<!-- AUTO:project:start -->
- [[project_kaggle_disaster_tweets_baseline_improvement|project: kaggle_disaster_tweets_baseline_improvement]]
<!-- AUTO:project:end -->

