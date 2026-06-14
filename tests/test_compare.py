from ai_cost_auditor_mcp import compare_model_cost


def test_compare_model_cost_orders_by_total_cost():
    models = [
        "openai/gpt-4.1",
        "openai/gpt-3.5-turbo",
        "anthropic/claude-2.1",
    ]

    results = compare_model_cost(models, prompt_tokens=500, completion_tokens=500)

    assert len(results) == 3
    assert results[0]["total_cost"] <= results[1]["total_cost"]
    assert results[1]["total_cost"] <= results[2]["total_cost"]
    assert {item["model_name"] for item in results} == {
        "openai/gpt-4.1",
        "openai/gpt-3.5-turbo",
        "anthropic/claude-2.1",
    }
