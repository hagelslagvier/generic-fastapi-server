from abc import ABC, abstractmethod
from datetime import timedelta


class HealthCheckProbeInterface(ABC):
    @abstractmethod
    def get_uptime(self) -> timedelta:
        pass

    @abstractmethod
    def get_cpu_usage(self) -> int:
        pass

    @abstractmethod
    def get_ram_usage(self) -> int:
        pass
