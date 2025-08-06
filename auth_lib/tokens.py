import jwt
import time
import uuid
from typing import Any, Dict
from jwt import InvalidTokenError

ALGORITHM = "RS256"

def create_service_token(
    issuer: str,
    audience: str,
    private_key,
    kid: str,
    lifetime_seconds: int = 30,
    extra_claims: Dict[str, Any] | None = None,
) -> str:
    now = int(time.time())
    payload = {
        "iss": issuer,
        "sub": issuer,
        "aud": audience,
        "iat": now,
        "exp": now + lifetime_seconds,
        "jti": str(uuid.uuid4()),
    }
    if extra_claims:
        payload.update(extra_claims)

    headers = {"kid": kid}
    token = jwt.encode(payload, private_key, algorithm=ALGORITHM, headers=headers)
    return token

def verify_token(
    token: str,
    expected_audience: str,
    public_keys_map: Dict[str, Any],
    issuer_whitelist: set[str] | None = None,
) -> Dict[str, Any]:
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    if not kid or kid not in public_keys_map:
        raise InvalidTokenError("Unknown kid")

    key = public_keys_map[kid]
    payload = jwt.decode(
        token,
        key=key,
        algorithms=[ALGORITHM],
        audience=expected_audience,
        options={"require": ["exp", "iat", "iss", "aud", "jti"]},
    )
    if issuer_whitelist and payload.get("iss") not in issuer_whitelist:
        raise InvalidTokenError("Unexpected issuer")
    return payload

