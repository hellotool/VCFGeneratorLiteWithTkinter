# AGENTS.md

## Introduction

This project uses uv for management and Poe the poet for task management.

No operation should modify the system environment. For example, no global packages should be installed.

## Tech Stack

- Development Language: Python 3.12+
- UI Framework: Tkinter
- Package Manager: uv
- Task Runner: Poe the Poet
- Internationalization: gettext
- Code Quality:
  - Testing Tool: pytest
  - Formatter: Ruff
  - Linters: Ruff, Pyright

## Setup Commands

- Install dependencies: `uv sync`
- Run tests: `uv run poe test`
- Format code: `uv run poe format`
- Check code: `uv run poe check`
- Fix code: `uv run poe fix`

## Build Commands

- Build installer: `uv run poe build-installer`
- Build portable: `uv run poe build-portable`
- Build zipapp: `uv run poe build-zipapp`
- Build wheel: `uv run poe build-wheel`

### Localization Commands

- Extract: `uv run poe l10n-extract`
- Compile: `uv run poe l10n-compile`
- Initialize: `uv run poe l10n-init`
- Update: `uv run poe l10n-update`

## Project Structure

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
├── pyproject.toml                  # 项目配置
└── os-notices.toml                 # 开源声明信息
```

## Code Style

- Python 3.12+
- Ruff linter with strict type checking
- Line length: 120 characters
- No unnecessary type annotations for None returns

## More Information

For information on visual design, version management, and build guides, please refer to the `docs/dev` directory.
