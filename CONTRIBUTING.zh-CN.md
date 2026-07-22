# 贡献指南

**简体中文** |
[English](./CONTRIBUTING.md)

首先，感谢您考虑为 **VCF 生成器 Lite** 做出贡献！

我们欢迎任何形式的贡献，无论是报告问题、提出建议、修复错误还是添加新功能。

> [!TIP]
>
> 如果您是开源贡献的新手，这些资源或许能帮到您：
>
> - GitHub 社区的 [开源软件指南][how-to-contribute-github-opensource-guide]
> - Gitee 社区的 [开源指北][participating-gitee-opensource-guide]

## 行为准则

参与本项目时，请您遵守我们的 [贡献者公约](./CODE_OF_CONDUCT.zh-CN.md)。我们致力于为每个人提供友善、包容的社区环境。

## 如何贡献

### 提交问题或建议

如果您在使用中遇到问题或有改进建议，欢迎通过以下任一渠道提交反馈：

- [Gitee Issues][issues-gitee]
- [GitHub Issues][issues-github]

### 本地化应用

本地化工作包括添加**号码检测器**以支持更多号码类型，以及翻译**应用界面**文本。

> [!TIP]
>
> **使用 AI 辅助本地化**
>
> 如果您不熟悉代码或翻译文件格式，可以使用 GitHub Copilot、Trae 等现代 AI 工具，只需用自然语言描述需求，AI 工具会自动生成符合规范的代码或完成翻译。

详细步骤请参考：

- [添加号码检测器](./docs/dev/globalization/phone-detector.md)
- [翻译应用](./docs/dev/globalization/translation.md)

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
- 单行最大 120 字符
- 其他情况以 [PEP 8][pep-0008] 为准。

#### Markdown 文档（`.md`）

- 不限制单行最大长度。
- 具体规则参考 `.markdownlint.json`。
- 其他情况遵循 [Markdownlint][markdownlint-repository-github]。

更多细节请参考 `.editorconfig`。

### 文档规范

遵守 [中文技术文档写作风格指南][zh-style-guide]。

文档按 [Diátaxis][diataxis] 框架组织为四类：入门教程、操作指南、技术参考、原理解析。

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
[diataxis]: https://diataxis.fr/
