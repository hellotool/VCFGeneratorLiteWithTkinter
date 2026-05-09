<div align="center">
<img src="./assets/images/icon.svg" width="192" height="192" alt="App icon" />

# VCF Generator Lite ![with Tkinter](https://img.shields.io/badge/with-Tkinter-00319C)

**Repositories**:
[![Gitee primary repository](https://img.shields.io/badge/Gitee-primary_repo-C71D23?logo=gitee)][repository-gitee]
[![GitHub secondary repository](https://img.shields.io/badge/GitHub-secondary_repo-0969da?logo=github)][repository-github]

**Platforms**:
[![Windows 8.1+ (exe)](https://img.shields.io/badge/Windows_8.1+-exe-0078D4?logo=windows)][release-gitee]
[![Python 3.12+ (pyzw)](https://img.shields.io/badge/Python_3.12+-pyzw-3776AB?logo=python&logoColor=f5f5f5)][release-gitee]

**Languages**:
[简体中文](./README.zh-CN.md) |
**English** |
<small>More translations are welcome!</small>

</div>

VCF Generator Lite is a simple and efficient tool that converts contact lists into a single vCard (`.vcf`) file. Generated files can be batch-imported into mobile phone contacts or used for various other purposes. Built with Python and Tkinter for a native desktop experience.

[![License](https://img.shields.io/github/license/hellotool/VCFGeneratorLiteWithTkinter)](./LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](./CODE_OF_CONDUCT.md)

[![GitHub - Test](https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/workflows/test.yml/badge.svg)][workflow-test]
[![GitHub - Release](https://img.shields.io/github/v/release/hellotool/VCFGeneratorLiteWithTkinter?logo=github)][release-github]
![GitHub - Stars](https://img.shields.io/github/stars/hellotool/VCFGeneratorLiteWithTkinter?style=flat&logo=github)
[![Gitee - Stars](https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/badge/star.svg?theme=dark)][stargazers-gitee]

## Features

- **Smart Parsing**: Batch contacts in `Name Phone Note` format (note optional), automatically handles tabs and spaces.
- **Batch Generation**: Combines all contacts into a single `.vcf` file.
- **Number Validation**: Automatically skips invalid numbers and quickly locates error rows.
- **Editing Assistance**: Displays line numbers in text area, supports one-click quote removal.

## Screenshots

<img src="./assets/images/screenshots/main_window.zh-CN.webp" width="451" alt="Main window" />
<img src="./assets/images/screenshots/invalid_lines_window.zh-CN.webp" width="362" alt="Invalid Lines Window" />

## Getting the App

### Downloading the Packages

You can download the package through the following channels:

- [Gitee Releases][release-gitee]
- [GitHub Releases][release-github]

Please select the appropriate software package for your platform:

| Platform       | Package Type           | Installation Required | File                                                      |
| -------------- | ---------------------- | --------------------- | --------------------------------------------------------- |
| Windows        | Installer              | Yes                   | VCFGeneratorLite-\<version\>-**win-amd64**-*setup.exe*    |
| Windows        | Portable Package       | No                    | VCFGeneratorLite-\<version\>-**win-amd64**-*portable.zip* |
| Cross-platform | Python Wheel           | Optional              | vcf_generator_lite-\<version\>-**py3-none-any**.*whl*     |
| Cross-platform | Python ZIP Application | No                    | VCFGeneratorLite-\<version\>-**py3**.*pyzw*               |

### Using Python Wheel

Python Wheel (`.whl`) files are suitable for users familiar with the command line. It is recommended to run them in an isolated environment to avoid dependency conflicts.

#### Method 1: Temporary Execution (Simplest, No Installation Required)

Use `uvx`, which automatically creates a temporary environment and runs the program.

```bash
uvx <path-to-whl-file>
```

> [!NOTE]
>
> `uvx` is the shorthand for `uv tool run`, provided by the [uv][uv-homepage] tool.

#### Method 2: Install for Long-Term Use

Install using one of the tools below, which automatically create an isolated virtual environment without affecting your system Python.

```bash
# Using pipx
pipx install <path-to-whl-file>

# Or using uv
uv tool install <path-to-whl-file>
```

After installation, simply run the following command in your terminal:

```bash
vcf-generator-lite
```

> [!TIP]
>
> If you haven't installed `uv` or `pipx` yet, please run `pip install uv` or `pip install pipx` first.

## Usage

1. Paste your contacts in the format `Name Phone Note` into the text field. The note is optional.
   ```text
   Qu Yuan			13333333333	Poet of the Warring States period
   Cao Cao			13444444444
   Tao Yuanming	13555555555
   Xie Lingyun		13666666666
   ```
2. Click **Generate**, select a path to save the file.
3. You can use the generated vCard file wherever you need it.

> [!NOTE]
>
> - You can use both tabs and spaces to separate fields.
> - The program will automatically remove extra spaces from the text field.
>
> Example: `Han Meimei   13333333333   A   well-known girl` will be recognized as
>
> | Name       | Phone       | Note              |
> | ---------- | ----------- | ----------------- |
> | Han Meimei | 13333333333 | A well-known girl |

### Using vCard Files

<details>
<summary>Import to Mobile Contacts</summary>

1. Transfer the vCard file to your phone.
2. Open the vCard file and select **Contacts**, then follow the prompts.
3. Wait for the import to complete.

</details>

<details>
<summary>Import to QQ Mail</summary>

1. Open the new version of the QQ Mail website.
2. In the sidebar, select **Apps > Contacts**, then choose **Manage > Import contacts**.
3. In the dialog box that appears, click the **Select File** button and select your vCard file.
4. Click **Start to import**.

</details>

<details>
<summary>Import to Lark</summary>

1. Open the Lark client.
2. In the sidebar, select **Contacts > Email Contacts**, then choose the **Add > Import contacts** button.
3. In the dialog box that appears, select or drag your vCard file.
4. Click **Import**.

</details>

## Compatibility

### System Requirements

| Software Package Type                | System Requirements           |
| ------------------------------------ | ----------------------------- |
| Windows Installer & Portable Package | Windows 8.1 or later          |
| Python ZIP Application               | Python 3.12 or later, Tkinter |

If you need to use this application on Windows 8 or earlier versions, please see [Running on older versions of Windows](./docs/compatibility/runs-on-older-windows.md).

If you need to double-click to launch a Python ZIP application directly on Windows, please install [Python Install Manager][pymanager] (recommended) or [Python Launcher][pylauncher].

### vCard Compatibility

- **vCard Version**: 2.1
- **Supported Fields**: Name, Phone Number, Note
- **Known Issues**:
  - **Windows Contacts**: May display garbled characters in non-UTF-8 environments.

### Other Compatibility

| System Environment                     | Issue                              | Description                                                                                | Workaround                                                                                                                                  |
| -------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows 10 or later                    | Dark mode not supported            | Tkinter has no built-in dark theme.                                                        | Use [high contrast themes][windows-high-contrast-support] or modify the system theme with third-party tools (e.g., [Rectify11][rectify11]). |
| Windows 10 or later                    | UI becomes blurry when DPI changes | App doesn't support DPI adjustment after startup                                           | Avoid changing DPI while the application is running.                                                                                        |
| Python Install Manager 26.0 or earlier | Command line window appears        | Doesn't support automatic upgrade to windowed Python interpreter. ([python/pymanager#216]) | Upgrade the Python Install Manager to version 26.1 or later, or use the [Python launcher][pylauncher].                                      |

## License

This project is licensed under the Apache 2.0 license. For details, please refer to the [LICENSE file](./LICENSE).

```txt
Copyright 2023-2026 Jesse205

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## Credits

### AI Assistance

Parts of this project were generated with AI assistance:

- **DeepSeek**: Coding guidance, code generation, documentation optimization, language translation.
- **Yuanbao**: Coding guidance, code generation, language translation.
- **Tongyi Lingma**: Code completion, coding guidance.
- **WorkBuddy**: Code review, documentation optimization.
- **Trae**: Code generation, documentation optimization.
- **OpenCode**: Documentation optimization.

### Open Source

This project uses open source code. See [Open Source Notices (Chinese)](./docs/legal/os-notices.md) for details.

## More Documentation

- [Contribution Guidelines](./CONTRIBUTING.md)
- [Development (Chinese)](./docs/dev/index.md)
- [FAQ (Chinese)](./docs/faq.md)

[repository-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/
[repository-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/
[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[stargazers-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/stargazers

[workflow-test]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/workflows/test.yml

[pylauncher]: https://docs.python.org/zh-cn/3.15/using/windows.html#python-launcher-for-windows-deprecated
[pymanager]: https://docs.python.org/zh-cn/3.15/using/windows.html#python-install-manager
[windows-high-contrast-support]: https://support.microsoft.com/en-us/windows/turn-high-contrast-mode-on-or-off-in-windows-909e9d89-a0f9-a3a9-b993-7a6dcee85025
[rectify11]: https://www.rectify11.com/
[uv-homepage]: https://docs.astral.sh/uv/

[python/pymanager#216]: https://github.com/python/pymanager/issues/216
