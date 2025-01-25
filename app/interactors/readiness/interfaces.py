from abc import ABC, abstractmethod


class ReadinessProbeInterface(ABC):
    """
    Defines the interface for implementing a readiness probe.
    """

    @abstractmethod
    def is_ready(self) -> bool:
        """
        Checks if the service or application is ready to handle requests.

        Returns:
            bool: True if the system is ready, False otherwise.
        """

    @abstractmethod
    def set_ready(self, ready: bool) -> None:
        """
        Set the readiness state of the service or application.

        Args:
            ready (bool): The desired readiness state. True for ready, False for not ready.
        """
