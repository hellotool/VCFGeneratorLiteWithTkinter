# 图标设计

本节介绍 VCF 生成器 Lite 项目的图标设计规范。

## 系统图标

由于 Tkinter 无法对图片进行分数缩放，因此使用 Emoji 替代系统图标。

Emoji 尺寸需根据当前字体大小动态计算，以保证视觉协调。

## 应用图标

### 设计规范

- **遵循标准**：[Windows 11 图标设计规范][win-icon-design]
- **配色方案**：[2014 Material Design 调色板][material-colors]
- **设计工具**：Inkscape
- **设计文件**：`assets/design/icon.svg`

### 更新流程

1. 使用 Inkscape 编辑 `assets/design/icon.svg`，导出以下资源：
   - 大图标：PNG，480×480
   - 小图标：PNG，48×48
   - 矢量图标：SVG
2. 使用 PhotoDemon 基于大图标生成 ICO 文件。
3. 将生成的文件替换至对应路径。

### 图标文件路径

| 路径                                                  | 格式       | 用途                  |
| ----------------------------------------------------- | ---------- | --------------------- |
| `assets/images/icon.svg`                              | SVG        | 文档展示              |
| `assets/images/icon.ico`                              | ICO        | Windows 端应用图标    |
| `src/vcf_generator_lite/resources/images/icon-48.png` | PNG，48×48 | 窗口标题栏/任务栏图标 |

### ICO 图标规格

| 类型   | 尺寸列表                   |
| ------ | -------------------------- |
| PNG    | 256×256                    |
| 32-bpp | 64×64, 48×48, 32×32, 16×16 |

[win-icon-design]: https://learn.microsoft.com/zh-cn/windows/apps/design/style/iconography/overview
[material-colors]: https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors
