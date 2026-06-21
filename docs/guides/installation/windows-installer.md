# Windows 安装程序

适用于大多数 Windows 用户，无需额外环境依赖。

**文件**：`VCFGeneratorLite-v<应用版本>-win-amd64-setup.exe`

您可以从 [Gitee 发行版][release-gitee] 或 [GitHub Releases][release-github] 下载。

## 安装步骤

1. 双击 `-setup.exe` 文件启动安装向导。
2. 按照提示选择安装路径和其他选项。
3. 点击 **安装**，等待安装完成。

> [!NOTE]
>
> 如果 Windows SmartScreen 弹出安全警告，请点击 **更多信息** → **仍要运行**。这是因为安装程序未经过代码签名。

## 启动

安装完成后，通过以下任一方式启动：

- 在 **开始菜单** 中搜索 `VCF 生成器 Lite` 并点击启动。
- 双击 **桌面快捷方式** 启动（需在安装时勾选创建）。

## 卸载

通过 **设置 > 应用 > 已安装的应用** 或 **控制面板 > 程序和功能** 卸载。

## 高级：静默安装

安装程序基于 InnoSetup 构建，支持 [命令行参数][innosetup-params]（如 `/SILENT`、`/DIR`），可用于自动化部署。

[release-gitee]: https://gitee.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[release-github]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/releases/latest
[innosetup-params]: https://jrsoftware.org/ishelp/index.php?topic=setupcmdline
