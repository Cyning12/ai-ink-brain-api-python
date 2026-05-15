# -*- coding: utf-8 -*-
"""双人盲审 + 自动合并 + LLM 仲裁 + 可选仅人工 webhook。"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from typing import Any

from tools.rubric_review.config import ReviewRuntimeConfig
from tools.rubric_review.llm_backends import complete_json

logger = logging.getLogger(__name__)


@dataclass
class ReviewResult:
    dimension_scores: dict[str, int]
    justification: str
    model_used: str = ""


@dataclass
class FullReviewState:
    rubric: dict[str, Any]
    artifact_text: str
    review_a: ReviewResult
    review_b: ReviewResult
    final_scores: dict[str, int | None]
    arbitration_needed: bool
    arbitration_mode: str  # none | llm | human_pending
    arbitration_justification: str | None = None
    disputed_dimensions: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)


class DoubleBlindReviewer:
    """reviewer_models: (R1 模型, R2 模型, 仲裁模型)。siliconflow 下由 CLI 对池子洗牌后传入。"""

    def __init__(
        self,
        rubric: dict[str, Any],
        cfg: ReviewRuntimeConfig,
        *,
        reviewer_models: tuple[str, str, str],
        random_seed: int | None = None,
    ):
        self.rubric = rubric
        self.cfg = cfg
        self._model_r1, self._model_r2, self._model_arb = reviewer_models
        self._random_seed = random_seed
        rules = rubric.get("adjudication_rules") or {}
        self._max_diff = int(rules.get("max_score_diff_for_auto_accept", 1))
        self._auto_strategy = str(rules.get("auto_resolution_strategy", "average"))
        self._fallback = str(rules.get("fallback", "llm_arbiter"))

    def _meta_prologue(self) -> dict[str, Any]:
        return {
            "reviewer_r1_model": self._model_r1,
            "reviewer_r2_model": self._model_r2,
            "arbitration_model": self._model_arb,
            "random_seed": self._random_seed,
        }

    def _api_key(self) -> str:
        if self.cfg.backend == "siliconflow":
            k = self.cfg.siliconflow_api_key
            if not k:
                raise RuntimeError("缺少 SILICONFLOW_API_KEY（或与 api.rag_env.must_siliconflow_api_key 一致）")
            return k
        if self.cfg.backend == "openai":
            k = self.cfg.openai_api_key
        else:
            k = self.cfg.anthropic_api_key
        if not k:
            raise RuntimeError(
                f"缺少 API Key：请设置环境变量 "
                f"{'OPENAI_API_KEY' if self.cfg.backend == 'openai' else 'ANTHROPIC_API_KEY'}"
            )
        return k

    def _build_prompt(self, artifact: str) -> str:
        rubric_text = json.dumps(self.rubric, ensure_ascii=False, indent=2)
        smin = self.rubric["scoring"]["min"]
        smax = self.rubric["scoring"]["max"]
        dim_ids = [d["id"] for d in self.rubric["dimensions"]]
        return f"""你是一名不偏不倚的评审员。请仅依据下列 rubric 对「工件」逐项打分。

Rubric（JSON）：
{rubric_text}

工件正文：
---
{artifact}
---

输出要求：只输出一个 JSON 对象（不要 markdown 围栏），格式严格如下：
{{
  "dimension_scores": {{ {", ".join(f'"{k}": <int>' for k in dim_ids)} }},
  "justification": "对每个 dimension 简述给分依据（中文简洁）。"
}}
每个分数必须是 {smin} 到 {smax} 的整数，且每个 dimension 都必须出现。"""

    def _call_llm(self, artifact: str, run_label: str, model: str) -> ReviewResult:
        prompt = self._build_prompt(artifact)
        prompt2 = f"{prompt}\n\n[内部标签: reviewer={run_label}]\n"
        data = complete_json(
            backend=self.cfg.backend,
            api_key=self._api_key(),
            model=model,
            user_prompt=prompt2,
            max_retries=self.cfg.max_retries,
            retry_base_seconds=self.cfg.retry_base_seconds,
            siliconflow_base_url=self.cfg.siliconflow_base_url
            if self.cfg.backend == "siliconflow"
            else None,
        )
        scores = data.get("dimension_scores") or {}
        jus = str(data.get("justification") or "").strip()
        return ReviewResult(dimension_scores=scores, justification=jus, model_used=model)

    def double_blind_review(self, artifact: str) -> tuple[ReviewResult, ReviewResult]:
        logger.info("开始双人评审 R1=%s R2=%s", self._model_r1, self._model_r2)
        a = self._call_llm(artifact, "R1", self._model_r1)
        b = self._call_llm(artifact, "R2", self._model_r2)
        return a, b

    def _merge_auto(self, review_a: ReviewResult, review_b: ReviewResult) -> tuple[dict[str, int | None], list[str]]:
        final: dict[str, int | None] = {}
        disputed: list[str] = []
        for dim in self.rubric["dimensions"]:
            dim_id = dim["id"]
            sa = review_a.dimension_scores.get(dim_id)
            sb = review_b.dimension_scores.get(dim_id)
            if sa is None or sb is None:
                raise ValueError(f"缺少维度分数: {dim_id}")
            if abs(int(sa) - int(sb)) <= self._max_diff:
                if self._auto_strategy == "average":
                    final[dim_id] = round((int(sa) + int(sb)) / 2.0)
                elif self._auto_strategy == "min":
                    final[dim_id] = min(int(sa), int(sb))
                elif self._auto_strategy == "max":
                    final[dim_id] = max(int(sa), int(sb))
                else:
                    final[dim_id] = int(sa)
            else:
                final[dim_id] = None
                disputed.append(dim_id)
        return final, disputed

    def _arbitrate_llm(self, review_a: ReviewResult, review_b: ReviewResult, artifact: str) -> tuple[dict[str, int], str]:
        smin = self.rubric["scoring"]["min"]
        smax = self.rubric["scoring"]["max"]
        dim_ids = [d["id"] for d in self.rubric["dimensions"]]
        prompt = f"""你是仲裁员。两名评审对同一工件打分不一致。请阅读 rubric 摘要、工件与双方理由，为每个维度给出最终整数分数。

