# Rubric 多轮示例

- **`multiround.example.json`**：三轮 `S0`/`S1`/`S2`，指向同目录下 `round_*.md` 与 **`min_rubric.json`**（2 维演示用，节省 token）。
- 在仓根执行：

```bash
python -m tools.rubric_review.multi_round \
  --manifest tools/rubric_review/examples/multiround.example.json \
  --random-seed 42
```

默认输出在 **`docs/diary/jsonPKmermaid/rubric_runs/`**（可用 `--output-dir` 覆盖）。

生产环境可将 `rubric` 改为指向你维护的完整 Rubric（路径相对 manifest 文件所在目录填写）。
