---
type: memo
status: inbox
author: takeikumi
created: 2026-01-15
updated: 2026-01-15
tags: [experiment, workflow, external-gpu, api, colab, kaggle]
links:
  - task_disaster_tweets_bert_discussion_20260114141258
---

# 外部GPU環境での実験実行フロー設計

## 学び / 気づき

- BERTモデルのような計算時間がかかるモデルを実行する場合、ローカル環境ではGPUが不足するため、外部GPU環境（Google Colab、Kaggle Notebooksなど）の利用が必須
- 現在の実験フロー（`experiments/`、`results/`ディレクトリ構造、`train.py`、`predict.py`）は**ローカル実行前提**のため、外部GPU環境での実行に対応する必要がある
- **実際の運用では、多くの場合1つの環境（ColabまたはKaggle）に絞ることが多い**。チーム開発では特に標準化が重要
- **実装方針**: インターフェースを抽象化（統一インターフェースを定義）した上で、まずはKaggleだけ実装する。将来的な拡張を見越した設計にしておく
- 複数の外部GPU環境に対応するには、実行環境を抽象化した統一インターフェースが有効

## 事実 / 観察

### 現状の問題点

- 実験フローがローカル実行前提（`REPO_ROOT`基準のパス、ローカルファイルシステム構造）
- 外部環境（Colab、Kaggle）ではファイルパスが異なる
- 結果をローカルに直接保存できない
- 複数の外部GPU環境（Colab、Kaggleなど）への対応が必要

### 外部GPU環境のAPI対応状況

1. **Kaggle API** ✅
   - 公式APIが存在
   - ノートブックの実行、結果の取得が可能
   - `kaggle kernels push`、`kaggle kernels pull`など

2. **Google Colab API** ⚠️
   - 公式APIは存在しない
   - Google Drive API経由での連携は可能（制約あり）
   - 実行は手動または半自動化

3. **その他の環境**
   - GCP Vertex AI Workbench: APIあり
   - AWS SageMaker: APIあり
   - Paperspace Gradient: APIあり

### 設計案

**アプローチ: 実行環境を抽象化した統一インターフェース**

```python
# 実行環境の抽象化
class ExecutionBackend:
    """外部GPU実行環境の統一インターフェース"""
    
    def submit_notebook(self, notebook_path, config):
        """ノートブックを実行環境に送信"""
        pass
    
    def check_status(self, execution_id):
        """実行状態を確認"""
        pass
    
    def download_results(self, execution_id, output_dir):
        """結果をダウンロード"""
        pass

class KaggleBackend(ExecutionBackend):
    """Kaggle APIを使用"""
    pass

class ColabBackend(ExecutionBackend):
    """Colab用（制約あり）"""
    pass
```

**推奨される実装方針**

1. **インターフェースの定義（抽象化）**: まず、共通のインターフェース（`ExecutionBackend`）を定義し、必要なメソッドを明確にする
2. **Kaggle実装（優先）**: インターフェースを実装するクラスとして、`KaggleBackend`のみを実装。動作する実装を完成させる
3. **使用**: インターフェース経由でKaggleBackendを使用。環境が変わっても、使用側のコードは変更不要
4. **将来の拡張（必要に応じて）**: 他の環境（Colab、GCP Vertex AI、AWS SageMakerなど）を追加する場合も、同じインターフェースを実装するだけ

**この方針のメリット**:
- 設計が明確（インターフェースで「何が必要か」が明確）
- 拡張しやすい（新しい環境を追加するときに、インターフェースに沿って実装すればよい）
- 実装がシンプル（まずはKaggleだけ実装すれば動作する）
- チーム開発に適している（1つの環境に標準化しながら、将来の拡張も考慮）

**実行フロー案**

```
1. ローカルで実験コードを作成
   ↓
2. 実行環境を選択（Kaggle/Colab）
   ↓
3. スクリプト/ノートブックを外部環境に送信
   ↓
4. 外部環境で実行（API経由または手動）
   ↓
5. 結果をローカルにダウンロード
   ↓
6. results/ディレクトリに統合
```

**ディレクトリ構造案**

```
scripts/
├── execution/
│   ├── backend.py          # 実行環境の抽象化
│   ├── kaggle_backend.py   # Kaggle API実装
│   ├── colab_backend.py    # Colab用（制約あり）
│   └── executor.py         # 統一実行インターフェース

experiments/
└── exp[timestamp]_bert/
    ├── exp[timestamp]_config.yaml
    ├── exp[timestamp]_train.py          # ローカル実行用（関数化）
    ├── exp[timestamp]_predict.py        # ローカル実行用（関数化）
    └── exp[timestamp]_notebook.ipynb    # 外部環境用ノートブック
```

**train.pyとnotebook.ipynbの関係: 関数分離アプローチ**

Kaggle APIは`.py`ファイルを直接実行できないため、ノートブック（`.ipynb`）が必要。しかし、コードの重複を避けるために**関数分離アプローチ**を採用:

1. **train.pyを関数化**: 環境に依存しないロジック（データ処理、学習など）を関数として実装
   - `load_config()`, `load_data()`, `preprocess_data()`, `train_model()`, `save_results()`など
   - メイン関数`main(config_path, data_root, results_dir, exp_id)`で全体の流れをまとめる
   - パスなどの環境依存部分を引数として受け取る

2. **ローカル実行**: `if __name__ == "__main__"`でローカル環境のパスを設定して実行

3. **ノートブックでの実行**: ノートブックから関数をインポートし、Kaggle環境のパスを設定して実行
   ```python
   from train import main
   main(config_path_kaggle, data_root_kaggle, results_dir_kaggle, exp_id)
   ```

**このアプローチのメリット**:
- コードの重複が最小限（ロジックは1箇所）
- 環境差をパス設定だけで分離
- メンテナンス性が高い（ロジック変更は1箇所のみ）
- テストしやすい（各関数を個別にテスト可能）

## 次に試すこと

- Kaggle APIの詳細調査
- 実行環境抽象化インターフェースの設計詳細化
- 実装計画の立案
- プロトタイプの作成

## 参考資料

- Kaggle API Documentation: https://github.com/Kaggle/kaggle-api
- 関連タスク: [[task_disaster_tweets_bert_discussion_20260114141258|Disaster Tweets: BERTモデルの実験（ディスカッションから取得）]]
