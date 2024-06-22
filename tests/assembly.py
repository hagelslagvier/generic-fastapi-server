import pathlib
from typing import Optional

from injector import Injector

from app.assembly import assemble_app, assemble_db
from app.config import Config

HERE = pathlib.Path(__file__)
DB_FILE_PATH = HERE.parent / "test_db.sqlite3"


def assemble_test_config(injector: Optional[Injector]) -> Injector:
    def make_config() -> Config:
        return Config(db_url=f"sqlite:///{DB_FILE_PATH}")

    injector = injector or Injector()
    injector.binder.bind(Config, to=make_config)

    return injector


test_root_injector = Injector()
assemble_test_config(test_root_injector)
assemble_db(test_root_injector)
assemble_app(test_root_injector)
