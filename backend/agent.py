from functools import lru_cache

# pyrefly: ignore [missing-import]
from openai import OpenAI

from .config import settings
from .skill_loader import load_skill
from .serpapi_client import SerpApiClientError, get_serpapi_results


SKILL_PROMPT = load_skill(settings.skill_file_path)


def _format_serpapi_context(message: str) -> str:
    lower_message = message.lower()
    if not any(keyword in lower_message for keyword in ("hotel", "stay", "destination", "city", "where", "place", "area", "weather", "food", "dining", "restaurant", "eat")):
        return ""

    try:
        results = get_serpapi_results(message)
    except SerpApiClientError:
        return ""

    if not results:
        return ""

    lines = ["Search context:"]
    for res in results:
        parts = [f"Title: {res.title}"]
        if res.snippet:
            parts.append(f"Snippet: {res.snippet}")
        if res.link:
            parts.append(f"Link: {res.link}")
        lines.append("- " + "; ".join(parts))
    return "\n".join(lines)


@lru_cache
def get_client() -> OpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    return OpenAI(
        api_key=settings.openai_api_key,
    )


def get_reply(message: str, history: list[dict[str, str]]) -> str:
    messages = [*history, {"role": "user", "content": message}]
    serpapi_context = _format_serpapi_context(message)
    if serpapi_context:
        messages.insert(-1, {"role": "system", "content": serpapi_context})

    client = get_client()
    response = client.chat.completions.create(
        model=settings.openai_model,
        messages=[{"role": "system", "content": SKILL_PROMPT}, *messages],
    )
    content = response.choices[0].message.content if response.choices else None
    return content or "I'm sorry, I couldn't generate a reply right now."
