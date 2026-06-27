import uuid
from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from backend.agent import build_tour, generate_response, summarize_sources
    from backend.config import settings
    from backend.memory import append_message, get_history
    from backend.schemas import (
        ChatRequest,
        GenerateRequest,
        GenerateResponse,
        HealthResponse,
        SourceSummaryRequest,
        SourceSummaryResponse,
        TourRequest,
        TourResponse,
        TTSRequest,
    )
    from backend.tts import synthesize_wav_bytes
else:
    from .agent import build_tour, generate_response, summarize_sources
    from .config import settings
    from .memory import append_message, get_history
    from .schemas import (
        ChatRequest,
        GenerateRequest,
        GenerateResponse,
        HealthResponse,
        SourceSummaryRequest,
        SourceSummaryResponse,
        TourRequest,
        TourResponse,
        TTSRequest,
    )
    from .tts import synthesize_wav_bytes

app = FastAPI(title="Bac Bling AI Agent API", version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version=settings.app_version, service=settings.service_name)


@app.post("/api/v1/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest) -> GenerateResponse:
    conversation_id = payload.conversation_id or str(uuid.uuid4())
    history = get_history(conversation_id)

    try:
        response = generate_response(
            message=payload.message,
            history=history,
            output_type=payload.output_type,
            source_mode=payload.source_mode,
            conversation_id=conversation_id,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate reply: {exc}")

    append_message(conversation_id, "user", payload.message)
    append_message(conversation_id, "assistant", response.reply)

    return response


@app.post("/api/v1/chat", response_model=GenerateResponse)
def chat(payload: ChatRequest) -> GenerateResponse:
    return generate(payload)


@app.post("/api/v1/source-summary", response_model=SourceSummaryResponse)
def source_summary(payload: SourceSummaryRequest) -> SourceSummaryResponse:
    return summarize_sources(topic=payload.topic, source_mode=payload.source_mode)


@app.post("/api/v1/tour", response_model=TourResponse)
def tour(payload: TourRequest) -> TourResponse:
    return build_tour(
        theme=payload.theme,
        duration=payload.duration,
        audience=payload.audience,
        source_mode=payload.source_mode,
    )


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
