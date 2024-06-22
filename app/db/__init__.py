import pathlib

from sqlalchemy import create_engine

HERE = pathlib.Path(__file__)

DB_PATH = HERE.parent / "db.sqlite3"

engine = create_engine(url=f"sqlite:////{DB_PATH}")

if __name__ == "__main__":
    from app.db.orm.models import Base

    def create_db_schema() -> None:
        Base.metadata.create_all(engine)

    create_db_schema()
