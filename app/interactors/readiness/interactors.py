import socket
from pathlib import Path
from tempfile import gettempdir

from app.interactors.readiness.interfaces import ReadinessProbeInterface


class ReadinessProbe(ReadinessProbeInterface):
    def __init__(self) -> None:
        self.file_path = Path(gettempdir()) / socket.gethostname()

    def is_ready(self) -> bool:
        return self.file_path.exists()

    def set_ready(self, ready: bool) -> None:
        if ready:
            path = str(self.file_path)
            open(path, "w")
        else:
            Path.unlink(self.file_path, missing_ok=True)
