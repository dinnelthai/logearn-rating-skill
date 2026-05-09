#!/usr/bin/env python3
"""
持仓结构维度使用示例

展示如何使用LogEarn Skills API的持仓数据来识别断头盘和刷量币
"""

from rating_system import RatingSystem, TokenSignal


def example_healthy_holding():
    """示例1: 健康的持仓结构"""
    print("=" * 60)
    print("示例1: 健康的持仓结构（优质项目）")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    signal = TokenSignal(
        ca="healthy_token",
        symbol="GOOD",
        token_name="Good Project",
        description="AI powered",
        
        # 聪明钱数据
        smart_money_ratio=0.12,
        
        # 流动性数据
        pool_liquidity=100000,
        mcap=500000,
        
        # 持仓结构数据 - 健康特征
        smart_volume=0.18,      # 聪明钱持仓 18%
        whale_volume=0.15,      # 巨鲸持仓 15%
        new_volume=0.25,        # 新地址持仓 25% (健康范围)
        old_volume=0.38,        # 老地址持仓 38% (坚定持有者多)
        shit_volume=0.015,      # 垃圾地址持仓 1.5% (非常干净)
        scam_volume=0.005       # 诈骗地址持仓 0.5% (安全)
    )
    
    result = rating_system.calculate_rating(signal)
    
    print(f"\n总评分: {result['rating']}")
    print(f"评级: {result['grade']}")
    print(f"建议: {result['recommendation']}")
    print("\n各维度评分:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    # 详细分析持仓结构
    print("\n持仓结构分析:")
    print(f"  ✅ 聪明钱+巨鲸: {(signal.smart_volume + signal.whale_volume)*100:.1f}% (专业投资者认可)")
    print(f"  ✅ 新地址占比: {signal.new_volume*100:.1f}% (健康范围)")
    print(f"  ✅ 老地址占比: {signal.old_volume*100:.1f}% (坚定持有者多)")
    print(f"  ✅ 垃圾地址: {signal.shit_volume*100:.1f}% (非常干净)")
    print(f"  ✅ 诈骗地址: {signal.scam_volume*100:.1f}% (安全)")
    print()


def example_risky_holding():
    """示例2: 断头盘特征"""
    print("=" * 60)
    print("示例2: 断头盘特征（高风险项目）")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    signal = TokenSignal(
        ca="risky_token",
        symbol="RISK",
        token_name="Risky Token",
        
        # 聪明钱数据
        smart_money_ratio=0.03,
        
        # 流动性数据
        pool_liquidity=20000,
        mcap=150000,
        
        # 持仓结构数据 - 断头盘特征
        smart_volume=0.02,      # 聪明钱持仓 2% (很少)
        whale_volume=0.03,      # 巨鲸持仓 3% (很少)
        new_volume=0.68,        # 新地址持仓 68% ⚠️ 断头盘风险
        old_volume=0.08,        # 老地址持仓 8% (坚定持有者少)
        shit_volume=0.06,       # 垃圾地址持仓 6% ⚠️ 断头盘概率大
        scam_volume=0.03        # 诈骗地址持仓 3% ⚠️ 高风险
    )
    
    result = rating_system.calculate_rating(signal)
    
    print(f"\n总评分: {result['rating']}")
    print(f"评级: {result['grade']}")
    print(f"建议: {result['recommendation']}")
    print("\n各维度评分:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    # 详细分析持仓结构
    print("\n持仓结构分析:")
    print(f"  ❌ 聪明钱+巨鲸: {(signal.smart_volume + signal.whale_volume)*100:.1f}% (专业投资者不认可)")
    print(f"  ❌ 新地址占比: {signal.new_volume*100:.1f}% (>60% 断头盘风险)")
    print(f"  ❌ 老地址占比: {signal.old_volume*100:.1f}% (坚定持有者少)")
    print(f"  ❌ 垃圾地址: {signal.shit_volume*100:.1f}% (>4% 断头盘概率大)")
    print(f"  ❌ 诈骗地址: {signal.scam_volume*100:.1f}% (高风险)")
    print()


def example_moderate_holding():
    """示例3: 中等持仓结构"""
    print("=" * 60)
    print("示例3: 中等持仓结构（谨慎观察）")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    signal = TokenSignal(
        ca="moderate_token",
        symbol="MEME",
        token_name="Meme Coin",
        description="pepe dog",
        
        # 聪明钱数据
        smart_money_ratio=0.07,
        
        # 流动性数据
        pool_liquidity=40000,
        mcap=250000,
        
        # 持仓结构数据 - 中等特征
        smart_volume=0.09,      # 聪明钱持仓 9%
        whale_volume=0.08,      # 巨鲸持仓 8%
        new_volume=0.45,        # 新地址持仓 45% (一般)
        old_volume=0.25,        # 老地址持仓 25% (一般)
        shit_volume=0.035,      # 垃圾地址持仓 3.5% (可接受)
        scam_volume=0.015       # 诈骗地址持仓 1.5% (警惕)
    )
    
    result = rating_system.calculate_rating(signal)
    
    print(f"\n总评分: {result['rating']}")
    print(f"评级: {result['grade']}")
    print(f"建议: {result['recommendation']}")
    print("\n各维度评分:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    # 详细分析持仓结构
    print("\n持仓结构分析:")
    print(f"  ⚠️ 聪明钱+巨鲸: {(signal.smart_volume + signal.whale_volume)*100:.1f}% (一般)")
    print(f"  ⚠️ 新地址占比: {signal.new_volume*100:.1f}% (一般)")
    print(f"  ⚠️ 老地址占比: {signal.old_volume*100:.1f}% (一般)")
    print(f"  ✅ 垃圾地址: {signal.shit_volume*100:.1f}% (可接受)")
    print(f"  ⚠️ 诈骗地址: {signal.scam_volume*100:.1f}% (警惕)")
    print()


def compare_holding_structures():
    """示例4: 对比不同持仓结构"""
    print("=" * 60)
    print("示例4: 对比不同持仓结构的评分差异")
    print("=" * 60)
    
    rating_system = RatingSystem()
    
    # 基础配置（相同）
    base_config = {
        "symbol": "TEST",
        "token_name": "Test Token",
        "smart_money_ratio": 0.10,
        "pool_liquidity": 50000,
        "mcap": 300000,
    }
    
    # 三种不同的持仓结构
    holdings = [
        {
            "name": "优质持仓",
            "ca": "good",
            "smart_volume": 0.20,
            "whale_volume": 0.15,
            "new_volume": 0.20,
            "old_volume": 0.40,
            "shit_volume": 0.01,
            "scam_volume": 0.005,
        },
        {
            "name": "一般持仓",
            "ca": "medium",
            "smart_volume": 0.08,
            "whale_volume": 0.10,
            "new_volume": 0.40,
            "old_volume": 0.28,
            "shit_volume": 0.03,
            "scam_volume": 0.02,
        },
        {
            "name": "断头盘",
            "ca": "bad",
            "smart_volume": 0.02,
            "whale_volume": 0.03,
            "new_volume": 0.70,
            "old_volume": 0.05,
            "shit_volume": 0.08,
            "scam_volume": 0.05,
        },
    ]
    
    results = []
    for h in holdings:
        signal = TokenSignal(
            ca=h["ca"],
            **base_config,
            smart_volume=h["smart_volume"],
            whale_volume=h["whale_volume"],
            new_volume=h["new_volume"],
            old_volume=h["old_volume"],
            shit_volume=h["shit_volume"],
            scam_volume=h["scam_volume"],
        )
        
        result = rating_system.calculate_rating(signal)
        results.append({
            "name": h["name"],
            "rating": result["rating"],
            "holding_score": result["breakdown"]["holding_structure"],
            "new_volume": h["new_volume"],
            "shit_volume": h["shit_volume"],
        })
    
    print("\n对比结果:")
    print(f"{'持仓类型':<10} {'总评分':<8} {'持仓评分':<10} {'新地址%':<10} {'垃圾地址%':<10}")
    print("-" * 60)
    for r in results:
        print(f"{r['name']:<10} {r['rating']:<8.1f} {r['holding_score']:<10.1f} "
              f"{r['new_volume']*100:<10.1f} {r['shit_volume']*100:<10.1f}")
    
    print("\n结论:")
    print("  • 新地址占比和垃圾地址占比是识别断头盘的关键指标")
    print("  • 新地址>60% 或 垃圾地址>4% 会显著降低评分")
    print("  • 聪明钱+巨鲸持仓高的项目更值得信赖")
    print()


if __name__ == "__main__":
    example_healthy_holding()
    example_risky_holding()
    example_moderate_holding()
    compare_holding_structures()
