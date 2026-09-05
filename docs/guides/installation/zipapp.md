# Python ZIP 应用

轻量级的跨平台分发方式，无需安装即可运行。

**文件**：`VCFGeneratorLite-v<应用版本>-py3.pyzw`

您可以从 [Gitee 发行版][release-gitee] 或 [GitHub Releases][release-github] 下载。

**前置条件**：

- [Python 3.12 及以上版本](#安装-python)（含 Tkinter）

## 安装 Python

请参考 Python 官方安装指南安装 Python 3.12 及以上版本：

- [Windows][python-guide-windows]
- [Linux][python-guide-unix]
- [macOS][python-guide-macos]

Windows 用户推荐通过 [Python 安装管理器][pymanager-docs]（[Microsoft Store][msstore-python] 或官网下载）安装。如果使用遗留安装程序，请确保勾选 **Add Python to PATH** 和 **Install launcher for all users**（安装 Python 启动器，用于双击打开 `.pyzw` 文件）。

## 在 Windows 中双击启动

双击 `.pyzw` 文件即可运行。需要安装以下任一工具来关联 `.pyzw` 文件：

- [Python 安装管理器][pymanager-docs]（推荐）：Python 官方提供，自动管理 Python 版本。
- [Python 启动器][pylauncher-docs]（已弃用）：可在遗留安装程序界面中勾选安装。

> [!NOTE]
>
> 如果双击后显示命令行窗口而非应用界面，请参考 [常见问题](../../troubleshooting/faq.md#双击后显示命令行窗口)。

## 在 Windows 命令行中启动

```bash
python <pyzw 文件路径>
```

## 在 Linux / macOS / WSL 命令行中启动

```bash
chmod +x <pyzw 文件路径>
./<pyzw 文件路径>
```

或：

```bash
python3 <pyzw 文件路径>
```

[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[msstore-python]: https://apps.microsoft.com/detail/9NQ7512CXL7T
[python-guide-windows]: https://docs.python.org/zh-cn/3.14/using/windows.html
[python-guide-unix]: https://docs.python.org/zh-cn/3.14/using/unix.html
[python-guide-macos]: https://docs.python.org/zh-cn/3.14/using/mac.html
[pymanager-docs]: https://docs.python.org/zh-cn/3.14/using/windows.html#python-install-manager
[pylauncher-docs]: https://docs.python.org/zh-cn/3.14/using/windows.html#python-launcher-for-windows-deprecated
