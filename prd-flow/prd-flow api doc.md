# PRD Flow 接口文档

- **Skill ID**：`prd_flow`
- **协议名称**：`PRD Flow Protocol`
- **协议版本**：`1.0.0`
- **文档版本**：`v1.0`
- **适用宿主**：OpenClaw / Cursor / Claude Code
- **文档状态**：正式草案

---

## 1. 文档目标

本文档定义一套统一的 Skill 输入输出协议，用于支撑以下完整闭环：

> 用户需求输入 → 需求澄清 → 需求分析 → PRD 生成

该协议面向多宿主环境设计，目标是让同一套 Skill 能被 OpenClaw、Cursor、Claude Code 等工具稳定复用。

---

## 2. 设计原则

### 2.1 宿主无关

同一协议可被不同宿主调用，宿主仅负责 UI 展示、状态存储、文件写入等外围能力。

### 2.2 JSON First

所有中间结果必须优先结构化输出为 JSON；Markdown 作为最终文档产物之一输出。

### 2.3 支持多轮澄清

协议必须支持：

- 首次发起
- 问题返回
- 用户补答
- 继续分析
- 输出 PRD

### 2.4 支持暂停与恢复

协议通过 `sessionId + state` 支持流程中断、恢复与续跑。

### 2.5 可扩展

协议设计需支持未来扩展：

- 审稿器（Reviewer）
- 多模板 PRD
- 多领域插件
- Schema 校验与质量门禁

---

## 3. 能力范围

本 Skill 聚焦以下能力：

1. **需求澄清（Clarification）**
   
   - 判断当前信息是否足以进入需求分析
   - 生成最少但高价值的澄清问题

2. **需求分析（Analysis）**
   
   - 将原始需求整理为结构化分析结果
   - 区分已确认事实、推断建议、待确认项

3. **PRD 渲染（Rendering）**
   
   - 将分析结果渲染为 Markdown PRD
   - 支持 Mermaid 图生成

---

## 4. 统一入口

### 4.1 Tool Name

```text
prd_flow.run
```

### 4.2 调用方式

宿主统一通过同一个入口发起调用，使用 `action` 和 `mode` 控制执行行为。

---

## 5. 生命周期定义

### 5.1 Action 枚举

| 值            | 含义           |
| ------------ | ------------ |
| `start`      | 发起新流程        |
| `continue`   | 基于已有状态继续执行   |
| `retry`      | 对当前阶段重试      |
| `regenerate` | 基于相同输入重新生成结果 |
| `abort`      | 终止流程         |

### 5.2 Mode 枚举

| 值              | 含义               |
| -------------- | ---------------- |
| `auto`         | 由 Skill 自动判断执行路径 |
| `full`         | 执行完整闭环：澄清→分析→渲染  |
| `clarify_only` | 仅执行需求澄清          |
| `analyze_only` | 仅执行需求分析          |
| `render_only`  | 仅执行 PRD 渲染       |
| `review_only`  | 已保留协议位，当前版本返回 `UNSUPPORTED_MODE` |

---

## 6. 请求协议（Request）

### 6.1 顶层结构

```json
{
  "protocolVersion": "1.0.0",
  "skillId": "prd_flow",
  "requestId": "req_20260415_001",
  "sessionId": "session_abc123",
  "action": "start",
  "mode": "full",
  "host": {
    "name": "cursor",
    "version": "0.48.0",
    "capabilities": {
      "canRenderMarkdown": true,
      "canStoreState": true,
      "canUploadFiles": true,
      "canWriteFiles": true,
      "canShowForms": false
    }
  },
  "input": {
    "userRequest": "我想做一个面向园区运维人员的设备巡检异常闭环管理功能",
    "inputType": "text",
    "attachments": [],
    "extractedContent": {
      "ocrText": "",
      "imageSummaries": [],
      "tables": []
    },
    "context": {
      "domain": "iot",
      "businessLine": "园区物联平台",
      "projectName": "设备运维平台",
      "targetPlatform": "Web",
      "additionalContext": []
    }
  },
  "state": null,
  "options": {
    "language": "zh-CN",
    "prdTemplate": "standard",
    "maxClarificationRounds": 2,
    "allowDraftWithPending": true,
    "requireDiagram": "auto",
    "strictJson": true,
    "maskSensitiveData": true,
    "outputFormats": ["json", "markdown"]
  }
}
```

