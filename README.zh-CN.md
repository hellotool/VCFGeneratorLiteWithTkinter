<div align="center">
<img src="./assets/images/icon.svg" width="192" height="192" alt="应用图标" />

# VCF 生成器 Lite ![使用 Tkinter](https://img.shields.io/badge/使用-Tkinter-00319C)

**仓库**：
[![Gitee 主仓库](https://img.shields.io/badge/Gitee-主仓库-C71D23?logo=gitee)][repository-gitee]
[![GitHub 副仓库](https://img.shields.io/badge/GitHub-副仓库-0969da?logo=github)][repository-github]

**平台**：
[![Windows 8.1+ (exe)](https://img.shields.io/badge/Windows_8.1+-exe-0078D4?logo=windows)][release-gitee]
[![Python 3.12+ (pyzw)](https://img.shields.io/badge/Python_3.12+-pyzw-3776AB?logo=python&logoColor=f5f5f5)][release-gitee]

**语言**：
**简体中文** |
[English](./README.md) |
<small>期待您的翻译！</small>

</div>

VCF 生成器 Lite 是一个简单高效的工具，可以将联系人列表转换为单个 vCard (`.vcf`) 文件。生成的文件可以批量导入到手机通讯录或用于其他各种用途。使用 Python 和 Tkinter 构建，提供原生桌面体验。

[![许可证](https://img.shields.io/github/license/hellotool/VCFGeneratorLiteWithTkinter?label=许可证)](./LICENSE)
[![贡献者公约](https://img.shields.io/badge/贡献者公约-2.1-4baaaa.svg)](./CODE_OF_CONDUCT.zh-CN.md)

[![GitHub - 测试](https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/workflows/test.yml/badge.svg)][workflow-test]
[![GitHub - Release](https://img.shields.io/github/v/release/hellotool/VCFGeneratorLiteWithTkinter?logo=github)][release-github]
![GitHub - Stars](https://img.shields.io/github/stars/hellotool/VCFGeneratorLiteWithTkinter?style=flat&logo=github)
[![Gitee - Stars](https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/badge/star.svg?theme=dark)][stargazers-gitee]

## 功能

- **智能解析**：按 `姓名 电话 备注` 格式批量识别联系人（备注可选），自动处理制表符和空格。
- **批量生成**：将所有联系人合并生成单个 `.vcf` 文件。
- **号码校验**：自动跳过无效号码，并快速定位错误行。
- **辅助编辑**：文本区显示行号，支持一键删除引号。

## 软件截图

<img src="./assets/images/screenshots/main_window.zh-CN.webp" width="451" alt="主窗口" />
<img src="./assets/images/screenshots/invalid_lines_window.zh-CN.webp" width="376" alt="错误行展示窗口" />

## 获取应用

### 下载软件包

您可以通过以下渠道下载软件包：

- [Gitee 发行版][release-gitee]（推荐中国大陆地区用户使用）
- [GitHub Releases][release-github]

请根据您的使用平台选择相应的软件包：

| 平台    | 软件包类型      | 需要安装 | 文件                                                       |
| ------- | --------------- | -------- | ---------------------------------------------------------- |
| Windows | 安装程序        | 是       | VCFGeneratorLite-\<应用版本\>-**win-amd64**-*setup.exe*    |
| Windows | 便携包          | 否       | VCFGeneratorLite-\<应用版本\>-**win-amd64**-*portable.zip* |
| 跨平台  | Python Wheel    | 可选     | vcf_generator_lite-\<应用版本\>-**py3-none-any**.*whl*     |
| 跨平台  | Python ZIP 应用 | 否       | VCFGeneratorLite-\<应用版本\>-**py3**.*pyzw*               |

### 使用 Python Wheel

Python Wheel (`.whl`) 文件适合熟悉命令行的用户。推荐使用隔离环境运行，避免依赖冲突。

#### 方式一：临时运行（最简单，无需安装）

使用 `uvx`，它会自动创建临时环境并运行程序。

```bash
uvx <whl文件路径>
```

> [!NOTE]
>
> `uvx` 是 `uv tool run` 的简写形式，由 [uv][uv-homepage] 工具提供。

#### 方式二：安装后使用（适合长期使用）

使用以下工具之一安装，会自动创建独立虚拟环境，不影响系统 Python。

```bash
# 使用 pipx
pipx install <whl文件路径>

# 或使用 uv
uv tool install <whl文件路径>
```

安装完成后，以后只需在终端中输入以下命令即可运行：

```bash
vcf-generator-lite
```

> [!TIP]
>
> 如果尚未安装 `uv` 或 `pipx`，请先运行 `pip install uv` 或 `pip install pipx`。

## 使用方法

1. 把名字和电话以每行 `姓名 电话 备注` 的格式复制到主界面的文本框中，其中备注可忽略。例如：
   ```text
   屈原		13333333333	战国时期诗人
   曹操		13444444444
   陶渊明	13555555555
   谢灵运	13666666666
   ```
2. 点击 **开始生成**，选择一个路径保存文件。
3. 然后就可以在需要的地方使用生成的 vCard 文件了！

> [!NOTE]
>
> - 您可以同时使用制表符和空格分割字段。
> - 程序会自动去除文本框内多余的空格。
>
> 示例：`东坡居士    苏轼   13333333333  眉州眉山人` 将会被识别为
>
> | 姓名          | 电话        | 备注       |
> | ------------- | ----------- | ---------- |
> | 东坡居士 苏轼 | 13333333333 | 眉州眉山人 |

### 使用 vCard 文件

<details>
<summary>导入到手机通讯录</summary>

1. 将 vCard 文件传输到手机。
2. 打开 vCard 文件，选择 **通讯录**，然后根据提示操作。
3. 等待导入完成。

</details>

<details>
<summary>导入到 QQ 邮箱</summary>

1. 打开新版 QQ 邮箱网站。
2. 在侧边栏中选择 **应用 > 联系人**，然后选择 **管理 > 导入联系人**。
3. 在弹出的对话框中，点击 **选择文件** 选择框，选择您的 vCard 文件。
4. 点击 **开始导入**。

</details>

<details>
<summary>导入到飞书</summary>

1. 打开飞书客户端。
2. 在侧边栏中选择 **通讯录 > 邮箱通讯录**，然后选择 **添加 > 导入联系人** 按钮。
3. 在弹出的对话框中，选择或拖入您的 vCard 文件。
4. 点击 **导入**。

</details>

## 兼容性说明

### 系统要求

| 软件包类型               | 系统环境                        |
| ------------------------ | ------------------------------- |
| Windows 安装程序、便携包 | Windows 8.1 或更高版本          |
| Python ZIP 应用          | Python 3.12 或更高版本、Tkinter |

如果您需要在 Windows 8 或更低版本中使用本应用，请参阅 [在旧版本 Windows 中运行](./docs/compatibility/runs-on-older-windows.md)。

如果您需要在 Windows 中直接双击启动 Python ZIP 应用，请安装 [Python 安装管理器][pymanager]（推荐）或者 [Python 启动器][pylauncher]。

### vCard 兼容性

- **支持 vCard 版本**：2.1
- **支持字段**：姓名、电话号码、备注
- **已知问题**：
  - **Windows 联系人**：在非 UTF-8 环境下可能出现乱码。

### 其他兼容性

| 系统环境                          | 问题                       | 说明                                                              | 规避方法                                                                                                         |
| --------------------------------- | -------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Windows 10 或更高版本             | 不支持深色模式             | Tkinter 没有内置深色主题。                                        | 使用[高对比度主题][windows-high-contrast-support]，或者使用第三方工具（如 [Rectify11][rectify11]）修改系统主题。 |
| Windows 10 或更高版本             | DPI 变化时界面变模糊       | 应用不支持启动后调节 DPI。                                        | 请避免在应用程序运行时更改 DPI。                                                                                 |
| Python 安装管理器 26.0 或更低版本 | 双击启动后会显示命令行窗口 | 不支持自动升级为窗口化的 Python 解释器。 ([python/pymanager#216]) | 将 Python 安装管理器 升级到 26.1 或更高版本，或使用 [Python 启动器][pylauncher]。                                |

## 致谢

### AI 辅助

本项目的部分内容通过 AI 辅助生成：

- **DeepSeek**：指导编码、生成代码、文档优化、语言翻译。
- **元宝**：指导编码、生成代码、语言翻译。
- **通义灵码**：补全代码、指导编码。
- **WorkBuddy**：审查代码、文档优化。
- **Trae**：生成代码、文档优化。
- **OpenCode**：文档优化。

### 开源代码

本项目使用了开源代码。详细信息请参阅 [开源声明](./docs/legal/os-notices.md)。

## 许可证

本项目以 Apache 2.0 许可证授权，详情请参阅 [LICENSE 文件](./LICENSE)。

```txt
Copyright 2023-2026 Jesse205

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 更多文档

- [贡献指南](./CONTRIBUTING.zh-CN.md)
- [开发文档](./docs/dev/index.md)
- [常见问题](./docs/faq.md)

[repository-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/
[repository-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/
[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[stargazers-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/stargazers

[workflow-test]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/workflows/test.yml

[pylauncher]: https://docs.python.org/zh-cn/3.15/using/windows.html#python-launcher-for-windows-deprecated
[pymanager]: https://docs.python.org/zh-cn/3.15/using/windows.html#python-install-manager
[windows-high-contrast-support]: https://support.microsoft.com/zh-cn/windows/%E5%9C%A8-windows-%E4%B8%AD%E6%9B%B4%E6%94%B9%E9%A2%9C%E8%89%B2%E5%AF%B9%E6%AF%94%E5%BA%A6-fedc744c-90ac-69df-aed5-c8a90125e696
[rectify11]: https://www.rectify11.com/
[uv-homepage]: https://docs.astral.sh/uv/

[python/pymanager#216]: https://github.com/python/pymanager/issues/216
