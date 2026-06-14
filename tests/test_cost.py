from ai_cost_auditor_mcp import estimate_task_cost


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
