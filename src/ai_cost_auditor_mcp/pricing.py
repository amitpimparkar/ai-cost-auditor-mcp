from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class ModelPricing:
    provider: str
    model_name: str
    input_cost_per_1k: float
    output_cost_per_1k: float

    def format(self) -> str:
        return f"{self.provider}/{self.model_name}: input ${self.input_cost_per_1k:.6f}/1k, output ${self.output_cost_per_1k:.6f}/1k"


DEFAULT_MODEL_PRICING: Dict[str, ModelPricing] = {
    "openai/gpt-4.1": ModelPricing(
        provider="openai",
        model_name="gpt-4.1",
        input_cost_per_1k=0.003,  # example published pricing; update from provider docs
        output_cost_per_1k=0.004,  # example published pricing
    ),
    "openai/gpt-3.5-turbo": ModelPricing(
        provider="openai",
        model_name="gpt-3.5-turbo",
        input_cost_per_1k=0.0015,
        output_cost_per_1k=0.002,
    ),
    "gemini/gemini-pro": ModelPricing(
        provider="gemini",
        model_name="gemini-pro",
        input_cost_per_1k=0.0021,
        output_cost_per_1k=0.0028,
    ),
    "gemini/gemini-1.5-pro": ModelPricing(
        provider="gemini",
        model_name="gemini-1.5-pro",
        input_cost_per_1k=0.0014,
        output_cost_per_1k=0.0019,
    ),
    "mistral/mistral-large": ModelPricing(
        provider="mistral",
        model_name="mistral-large",
        input_cost_per_1k=0.0025,
        output_cost_per_1k=0.0035,
    ),
    "mistral/mistral-small": ModelPricing(
        provider="mistral",
        model_name="mistral-small",
        input_cost_per_1k=0.0012,
        output_cost_per_1k=0.0017,
    ),
    "anthropic/claude-3.5": ModelPricing(
        provider="anthropic",
        model_name="claude-3.5",
        input_cost_per_1k=0.0018,
        output_cost_per_1k=0.0024,
    ),
    "anthropic/claude-2.1": ModelPricing(
        provider="anthropic",
        model_name="claude-2.1",
        input_cost_per_1k=0.0011,
        output_cost_per_1k=0.0016,
    ),
}


def get_model_pricing(model_name: str, override: Optional[Dict[str, float]] = None) -> ModelPricing:
    """Return pricing metadata for a known model, optionally applying overrides.

    Args:
        model_name: A canonical model key such as "openai/gpt-4.1".
        override: Optional pricing overrides for input and output cost.

    Raises:
        KeyError: If the model is not listed in DEFAULT_MODEL_PRICING.
    """
    normalized = model_name.strip().lower()
    pricing = DEFAULT_MODEL_PRICING[normalized]

    if override is None:
        return pricing

    return ModelPricing(
        provider=pricing.provider,
        model_name=pricing.model_name,
        input_cost_per_1k=override.get("input_cost_per_1k", pricing.input_cost_per_1k),
        output_cost_per_1k=override.get("output_cost_per_1k", pricing.output_cost_per_1k),
    )
