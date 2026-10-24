# 快速上手

本文介绍如何搭建开发环境并开始参与项目开发。

## 技术栈

| 类别       | 工具                                                                                            | 版本要求        |
| ---------- | ----------------------------------------------------------------------------------------------- | --------------- |
| 语言环境   | [Python][python-homepage]                                                                       | 3.12+           |
| UI 框架    | [Tkinter][tkinter-homepage] ([Tcl/Tk][tcl-homepage])                                            | Tcl/Tk 8.6+     |
| 包管理     | [uv][uv-homepage]                                                                               | 0.13.1+         |
| 版本控制   | [Git][git-homepage]                                                                             | -               |
| IDE        | [Visual Studio Code][vscode-homepage] 或 [PyCharm][pycharm-homepage]                            | PyCharm 2026.1+ |
| 任务运行器 | [Poe the Poet][poethepoet-homepage]                                                             | -               |
| 国际化     | [gettext][gettext-homepage]                                                                     | -               |
| 测试       | [pytest][pytest-homepage]                                                                       | -               |
| 代码质量   | [Ruff][ruff-homepage]（格式化 + 检查）、[Pyright][pyright-homepage]（类型检查）                 | -               |
| 构建       | [PyInstaller][pyinstaller-homepage]、[InnoSetup][innosetup-homepage]、[zipapp][zipapp-homepage] | -               |
| 文档质量   | [rumdl][rumdl-homepage]（格式化 + 检查）                                                        | -               |

## 项目结构

详见 [项目概览](./architecture/overview.md)。

## 前置要求

在开始之前，请确保您的系统已安装以下工具：

| 类别     | 工具                          |
| -------- | ----------------------------- |
| 语言环境 | [Python][python-homepage]       |
| 版本控制 | [Git][git-homepage]           |
| 包管理   | [uv][uv-homepage]             |
| IDE      | [Visual Studio Code][vscode-homepage] 或 [PyCharm][pycharm-homepage] |

## 获取源码

```bash
git clone https://github.com/hellotool/VCFGeneratorLiteWithTkinter.git
cd VCFGeneratorLiteWithTkinter
```

或者从 Gitee 克隆（中国大陆用户推荐）：

```bash
git clone https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter.git
cd VCFGeneratorLiteWithTkinter
```

## 安装依赖

使用 uv 安装项目依赖：

```bash
uv sync
```

该命令会创建虚拟环境并安装所有开发依赖。

## 常用命令

项目使用 Poe the Poet 作为任务运行器，常用命令如下：

| 命令                      | 说明                                          |
| ------------------------- | --------------------------------------------- |
| `uv run poe test`         | 运行测试                                      |
| `uv run poe format`       | 格式化代码与文档（改写文件）                  |
| `uv run poe format-check` | 检查格式（只读）                              |
| `uv run poe lint`         | 静态检查（Ruff + Pyright + rumdl）            |
| `uv run poe lint-fix`     | 修复可自动修复的 lint 问题（不改格式）        |
| `uv run poe check`        | 全量只读检查（`format-check` + `lint`）       |
| `uv run poe fix`          | 修复并验证（`lint-fix` → `format` → `check`） |

## 运行应用

### 开发模式

```bash
uv run python -m vcf_generator_lite
```

### 带调试输出

```bash
uv run python -m vcf_generator_lite -vv
```

## 下一步

- 阅读 [项目概览](./architecture/overview.md) 了解项目架构。

[poethepoet-homepage]: https://poethepoet.natn.io/
[pytest-homepage]: https://docs.pytest.org/en/stable/
[innosetup-homepage]: https://jrsoftware.org/isinfo.php
[pyinstaller-homepage]: https://pyinstaller.org/
[rumdl-homepage]: https://rumdl.dev/
[pyright-homepage]: https://microsoft.github.io/pyright/
[ruff-homepage]: https://docs.astral.sh/ruff/
[tcl-homepage]: https://www.tcl-lang.org/
[uv-homepage]: https://docs.astral.sh/uv/
[python-homepage]: https://www.python.org/
[git-homepage]: https://git-scm.com/
[vscode-homepage]: https://code.visualstudio.com/
[pycharm-homepage]: https://www.jetbrains.com/zh-cn/pycharm/
[gettext-homepage]: https://docs.python.org/zh-cn/3.15/library/gettext.html
[zipapp-homepage]: https://docs.python.org/zh-cn/3.15/library/zipapp.html
[tkinter-homepage]: https://docs.python.org/zh-cn/3.15/library/tkinter.html
