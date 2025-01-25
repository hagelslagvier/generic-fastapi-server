from abc import ABC, abstractmethod


class LivenessProbeInterface(ABC):
    """
    Defines the interface for implementing a liveness probe.
    """

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Check if the service or application is alive and functioning.

        Returns:
            bool: True if the system is alive, False otherwise.
        """
