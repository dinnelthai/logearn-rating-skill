#!/usr/bin/env python3
"""
评分系统使用示例
"""

from rating_system import RatingSystem, TokenSignal


def example_1_top_ai_coin():
    """示例1: 顶级AI币（有DexScreener推广）"""
    print("=" * 60)
    print("示例1: 顶级AI币（有DexScreener推广）")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    signal = TokenSignal(
        ca="example_ai_coin",
        symbol="AI",
        token_name="AI Agent",
        description="GPT powered agent",
        
        # 真实性数据
        new_wallet_ratio=0.35,
        shit_wallet_ratio=0.03,
        buyer_count=350,
        
        # 聪明钱数据
        smart_money_ratio=0.12,
        
        # 流动性数据
        pool_liquidity=50000,
        mcap=300000,
        
        # 推广数据
        has_dexscreener_ads=True,
        dex_ad_position="promoted",
        dex_ad_duration=7,
        twitter_followers=8000,
        telegram_members=3000,
        has_website=True,
        has_whitepaper=True,
        
        # 安全性数据
        liquidity_locked=True,
        lock_duration=180
    )
    
    result = rating_system.calculate_rating(signal)
    
    print(f"\n总评分: {result['rating']}")
    print(f"评级: {result['grade']}")
    print(f"建议: {result['recommendation']}")
    print("\n各维度评分:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    print()


def example_2_meme_coin():
    """示例2: 普通MEME币（无推广）"""
    print("=" * 60)
    print("示例2: 普通MEME币（无推广）")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    signal = TokenSignal(
        ca="example_meme_coin",
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
    
    result = rating_system.calculate_rating(signal)
    
    print(f"\n总评分: {result['rating']}")
    print(f"评级: {result['grade']}")
    print(f"建议: {result['recommendation']}")
    print("\n各维度评分:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    print()


def example_3_scam_coin():
    """示例3: 刷量垃圾币"""
    print("=" * 60)
    print("示例3: 刷量垃圾币")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    signal = TokenSignal(
        ca="example_scam_coin",
        symbol="SCAM",
        token_name="Random Token",
        
        new_wallet_ratio=0.70,      # 严重刷量
        shit_wallet_ratio=0.12,     # 垃圾钱包多
        buyer_count=80,
        smart_money_ratio=0.01,
        pool_liquidity=5000,
        mcap=100000,
        
        twitter_followers=200
    )
    
    result = rating_system.calculate_rating(signal)
    
    print(f"\n总评分: {result['rating']}")
    print(f"评级: {result['grade']}")
    print(f"建议: {result['recommendation']}")
    print("\n各维度评分:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    print()


def example_4_batch_rating():
    """示例4: 批量评分和筛选"""
    print("=" * 60)
    print("示例4: 批量评分和筛选")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    # 创建多个信号
    signals = [
        TokenSignal(
            ca="coin1", symbol="AI", token_name="AI Agent",
            new_wallet_ratio=0.35, shit_wallet_ratio=0.03,
            buyer_count=350, smart_money_ratio=0.12,
            pool_liquidity=50000, mcap=300000
        ),
        TokenSignal(
            ca="coin2", symbol="PEPE", token_name="Pepe Dog",
            new_wallet_ratio=0.45, shit_wallet_ratio=0.04,
            buyer_count=200, smart_money_ratio=0.06,
            pool_liquidity=30000, mcap=250000
        ),
        TokenSignal(
            ca="coin3", symbol="SCAM", token_name="Random",
            new_wallet_ratio=0.70, shit_wallet_ratio=0.12,
            buyer_count=80, smart_money_ratio=0.01,
            pool_liquidity=5000, mcap=100000
        )
    ]
    
    # 批量评分
    results = []
    for signal in signals:
        result = rating_system.calculate_rating(signal)
        results.append({
            "ca": signal.ca,
            "symbol": signal.symbol,
            "rating": result["rating"],
            "grade": result["grade"]
        })
    
    # 按评分排序
    results.sort(key=lambda x: x["rating"], reverse=True)
    
    print("\n评分排行:")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['symbol']} - {r['rating']}分 {r['grade']}")
    
    # 筛选优质币
    good_coins = [r for r in results if r["rating"] >= 60]
    print(f"\n优质币数量: {len(good_coins)}/{len(results)}")
    print()


if __name__ == "__main__":
    example_1_top_ai_coin()
    example_2_meme_coin()
    example_3_scam_coin()
    example_4_batch_rating()
