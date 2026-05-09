# logearn-rating-skill 评分系统文档

## 概述

独立评分系统，不依赖 Phase2，可单独运行。
数据来源：GMGN API + DexScreener Boost API + LogEarn 信号过滤链（已过滤rug/刷量等垃圾币）。

---

## 一、评分维度总览

| 维度 | 权重 | 数据来源 | 说明 |
|------|------|----------|------|
| 叙事 Narrative | 25% | 人工/外部 | 5子维度加权 + 关键词Tier |
| 安全性 Safety | 30% | GMGN | dev行为 + 流动性锁定 |
| 聪明钱 SmartMoney | 20% | GMGN | 聪明钱占比 |
| 推广 Promotion | 15% | DexScreener + GMGN | Boost金额 + 社交媒体 |
| 流动性 Liquidity | 10% | GMGN | 流动性/市值比 |

**评分范围**：0~100分
**买入阈值**：≥60分 ✅ 可以买入

---

## 二、数据结构 TokenSignal

```
TokenSignal {
    # 必要字段
    ca: str                    # 合约地址
    symbol: str                # 代币符号
    token_name: str            # 代币名称
    description: str           # 描述（用于关键词匹配）

    # 叙事子维度（0~1）
    narrative_credibility: float   # 可信度
    narrative_kol_approval: float  # KOL认可度
    narrative_community: float     # 社区活跃度
    narrative_purity: float       # 叙事纯度
    narrative_sentiment: float    # 市场情绪（默认0.5）

    # 聪明钱
    smart_money_ratio: float      # 聪明钱占比 = smart_holders数 / holder_count

    # 流动性
    pool_liquidity: float        # 流动性（USD）
    mcap: float                  # 市值（USD）

    # 推广
    has_dexscreener_ads: bool    # 是否有DexScreener广告
    dex_ad_position: str         # "promoted" | "trending" | ""
    dex_ad_duration: int          # 推广天数
    dex_boost_amount: float      # DexScreener Boost总预算（U）
    twitter_followers: int         # Twitter粉丝数
    telegram_members: int          # Telegram成员数
    has_kol_promotion: bool       # 是否有KOL推广
    has_website: bool             # 是否有官网
    has_whitepaper: bool          # 是否有白皮书

    # 安全性
    dev_sold_ratio: float        # 开发者卖出比例
    has_rug_history: bool         # 是否有Rug历史
    liquidity_locked: bool        # 流动性是否锁定
    lock_duration: int            # 锁定天数
}
```

---

## 三、各维度评分细则

### 3.1 叙事 Narrative（权重 25%）

**流程**：

```
输入：5个子维度 + symbol + name + description

STEP 1: 子维度加权
    base = Σ(weight × field_value)

    ┌─────────────────┬──────┐
    │ credibility    │ 30%  │
    │ kol_approval   │ 20%  │
    │ community      │ 20%  │
    │ purity         │ 15%  │
    │ sentiment      │ 15%  │
    └─────────────────┴──────┘

STEP 2: 关键词 Tier（30% 权重）
    text = symbol + token_name + description（转小写）

    SUPER_HOT（优先匹配）:
        ai/celebrity/news → 95分

    MAINSTREAM:
        meme → 80分
        defi → 75分
        gaming → 70分

    NORMAL:
        solana → 60分
        community → 55分

    未命中 → keyword_score = 0

STEP 3: 最终分数
    if keyword_score == 0:
        return base × 100

    total = base × 0.7 + keyword_score × 0.3
    return clamp(total, 0, 1) × 100
```

**关键词定义**：

```python
SUPER_HOT_NARRATIVES = {
    "ai":       {"keywords": ["ai","gpt","llm","agent","chatgpt","claude","gemini"], "score": 95},
    "celebrity": {"keywords": ["elon","trump","musk","biden"],                     "score": 95},
    "breaking": {"keywords": ["breaking","viral","trending","news"],               "score": 90},
}

MAINSTREAM_NARRATIVES = {
    "meme":   {"keywords": ["pepe","doge","shib","cat","dog","frog"], "score": 80},
    "defi":   {"keywords": ["defi","swap","lending","dao","yield"],  "score": 75},
    "gaming": {"keywords": ["game","nft","play","metaverse"],        "score": 70},
}

NORMAL_NARRATIVES = {
    "solana":   {"keywords": ["solana","sol","raydium","jupiter"],   "score": 60},
    "community":{"keywords": ["community","holder","diamond"],        "score": 55},
}
```

---

### 3.2 安全性 Safety（权重 30%）

**公式**：`safety = dev_behavior×0.40 + contract_score×0.30 + lock_score×0.30`

#### check_dev_behavior（开发者卖出比例）

| dev_sold_ratio | 分数 |
|----------------|------|
| < 5%           | 100  |
| < 20%          | 80   |
| < 50%          | 40   |
| ≥ 50%          | 10   |
| has_rug_history = True | **0（一票否决）** |

#### check_liquidity_lock（流动性锁定）

| 条件 | 分数 |
|------|------|
| 未锁定 | 50 |
| 锁定 ≤ 30天 | 60 |
| 锁定 ≤ 90天 | 70 |
| 锁定 ≤ 180天 | 80 |
| 锁定 ≤ 365天 | 90 |
| 锁定 > 365天 | 100 |

#### contract_score
默认 70分（需要合约检测数据才能更精确）

