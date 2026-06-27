from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json
import os
import sys
import uuid

# pyrefly: ignore [missing-import]
import streamlit as st
import streamlit.components.v1 as components
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

from frontend.api_client import ApiClientError, send_chat_message

DATA_DIR = PROJECT_ROOT / ".travel_advisor_data"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"


PROHIBITED_KEYWORDS = {
    "code", "lập trình", "python", "javascript", "c++", "java", "html", "css",
    "programming", "software", "developer", "viết hàm", "thuật toán", "algorithm",
    "sql", "git", "class", "function", "coding", "viết code",
}


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



def is_travel_scope_prompt(prompt: str) -> bool:
    lower_prompt = prompt.lower()
    travel_or_image_keywords = {
        "travel", "trip", "tour", "hotel", "weather", "food", "restaurant", "destination",
        "sightseeing", "landmark", "check-in", "checkin", "image", "photo", "picture",
        "ảnh", "hình", "hinh", "img", "quan họ", "quan ho", "bắc ninh", "bac ninh",
        "du lá»‹ch", "danh lam", "tháº¯ng cáº£nh",
    }
    if any(keyword in lower_prompt for keyword in travel_or_image_keywords):
        return True

    return not any(keyword in lower_prompt for keyword in PROHIBITED_KEYWORDS)


def get_recent_message(role: str) -> str:
    for message in reversed(st.session_state.messages):
        if message.get("role") == role:
            return str(message.get("content") or "")
    return ""


def infer_trip_subject() -> str:
    recent_text = f"{get_recent_message('user')} {get_recent_message('assistant')}".lower()
    candidates = [
        "Bắc Ninh",
        "Hà Nội",
        "Florence",
        "Italy",
        "Quan họ",
        "craft villages",
        "food",
        "hotel",
    ]
    for candidate in candidates:
        if candidate.lower() in recent_text:
            return candidate
    return "chuyến đi này"


def get_follow_up_suggestions() -> list[str]:
    recent_text = f"{get_recent_message('user')} {get_recent_message('assistant')}".lower()
    subject = infer_trip_subject()

    if any(keyword in recent_text for keyword in ("gia đình", "family", "trẻ em", "children")):
        return [
            f"Lịch trình {subject} nhẹ nhàng cho gia đình",
            "Nên đi khung giờ nào để đỡ mệt?",
            "Gợi ý chỗ ăn phù hợp trẻ em",
            "Rút gọn thành lịch trình nửa ngày",
        ]

    if any(keyword in recent_text for keyword in ("bạn bè", "friends", "check-in", "checkin", "ảnh", "photo")):
        return [
            f"Các điểm check-in đẹp ở {subject}",
            "Sắp xếp lịch trình theo từng khung giờ",
            "Nên đi buổi sáng hay buổi chiều?",
            "Thêm gợi ý ăn uống sau khi đi chơi",
        ]

    if any(keyword in recent_text for keyword in ("ăn", "food", "restaurant", "dining", "món")):
        return [
            f"Món nên thử nhất ở {subject}",
            "Gợi ý quán theo ngân sách vừa phải",
            "Xếp lịch ăn uống theo từng khung giờ",
            "Đi cùng nhóm bạn thì ăn ở đâu?",
        ]

    if any(keyword in recent_text for keyword in ("weather", "thời tiết", "mùa", "tháng")):
        return [
            f"Tháng nào đẹp nhất để đi {subject}?",
            "Nếu trời mưa thì nên đổi lịch thế nào?",
            "Gợi ý trang phục theo thời tiết",
            "Lịch trình trong nhà thay thế",
        ]

    if any(keyword in recent_text for keyword in ("hotel", "khách sạn", "stay", "ở đâu")):
        return [
            f"Nên ở khu nào tại {subject}?",
            "Gợi ý khách sạn theo ngân sách",
            "Lịch trình gần chỗ ở để ít di chuyển",
            "Đi cùng gia đình thì nên chọn khu nào?",
        ]

    return [
        f"Biến câu trả lời thành lịch trình ở {subject}",
        "Nên đi cùng ai thì phù hợp nhất?",
        "Sắp xếp lịch trình theo từng khung giờ",
        "Nên đi lúc nào để trải nghiệm tốt nhất?",
    ]



