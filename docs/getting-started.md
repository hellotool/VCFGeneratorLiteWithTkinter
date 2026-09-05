# 快速开始

本文介绍如何下载、安装 VCF 生成器 轻量版，并生成您的第一个 vCard 文件。

## 下载与安装

通过以下渠道下载软件包：

- [Gitee 发行版][release-gitee] — 推荐中国大陆用户使用
- [GitHub Releases][release-github]

根据您的系统环境和需求选择合适的软件包，点击对应指南查看详细的安装和启动方法：

| 平台    | 软件包类型       | 需要安装 | 文件                                                        | 指南                                                           |
| ------- | ---------------- | -------- | ----------------------------------------------------------- | -------------------------------------------------------------- |
| Windows | 安装程序（推荐） | 是       | VCFGeneratorLite-v\<应用版本\>-**win-amd64**--*setup.exe*   | [Windows 安装程序](./guides/installation/windows-installer.md) |
| Windows | 便携包           | 否       | VCFGeneratorLite-v\<应用版本\>-**win-amd64**-*portable.zip* | [Windows 便携包](./guides/installation/windows-portable.md)    |
| 跨平台  | Python Wheel     | 可选     | vcf_generator_lite-\<应用版本\>-**py3-none-any**.*whl*      | [Python Wheel](./guides/installation/wheel.md)                 |
| 跨平台  | Python ZIP 应用  | 否       | VCFGeneratorLite-v\<应用版本\>-**py3**.*pyzw*               | [Python ZIP 应用](./guides/installation/zipapp.md)             |

> [!TIP]
>
> 请查阅 [兼容性](./reference/compatibility.md) 了解系统要求。

## 生成第一个 vCard 文件

1. 启动应用，进入主窗口。
2. 按 `姓名 电话 备注` 的格式，将联系人复制到文本框中（每行一个联系人）。详见 [输入格式规范](./reference/input-format.md)：
   ```text
   屈原	13333333333	战国时期诗人
   曹操	13444444444
   陶渊明	13555555555
   谢灵运	13666666666
   ```
   > [!TIP]
   >
   > 如果您需要从 Excel 工作簿导入联系人数据，请参阅 [导入联系人](./guides/import-contacts.md)。
3. 点击 **开始生成** 按钮，选择保存路径。
4. 等待生成完成。如有无法识别的条目，应用会弹出无效条目窗口提示您修正。
5. 将生成的 `.vcf` 文件传输到目标设备或服务。

## 后续步骤

- 学习 [使用 vCard 文件](./guides/vcard-usage.md)，将生成的文件导入到各类设备和服务。
- 阅读 [应用功能](./reference/functions.md) 了解完整功能。
- 遇到问题时查阅 [常见问题](./troubleshooting/faq.md)。

[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
