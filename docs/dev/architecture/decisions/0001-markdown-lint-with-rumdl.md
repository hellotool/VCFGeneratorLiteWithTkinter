# 0001 使用 rumdl 做 Markdown 风格门禁

- 状态: 已采纳
- 日期: 2026-07-23

## 背景

本项目需要一套本地 Markdown 风格门禁，约束文档（含中文内容、参考链接写法）的写法，防止风格漂移。候选方案：

- `markdownlint-cli2`：Node 工具，依赖 npm 生态，配置走 `.markdownlint.yml`，无原生 VS Code 之外的轻量集成痛点。
- `lychee`：Rust 链接检查器，能递归扫仓库，但本次环境无法安装（网络受限）。
- `rumdl`：Rust 实现、与 markdownlint 规则兼容；uv 原生可得；读自有配置文件；有官方 VS Code 扩展 `rvben.rumdl` 提供实时 lint / Quick Fix / 保存格式化，且自动读取项目配置。

原仓库有一份 `.markdownlint.yml` 作为规则真相源，但在引入 rumdl 后成了孤儿文件（rumdl 不读它，CI 不跑 markdownlint，编辑器扩展也读项目的 rumdl 配置）。

## 决策

采用 `rumdl` 作为 Markdown 风格门禁。

- 配置源 = 根目录 `rumdl.toml`，使用**完整规则名**（如 `line-length` 而非 `MD013`），作为单一事实源。
- 删除 `.markdownlint.yml`，不再保留第二份规则配置。
- **链接检查不纳入**本地门禁（不校验锚点 / 外链 / 路径）。

## 后果

- 收益：单一事实源落在 `rumdl.toml`；贡献者装 `rvben.rumdl` 扩展即可获得实时提示，无需额外配置；规则与 markdownlint 兼容，迁移成本低。
- `flavor = "gfm"` 是 `Standard` 的别名（rumdl 的默认风味），经源码核实属正常行为，底层解析器已支持 GFM 扩展，无缺陷。
- 已知能力缺口（已接受，非阻塞）：
  - rumdl 的 `MD010`（对应 `no-hard-tabs`）没有 `ignore_code_languages` 键；其默认 `code-blocks = false` 已忽略全部代码块，比原 `.markdownlint.yml` 的 `ignore_code_languages: [text]` 更宽松，意图被覆盖但无法精确表达。
  - rumdl 没有 `MD062` / `table-pipe-style` 规则，表格管道风格无法强制校验。
- 后续：若表格管道风格必须强制，需重新评估（换回带该规则的工具，或接受此盲区）。
