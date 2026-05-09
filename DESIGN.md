# 🎯 评分系统重新设计方案

**设计时间**: 2026-05-09 09:09  
**设计原则**: 关注币的本质（出身），而非市场表现（趋势）

---

## 📊 新评分体系架构

### 核心理念

```
最终评分（0-100分）:
  - 叙事热度 25%  （热点叙事是根本）
  - 真实性 25%    （是否刷量、bot）
  - 安全性 20%    （是否恶意、Rug）
  - 聪明钱 15%    （聪明钱认可度）
  - 推广投入 10%  （DexScreener等推广费用）
  - 流动性 5%     （资金安全性）
```

**设计理念**:
- 叙事是根本：没有好叙事，再安全也没人买
- 真实性是基础：刷量币再热也是垃圾
- 推广是信心：愿意花钱推广说明项目方有信心

---

## � 维度1: 叙事热度评分 (25%)

**目标**: 评估叙事的热度和持续性

### 叙事分类

#### 超级热点叙事 (90-100分)

```python
SUPER_HOT_NARRATIVES = {
    "ai": {
        "keywords": ["ai", "gpt", "llm", "agent", "chatgpt", "claude", "gemini"],
        "score": 95,
        "reason": "AI是当前最热赛道"
    },
    "名人": {
        "keywords": ["elon", "trump", "musk", "biden"],
        "score": 95,
        "reason": "名人效应强大"
    },
    "新闻热点": {
        "keywords": ["breaking", "viral", "trending", "news"],
        "score": 90,
        "reason": "新闻热点爆发力强"
    }
}
```

#### 主流热点叙事 (70-85分)

```python
MAINSTREAM_NARRATIVES = {
    "meme": {
        "keywords": ["pepe", "doge", "shib", "cat", "dog", "frog"],
        "score": 80,
        "reason": "MEME是永恒主题"
    },
    "defi": {
        "keywords": ["defi", "swap", "lending", "dao", "yield"],
        "score": 75,
        "reason": "DeFi有实际应用"
    },
    "gaming": {
        "keywords": ["game", "nft", "play", "metaverse"],
        "score": 70,
        "reason": "Gaming有用户基础"
    }
}
```

#### 普通叙事 (50-65分)

```python
NORMAL_NARRATIVES = {
    "solana生态": {
        "keywords": ["solana", "sol", "raydium", "jupiter"],
        "score": 60,
        "reason": "Solana生态币"
    },
    "社区币": {
        "keywords": ["community", "holder", "diamond"],
        "score": 55,
        "reason": "社区驱动"
    }
}
```

#### 无叙事/冷门 (20-40分)

```python
NO_NARRATIVE = {
    "score": 30,
    "reason": "无明确叙事，难以吸引关注"
}
```

### 叙事评分逻辑

```python
def narrative_score(symbol, token_name, description=""):
    """
    叙事热度评分
    
    返回: 20-100分
    """
    text = f"{symbol} {token_name} {description}".lower()
    
    # 1. 检查超级热点
    for narrative, config in SUPER_HOT_NARRATIVES.items():
        for keyword in config["keywords"]:
            if keyword in text:
                return config["score"]
    
    # 2. 检查主流热点
    for narrative, config in MAINSTREAM_NARRATIVES.items():
        for keyword in config["keywords"]:
            if keyword in text:
                return config["score"]
    
    # 3. 检查普通叙事
    for narrative, config in NORMAL_NARRATIVES.items():
        for keyword in config["keywords"]:
            if keyword in text:
                return config["score"]
    
    # 4. 无叙事
    return NO_NARRATIVE["score"]
```

**权重**: 25%（最重要维度之一）

**示例**:
```
"AI AGENT" → 95分 (超级热点)
"PEPE DOG" → 80分 (主流热点)
"SOL COMMUNITY" → 60分 (普通叙事)
"RANDOM TOKEN" → 30分 (无叙事)
```

---

## � 维度2: 真实性评分 (25%)

**目标**: 检测是否bot刷量、假交易

### 检测指标

#### 1.1 新钱包占比检测

```python
def check_new_wallet_ratio(signal):
    """
    新钱包占比：反映是否有大量bot账号
    
    数据来源: tag_users_holding_percent.new_volume
    """
    ratio = signal.new_wallet_ratio
    
    if ratio < 0.30:      # <30% 非常健康
        return 100
    elif ratio < 0.40:    # 30-40% 正常
        return 85
    elif ratio < 0.50:    # 40-50% 一般
        return 70
    elif ratio < 0.60:    # 50-60% 可疑
        return 50
    else:                 # >60% 严重刷量
        return 20
```

