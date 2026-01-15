"""
Training Script: TF-IDF + Keyword Feature + LogisticRegression
Experiment ID: exp20260112174906
"""

import re
import json
import pickle
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np
import yaml
from scipy.sparse import hstack
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
    
    # ハッシュタグ除去
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

# keywordの欠損値処理
keyword_missing_strategy = config['preprocessing'].get('missing_value_strategy', 'unknown')
if keyword_missing_strategy == 'unknown':
    train_df['keyword'] = train_df['keyword'].fillna('unknown')
    test_df['keyword'] = test_df['keyword'].fillna('unknown')
    print(f"Keyword missing values filled with 'unknown': train={train_df['keyword'].isna().sum()}, test={test_df['keyword'].isna().sum()}")
elif keyword_missing_strategy == 'mode':
    mode_keyword = train_df['keyword'].mode()[0]
    train_df['keyword'] = train_df['keyword'].fillna(mode_keyword)
    test_df['keyword'] = test_df['keyword'].fillna(mode_keyword)
    print(f"Keyword missing values filled with mode '{mode_keyword}'")

print(f"Train keyword unique: {train_df['keyword'].nunique()}")
print(f"Test keyword unique: {test_df['keyword'].nunique()}")

# ターゲットエンコーディング関数
def target_encode_keyword(train_keyword, train_target, val_keyword, smoothing=1.0):
    """
    ターゲットエンコーディング（データリークを防ぐため、trainデータのみを使用）
    
    Args:
        train_keyword: trainデータのkeyword列
        train_target: trainデータのtarget列
        val_keyword: validationデータのkeyword列
        smoothing: 平滑化パラメータ（デフォルト1.0）
    
    Returns:
        val_keyword_encoded: validationデータのkeywordエンコーディング
        encoder_dict: エンコーダーの辞書（keyword -> 災害率）
    """
    # trainデータでkeywordごとの災害率を計算
    keyword_df = pd.DataFrame({
        'keyword': train_keyword,
        'target': train_target
    })
    
    keyword_stats = keyword_df.groupby('keyword')['target'].agg(['mean', 'count'])
    
    # 平滑化を適用（ベイズ推定）
    global_mean = train_target.mean()
    keyword_stats['encoded'] = (
        (keyword_stats['count'] * keyword_stats['mean'] + smoothing * global_mean) /
        (keyword_stats['count'] + smoothing)
    )
    
    # エンコーダー辞書を作成
    encoder_dict = keyword_stats['encoded'].to_dict()
    encoder_dict['__global_mean__'] = global_mean  # 未知のkeyword用
    
    # validationデータにエンコーディングを適用
    val_keyword_encoded = val_keyword.map(encoder_dict).fillna(global_mean)
    
    return val_keyword_encoded.values, encoder_dict

# TF-IDF特徴量エンジニアリング
print("Creating TF-IDF features...")
vectorizer = TfidfVectorizer(
    max_features=config['feature_engineering']['params']['max_features'],
    ngram_range=tuple(config['feature_engineering']['params']['ngram_range']),
    min_df=config['feature_engineering']['params']['min_df']
)

X_train_tfidf = vectorizer.fit_transform(train_df['text_processed'])
X_test_tfidf = vectorizer.transform(test_df['text_processed'])
y_train = train_df['target'].values

print(f"TF-IDF feature matrix shape: {X_train_tfidf.shape}")

# StratifiedKFoldでCV評価（keyword特徴量を含む）
print("Running Cross-Validation with keyword feature...")
cv = StratifiedKFold(
    n_splits=config['validation']['n_folds'],
    shuffle=config['validation']['shuffle'],
    random_state=config['validation']['random_state']
)

cv_scores = []
keyword_encoders = []  # 各フォールドのエンコーダーを保存（参考用）

smoothing = config['feature_engineering']['keyword_encoding'].get('smoothing', 1.0)

