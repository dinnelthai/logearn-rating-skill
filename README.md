# 🌟 LogEarn Rating Skill

**Solana Meme币评分系统 - 6维度智能评分**

基于叙事、真实性、安全性、聪明钱、推广投入和流动性的综合评分系统。

---

## 🎯 核心特性

### 6维度评分体系

```
1. 叙事热度 (25%) - AI/名人/MEME等热点叙事
2. 真实性 (25%) - bot检测、刷量检测、垃圾钱包过滤
3. 安全性 (20%) - 开发者行为、Rug检测、流动性锁定
4. 聪明钱 (15%) - 聪明钱占比和认可度
5. 推广投入 (10%) - DexScreener推广、社交媒体影响力
6. 流动性 (5%) - 流动性比率和资金安全性
```

### 评分范围

- **90-100分**: ⭐⭐⭐⭐⭐ 顶级（强烈推荐）
- **75-89分**: ⭐⭐⭐⭐ 优秀（推荐）
- **60-74分**: ⭐⭐⭐ 良好（可考虑）
- **45-59分**: ⭐⭐ 一般（谨慎）
- **30-44分**: ⭐ 较差（不推荐）
- **0-29分**: ❌ 垃圾（避免）

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/dinnelthai/logearn-rating-skill.git
cd logearn-rating-skill
```

### 基本使用

```python
from rating_system import RatingSystem, TokenSignal

# 创建评分系统
rating_system = RatingSystem()

# 创建Token信号
signal = TokenSignal(
    ca="3jG3vjwbEuQCR3YkJKtLmH41jqHx9n36BBW1Kznkpump",
    symbol="AI",
    token_name="AI Agent",
    description="GPT powered agent",
    
    # 真实性数据
    new_wallet_ratio=0.35,      # 新钱包占比 35%
    shit_wallet_ratio=0.03,     # 垃圾钱包占比 3%
    buyer_count=350,            # 交易地址数
    
    # 聪明钱数据
    smart_money_ratio=0.12,     # 聪明钱占比 12%
    
    # 流动性数据
    pool_liquidity=50000,       # 流动性 50K
    mcap=300000,                # 市值 300K
    
    # 推广数据（可选）
    has_dexscreener_ads=True,
    dex_ad_position="promoted",
    twitter_followers=8000
)

# 计算评分
result = rating_system.calculate_rating(signal)

print(f"总评分: {result['rating']}")
print(f"评级: {result['grade']}")
print(f"建议: {result['recommendation']}")
print("\n各维度评分:")
for key, value in result['breakdown'].items():
    print(f"  {key}: {value}")
```

### 输出示例

```
总评分: 87.7
评级: ⭐⭐⭐⭐ 优秀
建议: ✅ 可以买入

各维度评分:
  narrative: 95.0
  authenticity: 84.0
  safety: 85.0
  smart_money: 90.0
  promotion: 86.5
  liquidity: 75.0
```

---

## 📊 评分逻辑详解

### 1. 叙事热度 (25%)

**超级热点 (90-95分)**:
- AI相关: ai, gpt, llm, agent, chatgpt
- 名人相关: elon, trump, musk
- 新闻热点: breaking, viral, trending

**主流热点 (70-80分)**:
- MEME: pepe, doge, shib, cat, dog
- DeFi: defi, swap, lending, dao
- Gaming: game, nft, play

**普通叙事 (55-60分)**:
- Solana生态
- 社区驱动

**无叙事 (30分)**:
- 随机币名

---

### 2. 真实性 (25%)

**新钱包占比检测**:
- < 30%: 100分（真实交易）
- 30-40%: 85分
- 40-50%: 70分
- 50-60%: 50分
- > 60%: 20分（刷量嫌疑）

**垃圾钱包占比检测**:
- < 2%: 100分
- 2-5%: 80分
- 5-10%: 50分
- > 10%: 10分（严重刷量）

**交易地址数量**:
- > 500: 100分
- 300-500: 90分
- 200-300: 80分
- 100-200: 70分
- < 100: 40分

---

### 3. 安全性 (20%)

**开发者行为**:
- 有Rug历史: 0分（一票否决）
- 开发者卖出 < 5%: 100分
- 开发者卖出 5-20%: 80分
- 开发者卖出 > 50%: 10分

**流动性锁定**:
- 锁定 > 365天: 100分
- 锁定 180-365天: 90分
- 锁定 90-180天: 80分
- 未锁定: 50分

---

### 4. 聪明钱 (15%)

- > 15%: 100分（顶级）
- 10-15%: 90分（优秀）
- 5-10%: 75分（良好）
- 2-5%: 60分（一般）
- < 2%: 40分（较差）

---

### 5. 推广投入 (10%)

**DexScreener推广 (40%)**:
- Promoted位置 + 7天: 100分
- Trending位置: 80分
- 无推广: 40分

**社交媒体 (30%)**:
- Twitter粉丝 > 10K: +20分
- Telegram成员 > 5K: +15分
- KOL推广: +15分

**网站质量 (30%)**:
- 有官网: +20分
- 有白皮书: +20分

---

### 6. 流动性 (5%)

流动性比率 = 流动性 / 市值

- > 30%: 100分
- 20-30%: 90分
- 10-20%: 75分
- 5-10%: 60分
- < 5%: 30分

---

## 📈 评分示例

### 示例1: 顶级AI币（有推广）

```python
signal = TokenSignal(
    ca="example1",
    symbol="AI",
    token_name="AI Agent",
    new_wallet_ratio=0.35,
    shit_wallet_ratio=0.03,
    buyer_count=350,
    smart_money_ratio=0.12,
    pool_liquidity=50000,
    mcap=300000,
    has_dexscreener_ads=True,
    dex_ad_position="promoted",
    twitter_followers=8000
)