**权重**: 40%

---

#### 1.2 垃圾钱包占比检测

```python
def check_shit_wallet_ratio(signal):
    """
    垃圾钱包占比：反映是否有专业刷量团队
    
    数据来源: tag_users_holding_percent.shit_volume
    """
    ratio = signal.shit_wallet_ratio
    
    if ratio < 0.02:      # <2% 非常干净
        return 100
    elif ratio < 0.05:    # 2-5% 可接受
        return 80
    elif ratio < 0.10:    # 5-10% 可疑
        return 50
    else:                 # >10% 严重刷量
        return 10
```

**权重**: 40%

---

#### 1.3 交易地址数量检测

```python
def check_buyer_count(signal):
    """
    交易地址数量：反映真实参与度
    
    数据来源: buyer_count_d1
    """
    count = signal.buyer_count
    
    if count > 500:       # >500 非常活跃
        return 100
    elif count > 300:     # 300-500 活跃
        return 90
    elif count > 200:     # 200-300 正常
        return 80
    elif count > 100:     # 100-200 一般
        return 70
    else:                 # <100 冷清
        return 40
```

**权重**: 20%

---

### 真实性总分计算

```python
def authenticity_score(signal):
    """真实性评分 (35%)"""
    
    new_wallet_score = check_new_wallet_ratio(signal)
    shit_wallet_score = check_shit_wallet_ratio(signal)
    buyer_count_score = check_buyer_count(signal)
    
    # 加权平均
    score = (
        new_wallet_score * 0.40 +
        shit_wallet_score * 0.40 +
        buyer_count_score * 0.20
    )
    
    return round(score, 1)
```

**示例**:
```
新钱包占比: 35% → 85分
垃圾钱包占比: 3% → 80分
交易地址: 250 → 80分

真实性 = 85*0.4 + 80*0.4 + 80*0.2 = 82分
```

---

## 🛡️ 维度2: 安全性评分 (35%)

**目标**: 检测是否有恶意行为、Rug风险

### 检测指标

#### 2.1 开发者行为检测

```python
def check_dev_behavior(ca, signal):
    """
    开发者行为：是否大量抛售
    
    需要新增数据:
    - dev_wallet_address
    - dev_sold_ratio (开发者卖出比例)
    """
    dev_sold_ratio = get_dev_sold_ratio(ca)
    
    if dev_sold_ratio is None:
        return 70  # 无法获取，给中等分
    
    if dev_sold_ratio < 0.05:     # <5% 未抛售
        return 100
    elif dev_sold_ratio < 0.20:   # 5-20% 小幅抛售
        return 80
    elif dev_sold_ratio < 0.50:   # 20-50% 大量抛售
        return 40
    else:                          # >50% 疑似Rug
        return 10
```

**权重**: 40%

---

#### 2.2 合约安全检测

```python
def check_contract_safety(ca):
    """
    合约安全：是否有后门、权限问题
    
    需要新增数据:
    - is_mintable (是否可增发)
    - is_freezable (是否可冻结)
    - ownership_renounced (是否放弃权限)
    """
    score = 100
    
    # 可增发 → 扣分
    if is_mintable(ca):
        score -= 30
    
    # 可冻结 → 扣分
    if is_freezable(ca):
        score -= 30
    
    # 未放弃权限 → 扣分
    if not ownership_renounced(ca):
        score -= 20
    
    return max(score, 0)
```

**权重**: 30%

---

#### 2.3 流动性锁定检测

```python
def check_liquidity_lock(ca):
    """
    流动性锁定：是否锁定流动性
    
    需要新增数据:
    - liquidity_locked
    - lock_duration (锁定时长)
    """
    if not liquidity_locked(ca):
        return 50  # 未锁定
    
    lock_days = get_lock_duration(ca)
    
    if lock_days > 365:       # >1年
        return 100
    elif lock_days > 180:     # 6个月-1年
        return 90
    elif lock_days > 90:      # 3-6个月
        return 80
    elif lock_days > 30:      # 1-3个月
        return 70
    else:                     # <1个月
        return 60
```

**权重**: 30%

---

### 安全性总分计算

