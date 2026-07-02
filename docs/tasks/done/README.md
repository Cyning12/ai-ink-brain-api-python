# done/ · 已完成任务导航（Hub）

> **用途**：日常浏览 **只打开本文件**；`_views/done.md` 为薄指针。
> **真值**：各 task 文件头部 `状态` + `docs/tasks/done/`（或域子目录）物理位置。
> **P0 说明**：本 Hub 已按域分组，但物理文件仍扁平存放于 `done/`；P1 子 task 再分批 `git mv` 到 `done/<domain>/`。

---

## 域目录（domain）

| 域 slug | 说明 | 目录（P1 目标） |
|---------|------|----------------|
| `harness` | 本仓流程 / CI / 帽子 | `done/harness/` |
| `governance` | Wiki / 索引 / 治理线 | `done/governance/` |
| `chatbi` | ChatBI V2/V3 · unified chat | `done/chatbi/` |
| `engineering` | 图谱闸口 / RAG / 跨仓工程 | `done/engineering/` |
| `standards` | 编码规范 · api 模块化 Epic | `done/standards/` |
| `epics` | 母单 · MANIFEST · Loop | `done/epics/` |

**推断**：[`FRAGMENT_task_domain_infer_v1_zh.md`](../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)。

---
## harness（本仓流程 / CI / 帽子）

| 关账日 | task | freeze_id / 摘要 |
|--------|------|------------------|
| 2026-07-02 | [task_ops_session_s0_schema_v1.md](./task_ops_session_s0_schema_v1.md) | `OPS-SESSION-ORCH-SPEC-V1` · Session S0 schema · gate_sync · harness_runtime 骨架 |
| 2026-06-02 | [task_harness_invokes_by_task_prompts_sync_v1.md](./task_harness_invokes_by_task_prompts_sync_v1.md) | — |
| 2026-05-30 | [task_harness_p0_task_validate_v1.md](./task_harness_p0_task_validate_v1.md) | — |
| 2026-05-30 | [task_harness_p0_status_cursor_v1.md](./task_harness_p0_status_cursor_v1.md) | — |
| 2026-05-30 | [task_harness_p0_audit_selfcheck_v1.md](./task_harness_p0_audit_selfcheck_v1.md) | — |
| 2026-05-29 | [task_harness_theory_align_p1_v1.md](./task_harness_theory_align_p1_v1.md) | — |
| 2026-05-29 | [task_harness_theory_align_p0_v1.md](./task_harness_theory_align_p0_v1.md) | — |
| 2026-05-26 | [task_harness_workspace_taxonomy_promote_v1.md](./task_harness_workspace_taxonomy_promote_v1.md) | — |
| 2026-05-23 | [task_harness_p1_docs_consolidation_v1.md](./task_harness_p1_docs_consolidation_v1.md) | — |
| 2026-05-22 | [task_harness_in_repo_prompts_and_rules_v1.md](./task_harness_in_repo_prompts_and_rules_v1.md) | — |
| — | [task_harness_semi_auto_retirement_phase2_v1.md](./task_harness_semi_auto_retirement_phase2_v1.md) | — |
| — | [task_harness_kpi_v1_2_pilot_v1.md](./task_harness_kpi_v1_2_pilot_v1.md) | — |
| — | [task_harness_chain_orchestration_spec_v1.md](./task_harness_chain_orchestration_spec_v1.md) | — |

## governance（Wiki / 索引 / 治理线）

