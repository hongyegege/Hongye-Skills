# 图片预处理 — UI 长图自动切分

> 当输入图片为多屏横向拼接的设计稿长图，或像素超过 AI 模型限制时，自动触发预处理流程。

---

## 触发条件

满足**任意一条**即触发：

| 条件 | 阈值 | 说明 |
|------|------|------|
| 总像素超限 | > 25,000,000 px | AI 图像模型（qwen 等）的硬性上限 |
| 宽高比异常 | width / height > 2:1 | 疑似多屏横向拼接的设计交付格式 |

## 自动处理流程

```
输入长图
    ↓
检测边界（黑底列扫描 → 找连续亮区段）
    ↓
逐个裁切单个屏幕
    ↓
resize 到可读尺寸（宽度 ≤ 1280px）
    ↓
逐个 read 分析（图像识别）
    ↓
合并复述现有交互逻辑
    ↓
进入 Step 1 确认环节
```

## 脚本用法

```bash
python3 scripts/split_ui_strip.py <input_image> [output_dir] [--max_width 1280]
```

**参数说明**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `input` | 必填 | 输入图片路径 |
| `output_dir` | 与输入同目录的 `screens/` | 切分后图片的保存目录 |
| `--max_width` | 1280 | 单屏最大宽度（px） |
| `--quality` | 90 | JPEG 输出质量 |
| `--check_only` | - | 仅检查是否需要预处理，不执行切分 |

**示例**：

```bash
# 基本用法
python3 scripts/split_ui_strip.py /root/.openclaw/media/inbound/xxx.png /tmp/screens

# 检查是否需要预处理（不切分）
python3 scripts/split_ui_strip.py /root/.openclaw/media/inbound/xxx.png --check_only

# 指定较小宽度（适配移动端截图）
python3 scripts/split_ui_strip.py /root/.openclaw/media/inbound/xxx.png ./screens --max_width 960
```

## 输出格式

```
📐 原始尺寸：7680×4320  像素：33,177,600
⚠️  检测到需要预处理：
   • 像素超限：33,177,600 > 25,000,000
   • 宽高比异常：1.8:1（疑似多屏拼接长图）

🔧 开始切分，输出目录：/tmp/screens
📱 检测到 13 个屏幕
  ✅ screen_00.jpg  (517×2400)
  ✅ screen_01.jpg  (517×2400)
  ...
  ✅ screen_12.jpg  (517×2400)

✅ 完成！共切分出 13 个屏幕
```

## 后续处理

切分完成后，对每个屏幕**逐个执行 `read` 工具**进行图像识别，然后将识别结果**合并复述**给操作者确认。

**注意**：如果单个屏幕像素仍然过大（高度很长），可进一步裁切为上下两半分别识别。

## 边界情况处理

| 情况 | 处理方式 |
|------|---------|
| 单张手机截图（非拼接） | `--check_only` 返回无需预处理，直接进入 Step 1 |
| 背景非黑色（白色/灰色） | 调整 `threshold` 参数（默认 100，浅色背景可降低到 50） |
| 屏幕间无间隔（紧密拼接） | 按预估屏幕数量等分切分 |
| RGBA 图片（含透明通道） | 脚本自动 `convert('RGB')` 处理，避免 JPEG 保存失败 |

## 依赖

- Python 3.8+
- Pillow（PIL）
- numpy

（均为 OpenClaw 环境已安装依赖）
