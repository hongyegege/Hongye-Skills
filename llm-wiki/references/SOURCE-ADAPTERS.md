# 多源适配手册 — Source Adapter Reference

> 本文件详细说明每种文档来源的抓取策略、图片处理和常见陷阱。
> Ingest Step 1（抓取源文档）时查阅本文件。

---

## 一、来源识别规则

Agent 收到入库请求时，按以下优先级识别来源类型：

```
优先级    匹配条件                          适配器
─────────────────────────────────────────────────────────
1        URL host 含 feishu.cn             Feishu Adapter
2        URL host 含 mp.weixin.qq.com      WeChat Adapter
3        URL 以 http(s):// 开头            Web Adapter
4        文件路径以 .pdf 结尾               PDF Adapter
5        文件路径存在（本地文件）            Local Adapter
6        无 URL 无路径（粘贴文本）           Direct Adapter
```

---

## 二、适配器详细手册

### 2.1 Feishu Adapter（飞书文档）

#### 识别
- URL 格式：`https://{host}.feishu.cn/docx/{token}` 或 `https://{host}.feishu.cn/wiki/{token}`
- 用户说"飞书文档"并提供链接

#### 抓取流程
```
1. feishu_fetch_doc(doc_id=URL或token)
   → 返回 Markdown 格式全文
2. 提取文档中的图片/画板引用
3. 对每个图片：feishu_doc_media(action=download, resource_token=img_xxx)
4. 对每个画板：feishu_doc_media(action=download, resource_type=whiteboard, resource_token=xxx)
```

#### 图片处理
- 飞书图片使用 `image_key`（如 `img_xxx`），需要通过 API 下载
- 画板缩略图使用 `whiteboard_id`
- 下载后保存到 `{领域目录}/{主题}-images/`
- Wiki 页面中替换为本地相对路径引用

#### 常见陷阱
| 陷阱 | 说明 | 解决方案 |
|------|------|----------|
| authcode 过期 | 飞书 CDN URL 中的 authcode 有有效期 | 必须用 API 下载，不能直接 curl URL |
| 文档权限 | 部分文档需要用户授权才能读取 | 确保 Agent 已获得用户 OAuth 授权 |
| 嵌入表格 | 飞书多维表格/电子表格嵌入在文档中 | 提取为 Markdown 表格或单独导出 |
| 超大文档 | >5 万字可能需要分页获取 | feishu_fetch_doc 支持 offset/limit 分页 |

---

### 2.2 WeChat Adapter（微信公众号文章）

#### 识别
- URL 格式：`https://mp.weixin.qq.com/s/{id}` 或 `https://mp.weixin.qq.com/s?__biz=...`
- 用户说"微信文章"并提供链接

#### 抓取流程（三级降级策略）

```
Level 1 — 移动端 UA 直连（最稳定）
  exec: curl -L -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)..." {URL}
  → 解析 HTML 提取正文

Level 2 — 搜索镜像站（Level 1 失败时）
  1. web_search("{文章标题}")
  2. 在结果中寻找网易(163.com)/知乎/搜狐等平台的转载
  3. web_fetch(镜像URL) → 内容完全一致，无反爬

Level 3 — Browser 工具（最后手段）
  browser: 打开原文 → 等待渲染 → snapshot 提取
  ⚠️ 可能触发滑块验证码，成功率低
```

#### 图片处理
- 微信图片 URL 格式：`https://mmbiz.qpic.cn/...`
- 这些 URL 通常可直接 curl 下载（无 authcode）
- 批量下载：`for url in $(grep -oP 'https://mmbiz[^"]+' source.md); do curl -O ...; done`

#### 常见陷阱
| 陷阱 | 说明 | 解决方案 |
|------|------|----------|
| 滑块验证码 | 自动化浏览器触发反爬 | 不用 browser，走 Level 1/2 |
| JS 动态渲染 | web_fetch 拿不到正文 | 用 curl + 移动端 UA |
| 图片防盗链 | 部分图片有 Referer 检查 | curl 加 `-H "Referer: https://mp.weixin.qq.com"` |
| 文章被删 | 404 或"该内容已被发布者删除" | 搜索缓存（搜狗微信搜索、archive.org） |

---

### 2.3 Web Adapter（网页/博客）

#### 识别
- URL 以 `http://` 或 `https://` 开头
- 不属于飞书或微信域名

#### 抓取流程
```
1. web_fetch(url=URL, extractMode="markdown")
   → 自动提取正文，返回 Markdown
2. 如果 web_fetch 返回内容过少（< 500 字符）：
   a. 尝试 extractMode="text"
   b. 使用 browser 工具打开页面 → snapshot 提取
3. 提取页面中的图片 URL
4. 下载图片到本地
```

