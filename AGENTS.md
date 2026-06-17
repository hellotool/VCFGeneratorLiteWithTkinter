# AGENTS.md

## 简介

本项目使用 uv 进行管理，使用 Poe the Poet 进行任务管理。

任何操作都不应修改系统环境。例如，不应安装全局包。

## 技术栈

- 开发语言：Python 3.12+
- UI 框架：Tkinter
- 包管理器：uv
- 任务运行器：Poe the Poet
- 国际化：gettext
- 代码质量：
  - 测试工具：pytest
  - 格式化工具：Ruff
  - 代码检查：Ruff、Pyright

## 设置命令

- 安装依赖：`uv sync`
- 运行测试：`uv run poe test`
- 格式化代码：`uv run poe format`
- 检查代码：`uv run poe check`
- 修复代码：`uv run poe fix`

## 构建命令

- 构建安装程序：`uv run poe build-installer`
  - `--force`：强制重建上游输出（PyInstaller 分发包）。
  - `--force-download`：强制联网下载 InnoSetup 扩展。
  - `--no-verify-ssl`：下载时跳过 SSL 验证。
- 构建便携包：`uv run poe build-portable`
  - `--force`：强制重建上游输出（PyInstaller 分发包）。
- 构建 ZIP 应用：`uv run poe build-zipapp`
  - `--force`：强制重建上游输出（Wheel）。
- 构建 Wheel：`uv run poe build-wheel`

## 项目结构

```txt
VCFGeneratorLiteWithTkinter/
├── assets/                         # 项目资源
├── dist/                           # 发布产物
├── scripts/                        # 项目脚本
├── packaging/                      # 打包配置
│   ├── innosetup/                  # InnoSetup 配置
│   └── pyinstaller/                # PyInstaller 配置
├── src/vcf_generator_lite          # 源代码
│   ├── core/                       # 业务逻辑
│   ├── models                      # 数据模型
│   ├── resources/                  # 静态资源（图标、数据等）
│   ├── ui/
│   │   ├── actions/                # 通用工具
│   │   ├── layouts/                # 通用布局
│   │   ├── themes/                 # 应用主题
│   │   ├── widgets/                # 自定义组件（增强型输入框等）
│   │   └── windows/                # 窗口
│   ├── utils/                      # 工具类
│   ├── __main__.py                 # 程序入口
│   └── constants.py                # 全局常量（名称、链接等）
├── tests/                          # 测试文件
└── pyproject.toml                  # 项目配置
```

## 代码风格

- 使用 Python 3.12 及以下语法。
- Ruff 检查器，严格类型检查。
- 行长度：120 字符
- 无返回值的函数不添加不必要的类型注解。
- 文档字符串使用 reStructuredText 规范。

## 文档风格

- 所有外部链接都要使用放置到底部引用。
- 用户文档（`docs/`）按 [Diátaxis](https://diataxis.fr/) 框架组织为四类：入门教程（Tutorials）、操作指南（How-to guides）、技术参考（Reference）、原理解析（Explanation）。
- 开发者文档（`docs/dev/`）按开发生命周期组织：开始 → 开发 → 架构与设计 → 发布。

## 更多信息

有关视觉设计、版本管理和构建指南的信息，请参阅 `docs/dev` 目录。

## 规则

- 在完成代码修改后，**请勿提交到版本控制**！
- 代码生成后必须使用 `uv run poe format` 格式化代码。
- 代码生成后必须使用 `uv run poe check` 检查代码。
- 每个文件结尾必须添加空行。
- 可翻译字符串必须使用带上下文的 `pgettext`（或 `pgettext_menu_label` / `LazyPgettext`），禁止使用 `_` / `gettext` 等无上下文的调用。
