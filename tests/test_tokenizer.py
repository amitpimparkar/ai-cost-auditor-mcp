from ai_cost_auditor_mcp import estimate_prompt_and_completion_tokens, estimate_tokens


def test_estimate_tokens_simple_text():
    token_count = estimate_tokens("Hello, world!")

    assert isinstance(token_count, int)
    assert token_count >= 2


def test_estimate_prompt_and_completion_tokens():
    prompt_tokens, completion_tokens = estimate_prompt_and_completion_tokens(
        "Hello, world!",
        "This is a response.",
    )

    assert prompt_tokens >= 2
    assert completion_tokens >= 3
