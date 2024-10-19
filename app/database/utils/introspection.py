import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph

ROOT_PATH = Path(__file__).parents[3]
ENV_BASE_PATH = ROOT_PATH / ".env.base"
ENV_PRODUCTION = ROOT_PATH / ".env"
ENV_DEVELOPMENT_PATH = ROOT_PATH / ".env.development"

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger("ERD")

for path in [
    ENV_BASE_PATH,  # dev + prod
    ENV_DEVELOPMENT_PATH,  # dev only
    ENV_PRODUCTION,  # prod only (see Dockerfile: COPY .env.production .env)
]:
    if path.exists() and path.is_file():
        load_dotenv(path)

DATABASE_URL = os.environ["DB_URL"]
ERD_PATH = ROOT_PATH / "ERD.svg"


def make_erd(db_url: str = DATABASE_URL, erd_path: str = str(ERD_PATH)) -> None:
    logger.info(f"Introspecting DB with URL {db_url} ...")

    engine = create_engine(db_url)

    metadata = MetaData()
    metadata.reflect(bind=engine)

    logger.info("Building ERD ...")
    graph = create_schema_graph(
        engine=engine,
        metadata=metadata,
        show_datatypes=True,
        show_indexes=True,
        rankdir="BT",
        concentrate=False,
    )

    logger.info(f"Saving ERD at {erd_path} ...")
    graph.write_svg(str(ERD_PATH))

    logger.info("Done!")


if __name__ == "__main__":
    make_erd()