### 6.2 顶层字段说明

| 字段                | 类型          | 必填  | 说明                         |
| ----------------- | ----------- | ---:| -------------------------- |
| `protocolVersion` | string      | 是   | 协议版本                       |
| `skillId`         | string      | 是   | 固定值：`prd_flow`       |
| `requestId`       | string      | 是   | 单次调用唯一标识                   |
| `sessionId`       | string      | 是   | 同一闭环流程的会话标识                |
| `action`          | enum        | 是   | 当前调用动作                     |
| `mode`            | enum        | 是   | 当前调用模式                     |
| `host`            | object      | 否   | 宿主信息与能力说明                  |
| `input`           | object      | 是   | 用户输入与上下文                   |
| `state`           | object/null | 否   | 上一轮运行状态；`start` 时可为 `null` |
| `options`         | object      | 否   | 输出策略与行为控制                  |

---

## 7. 输入对象（Input）

### 7.1 结构定义

```json
{
  "userRequest": "string",
  "inputType": "text|image|excel|mixed",
  "attachments": [],
  "extractedContent": {
    "ocrText": "string",
    "imageSummaries": [],
    "tables": []
  },
  "context": {
    "domain": "iot|b_end|c_end|general",
    "businessLine": "string",
    "projectName": "string",
    "targetPlatform": "Web|App|MiniProgram|Desktop|Mixed",
    "additionalContext": ["string"]
  }
}
```

### 7.2 字段说明

| 字段                 | 类型     | 必填  | 说明              |
| ------------------ | ------ | ---:| --------------- |
| `userRequest`      | string | 是   | 用户原始需求文本        |
| `inputType`        | enum   | 是   | 输入类型            |
| `attachments`      | array  | 否   | 用户上传的原始附件       |
| `extractedContent` | object | 否   | OCR、图片摘要、表格解析结果 |
| `context`          | object | 否   | 项目背景、领域、平台等上下文  |

### 7.3 attachments 结构

```json
[
  {
    "id": "file_001",
    "name": "需求草图.png",
    "type": "image",
    "mimeType": "image/png",
    "role": "source",
    "uri": "optional://host-managed",
    "description": "可选，宿主补充说明"
  }
]
```

#### `attachments.type` 枚举

- `text`
- `image`
- `excel`
- `pdf`
- `mixed`

#### `attachments.role` 枚举

- `source`
- `reference`
- `supporting`

### 7.4 表格解析结构示例

```json
[
  {
    "sheetName": "设备台账",
    "headers": ["设备ID", "设备名称", "状态", "最后在线时间"],
    "rows": [
      ["D001", "冷机-1", "离线", "2026-04-12 08:12:11"]
    ],
    "summary": "该表疑似用于设备状态台账"
  }
]
```

---

## 8. 状态对象（State）

### 8.1 设计目的

`state` 用于支撑多轮对话式流程，是协议闭环能力的核心。宿主在 `continue` 调用时应回传上一轮状态。

### 8.2 结构定义

```json
{
  "stage": "clarify",
  "status": "waiting_clarification",
  "iteration": 1,
  "clarification": {
    "round": 1,
    "askedQuestions": [
      {
        "id": "q1",
        "dimension": "scope",
        "label": "本次异常闭环是否包含工单派发与回单验收？"
      }
    ],
    "answers": [
      {
        "questionId": "q1",
        "answer": "包含工单派发，但暂不包含回单验收"
      }
    ],
    "missingFields": ["metric", "permission"]
  },
  "analysisResult": null,
  "renderResult": null
}
```

