#!/usr/bin/env python3
"""
为每个 skill 文件添加示例输出部分。
"""

from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent / "skills"

EXAMPLES = {
    "start": r"""## 示例输出

**用户**：我想创业，但不知道从哪里开始。

**OPC助手**：
📌 我需要了解你的基本情况，请回答以下三个问题（回复选项即可）：

**问题1：你目前的状态是？**  
A. 有稳定工作，想找副业  
B. 已经在做副业，想规模化  
C. 全部时间创业  

**问题2：你擅长什么？**  
A. 技术开发  
B. 内容创作  
C. 行业专业知识  
D. 产品设计  
E. 销售运营  

**问题3：你倾向的创业方向？**  
A. AI工具/软件产品  
B. 内容创业/知识付费  
C. 咨询服务/专业服务  
D. 电商/实物产品  
E. 还不确定  

请按格式回复：`1A 2B 3A`
""",
    "validate": r"""## 示例输出

**用户**：我想做一个AI工具帮助写小红书文案，有没有市场？

**OPC助手**：
🔍 想法：AI驱动的文案生成工具

📋 24小时验证计划：
1. **问题定义**：明确目标用户（小红书博主）的核心痛点（时间不够、创意枯竭）
2. **原型制作**（8小时）：用 Cursor/v0 搭建一个可输入关键词生成文案的网页原型
3. **获取反馈**（12小时）：
   - 在相关社群发布原型链接
   - 访谈至少5位目标用户
   - 收集邮箱或预约人数
4. **决策**：转化率 > 10% 则继续开发；否则重新定位或放弃

💡 参考案例：French Brain（Sina Khalife）在3天内获得200个订阅

👉 现在开始？输入 `/opc-launch` 进入72小时启动流程
""",
    "mvp": r"""## 示例输出

**用户**：如何构建一个最小可行产品（MVP）？

**OPC助手**：
🚀 MVP 三步法：

1. **确定核心功能**（1天）
   - 列出假设的功能，只保留1-2个核心
2. **快速实现**（2-3天）
   - 使用 Cursor + v0 开发，部署到 Vercel
3. **测试与迭代**（1周）
   - 找10位用户试用，每周改进

⚠️ MVP目标是验证假设，不是完美产品。
参考：`references/07-mvp-validation.md`
""",
    "canvas": r"""## 示例输出

**用户**：请帮我填写一人企业画布。
**OPC助手**:
请依次回答8个问题：
1. 细分客户：目标用户？
2. 价值主张：解决什么痛点？
3. 渠道通路：如何触达？
4. 竞争策略：如何差异化？
5. 原有方案与痛点：现有不足？
6. 解决方案：你的具体方案？
7. 关键业务：需要做哪些？
8. 成本收入资产：预算与预期？
请回复全部答案。
""",
    "pricing": r"""## 示例输出

**用户**：我的SaaS如何定价？
**OPC助手**:
💰 定价三要素：
1. 成本导向：覆盖服务器、API等成本。
2. 价值导向：客户价值应远高于价格。
3. 心理定价：使用$9/$19/$29。
推荐层次：免费版、基础($19)、专业($49)、企业($199)。
参考：ConvertKit定价页。
使用 `tools/income-tracker.md` 跟踪收入。
""",
    "review": r"""## 示例输出

**用户**：请review我的商业计划。
**OPC助手**:
我将从以下维度审阅：
- 问题-解决方案匹配
- 市场规模与定位
- 可行性（72小时MVP）
- 收入模型（LTV>CAC）
请提供：
- 一句话价值主张
- 目标用户画像
- 核心功能列表
- 预期收入模型
""",
    "launch": r"""## 示例输出

**用户**：我准备好发布了，步骤？
**OPC助手**:
🚀 72小时计划：
Day1: 核心功能开发，Vercel部署，支付沙箱测试。
Day2: 官网首页，分析埋点，邀请测试，准备文案。
Day3: Product Hunt发布，社群宣传，监控指标。
目标：首日10注册，首周50活跃。
参考案例：`references/13-master-cases.md` 中 Loom。
""",
    "diagnosis": r"""## 示例输出

**用户**：用户留存下降，怎么办？
**OPC助手**:
🔍 请先回答：
1. 数据指标：DAU/MAU、次日/7日/30日留存？
2. 用户反馈：负面反馈集中在哪？
3. 产品变动：最近30天有重大改动？
4. 竞品动态：是否有新产品分流？
常见原因：激活时刻不明确、引导不足、功能过多、通知策略不当。
建议使用 `tools/income-tracker.md` 监测。
""",
    "tools": r"""## 示例输出

**用户**：推荐创业工具栈。
**OPC助手**:
🧰 2025年推荐：
| 类别 | 工具 | 用途 | 费用 |
|------|------|------|------|
| 开发 | Cursor, v0 | AI辅助全栈 | 免费-$30 |
| 前端 | React, Vue | UI框架 | 免费 |
| 后端 | Supabase, PocketBase | BaaS | 免费 |
| 部署 | Vercel, Netlify | 自动部署 | 免费起步 |
| 支付 | Stripe, Ping++ | 收款 | 2.9%+$0.3 |
| 分析 | PostHog, Plausible | 开源分析 | 免费 |
| 文档 | Obsidian, Notion | 文档 | 免费 |
更多见 `tools/opc-steps.md`
""",
    "cases": r"""## 示例输出

**用户**：给我3个收入$5k-$10k的案例。
**OPC助手**:
根据案例库：
- Remote OK (@levelsio): $5k-$8k, Ruby on Rails
- ConvertKit (@nathanbarry): $10k-$15k, PHP
完整案例见 `references/13-master-cases.md`，版权归原作者。
""",
    "fetch": r"""## 示例输出

**用户**：/opc-fetch https://example.com/pricing
**OPC助手**:
🔗 正在抓取...
✅ 成功！标题：Example Pricing
摘要：
- Basic: $19/月
- Pro: $49/月
- Enterprise: custom
原始内容保存至 `fetched/example.com-pricing.html`
""",
    "all": r"""## 示例输出

**用户**：列出所有命令。
**OPC助手**:
/opc-start - 启动诊断
/opc-validate - 验证想法
/opc-canvas - 填写画布
/opc-launch - 发布计划
/opc-tools - 工具推荐
/opc-cases - 案例库
/opc-pricing - 定价策略
/opc-diagnosis - 问题诊断
/opc-iterate - 迭代建议
/opc-fetch - 抓取网页
/opc-all - 本列表
""",
    "code": r"""## 示例输出

**用户**：提供Stripe支付Python示例。
**OPC助手**:
```python
import stripe
stripe.api_key = "sk_test_..."
customer = stripe.Customer.create(email="user@example.com")
subscription = stripe.Subscription.create(customer=customer.id, items=[{"price": "price_..."}])
```
替换sk_test_...为你的测试Key，参考Stripe文档。
""",
    "quick": r"""## 示例输出

**用户**：?
**OPC助手**:
⚡ 快速命令:
验证 -> /opc-validate
启动 -> /opc-launch
案例 -> /opc-cases
工具 -> /opc-tools
定价 -> /opc-pricing
诊断 -> /opc-diagnosis
画布 -> /opc-canvas
帮助 -> /opc-start
""",
    "iterate": r"""## 示例输出

**用户**：上线后如何迭代？
**OPC助手**:
🔄 迭代循环：
1. 收集反馈（访谈、评论、数据）
2. 优先级排序（ICE模型）
3. 快速实验（2-3天小功能）
4. 度量效果（留存、收入）
5. 规模化成功实验
参考：Buffer每周更新两次。
工具：PostHog, Crisp, Linear
""",
    "generate": r"""## 示例输出

**用户**：生成AI写作工具的产品介绍。
**OPC助手**:
📝 产品介绍（示例）：
## 让AI成为你的专职文案写手
**痛点**: 每天2小时写小红书文案？灵感枯竭？
**解决方案**: XXX基于GPT-4的智能文案生成工具，输入关键词，30秒生成10条高质量文案。
**核心功能**: ✅批量生成 ✅多风格切换 ✅小红书排版 ✅一键发布
**定价**: 免费版5条/天，专业版$19/月 (无限)
👉 立即试用：https://xxx.com
需要调整请告诉我。
"""
}

def main():
    added = []
    for md_file in SKILLS_DIR.glob("*.md"):
        stem = md_file.stem
        if stem in EXAMPLES:
            content = md_file.read_text(encoding="utf-8")
            if "## 示例输出" in content or "## 示例对话" in content:
                continue
            example_section = "\n\n" + EXAMPLES[stem] + "\n"
            new_content = content.rstrip() + example_section
            md_file.write_text(new_content, encoding="utf-8")
            added.append(md_file.name)
    if added:
        print("Added examples to:", ", ".join(added))
    else:
        print("No changes made.")

if __name__ == "__main__":
    main()