from ai_cost_auditor_mcp import detect_token_waste


def test_detect_token_waste_balanced_ratio():
    result = detect_token_waste(prompt_tokens=550, completion_tokens=450)

    assert result["total_tokens"] == 1000
    assert result["prompt_ratio"] == 0.55
    assert result["completion_ratio"] == 0.45
    assert "balanced" in result["issues"][0].lower()
