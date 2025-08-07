import time
from typing import Any, Dict

import httpx


class JWKSClient:
    """
    Fetches & caches a JWKS document.
    Each key is stored by kid for O(1) lookup.
    """

    def __init__(self, url: str, cache_ttl: int = 300):
        self.url = url
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, Any] = {}
        self._expires_at = 0

    async def _refresh(self) -> None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(self.url, timeout=5)
        resp.raise_for_status()
        jwks = resp.json()
        self._cache = {k["kid"]: k for k in jwks["keys"]}
        self._expires_at = int(time.time()) + self.cache_ttl

    async def get_keys(self) -> Dict[str, Any]:
        if time.time() >= self._expires_at:
            await self._refresh()
        return self._cache
