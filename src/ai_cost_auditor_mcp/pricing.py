from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Union


@dataclass(frozen=True)
class ModelPricing:
    provider: str
    model_name: str
    input_cost_per_1k: float
    output_cost_per_1k: float

    def format(self) -> str:
        return f"{self.provider}/{self.model_name}: input ${self.input_cost_per_1k:.6f}/1k, output ${self.output_cost_per_1k:.6f}/1k"

    @staticmethod
    def normalize_cost(cost: float, cost_unit: str) -> float:
        """Convert pricing values to a normalized per-1k-token basis."""
        unit = cost_unit.strip().lower()
        if unit in {"1k", "k", "1000"}:
            return cost
        if unit in {"1m", "m", "1000000", "million"}:
            return cost / 1000.0
        if unit in {"1", "token", "per token"}:
            # Convert cost per single token to cost per 1k tokens
            return cost * 1000.0
        raise ValueError(
            f"Unsupported cost unit '{cost_unit}'. Use '1k', '1M', or 'token'."
        )

    @classmethod
    def from_costs(
        cls,
        provider: str,
        model_name: str,
        input_cost: float,
        output_cost: float,
        input_cost_unit: str = "1k",
        output_cost_unit: str = "1k",
    ) -> "ModelPricing":
        """Create ModelPricing by normalizing input and output cost units."""
        return cls(
            provider=provider,
            model_name=model_name,
            input_cost_per_1k=cls.normalize_cost(input_cost, input_cost_unit),
            output_cost_per_1k=cls.normalize_cost(output_cost, output_cost_unit),
        )


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


def get_model_pricing(model_name: str, override: Optional[Dict[str, object]] = None) -> ModelPricing:
    """Return pricing metadata for a known model, optionally applying overrides.

    Args:
        model_name: A canonical model key such as "openai/gpt-4.1".
        override: Optional pricing overrides for input and output cost.
            The override dictionary can provide:
                - input_cost_per_1k
                - output_cost_per_1k
                - input_cost_unit
                - output_cost_unit
            or combination values with explicit cost units.

    Raises:
        KeyError: If the model is not listed in DEFAULT_MODEL_PRICING.
    """
    normalized = model_name.strip().lower()
    pricing = DEFAULT_MODEL_PRICING[normalized]

    if override is None:
        return pricing

    input_cost = override.get(
        "input_cost_per_1k",
        override.get("input_cost", pricing.input_cost_per_1k),
    )
    output_cost = override.get(
        "output_cost_per_1k",
        override.get("output_cost", pricing.output_cost_per_1k),
    )
    input_cost_unit = override.get("input_cost_unit", "1k")
    output_cost_unit = override.get("output_cost_unit", "1k")

    # If values are already expressed per 1k tokens, keep them as-is.
    if override.get("input_cost_per_1k") is not None:
        normalized_input_cost = input_cost
    else:
        normalized_input_cost = ModelPricing.normalize_cost(input_cost, input_cost_unit)

    if override.get("output_cost_per_1k") is not None:
        normalized_output_cost = output_cost
    else:
        normalized_output_cost = ModelPricing.normalize_cost(output_cost, output_cost_unit)

    return ModelPricing(
        provider=pricing.provider,
        model_name=pricing.model_name,
        input_cost_per_1k=normalized_input_cost,
        output_cost_per_1k=normalized_output_cost,
    )
