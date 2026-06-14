---
name: llm-wiki
description: >-
  基于 Karpathy LLM Wiki 模式的个人知识库构建与维护系统。
  支持 Ingest（文档入库编译）、Query 沉淀（对话知识存回）、Lint 巡检（健康检查）三大核心工作流，
  多源适配（飞书、微信、网页、PDF、本地文件）。
  当用户需要构建知识库、入库文档、沉淀知识、巡检 Wiki 健康状态时使用。
version: 1.0.0
---

# LLM Wiki — 个人知识库构建系统

> 基于 Andrej Karpathy 的 LLM Wiki 模式，让 AI 助手帮你构建和维护一个持续生长的结构化知识库。
> 核心思想：Source（不可变原始文档）→ Wiki（编译后的结构化知识）→ 知识网络（交叉引用）

---

## 一、触发条件

当以下任一情况出现时，激活本 Skill：

| 触发场景 | 关键词示例 |
|----------|-----------|
| 用户想构建个人/团队知识库 | "建知识库"、"LLM Wiki"、"知识管理" |
| 用户提供文档要求入库 | "入库"、"ingest"、"加到知识库"、"存一下这个文档" |
| 用户要求查询知识库内容 | "知识库里有没有…"、"查一下…"、"之前那个文档…" |
| 对话产生了有价值的综合分析 | 用户说"沉淀一下"、"这个值得存" |
| 用户要求巡检知识库 | "lint"、"巡检"、"知识库健康检查" |
| 首次安装，需要初始化知识库 | "初始化知识库"、"setup wiki" |

---

## 二、知识库目录结构（标准骨架）

```
{知识库根目录}/
├── SCHEMA.md          # Wiki 维护规范（从模板生成，可定制）
├── INDEX.md           # 全仓库索引（唯一入口，随知识库增长自动更新）
├── log.md             # 操作时间线（每次 Ingest/Query/Lint 都追加记录）
│
├── {领域A}/           # 按主题划分的知识领域（用户自定义）
│   ├── page-a.md      # Wiki 页面（编译后的结构化知识）
│   ├── page-a-source.md  # Source 文件（不可变原始文档快照）
│   └── page-a-images/    # 关联图片/资产
│
├── {领域B}/
│   └── ...
│
└── queries/           # Query 沉淀（对话中产生的综合分析）
    └── analysis-xxx.md
```

**铁律**：
- Source 文件一旦创建，**永不修改**（不可变原则）
- Wiki 页面可以反复更新、重构、合并
- 每个 Source 对应一个 Wiki 页面（一一映射）
- 图片与 source/wiki 同目录存放（就近原则）

---

## 三、三大核心工作流

### 3.1 Ingest（文档入库）— 外部知识 → Wiki

> 完整 SOP 见 `references/INGEST-SOP-template.md`

**九步流程（每步必做，缺一不可）**：

```
Step 0  去重检查        先查后抓，避免重复入库
Step 1  抓取源文档      根据来源类型选择适配器（见第四节）
Step 2  保存 Source     不可变原始快照，命名 {name}-source.md
Step 3  编译 Wiki       提炼结构化知识，命名 {name}.md
Step 4  图片本地化      下载图片/画板，存放到同目录 *-images/
Step 5  更新索引        INDEX.md 新增条目 + 更新统计摘要
Step 6  完整性自检      source 文件 ≥ 2KB，有实际正文（非大纲）
Step 7  Query 沉淀      如入库过程中产生了有价值的讨论，存为 query 页面
Step 8  Git 提交        commit + push（如启用了版本管理）
```

**自检清单（入库完成后逐项确认）**：
- [ ] 去重检查已执行？
- [ ] Source 已保存且 ≥ 2KB？
- [ ] Wiki 已编译？
- [ ] 图片已本地化？
- [ ] INDEX.md 已更新？
- [ ] log.md 已追加记录？
- [ ] 交叉引用已添加？
- [ ] Git 已提交？

---

### 3.2 Query 沉淀 — 内部思考 → Wiki

> Karpathy: *"Good answers can be filed back into the wiki as new pages. Your explorations compound in the knowledge base just like ingested sources."*

**触发条件（满足任一）**：
- 回答了一个有价值的综合分析（对比、总结、趋势、联动关系）
- 用户说"存一下"或"沉淀一下"
- 回答涉及多个 Wiki 页面的串联，形成新视角

**流程**：
1. 将回答整理为结构化 Markdown
2. 保存到 `queries/` 或对应领域目录
3. 添加 frontmatter 和交叉引用
4. 更新 INDEX.md + log.md
5. Git 提交

**与 Ingest 的区别**：

| | Ingest | Query 沉淀 |
|---|---|---|
| 来源 | 外部文档 | 对话中的综合回答 |
| 触发 | 用户提供新文档 | 有价值的问答产出 |
| 知识性质 | 编译他人知识 | 积累自己的思考 |
| 价值 | 建立知识基础 | 产生知识复利 |

**铁律**：有价值的对话结束后，**主动询问用户**是否需要 Query 沉淀，不要等用户提醒。

---

### 3.3 Lint 巡检 — Wiki 健康检查

> 完整清单见 `references/LINT-checklist.md`

建议频率：**每 1-2 周**，或每次大规模更新后执行。

