name: prd-flow
description: PRD 需求流。通过统一协议完成需求澄清、需求分析与 PRD 生成闭环。当用户要求生成 PRD、澄清需求、分析产品需求、输出结构化需求，或提及 PRD 流程、需求工作流、需求文档时触发。支持 start/continue 生命周期，支持 clarify_only / analyze_only / render_only / full / auto 等执行模式。

---

# PRD Flow

统一协议的需求闭环 Skill：需求澄清 → 需求分析 → PRD 渲染。

## 核心能力

1. **需求澄清（Clarifier）** — 判断信息是否充分，用最少高价值问题补齐缺口
2. **需求分析（Analyzer）** — 将需求转为结构化 JSON，区分已确认 / 推断 / 待确认三类信息
3. **PRD 渲染（Renderer）** — 将分析结果渲染为 Markdown，支持 Mermaid 流程图
4. **编排调度（Orchestrator）** — 根据 action/mode/state 决定下一步，无伪造内容

## 统一入口

Tool Name: `prd_flow.run`

## action 生命周期

| action       | 含义                             |
| ------------ | ------------------------------ |
| `start`      | 发起新流程，state 可为 null            |
| `continue`   | 基于已有 state 继续，要求 state 非空      |
| `retry`      | 重试当前阶段，无法识别阶段时返回 INVALID_STATE |
| `regenerate` | 基于相同输入重新生成，优先依据 state.stage    |
| `abort`      | 直接返回 aborted                   |

## mode 执行模式

| mode           | 行为                                                             |
| -------------- | -------------------------------------------------------------- |
| `auto`         | 由 Skill 自动判断执行路径，按澄清→分析→渲染顺序推进                                 |
| `full`         | 执行完整闭环                                                         |
| `clarify_only` | 仅澄清；可直接分析时 status=ready_for_analysis，questions 为空              |
| `analyze_only` | 仅分析；已有 analysisResult 时 completed；否则 status=ready_for_analysis |
| `render_only`  | 仅渲染；依赖 state.analysisResult，缺失返回 INVALID_STATE                 |
| `review_only`  | **未实现**，返回 UNSUPPORTED_MODE + failed                           |

## 澄清阶段规则（Clarifier）

**触发条件：** 当信息缺口（missingFields）会显著影响首轮分析质量时，needClarification=true。

**missingFields 枚举：** goal | persona | scope | flow | permission | constraint | integration | metric | risk

**问题约束：**

- needClarification=true 时，questions 数量 1~5
- needClarification=false 时，questions 必须为空数组
- single_select / multi_select 必须给 options

**sourceStatus 枚举：** explicit | inferred | pending_confirmation

- explicit：已确认事实
- inferred：推断建议
- pending_confirmation：待用户确认

**隐私脱敏：** options.maskSensitiveData=true 时，手机号、身份证、邮箱等统一打码为 `***`。

## 分析阶段规则（Analyzer）

**核心原则：**

- 不得将推断内容伪装为已确认事实
- 未明确信息标记为 pending_confirmation 或放入 openQuestions / suggestions
- 流程信息不足时不臆造复杂流程图
- 适配 IoT / B 端场景，优先关注角色权限、异常兜底、集成依赖、审计

**输出必须包含字段：**

- meta.domain：iot | b_end | c_end | general
- background.problem / goal / scope
- roles / scenarios / functionalRequirements
- nonFunctionalRequirements
- dataAndIntegration / metrics / risks
- diagram.diagramNeeded / diagramType / textFlow
- openQuestions / suggestions / traceability

## 渲染阶段规则（Renderer）

**Markdown 章节结构（固定）：**

1. 需求背景
2. 角色与场景
3. 功能需求
4. 数据与集成
5. 指标建议
6. 风险与兜底
7. 流程说明
8. 待确认问题
9. 建议项

**Mermaid 规则：**

- diagramNeeded=true 且 diagramType!=none 时生成 Mermaid 代码
- flowchart → `flowchart TD`
- sequence → `sequenceDiagram`
- state → `stateDiagram-v2`
- 仅基于 textFlow 字段，不得臆造节点

**信息状态标注：**

- explicit → 已确认
- inferred → 推断建议（用斜体或脚注标注）
- pending_confirmation → 待确认（需在"待确认问题"章节体现）

## 编排规则（Orchestrator）

**仅输出合法 JSON**，不输出 Markdown、代码块、前后解释。

**result 结构（三段式，始终返回）：**

json
{
"clarification": {},
"analysis": null,
"render": null
}

**澄清输出约束：**

- status=waiting_clarification + stage=clarify + nextAction=answer_questions

- result.clarification.needClarification=true

- questions 数量 1~5
  **完成输出约束：**

- status=completed + nextAction=show_prd

- result.render.markdown 必须存在
  **错误处理：**

- INVALID_REQUEST：请求结构不合法

- INVALID_STATE：状态不完整（continue 时 state 缺失）

- UNSUPPORTED_MODE：review_only 模式

- SCHEMA_VALIDATION_FAILED：输出未通过 Schema 校验

- CLARIFICATION_REQUIRED：需先完成澄清

- ANALYSIS_FAILED / RENDER_FAILED / INTERNAL_ERROR
  
  ## 内部提示词文件
  
  以下 prompts/ 目录下的文件分别对应各阶段实现逻辑：
  
  | 文件                        | 职责                               |
  | ------------------------- | -------------------------------- |
  | `prompts/Orchestrator.md` | 编排调度逻辑，根据 action/mode/state 决定响应 |
  | `prompts/clarifier.md`    | 澄清判断与问题生成逻辑                      |
  | `prompts/analyzer.md`     | 结构化分析逻辑                          |
  | `prompts/renderer.md`     | Markdown PRD 渲染逻辑                |
  
  ## 协议真源

- 请求 Schema：`schemas/request.schema.json`

- 响应 Schema：`schemas/response.schema.json`
  
  ## 示例参考
  
  各宿主（openclaw / cursor / claude_code）的 start / continue / completed 完整请求响应示例见 `examples/` 目录。Cursor 另有 `generate_prd.request.json` 快捷启动样例。
  
  ## 版本

- Skill Version: 1.0.0

- Protocol Version: 1.0.0
