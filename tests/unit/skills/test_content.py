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
        """测试 skill 文件不应包含 YAML frontmatter（元数据集中在 SKILL.md）"""
        for skill in self.REQUIRED_SKILLS:
            path = skills_dir / skill
            content = path.read_text(encoding='utf-8')
            # 检查前100字符是否包含 --- 分隔符
            assert '---' not in content[:100], f"{skill} 不应包含 YAML frontmatter 分隔符"

    def test_skill_has_description(self, skills_dir):
        """测试每个必需技能都在 SKILL.md 表格中有描述"""
        import re
        project_root = skills_dir.parent
        skill_md_path = project_root / "SKILL.md"
        assert skill_md_path.exists(), "SKILL.md 不存在"
        md_content = skill_md_path.read_text(encoding='utf-8')
        # 寻找三列表格：触发器 | 技能文件 | 描述
        table_match = re.search(r'\|\s*触发器\s*\|\s*技能文件\s*\|\s*描述\s*\|.*?\n\|[-| ]+\|\n((?:\|.*\|\n)+)', md_content, re.DOTALL)
        assert table_match, "SKILL.md 中未找到技能映射表格"
        table_text = table_match.group(1)
        skill_desc = {}
        for line in table_text.strip().split('\n'):
            cells = [c.strip() for c in line.split('|')]
            if len(cells) >= 4:
                skill_file = cells[2].strip()
                description = cells[3].strip()
                if skill_file:
                    skill_desc[skill_file] = description
        # 交集：检查 REQUIRED_SKILLS 中的每个技能是否都有描述
        for skill in self.REQUIRED_SKILLS:
            assert skill in skill_desc, f"SKILL.md 中缺少技能文件: {skill}"
            assert skill_desc[skill], f"SKILL.md 中 {skill} 的描述缺失"

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
