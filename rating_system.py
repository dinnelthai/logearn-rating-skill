#!/usr/bin/env python3
"""
独立评分系统 - 基于新设计方案

不依赖Phase2，可以单独运行
"""

from dataclasses import dataclass
from typing import Optional, Dict


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


@dataclass
class TokenSignal:
    """Token信号数据"""
    ca: str
    symbol: str
    token_name: str
    description: str = ""

    # 叙事子维度（meme-rating-system 方案）
    narrative_credibility: float = 0.0   # 0~1
    narrative_kol_approval: float = 0.0  # 0~1
    narrative_community: float = 0.0      # 0~1
    narrative_purity: float = 0.0         # 0~1
    narrative_sentiment: float = 0.5      # 0~1

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
    dex_ad_position: str = ""            # 推广位置: trending/promoted
    dex_ad_duration: int = 0             # 推广天数
    dex_boost_amount: float = 0.0        # DexScreener Boost 总预算（U）
    twitter_followers: int = 0           # Twitter粉丝
    telegram_members: int = 0           # Telegram成员
    has_kol_promotion: bool = False     # 是否有KOL推广
    has_website: bool = False           # 是否有官网
    has_whitepaper: bool = False        # 是否有白皮书

    # 安全性数据（可选）
    dev_sold_ratio: float = 0.0         # 开发者卖出比例
    has_rug_history: bool = False       # 是否有Rug历史
    liquidity_locked: bool = False      # 流动性是否锁定
    lock_duration: int = 0              # 锁定天数

    # LogEarn持仓结构数据（tag_users_holding_percent）
    smart_volume: float = 0.0           # 聪明钱地址持仓占比
    whale_volume: float = 0.0           # 巨鲸地址持仓占比
    new_volume: float = 0.0             # 新地址持仓占比
    old_volume: float = 0.0             # 老地址持仓占比
    frequent_volume: float = 0.0        # 高频交易地址持仓占比
    amm_volume: float = 0.0             # AMM做市商地址持仓占比
    exchange_volume: float = 0.0        # 交易所地址持仓占比
    scam_volume: float = 0.0            # 诈骗地址持仓占比
    shit_volume: float = 0.0            # 垃圾地址持仓占比


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
    # 采用 meme-rating-system 方案：子维度加权 + 关键词 Tier

    WEIGHTS_NARRATIVE = {
        "credibility": 0.30,
        "kol_approval": 0.20,
        "community": 0.20,
        "purity": 0.15,
        "sentiment": 0.15
    }

    def narrative_score(self, signal: TokenSignal) -> float:
        """叙事热度评分（meme-rating-system 方案）

        70% 子维度加权 + 30% 关键词 Tier
        """
        # 子维度加权
        fields = {
            "credibility":  signal.narrative_credibility,
            "kol_approval": signal.narrative_kol_approval,
            "community":    signal.narrative_community,
            "purity":       signal.narrative_purity,
            "sentiment":    signal.narrative_sentiment,
        }
        base = sum(self.WEIGHTS_NARRATIVE[k] * fields[k] for k in self.WEIGHTS_NARRATIVE)

        # 关键词 Tier（30% 权重）
        text = f"{signal.symbol} {signal.token_name} {signal.description}".lower()
        keyword_score = 0.0

        for narrative, config in self.SUPER_HOT_NARRATIVES.items():
            for keyword in config["keywords"]:
                if keyword in text:
                    keyword_score = max(keyword_score, config["score"] / 100)
                    break

        if keyword_score == 0:
            for narrative, config in self.MAINSTREAM_NARRATIVES.items():
                for keyword in config["keywords"]:
                    if keyword in text:
                        keyword_score = max(keyword_score, config["score"] / 100)
                        break

        if keyword_score == 0:
            for narrative, config in self.NORMAL_NARRATIVES.items():
                for keyword in config["keywords"]:
                    if keyword in text:
                        keyword_score = max(keyword_score, config["score"] / 100)
                        break

        # 无叙事
        if keyword_score == 0:
            return round(base * 100, 1)

        # Blend: 70% 子维度，30% 关键词
        total = base * 0.7 + keyword_score * 0.3
        return round(clamp(total, 0, 1) * 100, 1)
    
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
        """DexScreener推广检测

        Boost 金额来源：GET /token-boosts/top/v1 -> totalAmount（U）
        - totalAmount >= 1000U  → 100分
        - totalAmount >= 500U   → 85分
        - totalAmount >= 100U   → 70分
        - totalAmount > 0U      → 55分
        - 无 Boost              → 40分（无推广基准）
        """
        boost = signal.dex_boost_amount

        # Boost 金额直接决定分数（独立判断）
        if boost >= 1000:
            return 100.0
        elif boost >= 500:
            return 85.0
        elif boost >= 100:
            return 70.0
        elif boost > 0:
            return 55.0

        # 无 Boost，看是否有广告位
        if not signal.has_dexscreener_ads:
            return 40.0

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
    
    # ========== 维度6: 持仓结构 (15%) ==========
    
    def check_new_volume(self, ratio: float) -> float:
        """新地址持仓占比检测
        
        新钱包持仓占比越高，断头盘风险越大
        """
        if ratio < 0.30:      # <30% 健康
            return 100
        elif ratio < 0.40:    # 30-40% 正常
            return 85
        elif ratio < 0.50:    # 40-50% 一般
            return 70
        elif ratio < 0.60:    # 50-60% 可疑
            return 50
        else:                 # >60% 断头盘风险
            return 20
    
    def check_shit_volume(self, ratio: float) -> float:
        """垃圾地址持仓占比检测
        
        垃圾钱包>4%则断头盘概率很大
        """
        if ratio < 0.02:      # <2% 非常干净
            return 100
        elif ratio < 0.04:    # 2-4% 可接受
            return 85
        elif ratio < 0.06:    # 4-6% 高风险
            return 50
        elif ratio < 0.10:    # 6-10% 严重风险
            return 30
        else:                 # >10% 极高风险
            return 10
    
    def check_scam_volume(self, ratio: float) -> float:
        """诈骗地址持仓占比检测"""
        if ratio < 0.01:      # <1% 安全
            return 100
        elif ratio < 0.03:    # 1-3% 警惕
            return 70
        elif ratio < 0.05:    # 3-5% 高风险
            return 40
        else:                 # >5% 极高风险
            return 10
    
    def check_smart_whale_volume(self, smart: float, whale: float) -> float:
        """聪明钱+巨鲸持仓占比检测
        
        聪明钱和巨鲸持仓越高，说明专业投资者认可
        """
        total = smart + whale
        
        if total > 0.30:      # >30% 顶级
            return 100
        elif total > 0.20:    # 20-30% 优秀
            return 90
        elif total > 0.10:    # 10-20% 良好
            return 75
        elif total > 0.05:    # 5-10% 一般
            return 60
        else:                 # <5% 较差
            return 40
    
    def check_old_volume(self, ratio: float) -> float:
        """老地址持仓占比检测
        
        老地址持仓高说明有坚定持有者
        """
        if ratio > 0.40:      # >40% 优秀
            return 100
        elif ratio > 0.30:    # 30-40% 良好
            return 85
        elif ratio > 0.20:    # 20-30% 一般
            return 70
        elif ratio > 0.10:    # 10-20% 较差
            return 55
        else:                 # <10% 很差
            return 40
    
    def holding_structure_score(self, signal: TokenSignal) -> float:
        """持仓结构评分
        
        权重分配：
        - 新地址占比 30% (断头盘风险)
        - 垃圾地址占比 25% (刷量风险)
        - 诈骗地址占比 20% (安全风险)
        - 聪明钱+巨鲸 15% (专业认可)
        - 老地址占比 10% (持有信心)
        """
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
    
    # ========== 维度7: 流动性 (5%) ==========
    
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
        """计算最终评分（6维度）

        权重：叙事20% + 安全性25% + 聪明钱15% + 推广10% + 持仓结构15% + 流动性15%
        """
        narrative    = self.narrative_score(signal)
        safety       = self.safety_score(signal)
        smart_money  = self.smart_money_score(signal)
        promotion    = self.promotion_score(signal)
        holding      = self.holding_structure_score(signal)
        liquidity    = self.liquidity_score(signal)

        final_score = (
            narrative    * 0.20 +
            safety       * 0.25 +
            smart_money  * 0.15 +
            promotion    * 0.10 +
            holding      * 0.15 +
            liquidity    * 0.15
        )

        return {
            "rating": round(final_score, 1),
            "breakdown": {
                "narrative":   round(narrative, 1),
                "safety":      round(safety, 1),
                "smart_money": round(smart_money, 1),
                "promotion":   round(promotion, 1),
                "holding_structure": round(holding, 1),
                "liquidity":   round(liquidity, 1),
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


# ========== 筹码分析（基于GMGN API）============

class ChipAnalysis:
    """GMGN筹码结构分析"""

    def __init__(self):
        pass

    def analyze(self, ca: str, chain: str = 'sol') -> dict:
        """从GMGN API拉取筹码结构数据并分析"""
        from gmgn_api import GMGNAPI
        gmgn = GMGNAPI()
        info = gmgn.get_full_token_analysis(ca, chain=chain)

        i = info.get('info', {})
        s = info.get('security', {})
        stat = i.get('stat', {})
        wts = i.get('wallet_tags_stat', {})
        lock_summary = s.get('lock_summary', {})
        holders = info.get('holders', [])
        smart_holders = info.get('smart_holders', [])

        holder_count = i.get('holder_count', 0) or 0
        top10_rate = float(stat.get('top_10_holder_rate', 0) or 0)  # 0~1
        burn_ratio = float(s.get('burn_ratio', 0) or 0)              # 0~1
        dev_hold = float(stat.get('dev_team_hold_rate', 0) or 0)    # 0~1
        creator_hold = float(stat.get('creator_hold_rate', 0) or 0)  # 0~1
        bot_degen_rate = float(stat.get('bot_degen_rate', 0) or 0)  # 0~1
        fresh_wallet_rate = float(stat.get('fresh_wallet_rate', 0) or 0)  # 0~1

        smart_count = wts.get('smart_wallets', 0) or 0
        smart_rate = smart_count / holder_count if holder_count else 0

        sniper_count = wts.get('sniper_wallets', 0) or 0

        lock_info = lock_summary.get('lock_detail', [])
        lock_percent = sum(float(l.get('percent', 0)) for l in lock_info) if lock_info else 0
        is_locked = lock_summary.get('is_locked', False)

        # 计算TopHolder大车头（单个最大持仓占比）
        top1_rate = 0.0
        top3_rate = 0.0
        top5_rate = 0.0
        if holders:
            sorted_holders = sorted(holders, key=lambda h: float(h.get('amount_percentage', 0) or 0), reverse=True)
            if len(sorted_holders) >= 1:
                top1_rate = float(sorted_holders[0].get('amount_percentage', 0) or 0)
            if len(sorted_holders) >= 3:
                top3_rate = sum(float(h.get('amount_percentage', 0) or 0) for h in sorted_holders[:3])
            if len(sorted_holders) >= 5:
                top5_rate = sum(float(h.get('amount_percentage', 0) or 0) for h in sorted_holders[:5])

        # 计算聪明钱平均持仓（仅当前仍持有的）
        smart_avg_hold = 0.0
        active_smart = [h for h in smart_holders if h.get('balance', 0) and float(h.get('balance', 0)) > 0]
        if active_smart:
            smart_avg_hold = sum(float(h.get('amount_percentage', 0) or 0) for h in active_smart) / len(active_smart)

        # 计算套牢比例（有成本且当前亏损的holder）
        locked_holders = 0
        for h in holders:
            cost = float(h.get('cost', 0) or 0)
            profit_change = float(h.get('profit_change', 0) or 0)
            if cost > 0 and profit_change < 0:
                locked_holders += 1
        locked_rate = locked_holders / len(holders) if holders else 0

        return {
            'holder_count': holder_count,
            'top10_rate': top10_rate,
            'top1_rate': top1_rate,
            'top3_rate': top3_rate,
            'top5_rate': top5_rate,
            'burn_ratio': burn_ratio,
            'dev_hold': dev_hold,
            'creator_hold': creator_hold,
            'smart_count': smart_count,
            'smart_rate': smart_rate,
            'smart_avg_hold': smart_avg_hold,
            'sniper_count': sniper_count,
            'bot_degen_rate': bot_degen_rate,
            'fresh_wallet_rate': fresh_wallet_rate,
            'locked_rate': locked_rate,
            'is_locked': is_locked,
            'lock_percent': lock_percent,
            'holders': holders,
            'smart_holders': smart_holders,
        }

    def score_top_concentration(self, rate: float) -> float:
        """Top集中度评分"""
        if rate < 0.20:
            return 100
        elif rate < 0.30:
            return 90
        elif rate < 0.40:
            return 75
        elif rate < 0.50:
            return 60
        elif rate < 0.60:
            return 40
        else:
            return 20

    def score_burn_ratio(self, rate: float) -> float:
        """烧毁比例评分"""
        if rate >= 0.90:
            return 100
        elif rate >= 0.70:
            return 90
        elif rate >= 0.50:
            return 75
        elif rate >= 0.30:
            return 60
        else:
            return 30

    def score_smart_money(self, rate: float) -> float:
        """聪明钱占比评分"""
        if rate > 0.10:
            return 100
        elif rate > 0.05:
            return 85
        elif rate > 0.02:
            return 70
        elif rate > 0.01:
            return 55
        else:
            return 40

    def score_bot_degen(self, rate: float) -> float:
        """机器人/degen占比评分（越低越好）"""
        if rate < 0.10:
            return 100
        elif rate < 0.20:
            return 85
        elif rate < 0.30:
            return 70
        elif rate < 0.40:
            return 55
        else:
            return 30

    def score_locked(self, is_locked: bool, lock_percent: float) -> float:
        """锁仓评分"""
        if not is_locked:
            return 40
        if lock_percent >= 0.90:
            return 100
        elif lock_percent >= 0.70:
            return 90
        elif lock_percent >= 0.50:
            return 75
        elif lock_percent >= 0.30:
            return 60
        else:
            return 50

    def score_fresh_wallet(self, rate: float) -> float:
        """新钱包占比评分（越低越好，刷量风险低）"""
        if rate < 0.10:
            return 100
        elif rate < 0.20:
            return 85
        elif rate < 0.30:
            return 70
        elif rate < 0.40:
            return 55
        else:
            return 30

    def calculate_chip_score(self, chip: dict) -> dict:
        """计算筹码综合评分

        权重：Top10集中度30% + 烧毁比例25% + 聪明钱占比20% +
              机器人占比15% + 锁仓10%
        """
        top_s = self.score_top_concentration(chip['top10_rate'])
        burn_s = self.score_burn_ratio(chip['burn_ratio'])
        smart_s = self.score_smart_money(chip['smart_rate'])
        bot_s = self.score_bot_degen(chip['bot_degen_rate'])
        lock_s = self.score_locked(chip['is_locked'], chip['lock_percent'])

        composite = (
            top_s  * 0.30 +
            burn_s * 0.25 +
            smart_s * 0.20 +
            bot_s  * 0.15 +
            lock_s * 0.10
        )

        return {
            'chip_score': round(composite, 1),
            'top_concentration': top_s,
            'burn_ratio_score': burn_s,
            'smart_money': smart_s,
            'bot_degen': bot_s,
            'locked': lock_s,
        }


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
        lock_duration=180,
        # 持仓结构数据
        smart_volume=0.15,
        whale_volume=0.12,
        new_volume=0.25,
        old_volume=0.35,
        shit_volume=0.02,
        scam_volume=0.01
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
        has_website=True,
        # 持仓结构数据
        smart_volume=0.08,
        whale_volume=0.10,
        new_volume=0.40,
        old_volume=0.28,
        shit_volume=0.03,
        scam_volume=0.02
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
        twitter_followers=200,
        # 持仓结构数据（断头盘特征）
        smart_volume=0.02,
        whale_volume=0.03,
        new_volume=0.65,
        old_volume=0.08,
        shit_volume=0.08,
        scam_volume=0.04
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
