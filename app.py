import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import logging

app = FastAPI(title="AI Cost Auditor MCP Bridge")

logger = logging.getLogger("uvicorn.error")

@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Minimal MCP-like handler: expects JSON with `input.text` or `text`.

    This adapts inputs to your library function `estimate_task_cost_from_text`
    and returns a JSON response. Adjust mapping to match your real MCP schema.
    """
    body = await request.json()

    # Accept several common shapes
    text = None
    if isinstance(body, dict):
        # common MCP shapes
        text = (body.get("input", {}) or {}).get("text")
        if not text:
            text = body.get("text") or body.get("prompt") or body.get("query")

    if not text:
        return JSONResponse({"error": "no text provided"}, status_code=400)

    try:
        # import inside handler to ensure package is installed in runtime
        from ai_cost_auditor_mcp import estimate_task_cost_from_text

        result = estimate_task_cost_from_text(text)

        return {"result": result}
    except Exception as e:
        logger.exception("handler error")
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
