# 持仓结构维度详解

## 📊 概述

持仓结构维度是基于 **LogEarn Skills API** 的 `tag_users_holding_percent` 数据，用于识别断头盘和刷量币的核心维度。

**权重**: 15%（在6维度评分体系中）

---

## 🎯 核心功能

### 断头盘识别

**断头盘特征**:
- ❌ 新地址持仓占比 > 60%
- ❌ 垃圾地址持仓占比 > 4%
- ❌ 诈骗地址持仓占比 > 3%
- ❌ 聪明钱+巨鲸持仓 < 5%
- ❌ 老地址持仓 < 10%

---

## 📈 评分逻辑

### 子维度权重分配

```
持仓结构评分 = 
  新地址占比检测 (30%) +
  垃圾地址占比检测 (25%) +
  诈骗地址占比检测 (20%) +
  聪明钱+巨鲸持仓 (15%) +
  老地址占比检测 (10%)
```

---

## 🔍 各子维度详解

### 1. 新地址持仓占比 (30%)

**检测逻辑**: 新钱包持仓占比越高，断头盘风险越大

| 占比范围 | 评分 | 说明 |
|---------|------|------|
| < 30% | 100分 | 健康 |
| 30-40% | 85分 | 正常 |
| 40-50% | 70分 | 一般 |
| 50-60% | 50分 | 可疑 |
| **> 60%** | **20分** | **断头盘风险** ⚠️ |

**数据来源**: `new_volume` (LogEarn Skills API)

---

### 2. 垃圾地址持仓占比 (25%)

**检测逻辑**: 垃圾钱包 > 4% 则断头盘概率很大

| 占比范围 | 评分 | 说明 |
|---------|------|------|
| < 2% | 100分 | 非常干净 |
| 2-4% | 85分 | 可接受 |
| **4-6%** | **50分** | **断头盘概率大** ⚠️ |
| 6-10% | 30分 | 严重风险 |
| > 10% | 10分 | 极高风险 |

**数据来源**: `shit_volume` (LogEarn Skills API)

---

### 3. 诈骗地址持仓占比 (20%)

**检测逻辑**: 诈骗地址越多，安全风险越高

| 占比范围 | 评分 | 说明 |
|---------|------|------|
| < 1% | 100分 | 安全 |
| 1-3% | 70分 | 警惕 |
| 3-5% | 40分 | 高风险 |
| > 5% | 10分 | 极高风险 |

**数据来源**: `scam_volume` (LogEarn Skills API)

---

### 4. 聪明钱+巨鲸持仓 (15%)

**检测逻辑**: 专业投资者持仓越高，项目越值得信赖

| 占比范围 | 评分 | 说明 |
|---------|------|------|
| > 30% | 100分 | 顶级 |
| 20-30% | 90分 | 优秀 |
| 10-20% | 75分 | 良好 |
| 5-10% | 60分 | 一般 |
| < 5% | 40分 | 较差 |

**数据来源**: `smart_volume` + `whale_volume` (LogEarn Skills API)

---

### 5. 老地址持仓占比 (10%)

**检测逻辑**: 老地址持仓高说明有坚定持有者

| 占比范围 | 评分 | 说明 |
|---------|------|------|
| > 40% | 100分 | 坚定持有者多 |
| 30-40% | 85分 | 良好 |
| 20-30% | 70分 | 一般 |
| 10-20% | 55分 | 较差 |
| < 10% | 40分 | 很差 |

**数据来源**: `old_volume` (LogEarn Skills API)

---

## 💡 使用示例

### 健康持仓结构

```python
signal = TokenSignal(
    ca="good_token",
    symbol="GOOD",
    token_name="Good Project",
    
    # 持仓结构数据
    smart_volume=0.18,      # 聪明钱 18%
    whale_volume=0.15,      # 巨鲸 15%
    new_volume=0.25,        # 新地址 25% ✅
    old_volume=0.38,        # 老地址 38% ✅
    shit_volume=0.015,      # 垃圾地址 1.5% ✅
    scam_volume=0.005       # 诈骗地址 0.5% ✅
)

# 持仓结构评分: 98.5分 (优秀)
```

### 断头盘特征

```python
signal = TokenSignal(
    ca="bad_token",
    symbol="SCAM",
    token_name="Risky Token",
    
    # 持仓结构数据
    smart_volume=0.02,      # 聪明钱 2%
    whale_volume=0.03,      # 巨鲸 3%
    new_volume=0.68,        # 新地址 68% ❌ 断头盘
    old_volume=0.08,        # 老地址 8% ❌
    shit_volume=0.06,       # 垃圾地址 6% ❌ 断头盘
    scam_volume=0.03        # 诈骗地址 3% ❌
)

# 持仓结构评分: 31.5分 (高风险)
```

---

## 📊 数据来源

### LogEarn Skills API

**API文档**: https://github.com/logearn/logearn-skills/blob/main/api.md

**字段说明** (`tag_users_holding_percent`):

