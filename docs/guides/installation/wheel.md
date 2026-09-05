# Python Wheel

适用于已安装 Python 的用户，支持跨平台使用。

**文件**：`vcf_generator_lite-<应用版本>-py3-none-any.whl`

您可以从 [Gitee 发行版][release-gitee] 或 [GitHub Releases][release-github] 下载。

**前置条件**：

- [Python 3.12 及以上版本](#安装-python)
- [uv][uv-website]（推荐）或 [pipx][pipx-website]

## 安装 Python

请参考 Python 官方安装指南安装 Python 3.12 及以上版本：

- [Windows][python-guide-windows]
- [Linux][python-guide-unix]
- [macOS][python-guide-macos]

Windows 用户推荐通过 [Python 安装管理器][pymanager-docs]（[Microsoft Store][msstore-python] 或官网下载）安装。如果使用遗留安装程序，请确保勾选 **Add Python to PATH**。

## 方式一：直接运行（无需安装）

使用 `uvx` 直接在临时环境中运行，适合一次性使用：

```bash
uvx <whl 文件路径>
```

> [!NOTE]
>
> `uvx` 是 [uv][uv-website] 提供的命令，会自动创建临时环境并运行程序，不会影响系统环境。

## 方式二：安装到全局环境

适合长期使用。安装后，应用将作为全局命令可用：

> [!WARNING]
>
> 请勿使用 `pip install` 直接安装。这会污染系统 Python 环境，可能与其他包产生依赖冲突。请使用以下隔离环境工具。

```bash
# 使用 pipx
pipx install <whl 文件路径>

# 或使用 uv
uv tool install <whl 文件路径>
```

### 启动

安装完成后，在终端中执行以下命令启动应用：

```bash
vcf-generator-lite
```

### 验证安装

执行以下命令确认安装成功：

```bash
vcf-generator-lite --version
```

> [!TIP]
>
> 如果终端提示找不到 `vcf-generator-lite` 命令，请检查 pipx 或 uv 的安装目录是否已添加到系统 `PATH` 环境变量中。

### 卸载

```bash
# 使用 pipx
pipx uninstall vcf-generator-lite

# 或使用 uv
uv tool uninstall vcf-generator-lite
```

[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[msstore-python]: https://apps.microsoft.com/detail/9NQ7512CXL7T
[python-guide-windows]: https://docs.python.org/zh-cn/3.14/using/windows.html
[python-guide-unix]: https://docs.python.org/zh-cn/3.14/using/unix.html
[python-guide-macos]: https://docs.python.org/zh-cn/3.14/using/mac.html
[pymanager-docs]: https://docs.python.org/zh-cn/3.14/using/windows.html#python-install-manager
[uv-website]: https://docs.astral.sh/uv/
[pipx-website]: https://pipx.pypa.io/stable/
