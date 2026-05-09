# 评分系统功能梳理

## 🎯 核心功能

**这是一个 Solana Meme币评分系统，最终输出一个 0-100 的综合评分，用于判断代币的投资价值。**

---

## 📊 输入 → 处理 → 输出

### 输入数据 (TokenSignal)

```python
signal = TokenSignal(
    # 基础信息
    ca="代币地址",
    symbol="代币符号",
    token_name="代币名称",
    description="描述",
    
    # 6个维度的原始数据
    # ... (见下方详细说明)
)
```

### 处理流程

```
输入数据 → 6个维度评分 → 加权计算 → 最终评分 → 评级+建议
```

### 最终输出

```python
{
    "rating": 74.5,                    # 最终评分 (0-100)
    "grade": "⭐⭐⭐ 良好",              # 评级
    "recommendation": "✅ 可以买入",    # 买入建议
    "breakdown": {                     # 各维度详细评分
        "narrative": 33.8,             # 叙事热度
        "safety": 85.0,                # 安全性
        "smart_money": 90.0,           # 聪明钱
        "promotion": 86.5,             # 推广投入
        "holding_structure": 87.2,     # 持仓结构
        "liquidity": 75.0              # 流动性
    }
}
```

---

## 🔢 评分计算公式

### 最终评分 = 6个维度加权求和

```python
最终评分 = 
    叙事热度 × 20% +
    安全性 × 25% +
    聪明钱 × 15% +
    推广投入 × 10% +
    持仓结构 × 15% +
    流动性 × 15%
```

**范围**: 0-100分

---

## 📈 6个维度详解

### 维度1: 叙事热度 (20%)

**输入数据**:
```python
symbol="AI"                        # 代币符号
token_name="AI Agent"              # 代币名称
description="GPT powered"          # 描述
narrative_credibility=0.8          # 可信度 (0-1)
narrative_kol_approval=0.7         # KOL认可 (0-1)
narrative_community=0.6            # 社区活跃度 (0-1)
narrative_purity=0.5               # 叙事纯度 (0-1)
narrative_sentiment=0.5            # 情绪指数 (0-1)
```

**计算逻辑**:
- 70% 子维度加权 (credibility, kol_approval, community, purity, sentiment)
- 30% 关键词匹配 (AI=95分, MEME=80分, Solana=60分, 无叙事=30分)

**输出**: 0-100分

---

### 维度2: 安全性 (25%)

**输入数据**:
```python
has_rug_history=False              # 是否有Rug历史
dev_sold_ratio=0.05                # 开发者卖出比例 (0-1)
liquidity_locked=True              # 流动性是否锁定
lock_duration=180                  # 锁定天数
```

**计算逻辑**:
- 开发者行为 (40%): Rug历史→0分, 卖出<5%→100分
- 合约安全 (30%): 默认70分 (需要合约检测数据)
- 流动性锁定 (30%): 锁定>365天→100分, 未锁定→50分

**输出**: 0-100分

**一票否决**: 有Rug历史 → 直接0分

---

### 维度3: 聪明钱 (15%)

**输入数据**:
```python
smart_money_ratio=0.12             # 聪明钱占比 (0-1)
```

**计算逻辑**:
- >15% → 100分
- 10-15% → 90分
- 5-10% → 75分
- 2-5% → 60分
- <2% → 40分

**输出**: 0-100分

---

### 维度4: 推广投入 (10%)

**输入数据**:
```python
# DexScreener推广
has_dexscreener_ads=True           # 是否有推广
dex_ad_position="promoted"         # 推广位置
dex_ad_duration=7                  # 推广天数
dex_boost_amount=1000              # Boost金额(U)

# 社交媒体
twitter_followers=8000             # Twitter粉丝
telegram_members=3000              # Telegram成员
has_kol_promotion=True             # KOL推广

# 网站质量
has_website=True                   # 是否有官网
has_whitepaper=True                # 是否有白皮书
```

