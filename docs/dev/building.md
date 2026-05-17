# 构建指南

## 前置要求

1. 完成[开发指南](./index.md)中的环境搭建。
2. 根据目标软件包类型，安装对应的额外工具。

## 构建命令

- **构建安装程序**：`uv run poe build-installer`
  - `--force`：强制重建上游输出（PyInstaller 分发包）
  - `--force-download`：强制联网下载 InnoSetup 扩展（即使本地已存在）
  - `--no-verify-ssl`：下载扩展时不验证 SSL 证书
- **构建便携包**：`uv run poe build-portable`
  - `--force`：强制重建上游输出（PyInstaller 分发包）
- **构建 ZIP 应用**：`uv run poe build-zipapp`
  - `--force`：强制重建上游输出（Wheel）
- **构建 Wheel**：`uv run poe build-wheel`

### 额外工具

- [InnoSetup 6.6+][innosetup-homepage]：构建 Windows 安装程序
- [UPX][upx-homepage]（可选）：构建 Windows 安装程序、Windows 便携包

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

## 版本管理

```bash
# 设置指定版本
uv version 1.2.3

# 更新补丁版本并标记为开发版本
uv version --bump patch --bump dev

# 标记为稳定版本
uv version --bump stable
```

详细的版本命名规范请参阅[版本管理规范](./versioning.md)。

[innosetup-homepage]: https://jrsoftware.org/isinfo.php
[upx-homepage]: https://upx.github.io/
