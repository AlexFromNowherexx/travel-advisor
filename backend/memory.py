from collections import defaultdict

_conversations: dict[str, list[dict[str, str]]] = defaultdict(list)


def get_history(conversation_id: str) -> list[dict[str, str]]:
    return _conversations[conversation_id]


def append_message(conversation_id: str, role: str, content: str) -> None:
    _conversations[conversation_id].append({"role": role, "content": content})
