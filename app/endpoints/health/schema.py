from pydantic import BaseModel


class HealthReport(BaseModel):
    status: str
    uptime: str
    cpu: int
    ram: int


class HealthReportError(BaseModel):
    status: str
    error_type: str
    error: str
