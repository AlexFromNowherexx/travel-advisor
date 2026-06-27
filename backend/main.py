import uuid
from pathlib import Path
import sys
from html import escape

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from openai import APIError, OpenAIError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from backend.agent import get_reply, check_guardrails
    from backend.config import settings
    from backend.memory import append_message, get_history
    from backend.schemas import ChatRequest, ChatResponse, HealthResponse, ImageResult, TTSRequest, TTSResponse
    from backend.serpapi_client import SerpApiClientError, get_serpapi_image_results
    from backend.tts import synthesize_wav_bytes
else:
    from .agent import get_reply, check_guardrails
    from .config import settings
    from .memory import append_message, get_history
    from .schemas import ChatRequest, ChatResponse, HealthResponse, ImageResult, TTSRequest, TTSResponse
    from .serpapi_client import SerpApiClientError, get_serpapi_image_results
    from .tts import synthesize_wav_bytes

app = FastAPI(title="Voice Travel Agent API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


def _should_search_images(message: str) -> bool:
    lower_message = message.lower()
    image_keywords = (
        "image",
        "images",
        "photo",
        "photos",
        "picture",
        "pictures",
        "ảnh",
        "hình",
        "hinh",
        "check-in",
        "checkin",
        "img",
    )
    travel_search_keywords = (
        "quan họ",
        "quan ho",
        "bắc ninh",
        "bac ninh",
        "hà nội",
        "ha noi",
        "hội an",
        "hoi an",
        "đà nẵng",
        "da nang",
        "sapa",
        "sa pa",
        "huế",
        "hue",
        "hạ long",
        "ha long",
        "phú quốc",
        "phu quoc",
        "đà lạt",
        "da lat",
        "nha trang",
        "du lịch",
        "du lich",
        "danh lam",
        "thắng cảnh",
        "thang canh",
        "landmark",
        "destination",
        "tour",
    )
    return any(keyword in lower_message for keyword in image_keywords) or any(
        keyword in lower_message for keyword in travel_search_keywords
    )


def _image_query(message: str) -> str:
    query = message
    for token in (
        "search images for",
        "search image for",
        "search images",
        "search image",
        "tìm hình ảnh",
        "tim hinh anh",
        "tìm ảnh",
        "tim anh",
        "hình ảnh",
        "hinh anh",
        "ảnh",
        "img",
        "html",
        "tag",
        "search",
        "tìm",
        "tim",
    ):
        query = query.replace(token, " ")
        query = query.replace(token.title(), " ")
    query = " ".join(query.split())
    if not query:
        query = "Vietnam travel"
    return query


def _is_safe_image_url(url: str | None) -> bool:
    return bool(url and url.startswith(("http://", "https://")))


def _build_image_html(images: list[ImageResult]) -> str:
    if not images:
        return ""

    tags = []
    for image in images:
        src = image.thumbnail_url or image.image_url
        if not _is_safe_image_url(src):
            continue
        href = image.source_url if _is_safe_image_url(image.source_url) else image.image_url
        alt = escape(image.title, quote=True)
        img_tag = (
            f'<img src="{escape(src, quote=True)}" alt="{alt}" '
            'loading="lazy" style="width: 180px; height: 120px; object-fit: cover; '
            'border-radius: 8px; margin: 6px;" />'
        )
        if _is_safe_image_url(href):
            img_tag = f'<a href="{escape(href, quote=True)}" target="_blank" rel="noopener noreferrer">{img_tag}</a>'
        tags.append(img_tag)

    if not tags:
        return ""
    return '<div class="image-results">' + "".join(tags) + "</div>"


def get_image_results(message: str) -> tuple[list[ImageResult], str]:
    if not _should_search_images(message):
        return [], ""

    try:
        results = get_serpapi_image_results(_image_query(message))
    except SerpApiClientError:
        return [], ""

    images = [
        ImageResult(
            title=result.title,
            image_url=result.image_url,
            thumbnail_url=result.thumbnail_url,
            source_url=result.source_url,
        )
        for result in results
        if _is_safe_image_url(result.image_url)
    ]
    return images, _build_image_html(images)


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    conversation_id = payload.conversation_id or str(uuid.uuid4())

    if not check_guardrails(payload.message):
        return ChatResponse(
            reply="Xin lỗi, tôi chỉ có thể hỗ trợ các câu hỏi liên quan đến danh lam thắng cảnh và thông tin du lịch. Vui lòng không hỏi các chủ đề khác như lập trình hay kiến thức khác ngoài du lịch.",
            conversation_id=conversation_id
        )

    history = get_history(conversation_id)

    try:
        reply = get_reply(payload.message, history)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except (OpenAIError, APIError) as exc:
        raise HTTPException(status_code=502, detail=f"Model request failed: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate reply: {exc}")

    append_message(conversation_id, "user", payload.message)
    append_message(conversation_id, "assistant", reply)

    images, image_html = get_image_results(payload.message)

    return ChatResponse(reply=reply, conversation_id=conversation_id, images=images, image_html=image_html)


@app.post("/api/v1/tts", response_class=Response)
def tts(payload: TTSRequest) -> Response:
    try:
        audio_bytes = synthesize_wav_bytes(payload.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to synthesize speech: {exc}")

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
        headers={"Content-Disposition": 'inline; filename="reply.wav"'},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000)
