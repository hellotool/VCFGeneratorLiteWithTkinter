# 0007 用显式别名登记替代整条导入别名规则豁免

- 状态: 已采纳
- 日期: 2026-10-11

## 背景

`ruff.toml` 原先把 `unconventional-import-alias` 整条放进 `ignore`，注释理由是"很多情况下简写语义不明，要尽量避免简写"。这条规则的默认约定表恰好以简写为主：ruff 0.16.9 的内置约定把 `pandas` 固化为 `pd`，实测 `import pandas as dataframe` 在 `--isolated` 默认配置下报 ICN001。

项目需要一处例外。`bootstrap.setup_l10n()` 写作 `import gettext as gettextlib`（`bootstrap.py:20`），而 gettext 生态的惯用别名是 `_`，与项目规范直接冲突——`i18n-mechanism.md` 明确禁止使用 `_` 与无上下文的 `gettext` 调用。整条豁免让 `gettextlib` 合法，代价是全树不再有任何别名约束。

## 决策

用登记别名取代整条豁免：从 `ignore` 中移除 `unconventional-import-alias`，改在 `[lint.flake8-import-conventions.aliases]` 只声明 `"gettext" = "gettextlib"`。

- 取该表的**替换语义**：默认约定表随整体覆盖而失效，`pandas` → `pd` 之类的简写不再被要求。这是选用 `aliases` 而非 `extend-aliases` 的直接原因，两者在 ruff 0.16.9 下行为不同，实测同一探针（`import pandas as dataframe` + `import gettext`）在 `aliases` 下只报 gettext 一条，在 `extend-aliases` 下两条都报。
- `gettext` 的唯一合法别名就此固定为 `gettextlib`：`import gettext` 与 `import gettext as gt` 均报 ICN001。
- 不做：不逐条登记其他模块的别名，不启用 `banned-aliases` 显式封禁 `_`。

## 后果

- 收益：约束从"关掉一条规则"收敛为"锁死一条别名"，猴子补丁所需的 `gettextlib` 写法获得机器保护，不会被顺手改回生态默认的 `as _`。
- 代价：重新开启这条规则**不等于**恢复全树别名约束。它只作用于登记表内的模块，实测 `import os as oslib` 与 `import pandas as dataframe` 在当前配置下都无告警，其他模块的随意别名仍只能靠评审拦截。这是接受替换语义的必然结果，不是可修的配置疏漏。
- 限制：规则的管辖范围不含 from-import，而项目里 `from gettext import pgettext` 才是主要形态（`bootstrap.py` 内多处），因此该规则实际覆盖的是极少数写法。
- 后续：若将来需要约束新的模块别名，应在 `aliases` 表中逐条登记符合项目取向的全称别名，而不是回到 `ignore` 整条规则；若确实要恢复默认约定表，改用 `extend-aliases` 即可，但那等于把简写重新写成规范，需另写一篇决策来支撑。
