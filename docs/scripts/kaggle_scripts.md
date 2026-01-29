# Kaggle提出スクリプト

このドキュメントでは、Kaggle提出用のスクリプト（`scripts/kaggle/`）の目的、使い方、入出力を説明します。

## 1. `scripts/kaggle/check_kaggle_auth.sh`

### 目的

Kaggle API認証を確認するスクリプト。  
`~/.kaggle/kaggle.json` の存在と権限、API認証の動作を確認します。

### 使い方

```bash
bash scripts/kaggle/check_kaggle_auth.sh
```

または

```bash
chmod +x scripts/kaggle/check_kaggle_auth.sh
./scripts/kaggle/check_kaggle_auth.sh
```

### 動作

1. `~/.kaggle/kaggle.json` の存在確認
2. ファイル権限の確認（推奨: `600`）
3. API認証テスト（`kaggle competitions list`）
4. 利用可能なコンペティションの一覧表示（最初の5件）

### 実行結果例

```
==========================================
Kaggle API認証確認
==========================================

✅ kaggle.jsonが見つかりました
-rw-------  1 user  staff   123 Jan 14 12:00 /Users/user/.kaggle/kaggle.json

✅ ファイル権限は正しく設定されています (600)

API認証をテストします...
✅ 認証成功！Kaggle APIが使用できます

利用可能なコンペティション（最初の5件）:
```
ref                                                      deadline  category  reward  teamCount  userHasEntered
------------------------------------------------------  ---------  --------  ------  ---------  --------------
nlp-getting-started                                     2026-01-31  Getting   $0      1234       True
...
```

==========================================
```

### エラー時の対処

- **`kaggle.json` が見つからない場合**:
  1. https://www.kaggle.com/ → Account → API → Create New API Token
  2. ダウンロードした `kaggle.json` を `~/.kaggle/` に配置
  3. `chmod 600 ~/.kaggle/kaggle.json` を実行

- **認証に失敗する場合**:
  - `kaggle.json` の内容を確認
  - ファイル権限が `600` になっているか確認

## 2. `scripts/kaggle/submit_to_kaggle.sh`

### 目的

Kaggleコンペティションに提出ファイルを送信するスクリプト。  
実験結果（`submission.csv`）をKaggle APIを使用して提出します。

### 使い方

```bash
# スクリプトを編集して実験IDと提出ファイルを設定
vim scripts/kaggle/submit_to_kaggle.sh

# 実行
bash scripts/kaggle/submit_to_kaggle.sh
```

### 設定項目

スクリプト内の以下の変数を編集してください：

```bash
EXP_ID="exp20260112174906"
COMPETITION="nlp-getting-started"
SUBMISSION_FILE="results/${EXP_ID}_keyword_tfidf_lr/${EXP_ID}_submission.csv"
MESSAGE="${EXP_ID}: keyword feature + TF-IDF + LogisticRegression"
```

### 動作

1. 提出ファイルの存在確認
2. Kaggle API認証確認
3. 提出実行（`kaggle competitions submit`）
4. 結果の表示

### 実行結果例

```
==========================================
Kaggle提出スクリプト
==========================================
実験ID: exp20260112174906
コンペティション: nlp-getting-started
提出ファイル: results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_submission.csv
メッセージ: exp20260112174906: keyword feature + TF-IDF + LogisticRegression
==========================================

提出ファイルを確認しました:
-rw-r--r--  1 user  staff  98K Jan 14 12:00 results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_submission.csv

Kaggle API認証を確認中...
認証OK

提出を実行します...
Successfully submitted to nlp-getting-started

==========================================
提出が完了しました！
Kaggleのコンペティションページで結果を確認してください
https://www.kaggle.com/competitions/nlp-getting-started/submissions
==========================================
```

### エラーハンドリング

- 提出ファイルが見つからない場合: エラーメッセージを表示して終了
- API認証に失敗した場合: エラーメッセージを表示して終了
- 提出に失敗した場合: エラーメッセージを表示して終了

## 3. `scripts/kaggle/submit_with_token.sh`

### 目的

Kaggle APIトークンを直接指定して提出するスクリプト。  
環境変数や設定ファイルを使用せず、コマンドライン引数でトークンを指定します。

### 使い方

```bash
bash scripts/kaggle/submit_with_token.sh \
  <コンペティション名> \
  <提出ファイル> \
  <メッセージ> \
  <username> \
  <key>
```

**例**:
```bash
bash scripts/kaggle/submit_with_token.sh \
  nlp-getting-started \
  results/exp20260112174906_keyword_tfidf_lr/exp20260112174906_submission.csv \
  "exp20260112174906: keyword feature" \
  your_username \
  your_api_key
```

### 注意事項

- APIキーをコマンドライン引数で指定するため、シェル履歴に残る可能性があります
- 通常は `submit_to_kaggle.sh` を使用することを推奨します

## 関連ドキュメント

- [スクリプトガイド](../scripts_guide.md) - スクリプトの概要
- [ワークフロー管理スクリプト](./workflow_scripts.md) - ワークフロー管理用スクリプト
- [スクリプト実行のワークフロー](./scripts_workflow.md) - 典型的な使用フロー
- [トラブルシューティング](./scripts_troubleshooting.md) - よくある問題と解決方法

