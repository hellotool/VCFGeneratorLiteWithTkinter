# 翻译指南

本文介绍如何翻译 VCF 生成器 Lite 的界面文本。

## 文件结构

```mermaid
flowchart TD
    ROOT["src/vcf_generator_lite/resources/locales/"]

    ROOT --> TEMPLATES["templates/"]
    TEMPLATES --> POT["vcf-generator-lite.pot<br/>由 pybabel extract 生成"]

    ROOT --> ZH["zh_CN/"]
    ZH --> ZH_LC["LC_MESSAGES/"]
    ZH_LC --> ZH_PO["vcf-generator-lite.po<br/>翻译源文件"]
    ZH_LC --> ZH_MO["vcf-generator-lite.mo<br/>编译产物（运行时加载）"]

    ROOT --> OTH["<其他语言>/"]
    OTH --> OTH_LC["LC_MESSAGES/"]
    OTH_LC --> OTH_PO["vcf-generator-lite.po"]
    OTH_LC --> OTH_MO["vcf-generator-lite.mo"]

    classDef others fill:#9E9E9E10,stroke:#9E9E9E
    classDef lang fill:#79554822,stroke:#795548
    classDef pot fill:#3F51B522,stroke:#3F51B5
    classDef po fill:#2196F322,stroke:#2196F3
    classDef mo fill:#00BCD422,stroke:#00BCD4

    class ROOT,TEMPLATES,ZH_LC,OTH_LC others
    class ZH,OTH lang
    class ZH_PO,OTH_PO po
    class ZH_MO,OTH_MO mo
    class POT pot
```

## 常用命令

通过 Poe the Poet 任务运行：

| 命令                                       | 说明                           |
| ------------------------------------------ | ------------------------------ |
| `uv run poe l10n-extract`                  | 重新生成 `.pot` 模板           |
| `uv run poe l10n-init --locale <locale>`   | 初始化新的语言（生成 `.po`）   |
| `uv run poe l10n-update`                   | 更新已有 `.po`（合并新字符串） |
| `uv run poe l10n-compile`                  | 编译所有语言为 `.mo`           |
| `uv run poe l10n-compile -locale <locale>` | 编译指定语言                   |

## 翻译流程

> [!TIP]
>
> **使用 AI 辅助翻译**
>
> 您可以使用 GitHub Copilot、Trae 等现代 AI 工具，只需用自然语言描述需求，AI 会自动完成语言文件初始化、逐条翻译、处理变量占位符和 fuzzy 标记，并编译生成 `.mo` 文件。
>
> **示例提示词**：`把应用界面翻译成法语。`

### 1. 提取字符串

修改源码后，重新生成模板：

```bash
uv run poe l10n-extract
```

### 2. 新增语言

`--locale` 参数遵循 gettext 命名约定，格式为 `language_territory.codeset@modifier`，例如下 `fr_FR` 表示法语（法国）。

```bash
uv run poe l10n-init --locale fr_FR
```

然后编辑生成的 `src/vcf_generator_lite/resources/locales/<locale>/LC_MESSAGES/vcf-generator-lite.po`。

### 3. 更新已有翻译

同步翻译模板：

```bash
uv run poe l10n-update
```

然后编辑对应语言的 .po 文件。新出现的 msgid 会被自动追加到所有 .po 文件中，已翻译的 msgstr 保持不变。

### 4. 编译

翻译完成后，需要编译为二进制格式：

```bash
uv run poe l10n-compile
```

> [!IMPORTANT]
>
> 一定要提交编译后的 `.mo` 文件，否则在打包产物中将无法显示翻译。

### 5. 测试翻译

启动应用查看翻译效果：

```bash
LANGUAGE=<locale> uv run python -m vcf_generator_lite
```

## 注意事项

### 处理变量占位符

部分字符串包含变量占位符，翻译时必须保留：

```po
msgid "Generated {count} contacts"
msgstr "已生成 {count} 个联系人"
```

> [!IMPORTANT]
>
> - 保留花括号 `{}` 及其中的变量名
> - 可以调整占位符在句子中的位置
> - 不要修改变量名

### 处理 fuzzy 标记

如果 `msgstr` 前有 `#, fuzzy` 标记，表示该翻译可能不准确，需要人工核对：

```diff
 #: src/vcf_generator_lite/ui/windows/invalid_items_dialog/layout.py:118
-#, fuzzy
 msgctxt "common.button_ok"
 msgid "OK"
-msgstr "好的"
+msgstr "确定"
```

确认翻译正确后，删除 `#, fuzzy` 行。

## 提交翻译

翻译完成后，提交 Pull Request：

1. 确保 MO 文件已编译
2. 测试翻译效果
3. 创建 PR，说明翻译的语言
