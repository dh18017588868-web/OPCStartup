#!/usr/bin/env python3
"""
交互式定价计算器：根据成本和竞品给出价格建议。
"""

def input_float(prompt, allow_empty=False):
    while True:
        val = input(prompt)
        if allow_empty and not val:
            return None
        try:
            return float(val)
        except ValueError:
            print("请输入有效的数字")

def main():
    print("💰 定价计算器（基于成本+价值）\n")
    monthly_cost = input_float("每月总成本（服务器、API、人力等，元）: ")
    target_margin = input_float("目标利润率（%，如 30）: ") / 100
    competitor_price = input_float("竞品月付价格（如已知，否则回车跳过）: ", allow_empty=True)
    
    # 简化：假设 100 个用户来算人均成本
    est_users = 100
    cost_per_user = monthly_cost / est_users if est_users else 0
    base_price = cost_per_user * (1 + target_margin)
    
    tiers = []
    tiers.append(("免费", 0))
    basic = max(base_price, 19)
    tiers.append(("基础", round(basic, 0)))
    pro = max(base_price * 3, 49)
    tiers.append(("专业", round(pro, 0)))
    enterprise = max(base_price * 10, 199)
    tiers.append(("企业", round(enterprise, 0)))
    
    print("\n📊 建议价格档位（月付）:")
    for name, price in tiers:
        if price == 0:
            print(f"- {name}: 免费")
        else:
            print(f"- {name}: ¥{price:.0f}/月")
    
    import json
    result = {
        "monthly_cost": monthly_cost,
        "target_margin": target_margin,
        "estimated_users": est_users,
        "cost_per_user": cost_per_user,
        "suggestions": [{"name": n, "price": p} for n,p in tiers]
    }
    with open("pricing_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("\n结果已保存至 pricing_output.json")

if __name__ == "__main__":
    main()