# 国际化机制

本文介绍项目的国际化（i18n）实现机制。

对于翻译应用，请参考 [翻译指南](./translation.md)。

对于号码检测器开发，请参考 [号码检测器开发](./phone-detector.md)。

## 技术选型

- **底层实现**：[Python 标准库 `gettext`][python-docs-gettext]
- **关键字提取**：[Babel][babel-homepage]
- **ZIP 应用兼容**：[`utils/i18n/zipapp_gettext.py`][zipapp-gettext.py] 提供了基于 `Traversable` 的自定义 `translation()` 和 `find()` 实现，替代标准库中不兼容 ZIP 应用内嵌资源的对应函数。

> [!IMPORTANT]
>
> 启动时 `bootstrap.setup_l10n()` 通过猴子补丁**替换全局 `gettext` 模块中的函数**（`gettext`、`ngettext`、`pgettext`、`npgettext`）。
> 因此 `from gettext import pgettext` 等导入的实际上是项目内的 `translation` 对象上的方法。
>
> **请勿在 `bootstrap.py` 以及 `__main__.py` 中在顶部导入项目模块、gettext 模块或者 argparse 模块。**

## 关键字约定

除了支持 Babel 默认识别标准关键字（`pgettext`、`npgettext`、`gettext`、`ngettext` 等）外，本项目还额外声明了 `pgettext_menu_label` 与 `LazyPgettext`。

- **`pgettext_menu_label`**：项目自定义函数，位于 `utils/tkinter/menu.py`，把 `&` 解析为访问键位置。
- **`LazyPgettext`**：项目自定义的 `NamedTuple`，定义在 `models/lazy.py`。用于模块级别定义的字符串常量，避免在导入阶段触发翻译查找。实际翻译在调用点通过 `pgettext(item.context, item.message)` 完成。

> [!IMPORTANT]
>
> 禁止使用 `_` / `gettext`，应用内所有可翻译字符串必须显式声明上下文。

## 编写可翻译字符串

### 上下文格式

- `app`：应用级上下文
  - `.name`：应用名称
  - `.description`：应用描述
- `window_*`：窗口上下文
  - `.title`：窗口标题
- `dialog_*`：对话框上下文
  - `.title`：对话框标题
  - `.message`：对话框消息
  - `.detail`：对话框详细消息
- `startup`：启动时上下文
- `button_*`：按钮文本
- `label_*`：标签文本
- `entry_*`：文本框文本
- `error_*`：错误文本

### 带上下文的字符串

项目统一使用 `pgettext`：

```python
from gettext import pgettext

menu_label = pgettext("menu_file", "File")
```

### 菜单标签（带助记符）

使用 `pgettext_menu_label`，在原文中用 `&` 标记快捷键字母：

```python
from vcf_generator_lite.utils.tkinter.menu import pgettext_menu_label

parsed_label = pgettext_menu_label("window_main.menu_help_about", "&About {app_name}")
# 返回 ParsedLabel(label="About {app_name}", underline=0)
```

### 延迟翻译

`LazyPgettext` 用于模块级别定义的常量字符串，避免在导入阶段触发 `pgettext` 查找。

```python
from vcf_generator_lite.models.lazy import LazyPgettext

GREETING = LazyPgettext("greeting", "Hello")
```

`LazyPgettext` 保留 context 和 message，未翻译时 `str()` 返回原始英文。实际翻译在使用点通过 `pgettext` 完成：

```python
from gettext import pgettext

label = pgettext(GREETING.context, GREETING.message)
```

业务场景（字段类型标注、配置数据装配）见具体业务文档，例如 [号码检测器开发](./phone-detector.md) 中 `PhoneDetector.name` 的使用。

## 语言回退

当指定语言缺少翻译时，会自动回退到英文。

**回退顺序：**

1. 用户指定语言（如 `zh_CN`）
2. 语言变体（如 `zh`）
3. 默认语言（`en`）

[python-docs-gettext]: https://docs.python.org/zh-cn/3/library/gettext.html
[babel-homepage]: https://babel.pocoo.org/
[zipapp-gettext.py]: ../../../src/vcf_generator_lite/utils/i18n/zipapp_gettext.py
