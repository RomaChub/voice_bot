from sqlalchemy import Column, Integer, String, Table, MetaData


metadata = MetaData()


ValueOrm = Table(
    "values",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", String, nullable=False),
    Column("core_value", String, nullable=False),
)

