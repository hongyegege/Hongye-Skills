# SCHEMA.md — {{知识库名称}} Wiki 维护规范

> 本文档定义知识库的结构、命名、工作流与维护规范。
> 所有 AI 助手在操作本知识库时，必须遵循本规范。
> 创建时间：{{创建日期}}
> 维护者：{{维护者}}
> 生成自：llm-wiki skill v1.0.0

---

## 一、目录结构规范

```
{{知识库根目录}}/
├── SCHEMA.md                    # 本文件 — Wiki 维护规范
├── log.md                       # 时间线日志（所有操作记录）
├── INDEX.md                     # 全仓库索引（唯一索引入口）
├── INGEST-SOP.md                # Ingest 标准作业流程
│
{{#each 领域列表}}
├── {{领域名}}/                  # {{领域描述}}
│   ├── page.md                  # Wiki 页面（编译后）
│   ├── page-source.md           # Source 文件（不可变）
│   └── page-images/             # 关联图片
{{/each}}
│
└── queries/                     # Query 沉淀（综合分析产出）
    └── analysis-xxx.md
```

### 目录职责

| 目录 | 职责 | 说明 |
|------|------|------|
| 根目录 | 系统文件（SCHEMA/log/INDEX/SOP） | 不放知识内容 |
| {领域}/ | 该领域的所有知识页面 + source + 图片 | 按主题就近存放 |
| queries/ | 对话中产生的综合分析 | 知识复利的载体 |

### 图片存放规范

**所有图片一律存放在对应领域目录下，与 source/wiki 同目录。**

| 场景 | 存放路径 | 示例 |
|------|----------|------|
| 少量图片（<5 张） | 与 source/wiki 同目录 | `{领域}/` |
| 多张图片（≥5 张） | `{主题}-images/` 子目录 | `{领域}/gateway-images/` |

**命名规则**：`{序号}-{功能描述}.png`（有意义，不随机）

**禁止**：图片不得放在远离对应文档的位置。

---

## 二、命名规范

### 文件名
- 使用 **kebab-case**（小写 + 短横线分隔）
- 避免空格、中文文件名、特殊字符
- 示例：`gateway.md`、`smart-solution-framework.md`

### Source 文件
- 在 Wiki 页面同名后加 `-source` 后缀
- 示例：`gateway-source.md` → `gateway.md`

### 领域目录
- 使用 kebab-case 命名
- 示例：`product-knowledge/`、`investment-notes/`、`learning/`

---

## 三、Source 文件规范

### 定义
Source 文件是从原始材料（飞书文档、网页文章、PDF、会议记录等）导出的**未经编译的完整原文**。

### 规则

| 规则 | 说明 |
|------|------|
| **不可变** | Source 文件一旦创建，永不修改 |
| **命名** | 必须以 `-source.md` 结尾 |
| **存放** | 放在对应领域的子目录中 |
| **一一对应** | 每个 `-source.md` 应有对应的编译后 `.md` 页面 |
| **完整性** | 必须包含完整原文，禁止只存摘要或大纲 |
| **最小体积** | < 2KB 必须报警，大概率只有摘要没有原文 |

### Source 文件头部模板

```markdown
---
source_type: feishu | wechat | web | local | pdf | direct
source_url: 原始链接（如有）
fetched_at: YYYY-MM-DD HH:MM
fetched_by: agent-name
---

# 文档标题

（完整正文内容）
```

---

## 四、Wiki 页面结构规范

### 标准页面模板

```markdown
---
title: 页面标题
type: knowledge | reference | analysis
category: 所属领域
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - xxx-source.md
tags:
  - 标签1
  - 标签2
related:
  - "../other-dir/page.md"
---

# 页面标题

> 一句话概述（用于索引摘要）

## 正文内容...

---

## 🔗 关联页面
- [页面名称](../path/to/page.md) — 关联说明
```

### frontmatter 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 页面标题 |
| `type` | string | ✅ | `knowledge`（领域知识）/ `reference`（参考资料）/ `analysis`（分析产出） |
| `category` | string | ✅ | 所属领域 |
| `created` | date | ✅ | 创建日期 |
| `updated` | date | ✅ | 最后更新日期 |
| `sources` | array | ✅ | 源文件名列表 |
| `tags` | array | 推荐 | 关键词标签 |
| `related` | array | 推荐 | 关联页面相对路径 |

---

## 五、交叉引用规范

### 语法
使用**标准 Markdown 链接**格式，不使用 `[[双链]]` 语法：

```markdown
[页面显示名称](../relative/path/to/page.md) — 一句话说明
```

### 路径规则

| 关系 | 格式 | 示例 |
|------|------|------|
| 同目录 | `page.md` | `[网关](gateway.md)` |
| 上级目录 | `../page.md` | `[平台](../platform-overview.md)` |
| 兄弟目录 | `../other/page.md` | `[计费](../t-building/billing.md)` |

### 关联页面区块
放在页面最末尾，用 `---` 分割线分隔：

```markdown
---

## 🔗 关联页面
- [页面名](../path/page.md) — 说明
```

---

## 六、工作流规范

### 6.1 Ingest（新文档入库）
详见 `INGEST-SOP.md`。核心九步：去重 → 抓取 → 保存 Source → 编译 Wiki → 图片本地化 → 更新索引 → 完整性自检 → Query 沉淀 → Git 提交。

### 6.2 Query 沉淀（对话知识存回）
有价值的综合回答 → 整理为 Markdown → 保存到 queries/ 或对应领域 → 更新索引和日志。

**触发时机**：
- 回答涉及多个 Wiki 页面的信息串联
- 用户说"存一下"
- Agent 主动判断值得保留

### 6.3 Lint 巡检（定期健康检查）
建议每 1-2 周或大规模更新后执行。详见 `references/LINT-checklist.md`（Skill 安装后存放在 Skill 目录内）。

---

## 七、Git 提交规范

### Commit Message 格式
```
[类型] 简述内容
```

### 类型说明

| 类型 | 用途 | 示例 |
|------|------|------|
| `[ingest]` | 新文档入库 | `[ingest] 新增网关单品知识页面` |
| `[query]` | Query 沉淀 | `[query] 沉淀多平台联动分析` |
| `[lint]` | 巡检修复 | `[lint] 修复 3 处失效链接` |
| `[schema]` | 规范变更 | `[schema] 更新目录结构` |
| `[index]` | 索引更新 | `[index] 同步新增 5 个条目` |
| `[batch]` | 批量操作 | `[batch] 批量入库 12 篇文章` |

### 原则
- 每个操作独立 commit
- Commit message 不包含敏感信息
- 使用通用描述

---

## 八、版本历史

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| {{创建日期}} | v1.0 | 初始版本，由 llm-wiki skill 生成 |

---

*本规范由用户确认生效，后续随知识库演进而持续更新。*
