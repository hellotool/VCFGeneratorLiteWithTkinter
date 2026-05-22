---
name: translate-app
description: Translates the VCF Generator Lite application interface to new languages. Use when user needs to add or update translations for the application, initialize new locales, or compile translation files.
---

# 翻译应用界面

为 VCF 生成器 Lite 应用添加或更新界面翻译。

## 前置要求

在开始翻译前，必须：

1. 阅读 `src/vcf_generator_lite/resources/locales/zh_CN/LC_MESSAGES/vcf-generator-lite.po`，了解现有翻译文件的格式和约定。
2. 了解 gettext 的 `.po` 文件格式：`msgctxt`（翻译上下文）、`msgid`（原文）、`msgstr`（译文）。

## 文件位置

| 文件     | 路径                                                                                  |
| -------- | ------------------------------------------------------------------------------------- |
| 翻译模板 | `src/vcf_generator_lite/resources/locales/templates/vcf-generator-lite.pot`           |
| 语言文件 | `src/vcf_generator_lite/resources/locales/<locale>/LC_MESSAGES/vcf-generator-lite.po` |
| 编译产物 | `src/vcf_generator_lite/resources/locales/<locale>/LC_MESSAGES/vcf-generator-lite.mo` |

## 工作流程

### 维护者前置步骤（源代码已变更时）

如果源代码中的翻译字符串发生了变更，需要先同步模板：

1. 提取翻译字符串：
   ```bash
   uv run poe l10n-extract
   ```
2. 更新语言文件：
   ```bash
   uv run poe l10n-update
   ```

### 翻译贡献者前置步骤

1. 准备语言文件：
   - 如果是首次翻译某个语言：
     ```bash
     uv run poe l10n-init -l <language[_territory]>
     ```
   - 如果该语言的 `.po` 文件已存在，同步最新模板：
     ```bash
     uv run poe l10n-update
     ```

### 通用步骤（所有角色）

1. 编辑 `.po` 文件：逐条翻译新增或变更的条目。
2. 编译翻译：
   ```bash
   uv run poe l10n-compile -l <language_code>
   ```

## 翻译约定

### 变量占位符

保持所有变量占位符原样不动，包括类型、数量、顺序：

| 占位符类型 | 示例                   | 规则                                                                  |
| ---------- | ---------------------- | --------------------------------------------------------------------- |
| 百分号格式 | `%s`, `%d`, `%(name)s` | 数量和顺序不可调整。`%s` 是位置相关的，调换顺序会导致运行时替换错位。 |
| 花括号格式 | `{url}`, `{count}`     | 保持原样。命名占位符可以调整顺序，但通常不需要。                      |

重要：不要将 `%s` 改为 `%d` 或其他类型，也不要在译文中增加或删除占位符。

### fuzzy 标记

如果 `.po` 文件中的条目带有 `#, fuzzy` 标记，说明该翻译是自动生成的模糊匹配，编译时会被忽略。翻译完成后必须删除该标记。

```po
# 翻译前
#, fuzzy
msgctxt "error"
msgid "File not found"
msgstr "文件不存在"

# 翻译后（删除 fuzzy 行）
msgctxt "error"
msgid "File not found"
msgstr "找不到文件"
```

### 翻译注意事项

1. 上下文感知：同一个 `msgid` 在不同 `msgctxt` 下可能需要不同的译文。
2. 保持换行：如果原文包含 `\n`，译文也应包含相同数量的 `\n`。
3. 特殊字符：`msgstr` 中的 `"` 需要转义为 `\"`。
4. 使用 UTF-8 编码：所有 `.po` 文件均为 UTF-8 编码。
5. 参考已有翻译：不确定时，参考 `zh_CN` 的翻译风格保持一致。

## 验证翻译

1. 启动应用，切换系统语言或设置 `LANG` 环境变量为对应的 locale。
2. 检查所有界面文本是否已翻译，特别注意菜单、按钮、错误提示。
3. 确认变量占位符在翻译后仍能正确替换。

## 常见错误

| 错误                      | 正确做法                        |
| ------------------------- | ------------------------------- |
| 翻译了变量占位符          | 保持 `%s`、`{url}` 等原样       |
| 忘记删除 `#, fuzzy` 标记  | 确认翻译后删除该行              |
| 译文缺少 `\n` 换行        | 保持与原文相同的换行数量        |
| `.po` 文件不是 UTF-8 编码 | 使用 UTF-8 编码保存             |
| 未编译就测试              | 修改后必须先运行 `l10n-compile` |
