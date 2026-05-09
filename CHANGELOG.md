# 更新日志

## [1.1.0] - 2026-05-09

### ✨ 新增功能

#### 持仓结构维度 (15%)

新增第6个评分维度：**持仓结构**，用于识别断头盘和刷量币。

**核心功能**:
- ✅ 新地址持仓占比检测（断头盘识别）
- ✅ 垃圾地址持仓占比检测（刷量检测）
- ✅ 诈骗地址持仓占比检测（安全评估）
- ✅ 聪明钱+巨鲸持仓检测（专业认可）
- ✅ 老地址持仓占比检测（持有信心）

**数据来源**: LogEarn Skills API - `tag_users_holding_percent`

**新增字段**:
```python
# TokenSignal新增字段
smart_volume: float = 0.0       # 聪明钱地址持仓占比
whale_volume: float = 0.0       # 巨鲸地址持仓占比
new_volume: float = 0.0         # 新地址持仓占比
old_volume: float = 0.0         # 老地址持仓占比
frequent_volume: float = 0.0    # 高频交易地址持仓占比
amm_volume: float = 0.0         # AMM做市商地址持仓占比
exchange_volume: float = 0.0    # 交易所地址持仓占比
scam_volume: float = 0.0        # 诈骗地址持仓占比
shit_volume: float = 0.0        # 垃圾地址持仓占比
```

**新增方法**:
- `check_new_volume()` - 新地址占比检测
- `check_shit_volume()` - 垃圾地址占比检测
- `check_scam_volume()` - 诈骗地址占比检测
- `check_smart_whale_volume()` - 聪明钱+巨鲸检测
- `check_old_volume()` - 老地址占比检测
- `holding_structure_score()` - 持仓结构综合评分

**关键阈值**:
- 🚨 新地址 > 60% → 断头盘风险
- 🚨 垃圾地址 > 4% → 断头盘概率大
- 🚨 诈骗地址 > 3% → 高风险

### 🔄 变更

#### 评分体系调整

从 **5维度** 升级为 **6维度**：

**旧版本 (v1.0.0)**:
```
1. 叙事热度 (25%)
2. 安全性 (30%)
3. 聪明钱 (20%)
4. 推广投入 (15%)
5. 流动性 (10%)
```

**新版本 (v1.1.0)**:
```
1. 叙事热度 (20%) ⬇️ -5%
2. 安全性 (25%) ⬇️ -5%
3. 聪明钱 (15%) ⬇️ -5%
4. 推广投入 (10%) ⬇️ -5%
5. 持仓结构 (15%) 🆕 NEW
6. 流动性 (15%) ⬆️ +5%
```

**调整原因**:
- 持仓结构是识别断头盘的关键维度，权重15%
- 流动性重要性提升，从10%增加到15%
- 其他维度权重适当降低，保持总和100%

#### 输出格式变更

评分结果新增 `holding_structure` 字段：

```python
{
    "rating": 74.5,
    "breakdown": {
        "narrative": 33.8,
        "safety": 85.0,
        "smart_money": 90.0,
        "promotion": 86.5,
        "holding_structure": 87.2,  # 🆕 新增
        "liquidity": 75.0
    },
    "grade": "⭐⭐⭐ 良好",
    "recommendation": "✅ 可以买入"
}
```

### 📚 文档更新

- ✅ 更新 `README.md` - 新的6维度说明
- ✅ 新增 `HOLDING_STRUCTURE.md` - 持仓结构详细文档
- ✅ 新增 `holding_structure_example.py` - 使用示例
- ✅ 更新 `rating_system.py` - 测试示例

### 🐛 修复

- 修复了README中维度数量不一致的问题（文档说6维度，实际只有5维度）

### 🔧 技术细节

**代码位置**:
- `rating_system.py:60-69` - TokenSignal新增字段
- `rating_system.py:398-503` - 持仓结构评分实现
- `rating_system.py:527-560` - 最终评分计算更新

**权重分配**:
```python
final_score = (
    narrative    * 0.20 +  # 叙事热度
    safety       * 0.25 +  # 安全性
    smart_money  * 0.15 +  # 聪明钱
    promotion    * 0.10 +  # 推广投入
    holding      * 0.15 +  # 持仓结构 🆕
    liquidity    * 0.15    # 流动性
)
```

---

## [1.0.0] - 2026-05-09

### ✨ 初始版本

**5维度评分体系**:
1. 叙事热度 (25%)
2. 安全性 (30%)
3. 聪明钱 (20%)
4. 推广投入 (15%)
5. 流动性 (10%)

**核心功能**:
- ✅ 叙事热度评分（AI/MEME/DeFi等）
- ✅ 安全性评分（开发者行为、流动性锁定）
- ✅ 聪明钱评分（聪明钱占比）
- ✅ 推广投入评分（DexScreener、社交媒体）
- ✅ 流动性评分（流动性比率）
- ✅ 筹码分析（基于GMGN API）

**评分等级**:
- 90-100分: ⭐⭐⭐⭐⭐ 顶级
- 75-89分: ⭐⭐⭐⭐ 优秀
- 60-74分: ⭐⭐⭐ 良好
- 45-59分: ⭐⭐ 一般
- 30-44分: ⭐ 较差
- 0-29分: ❌ 垃圾

---

## 版本说明

### 语义化版本

遵循 [Semantic Versioning 2.0.0](https://semver.org/)

- **主版本号**: 不兼容的API修改
- **次版本号**: 向下兼容的功能性新增
- **修订号**: 向下兼容的问题修正

### 升级指南

#### 从 v1.0.0 升级到 v1.1.0

**代码变更**:

```python
# 旧版本 (v1.0.0)
signal = TokenSignal(
    ca="...",
    symbol="AI",
    token_name="AI Agent",
    smart_money_ratio=0.12,
    pool_liquidity=50000,
    mcap=300000
)

# 新版本 (v1.1.0) - 新增持仓结构字段
signal = TokenSignal(
    ca="...",
    symbol="AI",
    token_name="AI Agent",
    smart_money_ratio=0.12,
    pool_liquidity=50000,
    mcap=300000,
    # 🆕 新增持仓结构数据
    smart_volume=0.15,
    whale_volume=0.12,
    new_volume=0.25,
    old_volume=0.35,
    shit_volume=0.02,
    scam_volume=0.01
)
```

**向下兼容**:
- ✅ 持仓结构字段为可选，默认值为0.0
- ✅ 旧代码无需修改即可运行
- ⚠️ 但建议添加持仓结构数据以获得更准确的评分

**评分差异**:
- 由于权重调整，相同输入的评分可能略有不同
- 新增持仓结构维度后，评分更加全面和准确

---

**维护者**: LogEarn Team  
**许可证**: MIT
