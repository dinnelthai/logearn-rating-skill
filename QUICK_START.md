# 快速开始指南

## 🚀 5分钟上手

### 1. 基本使用

```python
from rating_system import RatingSystem, TokenSignal

# 创建评分系统
rating_system = RatingSystem()

# 创建Token信号（最小配置）
signal = TokenSignal(
    ca="your_token_address",
    symbol="TOKEN",
    token_name="Token Name",
    
    # 必需数据
    smart_money_ratio=0.10,     # 聪明钱占比
    pool_liquidity=50000,       # 流动性
    mcap=300000,                # 市值
    
    # 持仓结构数据（推荐）
    new_volume=0.30,            # 新地址持仓
    shit_volume=0.03,           # 垃圾地址持仓
    scam_volume=0.01            # 诈骗地址持仓
)

# 计算评分
result = rating_system.calculate_rating(signal)

# 查看结果
print(f"评分: {result['rating']}")
print(f"评级: {result['grade']}")
print(f"建议: {result['recommendation']}")
```

---

## 📊 6维度评分体系

| 维度 | 权重 | 关键指标 |
|------|------|---------|
| 叙事热度 | 20% | AI/MEME/名人等热点 |
| 安全性 | 25% | 开发者行为、流动性锁定 |
| 聪明钱 | 15% | 聪明钱占比 |
| 推广投入 | 10% | DexScreener、社交媒体 |
| **持仓结构** | **15%** | **断头盘识别** 🆕 |
| 流动性 | 15% | 流动性比率 |

---

## 🚨 断头盘识别（核心功能）

### 关键阈值

```python
# ❌ 断头盘特征
new_volume > 0.60        # 新地址持仓 > 60%
shit_volume > 0.04       # 垃圾地址持仓 > 4%
scam_volume > 0.03       # 诈骗地址持仓 > 3%

# ✅ 健康特征
new_volume < 0.30        # 新地址持仓 < 30%
shit_volume < 0.02       # 垃圾地址持仓 < 2%
scam_volume < 0.01       # 诈骗地址持仓 < 1%
```

### 快速检测

```python
def is_duantoupan(signal):
    """快速判断是否为断头盘"""
    # 新地址占比过高
    if signal.new_volume > 0.60:
        return True, "新地址占比>60%"
    
    # 垃圾地址占比过高
    if signal.shit_volume > 0.04:
        return True, "垃圾地址占比>4%"
    
    # 诈骗地址占比过高
    if signal.scam_volume > 0.03:
        return True, "诈骗地址占比>3%"
    
    return False, "持仓结构健康"

# 使用
is_bad, reason = is_duantoupan(signal)
if is_bad:
    print(f"⚠️ 断头盘风险: {reason}")
```

---

## 📈 评分等级

| 分数 | 评级 | 建议 |
|------|------|------|
| 90-100 | ⭐⭐⭐⭐⭐ 顶级 | 强烈推荐 |
| 75-89 | ⭐⭐⭐⭐ 优秀 | 推荐 |
| **60-74** | **⭐⭐⭐ 良好** | **可考虑** |
| 45-59 | ⭐⭐ 一般 | 谨慎 |
| 30-44 | ⭐ 较差 | 不推荐 |
| 0-29 | ❌ 垃圾 | 避免 |

**买入阈值**: ≥ 60分

---

## 💡 实用场景

### 场景1: 批量筛选

```python
def filter_good_tokens(signals):
    """筛选评分≥60的优质币"""
    rating_system = RatingSystem()
    good_tokens = []
    
    for signal in signals:
        result = rating_system.calculate_rating(signal)
        
        # 评分≥60 且 持仓结构健康
        if result['rating'] >= 60 and result['breakdown']['holding_structure'] >= 70:
            good_tokens.append({
                'ca': signal.ca,
                'symbol': signal.symbol,
                'rating': result['rating'],
                'holding': result['breakdown']['holding_structure']
            })
    
    return sorted(good_tokens, key=lambda x: x['rating'], reverse=True)
```

### 场景2: 风险预警

```python
def check_risks(signal):
    """检查各维度风险"""
    rating_system = RatingSystem()
    result = rating_system.calculate_rating(signal)
    
    warnings = []
    
    # 持仓结构风险
    if result['breakdown']['holding_structure'] < 50:
        warnings.append("⚠️ 持仓结构异常（可能是断头盘）")
    
    # 安全性风险
    if result['breakdown']['safety'] < 50:
        warnings.append("⚠️ 安全性较低")
    
    # 聪明钱不认可
    if result['breakdown']['smart_money'] < 60:
        warnings.append("⚠️ 聪明钱占比低")
    
    return warnings
```

### 场景3: 交易决策

```python
def should_buy(signal):
    """判断是否应该买入"""
    rating_system = RatingSystem()
    result = rating_system.calculate_rating(signal)
    
    # 总评分
    if result['rating'] < 60:
        return False, "总评分过低"
    
    # 持仓结构检查
    if result['breakdown']['holding_structure'] < 60:
        return False, "持仓结构异常"
    
    # 安全性检查
    if result['breakdown']['safety'] < 50:
        return False, "安全性不足"
    
    return True, "可以买入"
```

