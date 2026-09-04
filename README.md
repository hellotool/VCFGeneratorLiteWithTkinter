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

VCF Generator Lite is a simple and efficient application that converts contact lists into a single vCard (`.vcf`) file. Generated files can be batch-imported into mobile phone contacts or used for various other purposes.

Built with Python and Tkinter for a native desktop application.

[![License](https://img.shields.io/github/license/hellotool/VCFGeneratorLiteWithTkinter)](./LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](./CODE_OF_CONDUCT.md)

[![GitHub - Test](https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/workflows/test.yml/badge.svg)][workflow-test]
[![GitHub - Release](https://img.shields.io/github/v/release/hellotool/VCFGeneratorLiteWithTkinter?logo=github)][release-github]
![GitHub - Stars](https://img.shields.io/github/stars/hellotool/VCFGeneratorLiteWithTkinter?style=flat&logo=github)
[![Gitee - Stars](https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/badge/star.svg?theme=dark)][stargazers-gitee]

## Features

### Core Features

- **Smart Parsing**: Auto-recognizes and parses `Name Phone Notes` format; multiple spaces merged automatically.
- **Regional Support**: Covers phone number rules for Mainland China, Hong Kong, Macau, and Taiwan.
- **Editing Aids**: Built-in line numbers; one-click removal of cell quotes.
- **Number Validation**: Filters invalid numbers and jumps to the offending line for quick fixes.
- **Batch Export**: Merges all contacts into a single `.vcf` file.
- **Massive Scale**: Handles millions of contacts per run, limited only by available memory.

### UI & Interaction

- **Native Look**: Layout follows Windows 7 design guidelines, styled by the OS.
- **UI Scaling**: Auto-adapts to high DPI and system scaling, crisp on high-res displays.
- **Multi-Monitor Ready**: Child windows follow the parent and stay fully within the current display.
- **Multilingual**: Built-in Chinese and English UI, switching automatically with system language.

### Distribution, Licensing & Privacy

- **Extremely Lightweight**: Minimal dependencies, the Python ZIP app is under 100KB, download and run.
- **Completely Free**: All features free forever, no registration or payment.
- **Clean and Distraction-Free**: No ads, no bundles, no promotions.
- **No Disk Logs**: Logs go to stdout only, nothing is written to disk.
- **Open Source**: Licensed under Apache License 2.0, free to modify, distribute, and use commercially.

## Use Cases

- **Corporate Directory Distribution**: HR or admin staff bulk-import the company directory into employees' phones.
- **Event Participant Contacts**: Organizers of meetings, training, or team-building events quickly share attendee contacts.
- **Client Data Migration**: Sales and support staff bulk-migrate client contacts when switching phones or devices.
- **Data Migration**: Export contacts from Excel, legacy systems, or other formats to a new phone.
- **School-Home Contact Distribution**: Teachers or administrators share student and parent contacts for a class.

## Screenshots

<img src="./assets/images/screenshots/main_window.zh-CN.webp" width="451" alt="Main window" />
<img src="./assets/images/screenshots/invalid_lines_window.zh-CN.webp" width="362" alt="Invalid Lines Window" />

## Download and Installation

Download packages from the following channels:

- [Gitee Releases][release-gitee]
- [GitHub Releases][release-github]

Select a package for your platform and click the guide for detailed installation instructions:

| Platform       | Package Type           | Installation Required | File                                                      | Guide                                                                |
| -------------- | ---------------------- | --------------------- | --------------------------------------------------------- | -------------------------------------------------------------------- |
| Windows        | Installer              | Yes                   | VCFGeneratorLite-\<version\>-**win-amd64**-*setup.exe*    | [Windows Installer](./docs/guides/installation/windows-installer.md) |
| Windows        | Portable Package       | No                    | VCFGeneratorLite-\<version\>-**win-amd64**-*portable.zip* | [Windows Portable](./docs/guides/installation/windows-portable.md)   |
| Cross-platform | Python Wheel           | Optional              | vcf_generator_lite-\<version\>-**py3-none-any**.*whl*     | [Python Wheel](./docs/guides/installation/wheel.md)                  |
| Cross-platform | Python ZIP Application | No                    | VCFGeneratorLite-\<version\>-**py3**.*pyzw*               | [Python ZIP App](./docs/guides/installation/zipapp.md)               |

## Usage

1. Paste your contacts in the format `Name Phone Note` into the text box. The note is optional.
   ```text
   Qu Yuan		13333333333	Poet of the Warring States period
   Cao Cao		13444444444
   Tao Y.M.	13555555555
   Xie Lingyun	13666666666
   ```
2. Click **Generate**, select a path to save the file.
3. You can use the generated vCard file wherever you need it. See [Using vCard Files](./docs/guides/vcard-usage.md) for details.

For more information, see [User Documentation](./docs/index.md).

For system requirements, vCard compatibility, and known issues, see [Compatibility](./docs/reference/compatibility.md).

## Credits

### AI Assistance

Parts of this project were generated with AI assistance:

- **Trae**: Code generation, document optimization, code optimization, language translation  
- **Qoder**: Code completion, document optimization, coding guidance  
- **DeepSeek**: Coding guidance, code generation, document optimization, language translation  
- **Yuanbao**: Coding guidance, code generation, language translation  
- **WorkBuddy**: Code review, document optimization  
- **OpenCode**: Document optimization

## License

This project is licensed under the Apache 2.0 license. For details, please refer to the [LICENSE file](./LICENSE).

## Third-Party Notices

This project uses third-party open source code. For details, please refer to the [NOTICES file](./NOTICES.md).

## More Documentation

- [Contribution Guidelines](./CONTRIBUTING.md)
- [Development (Chinese)](./docs/dev/index.md)
- [User Documentation (Chinese)](./docs/index.md)

---

<div align="center">
Copyright © 2023-2026 Jesse205
</div>

[repository-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/
[repository-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/
[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[stargazers-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/stargazers

[workflow-test]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/workflows/test.yml