def scroll_chat_to_bottom() -> None:
    components.html(
        """
        <script>
        const scrollToBottom = () => {
            const doc = window.parent?.document || document;
            const candidates = [
                doc.scrollingElement,
                doc.documentElement,
                doc.body,
                ...doc.querySelectorAll('section.main, [data-testid=\"stAppViewContainer\"], [data-testid=\"stMain\"], [data-testid=\"stVerticalBlock\"], div')
            ].filter(Boolean);

            candidates.forEach((element) => {
                if (element.scrollHeight > element.clientHeight) {
                    element.scrollTop = element.scrollHeight;
                }
            });
        };
        scrollToBottom();
        window.setTimeout(scrollToBottom, 0);
        window.setTimeout(scrollToBottom, 50);
        window.setTimeout(scrollToBottom, 150);
        window.setTimeout(scrollToBottom, 350);
        window.setTimeout(scrollToBottom, 800);
        </script>
        """,
        height=0,
        width=0,
    )


def queue_follow_up_prompt(prompt: str) -> None:
    st.session_state.pending_prompt = prompt
    st.session_state.keep_chat_at_bottom = True

def render_follow_up_suggestions() -> None:
    if not st.session_state.messages:
        return
    if st.session_state.messages[-1].get("role") != "assistant":
        return

    st.markdown('<div class="followup-title">Gợi ý hỏi tiếp</div>', unsafe_allow_html=True)
    columns = st.columns(2)
    for index, suggestion in enumerate(get_follow_up_suggestions()):
        with columns[index % 2]:
            st.button(
                suggestion,
                key=f"followup_{len(st.session_state.messages)}_{index}_{st.session_state.conversation_id}",
                on_click=queue_follow_up_prompt,
                args=(suggestion,),
            )


