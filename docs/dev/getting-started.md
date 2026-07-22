# 快速上手

本文介绍如何搭建开发环境并开始参与项目开发。

## 技术栈

| 类别       | 技术                                       | 版本要求                        |
| ---------- | ------------------------------------------ | ------------------------------- |
| 语言环境   | Python                                     | 3.12+                           |
| UI 框架    | Tkinter                                    | Python 标准库                   |
| 包管理     | uv                                         | 0.10.1+                         |
| 版本控制   | Git                                        | 任意版本                        |
| IDE        | Visual Studio Code 或 PyCharm              | PyCharm 2026.1+（如使用）       |
| 任务运行器 | Poe the Poet                               | 0.46.0+                         |
| 国际化     | gettext                                    | -                               |
| 测试       | pytest                                     | 9.0.3+                          |
| 代码质量   | Ruff（格式化 + 检查）、Pyright（类型检查） | Ruff 0.15.13+、Pyright 1.1.409+ |
| 构建       | PyInstaller、InnoSetup、zipapp             | PyInstaller 6.20.0+             |

## 项目结构

详见 [项目概览](./architecture/overview.md)。

## 前置要求

在开始之前，请确保您的系统已安装以下工具：

| 类别     | 工具                          |
| -------- | ----------------------------- |
| 语言环境 | Python                        |
| 版本控制 | Git                           |
| 包管理   | uv                            |
| IDE      | Visual Studio Code 或 PyCharm |

## 获取源码

```bash
# 克隆仓库
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

该命令会创建虚拟环境并安装所有必需的开发依赖，包括：

- poethepoet（任务运行器）
- pyright（类型检查）
- ruff（代码检查和格式化）
- pytest（测试框架）
- babel（国际化）
- pyinstaller（构建工具）

## 常用命令

项目使用 Poe the Poet 作为任务运行器，常用命令如下：

| 命令                | 说明                       |
| ------------------- | -------------------------- |
| `uv run poe test`   | 运行测试                   |
| `uv run poe format` | 格式化代码（Ruff）         |
| `uv run poe check`  | 检查代码（Ruff + Pyright） |
| `uv run poe fix`    | 自动修复代码问题           |

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