#### 图片处理
- 从 Markdown 内容中提取 `![](url)` 中的 URL
- 使用 `exec: curl -L -o {filename} {url}` 下载
- 注意相对路径图片：需要拼接为完整 URL

#### 常见陷阱
| 陷阱 | 说明 | 解决方案 |
|------|------|----------|
| 登录墙 | 需要登录才能查看内容 | 提示用户手动粘贴内容 |
| 反爬机制 | 返回 403/Captcha | 尝试 browser 工具或搜索缓存 |
| SPA 应用 | 内容靠 JS 渲染 | 使用 browser 工具 |
| 编码问题 | 中文乱码 | web_fetch 通常处理正确，异常时手动修正 |

---

### 2.4 Local Adapter（本地文件）

#### 识别
- 文件路径以 `/` 或 `./` 或 `~/` 开头
- 或用户说"读取本地文件"

#### 抓取流程
```
1. read(path=文件路径)
   → 文本文件：直接获取内容
   → 图片文件：image 工具分析
2. 如果是 .docx / .xlsx 等 Office 格式：
   exec: python3 -c "import docx; ..." 或用 pandoc 转换
3. 如果是 .csv：
   read 直接读取，解析为结构化内容
```

#### 图片处理
- 本地文件的图片通常已在同目录或指定目录
- 复制到 Wiki 的 `{主题}-images/` 即可

#### 常见陷阱
| 陷阱 | 说明 | 解决方案 |
|------|------|----------|
| 文件编码 | GBK/GB2312 编码的中文文件 | `exec: iconv -f GBK -t UTF-8 {file}` |
| Office 格式 | .docx/.xlsx 不能直接 read | 用 pandoc 或 python 库转换 |
| 大文件 | >100MB 文件读取超时 | 分段读取或提取关键部分 |
| 路径不存在 | 文件路径错误 | 先 ls 确认路径 |

---

### 2.5 PDF Adapter

#### 识别
- 文件路径以 `.pdf` 结尾
- URL 指向 PDF 文件（Content-Type: application/pdf）

#### 抓取流程
```
1. 本地 PDF：pdf(path=文件路径, prompt="提取全文内容")
   → 返回结构化文本
2. 在线 PDF：
   a. exec: curl -L -o /tmp/doc.pdf {URL}
   b. pdf(path="/tmp/doc.pdf", prompt="提取全文内容")
3. 如果 PDF 是扫描件（纯图片）：
   → 需要 OCR，使用 image 工具逐页分析
```

#### 图片处理
- PDF 中的嵌入图片需要专门提取
- `exec: python3 -c "import fitz; ..."（PyMuPDF）` 提取图片
- 或 `exec: pdfimages -j {pdf} {output_prefix}`

#### 常见陷阱
| 陷阱 | 说明 | 解决方案 |
|------|------|----------|
| 扫描件 PDF | 纯图片无文本层 | 用 image 工具逐页 OCR |
| 多栏排版 | 提取后文字顺序混乱 | 手动整理或逐页处理 |
| 表格 | 提取后格式丢失 | 手动重建 Markdown 表格 |
| 加密 PDF | 需要密码 | 提示用户提供密码或手动导出 |

---

### 2.6 Direct Adapter（直接粘贴）

#### 识别
- 用户直接粘贴文本内容
- 无 URL、无文件路径

#### 抓取流程
```
1. 直接使用用户提供的文本
2. 添加 source_type: direct 头部
3. 无需下载图片（通常无图片）
```

#### 常见陷阱
| 陷阱 | 说明 | 解决方案 |
|------|------|----------|
| 格式丢失 | 粘贴时丢失表格/链接等格式 | 请用户尽量提供 Markdown 或富文本 |
| 来源不明 | 无法记录原始 URL | 询问用户来源信息，记录在 source 头部 |
| 内容截断 | 长文本粘贴不完整 | 提醒用户确认完整性 |

---

## 三、统一输出格式

无论哪种来源，最终保存为 `-source.md` 时使用统一头部：

```yaml
---
source_type: feishu | wechat | web | local | pdf | direct
source_url: "原始链接"（如有）
fetched_at: 2026-06-14 14:00
fetched_by: agent-name
adapter_notes: "抓取过程备注"（可选，如：通过镜像站获取）
---

# 文档标题

（完整正文内容，禁止只存大纲或摘要）
```

---

## 四、新增适配器指南

当遇到本手册未覆盖的新来源时：

1. **评估可行性**：能否通过现有工具（web_fetch/browser/exec/read）获取内容
2. **设计抓取流程**：遵循"抓取 → 转 Markdown → 保存 source"的统一模式
3. **记录陷阱**：首次操作后记录遇到的问题
4. **更新本手册**：追加新适配器章节，供后续使用

---

*本手册由 llm-wiki skill v1.0.0 提供，随新来源接入持续扩展。*
