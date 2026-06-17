# 号码检测器开发

号码检测器用于识别和验证电话号码格式。项目内置支持中国大陆、港澳台地区的号码格式，您可以通过添加新的检测器来支持其他地区。

## 数据结构

### PhoneDetector

每个国家/地区的号码检测器对应一个 [`PhoneDetector`][phone_detector.py] 实例，由以下字段组成：

- **id**：唯一标识符，格式为 `builtin.<国家>`，全部小写，如 `builtin.germany`。当同一国家内不同地区需要划分不同规则时，可在国家后追加地区标识，例如 `builtin.china.mainland`、`builtin.china.hongkong`。
- **locale_territories**：[ISO 3166-1][iso-3166] 二位地区代码集合，如 `{"CN"}`、`{"HK", "MO"}`。一个检测器可适用于多个地区。
- **name**：使用 `LazyPgettext` 包装的可翻译名称。
- **rules**：一个返回 `PhoneRule` 实例列表的函数，定义该检测器的验证规则。

### PhoneRule

每个验证规则对应一个 [`PhoneRule`][phone_detector.py] 实例，由以下字段组成：

- **length**：粗略长度检查，包含国际区号的总字符数。可选形式：
  - `int`：固定长度，如 `11` 表示恰好 11 个字符。
  - `set[int]`：多个可选长度，如 `{11, 14}` 匹配长度为 11 或 14 个字符的号码（适用于中国大陆手机号不带/带 `+86` 的场景）。
  - `range(min, max+1)`：长度范围。`range` 的结束值不包含在内，因此 `range(10, 16)` 匹配 10~15 个字符，不包含 16 个字符。
  - `None`：不限制长度，仅用正则匹配。此选项仅用无固定长度的电话号码。
- **regex**：Python 编译后的正则表达式对象（`re.compile()` 的结果）。编写语法可参考 [Python 正则表达式文档][python-docs-re]。如有反斜杠，请使用原始字符串 `r"..."`。建议包含国际区号（如 `(?:\+86)?`）以支持带区号和不带区号两种情况。

> [!IMPORTANT]
>
> 编写正则时请确保覆盖所有合法输入格式。例如德国号码在国内拨打时必须带 `0`，国际拨打时必须带 `+49`，因此正则应写为 `^(?:0|\+49)...` 而非 `^(?:\+49)?...`。

## 添加检测器

> [!TIP]
>
> **使用 AI 辅助添加**
>
> 如果您不熟悉代码或正则表达式，可使用 GitHub Copilot、Trae 等现代 AI 工具，只需用自然语言描述需求，AI 会自动生成符合规范的代码。
>
> **示例提示词**：`添加德国的电话号码检测器。手机号以 015/016/017 开头，用户号码 7~8 位，共 10~11 位；固话区号 2~5 位，本地号码 3~8 位；国内拨打带 0，国际拨打带 +49。`

### 1. 编辑配置文件

打开 [phone_detectors.py][phone_detectors.py]。

### 2. 添加检测器条目

在 `PHONE_DETECTORS` 列表末尾追加一条 `PhoneDetector` 实例：

```python
PhoneDetector(
    id="builtin.<国家>",
    locale_territories={"XX"},
    name=LazyPgettext("phone_detector.<国家>", "Name"),
    rules=lambda: [
        PhoneRule(
            length=11,
            regex=re.compile(r"^正则表达式$"),
        ),
        # 可添加多条规则（如手机号、固话分开）
    ],
),
```

### 3. 运行检查

提交前请确保代码通过 Ruff 和 Pyright 检查：

```bash
uv run poe check
```

同时运行格式化：

```bash
uv run poe format
```

## 完整示例

### 添加德国手机号检测器

```python
# src/vcf_generator_lite/configs/phone_detectors.py

PHONE_DETECTORS: list[PhoneDetector] = [
    ...
    PhoneDetector(
        id="builtin.germany",
        locale_territories={"DE"},
        name=LazyPgettext("phone_detector.germany", "Germany"),
        rules=lambda: [
            # 手机号：必须带 0（国内）或 +49（国际），后接 1[567]x，用户号 7~8 位
            PhoneRule(
                length=range(11, 15),  # 匹配 11~14 个字符，覆盖 11、12（国内）和 13、14（国际）
                regex=re.compile(r"^(?:0|\+49)1[567]\d{8,9}$")
            ),
            # 固话（合并国内/国际）：必须以 0 或 +49 开头，区号 2~5 位，本地 3~8 位
            PhoneRule(
                length=range(6, 17),   # 匹配 6~16 个字符（国内最长为 1+5+8=14，国际最长为 3+5+8=16）
                regex=re.compile(r"^(?:0|\+49)\d{2,5}\d{3,8}$")
            ),
        ],
    ),
]
```

## 编写测试

添加新检测器后，请在 [test_phone_detectors.py][test_phone_detectors.py] 中新增一个测试类，参考已有测试类（如 `TestChinaMainlandPhoneDetector`），至少覆盖以下场景：

- **地区归属**：使用 `locale_territories` 断言包含目标地区代码。
- **合法号码**：使用 `@pytest.mark.parametrize` 覆盖带国际区号、不带国际区号、典型手机号段、固话区号等典型号码。
- **非法号码**：使用 `@pytest.mark.parametrize` 覆盖错号段、长度越界、格式异常等场景。

补充建议手动测试以下场景：

1. **带国际区号**：如 `+491701234567`。
2. **不带国际区号**：如 `01701234567`。
3. **边界长度**：测试最小和最大长度的号码。
4. **无效号码**：确保错误格式的号码被正确拒绝。

## 本地化检测器名称

新检测器添加完成后，其 `name` 字段的英文文本（如 `"Germany"`）仅作为未翻译时的默认显示。翻译流程请参见 [翻译指南](./translation.md)。

## 地区匹配

号码检测器会根据系统语言的地区自动选择：

- 系统语言为 `zh_CN` 时，地区为 `CN`，启用中国大陆号码检测器。
- 系统语言为 `zh_TW` 时，地区为 `TW`，启用台湾号码检测器。
- 如果匹配到任何号码检测器，则默认列表中首个号码检测器。

## 提交贡献

完成检测和测试后，提交 Pull Request：

1. 确保代码检查通过：`uv run poe check`
2. 确保测试通过：`uv run poe test`
3. 创建 PR，说明：
   - 添加的号码格式
   - 支持的国家/地区

[phone_detector.py]: ../../../src/vcf_generator_lite/models/phone_detector.py
[phone_detectors.py]: ../../../src/vcf_generator_lite/configs/phone_detectors.py
[test_phone_detectors.py]: ../../../tests/configs/test_phone_detectors.py
[python-docs-re]: https://docs.python.org/zh-cn/3/library/re.html

[iso-3166]: https://www.iso.org/iso-3166-country-codes.html
