---
id: 20260211150000
title: Deep Past Challenge - train.csv の文書ジャンルと文体
author: takeikumi
type: permanent
tags:
  - kaggle
  - machine-translation
  - deep-past
  - data
  - genre
links:
  - deep_past_dataset_overview_20260211121000
  - deep_past_eda_results_20260211140000
  - deep_past_competition_overview_structure_20260210110000
created: 2026-02-11
updated: 2026-02-11
---

# Deep Past Challenge - train.csv の文書ジャンルと文体

`train.csv` に含まれる英訳（`translation`）を手がかりに、データセットがどのような文書からなるか整理する。

## 1. 主な文書ジャンル・形式

### 1.1 商業・法律文書（契約・証書）

- **借金・貸付契約（debt/loan contracts）**
  - 銀（KÙ.BABBAR）、銅（URUDU）、錫（AN.NA）の貸借
  - 返済期限・利子条項（例: 1.5 GÍN per mina per month）
  - 封（KIŠIB）と証人の列挙
- **商業記録（business records）**
  - 織物（TÚG, kutānu）、ロバ、銅・錫の在庫・取引記録
  - 税・関税（niṣḫātum, šaddu'ātum）の記録
- **証人付きの証言・判決記録**
  - 「Kanesh 植民地が私たちに裁きを下した」（The Kanesh colony gave us for these proceedings）
  - 「アッシュルの短剣の前で証言した」（we gave our testimony before Aššur's dagger）

### 1.2 私信・書簡（letters）

- **定型の宛先表示**
  - "From X to Y: say..."（X から Y へ。こう言え…）
  - 仲介者に「Y に言え」と託す形式
- **内容**
  - 銀・銅・織物の送付依頼・確認
  - 裁判・債務処理の進捗報告
  - 親族への指示・遺言の言及
- **感情的な表現**
  - "Urgent!"（至急）、"My dear brother"（兄弟よ）
  - "Do not obstruct me!"（私を妨げるな）

### 1.3 目録・一覧

- **粘土板のリスト**
  - 「Puzur-Aššur と Puzur-Adad の銀 10 ミナについての粘土板」など
- **配分・払い戻しの記録**
  - 銀・銅・織物の数量と受け取り者

## 2. 時代・地理・言語

- **時代**: 古アッシリア期（Old Assyrian period）、おおよそ **紀元前 2000–1700 年**
- **地理**: 主に **カネシュ（Kültepe、トルコ）** の古アッシリア商業植民地
- **言語**: **アッカド語** の古アッシリア方言。転写はローマ字化された楔形文字
- **固有名**: アッシリア系人名（例: Ennam-Aššur, Ali-ahum）、神名（Šamaš, Ištar）、地名（Aššur, Kanesh, Burušhaddum）が頻出

## 3. 文体・表現の特徴

### 3.1 定型的表現

- **封・証人**: "Seal of X, seal of Y... Witnessed by A, by B"
- **宛先**: "To X from Y: say, thus says Z..."
- **債務**: "X owes Y minas of silver to Z"
- **時系列**: 月名（ITU.KAM）、週（ḫamuštum）、名年（limum）による日付

### 3.2 数値・単位

- **重量**: ミナ（ma-na）、シェケル（GÍN）、タラント（GÚ）
- **通貨・物品**: 銀（KÙ.BABBAR）、金（KÙ.GI）、銅（URUDU）、錫（AN.NA）
- **分数**: 0.33333 ma-na（1/3 ミナ）、0.5 GÍN など十進的な表記

### 3.3 固有名詞の多さ

- 人名・地名・神名が多く、大文字始まりの固有名詞や ALL CAPS のロゴグラム（例: KÙ.BABBAR, DUMU）が頻出
- ベースラインの EDA でも「先頭大文字トークン」「固有名詞らしき表現」が多数観察される

## 4. 英訳の日本語訳サンプル

以下、`train.csv` の英訳からいくつかを日本語に訳した例。

### 例 1: 借金契約（短い証書）

**英訳**:  
"Seal of Mannum-balum-Aššur son of Ṣilli-Adad, seal of Šu-Illil son of Mannum-kī-Aššur, seal of Puzur-Aššur son of Ataya. Puzur-Aššur son of Ataya owes 22 shekels of good silver to Ali-ahum. Reckoned from the week of Ilī-dan, month of Ša-kēnātim, in the eponymy of Enna-Suen, he will pay in 14 weeks. If he has not paid in time, he will add interest at the rate 1.5 shekel per mina per month."

