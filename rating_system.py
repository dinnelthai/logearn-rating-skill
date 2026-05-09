#!/usr/bin/env python3
"""
独立评分系统 - 基于新设计方案

不依赖Phase2，可以单独运行
"""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class TokenSignal:
    """Token信号数据"""
    ca: str
    symbol: str
    token_name: str
    description: str = ""
    
    # 真实性数据
    new_wallet_ratio: float = 0.0       # 新钱包占比
    shit_wallet_ratio: float = 0.0      # 垃圾钱包占比
    buyer_count: int = 0                # 交易地址数
    
    # 聪明钱数据
    smart_money_ratio: float = 0.0      # 聪明钱占比
    
    # 流动性数据
    pool_liquidity: float = 0.0         # 流动性
    mcap: float = 0.0                   # 市值
    
    # 推广数据（可选）
    has_dexscreener_ads: bool = False   # 是否有DexScreener推广
    dex_ad_position: str = ""           # 推广位置: trending/promoted
    dex_ad_duration: int = 0            # 推广天数
    twitter_followers: int = 0          # Twitter粉丝
    telegram_members: int = 0           # Telegram成员
    has_kol_promotion: bool = False     # 是否有KOL推广
    has_website: bool = False           # 是否有官网
    has_whitepaper: bool = False        # 是否有白皮书
    
    # 安全性数据（可选）
    dev_sold_ratio: float = 0.0         # 开发者卖出比例
    has_rug_history: bool = False       # 是否有Rug历史
    liquidity_locked: bool = False      # 流动性是否锁定
    lock_duration: int = 0              # 锁定天数


