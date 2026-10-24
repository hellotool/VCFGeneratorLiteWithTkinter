# 0010 Poe 任务文件改用 YAML 并移除 include 指针

- 状态: 已采纳，取代 [0003](./0003-poe-tasks-in-dedicated-file.md)
- 日期: 2026-10-24

## 背景

[0003][ref-0003] 把任务定义从 `pyproject.toml` 迁到根目录 `poe_tasks.toml`，并在 `pyproject.toml` 保留 `executor` + `include` 指针；其中明确否决了"完全删掉 `[tool.poe]`"，理由是 `pyproject.toml` 里不留痕迹会降低任务文件的可发现性。

这套配置此后暴露两个问题。其一，TOML 任务文件要为每个参数重复 `[[tasks.X.args]]` 表头，参数越多重复越多，且没有可用的 JSON Schema 供编辑器校验。其二，`include` 让同一个文件名同时出现在 `pyproject.toml` 与文件系统中，改名或移动要改两处。

poe 0.49.0 在 `pyproject.toml` 不含 `[tool.poe]` 时，会按约定文件名自动发现任务文件（`poe_tasks.toml` / `poe_tasks.yaml` / `poe_tasks.yml` / `poe_tasks.json`，见 `poethepoet/config/config.py`），因此 `include` 指针不是必需的。

## 决策

- 任务定义迁到根目录 `poe_tasks.yml`，`executor: uv` 直接写在文件内。
- 删除 `pyproject.toml` 中的 `[tool.poe]`（含 `include` 指针），不再保留 `poe_tasks.toml`。
- 文件首行声明 `# yaml-language-server: $schema=...`，指向 SchemaStore 的 [partial-poe schema][ref-partial-poe]，供编辑器做校验与补全。
- 任务集合与行为不变：任务名、`help`、`args` 与旧 TOML 逐项一致，共 16 个任务。

## 后果

- 收益：任务文件可用 JSON Schema 校验；`args` 改为列表项，去掉重复表头；`pyproject.toml` 不再引用任务文件名，少一处同步点。
- 代价 / 限制：任务文件靠 poe 的约定名自动发现，`pyproject.toml` 中不再有痕迹——即 0003 以可发现性为由否决过的形态；YAML 对缩进敏感；需要支持独立 YAML 任务文件的 poe（项目锁定 0.49.0）。
- 验证：`uv run poe` 列出的任务与旧文件一致；`uv run poe check`、`uv run poe test` 通过。
- 缺口：任务定义仍无测试覆盖（同 [0003][ref-0003]）。

[ref-0003]: ./0003-poe-tasks-in-dedicated-file.md
[ref-partial-poe]: https://json.schemastore.org/partial-poe.json