| 关账日 | task | freeze_id / 摘要 |
|--------|------|------------------|
| 2026-06-13 | [task_governance_tasks_done_index_hygiene_v1.md](./task_governance_tasks_done_index_hygiene_v1.md) | done 索引卫生治理 · Hub + 薄指针 + Wiki 链路同步 · PR #160 · `GOV-TASKS-DONE-HYGIENE@2026-06-13` |
| 2026-06-08 | [task_governance_kimi_harness_pilot_recentsync_v1.md](./task_governance_kimi_harness_pilot_recentsync_v1.md) | — |
| 2026-06-06 | [task_gov_docs_noise_p3_index_v1.md](./task_gov_docs_noise_p3_index_v1.md) | — |
| 2026-06-06 | [task_gov_docs_noise_p2_readorder_v1.md](./task_gov_docs_noise_p2_readorder_v1.md) | — |
| 2026-06-06 | [task_gov_docs_noise_p1_archived_v1.md](./task_gov_docs_noise_p1_archived_v1.md) | — |
| 2026-06-06 | [task_gov_docs_noise_p0_readme_v1.md](./task_gov_docs_noise_p0_readme_v1.md) | — |
| 2026-05-29 | [task_governance_wiki_t4_ops_v1.md](./task_governance_wiki_t4_ops_v1.md) | — |
| 2026-05-29 | [task_governance_wiki_milestone_acceptance_expand_v1.md](./task_governance_wiki_milestone_acceptance_expand_v1.md) | — |
| 2026-05-29 | [task_governance_task_schedule_wiki_bridge_v1.md](./task_governance_task_schedule_wiki_bridge_v1.md) | — |
| 2026-05-28 | [task_governance_wiki_unit_ab_closeout_v1.md](./task_governance_wiki_unit_ab_closeout_v1.md) | — |
| 2026-05-28 | [task_governance_wiki_t4_rollout_v1.md](./task_governance_wiki_t4_rollout_v1.md) | — |
| 2026-05-28 | [task_governance_wiki_ingest_batch_3_v1.md](./task_governance_wiki_ingest_batch_3_v1.md) | — |
| 2026-05-28 | [task_governance_wiki_docs_hygiene_v1.md](./task_governance_wiki_docs_hygiene_v1.md) | — |
| 2026-05-28 | [task_governance_l2_phase_c_impl_v1.md](./task_governance_l2_phase_c_impl_v1.md) | — |
| 2026-05-27 | [task_governance_wiki_t4_expand_v2.md](./task_governance_wiki_t4_expand_v2.md) | — |
| 2026-05-27 | [task_governance_wiki_ingest_batch_v1.md](./task_governance_wiki_ingest_batch_v1.md) | — |
| 2026-05-27 | [task_governance_wiki_ingest_batch_2_v1.md](./task_governance_wiki_ingest_batch_2_v1.md) | — |
| 2026-05-27 | [task_governance_wiki_ctx_ab_representative_v1.md](./task_governance_wiki_ctx_ab_representative_v1.md) | — |
| 2026-05-27 | [task_governance_wiki_agent_readorder_v1.md](./task_governance_wiki_agent_readorder_v1.md) | — |
| 2026-05-27 | [task_governance_t4_spec_active_v1.md](./task_governance_t4_spec_active_v1.md) | — |
| 2026-05-27 | [task_governance_l2_phase_c_design_v1.md](./task_governance_l2_phase_c_design_v1.md) | — |
| 2026-05-27 | [task_governance_l2_manifest_ci_v1.md](./task_governance_l2_manifest_ci_v1.md) | — |
| 2026-05-26 | [task_wiki_ctx_ab_v1.md](./task_wiki_ctx_ab_v1.md) | — |
| 2026-05-26 | [task_wiki_ctx_ab_multi_slug_v1.md](./task_wiki_ctx_ab_multi_slug_v1.md) | — |
| 2026-05-26 | [task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md](./task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md) | — |
| 2026-05-26 | [task_wiki_ctx_ab_multi_bq3_recheck_v1.md](./task_wiki_ctx_ab_multi_bq3_recheck_v1.md) | — |
| 2026-05-26 | [task_governance_wiki_spec_comparison_sync_v1.md](./task_governance_wiki_spec_comparison_sync_v1.md) | — |
| 2026-05-26 | [task_governance_wiki_bq3_spec_schedule_sync_v1.md](./task_governance_wiki_bq3_spec_schedule_sync_v1.md) | — |
| 2026-05-26 | [task_governance_recent_schedule_wiki_sync_v1.md](./task_governance_recent_schedule_wiki_sync_v1.md) | — |
| 2026-05-26 | [task_governance_loop_c2_verify_r2_index_sync_v1.md](./task_governance_loop_c2_verify_r2_index_sync_v1.md) | — |
| 2026-05-26 | [task_governance_loop_c2_verify_r1_schedule_draft_v1.md](./task_governance_loop_c2_verify_r1_schedule_draft_v1.md) | — |
| 2026-05-26 | [task_coding_wiki_t1c_test_archive_v1.md](./task_coding_wiki_t1c_test_archive_v1.md) | — |
| 2026-05-26 | [task_coding_wiki_schema_test_strategy_rule_v1.md](./task_coding_wiki_schema_test_strategy_rule_v1.md) | — |
| 2026-05-26 | [task_coding_wiki_pilot_v1.md](./task_coding_wiki_pilot_v1.md) | — |
| 2026-05-26 | [task_coding_wiki_ingest_test_strategy_v1.md](./task_coding_wiki_ingest_test_strategy_v1.md) | — |
| 2026-05-22 | [task_docs_tasks_reorg_move_v1.md](./task_docs_tasks_reorg_move_v1.md) | — |
| 2026-04-28 | [task_docs_truth_and_rag_unify_v1.md](./task_docs_truth_and_rag_unify_v1.md) | — |
| — | [task_governance_wiki_t4_r2_l0_align_v1.md](./task_governance_wiki_t4_r2_l0_align_v1.md) | — |
| — | [task_governance_wiki_t4_r1_pilot_v1.md](./task_governance_wiki_t4_r1_pilot_v1.md) | — |
| — | [task_governance_l2_r3_test_manifest_v1.md](./task_governance_l2_r3_test_manifest_v1.md) | — |

