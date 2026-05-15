"""测试每个 skill 文件包含必要的示例输出和章节。"""

from pathlib import Path
import pytest

# 项目根目录假设：tests 在项目根下，skills 在根下
PROJECT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"

REQUIRED_SECTIONS = ["## 角色", "## 命令列表", "## 输出格式"]

def test_each_skill_has_example():
    """每个 skill 文件必须包含一个示例输出部分。"""
    for md_file in SKILLS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        assert "## 示例输出" in content or "## 示例对话" in content, \
            f"{md_file.name} 缺少示例输出（需要添加 ## 示例输出 或 ## 示例对话）"

def test_each_skill_has_required_sections():
    """每个 skill 必须包含角色、命令列表、输出格式三节。"""
    for md_file in SKILLS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        missing = [sec for sec in REQUIRED_SECTIONS if sec not in content]
        assert not missing, f"{md_file.name} 缺少必需章节: {missing}"

def test_example_contains_conversation():
    """示例输出应包含用户与助手的对话。"""
    for md_file in SKILLS_DIR.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        # 检查是否包含用户和助手的关键词（支持中英文）
        has_user = any(kw in content for kw in ["**用户**", "**User**", "User:", "用户："])
        has_assistant = any(kw in content for kw in ["**OPC助手**", "**Assistant**", "Assistant:", "助手："])
        if "## 示例输出" in content:
            assert has_user and has_assistant, f"{md_file.name} 的示例应包含用户和助手的对话"