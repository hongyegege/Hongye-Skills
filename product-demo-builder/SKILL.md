---
name: product-demo-builder
description: Use when a user wants to turn a PRD, product description, solution, Markdown/text mind map, or existing HTML into an offline clickable product Demo; not for static UI images or launch-story pages.
metadata:
  openclaw:
    emoji: "🧩"
    requires:
      bins: []
      env: []
---

# Product Demo Builder

## Outcome

生成一套可直接双击打开的离线 Demo，并同时交付：

- `index.html`：自包含 HTML、CSS、JavaScript；
- `demo-manifest.json`：产品、页面、状态、动作、流程和验收路径；
- `verification-report.md`：结构验证、烟测结果、降级项和待确认项。

视觉与交互默认沿用附件的展示语法：左侧演示控制台 + 右侧舞台 + 手机设备框；控制台可切换产品、页面和状态，手机内部使用真实 DOM 控件完成导航、输入、弹窗、加载、成功/失败、空状态、Toast 和重置。手机是默认舞台，也可按 manifest 改为桌面、平板或多设备。

## Trigger and boundaries

触发信号：PRD、功能说明、产品方案、解决方案、Markdown/文本思维导图、现有 HTML/截图，以及“交互 Demo / 可点击原型 / 产品演示 HTML”等明确意图。

不触发或转交：

- 只要静态效果图或绘图 Prompt：转 `ui-mockup`；
- 需要发布会叙事、Keynote 式讲解页：转 `product-launch-speech`；
- 生产级网站、真实后端、登录、支付或线上部署：先说明本 Skill 只提供离线 Mock，除非用户明确扩展范围。

## Mandatory workflow

### 1. Inspect sources and preserve boundaries

先读取用户提供的文档、思维导图、HTML、截图和已有规范。把信息分成：

- 已确认事实；
- 用户提出但尚未确认的方案；
- 缺失或互相冲突的内容。

不要因为示例附件中出现过某个页面、字段或文案，就把它假设成新产品必需能力。

### 2. Build the manifest before HTML

按 [references/manifest-schema.md](references/manifest-schema.md) 建立 manifest。至少收集：产品目标、受众、主路径、页面清单、区域与控件、字段、跳转、关键状态、反馈、样例数据、文案、视觉资产、舞台类型和验收流程。

### 3. Enforce the question gate

按 [references/question-gate.md](references/question-gate.md) 逐轮追问。只要缺口可能改变页面结构、主路径、关键状态、文案含义、品牌素材或验收方式，就不能生成 HTML。每轮优先问当前最影响结构的 1–3 个问题；不得用未声明的假设悄悄填空。

只有当所有必填项被确认，或用户明确接受“占位内容/待确认项”并将其写入 manifest 后，才进入生成阶段。

### 4. Select interaction patterns and generate

读取 [references/interaction-patterns.md](references/interaction-patterns.md)，从模板中组合：

- 页面导航、页面预览和产品切换；
- 列表、空状态、滑动删除；
- 输入、校验、确认弹窗；
- loading、success、failed、expired、toast；
- 离线异步 Mock、重置和返回；
- 产品 `capabilities` 控制页面和动作是否出现。

不要复制整套产品页面来表达只有文案、颜色或能力不同的变体；优先使用 `productConfig`、共享组件和状态配置。

### 5. Keep the generated artifact offline

默认内联 CSS/JavaScript 和可控 SVG/CSS 图形，不请求网络、不读取 API Key、不依赖后端。二维码只作为视觉占位，不得声称可被扫码。动态结果必须由确定性 Mock 数据、状态机和短延迟产生。

### 6. Validate before reporting

运行 `scripts/validate_demo.py`，并在有浏览器自动化能力时运行 `scripts/smoke_test.mjs`。验证要求见 [references/output-contract.md](references/output-contract.md)。若浏览器不可用，报告中必须明确标记“浏览器烟测未执行”，不能把静态校验表述为完整交互通过。

## Public-example sanitization

示例附件只以脱敏副本发布。先运行 `scripts/sanitize_reference.py`，遵循 [references/sanitization-policy.md](references/sanitization-policy.md)：

- 清除公司、组织、品牌名称及其大小写/代码变体；
- 产品名统一替换为“产品 A / 产品 B”，代码键使用 `productA/productB`；
- 邮箱、手机号、访问令牌、内部 URL 和明显个人识别数据替换为虚构值；
- 原始附件不覆盖；
- 脱敏后再次运行敏感词扫描，发现残留就停止交付。

## Resource routing

- 需要定义字段、页面、状态和动作时：读 `references/manifest-schema.md`；
- 信息不足或冲突时：读 `references/question-gate.md`；
- 选择通用交互时：读 `references/interaction-patterns.md`；
- 生成 companions 或验收报告时：读 `references/output-contract.md`；
- 复制/发布参考附件前：读 `references/sanitization-policy.md`；
- 需要可复用 HTML 骨架时：使用 `assets/demo-shell.template.html`。
