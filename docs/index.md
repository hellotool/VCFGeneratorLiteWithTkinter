# VCF 生成器 Lite 文档

VCF 生成器 Lite 是一款简单高效的桌面工具，可将联系人列表批量转换为 vCard（`.vcf`）文件，便于导入手机通讯录、邮箱或其他通讯录应用。

```mermaid
graph LR
    A[Excel] --> D[VCF 生成器 Lite]
    B[微信/邮件] --> D
    C[网页/其他] --> D
    D --> E[.vcf 文件]
    E --> F[手机通讯录]
    E --> G[QQ 邮箱/Outlook]
    E --> H[飞书/其他]
```

## 入门教程

- [快速开始](./getting-started.md) — 下载、安装与第一次使用

## 操作指南

- [安装与启动](./guides/installation/index.md) — 各软件包类型的安装和启动方法
- [导入联系人](./guides/import-contacts.md) — 将联系人数据导入到应用中
- [使用 vCard 文件](./guides/vcard-usage.md) — 将生成的 vCard 文件导入到各类设备和服务

## 参考文档

- [应用功能](./reference/functions.md) — 应用提供的功能和选项
- [命令行参数](./reference/command-line.md) — 命令行启动时的参数说明
- [快捷键速查](./reference/shortcuts.md) — 各平台快捷键一览表
- [输入格式规范](./reference/input-format.md) — 联系人输入格式的详细说明
- [兼容性](./reference/compatibility.md) — 系统要求、vCard 兼容性与已知问题

## 故障排除

- [常见问题](./troubleshooting/faq.md) — 使用过程中的常见疑问
- [在旧版 Windows 中运行](./troubleshooting/runs-on-older-windows.md) — Windows 8 及更早版本的运行方案

## 开发者

如果您希望参与开发、翻译或了解项目架构，请阅读 [开发者文档](./dev/index.md)。

## 反馈与支持

- [GitHub Discussions][discussions-github] — 技术交流与讨论
- [GitHub Issues][issues-github] — 报告问题或提交建议
- [Gitee Issues][issues-gitee] — 报告问题或提交建议（国内用户推荐）

## 许可证

本项目基于 Apache License 2.0 开源。第三方依赖的许可证信息请参阅 [NOTICES](../NOTICES.md) 文件。

[discussions-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/discussions
[issues-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/issues
[issues-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/issues
