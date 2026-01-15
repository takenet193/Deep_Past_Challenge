#!/bin/bash
# Kaggle APIトークンを使用した提出スクリプト

# トークンを環境変数として設定（画像から取得したトークン）
export KAGGLE_API_TOKEN="KGAT_5345688a7e7d12cff6dcf8b56557950f"

EXP_ID="exp20260112174906"
COMPETITION="nlp-getting-started"
SUBMISSION_FILE="results/${EXP_ID}_keyword_tfidf_lr/${EXP_ID}_submission.csv"
MESSAGE="${EXP_ID}: keyword feature + TF-IDF + LogisticRegression"

echo "=========================================="
echo "Kaggle提出スクリプト（環境変数使用）"
echo "=========================================="
echo "実験ID: ${EXP_ID}"
echo "コンペティション: ${COMPETITION}"
echo "提出ファイル: ${SUBMISSION_FILE}"
echo "メッセージ: ${MESSAGE}"
echo "=========================================="
echo ""

# ファイルの存在確認
if [ ! -f "${SUBMISSION_FILE}" ]; then
    echo "エラー: 提出ファイルが見つかりません: ${SUBMISSION_FILE}"
    exit 1
fi

echo "提出ファイルを確認しました:"
ls -lh "${SUBMISSION_FILE}"
echo ""

# Kaggle API認証確認
echo "Kaggle API認証を確認中..."
if ! kaggle competitions list > /dev/null 2>&1; then
    echo "エラー: Kaggle API認証に失敗しました"
    echo "トークンが正しく設定されているか確認してください"
    exit 1
fi

echo "認証OK"
echo ""

# 提出実行
echo "提出を実行します..."
kaggle competitions submit \
    -c "${COMPETITION}" \
    -f "${SUBMISSION_FILE}" \
    -m "${MESSAGE}"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "提出が完了しました！"
    echo "Kaggleのコンペティションページで結果を確認してください"
    echo "https://www.kaggle.com/competitions/${COMPETITION}/submissions"
    echo "=========================================="
else
    echo ""
    echo "=========================================="
    echo "提出に失敗しました"
    echo "エラーメッセージを確認してください"
    echo "=========================================="
    exit 1
fi

