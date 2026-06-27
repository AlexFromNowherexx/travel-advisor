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


def check_guardrails(message: str) -> bool:
    """
    Checks if a user query violates the guardrail rules (e.g. asking about programming/coding).
    Returns True if the message is valid (travel/sightseeing related).
    Returns False if it is invalid.
    """
    prohibited_keywords = {
        "code", "lập trình", "python", "javascript", "c++", "java", "html", "css",
        "programming", "software", "developer", "viết hàm", "thuật toán", "algorithm",
        "sql", "git", "class", "function", "coding", "viết code"
    }
    lower_message = message.lower()
    travel_or_image_keywords = {
        "travel", "trip", "tour", "hotel", "weather", "food", "restaurant", "destination",
        "sightseeing", "landmark", "check-in", "checkin", "image", "photo", "picture",
        "ảnh", "hình", "hinh", "img", "quan họ", "quan ho", "bắc ninh", "bac ninh",
        "du lá»‹ch", "danh lam", "tháº¯ng cáº£nh",
    }
    if any(keyword in lower_message for keyword in travel_or_image_keywords):
        return True

    if any(kw in lower_message for kw in prohibited_keywords):
        return False

    try:
        client = get_client()
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict guardrail classifier. Classify if the user query is related to travel, sightseeing, "
                        "landmarks, trip planning, hotels, weather, or dining. If the query is about programming, coding, engineering, "
                        "mathematics, or anything completely unrelated to sightseeing/travel, output 'invalid'. "
                        "Otherwise, output 'valid'. Output ONLY 'valid' or 'invalid' with no other text."
                    )
                },
                {"role": "user", "content": message}
            ],
            temperature=0.0,
            max_tokens=5
        )
        result = response.choices[0].message.content.strip().lower()
        if "invalid" in result:
            return False
    except Exception:
        # Fallback to True to avoid completely blocking the user in case of connection failure
        return True
    return True
