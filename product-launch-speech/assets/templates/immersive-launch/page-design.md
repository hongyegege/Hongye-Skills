# 超级小 T 发布会页设计说明

## Visual Design

整体采用黑色沉浸舞台、蓝色 AI 主色和玻璃质感卡片，营造正式发布会里的产品 Demo 区域。画面中心是手机样机，右侧是演示流程和可点击话术，页面下方保留组件库与 Key Visual，方便直接截图进入汇报材料。

主要视觉变量：

- 背景：`#000000`
- 主文字：`#f5f5f7`
- 辅助文字：`rgba(255,255,255,0.65)`
- AI 主色：`#0a84ff`
- 成功状态：`#30d158`
- 警示状态：`#ff9f0a`

## Page Sections

1. Hero / Intro：用“说一句，就好了。”概括产品主张，并解释全屏 Live 态是超级小 T 的主形态。
2. Live Demo：手机样机展示“听、想、说、微调、执行”的完整流程，右侧提供流程状态和示例话术。
3. Component Library：展示生成式 UI 的原子组件，包括场景预览卡、温控盘、状态总览、设备控制面板、动作编辑卡。
4. Key Visual：提供可直接截图进 PPT 的发布会主视觉静帧。

## Interaction Design

页面主交互围绕 `runScene(sceneKey)` 状态机：

- `idle`：待命状态，展示家庭环境摘要和主动建议。
- `listening`：打字机展示用户输入，手机边框和光球进入聆听态。
- `thinking`：展示思考态文本与动态点。
- `speaking`：隐藏底部输入区，展开生成式 UI 卡片。
- `editing`：点击可编辑参数后打开局部编辑弹层。
- `executing`：确认后显示执行完成卡，再回到待命。

辅助交互包括今日摘要弹层、温度详情弹层、空气质量半弹窗、3D 空间页、洗衣机详情页和设备列表页。

## Copy Inventory

- 页面标题：超级小 T · 全屏 Live 交互 Demo
- 品牌副标题：TCL APP · AI Assistant · Concept v0.3
- Hero 标题：说一句，就好了。
- 主说明：全屏 Live 态是超级小 T 的主形态，一个持续对话的沉浸管家。
- 示例话术：我想看个电视、家里有点热、家里怎么样、我想修空调、空调不制冷怎么办。
- 组件库标题：生成式 UI 组件库 · 样本
- Key Visual 标题：PPT Key Visual · 可直接截图使用

## Change Notes

小幅修改时优先改本文档，再由 Codex 对照当前 HTML 增量更新：

- 修改产品名称时，同步更新 `<title>`、Header、Hero、Key Visual 中的品牌文案。
- 修改配色时，优先调整 CSS `:root` 变量，避免逐个改组件颜色。
- 修改演示路径时，先更新示例话术和 `SCENES` 配置，再更新右侧流程说明。
- 增减页面模块时，保持 Hero、Live Demo、Features、Key Visual 四类核心区域仍可识别。
