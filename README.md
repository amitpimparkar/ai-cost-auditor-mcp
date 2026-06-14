# AI Cost Auditor MCP

A reusable Python package for estimating LLM task cost, comparing model costs across providers, and detecting token waste patterns.

## Features

- `estimate_task_cost()` for per-task cost breakdowns
- `compare_model_cost()` to rank model cost estimates
- `detect_token_waste()` to identify inefficient prompt/output token usage
- Built with eight reference models across OpenAI, Gemini, Mistral, and Anthropic

## Supported models

- OpenAI: `openai/gpt-4.1`, `openai/gpt-3.5-turbo`
- Gemini: `gemini/gemini-pro`, `gemini/gemini-1.5-pro`
- Mistral: `mistral/mistral-large`, `mistral/mistral-small`
- Anthropic: `anthropic/claude-3.5`, `anthropic/claude-2.1`

## Installation

```bash
pip install .
```

## Usage

```python
from ai_cost_auditor_mcp import (
    estimate_task_cost,
    estimate_task_cost_from_text,
    compare_model_cost,
    detect_token_waste,
    estimate_tokens,
)

cost = estimate_task_cost(
    model_name="openai/gpt-4.1",
    prompt_tokens=1200,
    completion_tokens=400,
)
print(cost)

comparison = compare_model_cost(
    [
        "openai/gpt-4.1",
        "openai/gpt-3.5-turbo",
        "gemini/gemini-pro",
        "anthropic/claude-3.5",
    ],
    prompt_tokens=1200,
    completion_tokens=400,
)
print(comparison)

waste = detect_token_waste(prompt_tokens=1200, completion_tokens=400)
print(waste)
```

## Dynamic text-based token estimation

```python
from ai_cost_auditor_mcp import estimate_task_cost_from_text, estimate_tokens

prompt = "Summarize the report and give three recommendations."
response = "Here are three recommendations..."

prompt_tokens = estimate_tokens(prompt, model_name="openai/gpt-4.1")
completion_tokens = estimate_tokens(response, model_name="openai/gpt-4.1")

cost = estimate_task_cost(
    model_name="openai/gpt-4.1",
    prompt_tokens=prompt_tokens,
    completion_tokens=completion_tokens,
)
print(cost)

# Or use the helper that accepts raw text directly:
cost_from_text = estimate_task_cost_from_text(
    model_name="openai/gpt-4.1",
    prompt_text=prompt,
    completion_text=response,
)
print(cost_from_text)
```

## Custom pricing

Pricing rules are stored in the package defaults, but developers can override values at runtime.
The override supports both per-1k and per-1M units by providing unit metadata.

```python
custom_cost = estimate_task_cost(
    model_name="openai/gpt-4.1",
    prompt_tokens=1200,
    completion_tokens=400,
    pricing_override={
        "input_cost": 3500.0,
        "input_cost_unit": "1M",
        "output_cost": 4200.0,
        "output_cost_unit": "1M",
    },
)
```

## Testing

```bash
pip install pytest
pytest -q
```
