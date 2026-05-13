# 案例库设计

> 双轨案例库：基础库（引用）+ 垂直库（自建）

## 一、案例库架构

### 1.1 双轨模式

| 案例库 | 来源 | 数量 | 特点 |
|--------|------|------|------|
| **基础库** | 引用 Fangx-AI/one-person-company-skill | 100+ 条 | 覆盖广，什么行业都有 |
| **垂直库** | 自建，聚焦"一人+AI" | 50+ 条 | 聚焦、深度、可操作 |

### 1.2 垂直库分类

**六大垂直赛道**：

| 赛道 | 示例 | 核心问题 |
|------|------|----------|
| **AI 工具类** | 提示词网站、AI 插件、Agent 产品 | 如何让用户持续使用？ |
| **内容创作类** | 小红书代运营、短视频制作、B站UP主 | 如何从流量到变现？ |
| **知识付费类** | 课程、训练营、社群、咨询 | 如何建立信任和复购？ |
| **SaaS/效率类** | 自动化工具、效率插件、数据产品 | 如何差异化和大厂竞争？ |
| **电商出海类** | Temu、亚马逊、独立站 | 如何选品和供应链？ |
| **服务外包类** | 设计外包、开发外包、运营外包 | 如何标准化和规模化？ |

---

## 二、案例数据结构

### 2.1 基础字段

```yaml
case_id: "case_001"
name: "AI 提示词商店"
category: "ai-tool"
stage: "mvp"  # idea / mvp / growth / mature
target_user: "运营、产品、开发者"
pricing: "¥9.9-99/个"
revenue: "月入 ¥5000-20000"
acquisition: "小红书、知乎、公众号"
key_insight: "用免费内容获客，付费提示词变现"
failure_reason: "内容获客不够持续"
```

### 2.2 扩展字段

```yaml
# 商业模式
business_model: "一次性付费 + 订阅"
m毛利率: "80%+"

# 获客
channels:
  - name: "小红书"
    cost: "内容换流量"
    effect: "好"
  - name: "知乎"
    cost: "内容换流量"
    effect: "一般"

# 交付
delivery:
  form: "数字产品"
  time: "即时"

# 复购
repurchase: "低，主要靠新用户"

# 一人适配性
solo_friendly: "高"
ai_amplify: "高"
```

---

## 三、案例检索逻辑

### 3.1 匹配流程

```
用户输入产品想法
    ↓
提取关键词（产品类型、目标用户、使用场景）
    ↓
在垂直库中匹配（权重 70%）
    ↓
在基础库中匹配（权重 30%）
    ↓
返回 Top 3-5 案例
    ↓
分析每个案例的成败关键
```

### 3.2 匹配规则

| 匹配维度 | 权重 | 说明 |
|----------|------|------|
| 产品类型 | 30% | 同类型产品优先 |
| 目标用户 | 30% | 同用户群优先 |
| 商业模式 | 20% | 同收费模式优先 |
| 阶段 | 20% | 同阶段（idea/mvp/growth）优先 |

---

## 四、垂直库案例示例

### 4.1 AI 工具类

**案例 1：AI 提示词商店**

```yaml
name: "AI 提示词商店"
tagline: "一个提示词交易平台"
target_user: "需要用好 AI 的运营、产品、开发者"
pricing: "单个 ¥9.9-99，会员 ¥99/月"
revenue: "月入 ¥5000-20000"
acquisition: "小红书、知乎免费内容"
key_insight: "高频场景提示词（小红书、PPT、Excel）最好卖"
failure_reason: "内容获客不够持续，用户复购低"
solo_friendly: "高"
```

**案例 2：AI 写作助手**

```yaml
name: "AI 写作助手"
tagline: "针对特定场景的 AI 写作工具"
target_user: "自媒体人、内容创作者"
pricing: "免费版 + ¥49/月"
revenue: "月入 ¥10000-50000"
acquisition: "小红书、抖音"
key_insight: "工具+内容一起做，工具获客，内容变现"
failure_reason: "工具做太好可能变成大厂竞品"
solo_friendly: "中"
```

### 4.2 内容创作类

**案例 3：小红书博主**

