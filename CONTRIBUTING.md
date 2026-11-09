# Contribution Guidelines

[简体中文](./CONTRIBUTING.zh-CN.md) |
**English**

First and foremost, thank you for considering contributing to **VCF Generator Lite**!

We welcome contributions of any kind, whether it's reporting issues, suggesting improvements, fixing bugs, or adding new features.

> [!TIP]
>
> If you're new to open source contributions, these resources might help you:
>
> - GitHub Community's [Open Source Guide][how-to-contribute-github-opensource-guide]
> - Gitee Community's [Open Source Guide][participating-gitee-opensource-guide]

## Code of Conduct

When participating in this project, please abide by our [Contributor Covenant](./CODE_OF_CONDUCT.md). We are committed to providing a friendly and inclusive community environment for everyone.

## How to Contribute

### Submitting Issues or Suggestions

If you encounter problems or have improvement suggestions while using the application, feel free to submit feedback through any of the following channels:

- [Gitee Issues][issues-gitee]
- [GitHub Issues][issues-github]

### Localizing the Application

Localization work includes adding **phone detectors** to support more number types, and translating **application interface** texts (including phone detector names).

> [!TIP]
>
> **Using AI Agent to assist with localization**
>
> If you are not familiar with coding or the translation process, you can use various AI Agent tools like Trae and Codex to assist with localization. Simply describe your needs in natural language, and the AI Agent tool will automatically complete all the work for you.

Detailed guides for each task:

- [Add Phone Detector](./docs/dev/globalization/phone-detector.md)
- [Translate App](./docs/dev/globalization/translation.md)

### Participating in Development

1. Ensure there are no related pull requests (PRs) in the [Gitee repository][repository-gitee] or [GitHub repository][repository-github].
2. Fork this repository.
3. Clone the repository locally using [Git][git-homepage].
4. Read the [Development Guide](./docs/dev/index.md) to familiarize yourself with the project development methods and related conventions.
5. Create a branch, such as `feature/xxx` or `bugfix/xxx`.
6. Write your code.
7. Run the following commands to ensure the code complies with standards and introduces no errors:
   ```bash
   uv run poe fix
   uv run poe test
   ```
8. Commit your code.
9. Submit a PR to this repository.

## Standards

### Code Standards

Relevant conventions can be found in the [Development Guide](./docs/dev/index.md).

You can write code to your heart's content; the `uv run poe fix` command and your IDE will help you check and fix minor issues.

### Documentation Standards

Documentation follows the [Google Developer Style Guide][google-style-guide] and the [Google Technical Writing][google-technical-writing] courses for clarity, voice, accessibility, and inclusive language. The [Chinese Technical Documentation Style Guide][zh-style-guide] supplements these as a reference for Chinese-language writing.

Documentation is organized using the [Diátaxis][diataxis] framework into four categories: Tutorials, How-to guides, Reference, and Explanation.

You can write the documentation to your heart's content; the `uv run poe fix` command and your IDE will help you check and fix minor issues.

### Git Commit Standards

Follow [Conventional Commits][conventionalcommits-homepage].

[repository-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/
[repository-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/
[issues-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/issues
[issues-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/issues

[git-homepage]: https://git-scm.com/
[conventionalcommits-homepage]: https://www.conventionalcommits.org/en/v1.0.0/

[how-to-contribute-github-opensource-guide]: https://opensource.guide/how-to-contribute/
[participating-gitee-opensource-guide]: https://gitee.com/opensource-guide/guide/participating/roles.html
[zh-style-guide]: https://zh-style-guide.readthedocs.io/zh-cn/latest/index.html

[google-style-guide]: https://developers.google.com/style
[google-technical-writing]: https://developers.google.com/tech-writing

[diataxis]: https://diataxis.fr/
