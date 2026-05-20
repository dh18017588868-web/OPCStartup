# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-05-16

### Added
- 添加 MIT LICENSE 文件
- 创建自动化验证脚本 `scripts/validate.py`
- 添加 GitHub Actions 工作流 `.github/workflows/validate.yml`
- 完善贡献指南 `CONTRIBUTING.md`
- 创建本 CHANGELOG.md
- 构建案例数据库 `references/cases/` (10个经典案例)
- 更新 `13-master-cases.md` 包含案例索引
- 创建案例收集脚本 `scripts/collect-cases.py` (支持 Indie Hackers RSS, Twitter API)
- 添加定时工作流 `.github/workflows/weekly-case-collection.yml` (每周一自动运行)
- 添加 GitHub Actions release workflow (`.github/workflows/release.yml`) 实现自动发布
- 更新 validate.yml 添加 `permissions` 块，确保正确的 token scope

### Fixed
- 统一 `skills/quick.md` 结构，添加 "工作流程" 部分
- 修正 README 中的仓库链接引用，将旧的 `huiwang` 统一为 `OPCStartup`

### Changed
- 优化项目结构，确保 16 个技能文件完整
- 案例数据采用 JSONL 格式存储，支持自动化更新

## [Unreleased]
## [Unreleased]

### Added
- Comprehensive test suite (unit, integration, trigger validation)
- GitHub Actions platform compatibility workflow
- MkDocs documentation site with `make docs` target
- Internationalization: English skill files (.en.md) and EN triggers
- Performance optimizations: caching and parallel validation
- CODE OF CONDUCT and contribution guidelines
- Competitor analysis template and annual report generator
- Documentation badges in README

### Changed
- Updated Makefile with docs targets
- Enhanced .gitignore with sensitive file patterns

### Fixed
- Various minor bugs and formatting issues


---

## [1.0.1] - 2025-05-13

### Added
- 添加 YAML 头部配置
- 优化触发器列表
- 完善文档结构

## [1.0.0] - 2025-05-01

### Added
- 初始版本发布
- 16 个核心技能
- 30+ 参考文档

---

*This changelog is maintained manually. Please update it when merging PRs.*

### Added
- Add `/opc-run` one-click startup skill
- Enhance test coverage
- Fix table consistency
- Improve CI
