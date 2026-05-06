# 构建指南

## 前置要求

1. 完成[开发指南](./index.md)中的环境搭建。
2. 根据目标软件包类型，安装对应的额外工具。

## 构建命令

| 软件包类型       | 额外工具                                                          | 构建命令                     |
| ---------------- | ----------------------------------------------------------------- | ---------------------------- |
| Windows 安装程序 | [InnoSetup 6.6+][innosetup-homepage]、[UPX][upx-homepage]（可选） | `uv run poe build-installer` |
| Windows 便携包   | [UPX][upx-homepage]（可选）                                       | `uv run poe build-portable`  |
| Python ZIP 应用  | 无                                                                | `uv run poe build-zipapp`    |
| Python Wheel     | 无                                                                | `uv run poe build-wheel`     |

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
