"""
OPCValidator 单元测试
"""

import pytest
from pathlib import Path


class TestOPCValidator:
    """OPCValidator 测试类"""

    def test_initialization(self, project_root):
        """测试验证器初始化"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        validator = OPCValidator(project_root)
        assert validator.project == Path(project_root).resolve()
        assert validator.errors == 0
        assert validator.warnings == 0
        assert validator.passed == 0

    def test_check_required_files_success(self, project_root, skills_dir):
        """测试必需文件检查 - 成功情况"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        # 确保 README.md 和 SKILL.md 存在
        readme = project_root / "README.md"
        skill = project_root / "SKILL.md"
        assert readme.exists()
        assert skill.exists()

        validator = OPCValidator(project_root)
        validator.check_required_files()
        # 应该通过 2 项检查
        assert validator.passed >= 2
        assert validator.errors == 0

    def test_check_license_success(self, project_root):
        """测试许可证检查 - MIT"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        license_file = project_root / "LICENSE"
        assert license_file.exists()

        validator = OPCValidator(project_root)
        validator.check_license()
        assert "mit" in (license_file.read_text(encoding='utf-8').lower())
        assert validator.errors == 0
        assert validator.passed >= 1

    def test_check_skills_structure(self, project_root, skills_dir):
        """测试技能文件完整性"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        validator = OPCValidator(project_root)
        validator.check_skills_structure()

        expected_skills = [
            "start.md", "validate.md", "mvp.md", "canvas.md",
            "pricing.md", "review.md", "launch.md", "diagnosis.md",
            "tools.md", "cases.md", "fetch.md", "all.md",
            "code.md", "quick.md", "iterate.md", "generate.md"
        ]

        existing = [f.name for f in skills_dir.glob("*.md")]

        # 所有期望的技能文件都应该存在
        for skill in expected_skills:
            assert skill in existing, f"缺失技能文件: {skill}"

        # 错误数应该为0（除非有额外文件导致警告）
        assert validator.errors == 0

    def test_check_skill_triggers(self, project_root):
        """测试 SKILL.md 触发器"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        skill_md = project_root / "SKILL.md"
        assert skill_md.exists()

        validator = OPCValidator(project_root)
        initial_errors = validator.errors
        validator.check_skill_triggers()

        # 应该成功解析触发器
        assert validator.passed > 0
        # 不应该有重复触发器的错误
        assert validator.errors == initial_errors

    def test_check_references(self, project_root):
        """测试引用文档"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        refs_dir = project_root / "references"
        if not refs_dir.exists():
            pytest.skip("references 目录不存在，跳过测试")

        validator = OPCValidator(project_root)
        validator.check_references()

        refs = list(refs_dir.glob("*.md"))
        assert len(refs) > 0, "应该有引用文档"
        assert validator.passed > 0

    def test_check_quick_md_structure(self, project_root):
        """测试 quick.md 结构"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        quick_md = project_root / "skills" / "quick.md"
        if not quick_md.exists():
            pytest.skip("quick.md 不存在，跳过测试")

        validator = OPCValidator(project_root)
        validator.check_quick_md_structure()

        content = quick_md.read_text(encoding='utf-8')
        required_sections = ["## 角色", "## 工作流程", "## 输出格式"]
        for section in required_sections:
            assert section in content, f"quick.md 缺少: {section}"

        assert validator.errors == 0

    def test_check_tables(self, project_root):
        """测试 Markdown 表格格式"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        validator = OPCValidator(project_root)
        validator.check_tables()

        # 应该检查了所有 md 文件
        assert validator.passed > 0 or validator.warnings > 0
        # 表格格式一致性检查不应该有错误，最多警告
        assert validator.errors == 0

    def test_check_encoding(self, project_root):
        """测试文件编码"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        validator = OPCValidator(project_root)
        validator.check_encoding()

        # 所有 UTF-8 文件应该通过检查
        assert validator.passed > 0
        assert validator.errors == 0

    def test_run_all(self, project_root):
        """测试运行所有验证"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        validator = OPCValidator(project_root)
        exit_code = validator.run_all()
        # run_all 返回错误数，应该为0
        assert exit_code == 0, f"验证失败，错误数: {exit_code}"


class TestValidatorEdgeCases:
    """边界情况测试"""

    def test_missing_required_files(self, tmp_path, project_root):
        """测试缺失必需文件"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        # 创建一个空的项目目录
        empty_project = tmp_path / "empty"
        empty_project.mkdir()

        validator = OPCValidator(empty_project)
        validator.check_required_files()

        # 应该产生错误（缺少 README 和 SKILL.md）
        assert validator.errors > 0

    def test_invalid_license(self, tmp_path, project_root):
        """测试无效许可证"""
        import sys
        sys.path.insert(0, str(project_root / "scripts"))
        from validate import OPCValidator

        project = tmp_path / "bad_license"
        project.mkdir()
        (project / "LICENSE").write_text("Some random license", encoding='utf-8')
        (project / "README.md").write_text("# Test", encoding='utf-8')
        (project / "SKILL.md").write_text("---\ntriggers: []\n---", encoding='utf-8')

        validator = OPCValidator(project)
        validator.check_license()

        # 应该产生警告或错误（不是 MIT）
        assert validator.warnings > 0 or validator.errors > 0
