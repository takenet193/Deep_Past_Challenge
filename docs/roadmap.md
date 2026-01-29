# 実装ロードマップ

## フェーズ1: 基盤構築（1-2週間）✅ **完了**

### 完了済み
- [x] 基本的なディレクトリ構造作成（詳細は[README.md](../README.md#ディレクトリ構造)を参照）
- [x] マルチエージェントシステム定義（kaggle_team.mdc）
- [x] 実験フロー定義（experiment_flow_instructions.mdc）
- [x] README.mdの作成
- [x] KaggleBaseのObsidian vault初期化
  - [x] Zettelkastenテンプレート作成
  - [x] GTDテンプレート作成
  - [x] タグ規則の適用
- [x] task_converter.pyの実装 ✅
- [x] task_loader.pyの実装 ✅
- [x] sync_project_links.pyの実装 ✅

## フェーズ2: ワークフロー検証（2-3週間）✅ **進行中**

- [x] 初回実験（exp20260106030720_baseline_tfidf_lr）でワークフロー全体を検証
  - [x] KaggleBaseでタスク作成
  - [x] JSON変換
  - [x] マルチエージェントでの実験実行
  - [x] 結果の知識ベースへのフィードバック
- [x] 複数の実験サイクルを回して課題抽出
  - exp20260106030720_baseline_tfidf_lr
  - exp20260112174906_keyword_tfidf_lr
  - exp20260112201310_lr_c_tuning
- [x] ワークフローの改善
- [ ] ドキュメント改訂（実装内容に合わせた更新）← **現在進行中**

## フェーズ3: 自動化・効率化（3-4週間）⏳ **将来実装**

> **注**: フェーズ2でワークフローが安定した後、必要に応じて導入を検討。

- [ ] **監視スクリプトシステムの導入** 🆕
  - [ ] task_watcher.py（タスク自動変換）
  - [ ] knowledge_watcher.py（知識インデックス化）
  - [ ] results_watcher.py（結果自動知識化）
  - [ ] experiment_watcher.py（コード品質検証）
  - [ ] watch_all.py（統合監視システム）
- [ ] Kaggle Discussion自動取り込みパイプライン
  - [ ] Kaggle API連携
  - [ ] 定期実行スクリプト
- [ ] タスク優先度計算機能
- [ ] 計算資源スケジューリング（基本版）

**現状**: 手動フロー（`python scripts/workflow/task_converter.py`）で十分に機能しているため、監視スクリプトの優先度は低い。

## フェーズ4: MLOps統合（知人と協力）⏳ **将来実装**

> **注**: ローカル開発環境でのワークフローが確立した後、必要に応じて検討。

- [ ] GitHub Actions設定
- [ ] DVC導入
- [ ] MLflow連携
- [ ] W&B連携
- [ ] 計算資源の最適割り当て（クラウド版）

**現状**: ローカル環境での開発が中心。MLOpsパイプラインは将来の拡張として計画。

## フェーズ5: 高度な機能（将来）

- [ ] Obsidian Graph Viewでの実験系統樹可視化の自動化
- [ ] アンサンブルモデルの自動生成
- [ ] ハイパーパラメータ最適化の自動化
- [ ] リアルタイムダッシュボード
- [ ] チーム間の非同期コミュニケーション強化

## 関連ドキュメント

- [プロジェクトアーキテクチャ](./project_architecture.md) - システム設計の概要
- [システム概要](./system_overview.md) - システム全体の概要
- [将来実装機能の詳細設計](./future_features.md) - 将来実装予定の機能の詳細設計

