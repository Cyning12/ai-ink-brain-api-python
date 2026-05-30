# PROMPT LOOP · 22 → 关账（单 round · 可跨 Loop 复用）

> **用法**：替换 `{{ROUND}}`、`{{TASK_PATH}}`、`{{TASK_SLUG}}`、`{{VERIFY_COMMAND}}`

---

## §3 可复制 Prompt 正文

```text
Harness Loop 单 round 执行（p0-openspec-tdd · round={{ROUND}}）

真值：
- task：{{TASK_PATH}}
- LOOP_MANIFEST：docs/harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md
- git_branch：task/harness-p0-openspec-tdd
- verify：{{VERIFY_COMMAND}}

顺序：22 R1 → 30 → 40 → 50（若 task required）→ 关账 git mv done/

开帽：落盘 docs/harness/invokes/by-task/{{TASK_SLUG}}/invoke_*_22_*.md

扫描 human_gate；pending 则拒开工并输出 gate_id。

禁止：再开 10 帽；越界改非本 round 范围。
```
