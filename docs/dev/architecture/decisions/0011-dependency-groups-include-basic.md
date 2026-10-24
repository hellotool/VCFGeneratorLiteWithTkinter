# 0011 各依赖组自带 basic

- 状态: 已采纳
- 日期: 2026-10-24

## 背景

`[dependency-groups]` 此前只在 `dev` 里聚合 `basic`（poethepoet），其余功能组彼此独立。因此任何不走 `dev` 的调用都得自己并列 `--group basic` 才能拿到任务运行器：`.github/workflows/test.yml` 写 `uv run --group test --group basic poe test`，`build.yml` 的四个构建步骤同样并列 `--group build --group basic`。调用点越多，"别忘了 basic" 越容易漏，而漏掉的报错是 poe 不存在，与真实意图（跑测试 / 构建）相距较远。

## 决策

- `lint`、`test`、`build`、`docs`、`l10n` 五个功能组各自 `{ include-group = "basic" }`，任一功能组单独安装即可运行 poe 任务。
- `dev` 继续聚合全部功能组；`basic` 仍保留为独立组，供只需要任务运行器的场景使用。
- 组内重复由 uv 解析时去重，lockfile 内容不因重复列出而改变。

## 后果

- 收益：任一功能组自足，调用方不必再记 `--group basic`；poethepoet 的版本仍只在 `basic` 一处声明。
- 代价：功能组不再是"最小依赖集"的严格定义，读 `[dependency-groups]` 时要顺着 include 展开才知道实际安装了哪些包。
- 现状遗留：CI 中现存的 `--group basic` 成为冗余参数，保留不影响结果；本次未改动工作流。
- 验证：`uv lock --check` 通过；`uv run poe check`、`uv run poe test` 通过。
