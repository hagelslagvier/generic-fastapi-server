from datetime import datetime, timedelta

import psutil

from app.interactors.liveness.interfaces import LivenessCheckProbeInterface


class LivenessCheckProbe(LivenessCheckProbeInterface):
    def get_uptime(self) -> timedelta:
        now = datetime.now()
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = now - boot_time
        return uptime

    def get_cpu_usage(self) -> int:
        cpu_usage = psutil.cpu_percent(interval=0.05)
        return int(cpu_usage)

    def get_ram_usage(self) -> int:
        ram_usage = psutil.virtual_memory().percent
        return int(ram_usage)
