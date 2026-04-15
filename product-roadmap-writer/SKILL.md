---
name: product-roadmap-writer
description: >-
  Produces B2B/industry product roadmaps using the 五看三定 framework (five
  perspectives, three commitments): strategic analysis, goals, product
  packages, AI embedding, dependencies, and risks. Use when the user asks for
  产品规划, 路线图, 五看三定, 中长期规划, platform/solution/IoT/energy/AI
  product planning, or writing planning documents for management review.
---

# Product Roadmap Writer（五看三定）

## 何时应用

在用户需要撰写或迭代**产品规划、路线图、战略到落地的规划文档**时启用本 Skill。典型领域：设备智能化、产业数字化、平台型产品、AI 解决方案、能源管理与 IoT。

## 必读资源（渐进披露）

1. **方法论全文**：执行任务前阅读 [wugan-sanding-methodology.md](wugan-sanding-methodology.md)。其中包含角色、原则、五看三定结构、输出模板、信息采集模板、自检清单等**完整撰写规范**。
2. **结构与颗粒度参考**：对齐 [examples/商用空调智能化产品规划（2026年H2）.md](examples/商用空调智能化产品规划（2026年H2）.md) 的章节层次、表格化程度、业务环节拆解与 P1/P2/P3 表达方式，作为**同一方法论下的成稿样例**（勿机械照抄具体业务数据）。

若用户提供了其他参考样例，优先级为：**用户提供的材料 > 本 Skill 内参考文档 > 仅方法论**。

## Agent 执行步骤

1. **判断信息充分性**，按方法论中的模式 A（信息采集）/ B（补全追问）/ C（直接生成）执行；若用户要求“先出初稿”，允许假设并单列「假设前提」。
2. **通读** `wugan-sanding-methodology.md` 中的交互规则与输出结构，再开始写作。
3. **产出**时遵循方法论中的：推导链、对我方意味着什么、竞争表格化、看自己六维度、机会可追溯、控制点与产品包映射、AI 与治理边界、内外部依赖拆分、版本（详细/汇报/初稿）。
4. **风格**向参考文档靠拢：结论先行、表格与业务环节拆解、专业可汇报。

## 与方法论文件的关系

- 本 `SKILL.md` 仅作入口与导航；**规则与细节以 `wugan-sanding-methodology.md` 为准**。
- 参考文档仅用于**结构、深度、表达风格**对齐，不替代用户提供的主题与事实。

## 快速检查（执行前）

- [ ] 已打开或已内化 `wugan-sanding-methodology.md` 中的模式判断与输出清单
- [ ] 需要参考颗粒度时已查阅 `examples/商用空调智能化产品规划（2026年H2）.md`
- [ ] 信息不足时未编造核心事实，或已标注假设前提
