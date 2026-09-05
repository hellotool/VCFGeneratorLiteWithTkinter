# 界面设计

应用界面整体遵循 [Windows 7 设计][win7-uxguide]，但在某些方面有所不同。

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
| 5.25p   | 7epx            |

### 布局原则

1. 优先使用 `pack` 布局管理器，构建响应式用户界面。
2. 组件间距统一使用 `8.25p`（`11epx`）。
3. 适配缩放：布局中优先使用 p 单位。若目标控件或容器不支持 p 单位，则需通过 `scale` 工具函数自行缩放。

[win-epx]: https://learn.microsoft.com/zh-cn/windows/apps/design/layout/screen-sizes-and-breakpoints-for-responsive-design#effective-pixels-and-scale-factor
[win7-uxguide]: https://learn.microsoft.com/zh-cn/windows/win32/uxguide/guidelines
[win7-vis-layout]: https://learn.microsoft.com/zh-cn/windows/win32/uxguide/vis-layout
