from enum import StrEnum

from pydantic import BaseModel


class LivenessStatus(StrEnum):
    HEALTHY = "HEALTHY"
    READY = "READY"
    UNHEALTHY = "UNHEALTHY"


class LivenessReport(BaseModel):
    status: LivenessStatus
    uptime: str
    cpu: int
    ram: int


class LivenessReportError(BaseModel):
    status: LivenessStatus
    error_type: str
    error: str
