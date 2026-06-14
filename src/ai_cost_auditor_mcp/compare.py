from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from .cost import estimate_task_cost


def compare_model_cost(
    model_names: Iterable[str],
    prompt_tokens: int,
    completion_tokens: int = 0,
    pricing_overrides: Optional[Dict[str, Dict[str, float]]] = None,
) -> List[Dict[str, float]]:
    """Compare estimated cost across multiple LLM models.

    Args:
        model_names: List of canonical model names to compare.
        prompt_tokens: Number of prompt/input tokens.
        completion_tokens: Number of output tokens.
        pricing_overrides: Optional per-model override mapping.

    Returns:
        A sorted list of cost estimates by ascending total cost.
    """
    pricing_overrides = pricing_overrides or {}
    estimates = []

    for model_name in model_names:
        estimate = estimate_task_cost(
            model_name=model_name,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            pricing_override=pricing_overrides.get(model_name),
        )
        estimates.append(estimate)

    estimates.sort(key=lambda metric: metric["total_cost"])
    return estimates
