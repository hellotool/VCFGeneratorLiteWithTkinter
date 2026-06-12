---
name: add-phone-detector
description: Adds new phone number detectors to the VCF Generator Lite application. Use when user needs to add support for a new country or region's phone number detection rules, or when modifying existing phone number validation rules.
---

# 添加号码检测器

为 VCF 生成器 Lite 应用添加新的号码检测器配置。

## 前置要求

在添加新检测器前，必须阅读以下文件了解结构和约定：

1. `src/vcf_generator_lite/models/phone_detector.py` — `PhoneRule` 和 `PhoneDetector` 的字段定义与约束。
2. `src/vcf_generator_lite/models/lazy.py` — `LazyPgettext` 的用法。
3. `src/vcf_generator_lite/configs/phone_detectors.py` — 现有配置，确认格式和排布。
4. `docs/dev/l10n/phone-detector.md` — 添加号码检测器的指南，包含字段说明、示例和测试要求。

## 示例

```python
PhoneDetector(
    id="builtin.china.mainland",
    locale_territories={"CN"},
    name=LazyPgettext("phone_detector.china.mainland", "Chinese mainland"),
    rules=[
        # 手机号：1 开头，11 位。带 +86 时 14 位。
        PhoneRule(length=[11, 14], regex=re.compile(r"^(?:\+86)?1[3456789]\d{9}$")),
        # 固话：区号 + 号码，10-12 位。带 +86 时 13-15 位。
        PhoneRule(length=range(10, 16), regex=re.compile(r"^(?:\+86)?0\d{2,3}\d{7,8}$")),
    ],
),
```

## 添加新检测器的步骤

1. 确定目标国家/地区的 ISO 3166-1 地区代码。
2. 研究该地区的电话号码规则（手机号号段、固话区号、号码长度）。
3. 确定 `id`。
4. 编写正则表达式，确保国际区号可选。
5. 设置 `length`，覆盖带/不带国际区号的所有情况。
6. 将新条目追加到 `PHONE_DETECTORS` 列表末尾。
7. 在 `test_phone_detectors.py` 中新增测试类。
8. 运行 `uv run poe check` 确保代码通过 Ruff 和 Pyright 检查。
9. 运行 `uv run poe test` 确保新增测试通过且现有测试不受影响。

## 翻译名称

新检测器添加完成后，其 `name` 字段的英文文本（如 `"Japan"`）仅作为未翻译时的默认显示。请使用 `translate-app` 技能翻译该名称。

## 常见错误

| 错误                                          | 正确做法                              |
| --------------------------------------------- | ------------------------------------- |
| `length` 只包含本地号码长度，忘记带区号的情况 | 同时列出带区号的长度，如 `[11, 14]`   |
| `regex` 中忘记转义 `+`                        | 使用 `\+` 匹配字面量加号              |
| `range` 的上限写错                            | `range(min, max+1)`，注意上限是开区间 |
