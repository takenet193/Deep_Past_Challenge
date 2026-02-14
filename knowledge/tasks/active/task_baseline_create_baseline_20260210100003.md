---
type: task
id: task-20260210100003
title: ベースラインを作成する
author: takeikumi
status: active
priority: high
project: baseline
mode: implementation
due_date: null
context: []
tags:
  - baseline
  - kaggle
  - machine-translation
related_notes:
  - harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000
assignee: null
assigned_agent: null
dependencies:
  - task-20260210100002
created: 2026-02-10
updated: 2026-02-10
---

# タスク: ベースラインを作成する

## 目的

機械翻訳のベースライン（シンプルな最初の解）を実装し、コンペに提出できる状態まで進める。

## 手順

- [x] ベースラインのアプローチを決める（harukiharada の ByT5 + Optuna + Chunked Beam Search を再現）
- [ ] Kaggle からノートブックを取得し、ローカルで再現する
- [ ] 実装する（自前ベースライン or 再現ベースの改良）
- [ ] ローカルで検証する
- [ ] 提出ファイルを作成し、コンペに提出する

## 参考モデル（2026-02-13 調査）

- **harukiharada**: ByT5 + Optuna Tuning + Chunked Beam Search
  - URL: https://www.kaggle.com/code/harukiharada/byt5-optuna-tuning-chunked-beam-search
  - スコア: 35.1（Bronze）
  - リファレンス: `knowledge/zettelkasten/references/harukiharada_byt5_optuna_chunked_beam_search_reference_20260213000000.md`
- **再現計画**: `docs/baseline_byt5_reproduction_plan.md`
- **依存関係**: `requirements-baseline.txt`

## 結果（実施報告）/ 学び / 次のアクション

- **結果**: harukiharada の ByT5 アプローチを調査し、リファレンスノート・再現計画を作成
- **学び**: ByT5 はバイトレベルでノイズ耐性が高く、古代テキスト・低リソース翻訳向き。Chunked Beam Search で長文に対応
- **次のアクション**: Kaggle CLI でノートブックを取得し、ローカル環境で軽量版を実行して動作確認

> 注: タスク完了時（`status: completed`に変更時）は、必ずこのセクションに実施報告を記載してください。

<!-- AUTO:project:start -->
- [[project_baseline|project: baseline]]
<!-- AUTO:project:end -->
