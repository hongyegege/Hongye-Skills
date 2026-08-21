# Demo Manifest Schema

`demo-manifest.json` 是需求与 HTML 之间的唯一结构化契约。它描述演示范围，不描述后端 API 实现。

## Minimum shape

```json
{
  "meta": {
    "title": "设备分享 Demo",
    "purpose": "演示分享与成员管理",
    "audience": "产品评审",
    "frame": "phone",
    "language": "zh-CN",
    "offline": true
  },
  "theme": {
    "tokens": {"brand": "#2F6BFF", "surface": "#FFFFFF"},
    "font": "system-ui",
    "assets": []
  },
  "products": [
    {
      "id": "productA",
      "name": "产品 A",
      "theme": "product-a",
      "capabilities": {"manage": true},
      "copy": {}
    }
  ],
  "components": [],
  "screens": [],
  "states": [],
  "actions": [],
  "data": {},
  "flows": [],
  "acceptanceFlows": []
}
```

## Field contract

### `meta`

- `title`, `purpose`, `audience`, `language`：必须确认；
- `frame`：`phone`、`desktop`、`tablet` 或 `multi`；缺失时继续追问；
- `offline`：本 Skill 默认必须为 `true`。

### `products`

每个产品必须有 `id`、展示名、主题引用、能力开关和文案覆盖。产品差异优先放在 `capabilities` 与 `copy`，不要复制完整页面。

### `screens`

每屏包含：

```json
{
  "id": "share-home",
  "title": "分享首页",
  "entry": true,
  "regions": [
    {"id": "qr", "component": "qr-state", "required": true}
  ],
  "visibleWhen": {"capability": "share"}
}
```

`regions[].component` 必须能映射到模板组件或明确的自定义组件说明。

### `states`

每个关键状态必须声明 `id`、所属页面、触发条件、可见反馈和可恢复动作。推荐至少覆盖 `normal`、`loading`、`success`、`failed`、`empty`、`expired`、`confirm` 中适用的状态。

### `actions`

```json
{
  "id": "refresh-qr",
  "event": "click",
  "target": "qr-stage",
  "from": "share-home",
  "to": "share-home",
  "effects": ["loading", "increment:qrVersion"],
  "feedback": {"success": "二维码已刷新", "failure": "二维码加载失败"}
}
```

每个动作必须有目标、起点和结果；动作目标必须能在 HTML 的 `data-target` 或 `data-action` 中找到。

### `flows` and `acceptanceFlows`

`flows` 描述所有已确认路径；`acceptanceFlows` 只列必须烟测的路径，每条包含起始页面、操作序列、预期状态和可观察结果。

## Validation invariants

1. `screens[].id` 唯一；
2. `actions[].id` 唯一；
3. 每个 `action.from` 与 `action.to` 都引用存在的页面或状态；
4. `acceptanceFlows` 中的动作都能在 `actions` 找到；
5. `products[].capabilities` 只能隐藏或展示已声明能力，不得凭空创建页面；
6. `meta.offline` 为 `true` 时不得声明外部 URL、真实接口或密钥。