| 字段 | 说明 | 用途 |
|------|------|------|
| `smart_volume` | 聪明钱地址持仓占比 | 专业投资者认可度 |
| `whale_volume` | 巨鲸地址持仓占比 | 大户认可度 |
| `new_volume` | 新地址持仓占比 | 断头盘风险检测 |
| `old_volume` | 老地址持仓占比 | 坚定持有者比例 |
| `frequent_volume` | 高频交易地址持仓占比 | 交易活跃度 |
| `amm_volume` | AMM做市商地址持仓占比 | 流动性提供者 |
| `exchange_volume` | 交易所地址持仓占比 | 中心化交易所持仓 |
| `scam_volume` | 诈骗地址持仓占比 | 安全风险检测 |
| `shit_volume` | 垃圾地址持仓占比 | 刷量风险检测 |

---

## 🎯 实战应用

### 风险预警

```python
def check_holding_risk(signal):
    """检查持仓结构风险"""
    warnings = []
    
    # 断头盘风险
    if signal.new_volume > 0.60:
        warnings.append("⚠️ 新地址占比>60%，断头盘风险")
    
    # 刷量风险
    if signal.shit_volume > 0.04:
        warnings.append("⚠️ 垃圾地址占比>4%，断头盘概率大")
    
    # 安全风险
    if signal.scam_volume > 0.03:
        warnings.append("⚠️ 诈骗地址占比>3%，高风险")
    
    # 专业投资者不认可
    if (signal.smart_volume + signal.whale_volume) < 0.05:
        warnings.append("⚠️ 聪明钱+巨鲸<5%，专业投资者不认可")
    
    return warnings
```

### 筛选优质币

```python
def filter_by_holding_structure(signals):
    """根据持仓结构筛选优质币"""
    good_tokens = []
    
    for signal in signals:
        # 条件1: 新地址占比 < 50%
        if signal.new_volume >= 0.50:
            continue
        
        # 条件2: 垃圾地址占比 < 4%
        if signal.shit_volume >= 0.04:
            continue
        
        # 条件3: 诈骗地址占比 < 3%
        if signal.scam_volume >= 0.03:
            continue
        
        # 条件4: 聪明钱+巨鲸 > 10%
        if (signal.smart_volume + signal.whale_volume) < 0.10:
            continue
        
        good_tokens.append(signal)
    
    return good_tokens
```

---

## 📈 评分影响

### 对总评分的影响

持仓结构维度占总评分的 **15%**，对最终评分有显著影响：

| 持仓结构评分 | 对总评分的贡献 | 影响 |
|------------|--------------|------|
| 100分 | +15分 | 优质持仓 |
| 75分 | +11.25分 | 一般持仓 |
| 50分 | +7.5分 | 可疑持仓 |
| 25分 | +3.75分 | 断头盘 |

### 实际案例对比

```
案例1: 优质持仓 (98.5分)
  总评分: 69.6分 → 持仓贡献 +14.8分

案例2: 一般持仓 (74.5分)
  总评分: 62.8分 → 持仓贡献 +11.2分

案例3: 断头盘 (31.5分)
  总评分: 49.8分 → 持仓贡献 +4.7分
  
差异: 优质持仓比断头盘高出 10.1分
```

---

## 🔧 实现细节

### 代码位置

`@/Users/leon/logearn-rating-skills/logearn-rating-skill/rating_system.py:398-503`

### 核心方法

```python
def holding_structure_score(self, signal: TokenSignal) -> float:
    """持仓结构评分"""
    new_score = self.check_new_volume(signal.new_volume)
    shit_score = self.check_shit_volume(signal.shit_volume)
    scam_score = self.check_scam_volume(signal.scam_volume)
    smart_whale_score = self.check_smart_whale_volume(
        signal.smart_volume, signal.whale_volume
    )
    old_score = self.check_old_volume(signal.old_volume)
    
    score = (
        new_score * 0.30 +
        shit_score * 0.25 +
        scam_score * 0.20 +
        smart_whale_score * 0.15 +
        old_score * 0.10
    )
    
    return round(score, 1)
```

---

## 📝 总结

### 核心价值

1. **断头盘识别**: 通过新地址和垃圾地址占比，有效识别断头盘
2. **刷量检测**: 垃圾地址占比 > 4% 是刷量的重要信号
3. **安全评估**: 诈骗地址占比反映项目安全性
4. **专业认可**: 聪明钱+巨鲸持仓反映专业投资者态度
5. **持有信心**: 老地址占比反映坚定持有者比例

### 关键阈值

- 🚨 **新地址 > 60%** → 断头盘风险
- 🚨 **垃圾地址 > 4%** → 断头盘概率大
- 🚨 **诈骗地址 > 3%** → 高风险
- ✅ **聪明钱+巨鲸 > 20%** → 专业认可
- ✅ **老地址 > 30%** → 坚定持有者多

---

**更新时间**: 2026-05-09  
**版本**: 1.1.0  
**状态**: 🟢 已实现
