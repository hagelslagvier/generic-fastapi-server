from fastapi import APIRouter, Depends
from injector import Injector

from app.database.orm.models import User
from app.dependencies.auth import get_user_from_token
from app.dependencies.injector import make_injector
from app.endpoints.health.schema import HealthReport, HealthReportError, HealthStatus
from app.interactors.health_check.interfaces import HealthCheckProbeInterface

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("/")
def get(
    client: User | None = Depends(get_user_from_token),
    injector: Injector = Depends(make_injector),
) -> HealthReport | HealthReportError:
    health_check_probe = injector.get(HealthCheckProbeInterface)

    try:
        uptime = health_check_probe.get_uptime()
        cpu_usage = health_check_probe.get_cpu_usage()
        ram_usage = health_check_probe.get_ram_usage()

        return HealthReport(
            status=HealthStatus.HEALTHY,
            uptime=str(uptime),
            cpu=cpu_usage,
            ram=ram_usage,
        )

    except Exception as error:
        return HealthReportError(
            status=HealthStatus.UNHEALTHY,
            error_type=error.__class__.__name__,
            error=str(error),
        )
