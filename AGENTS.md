# Agent instructions — Travel Advisor

This repo uses **spec-driven development**. Implement only what is defined in `specs/`. Update specs before changing scope.

## Project goal

Build an MVP **travel consultant AI** that helps users plan trips by recommending:

- Destinations
- Hotels
- Weather (for travel dates / location)
- Food and dining locations

## Architecture (MVP)

```
User → Streamlit UI → FastAPI (/chat) → OpenAI + travel-consultant skill
```

- **Streamlit**: chat UI, session state, calls backend over HTTP.
- **FastAPI**: single chat endpoint, OpenAPI schema, no business logic in the UI.
- **Skill file** (`skills/travel-consultant/SKILL.md`): system-style instructions for tone, safety, and recommendation categories.

## Rules for coding agents

1. **Read specs first** — `specs/product-spec.md` is the source of truth for features.
2. **Do not expand scope** — no booking, payments, multi-user accounts, or live map integrations in MVP.
3. **Keep dependencies minimal** — `fastapi`, `uvicorn`, `streamlit`, `openai`, `httpx`, `pydantic-settings` unless the implementation plan says otherwise.
4. **Secrets** — never commit API keys; use environment variables only.
5. **OpenAPI** — FastAPI must expose `/docs` and a stable `POST /api/v1/chat` contract matching the product spec.
6. **Skill usage** — load `skills/travel-consultant/SKILL.md` into the agent system prompt (or equivalent) on every request.
7. **Errors** — return clear JSON errors from the API; show a friendly message in Streamlit.
8. **Tests** — follow `specs/test-plan.md` before marking work complete.

## When implementing

1. Complete tasks in order in `specs/implementation-plan.md`.
2. Log spec changes in `specs/change-log.md`.
3. Update README “Getting started” if run commands change.

## Out of scope (unless spec is updated)

- User authentication
- Persistent chat history in a database
- Real-time hotel/weather API integrations (MVP uses model knowledge + clear disclaimers)
- Mobile-native apps
- Internationalization

## File ownership

| Area | Location |
|------|----------|
| Specs | `specs/` |
| Skill | `skills/travel-consultant/SKILL.md` |
| API | `backend/` |
| UI | `frontend/` |
