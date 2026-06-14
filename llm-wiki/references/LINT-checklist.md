# Lint 巡检清单 — LLM Wiki 健康检查

> **频率建议**：每 1-2 周执行一次，或每次大规模更新后执行。
> **执行方式**：逐项检查，🔴 级直接修复，🟡 级汇总请用户确认，🟢 级仅提示。
> **产出**：Lint 报告追加到 log.md。

---

## 巡检清单（9 项）

### 1. Source 未编译 🔴 必修

**检查内容**：所有 `-source.md` 文件是否都有对应的编译后 `.md` 页面。

**命令**：
```bash
# 找出所有 source 文件
find {知识库根目录} -name "*-source.md" | sort

# 对每个 source，检查对应 wiki 是否存在
for f in $(find {知识库根目录} -name "*-source.md"); do
  wiki="${f%-source.md}.md"
  [ ! -f "$wiki" ] && echo "❌ 未编译: $f"
done
```

**修复**：为未编译的 source 创建对应的 Wiki 页面（执行 Ingest Step 3）。

---

### 2. 失效交叉引用 🔴 必修

**检查内容**：所有 Wiki 页面中 `🔗 关联页面` 区块的链接指向是否真实存在。

**命令**：
```bash
# 提取所有 markdown 链接中的路径
grep -roh '\[.*\](.*\.md)' {知识库根目录} --include="*.md" | \
  grep -oP '\(.*\.md\)' | tr -d '()' | sort -u

# 对每个链接路径验证文件是否存在
for link in $(grep -roh '](\.\.?/[^)]*\.md)' {知识库根目录} --include="*.md" | tr -d '[]()'); do
  # 需要解析相对路径
  echo "检查: $link"
done
```

**简化方法**：
```bash
# 列出所有 .md 文件，然后检查 related 字段中的路径
find {知识库根目录} -name "*.md" | sort
# 手动/Agent 逐页检查 frontmatter 中的 related 数组
```

**修复**：更新或删除失效链接。

---

### 3. 孤立页面 🟡 建议修

**检查内容**：每个 Wiki 页面是否至少被一个其他页面通过 `related` 或正文链接引用。

**命令**：
```bash
# 列出所有 wiki 页面
all_pages=$(find {知识库根目录} -name "*.md" ! -name "*-source.md" ! -name "SCHEMA.md" ! -name "INDEX.md" ! -name "log.md" ! -name "INGEST-SOP.md")

for page in $all_pages; do
  basename=$(basename "$page")
  # 检查是否被其他文件引用
  refs=$(grep -rl "$basename" {知识库根目录} --include="*.md" | grep -v "$page" | wc -l)
  [ "$refs" -eq 0 ] && echo "⚠️ 孤立: $page"
done
```

**修复**：为孤立页面找到合适的关联页面，添加交叉引用。

---

### 4. frontmatter 不完整 🟡 建议修

**检查内容**：每个 Wiki 页面（非 source、非系统文件）是否包含完整的 YAML frontmatter。

**必含字段**：`title`、`type`、`category`、`created`、`updated`、`sources`

**命令**：
```bash
for f in $(find {知识库根目录} -name "*.md" ! -name "*-source.md" ! -name "SCHEMA.md" ! -name "INDEX.md" ! -name "log.md"); do
  # 检查是否有 frontmatter
  head -1 "$f" | grep -q "^---" || echo "❌ 无 frontmatter: $f"
  # 检查必要字段
  for field in title type category created updated sources; do
    grep -q "^${field}:" "$f" || echo "⚠️ 缺少 ${field}: $f"
  done
done
```

**修复**：补充缺失的 frontmatter 字段。

---

### 5. 内容矛盾 🟡 人工确认

**检查内容**：不同页面对同一事实（产品规格、功能支持、版本号等）的描述是否一致。

**方法**：
1. 提取所有页面中的关键数据点（版本号、日期、数值等）
2. 按主题分组对比
3. 标记不一致的地方

**注意**：此项通常需要 Agent 阅读理解内容，纯命令无法完成。建议 Agent 每次聚焦一个主题做矛盾检查。

**修复**：标记矛盾点，请用户确认哪个版本正确，然后统一更新。

---

### 6. 过时声明 🟡 人工确认

**检查内容**：搜索可能已过期的标记性文字。

