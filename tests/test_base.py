import json as _json
import pytest
from fastapi import HTTPException

from interservice.base import BaseHTTPService
from interservice.config import Services


class DummyService(BaseHTTPService):
    def __init__(self):
        super().__init__(Services.EXTRACTION_AGENT)


@pytest.mark.asyncio
async def test_api_call_success(monkeypatch):
    service = DummyService()

    class FakeResponse:
        status_code = 200

        def json(self):
            return {"ok": True}

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def request(self, method, url, params=None, json=None):
            return FakeResponse()

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout: FakeClient())
    data = await service._call_("get", "/health")
    assert data == {"ok": True}


@pytest.mark.asyncio
async def test_api_call_connect_error(monkeypatch):
    service = DummyService()

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def request(self, method, url, params=None, json=None):
            import httpx

            raise httpx.ConnectError("boom")

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout: FakeClient())

    with pytest.raises(HTTPException) as exc:
        await service._call_("get", "/health")
    assert exc.value.status_code == 503
    assert "unreachable" in exc.value.detail


@pytest.mark.asyncio
async def test_api_call_http_error(monkeypatch):
    service = DummyService()

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def request(self, method, url, params=None, json=None):
            import httpx

            raise httpx.HTTPError("boom")

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout: FakeClient())

    with pytest.raises(HTTPException) as exc:
        await service._call_("get", "/health")
    assert exc.value.status_code == 502
    assert "HTTP error" in exc.value.detail


@pytest.mark.asyncio
async def test_api_call_non_200_with_json_detail(monkeypatch):
    service = DummyService()

    class FakeResponse:
        status_code = 404

        def json(self):
            return {"detail": "not found"}

        @property
        def text(self):
            return ""

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def request(self, method, url, params=None, json=None):
            return FakeResponse()

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout: FakeClient())

    with pytest.raises(HTTPException) as exc:
        await service._call_("get", "/missing")
    assert exc.value.status_code == 404
    assert exc.value.detail == "not found"


@pytest.mark.asyncio
async def test_api_call_non_200_with_invalid_json(monkeypatch):
    service = DummyService()

    class FakeResponse:
        status_code = 500

        def json(self):
            raise ValueError("invalid json")

        @property
        def text(self):
            return "oops"

    class FakeClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def request(self, method, url, params=None, json=None):
            return FakeResponse()

    import httpx

    monkeypatch.setattr(httpx, "AsyncClient", lambda timeout: FakeClient())

    with pytest.raises(HTTPException) as exc:
        await service._call_("get", "/error")
    assert exc.value.status_code == 500
    assert exc.value.detail == "oops"


