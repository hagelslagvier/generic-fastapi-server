import psutil

from app.interactors.liveness.interfaces import LivenessProbeInterface


class LivenessProbe(LivenessProbeInterface):
    def __init__(self, cpu_limit: int, ram_limit: int) -> None:
        self.cpu_limit = cpu_limit
        self.ram_limit = ram_limit

    def is_alive(self) -> bool:
        if not 0 <= self._get_cpu_usage() <= self.cpu_limit:
            return False

        if not 0 <= self._get_ram_usage() <= self.ram_limit:
            return False

        return True

    def _get_cpu_usage(self) -> int:
        cpu_usage = psutil.cpu_percent(interval=0.25)

        return int(cpu_usage)

    def _get_ram_usage(self) -> int:
        ram_usage = psutil.virtual_memory().percent

        return int(ram_usage)
