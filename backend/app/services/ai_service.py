import httpx

from app.core.config import settings
from app.models.schemas import ChatMessage


def _system_prompt(context_blob: str) -> str:
    return (
        "You are a portfolio assistant. Answer ONLY using the provided portfolio context.\n"
        "Rules:\n"
        "1) If the answer is not in context, say: 'I do not have that information in this portfolio.'\n"
        "2) Be concise, professional, and accurate.\n"
        "3) Do not invent metrics, employers, education, or skills.\n"
        "4) If asked for contact, provide the listed email.\n\n"
        f"Portfolio Context:\n{context_blob}"
    )


async def generate_grounded_answer(
    user_message: str,
    history: list[ChatMessage],
    context_blob: str
) -> str:
    if not settings.openrouter_api_key:
        return "OpenRouter API key is not configured."

    # Inject portfolio context as a system instruction to keep answers grounded.
    messages = [{"role": "system", "content": _system_prompt(context_blob)}]
    for item in history[-8:]:
        messages.append({"role": item.role, "content": item.content})
    messages.append({"role": "user", "content": user_message})

    payload = {"model": settings.openrouter_model, "messages": messages, "temperature": 0.2, "max_tokens": 300}

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "portfolio-ai"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"OpenRouter request failed ({response.status_code}): {response.text}") from exc

        data = response.json()
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("OpenRouter returned no choices.")
        message = choices[0].get("message", {})
        content = _extract_text_content(message.get("content"))
        if not content:
            # Some providers return plain text at top level for compatibility.
            content = _extract_text_content(choices[0].get("text"))
        if not content:
            raise RuntimeError(f"OpenRouter returned an empty response. Raw choice: {choices[0]}")
        return content


def _extract_text_content(value: object) -> str:
    if isinstance(value, str):
        return value.strip()

    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str) and text.strip():
                    parts.append(text.strip())
        return "\n".join(parts).strip()

    return ""
