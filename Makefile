# OPC Startup Makefile
.PHONY: help validate test clean package release collect install-deps docs docs-serve collect-policies validate-policies

.DEFAULT_GOAL := help

help: ## 显示帮助
	@echo "OPC Startup - 可用命令:"
	@grep -E '^[a-z_]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

validate: ## 运行项目验证
	@python scripts/validate.py

install-deps: ## 安装开发依赖
	@python -m pip install -r requirements.txt

test: validate pytest ## 运行所有测试

clean: ## 清理临时文件
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 清理完成"

package: clean ## 创建发布包
	@mkdir -p dist
	@git archive --format=zip --output=dist/OPCStartup-main.zip HEAD
	@echo "✅ 包已创建: dist/OPCStartup-main.zip"

release: test package ## 准备发布
	@echo "🚀 发布准备完成"
	@echo "请确保 CHANGELOG.md 已更新，然后打 tag 并推送"

collect: ## 收集政策数据
	@echo "开始收集政策数据..."
	@python scripts/collect_policies.py

docs: ## 生成文档
	@mkdocs build

docs-serve: ## 启动文档服务器
	@mkdocs serve

collect-policies: ## 收集政策 (别名)
	@$(MAKE) collect

validate-policies: ## 验证政策数据
	@python scripts/validate_policies.py
