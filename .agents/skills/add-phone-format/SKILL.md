---
name: add-phone-format
description: Adds new phone number formats to the VCF Generator Lite application. Use when user needs to add support for a new country or region's phone number formats, or when modifying existing phone format validation rules.
---

# 添加号码格式

为 VCF 生成器 Lite 应用添加新的号码格式配置。

## 前置要求

在添加新格式前，必须阅读以下文件了解结构和约定：

1. `src/vcf_generator_lite/models/phone_format.py` — `PhoneRule` 和 `CountryPhoneFormat` 的字段定义与约束。
2. `src/vcf_generator_lite/models/lazy.py` — `LazyPgettext` 的用法。
3. `src/vcf_generator_lite/configs/phone_formats.py` — 现有配置，确认格式和排布。

## 示例

```python
CountryPhoneFormat(
    id="builtin.china.mainland",
    locale_territories={"CN"},
    name=LazyPgettext("phone_format.china.mainland", "Chinese mainland"),
    rules=[
        # 手机号：1 开头，11 位。带 +86 时 14 位。
        PhoneRule(length=[11, 14], regex=re.compile(r"^(?:\+86)?1[3456789]\d{9}$")),
        # 固话：区号 + 号码，10-12 位。带 +86 时 13-15 位。
        PhoneRule(length=range(10, 16), regex=re.compile(r"^(?:\+86)?0\d{2,3}\d{7,8}$")),
    ],
),
```

## 添加新格式的步骤

1. 确定目标国家/地区的 ISO 3166-1 地区代码。
2. 研究该地区的电话号码规则（手机号号段、固话区号、号码长度）。
3. 确定 `id`，格式为 `builtin.<国家>.<地区>`。
4. 编写正则表达式，确保国际区号可选。
5. 设置 `length`，覆盖带/不带国际区号的所有情况。
6. 将新条目追加到 `PHONE_FORMATS` 列表末尾。
7. 运行 `uv run poe check` 确保代码通过 Ruff 和 Pyright 检查。
8. 运行 `uv run poe test` 确保现有测试不受影响。

## 常见错误

| 错误                                          | 正确做法                              |
| --------------------------------------------- | ------------------------------------- |
| `length` 只包含本地号码长度，忘记带区号的情况 | 同时列出带区号的长度，如 `[11, 14]`   |
| `regex` 中忘记转义 `+`                        | 使用 `\+` 匹配字面量加号              |
| `range` 的上限写错                            | `range(min, max+1)`，注意上限是开区间 |
| `id` 使用大写或下划线                         | 统一使用小写 + 点分隔                 |