### 8.3 stage 枚举

| 值         | 含义     |
| --------- | ------ |
| `intake`  | 输入接收阶段 |
| `clarify` | 澄清阶段   |
| `analyze` | 分析阶段   |
| `render`  | 渲染阶段   |
| `done`    | 完成     |
| `failed`  | 失败     |

### 8.4 status 枚举

| 值                       | 含义         |
| ----------------------- | ---------- |
| `waiting_input`         | 等待输入       |
| `waiting_clarification` | 等待用户回答澄清问题 |
| `ready_for_analysis`    | 可进入分析      |
| `ready_for_render`      | 可进入渲染      |
| `completed`             | 已完成        |
| `failed`                | 执行失败       |
| `aborted`               | 已终止        |

---

## 9. 选项对象（Options）

### 9.1 结构定义

```json
{
  "language": "zh-CN",
  "prdTemplate": "lite|standard|full",
  "maxClarificationRounds": 2,
  "allowDraftWithPending": true,
  "requireDiagram": "auto|always|never",
  "strictJson": true,
  "maskSensitiveData": true,
  "outputFormats": ["json", "markdown"]
}
```

### 9.2 字段说明

| 字段                       | 类型      | 必填  | 说明                                    |
| ------------------------ | ------- | ---:| ------------------------------------- |
| `language`               | string  | 否   | 输出语言，例如 `zh-CN`                       |
| `prdTemplate`            | enum    | 否   | PRD 模板等级：`lite` / `standard` / `full` |
| `maxClarificationRounds` | number  | 否   | 最大澄清轮次                                |
| `allowDraftWithPending`  | boolean | 否   | 即使存在待确认项，也允许先输出草稿                     |
| `requireDiagram`         | enum    | 否   | `auto` / `always` / `never`           |
| `strictJson`             | boolean | 否   | 是否要求严格 JSON 输出                        |
| `maskSensitiveData`      | boolean | 否   | 是否打码敏感信息                              |
| `outputFormats`          | array   | 否   | 输出格式，例如 `json`、`markdown`             |

---

## 10. 响应协议（Response）

### 10.1 顶层结构

```json
{
  "protocolVersion": "1.0.0",
  "skillId": "prd_flow",
  "requestId": "req_20260415_001",
  "sessionId": "session_abc123",
  "status": "waiting_clarification",
  "stage": "clarify",
  "nextAction": "answer_questions",
  "message": "当前信息可进入澄清环节，建议先补充 2 个关键问题后再分析。",
  "result": {
    "clarification": {},
    "analysis": null,
    "render": null
  },
  "quality": {
    "analysisConfidence": "medium",
    "schemaValid": true,
    "warnings": []
  },
  "error": null
}
```

### 10.2 顶层字段说明

| 字段                | 类型          | 必填  | 说明           |
| ----------------- | ----------- | ---:| ------------ |
| `protocolVersion` | string      | 是   | 协议版本         |
| `skillId`         | string      | 是   | Skill ID     |
| `requestId`       | string      | 是   | 回传请求 ID      |
| `sessionId`       | string      | 是   | 回传会话 ID      |
| `status`          | enum        | 是   | 当前流程状态       |
| `stage`           | enum        | 是   | 当前所处阶段       |
| `nextAction`      | enum        | 是   | 建议宿主下一步动作    |
| `message`         | string      | 否   | 面向宿主或用户的简要说明 |
| `result`          | object      | 是   | 业务结果         |
| `quality`         | object      | 否   | 质量信息与告警      |
| `error`           | object/null | 否   | 错误信息         |

### 10.3 nextAction 枚举

| 值                  | 含义          |
| ------------------ | ----------- |
| `answer_questions` | 展示问题并收集用户回答 |
| `call_analyze`     | 进入分析阶段      |
| `call_render`      | 进入渲染阶段      |
| `show_prd`         | 展示 PRD 文档   |
| `retry`            | 允许宿主重试      |
| `abort`            | 终止流程        |
| `none`             | 无需进一步动作     |

