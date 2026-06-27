from typing import Annotated

from pydantic import BaseModel, StringConstraints


class ChatRequest(BaseModel):
    message: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    conversation_id: str | None = None


class ImageResult(BaseModel):
    title: str
    image_url: str
    thumbnail_url: str | None = None
    source_url: str | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    images: list[ImageResult] = []
    image_html: str = ""


class HealthResponse(BaseModel):
    status: str


class TTSRequest(BaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class TTSResponse(BaseModel):
    content_type: str = "audio/wav"
    filename: str = "reply.wav"
    size_bytes: int
    sample_rate: int | None = None
