import logging

from sqlalchemy import MetaData, create_engine
from sqlalchemy_schemadisplay import create_schema_graph

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger("database.utils.introspection")


def make_erd(db_url: str, erd_path: str) -> None:
    logger.info(f"Introspecting DB with URL {db_url}...")

    engine = create_engine(db_url)

    metadata = MetaData()
    metadata.reflect(bind=engine)

    logger.info("Building ERD...")
    graph = create_schema_graph(
        engine=engine,
        metadata=metadata,
        show_datatypes=True,
        show_indexes=True,
        rankdir="BT",
        concentrate=False,
    )

    logger.info(f"Saving ERD at '{erd_path}' ...")
    graph.write_svg(erd_path)

    logger.info("Done!")