**日本語訳**:  
「Ṣilli-Adad の子 Mannum-balum-Aššur の封、Mannum-kī-Aššur の子 Šu-Illil の封、Ataya の子 Puzur-Aššur の封。Ataya の子 Puzur-Aššur は Ali-ahum に良質の銀 22 シェケルを負っている。Ilī-dan の週、Ša-kēnātim の月、Enna-Suen の名年のもと、14 週以内に支払う。期日までに支払わない場合、1 ミナあたり月 1.5 シェケルの利子を加える。」

### 例 2: 私信（織物の受け取り）

**英訳**:  
"Itūr-ilī has received one textile of ordinary quality."

**日本語訳**:  
「Itūr-ilī が普通品質の織物を 1 着受け取った。」

### 例 3: 書簡の一部（商業指示）

**英訳**:  
"From Šukkutum to Ištar-lamassī and Nitahšušar: Why is that you (fem. plur.) have written me, saying: The house is no longer a house. Urgent, to Ennam-Aššur... Do not fear!. To Ištar-lamassī: If you are truly my sister, then encourage her. Do not fear. To Nitahšušar: Air the textiles that I left. Also, the tablets should be guarded."

**日本語訳**:  
「Šukkutum から Ištar-lamassī と Nitahšušar へ：あなた方が私に『家はもはや家ではない』と書き送ったのはなぜか。至急、Ennam-Aššur に…恐れるな。Ištar-lamassī へ：あなたが真に私の姉妹なら、彼女を励ましてほしい。恐れるな。Nitahšušar へ：私が残した織物に風を通せ。また、粘土板は守るように。」

### 例 4: 目録（粘土板のリスト）

**英訳**:  
"A tablet about 10 minas of silver of Puzur-Assur and Puzur-Adad; a tablet about 4 minas of silver of Puzur-Assur; a tablet about 10 minas of silver of Asanum; a tablet about 10 minas of silver of Alpili; a tablet about 10 minas of silver of Asanum and Puzur-Istar; a tablet about 5 minas of silver of Assur-sululi; a tablet about 17 minas and 15 shekels of silver of Ennanatum; a tablet about a debt of our father, I obtained it in Kuburnat."

**日本語訳**:  
「Puzur-Assur と Puzur-Adad の銀 10 ミナについての粘土板；Puzur-Assur の銀 4 ミナについての粘土板；Asanum の銀 10 ミナについての粘土板；Alpili の銀 10 ミナについての粘土板；Asanum と Puzur-Ištar の銀 10 ミナについての粘土板；Assur-sululi の銀 5 ミナについての粘土板；Ennanatum の銀 17 ミナ 15 シェケルについての粘土板；私たちの父の借金についての粘土板を、Kuburnat で入手した。」

### 例 5: 商業報告（短い）

**英訳**:  
"To Ali-ahum from Puzur-Aššur: 0.5 mina of silver that I acquired for myself(?) and you sent to me, 0.5 mina of silver under my seal Ennānum son of Kuziya brought to you. My dear brother, pay attention to the missives from the City that Ennānum brought to you, and give it (an answer?) to the very first express transport so they may bring it."

**日本語訳**:  
「Puzur-Aššur から Ali-ahum へ：私が自分のために手に入れ、あなたが送ってくれた銀 0.5 ミナ、私の封のある銀 0.5 ミナを Kuziya の子 Ennānum があなたのもとに届けた。兄弟よ、Ennānum が届けた都市からの書簡に注意し、最初の飛脚便に（返答を？）託して届けさせるように。」

## 5. ベースライン実装への示唆

- **固有名詞の扱い**: 人名・地名・神名が多いため、大文字やロゴグラムをそのまま残すか、正規化するかを前処理で決める必要がある
- **定型句の学習**: "Seal of...", "Witnessed by...", "From X to Y: say..." など定型表現はモデルが習得しやすい可能性
- **数字・単位**: 分数表記（0.33333 など）や mina/shekel の扱いを一貫させる
- **文長**: 書簡は長く、証書・目録は短いことが多い。文単位で分割する場合は長さ分布に注意
