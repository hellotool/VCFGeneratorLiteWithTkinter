# 0004 将 precommit 任务更名为 ensure-quality

- 状态: 已取代（由 [0005](./0005-restructure-check-lint-fix-tasks.md) 取代），曾取代 [0002](./0002-local-precommit-as-verification-contract.md)
- 日期: 2026-09-26

## 背景

名称为 `precommit` 的 poe 任务是一条本地验证契约：`format → check → test`。但它**并不依赖** pre-commit 框架，也不由 git hook 触发，`precommit` 这个名称容易误导贡献者以为它与提交钩子有关。

在考虑替代名时，存在一组相互冲突的约束：

- 任何语义偏向"检查 / 校验 / 验证"的词（如 `fullcheck`、`verify`）都只涵盖 `check`，会漏掉 `format` 环节，均被否决。
- 需要表达"确保整体质量良好"的**目标**而非常规的单一动作；但纯名词 `quality` 与现有 `test` / `format` / `check` / `fix` 的动词式命名不一致。
- 故采用动词 + 目标组合 `ensure-quality`，兼顾语义准确与动词风格。

此外，`format + check + test` 三条命令被散落在 `CONTRIBUTING.md`、`CONTRIBUTING.zh-CN.md`、`docs/dev/release/release-process.md` 等文档中，重复维护、易漂移。CI 工作流（`test.yml` / `build.yml` / `prepare-release.yml`）仅调用独立的 `test` / `build-*` 任务，不引用 `precommit`，因此改名前 CI 不受影响。

## 决策

将 poe 任务 `precommit` 更名为 `ensure-quality`：`ensure-quality` = `format → check → test`，作为本仓库唯一的全量本地校验入口。

- 验证契约的实质（步骤、顺序、内容）不变，仅更换命令名。
- 各处文档中并列的 `format` + `check` + `test` 三条命令统一替换为单一 `uv run poe ensure-quality`。
- 同步更新 `AGENTS.md` 中的引用与架构决策记录。

## 后果

- 收益：命令名语义准确（既不暗示 git hook，也不遗漏格式化环节）；动词式命名与 `test` / `format` / `check` / `fix` 一致；贡献者一条命令即可完成全量本地校验；文档中的验证步骤由三条压缩为一条，减少漂移。
- 代价 / 限制：CLI 命令名变更，`AGENTS.md`、贡献指南、发布流程等处的旧引用需一次性同步；历史文档（如 ADR 0002、0003）保留原有 `precommit` 提及作为演进轨迹，不再回改。
- 后续：与 [0002][ref-0002] 中记录的已知缺口一致，CI 仍只跑 `test`；若之后复刻本地 `ensure-quality`（至少 `check` + `test`）至 CI，可消除"本地绿远端不知道"的盲区。

[ref-0002]: ./0002-local-precommit-as-verification-contract.md
