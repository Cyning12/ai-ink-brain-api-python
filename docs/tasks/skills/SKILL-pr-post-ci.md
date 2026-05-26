# SKILL：PR 后 CI 监听 · 说明同步 · 条件合并（方案 C）

> **SKILL ID**：`pr-post-ci`  
> **SPEC**：[`docs/spec/governance/SPEC-Governance-PR-Post-CI-v1.md`](../../spec/governance/SPEC-Governance-PR-Post-CI-v1.md)  
> **自动化**：[`pr-post-ci.yml`](../../../.github/workflows/pr-post-ci.yml) · [`.mergify.yml`](../../../.mergify.yml) · [`tools/pr_post_ci_update_body.py`](../../../tools/pr_post_ci_update_body.py)

---

## 何时用

| 场景 | 用本 SKILL | 用 babysit（Cursor 全局） |
| --- | --- | --- |
| 开 PR / push 后刷新 body | ✅ | ✅ |
| CI 全绿后勾 Test plan | Bot 先做；人补 Summary | ✅ |
| 纯 docs + 打 `automerge` | Bot merge | ✅ |
| 含 `api/` 或评论/冲突 | ✅ 人 merge | ✅ |

---

## 硬约束

1. **禁止**在未 Required 全绿时 `gh pr merge`（除非用户明文）。  
2. **禁止** Agent 自行添加 `automerge` 标签（除非用户授权且 diff 无 `api/`、`tests/`、workflow）。  
3. **push 扩大范围后**必须更新 PR Summary（bot **不**写叙述性 Summary）。  
4. 多主题 squash PR 须 **分节 Summary**（见 PR #54 教训）。

---

## 教训 · PR #60（docs/wiki · 2026-05-26）

| 现象 | 根因 | 正确做法 |
| --- | --- | --- |
| **未 automerge** | PR **无** `automerge` 标签；PR checks 仅 Vercel，**无** `pytest` / `manifest_check` / `contract_check` success → Mergify 条件 M3 不满足 | docs-only 也要等三项 Required 全绿；**人**打 `automerge` 后由 Mergify **squash**（勿用 `gh pr merge --merge` 绕过） |
| **Test plan 未勾选** | `pr-post-ci` 仅在上述三项 **全绿且 PR 仍 OPEN** 时勾 `## Test plan`；合并过早或 Required 未挂上 PR 则 bot 不改 body | **全绿后、merge 前** 看 body 是否已出现 `## CI 状态（自动 · pr-post-ci）` 与已勾项；可本地 `python tools/pr_post_ci_update_body.py --pr <N>` |
| **「合入后」仍 `[ ]`** | 符合预期：含 **合入后** / **可选** 的条目 **不** 自动勾（SPEC §3.1） | Test plan 拆成「CI 项（可自动勾）」与「合入后验收（保留 `[ ]`）」 |

**时序（硬）**：

```text
push 定稿 → 等 pytest + manifest_check + contract_check 全绿
  → pr-post-ci 更新 body（Test plan + CI 表）
  → 人/Agent 补 Summary → （可选）人打 automerge
  → merge（Mergify squash 或人触发）
```

**禁止**：仅 Vercel 绿就 merge；合并后再指望 bot 改已关 PR 的 Test plan。

---

## 流程

```text
1. gh pr create（带 Summary + Test plan 模板）
2. push → 等待 CI（或 gh pr checks --watch）
3. Bot pr-post-ci 追加 CI 表 / 勾选项 / 变更统计
4. 人/Agent 对照 gh pr diff 刷新 Summary
5. 若 docs-only 且人打 automerge → Mergify squash
6. 否则 gh pr merge（人触发）
```

---

## 开 PR 模板（摘要）

```markdown
## Summary
- （人写）本 PR 主题 …
- （可选）依赖 / freeze_id …

## Test plan
- [ ] CI pytest 绿
- [ ] CI tech-graph manifest + contract 绿
- [ ] （业务向）…
```

**Bot 自动勾选**（Required 全绿且 PR 仍 open）：勾选 `## Test plan` 内 **不含** `合入后` / `automerge` / `Mergify` / `可选` 等词的 `- [ ]` 行；Mergify 是否真 merge、合入后验收 **保留 `[ ]`**（见 SPEC §3.1 · #56）。

---

## 本地命令

```bash
gh pr checks --watch
python tools/pr_post_ci_update_body.py --pr <N> --dry-run
python tools/pr_post_ci_update_body.py --pr <N>
gh pr edit <N> --body-file /tmp/body.md
```

---

## 前端仓镜像清单

复制 workflow/mergify 时修改：

| 项 | 后端本仓 | 前端 ai-ink-brain |
| --- | --- | --- |
| Required checks | pytest, manifest_check, contract_check | quality / lint-and-build 等 |
| 禁止 automerge 路径 | `api/` | `app/`、`components/`、`lib/` |
| 包管理 | requirements.txt | pnpm-lock.yaml |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-26 | v1：方案 C 落盘 |
| 2026-05-26 | v1.1：对齐 #56 修订（Test plan / CI 表 / 已关闭 PR） |
| 2026-05-26 | v1.2：教训 PR #60（全绿后 merge 前改 body · automerge 条件） |
