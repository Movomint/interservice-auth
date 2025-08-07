from .tokens import create_service_token


def auth_header(
    *,
    audience: str,
    issuer: str,
    kid: str,
    private_key: str | bytes,
) -> dict[str, str]:
    """Convenience helper for client requests."""
    token = create_service_token(
        issuer=issuer,
        audience=audience,
        private_key=private_key,
        kid=kid,
    )
    return {"Authorization": f"Bearer {token}"}
