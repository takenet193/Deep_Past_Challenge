"""
Prediction Script: Generate submission.csv with keyword feature
Experiment ID: exp20260112174906
"""

import re
import pickle
from pathlib import Path

import pandas as pd
import numpy as np
import yaml
from scipy.sparse import hstack, csr_matrix

# パス設定
EXP_DIR = Path(__file__).parent
REPO_ROOT = EXP_DIR.parent.parent  # experiments/expXXX/ -> experiments/ -> repo_root
CONFIG_PATH = EXP_DIR / f"{EXP_DIR.name.split('_')[0]}_config.yaml"
RESULTS_DIR = REPO_ROOT / "results" / EXP_DIR.name

# 実験IDを取得
EXP_ID = EXP_DIR.name.split('_')[0]

# config.yamlを読み込む
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

print(f"Experiment ID: {EXP_ID}")
print(f"Loading model from: {RESULTS_DIR}")

# モデル、ベクトライザー、エンコーダーを読み込み
model_path = RESULTS_DIR / f"{EXP_ID}_model.pkl"
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    vectorizer = model_data['vectorizer']
    keyword_encoder = model_data['keyword_encoder']

print("Model loaded successfully")

# テストデータを読み込み
test_path = REPO_ROOT / config['data']['test_path']
test_df = pd.read_csv(test_path)

print(f"Test data shape: {test_df.shape}")

# 前処理関数（train.pyと同じ）
def preprocess_text(text, config_prep):
    """テキスト前処理"""
    if pd.isna(text):
        return ""
    
    # lowercase
    if config_prep.get('lowercase', False):
        text = text.lower()
    
    # URL除去
    if config_prep.get('remove_urls', False):
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        text = re.sub(url_pattern, '', text)
    
    # メンション除去
    if config_prep.get('remove_mentions', False):
        mention_pattern = r'@\w+'
        text = re.sub(mention_pattern, '', text)
    
    # ハッシュタグ除去
    if config_prep.get('remove_hashtags', False):
        hashtag_pattern = r'#\w+'
        text = re.sub(hashtag_pattern, '', text)
    
    return text

# 前処理を適用
print("Preprocessing test data...")
test_df['text_processed'] = test_df['text'].apply(
    lambda x: preprocess_text(x, config['preprocessing'])
)

# keywordの欠損値処理（train.pyと同じ）
keyword_missing_strategy = config['preprocessing'].get('missing_value_strategy', 'unknown')
if keyword_missing_strategy == 'unknown':
    test_df['keyword'] = test_df['keyword'].fillna('unknown')
elif keyword_missing_strategy == 'mode':
    # modeはtrainデータから取得する必要があるが、ここではunknownで処理
    test_df['keyword'] = test_df['keyword'].fillna('unknown')

# TF-IDF特徴量エンジニアリング
print("Creating TF-IDF features...")
X_test_tfidf = vectorizer.transform(test_df['text_processed'])

# keyword特徴量のエンコーディング（学習時に計算したエンコーダーを使用）
print("Encoding keyword features...")
test_keyword_encoded = test_df['keyword'].map(keyword_encoder).fillna(keyword_encoder.get('__global_mean__', 0.0))
test_keyword_encoded_2d = test_keyword_encoded.values.reshape(-1, 1)
test_keyword_encoded_sparse = csr_matrix(test_keyword_encoded_2d)

# 特徴量を結合
X_test = hstack([test_keyword_encoded_sparse, X_test_tfidf])

print(f"Test feature matrix shape: {X_test.shape}")

# 予測
print("Making predictions...")
y_pred = model.predict(X_test)

# submission.csvを作成
submission_df = pd.DataFrame({
    'id': test_df['id'],
    'target': y_pred
})

submission_path = RESULTS_DIR / f"{EXP_ID}_submission.csv"
submission_df.to_csv(submission_path, index=False)

print(f"Submission file saved to: {submission_path}")
print(f"Submission shape: {submission_df.shape}")
print(f"Target distribution: {submission_df['target'].value_counts().to_dict()}")

print("Prediction completed!")




