from __future__ import annotations

from typing import Dict


def detect_token_waste(
    prompt_tokens: int,
    completion_tokens: int,
    ideal_prompt_ratio: float = 0.55,
    waste_threshold: float = 0.15,
) -> Dict[str, object]:
    """Detect token inefficiencies in prompt and output usage.

    This helper is intended to flag when token usage is unexpectedly imbalanced.
    It is useful for auditing prompt design and model selection.

    Args:
        prompt_tokens: Number of input tokens sent to the model.
        completion_tokens: Number of output tokens received from the model.
        ideal_prompt_ratio: Target ratio of prompt tokens compared to total tokens.
        waste_threshold: Tolerance before reporting token waste.

    Returns:
        A dict with the computed ratios and potential waste guidance.
    """
    if prompt_tokens < 0 or completion_tokens < 0:
        raise ValueError("Token counts must be non-negative integers.")

    total_tokens = max(1, prompt_tokens + completion_tokens)
    prompt_ratio = prompt_tokens / total_tokens
    completion_ratio = completion_tokens / total_tokens

    prompt_overuse = max(0.0, prompt_ratio - ideal_prompt_ratio)
    completion_overuse = max(0.0, completion_ratio - (1 - ideal_prompt_ratio))

    issues = []
    if prompt_overuse > waste_threshold:
        issues.append(
            "Prompt tokens represent a larger-than-expected portion of total usage."
        )
    if completion_overuse > waste_threshold:
        issues.append(
            "Completion tokens represent a larger-than-expected portion of total usage."
        )
    if not issues:
        issues.append("Token usage appears balanced for the selected ratio.")

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "prompt_ratio": round(prompt_ratio, 4),
        "completion_ratio": round(completion_ratio, 4),
        "issues": issues,
        "waste_threshold": waste_threshold,
        "ideal_prompt_ratio": ideal_prompt_ratio,
    }
