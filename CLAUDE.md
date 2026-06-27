# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development commands

- Install dependencies: `pip install -r requirements.txt`
- Run API locally: `uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000`
- Run Streamlit UI: `streamlit run frontend/app.py`
- Run all tests: `pytest`
- Run a single test file: `pytest tests/test_chat.py`
- Run a single test: `pytest tests/test_chat.py::test_chat_contract`

## Runtime configuration

- Environment is loaded from `.env` via `backend/config.py`.
- Required Azure variables for real model calls:
  - `AZURE_OPENAI_API_KEY`
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_DEPLOYMENT`
- Optional local UI override: `API_BASE_URL` (defaults to `http://localhost:8000` in [frontend/app.py](frontend/app.py)).

## High-level architecture

This is a two-process Python app:

1. **Frontend (Streamlit)** in [frontend/app.py](frontend/app.py)
   - Stores chat transcript + `conversation_id` in `st.session_state`.
   - Sends each user message to backend using [frontend/api_client.py](frontend/api_client.py).

2. **Backend (FastAPI)** in [backend/main.py](backend/main.py)
   - Exposes `GET /health` and `POST /api/v1/chat`.
   - On each chat request:
     - Reuses or creates `conversation_id`.
     - Loads prior turns from in-memory store ([backend/memory.py](backend/memory.py)).
     - Calls agent reply generator ([backend/agent.py](backend/agent.py)).
     - Appends user + assistant turns back into memory.

3. **Agent layer** in [backend/agent.py](backend/agent.py)
   - Creates cached `AzureOpenAI` client from settings.
   - Loads and applies the skill prompt from [skills/travel-consultant/SKILL.md](skills/travel-consultant/SKILL.md) as `instructions` for `responses.create(...)`.
   - Sends full conversation history + latest user message to Azure OpenAI.

## Data/contracts

- Request/response schemas are in [backend/schemas.py](backend/schemas.py).
- `ChatRequest.message` is stripped and must be non-empty.
- Chat history is process-local only (module-level dict); restarting the API clears all conversations.

## Project constraints to keep

From [AGENTS.md](AGENTS.md):

- Keep MVP scope: travel advice only (no booking/payments/auth/live provider integrations unless specs change).
- Preserve stable API contract for `POST /api/v1/chat` and OpenAPI docs.
- Keep skill-driven behavior sourced from `skills/travel-consultant/SKILL.md`.
- Keep dependency footprint aligned with `requirements.txt` unless explicitly needed.
