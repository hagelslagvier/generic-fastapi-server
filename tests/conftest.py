from collections.abc import Generator

import pytest
from sqlalchemy import Engine, MetaData
from sqlalchemy.orm import Session

from app.db.orm.crud.generic import session_factory
from app.db.orm.models import Base as ORMBase
from tests.assembly import test_root_injector
from tests.test_crud.generic_models import Base as GenericBase


def merge_metadata(*chunks: MetaData) -> MetaData:
    metadata = MetaData()
    for chunk in chunks:
        for table_name, table in chunk.tables.items():
            metadata._add_table(table_name, table.schema, table)  # noqa

    return metadata


metadata = merge_metadata(ORMBase.metadata, GenericBase.metadata)


@pytest.fixture
def engine() -> Generator[Engine, None, None]:
    engine = test_root_injector.get(Engine)
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    yield engine


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with session_factory(bind=engine) as session:
        yield session
