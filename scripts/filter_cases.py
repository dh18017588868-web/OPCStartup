#!/usr/bin/env python3
"""
过滤案例库：根据类别、收入范围、技术栈等筛选案例
"""

import json
import argparse
from pathlib import Path

def load_cases(cases_dir):
    cases = []
    for file in cases_dir.glob("*.jsonl"):
        with open(file, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        cases.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return cases

def main():
    parser = argparse.ArgumentParser(description="Filter OPC case database")
    parser.add_argument("--category", help="Filter by category (e.g., saas, content, service, ecommerce)")
    parser.add_argument("--min-revenue", type=float, help="Minimum monthly revenue (USD)")
    parser.add_argument("--max-revenue", type=float, help="Maximum monthly revenue (USD)")
    parser.add_argument("--tech", help="Technology stack keyword (e.g., python, react, ruby)")
    parser.add_argument("--limit", type=int, default=10, help="Max number of results")
    args = parser.parse_args()
    
    cases_dir = Path(__file__).parent.parent / "references" / "cases"
    cases = load_cases(cases_dir)
    
    filtered = []
    for c in cases:
        if args.category and args.category.lower() not in c.get("category", "").lower():
            continue
        rev_min = c.get("revenue_min", 0)
        rev_max = c.get("revenue_max", rev_min)
        if args.min_revenue is not None and rev_max < args.min_revenue:
            continue
        if args.max_revenue is not None and rev_min > args.max_revenue:
            continue
        if args.tech:
            tools = " ".join(str(t).lower() for t in c.get("tools", []))
            if args.tech.lower() not in tools:
                continue
        filtered.append(c)
    
    filtered.sort(key=lambda x: x.get("revenue_max", 0) or x.get("revenue_min", 0), reverse=True)
    for c in filtered[:args.limit]:
        print(f"{c['id']}: {c['product']} by {c['author']} ({c.get('category')}) Revenue: ${c.get('revenue_min','?')}~${c.get('revenue_max','?')} /mo")
        print(f"   Tools: {', '.join(c.get('tools', []))}")
        print(f"   Source: {c.get('source_url')}\n")

if __name__ == "__main__":
    main()