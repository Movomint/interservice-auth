import time
import uuid
from typing import Any, Dict, Mapping

import jwt
from jwt import InvalidTokenError

ALGORITHM = "RS256"
_OPTIONS = {"require": ["exp", "iat", "nbf", "iss", "aud", "jti"]}


def create_service_token(
    *,
    issuer: str,
    audience: str,
    private_key: str | bytes,
    kid: str,
    lifetime_seconds: int = 30,
    not_before_skew: int = 5,
    extra_claims: Dict[str, Any] | None = None,
) -> str:
    """Mint a short-lived JWT signed with the service’s private RSA key."""
    now = int(time.time())
    payload: Dict[str, Any] = {
        "iss": issuer,
        "sub": issuer,  
        "aud": audience,
        "iat": now,
        "nbf": now - not_before_skew,
        "exp": now + lifetime_seconds,
        "jti": str(uuid.uuid4()),
        **(extra_claims or {}),
    }
    headers = {"kid": kid}
    return jwt.encode(payload, private_key, algorithm=ALGORITHM, headers=headers)


def verify_token(
    *,
    token: str,
    expected_audience: str,
    public_keys_map: Mapping[str, str | bytes],
    issuer_whitelist: set[str] | None = None,
    leeway: int = 30,
) -> Dict[str, Any]:
    """Validate a JWT using the matching public key from `public_keys_map`."""
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")
    if not kid or kid not in public_keys_map:
        raise InvalidTokenError("Unknown or missing kid")

    payload = jwt.decode(
        token,
        key=public_keys_map[kid],
        algorithms=[ALGORITHM],
        audience=expected_audience,
        options=_OPTIONS,
        leeway=leeway,
    )
    if issuer_whitelist and payload.get("iss") not in issuer_whitelist:
        raise InvalidTokenError("Unexpected issuer")

    return payload
