# 0002 本地 precommit 作为验证契约

- 状态: 已采纳
- 日期: 2026-07-23

## 背景

GitHub Actions 工作流（`test.yml` / `build.yml` / `prepare-release.yml`）只运行 `poe test`，**不跑** lint / 类型检查 / Markdown 检查。在 AI 辅助开发场景下，模型改代码的速度远快于人，若缺少本地可自我验证的契约，改动可能在本地"看起来没问题"却破坏了远端才检查到的东西。

本仓库已有 uv 锁环境、`poe` 任务自动化、`pyright` 类型约束、`src/` 清晰分层、i18n 纪律等基础，但"改完即自检"的闭环只在本地、未与 CI 对齐。

## 决策

`poe precommit` = `format → check → test` 是本仓库的**验证契约**，任何改动（含文档）完成后必须本地跑通才算改完。

- `format` = `ruff format` + `rumdl fmt .`（代码与文档一体格式化）。
- `check` = `ruff check` + `pyright` + `rumdl check .`（代码与文档一体检查，**不单列 docs 任务**，命名为 `docs` 无"检查文档"语义且制造不必要的拆分）。
- `test` = `pytest`。

## 后果

- 收益：一条命令即可在本地确认改动未破坏格式、lint、类型与测试，AI 改动后能即时自检。
- 代价 / 限制：本地绿 ≠ 远端绿——CI 仅跑 `test`，lint / 类型 / Markdown 检查不在 CI 内（已知缺口）。
- 后续：可让 CI 复刻本地 `precommit`（至少 `check` + `test`），消除"本地绿远端不知道"的盲区。配置真相源为根目录 `rumdl.toml`，`AGENTS.md` 应指向它。
