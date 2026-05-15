#!/usr/bin/env python3
"""
OPC Startup 项目验证脚本
检查项目完整性、引用一致性、格式规范等
"""

import os
import re
import sys
from pathlib import Path
from collections import Counter

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def info(msg):
    print(f"{colors.OKBLUE}ℹ {msg}{colors.ENDC}")

def success(msg):
    print(f"{colors.OKGREEN}✓ {msg}{colors.ENDC}")

def warning(msg):
    print(f"{colors.WARNING}⚠ {msg}{colors.ENDC}")

def fail(msg):
    print(f"{colors.FAIL}✗ {msg}{colors.ENDC}")

def header(msg):
    print(f"\n{colors.HEADER}{colors.BOLD}=== {msg} ==={colors.ENDC}")

class OPCValidator:
    def __init__(self, project_root):
        self.project = Path(project_root).resolve()
        self.errors = 0
        self.warnings = 0
        self.passed = 0
    
    def check(self, condition, fail_msg=None, warn_msg=None, success_msg=None):
        if condition:
            if success_msg:
                success(success_msg)
            self.passed += 1
            return True
        else:
            if fail_msg:
                fail(fail_msg)
                self.errors += 1
            return False
    
    def run_all(self):
        header("OPC Startup 项目验证")
        
        self.check_required_files()
        self.check_license()
        self.check_skills_structure()
        self.check_skill_triggers()
        self.check_references()
        self.check_quick_md_structure()
        self.check_tables()
        self.check_encoding()
        
        self.summary()
        return self.errors
    
    def check_required_files(self):
        header("必需文件检查")
        required = ["README.md", "SKILL.md"]
        for f in required:
            path = self.project / f
            self.check(
                path.exists(),
                fail_msg=f"缺少必需文件: {f}",
                success_msg=f"{f} 存在"
            )
    
    def check_license(self):
        header("许可证检查")
        license_path = self.project / "LICENSE"
        if license_path.exists():
            with open(license_path) as f:
                content = f.read(100).lower()
            if "mit" in content:
                success("LICENSE 文件存在且为 MIT")
                self.passed += 1
            else:
                warning("LICENSE 文件存在但可能不是 MIT")
                self.warnings += 1
        else:
            fail("缺少 LICENSE 文件")
            self.errors += 1
    
    def check_skills_structure(self):
        header("技能文件完整性")
        skills_dir = self.project / "skills"
        if not skills_dir.exists():
            fail("skills 目录不存在")
            self.errors += 1
            return
        
        expected_skills = [
            "start.md", "validate.md", "mvp.md", "canvas.md",
            "pricing.md", "review.md", "launch.md", "diagnosis.md",
            "tools.md", "cases.md", "fetch.md", "all.md",
            "code.md", "quick.md", "iterate.md", "generate.md"
        ]
        
        existing = [f.name for f in skills_dir.glob("*.md")]
        
        for skill in expected_skills:
            if skill in existing:
                success(f"技能文件存在: {skill}")
            else:
                fail(f"缺失技能文件: {skill}")
                self.errors += 1
        
        # 检查是否有额外文件
        extra = set(existing) - set(expected_skills)
        if extra:
            warning(f"额外技能文件: {extra}")
    
    def check_skill_triggers(self):
        header("SKILL.md 触发器检查")
        skill_md = self.project / "SKILL.md"
        if not skill_md.exists():
            return
        
        with open(skill_md) as f:
            content = f.read()
        
        # 提取触发器
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w+:|---|$)', content, re.DOTALL)
        if not trigger_match:
            fail("无法找到 triggers 部分")
            self.errors += 1
            return
        
        triggers_block = trigger_match.group(1)
        triggers = re.findall(r'-\s*"([^"]+)"', triggers_block)
        
        success(f"触发器数量: {len(triggers)}")
        
        # 检查重复
        dup = [k for k,v in Counter(triggers).items() if v>1]
        if dup:
            fail(f"重复触发器: {dup}")
            self.errors += 1
        else:
            success("无重复触发器")
        
        # 检查大小写规范（应全大写或混合）
        lower_triggers = [t for t in triggers if t.islower()]
        if lower_triggers:
            warning(f"小写触发器(建议大写): {lower_triggers}")
        else:
            success("触发器大小写规范")
    
    def check_references(self):
        header("引用文档存在性")
        refs_dir = self.project / "references"
        if not refs_dir.exists():
            warning("references 目录不存在")
            return
        
        refs = list(refs_dir.glob("*.md"))
        success(f"引用文档数量: {len(refs)}")
        
        # 检查编号连续性
        numbers = []
        for f in refs:
            m = re.match(r'^(\d+)-', f.name)
            if m:
                numbers.append(int(m.group(1)))
        
        if numbers:
            numbers.sort()
            min_n, max_n = min(numbers), max(numbers)
            expected = set(range(min_n, max_n+1))
            missing = expected - set(numbers)
            if missing:
                warning(f"编号不连续，缺失: {sorted(missing)}")
            else:
                success(f"编号连续 {min_n}-{max_n}")
    
    def check_quick_md_structure(self):
        header("quick.md 结构检查")
        quick_md = self.project / "skills" / "quick.md"
        if not quick_md.exists():
            return
        
        with open(quick_md) as f:
            content = f.read()
        
        required_sections = ["## 角色", "## 工作流程", "## 输出格式"]
        for section in required_sections:
            if section in content:
                success(f"quick.md 包含: {section}")
            else:
                fail(f"quick.md 缺少: {section}")
                self.errors += 1
    
    def check_tables(self):
        header("Markdown 表格格式")
        # 简单的表格列数一致性检查
        table_pattern = re.compile(r'\n\|[^\n]+\n\|[-\s\|:]+\n(?:\|[^\n]+\n?)+')
        
        issues = []
        for md_file in self.project.rglob("*.md"):
            with open(md_file) as f:
                content = f.read()
            
            tables = table_pattern.findall(content)
            for table in tables:
                lines = table.strip().split('\n')
                col_counts = [line.count('|') for line in lines]
                if len(set(col_counts)) > 1:
                    issues.append(md_file.name)
                    break
        
        if issues:
            warning(f"表格可能不一致的文件: {issues}")
            self.warnings += 1
        else:
            success("所有表格格式一致")
    
    def check_encoding(self):
        header("文件编码检查")
        # 检查非UTF-8文件
        for md_file in self.project.rglob("*.md"):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    f.read()
            except UnicodeDecodeError:
                fail(f"文件可能不是UTF-8: {md_file.name}")
                self.errors += 1
        
        success("所有 Markdown 文件为 UTF-8 编码")
    
    def summary(self):
        header("验证结果摘要")
        total = self.passed + self.errors
        print(f"总计: {total} 项检查")
        print(f"{colors.OKGREEN}通过: {self.passed}{colors.ENDC}")
        if self.warnings:
            print(f"{colors.WARNING}警告: {self.warnings}{colors.ENDC}")
        if self.errors:
            print(f"{colors.FAIL}错误: {self.errors}{colors.ENDC}")
        else:
            print(f"{colors.OKGREEN}所有检查通过!{colors.ENDC}")

if __name__ == "__main__":
    project_root = os.getenv("PROJECT_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    validator = OPCValidator(project_root)
    sys.exit(validator.run_all())
