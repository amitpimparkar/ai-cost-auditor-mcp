from ai_cost_auditor_mcp import estimate_task_cost, estimate_task_cost_from_text


def test_estimate_task_cost_default_model():
    result = estimate_task_cost(
        model_name="openai/gpt-3.5-turbo",
        prompt_tokens=1000,
        completion_tokens=500,
    )

    assert result["model_name"] == "openai/gpt-3.5-turbo"
    assert result["prompt_tokens"] == 1000
    assert result["completion_tokens"] == 500
    assert result["input_cost"] == 0.0015
    assert result["output_cost"] == 0.001
    assert result["total_cost"] == 0.0025


def test_estimate_task_cost_from_text():
    result = estimate_task_cost_from_text(
        model_name="openai/gpt-3.5-turbo",
        prompt_text="Hello, this is an example prompt.",
        completion_text="Hello, this is a short response.",
    )

    assert result["prompt_tokens"] > 0
    assert result["completion_tokens"] > 0
    assert result["total_cost"] > 0


def test_estimate_task_cost_with_per_million_override():
    # Example: provider publishes input/output costs per 1M tokens.
    result = estimate_task_cost(
        model_name="openai/gpt-3.5-turbo",
        prompt_tokens=1000,
        completion_tokens=1000,
        pricing_override={
            "input_cost": 1500.0,
            "input_cost_unit": "1M",
            "output_cost": 2000.0,
            "output_cost_unit": "1M",
        },
    )

    # 1500 per 1M => 1.5 per 1k, 2000 per 1M => 2.0 per 1k
    assert result["input_cost"] == 1.5
    assert result["output_cost"] == 2.0
    assert result["total_cost"] == 3.5
