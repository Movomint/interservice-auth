import httpx
import json as jsonlib
import os
from .config import Services, get_service_url
from fastapi import HTTPException
from typing import Any

_SERVICE_CLASS_REGISTRY: dict[Services, type["BaseHTTPService"]] = {}

class BaseHTTPService:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        service_name = getattr(cls, "SERVICE", None)
        if service_name is not None:
            _SERVICE_CLASS_REGISTRY[service_name] = cls

    def __init__(self, service: Services | None = None):
        service = service or getattr(self, "SERVICE", None)
        if service is None:
            raise ValueError("SERVICE must be provided on the subclass or passed to __init__")
        self.name = service.value
        self.base_url = get_service_url(service)
        self.timeout = 30
        secret = os.environ.get("INTERNAL_AUTH_SECRET")
        self._default_headers: dict[str, str] = {"X-Internal-Auth": secret} if secret else {}

    async def _call_(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
        headers: dict[str, str] | None = None,
    ) -> Any:
        url = self.base_url + "/" + path.lstrip("/")

        req_headers = dict(self._default_headers)
        if headers:
            req_headers.update(headers)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.request(
                    method.upper(), url, params=params, json=json, headers=req_headers
                )
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"{self.name} service unreachable")
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail=f"{self.name} HTTP error")

        if resp.status_code != 200:
            try:
                error = resp.json()
                detail = error["detail"] if isinstance(error, dict) and "detail" in error else error
            except (ValueError, jsonlib.JSONDecodeError):
                detail = resp.text if resp.text else f"{self.name} service returned status {resp.status_code}"
            raise HTTPException(status_code=resp.status_code, detail=detail)

        return resp.json()


def get_service_client(name: Services) -> BaseHTTPService:
    cls = _SERVICE_CLASS_REGISTRY[name]
    return cls(name)
