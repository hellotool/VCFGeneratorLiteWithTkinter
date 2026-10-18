# 0009 测试矩阵按平台分层并在 Linux 上启用 Xvfb

- 状态: 已采纳
- 日期: 2026-10-17

## 背景

`tests/ui/windows/main_window/test_layout_keys.py` 是首批依赖真实控件的测试：它用假监听器驱动
`MainLayout`，靠 `event_generate` 派发按键。实测约束有三条。其一，按键事件只在窗口已映射时派发，
`withdraw()` 的根窗口上 `event_generate("<Return>")` 连 Text 类绑定的插入换行都不会执行，因此无图形
环境的作业里这些测试无法真正跑到。其二，同一线程内"每个用例建销一个根窗口"叠加 pytest 默认的
`--capture=fd` 会偶发 `TclError: Can't find a usable init.tcl`（同一进程内该文件可读）；会话级共用单个
根窗口时 3 轮全绿，改为每用例建根窗口时 3 轮均报错，改用 `--capture=sys` 后两种形状都全绿，说明需要
两个条件同时成立。其三，作业数量有成本差异：macOS runner 的分钟计费高于 Linux 与 Windows，而
`test.yml` 原本只在 `ubuntu-latest` 上跑 `["3.12", "3.13", "3.14t"]` 三个版本，Windows 与 macOS 完全不跑
测试（`build.yml` 只在 `windows-latest` 与 `ubuntu-latest` 构建产物）。

## 决策

`test.yml` 的矩阵改为 `os × python-version`：Linux 全测三个版本，Windows 与 macOS 只测最老与最新两个
版本（用 `exclude` 排除 `3.13`），并设 `fail-fast: false`，作业数由 3 增至 7。GUI 测试的图形环境用
Xvfb 解决：测试步骤在 `RUNNER_OS` 为 Linux 时先确认 `Xvfb` 是否存在、缺失才 `apt-get install`，随后用
`xvfb-run -a` 包裹既有的 `poe test`；Windows 与 macOS 直接跑，不改命令。

不改动 pytest 的全局捕获模式，也不给 GUI 测试加 marker 或独立任务：根窗口保持会话作用域即可避开上述
交互，该约束连同 2×2 实测结果写在 fixture 的文档串里。不在 CI 里做打包产物的 GUI 冒烟，不引入
`macos-13` 等更早的 runner 镜像。

## 后果

收益是 GUI 测试在 Linux 上真跑而不是静默跳过，并且控件路径语义（Enter 在输入框内换行、组合键提交、
焦点在编辑区子树内不提交）首次进入回归门禁；Windows 与 macOS 的 GUI 路径也进入常态验证，而这正是
本次快捷键改动的主战场。

代价与缺口如下。Windows 与 macOS 上 `3.13` 不被覆盖，属刻意的成本取舍，跨版本回归只能靠 Linux 与本地
兜住。macOS runner 计费倍率使分钟成本上升，且 macOS 上 `--capture=fd` 与 Tk 的交互未实测，若将来有人把
根窗口改成用例级隔离，需按 fixture 文档串改用 `--capture=sys`。三平台随附的 Tcl/Tk 版本不同（本地为
8.6.15），断言只依赖按键派发与控件路径语义，不依赖具体 Tk 版本号。无图形环境的 Linux 作业仍会把这批
测试按"缺少图形显示"跳过，判定条件已收窄到只认 `no display name` 与 `couldn't connect to display`，
其余 `TclError` 一律抛出而不是咽成跳过。Gitee 侧未配置等价流水线，测试仍只在 GitHub Actions 上执行。
