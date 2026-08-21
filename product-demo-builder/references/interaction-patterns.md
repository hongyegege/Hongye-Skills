# Interaction Patterns

这些模式用于组合附件风格的 Demo，不是生产级业务组件。

## Shell

- 左侧控制台：产品切换、页面预览、状态切换、重置；
- 右侧舞台：标题、徽标、设备框、提示；
- 手机默认 `390×844` 或等比例设备框；小于 `760px` 时隐藏控制台并全屏展示；
- 所有交互挂在舞台根节点下，使用事件委托，避免重复全局监听器。

## Rendering

- `render(state, manifest)` 负责从当前状态生成页面；
- 页面使用 `data-screen`，元素使用 `data-action`、`data-target` 和必要的 `data-id`；
- 每次渲染前清理过期 modal/loading timer；
- 动态插入文本必须转义；
- 页面内容可以重建，但必须恢复当前输入值、选中项和可见状态。

## Required patterns

### Navigation

页面入口、返回和 Tab 必须写入 manifest；无效返回动作要有明确 Toast 或回到指定页面。

### Lists and empty states

列表至少声明 filled/empty 两种状态。需要删除时优先采用滑动显露操作按钮，并同时提供键盘/点击替代路径。

### Input and confirmation

输入为空时主按钮禁用；提交前可展示确认弹窗；取消不改变数据；确认可进入 loading，再进入成功或失败反馈。

### Async feedback

默认使用确定性短延迟：loading 400–1000ms，Toast 1500–2200ms。所有定时器必须在 reset、切页和卸载时清理。

### QR visual placeholder

可以用固定种子生成视觉 QR 网格，但必须在文案或报告中标注“仅为视觉占位，不可扫码”。

### Capability variants

产品 A/B 应共享页面骨架，通过 `capabilities` 控制入口、按钮和模块；不要用隐藏元素模拟不存在的业务能力。

## Accessibility floor

- 交互按钮使用 `<button>`；
- 输入有 `label` 或清晰 `aria-label`；
- Toast 使用 `aria-live="polite"`；
- modal 打开时提供关闭动作；
- 图标和装饰元素标记 `aria-hidden="true"`。
