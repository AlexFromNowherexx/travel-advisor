from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints


OutputType = Literal[
    "tour_itinerary",
    "checkin_recommendation",
    "historical_narrative",
    "source_summary",
    "general_qa",
]
SourceMode = Literal["strict", "balanced", "exploratory"]
Confidence = Literal["high", "medium", "low", "not_enough_evidence"]


class SourceMetadata(BaseModel):
    title: str
    url: str | None = None
    file_name: str | None = None
    source_type: str
    trust_level: str
    used_for: str
    accessed_at: str | None = None


class GenerateRequest(BaseModel):
    message: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    output_type: OutputType = "general_qa"
    source_mode: SourceMode = "strict"
    conversation_id: str | None = None


class GenerateResponse(BaseModel):
    reply: str
    output_type: OutputType
    intent: OutputType
    confidence: Confidence
    sources: list[SourceMetadata] = []
    warnings: list[str] = []
    agent_trace: list[str] = []
    conversation_id: str


class SourceSummaryRequest(BaseModel):
    topic: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    source_mode: SourceMode = "strict"


class SourceSummaryItem(BaseModel):
    title: str
    source_type: str
    trust_level: str
    summary: str
    limitations: str
    usage_rule: str
    url: str | None = None
    file_name: str | None = None


class SourceSummaryResponse(BaseModel):
    topic: str
    sources: list[SourceSummaryItem]
    not_enough_evidence: list[str] = []


class TourRequest(BaseModel):
    theme: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    duration: Literal["half_day", "1_day", "2_days"] = "1_day"
    audience: str = "culture-oriented travelers"
    source_mode: SourceMode = "strict"


class TourResponse(BaseModel):
    tour_name: str
    duration: Literal["half_day", "1_day", "2_days"]
    schedule: dict[str, list[str]]
    sources: list[SourceMetadata] = []
    warnings: list[str] = []


class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


class ChatRequest(GenerateRequest):
    pass


class ChatResponse(GenerateResponse):
    pass


class TTSRequest(BaseModel):
    text: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class TTSResponse(BaseModel):
    content_type: str = "audio/wav"
    filename: str = "reply.wav"
    size_bytes: int
    sample_rate: int | None = None
