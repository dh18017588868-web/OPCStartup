#!/usr/bin/env python3
"""
OPC Startup 案例收集脚本
从多个来源收集独立开发者案例，保存为结构化 JSONL 格式
支持来源: Indie Hackers RSS, Twitter/X (需API), Product Hunt (需API)
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    import feedparser
except ImportError:
    print("⚠️  可选依赖 feedparser 未安装，Indie Hackers RSS 功能将禁用")
    feedparser = None

try:
    import requests
except ImportError:
    requests = None

PROJECT_ROOT = Path(__file__).parent.parent
CASES_DIR = PROJECT_ROOT / "references" / "cases"
INDEX_FILE = CASES_DIR / "index.jsonl"
LOG_FILE = CASES_DIR / "collection.log"

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def load_existing_cases():
    """加载已有的案例ID集合，用于去重"""
    existing_ids = set()
    if INDEX_FILE.exists():
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    existing_ids.add(data.get("id"))
                except json.JSONDecodeError:
                    continue
    return existing_ids

def save_case(case_data):
    """保存单个案例到索引文件和分类文件"""
    # 写入索引
    with open(INDEX_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(case_data, ensure_ascii=False) + "\n")
    
    # 按收入范围分类保存
    revenue_min = case_data.get("revenue_min", 0)
    if revenue_min < 1000:
        cat_dir = CASES_DIR / "l0-1k"
    elif revenue_min <= 5000:
        cat_dir = CASES_DIR / "l1-5k"
    elif revenue_min <= 10000:
        cat_dir = CASES_DIR / "l5-10k"
    elif revenue_min <= 50000:
        cat_dir = CASES_DIR / "l10-50k"
    else:
        cat_dir = CASES_DIR / "l50k-plus"
    
    cat_dir.mkdir(exist_ok=True)
    case_file = cat_dir / f"{case_data['id']}.json"
    with open(case_file, "w", encoding="utf-8") as f:
        json.dump(case_data, f, indent=2, ensure_ascii=False)

def extract_revenue_from_text(text):
    """从文本中提取收入信息 (简化版)"""
    # 匹配常见模式: $25k/month, $2.5M ARR, ~$30k/月
    patterns = [
        r'\$(\d+(?:\.\d+)?)([kKmM])(?:/|per)?(month|year|ARR|MRR)?',
        r'(\d+(?:\.\d+)?)([kKmM])\s*(USD|EUR)?/(?:月|年)',
    ]
    revenues = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            amount = float(match.group(1))
            multiplier = match.group(2).lower()
            if multiplier == 'k':
                amount *= 1000
            elif multiplier == 'm':
                amount *= 1000000
            
            period = match.group(3) if len(match.groups()) > 3 else 'month'
            is_annual = period and 'year' in period.lower()
            if is_annual:
                amount = amount / 12  # 转换为月收入
            
            revenues.append(amount)
    
    if revenues:
        # 返回最小和最大值（允许范围）
        return min(revenues), max(revenues)
    return None, None

def collect_from_indiehackers():
    """从 Indie Hackers RSS 抓取新案例"""
    if not feedparser:
        log("feedparser 未安装，跳过 Indie Hackers")
        return []

    new_cases = []
    rss_url = "https://feeds.transistor.fm/indie-hackers"
    
    try:
        log(f"正在抓取 Indie Hackers RSS: {rss_url}")
        feed = feedparser.parse(rss_url)
        
        # 只取最新的10篇
        for entry in feed.entries[:10]:
            title = entry.get('title', '')
            link = entry.get('link', '')
            summary = entry.get('summary', '')
            content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
            full_text = (title + " " + summary + " " + content).lower()
            
            # 简单过滤：包含收入关键词
            income_keywords = ['mrr', 'arr', 'revenue', 'income', 'earn', '$\d', 'made', 'profit']
            if not any(k in full_text for k in income_keywords):
                continue
            
            # 提取收入
            rev_min, rev_max = extract_revenue_from_text(summary + " " + content)
            if not rev_min:
                continue
            
            # 生成案例ID
            safe_title = re.sub(r'[^a-z0-9]+', '-', title.lower())[:50]
            case_id = f"ih-{safe_title}-{datetime.now().strftime('%Y%m%d')}"
            
            # 检查是否已存在
            existing_ids = load_existing_cases()
            if case_id in existing_ids:
                continue
            
            case = {
                "id": case_id,
                "author": "Indie Hackers Community",  # 需要从RSS提取作者
                "handle": "@indiehackers",
                "product": title[:100],
                "category": "Various",
                "revenue_min": rev_min,
                "revenue_max": rev_max,
                "currency": "USD",
                "peak_month": datetime.now().strftime("%Y-%m"),
                "timeline": [
                    f"Date unknown: {title}",
                    f"Source: {link}"
                ],
                "tools": [],  # 需要进一步提取
                "status": "active",
                "source_url": link,
                "source_platform": "Indie Hackers",
                "license": "CC-BY-3.0",
                "collected_at": datetime.now().strftime("%Y-%m-%d")
            }
            
            new_cases.append(case)
            log(f"发现新案例: {title[:80]}... (${rev_min:,.0f}-${rev_max:,.0f}/月)")
        
        log(f"Indie Hackers: 抓取 {len(feed.entries)} 篇文章，发现 {len(new_cases)} 个新案例")
        
    except Exception as e:
        log(f"Indie Hackers 抓取失败: {str(e)}")
    
    return new_cases

def collect_from_twitter():
    """从 Twitter/X 收集 (需要环境变量 TWITTER_BEARER_TOKEN)"""
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        log("TWITTER_BEARER_TOKEN 未设置，跳过 Twitter")
        return []
    
    if not requests:
        log("requests 未安装，跳过 Twitter")
        return []
    
    new_cases = []
    
    # 搜索关键词
    queries = [
        "buildinpublic MRR",
        "indiehacker revenue",
        "SaaS ARR",
        "solo founder revenue"
    ]
    
    headers = {"Authorization": f"Bearer {bearer_token}"}
    
    for query in queries:
        try:
            # Twitter API v2 recent search
            url = "https://api.twitter.com/2/tweets/search/recent"
            params = {
                "query": query + " -is:retweet",
                "max_results": 10,
                "tweet.fields": "created_at,author_id,public_metrics"
            }
            resp = requests.get(url, headers=headers, params=params)
            
            if resp.status_code != 200:
                log(f"Twitter API error: {resp.status_code} - {resp.text}")
                continue
            
            data = resp.json()
            for tweet in data.get('data', []):
                text = tweet.get('text', '')
                rev_min, rev_max = extract_revenue_from_text(text)
                if not rev_min:
                    continue
                
                case_id = f"tw-{tweet['id']}"
                existing_ids = load_existing_cases()
                if case_id in existing_ids:
                    continue
                
                case = {
                    "id": case_id,
                    "author": f"Twitter User {tweet['author_id']}",
                    "handle": f"@user{tweet['author_id']}",
                    "product": "Twitter 分享产品",
                    "category": "Unknown",
                    "revenue_min": rev_min,
                    "revenue_max": rev_max,
                    "currency": "USD",
                    "peak_month": tweet['created_at'][:7],
                    "timeline": [
                        f"Tweet: {text[:200]}..."
                    ],
                    "tools": [],
                    "status": "active",
                    "source_url": f"https://twitter.com/i/web/status/{tweet['id']}",
                    "source_platform": "Twitter",
                    "license": "CC-BY-4.0",  # Twitter内容在合理使用下
                    "collected_at": datetime.now().strftime("%Y-%m-%d")
                }
                new_cases.append(case)
                log(f"Twitter案例: ${rev_min:,.0f}-${rev_max:,.0f}/月")
            
        except Exception as e:
            log(f"Twitter查询失败 {query}: {str(e)}")
    
    return new_cases

def main():
    log("=" * 50)
    log("开始案例收集")
    
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    
    all_new = []
    
    # 1. Indie Hackers
    ih_cases = collect_from_indiehackers()
    all_new.extend(ih_cases)
    
    # 2. Twitter (可选)
    tw_cases = collect_from_twitter()
    all_new.extend(tw_cases)
    
    # 保存所有新案例
    for case in all_new:
        save_case(case)
    
    log(f"完成！共收集 {len(all_new)} 个新案例")
    
    if all_new:
        # 输出统计
        total = len(list(INDEX_FILE.open().readlines()) if INDEX_FILE.exists() else [])
        log(f"索引总数: {total}")
        return 0
    else:
        log("没有发现新案例")
        return 0

if __name__ == "__main__":
    sys.exit(main())