**命令**：
```bash
grep -rn "待验证\|TODO\|待定\|计划中\|v1\.0\|FIXME\|HACK\|XXX" {知识库根目录} --include="*.md"
```

**处理**：逐条确认是否已过期，更新或移除标记。

---

### 7. 命名不规范 🟢 提示

**检查内容**：文件名是否全部 kebab-case、无空格、无中文、无特殊字符。

**命令**：
```bash
find {知识库根目录} -name "*.md" | while read f; do
  basename=$(basename "$f")
  # 检查是否有空格或大写
  echo "$basename" | grep -qP '[\s\p{Han}]' && echo "⚠️ 命名不规范: $f"
done
```

**修复**：重命名文件（同时更新所有引用该文件的交叉引用链接）。

---

### 8. INDEX.md 同步 🟡 建议修

**检查内容**：INDEX.md 是否覆盖所有 Wiki 页面，有无遗漏。

**命令**：
```bash
# 列出实际 wiki 页面
actual=$(find {知识库根目录} -name "*.md" ! -name "*-source.md" ! -name "SCHEMA.md" ! -name "INDEX.md" ! -name "log.md" ! -name "INGEST-SOP.md" -printf "%f\n" | sort)

# 列出 INDEX.md 中提到的页面
indexed=$(grep -oP '\[.*?\]\(.*?\.md\)' {知识库根目录}/INDEX.md | grep -oP '\(.*?\.md\)' | tr -d '()' | xargs -I{} basename {} | sort -u)

# 对比差异
diff <(echo "$actual") <(echo "$indexed")
```

**修复**：将遗漏的页面补充到 INDEX.md 对应分类中。

---

### 9. log.md 同步 🟢 提示

**检查内容**：最近的操作（Ingest/Query/Lint）是否在 log.md 中有对应记录。

**方法**：
1. 检查最近的 git commits（如启用 Git）
2. 检查文件修改时间
3. 与 log.md 中的记录对比

**命令**：
```bash
# 最近 7 天的 git commits
git log --oneline --since="7 days ago" 2>/dev/null

# 最近 7 天修改的文件
find {知识库根目录} -name "*.md" -mtime -7

# log.md 最后 20 行
tail -20 {知识库根目录}/log.md
```

**修复**：补充遗漏的日志记录。

---

## 巡检报告模板

巡检完成后，追加到 log.md：

```markdown
## [YYYY-MM-DD] Lint 巡检 | 第 N 次定期健康检查

### 检查结果摘要

| # | 检查项 | 结果 | 严重度 | 处理 |
|---|--------|------|--------|------|
| 1 | Source 未编译 | X 处 / ✅ | 🔴 | 已修复 / 无问题 |
| 2 | 失效链接 | X 处 / ✅ | 🔴 | 已修复 / 无问题 |
| 3 | 孤立页面 | X 处 / ✅ | 🟡 | 待用户确认 / 无问题 |
| 4 | frontmatter | X 处 / ✅ | 🟡 | 已修复 / 无问题 |
| 5 | 内容矛盾 | X 处 / ✅ | 🟡 | 待用户确认 / 无问题 |
| 6 | 过时声明 | X 处 / ✅ | 🟡 | 待用户确认 / 无问题 |
| 7 | 命名规范 | X 处 / ✅ | 🟢 | 仅提示 / 无问题 |
| 8 | INDEX 同步 | X 处 / ✅ | 🟡 | 已修复 / 无问题 |
| 9 | log 同步 | X 处 / ✅ | 🟢 | 仅提示 / 无问题 |

### 修复明细
（列出具体修复了哪些文件的哪些问题）

### 待用户确认
（列出 🟡 级需要用户决策的问题）

- Git Commit: {hash}
```

---

## 自动化建议

### 定时巡检（通过 OpenClaw cron）

```yaml
# 每周日凌晨 3:00 自动执行 Lint
schedule: "0 3 * * 0"
task: |
  读取 LINT-checklist.md，对知识库执行全量 9 项巡检。
  修复 🔴 级问题，🟡 级问题汇总后在下次用户对话时汇报。
  将报告追加到 log.md，git commit。
```

### 增量巡检（Ingest 后自动触发）

每次 Ingest 完成后，自动执行第 1、2、8 项检查（Source 编译、链接有效性、INDEX 同步），确保单次入库质量。

---

*本清单由 llm-wiki skill v1.0.0 提供，随知识库规模增长可扩展更多检查项。*
