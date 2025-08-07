from fastapi import Request, HTTPException, status

from .jwks import JWKSClient
from .tokens import verify_token


def require_internal_auth(expected_audience: str, jwks_url: str):
    """
    FastAPI dependency that enforces service-to-service auth.
    Usage:

        app = FastAPI()
        guard = require_internal_auth("db-api", "https://core-api/jwks.json")

        @app.get("/records")
        async def read_records(request: Request, _=Depends(guard)):
            ...
    """
    jwks = JWKSClient(jwks_url)

    async def _guard(request: Request):
        auth = request.headers.get("authorization")
        if not auth or not auth.lower().startswith("bearer "):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing token")

        token = auth.split()[1]
        keys = await jwks.get_keys()
        verify_token(
            token=token,
            expected_audience=expected_audience,
            public_keys_map=keys,
        )

    return _guard
