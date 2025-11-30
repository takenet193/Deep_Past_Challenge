# Roadmap

このファイルは `scripts/generate_roadmap.py` を実行することで、`plan.json` から自動生成されます。

## 生成方法

```bash
python scripts/generate_roadmap.py
```

または、カスタムパスを指定する場合:

```bash
python scripts/generate_roadmap.py --input .cursor/plan.json --output docs/ROADMAP.md
```

## 注意

このファイルを手動で編集しても、次回 `generate_roadmap.py` を実行すると上書きされます。
タスクの内容を変更する場合は、`plan.json` を編集してください。

