from pydantic import BaseModel


class ReadinessStatus(BaseModel):
    is_ready: bool
