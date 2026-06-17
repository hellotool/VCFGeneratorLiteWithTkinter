# 快速开始

本文介绍如何获取、安装 VCF 生成器 Lite，并生成您的第一个 vCard 文件。

## 获取应用

通过以下渠道下载软件包：

- [Gitee 发行版][release-gitee] — 推荐中国大陆用户使用
- [GitHub Releases][release-github]

### 选择软件包

根据您的系统环境选择合适的软件包：

| 平台    | 软件包类型      | 需要安装 | 文件                                                      |
| ------- | --------------- | -------- | --------------------------------------------------------- |
| Windows | 安装程序        | 是       | VCFGeneratorLite-v\<应用版本\>-**win-amd64**-setup.exe    |
| Windows | 便携包          | 否       | VCFGeneratorLite-v\<应用版本\>-**win-amd64**-portable.zip |
| 跨平台  | Python Wheel    | 可选     | vcf_generator_lite-\<应用版本\>-**py3-none-any**.whl      |
| 跨平台  | Python ZIP 应用 | 否       | VCFGeneratorLite-v\<应用版本\>-**py3**.pyzw               |

> [!TIP]
>
> 请查阅 [兼容性](./reference/compatibility.md) 了解系统要求。

## 安装与启动

### Windows 安装程序

双击 `.exe` 文件，按提示完成安装后，从开始菜单启动应用。

### Windows 便携包

解压 `.zip` 文件后，双击 `vcf_generator_lite.exe` 即可运行。

### Python Wheel

您可以直接使用以下命令运行应用：

```bash
uvx <whl 文件路径>
```

> [!NOTE]
>
> `uvx` 是 [uv][uv-website] 工具提供的命令，会自动创建临时环境并运行程序。

您也可以选择安装应用到系统环境：

```bash
# 使用 pipx
pipx install <whl 文件路径>

# 或使用 uv
uv tool install <whl 文件路径>
```

安装完成后，在终端执行 `vcf-generator-lite` 启动应用。

### Python ZIP 应用

双击 `.pyzw` 文件即可运行（需要 Python 3.12 及以上版本）。

在 Windows 中双击启动需要安装 [Python 安装管理器][pymanager-docs]（推荐）或 [Python 启动器][pylauncher-docs]。

## 生成第一个 vCard

1. 启动应用，进入主窗口。
2. 按 `姓名 电话 备注` 的格式，将联系人复制到文本框中（每行一个联系人）。详见 [输入格式规范](./reference/input-format.md)：
   ```text
   屈原	13333333333	战国时期诗人
   曹操	13444444444
   陶渊明	13555555555
   谢灵运	13666666666
   ```
3. 点击 **开始生成** 按钮，选择保存路径。
4. 等待生成完成。如有无法识别的条目，应用会弹出无效条目窗口提示您修正。
5. 将生成的 `.vcf` 文件传输到目标设备或服务。

## 后续步骤

- 学习 [使用 vCard 文件](./guides/vcard-usage.md)，将生成的文件导入到各类设备和服务。
- 阅读 [用户指南](./guides/index.md) 了解完整功能。
- 遇到问题时查阅 [常见问题](./troubleshooting/faq.md)。

[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest

[uv-website]: https://docs.astral.sh/uv/

[pymanager-docs]: https://docs.python.org/zh-cn/3.14/using/windows.html#python-install-manager
[pylauncher-docs]: https://docs.python.org/zh-cn/3.14/using/windows.html#python-launcher-for-windows-deprecated
