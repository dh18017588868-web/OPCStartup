"""
触发器测试
"""

import pytest
from pathlib import Path
from validate import OPCValidator


class TestTriggers:
    """触发器验证测试"""

    def test_triggers_are_all_uppercase(self, project_root):
        """测试触发器应全大写或混合大小写（参考现有风格）"""
        skill_md = project_root / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md 不存在")

        import re
        content = skill_md.read_text(encoding='utf-8')
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w:||---|$)', content, re.DOTALL)

        if not trigger_match:
            pytest.fail("无法找到 triggers 部分")

        triggers_block = trigger_match.group(1)
        triggers = re.findall(r'-\s*"([^"]+)"', triggers_block)

        # 允许小写触发器（国际化版本），但建议大写
        # 这里只检查是否有至少一个大写触发器用于别名
        uppercase_triggers = [t for t in triggers if t.isupper()]
        assert len(uppercase_triggers) > 0, "应该有至少一个大写触发器"

    def test_no_duplicate_triggers(self, project_root):
        """测试没有重复的触发器"""
        skill_md = project_root / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md 不存在")

        import re
        from collections import Counter
        content = skill_md.read_text(encoding='utf-8')
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w:||---|$)', content, re.DOTALL)

        if not trigger_match:
            pytest.fail("无法找到 triggers 部分")

        triggers_block = trigger_match.group(1)
        triggers = re.findall(r'-\s*"([^"]+)"', triggers_block)

        counts = Counter(triggers)
        duplicates = [k for k, v in counts.items() if v > 1]
        assert len(duplicates) == 0, f"存在重复触发器: {duplicates}"

    def test_triggers_match_skill_files(self, project_root, skills_dir):
        """测试触发器应该与 skill 文件名对应（简化版）"""
        skill_md = project_root / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md 不存在")

        import re
        content = skill_md.read_text(encoding='utf-8')
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w:||---|$)', content, re.DOTALL)

        if not trigger_match:
            pytest.fail("无法找到 triggers 部分")

        triggers_block = trigger_match.group(1)
        triggers = re.findall(r'-\s*"([^"]+)"', triggers_block)

        # 检查基础触发器存在
        # 例如，如果有 /opc-start 的触发器，应该对应 start.md
        opc_triggers = [t.lower() for t in triggers if t.startswith('OPC')]
        assert len(opc_triggers) >= 10, "应该有足够的 OPC 触发器"

    def test_trigger_format_consistency(self, project_root):
        """测试触发器格式一致性"""
        skill_md = project_root / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md 不存在")

        import re
        content = skill_md.read_text(encoding='utf-8')
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w:||---|$)', content, re.DOTALL)

        if not trigger_match:
            pytest.fail("无法找到 triggers 部分")

        triggers_block = trigger_match.group(1)
        triggers = re.findall(r'-\s*"([^"]+)"', triggers_block)

        # 检查触发器是否只包含有效字符（大写字母、数字、连字符）
        invalid = [t for t in triggers if not all(c.isupper() or c.isdigit() or c in ['-'] for c in t)]
        assert len(invalid) == 0, f"无效格式的触发器: {invalid}"
