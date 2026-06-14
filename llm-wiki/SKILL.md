---
name: llm-wiki
description: >-
  基于 Karpathy LLM Wiki 模式的个人知识库构建与维护系统。
  支持 Ingest（文档入库编译）、Query 沉淀（对话知识存回）、Lint 巡检（健康检查）三大核心工作流，
  多源适配（飞书、微信、网页、PDF、本地文件）。
  当用户需要构建知识库、入库文档、沉淀知识、巡检 Wiki 健康状态时使用。
  也适用于用户说"帮我整理这些文档"、"做个知识管理"、"把这篇文章存起来"、
  "build my wiki"、"ingest this article"、"knowledge management"、"note-taking system"、
  "个人笔记系统"、"文档归档"、"资料整理入库"、"第二大脑"、"second brain"、"PKM"、
  "文档管理"、"documentation"、"notion 替代"、"obsidian 知识库"等场景。
  即使用户没有明确说"知识库"，只要涉及将散乱文档结构化为可持续增长的知识体系，都应使用此 Skill。
compatibility:
  tools:
    - read          # 读取本地文件
    - write         # 写入文件
    - exec          # 执行命令（git、curl、文件检查等）
    - web_fetch     # 抓取网页内容
    - web_search    # 搜索网页（微信镜像等场景）
  optional_tools:
    - feishu_fetch_doc   # 飞书文档抓取（需飞书集成）
    - feishu_doc_media   # 飞书图片/画板下载（需飞书集成）
    - pdf                # PDF 分析（可选，pdf 来源场景）
    - browser            # 浏览器自动化（可选，反爬场景兜底）
version: 1.4.0
---

# LLM Wiki — 个人知识库构建系统

> 基于 Andrej Karpathy 的 LLM Wiki 模式，让 AI 助手帮你构建和维护一个持续生长的结构化知识库。
> 核心思想：Source（不可变原始文档）→ Wiki（编译后的结构化知识）→ 知识网络（交叉引用）

---

