# 常见问题（FAQ）

## 生成文件时界面卡顿

CPython 的[全局解释器锁（GIL）][gil]限制了同一时刻只能有一个线程执行 Python 字节码，这可能在多线程场景下影响界面响应。

如果您使用的是 Python ZIP 应用且遇到界面卡顿，可以尝试切换到**自由线程（free-threading） Python 解释器**运行应用。自由线程模式允许多个线程在同一解释器中同时执行 Python 字节码，从而绕过 GIL 限制，提升多线程性能。

有关自由线程的更多信息，请参阅 [自由线程的 CPython][free-threaded-cpython]。

## 提示“缺失号码或号码不正确”

本工具目前仅支持识别 **11 位中国大陆手机号**。

输入以下类型的号码时会触发此提示：

- 固定电话
- 短号
- 其他国家/地区手机号

> [!NOTE]
>
> 未来版本可能会扩展支持更多号码格式，敬请关注更新！

## 如何导入 Excel 工作簿？

当前版本仅支持通过手动输入或粘贴的方式添加联系人，格式为：`姓名 电话 备注`。

如需从 Excel 导入，请按以下步骤操作：

1. 调整 Excel 中的字段顺序，使其与 `姓名 电话 备注` 一致。
2. 选中需要导入的联系人数据并复制（Ctrl+C）。
3. 在本工具输入框中粘贴（Ctrl+V）。

## 更多帮助

仍未找到答案？欢迎通过以下渠道联系我们：

- [GitHub Discussions][discussions-github] – 技术交流与讨论。
- [GitHub Issues][issues-github] – 报告问题或提交建议。
- [Gitee Issues][issues-gitee] – 报告问题或提交建议（国内用户推荐）。

[issues-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/issues
[issues-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/issues

[discussions-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/discussions

[gil]: https://docs.python.org/zh-cn/3.13/glossary.html#term-global-interpreter-lock
[free-threaded-cpython]: https://docs.python.org/zh-cn/3.14/whatsnew/3.13.html#whatsnew313-free-threaded-cpython