**计算逻辑**:
- DexScreener推广 (40%): Boost≥1000U→100分, Promoted+7天→100分
- 社交媒体 (30%): Twitter>10K→+20分, Telegram>5K→+15分
- 网站质量 (30%): 有官网→+20分, 有白皮书→+20分

**输出**: 0-100分

---

### 维度5: 持仓结构 (15%) 🆕

**输入数据** (来自LogEarn Skills API):
```python
smart_volume=0.15                  # 聪明钱持仓占比 (0-1)
whale_volume=0.12                  # 巨鲸持仓占比 (0-1)
new_volume=0.25                    # 新地址持仓占比 (0-1)
old_volume=0.35                    # 老地址持仓占比 (0-1)
shit_volume=0.02                   # 垃圾地址持仓占比 (0-1)
scam_volume=0.01                   # 诈骗地址持仓占比 (0-1)
```

**计算逻辑**:
- 新地址占比 (30%): <30%→100分, >60%→20分 (断头盘)
- 垃圾地址占比 (25%): <2%→100分, >4%→50分 (断头盘)
- 诈骗地址占比 (20%): <1%→100分, >5%→10分
- 聪明钱+巨鲸 (15%): >30%→100分, <5%→40分
- 老地址占比 (10%): >40%→100分, <10%→40分

**输出**: 0-100分

**关键阈值**:
- 🚨 new_volume > 60% → 断头盘风险
- 🚨 shit_volume > 4% → 断头盘概率大
- 🚨 scam_volume > 3% → 高风险

---

### 维度6: 流动性 (15%)

**输入数据**:
```python
pool_liquidity=50000               # 流动性池金额
mcap=300000                        # 市值
```

**计算逻辑**:
- 流动性比率 = pool_liquidity / mcap
- >30% → 100分
- 20-30% → 90分
- 10-20% → 75分
- 5-10% → 60分
- <5% → 30分

**输出**: 0-100分

---

## 🎯 最终输出详解

### 1. 评分 (rating)

**范围**: 0-100分

**计算公式**:
```python
rating = (
    narrative × 0.20 +
    safety × 0.25 +
    smart_money × 0.15 +
    promotion × 0.10 +
    holding_structure × 0.15 +
    liquidity × 0.15
)
```

**示例**: 74.5分

---

### 2. 评级 (grade)

**分级标准**:
```python
90-100分 → "⭐⭐⭐⭐⭐ 顶级"
75-89分  → "⭐⭐⭐⭐ 优秀"
60-74分  → "⭐⭐⭐ 良好"
45-59分  → "⭐⭐ 一般"
30-44分  → "⭐ 较差"
0-29分   → "❌ 垃圾"
```

**示例**: "⭐⭐⭐ 良好"

---

### 3. 建议 (recommendation)

**决策逻辑**:
```python
≥60分 → "✅ 可以买入"
45-59分 → "⚠️ 观察"
<45分 → "❌ 不建议买入"
```

**示例**: "✅ 可以买入"

---

### 4. 详细评分 (breakdown)

**包含6个维度的具体分数**:
```python
{
    "narrative": 33.8,             # 叙事热度评分
    "safety": 85.0,                # 安全性评分
    "smart_money": 90.0,           # 聪明钱评分
    "promotion": 86.5,             # 推广投入评分
    "holding_structure": 87.2,     # 持仓结构评分
    "liquidity": 75.0              # 流动性评分
}
```

**用途**: 
- 查看各维度表现
- 识别弱点
- 风险预警

---

## 💡 完整使用流程

### Step 1: 准备数据

```python
from rating_system import RatingSystem, TokenSignal

# 创建Token信号
signal = TokenSignal(
    ca="token_address",
    symbol="AI",
    token_name="AI Agent",
    
    # 填入各维度数据
    smart_money_ratio=0.12,
    pool_liquidity=50000,
    mcap=300000,
    new_volume=0.25,
    shit_volume=0.02,
    # ... 其他字段
)
```

### Step 2: 计算评分

```python
# 创建评分系统
rating_system = RatingSystem()

# 计算评分
result = rating_system.calculate_rating(signal)
```