def handle_prompt(prompt: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    persist_current_conversation()

    with st.chat_message("user"):
        st.markdown(prompt)

    if not is_travel_scope_prompt(prompt):
        with st.chat_message("assistant"):
            reply = "Yêu cầu không hợp lệ. Tôi chỉ hỗ trợ tìm hiểu về danh lam thắng cảnh và du lịch."
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            persist_current_conversation()
        return

    scroll_chat_to_bottom()

    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            try:
                result = send_chat_message(
                    st.session_state.api_base_url,
                    prompt,
                    st.session_state.conversation_id,
                )
                reply = result["reply"]
                image_html = result.get("image_html") or ""
                display_reply = f"{reply}\n\n{image_html}" if image_html else reply
                st.session_state.conversation_id = result["conversation_id"]
                st.markdown(reply)
                if image_html:
                    st.markdown(image_html, unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": display_reply})
                persist_current_conversation()
            except ApiClientError as exc:
                st.error(f"Could not reach API: {exc}")
            except Exception as exc:
                st.error(f"Unexpected error: {exc}")

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



def apply_sidebar_chat_styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background: #f7f7f8;
        }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-size: 18px !important;
            font-weight: 600 !important;
            margin-bottom: 10px !important;
        }
        [data-testid="stSidebar"] .stButton {
            margin: 0 !important;
        }
        [data-testid="stSidebar"] .stButton > button {
            display: flex !important;
            justify-content: flex-start !important;
            align-items: center !important;
            width: 100% !important;
            height: 36px !important;
            min-height: 36px !important;
            padding: 8px 10px !important;
            margin: 1px 0 !important;
            border: 0 !important;
            border-radius: 6px !important;
            background: transparent !important;
            box-shadow: none !important;
            color: #2f2f2f !important;
            font-size: 16px !important;
            font-weight: 400 !important;
            line-height: 20px !important;
            text-align: left !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: #ececec !important;
            color: #111827 !important;
        }
        [data-testid="stSidebar"] .stButton > button:focus,
        [data-testid="stSidebar"] .stButton > button:active {
            background: #e9e9e9 !important;
            border: 0 !important;
            box-shadow: none !important;
            outline: none !important;
            color: #111827 !important;
        }
        [data-testid="stSidebar"] .stButton > button p {
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            width: 100% !important;
            text-align: left !important;
        }
        [data-testid="stSidebar"] hr {
            margin: 14px 0 !important;
        }
        .followup-title {
            color: #6b7280;
            font-size: 13px;
            margin: 18px 0 8px;
        }
        div[data-testid="column"] .stButton > button {
            justify-content: flex-start !important;
            min-height: 40px !important;
            padding: 9px 12px !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 12px !important;
            background: #ffffff !important;
            color: #374151 !important;
            box-shadow: none !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            text-align: left !important;
        }
        div[data-testid="column"] .stButton > button:hover {
            background: #f7f7f8 !important;
            border-color: #d1d5db !important;
            color: #111827 !important;
        }
        div[data-testid="column"] .stButton > button p {
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            white-space: nowrap !important;
            width: 100% !important;
            text-align: left !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def hide_streamlit_deploy_button() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stToolbarActions"] > :last-child,
        [data-testid="stToolbar"] a[href*="share.streamlit.io"],
        [data-testid="stToolbar"] button[title="Deploy"],
        [data-testid="stToolbar"] button[aria-label="Deploy"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            min-width: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            overflow: hidden !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    components.html(
        """
        <script>
        const hideDeploy = () => {
            const root = window.parent?.document || document;
            const candidates = root.querySelectorAll('button, a, [role=\"button\"], [data-testid=\"stToolbarActions\"] *');
            candidates.forEach((element) => {
                const text = (element.textContent || '').trim();
                const label = element.getAttribute('aria-label') || element.getAttribute('title') || '';
                if (text === 'Deploy' || label === 'Deploy') {
                    const target = element.closest('button, a, [role=\"button\"]') || element;
                    target.style.setProperty('display', 'none', 'important');
                    target.style.setProperty('visibility', 'hidden', 'important');
                    target.style.setProperty('width', '0', 'important');
                    target.style.setProperty('min-width', '0', 'important');
                    target.style.setProperty('padding', '0', 'important');
                    target.style.setProperty('margin', '0', 'important');
                    target.style.setProperty('overflow', 'hidden', 'important');
                }
            });
        };
        hideDeploy();
        window.setInterval(hideDeploy, 300);
        </script>
        """,
        height=0,
        width=0,
    )

st.set_page_config(page_title="Travel Agent", page_icon="✈️")
hide_streamlit_deploy_button()
apply_sidebar_chat_styles()
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
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "keep_chat_at_bottom" not in st.session_state:
    st.session_state.keep_chat_at_bottom = False

with st.sidebar:
    st.header("Chats")
    if st.button("New chat", width="stretch"):
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
            button_label = label
            if st.button(button_label, key=f"chat_{conversation['id']}", width="stretch"):
                open_chat(conversation["id"])
                st.rerun()
    else:
        st.caption("No previous chats yet.")

    st.divider()
    st.header("Travel Advisor Tips")
    st.write("Ask for destinations, hotels, weather, or food to search integration when available.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=msg["role"] == "assistant")

prompt = st.chat_input("Ask about your trip")

if st.session_state.pending_prompt:
    prompt_to_send = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    handle_prompt(prompt_to_send)
    render_follow_up_suggestions()
    if st.session_state.keep_chat_at_bottom:
        st.session_state.keep_chat_at_bottom = False
        scroll_chat_to_bottom()
elif prompt:
    handle_prompt(prompt)
    render_follow_up_suggestions()
elif st.session_state.messages and st.session_state.messages[-1].get("role") == "assistant":
    render_follow_up_suggestions()

st.caption("Powered by our AI agents")
