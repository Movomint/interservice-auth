import os
from enum import Enum

CORE_API_BASE_URL = os.environ.get('CORE_API_BASE_URL', 'http://core-api:8000')
DATABASE_API_BASE_URL = os.environ.get('DATABASE_API_BASE_URL', 'http://database-api:8001')
AGENT_PLATFORM_BASE_URL = os.environ.get('AGENT_PLATFORM_BASE_URL', 'http://agent-platform:8002')
INTERNAL_API_BASE_URL = os.environ.get('INTERNAL_API_BASE_URL', 'http://internal-api:8005')

class Services(str, Enum):
    CORE_API = 'core-api'
    AGENT_PLATFORM = 'agent-platform'
    DATABASE = 'database'
    INTERNAL_API = 'internal-api'

SERVICE_REGISTRY: dict[Services, str] = {
    Services.CORE_API: CORE_API_BASE_URL,
    Services.DATABASE: DATABASE_API_BASE_URL,
    Services.AGENT_PLATFORM: AGENT_PLATFORM_BASE_URL,
    Services.INTERNAL_API: INTERNAL_API_BASE_URL
}


def get_service_url(name: Services) -> str:
    return SERVICE_REGISTRY[name]
