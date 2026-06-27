from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
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
from frontend.auth import authenticate, register_user

DATA_DIR = PROJECT_ROOT / ".travel_advisor_data"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"


st.set_page_config(page_title="Travel Agent", page_icon="✈️")

def initialize_auth_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = None
        return

    if not st.session_state.authenticated:
        st.session_state.user_email = None
    elif "user_email" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = None


initialize_auth_state()


def render_login_form() -> None:
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Mật khẩu", type="password", key="login_password")
        submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
        if submitted:
            ok, message = authenticate(email, password)
            if ok:
                st.session_state.authenticated = True
                st.session_state.user_email = email.strip().lower()
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def render_register_form() -> None:
    with st.form("register_form", clear_on_submit=False):
        email = st.text_input("Email", key="register_email")
        password = st.text_input(
            "Mật khẩu (tối thiểu 8 ký tự, có chữ và số)",
            type="password",
            key="register_password",
        )
        confirm = st.text_input(
            "Nhập lại mật khẩu",
            type="password",
            key="register_confirm",
        )
        submitted = st.form_submit_button("Đăng ký", use_container_width=True)
        if submitted:
            ok, message = register_user(email, password, confirm)
            if ok:
                st.success(message)
            else:
                st.error(message)


def render_auth_screen() -> None:
    st.title("✈️ Travel Agent")
    st.caption("Đăng nhập để bắt đầu khám phá chuyến đi của bạn.")
    login_tab, register_tab = st.tabs(["Đăng nhập", "Đăng ký"])
    with login_tab:
        render_login_form()
    with register_tab:
        render_register_form()


def logout() -> None:
    for key in [
        "messages",
        "conversation_id",
        "conversations",
        "login_email",
        "login_password",
        "register_email",
        "register_password",
        "register_confirm",
    ]:
        st.session_state.pop(key, None)
    st.session_state.authenticated = False
    st.session_state.user_email = None


def load_conversations() -> dict[str, dict]:
    if not CONVERSATIONS_FILE.exists():
        return {}
    try:
        data = json.loads(CONVERSATIONS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def save_conversations(conversations: dict[str, dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONVERSATIONS_FILE.write_text(
        json.dumps(conversations, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def make_title(message: str) -> str:
    clean = " ".join(message.split())
    if not clean:
        return "New chat"
    return clean[:42] + ("..." if len(clean) > 42 else "")


def persist_current_conversation() -> None:
    conversation_id = st.session_state.conversation_id
    messages = st.session_state.messages
    if not messages:
        return

    conversations = st.session_state.conversations
    existing = conversations.get(conversation_id, {})
    first_user_message = next(
        (msg["content"] for msg in messages if msg.get("role") == "user"),
        "New chat",
    )
    conversations[conversation_id] = {
        "id": conversation_id,
        "title": existing.get("title") or make_title(first_user_message),
        "messages": messages,
        "created_at": existing.get("created_at") or datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    save_conversations(conversations)


def start_new_chat() -> None:
    persist_current_conversation()
    st.session_state.conversation_id = str(uuid.uuid4())
    st.session_state.messages = []


def open_chat(conversation_id: str) -> None:
    persist_current_conversation()
    conversation = st.session_state.conversations.get(conversation_id)
    if not conversation:
        return
    st.session_state.conversation_id = conversation_id
    st.session_state.messages = list(conversation.get("messages", []))


def render_chat_screen() -> None:
    st.title("Travel Agent")
    st.write("Type about your trip goals, and get destination, hotel, weather, and food guidance.")

    if "conversations" not in st.session_state:
        st.session_state.conversations = load_conversations()
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    if "api_base_url" not in st.session_state:
        st.session_state.api_base_url = os.getenv("API_BASE_URL", "http://localhost:8000")

    with st.sidebar:
        st.caption(f"Đang đăng nhập: **{st.session_state.user_email}**")
        if st.button("Đăng xuất", use_container_width=True):
            logout()
            st.rerun()
        st.divider()
        st.header("Chats")
        if st.button("New chat", use_container_width=True):
            start_new_chat()
            st.rerun()

        conversations = sorted(
            st.session_state.conversations.values(),
            key=lambda item: item.get("updated_at", ""),
            reverse=True,
        )

        if conversations:
            for conversation in conversations:
                label = conversation.get("title") or "Untitled chat"
                is_current = conversation.get("id") == st.session_state.conversation_id
                button_label = f"✓ {label}" if is_current else label
                if st.button(button_label, key=f"chat_{conversation['id']}", use_container_width=True):
                    open_chat(conversation["id"])
                    st.rerun()
        else:
            st.caption("No previous chats yet.")

        st.divider()
        st.header("Travel Advisor Tips")
        st.write("Ask for destinations, hotels, weather, or food to search integration when available.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about your trip"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        persist_current_conversation()

        with st.chat_message("user"):
            st.markdown(prompt)

        prohibited_keywords = {
            "code", "lập trình", "python", "javascript", "c++", "java", "html", "css",
            "programming", "software", "developer", "viết hàm", "thuật toán", "algorithm",
            "sql", "git", "class", "function", "coding", "viết code",
        }
        lower_prompt = prompt.lower()
        if any(kw in lower_prompt for kw in prohibited_keywords):
            with st.chat_message("assistant"):
                reply = "Yêu cầu không hợp lệ. Tôi chỉ hỗ trợ tìm hiểu về danh lam thắng cảnh và du lịch."
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                persist_current_conversation()
        else:
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
                        persist_current_conversation()
                    except ApiClientError as exc:
                        st.error(f"Could not reach API: {exc}")
                    except Exception as exc:
                        st.error(f"Unexpected error: {exc}")

    st.caption("Powered by OpenAI & SerpAPI.")


if not st.session_state.authenticated:
    render_auth_screen()
else:
    render_chat_screen()
