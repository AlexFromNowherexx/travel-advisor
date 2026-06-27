import httpx


class ApiClientError(RuntimeError):
    pass


def _extract_error_message(response: httpx.Response, exc: Exception) -> str:
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict):
        detail = payload.get("detail")
        if detail:
            return str(detail)

    text = response.text.strip()
    if text:
        return text

    return str(exc)


def send_chat_message(
    api_base_url: str,
    message: str,
    conversation_id: str | None = None,
    output_type: str = "tour_itinerary",
    source_mode: str = "strict",
) -> dict:
    payload = {
        "message": message,
        "conversation_id": conversation_id,
        "output_type": output_type,
        "source_mode": source_mode,
    }
    response = httpx.post(f"{api_base_url}/api/v1/generate", json=payload, timeout=30)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ApiClientError(_extract_error_message(response, exc)) from exc
    return response.json()


def request_tts_audio(api_base_url: str, text: str) -> bytes:
    response = httpx.post(f"{api_base_url}/api/v1/tts", json={"text": text}, timeout=30)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise ApiClientError(_extract_error_message(response, exc)) from exc
    return response.content
