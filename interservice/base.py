import httpx
from .config import Services, get_service_url
from fastapi import HTTPException
from typing import Any

_SERVICE_CLASS_REGISTRY: dict[Services, type["BaseHTTPService"]] = {}

def register_service(name: Services):
    def deco(cls):
        _SERVICE_CLASS_REGISTRY[name] = cls
        return cls
    return deco

class BaseHTTPService:
    def __init__(self, service: Services):
        self.name = service.value  
        self.base_url = get_service_url(service)
        self.timeout = 30

    async def api_call(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        url = self.base_url + "/" + path.lstrip("/")
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.request(method.upper(), url, params=params, json=json)
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"{self.name} service unreachable")
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail=f"{self.name} HTTP error")

        if resp.status_code != 200:
            try:
                error = resp.json()
                detail = error["detail"] if isinstance(error, dict) and "detail" in error else error
            except (ValueError, json.JSONDecodeError):
                # Handle cases where response is not valid JSON
                detail = resp.text if resp.text else f"{self.name} service returned status {resp.status_code}"
            
            raise HTTPException(
                status_code=resp.status_code,
                detail=detail
            )
       
        return resp.json()