| # | 检查项 | 严重度 |
|---|--------|--------|
| 1 | Source 未编译（有 -source.md 但无对应 .md） | 🔴 必修 |
| 2 | 失效交叉引用链接 | 🔴 必修 |
| 3 | 孤立页面（未被任何其他页面引用） | 🟡 建议修 |
| 4 | frontmatter 不完整 | 🟡 建议修 |
| 5 | 内容矛盾（不同页面对同一事实描述不一致） | 🟡 人工确认 |
| 6 | 过时声明（待验证/TODO/计划等标记） | 🟡 人工确认 |
| 7 | 命名不规范（非 kebab-case） | 🟢 提示 |
| 8 | INDEX.md 与 Wiki 页面不同步 | 🟡 建议修 |
| 9 | log.md 遗漏近期操作 | 🟢 提示 |

**执行后产出**：
- Lint 报告追加到 log.md
- 🔴 级问题直接修复
- 🟡 级问题汇总后请用户确认

---

## 四、多源适配器

> 详细操作手册见 `references/SOURCE-ADAPTERS.md`

### 来源识别优先级

```
用户提供的输入            识别方式                适配器
─────────────────────────────────────────────────────────────
飞书文档 URL              host 含 feishu.cn      → Feishu Adapter
微信公众号 URL            host 含 mp.weixin      → WeChat Adapter
其他网页 URL              http/https 开头        → Web Adapter
本地文件路径              /path/to/file          → Local Adapter
PDF 文件/URL              .pdf 后缀或 PDF MIME  → PDF Adapter
纯文字/粘贴内容           无 URL 无路径          → Direct Adapter
```

### 适配器速查表

| 来源 | 抓取方式 | 图片处理 | 易踩的坑 |
|------|----------|----------|----------|
| **飞书文档** | `feishu_fetch_doc` | `feishu_doc_media` | authcode 过期，需用 user token |
| **微信公众号** | 移动端 UA curl → 备选搜索镜像 | 直接从正文提取 img URL | 滑块验证码、JS 动态渲染 |
| **网页** | `web_fetch` (markdown) | 提取 img 标签下载 | 反爬、登录墙 |
| **本地文件** | `read` 工具 | 同目录引用即可 | 编码问题（GBK→UTF-8） |
| **PDF** | `pdf` 分析工具 | 提取嵌入图片 | 扫描件需 OCR |
| **直接粘贴** | 用户原文 | 无 | 格式丢失 |

### 统一输出格式

无论哪种来源，最终输出统一的 Markdown 格式保存为 `-source.md`：

```markdown
---
source_type: feishu | wechat | web | local | pdf | direct
source_url: 原始链接（如有）
fetched_at: YYYY-MM-DD HH:MM
fetched_by: agent-name
---

# 文档标题

（完整正文内容，禁止只存大纲或摘要）
```

---

## 五、首次安装流程（Setup）

> 详细步骤见 `references/SETUP-GUIDE.md`

### 5.1 向用户确认以下信息

```
1. 知识库根目录位置（默认：workspace/wiki/ 或用户指定路径）
2. 知识库名称（用于 SCHEMA.md 标题）
3. 初始领域分类（至少 1 个，如：产品/技术/投资/学习）
4. 是否启用 Git 版本管理（推荐：是）
5. Git 远程仓库地址（可选，用于备份）
6. 主要文档来源（飞书/微信/网页/本地，可多选）
```

### 5.2 执行初始化

```
1. 创建目录骨架（根目录 + 各领域子目录 + queries/）
2. 从 SCHEMA-template.md 生成定制化 SCHEMA.md（替换变量）
3. 从 INGEST-SOP-template.md 复制为 INGEST-SOP.md
4. 初始化 INDEX.md（空表格 + 统计摘要占位）
5. 初始化 log.md（首条记录：知识库创建）
6. git init + 首次 commit（如启用）
7. 向用户汇报：目录结构 + 文件清单 + 下一步建议
```

### 5.3 验证

- [ ] 目录结构正确？
- [ ] SCHEMA.md 变量已替换？
- [ ] INDEX.md 和 log.md 已创建？
- [ ] Git 首次 commit 成功（如启用）？

---

## 六、铁律（所有操作必须遵守）

| # | 铁律 | 违反后果 |
|---|------|----------|
| 1 | Source 文件创建后**永不修改** | 知识溯源链断裂 |
| 2 | 入库前**必须先做去重检查**（Step 0） | 重复内容污染知识库 |
| 3 | Source 必须包含**完整原文**，禁止只存摘要/大纲 | 信息不可逆丢失 |
| 4 | Source 文件 < 2KB **必须报警**，重新抓取 | 说明只拿到了摘要 |
| 5 | 每次入库后**必须更新 INDEX.md + log.md** | 索引与实际脱节 |
| 6 | 交叉引用使用**标准 Markdown 链接**，不用 [[双链]] | 兼容性问题 |
| 7 | 有价值的对话后**主动询问**是否沉淀 | 知识复利机会丢失 |
| 8 | Lint 报告中的 🔴 级问题**必须立即修复** | 知识库健康度下降 |

---

## 七、参考文件清单

| 文件 | 路径 | 用途 |
|------|------|------|
| Wiki 维护规范模板 | `references/SCHEMA-template.md` | Setup 时生成为定制化 SCHEMA.md |
| Ingest SOP 模板 | `references/INGEST-SOP-template.md` | Setup 时复制为 INGEST-SOP.md |
| Lint 巡检清单 | `references/LINT-checklist.md` | 每次巡检时对照执行 |
| 安装指南 | `references/SETUP-GUIDE.md` | 首次安装 Setup 详细步骤 |
| 多源适配手册 | `references/SOURCE-ADAPTERS.md` | Ingest Step 1 时查阅具体适配器 |

---

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-06-14 | 首版：基于宏也数字分身仓库实践提炼，多源适配 |