## chatbi（ChatBI V2/V3 · unified chat）

| 关账日 | task | freeze_id / 摘要 |
|--------|------|------------------|
| 2026-06-04 | [task_chatbi_intent_hints_step1_v1.md](./task_chatbi_intent_hints_step1_v1.md) | — |
| 2026-06-04 | [task_chatbi_graph_p0_foundation_v1.md](./task_chatbi_graph_p0_foundation_v1.md) | — |
| 2026-05-29 | [task_chatbi_v3_p2_resilience_rate_limit_v1.md](./task_chatbi_v3_p2_resilience_rate_limit_v1.md) | — |
| 2026-05-29 | [task_chatbi_v3_p2_resilience_circuit_breaker_v1.md](./task_chatbi_v3_p2_resilience_circuit_breaker_v1.md) | — |
| 2026-05-29 | [task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md](./task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md) | — |
| 2026-05-25 | [task_chatbi_v3_p2_resilience_health_ready_v1.md](./task_chatbi_v3_p2_resilience_health_ready_v1.md) | — |
| 2026-05-24 | [task_chatbi_v3_p2_resilience_v1.md](./task_chatbi_v3_p2_resilience_v1.md) | — |
| 2026-05-22 | [task_chatbi_v2_acceptance_runner_v1.md](./task_chatbi_v2_acceptance_runner_v1.md) | — |
| 2026-05-22 | [task_05_query_rewrite_observability.md](./task_05_query_rewrite_observability.md) | — |
| 2026-05-20 | [task_chatbi_v3_prompt_injection_guard_poc_v1.md](./task_chatbi_v3_prompt_injection_guard_poc_v1.md) | — |
| 2026-05-14 | [task_chatbi_v3_sql_ast_text2sql_gate_v1.md](./task_chatbi_v3_sql_ast_text2sql_gate_v1.md) | — |
| 2026-05-11 | [task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md](./task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) | — |
| 2026-05-11 | [task_chatbi_v2_rewrite_timeline_llm_prompt_capture_v1.md](./task_chatbi_v2_rewrite_timeline_llm_prompt_capture_v1.md) | — |
| 2026-05-11 | [task_chatbi_v2_incremental_sse_backend_v1.md](./task_chatbi_v2_incremental_sse_backend_v1.md) | — |
| 2026-05-11 | [task_chatbi_v2_docs_acceptance_archive_2026-05-11.md](./task_chatbi_v2_docs_acceptance_archive_2026-05-11.md) | — |
| 2026-05-11 | [task_chatbi_v2_agent_p1_behavior.md](./task_chatbi_v2_agent_p1_behavior.md) | — |
| 2026-05-06 | [task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md](./task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md) | — |
| 2026-04-30 | [task_unified_chat_router_trace_text2sql_exec_v1.md](./task_unified_chat_router_trace_text2sql_exec_v1.md) | — |
| 2026-04-30 | [task_unified_chat_router_observability_full_trace_v1.md](./task_unified_chat_router_observability_full_trace_v1.md) | — |
| 2026-04-30 | [task_unified_chat_router_evidence_observability_v1.md](./task_unified_chat_router_evidence_observability_v1.md) | — |
| 2026-04-30 | [task_unified_chat_router_evidence_event_v1.md](./task_unified_chat_router_evidence_event_v1.md) | — |
| 2026-04-29 | [task_chatbi_v2_agent_p0_backend.md](./task_chatbi_v2_agent_p0_backend.md) | — |
| 2026-04-29 | [done_chatbi_v2_agent_p0_backend_modules_intent_tools_memory.md](./done_chatbi_v2_agent_p0_backend_modules_intent_tools_memory.md) | — |
| 2026-04-29 | [done_chatbi_v2_agent_p0_backend_constraints_2026-04-29.md](./done_chatbi_v2_agent_p0_backend_constraints_2026-04-29.md) | — |
| 2026-04-28 | [done_unified_chat_streaming_backend_sse_v1.md](./done_unified_chat_streaming_backend_sse_v1.md) | — |
| 2026-04-28 | [done_unified_chat_backend_v1.md](./done_unified_chat_backend_v1.md) | — |
| — | [task_text2sql_schema_prefetch_before_mutate_v1.md](./task_text2sql_schema_prefetch_before_mutate_v1.md) | — |
| — | [task_portfolio_rag_demo_v1.md](./task_portfolio_rag_demo_v1.md) | — |
| — | [task_intent_router_backend_v1.md](./task_intent_router_backend_v1.md) | — |
| — | [task_chatbi_v3_text2sql_tool_latency_obs_v1.md](./task_chatbi_v3_text2sql_tool_latency_obs_v1.md) | — |
| — | [task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md](./task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md) | — |
| — | [task_chatbi_v3_lowconf_sql_preview_v1.md](./task_chatbi_v3_lowconf_sql_preview_v1.md) | — |
| — | [task_chatbi_v3_lowconf_rag_preview_v1.md](./task_chatbi_v3_lowconf_rag_preview_v1.md) | — |
| — | [task_chatbi_v2_text2sql_multiturn_grounding_v1.md](./task_chatbi_v2_text2sql_multiturn_grounding_v1.md) | — |
| — | [task_chatbi_v2_agent_p1d_intent_prompt_and_thresholds_v1.md](./task_chatbi_v2_agent_p1d_intent_prompt_and_thresholds_v1.md) | — |
| — | [task_chatbi_v2_agent_p1_eval_benchmark_v1.md](./task_chatbi_v2_agent_p1_eval_benchmark_v1.md) | — |
| — | [task_chatbi_text2sql_denial_final_answer_no_respin_v1.md](./task_chatbi_text2sql_denial_final_answer_no_respin_v1.md) | — |
| — | [task_chatbi_level_gate_v1.md](./task_chatbi_level_gate_v1.md) | — |
| — | [task_chatbi_intent_llm_retry_u1_5_v1.md](./task_chatbi_intent_llm_retry_u1_5_v1.md) | — |
| — | [task_chatbi_intent_hints_step2_v1.md](./task_chatbi_intent_hints_step2_v1.md) | — |
| — | [task_chatbi_baseline_merge_gate_v1.md](./task_chatbi_baseline_merge_gate_v1.md) | — |
| — | [done_chatbi_v2_agent_p0_backend_full_2026-04-29.md](./done_chatbi_v2_agent_p0_backend_full_2026-04-29.md) | — |