# 结果: 87.7分 ⭐⭐⭐⭐ 优秀
```

### 示例2: 普通MEME币（无推广）

```python
signal = TokenSignal(
    ca="example2",
    symbol="PEPE",
    token_name="Pepe Dog",
    new_wallet_ratio=0.45,
    shit_wallet_ratio=0.04,
    buyer_count=200,
    smart_money_ratio=0.06,
    pool_liquidity=30000,
    mcap=250000
)

# 结果: 73.9分 ⭐⭐⭐ 良好
```

### 示例3: 刷量垃圾币

```python
signal = TokenSignal(
    ca="example3",
    symbol="SCAM",
    token_name="Random Token",
    new_wallet_ratio=0.70,      # 严重刷量
    shit_wallet_ratio=0.12,     # 垃圾钱包多
    buyer_count=80,
    smart_money_ratio=0.01,
    pool_liquidity=5000,
    mcap=100000
)

# 结果: 39.5分 ⭐ 较差
```

---

## 🔧 高级用法

### 自定义叙事配置

```python
# 添加新的叙事类型
rating_system.SUPER_HOT_NARRATIVES["web3"] = {
    "keywords": ["web3", "metaverse", "vr"],
    "score": 90
}

# 计算评分
result = rating_system.calculate_rating(signal)
```

### 批量评分

```python
signals = [signal1, signal2, signal3]

results = []
for signal in signals:
    result = rating_system.calculate_rating(signal)
    results.append({
        "ca": signal.ca,
        "rating": result["rating"],
        "grade": result["grade"]
    })

# 按评分排序
results.sort(key=lambda x: x["rating"], reverse=True)
```

---

## 📚 文档

- [DESIGN.md](DESIGN.md) - 完整的设计方案
- [ANALYSIS.md](ANALYSIS.md) - 旧系统分析和问题

---

## 🎯 使用场景

### 1. 交易决策

```python
result = rating_system.calculate_rating(signal)

if result["rating"] >= 60:
    print("✅ 可以买入")
elif result["rating"] >= 45:
    print("⚠️ 观察")
else:
    print("❌ 不建议买入")
```

### 2. 风险评估

```python
breakdown = result["breakdown"]

# 检查关键指标
if breakdown["authenticity"] < 50:
    print("⚠️ 警告: 可能存在刷量")

if breakdown["safety"] < 50:
    print("⚠️ 警告: 安全性较低")

if breakdown["narrative"] < 50:
    print("⚠️ 警告: 叙事较弱")
```

### 3. 筛选优质币

```python
def filter_good_tokens(signals):
    """筛选评分>=75的优质币"""
    good_tokens = []
    
    for signal in signals:
        result = rating_system.calculate_rating(signal)
        if result["rating"] >= 75:
            good_tokens.append({
                "ca": signal.ca,
                "symbol": signal.symbol,
                "rating": result["rating"],
                "breakdown": result["breakdown"]
            })
    
    return sorted(good_tokens, key=lambda x: x["rating"], reverse=True)
```

---

## 🔬 测试

```bash
# 运行测试示例
python3 rating_system.py
```

输出:
```
============================================================
示例1: 顶级AI币（有DexScreener推广）
============================================================

总评分: 87.7
评级: ⭐⭐⭐⭐ 优秀
建议: ✅ 可以买入

各维度评分:
  narrative: 95
  authenticity: 84.0
  safety: 85.0
  smart_money: 90
  promotion: 86.5
  liquidity: 75
```

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 License

MIT License

---

## 🙏 致谢

感谢LogEarn提供的数据支持。

---

**开发时间**: 2026-05-09  
**版本**: 1.0.0  
**状态**: 🟢 稳定
