# 故障排除手册 — LLM Wiki Troubleshooting

> 遇到常见问题时查阅本文件。
> 按场景分类，快速定位解决方案。

---

## 一、Ingest 抓取失败

### 1.1 飞书文档抓取返回空内容

**症状**：`feishu_fetch_doc` 返回空或只有标题

**原因**：
- 文档权限不足（需要文档所有者授权）
- user_access_token 过期

**解决**：
1. 检查 token 有效性：重新发起一次飞书工具调用，系统会自动触发授权流程
2. 确认文档是否对当前用户可见（在飞书中手动打开确认）
3. 如果文档是他人分享给你的，确认分享权限包含"可阅读"

---

### 1.2 微信公众号文章抓取失败

**症状**：curl 返回空内容或 web_fetch 只有框架无正文

**原因**：微信的三重防护（JS 动态渲染 + 滑块验证码 + 反爬加密）

**解决**（按优先级）：
1. **移动端 UA 直连**（最稳定）：
   ```bash
   curl -L -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38" "{URL}"
   ```
2. **搜索镜像站**：
   ```
   web_search("{文章标题}") → 找到 163.com/zhihu/sohu 等转载 → web_fetch 镜像 URL
   ```
3. **搜狗微信搜索**：`https://weixin.sogou.com/` 搜索文章标题
4. **兜底**：请用户手动复制文章正文

---

### 1.3 网页抓取返回 403/登录墙

**症状**：web_fetch 返回 403 Forbidden 或登录页面

**解决**：
1. 尝试 `browser` 工具打开页面（可能绕过部分反爬）
2. 搜索 Google Cache：`web_search("cache:{URL}")`
3. 尝试 archive.org：`web_fetch("https://web.archive.org/web/{URL}")`
4. 兜底：请用户手动复制内容，使用 Direct Adapter

---

### 1.4 PDF 提取文本乱码/不完整

**症状**：pdf 工具提取的文本有乱码、缺页、表格格式混乱

**原因**：
- 扫描件 PDF（纯图片无文本层）
- 特殊编码的 PDF

**解决**：
1. 扫描件 → 用 `image` 工具逐页分析（相当于 OCR）
2. 表格格式丢失 → 手动重建 Markdown 表格
3. 大 PDF → 分页处理：`pdf(path, pages="1-10")` 分批提取

---

## 二、Source 文件质量问题

### 2.1 Source 文件太小（低于阈值）

**症状**：Step 6 自检发现 source 文件 < 阈值

**原因**：只抓到了摘要/大纲，没有完整原文

**解决**：
1. 重新用对应适配器抓取一次
2. 微信文章：检查是否命中了反爬，换 Level 1/2 策略
3. 飞书文档：检查是否分页获取（大文档需要 offset/limit）
4. 如果多次尝试仍然太小，请用户确认原文是否确实很短

---

### 2.2 Source 文件内容是 HTML 标签而非正文

**症状**：source 文件里全是 `<div>`、`<script>` 等标签

**原因**：抓取工具返回了原始 HTML 而非提取后的正文

**解决**：
1. web_fetch 时确保 `extractMode="markdown"`
2. 如果用 curl 直连，需要用 grep/sed 提取正文区域
3. 使用 browser 工具的 snapshot 功能获取渲染后内容

---

## 三、索引与日志问题

### 3.1 INDEX.md 统计数字与实际不符

**症状**：INDEX 底部统计说 30 个页面，但实际有 35 个

**原因**：某次 Ingest 忘记更新统计摘要

**解决**：
```bash
# 重新统计
echo "Wiki pages: $(find {wiki_root} -name '*.md' ! -name '*-source.md' ! -name 'SCHEMA.md' ! -name 'INDEX.md' ! -name 'log.md' ! -name 'INGEST-SOP.md' | wc -l)"
echo "Sources: $(find {wiki_root} -name '*-source.md' | wc -l)"
echo "Images: $(find {wiki_root} -name '*.png' -o -name '*.jpg' -o -name '*.gif' | wc -l)"
```
然后手动更新 INDEX.md 底部的统计摘要。

---

### 3.2 log.md 记录缺失

**症状**：最近入库了文档但 log.md 没有记录

**解决**：补写一条记录，格式：
```markdown
## [YYYY-MM-DD] Ingest | 文档标题
- Source: 路径
- Wiki: 路径
- 图片: 路径（张数）
- 来源: 原始来源
- 说明: 一句话摘要
```

---

## 四、Git 相关问题

### 4.1 git push 被 pre-push hook 拦截

**症状**：push 时报 "pre-push check failed"

**原因**：钩子检测到异常（大量删除、本地远端差异过大等）

**解决**：
1. 检查 `git diff --cached --name-only` 是否有意外删除
2. 如果是正常操作，确认无误后请用户批准：`SKIP_PUSH_CHECK=1 git push`
3. 如果是误拦截（如正常的大规模重构），向用户说明情况后推进

---

### 4.2 远端有更新导致 push 被拒

**症状**：`rejected - fetch first`

**解决**：
```bash
git pull --rebase origin main
git push origin main
```

---

### 4.3 未启用 Git 时的数据备份

**症状**：用户选择不启用 Git，但担心数据丢失

**解决**：
1. 定期将知识库目录打包备份：`tar -czf wiki-backup-$(date +%Y%m%d).tar.gz {wiki_root}`
2. 或同步到云存储（飞书云空间、网盘等）

---

## 五、Setup 初始化问题

### 5.1 SCHEMA.md 生成后仍有 {变量} 残留

**症状**：Setup 完成后 SCHEMA.md 中仍有 `{知识库名称}` 等占位符

**解决**：
```bash
# 检查残留
grep -n '{' {wiki_root}/SCHEMA.md

# 手动替换
sed -i 's/{知识库名称}/实际名称/g' {wiki_root}/SCHEMA.md
```

---

### 5.2 领域目录名含中文或空格

**症状**：创建的目录名包含中文（如 `产品/`）或空格

**解决**：
1. 领域目录名应使用 kebab-case 英文
2. 重命名：`mv "产品/" "product/"`
3. 更新 SCHEMA.md 和 INDEX.md 中的引用

---

## 六、Lint 巡检问题

### 6.1 lint.sh 脚本报错 "command not found"

**症状**：`bash lint.sh` 报错找不到 find/grep 等命令

**原因**：极少数环境可能缺少 GNU coreutils

**解决**：
1. 确认环境：`which find grep wc`
2. macOS 上安装 GNU 版本：`brew install findutils grep`
3. 或者手动按 LINT-checklist.md 中的命令逐项执行

---

### 6.2 大量孤立页面需要修复

**症状**：Lint 报告几十个孤立页面

**解决**：
1. 优先修复高价值页面（被查询频率最高的）
2. 批量处理：找到同领域页面，互相添加交叉引用
3. 创建"领域总览"页面，引用该领域下所有页面

---

*本手册由 llm-wiki skill v1.1.0 提供，随实践积累持续扩展。*
*遇到本手册未覆盖的问题，请记录到本文件中，供后续用户参考。*
