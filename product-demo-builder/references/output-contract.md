# Output Contract

## Required files

### `index.html`

- 单一完整 HTML 文档；
- 内联 CSS 与 JavaScript；
- 不依赖网络、API Key 或后端；
- 能直接双击打开；
- 包含控制台、舞台、默认页面和至少一条完整可点击流程；
- 所有待确认内容使用明确标记，不得伪装成真实事实。

### `demo-manifest.json`

必须是生成 HTML 所依据的 manifest 原件，而不是生成后的摘要。它用于后续增量修改和验证。

### `verification-report.md`

至少包含：

1. 输入来源与生成时间；
2. 已确认项、占位项和待确认项；
3. 页面/状态/动作/验收路径统计；
4. 静态验证结果；
5. 浏览器烟测结果或未执行原因；
6. 敏感词、个人数据和外部依赖扫描结果；
7. 已知限制，例如视觉 QR 不可扫码。

## Completion language

只有 `validate_demo.py` 退出码为 0，且至少一条主路径烟测通过，才能报告“已验证”。如果浏览器不可用，只能报告“静态校验通过，浏览器烟测未执行”。
