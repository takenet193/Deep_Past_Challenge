"""
Deep Past Challenge - Baseline EDA Script
タスク: task_baseline_eda_20260211123000

このスクリプトは、train/test データの構造、長さ分布、記号出現、語彙、翻訳特徴を分析し、
ベースライン実装の方針を決めるための洞察を提供する。
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # GUI なしで画像保存
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from pathlib import Path
import sys

# Windows で UTF-8 出力を強制
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# プロジェクトルート
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_DIR = PROJECT_ROOT / "results"
FIGURES_DIR = RESULTS_DIR / "figures"

# データファイルパス
TRAIN_CSV = DATA_DIR / "train.csv"
TEST_CSV = DATA_DIR / "test.csv"
SAMPLE_SUBMISSION_CSV = DATA_DIR / "sample_submission.csv"
SENTENCES_CSV = DATA_DIR / "Sentences_Oare_FirstWord_LinNum.csv"
PUBLISHED_TEXTS_CSV = DATA_DIR / "published_texts.csv"
LEXICON_CSV = DATA_DIR / "OA_Lexicon_eBL.csv"


def print_section(title):
    """セクション区切りを出力"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def analyze_basic_structure():
    """タスク項目1: 基本構造の把握"""
    print_section("1. 基本構造の把握")
    
    # 各ファイルを読み込み、基本情報を表示
    files = {
        "train.csv": TRAIN_CSV,
        "test.csv": TEST_CSV,
        "sample_submission.csv": SAMPLE_SUBMISSION_CSV,
        "Sentences_Oare_FirstWord_LinNum.csv": SENTENCES_CSV,
        "published_texts.csv": PUBLISHED_TEXTS_CSV,
        "OA_Lexicon_eBL.csv": LEXICON_CSV,
    }
    
    for name, path in files.items():
        print(f"\n--- {name} ---")
        if not path.exists():
            print(f"  ファイルが見つかりません: {path}")
            continue
            
        df = pd.read_csv(path)
        print(f"  Shape: {df.shape} (行数={df.shape[0]}, 列数={df.shape[1]})")
        print(f"  Columns: {df.columns.tolist()}")
        
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            print(f"  NULL counts:")
            for col, count in null_counts[null_counts > 0].items():
                print(f"    {col}: {count}")
        else:
            print(f"  NULL: なし")
    
    # train/test/submission の関係を確認
    print("\n--- データの関係 ---")
    train = pd.read_csv(TRAIN_CSV)
    test = pd.read_csv(TEST_CSV)
    submission = pd.read_csv(SAMPLE_SUBMISSION_CSV)
    
    print(f"  train: {len(train)} 文書（文書単位）")
    print(f"  test: {len(test)} 文（本番は約4,000文）")
    print(f"  sample_submission: {len(submission)} 行（test.id と対応）")
    
    # test の text_id のユニーク数
    if 'text_id' in test.columns:
        unique_texts = test['text_id'].nunique()
        print(f"  test の text_id ユニーク数: {unique_texts} 文書")
    
    return train, test, submission


