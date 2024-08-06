from sqlalchemy import MetaData


def merge_metadata(*chunks: MetaData) -> MetaData:
    metadata = MetaData()
    for chunk in chunks:
        for table_name, table in chunk.tables.items():
            metadata._add_table(table_name, table.schema, table)

    return metadata
