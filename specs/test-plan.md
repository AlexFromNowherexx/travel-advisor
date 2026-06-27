# Test plan — Voice Travel Agent MVP

**Version:** 0.2.0  
**Applies to:** MVP as defined in `product-spec.md`

---

## 1. Test strategy

| Level | Scope | Tool |
|-------|--------|------|
| Unit | Skill loader, schemas, memory store, provider adapter, SerpAPI client | pytest |
| API | `/health`, `/api/v1/chat` (mocked model + mocked SerpAPI) | pytest + httpx TestClient |
| Manual | Full UI + real provider + optional SerpAPI calls | Browser + checklist |
| Contract | OpenAPI matches implementation | FastAPI `/openapi.json` review |

No E2E browser automation required for MVP.

---

## 2. Automated tests

### 2.1 Health endpoint

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| AT-1 | Health OK | `GET /health` | `200`, body `{"status":"ok"}` |

### 2.2 Chat endpoint (mocked model)

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| AT-2 | Valid message | `POST /api/v1/chat` with `{"message":"Hello"}` | `200`, `reply` non-empty string, `conversation_id` present |
| AT-3 | Empty message | `POST` with `{"message":""}` | `422` validation error |
| AT-4 | Missing message field | `POST` with `{}` | `422` |
| AT-5 | Conversation continuity | Two posts with same `conversation_id` | Same id returned; agent receives prior context (mock asserts call count/history) |
| AT-6 | Provider failure | Mock provider to raise | `502` or `500` with `detail` message |

### 2.3 SerpAPI integration

| ID | Case | Expected |
|----|------|----------|
| AT-7 | SerpAPI client success | Returns search results |
| AT-8 | SerpAPI client failure | Falls back safely without breaking chat flow |
| AT-9 | SerpAPI request for search context | Agent includes retrieved context when available |

### 2.4 Skill loader

| ID | Case | Expected |
|----|------|----------|
| AT-10 | Skill file exists | Loader returns non-empty string containing “travel” |
| AT-11 | Skill file missing | Startup or first load raises clear error |

### 2.5 Schemas

| ID | Case | Expected |
|----|------|----------|
| AT-12 | Request/response models | Match product-spec JSON examples |

**Run command:** `pytest -q` from project root (after implementation).

---

## 3. Manual test scenarios

**Setup:** API running on port 8000, Streamlit on 8501, configured provider runtime, and SerpAPI credentials if testing enrichment.

| ID | Scenario | Steps | Pass criteria |
|----|----------|-------|----------------|
| MT-1 | App loads | Open Streamlit URL | Chat UI visible, no crash |
| MT-2 | Destination advice | Ask: “Suggest 3 cities in Italy for food and art in September” | Reply lists destinations with short rationale; SerpAPI enrichment used if available |
| MT-3 | Hotels | Follow up: “Mid-range hotels in Florence” | Hotel-style suggestions; mentions budget alignment; SerpAPI data used when available |
| MT-4 | Weather | Ask: “What’s the weather like in Florence in September?” | Weather description; disclaimer if approximate |
| MT-5 | Food | Ask: “Where should I eat in Florence?” | Food areas or restaurant types named |
| MT-6 | Clarifying questions | Ask: “I want a vacation” (vague) | Agent asks for destination/dates/budget |
| MT-7 | API docs | Open `http://localhost:8000/docs` | `POST /api/v1/chat` documented; try from Swagger |
| MT-8 | API down | Stop API, send chat message | Streamlit shows friendly error |
| MT-9 | Missing provider config | Unset provider vars, restart API | Clear error (no silent hang) |
| MT-10 | Sidebar chat history | Send a message, click New chat, then select the old chat in the left sidebar | Previous user and assistant messages are restored |
| MT-11 | Follow-up suggestions | Send a travel question, then click one suggested follow-up | The suggestion is sent as the next user message and receives an assistant answer |

Record pass/fail and date in a comment or `specs/change-log.md` when executed.

---

## 4. OpenAPI / contract checks

| ID | Check |
|----|--------|
| OC-1 | `/openapi.json` includes `ChatRequest` and `ChatResponse` (or equivalent names) |
| OC-2 | `POST /api/v1/chat` request body requires `message` |
| OC-3 | Response includes `reply` and `conversation_id` |

---

## 5. Skill content review (static)

Before release, human review of `skills/travel-consultant/SKILL.md`:

- [ ] Covers destination, hotel, weather, food
- [ ] Includes safety and “not a booking service” disclaimer
- [ ] Tone is helpful and concise
- [ ] Instructs to ask clarifying questions when needed

---

## 6. Exit criteria

MVP is test-complete when:

- All AT-* tests pass in CI or locally
- All MT-* scenarios pass once manually
- OC-* contract checks pass
- Skill review checklist complete

---

## 7. Out of scope for testing (MVP)

- Load testing
- Security penetration testing
- Cross-browser matrix (Chrome sufficient for manual runs)
