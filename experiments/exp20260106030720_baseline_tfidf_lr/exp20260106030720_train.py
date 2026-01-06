"""
Baseline Training Script: TF-IDF + LogisticRegression
Experiment ID: exp20260106030720
"""

import re
import json
import pickle
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import f1_score

# パス設定
EXP_DIR = Path(__file__).parent
REPO_ROOT = EXP_DIR.parent.parent  # experiments/expXXX/ -> experiments/ -> repo_root
CONFIG_PATH = EXP_DIR / f"{EXP_DIR.name.split('_')[0]}_config.yaml"
RESULTS_DIR = REPO_ROOT / "results" / EXP_DIR.name

# 実験IDを取得
EXP_ID = EXP_DIR.name.split('_')[0]

# 結果ディレクトリを作成
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# config.yamlを読み込む
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

# 乱数シードを設定
np.random.seed(config['seed'])

print(f"Experiment ID: {EXP_ID}")
print(f"Config loaded from: {CONFIG_PATH}")

# データ読み込み
train_path = REPO_ROOT / config['data']['train_path']
test_path = REPO_ROOT / config['data']['test_path']

print(f"Loading data from: {train_path}")
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

print(f"Train shape: {train_df.shape}")
print(f"Test shape: {test_df.shape}")

# 前処理関数
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
    
    # ハッシュタグ除去（今回はfalseなのでスキップ）
    if config_prep.get('remove_hashtags', False):
        hashtag_pattern = r'#\w+'
        text = re.sub(hashtag_pattern, '', text)
    
    return text

# 前処理を適用
print("Preprocessing text...")
train_df['text_processed'] = train_df['text'].apply(
    lambda x: preprocess_text(x, config['preprocessing'])
)
test_df['text_processed'] = test_df['text'].apply(
    lambda x: preprocess_text(x, config['preprocessing'])
)

# TF-IDF特徴量エンジニアリング
print("Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=config['feature_engineering']['params']['max_features'],
    ngram_range=tuple(config['feature_engineering']['params']['ngram_range']),
    min_df=config['feature_engineering']['params']['min_df']
)

X_train = vectorizer.fit_transform(train_df['text_processed'])
X_test = vectorizer.transform(test_df['text_processed'])
y_train = train_df['target'].values

print(f"Feature matrix shape: {X_train.shape}")

# モデル定義
model = LogisticRegression(
    C=config['model']['params']['C'],
    max_iter=config['model']['params']['max_iter'],
    random_state=config['model']['params']['random_state']
)

# StratifiedKFoldでCV評価
print("Running Cross-Validation...")
cv = StratifiedKFold(
    n_splits=config['validation']['n_folds'],
    shuffle=config['validation']['shuffle'],
    random_state=config['validation']['random_state']
)

cv_scores = cross_val_score(
    model, X_train, y_train,
    cv=cv,
    scoring='f1',
    n_jobs=-1
)

cv_mean = cv_scores.mean()
cv_std = cv_scores.std()

print(f"CV F1 Score: {cv_mean:.4f} (+/- {cv_std:.4f})")
print(f"CV Scores per fold: {cv_scores}")

# 全データで学習（最終モデル）
print("Training final model on full data...")
model.fit(X_train, y_train)

# Train F1スコア
y_train_pred = model.predict(X_train)
train_f1 = f1_score(y_train, y_train_pred)
print(f"Train F1 Score: {train_f1:.4f}")

# 結果を保存
results = {
    'experiment_id': EXP_ID,
    'train_f1': float(train_f1),
    'cv_mean': float(cv_mean),
    'cv_std': float(cv_std),
    'cv_scores': cv_scores.tolist(),
    'public_lb': None
}

# metrics.json
metrics_path = RESULTS_DIR / f"{EXP_ID}_metrics.json"
with open(metrics_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"Metrics saved to: {metrics_path}")

# cv_results.json
cv_results = {f'fold_{i}': float(score) for i, score in enumerate(cv_scores)}
cv_results_path = RESULTS_DIR / f"{EXP_ID}_cv_results.json"
with open(cv_results_path, 'w') as f:
    json.dump(cv_results, f, indent=2)
print(f"CV results saved to: {cv_results_path}")

# モデルとベクトライザーを保存
if config['output']['save_model']:
    model_path = RESULTS_DIR / f"{EXP_ID}_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': vectorizer
        }, f)
    print(f"Model saved to: {model_path}")

print("Training completed!")

