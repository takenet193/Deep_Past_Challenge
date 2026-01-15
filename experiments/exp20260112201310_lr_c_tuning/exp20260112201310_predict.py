"""
Prediction Script: Generate submission.csv
Experiment ID: exp20260112201310
"""

import re
import pickle
from pathlib import Path

import pandas as pd
import numpy as np
import yaml

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

# モデルとベクトライザーを読み込み
model_path = RESULTS_DIR / f"{EXP_ID}_model.pkl"
with open(model_path, 'rb') as f:
    model_data = pickle.load(f)
    model = model_data['model']
    vectorizer = model_data['vectorizer']
    best_C = model_data.get('best_C', None)

print("Model loaded successfully")
if best_C is not None:
    print(f"Best C used: {best_C}")

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

# 特徴量エンジニアリング
print("Creating TF-IDF features...")
X_test = vectorizer.transform(test_df['text_processed'])

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




