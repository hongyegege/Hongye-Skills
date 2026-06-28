# Hongye-Skills

宏也株式会社（Hongye Co., Ltd.）内部 Skill 仓库，收录面向 OpenClaw 的 AI Agent 技能模块。每个 Skill 均可独立安装到 OpenClaw 环境中使用。

---

## 📋 技能总览

| # | 技能名称 | 一句话说明 | 版本 | 适用场景 |
|---|----------|-----------|------|----------|
| 1 | [proposal-review-panel](#1-proposal-review-panel-五维评审团) | 五维评审团，对智能家居/IoT 洞察报告进行多角色交叉评审 | v1.0 | 报告评审、方案审查 |
| 2 | [product-roadmap-writer](#2-product-roadmap-writer五看三定) | 基于「五看三定」方法论生成 B2B/行业产品规划路线图 | v1.0 | 产品规划、路线图撰写 |
| 3 | [daily-review-manager](#3-daily-review-manager每日复盘) | 接收、记录、整理每日复盘，自动生成周报/月报 | v1.0 | 个人复盘、知识管理 |
| 4 | [meeting-writer](#4-meeting-writer会议纪要生成) | 将会议内容整理为标准格式会议纪要，自动创建飞书文档 | v1.0 | 会议纪要、Meeting Minutes |
| 5 | [prd-workflow](#5-prd-workflowprd-端到端生成工作流) | PRD 端到端生成工作流：多格式输入 + 双模板匹配 + 逻辑重构 + 飞书文档创建 | v1.0 | PRD 文档生成、需求整理 |
| 6 | [llm-wiki](#6-llm-wiki个人知识库构建系统) ⭐ | 基于 Karpathy LLM Wiki 模式的知识库构建系统：Ingest 入库 + Query 沉淀 + Lint 巡检 | **v1.5.0** | 知识管理、第二大脑、文档归档 |
| 7 | [ui-mockup](#7-ui-mockup界面效果图生成) | PRD → 界面效果图 SOP：分析现有 UI → 明确改动点 → 生成结构化 Prompt → AI 出图 | v1.0 | UI 效果图、界面设计、PRD 可视化 |
| 8 | [product-launch-speech](#8-product-launch-speech产品发布演示页) | 生成自包含 HTML 产品发布演示页 + 可编辑 page-design.md，支持沉浸式舞台风格与增量修改 | v1.0 | 产品发布、Keynote 式介绍页、交互 Demo |

---

## 1. proposal-review-panel（五维评审团）

> 🏷️ 智能家居 · IoT · 报告评审 · 多角色评审

### 功能简介

对智能家居 / IoT 产品洞察报告、方案规划报告进行 **5 个角色的交叉评审**，模拟真实企业中不同高管视角的独立意见。输入一份文档，输出结构化的多维度评审报告。

### 五位评审角色

| 角色 | 视角 | 核心关注 |
|------|------|----------|
| 🌐 **外部行业战略分析专家** | 全球智能家居全景 | 行业趋势、竞品对标、市场格局、生态平台、风险窗口 |
| 🏢 **企业总经理**  | 战略决策者 | 汇报结构、业务价值、差异化竞争、"第一/唯一/最" |
| 📊 **IoT业务技术负责人** | 务实落地者 | 成本可控、用户可感知、ROI 指标、隐私红线 |
| 📐 **战略与规划部负责人** | 逻辑结构化 | 文档结构完整性、资源保障、路线图、备选方案 |
| ✍️ **顶级润色专家** | 格式/结构/语言 | 去 AI 味、逻辑闭环、高层可读性、企业级排版 |

### 评审输出

每个角色依次输出：**亮点 → 问题 → 优化建议**，要求：
- 所有问题精准定位到报告具体章节/句子
- 所有优化建议提供可直接复制的修改示例（原句 → 修改后）
- 指出盲区、漏洞、错误判断，禁止空泛评价
- 所有判断带依据：行业趋势、对标案例、数据逻辑

### 使用方式

1. 将 `proposal-review-panel/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 上传报告/方案/规划文档，并要求「评审」或「五维评审」
3. Agent 自动按 5 个角色依次输出评审意见

### 触发关键词

评审、review、审查、提意见、五维评审、交叉评审

---

## 2. product-roadmap-writer（五看三定）

> 🏷️ 产品规划 · 路线图 · 五看三定 · 战略规划

### 功能简介

基于「**五看三定**」方法论生成 B2B / 行业产品规划路线图。适用于设备智能化、产业数字化、平台型产品、AI 解决方案、能源管理与 IoT 领域的战略规划文档撰写。

### 方法论框架

**五看：** 看行业 → 看市场 → 看客户 → 看竞争 → 看自己

**三定：** 定控制点 → 定目标 → 定策略

### 输出内容

| 章节 | 内容 |
|------|------|
| 战略分析 | 五看维度全面分析 |
| 目标设定 | 短期/中期/长期目标 |
| 产品包规划 | 产品包定义与映射 |
| AI 嵌入方案 | AI 能力融入规划 |
| 依赖拆分 | 内外部依赖梳理 |
| 风险评估 | 风险点与应对 |

### 参考资源

| 文件 | 用途 |
|------|------|
| `wugan-sanding-methodology.md` | 方法论全文：角色、原则、结构、模板、自检清单 |
| `examples/商用空调智能化产品规划（2026年H2）.md` | 成稿样例：章节层次、表格化程度、业务拆解参考 |

### 执行模式

- **模式 A（信息采集）**：信息充分时直接生成
- **模式 B（补全追问）**：信息不足时先追问补齐
- **模式 C（直接生成）**：用户要求"先出初稿"时，允许假设并单列「假设前提」

### 使用方式

1. 将 `product-roadmap-writer/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 提供规划主题（如"商用空调智能化产品规划"）
3. Agent 自动按五看三定方法论生成规划文档

### 触发关键词

产品规划、路线图、五看三定、中长期规划、platform planning、product roadmap

---

## 3. daily-review-manager（每日复盘）

> 🏷️ 个人复盘 · 日记 · 周报 · 月报 · 知识管理

### 功能简介

自动化管理每日复盘内容，支持文字和语音输入，自动结构化存储，并可生成周报和月报。适用于个人知识管理、日记记录、工作总结等场景。

### 核心功能

| 功能 | 说明 |
|------|------|
| 📝 **复盘记录** | 接收文字或语音输入，自动结构化存储 |
| 🎙️ **语音转写** | 自动使用 Whisper 将语音转换为文字 |
| 📊 **周报生成** | 汇总本周复盘内容，按主题分类统计 |
| 📈 **月报生成** | 汇总本月复盘，包含成长曲线与亮点汇总 |
| ⏰ **定时提醒** | 可设置每日复盘提醒时间 |

### 存储格式

复盘内容统一存储在 `dailyreview.md` 中，每条包含：
- 记录时间
- 复盘内容
- 主题
- 内容亮点
- 心情

### 使用方式

1. 将 `daily-review-manager/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 发送文字或语音，包含关键词即可触发
3. 随时可要求生成周报/月报

### 触发关键词

复盘、今天感悟、流水账、记录复盘、每日复盘、周报、月报、工作总结、今日总结

### 依赖工具

| 工具 | 用途 |
|------|------|
| ffmpeg | 语音文件处理 |
| whisper | 语音转文字 |

---

## 4. meeting-writer（会议纪要生成）

> 🏷️ 会议纪要 · Meeting Minutes · 飞书文档 · 结构化整理

### 功能简介

将原始会议讨论内容（录音转写稿、讨论要点、会议记录草稿）整理为 **标准格式会议纪要**，并自动创建为飞书文档保存到指定文件夹。

### 会议纪要结构

| 区块 | 说明 |
|------|------|
| **元信息表（置顶）** | 会议时间/地点/召集人/与会人/请假/缺席/迟到/纪要审核/纪要整理（无标题） |
| **一、主要纪要** | 会议背景 + 按议题分组的讨论要点 |
| **二、遗留事项汇总** | 待办事项表格：问题/提出人/责任人/确认人/闭环时间 |

### 核心能力

| 能力 | 说明 |
|------|------|
| 📋 **按议题维度组织** | 不按发言人流水账，同一议题下交叉引用各方观点 |
| ✍️ **结构化提炼** | 讨论要点按发言人分组，提炼核心观点 |
| 📊 **遗留事项提取** | 自动提取待办事项并填入责任矩阵 |
| 🚀 **飞书一键创建** | 自动创建飞书文档到「会议纪要」文件夹 |

### 使用方式

1. 将 `meeting-writer/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 发送会议内容（录音转写稿、讨论要点、会议记录草稿等）
3. Agent 自动整理并创建飞书文档，返回文档链接

### 触发关键词

整理会议纪要、meeting minutes、会议记录、帮我做个会议记录、会议纪要

---

## 5. PRD-Workflow（PRD 端到端生成工作流）

> 🏷️ 产品需求 · PRD 生成 · 端到端编排 · 多格式输入 · 逻辑重构

### 功能简介

**PRD 端到端生成工作流**，覆盖从需求材料输入到飞书文档产出的完整链路：

1. **多格式输入** — 支持 Excel / Word / PDF / 图片 / Markdown / 飞书文档 / 纯文本
2. **模板参照** — 优先使用用户提供的参考材料，降级使用内置通用模板
3. **需求确认** — 智能判断是否需要确认，避免不必要的交互成本
4. **逻辑重构** — 深度去重、归纳、推导场景、提取公共规则（内置）
5. **标准化输出** — L1-L3 分层结构 + 功能矩阵 + 附录，统一格式

### 8 步执行流程

```
环境自检 → 文件解析 → 模板检索 → 需求确认 → 逻辑重构 → PRD 生成 → 创建文档 → 知识沉淀
```

### 核心特性

| 特性 | 说明 |
|------|------|
| 📂 **多格式解析** | Excel（pandas）、Word（python-docx）、PDF、图片 OCR、Markdown、飞书文档 |
| 📐 **内置通用模板** | 内置 PRD-template.md 作为保底格式参照，开箱即用 |
| 🔄 **优雅降级** | 环境自检 + 降级提示，缺失依赖时自动降级而非报错 |
| 🎯 **智能确认** | 需求明确时直接执行，需求模糊时才确认，提高效率 |
| 📊 **PK 产品对比** | 多产品用 ✔/✘ 矩阵对比，差异写备注列 |
| 📝 **用户引导** | 无知识库时主动引导用户提供参考材料 |

### 输入格式支持

| 格式 | 解析方式 | 示例场景 |
|------|---------|----------|
| Excel (.xlsx) | 解析所有 Sheet，自动识别核心表 | FDS 功能需求表、业务需求清单 |
| Word (.docx) | 提取文本内容 | 旧版 PRD、产品说明文档 |
| PDF (.pdf) | PDF 文本提取 | 产品规格书、技术规范 |
| 图片 (.png/.jpg) | OCR 识别文字 | 需求截图、手绘原型 |
| Markdown (.md) | 直接读取 | 功能清单、需求描述 |
| 飞书文档 URL | 拉取飞书云文档内容 | 在线需求文档、历史 PRD |
| 纯文本 | 直接使用用户输入 | 口语化需求描述 |

### 使用方式

1. 将 `prd-workflow/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 发送需求材料（文件/URL/文本），要求"写 PRD"、"生成需求文档"等
3. Agent 自动解析 → 确认 → 重构 → 创建飞书文档，返回文档链接

### 触发关键词

写 PRD、生成需求文档、创建产品需求文档、帮我整理、帮我做成 PRD、参照历史 PRD、参考蒸馏信息、按模板输出、功能描述重构

### 项目结构

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 主入口：触发条件 + 8 步执行流程 + 环境自检 + 模板匹配策略 |
| `reference/device-import-template.md` | 单品导入模板（设备导入/单品 PRD） |
| `reference/platform-template.md` | 平台产品模板（平台级产品建设 PRD） |
| `guides/onboarding.md` | 用户引导：如何配置个人参考知识库 |
| `assets/logic-reconstruct.md` | 逻辑重构方法论（5 步重构法 + L1-L3 分层规范） |
| `evals/evals.json` | 评估测试集（4 套用例） |

---

## 6. llm-wiki（个人知识库构建系统）⭐

> 🏷️ 知识管理 · 第二大脑 · PKM · LLM Wiki · Karpathy · 文档入库

### 功能简介

基于 **Andrej Karpathy 的 LLM Wiki 模式**构建的个人知识库系统。核心思想：**Source（不可变原始文档）→ Wiki（编译后的结构化知识）→ 知识网络（交叉引用）**。

经过 5 轮 Skill Creator 深度审查（37 个问题修复），评分从 7.5 提升至 9.95。

### 三大核心工作流

| 工作流 | 说明 | 触发场景 |
|--------|------|----------|
| **Ingest（文档入库）** | 外部文档 → Source 快照 → Wiki 编译 → 交叉引用 | 用户提供文档要求入库 |
| **Query 沉淀** | 对话中的综合分析 → 存回知识库 | 有价值的问答产出 |
| **Lint 巡检** | 9 项健康检查（失效链接、未编译、孤立页面等） | 定期维护知识库 |

### 多源适配器

支持 6 种来源类型，统一输出为标准 Source 格式：

| 来源 | 适配器 | 特殊处理 |
|------|--------|----------|
| 飞书文档 | `feishu_fetch_doc` | authcode 过期降级 |
| 微信公众号 | 移动端 UA curl + 镜像站 | 三级降级策略 |
| 网页/博客 | `web_fetch` | 反爬、登录墙 |
| 本地文件 | `read` 工具 | GBK→UTF-8 编码 |
| PDF | `pdf` 分析工具 | 扫描件 OCR |
| 粘贴文本 | 直接使用 | 格式丢失 |

### 核心特性

| 特性 | 说明 |
|------|------|
| 📐 **九步 Ingest SOP** | 去重 → 抓取 → Source → Wiki → 图片 → 索引 → 自检 → 沉淀 → Git |
| 🛡️ **工具降级矩阵** | optional_tools 不可用时自动降级，流程不卡死 |
| 📊 **编译质量标准** | 信息保留率 80%+，压缩比 30-60%，好 vs 坏对比示例 |
| 🔍 **智能查询** | 5 种搜索结果处理策略（0/1-3/4-10/10+/矛盾） |
| 🏥 **自动化巡检** | `scripts/lint.sh` 支持 `--stats` 自动统计 |
| 📖 **故障排除手册** | 228 行详细 FAQ，覆盖常见坑点 |

### 使用方式

```bash
# 1. 复制 Skill 到 OpenClaw
cp -r Hongye-Skills/llm-wiki ~/.openclaw/workspace/skills/

# 2. 初始化知识库（用户说"帮我建个知识库"即可触发）
# Agent 会自动执行 Setup 流程

# 3. 入库文档
# 用户：「帮我把这篇微信文章存到知识库 https://mp.weixin.qq.com/s/xxx」

# 4. 查询知识库
# 用户：「知识库里关于 Matter 有什么？」

# 5. 定期巡检
bash ~/.openclaw/workspace/skills/llm-wiki/scripts/lint.sh ~/wiki --stats
```

### 触发关键词

建知识库、知识管理、入库、second brain、PKM、ingest、wiki health check、第二大脑、文档归档、notion 替代

### 文件清单（9 个文件，~60KB）

```
llm-wiki/
├── SKILL.md                        (500行) 技能入口
├── references/
│   ├── SCHEMA-template.md          (309行) Wiki 维护规范模板
│   ├── INGEST-SOP-template.md      (263行) Ingest 九步 SOP
│   ├── LINT-checklist.md           (243行) Lint 巡检清单
│   ├── SETUP-GUIDE.md              (241行) 安装初始化指南
│   ├── SOURCE-ADAPTERS.md          (244行) 多源适配手册
│   ├── TROUBLESHOOTING.md          (228行) 故障排除手册
│   └── QUERY-TEMPLATE.md           (58行)  Query 沉淀模板
└── scripts/
    └── lint.sh                     (251行) 自动化巡检脚本
```

---

## 7. ui-mockup（界面效果图生成）

> 🏷️ UI 效果图 · 界面设计 · PRD 可视化 · RASCEF · Atomic Prompting

### 功能简介

**PRD → 界面效果图的结构化编排引擎**，覆盖 6 个步骤：从分析现有 UI 交互逻辑，到明确新增/改动点，再到生成结构化 UI Prompt，最后配合截图喂给 AI 绘图工具输出效果图。

### 6 步执行流程

```
Step 0  图片预处理    — 自动切分多屏拼接长图（可选）
Step 1  确认现有逻辑  — 结构化理解当前页面
Step 2  明确改动点    — 增量思维，只改需要改的
Step 3  生成 Prompt   — RASCEF + Atomic Prompting 框架
Step 4  AI 出图       — 截图 + Prompt 喂给绘图工具
Step 5  评审迭代      — 不满意时的修正路径
```

### 核心原则

| ❌ 禁止 | ✅ 必须 |
|---------|---------| 
| 另起炉灶 | 先确认现有逻辑，再讨论改动 |
| 改动未描述的区域 | 明确标注"哪些区域不动"和"哪些区域改动" |
| 一次出图就期望完美 | 预期 2-3 轮迭代 |
| 跳过 Step 1 | 提供 ASCII 线框图示意改动位置 |

### 使用方式

1. 将 `ui-mockup/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 发送 PRD 内容 + 现有页面截图（可选）
3. Agent 自动按 6 步流程生成 UI Prompt 并出图

### 触发关键词

出效果图、UI 效果图、界面效果图、生成 UI mockup、根据 PRD 出图、界面设计稿、UI 原型图

---

## 8. product-launch-speech（产品发布演示页）

> 🏷️ 产品发布 · Keynote · 交互 Demo · HTML 演示页 · page-design.md

### 功能简介

将产品文档、README、功能清单、演示脚本或现有 `page-design.md` 转化为 **自包含的 HTML 产品发布演示页**（`index.html`）及配套的 **可编辑设计说明**（`page-design.md`）。页面风格偏向沉浸式舞台演示，而非普通营销落地页。

### 核心产出

| 产出 | 说明 |
|------|------|
| `index.html` | 单文件自包含 HTML：内联 CSS/JS，含 Hero、Live Demo、Features、Key Visual 等核心区块 |
| `page-design.md` | 编辑契约文档，支持后续小改动时无需重读全部原始材料 |

### 执行流程

```
素材调研 → 页面蓝图 → 生成 HTML + MD → validate_artifact.py 校验 → 交互冒烟测试
```

### 模板与参考

| 路径 | 用途 |
|------|------|
| `assets/templates/immersive-launch/` | 沉浸式舞台风格起始模板 |
| `references/template-registry.md` | 模板选择与扩展规则 |
| `references/style-presets.md` | 视觉风格预设 |
| `references/interaction-patterns.md` | 交互与 Demo 模式 |
| `references/page-design-contract.md` | page-design.md 结构契约 |
| `scripts/validate_artifact.py` | HTML + MD 产物校验 |

### 使用方式

1. 将 `product-launch-speech/` 文件夹复制到 OpenClaw 的 `skills/` 目录
2. 提供产品材料（文档、README、功能列表、现有 HTML 或 page-design.md）
3. Agent 生成演示页并运行校验脚本，确保结构合规

### 触发关键词

产品发布、launch page、Keynote 式介绍、产品演示页、HTML demo、page-design、发布演讲、interactive demo

---

## 📦 安装方式

将目标 Skill 文件夹复制到 OpenClaw 的 skills 目录：

```bash
# 克隆本仓库
git clone https://github.com/hongyegege/Hongye-Skills.git

# 复制单个 Skill 到 OpenClaw
cp -r Hongye-Skills/<skill-name> ~/.openclaw/workspace/skills/

# 或直接在 OpenClaw 中使用 clawhub 安装
clawhub install hongyegege/Hongye-Skills/<skill-name>
```

重启 Gateway 即可生效。

---

## 📜 版本记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-06-29 | product-launch-speech v1.0 | 新增 product-launch-speech（产品发布演示页）：自包含 HTML + page-design.md + 沉浸式模板 + 校验脚本 |
| 2026-06-14 | **llm-wiki v1.5.0** | 新增 llm-wiki（个人知识库构建系统），经过 5 轮 Skill Creator 深度审查，37 个问题修复，评分 9.95 |
| 2026-05-28 | prd-workflow v1.0 | 升级：新增平台产品模板、原模板重命名为单品导入模板、两个模板均追加评审/编辑/需求申请三表置顶、SKILL.md 增加模板自动匹配策略 |
| 2026-05-19 | prd-workflow | 新增 prd-workflow（PRD 端到端生成工作流）；删除 prd-flow（已被 prd-workflow 替代） |
| 2026-05-13 | meeting-writer v1.0 | 新增 meeting-writer（会议纪要生成） |
| 2026-05-08 | proposal-review-panel v1.0 | 新增 proposal-review-panel（五维评审团） |
| 2026-04-xx | v1.0 | 新增 prd-flow、product-roadmap-writer、daily-review-manager、ui-mockup |

---

## 📝 贡献说明

本仓库收录宏也团队内部创建的 OpenClaw Skill。如需贡献或反馈，请联系秘书长。
