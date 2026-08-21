# Sanitization Policy

示例附件只能以副本形式脱敏，原始文件不得覆盖。

## Forbidden terms

默认扫描大小写不敏感，并同时扫描可见文本、HTML 属性、CSS、JavaScript、注释、URL 参数和 JSON 字符串：

- `TCL`
- `TCLHome`
- `TCL Home`
- `TCL+`
- `TCLer`
- `TCL ID`
- `TCL Account`
- `TCLHome API`
- `Hongye`
- `鸿鹄`

规则应允许继续追加公司、组织、品牌和内部项目名称。

## Replacement map

| 原值类别 | 替换值 |
|---|---|
| 产品 A 相关名称 | `产品 A` / `productA` |
| 产品 B 相关名称 | `产品 B` / `productB` |
| 主题名称 | `产品 A 主题` / `产品 B 主题` |
| 邮箱 | `demo-user@example.invalid` |
| 手机号 | `00000000000` |
| 内部 URL | 删除或替换为 `https://example.invalid/` |
| API/访问令牌 | 删除并报告 |

## Public-data checks

扫描以下模式：API key、Bearer token、GitHub token、常见云厂商 key、邮箱、11 位手机号、内部域名、`file://` 之外的外部资源 URL。发现命中时，脱敏脚本必须报告文件、匹配类别和替换结果。

## Release rule

敏感词扫描有任何命中，示例不能进入最终本地 Skill 包；必须先替换并重新扫描。