```python
def safety_score(ca, signal):
    """安全性评分 (35%)"""
    
    dev_score = check_dev_behavior(ca, signal)
    contract_score = check_contract_safety(ca)
    lock_score = check_liquidity_lock(ca)
    
    # 加权平均
    score = (
        dev_score * 0.40 +
        contract_score * 0.30 +
        lock_score * 0.30
    )
    
    # 一票否决：如果有Rug历史，直接0分
    if has_rug_history(get_dev_wallet(ca)):
        return 0
    
    return round(score, 1)
```

**示例**:
```
开发者抛售: 8% → 80分
合约安全: 无后门 → 100分
流动性锁定: 6个月 → 90分

安全性 = 80*0.4 + 100*0.3 + 90*0.3 = 89分
```

---

## 💰 维度3: 聪明钱评分 (20%)

**目标**: 聪明钱是否认可

### 检测指标

```python
def smart_money_score(signal):
    """
    聪明钱评分：聪明钱占比
    
    数据来源: smart_money_ratio
    """
    ratio = signal.smart_money_ratio
    
    # 降低阈值（之前30%太高）
    if ratio > 0.15:      # >15% 顶级
        return 100
    elif ratio > 0.10:    # 10-15% 优秀
        return 90
    elif ratio > 0.05:    # 5-10% 良好
        return 75
    elif ratio > 0.02:    # 2-5% 一般
        return 60
    else:                 # <2% 较差
        return 40
```

**权重**: 100%（单一指标）

**示例**:
```
聪明钱占比: 8% → 75分
```

---

## � 维度4: 推广投入评分 (10%)

**目标**: 评估项目方的推广投入和信心

### 检测指标

#### 4.1 DexScreener推广检测

```python
def check_dexscreener_ads(ca):
    """
    DexScreener推广检测
    
    需要新增数据:
    - has_dexscreener_ads (是否有DexScreener推广)
    - dex_ad_duration (推广持续时间，天)
    - dex_ad_position (推广位置: trending/promoted)
    """
    if not has_dexscreener_ads(ca):
        return 40  # 无推广
    
    duration = get_dex_ad_duration(ca)
    position = get_dex_ad_position(ca)
    
    score = 60  # 基础分
    
    # 推广位置加分
    if position == "trending":
        score += 20  # Trending位置
    elif position == "promoted":
        score += 30  # Promoted位置（更贵）
    
    # 持续时间加分
    if duration >= 7:
        score += 10  # 推广7天以上
    elif duration >= 3:
        score += 5   # 推广3-7天
    
    return min(score, 100)
```

**权重**: 40%

---

#### 4.2 社交媒体推广检测

```python
def check_social_promotion(ca):
    """
    社交媒体推广检测
    
    需要新增数据:
    - twitter_followers (Twitter粉丝数)
    - telegram_members (Telegram成员数)
    - has_kol_promotion (是否有KOL推广)
    """
    score = 50  # 基础分
    
    # Twitter粉丝
    followers = get_twitter_followers(ca)
    if followers > 10000:
        score += 20
    elif followers > 5000:
        score += 15
    elif followers > 1000:
        score += 10
    
    # Telegram成员
    members = get_telegram_members(ca)
    if members > 5000:
        score += 15
    elif members > 1000:
        score += 10
    elif members > 500:
        score += 5
    
    # KOL推广
    if has_kol_promotion(ca):
        score += 15
    
    return min(score, 100)
```

**权重**: 30%

---

#### 4.3 网站和文档质量

```python
def check_website_quality(ca):
    """
    网站和文档质量检测
    
    需要新增数据:
    - has_website (是否有官网)
    - has_whitepaper (是否有白皮书)
    - website_quality_score (网站质量评分)
    """
    score = 40  # 基础分
    
    if has_website(ca):
        score += 20
        
        # 网站质量
        quality = get_website_quality_score(ca)
        if quality > 80:
            score += 20
        elif quality > 60:
            score += 10
    
    if has_whitepaper(ca):
        score += 20
    
    return min(score, 100)
```

**权重**: 30%

---

### 推广投入总分计算

```python
def promotion_score(ca):
    """推广投入评分 (10%)"""
    
    dex_score = check_dexscreener_ads(ca)
    social_score = check_social_promotion(ca)
    website_score = check_website_quality(ca)
    
    # 加权平均
    score = (
        dex_score * 0.40 +
        social_score * 0.30 +
        website_score * 0.30
    )
    
    return round(score, 1)
```

