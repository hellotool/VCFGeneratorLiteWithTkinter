# 视觉设计

视觉设计整体遵循 [Windows 7 设计][win7-uxguide]，但在某些方面有所不同。

## 应用主题

应用使用系统默认主题。部分预置主题存在缺陷，因此本应用引入了主题补丁器。

主题补丁器相关代码位于：`src/vcf_generator_lite/ui/themes/`。

## 界面布局

界面边距遵循 [Windows 7 布局设计][win7-vis-layout]。

开发时使用点（`p`）作为逻辑单位，以适配高 DPI 屏幕。

Tk 默认 DPI 为 72，而 Windows 默认 DPI 为 96，因此[有效像素（epx）][win-epx]与点的换算关系为：

- `1p = 1.333epx`
- `1epx = 0.75p`

常用尺寸对照如下：

| 点（p） | 有效像素（epx） |
| ------- | --------------- |
| 8.25p   | 11epx           |
| 5.255p  | 7epx            |

### 布局原则

1. 优先使用 `pack` 布局管理器，构建响应式用户界面。
2. 组件间距统一使用 `8.25p`（`11epx`）。
3. 适配缩放：布局中优先使用 p 单位。若目标控件或容器不支持 p 单位，则需通过 `scale` 工具函数自行缩放。

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

[win-epx]: https://learn.microsoft.com/zh-cn/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design#effective-pixels-and-scale-factor
[win-icon-design]: https://learn.microsoft.com/zh-cn/windows/apps/design/style/iconography/overview
[win7-uxguide]: https://learn.microsoft.com/zh-cn/windows/win32/uxguide/guidelines
[win7-vis-layout]: https://learn.microsoft.com/zh-cn/windows/win32/uxguide/vis-layout
[material-colors]: https://m2.material.io/design/color/the-color-system.html#tools-for-picking-colors
