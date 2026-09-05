# 在旧版 Windows 中运行

VCF 生成器 轻量版 支持的最低 Windows 版本为 Windows 8.1。如果您需要在 Windows 8 或更低版本中运行，可以尝试以下方案。

> [!CAUTION]
>
> 通过以下方式运行应用可能**存在安全和稳定性风险**。如果您选择继续，请注意从可信来源获取资源，并在安装前进行病毒扫描。

## 方案一：使用 PythonVista ![Windows 7][badge_windows_7] ![Windows 8][badge_windows_8]

PythonVista 是一个使旧版 Python 应用能在 Windows Vista、7、8 上运行的兼容层。

1. **获取 Python 嵌入包**：从 [PythonVista][pythonvista_repository_github] 仓库下载：
   - `python-3.14.x-embed-amd64.zip`
2. **提取 DLL 文件**：解压下载的 ZIP 包，从中获取以下文件：
   - `python314.dll`
   - `api-ms-win-core-path-l1-1-0.dll`
3. **修补程序**：
   1. 对于安装版类型：完成应用安装。
   2. 打开本应用安装目录下的 `_internal` 文件夹。
   3. 将下载的两个 DLL 文件覆盖到该目录。

**对于 Python ZIP 应用用户：**

您只需要安装 PythonVista 提供的 Python。

1. **获取 Python 安装程序**：从 [PythonVista][pythonvista_repository_github] 仓库下载：
   - 64 位系统：`python-3.14.x-amd64-full.exe`
   - 32 位系统：`python-3.14.x-full.exe`
2. **安装 Python**：运行安装程序，按照提示进行安装。

## 方案二：使用 VxKex NEXT ![Windows 7][badge_windows_7]

VxKex NEXT 是一个 Windows API 兼容层，可使新版 Windows 应用在旧版系统上运行。

**对于安装程序、便携包用户：**

1. **安装 VxKex NEXT**：从 [VxKex NEXT Release][vxkex-next_release_github] 下载最新版本并安装。
2. **配置应用**：
   1. 打开 **VxKex NEXT 全局设置**（可在开始菜单中找到）。
   2. 将本应用目录下的 `vcf_generator_lite.exe` 添加到应用程序列表中。

**对于 Python ZIP 应用用户：**

1. **安装 VxKex NEXT**：从 [VxKex NEXT Release][vxkex-next_release_github] 下载最新版本并安装。
2. **安装 Python**：
   1. 打开 **VxKex NEXT 加载器**（可在开始菜单中找到）。
   2. 选择官方的 Python 安装程序路径，并在更多选项中勾选 **报告其他版本的 Windows**，并选择 Windows 10 或以上版本。
   3. 运行安装程序以完成 Python 安装。
3. **配置启动方式**：
   1. 将 Python 软件目录下的 `python.exe` 与 `pythonw.exe` 添加到 VxKex NEXT 的应用程序列表。
   2. 在 Python ZIP 应用的属性窗口中，将打开方式修改为 Python 软件目录中 `pythonw.exe`。

> [!NOTE]
>
> 您可能无法使用 Python 启动器来启动本应用，因为 Python 启动器找不到任何 Python 版本。

[pythonvista_repository_github]: https://github.com/adang1345/PythonVista
[vxkex-next_release_github]: https://github.com/YuZhouRen86/VxKex-NEXT/releases/latest

[badge_windows_7]: https://img.shields.io/badge/Windows-7-0078D4?logo=windows
[badge_windows_8]: https://img.shields.io/badge/Windows-8-7200AC?logo=windows
