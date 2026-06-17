# 构建指南

所有构建产物输出到 `dist/` 目录。

## 构建命令

- **构建安装程序**：`uv run poe build-installer`
  - `--force`：强制重建上游输出（PyInstaller 分发包）。
  - `--force-download`：强制联网下载 InnoSetup 扩展（即使本地已存在）。
  - `--no-verify-ssl`：下载扩展时不验证 SSL 证书。
- **构建便携包**：`uv run poe build-portable`
  - `--force`：强制重建上游输出（PyInstaller 分发包）。
- **构建 ZIP 应用**：`uv run poe build-zipapp`
  - `--force`：强制重建上游输出（Wheel）。
- **构建 Wheel**：`uv run poe build-wheel`

```bash
# 强制重建 PyInstaller 分发包后打包便携版
uv run poe build-portable --force

# 强制重建 Wheel 后打包 ZIP 应用
uv run poe build-zipapp --force

# 强制重建 PyInstaller 分发包 + 强制下载扩展后构建安装程序
uv run poe build-installer --force --force-download

# 只强制下载扩展（不强制重建上游）
uv run poe build-installer --force-download

# 下载扩展时不验证 SSL
uv run poe build-installer --no-verify-ssl
```

## 构建依赖

| 依赖                            | 适用类型         | 说明                        |
| ------------------------------- | ---------------- | --------------------------- |
| PyInstaller                     | 安装程序、便携包 | 通过 `uv sync` 自动安装     |
| [InnoSetup][innosetup-homepage] | 安装程序         | 需手动安装并添加到系统 PATH |
| zipapp                          | ZIP 应用         | Python 标准库，无需额外安装 |

[innosetup-homepage]: https://jrsoftware.org/isinfo.php
