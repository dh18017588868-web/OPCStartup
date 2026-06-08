#!/usr/bin/env python3
"""
OPC Startup 政策收集脚本
从政府官网收集OPC相关政策（政府发文、园区建设、公司补贴）
地区：江苏、浙江、上海（江浙沪）
合规：仅收集链接和摘要，尊重原创版权
"""

import json
import os
import re
import sys
import feedparser
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse

# Cookie和Session设置
requests.packages.urllib3.disable_warnings()

PROJECT_ROOT = Path(__file__).parent.parent
POLICIES_DIR = PROJECT_ROOT / "references" / "policies"
INDEX_FILE = POLICIES_DIR / "index.jsonl"
LOG_FILE = POLICIES_DIR / "collection.log"

# 地区配置（江浙沪 + 国家级参考）
REGIONS = {
    "national": {
        "name": "国家级",
        "rss_sources": [
            "http://www.gov.cn/xml/content.xml",  # 国务院
            "http://www.most.gov.cn/rss/举措.xml",  # 科技部
            "http://www.miit.gov.cn/rss/政策.xml",  # 工信部
        ]
    },
    "shanghai": {
        "name": "上海",
        "rss_sources": [
            "http://www.shanghai.gov.cn/rss/szfwj.xml",  # 市政府文件
            "http://www.shanghai.gov.cn/rss/gggs.xml",  # 公示公告
            "http://kw.shanghai.gov.cn/rss/政策文件.xml",  # 科委政策
        ]
    },
    "zhejiang": {
        "name": "浙江",
        "rss_sources": [
            "http://www.zj.gov.cn/col/col1543871/index.html",  # 省政府-政策文件
            # RSS XML地址（如果直接RSS不可用，尝试以下变体）
            "http://www.zj.gov.cn/module/web/jpage/dataproxy.jsp?appid=1&webid=1&path=/",
        ]
    },
    "jiangsu": {
        "name": "江苏",
        "rss_sources": [
            "http://www.jiangsu.gov.cn/col/col59345/index.html",  # 省政府-政策
        ]
    }
}

# 政策类型映射
POLICY_KEYWORDS = {
    "government": ["政策", "通知", "办法", "规定", "意见", "方案", "条例", "决定", "令"],
    "subsidies": ["补贴", "资助", "奖励", "扶持", "资金", "补助", "项目资金", "财政支持"],
    "park-construction": ["园区", "产业园", "孵化器", "基地", "示范区", "园区建设", "众创空间"]
}

# 用户代理（遵守robots.txt）
USER_AGENT = "OPCAgent/1.0 (OPC Startup Policy Collector; contact: opc-startup@noreply.github.com)"