---

## 11. result 对象定义

```json
{
  "clarification": {},
  "analysis": {},
  "render": {}
}
```

### 11.1 使用规则

- 澄清阶段：仅填充 `clarification`
- 分析阶段：填充 `analysis`
- 渲染完成：填充 `render`
- `full` 模式下可同时返回 `analysis + render`

---

## 12. 澄清结果（ClarificationResult）

### 12.1 结构定义

```json
{
  "needClarification": true,
  "readyForAnalysis": false,
  "round": 1,
  "remainingRounds": 1,
  "missingFields": ["scope", "permission", "metric"],
  "questions": [
    {
      "id": "q1",
      "dimension": "scope",
      "label": "本次需求是否包含异常工单的派发、转派和关闭全流程？",
      "type": "single_select",
      "required": true,
      "priority": "high",
      "placeholder": "请选择最符合的范围",
      "options": [
        { "id": "opt1", "label": "仅记录异常" },
        { "id": "opt2", "label": "记录异常 + 派发处理" },
        { "id": "opt3", "label": "完整闭环（记录、派发、处理、关闭）" }
      ],
      "reason": "范围不同会显著影响流程设计与功能拆解"
    }
  ],
  "summary": "角色权限和范围边界仍不清晰，建议先补充。",
  "stopReason": null
}
```

### 12.2 字段约束

1. `needClarification=false` 时，`questions` 必须为空数组。
2. `readyForAnalysis=true` 时，宿主可直接进入分析阶段。
3. 达到最大澄清轮次但允许出草稿时，可设置：

```json
{
  "needClarification": false,
  "readyForAnalysis": true,
  "stopReason": "max_round_reached_generate_draft"
}
```

---

## 13. 澄清续跑输入示例

宿主在收集用户回答后，使用 `action=continue` 继续调用。

```json
{
  "protocolVersion": "1.0.0",
  "skillId": "prd_flow",
  "requestId": "req_20260415_002",
  "sessionId": "session_abc123",
  "action": "continue",
  "mode": "full",
  "input": {
    "userRequest": "我想做一个面向园区运维人员的设备巡检异常闭环管理功能",
    "inputType": "text",
    "attachments": [],
    "extractedContent": {
      "ocrText": "",
      "imageSummaries": [],
      "tables": []
    },
    "context": {
      "domain": "iot",
      "businessLine": "园区物联平台",
      "projectName": "设备运维平台",
      "targetPlatform": "Web",
      "additionalContext": []
    }
  },
  "state": {
    "stage": "clarify",
    "status": "waiting_clarification",
    "iteration": 1,
    "clarification": {
      "round": 1,
      "answers": [
        {
          "questionId": "q1",
          "answer": "完整闭环（记录、派发、处理、关闭）"
        }
      ]
    }
  },
  "options": {
    "language": "zh-CN",
    "prdTemplate": "standard",
    "maxClarificationRounds": 2,
    "allowDraftWithPending": true,
    "requireDiagram": "auto",
    "strictJson": true,
    "maskSensitiveData": true,
    "outputFormats": ["json", "markdown"]
  }
}
```

---

## 14. 分析结果（AnalysisResult）

### 14.1 结构定义

