# 开发指南

## 技术栈

- **IDE**: [Visual Studio Code][vscode-homepage] 或者 [PyCharm 2026.1+][pycharm-homepage]
- **开发语言**: [Python 3.12+][python-homepage]
- **UI 框架**: [Tkinter][tkinter-homepage]
- **包管理工具**: [uv][uv-homepage]
- **任务运行器**: [Poe the Poet][poethepoet-homepage]
- **国际化**：[gettext][python-docs-gettext]
- **代码质量**:
  - **测试工具**: [pytest][pytest-homepage]
  - **格式化工具**: [Ruff][ruff-formatter-homepage]
  - **代码检查工具**: [Ruff][ruff-linter-homepage]、[Pyright][pyright-homepage]
- **构建工具**:
  - **创建可执行文件**：[PyInstaller][pyinstaller-homepage]
  - **体积优化工具**：[UPX][upx-homepage]
  - **创建安装程序（仅 Windows 平台）**：[InnoSetup 6.7+][innosetup-homepage]
  - **创建 ZIP 应用**：[zipapp][python-docs-zipapp]（Python 标准库）

## 环境搭建

### 前置要求

1. 安装 [Python 3.12+][python-homepage]（需包含 Tkinter 支持）
2. 安装 [uv][uv-installation]

### 安装依赖

```bash
uv sync
```

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

## 常用命令

| 命令                                 | 描述                           |
| ------------------------------------ | ------------------------------ |
| `uv run vcf-generator-lite`          | 运行应用                       |
| `uv run poe test`                    | 测试应用                       |
| `uv run poe format`                  | 格式化代码                     |
| `uv run poe check`                   | 检查代码                       |
| `uv version`                         | 查看当前版本                   |
| `uv version 1.2.3`                   | 更新版本号为 `1.2.3`           |
| `uv version --bump patch --bump dev` | 更新补丁版本，并更新为开发版本 |
| `uv version --bump stable`           | 更新为稳定版本                 |

要查看更多命令，请运行 `uv --help` 与 `uv run poe --help`。

## 相关文档

- [视觉设计](./visual.md)
- [构建指南](./building.md)
- [版本管理规范](./versioning.md)

[vscode-homepage]: https://code.visualstudio.com/
[pycharm-homepage]: https://www.jetbrains.com/zh-cn/pycharm/
[python-homepage]: https://www.python.org/
[uv-homepage]: https://docs.astral.sh/uv/
[uv-installation]: https://docs.astral.sh/uv/getting-started/installation/
[tkinter-homepage]: https://docs.python.org/zh-cn/3/library/tk.html
[pytest-homepage]: https://docs.pytest.org/en/stable/
[ruff-formatter-homepage]: https://docs.astral.sh/ruff/formatter/
[ruff-linter-homepage]: https://docs.astral.sh/ruff/linter/
[pyright-homepage]: https://microsoft.github.io/pyright/
[pyinstaller-homepage]: https://pyinstaller.org/en/stable/
[upx-homepage]: https://upx.github.io/
[innosetup-homepage]: https://jrsoftware.org/isinfo.php
[poethepoet-homepage]: https://poethepoet.natn.io/
[python-docs-zipapp]: https://docs.python.org/zh-cn/3/library/zipapp.html
[python-docs-gettext]: https://docs.python.org/zh-cn/3/library/gettext.html
