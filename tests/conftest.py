"""Pytest 配置和共享 fixtures"""

import pytest
import os
import sys
from pathlib import Path

# Determine project root
PROJECT_ROOT = Path(os.getenv("PROJECT_ROOT", "/home/ubuntu/hermes/projects/OPCStartup")).resolve()

# Add scripts directory to Python path for direct imports (fix CI import error)
scripts_path = PROJECT_ROOT / "scripts"
if str(scripts_path) not in sys.path:
    sys.path.insert(0, str(scripts_path))


@pytest.fixture
def project_root():
    """项目根目录路径"""
    return PROJECT_ROOT


@pytest.fixture
def skills_dir(project_root):
    """skills 目录路径"""
    return project_root / "skills"


@pytest.fixture
def references_dir(project_root):
    """references 目录路径"""
    return project_root / "references"


@pytest.fixture
def scripts_dir(project_root):
    """scripts 目录路径"""
    return project_root / "scripts"


@pytest.fixture
def temp_project(tmp_path, project_root):
    """创建临时项目副本用于隔离测试"""
    import shutil
    temp_dir = tmp_path / "opc_test"
    shutil.copytree(project_root, temp_dir, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.pyc', 'dist'))
    return temp_dir


@pytest.fixture
def validator_class():
    """导入 OPCValidator 类"""
    from validate import OPCValidator
    return OPCValidator
