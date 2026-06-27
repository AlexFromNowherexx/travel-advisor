from pathlib import Path
import os
import sys
import uuid

# pyrefly: ignore [missing-import]
import streamlit as st
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

from frontend.api_client import ApiClientError, send_chat_message

OUTPUT_TYPES = {
    "Tour itinerary": "tour_itinerary",
    "Check-in recommendation": "checkin_recommendation",
    "Historical narrative": "historical_narrative",
    "Source summary": "source_summary",
    "General Q&A": "general_qa",
}
SOURCE_MODES = {
    "Strict": "strict",
    "Balanced": "balanced",
    "Exploratory": "exploratory",
}


def render_response(result: dict) -> None:
    st.markdown(result["reply"])

    details_tabs = st.tabs(["Sources", "Warnings", "Agent trace"])
    with details_tabs[0]:
        sources = result.get("sources") or []
        if sources:
            st.dataframe(sources, use_container_width=True, hide_index=True)
        else:
            st.info("No sources returned.")

    with details_tabs[1]:
        warnings = result.get("warnings") or []
        if warnings:
            for warning in warnings:
                st.warning(warning)
        else:
            st.success("No warnings returned.")

    with details_tabs[2]:
        st.write(
            {
                "output_type": result.get("output_type"),
                "intent": result.get("intent"),
                "confidence": result.get("confidence"),
                "conversation_id": result.get("conversation_id"),
                "agent_trace": result.get("agent_trace", []),
            }
        )


st.set_page_config(page_title="Bac Bling AI Agent")
st.title("Bac Bling AI Agent")
st.caption("Source-aware Bac Ninh tourism, check-in, and cultural storytelling demo.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

with st.sidebar:
    st.header("Demo controls")
    output_label = st.radio("Output type", list(OUTPUT_TYPES), index=0)
    source_label = st.radio("Source mode", list(SOURCE_MODES), index=0)
    st.divider()
    st.write("Try prompts about Quan ho, craft villages, check-in spots, source summaries, or industrial-zone route warnings.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and isinstance(msg.get("content"), dict):
            render_response(msg["content"])
        else:
            st.markdown(msg["content"])

if prompt := st.chat_input("Ask about Bac Ninh"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Coordinating the four agents..."):
            try:
                result = send_chat_message(
                    st.session_state.api_base_url,
                    prompt,
                    st.session_state.conversation_id,
                    output_type=OUTPUT_TYPES[output_label],
                    source_mode=SOURCE_MODES[source_label],
                )
                st.session_state.conversation_id = result["conversation_id"]
                render_response(result)
                st.session_state.messages.append({"role": "assistant", "content": result})
            except ApiClientError as exc:
                st.error(f"Could not reach API: {exc}")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

st.caption("MVP scope: no booking, payment, live maps, or guaranteed real-time operating data.")
