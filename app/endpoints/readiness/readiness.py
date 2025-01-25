from fastapi import APIRouter, Depends
from injector import Injector

from app.database.orm.models import User
from app.dependencies.auth import get_user_from_token
from app.dependencies.injector import make_injector
from app.endpoints.readiness.schema import ReadinessStatus
from app.interactors.readiness.interfaces import ReadinessProbeInterface

router = APIRouter(
    prefix="/readiness",
    tags=["readiness"],
)


@router.get("/")
def get(
    client: User | None = Depends(get_user_from_token),
    injector: Injector = Depends(make_injector),
) -> ReadinessStatus:
    readiness_probe = injector.get(ReadinessProbeInterface)
    readiness_status = ReadinessStatus(is_ready=readiness_probe.is_ready())

    return readiness_status
