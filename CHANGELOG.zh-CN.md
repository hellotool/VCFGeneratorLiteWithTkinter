<!-- markdownlint-disable no-duplicate-heading -->

# 更新日志

**简体中文** |
[English](./CHANGELOG.md)

本项目的所有重要变更都将记录在此文件中。

格式基于汉化后的 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [Python 包版本规范](https://packaging.python.org/en/latest/specifications/version-specifiers/)。

“未发布”中的日志散落在各个语言文件中，将会在发布新版本时合并。

## [未发布]

### 新增

- 翻译所有 CLI 内容。
- verbose 模式新增更多日志信息。
- 添加多地区号码格式支持。
- 支持中国港澳台地区电话号码格式。
- 未捕获异常时自动保存错误日志，并引导用户反馈给开发者。

### 修复

- 修复引号清理功能在包含换行符时的错误行为。
- 修复自 `v4.3.0` 版本以来的进度条显示问题。

### 变更

- 将翻译框架迁移到 gettext
- 提升 `LANGUAGE` 环境变量优先级。
- 在 AI 的指导下重构项目，各层次职责更加清晰，代码更加模块化，可维护性更高。

## [5.0.4] - 2026-05-07

### 新增

- 新增更新日志。

### 修复

- 修正所有组件之间的间距。
- 修复应用图标中参数错误。

### 变更

- 将示例联系人改为中国古代诗人。
- 重新整理项目文档。

## [5.0.3] - 2026-04-28

### 新增

- Windows GUI 版本支持以信息框显示命令行输出，如 `.\vcf-generator-lite.exe --version`。

### 修复

- 修复无效联系人对话框列表右侧溢出问题。

### 移除

- 移除 Linux 端尺寸调整控件。

## [5.0.2] - 2026-04-16

### 变更

- 优化无效联系人对话框加载流程，先显示窗口再异步插入数据以提升响应速度。

### 修复

- 修复无效联系人对话框标题纵向边距过大的问题。
- 移除停止生成菜单项中意外显示的快捷键提示。
- 修复关闭文件时因异常导致的界面卡死问题。
- 修复语言回退场景下文件选择逻辑混乱的问题。
- 修复英语语言环境下可能出现的闪退及报错问题。

### 移除

- 移除无效联系人场景下的警告日志生成逻辑。

## [5.0.1] - 2026-04-15

### 新增

- 引入主题补丁器，允许用户自定义主题补丁，并防止补丁被应用到外部主题。

### 修复

- 修复使用自定义主题时可能找不到字体的问题。
- 修复子窗口背景色未跟随主题的问题。
- 为 Linux 中保存对话框的部分组件支持高 DPI。
- 修复 Linux 中警告图标过大的问题。

### 变更

- 重构项目部分代码。

## [5.0.0] - 2026-04-06

### 新增

- Windows 端版本号的构建号现支持预发布、后发布及开发代码标识。
- 新增支持停止生成文件的功能。
- 关于窗口中添加了环境信息。
- 开源了图标设计文件，并优化了图标外观。

### 修复

- 修复 ZIP 应用缺失 shebang 行。
- Linux 端不再强制居中于屏幕，解决了多屏幕环境下的居中错位问题。
- 修复定位错误号码时不会自动滚动。
- 修复链接引用错误。

### 变更

- 对项目整体代码进行了重构。
- 优化了界面中的文案表述。
- 优化了项目文件的组织结构。

## [4.4.1] - 2026-03-11

### 新增

- 新增 Python Wheel 格式分发支持。
- 支持 darwin 风格快捷键显示。
- 编辑框始终高亮显示当前选中文字，便于定位错误。

### 修复

- 重构 VCF 生成器逻辑，解决线程池泄露。
- 修复 Windows 下路径分隔符误用 `/`。
- 修复高 DPI 缩放下树形视图行高计算错误。
- 修复 Linux 下符号栏可被意外选中。

### 变更

- 移除主题化背景 Frame，小幅提升性能。
- 优化代码结构，提升可维护性。

## [4.4.0] - 2026-02-15

### 新增

- 主窗口编辑区新增行号显示，支持点击行号选中整行，拖拽行号可连续多选。
- 在错误行显示窗口中双击任意表格项，即可快速定位至原始文本对应位置。
- 为 X11 窗口系统添加重做操作快捷键。
- 文件生成成功后，自动显示性能耗时及总行数统计。

### 变更

- 精简错误行显示窗口中原因字段的文本长度，并实现中文化显示。
- 升级至 Python 3.14t 自由线程版本，显著减少主线程阻塞。
- 迁移至 `uv` 工具链，提升依赖管理与构建效率。
- 补充并完善多项单元测试，提高代码健壮性。

## [4.3.0] - 2025-12-31

### 新增

- 添加对英文界面的初步支持，暂不支持用户自定义译文。
- 当联系人信息出现错误时，无效联系人对话框会明确显示错误原因。
- 在打开链接失败时向用户发出提示。
- 在无效联系人对话框的标题和内容之间添加分割线，提升可读性。
- 为无效联系人对话框中的警告图标添加颜色标识。
- 开发阶段启用彩色日志输出，提升调试效率。
- 添加更多测试用例，提升稳定性。

### 修复

- 通过删除关于对话框，修复了其中图标缩放异常的问题。
- 因删除关于对话框，解决了其编辑框的所有已知问题。

### 变更

- 删除旧版关于窗口，替换为更简洁的关于信息框。
- 取消 Zip 应用的编译依赖，使其支持多版本 Python 解释器。
- 删除显式主题设置，重构为主题补丁，为未来自定义主题功能做准备。
- 将开始生成按钮的快捷键由 `Ctrl+S` 更改为 `Ctrl+G`。
- 在生成文件过程中，开始生成按钮将显示忙碌状态。
- 移除用于构建菜单的 DSL 相关类和函数。
- 简化启用 DPI 感知的代码逻辑。
- 将 `os_notices.md` 更名为 `os-notices.md`。
- 更新部分依赖库至最新版本。
- 优化应用构建流程，提高效率。

### 移除

- 移除 tkhtmlview 组件。

## [4.2.1] - 2025-05-30

### 修复

- 修复备注乱码的问题。

## [4.2.0] - 2025-05-30

### 新增

- 支持备注字段。
- 崭新的 APP 图标。
- 无效窗口警告图标使用 Emoji 图标。
- 启动后自动聚焦文本框。
- 为移除引号功能提供访问键。

### 修复

- 修复 Windows 中窗口居中问题，Linux 中仍然存在一些问题。
- 修复高字体缩放下缩放失效的问题。

### 变更

- 重构项目代码。
- 添加窗口类名。
- 开源声明移动到网站中。
- 优化生成进度条。

## [4.1.3] - 2025-03-13

### 变更

- 安装器在安装更新前将会自动卸载老版本，修复覆盖安装导致资源错乱的问题。
- 优化资源调用逻辑。

## [4.1.2] - 2025-03-10

### 变更

- 仅修改了文档和构建输出文件名，功能无变化。

## [4.1.1] - 2025-03-10

### 变更

- 仅修改了文档和构建输出文件名，功能无变化。

## [4.1.0] - 2025-03-04

### 新增

- 新增无效号码列表对话框。

### 修复

- 修复 Windows 7 菜单字体错误。

### 变更

- 优化 UI 界面。
- 保存文件时使用上一次保存使用的文件名。

## [4.0.0] - 2025-03-01

> [!CAUTION]
>
> 上个版本（3.0.3）有严重 bug，建议直接使用本版本或更新版本。

### 新增

- 支持配置文件。

### 变更

- 重构项目代码。
- 更换许可证为 Apache 2.0。

## [3.0.3] - 2025-02-08

> [!CAUTION]
>
> 此版本有严重 bug，生成的 VCF 文件无法被识别，请直接使用 v4.0.0 或更高版本。

### 新增

- ZIP 应用版支持 Linux。
- 关于窗口支持使用回车键和 Escape 键关闭窗口。
- 编辑框支持原生主题。

### 变更

- 非 Windows 系统改用 Clam 主题。
- 阻止用户在文件生成期间关闭窗口。

## [3.0.2] - 2025-01-28

### 变更

- 优化代码。

## [3.0.1] - 2025-01-19

### 新增

- 新增 ZIP 应用。
- 尝试支持 Linux 系统。

### 修复

- 修复生成文件未正常关闭的问题。

### 变更

- 编辑器使用默认颜色设置。

## [3.0.0] - 2025-01-13

### 新增

- 添加菜单访问快捷键，并设置转换操作的快捷键为 `Ctrl+S`。
- 在生成文件的过程中增加进度条显示。
- 引入多线程技术，实现文本生成与文件生成的并行处理，同时确保生成文件时不阻塞用户界面。
- 增加移除引号的功能。
- 对于无法处理的号码，添加行号标识，便于用户快速定位。
- 将生成完成对话框与无法识别号码的对话框合并，提醒用户无法识别的号码将不会被添加到文件中。
- 输入框支持显示制表符（Tab）。
- 使用 GitHub Actions 进行编译和打包流程。

### 修复

- 优化高分辨率屏幕的缩放功能，确保在 Windows 7 上也能实现良好的缩放效果。

### 变更

- 改进用户界面设计，优化文案内容。
- 将 Python 版本升级至 3.13，不再支持 Windows 7 系统，Windows 7 用户可通过手动应用补丁继续运行。
- 设置窗口默认居中显示，提升用户体验。
- 调整并更新部分库的开源许可证信息。

## [2.0.2] - 2024-06-21

### 变更

- 更新应用图标。
- 更新 PyInstaller 版本。

## [2.0.1] - 2024-06-17

### 新增

- 新增关于页面。

### 修复

- 修复另存为对话框中扩展名错误。

### 变更

- 优化对高分屏的适配。
- 继续重构项目代码。

## [2.0.0] - 2024-03-25

### 新增

- 在生成完毕后显示所有错误行。
- 添加应用图标。
- 添加安装器，废除直接运行与启动器方式。
- 使用 poetry 包管理工具。
- 添加右键菜单。
- 保存文件支持选择路径与文件名。

### 变更

- 优化 UI 界面。
- 重构项目代码。
- 适配高分屏。
- 调整使用说明。

## [1.1] - 2023-06-12

### 新增

- 自动删除每行首尾空格。

## [1.0] - 2023-04-21

### 新增

- 初始版本发布。

[未发布]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/compare/v5.0.4...HEAD
[5.0.4]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.4
[5.0.3]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.3
[5.0.2]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.2
[5.0.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.1
[5.0.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v5.0.0
[4.4.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.4.1
[4.4.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.4.0
[4.3.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.3.0
[4.2.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.2.1
[4.2.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.2.0
[4.1.3]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.3
[4.1.2]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.2
[4.1.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.1
[4.1.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.1.0
[4.0.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v4.0.0
[3.0.3]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.3
[3.0.2]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.2
[3.0.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.1
[3.0.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v3.0.0
[2.0.2]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v2.0.2
[2.0.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v2.0.1
[2.0.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v2.0.0
[1.1]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v1.1
[1.0]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/tag/v1.0
