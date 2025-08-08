import jwt
import pytest
from fastapi import HTTPException

from interservice.auth import verify_internal_token


def _make_token(payload: dict) -> str:
    secret = "test-secret"
    return jwt.encode(payload, secret, algorithm="HS256")


def test_verify_internal_token_accepts_valid_bearer() -> None:
    token = _make_token({"sub": "service-a"})
    payload = verify_internal_token(authorization=f"Bearer {token}")
    assert payload["sub"] == "service-a"


@pytest.mark.parametrize(
    "header",
    [
        "",  # empty
        "Bearer ",  # missing token
        "Token abc",  # wrong scheme
    ],
)
def test_verify_internal_token_rejects_bad_header(header: str) -> None:
    with pytest.raises(HTTPException) as exc:
        verify_internal_token(authorization=header)
    assert exc.value.status_code == 401


def test_verify_internal_token_rejects_bad_token() -> None:
    with pytest.raises(HTTPException) as exc:
        verify_internal_token(authorization="Bearer not-a-jwt")
    assert exc.value.status_code == 403


