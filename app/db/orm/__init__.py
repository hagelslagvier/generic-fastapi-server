import pathlib

from sqlalchemy import create_engine

db_path = pathlib.Path(__file__).parents[1] / "db.sqlite3"
db_url = f"sqlite:///{db_path}"

engine = create_engine(db_url)
