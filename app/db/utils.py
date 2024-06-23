from sqlalchemy import Engine

from app.assembly import root_injector
from app.db.orm.models import Base


def create_db_schema() -> None:
    engine = root_injector.get(Engine)
    Base.metadata.create_all(engine)