### Step 3: 获取输出

```python
# 最终评分
print(f"评分: {result['rating']}")           # 74.5

# 评级
print(f"评级: {result['grade']}")            # ⭐⭐⭐ 良好

# 建议
print(f"建议: {result['recommendation']}")   # ✅ 可以买入

# 各维度详细评分
for key, value in result['breakdown'].items():
    print(f"{key}: {value}")
```

### Step 4: 决策

```python
# 买入决策
if result['rating'] >= 60:
    if result['breakdown']['holding_structure'] >= 60:
        if result['breakdown']['safety'] >= 50:
            print("✅ 可以买入")
        else:
            print("⚠️ 安全性不足")
    else:
        print("⚠️ 持仓结构异常（可能是断头盘）")
else:
    print("❌ 评分过低，不建议买入")
```

---

## 📊 输出示例

### 示例1: 优质项目

**输入**:
```python
signal = TokenSignal(
    ca="good_token",
    symbol="AI",
    token_name="AI Agent",
    smart_money_ratio=0.12,
    pool_liquidity=50000,
    mcap=300000,
    new_volume=0.25,        # 健康
    shit_volume=0.02,       # 干净
    scam_volume=0.01,       # 安全
    smart_volume=0.15,
    whale_volume=0.12,
    old_volume=0.35
)
```

**输出**:
```python
{
    "rating": 74.5,
    "grade": "⭐⭐⭐ 良好",
    "recommendation": "✅ 可以买入",
    "breakdown": {
        "narrative": 33.8,
        "safety": 85.0,
        "smart_money": 90.0,
        "promotion": 86.5,
        "holding_structure": 87.2,  # 优秀
        "liquidity": 75.0
    }
}
```

---

### 示例2: 断头盘

**输入**:
```python
signal = TokenSignal(
    ca="bad_token",
    symbol="SCAM",
    token_name="Random",
    smart_money_ratio=0.01,
    pool_liquidity=5000,
    mcap=100000,
    new_volume=0.68,        # 断头盘风险
    shit_volume=0.06,       # 断头盘概率大
    scam_volume=0.03,       # 高风险
    smart_volume=0.02,
    whale_volume=0.03,
    old_volume=0.08
)
```

**输出**:
```python
{
    "rating": 40.0,
    "grade": "⭐ 较差",
    "recommendation": "❌ 不建议买入",
    "breakdown": {
        "narrative": 7.5,
        "safety": 76.0,
        "smart_money": 40.0,
        "promotion": 43.0,
        "holding_structure": 31.5,  # 断头盘特征
        "liquidity": 30.0
    }
}
```

---

## 🎯 核心价值

### 1. 综合评估
- 不是单一指标，而是6个维度的综合评分
- 全面反映代币的投资价值

### 2. 断头盘识别
- 通过持仓结构维度，有效识别断头盘
- 关键阈值：new_volume>60%, shit_volume>4%

### 3. 风险预警
- 各维度评分可以识别具体风险
- 一票否决机制（Rug历史）

### 4. 决策支持
- 明确的买入建议（≥60分可买入）
- 详细的评分breakdown用于分析

---

## 📌 关键要点

### 输入要求
- **必需字段**: ca, symbol, token_name, smart_money_ratio, pool_liquidity, mcap
- **推荐字段**: 持仓结构数据 (new_volume, shit_volume, scam_volume)
- **可选字段**: 推广数据、安全性数据、叙事数据

### 输出内容
1. **rating** (0-100) - 最终评分
2. **grade** (⭐) - 评级
3. **recommendation** (✅/⚠️/❌) - 买入建议
4. **breakdown** ({}) - 6个维度详细评分

### 决策阈值
- **买入**: rating ≥ 60
- **观察**: 45 ≤ rating < 60
- **避免**: rating < 45

### 风险识别
- **断头盘**: new_volume > 60% 或 shit_volume > 4%
- **Rug风险**: has_rug_history = True
- **安全风险**: scam_volume > 3%

---

**版本**: 1.1.0  
**更新时间**: 2026-05-09