Rubric 名称：{self.rubric.get("rubric_name", "")}
分数范围：{smin}-{smax}
维度 id：{dim_ids}

工件：
---
{artifact}
---

评审 R1 分数：{json.dumps(review_a.dimension_scores, ensure_ascii=False)}
评审 R1 理由：{review_a.justification}

评审 R2 分数：{json.dumps(review_b.dimension_scores, ensure_ascii=False)}
评审 R2 理由：{review_b.justification}

只输出 JSON：{{ "dimension_scores": {{...全部维度...}}, "final_justification": "仲裁说明（中文）" }}"""
        logger.info("LLM 仲裁 model=%s", self._model_arb)
        data = complete_json(
            backend=self.cfg.backend,
            api_key=self._api_key(),
            model=self._model_arb,
            user_prompt=prompt,
            max_retries=self.cfg.max_retries,
            retry_base_seconds=self.cfg.retry_base_seconds,
            siliconflow_base_url=self.cfg.siliconflow_base_url
            if self.cfg.backend == "siliconflow"
            else None,
        )
        scores = {k: int(v) for k, v in (data.get("dimension_scores") or {}).items()}
        jus = str(data.get("final_justification") or "").strip()
        return scores, jus

    def run(
        self,
        artifact: str,
        *,
        arbitration_override: str | None = None,
    ) -> FullReviewState:
        """arbitration_override: None 跟随 rubric；'llm'；'human_webhook'。"""
        base_meta = self._meta_prologue()
        ra, rb = self.double_blind_review(artifact)
        partial, disputed = self._merge_auto(ra, rb)
        mode = "none"
        arb_jus: str | None = None

        override = (arbitration_override or "").strip().lower() or None
        eff_fallback = override or self._fallback
        if eff_fallback == "llm_arbiter_or_human":
            eff_fallback = "llm_arbiter"

        if not disputed:
            merged = {k: int(v) for k, v in partial.items() if v is not None}
            return FullReviewState(
                rubric=self.rubric,
                artifact_text=artifact,
                review_a=ra,
                review_b=rb,
                final_scores=merged,
                arbitration_needed=False,
                arbitration_mode=mode,
                disputed_dimensions=[],
                meta={**base_meta, "effective_fallback": eff_fallback},
            )

        if eff_fallback == "human_webhook":
            return FullReviewState(
                rubric=self.rubric,
                artifact_text=artifact,
                review_a=ra,
                review_b=rb,
                final_scores=partial,
                arbitration_needed=True,
                arbitration_mode="human_pending",
                arbitration_justification=None,
                disputed_dimensions=disputed,
                meta={
                    **base_meta,
                    "effective_fallback": eff_fallback,
                    "note": "争议维度未填终分，待人工 webhook 侧处理",
                },
            )

        mode = "llm"
        arb_scores, arb_jus = self._arbitrate_llm(ra, rb, artifact)
        final: dict[str, int | None] = {}
        for dim in self.rubric["dimensions"]:
            did = dim["id"]
            if partial.get(did) is not None:
                final[did] = int(partial[did])  # type: ignore[arg-type]
            else:
                if did not in arb_scores:
                    raise RuntimeError(f"LLM 仲裁输出缺少维度: {did}")
                final[did] = int(arb_scores[did])
        return FullReviewState(
            rubric=self.rubric,
            artifact_text=artifact,
            review_a=ra,
            review_b=rb,
            final_scores=final,  # type: ignore[arg-type]
            arbitration_needed=True,
            arbitration_mode=mode,
            arbitration_justification=arb_jus,
            disputed_dimensions=disputed,
            meta={**base_meta, "effective_fallback": eff_fallback},
        )
