# PRD Flow

统一协议的需求闭环 Skill：需求澄清 -> 需求分析 -> PRD 渲染。

## 目录说明

- `SKILL.md`：标准 Skill 入口文档（含 frontmatter）
- `PRD Flow 接口文档.md`：完整协议文档
- `manifest.json`：Skill 元信息、入口与路径索引
- `schemas/`：请求与响应 JSON Schema
- `prompts/`：Orchestrator / Clarifier / Analyzer / Renderer 提示词
- `examples/`：按宿主拆分的请求与响应示例

## 协议真源

本仓库采用 Schema First：

- 请求真源：`schemas/request.schema.json`
- 响应真源：`schemas/response.schema.json`

`SKILL.md`、接口文档和 `prompts/` 都应与上述 schema 保持一致。

## 示例覆盖范围

每个宿主目录均提供以下最小示例集：

- `start.request.json`
- `continue.request.json`
- `waiting_clarification.response.json`
- `completed.response.json`

其中 `examples/Cursor/generate_prd.request.json` 保留为 Cursor 的快捷启动样例。

## 本地校验示例（AJV）

在仓库根目录执行：

```bash
npx ajv-cli validate --spec=draft2020 -s ./schemas/request.schema.json -d "./examples/**/**.request.json"
npx ajv-cli validate --spec=draft2020 -s ./schemas/response.schema.json -d "./examples/**/**.response.json"
```

若提示找不到 `ajv-cli`，先安装：

```bash
npm install -g ajv-cli
```

## 版本

- Skill Version: `1.0.0`
- Protocol Version: `1.0.0`
