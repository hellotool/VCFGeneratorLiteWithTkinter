# 0003 Poe Tasks Defined in a Dedicated File

- 状态: 已采纳
- 日期: 2026-09-06

## 背景

迁移前 `pyproject.toml` 共 158 行，其中第 45–149 行（约三分之二篇幅）是 poe 任务定义。

14 个任务中 8 个是 `script` 类型，逻辑本体已在 `scripts/` 下 12 个 Python 文件（678 行）中；剩下 6 个是薄声明，全部无 shell 语法。

项目是 src-layout 的 GUI 应用（`[project.gui-scripts]`），不是会被其他包依赖的库。

曾评估过的另一条路：poe 的 packaged tasks（`include_script` + `poethepoet_tasks`），即在 Python 代码里定义任务。

## 决策

任务定义从 `pyproject.toml` 迁至根目录独立文件 `poe_tasks.toml`，`pyproject.toml` 仅保留 `executor` 与 `include` 指针：

```toml
[tool.poe]
executor = "uv"
include = "poe_tasks.toml"
```

`poe_tasks.toml` 内使用不带 `tool.poe` 命名空间的 `[tasks.X]` / `[[tasks.X.args]]` 形式承载全部 14 个任务。已验证 `uv --no-config run poe` 列出的任务名与 help 与迁移前逐字一致，跨任务引用（precommit 并行引用 format/check/test）与 args 解析均正常。

选择 `include` 而非"完全改用独立 `poe_tasks.toml`（删掉 `pyproject.toml` 里的 `[tool.poe]`）"：

- poe 的配置查找顺序是 `pyproject.toml` → `poe_tasks.toml`，且二者不合并——只要 `pyproject.toml` 里存在 `[tool.poe]`，就不会再读 `poe_tasks.toml`。若完全删掉 `[tool.poe]`，`pyproject.toml` 里将不留任何痕迹，新贡献者更难发现任务在哪；保留 include 指针则兼具分离与可发现性。
- 保留在 `pyproject.toml` 的 `executor = "uv"` 依然生效。

否决 packaged tasks（代码内定义任务）：

- 新增 dev 依赖 `poethepoet_tasks`；
- 要求模块可被 import，本项目 src 布局 + uv 下根目录模块不在 `sys.path`，路径要额外处理；
- 每次调用乃至 shell tab 补全都需另起 Python 子进程 import 求值；
- 生成函数被要求不得向 stdout 输出、须避免副作用；
- 其核心收益（跨项目复用、按 tag 选子集、动态生成配置）在本项目无消费方——本项目不是会被依赖的库；
- 而"把逻辑放进 Python 代码"这个诉求，现有 8 个 `script` 任务早已满足。

## 后果

- 收益：`pyproject.toml` 回归单一职责（打包与依赖）；任务文件可自由加注释与分组；任务数量增长不再撑大 `pyproject.toml`；纯声明式，零新增依赖、零 import 副作用、零补全性能损耗。
- 代价 / 限制：多一个根目录文件；贡献者需要知道任务定义在 `poe_tasks.toml`（已通过在 `pyproject.toml` 留 include 指针 + 同步 `AGENTS.md` 与架构 overview 文档缓解）；需要 poe ≥ 0.12.0（项目锁定 0.46.0，满足）。
- 需注意的行为：poe 的 include 冲突规则是"已存在项优先，被 include 的值被忽略（不报错）"，因此在 `pyproject.toml` 里重复定义同名任务会静默失效（见 Poe 配置文档 [poe-config]）。
- 缺口：任务定义与 `scripts/` 下的脚本目前均无测试覆盖。
- 重新评估的触发条件：若将来需要把这套任务抽成共享包供多个项目复用，再考虑改用 `include_script`（packaged tasks）。

[poe-config]: https://poethepoet.natn.io/config/index.html
