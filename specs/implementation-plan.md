# Implementation plan - Bac Bling AI Agent MVP

**Prerequisite:** `specs/product-spec.md` is the source of truth. Do not add booking, payments, auth, live maps, or unsupported real-time claims unless the product spec is updated first.

**Order:** Work top to bottom. Log notable product/spec changes in `specs/change-log.md`.

---

## Phase 0 - Repository setup

| # | Task | Output |
|---|------|--------|
| 0.1 | Keep Python dependency set minimal | `requirements.txt` installable |
| 0.2 | Maintain `.env.example` with product-spec variables | Documented local config |
| 0.3 | Keep secrets out of git | API keys via environment only |

## Phase 1 - Bac Bling skill

| # | Task | Output |
|---|------|--------|
| 1.1 | Update `skills/travel-consultant/SKILL.md` for Bac Ninh tourism and source-aware storytelling | Skill matches product spec |
| 1.2 | Include four logical agents and verification rules | Orchestrator, Search, Cultural-Historical, Tourism |
| 1.3 | Include sensitive-claim and industrial-zone warnings | Hallucination guardrails |

## Phase 2 - FastAPI backend

| # | Task | Output |
|---|------|--------|
| 2.1 | `backend/config.py` - source mode, source limits, provider/search toggles | Settings from env |
| 2.2 | `backend/schemas.py` - product-spec request/response models | Stable OpenAPI contract |
| 2.3 | `backend/agent.py` - four logical agents and source/fact-check layer | Structured generation |
| 2.4 | `backend/memory.py` - in-memory conversation store | MVP continuity |
| 2.5 | `backend/main.py` - routes | `/health`, `/api/v1/generate`, `/api/v1/source-summary`, `/api/v1/tour` |
| 2.6 | Keep `/api/v1/chat` only as a compatibility alias | Older callers still work |

## Phase 3 - Streamlit frontend

| # | Task | Output |
|---|------|--------|
| 3.1 | Add text input for Bac Ninh requests | Main demo flow |
| 3.2 | Add `output_type` control | Five supported output types |
| 3.3 | Add `source_mode` control | strict/balanced/exploratory |
| 3.4 | Display answer separately from sources, warnings, and agent trace | Reviewer-friendly UI |
| 3.5 | Show friendly API errors | Clear user feedback |

## Phase 4 - Documentation

| # | Task | Output |
|---|------|--------|
| 4.1 | Update README getting-started commands | Accurate local setup |
| 4.2 | Document API endpoints and MVP limits | Demo clarity |
| 4.3 | Update changelog | Traceability |

## Phase 5 - Tests

| # | Task | Output |
|---|------|--------|
| 5.1 | Test `/health` metadata | service/version contract |
| 5.2 | Test `/api/v1/generate` | structured response contract |
| 5.3 | Test `/api/v1/source-summary` | source summary contract |
| 5.4 | Test `/api/v1/tour` | tour contract |
| 5.5 | Test sensitive claim handling | unsupported historical claims not asserted |

**Run tests:** `pytest -q`

---

## Definition of Done

- Product-spec endpoints are implemented.
- UI can generate all five output types.
- Sources, warnings, confidence, and agent trace are visible.
- Sensitive historical claims and industrial-zone route claims are guarded.
- Automated tests pass.