**示例**:
```
DexScreener推广: Promoted位置 + 7天 → 100分
Twitter粉丝: 8000 → 75分
有官网+白皮书 → 80分

推广投入 = 100*0.4 + 75*0.3 + 80*0.3 = 86.5分
```

**说明**:
- 愿意花钱推广 = 项目方有信心
- DexScreener推广很贵，能上说明不是骗子
- 社交媒体活跃度反映真实热度

---

## �💧 维度5: 流动性评分 (5%)

**目标**: 资金安全性

### 检测指标

```python
def liquidity_score(signal):
    """
    流动性评分：流动性/市值比率
    
    数据来源: pool_liquidity / mcap
    """
    liq_ratio = signal.pool_liquidity / signal.mcap if signal.mcap > 0 else 0
    
    # 降低阈值（之前50%太高）
    if liq_ratio > 0.30:      # >30% 非常充足
        return 100
    elif liq_ratio > 0.20:    # 20-30% 充足
        return 90
    elif liq_ratio > 0.10:    # 10-20% 正常
        return 75
    elif liq_ratio > 0.05:    # 5-10% 一般
        return 60
    else:                     # <5% 不足
        return 30
```

**权重**: 100%（单一指标）

**示例**:
```
流动性比率: 15% → 75分
```

---

## 🎯 最终评分计算

### 公式

```python
def calculate_final_rating(ca, signal, symbol, token_name, description=""):
    """
    最终评分 = 各维度加权求和
    
    范围: 0-100分
    """
    
    # 1. 叙事热度 (25%)
    narrative = narrative_score(symbol, token_name, description)
    
    # 2. 真实性 (25%)
    authenticity = authenticity_score(signal)
    
    # 3. 安全性 (20%)
    safety = safety_score(ca, signal)
    
    # 4. 聪明钱 (15%)
    smart_money = smart_money_score(signal)
    
    # 5. 推广投入 (10%)
    promotion = promotion_score(ca)
    
    # 6. 流动性 (5%)
    liquidity = liquidity_score(signal)
    
    # 加权求和
    final_score = (
        narrative * 0.25 +
        authenticity * 0.25 +
        safety * 0.20 +
        smart_money * 0.15 +
        promotion * 0.10 +
        liquidity * 0.05
    )
    
    return {
        "rating": round(final_score, 1),
        "breakdown": {
            "narrative": round(narrative, 1),
            "authenticity": round(authenticity, 1),
            "safety": round(safety, 1),
            "smart_money": round(smart_money, 1),
            "promotion": round(promotion, 1),
            "liquidity": round(liquidity, 1)
        }
    }
```

---

## 📊 评分示例

### 示例1: 顶级AI币（有DexScreener推广）

```python
# 输入数据
signal = {
    "new_wallet_ratio": 0.35,      # 35%
    "shit_wallet_ratio": 0.03,     # 3%
    "buyer_count": 350,
    "smart_money_ratio": 0.12,     # 12%
    "pool_liquidity": 50000,
    "mcap": 300000,                # 流动性比率 16.7%
}
symbol = "AI AGENT"
token_name = "GPT Agent"
has_dexscreener_ads = True         # 有DexScreener推广
dex_ad_position = "promoted"       # Promoted位置
twitter_followers = 8000

# 计算过程
narrative = 95分 (AI超级热点)
authenticity = 85*0.4 + 80*0.4 + 90*0.2 = 84分
safety = 80*0.4 + 100*0.3 + 90*0.3 = 89分
smart_money = 90分
promotion = 100*0.4 + 75*0.3 + 80*0.3 = 86.5分
liquidity = 75分

final_score = 95*0.25 + 84*0.25 + 89*0.20 + 90*0.15 + 86.5*0.10 + 75*0.05
            = 23.75 + 21 + 17.8 + 13.5 + 8.65 + 3.75
            = 88.45分
```

**结果**: ⭐⭐⭐⭐⭐ **88.5分（顶级）**

**分析**:
- ✅ AI热点叙事（95分）
- ✅ 真实交易（84分）
- ✅ 安全可靠（89分）
- ✅ 聪明钱认可（90分）
- ✅ 重金推广（86.5分）
- ✅ 流动性充足（75分）

---

### 示例2: 普通MEME币（无推广）

