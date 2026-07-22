# 常见问题

本文汇总用户在使用 VCF 生成器 Lite 时常见的问题与解答。

## 如何导入联系人数据

**问题描述：**

如何将联系人数据导入到应用中？

**解决方案：**

无论数据来自 Excel、微信、邮件还是网页，都可以通过复制粘贴的方式导入。

1. 从任意来源复制联系人数据（<kbd>Ctrl</kbd>+<kbd>C</kbd>）。
2. 打开 VCF 生成器 Lite。
3. 在文本框中粘贴（<kbd>Ctrl</kbd>+<kbd>V</kbd>）。

数据格式为 `姓名 电话 备注`，应用会自动识别行中的电话号码，将电话号码左侧内容作为姓名，右侧内容作为备注。

详细步骤请参阅 [导入联系人](../guides/import-contacts.md)。

## 生成的 vCard 文件有什么用

**问题描述：**

生成的 `.vcf` 文件能做什么？

**解决方案：**

vCard 文件是一种标准的电子名片格式，几乎所有通讯录应用都支持导入。您可以将生成的 `.vcf` 文件：

- 导入到手机通讯录（华为、小米、OPPO、vivo 等）
- 导入到 QQ 邮箱的联系人
- 导入到飞书通讯录
- 导入到 Outlook、Thunderbird 等邮件客户端

详细步骤请参阅 [使用 vCard 文件](../guides/vcard-usage.md)。

## 提示"缺失号码或号码不正确"

**问题描述：**

生成时提示某些行缺失号码或号码格式不正确。

**原因：**

输入的号码未匹配任何已启用的号码格式。可能是您输入的号码格式不正确，也可能是对应的号码格式未被勾选。

**解决方案：**

1. 检查菜单 **选项 > 号码格式**，确认需要的号码格式已勾选。
2. 检查输入的号码格式是否正确。
3. 如果某地区受支持的号码格式不完整，或您希望添加新地区的号码格式，欢迎通过 [GitHub Issues][issues-github] 或 [Gitee Issues][issues-gitee] 提交反馈。
4. 您也可以自行添加号码格式，详见 [号码检测器开发指南](../dev/globalization/phone-detector.md)。

## 生成的 vCard 文件导入后出现乱码

**问题描述：**

将生成的 vCard 文件导入 Windows 联系人后，非英文字符显示为乱码。

**原因：**

Windows 联系人默认使用系统编码读取 vCard 文件，而本应用生成的文件使用 UTF-8 编码（通过 Quoted-Printable 编码）。

**解决方案：**

在 Windows 设置中勾选 **使用 Unicode UTF-8 提供全球语言支持**：

1. 打开 **控制面板 > 时钟和区域 > 区域**。
2. 切换到 **管理** 选项卡，点击 **更改系统区域设置**。
3. 勾选 **Beta 版: 使用 Unicode UTF-8 提供全球语言支持**。
4. 重启计算机后重新导入 vCard 文件。

## 生成文件时界面卡顿

**问题描述：**

生成 vCard 文件时，应用界面可能出现短暂卡顿。

**原因：**

CPython 的[全局解释器锁（GIL）][gil-docs]限制了同一时刻只能有一个线程执行 Python 字节码，这会在多线程场景下影响界面响应。

**解决方案：**

这是正常现象。生成完成后界面会恢复正常。

对于专业用户，您可以尝试切换到[自由线程 Python 解释器][free-threaded-cpython-docs]运行应用。自由线程模式允许多个线程在同一解释器中同时执行 Python 字节码，从而绕过 GIL 限制，提升多线程性能。

## 如何添加新的号码格式

**问题描述：**

需要识别某个地区的电话号码格式，但应用不支持识别该格式。

**解决方案：**

本应用支持通过编辑号码检测器 Python 配置文件来扩展号码格式。详细步骤请参阅 [号码检测器开发](../dev/globalization/phone-detector.md)。完成后可通过 Pull Request 提交更改，贡献给项目。

## 双击后显示命令行窗口

**问题描述：**

双击应用图标后，显示了命令行窗口，而不是应用界面。

**原因：**

Python 安装管理器 26.0 或更低版本不支持自动升级为窗口化的 Python 解释器（[python/pymanager#216]）。

**解决方案：**

- 将 Python 安装管理器升级到 26.1 或更高版本。
- 或使用 [Python 启动器][pylauncher-docs]。

## 界面模糊

**问题描述：**

在 Windows 中，当调整显示缩放比例或将窗口移动到不同屏幕时，应用界面会显示模糊。

在 GNU/Linux 中，应用界面可能会显示模糊。

**原因：**

应用的显示缩放比例在启动时确定，运行中无法动态调整。

在 Windows 中，为了解决缩放不匹配的问题，当屏幕 DPI 变化时，系统会自动进行位图拉伸。

而在 GNU/Linux 中，缩放通常由 X11 显示服务器进行位图拉伸，应用始终以 96 DPI 显示。

**解决方案：**

暂无解决方案。

## 没有深色模式

**问题描述：**

在系统设置为深色模式后，应用仍显示浅色主题。

**原因：**

Tkinter 并没有内置深色主题，Windows 视觉样式也没有提供深色主题。

**解决方案：**

- 使用 Windows 的 [高对比度主题][windows-high-contrast-support]。
- 或使用第三方工具（如 [Rectify11][rectify11-website]）修改系统主题。

## 更多帮助

仍未找到答案？欢迎通过以下渠道联系我们：

- [GitHub Discussions][discussions-github] — 技术交流与讨论
- [GitHub Issues][issues-github] — 报告问题或提交建议
- [Gitee Issues][issues-gitee] — 报告问题或提交建议（中国大陆地区用户推荐）

[issues-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/issues
[issues-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/issues

[discussions-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/discussions

[pylauncher-docs]: https://docs.python.org/zh-cn/3.14/using/windows.html#python-launcher-for-windows-deprecated
[gil-docs]: https://docs.python.org/zh-cn/3.14/glossary.html#term-global-interpreter-lock
[free-threaded-cpython-docs]: https://docs.python.org/zh-cn/3.14/whatsnew/3.13.html#whatsnew313-free-threaded-cpython
[windows-high-contrast-support]: https://support.microsoft.com/zh-cn/windows/%E5%9C%A8-windows-%E4%B8%AD%E6%9B%B4%E6%94%B9%E9%A2%9C%E8%89%B2%E5%AF%B9%E6%AF%94%E5%BA%A6-fedc744c-90ac-69df-aed5-c8a90125e696

[python/pymanager#216]: https://github.com/python/pymanager/issues/216

[rectify11-website]: https://www.rectify11.com/
