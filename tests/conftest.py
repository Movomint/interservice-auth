import os
import sys
from typing import Generator

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("INTERNAL_AUTH_SECRET", "test-secret")


@pytest.fixture(autouse=True)
def set_internal_auth_secret(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.setenv("INTERNAL_AUTH_SECRET", "test-secret")
    yield
