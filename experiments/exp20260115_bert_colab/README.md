# Experiment: exp20260115_bert_colab - BERT (Colab実行)

## 実行環境

- **実行場所**: Google Colab
- **GPU**: Tesla T4
- **実行日**: 2026-01-15

## 注意

この実験は**Colab上で実行**されたため、実際のコードファイル（train.py, predict.py）はローカルには存在しません。

- 実験コード: Colab上で実行（ノートブック形式）
- データ: Google Drive (`/content/drive/MyDrive/kaggle_disaster_tweet/`)
- 結果: Google Driveに保存 (`submission.csv`)

## 実験内容

- **モデル**: BERT (bert-base-uncased)
- **分類ヘッド**: Linear(768 → 2) + Dropout(0.5)
- **エポック数**: 25
- **バッチサイズ**: 64 (GPUメモリ制約により256から変更)
- **学習率**: 2e-5
- **重み減衰**: 1e-2
- **オプティマイザ**: AdamW
- **損失関数**: CrossEntropyLoss

## 学習結果

- **最終エポックの平均loss**: 0.015667
- **実行時間**: 約50分（25エポック）

## 評価結果

- **Public LB F1 Score**: **0.81060**
- **ベースラインとの比較**: 
  - ベースライン（exp20260106030720）: Public LB=0.80079
  - **向上**: +0.00981（約1.2%向上）
- **評価**: ベースライン（TF-IDF + LogisticRegression）を上回る性能を達成。深層学習モデル（BERT）の効果が確認できた。

## 参考資料

- **ベースノートブック**: `bert.ipynb`（このディレクトリ内、Kaggleディスカッションから取得したオリジナル）
- タスク: [[task_disaster_tweets_bert_discussion_20260114141258|Disaster Tweets: BERTモデルの実験（ディスカッションから取得）]]

