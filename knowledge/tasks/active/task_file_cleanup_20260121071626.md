---
type: task
id: task-20260121071626
title: 旧プロジェクトファイルの整理・削除
author: takeikumi
status: active
priority: high
project: git_repository_setup
mode: cleanup
due_date: null
context: []
tags:
  - git
  - cleanup
  - setup
related_notes: []
assignee: null
assigned_agent: null
dependencies: []
created: 2026-01-21
updated: 2026-01-21
---

# タスク: 旧プロジェクトファイルの整理・削除

## 目的

旧プロジェクト（Disaster Tweets）に固有なファイルが残っていないか確認し、不要なファイルを削除する。
Gitリポジトリを作成する前に、プロジェクトをクリーンな状態にする。

## 完了条件

- 旧プロジェクト固有のファイルがすべて削除されている
- 不要になったファイルがない
- プロジェクトが新しいコンペ用のクリーンな状態になっている

## チェック項目

### 1. Knowledge Base (`knowledge/`)
- [ ] `knowledge/tasks/active/` の旧プロジェクトタスクファイル
- [ ] `knowledge/tasks/completed/` の旧プロジェクトタスクファイル
- [ ] `knowledge/tasks/projects/` の旧プロジェクトプロジェクトファイル（`project_kaggle_disaster_tweets*.md`など）
- [ ] `knowledge/zettelkasten/permanent/` の旧プロジェクトノート（`disaster_tweets*.md`など）
- [ ] `knowledge/inbox/` の旧プロジェクト関連ファイル

### 2. ドキュメント (`docs/`)
- [ ] 旧プロジェクト固有の内容が含まれていないか確認
- [ ] 例示としてDisaster Tweetsの参照が残っていないか確認

### 3. その他
- [ ] `.obsidian/` の設定ファイルが旧プロジェクト用になっていないか
- [ ] その他、旧プロジェクト固有のファイルがないか

## 手順

1. [ ] プロジェクト全体をスキャンして、旧プロジェクト関連のファイルを特定
2. [ ] 削除すべきファイルをリストアップ
3. [ ] 削除を実行
4. [ ] 削除後の状態を確認

## メモ

- アーキテクチャとして残すべきファイル（テンプレート、スクリプトなど）は削除しない
- 削除前に重要な情報がないか確認すること

<!-- AUTO:project:start -->
- [[project_git_repository_setup|project: git_repository_setup]]
<!-- AUTO:project:end -->

