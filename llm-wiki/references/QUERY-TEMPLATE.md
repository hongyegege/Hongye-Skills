# Query 沉淀页面模板

> 对话中产生的综合分析存回知识库时，使用此模板。
> 由 SKILL.md 第三节 3.2 Query 沉淀引用。

---

## frontmatter 模板

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

## 正文结构模板

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

## 存放位置

- 跨领域分析 → `queries/` 目录
- 单领域分析 → 对应领域目录

## 命名规范

- `{主题}-query.md` 或 `{主题}-analysis.md`
- kebab-case，无空格无中文

## INDEX.md 记录格式

在 INDEX.md 的「🧠 Query 沉淀」表格中新增条目：

| 页面 | 主题 | 关联文档 | 更新日期 |
|------|------|----------|----------|
| [分析标题](queries/xxx-query.md) | 主题关键词 | page-a, page-b | YYYY-MM-DD |
