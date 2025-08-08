import os
from interservice.config import (
    Services,
    SERVICE_REGISTRY,
    get_service_url,
)


def test_services_enum_values() -> None:
    assert Services.EXTRACTION_AGENT.value == "extraction-agent"
    assert Services.DATABASE.value == "database"
    assert Services.LOAD_PLAN_PRO.value == "load-plan-pro"


def test_default_registry_uses_env_defaults() -> None:
    # No env overrides set in this test; just ensure keys exist and urls look like http(s)
    for service in Services:
        url = SERVICE_REGISTRY[service]
        assert url.startswith("http://") or url.startswith("https://")


def test_get_service_url_reads_overrides_from_env(monkeypatch) -> None:
    monkeypatch.setenv("EXTRACTION_AGENT_BASE_URL", "http://override:9001")
    monkeypatch.setenv("DATABASE_API_BASE_URL", "http://override:9002")
    monkeypatch.setenv("LOAD_PLAN_PRO_BASE_URL", "http://override:9003")

    # Re-import module to pick env up (module-level constants are evaluated at import)
    # Using importlib.reload to avoid relying on test order
    import importlib
    import interservice.config as cfg
    importlib.reload(cfg)

    assert cfg.get_service_url(cfg.Services.EXTRACTION_AGENT) == "http://override:9001"
    assert cfg.get_service_url(cfg.Services.DATABASE) == "http://override:9002"
    assert cfg.get_service_url(cfg.Services.LOAD_PLAN_PRO) == "http://override:9003"


