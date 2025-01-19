from enum import StrEnum

from pydantic import BaseModel


class HealthStatus(StrEnum):
    HEALTHY = "HEALTHY"
    READY = "READY"
    UNHEALTHY = "UNHEALTHY"


class HealthReport(BaseModel):
    status: HealthStatus
    uptime: str
    cpu: int
    ram: int


class HealthReportError(BaseModel):
    status: HealthStatus
    error_type: str
    error: str
