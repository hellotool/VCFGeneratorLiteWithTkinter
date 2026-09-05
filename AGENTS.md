# 智能体指引

## 概览

VCF 生成器 轻量版 是一个轻量级 vCard 文件生成器，用户提供的联系人表格后可通过本工具生成 vCard 文件。

## 技术栈

本项目使用 uv 进行管理，使用 Poe the Poet 进行任务管理。

- 语言环境：Python 3.12+
- UI 框架：Tkinter
- 包管理器：uv
- 任务运行器：Poe the Poet
- 国际化：gettext
- 代码质量：
  - 测试工具：pytest
  - 格式化工具：Ruff
  - 代码检查：Ruff、Pyright
- 文档质量：rumdl

## 设置命令

- 安装依赖：`uv sync`
- 运行测试：`uv run poe test`
- 格式化代码与文档：`uv run poe format`（代码 `ruff format` + 文档 `rumdl fmt .`）
- 检查代码与文档：`uv run poe check`（`ruff check` + `pyright` + `rumdl check`，规则见根目录 `rumdl.toml`）
- 修复代码：`uv run poe fix`
- 本地校验：`uv run poe precommit`（`format` + `check` + `test`）

## 文件组织

- `VCFGeneratorLiteWithTkinter/`
  - `assets/` — 项目资源
  - `dist/` — 发布产物
  - `scripts/` — 项目脚本
  - `packaging/` — 打包配置
    - `innosetup/` — InnoSetup 配置
    - `pyinstaller/` — PyInstaller 配置
  - `src/vcf_generator_lite` — 源代码
    - `core/` — 业务逻辑
    - `models/` — 数据模型
    - `configs/` — 配置（如号码检测器）
    - `resources/` — 静态资源（图标、数据等）
    - `ui/`
      - `actions/` — 通用操作
      - `layouts/` — 通用布局
      - `themes/` — 应用主题
      - `widgets/` — 自定义组件（增强型输入框等）
      - `windows/` — 窗口
    - `utils/` — 通用工具
    - `__main__.py` — 程序入口
    - `constants.py` — 全局常量（名称、链接等）
  - `tests/` — 测试文件
  - `docs/` — 用户文档
    - `dev/` — 开发文档
      - `architecture/decisions/` — 架构决策记录
        - `index.md` — 架构决策记录清单与规则
        - `_template.md` — 架构决策记录模板
  - `pyproject.toml` — 项目配置

## 规则

### 决策变更

- 涉及结构性或工具选型改动前，**必须**阅读相关决策了解决策来由，避免重拾已淘汰方案。
- 若改动引入了新的带权衡的决策，或推翻了既有的已采纳 ADR，**必须**新增对应 ADR。
- 变更既有决策时写新 ADR 将其标记为“已取代”，**禁止**改写旧文件。
- 新增或推翻 ADR 后，**必须**在决策清单中同步添加或更新一条记录。

### 文档编写

- **必须**使用 UTF-8 编码。
- 所有外部链接**必须**在文档末尾以参考链接的形式定义，格式为 `[标识]: URL`。示例：
  - 正文中引用：`[Example Homepage][example-homepage]`
  - 文档结尾：`[example-homepage]: https://example.com/`

### 代码编写

- 文件**必须**以换行符结尾。
- 代码行长度**应该**少于 120 字符。
- 无特殊情况时，**必须**使用 UTF-8 编码。
- 可翻译字符串**必须**使用带上下文的 gettext 函数或占位类（例如 `pgettext`、`pgettext_menu_label`、 `LazyPgettext`），**禁止**使用 `_` 或 `gettext` 等无上下文的调用。
- 编写 UI 相关代码时，**必须**阅读相关设计与架构文档。

#### 编写 Python 代码

- 文档字符串**必须**使用 reStructuredText 格式。
- **必须**遵循 PEP 8 规范。
- 无返回值函数**禁止**添加返回类型注解。
- **必须**为仅在新版 Python 可用的 API 添加 Python 版本判断或属性检查。
- **必须**使用 Python 3.12 兼容的语法

#### 编写 PowerShell 脚本

- **必须**使用 UTF-8 BOM 编码。

### 工具验证

- **必须**本地跑通 `uv run poe precommit`。

### 其他

- 无用户明确要求时，**禁止**将任何修改提交到版本控制。
- 无用户明确同意时，**禁止**执行修改系统全局环境的操作（例如：安装全局包）。