for fold, (train_idx, val_idx) in enumerate(cv.split(X_train_tfidf, y_train)):
    print(f"  Fold {fold + 1}/{config['validation']['n_folds']}...")
    
    # フォールド内のデータを分割
    train_keyword_fold = train_df.iloc[train_idx]['keyword']
    train_target_fold = train_df.iloc[train_idx]['target']
    val_keyword_fold = train_df.iloc[val_idx]['keyword']
    
    X_train_fold_tfidf = X_train_tfidf[train_idx]
    X_val_fold_tfidf = X_train_tfidf[val_idx]
    y_train_fold = y_train[train_idx]
    y_val_fold = y_train[val_idx]
    
    # keyword特徴量のターゲットエンコーディング（trainデータのみを使用）
    val_keyword_encoded, encoder_dict = target_encode_keyword(
        train_keyword_fold, train_target_fold, val_keyword_fold, smoothing=smoothing
    )
    keyword_encoders.append(encoder_dict)
    
    # keyword特徴量を2次元配列に変換（スパース行列と結合するため）
    val_keyword_encoded_2d = val_keyword_encoded.reshape(-1, 1)
    
    # 特徴量を結合
    from scipy.sparse import csr_matrix
    val_keyword_encoded_sparse = csr_matrix(val_keyword_encoded_2d)
    X_val_fold = hstack([val_keyword_encoded_sparse, X_val_fold_tfidf])
    
    # モデルを学習（trainデータでkeyword特徴量も作成）
    train_keyword_encoded, _ = target_encode_keyword(
        train_keyword_fold, train_target_fold, train_keyword_fold, smoothing=smoothing
    )
    train_keyword_encoded_2d = train_keyword_encoded.reshape(-1, 1)
    train_keyword_encoded_sparse = csr_matrix(train_keyword_encoded_2d)
    X_train_fold = hstack([train_keyword_encoded_sparse, X_train_fold_tfidf])
    
    # モデル学習
    model = LogisticRegression(
        C=config['model']['params']['C'],
        max_iter=config['model']['params']['max_iter'],
        random_state=config['model']['params']['random_state']
    )
    model.fit(X_train_fold, y_train_fold)
    
    # 予測と評価
    y_val_pred = model.predict(X_val_fold)
    fold_f1 = f1_score(y_val_fold, y_val_pred)
    cv_scores.append(fold_f1)
    print(f"    Fold {fold + 1} F1: {fold_f1:.4f}")

cv_scores = np.array(cv_scores)
cv_mean = cv_scores.mean()
cv_std = cv_scores.std()

print(f"CV F1 Score: {cv_mean:.4f} (+/- {cv_std:.4f})")
print(f"CV Scores per fold: {cv_scores}")

# 全データで学習（最終モデル）
print("Training final model on full data...")

# 全trainデータでkeywordエンコーディングを計算
train_keyword_encoded_full, keyword_encoder_full = target_encode_keyword(
    train_df['keyword'], train_df['target'], train_df['keyword'], smoothing=smoothing
)
train_keyword_encoded_full_2d = train_keyword_encoded_full.reshape(-1, 1)
from scipy.sparse import csr_matrix
train_keyword_encoded_full_sparse = csr_matrix(train_keyword_encoded_full_2d)

# 特徴量を結合
X_train_full = hstack([train_keyword_encoded_full_sparse, X_train_tfidf])

# モデル学習
model = LogisticRegression(
    C=config['model']['params']['C'],
    max_iter=config['model']['params']['max_iter'],
    random_state=config['model']['params']['random_state']
)
model.fit(X_train_full, y_train)

# Train F1スコア
y_train_pred = model.predict(X_train_full)
train_f1 = f1_score(y_train, y_train_pred)
print(f"Train F1 Score: {train_f1:.4f}")

# testデータのkeywordエンコーディング（全trainデータで計算したエンコーダーを使用）
test_keyword_encoded = test_df['keyword'].map(keyword_encoder_full).fillna(keyword_encoder_full['__global_mean__'])
test_keyword_encoded_2d = test_keyword_encoded.values.reshape(-1, 1)
test_keyword_encoded_sparse = csr_matrix(test_keyword_encoded_2d)
X_test_full = hstack([test_keyword_encoded_sparse, X_test_tfidf])

print(f"Final feature matrix shape: {X_train_full.shape}")
print(f"Test feature matrix shape: {X_test_full.shape}")

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

# モデル、ベクトライザー、エンコーダーを保存
if config['output']['save_model']:
    model_path = RESULTS_DIR / f"{EXP_ID}_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': model,
            'vectorizer': vectorizer,
            'keyword_encoder': keyword_encoder_full
        }, f)
    print(f"Model saved to: {model_path}")

print("Training completed!")