```json
{
  "meta": {
    "domain": "iot",
    "complexity": "medium",
    "analysisConfidence": "high",
    "template": "standard"
  },
  "background": {
    "problem": {
      "content": "当前巡检异常记录与处理链路割裂，缺少统一闭环追踪。",
      "sourceStatus": "explicit"
    },
    "goal": {
      "content": "建立巡检异常从发现、派发、处理到关闭的闭环管理机制。",
      "sourceStatus": "explicit"
    },
    "scope": {
      "inScope": [
        {
          "content": "异常记录、工单派发、处理跟踪、关闭归档",
          "sourceStatus": "explicit"
        }
      ],
      "outOfScope": [
        {
          "content": "自动维修调度优化",
          "sourceStatus": "inferred"
        }
      ]
    }
  },
  "roles": [
    {
      "name": "运维人员",
      "description": "负责发现异常、接单处理、反馈结果",
      "sourceStatus": "explicit"
    }
  ],
  "scenarios": [
    {
      "name": "巡检发现异常并发起闭环",
      "description": "运维人员在巡检时发现设备异常并记录，进入工单闭环流程",
      "actors": ["运维人员", "班组长"],
      "preconditions": ["存在设备台账", "运维人员具备巡检权限"],
      "sourceStatus": "explicit"
    }
  ],
  "functionalRequirements": [
    {
      "id": "FR-001",
      "module": "异常闭环管理",
      "feature": "异常记录",
      "description": "支持巡检过程中记录设备异常并提交",
      "priority": "P0",
      "actors": ["运维人员"],
      "businessRules": ["异常记录需绑定设备对象", "异常类型为必填"],
      "normalFlow": ["运维人员发起异常记录", "系统校验必填项", "提交成功并生成异常单"],
      "exceptionFlows": ["设备不存在时不允许提交", "网络异常时支持草稿保存或重试"],
      "acceptanceCriteria": ["异常记录可成功提交并生成唯一编号"],
      "sourceStatus": "explicit"
    }
  ],
  "nonFunctionalRequirements": [
    {
      "category": "audit",
      "content": "需记录异常单状态流转与处理人操作日志",
      "sourceStatus": "inferred"
    }
  ],
  "dataAndIntegration": {
    "dataObjects": [
      {
        "name": "异常单",
        "description": "记录异常事件、处理过程与关闭结果",
        "sourceStatus": "explicit"
      }
    ],
    "integrations": [
      {
        "name": "设备台账系统",
        "description": "用于查询设备基础信息",
        "sourceStatus": "inferred"
      }
    ]
  },
  "metrics": [
    {
      "name": "异常闭环率",
      "description": "一定周期内已关闭异常单占总异常单比例",
      "type": "business",
      "sourceStatus": "inferred"
    }
  ],
  "risks": [
    {
      "title": "角色权限边界不清",
      "impact": "可能导致越权查看或误操作",
      "mitigation": "在设计阶段明确角色可见范围与操作权限矩阵",
      "sourceStatus": "explicit"
    }
  ],
  "diagram": {
    "diagramNeeded": true,
    "diagramType": "flowchart",
    "reason": "闭环流程涉及多角色与状态流转，适合用流程图表达",
    "textFlow": [
      "开始",
      "运维人员记录异常",
      "系统生成异常单",
      "班组长派发处理",
      "运维人员处理并反馈",
      "班组长确认关闭",
      "结束"
    ]
  },
  "openQuestions": [
    {
      "id": "OQ-001",
      "question": "异常关闭后是否支持再次打开？",
      "impact": "影响状态机设计与权限策略",
      "severity": "medium"
    }
  ],
  "suggestions": [
    {
      "title": "补充异常状态流转矩阵",
      "content": "建议明确待处理、处理中、待确认、已关闭等状态定义",
      "type": "interaction"
    }
  ],
  "traceability": [
    {
      "targetId": "FR-001",
      "source": "clarification.answer.q1"
    }
  ]
}
```

### 14.2 关键约束

1. `sourceStatus` 仅允许以下枚举值：
   - `explicit`
   - `inferred`
   - `pending_confirmation`
2. 未确认事实不得写入 `explicit`。
3. `nonFunctionalRequirements` 建议纳入正式分析协议。
4. `traceability` 用于建立需求点与输入来源的映射关系。

---

## 15. 渲染结果（RenderResult）

### 15.1 结构定义

