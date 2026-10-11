# 架构决策记录（ADR）

本目录记录本项目的架构与工具选型决策。

## 决策清单

| 编号 | 标题 | 状态 | 日期 | 摘要 |
| --- | --- | --- | --- | --- |
| [0001](./0001-markdown-lint-with-rumdl.md) | 使用 rumdl 做 Markdown 风格门禁 | 已采纳 | 2026-07-23 | 采用 rumdl，配置源 = 根目录 `rumdl.toml`，删除 `.markdownlint.yml`，链接检查不纳入 |
| [0002](./0002-local-precommit-as-verification-contract.md) | 本地 precommit 作为验证契约 | 已取代（由 [0004](./0004-rename-precommit-to-ensure-quality.md) 取代） | 2026-07-23 | `precommit`（后更名 `ensure-quality`）= `format → check → test` 为验证契约，`check` 内含 rumdl，CI 仅跑 test 为已知缺口 |
| [0003](./0003-poe-tasks-in-dedicated-file.md) | Poe 任务定义置于独立文件 | 已采纳 | 2026-09-06 | 任务定义迁至根目录 `poe_tasks.toml`，`pyproject.toml` 仅留 `executor` + `include` 指针；弃用 packaged tasks |
| [0004](./0004-rename-precommit-to-ensure-quality.md) | 将 precommit 任务更名为 ensure-quality | 已取代（由 [0005](./0005-restructure-check-lint-fix-tasks.md) 取代） | 2026-09-26 | `precommit` 更名为 `ensure-quality`，仍等于 `format → check → test`；散落的 `format + check + test` 序列统一为单个 `poe ensure-quality`；CI 不受影响 |
| [0005](./0005-restructure-check-lint-fix-tasks.md) | 按 lint / check / fix 语义重组校验任务 | 已采纳 | 2026-10-07 | 裸动词等于工具默认行为（`lint` 只读、`format` 写文件），后缀标出反面（`lint-fix`、`format-check`）；`check` = `format-check` + `lint` 全只读，`fix` = `lint-fix → format → check` 用 `sequence` 保序且不含 `test`，本地校验为 `fix` + `test` 两条 |
| [0006](./0006-preflight-runtime-version-checks.md) | 启动阶段前置校验运行时版本 | 已采纳 | 2026-10-11 | `require_python` / `require_tkinter` 按 `setup_l10n` 前后分工（前者提示不翻译、后者可翻译），阈值集中到 `constants.py`，失败即 `sys.exit(1)`；已知缺口是 `console=False` 产物中提示被静默丢弃 |
| [0007](./0007-register-import-alias-instead-of-ignoring-rule.md) | 用显式别名登记替代整条导入别名规则豁免 | 已采纳 | 2026-10-11 | 不再 `ignore` `unconventional-import-alias`，改为 `aliases` 只登记 `gettext` → `gettextlib`；刻意取其替换语义以放弃 `pd` 一类简写约定，代价是不再约束其他模块的别名 |

## 风格

采用 **Nygard 轻量风格**，每篇 ADR 含元数据（状态、日期）与背景、决策、后果三个段落。

决策记录模板见 [`_template.md`](./_template.md)。

## 规则

- **顺序编号、不可变**：文件名 `NNNN-短文标题.md` 递增编号；已采纳的 ADR 绝不改写。
- **状态驱动**：`提议` / `已采纳` / `已废弃` / `已取代（由 NNNN 取代）`。只有 `已采纳` 才算约束。
- **一篇一决策**：只记一个决策，超过两屏应拆分。
- **变更写新篇**：推翻或修订既有 ADR 时，写新的已采纳 ADR，将旧篇标记为 `已取代`，保留演进轨迹。

## 何时写

凡遇到带权衡的“该不该”、“用哪个”（例如工具选型、目录结构、依赖取舍、接口边界），都写一篇。
