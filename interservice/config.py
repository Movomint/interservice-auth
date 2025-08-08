import os
from enum import Enum

EXTRACTION_AGENT_BASE_URL = os.environ.get('EXTRACTION_AGENT_BASE_URL', 'http://localhost:8001')
DATABASE_API_BASE_URL = os.environ.get('DATABASE_API_BASE_URL', 'http://localhost:8002')
LOAD_PLAN_PRO_BASE_URL = os.environ.get('LOAD_PLAN_PRO_BASE_URL', 'http://localhost:8003')

class Services(str, Enum):
    EXTRACTION_AGENT = 'extraction-agent'
    DATABASE = 'database'
    LOAD_PLAN_PRO = 'load-plan-pro'


SERVICE_REGISTRY: dict[Services, str] = {
    Services.EXTRACTION_AGENT: EXTRACTION_AGENT_BASE_URL,
    Services.DATABASE: DATABASE_API_BASE_URL,
    Services.LOAD_PLAN_PRO:  LOAD_PLAN_PRO_BASE_URL,
}


def get_service_url(name: Services) -> str:
    return SERVICE_REGISTRY[name]