```json
{
  "title": "设备巡检异常闭环管理 PRD",
  "summary": "已生成标准版 PRD，包含 1 个待确认问题与 1 项建议项。",
  "markdown": "# 设备巡检异常闭环管理 PRD\n\n## 1. 需求背景\n...",
  "artifacts": {
    "hasMermaid": true,
    "diagramType": "flowchart",
    "mermaid": "flowchart TD\nA[开始] --> B[运维人员记录异常]\nB --> C[系统生成异常单]\nC --> D[班组长派发处理]\nD --> E[运维人员处理并反馈]\nE --> F[班组长确认关闭]\nF --> G[结束]",
    "sections": [
      "需求背景",
      "角色与场景",
      "功能需求",
      "数据与集成",
      "指标建议",
      "风险与兜底",
      "流程说明",
      "待确认问题",
      "建议项"
    ]
  },
  "files": [
    {
      "name": "prd_设备巡检异常闭环管理.md",
      "contentType": "text/markdown",
      "suggestedPath": "./output/prd_设备巡检异常闭环管理.md"
    }
  ]
}
```

### 15.2 字段说明

| 字段          | 类型     | 必填  | 说明              |
| ----------- | ------ | ---:| --------------- |
| `title`     | string | 是   | 文档标题            |
| `summary`   | string | 否   | 结果摘要            |
| `markdown`  | string | 是   | PRD Markdown 内容 |
| `artifacts` | object | 否   | Mermaid、章节等附属产物 |
| `files`     | array  | 否   | 宿主落盘建议          |

---

## 16. 质量结果（Quality）

### 16.1 结构定义

```json
{
  "analysisConfidence": "high",
  "schemaValid": true,
  "warnings": [
    "仍存在 1 个待确认问题，建议评审前补齐"
  ],
  "validation": {
    "missingRequiredSections": [],
    "hasPendingConfirmation": true,
    "hasInferredContent": true,
    "renderConsistentWithAnalysis": true
  }
}
```

### 16.2 建议校验项

| 字段                             | 说明            |
| ------------------------------ | ------------- |
| `schemaValid`                  | JSON 结构是否合法   |
| `hasPendingConfirmation`       | 是否仍存在待确认项     |
| `hasInferredContent`           | 是否包含推断内容      |
| `renderConsistentWithAnalysis` | 渲染结果是否忠实于分析结果 |

---

## 17. 错误对象（Error）

### 17.1 结构定义

```json
{
  "code": "INVALID_STATE",
  "message": "当前 action=continue，但缺少有效 sessionId 或 state。",
  "details": {
    "expected": ["sessionId", "state.clarification.answers"],
    "received": ["requestId"]
  },
  "retryable": true
}
```

### 17.2 推荐错误码

| 错误码                        | 含义              |
| -------------------------- | --------------- |
| `INVALID_REQUEST`          | 请求结构不合法         |
| `INVALID_STATE`            | 状态不完整或不匹配       |
| `UNSUPPORTED_MODE`         | 不支持的执行模式        |
| `SCHEMA_VALIDATION_FAILED` | 输出未通过 Schema 校验 |
| `CLARIFICATION_REQUIRED`   | 需要先完成澄清         |
| `ANALYSIS_FAILED`          | 分析阶段失败          |
| `RENDER_FAILED`            | 渲染阶段失败          |
| `INTERNAL_ERROR`           | 内部未知错误          |

---

## 18. 标准状态机

### 18.1 流程图

```text
start
  ↓
intake
  ↓
clarify? ── yes ──> waiting_clarification
  │                    ↓
  │                continue
  │                    ↓
  └──── no ─────────> analyze
                         ↓
                      render
                         ↓
                        done
```

### 18.2 宿主行为建议

#### 场景 A：返回等待澄清

若返回：

```json
{
  "status": "waiting_clarification",
  "nextAction": "answer_questions"
}
```

宿主应：

1. 展示 `result.clarification.questions`
2. 收集用户回答
3. 使用 `action=continue` 再次调用

#### 场景 B：可进入分析

若返回：