class RatingSystem:
    """独立评分系统"""
    
    # 叙事配置
    SUPER_HOT_NARRATIVES = {
        "ai": {
            "keywords": ["ai", "gpt", "llm", "agent", "chatgpt", "claude", "gemini"],
            "score": 95
        },
        "名人": {
            "keywords": ["elon", "trump", "musk", "biden"],
            "score": 95
        },
        "新闻热点": {
            "keywords": ["breaking", "viral", "trending", "news"],
            "score": 90
        }
    }
    
    MAINSTREAM_NARRATIVES = {
        "meme": {
            "keywords": ["pepe", "doge", "shib", "cat", "dog", "frog"],
            "score": 80
        },
        "defi": {
            "keywords": ["defi", "swap", "lending", "dao", "yield"],
            "score": 75
        },
        "gaming": {
            "keywords": ["game", "nft", "play", "metaverse"],
            "score": 70
        }
    }
    
    NORMAL_NARRATIVES = {
        "solana": {
            "keywords": ["solana", "sol", "raydium", "jupiter"],
            "score": 60
        },
        "社区": {
            "keywords": ["community", "holder", "diamond"],
            "score": 55
        }
    }
    
    def __init__(self):
        pass
    
    # ========== 维度1: 叙事热度 (25%) ==========
    
    def narrative_score(self, signal: TokenSignal) -> float:
        """叙事热度评分"""
        text = f"{signal.symbol} {signal.token_name} {signal.description}".lower()
        
        # 检查超级热点
        for narrative, config in self.SUPER_HOT_NARRATIVES.items():
            for keyword in config["keywords"]:
                if keyword in text:
                    return config["score"]
        
        # 检查主流热点
        for narrative, config in self.MAINSTREAM_NARRATIVES.items():
            for keyword in config["keywords"]:
                if keyword in text:
                    return config["score"]
        
        # 检查普通叙事
        for narrative, config in self.NORMAL_NARRATIVES.items():
            for keyword in config["keywords"]:
                if keyword in text:
                    return config["score"]
        
        # 无叙事
        return 30.0
    
    # ========== 维度2: 真实性 (25%) ==========
    
    def check_new_wallet_ratio(self, ratio: float) -> float:
        """新钱包占比检测"""
        if ratio < 0.30:
            return 100
        elif ratio < 0.40:
            return 85
        elif ratio < 0.50:
            return 70
        elif ratio < 0.60:
            return 50
        else:
            return 20
    
    def check_shit_wallet_ratio(self, ratio: float) -> float:
        """垃圾钱包占比检测"""
        if ratio < 0.02:
            return 100
        elif ratio < 0.05:
            return 80
        elif ratio < 0.10:
            return 50
        else:
            return 10
    
    def check_buyer_count(self, count: int) -> float:
        """交易地址数量检测"""
        if count > 500:
            return 100
        elif count > 300:
            return 90
        elif count > 200:
            return 80
        elif count > 100:
            return 70
        else:
            return 40
    
    def authenticity_score(self, signal: TokenSignal) -> float:
        """真实性评分"""
        new_wallet_score = self.check_new_wallet_ratio(signal.new_wallet_ratio)
        shit_wallet_score = self.check_shit_wallet_ratio(signal.shit_wallet_ratio)
        buyer_count_score = self.check_buyer_count(signal.buyer_count)
        
        score = (
            new_wallet_score * 0.40 +
            shit_wallet_score * 0.40 +
            buyer_count_score * 0.20
        )
        
        return round(score, 1)
    
    # ========== 维度3: 安全性 (20%) ==========
    
    def check_dev_behavior(self, signal: TokenSignal) -> float:
        """开发者行为检测"""
        if signal.has_rug_history:
            return 0  # 一票否决
        
        ratio = signal.dev_sold_ratio
        
        if ratio < 0.05:
            return 100
        elif ratio < 0.20:
            return 80
        elif ratio < 0.50:
            return 40
        else:
            return 10
    
    def check_liquidity_lock(self, signal: TokenSignal) -> float:
        """流动性锁定检测"""
        if not signal.liquidity_locked:
            return 50
        
        days = signal.lock_duration
        
        if days > 365:
            return 100
        elif days > 180:
            return 90
        elif days > 90:
            return 80
        elif days > 30:
            return 70
        else:
            return 60
    
    def safety_score(self, signal: TokenSignal) -> float:
        """安全性评分"""
        dev_score = self.check_dev_behavior(signal)
        
        if dev_score == 0:  # Rug历史，直接0分
            return 0
        
        lock_score = self.check_liquidity_lock(signal)
        contract_score = 70  # 默认70分（需要合约检测数据）
        
        score = (
            dev_score * 0.40 +
            contract_score * 0.30 +
            lock_score * 0.30
        )
        
        return round(score, 1)
    
    # ========== 维度4: 聪明钱 (15%) ==========
    
    def smart_money_score(self, signal: TokenSignal) -> float:
        """聪明钱评分"""
        ratio = signal.smart_money_ratio
        
        if ratio > 0.15:
            return 100
        elif ratio > 0.10:
            return 90
        elif ratio > 0.05:
            return 75
        elif ratio > 0.02:
            return 60
        else:
            return 40
    
    # ========== 维度5: 推广投入 (10%) ==========
    
    def check_dexscreener_ads(self, signal: TokenSignal) -> float:
        """DexScreener推广检测"""
        if not signal.has_dexscreener_ads:
            return 40
        
        score = 60
        
        # 推广位置加分
        if signal.dex_ad_position == "promoted":
            score += 30
        elif signal.dex_ad_position == "trending":
            score += 20
        
        # 持续时间加分
        if signal.dex_ad_duration >= 7:
            score += 10
        elif signal.dex_ad_duration >= 3:
            score += 5
        
        return min(score, 100)
    
    def check_social_promotion(self, signal: TokenSignal) -> float:
        """社交媒体推广检测"""
        score = 50
        
        # Twitter粉丝
        if signal.twitter_followers > 10000:
            score += 20
        elif signal.twitter_followers > 5000:
            score += 15
        elif signal.twitter_followers > 1000:
            score += 10
        
        # Telegram成员
        if signal.telegram_members > 5000:
            score += 15
        elif signal.telegram_members > 1000:
            score += 10
        elif signal.telegram_members > 500:
            score += 5
        
        # KOL推广
        if signal.has_kol_promotion:
            score += 15
        
        return min(score, 100)
    
    def check_website_quality(self, signal: TokenSignal) -> float:
        """网站和文档质量"""
        score = 40
        
        if signal.has_website:
            score += 20
        
        if signal.has_whitepaper:
            score += 20
        
        return min(score, 100)
    
    def promotion_score(self, signal: TokenSignal) -> float:
        """推广投入评分"""
        dex_score = self.check_dexscreener_ads(signal)
        social_score = self.check_social_promotion(signal)
        website_score = self.check_website_quality(signal)
        
        score = (
            dex_score * 0.40 +
            social_score * 0.30 +
            website_score * 0.30
        )
        
        return round(score, 1)
    
    # ========== 维度6: 流动性 (5%) ==========
    
    def liquidity_score(self, signal: TokenSignal) -> float:
        """流动性评分"""
        if signal.mcap <= 0:
            return 30
        
        liq_ratio = signal.pool_liquidity / signal.mcap
        
        if liq_ratio > 0.30:
            return 100
        elif liq_ratio > 0.20:
            return 90
        elif liq_ratio > 0.10:
            return 75
        elif liq_ratio > 0.05:
            return 60
        else:
            return 30
    
    # ========== 最终评分 ==========
    
    def calculate_rating(self, signal: TokenSignal) -> Dict:
        """计算最终评分"""
        
        # 各维度评分
        narrative = self.narrative_score(signal)
        authenticity = self.authenticity_score(signal)
        safety = self.safety_score(signal)
        smart_money = self.smart_money_score(signal)
        promotion = self.promotion_score(signal)
        liquidity = self.liquidity_score(signal)
        
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
            },
            "grade": self._get_grade(final_score),
            "recommendation": self._get_recommendation(final_score)
        }
    
    def _get_grade(self, score: float) -> str:
        """获取评级"""
        if score >= 90:
            return "⭐⭐⭐⭐⭐ 顶级"
        elif score >= 75:
            return "⭐⭐⭐⭐ 优秀"
        elif score >= 60:
            return "⭐⭐⭐ 良好"
        elif score >= 45:
            return "⭐⭐ 一般"
        elif score >= 30:
            return "⭐ 较差"
        else:
            return "❌ 垃圾"
    
    def _get_recommendation(self, score: float) -> str:
        """获取建议"""
        if score >= 60:
            return "✅ 可以买入"
        elif score >= 45:
            return "⚠️ 观察"
        else:
            return "❌ 不建议买入"


