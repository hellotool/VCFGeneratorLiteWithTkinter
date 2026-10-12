# 0008 发布产物生成 GitHub 溯源声明

- 状态: 已采纳
- 日期: 2026-10-12

## 背景

四种产物经 GitHub Release 与 Gitee 两处分发，下载方此前无法确认手里的文件确实出自本仓库的构建，只能凭信任。GitHub 的 artifact attestations 可为产物签发可公开校验的构建溯源（[Artifact attestations][ref-artifact-attestations]）。

本项目自身的三条约束决定落点：

- 溯源由产生该文件的那次 run 签发才有意义，事后在别处补签等于白签。
- `build.yml` 有两个入口——独立 `workflow_dispatch` 与 `prepare-release.yml` 的 `workflow_call`——两边都得能签。
- 四种产物按输入开关分别构建，签名步骤碰到不存在的文件即失败，不能合并成每 job 一步。

## 决策

在 `build.yml` 里为四种产物各加一步 `actions/attest@v4`，紧跟对应的构建步骤；同时开启仓库的不可变发布（[Immutable releases][ref-immutable-releases]），把"发布即定版"从流程习惯变成平台强制。要点：

- 权限块在 `build.yml` 顶层与 `prepare-release.yml` 的 `build-apps` job 各写一份且内容相同——被调用方能拿到的范围只能是调用方授予范围的子集。
- 不在 release job 里签，不签测试构建。
- 不可变发布只对开启之后的发布生效：v6.0.2 草稿上的资产起初没有构建溯源，是靠重跑 Prepare Release 覆盖上传才拿到声明，而发布时已处于不可变模式下，于是同时生成了发布声明。
- 不做 SBOM，不生成 `SHA256SUMS` 校验和文件。

## 后果

- 收益：产物可核对签名者的仓库与 workflow 身份；声明按文件名与摘要绑定，Gitee 上的同字节副本同样能在 GitHub 侧验真。
- 代价：权限块两处重复，新增产物或调整 caller 时容易漏改一侧。两处漏配的暴露方式不一样——缺 `id-token` 会让签发步骤直接失败并提示补权限，缺 `artifact-metadata` 只落在一条 warning 上。
- 代价：调试用的 `workflow_dispatch` 构建同样会写入公开透明度日志，而声明一经删除，已分发的产物就永久无法通过验证。
- 不可逆：已发布版本的资产不能改也不能删，只能整条删除 Release，且删除后同名 tag 不可复用。"撤下 v6.0.2 再原样重发 v6.0.2"这条路已被封死，回滚手册里的"删除后重触发"从此只对草稿成立。
- 门槛：核验需要 GitHub CLI 且需访问 GitHub，签名发生在 reusable workflow 里，命令必须额外指定签名者；GitHub 在非交互终端下不打印结果，判据只有退出码或 `--format json`。发布页的 `Verified` 绿标说的是提交签名，不是产物溯源。
- 实测（2026-10-13 复验）：v6.0.2 由 [run 38272760592][ref-prod-run] 经 `workflow_call` 调用 `build.yml` 构建发布。四种产物各有一条 `https://slsa.dev/provenance/v1` 声明，`builder.id` 为 `build.yml@refs/heads/master`、`runner_environment` 为 `github-hosted`；`gh attestation verify` 对四个文件退出码均为 0，对追加一字节的同名副本为 1；从 Gitee 重新下载的四个同名同字节文件同样通过，摘要与 GitHub 侧声明一致。
- 实测：因不可变发布已生效，发布时另生成一条 `https://in-toto.io/attestation/release/v0.2` 声明，`gh release verify v6.0.2` 可读出该 tag 的提交与四个资产的摘要清单；它与构建溯源是两种声明，一个锁定发布内容，一个证明构建来源。
- 仍未实测：省略 `artifact-metadata: write` 是否可行（目前按 README 要求全量授予，缺失只会产生 warning）。

[ref-artifact-attestations]: https://docs.github.com/en/actions/concepts/security/artifact-attestations
[ref-immutable-releases]: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases
[ref-prod-run]: https://github.com/hellotool/VCFGeneratorLiteWithTkinter/actions/runs/38272760592
