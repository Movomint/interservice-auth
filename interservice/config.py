import os
from enum import Enum

CORE_API_BASE_URL = os.environ.get('CORE_API_BASE_URL', 'http://core-api:8000')
DATABASE_API_BASE_URL = os.environ.get('DATABASE_API_BASE_URL', 'http://database-api:8001')
EXTRACTION_AGENT_BASE_URL = os.environ.get('EXTRACTION_AGENT_BASE_URL', 'http://extraction-agent:8002')
MOVOTIME_BASE_URL = os.environ.get('MOVOTIME_BASE_URL', 'http://movotime:8003')
GATEWAY_BASE_URL = os.environ.get('GATEWAY_BASE_URL', 'https://gateway.movomint.com')
LOAD_PLAN_PRO_BASE_URL = os.environ.get('LOAD_PLAN_PRO_BASE_URL', '')

class Services(str, Enum):
    CORE_API = 'core-api'
    DATABASE = 'database'
    EXTRACTION_AGENT = 'extraction-agent'
    MOVOTIME = 'movotime'
    GATEWAY = 'gateway-service'
    LOAD_PLAN_PRO = 'load-plan-pro'


SERVICE_REGISTRY: dict[Services, str] = {
    Services.CORE_API: CORE_API_BASE_URL,
    Services.DATABASE: DATABASE_API_BASE_URL,
    Services.EXTRACTION_AGENT: EXTRACTION_AGENT_BASE_URL,
    Services.MOVOTIME:  MOVOTIME_BASE_URL,
    Services.GATEWAY: GATEWAY_BASE_URL,
    Services.LOAD_PLAN_PRO: LOAD_PLAN_PRO_BASE_URL
}


def get_service_url(name: Services) -> str:
    return SERVICE_REGISTRY[name]