---

## 🔧 数据来源

### LogEarn Skills API

**持仓结构数据** (`tag_users_holding_percent`):

```python
# API返回示例
{
    "smart_volume": 0.15,      # 聪明钱持仓 15%
    "whale_volume": 0.12,      # 巨鲸持仓 12%
    "new_volume": 0.25,        # 新地址持仓 25%
    "old_volume": 0.35,        # 老地址持仓 35%
    "shit_volume": 0.02,       # 垃圾地址持仓 2%
    "scam_volume": 0.01,       # 诈骗地址持仓 1%
    "frequent_volume": 0.08,   # 高频交易地址 8%
    "amm_volume": 0.05,        # AMM做市商 5%
    "exchange_volume": 0.03    # 交易所地址 3%
}
```

**API文档**: https://github.com/logearn/logearn-skills/blob/main/api.md

---

## 📚 完整示例

```python
from rating_system import RatingSystem, TokenSignal

# 创建评分系统
rating_system = RatingSystem()

# 完整配置示例
signal = TokenSignal(
    ca="3jG3vjwbEuQCR3YkJKtLmH41jqHx9n36BBW1Kznkpump",
    symbol="AI",
    token_name="AI Agent",
    description="GPT powered agent",
    
    # 叙事数据
    narrative_credibility=0.8,
    narrative_kol_approval=0.7,
    narrative_community=0.6,
    
    # 聪明钱数据
    smart_money_ratio=0.12,
    
    # 流动性数据
    pool_liquidity=50000,
    mcap=300000,
    
    # 安全性数据
    liquidity_locked=True,
    lock_duration=180,
    dev_sold_ratio=0.05,
    
    # 推广数据
    has_dexscreener_ads=True,
    dex_ad_position="promoted",
    dex_boost_amount=1000,
    twitter_followers=8000,
    has_website=True,
    
    # 持仓结构数据（LogEarn Skills API）
    smart_volume=0.15,
    whale_volume=0.12,
    new_volume=0.25,
    old_volume=0.35,
    shit_volume=0.02,
    scam_volume=0.01
)

# 计算评分
result = rating_system.calculate_rating(signal)

# 输出结果
print(f"总评分: {result['rating']}")
print(f"评级: {result['grade']}")
print(f"建议: {result['recommendation']}")
print("\n各维度评分:")
for key, value in result['breakdown'].items():
    print(f"  {key}: {value}")
```

---

## 🎯 最佳实践

### 1. 必须检查的指标

```python
# 最小必查项
✅ new_volume < 0.60      # 新地址持仓
✅ shit_volume < 0.04     # 垃圾地址持仓
✅ scam_volume < 0.03     # 诈骗地址持仓
✅ rating >= 60           # 总评分
```

### 2. 推荐检查的指标

```python
# 推荐检查项
✅ holding_structure >= 70    # 持仓结构评分
✅ safety >= 60               # 安全性评分
✅ smart_money >= 60          # 聪明钱评分
✅ (smart_volume + whale_volume) >= 0.10  # 专业投资者认可
```

### 3. 风险规避

```python
# 一票否决项
❌ has_rug_history = True     # 有Rug历史
❌ new_volume > 0.70          # 新地址>70%（严重断头盘）
❌ shit_volume > 0.10         # 垃圾地址>10%（严重刷量）
❌ scam_volume > 0.05         # 诈骗地址>5%（极高风险）
```

---

## 📖 更多资源

- [README.md](README.md) - 完整文档
- [HOLDING_STRUCTURE.md](HOLDING_STRUCTURE.md) - 持仓结构详解
- [DESIGN.md](DESIGN.md) - 设计方案
- [holding_structure_example.py](holding_structure_example.py) - 持仓结构示例
- [examples.py](examples.py) - 更多示例

---

## ❓ 常见问题

### Q1: 为什么我的评分比预期低？

**A**: 检查以下维度：
1. 持仓结构评分 - 新地址和垃圾地址占比是否过高
2. 叙事热度 - 是否有热点叙事
3. 推广投入 - 是否有DexScreener推广

### Q2: 如何识别断头盘？

**A**: 重点看3个指标：
- `new_volume > 0.60` → 断头盘风险
- `shit_volume > 0.04` → 断头盘概率大
- `scam_volume > 0.03` → 高风险

### Q3: 持仓结构数据从哪里获取？

**A**: 使用 LogEarn Skills API 的 `tag_users_holding_percent` 字段
- API文档: https://github.com/logearn/logearn-skills/blob/main/api.md

### Q4: 评分≥60就可以买入吗？

**A**: 不一定，还需要检查：
- 持仓结构评分 ≥ 60
- 安全性评分 ≥ 50
- 无Rug历史

---

**版本**: 1.1.0  
**更新时间**: 2026-05-09