```json
{
  "status": "ready_for_analysis",
  "nextAction": "call_analyze"
}
```

宿主可：

- 让 Skill 内部继续流转
- 或再次发起 `mode=analyze_only`

#### 场景 C：PRD 已完成

若返回：

```json
{
  "status": "completed",
  "nextAction": "show_prd"
}
```

宿主应：

- 展示 `result.render.markdown`
- 可将 `files` 写入工作区
- 可高亮 `openQuestions`

---

## 19. 宿主适配建议

### 19.1 OpenClaw

推荐作为工作流节点接入，重点消费以下字段：

- `status`
- `nextAction`
- `result.clarification`
- `result.analysis`
- `result.render.files`

### 19.2 Cursor

推荐场景：

- 发起 full 流程
- 将 PRD Markdown 直接写入项目目录
- 对输出文档进行进一步编辑

建议重点使用：

- `render.markdown`
- `render.artifacts.mermaid`
- `files.suggestedPath`

### 19.3 Claude Code

推荐场景：

- 读取本地需求资料与文档
- 生成结构化分析结果
- 将 PRD 写入 `/docs/prd/`

建议重点使用：

- `analysis`
- `render.markdown`
- `files`

---

## 20. 最小可落地版本（MVP）

### 20.1 Request MVP

```json
{
  "protocolVersion": "1.0.0",
  "skillId": "prd_flow",
  "requestId": "req_xxx",
  "sessionId": "session_xxx",
  "action": "start|continue",
  "mode": "auto|full|clarify_only|analyze_only|render_only|review_only",
  "input": {
    "userRequest": "string",
    "inputType": "text|image|excel|mixed",
    "attachments": [],
    "extractedContent": {},
    "context": {}
  },
  "state": null,
  "options": {
    "language": "zh-CN",
    "maxClarificationRounds": 2,
    "allowDraftWithPending": true,
    "outputFormats": ["json", "markdown"]
  }
}
```

### 20.2 Response MVP

```json
{
  "protocolVersion": "1.0.0",
  "skillId": "prd_flow",
  "requestId": "req_xxx",
  "sessionId": "session_xxx",
  "status": "waiting_clarification|completed|failed",
  "stage": "clarify|render|failed",
  "nextAction": "answer_questions|show_prd|retry",
  "message": "string",
  "result": {
    "clarification": {},
    "analysis": {},
    "render": {}
  },
  "quality": {
    "analysisConfidence": "low|medium|high",
    "schemaValid": true,
    "warnings": []
  },
  "error": null
}
```

---

## 21. 强约束

1. 任何阶段均不得输出 JSON 之外的包装说明。
2. Clarification / Analysis / Render 三类对象字段应保持稳定。
3. `sourceStatus` 仅允许：
   - `explicit`
   - `inferred`
   - `pending_confirmation`
4. 当 `needClarification=false` 时，`questions` 必须为空数组。
5. 当 `status=completed` 且 `outputFormats` 包含 `markdown` 时，必须返回 `render.markdown`。
6. 如果存在敏感信息，且 `maskSensitiveData=true`，输出中应统一打码为 `***`。

---

## 22. 推荐落地方式

建议将该协议拆分为以下交付件：

1. `SKILL.md`：对外说明文档（标准入口）
2. `request.schema.json`：请求 Schema
3. `response.schema.json`：响应 Schema
4. `examples/`：调用示例
5. `prompts/`：Clarifier / Analyzer / Renderer / Orchestrator Prompt 文件

建议目录结构如下：

```text
prd-flow/
├── SKILL.md
├── schemas/
│   ├── request.schema.json
│   ├── response.schema.json
│   ├── clarification.schema.json
│   ├── analysis.schema.json
│   └── render.schema.json
├── prompts/
│   ├── clarifier.md
│   ├── analyzer.md
│   ├── renderer.md
│   └── Orchestrator.md
└── examples/
    ├── start.request.json
    ├── continue.request.json
    └── completed.response.json
```
