from pathlib import Path


def load_skill(skill_file_path: str) -> str:
    path = Path(skill_file_path)
    if not path.is_absolute():
        path = Path(__file__).resolve().parents[1] / path
    if not path.exists():
        raise FileNotFoundError(f"Skill file not found: {path}")
    return path.read_text(encoding="utf-8")
