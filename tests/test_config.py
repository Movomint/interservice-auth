from interservice.config import (
    Services,
    SERVICE_REGISTRY
)


def test_services_enum_values() -> None:
    assert Services.CORE_API.value == "core-api"
    assert Services.DATABASE.value == "database"


def test_default_registry_uses_env_defaults() -> None:
    for service in Services:
        url = SERVICE_REGISTRY[service]
        assert url.startswith("http://") or url.startswith("https://")


def test_get_service_url_reads_overrides_from_env(monkeypatch) -> None:
    monkeypatch.setenv("CORE_API_BASE_URL", "http://override:9001")
    monkeypatch.setenv("DATABASE_API_BASE_URL", "http://override:9002")

    import importlib
    import interservice.config as cfg
    importlib.reload(cfg)

    assert cfg.get_service_url(cfg.Services.CORE_API) == "http://override:9001"
    assert cfg.get_service_url(cfg.Services.DATABASE) == "http://override:9002"


