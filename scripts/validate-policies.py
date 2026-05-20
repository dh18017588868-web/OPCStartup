#!/usr/bin/env python3
"""
OPC Startup 政策数据验证脚本
检查政策数据的完整性、格式正确性和合规性
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
POLICIES_DIR = PROJECT_ROOT / "references" / "policies"
INDEX_FILE = POLICIES_DIR / "index.jsonl"

class PolicyValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = 0

    def log_error(self, msg: str):
        self.errors.append(msg)
        print(f"❌ {msg}")

    def log_warning(self, msg: str):
        self.warnings.append(msg)
        print(f"⚠️  {msg}")

    def log_pass(self, msg: str):
        self.passed += 1
        print(f"✅ {msg}")

    def validate_policy_item(self, policy: dict, line_num: int):
        """验证单条政策记录"""
        required_fields = ["id", "title", "url", "summary", "region", "region_name", "policy_type", "collected_at"]

        # 必需字段检查
        for field in required_fields:
            if field not in policy:
                self.log_error(f"行{line_num}: 缺少必需字段 '{field}'")
                return False

        # ID格式
        policy_id = policy.get("id", "")
        if not re.match(r'^[a-z]+-[a-z0-9]+-[a-f0-9]+$', policy_id):
            self.log_warning(f"行{line_num}: ID格式不规范: {policy_id}")

        # URL有效性
        url = policy.get("url", "")
        if not url.startswith("http"):
            self.log_error(f"行{line_num}: URL格式无效: {url}")
        elif not ("gov.cn" in url or ".org" in url):
            self.log_warning(f"行{line_num}: URL非gov.cn或org域名，请确认版权合规: {url}")

        # 标题长度
        title = policy.get("title", "")
        if len(title) > 200:
            self.log_warning(f"行{line_num}: 标题过长({len(title)}字符): {title[:50]}...")

        # 摘要长度（合规要求）
        summary = policy.get("summary", "")
        if len(summary) > 500:
            self.log_warning(f"行{line_num}: 摘要过长({len(summary)}字符)，建议精简")
        if len(summary) < 10:
            self.log_warning(f"行{line_num}: 摘要过短({len(summary)}字符): {summary}")

        # 地区字段
        region = policy.get("region", "")
        if region not in ["national", "shanghai", "zhejiang", "jiangsu", "beijing"]:
            self.log_warning(f"行{line_num}: 未知地区代码: {region}")

        # 政策类型
        policy_type = policy.get("policy_type", "")
        if policy_type not in ["government", "subsidies", "park-construction", "tax-incentives"]:
            self.log_warning(f"行{line_num}: 未知政策类型: {policy_type}")

        # 时间格式
        published = policy.get("published_at", "")
        if published:
            # 尝试解析常见格式
            for fmt in ["%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
                try:
                    datetime.strptime(published, fmt)
                    break
                except ValueError:
                    continue
            else:
                self.log_warning(f"行{line_num}: 发布时间格式无法识别: {published}")

        collected = policy.get("collected_at", "")
        if not collected:
            self.log_error(f"行{line_num}: 缺少 collected_at 字段")
        else:
            try:
                datetime.strptime(collected, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                self.log_warning(f"行{line_num}: collected_at格式错误: {collected}")

        # content_hash存在且格式正确
        content_hash = policy.get("content_hash", "")
        if not content_hash or len(content_hash) != 12:
            self.log_warning(f"行{line_num}: content_hash格式错误: {content_hash}")

        # 版权合规检查：没有full_text字段（避免存储全文）
        if "full_text" in policy:
            self.log_error(f"行{line_num}: ⚠️ 版权违规：不应存储全文内容（full_text字段）")

        # 检查是否有过度摘要（接近原文）
        if len(summary) > 300 and summary in title:
            self.log_warning(f"行{line_num}: 摘要可能是全文复制，存在版权风险")

        self.log_pass(f"行{line_num}: 基本格式正确")
        return True

    def validate_files_structure(self):
        """验证目录结构"""
        if not POLICIES_DIR.exists():
            self.log_error(f"政策目录不存在: {POLICIES_DIR}")
            return False

        required_dirs = ["by-region", "by-type"]
        for d in required_dirs:
            dir_path = POLICIES_DIR / d
            if not dir_path.exists():
                self.log_warning(f"缺少目录: {dir_path}")
            else:
                self.log_pass(f"目录存在: {d}/")

        return True

    def run(self) -> int:
        """运行验证"""
        print("=" * 60)
        print("🔍 政策数据验证")
        print(f"索引文件: {INDEX_FILE}")
        print("=" * 60)

        # 检查索引文件
        if not INDEX_FILE.exists():
            self.log_error(f"索引文件不存在: {INDEX_FILE}")
            return 1

        # 验证文件结构
        self.validate_files_structure()

        # 逐行验证JSONL
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total = len(lines)
        print(f"\n📊 总记录数: {total}\n")

        imported = False
        try:
            import re as regex_module
            globals()['re'] = regex_module
            imported = True
        except ImportError:
            print("⚠️  re模块不可用，跳过正则检查")

        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                policy = json.loads(line)
                self.validate_policy_item(policy, i)
            except json.JSONDecodeError as e:
                self.log_error(f"行{i}: JSON解析失败 - {e}")

        # 总结
        print("\n" + "=" * 60)
        print("📈 验证结果")
        print("=" * 60)
        print(f"总计记录: {total}")
        print(f"通过检查: {self.passed}")
        print(f"警告: {len(self.warnings)}")
        print(f"错误: {len(self.errors)}")

        if self.warnings:
            print("\n⚠️  警告列表:")
            for w in self.warnings[:10]:  # 只显示前10条
                print(f"  - {w}")
            if len(self.warnings) > 10:
                print(f"  ... 还有 {len(self.warnings)-10} 条警告")

        if self.errors:
            print("\n❌ 错误列表:")
            for e in self.errors:
                print(f"  - {e}")
            print("\n❌ 验证失败！请修复错误后重新提交。")
            return 1

        if self.warnings:
            print("\n⚠️  发现警告，建议修复。")
            return 0  # 警告不阻塞流程
        else:
            print("\n✅ 所有检查通过！数据质量良好。")
            return 0

if __name__ == "__main__":
    validator = PolicyValidator()
    sys.exit(validator.run())