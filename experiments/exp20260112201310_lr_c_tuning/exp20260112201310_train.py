"""
Training Script: TF-IDF + LogisticRegression (C値グリッドサーチ)
Experiment ID: exp20260112201310
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

# C値グリッドを取得
c_grid = config['model']['c_grid']
print(f"C値グリッド: {c_grid}")

# StratifiedKFoldを設定
cv = StratifiedKFold(
    n_splits=config['validation']['n_folds'],
    shuffle=config['validation']['shuffle'],
    random_state=config['validation']['random_state']
)

# C値スイープ
print("\n" + "="*60)
print("Running C-value Grid Search...")
print("="*60)

c_search_results = []

for C in c_grid:
    print(f"\n--- C = {C} ---")
    
    # モデル定義
    model = LogisticRegression(
        C=C,
        max_iter=config['model']['params']['max_iter'],
        random_state=config['model']['params']['random_state']
    )
    
    # CV評価
    cv_scores = cross_val_score(
        model, X_train, y_train,
        cv=cv,
        scoring='f1',
        n_jobs=-1
    )
    
    cv_mean = cv_scores.mean()
    cv_std = cv_scores.std()
    
    # 全データで学習してTrain F1を計算
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    train_f1 = f1_score(y_train, y_train_pred)
    
    print(f"  CV Mean F1: {cv_mean:.4f} (+/- {cv_std:.4f})")
    print(f"  CV Scores: {cv_scores}")
    print(f"  Train F1: {train_f1:.4f}")
    print(f"  Train-CV Gap: {train_f1 - cv_mean:.4f}")
    
    # 結果を保存
    c_search_results.append({
        'C': float(C),
        'cv_mean': float(cv_mean),
        'cv_std': float(cv_std),
        'cv_scores': cv_scores.tolist(),
        'train_f1': float(train_f1),
        'train_cv_gap': float(train_f1 - cv_mean)
    })

# C値スイープ結果を保存
c_search_path = RESULTS_DIR / f"{EXP_ID}_c_search.json"
with open(c_search_path, 'w') as f:
    json.dump(c_search_results, f, indent=2)
print(f"\nC値スイープ結果を保存: {c_search_path}")

# ベストCの選択
# CV Mean F1が最大のCを選択（同点の場合はより小さいCを優先）
best_result = max(c_search_results, key=lambda x: (x['cv_mean'], -x['C']))
best_C = best_result['C']

print("\n" + "="*60)
print("Best C Selection")
print("="*60)
print(f"Best C: {best_C}")
print(f"Best CV Mean F1: {best_result['cv_mean']:.4f} (+/- {best_result['cv_std']:.4f})")
print(f"Best Train F1: {best_result['train_f1']:.4f}")
print(f"Train-CV Gap: {best_result['train_cv_gap']:.4f}")

# ベストCで最終モデルを学習
print("\n" + "="*60)
print("Training final model with best C...")
print("="*60)

final_model = LogisticRegression(
    C=best_C,
    max_iter=config['model']['params']['max_iter'],
    random_state=config['model']['params']['random_state']
)

final_model.fit(X_train, y_train)

# 最終モデルのTrain F1
y_train_pred_final = final_model.predict(X_train)
final_train_f1 = f1_score(y_train, y_train_pred_final)
print(f"Final Train F1: {final_train_f1:.4f}")

# 最終結果を保存
final_results = {
    'experiment_id': EXP_ID,
    'best_C': float(best_C),
    'train_f1': float(final_train_f1),
    'cv_mean': float(best_result['cv_mean']),
    'cv_std': float(best_result['cv_std']),
    'cv_scores': best_result['cv_scores'],
    'train_cv_gap': float(best_result['train_cv_gap']),
    'c_search_results': c_search_results,
    'public_lb': None
}

# metrics.json
metrics_path = RESULTS_DIR / f"{EXP_ID}_metrics.json"
with open(metrics_path, 'w') as f:
    json.dump(final_results, f, indent=2)
print(f"Metrics saved to: {metrics_path}")

# cv_results.json（ベストCの結果）
cv_results = {f'fold_{i}': float(score) for i, score in enumerate(best_result['cv_scores'])}
cv_results_path = RESULTS_DIR / f"{EXP_ID}_cv_results.json"
with open(cv_results_path, 'w') as f:
    json.dump(cv_results, f, indent=2)
print(f"CV results saved to: {cv_results_path}")

# モデルとベクトライザーを保存
if config['output']['save_model']:
    model_path = RESULTS_DIR / f"{EXP_ID}_model.pkl"
    with open(model_path, 'wb') as f:
        pickle.dump({
            'model': final_model,
            'vectorizer': vectorizer,
            'best_C': best_C
        }, f)
    print(f"Model saved to: {model_path}")

print("\n" + "="*60)
print("Training completed!")
print("="*60)




