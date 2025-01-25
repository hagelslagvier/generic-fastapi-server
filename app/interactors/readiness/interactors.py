import socket

from inzicht import GenericCRUD, session_factory
from sqlalchemy import Engine

from app.database.orm.models import ReadinessStatus
from app.interactors.readiness.interfaces import ReadinessProbeInterface


class ReadinessStatusCRUD(GenericCRUD[ReadinessStatus]):
    pass


class ReadinessProbe(ReadinessProbeInterface):
    def __init__(self, bind: Engine, hostname: str = "") -> None:
        self.engine = bind
        self.hostname = hostname or socket.gethostname()

    def is_ready(self) -> bool:
        with session_factory(bind=self.engine) as session:
            items = ReadinessStatusCRUD(session=session).read_many(
                where=ReadinessStatus.hostname == self.hostname
            )
            found = list(items)
            if len(found) == 1:
                [probe] = found
                return probe.ready
            else:
                return False

    def set_ready(self, ready: bool) -> None:
        with session_factory(bind=self.engine) as session:
            items = ReadinessStatusCRUD(session=session).read_many(
                where=ReadinessStatus.hostname == self.hostname
            )
            found = list(items)
            if len(found) == 0:
                ReadinessStatusCRUD(session=session).create(
                    payload={"ready": ready, "hostname": self.hostname}
                )
            else:  # since unique constraint
                [probe] = found
                probe.ready = ready
