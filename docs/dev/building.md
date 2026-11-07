# 构建指南

本文介绍如何构建项目的四种发布包。所有构建产物输出到 `dist/` 目录。

## 构建产物

请确认您需要构建的产物：

| 产物             | 运行平台 | 文件名格式                                            |
| ---------------- | -------- | ----------------------------------------------------- |
| Windows 安装程序 | Windows  | `VCFGeneratorLite-v{version}-{platform}-setup.exe`    |
| Windows 便携包   | Windows  | `VCFGeneratorLite-v{version}-{platform}-portable.zip` |
| Python Wheel     | 跨平台   | `vcf_generator_lite-{version}-py3-none-any.whl`       |
| Python ZIP 应用  | 跨平台   | `VCFGeneratorLite-v{version}-py3.pyzw`                |

其中 `{version}` 为项目当前版本号，`{platform}` 为构建平台标识（如 `win-amd64`、`win-arm64`）。

## 前置条件

在构建之前，请确保已完成开发环境搭建（参见 [快速上手](./getting-started.md)），并根据目标产物确认以下依赖：

| 依赖                                            | 适用产物         | 安装方式                                          |
| ----------------------------------------------- | ---------------- | ------------------------------------------------- |
| [PyInstaller][pyinstaller-homepage]             | 安装程序、便携包 | `uv sync` 自动安装。                              |
| [InnoSetup][innosetup-homepage]                 | 安装程序         | 手动安装并添加到系统 PATH。                       |
| [InnoSetup 简体中文语言文件][innosetup-chinese] | 安装程序         | 初始化 Git 子模块： `git submodule update --init` |
| zipapp                                          | ZIP 应用         | Python 标准库，无需额外安装。                     |

## 构建命令

执行以下命令构建目标产物：

### 构建安装程序

```bash
uv run poe build-installer
```

构建 Windows 安装程序（`.exe`）。此命令会先通过 PyInstaller 打包应用，再调用 InnoSetup 编译安装程序。

可用参数：

| 参数               | 说明                                            |
| ------------------ | ----------------------------------------------- |
| `--force`          | 强制重建 PyInstaller 分发包（即使已存在）。     |
| `--force-download` | 强制重新下载 InnoSetup 扩展（即使本地已存在）。 |
| `--no-verify-ssl`  | 下载扩展时不验证 SSL 证书。                     |

### 构建便携包

```bash
uv run poe build-portable
```

构建 Windows 便携包（`.zip`）。此命令会先通过 PyInstaller 打包应用，再压缩为 ZIP。

可用参数：

| 参数      | 说明                                        |
| --------- | ------------------------------------------- |
| `--force` | 强制重建 PyInstaller 分发包（即使已存在）。 |

### 构建 ZIP 应用

```bash
uv run poe build-zipapp
```

构建 Python ZIP 应用（`.pyzw`）。此命令会先构建 Wheel，再将 Wheel 包与其依赖打包为 ZIP 应用。

可用参数：

| 参数      | 说明                           |
| --------- | ------------------------------ |
| `--force` | 强制重建 Wheel（即使已存在）。 |

### 构建 Wheel

```bash
uv run poe build-wheel
```

构建标准 Python Wheel 包。

## 构建依赖链

各构建命令之间存在上下游依赖关系：

```txt
build-installer ──→ PyInstaller ──→ 源码
build-portable  ──→ PyInstaller ──→ 源码
build-zipapp    ──→ Wheel       ──→ 源码
build-wheel     ──→ 源码
```

默认情况下，如果上游产物已存在，构建命令会跳过重复构建。使用 `--force` 可强制重建上游产物。例如：

```bash
# 强制重建 PyInstaller 分发包后打包便携版
uv run poe build-portable --force

# 强制重建 PyInstaller 分发包后构建安装程序
uv run poe build-installer --force

# 强制重建 Wheel 后打包 ZIP 应用
uv run poe build-zipapp --force
```

## CI/CD

构建流程集成了 GitHub Actions（`.github/workflows/`）：

- **`build.yml`**：构建四种产物，可手动触发或在发布流程中被调用，并为每种产物生成溯源声明。
- **`prepare-release.yml`**：自动执行测试、构建、上传产物并创建草稿 Release。

本地构建与 CI 使用相同的 Poe 命令，产出的文件内容一致；差别在于溯源声明只能由 GitHub Actions 用作业身份签发，本地构建不产生声明。详细的发布步骤参见 [发布流程](./release/release-process.md)。

[innosetup-homepage]: https://jrsoftware.org/isinfo.php
[innosetup-chinese]: https://github.com/kira-96/Inno-Setup-Chinese-Simplified-Translation
[pyinstaller-homepage]: https://pyinstaller.org/
