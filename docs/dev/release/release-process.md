# 发布流程

## 概述

发布流程主要在 GitHub Actions 中执行（`.github/workflows/`）：

- **`test.yml`**：在 push 与 PR 时运行测试与代码检查。
- **`build.yml`**：手动触发（`workflow_dispatch`）或在发布流程中被调用，构建四种产物。
- **`prepare-release.yml`**：手动触发，自动构建、上传产物并创建/更新草稿 Release。

发布产物共有四种：

| 产物             | 运行平台 |
| ---------------- | -------- |
| Windows 安装程序 | Windows  |
| Windows 便携包   | Windows  |
| Python Wheel     | 跨平台   |
| Python ZIP 应用  | 跨平台   |

## 发布步骤

### 1. 准备阶段

1. **更新版本号**：根据变更规模选择合适的版本号。详情请参见 [版本管理规范](./versioning.md)。
2. **更新变更日志**：在 `CHANGELOG.md` 与 `CHANGELOG.zh-CN.md` 中新增版本，合并并翻译变更日志。
3. **同步本地化**：若新引入了可翻译字符串，请运行：
   ```bash
   uv run poe l10n-extract
   uv run poe l10n-update
   uv run poe l10n-compile
   ```
4. **本地自检**：
   ```bash
   uv run poe format
   uv run poe check
   uv run poe test
   ```

### 2. 提交与合并

创建 `release/<version>` 分支，合并上述更改到该分支，在推送到 GitHub 后，CI 会自动进行测试。

实践中，为了极致地节省 Runner 资源，您可以直接将提交推送到 `master` 分支。

### 3. 触发 Prepare Release 工作流

在 GitHub 上：

1. 进入 **Actions** 标签页。
2. 选择 **Prepare Release** 工作流。
3. 点击 **Run workflow**。
4. 选择您要创建新版本的分支。
5. 等待工作流完成（约 5-15 分钟，取决于队列）。

工作流会：

- 读取 `uv version --short` 作为目标版本。
- 运行测试与四种产物的构建。
- 若是新版本，创建草稿 Release 并上传产物。
- 若是已存在的草稿 Release，将产物覆盖上传。
- 若是已发布的 Release，则报错并退出。

### 4. 编辑草稿 Release

1. 进入 **Releases** 页面，找到新建的草稿。
2. 编辑 Release Notes，根据 `CHANGELOG.md` 对应版本的内容做微调（例如修改标题级别）。
3. 如果是 `a` / `b` / `rc` / `dev` 版本，勾选 **Set as a pre-release**。
4. 点击 **Publish release**。

### 5. 同步发布

在发布到 GitHub 后，需要同步发布到 Gitee：

1. 在 Gitee 上同步 GitHub 仓库。
2. 在 GitHub 上下载对应的构建产物。
3. 在 Gitee 上根据标签、构建产物和 `CHANGELOG.zh-CN.md` 发布发行版。

## 回滚策略

发布前请确认：

- 草稿 Release 内容是否完整。
- 是否需要先以 pre-release 形式发布以收集反馈。
- 在 GitHub Actions 中可使用 `gh release delete <tag>` 删除草稿并重新触发。

如需紧急修复：

1. 修复源码并按 [语义化版本][semver-spec] 提升 patch 版本号。
2. 走完整发布流程发布新版本。
3. 在旧 Release 中追加说明，引导用户升级。

[semver-spec]: https://semver.org/spec/v2.0.0.html
