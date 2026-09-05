# 构建指南

本文介绍如何构建项目的四种发布包。所有构建产物输出到 `dist/` 目录。

## 前置条件

在构建之前，请确保已完成开发环境搭建（参见 [快速上手](./getting-started.md)），并根据目标产物确认以下依赖：

| 依赖                            | 适用产物         | 安装方式                                   |
| ------------------------------- | ---------------- | ------------------------------------------ |
| PyInstaller                     | 安装程序、便携包 | `uv sync` 自动安装。                       |
| [InnoSetup][innosetup-homepage] | 安装程序         | 手动安装并添加到系统 PATH。                |
| InnoSetup 中文简体语言文件      | 安装程序         | 首次构建安装程序时自动下载，无需手动准备。 |
| zipapp                          | ZIP 应用         | Python 标准库，无需额外安装。              |

## 构建产物

| 产物             | 文件名格式                                            | 运行平台 |
| ---------------- | ----------------------------------------------------- | -------- |
| Windows 安装程序 | `VCFGeneratorLite-v{version}-{platform}-setup.exe`    | Windows  |
| Windows 便携包   | `VCFGeneratorLite-v{version}-{platform}-portable.zip` | Windows  |
| Python Wheel     | `vcf_generator_lite-{version}-py3-none-any.whl`       | 跨平台   |
| Python ZIP 应用  | `VCFGeneratorLite.pyzw`                               | 跨平台   |

其中 `{version}` 为项目当前版本号，`{platform}` 为构建平台标识（如 `win-amd64`、`win-arm64`）。

## 构建命令

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

# 强制重建 PyInstaller 分发包 + 强制下载扩展后构建安装程序
uv run poe build-installer --force --force-download

# 只强制下载扩展（不强制重建上游）
uv run poe build-installer --force-download

# 下载扩展时不验证 SSL
uv run poe build-installer --no-verify-ssl

# 强制重建 Wheel 后打包 ZIP 应用
uv run poe build-zipapp --force
```

## CI/CD

构建流程集成了 GitHub Actions（`.github/workflows/`）：

- **`build.yml`**：构建四种产物，可手动触发或在发布流程中被调用。
- **`prepare-release.yml`**：自动执行测试、构建、上传产物并创建草稿 Release。

本地构建与 CI 使用相同的 Poe 命令，构建行为一致。详细的发布步骤参见 [发布流程](./release/release-process.md)。

[innosetup-homepage]: https://jrsoftware.org/isinfo.php
