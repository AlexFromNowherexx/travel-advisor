# Manual test guide — Voice Travel Agent MVP

**Version:** 0.2.0  
**Applies to:** Voice Travel Agent MVP

This file describes how to manually validate the app after implementation.

---

## 1. Goal

Confirm that the Streamlit UI, FastAPI backend, model provider, and SerpAPI enrichment work together for a basic voice-first travel flow.

---

## 2. Prerequisites

Before testing, make sure:

- Python dependencies are installed.
- `.env` is configured with the provider and SerpAPI settings.
- The backend is running on `http://localhost:8000`.
- The Streamlit app is running on `http://localhost:8501`.
- Ollama is running locally if you are testing the Ollama path.
- SerpAPI credentials are available if you want to verify hotel/destination enrichment.

---

## 3. Start the app

In separate terminals:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
streamlit run frontend/app.py
```

---

## 4. What to verify

### 4.1 App loads

- Open the Streamlit URL.
- Confirm the title and instructions are visible.
- Confirm the chat area loads without errors.

### 4.2 Basic chat flow

- Type a travel question such as:
  - `Suggest 3 cities in Italy for food and art in September`
- Confirm the reply is readable and relevant.
- Confirm the conversation stays in session.

### 4.3 Destination recommendations

- Ask for destination suggestions.
- Confirm the response includes a clear recommendation and short rationale.
- If SerpAPI data is available, confirm it influences the answer.

### 4.4 Hotel recommendations

- Ask for mid-range hotels in a city.
- Confirm the response includes hotel-style suggestions.
- Confirm the response respects budget and style.
- If SerpAPI data is available, confirm it is used.

### 4.5 Clarifying questions

- Send a vague request such as:
  - `I want a vacation`
- Confirm the agent asks for missing details like destination, dates, or budget.

### 4.6 Error handling

- Stop the backend and send a message.
- Confirm the UI shows a friendly error.
- Restart the backend and confirm the app works again.

### 4.7 Voice-first behavior

- If voice input is implemented, record or submit an audio sample.
- Confirm the transcript appears correctly.
- Confirm the assistant response can be displayed and/or played back.
- If voice is unavailable, confirm text fallback still works.

---

## 5. Sample pass/fail checklist

| Check | Pass | Notes |
|------|------|------|
| Streamlit UI loads | [ ] |  |
| Backend health endpoint works | [ ] |  |
| SerpAPI-enhanced destination response works | [ ] |  |
| SerpAPI-enhanced hotel response works | [ ] |  |
| Clarifying question behavior works | [ ] |  |
| API error is handled cleanly | [ ] |  |
| Voice flow works or text fallback is present | [ ] |  |

---

## 6. Suggested test notes to record

Record the following after each manual test run:

- Date
- Provider used (`qwen` or `ollama`)
- Whether SerpAPI enrichment was enabled
- What worked
- What failed
- Any response quality issues

---

## 7. Expected result

The app should complete a full travel Q&A flow without crashing, and it should respond gracefully if the provider or SerpAPI data is unavailable.
