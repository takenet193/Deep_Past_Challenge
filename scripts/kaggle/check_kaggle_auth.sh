#!/bin/bash
# Kaggle認証確認スクリプト

echo "=========================================="
echo "Kaggle API認証確認"
echo "=========================================="
echo ""

# kaggle.jsonの存在確認
if [ -f ~/.kaggle/kaggle.json ]; then
    echo "✅ kaggle.jsonが見つかりました"
    ls -lh ~/.kaggle/kaggle.json
    echo ""
    
    # 権限確認
    PERM=$(stat -f "%OLp" ~/.kaggle/kaggle.json 2>/dev/null || stat -c "%a" ~/.kaggle/kaggle.json 2>/dev/null)
    if [ "$PERM" = "600" ]; then
        echo "✅ ファイル権限は正しく設定されています (600)"
    else
        echo "⚠️  ファイル権限を設定してください: chmod 600 ~/.kaggle/kaggle.json"
        echo "   現在の権限: $PERM"
    fi
    echo ""
    
    # API認証テスト
    echo "API認証をテストします..."
    if kaggle competitions list > /dev/null 2>&1; then
        echo "✅ 認証成功！Kaggle APIが使用できます"
        echo ""
        echo "利用可能なコンペティション（最初の5件）:"
        kaggle competitions list | head -6
    else
        echo "❌ 認証に失敗しました"
        echo "kaggle.jsonの内容を確認してください"
    fi
else
    echo "❌ kaggle.jsonが見つかりません"
    echo ""
    echo "配置手順:"
    echo "1. https://www.kaggle.com/ → Account → API → Create New API Token"
    echo "2. ダウンロードしたkaggle.jsonを ~/.kaggle/ に配置"
    echo "3. chmod 600 ~/.kaggle/kaggle.json を実行"
fi

echo ""
echo "=========================================="

