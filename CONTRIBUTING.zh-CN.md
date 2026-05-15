# 贡献指南

**简体中文** |
[English](./CONTRIBUTING.md)

首先，感谢您考虑为 **VCF 生成器 Lite** 做出贡献！

我们欢迎任何形式的贡献，无论是报告问题、提出建议、修复错误还是添加新功能。

> [!TIP]
>
> 如果你是开源贡献的新手，这些资源或许能帮到你：
>
> - GitHub 社区的 [开源软件指南][how-to-contribute-github-opensource-guide]。
> - Gitee 社区的 [开源指北][participating-gitee-opensource-guide]。

## 行为准则

参与本项目时，请遵守我们的 [贡献者公约](./CODE_OF_CONDUCT.zh-CN.md)。我们致力于为每个人提供友善、包容的社区环境。

## 如何贡献

### 提交问题或建议

如果您在使用中遇到问题或有改进建议，欢迎通过以下任一渠道提交反馈：

- [Gitee Issues][issues-gitee]
- [GitHub Issues][issues-github]

### 本地化应用

> [!NOTE]
>
> 当前应用仅支持识别 11 位中国大陆手机号，暂不支持其他类型的号码。

如需为应用添加新的语言支持，请按以下步骤操作：

1. **初始化语言文件**：执行以下命令，其中 `<语言标识>` 遵循 POSIX locale 规范，格式为 `语言[_地区]`（`语言` 为 ISO 639-1 代码，`地区` 为 ISO 3166-1 代码，如 `zh_CN`、`en`、`zh_TW`）：
   ```bash
   uv run poe l10n-init -l <语言代码>
   ```
2. **编辑翻译文件**：打开生成的 `.po` 文件，路径为：  
   ```txt
   src/vcf_generator_lite/resources/locales/<语言代码>/LC_MESSAGES/vcf-generator-lite.po
   ```
   根据 `msgid` 填写对应的 `msgstr` 翻译内容。
3. **编译语言文件** ：翻译完成后，执行以下命令生成 `.mo` 文件：  
   ```bash
   uv run poe l10n-compile -l <语言代码>
   ```

### 参与开发

1. 确保 [Gitee 仓库][repository-gitee] 或 [GitHub 仓库][repository-github] 中没有相关的拉取请求（PR）。
2. Fork 本仓库。
3. 使用 [Git][git-homepage] 将仓库克隆到本地。
4. 阅读[开发指南](./docs/dev/index.md)，熟悉项目开发方法。
5. 创建分支，如 `feature/xxx` 或 `bugfix/xxx`。
6. 编写代码。
7. 运行以下命令，确保代码符合规范且未引入错误：
   ```bash
   uv run poe format
   uv run poe check
   uv run poe test
   ```
8. 提交代码。
9. 向本仓库提交 PR。

## 规范

### 代码规范

#### Python 代码（`.py`）

- 函数参数必须声明类型注解。
- 单行最大 120 字符。
- 其他情况以 [PEP 8][pep-0008] 为准。

#### Markdown 文档（`.md`）

- 不限制单行最大长度。
- 具体规则参考 `.markdownlint.json`。
- 其他情况遵循 [Markdownlint][markdownlint-repository-github]。

更多细节请参考 `.editorconfig`。

### 文档规范

遵守 [中文技术文档写作风格指南][zh-style-guide]。

### Git 提交规范

遵循 [约定式提交][conventionalcommits-homepage]。

[repository-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/
[repository-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/
[issues-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/issues
[issues-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/issues

[markdownlint-repository-github]: https://github.com/DavidAnson/markdownlint
[git-homepage]: https://git-scm.com/
[conventionalcommits-homepage]: https://www.conventionalcommits.org/zh-hans/v1.0.0/

[how-to-contribute-github-opensource-guide]: https://opensource.guide/zh-hans/how-to-contribute/
[participating-gitee-opensource-guide]: https://gitee.com/opensource-guide/guide/participating/roles.html
[zh-style-guide]: https://zh-style-guide.readthedocs.io/zh-cn/latest/index.html

[pep-0008]: https://peps.python.org/pep-0008/