## engineering（图谱闸口 / RAG / 跨仓工程）

| 关账日 | task | freeze_id / 摘要 |
|--------|------|------------------|
| 2026-06-24 | [task_ops_desk_p2_langfuse_tracing_v1.md](./task_ops_desk_p2_langfuse_tracing_v1.md) | Ops Desk P2-5a · Langfuse tracing（Japan Cloud）· deep 路径 `@traceable` · `flush_traces()` · 生产默认关闭 · `OPS-DESK-KIMI-CODE-P2-LANGFUSE-TRACING` |
| 2026-06-22 | [task_ops_desk_p1_demo_cache_v1.md](./task_ops_desk_p1_demo_cache_v1.md) | Ops Desk P1-6 · Demo Cache `ops_demo_answers` · D1-D4 · fast hit / deep write-back · TTL 24h · `OPS-DESK-KIMI-CODE-P1-DEMO-CACHE` |
| 2026-06-21 | [task_ops_desk_p0_supabase_schema_v1.md](./task_ops_desk_p0_supabase_schema_v1.md) | Ops Desk P0-1 · Supabase 四表 DDL · rollback · pytest · `OPS-DESK-KIMI-CODE-P0-SUPABASE-SCHEMA` |
| 2026-06-17 | [task_engineering_graph_yaml_export_from_yaml_p1_v1.md](./task_engineering_graph_yaml_export_from_yaml_p1_v1.md) | Inform 闭环 P1 · graph.json export 改读 YAML · 单源闭环 · CI 不再依赖 `.ai.md` |
| 2026-06-16 | [task_engineering_graph_yaml_doc_hygiene_p0_v1.md](./task_engineering_graph_yaml_doc_hygiene_p0_v1.md) | Inform 闭环 P0 · Sub-graph 去 `.ai.md` 链 · QNA 幽灵节点 · pytest 防回归 |
| 2026-06-16 | [task_engineering_graph_yaml_post_epic_fix_v1.md](./task_engineering_graph_yaml_post_epic_fix_v1.md) | Post-Epic 修复 · `--all` · CI YAML · merge `f12e2a6` |
| 2026-06-16 | [task_engineering_graph_yaml_p0_00_main_v1.md](./task_engineering_graph_yaml_p0_00_main_v1.md) | 00_main YAML 图源试点 · KPI 88% · PR 待开 |
| 2026-06-06 | [task_rag_keyword_websearch_date_normalize_v1.md](./task_rag_keyword_websearch_date_normalize_v1.md) | — |
| 2026-06-06 | [task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md](./task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md) | — |
| 2026-06-06 | [task_rag_b2_fts_alias_backfill_v1.md](./task_rag_b2_fts_alias_backfill_v1.md) | — |
| 2026-06-06 | [task_rag_b1_metadata_structured_recall_v1.md](./task_rag_b1_metadata_structured_recall_v1.md) | — |
| 2026-06-06 | [task_03_hybrid_search_implementation.md](./task_03_hybrid_search_implementation.md) | — |
| 2026-06-06 | [Task 04.md](./Task 04.md) | — |
| 2026-05-21 | [task_engineering_tech_graph_gate_d_v2_tasks_v1.md](./task_engineering_tech_graph_gate_d_v2_tasks_v1.md) | — |
| 2026-05-20 | [task_engineering_tech_graph_gate_c_prime_f1_v1.md](./task_engineering_tech_graph_gate_c_prime_f1_v1.md) | — |
| 2026-05-20 | [task_engineering_tech_graph_gate_c_double_prime_v1.md](./task_engineering_tech_graph_gate_c_double_prime_v1.md) | — |
| 2026-05-19 | [task_engineering_tech_graph_v2_query_coverage_v1.md](./task_engineering_tech_graph_v2_query_coverage_v1.md) | — |
| 2026-05-18 | [task_engineering_tech_graph_scheme2_completion_v1.md](./task_engineering_tech_graph_scheme2_completion_v1.md) | — |
| 2026-05-18 | [task_engineering_tech_graph_gate_c_v2_dual_track_v1.md](./task_engineering_tech_graph_gate_c_v2_dual_track_v1.md) | — |
| 2026-05-17 | [task_engineering_tech_graph_v2_p4_extended_v1.md](./task_engineering_tech_graph_v2_p4_extended_v1.md) | — |
| 2026-05-17 | [task_engineering_tech_graph_v2_graph_query_v1.md](./task_engineering_tech_graph_v2_graph_query_v1.md) | — |
| 2026-05-15 | [task_engineering_tech_graph_graph_json_export_v1.md](./task_engineering_tech_graph_graph_json_export_v1.md) | — |
| 2026-05-15 | [task_engineering_tech_graph_gate_a_token_compare_v1.md](./task_engineering_tech_graph_gate_a_token_compare_v1.md) | — |
| 2026-05-15 | [task_engineering_tech_graph_gate_a_perf_compare_v1.md](./task_engineering_tech_graph_gate_a_perf_compare_v1.md) | — |
| 2026-05-15 | [task_engineering_chatbi_sse_first_v1.md](./task_engineering_chatbi_sse_first_v1.md) | — |
| 2026-04-27 | [task_tech_graph_p7_contract_ci_guardrail_v1.md](./task_tech_graph_p7_contract_ci_guardrail_v1.md) | — |
| 2026-04-27 | [task_tech_graph_p5_auto_render_from_manifest_v1.md](./task_tech_graph_p5_auto_render_from_manifest_v1.md) | — |
| 2026-04-27 | [task_tech_graph_p4_ci_guardrail_v1.md](./task_tech_graph_p4_ci_guardrail_v1.md) | — |
| 2026-04-27 | [task_tech_graph_p3_e2e_boundary_and_contract_v1.md](./task_tech_graph_p3_e2e_boundary_and_contract_v1.md) | — |
| 2026-04-24 | [task_rag_i18n_crosslingual_recall_v1.md](./task_rag_i18n_crosslingual_recall_v1.md) | — |
| — | [task_tech_graph_p6_cross_repo_contract_guardrail_v1.md](./task_tech_graph_p6_cross_repo_contract_guardrail_v1.md) | — |
| — | [task_tech_graph_p2_layered_views_and_failure_paths_v1.md](./task_tech_graph_p2_layered_views_and_failure_paths_v1.md) | — |
| — | [task_tech_graph_p1_manifest_and_validation_v1.md](./task_tech_graph_p1_manifest_and_validation_v1.md) | — |
| — | [task_tech_graph_p0_handoff_and_drift_check_v1.md](./task_tech_graph_p0_handoff_and_drift_check_v1.md) | — |
| — | [task_backend_improve_batch_a_p0_v1.md](./task_backend_improve_batch_a_p0_v1.md) | — |
| — | [README.md](./README.md) | — |