def analyze_length_distribution(train):
    """タスク項目2: 長さ・分布の確認"""
    print_section("2. 長さ・分布の確認")
    
    # 文字数・単語数の計算
    train['translit_len_char'] = train['transliteration'].str.len()
    train['translit_len_words'] = train['transliteration'].str.split().str.len()
    train['translation_len_char'] = train['translation'].str.len()
    train['translation_len_words'] = train['translation'].str.split().str.len()
    
    # 長さ比（length ratio）
    train['length_ratio'] = train['translation_len_words'] / train['translit_len_words']
    
    print("\n--- 転写（transliteration）の長さ統計 ---")
    print("文字数:")
    print(train['translit_len_char'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    print("\n単語数:")
    print(train['translit_len_words'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    
    print("\n--- 翻訳（translation）の長さ統計 ---")
    print("文字数:")
    print(train['translation_len_char'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    print("\n単語数:")
    print(train['translation_len_words'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    
    print("\n--- 長さ比（translation / transliteration）---")
    print(train['length_ratio'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    
    # 極端に長いサンプル
    long_threshold_words = train['translit_len_words'].quantile(0.95)
    long_samples = train[train['translit_len_words'] > long_threshold_words]
    print(f"\n極端に長いサンプル（95パーセンタイル以上）: {len(long_samples)} 件")
    
    # 可視化
    print("\n可視化を作成中...")
    
    # ヒストグラム：転写・翻訳の単語数分布
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    axes[0].hist(train['translit_len_words'].dropna(), bins=50, edgecolor='black', alpha=0.7)
    axes[0].set_title('Transliteration Length Distribution (words)', fontsize=12)
    axes[0].set_xlabel('Number of Words')
    axes[0].set_ylabel('Frequency')
    axes[0].grid(alpha=0.3)
    
    axes[1].hist(train['translation_len_words'].dropna(), bins=50, edgecolor='black', alpha=0.7, color='orange')
    axes[1].set_title('Translation Length Distribution (words)', fontsize=12)
    axes[1].set_xlabel('Number of Words')
    axes[1].set_ylabel('Frequency')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'length_distribution.png', dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  保存: {FIGURES_DIR / 'length_distribution.png'}")
    
    # 散布図：転写 vs 翻訳の長さ相関
    plt.figure(figsize=(8, 6))
    plt.scatter(train['translit_len_words'], train['translation_len_words'], alpha=0.3, s=10)
    plt.xlabel('Transliteration Words', fontsize=11)
    plt.ylabel('Translation Words', fontsize=11)
    plt.title('Length Correlation: Transliteration vs Translation', fontsize=12)
    plt.grid(alpha=0.3)
    plt.savefig(FIGURES_DIR / 'length_correlation.png', dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  保存: {FIGURES_DIR / 'length_correlation.png'}")
    
    # 箱ひげ図：長さの分布
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].boxplot([train['translit_len_words'].dropna()], labels=['Transliteration'])
    axes[0].set_ylabel('Number of Words')
    axes[0].set_title('Transliteration Length (boxplot)')
    axes[0].grid(alpha=0.3)
    
    axes[1].boxplot([train['translation_len_words'].dropna()], labels=['Translation'])
    axes[1].set_ylabel('Number of Words')
    axes[1].set_title('Translation Length (boxplot)')
    axes[1].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'length_boxplot.png', dpi=100, bbox_inches='tight')
    plt.close()
    print(f"  保存: {FIGURES_DIR / 'length_boxplot.png'}")
    
    # Sentences_Oare_FirstWord_LinNum.csv を使った文単位の分析
    print("\n--- 文単位での長さ分布（Sentences_Oare_FirstWord_LinNum.csv） ---")
    sentences = pd.read_csv(SENTENCES_CSV)
    print(f"  Sentences 件数: {len(sentences)}")
    if 'translation' in sentences.columns:
        sentences['sent_len_words'] = sentences['translation'].str.split().str.len()
        print("  文単位の翻訳長さ（単語数）統計:")
        print(sentences['sent_len_words'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    
    return train


def analyze_symbols(train):
    """タスク項目3: 記号・表記の出現状況"""
    print_section("3. 記号・表記の出現状況")
    
    # 記号類の頻度カウント
    print("--- 記号の出現頻度 ---")
    
    # 決定詞 {} 
    train['has_determinatives'] = train['transliteration'].str.contains(r'\{.*?\}', na=False)
    det_count = train['has_determinatives'].sum()
    det_pct = det_count / len(train) * 100
    print(f"  決定詞 {{}}: {det_count} / {len(train)} ({det_pct:.1f}%)")
    
    # 丸括弧 () の determinatives も確認
    train['has_paren_det'] = train['transliteration'].str.contains(r'\([a-z]+\)', na=False)
    paren_count = train['has_paren_det'].sum()
    paren_pct = paren_count / len(train) * 100
    print(f"  丸括弧 determinatives (): {paren_count} / {len(train)} ({paren_pct:.1f}%)")
    
    # 欠損記号
    train['has_brackets'] = train['transliteration'].str.contains(r'[\[\]]', na=False)
    bracket_count = train['has_brackets'].sum()
    bracket_pct = bracket_count / len(train) * 100
    print(f"  角括弧 []: {bracket_count} / {len(train)} ({bracket_pct:.1f}%)")
    
    train['has_ellipsis'] = train['transliteration'].str.contains(r'…|\.\.\.', na=False)
    ellipsis_count = train['has_ellipsis'].sum()
    ellipsis_pct = ellipsis_count / len(train) * 100
    print(f"  省略記号 …: {ellipsis_count} / {len(train)} ({ellipsis_pct:.1f}%)")
    
    train['has_gap'] = train['transliteration'].str.contains(r'<gap>|<big_gap>', na=False)
    gap_count = train['has_gap'].sum()
    gap_pct = gap_count / len(train) * 100
    print(f"  gap マーカー: {gap_count} / {len(train)} ({gap_pct:.1f}%)")
    
    # 書記記号
    train['has_exclamation'] = train['transliteration'].str.contains(r'!', na=False)
    exc_count = train['has_exclamation'].sum()
    exc_pct = exc_count / len(train) * 100
    print(f"  ! (確実な読解): {exc_count} / {len(train)} ({exc_pct:.1f}%)")
    
    train['has_question'] = train['transliteration'].str.contains(r'\?', na=False)
    q_count = train['has_question'].sum()
    q_pct = q_count / len(train) * 100
    print(f"  ? (不確実な読解): {q_count} / {len(train)} ({q_pct:.1f}%)")
    
    train['has_slash'] = train['transliteration'].str.contains(r'/', na=False)
    slash_count = train['has_slash'].sum()
    slash_pct = slash_count / len(train) * 100
    print(f"  / (行区切り): {slash_count} / {len(train)} ({slash_pct:.1f}%)")
    
    train['has_colon'] = train['transliteration'].str.contains(r':', na=False)
    colon_count = train['has_colon'].sum()
    colon_pct = colon_count / len(train) * 100
    print(f"  : (語区切り): {colon_count} / {len(train)} ({colon_pct:.1f}%)")
    
    # 決定詞の中身分析
    print("\n--- 決定詞の内訳（TOP 20） ---")
    determinatives = []
    for text in train['transliteration'].dropna():
        # {} で囲まれたもの
        determinatives.extend(re.findall(r'\{(.*?)\}', text))
        # () で囲まれた determinatives
        determinatives.extend(re.findall(r'\(([a-z]+)\)', text))
    
    det_freq = Counter(determinatives)
    for det, count in det_freq.most_common(20):
        print(f"  {{{det}}}: {count} 回")
    
    # 特殊文字の頻度
    print("\n--- 特殊文字の出現頻度 ---")
    special_chars = {
        'Ḫ': r'Ḫ',
        'ḫ': r'ḫ',
        'š': r'š',
        'Š': r'Š',
        'ṣ': r'ṣ',
        'Ṣ': r'Ṣ',
        'ṭ': r'ṭ',
        'Ṭ': r'Ṭ',
    }
    
    for char, pattern in special_chars.items():
        count = train['transliteration'].str.count(pattern).sum()
        print(f"  {char}: {count} 回")
    
    # 下付き数字の頻度
    print("\n--- 下付き数字の出現頻度 ---")
    subscript_chars = '₀₁₂₃₄₅₆₇₈₉ₓ'
    for char in subscript_chars:
        count = train['transliteration'].str.count(re.escape(char)).sum()
        if count > 0:
            print(f"  {char}: {count} 回")
    
    return train


def analyze_vocabulary(train):
    """タスク項目4: 語彙・辞書情報との関係"""
    print_section("4. 語彙・辞書情報との関係")
    
    # OA_Lexicon_eBL.csv を読み込み
    print("--- OA_Lexicon_eBL.csv とのマッチング ---")
    lexicon = pd.read_csv(LEXICON_CSV)
    print(f"  Lexicon 総件数: {len(lexicon)}")
    print(f"  Lexicon カラム: {lexicon.columns.tolist()}")
    
    # train.transliteration から単語を抽出
    train_words = set()
    for text in train['transliteration'].dropna():
        train_words.update(text.split())
    
    print(f"\n  train のユニーク単語数: {len(train_words)}")
    
    # lexicon.form とのカバレッジ
    if 'form' in lexicon.columns:
        lexicon_forms = set(lexicon['form'].dropna())
        print(f"  lexicon.form のユニーク数: {len(lexicon_forms)}")
        
        matched = train_words & lexicon_forms
        coverage = len(matched) / len(train_words) * 100 if len(train_words) > 0 else 0
        print(f"  カバレッジ: {len(matched)} / {len(train_words)} ({coverage:.1f}%)")
    
    # 固有名詞（type=PN/GN）の割合
    if 'type' in lexicon.columns:
        pn_count = lexicon[lexicon['type'] == 'PN'].shape[0]
        gn_count = lexicon[lexicon['type'] == 'GN'].shape[0]
        print(f"\n  Lexicon 内の固有名詞:")
        print(f"    PN (Person Name): {pn_count} 件")
        print(f"    GN (Geographic Name): {gn_count} 件")
    
    # ロゴグラム（全大文字+ドット）の頻度
    print("\n--- ロゴグラム（全大文字 + ドット）の頻度 TOP 30 ---")
    logograms = []
    for text in train['transliteration'].dropna():
        # 全大文字 + オプションのドット区切り + 下付き数字
        logograms.extend(re.findall(r'\b[A-Z₀-₉]+(?:\.[A-Z₀-₉]+)*\b', text))
    
    logo_freq = Counter(logograms)
    for logo, count in logo_freq.most_common(30):
        print(f"  {logo}: {count} 回")
    
    return train


def analyze_translation_features(train):
    """タスク項目5: 英訳側の特徴"""
    print_section("5. 英訳側の特徴")
    
    print("--- 翻訳テキストの長さ統計（単語数） ---")
    print(train['translation_len_words'].describe([0.25, 0.5, 0.75, 0.95, 0.99]))
    
    # 固有名詞候補（大文字開始）
    print("\n--- 固有名詞候補（大文字開始トークン）TOP 30 ---")
    proper_nouns = []
    for text in train['translation'].dropna():
        # ハイフン付きもカバー（Šalim-Aššur など）
        proper_nouns.extend(re.findall(r'\b[A-Z][a-zāēīūàèìùáéíúḫšṣṭ-]+\b', text))
    
    pn_freq = Counter(proper_nouns)
    for pn, count in pn_freq.most_common(30):
        print(f"  {pn}: {count} 回")
    
    # 記号（句読点）の頻度
    print("\n--- 句読点の頻度 ---")
    symbols = [',', '.', ':', ';', '?', '!', '...', '"', '(', ')']
    for symbol in symbols:
        count = train['translation'].str.count(re.escape(symbol)).sum()
        print(f"  '{symbol}': {count} 回")
    
    # 引用符の使用頻度（対話形式の多さ）
    train['has_quotes'] = train['translation'].str.contains(r'"', na=False)
    quote_count = train['has_quotes'].sum()
    quote_pct = quote_count / len(train) * 100
    print(f"\n  引用符を含むサンプル: {quote_count} / {len(train)} ({quote_pct:.1f}%)")
    
    # 括弧の使用（注釈）
    train['has_parens'] = train['translation'].str.contains(r'\(.*?\)', na=False)
    paren_count = train['has_parens'].sum()
    paren_pct = paren_count / len(train) * 100
    print(f"  括弧 () を含むサンプル: {paren_count} / {len(train)} ({paren_pct:.1f}%)")
    
    # 省略記号 ... の頻度
    train['has_ellipsis_trans'] = train['translation'].str.contains(r'\.\.\.', na=False)
    ellipsis_trans_count = train['has_ellipsis_trans'].sum()
    ellipsis_trans_pct = ellipsis_trans_count / len(train) * 100
    print(f"  省略記号 ... を含むサンプル: {ellipsis_trans_count} / {len(train)} ({ellipsis_trans_pct:.1f}%)")
    
    # 数値表現のパターン
    print("\n--- 数値表現のパターン（サンプル） ---")
    numeric_patterns = []
    for text in train['translation'].dropna():
        # mina, shekel などの単位
        numeric_patterns.extend(re.findall(r'\d+(?:\.\d+)?\s+(?:mina|minas|shekel|shekels|talent|talents)', text, re.IGNORECASE))
    
    if numeric_patterns:
        num_freq = Counter(numeric_patterns)
        for pattern, count in num_freq.most_common(20):
            print(f"  {pattern}: {count} 回")
    else:
        print("  数値表現パターンが見つかりませんでした")
    
    return train


def summarize_findings(train):
    """タスク項目6: ベースライン実装へのフィードバック"""
    print_section("6. ベースライン実装へのフィードバック")
    
    print("--- 前処理の優先度（まとめ） ---")
    print("\n【優先度：高】必須の前処理")
    print("  1. Ḫ/ḫ → H/h の置換（test は H/h のみ）")
    print("  2. 書記記号の除去（! ? / : < > ˹ ˺ [ ]）")
    print("  3. determinatives の統一（(d) → {d} など）")
    print("  4. train の文単位分割（Sentences_Oare_FirstWord_LinNum.csv 利用）")
    
    print("\n【優先度：中】推奨の前処理")
    print("  5. 欠損マーカーの統一（[x] → <gap>, … → <big_gap>）")
    print("  6. 下付き数字の ASCII 化（₅ → 5）")
    
    print("\n【優先度：低】検討の前処理")
    print("  7. 翻訳の引用符正規化")
    print("  8. アクセント付き母音の統一（必要に応じて）")
    
    print("\n--- 長さ制御の方針 ---")
    avg_translit = train['translit_len_words'].mean()
    avg_trans = train['translation_len_words'].mean()
    p95_translit = train['translit_len_words'].quantile(0.95)
    p95_trans = train['translation_len_words'].quantile(0.95)
    
    print(f"  転写: 平均 {avg_translit:.1f} 単語、95%ile {p95_translit:.1f} 単語")
    print(f"  翻訳: 平均 {avg_trans:.1f} 単語、95%ile {p95_trans:.1f} 単語")
    print(f"  → モデル入力長: {int(p95_translit * 1.2)} トークン程度")
    print(f"  → モデル出力長: {int(p95_trans * 1.2)} トークン程度")
    
    print("\n--- 追加データの活用優先度 ---")
    print("  ベースライン: まず train.csv（約1,500件）のみで構築")
    print("  将来: published_texts.csv + publications.csv から追加学習データを抽出")
    print("  辞書: OA_Lexicon_eBL.csv を固有名詞の正規化に活用")


def main():
    """EDA 全体の実行"""
    print("=" * 80)
    print("  Deep Past Challenge - Baseline EDA")
    print("  タスク: task_baseline_eda_20260211123000")
    print("=" * 80)
    
    # 1. 基本構造の把握
    train, test, submission = analyze_basic_structure()
    
    # 2. 長さ・分布の確認
    train = analyze_length_distribution(train)
    
    # 3. 記号・表記の出現状況
    train = analyze_symbols(train)
    
    # 4. 語彙・辞書情報との関係
    train = analyze_vocabulary(train)
    
    # 5. 英訳側の特徴
    train = analyze_translation_features(train)
    
    # 6. ベースライン実装へのフィードバック
    summarize_findings(train)
    
    print("\n" + "=" * 80)
    print("  EDA 完了")
    print("  結果は results/eda_output.txt と results/figures/ に保存されています")
    print("=" * 80)


if __name__ == "__main__":
    # --out / -o で結果を UTF-8 のファイルに直接書き出し（リダイレクト時の文字化け防止）
    _out_file = None
    if len(sys.argv) >= 2 and sys.argv[1] in ("--out", "-o"):
        out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else RESULTS_DIR / "eda_output.txt"
        _out_file = open(out_path, "w", encoding="utf-8")
        sys.stdout = _out_file
    try:
        main()
    finally:
        if _out_file is not None:
            _out_file.close()
            sys.stdout = sys.__stdout__
