# Usage Guide

## Importing the package

```python
from ai_cost_auditor_mcp import estimate_task_cost, compare_model_cost, detect_token_waste
```

## Estimating task cost

```python
cost = estimate_task_cost(
    model_name="openai/gpt-4.1",
    prompt_tokens=1500,
    completion_tokens=300,
)
print(cost)
```

## Comparing multiple models

```python
comparison = compare_model_cost(
    [
        "openai/gpt-4.1",
        "openai/gpt-3.5-turbo",
        "gemini/gemini-pro",
        "anthropic/claude-3.5",
    ],
    prompt_tokens=1500,
    completion_tokens=300,
)
```

## Detecting token waste

```python
waste = detect_token_waste(prompt_tokens=1500, completion_tokens=300)
print(waste)
```

## Override pricing

Developers can pass a custom pricing override to adapt to newer published costs without changing package code.

```python
estimate_task_cost(
    model_name="openai/gpt-4.1",
    prompt_tokens=1500,
    completion_tokens=300,
    pricing_override={"input_cost_per_1k": 0.0035, "output_cost_per_1k": 0.0045},
)
```
