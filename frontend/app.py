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

st.set_page_config(page_title="Travel Agent", page_icon="✈️")
st.title("Travel Agent")
st.write("Type about your trip goals, and get destination, hotel, weather, and food guidance.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

st.sidebar.header("Travel Advisor Tips")
st.sidebar.write("Ask for destinations, hotels, weather, or food to trigger SerpAPI search integration when available.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your trip"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            try:
                result = send_chat_message(
                    st.session_state.api_base_url,
                    prompt,
                    st.session_state.conversation_id,
                )
                reply = result["reply"]
                st.session_state.conversation_id = result["conversation_id"]
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except ApiClientError as exc:
                st.error(f"Could not reach API: {exc}")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

st.caption("Powered by OpenAI & SerpAPI.")
