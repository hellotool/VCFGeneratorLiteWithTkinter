# 0005 按 lint / check / fix 语义重组校验任务

- 状态: 已采纳，取代 [0004](./0004-rename-precommit-to-ensure-quality.md)
- 日期: 2026-10-07

## 背景

[0004][ref-0004] 将聚合任务定为 `ensure-quality` = `format → check → test`。落地一段时间后，该组任务名暴露出三个问题。

其一，`check` 名不副实。它只跑 `ruff check` + `pyright` + `rumdl check`，即静态检查；而"文件是否符合格式"这一半没有任何只读入口——`format` 只负责写，想验证格式只能手写 `ruff format --check`。同生态的工具都把这两件事合在一个动词下：Vite 的 `vp check` 一次跑完 format、lint 与类型检查（[vp check][ref-vp-check]），rstack 的 `rs check` 默认为 `rs lint` 后再 `rs fmt --check`，写操作只在 `--fix` 时发生（`rs check --fix` 等同 `rs lint --fix && rs fmt --write`，[rs check][ref-rs-check]）。

其二，顺序并不成立。`ensure-quality` 用 `parallel` 定义，`uv run poe --dry-run ensure-quality` 平铺出 6 条叶子命令并发执行，因此文档里的 `format → check → test` 只是叙述：`ruff check` 可能在 `ruff format` 改写同一批文件的同时读取它们。

其三，`fix` 这个名字被占用在一个窄命令（`ruff check --fix`）上，而真正的"修复并验证"入口叫 `ensure-quality`，两者语义重叠却分属两名。

## 决策

按"裸动词等于工具自身的默认行为"重组 `poe_tasks.toml`：

- `lint` = `ruff check` + `pyright` + `rumdl check`，承接原 `check` 的职责（只读，因为 `ruff check` 默认只读）。
- `lint-fix` = `ruff check --fix`，即原 `fix` 的窄能力。
- `format` = `ruff format` + `rumdl fmt`，名称与写文件行为均不变（因为 `ruff format` 默认就写）。
- `format-check` = `ruff format --check` + `rumdl fmt --check`，补上此前缺失的只读格式检查。
- `check` = `format-check` + `lint`，全部只读，可安全用于 CI 与钩子。
- `fix` = `lint-fix → format → check`，改用 `sequence` 声明，顺序真实生效；它取代 `ensure-quality`。
- 后缀只标出"默认的反面"，所以是 `lint-fix` 与 `format-check` 两个不对称的名字，而不是对称的 `-fix` / `-check` 两套；这样没有任何一个命令名与实际行为相反。
- **`fix` 不含 `test`**：聚合任务只覆盖静态质量，测试保持为独立的 `poe test`。
- 文档中的本地校验由单条 `ensure-quality` 拆回 `poe fix` + `poe test` 两条。
- 不做：不实现 `poe check --fix` 这类带开关的单命令形态（原因见后果）。

## 后果

- 收益：只读与写操作的分界清晰，`check` 失败可安全地当作门禁而不用担心它改动文件；`fix` 的三步顺序由 `sequence` 保证，消除了并发读写同一文件的竞争；命名与 Vite / rstack 等工具的 `check` 语义一致，降低跨项目的心智负担。
- 代价：任务总数由 14 增至 16，[0003][ref-0003] 记录的"14 个任务"成为历史数字；原 `fix`（`ruff check --fix`）更名为 `lint-fix`，`AGENTS.md`、双语 `CONTRIBUTING`、`docs/dev/getting-started.md`、发布流程、号码检测器指南与两个技能文档的旧引用需一次性同步。
- 限制：poe 0.48 做不到 rs / vp 的**命令形态**。已声明的布尔参数不会展开成命令行开关（`${fix}` 求值为 `True` 或空串，见 `poethepoet/env/task_env.py` 的 `register_task_args`），`switch` 任务在本机版本上直接抛 `AssertionError`（`poethepoet/task/base.py:76`），故 `poe check --fix` 这类"同一动词两态"无法声明式表达，只能一个态一个任务名；能对齐的是**语义**，不是命令行外观。
- 备选：`sequence` / `parallel` 的条目支持内联原始命令与任务名混排（`[{cmd = "ruff check --fix"}, "format", "check"]`，已用 `--dry-run` 验证展开正确），因此本可去掉 `format-check` 与 `lint-fix` 两个名字、把命令直接内联，任务数回到 14。保留它们是为了留住"只查格式而不改文件""只修 lint 而不动格式"两个窄入口，前者对应 `rs fmt --check`，后者可避免格式化噪声混进 diff。
- 缺口：`test` 不再被任何聚合任务覆盖，`poe fix` 通过不代表测试通过，需靠文档中"两条命令都跑"约束；CI（`.github/workflows/test.yml`）仍只跑 `poe test`，lint 与格式检查在远端依旧无人值守。与 [0002][ref-0002] 起记录的缺口同源，后续可在 CI 增补 `uv run poe check` 一并消除。

[ref-0002]: ./0002-local-precommit-as-verification-contract.md
[ref-0003]: ./0003-poe-tasks-in-dedicated-file.md
[ref-0004]: ./0004-rename-precommit-to-ensure-quality.md
[ref-vp-check]: https://viteplus.dev/guide/check
[ref-rs-check]: https://rstack.rs/zh/guide/cli/check
