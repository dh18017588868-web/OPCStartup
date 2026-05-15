#!/usr/bin/env python3
"""
健康诊断：根据输入指标给出建议
"""

def input_float(prompt, allow_empty=False):
    while True:
        val = input(prompt)
        if allow_empty and not val:
            return None
        try:
            return float(val)
        except ValueError:
            print("请输入数字或留空跳过")

def main():
    print("🔍 产品健康诊断\n")
    try:
        dau = input_float("日活 (DAU): ")
        mau = input_float("月活 (MAU): ")
        day1 = input_float("次日留存 (%), 留空跳过: ", allow_empty=True)
        day7 = input_float("7日留存 (%), 留空跳过: ", allow_empty=True)
        arpu = input_float("ARPU (元/月): ")
    except KeyboardInterrupt:
        print("\n取消")
        return
    
    issues = []
    if dau is not None and mau is not None and mau > 0:
        stickiness = dau / mau
        print(f"\n📈 粘性指标: DAU/MAU = {stickiness:.2%}")
        if stickiness < 0.1:
            issues.append("DAU/MAU < 10% → 激活时刻不足或产品价值不明确")
        elif stickiness < 0.2:
            issues.append("DAU/MAU 10-20% → 尚可，可优化习惯养成")
    if day1 is not None:
        print(f"次日留存: {day1:.1f}%")
        if day1 < 30:
            issues.append("次日留存 < 30% → 新用户引导或Aha时刻需加强")
    if day7 is not None:
        print(f"7日留存: {day7:.1f}%")
        if day7 < 15:
            issues.append("7日留存 < 15% → 中短期留存不佳")
    if arpu is not None:
        print(f"ARPU: ¥{arpu:.2f}")
        if arpu < 10:
            issues.append("ARPU 偏低 → 考虑提价或增加高级功能")
    
    if issues:
        print("\n⚠️ 发现以下问题：")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
    else:
        print("\n✅ 所有指标看起来健康！")
    
    import json
    result = {
        "dau": dau,
        "mau": mau,
        "stickiness": dau/mau if dau and mau else None,
        "day1_retention": day1,
        "day7_retention": day7,
        "arpu": arpu,
        "issues": issues
    }
    with open("diagnostic_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("\n详细结果已保存至 diagnostic_output.json")

if __name__ == "__main__":
    main()