```python
# 输入数据
signal = {
    "new_wallet_ratio": 0.45,      # 45%
    "shit_wallet_ratio": 0.04,     # 4%
    "buyer_count": 200,
    "smart_money_ratio": 0.06,     # 6%
    "pool_liquidity": 30000,
    "mcap": 250000,                # 流动性比率 12%
}
symbol = "PEPE DOG"
token_name = "Pepe Dog Coin"
has_dexscreener_ads = False        # 无推广
twitter_followers = 1200

# 计算过程
narrative = 80分 (MEME主流热点)
authenticity = 70*0.4 + 80*0.4 + 80*0.2 = 76分
safety = 80*0.4 + 70*0.3 + 80*0.3 = 77分
smart_money = 75分
promotion = 40*0.4 + 60*0.3 + 60*0.3 = 52分 (无DexScreener推广)
liquidity = 75分

final_score = 80*0.25 + 76*0.25 + 77*0.20 + 75*0.15 + 52*0.10 + 75*0.05
            = 20 + 19 + 15.4 + 11.25 + 5.2 + 3.75
            = 74.6分
```

**结果**: ⭐⭐⭐⭐ **74.6分（良好）**

**分析**:
- ✅ MEME热点（80分）
- ✅ 真实交易（76分）
- ✅ 安全可靠（77分）
- ✅ 聪明钱认可（75分）
- ⚠️ 推广不足（52分）← 拉低总分
- ✅ 流动性充足（75分）

---

### 示例3: 刷量垃圾币（无叙事）

```python
# 输入数据
signal = {
    "new_wallet_ratio": 0.70,      # 70% ⚠️
    "shit_wallet_ratio": 0.12,     # 12% ⚠️
    "buyer_count": 80,
    "smart_money_ratio": 0.01,     # 1%
    "pool_liquidity": 5000,
    "mcap": 100000,                # 流动性比率 5%
}
symbol = "RANDOM COIN"
token_name = "Random Token"
has_dexscreener_ads = False
twitter_followers = 200

# 计算过程
narrative = 30分 (无叙事) ⚠️
authenticity = 20*0.4 + 10*0.4 + 40*0.2 = 20分 ⚠️
safety = 50*0.4 + 70*0.3 + 60*0.3 = 59分
smart_money = 40分
promotion = 40*0.4 + 50*0.3 + 40*0.3 = 43分
liquidity = 60分

final_score = 30*0.25 + 20*0.25 + 59*0.20 + 40*0.15 + 43*0.10 + 60*0.05
            = 7.5 + 5 + 11.8 + 6 + 4.3 + 3
            = 37.6分
```

**结果**: ⭐ **37.6分（垃圾）**

**分析**:
- ❌ 无叙事（30分）← 致命伤
- ❌ 严重刷量（20分）← 致命伤
- ⚠️ 安全性一般（59分）
- ❌ 聪明钱不认可（40分）
- ❌ 无推广（43分）
- ⚠️ 流动性不足（60分）

---

## 🎯 买入/卖出阈值

### 阈值设定

```python
RATING_THRESHOLD = 60      # 买入阈值（提高到60）
RATING_SELL_THRESHOLD = 45 # 卖出阈值（提高到45）
```

**理由**:
- 新评分系统更严格
- 60分以上才是真正的好币
- 45分以下说明本质有问题

---

### 评分等级

```
90-100分: ⭐⭐⭐⭐⭐ 顶级（稀有）
75-89分:  ⭐⭐⭐⭐   优秀（可买）
60-74分:  ⭐⭐⭐     良好（可买）
45-59分:  ⭐⭐       一般（观察）
30-44分:  ⭐         较差（不买）
0-29分:   ❌         垃圾（拉黑）
```

---

## 🔄 与Phase2的配合

### Phase2 Filter → 初筛

```python
# phase2_filter.py 保持不变
- 创建时间 >= 前一天23点
- 生命周期 < 20小时
- 信号收益率 > 100%
- 当前市值 > 40k
- 历史最高市值 > 180k
- 交易地址 > 100
- 新钱包占比 < 60%
- 垃圾钱包占比 < 5%
```

**作用**: 快速过滤明显的垃圾币

---

### Rating System → 精筛

```python
# 评分系统（新设计）
- 真实性评分 35%
- 安全性评分 35%
- 聪明钱评分 20%
- 流动性评分 10%
- 叙事加成 0.8-1.3倍
```

**作用**: 深度评估币的本质

---

### 配合流程

```
LogEarn 24h信号
  ↓
Phase2 Filter（初筛）
  ├─ 不符合 → 丢弃
  └─ 符合 → 进入候选池
       ↓
Rating System（精筛）
  ├─ <60分 → 禁止买入
  ├─ 60-74分 → 允许买入（谨慎）
  └─ ≥75分 → 允许买入（推荐）
       ↓
Phase2 Trading
```

