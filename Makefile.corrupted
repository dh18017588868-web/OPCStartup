.PHONY: help validate test clean package release collect install-deps docs docs-serve collect-policies validate-policies

.DEFAULT_GOAL := help
     4|
     5|help: ## 显示帮助
     6|	@echo "OPC Startup - 可用命令:"
     7|	@grep -E '^[a-z_]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
     8|
     9|validate: ## 运行项目验证
    10|	@python scripts/validate.py
    11|
    12|install-deps: ## 安装开发依赖
    13|	@python -m pip install -r requirements.txt
    14|test: validate pytest ## 运行所有测试
    15|
    16|clean: ## 清理临时文件
    17|	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    18|	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
    19|	@echo "✅ 清理完成"
    20|
    21|package: clean ## 创建发布包
    22|	@mkdir -p dist
    23|	@git archive --format=zip --output=dist/OPCStartup-main.zip HEAD
    24|	@echo "✅ 包已创建: dist/OPCStartup-main.zip"
    25|
    26|release: test package ## 准备发布
    27|	@echo "🚀 发布准备完成"
    28|	@echo "请确保 CHANGELOG.md 已更新，然后打 tag 并推送"
    29|
collect: ## 手动运行案例收集
	@echo "📥 运行案例收集脚本..."
	@python scripts/collect-cases.py

collect-policies: ## 手动运行政策收集
	@echo "📋 运行政策收集脚本..."
	@python scripts/collect-policies.py

validate-policies: ## 验证政策数据
	@echo "🔍 验证政策数据..."
	@python scripts/validate-policies.py

docs: ## 构建 MkDocs 文档站点
	@echo "📚 构建 MkDocs 文档站点..."
	mkdocs build --strict
	@echo "✅ 文档已构建到 site/ 目录"

docs-serve: ## 在本地预览 MkDocs 文档
	@echo "🌐 启动 MkDocs 开发服务器..."
	mkdocs serve

