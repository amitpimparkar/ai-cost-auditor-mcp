from __future__ import annotations

import re
from typing import Optional


def _load_tiktoken():
    try:
        import tiktoken  # type: ignore

        return tiktoken
    except ImportError:
        return None


def estimate_tokens(text: str, model_name: Optional[str] = None) -> int:
    """Estimate token usage for a given text string.

    If the optional `tiktoken` library is installed, it will use the
    tokenizer for the specified model. Otherwise it falls back to a
    simple whitespace-and-symbol count heuristic.
    """
    if not text:
        return 0

    tiktoken = _load_tiktoken()
    if tiktoken is not None:
        try:
            if model_name:
                encoding = tiktoken.encoding_for_model(model_name)
            else:
                encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception:
            pass

    # Fallback heuristic: split on words and punctuation.
    tokens = re.findall(r"\w+|[^	\n\s\w]", text)
    return max(1, len(tokens))


def estimate_prompt_and_completion_tokens(
    prompt_text: str,
    completion_text: str,
    model_name: Optional[str] = None,
) -> tuple[int, int]:
    """Estimate prompt and completion token counts for given texts."""
    return (
        estimate_tokens(prompt_text, model_name=model_name),
        estimate_tokens(completion_text, model_name=model_name),
    )
