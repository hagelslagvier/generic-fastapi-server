from pydantic import BaseModel


class LivenessStatus(BaseModel):
    is_alive: bool
