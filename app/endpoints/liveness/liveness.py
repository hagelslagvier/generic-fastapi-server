from fastapi import APIRouter, Depends
from injector import Injector

from app.dependencies.injector import make_injector
from app.endpoints.liveness.schema import LivenessStatus
from app.interactors.liveness.interfaces import LivenessProbeInterface

router = APIRouter(
    prefix="/liveness",
    tags=["liveness"],
)


@router.get("/")
def get(
    injector: Injector = Depends(make_injector),
) -> LivenessStatus:
    liveness_probe = injector.get(LivenessProbeInterface)
    liveness_status = LivenessStatus(is_alive=liveness_probe.is_alive())

    return liveness_status