```yaml
name: "小红书 AI 教程博主"
tagline: "教普通人用 AI 做内容"
target_user: "想学 AI 的普通人、宝妈、上班族"
pricing: "免费内容 + ¥99 课程 + ¥365 社群"
revenue: "月入 ¥10000-100000"
acquisition: "小红书笔记"
key_insight: "用案例教学，容易出爆款"
failure_reason: "内容产出需要持续，压力大"
solo_friendly: "高"
```

**案例 4：短视频代运营**

```yaml
name: "AI 短视频制作服务"
tagline: "用 AI 工具批量生产短视频"
target_user: "本地商家、小老板"
pricing: "¥2000-5000/月"
revenue: "月入 ¥20000-50000"
acquisition: "小红书、抖音本地号"
key_insight: "聚焦本地生活商家，需求大，预算有限"
failure_reason: "交付重，一个人能服务的客户有限"
solo_friendly: "中"
```

### 4.3 知识付费类

**案例 5：AI 训练营**

```yaml
name: "AI 工具训练营"
tagline: "14 天学会使用 AI 工具"
target_user: "想提升效率的职场人"
pricing: "¥499/人，30人/期"
revenue: "¥15000/期"
acquisition: "公众号、个人微信"
key_insight: "口碑传播重要，需要好评"
failure_reason: "交付重，每期都要投入大量时间"
solo_friendly: "中"
```

**案例 6：付费社群**

```yaml
name: "AI 创业者社群"
tagline: "一人公司创业者交流社群"
target_user: "正在创业或想创业的人"
pricing: "¥365/年"
revenue: "月入 ¥5000-20000"
acquisition: "公众号、知乎"
key_insight: "需要持续提供价值，否则留不住人"
failure_reason: "社群运营需要时间，容易变成客服"
solo_friendly: "中"
```

### 4.4 SaaS/效率类

**案例 7：浏览器插件**

```yaml
name: "AI 效率浏览器插件"
tagline: "浏览器端 AI 增强工具"
target_user: "开发者、设计师、运营"
pricing: "免费版 + ¥19/月"
revenue: "月入 ¥5000-30000"
acquisition: "Product Hunt、少数派"
key_insight: "工具类产品，获客难，但一旦用户形成习惯就很难离开"
failure_reason: "大厂可能做类似功能"
solo_friendly: "高（技术类）"
```

### 4.5 电商出海类

**案例 8：Temu 无货源**

```yaml
name: "Temu 无货源电商"
tagline: "从多多拿货卖到海外"
target_user: "海外 C 端消费者"
pricing: "商品差价"
revenue: "月入 ¥5000-30000"
acquisition: "平台流量"
key_insight: "选品最重要，利润薄，现金流压力大"
failure_reason: "平台规则变化，罚款多"
solo_friendly: "中"
```

### 4.6 服务外包类

**案例 9：AI  Logo 设计**

```yaml
name: "AI Logo 设计服务"
tagline: "用 AI 工具快速生成 Logo"
target_user: "小老板、创业者"
pricing: "¥99-299/个"
revenue: "月入 ¥5000-20000"
acquisition: "小红书、闲鱼"
key_insight: "低价走量，用 AI 工具提高效率"
failure_reason: "客单价低，需要大量订单"
solo_friendly: "高"
```

---

## 五、使用方式

### 5.1 调用案例检索

```
/案例检索
产品想法：[你的产品想法]
目标用户：[目标用户]
使用场景：[使用场景]
```

### 5.2 返回格式

```markdown
## 匹配案例

### 案例 1：[案例名称]
- 定价：¥xxx
- 收入：¥xxx/月
- 获客：xxx
- 关键洞察：xxx
- 可借鉴点：xxx
- 失败教训：xxx

### 案例 2：...
### 案例 3：...
```

---

## 六、数据来源

### 6.1 基础库

引用：[Fangx-AI/one-person-company-skill](https://github.com/Fangx-AI/one-person-company-skill)
- 100+ 条标准化案例
- 30 条 Gold Cases
- 覆盖多种商业模式

### 6.2 垂直库

自建案例来源：
- 公开报道和采访
- 社群内真实案例
- 公开数据推算
- 持续更新迭代