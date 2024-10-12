from abc import ABC, abstractmethod
from datetime import timedelta


class HealthCheckProbeInterface(ABC):
    """
    Abstract interface for a health check probe, which provides methods
    to retrieve system health metrics such as uptime, CPU usage, and RAM usage.
    """

    @abstractmethod
    def get_uptime(self) -> timedelta:
        """
        Retrieve the system's uptime.

        Returns:
            timedelta: The duration for which the system has been running.
        """

    @abstractmethod
    def get_cpu_usage(self) -> int:
        """
        Retrieve the current CPU usage percentage.

        Returns:
            int: The CPU usage as a percentage (0-100).
        """

    @abstractmethod
    def get_ram_usage(self) -> int:
        """
        Retrieve the current RAM usage percentage.

        Returns:
            int: The RAM usage as a percentage (0-100).
        """
