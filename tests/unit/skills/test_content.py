"""
技能内容完整性测试
"""

import pytest
from pathlib import Path


class TestSkillsContent:
    """技能文件内容测试"""

    REQUIRED_SKILLS = [
        "start.md", "validate.md", "mvp.md", "canvas.md",
        "pricing.md", "review.md", "launch.md", "diagnosis.md",
        "tools.md", "cases.md", "fetch.md", "all.md",
        "code.md", "quick.md", "iterate.md", "generate.md"
    ]

    @pytest.fixture
    def skills_dir(self, project_root):
        return project_root / "skills"

    def test_all_skill_files_exist(self, skills_dir):
        """测试所有必需技能文件存在"""
        existing = [f.name for f in skills_dir.glob("*.md")]
        for skill in self.REQUIRED_SKILLS:
            assert skill in existing, f"缺失技能文件: {skill}"

    def test_skill_files_not_empty(self, skills_dir):
        """测试技能文件非空"""
        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            assert path.exists(), f"技能文件不存在: {skill}"
            content = path.read_text(encoding='utf-8')
            assert len(content.strip()) > 0, f"技能文件为空: {skill}"

    def test_skill_has_frontmatter(self, skills_dir):
        """测试 skill 文件有 frontmatter 分隔符"""
        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            content = path.read_text(encoding='utf-8')
            # 检查是否有 --- 分隔符（YAML frontmatter）
            assert '---' in content[:100], f"{skill} 应包含 YAML frontmatter 分隔符"

    def test_skill_has_description(self, skills_dir):
        """测试 skill 文件有描述信息"""
        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            content = path.read_text(encoding='utf-8')
            # YAML frontmatter 后应该有描述
            import re
            match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
            if match:
                frontmatter = match.group(1)
                assert 'description:' in frontmatter, f"{skill} frontmatter 中应有 description"

    def test_quick_skill_structure(self, skills_dir):
        """测试 quick.md 的结构完整性"""
        quick_path = skills_dir / "quick.md"
        if not quick_path.exists():
            pytest.skip("quick.md 不存在")

        content = quick_path.read_text(encoding='utf-8')
        required_sections = ["## 角色", "## 工作流程", "## 输出格式"]
        for section in required_sections:
            assert section in content, f"quick.md 缺少: {section}"

    def test_skills_have_examples(self, skills_dir):
        """测试 skill 文件包含示例"""
        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            content = path.read_text(encoding='utf-8')
            # 至少应该有"示例"或"例子"或"调用方式"等部分
            has_example = any(keyword in content for keyword in ["示例", "例子", "调用方式", "用法"])
            assert has_example, f"{skill} 应包含示例或用法说明"

    def test_no_broken_links_in_skills(self, skills_dir, project_root):
        """测试技能文件中的内部链接是否有效"""
        import re
        link_pattern = re.compile(r'\[[^\]]+\]\(([^)]+)\)')

        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            content = path.read_text(encoding='utf-8')
            links = link_pattern.findall(content)

            for link in links:
                # 只检查 skills/ 和 references/ 目录下的文件
                if link.startswith('skills/') or link.startswith('references/'):
                    target_path = project_root / link
                    assert target_path.exists(), f"{skill}: 链接失效: {link}"

    def test_skill_triggers_in_skill_content(self, skills_dir, project_root):
        """测试 skill 文件中提到的触发器与 SKILL.md 一致"""
        skill_md = project_root / "SKILL.md"
        if not skill_md.exists():
            pytest.skip("SKILL.md 不存在")

        import re
        content = skill_md.read_text(encoding='utf-8')
        trigger_match = re.search(r'triggers:(.*?)(?=\n\w:||---|$)', content, re.DOTALL)
        triggers_block = trigger_match.group(1)
        triggers = [t.lower() for t in re.findall(r'-\s*"([^"]+)"', triggers_block)]

        # 检查每个 skill 文件是否在其内容中提到对应的触发器
        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            skill_content = path.read_text(encoding='utf-8')
            skill_name_no_ext = skill.replace('.md', '')
            # 应该在 skill 内容中提及对应的命令
            has_mention = skill_name_no_ext in skill_content.lower()
            assert has_mention, f"{skill} 应在内容中提及技能名称 {skill_name_no_ext}"
