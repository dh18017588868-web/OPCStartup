# 贡献指南

感谢您考虑为 OPC Startup 项目做出贡献！🎉

## 行为准则

我们致力于提供一个开放、友好和尊重的社区环境。请遵守以下准则：

- 使用友好的语言和语气
- 尊重不同观点和经验
- 接受建设性批评
- 专注于项目的最大利益

## 如何贡献

### 报告问题 (Bug)

如果您发现问题或有改进建议，请先[搜索现有issues](https://github.com/dh18017588868-web/OPCStartup/issues)避免重复。

如果确实是一个新问题，请提交issue并包含：

1. **清晰的问题描述** - 发生了什么？
2. **重现步骤** - 如何重现这个问题？
3. **预期行为** - 您期望发生什么？
4. **环境信息** - 使用的平台 (Hermes/CodeBuddy/OpenClaw)、版本等
5. **附加信息** - 截图、日志、错误信息

### 提交 Pull Request (PR)

#### 前置准备

1. **Fork 本仓库**
2. **克隆到本地**
   ```bash
   git clone https://github.com/YOUR_USERNAME/OPCStartup.git
   cd OPCStartup
   ```
3. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/issue-number-description
   ```

#### 开发规范

##### 技能文件 (skills/*.md)

- 遵循标准结构：`角色 → 工作流程 → 输出格式`
- 使用一致的 Markdown 表格格式
- 所有命令应包含 `/opc-` 前缀
- 添加 `💡 其他Skill推荐` 部分关联相关技能
- 结尾可加 `---` 分隔线

##### 引用文档 (references/*.md)

- 文件名使用 `数字-描述性名称.md` 格式
- 编号遵循 SKILL.md 中的引用顺序
- 文档内部应包含适当的 `参考资源` 部分
- 跨文档引用使用 `` `01-opb-canvas.md` `` 格式

##### 一般规范

- 使用 **UTF-8 无 BOM** 编码
- 中英混合时，中文为主，英文补充
- 表格对齐使用标准 Markdown 格式
- 避免过长的单行 (建议 < 100 字符)
- 使用有意义的提交信息

#### 提交前检查

运行验证脚本：
```bash
./scripts/validate.py
# 或
python scripts/validate.py
```

确保所有检查通过。

#### 提交与推送

```bash
git add .
git commit -m "feat: add new skill for pricing guidance"
# 或
git commit -m "fix: correct broken reference in canvas.md"
```

提交信息约定 (推荐)：
- `feat:` 新功能
- `fix:` 修复
- `docs:` 文档改进
- `style:` 格式调整
- `refactor:` 重构
- `chore:` 构建/工具变更

推送：
```bash
git push origin feature/your-feature-name
```

#### 创建 Pull Request

1. 访问 https://github.com/YOUR_USERNAME/OPCStartup 并点击 "Compare & pull request"
2. 填写 PR 模板：
   - **标题**: 简洁明了概括更改
   - **描述**: 详细说明更改内容、原因、关联的 issue
   - **类型**: 新功能 / Bug修复 / 文档改进
3. 如果未完成，选择 "Create draft pull request"
4. 提交 PR 后，CI 会自动运行验证，确保检查通过

#### 代码审查

- 至少一名 Maintainer 会审查您的 PR
- 根据反馈进行修改并推送新提交
- 通过后会被合并到主分支

### 建议的工作流程

1. 先 fork 并 clone
2. 在本地开发并频繁运行验证脚本
3. 保持 PR 小而专注 (一个功能一个 PR)
4. 及时回复审查反馈
5. 合并后可以删除分支

## 开发设置

```bash
# 1. 克隆仓库
git clone https://github.com/dh18017588868-web/OPCStartup.git
cd OPCStartup

# 2. (可选) 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. 运行验证
python scripts/validate.py

# 4. 开始修改
```

## 验证脚本说明

`scripts/validate.py` 检查：
- 必需文件存在性
- LICENSE 文件类型
- 技能文件完整性（16个全）
- SKILL.md 触发器规范
- 引用文档编号连续
- quick.md 结构一致性
- Markdown 表格格式
- 文件编码 (UTF-8)

## 项目结构

```
OPCStartup/
├── README.md              # 项目说明
├── SKILL.md               # Skill 入口定义 (20个触发器)
├── LICENSE                # MIT License
├── skills/                # 16个技能文件
│   ├── start.md
│   ├── validate.md
│   └── ...
├── tools/                 # 实用工具
│   ├── opc-steps.md
│   └── ...
├── references/            # 30+ 参考文档
│   ├── 00-our-methodology.md
│   └── ...
├── scripts/               # 自动化脚本
│   └── validate.py
└── .github/
    └── workflows/
        └── validate.yml   # CI 自动化验证
```

## 更新 CHANGELOG

每次合并 PR 后，请在 [CHANGELOG.md](CHANGELOG.md) 中添加条目：

```markdown
## [Unreleased]

### Added
- 新功能描述

### Fixed
- Bug 修复描述

### Changed
- 改进描述
```

## 提问

如果对贡献流程有任何疑问，请[打开 issue](https://github.com/dh18017588868-web/OPCStartup/issues/new?title=Question%20about%20contributing)。

---

再次感谢您的贡献！👏