---

## 📊 数据需求

### 当前已有数据 ✅

```
- new_wallet_ratio (新钱包占比)
- shit_wallet_ratio (垃圾钱包占比)
- buyer_count (交易地址数)
- smart_money_ratio (聪明钱占比)
- pool_liquidity (流动性)
- mcap (市值)
- symbol, token_name (币名)
```

---

### 需要新增数据 ⚠️

```
1. 开发者行为
   - dev_wallet_address (开发者钱包)
   - dev_sold_ratio (开发者卖出比例)
   - rug_history (Rug历史)

2. 合约安全
   - is_mintable (是否可增发)
   - is_freezable (是否可冻结)
   - ownership_renounced (是否放弃权限)

3. 流动性锁定
   - liquidity_locked (是否锁定)
   - lock_duration (锁定时长)
```

**优先级**:
- P0: dev_sold_ratio, rug_history
- P1: liquidity_locked, lock_duration
- P2: is_mintable, is_freezable, ownership_renounced

---

## 🎯 实施步骤

### 阶段1: 基础版（使用现有数据）

```python
# 只用现有数据实现
def calculate_rating_v1(signal, symbol, token_name):
    """基础版：只用现有数据"""
    
    # 真实性（35%）
    authenticity = (
        check_new_wallet_ratio(signal) * 0.40 +
        check_shit_wallet_ratio(signal) * 0.40 +
        check_buyer_count(signal) * 0.20
    )
    
    # 安全性（35%）- 简化版
    safety = 70  # 默认70分（无法检测）
    
    # 聪明钱（20%）
    smart_money = smart_money_score(signal)
    
    # 流动性（10%）
    liquidity = liquidity_score(signal)
    
    # 本质评分
    base_score = (
        authenticity * 0.35 +
        safety * 0.35 +
        smart_money * 0.20 +
        liquidity * 0.10
    )
    
    # 叙事加成
    multiplier = get_narrative_multiplier(symbol, token_name)
    
    return base_score * multiplier
```

---

### 阶段2: 完整版（新增数据后）

```python
# 完整版：包含所有检测
def calculate_rating_v2(ca, signal, symbol, token_name):
    """完整版：包含安全性检测"""
    
    authenticity = authenticity_score(signal)
    safety = safety_score(ca, signal)  # 完整安全检测
    smart_money = smart_money_score(signal)
    liquidity = liquidity_score(signal)
    
    base_score = (
        authenticity * 0.35 +
        safety * 0.35 +
        smart_money * 0.20 +
        liquidity * 0.10
    )
    
    multiplier = get_narrative_multiplier(symbol, token_name)
    
    return base_score * multiplier
```

---

## 📊 对比：旧 vs 新

### 旧评分系统

```
叙事 25% → 关键词匹配
链上 45% → 包含年龄、信号（重复计算）
信号 20% → 收益率
流动性 10%

问题:
❌ 信号分数算了2次
❌ 关注趋势而非本质
❌ 阈值过高（30%聪明钱）
❌ 缺少安全性检测
```

---

### 新评分系统

```
真实性 35% → bot检测、刷量检测
安全性 35% → 开发者行为、合约安全
聪明钱 20% → 聪明钱占比（降低阈值）
流动性 10% → 流动性比率（降低阈值）
叙事加成 0.8-1.3倍 → 热点加成

优势:
✅ 关注币的本质（出身）
✅ 严格的安全检测
✅ 合理的阈值
✅ 叙事作为加成而非主体
```

---

## 🎯 总结

### 核心改进

1. **评分维度重构**
   - 移除：年龄、信号收益率
   - 新增：真实性、安全性
   - 保留：聪明钱、流动性
   - 叙事改为加成

2. **阈值优化**
   - 聪明钱：30% → 15%
   - 流动性：50% → 30%
   - 买入阈值：50 → 60

3. **关注本质**
   - ✅ 是否刷量
   - ✅ 是否恶意
   - ✅ 是否安全
   - ❌ 不关注价格趋势

---

### 预期效果

- **更准确**: 关注币的本质而非市场表现
- **更安全**: 严格的安全性检测
- **更合理**: 叙事作为加成而非主体
- **更实用**: 阈值符合实际情况

---

**设计完成时间**: 2026-05-09 09:09  
**下一步**: 实现基础版（使用现有数据）
