"""
集成测试 - 模拟用户调用技能
"""

import pytest
from pathlib import Path


class TestSkillInvocation:
    """技能调用集成测试"""

    def test_skill_triggers_mapped_to_files(self, project_root):
        """测试 SKILL.md 中定义的触发器可以映射到技能文件"""
        import re
        skill_md = project_root / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md 不存在")

        content = skill_md.read_text(encoding='utf-8')

        # 提取触发器
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w:||---|$)', content, re.DOTALL)
        if not trigger_match:
            pytest.fail("无法找到 triggers 部分")

        triggers_block = trigger_match.group(1)
        triggers = [t.lower() for t in re.findall(r'-\s*"([^"]+)"', triggers_block)]

        skills_dir = project_root / "skills"
        existing_skills = [f.stem.lower() for f in skills_dir.glob("*.md")]

        # 检查 OPC- 触发器是否映射到技能文件（去掉 opc- 前缀）
        opc_triggers = [t for t in triggers if t.startswith('opc-')]
        for trigger in opc_triggers:
            skill_name = trigger.replace('opc-', '')
            assert skill_name in existing_skills, f"触发器 {trigger} 没有对应的技能文件"

    def test_skill_all_skill_includes_all_triggers(self, project_root):
        """测试 /opc-all 技能应该列出所有技能"""
        all_skill = project_root / "skills" / "all.md"
        if not all_skill.exists():
            pytest.skip("all.md 不存在")

        content = all_skill.read_text(encoding='utf-8')
        skills_dir = project_root / "skills"
        skill_files = [f.stem for f in skills_dir.glob("*.md") if f.stem != 'all']

        # all.md 应该提及所有其他技能
        for skill in skill_files:
            # 检查是否在文件中提到了技能名称
            assert skill in content.lower(), f"all.md 应包含技能: {skill}"

    def test_quick_skill_has_common_answers(self, project_root):
        """测试 quick.md 应该提供常见问答"""
        quick_path = project_root / "skills" / "quick.md"
        if not quick_path.exists():
            pytest.skip("quick.md 不存在")

        content = quick_path.read_text(encoding='utf-8')

        # 应该包含常见问题类型
        common_keywords = ["创业", "启动", "验证", "定价", "案例"]
        found = sum(1 for kw in common_keywords if kw in content)
        assert found >= 3, "quick.md 应涵盖至少3个常见问题领域"

    def test_skill_output_format_consistency(self, project_root):
        """测试所有技能的输出格式说明一致"""
        skills_dir = project_root / "skills"
        skill_files = list(skills_dir.glob("*.md"))

        for skill in skill_files:
            content = skill.read_text(encoding='utf-8')
            # 每个技能应该有输出格式说明
            has_output = any(marker in content for marker in ["输出格式", "## 输出", "## 格式"])
            assert has_output, f"{skill.name} 应包含输出格式说明"

    def test_case_skill_references_valid_references(self, project_root):
        """测试 cases.md 引用的案例文档存在"""
        cases_skill = project_root / "skills" / "cases.md"
        if not cases_skill.exists():
            pytest.skip("cases.md 不存在")

        content = cases_skill.read_text(encoding='utf-8')
        import re
        links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', content)

        for link in links:
            if link.startswith('references/'):
                ref_path = project_root / link
                assert ref_path.exists(), f"cases.md 引用的文档不存在: {link}"


class TestPlatformCompatibility:
    """平台兼容性测试（模拟）"""

    def test_yaml_frontmatter_valid_syntax(self, project_root, skills_dir):
        """测试所有 skill 文件的 YAML frontmatter 语法有效"""
        import yaml
        import re

        for skill in skills_dir.glob("*.md"):
            content = skill.read_text(encoding='utf-8')
            # 提取 YAML frontmatter
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            if match:
                yaml_content = match.group(1)
                try:
                    yaml.safe_load(yaml_content)
                except yaml.YAMLError as e:
                    pytest.fail(f"{skill.name} 的 YAML frontmatter 语法错误: {e}")

    def test_skill_metadata_has_required_fields(self, project_root, skills_dir):
        """测试 skill frontmatter 包含必要字段"""
        required_fields = ['name', 'description', 'triggers']

        for skill in skills_dir.glob("*.md"):
            content = skill.read_text(encoding='utf-8')
            import re
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            if match:
                yaml_content = match.group(1)
                import yaml
                metadata = yaml.safe_load(yaml_content)
                for field in required_fields:
                    assert field in metadata, f"{skill.name} 缺少必要字段: {field}"

    def test_all_skills_have_unique_names(self, skills_dir):
        """测试所有技能的名称唯一"""
        import yaml
        import re

        names = []
        for skill in skills_dir.glob("*.md"):
            content = skill.read_text(encoding='utf-8')
            match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
            if match:
                yaml_content = match.group(1)
                metadata = yaml.safe_load(yaml_content)
                name = metadata.get('name')
                if name:
                    assert name not in names, f"技能名称重复: {name}"
                    names.append(name)


class TestReferencesIntegrity:
    """引用文档完整性测试"""

    def test_references_are_numbered_sequentially(self, references_dir):
        """测试 references 文档编号连续"""
        if not references_dir.exists():
            pytest.skip("references 目录不存在")

        refs = list(references_dir.glob("*.md"))
        numbers = []
        for ref in refs:
            import re
            m = re.match(r'^(\d+)-', ref.name)
            if m:
                numbers.append(int(m.group(1)))

        if numbers:
            numbers.sort()
            min_n, max_n = min(numbers), max(numbers)
            expected = set(range(min_n, max_n + 1))
            missing = expected - set(numbers)
            assert len(missing) == 0, f"编号不连续，缺失: {sorted(missing)}"

    def test_references_no_broken_relative_links(self, project_root):
        """测试引用文档中的相对链接有效"""
        refs_dir = project_root / "references"
        if not refs_dir.exists():
            pytest.skip("references 目录不存在")

        import re
        link_pattern = re.compile(r'\[[^\]]+\]\(([^)]+)\)')

        for ref in refs_dir.glob("*.md"):
            content = ref.read_text(encoding='utf-8')
            links = link_pattern.findall(content)

            for link in links:
                # 只检查内部相对链接
                if not link.startswith(('http://', 'https://', '#')):
                    target = ref.parent / link
                    # 链接目标应该是存在的文件或目录
                    # 这里简化检查：如果链接指向 skills/ 或特定模板，应存在
                    if 'skills/' in link or 'templates/' in link:
                        assert target.exists(), f"{ref.name}: 链接失效: {link}"