# ========== 测试示例 ==========

def test_rating_system():
    """测试评分系统"""
    
    rating_system = RatingSystem()
    
    # 示例1: 顶级AI币
    print("=" * 60)
    print("示例1: 顶级AI币（有DexScreener推广）")
    print("=" * 60)
    
    signal1 = TokenSignal(
        ca="test_ca_1",
        symbol="AI",
        token_name="AI Agent",
        description="GPT powered agent",
        new_wallet_ratio=0.35,
        shit_wallet_ratio=0.03,
        buyer_count=350,
        smart_money_ratio=0.12,
        pool_liquidity=50000,
        mcap=300000,
        has_dexscreener_ads=True,
        dex_ad_position="promoted",
        dex_ad_duration=7,
        twitter_followers=8000,
        telegram_members=3000,
        has_website=True,
        has_whitepaper=True,
        liquidity_locked=True,
        lock_duration=180
    )
    
    result1 = rating_system.calculate_rating(signal1)
    print(f"\n总评分: {result1['rating']}")
    print(f"评级: {result1['grade']}")
    print(f"建议: {result1['recommendation']}")
    print("\n各维度评分:")
    for key, value in result1['breakdown'].items():
        print(f"  {key}: {value}")
    
    # 示例2: 普通MEME币
    print("\n" + "=" * 60)
    print("示例2: 普通MEME币（无推广）")
    print("=" * 60)
    
    signal2 = TokenSignal(
        ca="test_ca_2",
        symbol="PEPE",
        token_name="Pepe Dog",
        new_wallet_ratio=0.45,
        shit_wallet_ratio=0.04,
        buyer_count=200,
        smart_money_ratio=0.06,
        pool_liquidity=30000,
        mcap=250000,
        twitter_followers=1200,
        has_website=True
    )
    
    result2 = rating_system.calculate_rating(signal2)
    print(f"\n总评分: {result2['rating']}")
    print(f"评级: {result2['grade']}")
    print(f"建议: {result2['recommendation']}")
    print("\n各维度评分:")
    for key, value in result2['breakdown'].items():
        print(f"  {key}: {value}")
    
    # 示例3: 刷量垃圾币
    print("\n" + "=" * 60)
    print("示例3: 刷量垃圾币")
    print("=" * 60)
    
    signal3 = TokenSignal(
        ca="test_ca_3",
        symbol="SCAM",
        token_name="Random Token",
        new_wallet_ratio=0.70,
        shit_wallet_ratio=0.12,
        buyer_count=80,
        smart_money_ratio=0.01,
        pool_liquidity=5000,
        mcap=100000,
        twitter_followers=200
    )
    
    result3 = rating_system.calculate_rating(signal3)
    print(f"\n总评分: {result3['rating']}")
    print(f"评级: {result3['grade']}")
    print(f"建议: {result3['recommendation']}")
    print("\n各维度评分:")
    for key, value in result3['breakdown'].items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    test_rating_system()