**示例**：UAP
- dev_sold_ratio = 0 → dev_behavior = 80
- liquidity_locked = False → lock_score = 50
- safety = 80×0.4 + 70×0.3 + 50×0.3 = 32 + 21 + 15 = **68分**

---

### 3.3 聪明钱 SmartMoney（权重 20%）

**公式**：smart_money_ratio = smart_holders数 / holder_count（来自GMGN）

| smart_money_ratio | 分数 |
|-------------------|------|
| > 15%             | 100  |
| > 10%             | 90   |
| > 5%              | 75   |
| > 2%              | 60   |
| ≤ 2%              | 40   |

---

### 3.4 推广 Promotion（权重 15%）

**公式**：`promotion = dex_score×0.40 + social_score×0.30 + website_score×0.30`

#### check_dexscreener_ads（DexScreener推广）

**Boost金额直接决定分数**（来自 DexScreener `/token-boosts/top/v1` → `totalAmount`）：

| dex_boost_amount | 分数 |
|------------------|------|
| ≥ 1000 U         | 100  |
| ≥ 500 U          | 85   |
| ≥ 100 U          | 70   |
| > 0 U            | 55   |
| 无 Boost，无广告  | 40   |

**有Boost时的位置加分**：
- promoted → +30
- trending → +20
- ≥7天 → +10
- ≥3天 → +5

#### check_social_promotion（社交媒体）

| Twitter粉丝 | 加分 | Telegram成员 | 加分 |
|-------------|------|--------------|------|
| > 10000 | +20 | > 5000 | +15 |
| > 5000 | +15 | > 1000 | +10 |
| > 1000 | +10 | > 500 | +5 |
| 有KOL推广 | +15 | - | - |

基础分 50，最高 100。

#### check_website_quality（网站/文档）

| 条件 | 加分 |
|------|------|
| 有官网 | +20 |
| 有白皮书 | +20 |

基础分 40，最高 100。

---

### 3.5 流动性 Liquidity（权重 10%）

**公式**：`liq_ratio = pool_liquidity / mcap`

| liq_ratio | 分数 |
|------------|------|
| > 30%      | 100  |
| > 20%      | 90   |
| > 10%      | 75   |
| > 5%       | 60   |
| ≤ 5%       | 30   |
| mcap = 0   | 30   |

---

## 四、最终评分

```
总分 = narrative×0.25 + safety×0.30 + smart_money×0.20 + promotion×0.15 + liquidity×0.10
```

**评级标准**：

| 分数 | 评级 | 建议 |
|------|------|------|
| ≥ 90 | ⭐⭐⭐⭐⭐ 顶级 | 可以买入 |
| ≥ 75 | ⭐⭐⭐⭐ 优秀 | 可以买入 |
| ≥ 60 | ⭐⭐⭐ 良好 | 可以买入 |
| ≥ 45 | ⭐⭐ 一般 | 观察 |
| ≥ 30 | ⭐ 较差 | 不建议买入 |
| < 30 | ❌ 垃圾 | 不建议买入 |

---

## 五、数据获取

### DexScreener Boost（无需认证）

```bash
# Top 30 Boosted Tokens
curl "https://api.dexscreener.com/token-boosts/top/v1"

# 最新 30 个 Boost
curl "https://api.dexscreener.com/token-boosts/latest/v1"

# 响应字段
{
  "tokenAddress": "...",
  "totalAmount": 500,   # Boost总预算（U）
  "description": "...",
  "links": [...]
}
```

### GMGN API

```python
from gmgn_api import GMGNAPI
gmgn = GMGNAPI()
info = gmgn.get_full_token_analysis(ca, chain='sol')

# 关键字段
info['info']['holder_count']          # 持仓人数
info['security']['top_10_holder_rate'] # Top10持仓占比
info['security']['burn_ratio']         # 烧毁比例
info['security']['dev_token_burn_ratio'] # 开发者烧毁比例
info['pool']['liquidity']              # 流动性
info['market_cap']                     # 市值
info['smart_holders']                 # 聪明钱列表
info['is_safe']                        # 安全标记
```

### TokenSignal 构造示例

```python
from rating_system import TokenSignal

signal = TokenSignal(
    ca='3jG3vjwbEuQCR3YkJKtLmH41jqHx9n36BBW1Kznkpump',
    symbol='UAP',
    token_name='UAP',
    description='FIRST EVER UAP RELEASED BY THE US GOVERNMENT CONFIRMED',
    # 叙事子维度
    narrative_credibility=0.8,
    narrative_kol_approval=0.7,
    narrative_community=0.5,
    narrative_purity=0.8,
    narrative_sentiment=0.6,
    # 聪明钱
    smart_money_ratio=0.0064,  # 28个聪明钱 / 4359 holder
    # 流动性
    pool_liquidity=109031,
    mcap=1197961,
    # 推广
    dex_boost_amount=500,      # DexScreener Boost 500U
    dex_ad_position='promoted',
    # 安全性
    dev_sold_ratio=0,
    has_rug_history=False,
    liquidity_locked=False,
)
```

---

## 六、代码调用

```python
from rating_system import RatingSystem, TokenSignal

rs = RatingSystem()
signal = TokenSignal(...)

result = rs.calculate_rating(signal)
# {
#   "rating": 63.2,
#   "breakdown": {
#     "narrative": 69.0,
#     "safety": 68.0,
#     "smart_money": 40,
#     "promotion": 61.0,
#     "liquidity": 60
#   },
#   "grade": "⭐⭐⭐ 良好",
#   "recommendation": "✅ 可以买入"
# }
```