def log(msg: str):
    """日志记录"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(f"[{timestamp}] {msg}")

def load_existing_policies() -> set:
    """加载已有政策ID集合，用于去重"""
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

def compute_content_hash(content: str) -> str:
    """计算内容hash用于去重"""
    import hashlib
    return hashlib.md5(content.encode("utf-8")).hexdigest()[:12]

def classify_policy_type(title: str, summary: str) -> str:
    """政策类型分类（基于关键词）"""
    text = (title + " " + summary).lower()
    for ptype, keywords in POLICY_KEYWORDS.items():
        if any(kw.lower() in text for kw in keywords):
            return ptype
    return "government"  # 默认为政府发文

def extract_region_from_url(url: str) -> str:
    """从URL提取地区标识"""
    parsed = urlparse(url)
    netloc = parsed.netloc.lower()
    if "shanghai" in netloc or "sh.gov.cn" in netloc:
        return "shanghai"
    elif "zhejiang" in netloc or "zj.gov.cn" in netloc:
        return "zhejiang"
    elif "jiangsu" in netloc or "js.gov.cn" in netloc:
        return "jiangsu"
    elif "gov.cn" in netloc:
        return "national"
    return "unknown"

def clean_summary(text: str, max_length: int = 500) -> str:
    """清理摘要文本，移除多余空白，截断"""
    if not text:
        return ""
    # 移除HTML标签（简单）
    text = re.sub(r'<[^>]+>', ' ', text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text)
    # 截断
    if len(text) > max_length:
        text = text[:max_length].rstrip() + "..."
    return text.strip()

def fetch_rss_feed(url: str, region_hint: str) -> List[Dict]:
    """从单个RSS源抓取政策信息"""
    policies = []
    try:
        log(f"抓取 RSS: {url}")
        feed = feedparser.parse(url)

        if feed.bozo:  # 有解析错误
            log(f"⚠️  RSS解析警告: {feed.bozo_exception}")

        # 取最近20条
        for entry in feed.entries[:20]:
            title = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            summary = clean_summary(entry.get('summary', entry.get('description', '')))

            if not title or not link:
                continue

            # 政策内容过滤：必须包含政策关键词
            full_text = (title + " " + summary).lower()
            if not any(kw in full_text for kw in ["opc", "一人公司", "小微企业", "初创", "创业", "补贴", "扶持", "政策"]):
                continue

            # 确定地区
            region = extract_region_from_url(link)
            if region == "unknown":
                region = region_hint

            # 分类
            policy_type = classify_policy_type(title, summary)

            # 生成ID（基于URL）
            url_hash = compute_content_hash(link)
            policy_id = f"{region}-{policy_type[:4]}-{url_hash}"

            # 检查是否已存在
            existing_ids = load_existing_policies()
            if policy_id in existing_ids:
                continue

            policy = {
                "id": policy_id,
                "title": title[:200],
                "url": link,
                "summary": summary,
                "region": region,
                "region_name": REGIONS.get(region, {}).get("name", region),
                "policy_type": policy_type,
                "source": "RSS:" + url,
                "published_at": entry.get('published', ''),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "content_hash": compute_content_hash(title + summary)
            }
            policies.append(policy)
            log(f"  ✅ {title[:60]}... ({region}, {policy_type})")

        log(f"  📊 {url}: 抓取 {len(feed.entries)} 条，有效政策 {len(policies)} 条")

    except Exception as e:
        log(f"❌ RSS抓取失败 {url}: {str(e)}")
        import traceback
        log(f"   详情: {traceback.format_exc()}")

    return policies

def save_policies(policies: List[Dict]):
    """保存政策数据到结构化目录"""
    POLICIES_DIR.mkdir(parents=True, exist_ok=True)

    for policy in policies:
        # 写入主索引
        with open(INDEX_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(policy, ensure_ascii=False) + "\n")

        # 按地区分类存储
        region_dir = POLICIES_DIR / "by-region" / policy["region"]
        region_dir.mkdir(parents=True, exist_ok=True)
        with open(region_dir / f"{policy['id']}.json", "w", encoding="utf-8") as f:
            json.dump(policy, f, indent=2, ensure_ascii=False)

        # 按类型分类存储
        type_dir = POLICIES_DIR / "by-type" / policy["policy_type"]
        type_dir.mkdir(parents=True, exist_ok=True)
        with open(type_dir / f"{policy['id']}.json", "w", encoding="utf-8") as f:
            json.dump(policy, f, indent=2, ensure_ascii=False)

def main():
    log("=" * 60)
    log("开始政策收集 (江浙沪地区)")
    log(f"输出目录: {POLICIES_DIR}")

    # 确保目录存在
    POLICIES_DIR.mkdir(parents=True, exist_ok=True)

    existing_ids = load_existing_policies()
    log(f"已有政策数: {len(existing_ids)}")

    all_new = []

    # 遍历所有地区RSS源
    for region, config in REGIONS.items():
        log(f"\n地区: {config['name']} ({region})")
        for url in config["rss_sources"]:
            try:
                policies = fetch_rss_feed(url, region)
                for p in policies:
                    if p["content_hash"] not in existing_ids:
                        all_new.append(p)
            except Exception as e:
                log(f"  跳过源 {url}: {e}")

    # 去重（基于content_hash）
    seen_hashes = set()
    unique_new = []
    for p in all_new:
        if p["content_hash"] not in seen_hashes:
            seen_hashes.add(p["content_hash"])
            unique_new.append(p)

    # 保存
    if unique_new:
        save_policies(unique_new)
        log(f"\n✅ 收集完成！新增 {len(unique_new)} 条政策")
    else:
        log("\nℹ️  本次无新政策")

    # 统计
    if INDEX_FILE.exists():
        total = len(list(INDEX_FILE.open(encoding="utf-8")))
        log(f"索引总数: {total}")
        # 按地区统计
        if total > 0:
            log("\n📈 统计:")
            for region in REGIONS.keys():
                count = len(list((POLICIES_DIR / "by-region" / region).glob("*.json")))
                if count > 0:
                    log(f"  {REGIONS[region]['name']}: {count} 条")

    return 0

if __name__ == "__main__":
    sys.exit(main())