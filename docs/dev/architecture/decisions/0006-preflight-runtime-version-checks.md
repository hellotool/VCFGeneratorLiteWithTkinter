# 0006 启动阶段前置校验运行时版本

- 状态: 已采纳
- 日期: 2026-10-11

## 背景

应用运行时依赖两个外部版本：解释器本身，以及 Tkinter 背后的 Tcl/Tk。改动前两者都不校验：

- `pyproject.toml:9` 声明 `requires-python = ">=3.12"`，但这只在安装期由包管理器生效，运行时不做判断，用低版本解释器直接启动时行为未定义。
- 旧 `bootstrap.py` 在模块顶层 `import tkinter.messagebox` 并 `from tkinter.messagebox import Message`。Tcl/Tk 缺失时，异常发生在 `main()` 中的 `from vcf_generator_lite.bootstrap import ...` 这一行，此时 `setup_excepthook()` 尚未执行，用户看不到任何应用内提示；Tcl/Tk 版本过低时同样没有拦截点，故障要到窗口创建后才以难以定位的形式暴露。

约束来自国际化机制：`setup_l10n()` 猴子补丁替换全局 `gettext` 的函数，且 `bootstrap.py`、`__main__.py` 禁止在顶层导入依赖 gettext 的模块（见 [i18n-mechanism.md][ref-i18n-mechanism]）。因此每个校验点都要单独回答"它排在 `setup_l10n()` 之前还是之后"，而先后直接决定该提示能否翻译——这是本决策的主要权衡。

另一侧的力量是打包形态：`packaging/pyinstaller/vcf_generator_lite.spec:49` 为 `console=False`，产物没有标准流可用。

## 决策

新增 `require_python()` 与 `require_tkinter()` 两个前置校验，失败即向 stderr 打印一行提示并 `sys.exit(1)`，不弹对话框、不尝试降级运行。要点：

- 阈值集中在 `constants.py`：`PYTHON_VERSION_MINIMUM = (3, 12)`、`TK_VERSION_MINIMUM = (8, 6)`，校验函数只引用常量，不在函数内硬编码。
- 调用顺序固定为 `require_python()` → `setup_l10n()` → `require_tkinter()` → `setup_excepthook()`（`__main__.py:54-58`）。
- 接受由此产生的翻译不对称：`require_python()` 必须排在补丁之前，其提示用 f-string 直出、不翻译；`require_tkinter()` 排在补丁之后，两条提示走 `pgettext`（上下文 `startup.tcltk_*`）。
- 把 `tkinter` 的导入从 `bootstrap.py` 顶层下沉到函数内，使校验有机会先于导入失败运行；顶层只保留 `TYPE_CHECKING` 块中的类型导入。
- `TkVersion` 是 float，用 `math.modf` 拆成主次版本再比较，避免 8.10 被读作 8.1。

## 后果

- 收益：解释器与 Tcl/Tk 的问题在启动最早期收敛为一行可读提示；`bootstrap.py` 不再因顶层导入第三方 GUI 模块而把校验点挤到异常之后；Tcl/Tk 的两条提示可翻译并已入 `zh_CN` 目录。
- 代价：新增校验自身受 `i18n-mechanism.md` 的导入时序约束。启动路径上共四处 `print`（`bootstrap.py:61`、`115`、`135`、`148`），只有 `115` 这条 Python 版本提示不翻译，因为它是唯一排在补丁之前的用户可见输出；代码里没有把这层时序关系写成注释，容易被后人"顺手补上 pgettext"而重新引入未打补丁时的调用。
- 缺口（已知，未修）：`console=False` 的产物里 `sys.stdout` / `sys.stderr` 均为 `None`，实测 `print(..., file=sys.stderr)` 不抛异常、内容静默丢弃，因此三条版本提示在打包产物上都不可见，用户只会看到应用没有启动。
- 该缺口不能靠 `stdio_msgbox_if_needed` 兜住：这个上下文自身依赖它要验证的前提——函数体第一句即 `from tkinter.messagebox import OK, Message`（`bootstrap.py:91`），tkinter 缺失时连上下文都进不去；其 `app_name` 入参来自 `app_text.py:1` 顶部 `from gettext import pgettext` 与 `app_text.py:7` 的调用，要求补丁已经生效。换言之 `require_*` 的职责正是判定这两个前提是否成立，把判定放进依赖前提的通道里构成循环。可用通道只剩不依赖 tkinter 与 gettext 的两类：Windows 下纯标准库的 `ctypes.windll.user32.MessageBoxW`（代价是提示无法翻译），以及项目既有的错误日志文件路径。属后续独立改动，实施时另写一篇决策。
- 限制：`math.modf` 的拆分假设次版本小于 10（代码注释已记录）；`TK_VERSION_MINIMUM = (8, 6)` 的具体取值依据在项目内没有文档留痕，本 ADR 也不代为论证，后续如需调整应另写一篇说明。
- 隐性依赖：`require_python()` 能否在低版本解释器上跑到，取决于它之前的导入链是否兼容。按代码走读，`__main__.py:1-2` 与 `bootstrap.py:1-9` 只导入标准库且不含 3.12 专属语法，故判断成立；此处未在旧解释器上实测。若今后有人把带新版本语法的模块提到 `bootstrap.py` 顶层，`require_python()` 会在导入阶段就被绕过，这条保护静默失效且没有任何测试能发现。

[ref-i18n-mechanism]: ../../globalization/i18n-mechanism.md
