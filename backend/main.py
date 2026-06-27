import uuid
from pathlib import Path
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from openai import APIError, OpenAIError

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from backend.agent import get_reply
    from backend.config import settings
    from backend.memory import append_message, get_history
    from backend.schemas import ChatRequest, ChatResponse, HealthResponse, TTSRequest, TTSResponse
    from backend.tts import synthesize_wav_bytes
else:
    from .agent import get_reply
    from .config import settings
    from .memory import append_message, get_history
    from .schemas import ChatRequest, ChatResponse, HealthResponse, TTSRequest, TTSResponse
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


@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    conversation_id = payload.conversation_id or str(uuid.uuid4())
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

    return ChatResponse(reply=reply, conversation_id=conversation_id)


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