**快速指引** — 根据用户意图直接跳到对应章节：
- 🆕 首次安装知识库 → [第五节 Setup](#五首次安装流程setup)
- 📥 用户给文档要求入库 → [第三节 3.1 Ingest](#31-ingest文档入库-外部知识--wiki)
- 🔍 用户查询知识库内容 → [第三节 3.4 查询](#34-查询-search--知识库检索)
- 🧠 对话产生了有价值的分析 → [第三节 3.2 Query 沉淀](#32-query-沉淀--内部思考--wiki)
- 🏥 定期巡检 → 执行 `scripts/lint.sh {知识库根目录}`
- ❓ 遇到问题 → 查阅 `references/TROUBLESHOOTING.md`

---

## 一、触发条件

当以下任一情况出现时，激活本 Skill：

| 触发场景 | 中文关键词 | English Keywords |
|----------|-----------|------------------|
| 构建个人/团队知识库 | "建知识库"、"知识管理"、"文档归档"、"资料整理入库"、"第二大脑"、"PKM" | "build my wiki", "knowledge base", "knowledge management", "second brain", "PKM" |
| 文档入库 | "入库"、"加到知识库"、"存一下这个文档"、"把这篇文章存起来" | "ingest this", "add to wiki", "save this doc" |
| 查询知识库 | "知识库里有没有…"、"查一下…"、"之前那个文档…" | "search wiki", "find in knowledge base" |
| Query 沉淀 | "沉淀一下"、"这个值得存"、"总结一下存起来" | "save this analysis", "file this back" |
| 巡检知识库 | "lint"、"巡检"、"知识库健康检查" | "lint", "wiki health check" |
| 初始化知识库 | "初始化知识库"、"搭建知识库" | "setup wiki", "initialize knowledge base" |
| 文档管理替代方案 | "notion 替代"、"文档管理"、"笔记系统" | "notion alternative", "documentation", "note-taking system" |

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

**核心原则**：
- Source 文件一旦创建就不修改，因为它是知识溯源的"证据链"——修改了就无法追溯知识从何而来
- Wiki 页面可以反复更新、重构、合并——它是编译产物，不是原始记录
- 每个 Source 对应一个 Wiki 页面（一一映射），确保每条知识都有据可查
- 图片与 source/wiki 同目录存放（就近原则），方便 LLM 编译时直接引用

---

## 三、核心工作流

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
Step 6  完整性自检      source 文件达到来源类型最小阈值（见第九节阈值表）
Step 7  Query 沉淀      如入库过程中产生了有价值的讨论，存为 query 页面
Step 8  Git 提交        commit + push（如启用了版本管理）
```

**自检清单（入库完成后逐项确认）**：
- [ ] 去重检查已执行？
- [ ] Source 已保存且达到最小阈值？
- [ ] Wiki 已编译？
- [ ] 图片已本地化？
- [ ] INDEX.md 已更新？
- [ ] log.md 已追加记录？
- [ ] 交叉引用已添加？
- [ ] Git 已提交？

#### Ingest Example：一篇微信文章入库的完整过程

```
用户输入：
  "帮我把这篇微信文章存到知识库 https://mp.weixin.qq.com/s/abc123"

Step 0  去重：git grep "网关计费" → 无匹配 → 继续
Step 1  抓取：curl -L -H "User-Agent: ...(iPhone)..." → 获得 8KB 正文
Step 2  保存 Source：

  文件：product/gateway-billing-source.md
  ──────────────────────────────────────────
  ---
  source_type: wechat
  source_url: https://mp.weixin.qq.com/s/abc123
  fetched_at: 2026-06-14 14:00
  fetched_by: agent-secretary
  ---
  # 网关计费方案设计与实现
  （8KB 完整原文...）

Step 3  编译 Wiki：

  文件：product/gateway-billing.md
  ──────────────────────────────────────────
  ---
  title: 网关计费方案
  type: knowledge
  category: product
  created: 2026-06-14
  updated: 2026-06-14
  sources: [gateway-billing-source.md]
  tags: [网关, 计费, 分户计费]
  related: ["../t-building/billing.md", "../hardware/gateway.md"]
  ---
  # 网关计费方案
  > 网关设备如何与楼宇计费系统联动的技术方案。
  ## 核心逻辑
  网关采集电表数据 → 上传至 T-Building → 计费引擎计算...
  ## 🔗 关联页面
  - [T-Building 分户计费](../t-building/billing.md) — 计费数据下游消费方
  - [楼宇网关](../hardware/gateway.md) — 数据采集上游设备

Step 4  图片：提取 2 张架构图 → product/gateway-billing-images/
Step 5  INDEX.md 新增条目 + log.md 追加记录
Step 6  自检：source 8KB > 3KB 阈值 ✅
Step 8  git add + commit "[ingest] 网关计费方案设计" + push
```

---

### 3.2 Query 沉淀 — 内部思考 → Wiki

> Karpathy: *"Good answers can be filed back into the wiki as new pages. Your explorations compound in the knowledge base just like ingested sources."*

**触发条件（满足任一即主动询问用户是否沉淀）**：
- 用户明确说"存一下"、"沉淀一下"、"file this back"
- 回答涉及多个 Wiki 页面的串联，形成新视角

**Agent 自主判断"有价值"的信号（满足 2 条及以上即建议沉淀）**：
- 回答中引用了 3 个及以上不同 Wiki 页面
- 回答包含对比分析、趋势推演、联动关系梳理等结构化输出
- 回答产生了知识库中尚不存在的新概念或新关联
- 用户追问了 2 轮以上，说明话题深度足够
- 回答被用户明确肯定（"说得好"、"这个有用"等）

**不应沉淀的信号**：
- 回答只是复述单个页面的内容（无新增价值）
- 简短的事实查询（"XX 的截止日期是什么"）
- 用户没有表现出持续兴趣

**流程**：
1. 将回答整理为结构化 Markdown
2. 保存到 `queries/` 或对应领域目录
3. 添加 frontmatter 和交叉引用（见下方模板）
4. 更新 INDEX.md + log.md
5. Git 提交

**Query 页面 frontmatter 模板**：
```markdown
---
title: 分析标题
type: analysis
category: 相关领域
created: YYYY-MM-DD
sources: []        # Query 无外部 source，留空即可
tags: [标签]
related: ["../page-a.md", "../page-b.md"]
trigger: "触发这次沉淀的对话场景描述"
---
```

**正文结构**：
```markdown
# 分析标题
> 一句话摘要

## 分析背景
为什么做这次分析，触发的场景是什么。

## 核心发现
结构化的分析内容。

## 关键原则
从分析中提炼的经验教训。

## 🔗 关联页面
- [页面名](../path/page.md) — 关联说明
```

**与 Ingest 的区别**：

| | Ingest | Query 沉淀 |
|---|---|---|
| 来源 | 外部文档 | 对话中的综合回答 |
| 触发 | 用户提供新文档 | 有价值的问答产出 |
| 知识性质 | 编译他人知识 | 积累自己的思考 |
| 价值 | 建立知识基础 | 产生知识复利 |

---

### 3.3 Lint 巡检 — Wiki 健康检查

> 完整清单见 `references/LINT-checklist.md`
> 自动化脚本见 `scripts/lint.sh`

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

### 3.4 页面生命周期管理 — 更新/删除/合并/查询

除了 Ingest（创建）之外，知识库运营还涉及以下操作：

#### 更新 Wiki 页面（Update）

**触发场景**：源文档有新版、信息过时、用户要求更新。

```
流程：
1. 获取新内容（同 Ingest Step 1）
2. 保存为新的 -source.md（版本号追加，如 xxx-v2-source.md）
3. 在已有 Wiki 页面上追加/修改内容，更新 frontmatter 的 updated 和 sources 字段
4. 更新 INDEX.md 更新日期
5. log.md 追加 "[update] 页面名 — 更新原因"
6. Git 提交

注意：旧 source 保留不删（不可变原则），新 source 与旧 source 并存
```

#### 删除 Wiki 页面（Delete）

**触发场景**：信息完全过时且被新页面替代、用户明确要求删除。

```
流程：
1. 向用户确认删除范围（仅删 Wiki？还是 source 一起删？）
2. 检查所有引用该页面的交叉引用链接
3. 更新引用方页面，移除失效链接或替换为新页面
4. 删除 Wiki + source + 图片目录（如用户确认全删）
5. 更新 INDEX.md（移除条目 + 更新统计）
6. log.md 追加 "[delete] 页面名 — 删除原因"
7. Git 提交（注意 pre-push hook 可能拦截大量删除）
```

#### 合并页面（Merge）

**触发场景**：两个页面内容高度重叠、粒度太细需要合并。

```
流程：
1. 确定保留页面（A）和被合并页面（B）
2. 将 B 的关键内容追加到 A，更新 A 的 frontmatter（sources 加入 B 的 source）
3. 在 B 的位置放置重定向说明："> 本页面已合并至 [A](../path/to/A.md)"
4. 更新所有引用 B 的交叉引用链接，改为指向 A
5. 更新 INDEX.md（移除 B 条目，更新 A 摘要）
6. log.md 追加 "[merge] B → A"
7. Git 提交
```

#### 查询（Search）— 知识库检索

**触发场景**：用户说"查一下…"、"知识库里有没有…"

```
知识库定位策略（先找到知识库在哪）：
1. 查找 SCHEMA.md 文件：find workspace/ -name "SCHEMA.md" -path "*/wiki/*" → 其所在目录即知识库根
2. 检查默认路径：workspace/wiki/
3. 如找不到，询问用户知识库位置，记住后写入 Agent 工作文件（如 TOOLS.md）以便后续复用

搜索策略（按优先级）：
1. INDEX.md 全文搜索：grep "关键词" INDEX.md → 快速定位相关页面
2. 页面正文搜索：grep -r "关键词" {知识库根目录}/ --include="*.md" -l → 列出匹配文件
3. 标签搜索：grep -r "tags:.*关键词" {知识库根目录}/ --include="*.md" → 按标签匹配
4. 读取匹配页面，提取关键信息，组织为结构化回答

搜索结果处理策略：
- 1-3 个匹配 → 全部读取，综合回答，每个结论标注来源页面路径
- 4-10 个匹配 → 按相关度排序，读取前 3 个详细回答，其余列标题供用户选择深入
- >10 个匹配 → 先给用户摘要列表（标题 + 一句话概述），让用户缩小范围
- 0 个匹配 → 明确告知"知识库中暂无相关内容"，建议用户提供文档入库
- 内容矛盾 → 标注不同页面的不同说法及更新日期，建议用户确认哪个是最新的

注意：查询结果应标注来源页面路径，方便用户追溯原文
```

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

**超大文档**（>5 万字）：分段抓取，每段独立保存为一个 source，对应多个 Wiki 页面。详见 INGEST-SOP 第三节「特殊情况处理」表。

### 工具不可用时的降级策略

当 optional_tools 中的工具在当前环境不可用时，按以下策略降级，确保 Ingest 流程不会卡死：

| 不可用工具 | 降级方案 |
|-----------|----------|
| `feishu_fetch_doc` | 请用户手动复制飞书文档正文，粘贴给 Agent，走 **Direct Adapter** |
| `feishu_doc_media` | 跳过图片本地化（Step 4），在 source 中保留飞书 CDN 链接（注意 authcode 会过期） |
| `pdf` | 请用户用其他工具将 PDF 转为文本（如在线转换），或提示安装 pdf 工具后重试 |
| `browser` | 微信文章仅使用 Level 1（curl 移动端 UA）和 Level 2（搜索镜像），不使用 Level 3（browser 直连） |

**铁律**：降级时告知用户当前降级方案和限制，让用户决定是否接受降级结果。

### 统一输出格式

无论哪种来源，最终输出统一的 Markdown 格式保存为 `-source.md`：

```markdown
---
source_type: feishu | wechat | web | local | pdf | direct
source_url: 原始链接（如有）
fetched_at: YYYY-MM-DD HH:MM
fetched_by: agent-name  # 执行 Ingest 的 Agent 名称（如 secretary-general、my-agent）
                       # 建议保持统一，便于追溯是哪个 Agent 入库的
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

## 六、多 Agent 并发编辑指引

如果知识库由多个 Agent 同时操作（如一个在 Ingest，另一个在 Query 沉淀），需要避免冲突：

```
并发安全规则：
1. INDEX.md 和 log.md 是高频写文件，多 Agent 同时写会产生冲突
2. 推荐做法：使用 Git 分支隔离，每个 Agent 在独立分支操作，完成后 merge
3. 简单场景：同一时刻只允许一个 Agent 写入 INDEX.md / log.md，其他 Agent 排队
4. 无 Git 场景：用文件锁（touch .wiki-lock / rm .wiki-lock）做简单互斥

注意：大多数场景下知识库由单个 Agent 操作，本章节可忽略。
仅当明确存在多 Agent 共享知识库的场景时才需要关注。
```

---

## 七、铁律（所有操作必须遵守）

| # | 铁律 | 原因 |
|---|------|------|
| 1 | Source 文件创建后**永不修改** | 它是知识溯源的证据链，修改后无法追溯原始信息 |
| 2 | 入库前**必须先做去重检查**（Step 0） | 重复入库会导致知识碎片化，同一内容多个版本难以维护 |
| 3 | Source 必须包含**完整原文**，禁止只存摘要/大纲 | Source 是"原始快照"，如果只存摘要就失去了与 Wiki 的区分意义 |
| 4 | Source 文件低于最小阈值**必须报警**（见第九节阈值表） | 文件过小说明抓取可能只拿到了摘要，信息不可逆丢失 |
| 5 | 每次入库后**必须更新 INDEX.md + log.md** | 索引是知识库的唯一入口，脱节后用户和 Agent 都无法找到内容 |
| 6 | 交叉引用使用**标准 Markdown 链接**，不用 [[双链]] | 标准 Markdown 在任何编辑器中都能渲染，双链依赖特定工具 |
| 7 | 有价值的对话后**主动询问**是否沉淀 | 对话中的综合分析如果不存下来，下次就得重新推导，知识复利归零 |
| 8 | Lint 报告中的 🔴 级问题**必须立即修复** | 失效链接和未编译页面会破坏知识网络的完整性 |

---

## 八、参考文件清单

| 文件 | 路径 | 用途 |
|------|------|------|
| Wiki 维护规范模板 | `references/SCHEMA-template.md` | Setup 时生成为定制化 SCHEMA.md |
| Ingest SOP 模板 | `references/INGEST-SOP-template.md` | Setup 时复制为 INGEST-SOP.md |
| Lint 巡检清单 | `references/LINT-checklist.md` | 每次巡检时对照执行 |
| 安装指南 | `references/SETUP-GUIDE.md` | 首次安装 Setup 详细步骤 |
| 多源适配手册 | `references/SOURCE-ADAPTERS.md` | Ingest Step 1 时查阅具体适配器 |
| 故障排除手册 | `references/TROUBLESHOOTING.md` | 遇到问题时查阅解决方案 |
| Lint 巡检脚本 | `scripts/lint.sh` | 自动化执行 Lint 检查 |

---

## 九、Source 文件最小阈值参考表

不同来源类型的正常文件大小差异很大，一刀切 2KB 会产生误报。以下阈值供 Step 6 自检参考：

| 来源类型 | 正常范围 | 报警阈值 | 说明 |
|----------|----------|----------|------|
| 微信公众号文章 | 5-50KB | < 3KB | 含排版和图片链接，正常较长 |
| 飞书 PRD/技术文档 | 5-80KB | < 3KB | 结构化文档，通常较大 |
| 普通网页/博客 | 2-30KB | < 1.5KB | 差异大，短文章可能确实只有 2KB |
| PDF 提取文本 | 3-100KB | < 2KB | 取决于页数和内容密度 |
| 本地文件 | 不限 | < 1KB | 几乎不应触发报警 |
| 粘贴文本 | 不限 | < 500B | 用户可能只粘贴了片段 |

**使用原则**：低于报警阈值 → 必须重新抓取确认。高于阈值但内容明显不完整（只有目录没有正文）→ 同样需要重新抓取。

---

## 十、版本迁移指南

### v1.3.x → v1.4.0

**变更内容**：INDEX.md 行填写示例、INGEST-SOP/SCHEMA 旧阈值统一、知识库定位机制、Query 页面 frontmatter 模板、fetched_by 命名规范。

**迁移方式**：无需操作。已生成的知识库内容不受影响。

### v1.2.x → v1.3.0

**变更内容**：工具降级矩阵、Wiki 编译质量标准、查询结果处理策略、跨领域文档规则、lint.sh --stats 自动统计、并发编辑指引。

**迁移方式**：无需操作。已生成的知识库内容不受影响。SCHEMA.md 中可手动补充「编译质量标准」和「跨领域规则」两个新章节。

### v1.1.x → v1.2.0

**变更内容**：新增 Ingest 完整示例、页面生命周期管理（更新/删除/合并/查询）、description 同义词扩展、铁律增加原因说明。

**迁移方式**：无需操作。已生成的知识库内容不受影响。

### 通用迁移原则

1. **Skill 升级不影响已有知识库**——模板变更只影响新 Setup
2. **新增字段可选**——已有页面无需强制补齐，仅新建页面使用新格式
3. **Breaking change 在 major 版本标注**——minor 版本保证向后兼容

---

## 十一、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.4.0 | 2026-06-14 | E1-E6：INDEX 填写示例、阈值统一、知识库定位、Query 模板、fetched_by 规范 |
| 1.3.0 | 2026-06-14 | D1-D7：工具降级、编译质量标准、查询结果策略、跨领域规则、lint.sh --stats、并发指引 |
| 1.2.0 | 2026-06-14 | O1-O6：Ingest 示例、页面生命周期、同义词扩展、快速指引、铁律原因说明 |
| 1.1.0 | 2026-06-14 | P5-P12：Setup 指引增强、错误历史标注、阈值场景化、Query 判断标准、Lint 脚本、FAQ、迁移指南、英文关键词 |
| 1.0.1 | 2026-06-14 | P1-P4：模板语法修复、路径引用修复、触发描述增强、工具声明新增 |
| 1.0.0 | 2026-06-14 | 首版：基于 Karpathy LLM Wiki 模式实践提炼，多源适配 |
