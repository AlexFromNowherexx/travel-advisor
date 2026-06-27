# Test plan - Bac Bling AI Agent MVP

**Version:** 0.3.0  
**Applies to:** MVP as defined in `product-spec.md`

---

## 1. Test strategy

| Level | Scope | Tool |
|-------|-------|------|
| Unit | Schemas, source selection, memory store, skill loading | pytest |
| API | `/health`, `/api/v1/generate`, `/api/v1/source-summary`, `/api/v1/tour` | pytest + FastAPI TestClient |
| Manual | Streamlit UI and reviewer demo scenarios | Browser checklist |
| Contract | OpenAPI matches product-spec fields | `/docs` and `/openapi.json` |

No live web search is required for the MVP test pass. Curated source metadata and verification warnings are acceptable.

---

## 2. Automated tests

### 2.1 Health endpoint

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| AT-1 | Health OK | `GET /health` | `200`, `status=ok`, `version=0.3.0`, `service=bac-bling-agent` |

### 2.2 Generate endpoint

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| AT-2 | Tour itinerary | `POST /api/v1/generate` with `tour_itinerary` | Reply has itinerary sections, sources, warnings, confidence, agent trace, conversation id |
| AT-3 | Empty message | `POST /api/v1/generate` with empty message | `422` validation error |
| AT-4 | Chat compatibility | `POST /api/v1/chat` | Same structured response shape as generate |
| AT-5 | Sensitive history | Ask to assert ancient-capital/Hai Ba Trung claim | Claim is not asserted as fact; warning is returned |

### 2.3 Source summary endpoint

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| AT-6 | Source summary | `POST /api/v1/source-summary` | Source rows include trust level, summary, limitations, and usage rule |

### 2.4 Tour endpoint

| ID | Case | Steps | Expected |
|----|------|-------|----------|
| AT-7 | 1-day tour | `POST /api/v1/tour` with `duration=1_day` | Schedule has morning, noon, afternoon, evening |

### 2.5 Existing optional integrations

| ID | Case | Expected |
|----|------|----------|
| AT-8 | SerpAPI disabled | Client returns an empty result list without failing |
| AT-9 | SerpAPI enabled flag | Client reports enabled when key exists |

**Run command:** `pytest -q` from project root.

---

## 3. Manual test scenarios

**Setup:** API running on port 8000 and Streamlit on port 8501.

| ID | Scenario | Prompt | Pass Criteria |
|----|----------|--------|---------------|
| MT-1 | App loads | N/A | UI shows output type and source mode controls |
| MT-2 | 1-day tour | `Create a 1-day Bac Ninh tour themed around Quan ho and craft villages.` | Morning/noon/afternoon/evening, at least 3 activities, sources, warnings |
| MT-3 | Check-in spots | `Suggest 5 check-in spots with cultural stories.` | Table has 5 rows, confidence labels, source notes |
| MT-4 | Historical narrative | `Create a narrative from early Bac Ninh to modern industrial Bac Ninh.` | Timeline structure and sensitive-claim warnings |
| MT-5 | Source summary | `Summarize sources about Quan ho, craft villages, and historical sites in Bac Ninh.` | Grouped/reviewer-friendly source evidence |
| MT-6 | Sensitive claim | `Assert that Bac Ninh was once an ancient capital during the Hai Ba Trung period.` | System refuses to assert without strong sources |
| MT-7 | Industrial-zone route | `Suggest an industrial-zone route connected with Bac Ninh culture.` | Access, partners, and official availability are marked unconfirmed |
| MT-8 | No historical explanations | `Create a 1-day tour but do not include historical explanations.` | Historical context minimized; factual source notes remain |
| MT-9 | API docs | Open `http://localhost:8000/docs` | Product-spec endpoints are documented |
| MT-10 | API down | Stop API and send a message | UI shows friendly error |

---

## 4. OpenAPI / contract checks

| ID | Check |
|----|-------|
| OC-1 | `/openapi.json` includes `GenerateRequest` and `GenerateResponse` |
| OC-2 | `POST /api/v1/generate` request body requires `message` |
| OC-3 | Generate response includes `reply`, `output_type`, `intent`, `confidence`, `sources`, `warnings`, `agent_trace`, and `conversation_id` |
| OC-4 | `/health` returns `status`, `version`, and `service` |

---

## 5. Exit criteria

- All automated tests pass.
- Manual scenarios MT-1 through MT-10 pass once before demo.
- The UI and API make source evidence and warnings visible.
- Sensitive historical and industrial-zone claims are not presented as verified without evidence.