## standards（编码规范 · api 模块化 Epic）

| 关账日 | task | freeze_id / 摘要 |
|--------|------|------------------|
| — | [task_standards_backend_p3_p4_l3_ruff_v1.md](./task_standards_backend_p3_p4_l3_ruff_v1.md) | — |
| — | [task_standards_backend_l2_draft_v1.md](./task_standards_backend_l2_draft_v1.md) | — |
| — | [task_api_tools_registry_split_w7.md](./task_api_tools_registry_split_w7.md) | — |
| — | [task_api_intent_stack_split_w8.md](./task_api_intent_stack_split_w8.md) | — |
| — | [task_api_env_rag_env_consolidation_w1.md](./task_api_env_rag_env_consolidation_w1.md) | — |
| — | [task_api_agent_loop_split_w6.md](./task_api_agent_loop_split_w6.md) | — |

## epics（母单 · MANIFEST · Loop）

| 关账日 | Epic / MANIFEST / Loop | 域 | 子 task 索引 |
|--------|------------------------|------|--------------|
| 2026-06-06 | [task_governance_docs_noise_line_manifest_v1.md](./task_governance_docs_noise_line_manifest_v1.md) | governance | — |
| 2026-05-30 | [task_harness_p0_openspec_tdd_loop_v1.md](./task_harness_p0_openspec_tdd_loop_v1.md) | harness | — |
| 2026-05-29 | [task_chatbi_v3_p2_resilience_loop_v1.md](./task_chatbi_v3_p2_resilience_loop_v1.md) | chatbi | — |
| 2026-05-28 | [task_harness_wiki_loop_unit_a_v1.md](./task_harness_wiki_loop_unit_a_v1.md) | harness | — |
| 2026-05-27 | [task_harness_wiki_loop_p2_followup_v1.md](./task_harness_wiki_loop_p2_followup_v1.md) | harness | — |
| 2026-05-26 | [task_harness_wiki_loop_c2_verify_v1.md](./task_harness_wiki_loop_c2_verify_v1.md) | harness | — |
| 2026-05-26 | [task_harness_wiki_loop_bq3_recheck_v1.md](./task_harness_wiki_loop_bq3_recheck_v1.md) | harness | — |
| 2026-05-26 | [task_harness_wiki_loop_a1_a4_v1.md](./task_harness_wiki_loop_a1_a4_v1.md) | harness | — |
| — | [task_standards_backend_api_modularization_manifest_v1.md](./task_standards_backend_api_modularization_manifest_v1.md) | standards | — |
| — | [task_harness_wiki_loop_t4_l2_v1.md](./task_harness_wiki_loop_t4_l2_v1.md) | harness | — |
| — | [task_harness_semi_auto_retirement_manifest_v1.md](./task_harness_semi_auto_retirement_manifest_v1.md) | harness | — |

---

## 关账维护（checklist）

1. `git mv docs/tasks/active/<file>.md docs/tasks/done/<domain>/<file>.md`（P1 批量迁移时）
2. 头部 `> **状态**：done（YYYY-MM-DD 验收通过）`
3. **本 Hub** 对应域表 **追加一行**（日期 · 链接 · freeze_id 一行摘要）
4. **`_views/done_by_domain.md`** 同步追加
5. **禁止**向 `_views/done.md` 追加长列表（保持 ≤15 行薄指针）

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-13 | v1：域分组 Hub · 薄指针 · P0 物理路径仍扁平 |

## 给维护者

`done`、`domain`、`Hub`、`_views`、`freeze_id`、`Epic`

