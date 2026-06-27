from frontend import auth


def test_register_and_authenticate_user(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "USERS_FILE", tmp_path / "users.json")

    ok, message = auth.register_user("Demo@Example.com", "Password123", "Password123")
    assert ok, message

    ok, message = auth.authenticate("demo@example.com", "Password123")
    assert ok, message


def test_authenticate_rejects_wrong_password(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "USERS_FILE", tmp_path / "users.json")
    auth.register_user("demo@example.com", "Password123", "Password123")

    ok, message = auth.authenticate("demo@example.com", "bad-password")

    assert not ok
    assert "không đúng" in message


def test_register_requires_strong_password(tmp_path, monkeypatch):
    monkeypatch.setattr(auth, "USERS_FILE", tmp_path / "users.json")

    ok, message = auth.register_user("demo@example.com", "short", "short")

    assert not ok
    assert "ít nhất 8" in message
